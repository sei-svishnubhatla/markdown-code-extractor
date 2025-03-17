The C Standard, 7.12.1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines three types of errors that relate specifically to math functions in `<math.h>`.  Paragraph 2 states
> *A domain error* occurs if an input argument is outside the domain over which the mathematical function is defined.

Paragraph 3 states
> A *pole error* (also known as a singularity or infinitary) occurs if the mathematical function has an exact infinite result as the finite input argument(s) are approached in the limit.

Paragraph 4 states
> a *range error* occurs if and only if the result overflows or underflows

An example of a domain error is the square root of a negative number, such as `sqrt(-1.0)`, which has no meaning in real arithmetic. Contrastingly, 10 raised to the 1-millionth power, `pow(10., 1e6)`, cannot be represented in many floating-point [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) because of the limited range of the type `double` and consequently constitutes a range error. In both cases, the function will return some value, but the value returned is not the correct result of the computation. An example of a pole error is `log(0.0)`, which results in negative infinity.
Programmers can prevent domain and pole errors by carefully bounds-checking the arguments before calling mathematical functions and taking alternative action if the bounds are violated.
Range errors usually cannot be prevented because they are dependent on the implementation of floating-point numbers as well as on the function being applied. Instead of preventing range errors, programmers should attempt to detect them and take alternative action if a range error occurs.
The following table lists the `double` forms of standard mathematical functions, along with checks that should be performed to ensure a proper input domain, and indicates whether they can also result in range or pole errors, as reported by the C Standard. Both `float` and `long double` forms of these functions also exist but are omitted from the table for brevity. If a function has a specific domain over which it is defined, the programmer must check its input values. The programmer must also check for range errors where they might occur. The standard math functions not listed in this table, such as `fabs()`, have no domain restrictions and cannot result in range or pole errors.

| Function | Domain | Range | Pole  |
| ----|----|----|----|
| acos(x) | -1 <= x && x <= 1 | No | No |
| asin(x) | -1 <= x && x <= 1 | Yes | No |
| atan(x) | None | Yes | No |
| atan2(y, x) | None | No | No |
| acosh(x) | x >= 1 | Yes | No |
| asinh(x) | None | Yes | No |
| atanh(x) | -1 < x && x < 1 | Yes | Yes |
| cosh(x), sinh(x) | None | Yes | No |
| exp(x), exp2(x), expm1(x) | None | Yes | No |
| ldexp(x, exp) | None | Yes | No |
| log(x), log10(x), log2(x) | x >= 0 | No | Yes |
| log1p(x) | x >= -1 | No | Yes |
| ilogb(x) | x != 0 && !isinf(x) && !isnan(x) | Yes | No |
| logb(x) | x != 0 | Yes; | Yes |
| scalbn(x, n), scalbln(x, n) | None | Yes | No |
| hypot(x, y) | None | Yes | No |
| pow(x,y) | x > 0 || (x == 0 && y > 0) ||
(x < 0 && y is an integer) | Yes | Yes |
| sqrt(x) | x >= 0 | No | No |
| erf(x) | None | Yes | No |
| erfc(x) | None | Yes | No |
| lgamma(x), tgamma(x) | x != 0 && ! (x < 0 && x is an integer) | Yes | Yes |
| lrint(x), lround(x) | None | Yes | No |
| fmod(x,;y), remainder(x, y),
remquo(x, y, quo) | y != 0 | Yes | No |
| nextafter(x, y),nexttoward(x, y) | None | Yes | No |
| fdim(x,y) | None | Yes | No; |
| fma(x,y,z) | None | Yes | No |

## Domain and Pole Checking
The most reliable way to handle domain and pole errors is to prevent them by checking arguments beforehand, as in the following exemplar:
``` java
double safe_sqrt(double x) {
  if (x < 0) {
    fprintf(stderr, "sqrt requires a nonnegative argument");
    /* Handle domain / pole error */
  }
  return sqrt (x);
}
```
## Range Checking
Programmers usually cannot prevent range errors, so the most reliable way to handle them is to detect when they have occurred and act accordingly.
The exact treatment of error conditions from math functions is tedious. The C Standard, 7.12.1 paragraph 5 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines the following behavior for floating-point overflow:
> A floating result overflows if a finite result value with ordinary accuracy would have magnitude (absolute value) too large for the representation with full precision in the specified type. A result that is exactly an infinity does not overflow. If a floating result overflows and default rounding is in effect, then the function returns the value of the macro HUGE_VAL, HUGE_VALF, or HUGE_VALL according to the return type, with the same sign as the correct value of the function; however, for the types with reduced-precision representations of numbers beyond the overflow threshold, the function may return a representation of the result with less than full precision for the type. If a floating resultoverflowsanddefaultroundingisineffectandtheintegerexpressionmath_errhandling & MATH_ERRNO is nonzero, then the integer expression errno acquires the value ERANGE. If a floating result overflows, and the integer expression math_errhandling & MATH_ERREXCEPT is nonzero, the "overflow" floating-point exception is raised (regardless of whether default rounding is in effect).

It is preferable not to check for errors by comparing the returned value against `HUGE_VAL` or `0` for several reasons:
-   These are, in general, valid (albeit unlikely) data values.
-   Making such tests requires detailed knowledge of the various error returns for each math function.
-   Multiple results aside from `HUGE_VAL` and `0` are possible, and programmers must know which are possible in each case.
-   Different versions of the library have varied in their error-return behavior.
It can be unreliable to check for math errors using `errno` because an [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) might not set `errno`. For real functions, the programmer determines if the implementation sets `errno` by checking whether `math_errhandling & MATH_ERRNO` is nonzero. 
The C Standard, 7.3.2, paragraph 1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],  states:
>  an implementation may set `errno` but is not required to.

The obsolete *System V Interface Definition* (SVID3) \[[UNIX 1992](AA.-Bibliography_87152170.html#AA.Bibliography-UNIX92)\] provides more control over the treatment of errors in the math library. The programmer can define a function named `matherr()` that is invoked if errors occur in a math function. This function can print diagnostics, terminate the execution, or specify the desired return value. The `matherr()` function has not been adopted by C or POSIX, so it is not generally portable.
The following error-handing template uses C Standard functions for floating-point errors when the C macro `math_errhandling` is defined and indicates that they should be used; otherwise, it examines `errno`:
``` java
#include <math.h>
#include <fenv.h>
#include <errno.h>
/* ... */
/* Use to call a math function and check errors */
{
  #pragma STDC FENV_ACCESS ON
  if (math_errhandling & MATH_ERREXCEPT) {
    feclearexcept(FE_ALL_EXCEPT);
  }
  errno = 0;
  /* Call the math function */
  if ((math_errhandling & MATH_ERRNO) && errno != 0) {
    /* Handle range error */
  } else if ((math_errhandling & MATH_ERREXCEPT) &&
             fetestexcept(FE_INVALID | FE_DIVBYZERO |
                          FE_OVERFLOW | FE_UNDERFLOW) != 0) {
    /* Handle range error */
  }
}
```
See [FLP03-C. Detect and handle floating-point errors](FLP03-C_%20Detect%20and%20handle%20floating-point%20errors) for more details on how to detect floating-point errors.
## Subnormal Numbers
A subnormal number is a nonzero number that does not use all of its precision bits \[[IEEE 754 2006](AA.-Bibliography_87152170.html#AA.Bibliography-IEEE7542006)\]. These numbers can be used to represent values that are closer to 0 than the smallest normal number (one that uses all of its precision bits). However, the `asin()`, `asinh()`, `atan()`, `atanh()`, and `erf()` functions may produce range errors, specifically when passed a subnormal number. When evaluated with a subnormal number, these functions can produce an inexact, subnormal value, which is an underflow error.
The C Standard, 7.12.1, paragraph 6 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines the following behavior for floating-point underflow:
> The result underflows if a nonzero result value with ordinary accuracy would have magnitude (absolute value) less than the minimum normalized number in the type; however a zero result that is specified to be an exact zero does not underflow. Also, a result with ordinary accuracy and the magnitude of the minimum normalized number may underflow.269) If the result underflows, the function returns an implementation-defined value whose magnitude is no greater than the smallest normalized positive number in the specified type; if the integer expression math_errhandling & MATH_ERRNO is nonzero, whether errno acquires the value ERANGE is implementation-defined; if the integer expression math_errhandling & MATH_ERREXCEPT s nonzero, whether the"underflow" floating-point exception is raised is implementation-defined. 

Implementations that support floating-point arithmetic but do not support subnormal numbers, such as IBM S/360 hex floating-point or nonconforming IEEE-754 implementations that skip subnormals (or support them by flushing them to zero), can return a range error when calling one of the following families of functions with the following arguments:
-   `fmod``((min+subnorm), min)`
-   `remainder``((min+``subnorm``), min)`
-   `remquo``((min+``subnorm``), min, quo)`
where `min` is the minimum value for the corresponding floating point type and `subnorm` is a subnormal value.
If Annex F is supported and subnormal results are supported, the returned value is exact and a range error cannot occur. The C Standard, F.10.7.1 paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], specifies the following for the `fmod()`, `remainder()`, and `remquo()` functions:
> When subnormal results are supported, the returned value is exact and is independent of the current rounding direction mode.

Annex F, subclause F.10.7.2, paragraph 2, and subclause F.10.7.3, paragraph 2, of the C Standard identify when subnormal results are supported.
## Noncompliant Code Example (`sqrt()`)
This noncompliant code example determines the square root of `x`:
``` c
#include <math.h>
void func(double x) {
  double result;
  result = sqrt(x);
}
```
However, this code may produce a domain error if `x` is negative.
## Compliant Solution (`sqrt()`)
Because this function has domain errors but no range errors, bounds checking can be used to prevent domain errors:
``` c
#include <math.h>
void func(double x) {
  double result;
  if (isless(x, 0.0)) {
    /* Handle domain error */
  }
  result = sqrt(x);
}
```
## Noncompliant Code Example (`sinh()`, Range Errors)
This noncompliant code example determines the hyperbolic sine of `x`:
``` c
#include <math.h>
void func(double x) {
  double result;
  result = sinh(x);
}
```
This code may produce a range error if `x` has a very large magnitude.
## Compliant Solution (`sinh()`, Range Errors)
Because this function has no domain errors but may have range errors, the programmer must detect a range error and act accordingly:
``` c
#include <math.h>
#include <fenv.h>
#include <errno.h>
void func(double x) { 
  double result;
  {
    #pragma STDC FENV_ACCESS ON
    if (math_errhandling & MATH_ERREXCEPT) {
      feclearexcept(FE_ALL_EXCEPT);
    }
    errno = 0;
    result = sinh(x);
    if ((math_errhandling & MATH_ERRNO) && errno != 0) {
      /* Handle range error */
    } else if ((math_errhandling & MATH_ERREXCEPT) &&
               fetestexcept(FE_INVALID | FE_DIVBYZERO |
                            FE_OVERFLOW | FE_UNDERFLOW) != 0) {
      /* Handle range error */
    }
  }
  /* Use result... */
}
```
## Noncompliant Code Example (`pow()`)
This noncompliant code example raises `x` to the power of `y`:
``` c
#include <math.h>
void func(double x, double y) {
  double result;
  result = pow(x, y);
}
```
This code may produce a domain error if `x` is negative and `y` is not an integer value or if `x` is 0 and `y` is 0. A domain error or pole error may occur if `x` is 0 and `y` is negative, and a range error may occur if the result cannot be represented as a `double`.
## Compliant Solution (`pow()`)
Because the `pow()` function can produce domain errors, pole errors, and range errors, the programmer must first check that `x` and `y` lie within the proper domain and do not generate a pole error and then detect whether a range error occurs and act accordingly:
``` c
#include <math.h>
#include <fenv.h>
#include <errno.h>
void func(double x, double y) {
  double result;
  if (((x == 0.0f) && islessequal(y, 0.0)) || isless(x, 0.0)) {
    /* Handle domain or pole error */
  }
  {
    #pragma STDC FENV_ACCESS ON
    if (math_errhandling & MATH_ERREXCEPT) {
      feclearexcept(FE_ALL_EXCEPT);
    }
    errno = 0;
    result = pow(x, y);
    if ((math_errhandling & MATH_ERRNO) && errno != 0) {
      /* Handle range error */
    } else if ((math_errhandling & MATH_ERREXCEPT) &&
               fetestexcept(FE_INVALID | FE_DIVBYZERO |
                            FE_OVERFLOW | FE_UNDERFLOW) != 0) {
      /* Handle range error */
    }
  }
  /* Use result... */
}
```
## Noncompliant Code Example (`asin()`, Subnormal Number)
This noncompliant code example determines the inverse sine of `x`:
``` c
#include <math.h>
void func(float x) {
  float result = asin(x);
  /* ... */
}
```
## Compliant Solution (`asin()`, Subnormal Number)
Because this function has no domain errors but may have range errors, the programmer must detect a range error and act accordingly:
``` c
#include <math.h>
#include <fenv.h>
#include <errno.h>
void func(float x) { 
  float result;
  {
    #pragma STDC FENV_ACCESS ON
    if (math_errhandling & MATH_ERREXCEPT) {
      feclearexcept(FE_ALL_EXCEPT);
    }
    errno = 0;
    result = asin(x);
    if ((math_errhandling & MATH_ERRNO) && errno != 0) {
      /* Handle range error */
    } else if ((math_errhandling & MATH_ERREXCEPT) &&
               fetestexcept(FE_INVALID | FE_DIVBYZERO |
                            FE_OVERFLOW | FE_UNDERFLOW) != 0) {
      /* Handle range error */
    }
  }
  /* Use result... */
}
```
## Risk Assessment
Failure to prevent or detect domain and range errors in math functions may cause unexpected results.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP32-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stdlib-limits | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FLP32 | Partially implemented |
| CodeSonar | 8.3p0 | MATH.DOMAIN.ATANMATH.DOMAIN.TOOHIGH
MATH.DOMAIN.TOOLOW
MATH.DOMAIN
MATH.RANGE
MATH.RANGE.GAMMA
MATH.DOMAIN.LOG
MATH.RANGE.LOG
MATH.DOMAIN.FE_INVALID
MATH.DOMAIN.POW
MATH.RANGE.COSH.TOOHIGH
MATH.RANGE.COSH.TOOLOW
MATH.DOMAIN.SQRT
 | Arctangent Domain ErrorArgument Too High
Argument Too Low
Floating Point Domain Error
Floating Point Range Error
Gamma on Zero
Logarithm on Negative Value
Logarithm on Zero
Raises FE_INVALID
Undefined Power of Zero
cosh on High Number
cosh on Low Number
sqrt on Negative Value |
| Helix QAC | 2024.4 | C5025C++5033 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP32-a | Validate values passed to library functions |
| PC-lint Plus | 1.4 | 2423 | Partially supported: reports domain errors for functions with the Semantics *dom_1, *dom_lt0, or *dom_lt1, including standard library math functions |
| Polyspace Bug Finder | R2024a | CERT-C: Rule FLP32-C | Checks for invalid use of standard library floating point routine (rule fully covered) |
| RuleChecker | 24.04 | stdlib-limits  | Partially checked |
| TrustInSoft Analyzer | 1.38 | out-of-range argument | Partially verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | FLP03-C. Detect and handle floating-point errors | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-682, Incorrect Calculation | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-391 and FLP32-C
Intersection( CWE-391, FLP32-C) =
-   Failure to detect range errors in floating-point calculations
CWE-391 - FLP32-C
-   Failure to detect errors in functions besides floating-point calculations
FLP32-C – CWE-391 =
-   Failure to detect domain errors in floating-point calculations
### CWE-682 and FLP32-C
Independent( INT34-C, FLP32-C, INT33-C) CWE-682 = Union( FLP32-C, list) where list =
-   Incorrect calculations that do not involve floating-point range errors
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.3.2, "Conventions"7.12.1, "Treatment of Error Conditions"
F.10.7, "Remainder Functions"  |
| [IEEE 754 2006;] |  |
| [Plum 1985] | Rule 2-2 |
| [Plum 1989] | Topic 2.10, "conv—Conversions and Overflow" |
| [UNIX 1992] | System V Interface Definition (SVID3) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152157) [](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152068)
## Comments:

|  |
| ----|
| The treatment of pow() in this rule is somewhat lacking.
The specified bounds check (x != 0 || y > 0) is insufficient: C99 says
a domain error also occurs "if x is finite and negative and y is finite
and not an integer value."
The CCE for pow() says "This code tests x and y to ensure that there
will be no range or domain errors" but it does not detect the range
error given in the introductory text at the top of the page: pow(10., 1e6)
Given that the page begins with "Prevent or detect domain errors and
range errors ...", and given the complexity involved in preventing pow()
errors, I think that the document should recommend detection for this
function instead of prevention.
On the subject of detection, the subsection entitled "Non-Compliant
Coding Example (Error Checking)" only talks about return values and errno.
There is no mention of error checking by examining the exception flags.
C90 required the maths functions to set errno on error.  C99 requires
them (the non-complex ones, that is) either to set errno or to set
the exception flags, or both.  So I think the recommendation (for
non-complex maths functions) should be:
1. If there is a simple bounds check that can be done to prevent domain
and range errors, then do it.  (This applies to all the current
examples except pow().)
2. Otherwise, detect errors as follows:
#include <math.h>
#if defined(math_errhandling) && (math_errhandling & MATH_ERREXCEPT)
#include <fenv.h>
#endif
[...]
#if defined(math_errhandling) && (math_errhandling & MATH_ERREXCEPT)
    feclearexcept(FE_ALL_EXCEPT);
#endif
errno = 0;
/* call the function */
#if !defined(math_errhandling) || (math_errhandling & MATH_ERRNO)
if (errno != 0){
    /* handle error */
}
#endif
#if defined(math_errhandling) && (math_errhandling & MATH_ERREXCEPT)
if (fetestexcept(FE_INVALID | FE_DIVBYZERO | FE_OVERFLOW) != 0){
    /* handle error */
}
#endif
Other functions besides pow() where detection should be used because
prevention would be too complicated include erfc(), lgamma() and tgamma().
                                        Posted by geoffclare at Apr 04, 2008 12:24
                                     |
| There is essentially no reason for a program to invoke pow() with a negative base.
                                        Posted by dagwyn at Apr 16, 2008 19:38
                                     |
| I've addressed these comments. I included Geoff's code sample under 'Compliant Example: Error Checking'
                                        Posted by svoboda at May 02, 2008 13:07
                                     |
| Your changes helped a lot, but there were still some problems relating to pow().; I have attempted to fix them.
                                        Posted by geoffclare at May 06, 2008 05:44
                                     |
| Shaun,
regarding the second NCCE under pow(), what does "result cannot be represented as a double" mean? It means the result is either a NaN or Infty... we can check for those two after computing the pow() to ensure no range errors happened, ahh... the beauty of  floating point 
                                        Posted by avolkovi at Jun 04, 2008 13:07
                                     |
| "result cannot be represented as a double" means the true (mathematical) result is outside the range of values that can be represented by double.; It does not mean the result is NaN or Infinity.  E.g. for pow(10.,1e6) the true result is ten to the power of one million, which is larger than DBL_MAX and therefore cannot be represented as a double.   The true result is not infinity.
Also note that some implementations do not support Inifinity and/or NaN, and so applications cannot reply on them being returned.
                                        Posted by geoffclare at Jun 05, 2008 05:48
                                     |
| This should be checkable by Rose. But there is a snag. The isLess() etc. functions, which are being used to do range checking, are not defined. If we could simply check for "x > 0.0", then we can do it. Is that what isGreater(x, 0) really means?
                                        Posted by svoboda at Jun 18, 2008 19:10
                                     |
| The difference between x > 0.0 and isgreater(x,0) is that isgreater(x,0) will not raise a floating-point exception if x is a NaN.
If you want to switch to using the operators, you would have to add explicit isnan() checks (in the cases where there isn't one already).
                                        Posted by geoffclare at Jun 20, 2008 10:28
                                     |
| For consistency with the way pow() was treated, shouldn't the new tgamma() examples have a NCCE that does no checking, then a NCCE that does only the domain checks, and then just give a reference to the Error Checking and Detection section instead of having a CS that duplicates code from it
                                        Posted by geoffclare at Jul 24, 2008 12:01
                                     |
| In that case, we should add the FE_UNDERFLOW flag to the Error Checking section
                                        Posted by avolkovi at Jul 24, 2008 12:30
                                     |
| agreed; the pow() section and the tgamma() section both follow the same outline.
                                        Posted by svoboda at Jul 24, 2008 12:31
                                     |
| Java universally deals with this issue by returning NaN; it might be worth a guideline to check if the result a math operation is Nan? Removing the exportable-java guideline.
                                        Posted by jpaulson at Mar 28, 2011 16:00
                                     |
| The new safe_sqrt() exemplar seems to me to be not very exemplary, as it handles the domain error in a particularly unhelpful way.; Is there a reason not to use the usual convention of a /* Handle error */ comment here?
                                        Posted by geoffclare at Apr 15, 2014 10:29
                                     |
| Agreed...fixed.
                                        Posted by svoboda at Apr 15, 2014 12:06
                                     |
| I think row 6 in the table should be asinh() and not asin()
                                        Posted by jeremyh at Nov 08, 2015 05:05
                                     |
| For log(x), log10(x), log2(x) I think the domain should be x > 0 rather than x >= 0 because they produce a pole error for x == 0.;  Log1p looks correct, the domain is given as x > -1.0  
                                        Posted by jeremyh at Nov 08, 2015 07:58
                                     |
| No, you have it backwards.; If x == 0 was outside the domain of the function, log(0) would produce a domain error, not a pole error.  The mistake is for log1p(x) which should give the domain as x >= -1.0.
                                        Posted by geoffclare at Nov 08, 2015 11:47
                                     |
| Agreed. I've fixed it, thanks!
                                        Posted by aballman at Nov 09, 2015 09:59
                                     |
| I looked at the wording in the standard, and I agree that log(), log10(), and log2();seem to be correct, while log1p() was incorrect with its domain. I've corrected.
                                        Posted by aballman at Nov 09, 2015 10:05
                                     |
| I noticed that in the documentation for cos(), sin(), and tan():Errors are reported as specified in math_errhandlingIf the implementation supports IEEE floating-point arithmetic (IEC 60559),if the argument is ±0, the result is 1.0if the argument is ±∞, NaN is returned and FE_INVALID is raisedif the argument is NaN, NaN is returnedI think it makes sense to add cos(), sin(), and tan() to the list as well.
                                        Posted by eddieohagan at Oct 13, 2016 10:25
                                     |
| tan() could certainly be in that list with a pole check, since;tan() returns an infinity as the function approaches pi / 2. However, I don't believe any IEEE floating point representation can exactly represent pi / 2, so I don't believe a pole error can technically occur in practice. I'm uncertain of how we might want to represent that in the list.We would have to do a lot more research before adding cos() and sin() to that list, because that's a difference in specification between POSIX and C. The C standard does not define any domain error when given infinity or NaN, while POSIX does. I suspect similar distinctions occur for other functions. We would need to make mention of where POSIX and C differ.
                                        Posted by aballman at Oct 13, 2016 11:03
                                     |
| The domain of atan2( y, x ) should be x != 0 || y != 0.x or y may be zero, only the case x=0 ∧ y=0 is undefined.
                                        Posted by netzwolf at Jan 31, 2022 11:35
                                     |
| Wait, isn't even that case defined too? In the C17 standard, under F.10.1.4, it says "atan2(±0, −0) returns ±π" and "atan2(±0, +0) returns ±0".
                                        Posted by jcsible at Jan 31, 2022 12:17
                                     |
| Correct. The C23 draft standard (sF.10.1.4) says:atan2(±0,−0)returns ±π.404Footnote 404:
atan2(0, 0) does not raise the "invalid" floating-point exception, nor does atan2(y, 0) raise the "divide-by-zero" floating- point exception.
Whether passing zeroes in constitutes a domain error depends on how you define atan2(y,x). Every definition I've seen references the "intermediate value" of y/x, which is undefined for x=y=0. But ISO C is clear on atan2(0,0) for both positive and negative zero :) So I took out the domain error.
                                        Posted by svoboda at Jan 31, 2022 13:44
                                     |
| Thanks for the clarifications and the reference to the standards. I noticed that the domain was obviously too narrow, but didn't realize that there is no domain restriction at all.
                                        Posted by netzwolf at Jan 31, 2022 15:00
                                     |

