If a constant value is given for an identifier, do not diminish the maintainability of the code in which it is used by assuming its value in expressions. Simply giving the constant a name is not enough to ensure modifiability; you must be careful to always use the name, and remember that the value can change. This recommendation is related to [DCL06-C. Use meaningful symbolic constants to represent literal values](DCL06-C_%20Use%20meaningful%20symbolic%20constants%20to%20represent%20literal%20values).
## Noncompliant Code Example
The header `stdio.h` defines the `BUFSIZ` macro, which expands to an integer constant expression that is the size of the buffer used by the `setbuf()` function. This noncompliant code example defeats the purpose of defining `BUFSIZ` as a constant by assuming its value in the following expression:
``` c
#include <stdio.h>
/* ... */
nblocks = 1 + ((nbytes - 1) >> 9); /* BUFSIZ = 512 = 2^9 */
```
The programmer's assumption underlying this code is that "everyone knows that `BUFSIZ` equals 512," and right-shifting 9 bits is the same (for positive numbers) as dividing by 512. However, if `BUFSIZ` changes to 1024 on some systems, modifications are difficult and error prone.
## Compliant Solution
This compliant solution uses the identifier assigned to the constant value in the expression:
``` c
#include <stdio.h>
/* ... */
nblocks = 1 + (nbytes - 1) / BUFSIZ;
```
Most modern C compilers will optimize this code appropriately.
## Risk Assessment
Assuming the value of an expression diminishes the maintainability of code and can produce [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) under any circumstances in which the constant changes.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP07-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP07 |  |
| Helix QAC | 2024.4 | C3120, C3121, C3122, C3123, C3131, C3132 |  |
| LDRA tool suite | 9.7.1 | 201 S | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP07-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP07-CPP. Do not diminish the benefits of constants by assuming their values in expressions |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] | Rule 1-5 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152191) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152126)
## Comments:

|  |
| ----|
| I think the example should include
[!note]
enum { BUFSIZ = 512 };

in the non-compliant code (and, presumably, the compliant code would include it too).
\[First attempt wrote the preformatted box inline, and then appeared with 'unknown macro' in the Wiki markup.\] 
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 15, 2008 22:18
\| \|
I would suggest mentioning the alternative compliant solution of introducing a second constant BUFSIZ_SHIFT with the value 9. This approach seems fairly common.
![](images/icons/contenttypes/comment_16.png) Posted by josh@freedesktop.org at Mar 16, 2008 06:45
\| \|
I added an explanation of where BUFSIZ is defined. I think this should address the initial concern.
I didn't add the BUFSIZ_SHIFT compliant solution, common as it may be. At some point I thought we had started a recommendation to avoid performing bitwise operations on arithmetic values, and vice versa, although I can not find it now.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 16, 2008 11:02
\| \|
BUFSIZ is not allowed to be defined as an enumeration constant.
;The talk about BUFSIZE_SHIFT brings up the point that C could benefit from a log-base-2 operator.  Anyway, in general:
#define X_OFFSET 9u  // the "u" is important for bitwise operations  
#define X_SIZE (1\<\<X_OFFSET)
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 14:39
\| \|
I don't see that any changes are required in response to this comment.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 16, 2008 09:13
\|
