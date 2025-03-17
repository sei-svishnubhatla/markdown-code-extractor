The three types `char`, `signed char`, and `unsigned char` are collectively called the *character types*. Compilers have the latitude to define `char` to have the same range, representation, and behavior as *either* `signed char` or `unsigned char`. Irrespective of the choice made, `char` is a separate type from the other two and is *not* compatible with either.
Use only `signed char` and `unsigned char` types for the storage and use of numeric values because it is the only portable way to guarantee the signedness of the character types (see [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type) for more information on representing characters).
## Noncompliant Code Example
In this noncompliant code example, the `char`-type variable `c` may be signed or unsigned. Assuming 8-bit, two's complement character types, this code may print out either `i/c = 5` (unsigned) or `i/c = -17` (signed). It is much more difficult to reason about the correctness of a program without knowing if these integers are signed or unsigned.
``` c
char c = 200;
int i = 1000;
printf("i/c = %d\n", i/c);
```
## Compliant Solution
In this compliant solution, the variable `c` is declared as `unsigned char`. The subsequent division operation is now independent of the signedness of `char` and consequently has a predictable result.
``` c
unsigned char c = 200;
int i = 1000;
printf("i/c = %d\n", i/c);
```
## Exceptions
**INT07-C-EX1:** [void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file](void%20FIO34-C_%20Use%20int%20to%20capture%20the%20return%20value%20of%20character%20IO%20functions%20that%20might%20be%20used%20to%20check%20for%20end%20of%20file) mentions that certain character IO functions return a value of type `int`. Despite being returned in an arithmetic type, the value is not actually numeric in nature, so it is acceptable to later store the result into a variable of type `char`.
## Risk Assessment
This is a subtle error that results in a disturbingly broad range of potentially severe [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). At the very least, this error can lead to unexpected numerical results on different platforms. Unexpected arithmetic values when applied to arrays or pointers can yield buffer overflows or other invalid memory access.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT07-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2012 rules 10.1, 10.3 and 10.4. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT07  |  |
| CodeSonar | 8.3p0 | LANG.TYPE.IOT | Inappropriate operand type |
| Compass/ROSE |  |  | Can detect violations of this recommendation. In particular, it flags any instance of a variable of type char (without a signed or unsigned qualifier) that appears in an arithmetic expression |
| ECLAIR | 1.2 | CC2.INT07 | Fully implemented |
| Helix QAC | 2024.4 | C1292, C1293, C4401, C4421, C4431, C4441, C4451 |  |
| Klocwork | 2024.4 | PORTING.SIGNED.CHAR |  |
| LDRA tool suite | 9.7.1 | 93 S, 96 S, 101 S, 329 S, 432 S, 458 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT07-aCERT_C-INT07-b | The plain char type shall be used only for the storage and use of character valuessigned and unsigned char type shall be used only for the storage and use of numeric values |
| PC-lint Plus | 1.4 | 9112 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT07-C | Checks for use of plain char type for numeric value (rec. fully covered) |
| Splint | 3.1.1 |  |  |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2012 rules 10.1, 10.3 and 10.4. |
| SonarQube C/C++ Plugin | 3.11 | S820 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT07-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT07-CPP. Use only explicitly signed or unsigned char type for numeric values |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Rule 10.1 (required)Rule 10.3 (required)
Rule 10.4 (required) |
| MITRE CWE | CWE-682, Incorrect calculation |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152392) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152450)
## Comments:

|  |
| ----|
| What about numeric values too large to fit into a char?
                                        Posted by jimg at Feb 08, 2013 16:48
                                     |
| This rule is only to be used when you intend to use a character type to hold a numeric value (in constrast to an actual character).
                                        Posted by svoboda at Feb 11, 2013 10:18
                                     |
| I think the Exception needs to be removed from this guideline because it is based on void FIO34-C, which isn't replaced/superseded by any other guideline.
                                        Posted by lallierc at Oct 01, 2015 07:46
                                     |
| I believe the VOIDed rule was superseded by;FIO34-C. Distinguish between characters read from a file and EOF or WEOF
                                        Posted by aballman at Oct 01, 2015 12:59
                                     |

