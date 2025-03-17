Make sure that included header file names are unique. According to the C Standard, subclause 6.10.2, paragraph 5 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> The [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) shall provide unique mappings for sequences consisting of one or more nondigits or digits (6.4.2.1) followed by a period (.) and a single nondigit. The first character shall not be a digit. The implementation may ignore distinctions of alphabetical case and restrict the mapping to eight significant characters before the period.

This means that
-   Only the first eight characters in the file name are guaranteed to be significant.
-   The file has only one nondigit character after the period in the file name.
-   The case of the characters in the file name is not guaranteed to be significant.
To guarantee that header file names are unique, all included files should differ (in a case-insensitive manner) in their first eight characters or in their (one-character) file extension.
Note that compliance with this recommendation does not require that short file names are used, only that the file names are unique.
## Noncompliant Code Example
This noncompliant code example contains references to headers that may exist independently in various environments but can be ambiguously interpreted by a C-compliant compiler:
``` c
#include "Library.h"
#include <stdio.h>
#include <stdlib.h>
#include "library.h"
#include "utilities_math.h"
#include "utilities_physics.h"
#include "my_library.h"
/* ... */
```
`Library.h` and `library.h` may refer to the same file. Also, because only the first eight characters are guaranteed to be significant, it is unclear whether `utilities_math.h` and `utilities_physics.h` are parsed. Finally, if a file such as `my_libraryOLD.h` exists, it may inadvertently be included instead of `my_library.h`.
## Compliant Solution
This compliant solution avoids the ambiguity by renaming the associated files to be unique under the preceding constraints:
``` c
#include "Lib_main.h"
#include <stdio.h>
#include <stdlib.h>
#include "lib_2.h"
#include "util_math.h"
#include "util_physics.h"
#include "my_library.h"
/* ... */
```
The only solution for mitigating ambiguity of a file, such as `my_libraryOLD.h`, is to rename old files with either a prefix (that would fall within the first eight characters) or add an extension (such as `my_library.h.old`).
## Exceptions
**PRE08-C-EX1:** Although the C Standard requires only the first eight characters in the file name to be significant, most modern systems have long file names, and compilers on such systems can typically differentiate them. Consequently, long file names in headers may be used, provided that all the implementations to which the code is ported can distinguish between these file names.
## Risk Assessment
Failing to guarantee uniqueness of header files may result in the inclusion of an older version of a header file, which may include incorrect macro definitions or obsolete function prototypes or result in other errors that may or may not be detected by the compiler. Portability issues may also stem from the use of header names that are not guaranteed to be unique.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE08-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE08 |  |
| ECLAIR | 1.2 | CC2.PRE08 | Fully implemented |
| Helix QAC | 2024.4 | C5002 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE08-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE08-CPP. Guarantee that header file names are unique |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.10.2, "Source File Inclusion" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152056) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152166)
## Comments:

|  |
| ----|
| I wonder if there should be a discussion of the "subdir/header.h" notation, or the distinction between <header.h> and "header.h"?
                                        Posted by jonathan.leffler@gmail.com at Mar 22, 2008 01:53
                                     |
| I added an exception as suggested above.
What do you want to say about "subdir/header.h" notation, or the distinction between <header.h> and "header.h"?
We are trying to omit "reference" material, unless we want to make a recommendation or rule concerning how it is to be used.
                                        Posted by rcs at May 05, 2008 01:16
                                     |
| 1.  Would the following code violate this guideline?
#include "a/b.h"
#include "c/b.h"
#include "b.h"

2\. How about:
``` java
#include <d.h>
#include "d.h"
```
?
3\. I have seen some compilers automatically append file extensions to header names mentioned in #include directives. Suppose a less experienced Programmer codes these lines:
``` java
#include "e.h"
#include "e"
```
if the compiler finds a file called 'e.h' for the second directive, does the code then violate this guideline?
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 27, 2009 13:24
\| \|
My opinion would be:
1\. no. 2. yes.  
3. yes.
The **intent** of this guideline is to diagnose situations in which a developer may not be including the intended file.
I tried to capture this idea under "False Positives" on the [Tool Selection and Validation](Tool%20Selection%20and%20Validation) page. However, this is still a work in progress. I'm pondering what it means for a tool to conform with this standard, and what is a quality of implementation issue. Perhaps you can help.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Feb 28, 2009 13:34
\| \|
> The intent of this guideline is to diagnose situations in which a developer may not be including the intended file.

Agreed. I think perhaps we should focus more on this intent and less on including a duplicate file. I just saw an example C file which purposely includes the same .h file twice. The first include has a certain macro undefined, and the second include has it defined. Duplicate header inclusion is not necessarily a Bad Thing, the bad thing is when you include the wrong file.
Also, since C99 leaves the details of what constitutes a unique header identifier as implementation-defined, the answers to Frank's queries vary from system to system, and you can create a system where all three questions can be answered 'no' and another system where all three questions can be answered 'yes'.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 02, 2009 16:42
\|
