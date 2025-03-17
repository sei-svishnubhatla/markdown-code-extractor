If a file with the same name as a standard header is placed in the search path for included source files, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
The following table from the C Standard, subclause 7.1.2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], lists these standard headers:

|  |  |  |  |  |  |
| ----|----|----|----|----|----|
| <assert.h> | <float.h> | <math.h> | <stdatomic.h> | <stdlib.h> | <time.h> |
| <complex.h> | <inttypes.h> | <setjmp.h> | <stdbool.h> | <stdnoreturn.h> | <uchar.h> |
| <ctype.h> | <iso646.h> | <signal.h> | <stddef.h> | <string.h> | <wchar.h> |
| <errno.h> | <limits.h> | <stdalign.h> | <stdint.h> | <tgmath.h> | <wctype.h> |
| <fenv.h> | <locale.h> | <stdarg.h> | <stdio.h> | <threads.h> |  |

Do not reuse standard header file names, system-specific header file names, or other header file names.
## Noncompliant Code Example
In this noncompliant code example, the programmer chooses to use a local version of the standard library but does not make the change clear:
``` c
#include "stdio.h"  /* Confusing, distinct from <stdio.h> */
/* ... */
```
## Compliant Solution
The solution addresses the problem by giving the local library a unique name (per [PRE08-C. Guarantee that header file names are unique](PRE08-C_%20Guarantee%20that%20header%20file%20names%20are%20unique)), which makes it apparent that the library used is not the original:
``` c
/* Using a local version of stdio.h */ 
#include "mystdio.h"
/* ... */
```
## Risk Assessment
Using header file names that conflict with other header file names can result in an incorrect file being included.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE04-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE04 |  |
| Cppcheck Premium | 24.11.0 | premium-cert-pre04-c |  |
| ECLAIR | 1.2 | CC2.PRE04 | Fully implemented |
| Helix QAC | 2024.4 | C5001 |  |
| LDRA tool suite | 9.7.1 | 568;S | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE04-CPP. Do not reuse a standard header file name |
| CERT Oracle Secure Coding Standard for Java | DCL01-J. Do not reuse public identifiers from the Java Standard Library |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.1.2, "Standard Headers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152383) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152353)
## Comments:

|  |
| ----|
| The intent seems to be "don't mislead".; Suppose you are using coding practices that would be secure if all standard items were using their usual names.  Suppose some bozo on the same project has reused a standard include file name, to name a header file he wrote.  Suppose that header file redefines something standard, to something less secure.  A layer of your careful defense gets defenestrated.  The violation itself doesn't necessary lead to a security hole, but it can pave the way for something that does.
                                        Posted by davearonson at Jan 03, 2008 14:25
                                     |
| This rule attempts to avoid landmines for the next developer down the line: if you have your own (say) stdio.h for some purpose, it may not be obvious to the followon dev that something special is going on here. If you need your own header to modify or redefine something in a standard, then you'd make a different name (say, "mystdio.h") that does what you like.
This is probably most common with "assert.h" - people define their own assertion mechanism (perhaps with somewhat different semantics) - and this could lead to a surprise.
Programmers who are surprised are rarely coding their best, though it's not always clear how to unblur the line between "good coding" and "secure coding".
                                        Posted by steve at Mar 13, 2008 20:00
                                     |
| Should this recommendation mention examples like the POSIX headers?  Should there be a recommendation (or, not as strong, a suggestion) about using "project/header.h" notation for header files?
I should have mentioned this before, too.  Do you need to allow an exception for headers provided to cover up a flawed implementation?  For example, <inttypes.h> might not be available in some platforms (without C99 support), and it is relatively easy write a private implementation of it for any of the architectures.  Granted, the target for this standard is C99 so the specific example is not all that good, but it is a real-world example that could still apply because the platform does not have C99 support still.  Any exception would have to be heavily qualified or caveated to explain that is not good.
Has any item anywhere covered "do not modify system headers"?  I came across a piece of code recently that had:
[!note]
#ifdef HP
#ifndef TIONCTTY
#define TIONCTTY _IO('t', 113)    /* Copied from /usr/include/sys/ioctl.h */
#endif
#endif
    ioctl(fd, TIOCNTTY, 0);

The claim that is was copied from was not referring to the header on HP - I've not located which system it is from because I don't care. OK - it didn't actually modify the system header - but the intent was the same. And HP-UX does not support the `TIOCNTTY ioctl()` so there was no point in trying to do it. Further, of course, there was no checking of the return code - though there's no guarantee that the value wasn't a "real" `ioctl` that did something else. There have been other cases where people have tried to modify inconvenient headers on a given platform - this is a discipline problem too, but nonetheless an issue for that.
Finally, do you need to beware of automatically adding verbiage in response to suggestions so that the standard becomes too long? (Of course, (wrap in XML tag jest mode="ironic" seriousness="nil")"my" suggestions are always absolutely incredibly valuable and you'd never want to consider leaving them out, but other people's ...(end XML jest tag)). \[I tried using literal XML notation; it doesn't appear in the Wiki output.\]
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 16, 2008 11:55
\| \|
It should probably be noted that because of deficiencies in implementations of standard headers, one defensible practice is to always use the "" form for including standard headers, which allows the porter to substitute a modified copy of the deficient standard header when necessary.; (Not all problems can be solved merely by #ifdefs.)  While this isn't an ideal approach, it may be necessary in order to get the job done.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 11, 2008 14:13
\| \|
After reading all of the comments, it seems to me like we should perhaps rewrite this rule along the lines of "Be aware of exactly what headers you are including, and if for some reason you are doing something out of the ordinary be VERY explicit about it"
;Does anyone else agree that our intended meaning is not really obvious to someone just reading the rule?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 10:58
\| \|
Looks like my concern is mostly addressed by [PRE08-C. Guarantee that header file names are unique](PRE08-C_%20Guarantee%20that%20header%20file%20names%20are%20unique)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 11:45
\|
