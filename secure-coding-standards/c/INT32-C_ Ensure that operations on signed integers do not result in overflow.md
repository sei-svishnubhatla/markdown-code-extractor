Signed integer overflow is [undefined behavior 36](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Consequently, [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) have considerable latitude in how they deal with signed integer overflow. (See [MSC15-C. Do not depend on undefined behavior](MSC15-C_%20Do%20not%20depend%20on%20undefined%20behavior).) An implementation that defines signed integer types as being modulo, for example, need not detect integer overflow. Implementations may also trap on signed arithmetic overflows, or simply assume that overflows will never happen and generate object code accordingly.  It is also possible for the same conforming implementation to emit code that exhibits different behavior in different contexts. For example, an implementation may determine that a signed integer loop control variable declared in a local scope cannot overflow and may emit efficient code on the basis of that determination, while the same implementation may determine that a global variable used in a similar context will wrap.
For these reasons, it is important to ensure that operations on signed integers do not result in overflow. Of particular importance are operations on signed integer values that originate from a [tainted source](BB.-Definitions_87152273.html#BB.Definitions-taintedsource) and are used as
-   Integer operands of any pointer arithmetic, including array indexing
-   The assignment expression for the declaration of a variable length array
-   The postfix expression preceding square brackets `[]` or the expression in square brackets `[]` of a subscripted designation of an element of an array object
-   Function arguments of type `size_t` or `rsize_t` (for example, an argument to a memory allocation function)
Integer operations will overflow if the resulting value cannot be represented by the underlying representation of the integer. The following table indicates which operations can result in overflow.

| Operator | Overflow | Operator | Overflow | Operator | Overflow | Operator | Overflow |
| ----|----|----|----|----|----|----|----|
| + | Yes | -= | Yes | << | Yes | < | No |
| - | Yes | *= | Yes | >> | No | > | No |
| * | Yes | /= | Yes | & | No | >= | No |
| / | Yes | %= | Yes | | | No | <= | No |
| % | Yes | <<= | Yes | ^ | No | == | No |
| ++ | Yes | >>= | No | ~ | No | != | No |
| -- | Yes | &= | No | ! | No | && | No |
| = | No | |= | No | unary + | No | || | No |
| += | Yes | ^= | No | unary - | Yes | ?: | No |

The following sections examine specific operations that are susceptible to integer overflow. When operating on integer types with less precision than `int`, integer promotions are applied. The usual arithmetic conversions may also be applied to (implicitly) convert operands to equivalent types before arithmetic operations are performed. Programmers should understand integer conversion rules before trying to implement secure arithmetic operations. (See [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules).)
## Implementation Details
GNU GCC invoked with the [`-fwrapv`](http://gcc.gnu.org/onlinedocs/gcc-4.5.2/gcc/Code-Gen-Options.html#index-fwrapv-2088) command-line option defines the same modulo arithmetic for both unsigned and signed integers.
GNU GCC invoked with the [`-ftrapv`](http://gcc.gnu.org/onlinedocs/gcc-4.5.2/gcc/Code-Gen-Options.html#index-ftrapv-2088) command-line option causes a trap to be generated when a signed integer overflows, which will most likely abnormally exit. On a UNIX system, the result of such an event may be a signal sent to the process.
GNU GCC invoked without either the `-fwrapv` or the `-ftrapv` option may simply assume that signed integers never overflow and may generate object code accordingly.
## Atomic Integers
The C Standard defines the behavior of arithmetic on atomic signed integer types to use two's complement representation with silent wraparound on overflow; there are no undefined results. Although defined, these results may be unexpected and therefore carry similar risks to [unsigned integer wrapping](BB.-Definitions_87152273.html#BB.Definitions-unsignedintegerwrapping). (See [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).) Consequently, signed integer overflow of atomic integer types should also be prevented or detected. 
## Addition
Addition is between two operands of arithmetic type or between a pointer to an object type and an integer type. This rule applies only to addition between two operands of arithmetic type. (See [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object) and [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts).)
Incrementing is equivalent to adding 1.
### Noncompliant Code Example
This noncompliant code example can result in a signed integer overflow during the addition of the signed operands `si_a` and `si_b`:
``` c
void func(signed int si_a, signed int si_b) {
  signed int sum = si_a + si_b;
  /* ... */
}
```
### Compliant Solution
This compliant solution ensures that the addition operation cannot overflow, regardless of representation:
``` c
#include <limits.h>
void f(signed int si_a, signed int si_b) {
  signed int sum;
  if (((si_b > 0) && (si_a > (INT_MAX - si_b))) ||
      ((si_b < 0) && (si_a < (INT_MIN - si_b)))) {
    /* Handle error */
  } else {
    sum = si_a + si_b;
  }
  /* ... */
}
```
### Compliant Solution (GNU)
This compliant solution uses the GNU extension `__builtin_sadd_overflow`, available with GCC, Clang, and ICC:
``` c
void f(signed int si_a, signed int si_b) {
  signed int sum;
  if (__builtin_sadd_overflow(si_a, si_b, &sum)) {
    /* Handle error */
  }
  /* ... */
}
```
## Subtraction
Subtraction is between two operands of arithmetic type, two pointers to qualified or unqualified versions of compatible object types, or a pointer to an object type and an integer type. This rule applies only to subtraction between two operands of arithmetic type. (See [ARR36-C. Do not subtract or compare two pointers that do not refer to the same array](ARR36-C_%20Do%20not%20subtract%20or%20compare%20two%20pointers%20that%20do%20not%20refer%20to%20the%20same%20array), [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object), and [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts) for information about pointer subtraction.)
Decrementing is equivalent to subtracting 1.
### Noncompliant Code Example
This noncompliant code example can result in a signed integer overflow during the subtraction of the signed operands `si_a` and `si_b`:
``` c
void func(signed int si_a, signed int si_b) {
  signed int diff = si_a - si_b;
  /* ... */
}
```
### Compliant Solution
This compliant solution tests the operands of the subtraction to guarantee there is no possibility of signed overflow, regardless of representation:
``` c
#include <limits.h>
void func(signed int si_a, signed int si_b) {
  signed int diff;
  if ((si_b > 0 && si_a < INT_MIN + si_b) ||
      (si_b < 0 && si_a > INT_MAX + si_b)) {
    /* Handle error */
  } else {
    diff = si_a - si_b;
  }
  /* ... */
}
```
### Compliant Solution (GNU)
This compliant solution uses the GNU extension `__builtin_ssub_overflow`, available with GCC, Clang, and ICC:
``` c
void func(signed int si_a, signed int si_b) {
  signed int diff;
  if (__builtin_ssub_overflow(si_a, si_b, &diff)) {
    /* Handle error */
  }
  /* ... */
}
```
## Multiplication
Multiplication is between two operands of arithmetic type.
### Noncompliant Code Example
This noncompliant code example can result in a signed integer overflow during the multiplication of the signed operands `si_a` and `si_b`:
``` c
void func(signed int si_a, signed int si_b) {
  signed int result = si_a * si_b;
  /* ... */
}
```
### Compliant Solution
The product of two operands can always be represented using twice the number of bits than exist in the precision of the larger of the two operands. This compliant solution eliminates signed overflow on systems where `long long` is at least twice the precision of `int`:
``` c
#include <stddef.h>
#include <assert.h>
#include <limits.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(umax_value) popcount(umax_value) 
void func(signed int si_a, signed int si_b) {
  signed int result;
  signed long long tmp;
  assert(PRECISION(ULLONG_MAX) >= 2 * PRECISION(UINT_MAX));
  tmp = (signed long long)si_a * (signed long long)si_b;
  /*
   * If the product cannot be represented as a 32-bit integer,
   * handle as an error condition.
   */
  if ((tmp > INT_MAX) || (tmp < INT_MIN)) {
    /* Handle error */
  } else {
    result = (int)tmp;
  }
  /* ... */
}
```
The assertion fails if long long has less than twice the precision of int. The  PRECISION() macro and popcount() function provide the correct precision for any integer type. (See INT35-C. Use correct integer precisions.)
### Compliant Solution
The following portable compliant solution can be used with any conforming implementation, including those that do not have an integer type that is at least twice the precision of int:
``` c
#include <limits.h>
void func(signed int si_a, signed int si_b) {
  signed int result;  
  if (si_a > 0) {  /* si_a is positive */
    if (si_b > 0) {  /* si_a and si_b are positive */
      if (si_a > (INT_MAX / si_b)) {
        /* Handle error */
      }
    } else { /* si_a positive, si_b nonpositive */
      if (si_b < (INT_MIN / si_a)) {
        /* Handle error */
      }
    } /* si_a positive, si_b nonpositive */
  } else { /* si_a is nonpositive */
    if (si_b > 0) { /* si_a is nonpositive, si_b is positive */
      if (si_a < (INT_MIN / si_b)) {
        /* Handle error */
      }
    } else { /* si_a and si_b are nonpositive */
      if ( (si_a != 0) && (si_b < (INT_MAX / si_a))) {
        /* Handle error */
      }
    } /* End if si_a and si_b are nonpositive */
  } /* End if si_a is nonpositive */
  result = si_a * si_b;
}
```
### Compliant Solution (GNU)
This compliant solution uses the GNU extension `__builtin_smul_overflow`, available with GCC, Clang, and ICC:
``` c
void func(signed int si_a, signed int si_b) {
  signed int result;
  if (__builtin_smul_overflow(si_a, si_b, &result)) {
    /* Handle error */
  }
}
```
## Division
Division is between two operands of arithmetic type. Overflow can occur during two's complement signed integer division when the dividend is equal to the minimum (negative) value for the signed integer type and the divisor is equal to `−1`. Division operations are also susceptible to divide-by-zero errors. (See [INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors](INT33-C_%20Ensure%20that%20division%20and%20remainder%20operations%20do%20not%20result%20in%20divide-by-zero%20errors).)
### Noncompliant Code Example
This noncompliant code example prevents divide-by-zero errors in compliance with  INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors but does not prevent a signed integer overflow error in two's-complement. 
``` c
void func(signed long s_a, signed long s_b) {
  signed long result;
  if (s_b == 0) {
    /* Handle error */
  } else {
    result = s_a / s_b;
  }
  /* ... */
}
```
### Implementation Details
On the x86-32 architecture, overflow results in a fault, which can be exploited as a  [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).
### Compliant Solution
This compliant solution eliminates the possibility of divide-by-zero errors or signed overflow:
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
The remainder operator provides the remainder when two operands of integer type are divided. Because many platforms implement remainder and division in the same instruction, the remainder operator is also susceptible to arithmetic overflow and division by zero. (See [INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors](INT33-C_%20Ensure%20that%20division%20and%20remainder%20operations%20do%20not%20result%20in%20divide-by-zero%20errors).)
### Noncompliant Code Example
Many hardware architectures implement remainder as part of the division operator, which can overflow. Overflow can occur during a remainder operation when the dividend is equal to the minimum (negative) value for the signed integer type and the divisor is equal to −1. It occurs even though the result of such a remainder operation is mathematically 0. This noncompliant code example prevents divide-by-zero errors in compliance with INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors but does not prevent integer overflow:
``` c
void func(signed long s_a, signed long s_b) {
  signed long result;
  if (s_b == 0) {
    /* Handle error */
  } else {
    result = s_a % s_b;
  }
  /* ... */
}
```
### Implementation Details
On x86-32 platforms, the remainder operator for signed integers is implemented by the `idiv` instruction code, along with the divide operator. Because `LONG_MIN / −1` overflows, it results in a software exception with `LONG_MIN % −1` as well.
### Compliant Solution
This compliant solution also tests the remainder operands to guarantee there is no possibility of an overflow:
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
## Left-Shift Operator
The left-shift operator takes two integer operands. The result of `E1 << E2` is `E1` left-shifted `E2` bit positions; vacated bits are filled with zeros. 
The C Standard, 6.5.8, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> If `E1` has a signed type and nonnegative value, and `E1 × 2`<sup>`E2`</sup> is representable in the result type, then that is the resulting value; otherwise, the behavior is undefined.

In almost every case, an attempt to shift by a negative number of bits or by more bits than exist in the operand indicates a logic error. These issues are covered by [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](INT34-C_%20Do%20not%20shift%20an%20expression%20by%20a%20negative%20number%20of%20bits%20or%20by%20greater%20than%20or%20equal%20to%20the%20number%20of%20bits%20that%20exist%20in%20the%20operand).
### Noncompliant Code Example
This noncompliant code example performs a left shift, after verifying that the number being shifted is not negative, and the number of bits to shift is valid.  The `PRECISION()` macro and `popcount()` function provide the correct precision for any integer type. (See [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions).) However, because this code does no overflow check, it can result in an unrepresentable value. 
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(umax_value) popcount(umax_value) 
void func(signed long si_a, signed long si_b) {
  signed long result;
  if ((si_a < 0) || (si_b < 0) ||
      (si_b >= PRECISION(ULONG_MAX))) {
    /* Handle error */
  } else {
    result = si_a << si_b;
  } 
  /* ... */
}
```
### Compliant Solution
This compliant solution eliminates the possibility of overflow resulting from a left-shift operation:
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(umax_value) popcount(umax_value) 
void func(signed long si_a, signed long si_b) {
  signed long result;
  if ((si_a < 0) || (si_b < 0) ||
      (si_b >= PRECISION(ULONG_MAX)) ||
      (si_a > (LONG_MAX >> si_b))) {
    /* Handle error */
  } else {
    result = si_a << si_b;
  } 
  /* ... */
}
```
## Unary Negation
The unary negation operator takes an operand of arithmetic type. Overflow can occur during two's complement unary negation when the operand is equal to the minimum (negative) value for the signed integer type.
### Noncompliant Code Example
This noncompliant code example can result in a signed integer overflow during the unary negation of the signed operand `s_a`:
``` c
void func(signed long s_a) {
  signed long result = -s_a;
  /* ... */
}
```
### Compliant Solution
This compliant solution tests the negation operation to guarantee there is no possibility of signed overflow:
``` c
#include <limits.h>
void func(signed long s_a) {
  signed long result;
  if (s_a == LONG_MIN) {
    /* Handle error */
  } else {
    result = -s_a;
  }
  /* ... */
}
```
Risk Assessment
Integer overflow can lead to buffer overflows and the execution of arbitrary code by an attacker.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT32-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | integer-overflow | Fully checked |
| CodeSonar | 8.3p0 | ALLOC.SIZE.ADDOFLOWALLOC.SIZE.IOFLOW
ALLOC.SIZE.MULOFLOW
ALLOC.SIZE.SUBUFLOW
MISC.MEM.SIZE.ADDOFLOW
MISC.MEM.SIZE.BAD
MISC.MEM.SIZE.MULOFLOW
MISC.MEM.SIZE.SUBUFLOW | Addition overflow of allocation sizeInteger overflow of allocation size
Multiplication overflow of allocation size
Subtraction underflow of allocation size
Addition overflow of size
Unreasonable size argument
Multiplication overflow of size
Subtraction underflow of size |
| Coverity | 2017.07 | TAINTED_SCALARBAD_SHIFT | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-int32-c |  |
| Helix QAC | 2024.4 | C2800, C2860C++2800, C++2860DF2801, DF2802, DF2803, DF2861, DF2862, DF2863 |  |
| Klocwork | 2024.4 | NUM.OVERFLOWCWARN.NOEFFECT.OUTOFRANGE
NUM.OVERFLOW.DF |  |
| LDRA tool suite | 9.7.1 | 493 S, 494 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT32-aCERT_C-INT32-b
CERT_C-INT32-c | Avoid signed integer overflowsInteger overflow or underflow in constant expression in '+', '-', '*' operator
Integer overflow or underflow in constant expression in '<<' operator |
| Parasoft Insure++ |  |  | Runtime analysis |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT32-C | Checks for:Integer overflowTainted division operandTainted modulo operandRule partially covered. |
| PVS-Studio | 7.35 | V1026, V1070, V1081, V1083, V1085, V5010 |  |
| TrustInSoft Analyzer | 1.38 | signed_overflow | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT02-C. Understand integer conversion rules | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT35-C. Use correct integer precisions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR30-C. Do not form or use out-of-bounds pointers or array subscripts | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR36-C. Do not subtract or compare two pointers that do not refer to the same array | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR37-C. Do not add or subtract an integer to a pointer to a non-array object | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | MSC15-C. Do not depend on undefined behavior | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | CON08-C. Do not assume that a group of calls to independently atomic methods is atomic | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | INT00-J. Perform explicit range checking to avoid integer overflow | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Arithmetic Wrap-Around Error [FIF] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Overflowing signed integers [intoflow] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-190, Integer Overflow or Wraparound | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-191 | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-680 | 2017-05-18: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-20 and INT32-C
See CWE-20 and ERR34-C
### CWE-680 and INT32-C
Intersection( INT32-C, MEM35-C) = Ø
Intersection( CWE-680, INT32-C) =
-   Signed integer overflows that lead to buffer overflows
CWE-680 - INT32-C =
-   Unsigned integer overflows that lead to buffer overflows
INT32-C – CWE-680 =
-   Signed integer overflows that do not lead to buffer overflows
### CWE-191 and INT32-C
Union( CWE-190, CWE-191) = Union( INT30-C, INT32-C)
Intersection( INT30-C, INT32-C) == Ø
Intersection(CWE-191, INT32-C) =
-   Underflow of signed integer operation
CWE-191 – INT32-C =
-   Underflow of unsigned integer operation
INT32-C – CWE-191 =
-   Overflow of signed integer operation
### CWE-190 and INT32-C
Union( CWE-190, CWE-191) = Union( INT30-C, INT32-C)
Intersection( INT30-C, INT32-C) == Ø
Intersection(CWE-190, INT32-C) =
-   Overflow (wraparound) of signed integer operation
CWE-190 – INT32-C =
-   Overflow of unsigned integer operation
INT32-C – CWE-190 =
-   Underflow of signed integer operation
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Arithmetic Boundary Conditions," pp. 211–223) |
| [ISO/IEC 9899:2024] | Subclause 6.5.8, "Bitwise shift operators" |
| [Seacord 2013b] | Chapter 5, "Integer Security" |
| [Viega 2005] | Section 5.2.7, "Integer Overflow" |
| [Warren 2002] | Chapter 2, "Basics" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152211) [](../c/Rule%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152254)
## Comments:

|  |
| ----|
| The compliant solution for unsigned int addition is rather unclear.; Is something wrong with "if (UINT_MAX - ui1 > ui2)"?
No general compliant solution for signed subtraction?
Re the general compliant solution for signed multiplication, all that nesting is rather messy, in ways that a temp var or two could help clear up.  How about this:
/* get easy cases over with fast, and eliminate 0 for the other part */
if (0 == si1 || 0 == si2) result = 0;
/* could similarly shortcut 1-case and maybe a few others */
else
{
    signed int   limit;
    signed short sign = Sign (si1);  /* may have to write this function or macro */
    if (Sign (si2) == sign) limit = INT_MAX / si2;
    else limit = INT_MIN / si2;
    /* either way, we're checking the magnitude of s1 */
    if ((1 == sign && si1 > limit) || (-1 == sign && si1 < limit))
    {
        /* handle error */
    }
    result = si1 * si2;
}

The main problem that I think may be lurking in the above, is the truncation semantics of division yielding a negative quotient, in which case limit may have to be incremented or decremented.  I have to think on that a bit more, but this should at least serve as a clearer starting point.
![](images/icons/contenttypes/comment_16.png) Posted by davearonson at Jan 07, 2008 12:19
\| \|
The following program ran to completion using Microsoft Visual Studio 2005 Version 8.0.50727.42 and run on an IA-32 Windows XP box:
``` java
int main(void) {
  // general signed
  signed int si1, si2;
  for (si1 = 0; si1 < INT_MAX; ++si1) {
    for (si2 = 0; si2 < INT_MAX; ++si2) {
      if (((si1>0) && (si2>0) && (si1 > (INT_MAX-si2))) || ((si1<0) && (si2<0) && (si1 < (INT_MIN-si2)))) {
        if ( ((si1^si2) | (((si1^(~(si1^si2) & (1 << (sizeof(int)*CHAR_BIT-1))))+si2)^si2)) >= 0);
        else printf("general signed error, two's complement ok for si1 = %d, si2 = %d.", si1, si2);
      }
      if ( ((si1^si2) | (((si1^(~(si1^si2) & (1 << (sizeof(int)*CHAR_BIT-1))))+si2)^si2)) >= 0) {
        if (((si1>0) && (si2>0) && (si1 > (INT_MAX-si2))) || ((si1<0) && (si2<0) && (si1 < (INT_MIN-si2))));
        else printf("two's complement error, general signed ok for si1 = %d, si2 = %d.", si1, si2);              
      }
    } // end for all values of si2
    printf("done.\n");
  } // end for all values of si1
    return 0;
}
```
The program took a while to run, but only output "done."
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 17, 2008 11:11
\| \|
In the ~uil example, some other rule ought to be violated (something like "don't unnecessarily embed platform dependencies").; Also, if one form is faster than the other, talk to your compiler vendor, because if they are truly equivalent tests then optimization should occur.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 17:57
\| \|
The ~uil example always seems to draw criticism, so I have removed it to [MSC14-C. Do not introduce unnecessary platform dependencies](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies) and give it as a non-compliant coding example. Please have a look at this new recommendation, if you have a chance.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 16, 2008 06:05
\| \|
This rule may be technically correct, but it throws too heavy a burden on any programmer doing any math; even something as simple as `x++`.
For instance, DCL06-A has example code that computes the quadratic formula:
``` java
  x = (-b + sqrt(b*b - 4*a*c)) / (2*a);
```
Concise and elegant, but this completely ignores overflow possibilities. This code can be done mostly with ints, just excepting the `sqrt()` function and divide operator.
This rule basically requires an if statement with a complex boolean expression and a 'handle-overflow' clause for every math operation. So securing this 1-line formula would mutate it into a 30-line quagmire of if statements. The overhead of checking for overflow would completely obscure the original formula in the code.
The ideal way to handle this would be with exceptions. In Java one could just say:
``` java
  try {
    x = (-b + Math.sqrt((double) (b*b - 4*a*c))) / (2*a);
  } catch (OverflowException exception) {
    /* handle exception */
  }
```
Does C99 (or POSIX) provide any exception mechanism for integer overflow? Can we, for instance, do the math, and then check `errno`?
And on top of that, the table omits the – operator! ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2008 13:02
\| \|
Subtraction is in the table, as well as unary negation.
C99 provides no mechanism for checking integer overflow. Signed integer overflow is undefined behavior and unsigned integer arithmetic is modulo.
However, this rule does not apply to: (-b + sqrt(b\*b - 4\*a\*c)) / (2\*a);
It only applies to integer values used in any of the the following ways:
-   as an array index
-   in any pointer arithmetic
-   as a length or size of an object
-   as the bound of an array (for example, a loop counter)
-   in security-critical code
The security-critical code is sort of a catch-all, but it doesn't catch quadratic formulas.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 17, 2008 14:09
\| \|
Grr...the wiki doesn't show that by – I was referring to the decrement operator (post- or pre-), not unary minus or subtraction. ![](images/icons/emoticons/sad.svg)
I think the rule does apply to quadratic formulas, or at least, it should. If my q.f. generates the wrong result, that is an unexpected arithmetic value, even if I don't use it for an array index. The steps I would need to take to know if my q.f. gave me the right answer are the same steps you need to take to ensure your array index is correct.
The only real difference (well, besides the fact my q.f. will involve floats) is that the math involved in array indices, pointer arithmetic, etc. is usually simpler than a q.f.
Hm. There IS one other difference, and it may be crucial. You can do a q.f. on any integers (or floats). But array indices, as well as your other domains, are generally used within pre-specified domains...eg. within your static array, whose length is specified at compile time in a declaration, or at run-time with a malloc() call.
I suppose this rule's domain (eg memory-related math), the math is simpler and more optimize-able than general math like my q.f.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2008 17:03
\| \|
I'm thinking of separating out unsigned again into a "avoid wrapping" rule or possibly recommendation.
What do people think?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 19, 2008 10:50
\| \|
I think the table about overflow/not overflow is misleading, I'd split it in arithmetic, bit, assignment, and conditional operations:
-   All assignment operators can truncate.
-   Bit operations cannot overflow, but I believe they can produce a trap representation: With two's complement, INT_MIN-1 if INT_MIN == -INT_MAX. Other representations: negative zero if that is a trap representation.
-   Both \<\< and \>\> have undefined behavior if the right operand is too large. Shifting a negative value (I think), or a positive value so it becomes negative, yields undefined behavior (C99 6.5.7p4). Remember that two's complement representation does not imply silent wraparound and so on, though it's a common combination.
The two's complement add/subtract solutions are broken:
-   An int can have fewer than sizeof(int)\*CHAR_BIT value bits: Some of the bits may be padding bits. Rare enough that one might "fix" code depending on no padding by refusing to compile if there is padding though. Note, this also breaks the "compliant" solutions for shifting. Googling for "*site:securecoding.cert.org sizeof CHAR_BIT*" found several other examples.
-   As mentioned, (1 \<\< (sign bit number) is undefined. Just use ~INT_MAX, that's what the limits.h constants are for. Except that can also break:
-   Even for two's complement, INT_MIN may be -INT_MAX so ~INT_MAX can be a trap representation. An example has been mentioned once on comp.lang.c, though I think the reason was poor - the implementation not bother to implement printf("%d", -INT-MAX-1) or something.
The general compliant addition/subtraction solutions are unnecessarily big. Look at what you need to catch and reduce it a bit:
``` java
if (si1 - si2 > INT_MAX || si1 - si2 < INT_MIN) error; /* may overflow */
if (si1 > INT_MAX + si2 || si1 < INT_MIN + si2) error; /* may overflow */
/* Remove overflows: (si2 < 0 ? (above expr) : (above expr again)),
 * removing the cases where si1 would be < INT_MIN or > INT_MAX: */
if (si2 < 0 ? si1 > INT_MAX + si2 : si1 < INT_MIN + si2) error;
```
Similar for addition.
Another trick when you know both values are nonnegative (which is a common case) is to convert to unsigned, then operations are well-defined so you can test for overflow afterwards:
``` java
assert(si1 >= 0 && si2 >= 0);
unsigned res = (unsigned) si1 + si2;
if (res < si1 || res > INT_MAX) { /* wrapped around or out of range */ }
```
The general compliant multiplication solution can be reduced by first swapping si1 and si2 if si1 \> si2, or something like that. And as big as it is, it looks like a good case for doing
``` java
if (LLONG_MAX/INT_MAX > INT_MAX)
    long long solution; /* or use INTMAX_MAX and intmax_t */
else
    general solution;
```
The division and modulo tests are not quite right - the point is not that LONG_MIN is a problem, but that a value \< -LONG_MAX, if that can exist, is a problem. Also you never need to do 3 tests:
``` java
if (sl2 == -1 ? sl1 < -LONG_MAX : sl2 == 0) error;
```
The same goes for unary negation - check if si1 \< -INT_MAX. Possibly this also affects the multiplication solution, but I got tired just looking at that.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 01, 2008 12:46
\| \|
Haven't kept track of separating or not unsigned/signed, but one nitpick: "avoid wrapping" sounds wrong.; If you mean it about unsigned, well-defined wrapping is one reason to use unsigned in the first place.  About signed it's right, though one can't depend on wrapping anyway so it's better to make it a case of "don't invoke undefined behavior except when the implementation you write for defines it".
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 02, 2008 10:46
\| \|
For multiplication, this should be equivalent:
``` java
if (si1 > si2) {
    int tmp = si2; si2 = si1; si1 = tmp;
}
if (si1 > 0 ? (si2 > INT_MAX / si1) :
    (si2 != 0 && si1 < (si2 > 0 ? INT_MIN : INT_MAX) / si2)) {
    handle error;
}
result = si1 * si2;Â;
```
 It helps to play around a bit with code like that![](images/icons/emoticons/smile.svg)
However one problem with this code is that it will compile but break on C90 implementations which can round away from zero if an operand is negative.  Many implementations support part of but not all C99, so it's probably best to catch it.  Either expand the test to handle that (just the thought makes me tired![](images/icons/emoticons/smile.svg) or add something to ensure the program will not compile if it makes wrong assumptions about the implementation:
``` java
#if (-1)/2 || 1/-2 || (-1)/-2
#  error "integer division rounding away from zero not supported"
#endif
```
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 02, 2008 12:03
\| \|
<http://wiki.dinkumware.com/twiki/bin/view/WG14/CriticalUndefinedBehavior>
states
INT_MIN % -1 is well-defined in the present standard to have value 0 without trapping, but lots of implementations get wrong.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 07, 2008 10:15
\| \|
Also from the [autoconf](http://www.linuxtopia.org/online_books/linux_development_tools/autoconf_guide/autoconf_reference_guide_160.html) manual:
On CPUs of the i386 family, dividing INT_MIN by -1 yields a SIGFPE signal which by default terminates the program. Worse, taking the remainder of these two values typically yields the same signal on these CPUs, even though the C standard requires INT_MIN % -1 to yield zero because the expression does not overflow.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 08, 2008 15:25
\| \|
Added details about what INT_MIN % -1 does on various platforms.
I would assert that the standard is not clear on this point. According to C99, section 6.5.5, paragraph 6:
> When integers are divided, the result of the / operator is the algebraic quotient with any fractional part discarded.) If the quotient a/b is representable, the expression (a/b)\*b + a%b shall equal a.

But, as noted above, INT_MIN/-1 is not representable (as a signed int); therefore one can argue that INT_MIN % -1 is undefined according to the standard.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 22, 2008 16:56
\| \|
Because the result of the INT_MIN % -1 operation is representable, I think the standard requires that the operation not overflow.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 22, 2008 17:06
\| \|
Do we know of machines on which the two's complement solutions run faster than the general solutions? I just tested both solutions for signed addition on the andrew linux machines and found the two's complement solution was about 50% slower.
![](images/icons/contenttypes/comment_16.png) Posted by tjwilson at Sep 09, 2010 14:26
\| \|
C11 modified the wording slightly:
> When integers are divided, the result of the / operator is the algebraic quotient with any fractional part discarded. If the quotient a/b is representable, the expression (a/b)\*b + a%b shall equal a; otherwise, the behavior of both a/b and a%b is undefined.

The key part, to me, is "if the quotient a/b is representable...otherwise, the behavior of **both** a/b and a%b is undefined."
;
Since INT_MIN/-1 is not representable, I believe INT_MIN % -1 is undefined as well, regardless of whether the result is representable.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 10, 2013 15:50
\| \|
Yes, that's right.; We actually participated in this discussion in WG14.  INT_MIN % -1 is explicitly undefined behavior in C11.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 11, 2013 10:59
\| \|
I've mostly reviewed this rule.; I'm just wondering if it is ok to call the UWIDTH() macro on an unsigned integer type to get the width of a signed integer type.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 16, 2013 13:10
\| \|
Under "Atomic Inetgers", it says "The C Standard defines;the behavior of arithmetic on atomic signed integer types to use two's complement representation with silent wraparound on overflow." 
I'm curious to know where in the standard I can find it.
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Jun 16, 2014 02:46
\| \|
There is this from subclause 7.17.7.5 paragraph 3:
;
> For signed integer types, arithmetic is defined to use two’s complement representation with silent wrap-around on overflow; there are no undefined results.

![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 19, 2014 10:42
\| \|
> However, on;GCC 4.2.4 and newer, with optimization enabled, taking the remainder of `LONG_MIN` by `−1` yields the value `0`.

I believe this is wrong or inaccurate.
Maybe gcc will yield the answer 0 at compile time, but I don't think it will do that at run time, because that means it will be force to insert extra branch instructions at every remainder operation if it can't rule out the possibility.
![](images/icons/contenttypes/comment_16.png) Posted by ntysdd at Aug 17, 2014 05:34
\| \|
I agree; that was probably the result of constant folding.; I removed everything from the implementation dependent section except the description of x86.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 17, 2014 13:15
\| \|
I propose an alternative and simpler sanitization for signed multiplication, that could pheraphs replace the complex one reported up in this page:
    void func(int a, int b) {
    ; if((b > 0 && a > INT_MAX/b) || (b < 0 && a < INT_MAX/b)) {
        /* Handle error */
      }
      if((b > 0 && a < INT_MIN/b) || (b < -1 && a > INT_MIN/b)) {
        /* Handle error */
      }
      int result = a * b;
      /* ... */
    }
The first "if" is for overflow, the second one is for underflow. Of course you can compact them. Note that the "b\<-1" condition excludes the "INT_MIN/-1" case. I tested it for all the combinations of a and b as signed shorts, and it is equivalent to the compliant sanitization reported up in this page. It is as simple as the method proposed by @Hallvard Furuseth, but it does not require to swap the two integers.
I'm currently explaining this sanitization style to my students in my secure coding course at the university.
Do you find any critical issues in it?
![](images/icons/contenttypes/comment_16.png) Posted by pericle.perazzo at Oct 14, 2020 09:46
\| \|
I think we're misusing the term "underflow" here. It refers to floating point numbers that get too close to zero (e.g., denormals). Going too far negative is just overflow, the same as going too far positive is.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Oct 14, 2020 09:56
\| \|
In addition to Joe's comment, your code also fails to account for the fact that INT_MIN / -1 can also overflow.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 14, 2020 11:04
\| \|
It does? It looks fine to me. Which inputs to the function would cause that overflow?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Oct 14, 2020 11:14
\| \|
Oh, you're right, this code does prevent INT_MIN/-1. So yes, it does appear to solve the problem, in much the same way as our compliant solution. It's shorter, but that's also because it has no comments :)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 15, 2020 10:53
\| \|
getting TAINTED_SCALAR;error with array\[index\] as well.
![](images/icons/contenttypes/comment_16.png) Posted by ritul at Jan 21, 2022 03:34
\|
