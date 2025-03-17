The `calloc()` function takes two arguments: the number of elements to allocate and the storage size of those elements. Typically, `calloc()` [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementations) multiply these arguments to determine how much memory to allocate. Historically, some implementations failed to check whether out-of-bounds results silently wrapped \[[RUS-CERT Advisory 2002-08:02](http://cert.uni-stuttgart.de/advisories/calloc.php)\]. If the result of multiplying the number of elements to allocate and the storage size wraps, less memory is allocated than was requested. As a result, it is necessary to ensure that these arguments, when multiplied, do not wrap.
Modern implementations of the C standard library should check for wrap. If the `calloc()` function implemented by the libraries used for a particular implementation properly handles [unsigned integer wrapping](BB.-Definitions_87152273.html#BB.Definitions-unsignedintegerwrapping) (in conformance with [INT30-C. Ensure that unsigned integer operations do not wrap](https://www.securecoding.cert.org/confluence/display/seccode/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap)) when multiplying the number of elements to allocate and the storage size, that is sufficient to comply with this recommendation and no further action is required.
## Noncompliant Code Example
In this noncompliant example, the user-defined function `get_size()` (not shown) is used to calculate the size requirements for a dynamic array of `long int` that is assigned to the variable `num_elements`. When `calloc()` is called to allocate the buffer, `num_elements` is multiplied by `sizeof(long)` to compute the overall size requirements. If the number of elements multiplied by the size cannot be represented as a `size_t`, then `calloc()` may allocate a buffer of insufficient size. When data is copied to that buffer, an overflow may occur.
``` c
size_t num_elements;
long *buffer = (long *)calloc(num_elements, sizeof(long));
if (buffer == NULL) {
  /* Handle error condition */
}
/* ... */
free(buffer);
buffer = NULL; 
```
## Compliant Solution
In this compliant solution, the two arguments `num_elements` and `sizeof(long)` are checked before the call to `calloc()` to determine if wrapping will occur:
``` c
long *buffer;
size_t num_elements;
if (num_elements > SIZE_MAX/sizeof(long)) {
  /* Handle error condition */
}
buffer = (long *)calloc(num_elements, sizeof(long));
if (buffer == NULL) {
  /* Handle error condition */
}
```
Note that the maximum amount of allocatable memory is typically limited to a value less than `SIZE_MAX` (the maximum value of `size_t`). Always check the return value from a call to any memory allocation function in compliance with [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors).
## Risk Assessment
Unsigned integer wrapping in memory allocation functions can lead to buffer overflows that can be [exploited](BB.-Definitions_87152273.html#BB.Definitions-exploit) by an attacker to execute arbitrary code with the permissions of the vulnerable process. Most implementations of `calloc()` now check to make sure silent wrapping does not occur, but it is not always safe to assume the version of `calloc()` being used is secure, particularly when using dynamically linked libraries.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM07-C | High | Unlikely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | ALLOC.SIZE.MULOFLOW | Multiplication overflow of allocation size |
| Compass/ROSE |  |  |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM07-a | The validity of values passed to library functions shall be checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM07-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM07-CPP. Ensure that the arguments to calloc(), when multiplied, can be represented as a size_t |
| MITRE CWE | CWE-190, Integer overflow (wrap or wraparound)CWE-128, Wrap-around error |

## Bibliography

|  |  |
| ----|----|
| [RUS-CERT] | Advisory 2002-08:02, "Flaw in calloc and Similar Routines" |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |
| [Secunia] | Advisory SA10635, "HP-UX calloc Buffer Size Miscalculation Vulnerability" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152115) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152072)
## Comments:

|  |
| ----|
| Is there an entry on this site regarding the similar overflow in the C++ new[] operator?; I looked but couldn't find one.  By the way, gcc still does not check if new[] overflows. 
http://gcc.gnu.org/bugzilla/show_bug.cgi?id=19351
Microsoft's compiler does. 
http://blogs.msdn.com/michael_howard/archive/2005/12/06/500629.aspx
                                        Posted by drew at Mar 23, 2008 18:05
                                     |
| For the automatic detection, do we really expect everyone to have a size check before every call to calloc() even though it is only necessary on non C99 compliant systems?  Seems like we'll be flagging a lot of code that no one will want to change....
                                        Posted by avolkovi at Jul 10, 2008 10:48
                                     |
| I believe so, according to the letter of this rec.  Probably this is a rec, not a rule, because following it strictly is probably unreasonable.
We can add exceptions to this rule to mitigate its 'unreasonability'. For instance, one could forego the check if the product is known at compile time.
                                        Posted by svoboda at Jul 11, 2008 11:12
                                     |
| Is it worthwhile for this rule to also handle multiplications inside malloc() or realloc()?
eg
  foo_t* foo = (foo_t*) malloc(sizeof(foo_t) * number);

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 09, 2010 16:09
\| \|
> If the libraries used for a particular implementation properly handle unsigned integer wrapping on the multiplication, that is sufficient to comply with this recommendation.

Can we rewrite this to the following?
; "If the libraries ensure that all the code doing multiplication (including the code implementing calloc())  properly handle unsigned integer wrapping, that is sufficient to comply with this recommendation."
I think it means the library is compliant to "INT30-C. Ensure that unsigned integer operations do not wrap", hence an alternative phrase is
  " If the library is compliant to INT30-C, then it means that integer wrapping does not happen inside calloc(). In this case, the library is compliant to this recommendation."
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Aug 30, 2013 08:38
\| \|
I made a change which may not have been exactly what you were asking for, but which might clarify further.; In the narrow sense of this rule, it is only necessary for the a library to add one check for unsigned wrapping when multiplying the arguments provided to the calloc() function.  If this check has been added, the application programmer can ignore this recommendation safely (even if wrap around checks elsewhere in the library have not been inserted).
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 31, 2013 08:50
\| \|
This guideline became alot more reasonable with the inclusion of the "don't need to check if the library checks" clause.
Now I'm wondering if this shouldn't be promoted back to a rule?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 31, 2013 08:58
\| \|
This is not necessary, as it is covered by [INT30-C. Ensure that unsigned integer operations do not wrap](https://www.securecoding.cert.org/confluence/display/seccode/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap).; This rule is here because the offense occurs "off stage", in a standard library function.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 31, 2013 08:59
\| \|
It prob is worth promoting (although we should prob clarify which standards require an explicit multiplciation check.)
This rule may be another in the set of 'rules for older C platforms, but not C11 (what about C99?)'. AFAIK EXP35-C is the only other rule in that set.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 01, 2013 21:27
\| \|
I don't think the langauge in the standard ever changed. I think this is just a matter of common implementation practice, which changed after the vulnerbility was publicized.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 03, 2013 09:09
\|
