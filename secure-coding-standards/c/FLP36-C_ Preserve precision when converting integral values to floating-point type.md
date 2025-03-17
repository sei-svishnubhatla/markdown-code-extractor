Narrower arithmetic types can be cast to wider types without any effect on the magnitude of numeric values. However, whereas integer types represent exact values, floating-point types have limited precision. The C Standard, 6.3.1.4 paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> When a value of integer type is converted to a standard floating type, if the value being converted can be represented exactly in the new type, it is unchanged. If the value being converted is in the range of values that can be represented but cannot be represented exactly, the result is either the nearest higher or nearest lower representable value, chosen in an implementation-defined manner. If the value being converted is outside the range of values that can be represented, the behavior is undefined. Results of some implicit conversions may be represented in greater range and precision than that required by the new type (see 6.3.1.8 and 6.8.7.5). 

Conversion from integral types to floating-point types without sufficient precision can lead to loss of precision (loss of least significant bits). No runtime exception occurs despite the loss.
## Noncompliant Code Example
In this noncompliant example, a large value of type `long int` is converted to a value of type `float` without ensuring it is representable in the type:
``` c
#include <stdio.h>
int main(void) {
  long int big = 1234567890L;
  float approx = big;
  printf("%ld\n", (big - (long int)approx));
  return 0;
}
```
For most floating-point hardware, the value closest to `1234567890` that is representable in type `float` is `1234567844`; consequently, this program prints the value `-46`.
## Compliant Solution
This compliant solution replaces the type `float` with a `double`. Furthermore, it uses an assertion to guarantee that the `double` type can represent any `long int` without loss of precision. (See [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions) and [MSC11-C. Incorporate diagnostic tests using assertions](MSC11-C_%20Incorporate%20diagnostic%20tests%20using%20assertions).)
``` c
#include <assert.h>
#include <float.h>
#include <limits.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
extern size_t popcount(uintmax_t); /* See INT35-C */
#define PRECISION(umax_value) popcount(umax_value) 
int main(void) {
  assert(PRECISION(LONG_MAX) <= DBL_MANT_DIG * log2(FLT_RADIX));
  long int big = 1234567890L;
  double approx = big;
  printf("%ld\n", (big - (long int)approx));
  return 0;
}
```
On the same implementation, this program prints `0`, implying that the integer value `1234567890` is representable in type `double` without change.
## Risk Assessment
Conversion from integral types to floating-point types without sufficient precision can lead to loss of precision (loss of least significant bits).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP36-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée keeps track of all floating point rounding errors and loss of precision and reports code defects resulting from those. |
| CodeSonar | 8.3p0 | LANG.TYPE.IAT | Inappropriate Assignment Type |
| Coverity | 2017.07 | MISRA C 2004 Rule 10.x (needs investigation) | Needs investigation |
| Cppcheck Premium | 24.11.0 | premium-cert-flp36-c |  |
| Helix QAC | 2024.4 | C1260, C1263, C1298, C1299, C1800, C1802, C1803, C1804, C4117, C4435, C4437, C4445C++3011 |  |
| Klocwork | 2024.4 | PORTING.CAST.FLTPNT |  |
| LDRA tool suite | 9.7.1 | 435 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP36-aCERT_C-FLP36-b | Implicit conversions from integral to floating type which may result in a loss of information shall not be usedImplicit conversions from integral constant to floating type which may result in a loss of information shall not be used |
| PC-lint Plus | 1.4 | 915, 922 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT-C: Rule FLP36-C | Checks for precision loss in integer to float conversion (rule fully covered) |
| PVS-Studio | 7.35 | V674 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP36-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL03-C. Use a static assertion to test the value of a constant expression | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | NUM13-J. Avoid loss of precision when converting primitive integers to floating-point | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 6.3.1.4, "Real Floating and Integer" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152068) [](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152017)
## Comments:

|  |
| ----|
| Wouldn't 1234567890L be a better example constant than 1234567890 (and more standards-honoring)?
                                        Posted by marcel.waldvogel at Apr 15, 2017 05:17
                                     |
| Fixed, thanks
                                        Posted by svoboda at Apr 17, 2017 17:50
                                     |

