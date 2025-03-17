The C Standard identifies the following condition under which division and remainder operations result in undefined behavior (UB):

|  |  |
| ----|----|
| UB | Description |
| 41 | The value of the second operand of the;/ or % operator is zero (6.5.5). |

Ensure that division and remainder operations do not result in divide-by-zero errors.
## Division
The result of the `/` operator is the quotient from the division of the first arithmetic operand by the second arithmetic operand. Division operations are susceptible to divide-by-zero errors. Overflow can also occur during two's complement signed integer division when the dividend is equal to the minimum (most negative) value for the signed integer type and the divisor is equal to `−1.` (See [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow).)
### Noncompliant Code Example
This noncompliant code example prevents signed integer overflow in compliance with INT32-C. Ensure that operations on signed integers do not result in overflow but fails to prevent a divide-by-zero error during the division of the signed operands `s_a` and `s_b`:  
``` c
#include <limits.h>
void func(signed long s_a, signed long s_b) {
  signed long result;
  if ((s_a == LONG_MIN) && (s_b == -1)) {
    /* Handle error */
  } else {
    result = s_a / s_b;
  }
  /* ... */
}
```
### Compliant Solution
This compliant solution tests the division operation to guarantee there is no possibility of divide-by-zero errors or signed overflow:
``` c
#include <limits.h>
void func(signed long s_a, signed long s_b) {
  signed long result;
  if ((s_b == 0) || ((s_a == LONG_MIN) && (s_b == -1))) {
    /* Handle error */
  } else {
    result = s_a / s_b;
  }
  /* ... */
}
```
## Remainder
The remainder operator provides the remainder when two operands of integer type are divided. 
### Noncompliant Code Example
This noncompliant code example prevents signed integer overflow in compliance with INT32-C. Ensure that operations on signed integers do not result in overflow but fails to prevent a divide-by-zero error during the remainder operation on the signed operands `s_a` and `s_b`:
``` c
#include <limits.h>
void func(signed long s_a, signed long s_b) {
  signed long result;
  if ((s_a == LONG_MIN) && (s_b == -1)) {
    /* Handle error */
  } else {
    result = s_a % s_b;
  }
  /* ... */
}
```
### Compliant Solution
This compliant solution tests the remainder operand to guarantee there is no possibility of a divide-by-zero error or an overflow error:
``` c
#include <limits.h>
void func(signed long s_a, signed long s_b) {
  signed long result;
  if ((s_b == 0 ) || ((s_a == LONG_MIN) && (s_b == -1))) {
    /* Handle error */
  } else {
    result = s_a % s_b;
  }
  /* ... */
}
```
## Risk Assessment
A divide-by-zero error can result in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) and denial of service.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT33-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | int-division-by-zeroint-modulo-by-zero | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT33 |  |
| CodeSonar | 8.3p0 | LANG.ARITH.DIVZEROLANG.ARITH.FDIVZERO
 | Division by zeroFloat Division By Zero |
| Compass/ROSE |  |  | Can detect some violations of this rule (In particular, it ensures that all operations involving division or modulo are preceded by a check ensuring that the second operand is nonzero.) |
| Coverity | 2017.07 | DIVIDE_BY_ZERO | Fully implemented |
| Cppcheck | ;2.15 | zerodivzerodivcond |  |
| Cppcheck Premium | 24.11.0 | zerodivzerodivcondpremium-cert-int33-c |  |
| Helix QAC | 2024.4 | C2830C++2830DF2831, DF2832, DF2833 |  |
| Klocwork | 2024.4 | DBZ.CONSTDBZ.CONST.CALL
DBZ.GENERAL
DBZ.ITERATOR
DBZ.ITERATOR.CALL |  |
| LDRA tool suite | 9.7.1 | 43 D, 127 D, 248 S, 629 S, 80 X | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT33-a | Avoid division by zero |
| Parasoft Insure++ |  |  | Runtime analysis |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT33-C | Checks for:Integer division by zeroTainted division operandTainted modulo operandRule fully covered. |
| SonarQube C/C++ Plugin | 3.11 | S3518 |  |
| PVS-Studio | 7.35 | V609 |  |
| TrustInSoft Analyzer | 1.38 | division_by_zero | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT32-C. Ensure that operations on signed integers do not result in overflow | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | NUM02-J. Ensure that division and remainder operations do not result in divide-by-zero errors | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Integer division errors [diverr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-369, Divide By Zero | 2017-07-07: CERT: Exact |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-682 and INT33-C
CWE-682 = Union( INT33-C, list) where list =
-   Incorrect calculations that do not involve division by zero
## Bibliography

|  |  |
| ----|----|
| [Seacord 2013b] | Chapter 5, "Integer Security" |
| [Warren 2002] | Chapter 2, "Basics" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152210) [](../c/Rule%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152418)
## Comments:

|  |
| ----|
| Add compliant solutions demonstrating the use of signals in Linux and structured exception handling in Windows?
                                        Posted by extwikiadmin at Jul 28, 2006 01:57
                                     |
| Another division and modulo nuance that might be worth including is their ability to return negative numbers. This is probably obvious for division, but it can be surprising sometimes when (-10 % 1024) evaluates to -10. One possible concern would be in code for hash tables that takes a user malleable signed index.
                                        Posted by jm at Dec 25, 2006 15:43
                                     |
| INT32 already has the NCCE/CCE pairs mentioned here. (although INT32 is strictly about signed integers.)
                                        Posted by svoboda at Jun 18, 2008 15:12
                                     |
| I don't think the "stupid" NCE adds anything, and in fact, it recreates the problem you were trying to fix in having a noncompliant example that violates multiple rules.;
                                        Posted by rcs_mgr at Nov 11, 2013 23:41
                                     |
| I added the 'stupid' NCCE b/c it is more likely to occur in the real world. Normally I am uncomfortable with NCCEs that violate multiple rules, but I feel less uncomfortable than usual here because we already have an NCCE (the 2nd one) that violates this rule but no others.I considered adding this 'stupid' NCCE to INT32-C but felt that that rule was long enough already.
                                        Posted by svoboda at Nov 12, 2013 09:13
                                     |
| Yeah, no one does any checking in the real world, but based on our examples, they can figure out this is wrong.; I'm going to remove.
                                        Posted by rcs at Nov 12, 2013 09:16
                                     |

