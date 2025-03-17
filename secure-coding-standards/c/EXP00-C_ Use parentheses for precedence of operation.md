C programmers commonly make errors regarding the precedence rules of C operators because of the unintuitive low-precedence levels of `&`, `|`, `^`, `<<`, and `>>`. Mistakes regarding precedence rules can be avoided by the suitable use of parentheses. Using parentheses defensively reduces errors and, if not taken to excess, makes the code more readable.
Subclause 6.5 of the C Standard defines the precedence of operation by the order of the subclauses.
## Noncompliant Code Example
The intent of the expression in this noncompliant code example is to test the least significant bit of `x`:
``` c
x & 1 == 0
```
Because of operator precedence rules, the expression is parsed as
``` c
x & (1 == 0)
```
which evaluates to
``` c
(x & 0)
```
and then to `0`.
## Compliant Solution
In this compliant solution, parentheses are used to ensure the expression evaluates as expected:
``` c
(x & 1) == 0
```
## Exceptions
**EXP00-C-EX1:** Mathematical expressions that follow algebraic order do not require parentheses. For instance, in the expression
``` java
x + y * z
```
the multiplication is performed before the addition by mathematical convention. Consequently, parentheses to enforce the algebraic order would be redundant:
``` c
x + (y * z)
```
## Risk Assessment
Mistakes regarding precedence rules may cause an expression to be evaluated in an unintended way, which can lead to [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and abnormal program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP00-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP00 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.PARENS | Missing Parentheses |
| ECLAIR | 1.2 | CC2.EXP00 | Fully implemented |
| Helix QAC | 2024.4 | C3389, C3390, C3391, C3392, C3393, C3394, C3395, C3396, C3397, C3398, C3399, C3400 |  |
| Klocwork | 2024.4 | CERT.EXPR.PARENS |  |
| LDRA tool suite | 9.7.1 | 361 S, 49 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP00-a | Use parenthesis to clarify expression order if operators with precedence lower than arithmetic are used |
| PC-lint Plus | 1.4 | 9050 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP00-C | Checks for possible unintended evaluation of expression because of operator precedence rules (rec. fully covered) |
| PVS-Studio | 7.35 | V502, V593, V634, V648, V1104 |  |
| SonarQube C/C++ Plugin | 3.11 | S864 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP00-CPP. Use parentheses for precedence of operation |
| ISO/IEC TR 24772:2013 | Operator Precedence/Order of Evaluation [JCW] |
| MISRA C:2012 | Rule 12.1 (advisory) |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Precedence," pp. 287–288) |
| [Kernighan 1988] |  |
| [NASA-GB-1740.13] | Section 6.4.3, "C Language" |

------------------------------------------------------------------------
[](../c/Rec_%2003_%20Expressions%20_EXP_) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152061)
## Comments:

|  |
| ----|
| Good rule of thumb: if you have to look at an operator precedence chart to *write* your code, then so will your reader; add parens if there is any doubt.
                                        Posted by steve at Mar 14, 2008 13:33
                                     |
| Sound advice indeed.
Is the assignment operator (especially in conditions) addressed separately?
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 21:39
                                     |
| Yes, in MSC02-A.
                                        Posted by svoboda at Apr 17, 2008 11:09
                                     |
| added exception for standard algebraic precedence.
                                        Posted by svoboda at Apr 17, 2008 11:34
                                     |

