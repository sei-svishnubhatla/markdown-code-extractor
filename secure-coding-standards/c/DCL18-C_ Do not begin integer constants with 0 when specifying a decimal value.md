The C Standard defines octal constants as a 0 followed by octal digits (0 1 2 3 4 5 6 7). Programming errors can occur when decimal values are mistakenly specified as octal constants.
## Noncompliant Code Example
In this noncompliant code example, a decimal constant is mistakenly prefaced with zeros so that all the constants are a fixed length:
``` c
i_array[0] = 2719;
i_array[1] = 4435;
i_array[2] = 0042;
```
Although it may appear that `i_array[2]` is assigned the decimal value 42, it is actually assigned the decimal value 34.
## Compliant Solution
To avoid using wrong values and to make the code more readable, do not preface constants with zeroes if the value is meant to be decimal:
``` c
i_array[0] = 2719;
i_array[1] = 4435;
i_array[2] =   42;
```
## Risk Assessment
Misrepresenting decimal values as octal can lead to incorrect comparisons and assignments.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL18-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | octal-constant | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL18 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.OC | Octal constant |
| Helix QAC | 2024.4 | C0339, C1272 |  |
| Klocwork | 2024.4 | MISRA.TOKEN.OCTAL.ESCAPEMISRA.TOKEN.OCTAL.INT |  |
| LDRA tool suite | ;9.7.1 | 83 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL18-aCERT_C-DCL18-b | Octal and hexadecimal escape sequences shall be terminatedOctal constants (other than zero) shall not be used |
| PC-lint Plus | 1.4 | 9001 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL18-C | Checks for use of octal constants (rec. fully covered) |
| PVS-Studio | 7.35 | V536 |  |
| RuleChecker | 24.04 | octal-constant | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | OctalConstantAndSequence |  |

## Related Guidelines

|  |  |
| ----|----|
| MISRA C:2012 | Rule 7.1 (required) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152269) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152335)
## Comments:

|  |
| ----|
| Victor, this looks like a good rule to work on. Comments:
    I emailed an announcement a few days ago with some style guidelines...please study them and have the rule conform to them.
    Your code should be expressed as non-compliant code example + compliant solution...should be fairly simple to tweak your current code.
    Some relevant discussion in the comments of DCL16-C. Use 'L', not 'l', to indicate a long value
                                        Posted by svoboda at Mar 29, 2009 10:50
                                     |
| I'm wondering how we can make this more enforceable.  The NCE shows decimal constants and octal constants being assigned to different elements of an array.  It would be easier to enforce that constraint.  Also, we could insist that for any given variable, it can only be assigned and or compared to decimal or octal constants but not both.  Opinions?
                                        Posted by rcs at Jul 22, 2009 09:48
                                     |
| You're talking as if decimal and octoal ints were actually two different types. That is, conversions between one and the other should be explicit. Sounds like a good idea to me. C99 doesn't distinguish them, of course, but a SA tool could.
                                        Posted by svoboda at Jan 28, 2011 13:14
                                     |
| I think that would lead to large numbers of false positives. For example, it's not uncommon to define INT_MAX to a decimal number (e.g., 2147483647) but UINT_MAX to hexadecimal (e.g., 0xffffffff).
                                        Posted by martinsebor at Jan 30, 2011 19:34
                                     |

