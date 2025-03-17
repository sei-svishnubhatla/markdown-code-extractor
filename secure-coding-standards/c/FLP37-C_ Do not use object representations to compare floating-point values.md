The object representation for floating-point values is implementation defined. However, an implementation that defines the `__STDC_IEC_559__` macro shall conform to the IEC 60559 floating-point standard and uses what is frequently referred to as IEEE 754 floating-point arithmetic \[ISO/IEC 9899:2024\]. The floating-point object representation used by IEC 60559 is one of the most common floating-point object representations in use today.
All floating-point object representations use specific bit patterns to encode the value of the floating-point number being represented. However, equivalence of floating-point values is not encoded solely by the bit pattern used to represent the value. For instance, if the floating-point format supports negative zero values (as IEC 60559 does), the values `-0.0` and `0.0` are equivalent and will compare as equal, but the bit patterns used in the object representation are not identical. Similarly, if two floating-point values are both (the same) NaN, they will not compare as equal, despite the bit patterns being identical, because they are not equivalent.
Do not compare floating-point object representations directly, such as by calling `memcmp()`or its moral equivalents. Instead, the equality operators (`==` and `!=`) should be used to determine if two floating-point values are equivalent.
## Noncompliant Code Example
In this noncompliant code example, `memcmp()` is used to compare two structures for equality. However, since the structure contains a floating-point object, this code may not behave as the programmer intended.
``` c
#include <stdbool.h>
#include <string.h>
struct S {
  int i;
  float f;
};
bool are_equal(const struct S *s1, const struct S *s2) {
  if (!s1 && !s2)
    return true;
  else if (!s1 || !s2)
    return false;
  return 0 == memcmp(s1, s2, sizeof(struct S));
}
```
## Compliant Solution
In this compliant solution, the structure members are compared individually:
``` c
#include <stdbool.h>
#include <string.h>
struct S {
  int i;
  float f;
};
bool are_equal(const struct S *s1, const struct S *s2) {
  if (!s1 && !s2)
    return true;
  else if (!s1 || !s2)
    return false;
  return s1->i == s2->i &&
         s1->f == s2->f;
}
```
## Risk Assessment
Using the object representation of a floating-point value for comparisons can lead to incorrect equality results, which can lead to unexpected behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP37-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | memcmp-with-float | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FLP37 | Fully implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-flp37-c |  |
| Helix QAC | 2024.4 | C5026C++3118 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.MEMCMP.PTR_ARG_TYPESCERT.MEMCMP.FLOAT_MEMBER |  |
| LDRA tool suite | 9.7.1 | 618 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP37-c | Do not use object representations to compare floating-point values |
| PC-lint Plus | 1.4 | 2498, 2499 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FLP37-C | Checks for memory comparison of floating-point values (rule fully covered) |
| PVS-Studio | 7.35 | V1014 |  |
| RuleChecker | 24.04 | memcmp-with-float | Partially checked |
| TrustInSoft Analyzer | 1.38 |  | Exhaustively verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP37-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Annex F, "ISO/IEC 60559 floating-point arithmetic" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152221) [](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](../c/Rule%2006_%20Arrays%20_ARR_)
## Comments:

|  |
| ----|
| you actually should never use the "==" operator to compare floating point variables as the compliant solution suggests, as floating point numbers have limited precision on different machine types.
                                        Posted by fakegermano at Jan 17, 2020 09:00
                                     |
| That depends entirely on what you are comparing and why you are comparing it, so I would disagree with the statement that you should never use == for comparing floating-point values. The rule is about how to determine if two floats are equal, and == is the canonical way to do that test for equality. If you need to tell whether two floats are "equal enough" because you want to account for precision, rounding, etc, you should use other approaches depending on the expected precision of the floats involved (max ULPs, using an epsilon, etc).
                                        Posted by aballman at Jan 17, 2020 09:20
                                     |
| Sure, but it depends too on how s1->f and s2→f are valued. If one is a constant (for example) and other is calculated, there is a great chance that the equality test by '==' always evaluated to false.
                                        Posted by jerome.guy at Jan 17, 2020 09:27
                                     |
| See recommendation FLP02-C. Avoid using floating-point numbers when precise computation is needed for discussion about using == on floating-point values vs. other approaches.
                                        Posted by svoboda at Jan 17, 2020 09:34
                                     |
| Again, this depends on the domain. If you need that comparison to be equality in your domain, that result may be entirely correct. For instance, if the constant you are comparing against is 0.0, you may really care about the difference between 0.0 and "almost 0.0" depending on the problem being solved.
                                        Posted by aballman at Jan 17, 2020 09:42
                                     |
| I agree with all which is written here. So, we could specify those limitations and remember FLP02-C. Avoid using floating-point numbers when precise computation is needed .In order to avoid confusion.
                                        Posted by jerome.guy at Jan 20, 2020 01:45
                                     |

