When developing new code, declare functions that return `errno` with a return type of `errno_t`.  Many existing functions that return `errno` are declared as returning a value of type `int`. It is semantically unclear by inspecting the function declaration or prototype if these functions return an error status or a value or, worse, some combination of the two. (See [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).)
C11 Annex K  introduced the new type `errno_t` that is defined to be type `int` in `errno.h` and elsewhere. Many of the functions defined in C11 Annex K return values of this type. The `errno_t` type should be used as the type of an object that may contain only values that might be found in `errno`. For example, a function that returns the value of `errno` should be declared as having the return type `errno_t`.
This recommendation depends on C11 Annex K being implemented. The following code can be added to remove this dependency:
``` cpp
#ifndef __STDC_LIB_EXT1__
  typedef int errno_t;
#endif
```
## Noncompliant Code Example
This noncompliant code example shows a function called `opener()` that returns `errno` error codes. However, the function is declared as returning an `int`. Consequently, the meaning of the return value is not readily apparent.
``` c
#include <errno.h>
#include <stdio.h>
enum { NO_FILE_POS_VALUES = 3 };
int opener(
  FILE *file,
  size_t *width,
  size_t *height,
  size_t *data_offset
) {
  size_t file_w;
  size_t file_h;
  size_t file_o;
  fpos_t offset;
  if (file == NULL) { return EINVAL; }
  errno = 0;
  if (fgetpos(file, &offset) != 0) { return errno; }
  if (fscanf(file, "%zu %zu %zu", &file_w, &file_h, &file_o)
        != NO_FILE_POS_VALUES) {
    return -1;
  }
  errno = 0;
  if (fsetpos(file, &offset) != 0) { return errno; }
  if (width != NULL) { *width = file_w; }
  if (height != NULL) { *height = file_h; }
  if (data_offset != NULL) { *data_offset = file_o; }
  return 0;
}
```
This noncompliant code example nevertheless complies with [ERR30-C. Take care when reading errno](ERR30-C_%20Take%20care%20when%20reading%20errno).
## Compliant Solution (POSIX)
In this compliant solution, the `opener()` function returns a value of type `errno_t`, providing a clear indication that this function returns an error code:
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
enum { NO_FILE_POS_VALUES = 3 };
errno_t opener(
  FILE *file,
  size_t *width,
  size_t *height,
  size_t *data_offset
) {
  size_t file_w;
  size_t file_h;
  size_t file_o;
  fpos_t offset;
  if (NULL == file) { return EINVAL; }
  errno = 0;
  if (fgetpos(file, &offset) != 0 ) { return errno; }
  if (fscanf(file, "%zu %zu %zu", &file_w, &file_h, &file_o)
        != NO_FILE_POS_VALUES) {
    return EIO;
  }
  errno = 0;
  if (fsetpos(file, &offset) != 0 ) { return errno; }
  if (width != NULL) { *width = file_w; }
  if (height != NULL) { *height = file_h; }
  if (data_offset != NULL) { *data_offset = file_o; }
  return 0;
}
```
This compliant solution is categorized as a POSIX solution because it returns `EINVAL and ``EIO`` `, which are defined by POSIX (IEEE Std 1003.1, 2013 Edition) but not by the C Standard.
## Risk Assessment
Failing to test for error conditions can lead to [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) of varying severity. Declaring functions that return an `errno` with a return type of `errno_t` will not eliminate this problem but may reduce errors caused by programmers' misunderstanding the purpose of a return value.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL09-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL09 |  |
| LDRA tool suite | ;9.7.1 | 634 S | Partially Implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL09-CPP. Declare functions that return errno with a return type of errno_t |
| ISO/IEC TR 24772:2013 | Ignored Error Status and Unhandled Exceptions [OYB] |

## Bibliography

|  |
| ----|
| [IEEE Std 1003.1:2013] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152145) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152093)
## Comments:

|  |
| ----|
| I submit that there is only one errno - and that is the one declared by .  Other functions return an error number, often as a type int that should be typedef'd as errno_t or equivalent.
Based on historic precedent, the POSIX standard is bad about conflating return status and real values - starting with functions like open, read, and write and progressing onwards.
I would not be happy about a function that returned EIO for a format error - that should be reserved for its original purpose, which was a device failure.;
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 15:21
                                     |
| I suppose that EIO for a format error would be confusing, but if it's *part of the contract* for that function, it's probably not so bad.
                                        Posted by steve at Mar 15, 2008 16:13
                                     |
| What is a better choice for a return value for this example?  
                                        Posted by rcs at Mar 16, 2008 22:14
                                     |
| There are portability problems with the use of the name errno_t.; Conforming C99 implementations do not define it in <errno.h>. Some implementations may have a way of enabling a non-conforming variation of the compiler which does define it, but applications cannot rely on that.  Therefore applications would have to define errno_t themselves.  This is fine for pure C99 applications but not for POSIX applications, since POSIX reserves all identifiers ending with _t for the implementaion (if any standard header is included).  So a POSIX application which defines errno_t runs the risk of not being portable to some POSIX implementations.
One way to solve the problem would be to recommend the application define a type name to use that does not end in _t.  You could also mention that at some point in the future the type errno_t may be adopted into the C standard from TR 24731-1 and it could then be used for this purpose.
                                        Posted by geoffclare at Mar 19, 2008 08:09
                                     |
| Using errno_t is safe.; First of all, it comes from those of us in WG14, the C committee, so it is not going to conflict with C.  Secondly, POSIX has a liaison who attends WG14 meetings regularly, and whose input was required for producing TR 24731-1, so if there were going to be any POSIX conflicts, we would know about it.  There is no need for an interim solution, which would just complicate code.  People can jump right in.
                                        Posted by dmk at Mar 19, 2008 14:22
                                     |
| I agree there is no conflict with C (which is why I wrote "This is fine for pure C99 applications").; I also agree there is no conflict between POSIX and TR 24731-1.  The problem is that there is currently no way to write a conforming POSIX application which uses the name errno_t (and includes any standard header).
An application which uses errno_t either has to assume that the implementation defines it (which POSIX allows but does not require, and therefore this assumption makes the application non-conforming), or it has to define errno_t itself (which POSIX forbids, because all names ending with _t are in the name space reserved for use by the implementation's headers).
                                        Posted by geoffclare at Mar 20, 2008 07:01
                                     |
| To solve this problem it is necessary to think about the spirit of the restriction.; Why is it nonconforming to define a name ending in _t?  Because POSIX or C might want to define new ones that could have a different meaning than the user's definition.  But errno_t is one of those new ones.  As long as the name is used in the same way that TR 24731-1 intends, it is unimportant whether that makes the code technically nonconforming, because the spirit of that restriction is being observed.
One way to handle this situation is to define it temporarily, for example, with something like the following.
#ifdef NO_SYSTEM_ERRNO_T
typedef int errno_t;
#endif

Then a configure script can define `NO_SYSTEM_ERRNO_T` if it probes the system on which the code is about to be compiled and finds `errno_t` missing.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 21, 2008 23:38
\| \|
It is entirely possible for a POSIX system to exist which predates TR 24731-1 and which uses the name errno_t for some completely different purpose. Your hypothetical configure script would not be able to handle this situation. Using a different name instead of one ending with \_t would both avoid the original problem and avoid the need for a configuration script.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 25, 2008 12:20
\| \|
If such a system existed and were commercially viable, it would have prompted the POSIX liaison to WG14 to raise the issue when TR 24731-1 was being drafted.
Also, the need for a configure script would not be avoided by changing names. The point is to use the same `errno_t` as TR 24731-1, so if a different name were used, there would still have to be some scaffolding to connect the different name with `errno_t` when possible.
In addition, using a different name would defeat the purpose of documenting at each function declaration and definition that this function returns exactly the same kind of value as TR 24731-1's `errno_t`.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 25, 2008 12:27
\| \|
If such a system existed, it would **not** have prompted the POSIX liaison to WG14 to raise an issue over TR 24731.; Namespace clashes between the standard and existing implementations have happened in the past and will happen again in future.  They are easily dealt with by the affected implementors simply by making the standard contents visible in headers when any standard feature-test macros (\_POSIX_C_SOURCE and/or \_XOPEN_SOURCE) are defined, and historical contents visible when no standard feature-test macros are defined.
Also POSIX had more serious concerns with TR 24731 to raise; a simple (and easily solvable) namespace clash with an existing implementation would not have merited inclusion.  See <http://www.opengroup.org/austin/docs/austin_250.txt>
I really don't see the importance of using the name errno_t from TR 24731-1. The stated purpose of documenting that a function returns an errno value can just as well be achieved by using a type name such as errno_val, errno_type or errno_T.  If and when TR 24731-1 is adopted into the C Standard, **that** will be the time to recommend the use of errno_t, not now.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 26, 2008 08:55
\| \|
As discussed in [Scope](Scope), this document takes the long-term view, and is concerned with C99 and its TRs.; In the long run, everyone will be able to include a system header and get `errno_t`.  An alternate name would clutter every single relevant function declaration and definition with a temporary fix for a theoretical problem that does not exist in reality.  That is not in the spirit of this document.
Also along the lines of taking the long-term view, this document will eventually become a WG14 TR, and it is a safe bet that WG14 will not be recommending the avoidance of one of its own type names. 
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 26, 2008 09:15
\| \|
I guess I owe you an apology.; If I had taken note of that part of the scope before, then I wouldn't have pushed the portability issue.
It might help other readers not to fall into the same trap if the reliance on TR 24731-1 is made clear.  For example the existing "NOTE" under the compliant code could be extended to say something like "Note also that this code is only portable to systems that implement TR 24731-1."
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 26, 2008 13:22
\| \|
Apology accepted, though it wasn't required.; I added a note more toward the top of the recommendation, to clarify the global nature of the reference to TR 24731-1.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 26, 2008 13:58
\| \|
Every substantial portable C;program would benefit from using a `"config.h"` header that is tailored to fit each platform. Then `"config.h"` can define `errno_t` where necessary and not where not necessary.
Another approach for handling variation among implementations of standard headers is to always `#include "errno.h"` (the "..." form) and on platforms where necessary, add to the project a local file:
``` java
/* errno.h -- interface to <errno.h> */
#include <errno.h>
typedef int errno_t;
```
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 12:20
\| \|
Re: config.h. Wasn't that one of the raison d'etres for GNU autoconf?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 15, 2008 13:39
\| \|
The beginning of the page has the table "Warning: This section is under construction."
is this the intended one?; or, should be removed?
![](images/icons/contenttypes/comment_16.png) Posted by yozo at May 29, 2013 23:26
\| \|
It was probably intended, because this recommendation was a bit rough.; I took a pass at it, removed the under contruction label, but added a review label.  Please have a look.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 16, 2013 16:42
\| \|
I've reviewed the content, and AFAICT, the only thing really missing is a CS that doesn't require POSIX.; Then again, I'm not 100% certain such an example would add much benefit either.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 17, 2013 13:18
\| \|
Think this is fine as is, I agree that another example will not really add much.
![](images/icons/contenttypes/comment_16.png) Posted by bluepilot at Sep 17, 2013 15:21
\| \|
Then I signed off as reviewed once.; Thanks for the confirmation!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 17, 2013 16:45
\|
