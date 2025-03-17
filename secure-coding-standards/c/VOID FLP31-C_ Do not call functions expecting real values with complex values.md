The header `tgmath.h` provides type-generic macros for math functions.
Although most functions from the `math.h` header have a complex counterpart in `complex.h`, several functions do not. Calling any of the following type-generic functions with complex values results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). This rule is a specialization of [EXP37-C. Call functions with the correct number and type of arguments](EXP37-C_%20Call%20functions%20with%20the%20correct%20number%20and%20type%20of%20arguments).
**Functions That Should Not Be Called with Complex Values**

|  |  |  |  |  |  |  |  |  |  |
| ----|----|----|----|----|----|----|----|----|----|
| atan2 | erf | fdim | fmin | ilogb | llround | logb | nextafter | rint | tgamma |
| cbrt | erfc | floor | fmod | ldexp | log10 | lrint | nexttoward | round | trunc |
| ceil | exp2 | fma | frexp | lgamma | log1p | lround | remainder | scalbn | ; |
| copysign | expm1 | fmax | hypot | llrint | log2 | nearbyint | remquo | scalbln | ; |

As a result, these functions must never be called with complex values.
## Noncompliant Code Example
This noncompliant code example attempts to take the logarithm of a complex number, resulting in undefined behavior:
``` c
#include <complex.h>
#include <tgmath.h>
void func(void) {
  double complex c = 2.0 + 4.0 * I;
  double complex result = log2(c);
}
```
## Compliant Solution
This compliant solution ensures that the logarithm is applied only to the real part of the complex number:
``` c
#include <complex.h>
#include <tgmath.h>
void func(void) {
  double complex c = 2.0 + 4.0 * I;
  double complex result = log2(creal(c));
}
```
## Risk Assessment
Using complex types with type-generic functions that accept only real types results in undefined behavior, possibly resulting in [abnormal program termination](http://BB.%20Definitions#abnormal%20termination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP31-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ECLAIR | 1.2 | CC2.FLP31 | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP31-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FLP31-CPP. Do not call functions expecting real values with complex values |
| ISO/IEC TR 24772:2013 | Subprogram Signature Mismatch [OTR] |
| MITRE CWE | Function call with incorrect argument type |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=372) [](https://www.securecoding.cert.org/confluence/display/seccode/FLP32-C.+Prevent+or+detect+domain+and+range+errors+in+math+functions?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Should we have a CS/NCCE pair here? I'm having trouble seeing how violations of this rule could pass the type checker.
                                        Posted by avolkovi at Jul 10, 2008 10:59
                                     |
| Yes.
                                        Posted by rcs at Jul 10, 2008 12:56
                                     |
| Ok, added a very contrived one, let me know what you think.
                                        Posted by avolkovi at Jul 11, 2008 10:11
                                     |
| Looks good to me.
Suggest you add a 'reivew' tag to any rule that gets significant changes, like a NCCE/CS pair.
                                        Posted by svoboda at Jul 11, 2008 11:36
                                     |
| ;It seems that this rule is simply a special case of EXP37-C. Call functions with the correct number and type of arguments. What is the general consensus on merging this rule into that one?
                                        Posted by eaevans at Nov 21, 2013 16:14
                                     |
| I am not overly familiar with _Complex, but I believe _Complex types are converted into real types by discarding the imaginary value. See 6.3.1.7.This is a specialization of EXP37-C, but a bit different in that EXP37-C is basically warning against bad redeclarations or messing up vararg calls;and FLP31-C is warning against UB due to conversions when the declarations are fine. I don't know that they should be merged, but I also don't have incredibly strong feelings on it either.
                                        Posted by aballman at Nov 21, 2013 16:38
                                     |

