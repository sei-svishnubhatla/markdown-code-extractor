Integer types in C have both a *size* and a *precision*. The size indicates the number of bytes used by an object and can be retrieved for any object or type using the `sizeof` operator.  The precision of an integer type is the number of bits it uses to represent values, excluding any sign and padding bits.
Padding bits contribute to the integer's size, but not to its precision. Consequently, inferring the precision of an integer type from its size may result in too large a value, which can then lead to incorrect assumptions about the numeric range of these types.  Programmers should use correct integer precisions in their code, and in particular, should not use the `sizeof` operator to compute the precision of an integer type on architectures that use padding bits or in strictly conforming (that is, portable) programs.
## Noncompliant Code Example
This noncompliant code example illustrates a function that produces 2 raised to the power of the function argument. To prevent undefined behavior in compliance with INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand, the function ensures that the argument is less than the number of bits used to store a value of type unsigned int.
``` c
#include <limits.h>
unsigned int pow2(unsigned int exp) {
  if (exp >= sizeof(unsigned int) * CHAR_BIT) {
    /* Handle error */
  }
  return 1 << exp;
}
```
However, if this code runs on a platform where `unsigned int` has one or more padding bits, it can still result in values for `exp` that are too large. For example, on a platform that stores `unsigned int` in 64 bits, but uses only 48 bits to represent the value, a left shift of 56 bits would result in undefined behavior.
## Compliant Solution
This compliant solution uses a `popcount()` function, which counts the number of bits set on any unsigned integer, allowing this code to determine the precision of any integer type, signed or unsigned.
``` c
#include <stddef.h>
#include <stdint.h>
/* Returns the number of set bits */
size_t popcount(uintmax_t num) {
  size_t precision = 0;
  while (num != 0) {
    if (num % 2 == 1) {
      precision++;
    }
    num >>= 1;
  }
  return precision;
}
#define PRECISION(umax_value) popcount(umax_value) 
```
Implementations can replace the `PRECISION()` macro with a type-generic macro that returns an integer constant expression that is the precision of the specified type for that implementation. This return value can then be used anywhere an integer constant expression can be used, such as in a static assertion. (See [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression).) The following type generic macro, for example, might be used for a specific implementation targeting the IA-32 architecture:
``` c
#define PRECISION(value)  _Generic(value, \
  unsigned char : 8, \
  unsigned short: 16, \
  unsigned int : 32, \
  unsigned long : 32, \
  unsigned long long : 64, \
  signed char : 7, \
  signed short : 15, \
  signed int : 31, \
  signed long : 31, \
  signed long long : 63)
```
The revised version of the `pow2()` function uses the `PRECISION()` macro to determine the precision of the unsigned type:
``` c
#include <stddef.h>
#include <stdint.h>
#include <limits.h>
extern size_t popcount(uintmax_t);
#define PRECISION(umax_value) popcount(umax_value)  
unsigned int pow2(unsigned int exp) {
  if (exp >= PRECISION(UINT_MAX)) {
    /* Handle error */
  }
  return 1 << exp;
}
```
### Implementation Details
Some platforms, such as the Cray Linux Environment (CLE; supported on Cray XT CNL compute nodes), provide `a _popcnt` instruction that can substitute for the `popcount()` function.
``` c
#define PRECISION(umax_value) _popcnt(umax_value)
```
## Risk Assessment
Mistaking an integer's size for its precision can permit invalid precision arguments to operations such as bitwise shifts, resulting in undefined behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT35-C | Low | Unlikely | Medium |  P2  |  L3  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports overflows due to insufficient precision. |
| CodeSonar | 8.3p0 | LANG.ARITH.BIGSHIFT | Shift Amount Exceeds Bit Width |
| Cppcheck Premium | 24.11.0 | premium-cert-int35-c |  |
| Helix QAC | 2024.4 | C0582C++3115 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-INT35-a | Use correct integer precisions when checking the right hand operand of the shift operator |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT35-C | Checks for situations when integer precisions are exceeded (rule fully covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-681, Incorrect Conversion between Numeric Types | 2017-10-30:MITRE:Unspecified Relationship2018-10-18:CERT:Partial Overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-190 and INT35-C
Intersection( INT35-C, CWE-190) = Ø
INT35-C used to map to CWE-190 but has been replaced with a new rule that has no overlap with CWE-190.
### CWE-681 and INT35-C
Intersection(INT35-C, CWE-681) = due to incorrect use of integer precision, conversion from one data type to another causing data to be omitted or translated in a way that produces unexpected values
CWE-681 - INT35-C = list2, where list2 =
-   conversion from one data type to another causing data to be omitted or translated in a way that produces unexpected values, not involving incorrect use of integer precision
INT35-C - CWE-681 = list1, where list1 = 
-   incorrect use of integer precision not related to conversion from one data type to another
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [C99 Rationale 2003] | 6.5.7, "Bitwise Shift Operators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152418)   [](../c/Rule%2004_%20Integers%20_INT_)   [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152081)
## Comments:

|  |
| ----|
| I may be becoming overly enamored with these, but I now think this would be another good application of a type generic macro.
                                        Posted by rcs_mgr at Nov 13, 2013 23:23
                                     |
| I'm wondering if we need a signed version of this function.; The standard does say this regarding the size:For each of the signed integer types, there is a corresponding (but different) unsigned integer type (designated with the keyword unsigned) that uses the same amount of storage (including sign information) and has the same alignment requirements.As this rule points out, size is not the same as width.I started researching actual architectures, but that hurt my brain.   It seems likely however that there are signed representations that use internal sign bits that may not be used to represent the value.So anyway, I’m not sure testing the width of an unsigned type is sufficient to determine the width of the corresponding signed type.I guess this might work, provided no one passes a negative number.  I started the width at one to count the sign bit: /* Returns the number of set bits */size_t popcount(intmax_t num) {  size_t width = 1;  assert(num > 0);  while (num != 0) {    if (num % 2 == 1) {      width++;    }    num >>= 1;  }  return width;}#define WIDTH(max_value) popcount(max_value) 
                                        Posted by rcs_mgr at Nov 17, 2013 09:50
                                     |
| For unsigned integer, isn't the following condition always true?UXXX_MAX = 2^PRECISION(UXXX_MAX) - 1PRECISION(UXXX_MAX) = log_2 (UXXX_MAX+1)So, a simple mapping table would do the job.;
                                        Posted by gmuenz at Aug 17, 2015 09:17
                                     |
| Yes, for an unsigned integer, that should work (assuming you don't actually use UXXX_MAX + 1, which will always result in;0 due to the overflow). However, it doesn't handle signed integer values (which also have to worry about oddball representations such as sign magnitude, etc). The _Generic example is effectively the simple mapping table solution, and it relies on types instead of values, which is a nice benefit.
                                        Posted by aballman at Aug 17, 2015 16:10
                                     |
| Thanks.My question came up because of the last CERT Secure Coding newsletter pointing to http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1899.pdfAt least for unsigned integers, the proposed *_WIDTH constants for limits.h seem to carry redundant information as we already have *_MAX.Are these constants just added for convenience? If so, the problem statement in the document is misleading.
                                        Posted by gmuenz at Aug 20, 2015 08:18
                                     |
| I think that you cannot calculate (in standard C);*_WIDTH from *_MAX in such a way that would work from a _Static_assert(), and so using macros solves that issue, even if the values may be redundant or calculable for a particular implementation.
                                        Posted by aballman at Aug 20, 2015 09:48
                                     |
| At https://groups.google.com/forum/embed/#!topic/comp.lang.c/NfedEFBFJ0k, the following formula is given:
Macro for the precision
/* Number of bits in inttype_MAX, or in any (1<<b)-1 where 0 <= b < 3E+10 */
#define IMAX_BITS(m) (                                                       \
    (m) / ((m) % 0x3fffffffL + 1) / 0x3fffffffL % 0x3fffffffL * 30           \
  + (m) % 0x3fffffffL / ((m) % 31 + 1) / 31 % 31 * 5                         \
  + 4 - 12 / ((m) % 31 + 3)                                                  \
)                                                                            \

In particular, the precision of an unsigned type `u_t` can be computed at compile-time: `IMAX_BITS((u_t) -1)`.
This is arguably better than a run-time function; it also has the advantage to be applicable to typedefs (as long as the underlying type is an unsigned integral type); finally, it does not rely on unportable macros.
![](images/icons/contenttypes/comment_16.png) Posted by loic.etienne at Aug 19, 2016 07:19
\| \|
Thank you for sharing this! I've looked it over (as well as the original link), and it seems plausible that it would work. However, I would feel more comfortable if we had a more authoritative, scholarly source than a google group link. Do you know of any other sources that can confirm the math? Also, this solution will violate;[INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap), will it not?
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 19, 2016 13:43
\| \|
I am pleased to do so.
I have unfortunately no further reference (perhaps you could ask the writer of the formula in the google group link in question).
I successfully tested the formula with gmp for each `2^k-1` with `0 <= k <= 1'000'000`, which is a trivial proof that the formula is correct over this range. The formula still holds for `k = 30'000'000'000`, but not for `k = 35'000'000'000`, in accordance with the comment. I will try to prove this formula (incl. overflow considerations) over the suitable range, and let you know if I succeed.
![](images/icons/contenttypes/comment_16.png) Posted by loic.etienne at Aug 19, 2016 18:13
\| \|
I managed to prove this formula. As to the overflows, there are none: only divisions and reminders are involved for the three summands, which are positive and whose sum is b \<= m.
**Proof of width formula**;Expand source
``` text
Lemma 0 (logarithm in base 2 of 2^B for B < 5)
----------------------------------------------
For 0 <= B < 5, M == 2^B-1: B == 4 - 12 / (M + 3)
Proof of Lemma 0
----------------
For B == 0, M ==  0: B == 0 == 4 - 12 / (M + 3);
For B == 1, M ==  1: B == 1 == 4 - 12 / (M + 3);
For B == 2, M ==  3: B == 2 == 4 - 12 / (M + 3);
For B == 3, M ==  7: B == 3 == 4 - 12 / (M + 3);
For B == 4, M == 15: B == 4 == 4 - 12 / (M + 3).
Lemma 1
-------
For 1 <= x, 0 <= y: (2^y-1) % (2^x-1) == 2^(y%x)-1
Example
-------
y == 11, x == 3
    (2^y-1) == 111'111'111'11b    { y bits }
    (2^x-1) == 111b               { x bits }
    (2^y-1) == 111'111'111'11b    { y bits }
  % (2^x-1) == 000'000'000'11b    { y%x bits }
Proof of Lemma 1
----------------
Special case y < x:
    (2^y-1) % (2^x-1) == 2^y-1 == 2^(y%x)-1
Induction over y
Anchor:
    y == 0
    proven above (y == 0 < 1 <= x)
Induction step:
    Induction hypothesis:
        for y' < y, (2^y'-1) % (2^x-1) == 2^(y'%x)-1
    case y < x
        proven above (y < x)
    case x <= y
        (2^y-1) % (2^x-1)
     == (2^(y-x)*2^x-1) % (2^x-1)
     == (2^(y-x)*(2^x-1) + 2^(y-x)-1) % (2^x-1)
     == (2^(y-x)-1) % (2^x-1)
     == 2^((y-x)%x)-1  { induction hypothesis with y' = y-x < y }
     == 2^(y%x)-1
Lemma 2 (logarithm in base 2^U of 2^B)
--------------------------------------
For 1 <= U, 0 <= B <= U*(2^U-1)-1, M == 2^B-1:
B/U == M / (M%(2^U-1) + 1) / (2^U-1) % (2^U-1)
Example
-------
U == 3, B == 14, M == 2^14-1
    2^U-1           == 111b                 { U bits }
    M               == 111'111'111'111'11b  { B bits }
    M%(2^U-1)       ==                 11b  { B%U bits }
    M%(2^U-1) + 1   ==               1'00b  { for right shift below }
    M               == 111'111'111'111'11b  { B bits }
  / (M%(2^U-1) + 1) ==    111'111'111'111b  { 111-patterns only }
  / (2^U-1)         ==    001'001'001'001b  { 001-patterns only }
  % (2^U-1)         ==                  4   { number of 001-patterns }
The last modulo makes 1000b and 1 equivalent, and thus sums up the number of
001-patterns modulo 2^U-1, which is B/U since B/U < 2^U-1.
Proof of Lemma 2
----------------
    M / (M%(2^U-1) + 1) / (2^U-1) % (2^U-1)
 == (2^B-1) / ((2^B-1)%(2^U-1) + 1) / (2^U-1) % (2^U-1)  { M == 2^B-1 }
 == (2^B-1) / 2^(B%U) / (2^U-1) % (2^U-1)  { Lemma 1 }
 == (2^(B-B%U)-1) / (2^U-1) % (2^U-1)
 == (2^(U*(B/U))-1) / (2^U-1) % (2^U-1)  { B == U*(B/U) + B%U }
 == ((2^U)^(B/U)-1) / (2^U-1) % (2^U-1)
 == (sum i in (0..(B/U)-1) (2^U)^i) % (2^U-1)  { Geometric sum }
 == (sum i in (0..(B/U)-1) 1^i) % (2^U-1)  { 2^U == 1 modulo 2^U-1 }
 == B/U % (2^U-1)
 == B/U  { B/U <= (U*(2^U-1)-1)/U == (2^U-1)-1 < 2^U-1 }
Formula 3 (width b of m == 2^b-1 with constants < 2^31)
-------------------------------------------------------
Remark 3.0:
    2^b-1 == m  { Hypothesis }
    2^(b%30)-1 == m % (2^30-1)  { Lemma 1 }
    (2^(b%30)-1)%(2^5-1) == 2^(b%5)-1 == m % (2^5-1)  { Lemma 1 }
For 0 <= b <= 30*(2^30-1) -1 == 32'212'254'689, m == 2^b-1:
    b
 ==
    b/30 * 30
  + b%30 / 5 * 5
  + b%5
 ==
    { Lemma 2 with U == 30, B == b, M == 2^b-1 }
    (2^b-1) / ((2^b-1)%(2^30-1) + 1) / (2^30-1) % (2^30-1) * 30
    { Lemma 2 with U == 5, B = b%30, M == 2^(b%30)-1 }
  + (2^(b%30)-1) / ((2^(b%30)-1)%(2^5-1) + 1) / (2^5-1) % (2^5-1) * 5
    { Lemma 0 with B == b%5, M == 2^(b%5)-1 }
  + 4 - 12 / (2^(b%5)-1 + 3)
 ==
    { Remark 3.0 }
    m / (m%(2^30-1) + 1) / (2^30-1) % (2^30-1) * 30
  + m % (2^30-1) / (m%(2^5-1) + 1) / (2^5-1) % (2^5-1) * 5
  + 4 - 12 / (m%(2^5-1) + 3)
```
![](images/icons/contenttypes/comment_16.png) Posted by loic.etienne at Sep 01, 2016 15:05
\|
