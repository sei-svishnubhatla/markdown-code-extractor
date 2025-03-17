Dereferencing a null pointer is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
On many platforms, dereferencing a null pointer results in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination), but this is not required by the standard. See "[Clever Attack Exploits Fully-Patched Linux Kernel](http://www.theregister.co.uk/2009/07/17/linux_kernel_exploit/)" \[[Goodin 2009](AA.-Bibliography_87152170.html#AA.Bibliography-Goodin2009)\] for an example of a code execution [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) that resulted from a null pointer dereference.
## Noncompliant Code Example
This noncompliant code example is derived from a real-world example taken from a vulnerable version of the `libpng` library as deployed on a popular ARM-based cell phone \[[Jack 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Jack07)\]. The  `libpng` library allows applications to read, create, and manipulate PNG (Portable Network Graphics) raster image files. The `libpng` library implements its own wrapper to `malloc()` that returns a null pointer on error or on being passed a 0-byte-length argument.
This code also violates [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors).
``` c
#include <png.h> /* From libpng */
#include <string.h>
void func(png_structp png_ptr, int length, const void *user_data) { 
  png_charp chunkdata;
  chunkdata = (png_charp)png_malloc(png_ptr, length + 1);
  /* ... */
  memcpy(chunkdata, user_data, length);
  /* ... */
 }
```
If `length` has the value `−1`, the addition yields 0, and `png_malloc()` subsequently returns a null pointer, which is assigned to `chunkdata`. The `chunkdata` pointer is later used as a destination argument in a call to `memcpy()`, resulting in user-defined data overwriting memory starting at address 0. In the case of the ARM and XScale architectures, the `0x0` address is mapped in memory and serves as the exception vector table; consequently, dereferencing `0x0` did not cause an [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).
## Compliant Solution
This compliant solution ensures that the pointer returned by `png_malloc()` is not null. It also uses the unsigned type `size_t` to pass the `length` parameter, ensuring that negative values are not passed to `func()`.
This solution also ensures that the `user_data` pointer is not null. Passing a null pointer to memcpy() would produce undefined behavior, even if the number of bytes to copy were 0.  The `user_data` pointer could be invalid in other ways, such as pointing to freed memory. However there is no portable way to verify that the pointer is valid, other than checking for null.
``` c
#include <png.h> /* From libpng */
#include <string.h>
 void func(png_structp png_ptr, size_t length, const void *user_data) { 
  png_charp chunkdata;
  if (length == SIZE_MAX) {
    /* Handle error */
  }
  if (NULL == user_data) {
    /* Handle error */
  }
  chunkdata = (png_charp)png_malloc(png_ptr, length + 1);
  if (NULL == chunkdata) {
    /* Handle error */
  }
  /* ... */
  memcpy(chunkdata, user_data, length);
  /* ... */
 }
```
## Noncompliant Code Example
In this noncompliant code example, `input_str` is copied into dynamically allocated memory referenced by `c_str`. If `malloc()` fails, it returns a null pointer that is assigned to `c_str`. When `c_str` is dereferenced in `memcpy()`, the program exhibits [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).  Additionally, if `input_str` is a null pointer, the call to `strlen()` dereferences a null pointer, also resulting in undefined behavior. This code also violates [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors).
``` c
#include <string.h>
#include <stdlib.h>
void f(const char *input_str) {
  size_t size = strlen(input_str) + 1;
  char *c_str = (char *)malloc(size);
  memcpy(c_str, input_str, size);
  /* ... */
  free(c_str);
  c_str = NULL;
  /* ... */
}
```
## Compliant Solution
This compliant solution ensures that both `input_str` and the pointer returned by `malloc()` are not null: 
``` c
#include <string.h>
#include <stdlib.h>
void f(const char *input_str) {
  size_t size;
  char *c_str;
  if (NULL == input_str) {
    /* Handle error */
  }
  size = strlen(input_str) + 1;
  c_str = (char *)malloc(size);
  if (NULL == c_str) {
    /* Handle error */
  }
  memcpy(c_str, input_str, size);
  /* ... */
  free(c_str);
  c_str = NULL;
  /* ... */
}
```
## Noncompliant Code Example
This noncompliant code example is from a version of `drivers/net/tun.c` and affects Linux kernel 2.6.30 \[[Goodin 2009](AA.-Bibliography_87152170.html#AA.Bibliography-Goodin2009)\]:
``` c
static unsigned int tun_chr_poll(struct file *file, poll_table *wait)  {
  struct tun_file *tfile = file->private_data;
  struct tun_struct *tun = __tun_get(tfile);
  struct sock *sk = tun->sk;
  unsigned int mask = 0;
  if (!tun)
    return POLLERR;
  DBG(KERN_INFO "%s: tun_chr_poll\n", tun->dev->name);
  poll_wait(file, &tun->socket.wait, wait);
  if (!skb_queue_empty(&tun->readq))
    mask |= POLLIN | POLLRDNORM;
  if (sock_writeable(sk) ||
     (!test_and_set_bit(SOCK_ASYNC_NOSPACE, &sk->sk_socket->flags) &&
     sock_writeable(sk)))
    mask |= POLLOUT | POLLWRNORM;
  if (tun->dev->reg_state != NETREG_REGISTERED)
    mask = POLLERR;
  tun_put(tun);
  return mask;
}
```
The `sk` pointer is initialized to `tun->sk` before checking if `tun` is a null pointer. Because null pointer dereferencing is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), the compiler (GCC in this case) can optimize away the `if (!tun)` check because it is performed after `tun->sk` is accessed, implying that `tun` is non-null. As a result, this noncompliant code example is vulnerable to a null pointer dereference exploit, because null pointer dereferencing can be permitted on several platforms, for example, by using `mmap(2)` with the `MAP_FIXED` flag on Linux and Mac OS X, or by using the `shmat()` POSIX function with the `SHM_RND` flag \[[Liu 2009](AA.-Bibliography_87152170.html#AA.Bibliography-Liu2009)\].
## Compliant Solution
This compliant solution eliminates the null pointer deference by initializing `sk` to `tun->sk` following the null pointer check. It also adds assertions to document that certain other pointers must not be null.
``` c
static unsigned int tun_chr_poll(struct file *file, poll_table *wait)  {
  assert(file);
  struct tun_file *tfile = file->private_data;
  struct tun_struct *tun = __tun_get(tfile);
  struct sock *sk;
  unsigned int mask = 0;
  if (!tun)
    return POLLERR;
  assert(tun->dev);
  sk = tun->sk;
  assert(sk);
  assert(sk->socket);
  /* The remaining code is omitted because it is unchanged... */
}
```
## Risk Assessment
Dereferencing a null pointer is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), typically [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination). In some situations, however, dereferencing a null pointer can lead to the execution of arbitrary code \[[Jack 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Jack07), [van Sprundel 2006](AA.-Bibliography_87152170.html#AA.Bibliography-vanSprundel06)\]. The indicated severity is for this more severe case; on platforms where it is not possible to exploit a null pointer dereference to execute arbitrary code, the actual severity is low.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP34-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | null-dereferencing | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP34 |  |
| CodeSonar | 8.3p0 | LANG.MEM.NPDLANG.STRUCT.NTAD
LANG.STRUCT.UPD | Null pointer dereferenceNull test after dereference
Unchecked parameter dereference |
| Compass/ROSE |  |  | Can detect violations of this rule. In particular, ROSE ensures that any pointer returned by malloc(), calloc(), or realloc() is first checked for NULL before being used (otherwise, it is free()-ed). ROSE does not handle cases where an allocation is assigned to an lvalue that is not a variable (such as a struct member or C++ function call returning a reference) |
| Coverity | 2017.07 | CHECKED_RETURNNULL_RETURNSREVERSE_INULLFORWARD_NULL | Finds instances where a pointer is checked against NULL and then later dereferencedIdentifies functions that can return a null pointer but are not checkedIdentifies code that dereferences a pointer and then checks the pointer against NULLCan find the instances where NULL is explicitly dereferenced or a pointer is checked against;NULL but then dereferenced anyway. Coverity Prevent cannot discover all violations of this rule, so further verification is necessary |
| Cppcheck | ;2.15 | nullPointer, nullPointerDefaultArg, nullPointerRedundantCheck |  |
| Cppcheck Premium | 24.11.0 | nullPointer, nullPointerDefaultArg, nullPointerRedundantCheck |  |
| Helix QAC | 2024.4 | DF2810, DF2811, DF2812, DF2813 | Fully implemented |
| Klocwork | 2024.4 | NPD.CHECK.CALL.MIGHTNPD.CHECK.CALL.MUST
NPD.CHECK.MIGHT
NPD.CHECK.MUST
NPD.CONST.CALL
NPD.CONST.DEREF
NPD.FUNC.CALL.MIGHT
NPD.FUNC.CALL.MUST
NPD.FUNC.MIGHT
NPD.FUNC.MUST
NPD.GEN.CALL.MIGHT
NPD.GEN.CALL.MUST
NPD.GEN.MIGHT
NPD.GEN.MUST
RNPD.CALL
RNPD.DEREF | Fully implemented |
| LDRA tool suite | 9.7.1 | 45 D, 123 D, 128 D, 129 D, 130 D, 131 D, 652 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP34-a | Avoid null pointer dereferencing |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 413, 418, 444, 613, 668 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP34-C | Checks for use of null pointers (rule partially covered) |
| PVS-Studio | 7.35 | V522, V595, V664, V713, V1004 |  |
| SonarQube C/C++ Plugin | 3.11 | S2259 |  |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | mem_access | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | EXP01-J. Do not use a null in a case where an object is required | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Null Pointer Dereference [XYH] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Dereferencing an out-of-domain pointer [nullref] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-476, NULL Pointer Dereference | 2017-07-06: CERT: Exact |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-690 and EXP34-C
EXP34-C = Union( CWE-690, list) where list =
-   Dereferencing null pointers that were not returned by a function
### CWE-252 and EXP34-C
Intersection( CWE-252, EXP34-C) = Ø
EXP34-C is a common consequence of ignoring function return values, but it is a distinct error, and can occur in other scenarios too.
## Bibliography 

|  |  |
| ----|----|
| [Goodin 2009] |  |
| [Jack 2007] |  |
| [Liu 2009] |  |
| [van Sprundel 2006] |  |
| [Viega 2005] | Section 5.2.18, "Null-Pointer Dereference" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152129) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152058)
## Comments:

|  |
| ----|
| Should that be: if (size >= SIZE_MAX) {
                                        Posted by jm at Dec 25, 2006 14:36
                                     |
| I believe in this case, either expression would work. 
SIZE_MAX is the largest possible value that a size_t could take, so it is not possible to have anything larger than SIZE_MAX.
The test was added to catch the possibly theoretical situation where the length of input_str was somehow the maximum size for size_t, and adding one to this size in the malloc expression (to allocated space for the trailing null byte) results in an integer overflow.
I say "theoretical" because I have not successfully produced strings of this length in testing.
                                        Posted by rcs at Dec 26, 2006 10:21
                                     |
| I added a comment to explain that SIZE_MAX is the limit of size_t
                                        Posted by rcs at Dec 26, 2006 10:24
                                     |
| Ah, gotcha. That makes sense. Yeah, I suspect once it's possible to allocate 2+gigs contiguously in amainstream install of a modern OS, we'll see a frenzy of new vulnerabilities come out. The 4gig boundary will probably be important too with unsigned int in LP64, but since size_t will be 64-bit, there will have to be some truncation that compilers will be able to warn on. (I think you cover that in a different rule.) The above check can't hurt, as I guess you could have a system with a 32-bit size_t that had a ton of memory and had some crazy banking/selector scheme with pointers. It also reinforces the notion to the reader that any time you see arithmetic in an allocation expression, you need to think about corner-cases.
                                        Posted by jm at Dec 26, 2006 18:02
                                     |
| In my experience, there are reasons to check for a NULL pointer other than dereferencing it.
A common memory-leak idiom, is reallocating storage and assigning its address to a pointer that already points to allocated storage. The correct idiom is to only allocate storage if the pointer is currently NULL. But no where in that particular idiom would a NULL pointer necessarily be deferenced.
                                        Posted by wlf@cert.org at Mar 15, 2007 09:40
                                     |
| The article easily misleads the reader into believeing that ensuring pointer validity boils down to checking for pointer being not equal to NULL.  Unfortunately the problem is much more complex, and generally unsolvable within standard C.  Consider the following example:
void f(int *x)
{
  *x = 12;
}
void g(void)
{
  int x, *p = &x;
  f(p+1);
}

There's no way f can check whether x points into valid memory or not. Using platform-specific means (e.g. parsing /proc/self/maps under linux) one might find out whether the pointer points into mapped memory, but this is still not a guarantee of validity because it is very coarse-grained – see again the above example. IMHO, the rule title should be changed to something less general.
![](images/icons/contenttypes/comment_16.png) Posted by zvrba at Mar 30, 2008 02:02
\| \|
That's true.; I've changed it to say null pointer instead of invalid pointer.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 30, 2008 10:52
\| \|
It is useful to have a function with portable interface but platform-dependent implementation:
extern bool invalid(const void \*); ...  
assert(!invalid(p)); // or whatever
Typical implementation:
bool invalid(const void \*p) {  
extern char \_etext;  
return p == NULL \|\| (char \*)p \< &\_etext;  
}
Note that it doesn't know how to check for non-heap, non-stack.  Many platforms can support testing for those also.
The idea is not to guarantee validity, but to catch a substantial number of problems that could occur.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 15:13
\| \|
Made code more compliant with other rules.
At this point we define size as strlen(input_str) + 1. Since SIZE_MAX represents the largest possible object, the largest possible string would then be SIZE_MAX-1 characters long (excluding '\0'). So the SIZE_MAX check was unnecessary.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2008 13:10
\| \|
This is a matter of style, and also following code walkthrough.; In the complaint version
We have mask = 0;
Then below, first change to mask  is
mask \|= `POLLIN | POLLRDNORM;`
 I like to make source code checking a little quicker by putting parenthesizes around  arguments to \|=  or &=  as
`mask |= (POLLOUT | POLLWRNORM);`
![](images/icons/contenttypes/comment_16.png) Posted by lsatenstein at Nov 08, 2012 10:05
\| \|
The final NCCE is actually more insidious than it seems at first.; Because null pointer dereferencing is UB, the if (!tun) check can be elided entirely by the optimizer (since the tun-\>sk implies that tun **must** be non-null).
<http://blog.llvm.org/2011/05/what-every-c-programmer-should-know_14.html>
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 11, 2013 10:32
\| \|
The 2nd NCCE/CS pair seems redundant with the first NCCE/CS pair.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 04, 2013 16:47
\| \|
One could argue that all code examples would be redundant with the first pair.; ![](images/icons/emoticons/smile.svg)  In this case, the difference is the assumption that `malloc()` always returns non-null for the second NCCE, whereas the first NCCE has the `malloc()` abstracted away.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 09:08
\| \|
I suggest that this topic needs to include calloc() and realloc();  Refer to [Linux man pages online](index)  for more enlightenment about malloc(), and friends.  
I believe that dereferencing NULL should not crash the system, should not allow a write to a NULL pointer area, but should always set errno,  If I am a hacker, could I trap a null failure that would force a memory dump. Could I capture, and I would be able to glean much security information from the dump?   The null pointer check for writing or dereferencing should be a compiler flag or library setting.
![](images/icons/contenttypes/comment_16.png) Posted by lsatenstein at Aug 02, 2014 11:49
\| \|
This rule applies to all null pointers, regardless of which function returned them.;
Believing that dereferencing NULL shouldn't crash the system doesn't make it true.  I guess you could write a proposal to modify the C Standard, but our coding standard is meant to provide guidance for the existing language.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 15, 2014 10:12
\| \|
Solution 1, it looks like, today's solution tomorrow's problem. int changed to size_t and if size_t parameter's is zero, allocate one word. Then we hit memcpy with length 0. When length is zero, it is probably unusable condition for this function.;  
![](images/icons/contenttypes/comment_16.png) Posted by vlad at Apr 12, 2018 14:13
\| \|
There are other problems with this code, as is noted in the rule. But passing 0 to memcpy() is not one of them. The standard will simply copy 0 bytes...which is essentially a no-op. (C11, S7.24.2.1)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 10:40
\| \|
That interpretation of the standard is not supported universally. See C17 7.1.4p1, which says, in part:
> Each of the following statements applies unless explicitly stated otherwise in the detailed descriptions that follow:
>
> If an argument to a function has an invalid value (such as a value outside the domain of the function, or a pointer outside the address space of the program, or a null pointer, or a pointer;to non-modifiable storage when the corresponding parameter is not const-qualified) or a type (after default argument promotion) not expected by a function with a variable number of arguments, the behavior is undefined.

The issue is: memcpy() and friends do not explicitly state that a null pointer is a valid pointer value, even if the number of bytes to copy is 0.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 16, 2018 11:32
\| \|
Isn't easier just to check valid range of length? I doubt that "length" of zero is a valid parameter, and although there no copy, but we see memory allocation. It looks like a logic bug, which can cause a memory leaking.;   
![](images/icons/contenttypes/comment_16.png) Posted by vlad at Apr 16, 2018 13:23
\| \|
Aaron, don't confuse Vladimir :)
A non-null but invalid pointer passed to memcpy() can indeed cause undefined behavior, but that is not the issue in the noncompliant code...the pointer will either be valid or null. And the compliant solution guarantees that the pointer will be valid if the code calls memcpy().
The issue of passing n=0 to memcpy() is distinct from null or invalid pointers. Best to cite C11 s7.24.2.1 here:
> The memcpy function copies n characters from the object pointed to by s2 into the object pointed to by s1. If copying takes place between objects that overlap, the behavior is undefined.

Clearly the standard enumerates 1 case of undefined behavior, but makes no special mention of n=0. (In contrast, the case of passing 0 bytes to malloc is addressed in C11.) 0 is certainly within the 'domain of the function' (a phrase defined by mathematics but not by C11), as copying 0 bytes is well-understood (although silly).
I would therefore assert that a platform whose memcpy() did anything besides a no-op when given n=0 and valid source/destination pointers was not C-standards-compliant.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 14:16
\| \|
> I would therefore assert that a platform whose memcpy() did anything besides a no-op when given n=0 and valid source/destination pointers was not C-standards-compliant.

Your assertion is not backed by the wording in the standard, nor by common implementer understanding. It's even called out explicitly in C17 7.24.1p2:
> Where an argument declared as size_t n specifies the length of the array for a function, n can have the value zero on a call to that function. Unless explicitly stated otherwise in the description of a particular function in this subclause, pointer arguments on such a call shall still have valid values, as described in 7.1.4. On such a call, a function that locates a character finds no occurrence, a function that compares two character sequences returns zero, and a function that copies characters copies zero characters.

Note that 7.1.4 explicitly states that a null pointer is not a valid pointer argument. The value 0 for the number of bytes to copy is not what causes the UB, it's the null pointer value which triggers it.
Optimizers are optimizing based on this latitude and have been for years. See the "Null pointer checks may be optimized away more aggressively" section in;<https://gcc.gnu.org/gcc-4.9/porting_to.html> as an example with one common implementation.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 16, 2018 14:41
\| \|
Aaron:I suspect we are talking past each other. So let me be more precise in my wording:
I assert that a platform whose memcpy() did anything besides copy zero bytes when given n=0 and valid src and dest pointers was not C-standards-compliant. By 'valid pointers' I mean that both src and dest pointers are not null and they both point to non-overlapping arrays containing at least n bytes each.
The n=0 is a mildly interesting edge case: Clearly a pointer that points to at least one valid byte could be used as the src or dest pointer to a call to memcpy(..., 0). I suppose there is a question of "Is a pointer that points to 0 bytes valid?" that we haven't considered here: I'd guess null pointers are not valid, even though they point to 0 bytes. Likewise, pointers to freed memory are not valid. I would also guess that pointers that point to the one-past-the-end of an array are also invalid. I'd guess WG14 has considered these questions, but I haven't until now :)
Finally, there is the matter of the compliant solution. Which ensures that the chunkdata pointer is valid, but makes no such check to the user_data pointer. I suppose we can check that that is not null, but we cannot check that it is valid (in any portable way).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 15:18
\| \|
> I assert that a platform whose memcpy() did anything besides copy zero bytes when given n=0 and valid src and dest pointers was not C-standards-compliant. By 'valid pointers' I mean that both src and dest pointers are not null and they both point to non-overlapping arrays containing at least n bytes each.

Phew, we're agreed here. Thank you for clarifying your assertion until I understood it properly.
> I'd guess null pointers are not valid, even though they point to 0 bytes.

Correct; a null pointer is not a valid pointer for the C library functions.
> Finally, there is the matter of the compliant solution. Which ensures that the chunkdata pointer is valid, but makes no such check to the user_data pointer. I suppose we can check that that is not null, but we cannot check that it is valid (in any portable way).

I think that checking for user_data being NULL would be an improvement to the CS so long as there is an explicit mention that user_data being NULL is invalid even if length == 0.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 16, 2018 15:36
\| \|
> I think that checking for user_data being NULL would be an improvement to the CS so long as there is an explicit mention that user_data being NULL is invalid even if length == 0.

Agreed. I've made this change.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 15:50
\| \|
Thanks, David! Small typo nit: "such as if i t pointed to freed memory" meant to say "if it" instead (removing whitespace).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 16, 2018 15:52
\| \|
Fixed, thanks
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 16:02
\| \|
Vladimir:
To be precise, once length is changed to a size_t and cannot take negative values, it cannot have an invalid value. 0 is a valid value as far as memcpy() is concerned, and malloc() has special language concerning malloc(0). So no checking of the length is necessary (besides preventing integer overflow, which the compliant solution does).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2018 17:05
\| \|
Why does the second compliant example permit using possibly-null pointers? Shouldn't the function check all pointers before dereferencing them or passing them to another function?
    static;unsigned int tun_chr_poll(struct file *file, poll_table *wait)  {
      if (!file) 
        // handle error  
      structtun_file *tfile = file->private_data;
      if (!tfile)
        // handle error
    /* The remaining code is omitted because it is unchanged... */
    }
![](images/icons/contenttypes/comment_16.png) Posted by jscottbosch at Jun 20, 2018 16:48
\| \|
Good question!; That noncompliant code example (it's currently the 3rd) came from the Linux kernel, whose source is publicly available.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 20, 2018 17:03
\| \|
Off by one error: It is the third example. But the problem also exists in the compliant version, so I'm not so sure that it's really compliant.;
![](images/icons/contenttypes/comment_16.png) Posted by jscottbosch at Jun 20, 2018 17:08
\| \|
Agreed. I added an assertion to that compliant code example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 21, 2018 18:56
\| \|
In the first compliant example it's useless to do allocation if the essential pointer user_data is NULL.
So we have to check all the arguments before performing any actions.
![](images/icons/contenttypes/comment_16.png) Posted by peter-awsmtek at May 12, 2021 07:59
\| \|
Whoops, you're right. I reordered that code example to do all the checks before allocations.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2021 15:11
\| \|
The description “The `sk`; pointer is initialized to `tun->sk`  before checking if `tun`  is a null pointer.” is provided for a non-compliant code example.  
Thus it seems that the arrow operator (member access through pointer) is usually treated also as a dereference operation.
![](images/icons/emoticons/help_16.svg) Would such an aspect be influenced in any ways if [the address of operator](https://en.cppreference.com/w/c/language/operator_member_access#Address_of) would be applied around similar expressions?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 10, 2023 11:40
\| \|
It depends on the specific details, but in general, taking the address of any valid memory is OK. Even if that memory contains a pointer which is not valid, or has been freed.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2023 12:51
\| \|
![](images/icons/emoticons/help_16.svg) Will the ordering matter a bit more for the safe evaluation of involved expressions?
Another source code example:
``` c
struct x * p1 = NULL;
struct y * p2 = &(p1->my_item);
if (!p1)
   return EINVAL;
```
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 10, 2023 13:40
\| \|
Yes the ordering matters. In your code example, the p1→my_item will be evaluated before t he & operator, and so this rule is violated, although you are really trying to do pointer arithmetic rather than see what the pointer points to.
FWIW the pointer arithmetic is also invalid because p1 does not point to valid memory, so you scan't just say something like
p2 = p1 + offsetof(struct x, my_item);
That code does not violate th is rule, but it violates [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2023 13:58
\| \|
> …, and so this rule is violated, …

-   May it be expected that the address of operator will eventually be evaluated only after a pointer dereference for a desirable access to a data structure member?
-   Would you become interested in a related clarification approach for a discussion topic like “[Reconsidering pointer dereferences before null pointer checks (with SmPL)](https://lore.kernel.org/cocci/1a11455f-ab57-dce0-1677-6beb8492a257@web.de/)”?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 10, 2023 14:27
\| \|
Markus:Unfortunately, your link also points to code that violates this rule, and is thus undefined behavior. See C23 (n3096) s6.5.3.2p3:
> The unary & operator yields the address of its operand. If the operand has type "type", the result has type "pointer to type". If the operand is the result of a unary \* operator, neither that operator nor the & operator is evaluated and the result is as if both were omitted, except that the constraints on the operators still apply and the result is not an lvalue. Similarly, if the operand is the result of a \[\] operator, neither the & operator nor the unary \* that is implied by the \[\] is evaluated and the result is as if the & operator were removed and the \[\] operator were changed to a + operator. Otherwise, the result is a pointer to the object or function designated by its operand.

In particular, this paragraph  enables & to cancel out \* (eg &\*x == x) and \[\]  (eg &x\[5\] == x + 5), but not -\>.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2023 14:45
\| \|
> Unfortunately, your link also points to code that violates this rule, and is thus undefined behavior.

-   Does this feedback indicate that you [understand the source code search pattern](https://lore.kernel.org/cocci/1a11455f-ab57-dce0-1677-6beb8492a257@web.de/) (which I published on the linked mailing list for the Coccinelle software yesterday)?
-   Would you like to help any further according to different understanding and expectations for affected implementation details?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 10, 2023 15:03
\| \|
Markus:Sorry, let me be more precise:
The code:
  &input-\>member
is undefined behavior (UB) if input does not actually point to a valid struct.  The platform does add offsetof( struct_type, member) to input and dereferences that. If input is null, that is technically not a null dereference, but we still consider it a violation of this rule for practicality, although to be anal, it is instead a violation of ARR30-C.
I note with interest, that ISO C does permit &\*x when x is null.  It also permits &x\[y\] to translate to x + y, but that is still UB if x is null because of ARR38-C. ISO C just has no similar wording for x-\>member.
If your code examples are simply searching for instances of C code of this nature, then the UB is not in your code, you just may be searching for code with potential UB.
Does that clarify things?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2023 15:21
\| \|
> The code:
>
> ; &input-\>member
>
> is undefined behavior (UB) if input does not actually point to a valid struct.

[One of the Coccinelle software maintainers expressed opposite development views today](https://lore.kernel.org/cocci/alpine.DEB.2.22.394.2304100959310.3387@hadrien/).
Thus I became a bit more curious about involved technical details.
> If input is null, that is technically not a null dereference,

It seems that my understanding needs also to grow for such information.
> but we still consider it a violation of this rule for practicality, although to be anal, it is instead a violation of ARR30-C.

I find it interesting in this case how you think in another direction.
> If your code examples are simply searching for instances of C code of this nature,

This is the intention for the referenced small script of the semantic patch language.
> then the UB is not in your code, you just may be searching for code with potential UB.

I got the impression that 31 source files of Linux modules will need further adjustments.
> Does that clarify things?

Partly, yes.
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 10, 2023 16:07
\| \|
Markus:
Thanks for the reference to Julia Lawall's response to your question. ;Overall, I disagree with her answer, and agree with the StackOverflow response (<https://stackoverflow.com/questions/25725286/does-taking-address-of-member-variable-through-a-null-pointer-yield-undefined-be>). However, I must add a few qualifications:
First of all, there is the question of whether this is for C or for C++. The two languages try to maximize compatibility, and occasionally succeed. :)
I'll just provide a few references to back up my beliefs. We should Zoom if you wish to talk more.
C23, s6.5.3.2p4 says:
> If an invalid value has been assigned to the pointer, the behavior of the unary \* operator is undefined.115)

Footnote 115 says:
> Thus, &\*E is equivalent to E (even if E is a null pointer), and &(E1\[E2\]) to ((E1)+(E2)). It is always true that if E is a function designator or an lvalue that is a valid operand of the unary & operator, \*&E is a function designator or an lvalue equal to E. If \*P is an lvalue and T is the name of an object pointer type, \*(T)P is an lvalue that has a type compatible with that to which T points. Among the invalid values for dereferencing a pointer by the unary \* operator are a null pointer, an address inappropriately aligned for the type of object pointed to, and the address of an object after the end of its lifetime.

which bolsters my assertion that x-\>member dereferences x (or at least an offset of x).
Furthermore, the C++20 draft (N4860) s7.6.2.1p1 says:
> The unary \* operator performs indirection: the expression to which it is applied shall be a pointer to an object type, or a pointer to a function type and the result is an lvalue referring to the object or function to which the expression points.

While not explicitly mentioning UB, I would infer that \*NULL is UB since NULL is not a pointer to an object or function type.
WG21 (the C++ working group) may wish to define 0-\>y, and they are within their right to do so. It would be tricky, and they would want WG14 (C working group) to at least bless this change, and more likely, make the analogous change to the C standard.
Finally, Clang and Coccinelle are part of the LLVM project, which will define some of the undefined behaviors in C++. Possibly Clang/LLVM may choose to always return a valid value for &NULL-\>member.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2023 16:53
\| \|
Thanks for your explanations.
Now it seems that I can inform also Linux contributors with higher confidence about further change possibilities (which I detected by the means of the Coccinelle software again recently).
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 11, 2023 02:54
\| \|
> The two languages try to maximize compatibility, …

Various developers and code reviewers are struggling also with evolution of the specifications for such programming languages.
Do you find another previous clarification approach interesting and helpful?
![](images/icons/emoticons/help_16.svg) [Does &((struct name \*)NULL -\> b) cause undefined behaviour in C11?](https://stackoverflow.com/questions/26906621/does-struct-name-null-b-cause-undefined-behaviour-in-c11)
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 13, 2023 03:22
\| \|
Markus:AFAICT the respponses to this StackOverflow question agree with my previous assertions. 0-\>member is undefined behavior. At best ISO C is under-specified in this regard, and perhaps should explicitly say so.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 13, 2023 06:04
\|
