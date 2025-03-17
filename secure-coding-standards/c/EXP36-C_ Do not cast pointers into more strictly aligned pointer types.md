Do not convert a pointer value to a pointer type that is more strictly aligned than the referenced type. Different alignments are possible for different types of objects. If the type-checking system is overridden by an explicit cast or the pointer is converted to a void pointer (`void *`) and then to a different type, the alignment of an object may be changed.
The C Standard, 6.3.2.3, paragraph 7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> A pointer to an object type may be converted to a pointer to a different object type. If the resulting pointer is not correctly aligned for the referenced type, the behavior is undefined.

See [undefined behavior 24.](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_24)
If the misaligned pointer is dereferenced, the program may [terminate abnormally](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination). On some architectures, the cast alone may cause a loss of information even if the value is not dereferenced if the types involved have differing alignment requirements.
## Noncompliant Code Example
In this noncompliant example, the `char` pointer `&c` is converted to the more strictly aligned `int` pointer `ip`. On some [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation), `cp` will not match `&c`. As a result, if a pointer to one object type is converted to a pointer to a different object type, the second object type must not require stricter alignment than the first.
``` c
#include <assert.h>
void func(void) {
  char c = 'x';
  int *ip = (int *)&c; /* This can lose information */
  char *cp = (char *)ip;
  /* Will fail on some conforming implementations */
  assert(cp == &c);
}
```
## Compliant Solution (Intermediate Object)
In this compliant solution, the `char` value is stored into an object of type `int` so that the pointer's value will be properly aligned:
``` c
#include <assert.h>
void func(void) {
  char c = 'x';
  int i = c;
  int *ip = &i;
  assert(ip == &i);
}
```
## Noncompliant Code Example
The C Standard allows any object pointer to be cast to and from `void *`. As a result, it is possible to silently convert from one pointer type to another without the compiler diagnosing the problem by storing or casting a pointer to `void *` and then storing or casting it to the final type. In this noncompliant code example, `loop_function()` is passed the char pointer `char_ptr` but returns an object of type `int` pointer:
``` c
int *loop_function(void *v_pointer) {
  /* ... */
  return v_pointer;
}
void func(char *char_ptr) {
  int *int_ptr = loop_function(char_ptr);
  /* ... */
}
```
This example compiles without warning using GCC 4.8 on Ubuntu Linux 14.04. However, `int_pointer` can be more strictly aligned than an object of type `char *`.
## Compliant Solution
Because the input parameter directly influences the return value, and `loop_function()` returns an object of type `int *`, the formal parameter `v_pointer` is redeclared to accept only an object of type `int *`:
``` c
int *loop_function(int *v_pointer) {
  /* ... */
  return v_pointer;
}
void func(int *loop_ptr) {
  int *int_ptr = loop_function(loop_ptr);
  /* ... */
}
```
## Noncompliant Code Example
Some architectures require that pointers are correctly aligned when accessing objects larger than a byte. However, it is common in system code that unaligned data (for example, the network stacks) must be copied to a properly aligned memory location, such as in this noncompliant code example:
``` c
#include <string.h>
struct foo_header {
  int len;
  /* ... */
};
void func(char *data, size_t offset) {
  struct foo_header *tmp;
  struct foo_header header;
  tmp = (struct foo_header *)(data + offset);
  memcpy(&header, tmp, sizeof(header));
  /* ... */
}
```
Assigning an unaligned value to a pointer that references a type that needs to be aligned is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). An [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) may notice, for example, that `tmp` and `header` must be aligned and use an inline `memcpy()` that uses instructions that assume aligned data.
## Compliant Solution
This compliant solution avoids the use of the `foo_header` pointer:
``` c
#include <string.h>
struct foo_header {
  int len;
  /* ... */
};
void func(char *data, size_t offset) {
  struct foo_header header; 
  memcpy(&header, data + offset, sizeof(header));
  /* ... */
}
```
## Exceptions
**EXP36-C-EX1:** Some hardware architectures have relaxed requirements with regard to pointer alignment. Using a pointer that is not properly aligned is correctly handled by the architecture, although there might be a performance penalty. On such an architecture, improper pointer alignment is permitted but remains an efficiency problem.
The x86 32- and 64-bit architectures usually impose only a performance penalty for violations of this rule, but under some circumstances, noncompliant code can still exhibit undefined behavior. Consider the following program:
``` c
#include <stdio.h>
#include <stdint.h>
#define READ_UINT16(ptr)       (*(uint16_t *)(ptr))
#define WRITE_UINT16(ptr, val) (*(uint16_t *)(ptr) = (val))
void compute(unsigned char *b1, unsigned char *b2,
             int value, int range) {
  int i;
  for (i = 0; i < range; i++) {
    int newval = (int)READ_UINT16(b1) + value;
    WRITE_UINT16(b2, newval);
    b1 += 2;
    b2 += 2;
  }
}
int main() {
  unsigned char buffer1[1024];
  unsigned char buffer2[1024];
  printf("Compute something\n");
  compute(buffer1 + 3, buffer2 + 1, 42, 500);
  return 0;
}
```
This code tries to read short ints (which are 16 bits long) from odd pairs in a character array, which violates this rule. On 32- and 64-bit x86 platforms, this program should run to completion without incident. However, the program aborts with a SIGSEGV due to the unaligned reads on a 64-bit platform running Debian Linux, when compiled with GCC 4.9.4 using the flags  `-O3`   or  `-O2 -ftree-loop-vectorize -fvect-cost-model`.
If a developer wishes to violate this rule and use undefined behavior, they must not only ensure that the hardware guarantees the behavior of the object code, but they must also ensure that their compiler, along with its optimizer, also respect these guarantees.
**EXP36-C-EX2**: If a pointer is known to be correctly aligned to the target type, then a cast to that type is permitted. There are several cases where a pointer is known to be correctly aligned to the target type. The pointer could point to an object declared with a suitable alignment specifier. It could point to an object returned by `aligned_alloc()`, `calloc()`, `malloc()`, or `realloc()`, as per the C standard, section 7.24.3, paragraph 1  \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\].
This compliant solution uses the alignment specifier, which is new to C11, to declare the `char` object `c` with the same alignment as that of an object of type `int`. As a result, the two pointers reference equally aligned pointer types:
``` c
#include <stdalign.h>
#include <assert.h>
void func(void) {
  /* Align c to the alignment of an int */
  alignas(int) char c = 'x';
  int *ip = (int *)&c; 
  char *cp = (char *)ip;
  /* Both cp and &c point to equally aligned objects */
  assert(cp == &c);
}
```
## Risk Assessment
Accessing a pointer or an object that is not properly aligned can cause a program to crash or give erroneous information, or it can cause slow pointer accesses (if the architecture allows misaligned accesses).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP36-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-cast-alignment | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP36 |  |
| CodeSonar | 8.3p0 | LANG.CAST.PC.OBJLANG.CAST.PC.VBASE | Cast: object pointersCast: virtual base to derived |
| Compass/ROSE |  |  | Can detect violations of this rule. However, it does not flag explicit casts to void * and then back to another pointer type |
| Coverity | 2017.07 | MISRA C 2004 Rule 11.4MISRA C 2012 Rule 11.1MISRA C 2012 Rule 11.2MISRA C 2012 Rule 11.5MISRA C 2012 Rule 11.7 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-exp36-c |  |
| ECLAIR | 1.2 | CC2.EXP36 | Fully implemented |
| EDG |  |  |  |
| GCC | 4.3.5 |  | Can detect some violations of this rule when the -Wcast-align flag is used |
| Helix QAC | 2024.4 | C0326, C3305C++3033, C++3038 |  |
| Klocwork | ;2024.4 | MISRA.CAST.OBJ_PTR_TO_OBJ_PTR.2012 |  |
| LDRA tool suite | 9.7.1 | 94 S, 606 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP36-a | Do not cast pointers into more strictly aligned pointer types |
| PC-lint Plus | 1.4 | 2445 | Partially supported: reports casts directly from a pointer to a less strictly aligned type to a pointer to a more strictly aligned type |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP36-C | Checks for source buffer misaligned with destination buffer (rule fully covered) |
| PVS-Studio | 7.35 | V548, V641,;V1032
 |  |
| RuleChecker | 24.04 | pointer-cast-alignment | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP36-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | VOID EXP56-CPP. Do not cast pointers into more strictly aligned pointer types | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Converting pointer values to more strictly aligned pointer types [alignconv] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 11.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 11.2 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 11.5 (advisory) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 11.7 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Bryant 2003] |  |
| [ISO/IEC 9899:2024] | 6.3.2.3, "Pointers" |
| [Walfridsson 2003] | Aliasing, Pointer Casts and GCC 3.3 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152058) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152099)
## Comments:

|  |
| ----|
| I am not sure if it can be tabulated as shown in "Implementation details" and especially the phrase "Common alignments" .
Unlike ARM and MIPS - IA-32 is forgiving when it comes to data alignment. i.e if a 32bit data; is not aligned on 4 byte boundary it can cause an exception -undefined behavior in MIPS and ARM based architecture; whereas in IA-32 world the 32bit data will be fetched (but the performance would not be the best). For the best performance align the data such that  32bit data is at an address that is a multiple of 4, 16bit data 's address is a multiple of 2 and so on ... 8bit data can go at any address.
When the compiler flag for alignment is used - each structure member after the first is stored  on either the size of the member type or n-byte  boundaries (where n is 1, 2, 4, 8, or 16),  whichever is smaller.
The "Implementation detail"  has to cover the compiler flag for alignment and the *natural* alignment.
 The "Risk Assessment" is OK, whereas the section "Implementation Details" has to be revisited.
                                        Posted by abhi at Mar 08, 2008 04:17
                                     |
| It may make sense here to just eliminate the section on "Implementation details".
The goal of this document is to provide appropriate guidance for all C99-compliant implementations.  The implementation details are mainly of value, I think, to highlight specific implementations that manifest the problem, sort of as "proof" the problem is real.
                                        Posted by rcs at Mar 08, 2008 08:36
                                     |
| Is the subject line too stringent, or the body not qualified enough?; There are two places (related) where the real issue is 'be cautious about converting a pointer to a loosely aligned type into a more strictly aligned type (and then dereferencing it)'.
Both involve memory allocation - the first case is 'void *' returned by memory allocators such as malloc(), for which of course it is OK to convert from the ... non-aligned? ... void * to any other type since the pointer returned is guaranteed to be sufficiently well aligned for any normal use.
The second case deals with legacy code (APIs) that pre-date C89 which use(d) 'char *' as the universal pointer instead of 'void *'.  When working with such code, you may be compelled to convert the 'char *' into (say) a 'long *'; as long as the caller provided a pointer that was correctly aligned in the first place, converting that to 'char *' and then back to 'long *' is safe.
I also learned to program in C on a machine where the 'char *' address for a given memory location was not the same bit value as the 'anything else pointer' address to the same memory location - a word-oriented architecture.  It was crucial to get all the functions (malloc() et al - this was the pre-ISO C days, early 80s) declared because if the compiler got to think that the function returned an 'int', it would be incorrectly interpreted.  Damn good for discipline.  (The machine was an ICL Perq - and it was a micro-programmable machine with good graphics.)
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 22:59
                                     |
| Is there any good reason to convert between different pointer types in general? (never mind alignment). Most pointer casts I have seen are either to/from void*, or to/from char* (for programmers that predate void*)  Maybe I'm just dense, but I'll not be the first or last to ask this question...we should at least have a compliant code example that illustrates proper pointer typecasting (that doesn't need void*).
                                        Posted by svoboda at Apr 17, 2008 10:24
                                     |
| this page has a neat example for when this would be necessary:
qsort(), which takes a void * and a int(*compar)(const void *, const void *) compare function... the compare function must cast from void * to some data * in order to carry out the comparison
our rule applies since you should not mix and match say a compare on int with a sort on char
                                        Posted by avolkovi at May 16, 2008 13:44
                                     |
| Sorry, qsort() is not what I'm looking for. qsort() takes void* arguments, as well as a comparison function that takes void* arguments. You feed qsort an array of void*s and a comparison fn that compares them and it sorts 'em for you. qsort does not pointer casts of its own; it expects you to do all that.
What I'm saying is that the void* is C's attempt at generic programming, with qsort being a c-generic quicksort algo. To use qsort you have to feed it void*s, and then cast them back to their original type.
But I'm wondering if there's any case where you WANT to convert a FOO* to a BAR* where neither FOO nor BAR are void. The void* lets you do this, we think its dangerous, but is it ever actually necessary?
                                        Posted by svoboda at May 22, 2008 17:05
                                     |
| One example void non-void* -> non-void* casts:  struct sockaddr_whatever* -> struct sockaddr*, since the socket functions use struct sockaddr* as the generic socket address pointer type.
That is a special case of using struct pointers as generic pointers instead of void* to emulate Pascal-like variant records:  You have several structs like
struct whatever {
    enum variant_type type; /* same for all the structs */
    ...rest of struct contents...;
};

If Foo and Bar are two such structs, C allows you to access a Foo's type element as ((Bar\*)foo)-\>type. You then typically cast your Bar\* pointer to the correct struct pointer type depending on the value of the type field.
Another example is hash functions that access data as e.g. unsigned int\* for speed. Of course the callers must then ensure the data is properly aligned, and the hash function needs a general case to cater to hosts where an unsigned int can have padding bits. Also I suspect this is dubious anyway due to C's type aliasing rules, but the implications of those rules aren't really clear to me.
A third is casts from pointers to union Maximally_aligned { all the types you might need }; which is a trick to e.g. put properly aligned opaque objects in stack variables. Though I think this trick also runs into type aliasing rules.
However regarding Alex's example, as he said it's the compare function to qsort which has to break this rule, in that it must cast from void\*. And I'm not sure what's special about non-void\* examples, when the main text itself uses casting from void\* as a non-conformant example. As you say, void\* is kind of C's generic pointer. So you may need to cast away from it when you use generic pointers.
Another example of casting from void\* is when you work with dynamic pointers pointer types implemented by hand:
``` java
typedef struct { enum Ptrtype type; void *ptr; } Dynptr;
```
Sometimes you can use a union of pointers instead of the void\* for that, at other times that's impractical. E.g. in C89 only the first union member can have an initializer.
You'll find examples of char\* -\> other ptr\* casts if you seach some packages for use of offsetof().
Another example of casting between various pointer types arises when you need to build an object in memory in ways not directly supported by the C standard. For example if you want to avoid malloc() calls, either due to speed or to combat memory fragmentation: If a conceptual object consists of several C objects of varying length, you can't just put them in a struct and malloc that. But if you are careful about alignment you can call malloc just once, and place the objects at various offsets from the start of the malloced memory.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 23, 2008 11:30
\| \|
"Once it is cast to an int \*, some architectures will require that the object is aligned on a four-byte boundary. If int_ptr is later dereferenced, the program may terminate abnormally."
It's even worse than that, as the mere cast to int\* may cause loss of information. No dereference is even required to cause this. The following code won't work on all conforming C99 implementations, even though it never dereferences anything:
``` java
char c = 'x';
int* p = (int*) &c; // this can lose information
char* p2 = (char*) p;
assert( p2 == &c ); // will fail on some conforming implementations
```
On some implementations p2 will not match &c.
![](images/icons/contenttypes/comment_16.png) Posted by sgreen at Aug 24, 2009 23:57
\| \|
i restructured the rule a bit and added this information to the introductory material. do you know of any specific implementations for which this assertion fails?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 29, 2009 09:57
\| \|
Should we add a compliant solution or NCE/CS that uses the new C1X max_align_t?
As usual, Dan Saks has a nice article on this complete with example:
<http://embedded.com/design/220900317?pgno=1>
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 15, 2010 14:19
\| \|
I think it might be worth mentioning although I don't think using `max_align_t` solves the problem this rule cautions against.
Incidentally, if/where we do mention a C1X feature I think we should make it clear that the feature may not be available for some time to come and, if possible, present a portable alternative.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 16, 2010 22:59
\| \|
The Automated Detection section may want to mention;`-Wcast-align` for Clang. It does not catch the second NCCE (that requires interprocedural analysis), but it does catch the other two NCCEs.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 05, 2017 08:39
\| \|
This rule should also extend to taking the address of a member of a packed struct, which can also be improperly aligned. Normally, the compiler catches this and inserts proper get/set code, but when faced with the address, the compiler doesn't know to insert such code. More info here:
<https://stackoverflow.com/questions/8568432/is-gccs-attribute-packed-pragma-pack-unsafe>
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 23, 2017 02:42
\| \|
I ran into a much more subtle variation on this issue.; In some software, it's common to have special macros to hide unaligned reads, like this:
`  #define READ_UINT16(ptr)  (*(uint16_t *)ptr)`
These macros are, of course, carefully protected so that on architectures where unaligned access is a problem, a more complicated variation is used.  Many believe that x86 (and x64), unlike most RISC systems, have no trouble reading unaligned words, so the definition above is used.
This works "most of the time."  But there are times when it won't, and it's subtle.
If you write a loop that uses this macro, and then compile with a reasonably modern version of gcc (tested on 4.9.4 and up), and with optimization set to "-O3", then the compiler unrolls the loop using SSE2 instructions.  Those instructions (like MOVDQ) require 16-byte alignment.  The compiler "believes" it knows the alignment of the input pointer -- it's two-byte aligned according to that cast -- so it provides fix-up for 2-to-16 byte alignment.  If the source pointer is not two-byte aligned, though, the fix-up fails and you get a SIGSEGV.
In other words, if you want to be safe, you can't even pull this trick when you're on a platform that allows unaligned access, because the optimizer will believe your lies.
![](images/icons/contenttypes/comment_16.png) Posted by carlsonj at Oct 10, 2018 11:12
\| \|
[James:](https://wiki.sei.cmu.edu/confluence/display/~carlsonj)
Very interesting! Do you have a small code example that would illustrate this behavior?; Does it depend on any specific compiler flags? Or platform (other than x86 or x86-64)?
As you know, **EXP36-C-EX1** permits mis-aligning pointers on platforms where the hardware guarantees (or defines) behavior, and I'd like to post counter-example there if you have one.
I can see the rationale:  Optimizers tend to assume that your program has no undefined behavior, because if it does then the optimizer is free to do anything. And dereferencing a misaligned pointer is undefined behavior in C11, even if it is well-defined on x86.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 10, 2018 12:16
\| \|
    % gcc -O3 -Wall -fPIC -o crash-me crash-me.c% ./crash-me
    Compute something
    Segmentation fault
    % gcc -O3 -Wall -fPIC -mno-sse2 -o crash-me crash-me.c
    % ./crash-me
    Compute something
    % gcc --version
    gcc (GCC) 4.9.4
    Copyright (C) 2015 Free Software Foundation, Inc.
    This is free software; see the source for copying conditions.  There is NO
    warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
    % cat crash-me.c
    #include <stdio.h>
    #include <stdint.h>
    #define READ_UINT16(ptr)       (*(uint16_t *)(ptr))
    #define WRITE_UINT16(ptr, val) (*(uint16_t *)(ptr) = (val))
    void
    compute(unsigned char *b1, unsigned char *b2, int value, int range)
    {
      int i;
      for (i = 0; i < range; i++) {
        int newval = (int)READ_UINT16(b1) + value;
        WRITE_UINT16(b2, newval);
        b1 += 2;
        b2 += 2;
      }
    }
    int
    main(int argc, char **argv)
    {
      unsigned char buffer1[1024];
      unsigned char buffer2[1024];
      printf("Compute something\n");
      compute(buffer1 + 3, buffer2 + 1, 42, 500);
      return 0;
    }
![](images/icons/contenttypes/comment_16.png) Posted by carlsonj at Oct 10, 2018 12:52
\| \|
[James](https://wiki.sei.cmu.edu/confluence/display/~carlsonj):
Thanks for this code example! I've tested it a bit more:
-   ;   Crashes on GCC 4.9.4 (Debian)
-       Doesn't crash on GCC 4.8.5 (RHEL7)
-       Doesn't crash w/o -fPIC
-       Doesn't crash with -mno-sse2
-       Crashes on -O3 or -Ofast
-       Also crashes on -O2 -ftree-loop-vectorize -fvect-cost-model
You're quite right that some SSE2 instructions like MOVDQA trap rather than just operate slowly. Presumably the program would work if the optimizer used MOVDQU instead (which does not require alignment).
This doesn't invalidate our rule, but since we discuss x86 hardware in **EX1**, we should provide your code example, as a sort of "exception to the exception" ![](images/icons/emoticons/smile.svg)
I also think we should submit a bug report to GCC.  If the optimizer is going to depend on assembly instructions with strict requirements, then GCC needs to at least document this fact. Perhaps those optimizations should be part of -Ofast rather than -O2.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 10, 2018 15:14
\| \|
Yes, 4.9.4 is the first place I saw the new optimizer behavior.; I admit I haven't done an exhaustive search to find the precise point where it was introduced.
One of the fun parts of this is that the SIGSEGV (at least on the systems where I've tested this) falsely says that the exception address (siginfo_t.si_addr) is zero.  That's fun, because the user is likely to spend untold amounts of time looking for a null pointer that doesn't in fact exist.
As for whether it's a bug or not, I'm less sure.  The author of the C code is definitely depending on "unspecified" behavior.  The weapon aimed at his foot is "unspecified" with respect to the chamber contents.  What I would really like to see is:
1.  Some kind of documentation (as you say) indicating that certain specified options cause the optimizer to invalidate long-standing opinion about what the x86 machine looks like.  This documentation should come with oft-enabled (i.e., at least ~~-~~Wall) warnings, at least when the conditions that can cause the problem (-fPIC and such) are present.
2.  As a stretch goal, I'd love to have an attribute or built-in function (or similar) that allows me to say, "I'm casting this to a pointer that appears to imply an alignment, but I'm not actually providing a promise of alignment, so please do not make make assumptions that might rely on that promise when optimizing."  I could use that in the #defines above to get the best of both worlds.  But I realize that it may be impractical to do this, and there may be cases where it's impossible to make it work reliably.
![](images/icons/contenttypes/comment_16.png) Posted by carlsonj at Oct 10, 2018 15:32
\| \|
Your second question I can sort of answer right away. Use this attribute to disable SSE on your function:
    __attribute__ ((target("no-sse")))
That may not be the answer you seek, but that's what GCC offers  ![](images/icons/emoticons/smile.svg)  
I got this solution from a similar tale of woe:  
<http://pzemtsov.github.io/2016/11/06/bug-story-alignment-on-x86.html>  
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 10, 2018 15:59
\| \|
True, and I know about that ... but it works only for a function, so you have to "somehow" know which particular functions are affected by this issue stemming from the implementation of this macro.; And, surprisingly, a function like this can't be in-lined to remove the overhead imposed.  The following fails to compile with obscure errors referring to incompatible attributes:
`__attribute__((always_inline, target("no-sse")))`
`static inline uint16_t read_uint16(const void *ptr)`
`{`
`  return *(uint16_t *)ptr;`
`}`
`__attribute((always_inline, target("no-sse")))`
`static inline void write_uint16(void *ptr, uint16_t val)`
`{`
`  *(uint16_t *)ptr = val;`
`}`
`#define READ_UINT16(ptr)       read_uint16(ptr)`
`#define WRITE_UINT16(ptr, val) write_uint16((ptr), (val))`
![](images/icons/contenttypes/comment_16.png) Posted by carlsonj at Oct 10, 2018 16:15
\| \|
I have created GCC bug [87581](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=87581) to document this issue.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 10, 2018 16:26
\| \|
I have amended **EX1** with the details of this program behavior. We can remove these details only if the GCC maintainers agree to change GCC's current behavior.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 11, 2018 08:28
\|
