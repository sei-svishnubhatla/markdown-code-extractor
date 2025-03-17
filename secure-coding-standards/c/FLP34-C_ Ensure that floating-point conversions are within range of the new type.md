If a floating-point value is to be converted to a floating-point value of a smaller range and precision or to an integer type, or if an integer type is to be converted to a floating-point type, the value must be representable in the destination type.
The C Standard, 6.3.1.4, paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], says,
> When a finite value of decimal floating type is converted to an integer type other than bool, the fractional part is discarded (i.e. the value is truncated toward zero). If the value of the integral part cannot be represented by the integer type, the "invalid" floating-point exception shall be raised and the result of the conversion is unspecified.

Paragraph 2 of the same subclause says,
> When a value of integer type is converted to a standard floating type, if the value being converted can be represented exactly in the new type, it is unchanged. If the value being converted is in the range of values that can be represented but cannot be represented exactly, the result is either the nearest higher or nearest lower representable value, chosen in an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) manner. If the value being converted is outside the range of values that can be represented, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

And subclause 6.3.1.5, paragraph 1+2, says,
> When a value of real floating type is converted to a real floating type, if the value being converted can be represented exactly in the new type, it is unchanged.
>
> When a value of real floating type is converted to a standard floating type, if the value being converted is in the range of values that can be represented but cannot be represented exactly, the result is either the nearest higher or nearest lower representable value, chosen in an implementation-defined manner. If the value being converted is outside the range of values that can be represented, the behavior is undefined. 

See [undefined behaviors 16](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_16) and [17](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_17).
This rule does not apply to demotions of floating-point types on [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) that support signed infinity, such as IEEE 754, as all values are within range.
## Noncompliant Code Example (`float` to `int`)
This noncompliant code example leads to undefined behavior if the integral part of `f_a` cannot be represented as an integer:
``` c
void func(float f_a) {
  int i_a;
  /* Undefined if the integral part of f_a cannot be represented. */
  i_a = f_a;
}
```
## Compliant Solution (`float` to `int`)
This compliant solution tests to ensure that the `float` value will fit within the `int` variable before performing the assignment.
``` c
#include <float.h>
#include <limits.h>
#include <math.h>
#include <stddef.h>
#include <stdint.h>
extern size_t popcount(uintmax_t); /* See INT35-C */
#define PRECISION(umax_value) popcount(umax_value)
void func(float f_a) {
  int i_a;
  if (isnan(f_a) ||
      PRECISION(INT_MAX) < log2f(fabsf(f_a)) ||
      (f_a != 0.0F && fabsf(f_a) < FLT_MIN)) {
    /* Handle error */
  } else {
    i_a = f_a;
  }
}
```
## Noncompliant Code Example (Narrowing Conversion)
This noncompliant code example attempts to perform conversions that may result in truncating values outside the range of the destination types:
``` c
void func(double d_a, long double big_d) {
  double d_b = (float)big_d;
  float f_a = (float)d_a;
  float f_b = (float)big_d;
}
```
As a result of these conversions, it is possible that `d_a` is outside the range of values that can be represented by a float or that `big_d` is outside the range of values that can be represented as either a `float` or a `double`. If this is the case, the result is undefined on implementations that do not support Annex F, "IEC 60559 Floating-Point Arithmetic."
## Compliant Solution (Narrowing Conversion)
This compliant solution checks whether the values to be stored can be represented in the new type:
``` c
#include <float.h>
#include <math.h>
void func(double d_a, long double big_d) {
  double d_b;
  float f_a;
  float f_b;
  if (d_a != 0.0 &&
      (isnan(d_a) ||
       isgreater(fabs(d_a), FLT_MAX) ||
       isless(fabs(d_a), FLT_MIN))) {
    /* Handle error */
  } else {
    f_a = (float)d_a;
  }
  if (big_d != 0.0 &&
      (isnan(big_d) ||
       isgreater(fabs(big_d), FLT_MAX) ||
       isless(fabs(big_d), FLT_MIN))) {
    /* Handle error */
  } else {
    f_b = (float)big_d;
  }
  if (big_d != 0.0 &&
      (isnan(big_d) ||
       isgreater(fabs(big_d), DBL_MAX) ||
       isless(fabs(big_d), DBL_MIN))) {
    /* Handle error */
  } else {
    d_b = (double)big_d;
  }  
}
```
## Risk Assessment
Converting a floating-point value to a floating-point value of a smaller range and precision or to an integer type, or converting an integer type to a floating-point type, can result in a value that is not representable in the destination type and is undefined behavior on implementations that do not support Annex F.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP34-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | SupportedAstrée reports all potential overflows resulting from floating-point conversions. |
| Compass/ROSE |  |  | Can detect some violations of this rule. However, it does not flag implicit casts, only explicit ones |
| CodeSonar | 8.3p0 | LANG.TYPE.IAT | Inappropriate Assignment Type |
| Coverity | 2017.07 | MISRA_CAST (needs verification) | Can detect instances where implicit float conversion is involved: implicitly converting a complex expression with integer type to floating type, implicitly converting a double expression to narrower float type (may lose precision), implicitly converting a complex expression from float to double, implicitly converting from float to double in a function argument, and so on |
| Cppcheck | ;2.15 | floatConversionOverflowsuspiciousFloatingPointCast |  |
| Cppcheck Premium | 24.11.0 | floatConversionOverflowsuspiciousFloatingPointCast |  |
| Helix QAC | 2024.4 | C4450, C4451, C4452, C4453, C4454, C4462, C4465C++3011 |  |
| Klocwork | 2024.4 | MISRA.CAST.FLOAT.WIDERMISRA.CAST.FLOAT.INT
MISRA.CAST.INT_FLOAT
MISRA.CONV.FLOAT |  |
| LDRA tool suite | 9.7.1 | 435 S, 93 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP34-aCERT_C-FLP34-b
 | Avoid implicit conversions from wider to narrower floating typeAvoid implicit conversions of floating point numbers from wider to narrower floating type |
| PC-lint Plus | 1.4 | 735, 736,915, 922,
9118, 9227 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FLP34-C | Checks for float conversion overflow (rule partially covered) |
| PVS-Studio | 7.35 | V615, V2003, V2004 |  |
| TrustInSoft Analyzer | 1.38 | float_to_int | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | NUM12-J. Ensure conversions of numeric types to narrower types do not result in lost or misinterpreted data | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Numeric Conversion Errors [FLC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-681, Incorrect Conversion between Numeric Types | 2017-06-29: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-197 | 2017-06-14: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-197 and FLP34-C
Independent( FLP34-C, INT31-C) FIO34-C = Subset( INT31-C)
CWE-197 = Union( FLP34-C, INT31-C)
### CWE-195 and FLP34-C
Intersection( CWE-195, FLP34-C) = Ø
Both conditions involve type conversion. However, CWE-195 explicitly focuses on conversions between unsigned vs signed types, whereas FLP34-C focuses on floating-point arithmetic.
### CWE-681 and FLP34-C
CWE-681 = Union( FLP34-C, INT31-C)
## Bibliography

|  |  |
| ----|----|
| [IEEE 754 2006] |  |
| [ISO/IEC 9899:2024] | Subclause 6.3.1.4, "Real Floating and Integer"Subclause 6.3.1.5, "Real Floating Types" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152396) [](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152221)
## Comments:

|  |
| ----|
| I cannot find anything in the standard that makes me too comfortable that -FLT_MAX is the minimum representable value.  FLT_MIN is the minimum normalized positive floating-point number.  I infer it from the standard (which defines floating point values in terms of a sign bit, a binary matissa, and binary exponent), but am not completely certain I've read the standard properly.
                                        Posted by hburch at May 23, 2007 15:25
                                     |
| It is -FLT_MAX, according to the glibc documentation, anyway.
                                        Posted by jpincar at May 25, 2007 10:26
                                     |
| All f.p. representations I am aware of use a separate sign bit, and if I recall correctly that is in the;numerical model used for <float.h> in the standard, so -FLT_MAX would be correct.
This rule ought to be extended to include demotion to integer types, not just to narrower floating types.
                                        Posted by dagwyn at Apr 16, 2008 19:42
                                     |
| The "Compliant Solution (float to int)"-code looks incorrect when the float is NaN.
                                        Posted by per.mildner at Aug 14, 2017 08:43
                                     |
| The "Compliant Solution (Narrowing Conversion)"-code looks incorrect when d_a is zero (presumably;isless(fabs(0.0), FLT_MIN) is true, which would lead to the error case). Also, presumably all positive doubles less than FLT_MIN are "in the range of values that can be represented (in a float)", so the entire isless-check looks fishy.
                                        Posted by per.mildner at Sep 07, 2017 04:25
                                     |
| The former CS currently produces INT_MIN when given NaN. I've added a check for NaN to resolve this.However, it works properly for 0.0. 0's absolute number is 0, the log of that is -infinity, and that is less than the precision of INT_MAX. :) Our rule FLP32-C. Prevent or detect domain and range errors in math functions permits;floating-point operations where the answer is precisely infinity or -infinity.I also tweaked the latter CS to gracefully handle NaN as well as 0.
                                        Posted by svoboda at Sep 12, 2017 10:17
                                     |
| Your comment seems to be about the "Compliant Solution (float to int)"-code. My comment about zero;d_a (in the "Compliant Solution (Narrowing Conversion)"-code) was incorrect since the entire test is guarded by d_a != 0.0 so it does not matter that isless(fabs(0.0), FLT_MIN) would be true.
                                        Posted by per.mildner at Sep 12, 2017 15:59
                                     |

