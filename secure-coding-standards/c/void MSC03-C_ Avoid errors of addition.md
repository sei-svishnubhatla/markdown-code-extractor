> [!warning]  
>
> This guideline has been deprecated by
>
> -   [EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement](EXP15-C_%20Do%20not%20place%20a%20semicolon%20on%20the%20same%20line%20as%20an%20if,%20for,%20or%20while%20statement)
> -   [MSC12-C. Detect and remove code that has no effect or is never executed](MSC12-C_%20Detect%20and%20remove%20code%20that%20has%20no%20effect%20or%20is%20never%20executed)

Errors of addition occur when characters are accidentally included, and the resulting code still compiles cleanly but behaves in an unexpected fashion.
This recommendation is related to [void MSC02-C. Avoid errors of omission](void%20MSC02-C_%20Avoid%20errors%20of%20omission) and [EXP00-C. Use parentheses for precedence of operation](EXP00-C_%20Use%20parentheses%20for%20precedence%20of%20operation).
## Noncompliant Code Example
This code block does nothing.
``` c
a == b;
```
It is almost always the case that the programmer mistakenly uses the equals operator `==` instead of the assignment operator `=`. Consequently, many compilers will warn about this condition.
## Compliant Solution
This code assigns the value of `b` to the variable `a`.
``` c
a = b;
```
## Noncompliant Code Example
The `{}` block is always executed because of the `;` following the `if` statement.
``` c
if (a == b); {
  /* ... */
}
```
It is almost always the case that the programmer mistakenly inserted the semicolon.
## Compliant Solution
This code executes the block only when `a` equals `b`.
``` c
if (a == b) {
  /* ... */
}
```
## Risk Assessment
Errors of addition can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC03-C | low | likely | medium | P6 | L2 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| LDRA tool suite | 9.7.1 | 5 S57 S
58 S
59 S | Fully implemented. |
| GCC | 4.3.5 | ; | Can detect violations of this recommendation when the -Wempty-body (enabled by -Wextra) and -Wall flags are used. |
| EDG Front End to Compass/ROSE | ; | ; | Can detect violations of this recommendation. |
| Compass/ROSE | ; | ; | Can detect violations of this recommendation. In particular, it flags statements that do not contain function calls or operations with side effects such as assignment. It also checks for if, do, while, or for statements with an empty body. |
| PRQA QA-C | Unable to render {include} The included page could not be found. | ; | Partially implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC03-C).
## Related Guidelines
[SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682): [VOID MSC03-CPP. Avoid errors of addition](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+MSC03-CPP.+Avoid+errors+of+addition)
[ISO/IEC TR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24772) "KOA Likely incorrect expressions"
[MITRE CWE](http://cwe.mitre.org/): [CWE-480](http://cwe.mitre.org/data/definitions/480.html), "Use of incorrect operator"
## Sources
\[[Hatton 1995](AA.-Bibliography_87152170.html#AA.Bibliography-Hatton95)\] Section 2.7.2, "Errors of omission and addition"
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MSC02-C.+Avoid+errors+of+omission?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=362) [](https://www.securecoding.cert.org/confluence/display/seccode/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| It should be noted that many compilers will warn about a==b;
                                        Posted by dagwyn at Apr 18, 2008 13:44
                                     |
| This issue has been addressed.
                                        Posted by avolkovi at May 19, 2008 15:02
                                     |

