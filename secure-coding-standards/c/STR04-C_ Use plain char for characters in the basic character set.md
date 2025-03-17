There are three *character types*: `char`, `signed char`, and `unsigned char`. Compilers have the latitude to define `char` to have the same range, representation, and behavior as either `signed char` or `unsigned char`. Irrespective of the choice made, `char` is a separate type from the other two and is not compatible with either.
For characters in the basic character set, it does not matter which data type is used, except for type compatibility. Consequently, it is best to use plain `char` for character data for compatibility with standard string-handling functions.
In most cases, the only portable operators on plain `char` types are assignment and equality operators (`=`, `==`, `!=` ). An exception is the translation to and from digits. For example, if the `char` `c` is a digit, `c - '0'` is a value between 0 and 9.
## Noncompliant Code Example
This noncompliant code example simply shows the standard string-handling function `strlen()` being called with a plain character string, a signed character string, and an unsigned character string. The `strlen()` function takes a single argument of type `const char` \*:
``` c
size_t len;
char cstr[] = "char string";
signed char scstr[] = "signed char string";
unsigned char ucstr[] = "unsigned char string";
len = strlen(cstr);
len = strlen(scstr);  /* Warns when char is unsigned */
len = strlen(ucstr);  /* Warns when char is signed */
```
Compiling at high warning levels in compliance with [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels) causes warnings to be issued when
-   Converting from `unsigned char[]` to `const char *` when `char` is signed
-   Converting from `signed char[]` to `const char *` when `char` is defined to be unsigned
Casts are required to eliminate these warnings, but excessive casts can make code difficult to read and hide legitimate warning messages.
If this C code were compiled using a C++ compiler, conversions from `unsigned char[]` to `const char *` and from `signed char[]` to `const char *` would be flagged as errors requiring casts.
## Compliant Solution
The compliant solution uses plain `char` for character data:
``` c
size_t len;
char cstr[] = "char string";
len = strlen(cstr);
```
Conversions are not required, and the code compiles cleanly at high warning levels without casts.
## Risk Assessment
Failing to use plain `char` for characters in the basic character set can lead to excessive casts and less effective compiler diagnostics.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR04-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2004 rule 6.1. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR04 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.IATLANG.TYPE.ICA
LANG.TYPE.IOT
LANG.TYPE.MOT | Inappropriate assignment typeInappropriate character arithmetic
Inappropriate operand type
Mismatched operand types |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.STR04 | Fully implemented |
| EDG |  |  |  |
| Helix QAC | 2024.4 | C0432, C0674, C0699 |  |
| LDRA tool suite | 9.7.1 | 93 S, 101 S, 329 S, 432 S, 458 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR04-a | The plain char type shall be used only for the storage and use of character values |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2004 rule 6.1. |
| SonarQube C/C++ Plugin | 3.11 | S810 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR04-CPP. Use plain char for characters in the basic character set |
| MISRA C:2012 | Rule 10.1 (required)Rule 10.2 (required)
Rule 10.3 (required)
Rule 10.4 (required) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152399) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152066)
## Comments:

|  |
| ----|
| This needs further discussion.; For characters in the basic character set, it doesn't matter which form is used (except for type compatibility), but for other data values it is safer to use type unsigned char.  Anyway, for non-basic characters one should generally be using wide characters, not any variety of type char.
                                        Posted by dagwyn at Apr 16, 2008 21:19
                                     |
| seems to me like STR00-C. Represent characters using an appropriate type deals with this necessary "further discussion"
                                        Posted by avolkovi at Jun 03, 2008 10:07
                                     |

