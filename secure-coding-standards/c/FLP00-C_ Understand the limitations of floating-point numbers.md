The C programming language provides the ability to use floating-point numbers for calculations. The C Standard specifies requirements on a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) for floating-point numbers but makes few guarantees about the specific underlying floating-point representation because of the existence of competing floating-point systems.
By definition, a floating-point number is of finite precision and, regardless of the underlying implementation, is prone to errors associated with rounding. (See [FLP01-C. Take care in rearranging floating-point expressions](FLP01-C_%20Take%20care%20in%20rearranging%20floating-point%20expressions) and [FLP02-C. Avoid using floating-point numbers when precise computation is needed](FLP02-C_%20Avoid%20using%20floating-point%20numbers%20when%20precise%20computation%20is%20needed).)
The most common floating-point system is specified by the IEEE 754 standard. An older floating-point system is the IBM floating-point representation (sometimes called IBM/370). Each of these systems has different precisions and ranges of representable values. As a result, they do not represent all of the same values, are not binary compatible, and have different associated error rates.
Because of a lack of guarantees on the specifics of the underlying floating-point system, no assumptions can be made about either precision or range. Even if code is not intended to be portable, the chosen compiler's behavior must be well understood at all compiler optimization levels.
Here is a simple illustration of precision limitations. The following code prints the decimal representation of 1/3 to 50 decimal places. Ideally, it would print 50 numeral 3s:
``` java
#include <stdio.h>
int main(void) {
  float f = 1.0f / 3.0f;
  printf("Float is %.50f\n", f);
  return 0;
}
```
On 64-bit Linux, with GCC 4.1, it produces
``` java
Float is 0.33333334326744079589843750000000000000000000000000
```
On 64-bit Windows, with Microsoft Visual Studio 2012, it produces
``` java
Float is 0.33333334326744080000000000000000000000000000000000
```
Additionally, compilers may treat floating-point variables differently under different levels of optimization \[[Gough 2005](AA.-Bibliography_87152170.html#AA.Bibliography-Gough2005)\]:
``` java
double a = 3.0;
double b = 7.0;
double c = a / b;
if (c == a / b) {
  printf("Comparison succeeds\n");
} else {
  printf("Unexpected result\n");
}
```
When compiled on an IA-32 Linux machine with GCC 3.4.4 at optimization level 1 or higher, or on an IA-64 Windows machine with Microsoft Visual Studio 2012 in Debug or Release mode, this code prints
``` java
Comparison succeeds
```
On an IA-32 Linux machine with GCC 3.4.4 with optimization turned off, this code prints
``` java
Unexpected result
```
The reason for this behavior is that Linux uses the internal extended precision mode of the x87 floating-point unit (FPU) on IA-32 machines for increased accuracy during computation. When the result is stored into memory by the assignment to `c`, the FPU automatically rounds the result to fit into a `double`. The value read back from memory now compares unequally to the internal representation, which has extended precision. Windows does not use the extended precision mode, so all computation is done with double precision, and there are no differences in precision between values stored in memory and those internal to the FPU. For GCC, compiling at optimization level 1 or higher eliminates the unnecessary store into memory, so all computation happens within the FPU with extended precision \[[Gough 2005](AA.-Bibliography_87152170.html#AA.Bibliography-Gough2005)\].
The standard constant `__FLT_EPSILON__` can be used to evaluate if two floating-point values are close enough to be considered equivalent given the granularity of floating-point operations for a given implementation. `__FLT_EPSILON__` represents the difference between 1 and the least value greater than 1 that is representable as a float. The granularity of a floating-point operation is determined by multiplying the operand with the larger absolute value by `__FLT_EPSILON__`.
``` java
#include <math.h>
float RelDif(float a, float b) {
  float c = fabsf(a);
  float d = fabsf(b);
  d = fmaxf(c, d);
  return d == 0.0f ? 0.0f : fabsf(a - b) / d;
}
/* ... */
float a = 3.0f;
float b = 7.0f;
float c = a / b;
if (RelDif(c, a / b) <= __FLT_EPSILON__) {
  puts("Comparison succeeds");
} else {
  puts("Unexpected result");
}
```
On all tested platforms, this code prints
``` java
Comparison succeeds
```
For `double` precision and `long double` precision floating-point values, use a similar approach using the `__DBL_EPSILON__` and `__LDBL_EPSILON__` constants, respectively.
Consider using numerical analysis to properly understand the numerical properties of the problem.
## Risk Assessment
Failing to understand the limitations of floating-point numbers can result in unexpected computational results and exceptional conditions, possibly resulting in a violation of data integrity.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP00-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.ARITH.FMULOFLOW | Float multiplication overflow |
| ECLAIR | 1.2 | CC2.FLP00 | Fully implemented |
| Helix QAC | 2024.4 | C0275, C0581, C1490, C3339,C3340, C3341, C3342, C3362 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP00-a | Floating-point expressions shall not be tested for equality or inequality |
| PC-lint Plus | 1.4 | 777, 9252 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. FLP00-C | Checks for absorption of float operand (rec. partially covered) |

## Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this recommendation on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FLP00-CPP. Understand the limitations of floating-point numbersFLP35-CPP. Take granularity into account when comparing floating-point values |
| CERT Oracle Secure Coding Standard for Java | NUM53-J. Use the strictfp modifier for floating-point calculation consistency across platforms |
| ISO/IEC TR 24772:2013 | Floating-point Arithmetic [PLF] |

## Bibliography

|  |  |
| ----|----|
| [Gough 2005] | Section 8.6, "Floating-Point Issues" |
| [Hatton 1995] | Section 2.7.3, "Floating-Point Misbehavior" |
| [IEEE 754 2006] |  |
| [Lockheed Martin 2005] | AV Rule 202, Floating-point variables shall not be tested for exact equality or inequality |

------------------------------------------------------------------------
[](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152462)
## Comments:

|  |
| ----|
| Added a code example illustrating FP trickiness.
Ideally we would have a CCE and NCCE pair. Definitely, we need more code samples illustrating our points. This would include:
    Example on a IBM/370 architecture, but I don't believe we have one handy.
    Code that differs on a platform with differing compiler optimiation levels
    Example displaying differing precision. (I don't think my 1/3 example does this, since both runs produce 7 digits of precision, they only differ much later.)
                                        Posted by svoboda at Jun 04, 2008 17:05
                                     |
| Added code that behaves differently with and without -O
                                        Posted by avolkovi at Jun 05, 2008 13:14
                                     |
| as for the IBM/360 architecture... I don't think anyone has made a machine that uses that floating point representation since the 1970's... so we really don't need to care 
                                        Posted by avolkovi at Jun 05, 2008 15:06
                                     |
| wikipedia says that IBM Floating Point Architecture was superseded by IEEE754-1985... that is 14 years before C99, do we really need to mention it? Or can we just say that IEEE754 is the dominant while others may exist
                                        Posted by avolkovi at Jun 06, 2008 11:12
                                     |
| Mentioning real examples often helps support the article, assuming we are correct in asserting these are the two most prevalent floating point representations.
The term "superseded" in the wikipedia article may have been too strong.  The article on IBM Floating Point Architecture says:
Since 1998, IBM mainframes have also included binary floating-point units which conform to IEEE 754. Decimal floating-point was added to IBM_System_z9 GA2 in millicode and in 2008 to the IBM_System_z10 in hardware. Now IBM mainframes support three floating-point radices with 3 HFP formats, 3 BFP formats, and 3 DFP formats. There are two floating-point units per core; one supporting HFP and BFP, and one supporting DFP; note there is one register file, FPRs, which holds all 3 formats.
                                        Posted by rcs_mgr at Jun 06, 2008 13:55
                                     |
| Windows does not use the extended precision mode, so all computation is done with double precision, and there are no differences in precision between values stored in memory and those internal to the FPUThat precision is default, but it can change. Or think about "float" instead of "double", "float" does have difference in precision between values stored in memory and those internal to the FPU.More over, even stick to double, things can get weird because FPU have larger exponent field.Overflow is a problem and double rounding may occure if underflow happens.For example, Java explicitly forbids float or double values having excess precision, but still allows them having larger exponent range (for performance reasons). So they need strictfp to get reproducible or consistent results.(Java has JIT, so strange things may happen only after a particular method called a few hundred times -- I observe that exactly – I believe that will defeat the most careful tests).I don't know if that will happen with MSVC, but I believe it will happen with gcc on Windows.By the way, gcc now has an option "-fexcess-precision=standard" for C. I think it is to address these kinds of problems.
                                        Posted by ntysdd at Aug 17, 2014 15:34
                                     |

