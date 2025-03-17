Functions that have an array as a parameter should also have an additional parameter that indicates the maximum number of elements that can be stored in the array. That parameter is required to ensure that the function does not access memory outside the bounds of the array and adversely influence program execution. It should be present for each array parameter (in other words, the existence of each array parameter implies the existence of a complementary parameter that represents the maximum number of elements in the array).
Note that *array* is used in this recommendation to mean array, string, or any other pointer to a contiguous block of memory in which one or more elements of a particular type are (potentially) stored. These terms are all effectively synonymous and represent the same potential for error.
Also note that this recommendation suggests the parameter accompanying array parameters indicates the maximum number of elements that can be stored in the array, not the maximum size, in bytes, of the array, because
1.  It does not make sense to think of array sizes in bytes in all cases—for example, in the case of an array of integers.
2.  If the size in bytes of the array is required, it can be derived from the number of elements in the array.
3.  It is better not to add to the cognitive load of the function user by requiring the user to calculate the size in bytes of the array.
In most cases, the distinction between the number of elements and number of bytes is moot: there is a clear mapping between the two, and it is easier to think in terms of number of elements anyway. Unfortunately, this issue can become muddled when working with multibyte strings because the logical entity being manipulated differs from that of the type being used to implement it. Here, it is important to remember that the type of the array is a character, not a multibyte character. Accordingly, the number of elements in the array is represented as a number of characters.
## Noncompliant Code Example
It is not necessary to go beyond the standard C library to find examples that violate this recommendation because the C language often prioritizes performance at the expense of [robustness](BB.-Definitions_87152273.html#BB.Definitions-robustness). The following are two examples from the C Standard, subclause 7.24 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
``` c
char *strncpy(char * restrict s1, const char * restrict s2, size_t n);
char *strncat(char * restrict s1, const char * restrict s2, size_t n);
```
These functions have two problems. First, there is no indication of the size of the first array, `s1`. As a result, it is not possible to discern within the function how large `s1` is and how many elements may be written into it. Second, it appears that a size is supplied for `s2`, but the `size_t` parameter `n` actually gives the number of elements to copy. Consequently, there is no way for either function to determine the size of the array `s2`.
## Compliant Solution
The C `strncpy()` and `strncat()` functions could be improved by adding element count parameters as follows:
``` c
char *improved_strncpy(char * restrict s1, size_t s1count, const char * restrict s2, size_t s2count, size_t n);
char *improved_strncat(char * restrict s1, size_t s1count, const char * restrict s2, size_t s2count, size_t n);
```
The `n` parameter is used to specify a number of elements to copy that is less than the total number of elements in the source string.
## Compliant Solution (C11 Annex K)
The C Standard, Annex K (normative) Bounds-checking interfaces, defines bounds-checking versions of standard C library string-handling functions:
``` c
errno_t strncpy_s(char * restrict s1, rsize_t s1max, const char * restrict s2, rsize_t n);
errno_t strcat_s(char * restrict s1, rsize_t s1max, const char * restrict s2);
```
There are two notable differences between the compliant solution and the secure versions from Annex K. First, the Annex K versions use `rsize_t` instead of `size_t`, which allows the size to be compared against the reasonable limit for a single object, `RSIZE_MAX`. Second, the Annex K versions do not require an element count for the second array. Consequently, these functions have limited ability to validate the input for `s2`. However, a size value for `s1` is required, so memory outside of the range for `s1` should not be overwritten.
## Exceptions
**API02-C-EX1:** Functions that can guarantee via their runtime-constraint handlers that no out-of-bounds read or write occurs may omit the maximum-elements argument. For instance, the `s2` parameter to `strcat_s()` needs no `max` parameter.
``` c
errno_t strcat_s(char * restrict s1, rsize_t s1max, const char * restrict s2);
```
As another example, consider `strcpy_s()`:
``` c
errno_t strcpy_s(char * restrict s1, rsize_t s1max, const char * restrict s2);
```
This function provides no explicit maximum argument to `s2`. However, it requires that `s1max` be larger than `s2`, thereby preventing an out-of-bounds read.
## Risk Assessment
Failure to follow this recommendation can result in improper memory accesses and buffer overflows that are detrimental to the correct and continued execution of the program.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API02-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.BO.* | A collection of checks that report uses of library functions prone to internal buffer overflows. |
| Parasoft C/C++test | 2024.2 | CERT_C-API02-aCERT_C-API02-b | Avoid using unsafe string functions which may cause buffer overflowsDon't use unsafe C functions that do write to range-unchecked buffers |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the CERT website.
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Annex K (normative) Bounds-checking Interfaces |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151926) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152287)
## Comments:

|  |
| ----|
| One nit with the second paragraph: an array can consist of one member.  An int* could represent a single integer, and is treated as an array with TooHigh=1.
This rule should actually discuss strncpy_s and strncat_s as the compliant solutions. (They are defined in TR24731-1, and will be in an appendix in C1x.)
I think the Risk Assessment should be high, not low. Poor APIs can lead to programmers writing outside an array bounds, leading to classic buffer overflows.
Finally, I feel a little queasy about complaining that C99 violates our recommendation, true as it may be. It undermines people's reliance on C. I would rather have a user-defined functions as the NCCE/CCEs; what do others think?
                                        Posted by svoboda at Nov 04, 2009 10:59
                                     |
| My only comment for this rule is that there should be two Compliant Solution sections, one for each compliant code. The first would contain the hypothetical API for strncpy/strncat, and the other addresses TR24731-1 and contains its APIs for strncpy_s/strcat_s. Other than that, this rule is complete.
                                        Posted by svoboda at Nov 06, 2009 13:49
                                     |
| The strcpy_s() function defined in TR 24731-1 Â§6.7.1.3 violates this rule:
#include <string.h>
errno_t strcpy_s(char * restrict s1,
rsize_t s1max,
const char * restrict s2);

Runtime-constraints
Neither s1 nor s2 shall be a null pointer. s1max shall not be greater than RSIZE_MAX. s1max shall not equal zero. s1max shall be greater than strnlen_s(s2, s1max).  
Copying shall not take place between objects that overlap.
However, I don't see anything wrong with this function because the definition requires that s1max shall be greater than strnlen_s(s2, s1max) which effectively prevents reading outside the bounds of s2.
This could potentially be added to the definition of the guideline, that is, something along the lines of "unless the definition of the function is such to preclude the possibility of an out-of-bounds read or write.
Even this isn't strictly true, because `strcpy_s()` clearly must determine the size of s2 by finding the first null byte, meaning it could read beyond the end of the array provided the array was not null terminated. Reading from the TooFar value results in undefined behavior.
The behavior of this function also seems inconsistent with the behavior of `strnlen_s()`
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 23, 2009 20:25
\| \|
> s1max shall be greater than strnlen_s(s2, s1max).

Actually, that is a tautological definition, because strnlen_s cannot return a value \> s1max. (TR24731-1 Section 6.7.1.3). I think they meant to say s1max \>= strlen(s2), but preferred interanl consistency.
Also strcat_s doesn't provide a size argument to s2. Which I also think is not a problem.
I suspect the rule is fine, but it needs an exception for when omitting a max argument cannot result in an out-of-bounds read or write.
I don't think this rule should try to address the case where the max size supplied actually lies, or when the string is not null-terminated...those are both conditions that are near impossible to enforce.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 24, 2009 10:40
\| \|
Added the exception described above.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 24, 2009 10:46
\| \|
Under Risk Assessment, the sentence "Failure to do so can result in buffer overflows in the program" needs to be restated to specify what "do so" means.
![](images/icons/contenttypes/comment_16.png) Posted by lallierc at Jul 12, 2012 23:28
\| \|
I find that strncpy() to be low risk and definitely not worth replacing.; I have been coding for 35 years and here is what I think and do.
a\) I usually use strcpy() when I know the sizes of source input and target output.
When I do not know the size of the input string, because it is dynamic, I use strncpy()
assume x to be a char \* pointer.
b\) I use x=strncpy() and check x, the output of strncpy() to determine if an overrun problem has occurred. That checking is done when I know little about the origin of the source to strncpy. But I do know about the target.
So, the next question is, what about having to modify someone elses code?   Again, x=strncpy(... ) and test x for sizeof(char \*restrict r1) versus size_t  before investigating further.  Any programmer just does not
put in code without knowing source and target of a copy.
If you apply the double restrict, what do you gain with  x being assigned by strncpy()?   It will mask and not tell you about the copy.  And please note, this is used for a copy of (null) terminated strings, and not arbitrary memory.
I would consider redirecting the above increased restriction proposed to functions such as memcpy, memcat or memmove. 
![](images/icons/contenttypes/comment_16.png) Posted by lsatenstein at Sep 26, 2012 10:57
\| \|
-   Other developers changing your code may have little time to understand it in full.; (Using strncpy() and strncpy_s() adds safeguards but this adds little to safety when someone changes the size of an object in a function that calls your function.  Explicitly propagating object sizes to every function call makes the code less "automatic").
-   The Open Group says on strncpy, "no return value is reserved to indicate an error."
![](images/icons/contenttypes/comment_16.png) Posted by ilatypov at Aug 09, 2013 00:14
\| \|
Hello David, my understanding is the strncpy and strncat in the first compliant solution part are optimized / improved non-standard functions, but they have the sames names than standard versions. I think they should be renamed in order to clearly identify we talk about new functions. Redefine standard functions by keeping the same name doesn't appear to me to be safe. Olivier.
![](images/icons/contenttypes/comment_16.png) Posted by obinnert at Feb 16, 2021 08:42
\| \|
Oliver:I decided that you are right: the dangers of redefining a standard function justify changing the names of the hypothetical improved functions. While we can hypothesize about how the standard could be improved, modifying standard functions in an incompatible manner is impossible in standard C and we do not wish to mislead anyone into thinking otherwise. So both improved functions have new names now.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 16, 2021 09:03
\|
