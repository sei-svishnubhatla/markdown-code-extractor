According to the C Standard, 7.4.1 paragraph 1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> The header `<ctype.h>` declares several functions useful for classifying and mapping characters. In all cases the argument is an `int`, the value of which shall be representable as an `unsigned char` or shall equal the value of the macro `EOF`. If the argument has any other value, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

See also [undefined behavior 112](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_112).
This rule is applicable only to code that runs on platforms where the `char` data type is defined to have the same range, representation, and behavior as `signed char`.
Following are the character classification functions that this rule addresses:

|  |  |  |  |
| ----|----|----|----|
| isalnum() | isalpha() | isascii()XSI | isblank() |
| iscntrl() | isdigit() | isgraph() | islower() |
| isprint() | ispunct() | isspace() | isupper() |
| isxdigit() | toascii()XSI | toupper() | tolower() |

<sup>XSI</sup> denotes an X/Open System Interfaces Extension to ISO/IEC 9945—POSIX. These functions are not defined by the C Standard.
This rule is a specific instance of [STR34-C. Cast characters to unsigned char before converting to larger integer sizes](STR34-C_%20Cast%20characters%20to%20unsigned%20char%20before%20converting%20to%20larger%20integer%20sizes).
## Noncompliant Code Example
On implementations where plain `char` is signed, this code example is noncompliant because the parameter to `isspace()`, `*t`, is defined as a `const char *`, and this value might not be representable as an `unsigned char`:
``` c
#include <ctype.h>
#include <string.h>
size_t count_preceding_whitespace(const char *s) {
  const char *t = s;
  size_t length = strlen(s) + 1;
  while (isspace(*t) && (t - s < length)) { 
    ++t;
  }
  return t - s;
} 
```
The argument to `isspace()` must be `EOF` or representable as an `unsigned char`; otherwise, the result is undefined.
## Compliant Solution
This compliant solution casts the character to `unsigned char` before passing it as an argument to the `isspace()` function:
``` c
#include <ctype.h>
#include <string.h>
size_t count_preceding_whitespace(const char *s) {
  const char *t = s;
  size_t length = strlen(s) + 1;
  while (isspace((unsigned char)*t) && (t - s < length)) { 
    ++t;
  }
  return t - s;
} 
```
## Risk Assessment
Passing values to character handling functions that cannot be represented as an `unsigned char` to character handling functions is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR37-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | ctype-limits | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR37 | Fully implemented |
| CodeSonar | 8.3p0 | MISC.NEGCHAR | Negative character value |
| Compass/ROSE |  |  | Could detect violations of this rule by seeing if the argument to a character handling function (listed above) is not an unsigned char |
| ECLAIR | 1.2 | CC2.STR37 | Fully implemented |
| Helix QAC | 2024.4 | C4413, C4414C++3051 |  |
| Klocwork | 2024.4 | AUTOSAR.STDLIB.CCTYPE.UCHARMISRA.ETYPE.ASSIGN.2012 |  |
| LDRA tool suite | 9.7.1 | 663 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR37-a | Do not pass incorrect values to ctype.h library functions |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR37-C | Checks for invalid use of standard library integer routine (rule fully covered) |
| RuleChecker | 24.04 | ctype-limits | Partially checked |
| TrustInSoft Analyzer | 1.38 | valid_char | Partially verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR37-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | STR34-C. Cast characters to unsigned char before converting to larger integer sizes | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Passing arguments to character-handling functions that are not representable as unsigned char [chrsgnext] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-704, Incorrect Type Conversion or Cast | 2017-06-14: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-686 and STR37-C
Intersection( CWE-686, STR37-C) = Ø
STR37-C is not about the type of the argument passed (which is signed int), but about the restrictions placed on the value in this type (must be 0-UCHAR_MAX or EOF). I interpret ‘argument type’ to be specific to the C language, so CWE-686 does not apply to incorrect argument values, just incorrect types (which is relatively rare in C, but still possible).
### CWE-704 and STR37-C
STR37-C = Subset( STR34-C)
### CWE-683 and STR37-C
Intersection( CWE-683, STR37-C) = Ø
STR37-C excludes mis-ordered function arguments (assuming they pass type-checking), because there is no easy way to reliably detect violations of CWE-683.
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.4.1, "Character Handling <ctype.h>" |
| [Kettlewell 2002] | Section 1.1, "<ctype.h> and Characters Types" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152133) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152326)
## Comments:

|  |
| ----|
| The Cast compliant solution seems to violate three other secure coding rules
+STR_CS.c:222: warning: EXP11-A: Do not apply operators expecting one type to data of an incompatible type
 STR_CS.c:222: warning: EXP05-A: Do not cast away a const qualification
 STR_CS.c:222: warning: INT01-A: Use rsize_t or size_t for all integer values representing the size of an object
                                        Posted by svoboda at Jul 08, 2008 16:23
                                     |
| Not sure about EXP11, but it is probably related to some cast due to t-s
EXP05 is "violated" because t is const but t-s is not, we need a better way to catch this exception in the checker
INT01 is "violated" because t-s does not have type size_t but length does
                                        Posted by avolkovi at Jul 09, 2008 09:49
                                     |
| Note EXP05-C. Do not cast away a const qualification was never violated in the compliant solution since the cast to unsigned char is not applied to the pointer but rather to the character resulting from dereferencing the pointer. The cast yields an rvalue (an unnamed temporary copy of the array element) that, unlike a pointer, cannot be used to modify the array element. I've removed the cast. Perhaps EXP05-C needs clarifying?
                                        Posted by martinsebor at Jan 09, 2010 20:06
                                     |
| Do we want to include POSIX functions here?
                                        Posted by rcs_mgr at Oct 26, 2011 20:47
                                     |
| The principle is simple. This should apply to all functions that take an argument which can be EOF or an unsigned char, and which promise undefined behavior if the argument is something else (such as a signed char with value < -1).
                                        Posted by svoboda at Oct 27, 2011 15:16
                                     |

