Parenthesize all parameter names in macro definitions. See also [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros) and [PRE02-C. Macro replacement lists should be parenthesized](PRE02-C_%20Macro%20replacement%20lists%20should%20be%20parenthesized).
## Noncompliant Code Example
This `CUBE()` macro definition is noncompliant because it fails to parenthesize the parameter names:
``` c
#define CUBE(I) (I * I * I)
```
As a result, the invocation
``` c
int a = 81 / CUBE(2 + 1);
```
expands to
``` c
int a = 81 / (2 + 1 * 2 + 1 * 2 + 1);  /* Evaluates to 11 */
```
which is clearly not the desired result.
## Compliant Solution
Parenthesizing all parameter names in the `CUBE()` macro allows it to expand correctly (when invoked in this manner):
``` c
#define CUBE(I) ( (I) * (I) * (I) )
int a = 81 / CUBE(2 + 1);
```
## Exceptions
**PRE01-C-EX1:** When the parameter names are surrounded by commas in the replacement text, regardless of how complicated the actual arguments are, there is no need for parenthesizing the macro parameters. Because commas have lower precedence than any other operator, there is no chance of the actual arguments being parsed in a surprising way. Comma separators, which separate arguments in a function call, also have lower precedence than other operators, although they are technically different from comma operators.
``` java
#define FOO(a, b, c) bar(a, b, c)
/* ... */
FOO(arg1, arg2, arg3);
```
**PRE01-C-EX2:** Macro parameters cannot be individually parenthesized when concatenating tokens using the `##` operator, converting macro parameters to strings using the `#` operator, or concatenating adjacent string literals. The following `JOIN()` macro concatenates both arguments to form a new token. The `SHOW()` macro converts the single argument into a string literal, which is then passed as a parameter to `printf()` and as a string and as a parameter to the `%d` specifier. For example, if `SHOW()` is invoked as `SHOW(66);`, the macro would be expanded to `printf("66" " = %d\n", 66);`.
``` java
#define JOIN(a, b) (a ## b)
#define SHOW(a) printf(#a " = %d\n", a)
```
See [PRE05-C. Understand macro replacement when concatenating tokens or performing stringification](PRE05-C_%20Understand%20macro%20replacement%20when%20concatenating%20tokens%20or%20performing%20stringification) for more information on using the `##` operator to concatenate tokens.
## Risk Assessment
Failing to parenthesize the parameter names in a macro can result in unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE01-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | macro-parameter-parentheses | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE01 | Fully implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-pre01-c | ; |
| ECLAIR | 1.2 | CC2.PRE01 | Fully implemented |
| Helix QAC | 2024.4 | C3410 |  |
| Klocwork | 2024.4 | MISRA.DEFINE.NOPARS |  |
| LDRA tool suite | 9.7.1 | 78 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE01-a | In the definition of a function-like macro each instance of a parameter shall be enclosed in parentheses unless it is used as the operand of # or ## |
| PC-lint Plus | 1.4 | 9022 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE01-C | Checks for expanded macro parameters not enclosed in parentheses (rule partially supported) |
| PVS-Studio | 7.35 | V733 |  |
| RuleChecker | 24.04 | macro-parameter-parentheses | Fully checked |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE01-CPP. Use parentheses within macros around parameter names |
| ISO/IEC TR 24772:2013 | Operator Precedence/Order of Evaluation [JCW]Pre-processor Directives  [NMP]  |
| MISRA C:2012 | Rule 20.7 (required) |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] |  |
| [Summit 2005] | Question 10.1 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152416) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152384)
## Comments:

|  |
| ----|
| This example:
#define SHOW(a) printf(#a " = %d\n", a)
gives wrong behavior for calls like SHOW(i%j).  It should be replaced with
#define SHOW(a) printf("%s = %d\n", #a, a)
                                        Posted by andersk at Mar 24, 2008 04:40
                                     |
| Silly question, why is this a rec & not a rule? It is easily enforceable by inspecting your #define statements, failure often yields unintended behavior, and you have a small list of exceptions.
                                        Posted by svoboda at Apr 10, 2008 17:41
                                     |
| RCS sez:
> so the distinction between a rule and a recommendation is a fairly gray area.  the best way i can describe it is in terms of remediation of an existing system.  if you can tell a software development manager that he should go back and spend $$$ to repair some problem, it is probably a rule.  if you can't make this argument, it is probably a recommendation.

in this specific case, failing to "Use parentheses within macros around parameter names" does not in itself constitute an error. the error occurs when this macro is used in a certain way.  although this is not the exact same thing, pre31-C gives an example of a rule:
PRE31-C. Never invoke an unsafe macro with arguments containing assignment, increment, decrement, volatile access, or function call
it is very hard to write the corresponding rule here.... don't call a macro if the arguments may expand in an unintended manner.
we could in fact reclassify this if you feel strongly.  right now, the main reason not to (besides my argument above) is that moving it now would result in having to shuffle a bunch of things around.
rCs
                                        Posted by svoboda at May 15, 2008 13:47
                                     |
| I think the MISRA C 2012 mapping is to 20.7 (required) rather than 20.1 ?
                                        Posted by amycgale at Aug 01, 2014 14:36
                                     |
| (on behalf of MISRA-C Working Group).; You are correct that Rule 20.7 is the appropriate mapping.One difference with the CERT rule is that the MISRA C:2012 rule does not require parenthesis within the macro definition. So the following would also be compliant in MISRA#define CUBE(I) ( I * I * I )int a = 81 / CUBE( (2 + 1) );
                                        Posted by liz.whiting@ldra.com at Sep 19, 2014 07:00
                                     |

