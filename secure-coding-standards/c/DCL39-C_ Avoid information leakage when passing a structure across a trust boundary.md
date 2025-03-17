The C Standard, 6.7.3.2, discusses the layout of structure fields. It specifies that non-bit-field members are aligned in an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) manner and that there may be padding within or at the end of a structure. Furthermore, initializing the members of the structure does not guarantee initialization of the padding bytes. The C Standard, 6.2.6.1, paragraph 6 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> When a value is stored in an object of structure or union type, including in a member object, the bytes of the object representation that correspond to any padding bytes take unspecified values (e.g. structure and union assignment may or may not copy any padding bits). 

Additionally, the storage units in which a bit-field resides may also have padding bits. For an object with automatic storage duration, these padding bits do not take on specific values and can contribute to leaking sensitive information.
When passing a pointer to a structure across a trust boundary to a different trusted domain, the programmer must ensure that the padding bytes and bit-field storage unit padding bits of such a structure do not contain sensitive information.
## Noncompliant Code Example
This noncompliant code example runs in kernel space and copies data from `arg` to user space. However, padding bytes may be used within the structure, for example, to ensure the proper alignment of the structure members. These padding bytes may contain sensitive information, which may then be leaked when the data is copied to user space.
``` c
#include <stddef.h>
struct test {
  int a;
  char b;
  int c;
};
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = {.a = 1, .b = 2, .c = 3};
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
## Noncompliant Code Example (`memset()`)
The padding bytes can be explicitly initialized by calling `memset()`:
``` c
#include <string.h>
struct test {
  int a;
  char b;
  int c;
};
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg;
  /* Set all bytes (including padding bytes) to zero */
  memset(&arg, 0, sizeof(arg));
  arg.a = 1;
  arg.b = 2;
  arg.c = 3;
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
However, a conforming compiler is free to implement `arg.b = 2` by setting the low-order bits of a register to 2, leaving the high-order bits unchanged and containing sensitive information. Then the platform copies all register bits into memory, leaving sensitive information in the padding bits. Consequently, this implementation could leak the high-order bits from the register to a user.
## Compliant Solution
This compliant solution serializes the structure data before copying it to an untrusted context:
``` java
#include <stddef.h>
#include <string.h>
struct test {
  int a;
  char b;
  int c;
};
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = {.a = 1, .b = 2, .c = 3};
  /* May be larger than strictly needed */
  unsigned char buf[sizeof(arg)];
  size_t offset = 0;
  memcpy(buf + offset, &arg.a, sizeof(arg.a));
  offset += sizeof(arg.a);
  memcpy(buf + offset, &arg.b, sizeof(arg.b));
  offset += sizeof(arg.b);
  memcpy(buf + offset, &arg.c, sizeof(arg.c));
  offset += sizeof(arg.c);
  /* Set all remaining bytes to zero */
  memset(buf + offset, 0, sizeof(arg) - offset);
  copy_to_user(usr_buf, buf, offset /* size of info copied */);
} 
```
This code ensures that no uninitialized padding bytes are copied to unprivileged users. **Important:** The structure copied to user space is now a packed structure and the `copy_to_user()` function (or other eventual user) would need to unpack it to recreate the original padded structure.
## Compliant Solution (Padding Bytes)
Padding bytes can be explicitly declared as fields within the structure. This solution is not portable, however, because it depends on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) and target memory architecture. The following solution is specific to the x86-32 architecture:
``` java
#include <assert.h>
#include <stddef.h>
struct test {
  int a;
  char b;
  char padding_1, padding_2, padding_3;
  int c;
};
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  /* Ensure c is the next byte after the last padding byte */
  static_assert(offsetof(struct test, c) ==
                offsetof(struct test, padding_3) + 1,
                "Structure contains intermediate padding");
  /* Ensure there is no trailing padding */
  static_assert(sizeof(struct test) ==
                offsetof(struct test, c) + sizeof(int),
                "Structure contains trailing padding");
  struct test arg = {.a = 1, .b = 2, .c = 3};
  arg.padding_1 = 0;
  arg.padding_2 = 0;
  arg.padding_3 = 0;
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
The C Standard `static_assert()` macro accepts a constant expression and an [error message](BB.-Definitions_87152273.html#BB.Definitions-error). The expression is evaluated at compile time and, if false, the compilation is terminated and the error message is output. (See [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression) for more details.) The explicit insertion of the padding bytes into the `struct` should ensure that no additional padding bytes are added by the compiler and consequently both static assertions should be true. However, it is necessary to validate these assumptions to ensure that the solution is correct for a particular implementation.
## Compliant Solution (Structure Packing—GCC)
GCC allows specifying declaration attributes using the keyword `__attribute__((__packed__))`. When this attribute is present, the compiler will not add padding bytes for memory alignment unless an explicit alignment specifier for a structure member requires the introduction of padding bytes.
``` java
#include <stddef.h>
struct test {
  int a;
  char b;
  int c;
} __attribute__((__packed__));
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = {.a = 1, .b = 2, .c = 3};
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
## Compliant Solution (Structure Packing—Microsoft Visual Studio)
Microsoft Visual Studio  supports `#pragma pack()` to suppress padding bytes \[[MSDN](http://msdn.microsoft.com/en-us/library/2e70t5y1(v=vs.110).aspx)\]. The compiler adds padding bytes for memory alignment, depending on the current packing mode, but still honors the alignment specified by `__declspec(align())`. In this compliant solution, the packing mode is set to 1 in an attempt to ensure all fields are given adjacent offsets:
``` java
#include <stddef.h>
#pragma pack(push, 1) /* 1 byte */
struct test {
  int a;
  char b;
  int c;
};
#pragma pack(pop)
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = {1, 2, 3};
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
The `pack` pragma takes effect at the first `struct` declaration after the pragma is seen.
## Noncompliant Code Example
This noncompliant code example also runs in kernel space and copies data from `struct test` to user space. However, padding bits will be used within the structure due to the bit-field member lengths not adding up to the number of bits in an unsigned object. Further, there is an unnamed bit-field that causes no further bit-fields to be packed into the same storage unit. These padding bits may contain sensitive information, which may then be leaked when the data is copied to user space. For instance, the uninitialized bits may contain a sensitive kernel space pointer value that can be trivially reconstructed by an attacker in user space.
``` c
#include <stddef.h>
struct test {
  unsigned a : 1;
  unsigned : 0;
  unsigned b : 4;
};
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = { .a = 1, .b = 10 };
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
## Compliant Solution
Padding bits can be explicitly declared, allowing the programmer to specify the value of those bits. When explicitly declaring all of the padding bits, any unnamed bit-fields of length `0` must be removed from the structure because the explicit padding bits ensure that no further bit-fields will be packed into the same storage unit.
``` java
#include <assert.h>
#include <limits.h>
#include <stddef.h>
struct test {
  unsigned a : 1;
  unsigned padding1 : sizeof(unsigned) * CHAR_BIT - 1;
  unsigned b : 4;
  unsigned padding2 : sizeof(unsigned) * CHAR_BIT - 4;
};
/* Ensure that we have added the correct number of padding bits. */
static_assert(sizeof(struct test) == sizeof(unsigned) * 2,
              "Incorrect number of padding bits for type: unsigned");
/* Safely copy bytes to user space */
extern int copy_to_user(void *dest, void *src, size_t size);
void do_stuff(void *usr_buf) {
  struct test arg = { .a = 1, .padding1 = 0, .b = 10, .padding2 = 0 };
  copy_to_user(usr_buf, &arg, sizeof(arg));
}
```
This solution is not portable, however, because it depends on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) and target memory architecture. The explicit insertion of padding bits into the `struct` should ensure that no additional padding bits are added by the compiler. However, it is still necessary to validate these assumptions to ensure that the solution is correct for a particular implementation. For instance, the DEC Alpha is an example of a 64-bit architecture with 32-bit integers that allocates 64 bits to a storage unit.
In addition, this solution assumes that there are no integer padding bits in an `unsigned int`.  The portable version of the width calculation from [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions) cannot be used because the bit-field width must be an integer constant expression.
From this situation, it can be seen that special care must be taken because no solution to the bit-field padding issue will be 100% portable.
 Risk Assessment
Padding units might contain sensitive data because the C Standard allows any padding to take unspecified values. A pointer to such a structure could be passed to other functions, causing information leakage.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL39-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | function-argument-with-padding | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL39 | Detects composite structures with padding, in particular those passed to trust boundary routines. |
| CodeSonar | 8.3p0 | MISC.PADDING.POTB | Padding Passed Across a Trust Boundary |
| Cppcheck Premium | 24.11.0
 | premium-cert-dcl39-c |  |
| Helix QAC | 2024.4 | DF4941, DF4942, DF4943 | Fully implemented |
| Klocwork | 2024.4 | PORTING.STORAGE.STRUCT
 | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL39-a | A pointer to a structure should not be passed to a function that can copy data to the user space |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL39-C | Checks for information leak via structure padding; |
| RuleChecker | 24.04 | function-argument-with-padding | Partially checked |

### Related Vulnerabilities
Numerous vulnerabilities in the Linux Kernel have resulted from violations of this rule. [CVE-2010-4083](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-4083) describes a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in which the `semctl()` system call allows unprivileged users to read uninitialized kernel stack memory because various fields of a `semid_ds struct` declared on the stack are not altered or zeroed before being copied back to the user.
[CVE-2010-3881](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-3881) describes a vulnerability in which structure padding and reserved fields in certain data structures in `QEMU-KVM` were not initialized properly before being copied to user space. A privileged host user with access to `/dev/kvm` could use this [flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) to leak kernel stack memory to user space.
[CVE-2010-3477](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2010-3477) describes a kernel information leak in `act_police` where incorrectly initialized structures in the traffic-control dump code may allow the disclosure of kernel memory to user space applications.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL39-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL03-C. Use a static assertion to test the value of a constant expression | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.2.6.1, "General"6.7.3.2, "Structure and Union Specifiers" |
| [Graff 2003] |  |
| [Sun 1993] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152410) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151998)
## Comments:

|  |
| ----|
| Curiously the linux kernel appears to be trying the memset approach dispite;the problem that assignments to fields after the zero initialization may leak sensitive information into padding.  They recently added this gcc plugin https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=c61f13eaa1ee17728c41370100d2d45c254ce76f which automatically zero initializes structs that may be copied to user space.  On the other hand there may be cases where fields may only be assigned to for certain values being returned to userspace perhaps something like the socket structs where this may not fix all problems but does provide useful defense in depth.
                                        Posted by tbsaunde at May 11, 2017 03:12
                                     |
| In case of TrustZone execution memset() is private and no one can set padding bytes. So it'll be a compliant solution.; 
                                        Posted by vlad at Apr 11, 2018 15:43
                                     |
| On one hand, it would be good for the Linux kernel to comply with this rule, especially as it runs on different hardware platforms, and it has been found vulnerable in the past, as noted in this rule.On the other hand, platform-independent compliance yields slower code, mainly because it ignores or disables several compiler optimizations. Also IIUC the kernel has GCC extensions built specifically for it, so they have more control over how their C code is interpreted than the average developer. Which means this rule is out of their scope, as their compiler could make several non-standard guarantees.
                                        Posted by svoboda at Apr 16, 2018 10:58
                                     |
| I wonder if the first compliant solution which discusses serialization is complete.It basically does;struct test arg = {.a = 1, .b = 2, .c = 3};  copies the members to an array without padding, but as mentioned earlier in the article, a could still contain sensitive information.
                                        Posted by abjoshi at Aug 12, 2018 05:26
                                     |
| In the 1st compliant solution, clearly no sensitive info is copied *into* the arg array. However, if the struct has any padding bits, the array is not filled completely...some uninitialized bytes will remain at the end. I tweaked that code example by zeroing out the remaining bytes.
                                        Posted by svoboda at Aug 15, 2018 09:04
                                     |
| I think this change is a bit too restrictive:However, a C11-compliant compiler is free to implement;arg.b = 2 It's not compliance, it's conformance, and this isn't a C11 thing. I'd say "a conforming compiler" instead.
                                        Posted by aballman at Aug 15, 2018 09:05
                                     |
| Agreed, changed.
                                        Posted by svoboda at Aug 15, 2018 09:09
                                     |
| a question on the description on CS(structure packing;– GCC).GCC allows specifying declaration attributes using the keyword __attribute__((__packed__)). When this attribute is present, the compiler will not add padding bytes for memory alignment unless otherwise required by the _Alignas alignment specifier, and ...
I'm confused at the phrase "... unless otherwise required ...", which was originally added on version 40.Could it be rewritten to the following?GCC allows specifying declaration attributes using the keyword __attribute__((__packed__)). When this attribute is present, the compiler will not add padding bytes for memory alignment.Even with this attribute present on the structure itself, you can align some members inside the structure with _Alignas specifier.
If this phrase has no important meaning, just removing this part makes the paragraph more understandable, I think...
                                        Posted by yozo at Oct 17, 2018 07:24
                                     |
| I think that reformulation downplays the problem. What the "unless otherwise required" was intended to convey is that packing the structure can still produce padding bits when the members have specific alignment requirements. Perhaps:GCC allows specifying declaration attributes using the keyword __attribute__((__packed__)). When this attribute is present, the compiler will not add padding bytes for memory alignment unless an explicit alignment specifier for a structure member requires introducing padding.
                                        Posted by aballman at Oct 17, 2018 10:06
                                     |
| I've adopted;Aaron's wording, which is clearer than the original, while still retaining the meaning. We wish to convey the fact that alignment trumps the GCC packed attribute when considering padding bytes.
                                        Posted by svoboda at Oct 17, 2018 14:35
                                     |
| Aaron, David, thanks!; The revised description is more easy-to-understand to translate to japanese (-:Here is a code to examine the compiler behavior with clang (Mac OS X).I confirmed that _Alignas adds a padding to the packed struct, as explained.
MacBook$ cat choi.c
#include <stdio.h>
struct {
  char c;
  int i;
} st0;
struct {
  char c;
  int i;
} __attribute__((__packed__)) st1;
struct {
  char c;
  _Alignas(int) int i;
} __attribute__((__packed__)) st2;
int main(int argc, char* argv[]){
  printf("sizeof char: %lu  sizeof int: %lu\n", sizeof(char), sizeof(int));
  printf("sizeof st0: %lu  sizeof st1: %lu  sizeof st2: %lu\n",
         sizeof st0, sizeof st1, sizeof st2);
  printf("st0.c: %p  st0.i: %p\n", &(st0.c), &(st0.i));
  printf("st1.c: %p  st1.i: %p\n", &(st1.c), &(st1.i));
  printf("st2.c: %p  st2.i: %p\n", &(st2.c), &(st2.i));
}
MacBook$ make choi
cc     choi.c   -o choi
choi.c:23:48: warning: taking address of packed member 'i' of class or structure '(anonymous)'
      may result in an unaligned pointer value [-Waddress-of-packed-member]
  printf("st1.c: %p  st1.i: %p\n", &(st1.c), &(st1.i));
                                               ^~~~~
1 warning generated.
MacBook$ ./choi
sizeof char: 1  sizeof int: 4
sizeof st0: 8  sizeof st1: 5  sizeof st2: 8
st0.c: 0x109b3f018  st0.i: 0x109b3f01c
st1.c: 0x109b3f020  st1.i: 0x109b3f021
st2.c: 0x109b3f028  st2.i: 0x109b3f02c
MacBook$ 

![](images/icons/contenttypes/comment_16.png) Posted by yozo at Oct 21, 2018 12:11
\| \|
First compliant solution use both "buf" and "buff" as local buffer identifier for "do_stuff" function, leading to code not able to compile.
![](images/icons/contenttypes/comment_16.png) Posted by obinnert at Apr 09, 2021 04:42
\| \|
Fixed, thanks
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 09, 2021 08:05
\|
