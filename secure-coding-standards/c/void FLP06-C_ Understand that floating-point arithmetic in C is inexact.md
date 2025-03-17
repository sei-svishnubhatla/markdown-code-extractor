> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [FLP00-C. Understand the limitations of floating-point numbers](FLP00-C_%20Understand%20the%20limitations%20of%20floating-point%20numbers)

Floating-point arithmetic in C is inexact. In particular, make sure that floating-point comparisons account for the underlying precision of the implementation.
## Noncompliant Code Example
The result of the comparison of `c` and `a / b` is implementation-dependent:
``` c
float a = 3.0;
float b = 7.0;
float c = a / b;
if (c == a / b) {
  puts("Comparison succeeds");
} else {
  puts("Unexpected result");
}
```
### Implementation Details
When compiled on an x86-32 Linux machine with a GCC compiler, version 4.7.2, at optimization level 1 or higher, or on a test x86-32 Windows 8 machine with Microsoft Visual Studio 2012, this code prints
``` java
Comparison succeeds
```
On an IA-32 Linux machine with a GCC compiler, version 4.7.2, with optimization turned off, this code prints
``` java
Unexpected result
```
## Compliant Solution
This compliant solution uses the standard constant `__FLT_EPSILON__` to evaluate if two floating-point values are close enough to be considered equivalent given the granularity of floating-point operations for a given implementation. `__FLT_EPSILON__` represents the difference between 1 and the least value greater than 1 that is representable as a float. The granularity of a floating-point operation is determined by multiplying the operand with the larger absolute value by `__FLT_EPSILON__`.
``` c
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

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP06-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ECLAIR | 1.2 | CC2.FLP06 | Fully implemented |

### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | FLP35-CPP. Take granularity into account when comparing floating-point values |

## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.7.3, "Floating-Point Misbehavior" |
| [Lockheed Martin 2005] | AV Rule 202, Floating-point variables shall not be tested for exact equality or inequality |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FLP05-C.+Don%27t+use+denormalized+numbers?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=372) [](https://www.securecoding.cert.org/confluence/display/seccode/FLP30-C.+Do+not+use+floating-point+variables+as+loop+counters?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This rule was reviewed and rejected by WG14.  Is this an attempt to resurrect it?  If so, I think we should take some more time to understand their objections and see if this rule can be stated in such a fashion as to eliminate their objections.
                                        Posted by rcs at Nov 03, 2008 09:42
                                     |
| I believe that in IEEE Standard 754 Floating-Point integers are represented by exact values, and if the result is also an integral value they are guaranteed to be an exact match.  Do we want to list this case as an exception to this rule?
                                        Posted by rcs at Jan 09, 2009 16:25
                                     |
| For reference, here is the 'dead' version of this rule:
VOID FLP30-C. Take granularity into account when comparing floating point values
                                        Posted by svoboda at Feb 12, 2009 11:09
                                     |
| Jim Thomas from HP asked me to remove the shortened version of this rule from the n1393 which I did because the rule was shortened to the form of "don't compare floating point numbers".  I'm still concerned that this rule implies that all equality comparisons of floating point numbers in code must be diagnosed (unless logic for granularity can be identified) and that this is going to create too many false positives.
                                        Posted by rcs at Oct 30, 2009 04:54
                                     |
| As I read it, this rule proscribes using == on two floats/doubles, which is not in itself the problem. Code like this is perfectly reliable:
  float x = y;
  if (x == y) {puts("true");}

The problem comes when two floats are compared after either or both have undergone math. (division in the case of the NCCE). Perhaps the rule should say "don't test for equality two floats if either is the result of a mathematical operation"
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 17, 2010 08:38
\| \|
When I programmed in APL a long time ago,
We had a user global (Quad CT) for comparison tolerance.; It was by default 10\*\*-<sup>10 </sup> or 0.0000000001
Thus, if both a and b are floats
a equals b iff abs(a-b) \< Quad CT
For finance stuff, we set QuadCT to 10\*\*<sup>-4 </sup>  0.0001
1.0/3.0 == 0.3333 with QuadCT set to 10\*\*<sup>-4</sup>
![](images/icons/contenttypes/comment_16.png) Posted by lsatenstein at Sep 18, 2012 19:54
\|
