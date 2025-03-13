 

Signed integer overflow is [undefined behavior
36](/confluence/display/c/BB.+Definitions#BB.Definitions-undefinedbehavior).
Consequently,
[implementations](/confluence/display/c/BB.+Definitions#BB.Definitions-implementation)
have considerable latitude in how they deal with signed integer
overflow. (See [MSC15-C. Do not depend on undefined
behavior](/confluence/display/c/MSC15-C.+Do+not+depend+on+undefined+behavior).)
An implementation that defines signed integer types as being modulo, for
example, need not detect integer overflow. Implementations may also trap
on signed arithmetic overflows, or simply assume that overflows will
never happen and generate object code accordingly.  It is also possible
for the same conforming implementation to emit code that exhibits
different behavior in different contexts. For example, an implementation
may determine that a signed integer loop control variable declared in a
local scope cannot overflow and may emit efficient code on the basis of
that determination, while the same implementation may determine that a
global variable used in a similar context will wrap.

For these reasons, it is important to ensure that operations on signed
integers do not result in overflow. Of particular importance are
operations on signed integer values that originate from a [tainted
source](/confluence/display/c/BB.+Definitions#BB.Definitions-taintedsource)
and are used as

- Integer operands of any pointer arithmetic, including array indexing
- The assignment expression for the declaration of a variable length
  array
- The postfix expression preceding square brackets `[]` or the
  expression in square brackets `[]` of a subscripted designation of an
  element of an array object
- Function arguments of type `size_t` or `rsize_t` (for example, an
  argument to a memory allocation function)

Integer operations will overflow if the resulting value cannot be
represented by the underlying representation of the integer. The
following table indicates which operations can result in overflow.

|          |          |          |          |           |          |          |          |
|----------|----------|----------|----------|-----------|----------|----------|----------|
| Operator | Overflow | Operator | Overflow | Operator  | Overflow | Operator | Overflow |
| `+`      | Yes      | `-=`     | Yes      | `<<`      | Yes      | `<`      | No       |
| `-`      | Yes      | `*=`     | Yes      | `>>`      | No       | `>`      | No       |
| `*`      | Yes      | `/=`     | Yes      | `&`       | No       | `>=`     | No       |
| `/`      | Yes      | `%=`     | Yes      | `|`       | No       | `<=`     | No       |
| `%`      | Yes      | `<<=`    | Yes      | `^`       | No       | `==`     | No       |
| `++`     | Yes      | `>>=`    | No       | `~`       | No       | `!=`     | No       |
| `--`     | Yes      | `&=`     | No       | `!`       | No       | `&&`     | No       |
| `=`      | No       | `|=`     | No       | `unary +` | No       | `||`     | No       |
| `+=`     | Yes      | `^=`     | No       | `unary -` | Yes      | `?:`     | No       |

The following sections examine specific operations that are susceptible
to integer overflow. When operating on integer types with less precision
than `int`, integer promotions are applied. The usual arithmetic
conversions may also be applied to (implicitly) convert operands to
equivalent types before arithmetic operations are performed. Programmers
should understand integer conversion rules before trying to implement
secure arithmetic operations. (See [INT02-C. Understand integer
conversion
rules](/confluence/display/c/INT02-C.+Understand+integer+conversion+rules).)

## Implementation Details

GNU GCC invoked with the
[`-fwrapv`](http://gcc.gnu.org/onlinedocs/gcc-4.5.2/gcc/Code-Gen-Options.html#index-fwrapv-2088)
command-line option defines the same modulo arithmetic for both unsigned
and signed integers.

GNU GCC invoked with the
[`-ftrapv`](http://gcc.gnu.org/onlinedocs/gcc-4.5.2/gcc/Code-Gen-Options.html#index-ftrapv-2088)
command-line option causes a trap to be generated when a signed integer
overflows, which will most likely abnormally exit. On a UNIX system, the
result of such an event may be a signal sent to the process.

GNU GCC invoked without either the `-fwrapv` or the `-ftrapv` option may
simply assume that signed integers never overflow and may generate
object code accordingly.

## Atomic Integers

The C Standard defines the behavior of arithmetic on atomic signed
integer types to use two's complement representation with silent
wraparound on overflow; there are no undefined results. Although
defined, these results may be unexpected and therefore carry similar
risks to [unsigned integer
wrapping](/confluence/display/c/BB.+Definitions#BB.Definitions-unsignedintegerwrapping). (See [INT30-C.
Ensure that unsigned integer operations do not
wrap](/confluence/display/c/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap).)
Consequently, signed integer overflow of atomic integer types should
also be prevented or detected. 

  

  

## Addition

Addition is between two operands of arithmetic type or between a pointer
to an object type and an integer type. This rule applies only to
addition between two operands of arithmetic type. (See [ARR37-C. Do not
add or subtract an integer to a pointer to a non-array
object](/confluence/display/c/ARR37-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+to+a+non-array+object)
and [ARR30-C. Do not form or use out-of-bounds pointers or array
subscripts](/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts).)

Incrementing is equivalent to adding 1.

### Noncompliant Code Example

This noncompliant code example can result in a signed integer overflow
during the addition of the signed operands `si_a` and `si_b`:

    void func(signed int si_a, signed int si_b) {
      signed int sum = si_a + si_b;
      /* ... */
    }

### <span style="line-height: 1.5;">Compliant Solution</span>

This compliant solution ensures that the addition operation cannot
overflow, regardless of representation:

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

### Compliant Solution (GNU) 

This compliant solution uses the GNU extension
`__builtin_sadd_overflow`, available with GCC, Clang, and ICC:

    void f(signed int si_a, signed int si_b) {
      signed int sum;
      if (__builtin_sadd_overflow(si_a, si_b, &sum)) {
        /* Handle error */
      }
      /* ... */
    }

  

## Subtraction

Subtraction is between two operands of arithmetic type, two pointers to
qualified or unqualified versions of compatible object types, or a
pointer to an object type and an integer type. This rule applies only to
subtraction between two operands of arithmetic type. (See [ARR36-C. Do
not subtract or compare two pointers that do not refer to the same
array](/confluence/display/c/ARR36-C.+Do+not+subtract+or+compare+two+pointers+that+do+not+refer+to+the+same+array),
[ARR37-C. Do not add or subtract an integer to a pointer to a non-array
object](/confluence/display/c/ARR37-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+to+a+non-array+object),
and [ARR30-C. Do not form or use out-of-bounds pointers or array
subscripts](/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts)
for information about pointer subtraction.)

Decrementing is equivalent to subtracting 1.

### Noncompliant Code Example

This noncompliant code example can result in a signed integer overflow
during the subtraction of the signed operands `si_a` and `si_b`:

    void func(signed int si_a, signed int si_b) {
      signed int diff = si_a - si_b;
      /* ... */
    }

### <span style="line-height: 1.5;">Compliant Solution</span>

This compliant solution tests the operands of the subtraction to
guarantee there is no possibility of signed overflow, regardless of
representation:

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

### Compliant Solution (GNU) 

This compliant solution uses the GNU extension
`__builtin_ssub_overflow`, available with GCC, Clang, and ICC:

    void func(signed int si_a, signed int si_b) {
      signed int diff;
      if (__builtin_ssub_overflow(si_a, si_b, &diff)) {
        /* Handle error */
      }

      /* ... */
    }

  

## Multiplication

Multiplication is between two operands of arithmetic type.

### Noncompliant Code Example

This noncompliant code example can result in a signed integer overflow
during the multiplication of the signed operands `si_a` and `si_b`:

    void func(signed int si_a, signed int si_b) {
      signed int result = si_a * si_b;
      /* ... */
    }

### Compliant Solution

The product of two operands can always be represented using twice the
number of bits than exist in the precision of the larger of the two
operands. This compliant solution eliminates signed overflow on systems
where `long long` is at least twice the precision of `int`:

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

<span style="line-height: 1.4285;font-size: 14.0px;">The assertion fails
if `long long` has less than twice the precision of `int`. The 
`PRECISION()` macro and `popcount()` function provide the correct
precision for any integer type. (See [INT35-C. Use correct integer
precisions](/confluence/display/c/INT35-C.+Use+correct+integer+precisions).)  
</span>

### Compliant Solution

The following portable compliant solution can be used with any
conforming implementation, including those that do not have an integer
type that is at least twice the precision of `int`:

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

### Compliant Solution (GNU) 

This compliant solution uses the GNU extension
`__builtin_smul_overflow`, available with GCC, Clang, and ICC:

    void func(signed int si_a, signed int si_b) {
      signed int result;
      if (__builtin_smul_overflow(si_a, si_b, &result)) {
        /* Handle error */
      }
    }

  

## Division

Division is between two operands of arithmetic type. Overflow can occur
during two's complement signed integer division when the dividend is
equal to the minimum (negative) value for the signed integer type and
the divisor is equal to `−1`. Division operations are also susceptible
to divide-by-zero errors. (See [INT33-C. Ensure that division and
remainder operations do not result in divide-by-zero
errors](/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors).)

### Noncompliant Code Example

This noncompliant code example prevents divide-by-zero errors in
compliance with  [INT33-C. Ensure that division and remainder operations
do not result in divide-by-zero
errors](/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors)
but does not prevent a signed integer overflow error in
two's-complement. 

    void func(signed long s_a, signed long s_b) {
      signed long result;
      if (s_b == 0) {
        /* Handle error */
      } else {
        result = s_a / s_b;
      }
      /* ... */
    }

### Implementation Details

On the x86-32 architecture, overflow results in a fault, which can be
exploited as a  [denial-of-service
attack](/confluence/display/c/BB.+Definitions#BB.Definitions-denial-of-service).

### Compliant Solution

This compliant solution eliminates the possibility of divide-by-zero
errors or signed overflow:

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

## Remainder

The remainder operator provides the remainder when two operands of
integer type are divided. Because many platforms implement remainder and
division in the same instruction, the remainder operator is also
susceptible to arithmetic overflow and division by zero. (See [INT33-C.
Ensure that division and remainder operations do not result in
divide-by-zero
errors](/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors).)

### Noncompliant Code Example

Many hardware architectures implement remainder as part of the division
operator, which can overflow. Overflow can occur during a remainder
operation when the dividend is equal to the minimum (negative) value for
the signed integer type and the divisor is equal to −1. It occurs even
though the result of such a remainder operation is mathematically 0.
This noncompliant code example prevents divide-by-zero errors in
compliance with [INT33-C. Ensure that division and remainder operations
do not result in divide-by-zero
errors](/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors)
but does not prevent integer overflow:

    void func(signed long s_a, signed long s_b) {
      signed long result;
      if (s_b == 0) {
        /* Handle error */
      } else {
        result = s_a % s_b;
      }
      /* ... */
    }

### Implementation Details

On x86-32 platforms, the remainder operator for signed integers is
implemented by the `idiv` instruction code, along with the divide
operator. Because `LONG_MIN / −1` overflows, it results in a software
exception with `LONG_MIN % −1` as well.

### Compliant Solution

This compliant solution also tests the remainder operands to guarantee
there is no possibility of an overflow:

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

  

## Left-Shift Operator

The left-shift operator takes two integer operands. The result of
`E1 << E2` is `E1` left-shifted `E2` bit positions; vacated bits are
filled with zeros. 

The C Standard, 6.5.8, paragraph 4 \[[ISO/IEC
9899:2024](/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2024)\],
states

> If `E1` has a signed type and nonnegative value, and
> `E1 × 2`<sup>`E2`</sup> is representable in the result type, then that
> is the resulting value; otherwise, the behavior is undefined.

In almost every case, an attempt to shift by a negative number of bits
or by more bits than exist in the operand indicates a logic error. These
issues are covered by [INT34-C. Do not shift an expression by a negative
number of bits or by greater than or equal to the number of bits that
exist in the
operand](/confluence/display/c/INT34-C.+Do+not+shift+an+expression+by+a+negative+number+of+bits+or+by+greater+than+or+equal+to+the+number+of+bits+that+exist+in+the+operand).

### Noncompliant Code Example

This noncompliant code example performs a left shift, after verifying
that the number being shifted is not negative, and the number of bits to
shift is valid.  The `PRECISION()` macro and `popcount()` function
provide the correct precision for any integer type. (See [INT35-C. Use
correct integer
precisions](/confluence/display/c/INT35-C.+Use+correct+integer+precisions).)
However, because this code does no overflow check, it can result in an
unrepresentable value. 

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

### Compliant Solution

This compliant solution eliminates the possibility of overflow resulting
from a left-shift operation:

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

## Unary Negation

The unary negation operator takes an operand of arithmetic type.
Overflow can occur during two's complement unary negation when the
operand is equal to the minimum (negative) value for the signed integer
type.

### Noncompliant Code Example

This noncompliant code example can result in a signed integer overflow
during the unary negation of the signed operand `s_a`:

    void func(signed long s_a) {
      signed long result = -s_a;
      /* ... */
    }

### Compliant Solution

This compliant solution tests the negation operation to guarantee there
is no possibility of signed overflow:

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

<span style="line-height: 1.5;font-size: 20.0px;">Risk Assessment</span>

Integer overflow can lead to buffer overflows and the execution of
arbitrary code by an attacker.

|  |  |  |  |  |  |
|----|----|----|----|----|----|
| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| INT32-C | High | Likely | High | <span style="color: rgb(204,153,0);">**P9**</span> | <span style="color: rgb(204,153,0);">**L2**</span> |

### Automated Detection

<table class="wrapped confluenceTable">
<tbody>
<tr>
<th class="confluenceTh"><p>Tool</p></th>
<th class="confluenceTh"><p>Version</p></th>
<th class="confluenceTh"><p>Checker</p></th>
<th class="confluenceTh"><p>Description</p></th>
</tr>
&#10;<tr>
<td class="confluenceTd"><a
href="/confluence/pages/viewpage.action?pageId=87152428">Astrée</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>integer-overflow<br />
</strong></p></td>
<td class="confluenceTd">Fully checked</td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/CodeSonar">CodeSonar</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>ALLOC.SIZE.ADDOFLOW<br />
ALLOC.SIZE.IOFLOW<br />
ALLOC.SIZE.MULOFLOW<br />
ALLOC.SIZE.SUBUFLOW<br />
MISC.MEM.SIZE.ADDOFLOW<br />
MISC.MEM.SIZE.BAD<br />
MISC.MEM.SIZE.MULOFLOW<br />
MISC.MEM.SIZE.SUBUFLOW</strong></p></td>
<td class="confluenceTd"><p>Addition overflow of allocation size<br />
Integer overflow of allocation size<br />
Multiplication overflow of allocation size<br />
Subtraction underflow of allocation size<br />
Addition overflow of size<br />
Unreasonable size argument<br />
Multiplication overflow of size<br />
Subtraction underflow of size</p></td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Coverity">Coverity</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>TAINTED_SCALAR</strong></p>
<p><strong>BAD_SHIFT</strong></p></td>
<td class="confluenceTd"><span>Implemented</span></td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Cppcheck+Premium">Cppcheck Premium</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p><span class="conf-macro output-inline"></span></p>
</div></td>
<td class="confluenceTd"><strong><span
style="color: rgb(0,0,0);">premium-cert-int32-c</span></strong></td>
<td class="confluenceTd">Partially implemented</td>
</tr>
<tr>
<td class="confluenceTd"><a href="/confluence/display/c/Helix+QAC">Helix
QAC</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>C2800, C2860</strong></p>
<p><strong>C++2800, C++2860</strong></p>
<p><strong>DF2801, DF2802, DF2803, DF2861, DF2862,
DF2863</strong></p></td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Klocwork">Klocwork</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>NUM.OVERFLOW</strong><br />
<strong>CWARN.NOEFFECT.OUTOFRANGE</strong><br />
<strong>NUM.OVERFLOW.DF</strong></p></td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="/confluence/display/c/LDRA">LDRA tool
suite</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>493 S,</strong> <strong>494
S</strong></p></td>
<td class="confluenceTd">Partially implemented</td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Parasoft">Parasoft C/C++test</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><strong>CERT_C-INT32-a</strong><br />
<strong>CERT_C-INT32-b</strong><br />
<strong>CERT_C-INT32-c</strong></p></td>
<td class="confluenceTd"><p>Avoid signed integer overflows<br />
Integer overflow or underflow in constant expression in '+', '-', '*'
operator<br />
Integer overflow or underflow in constant expression in '&lt;&lt;'
operator</p></td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Parasoft">Parasoft Insure++</a></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd">Runtime analysis</td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/Polyspace+Bug+Finder">Polyspace Bug
Finder</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><p><a
href="https://www.mathworks.com/help/bugfinder/ref/certcruleint32c.html">CERT
C: Rule INT32-C</a></p>
<p><br />
</p></td>
<td class="confluenceTd"><p>Checks for:</p>
<ul>
<li>Integer overflow</li>
<li>Tainted division operand</li>
<li>Tainted modulo operand</li>
</ul>
<p>Rule partially covered.</p></td>
</tr>
<tr>
<td class="confluenceTd"><a
href="https://wiki.sei.cmu.edu/confluence/display/cplusplus/PVS-Studio">PVS-Studio</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><strong><a
href="https://pvs-studio.com/en/docs/warnings/v1026/">V1026</a>, <a
href="https://pvs-studio.com/en/docs/warnings/v1070/">V1070</a>, <a
href="https://pvs-studio.com/en/docs/warnings/v1081/">V1081</a>, <a
href="https://pvs-studio.com/en/docs/warnings/v1083/">V1083</a>, <a
href="https://pvs-studio.com/en/docs/warnings/v1085/">V1085</a>, <a
href="https://pvs-studio.com/en/docs/warnings/v5010/">V5010</a></strong></td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a
href="/confluence/display/c/TrustInSoft+Analyzer">TrustInSoft
Analyzer</a></td>
<td class="confluenceTd"><div class="content-wrapper">
&#10;</div></td>
<td class="confluenceTd"><strong>signed_overflow<br />
</strong></td>
<td class="confluenceTd"><p>Exhaustively verified (see <a
href="https://taas.trust-in-soft.com/tsnippet/t/06486475">one compliant
and one non-compliant example</a>).</p></td>
</tr>
</tbody>
</table>

### Related Vulnerabilities

Search for
[vulnerabilities](/confluence/display/c/BB.+Definitions#BB.Definitions-vulnerability)
resulting from the violation of this rule on the [CERT
website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT32-C).

## Related Guidelines

<a
href="https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines"
class="external-link">Key here</a> (explains table format and
definitions)

|  |  |  |
|----|----|----|
| Taxonomy | Taxonomy item | Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [INT02-C. Understand integer conversion rules](https://wiki.sei.cmu.edu/confluence/display/c/INT02-C.+Understand+integer+conversion+rules) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [INT35-C. Use correct integer precisions](https://wiki.sei.cmu.edu/confluence/display/c/INT35-C.+Use+correct+integer+precisions) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors](https://wiki.sei.cmu.edu/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](https://wiki.sei.cmu.edu/confluence/display/c/INT34-C.+Do+not+shift+an+expression+by+a+negative+number+of+bits+or+by+greater+than+or+equal+to+the+number+of+bits+that+exist+in+the+operand) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](https://wiki.sei.cmu.edu/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [ARR36-C. Do not subtract or compare two pointers that do not refer to the same array](https://wiki.sei.cmu.edu/confluence/display/c/ARR36-C.+Do+not+subtract+or+compare+two+pointers+that+do+not+refer+to+the+same+array) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](https://wiki.sei.cmu.edu/confluence/display/c/ARR37-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+to+a+non-array+object) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [MSC15-C. Do not depend on undefined behavior](https://wiki.sei.cmu.edu/confluence/display/c/MSC15-C.+Do+not+depend+on+undefined+behavior) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT C](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard) | [CON08-C. Do not assume that a group of calls to independently atomic methods is atomic](https://wiki.sei.cmu.edu/confluence/display/c/CON08-C.+Do+not+assume+that+a+group+of+calls+to+independently+atomic+methods+is+atomic) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CERT Oracle Secure Coding Standard for Java](https://wiki.sei.cmu.edu/confluence/display/java/SEI+CERT+Oracle+Coding+Standard+for+Java) | [INT00-J. Perform explicit range checking to avoid integer overflow](https://wiki.sei.cmu.edu/confluence/display/java/NUM00-J.+Detect+or+prevent+integer+overflow) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [ISO/IEC TR 24772:2013](https://wiki.sei.cmu.edu/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IECTR24772-2013) | Arithmetic Wrap-Around Error \[FIF\] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [ISO/IEC TS 17961](https://wiki.sei.cmu.edu/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IECTS17961) | Overflowing signed integers \[intoflow\] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| [CWE 2.11](https://cwe.mitre.org/data/index.html) | <a href="http://cwe.mitre.org/data/definitions/190.html"
class="external-link" rel="nofollow">CWE-190</a>, Integer Overflow or Wraparound | 2017-05-18: CERT: Partial overlap |
| <a href="http://cwe.mitre.org/" class="external-link" rel="nofollow">CWE
2.11</a> | <a href="https://cwe.mitre.org/data/index.html191.html"
class="external-link" rel="nofollow">CWE-191</a> | 2017-05-18: CERT: Partial overlap |
| <a href="http://cwe.mitre.org/" class="external-link" rel="nofollow">CWE
2.11</a> | <a href="https://cwe.mitre.org/data/index.html680.html"
class="external-link" rel="nofollow">CWE-680</a> | 2017-05-18: CERT: Partial overlap |

## CERT-CWE Mapping Notes

<a
href="https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes"
class="external-link">Key here</a> for mapping notes

### CWE-20 and INT32-C

See CWE-20 and ERR34-C

### CWE-680 and INT32-C

Intersection( INT32-C, MEM35-C) = Ø

Intersection( CWE-680, INT32-C) =

- Signed integer overflows that lead to buffer overflows

CWE-680 - INT32-C =

- Unsigned integer overflows that lead to buffer overflows

INT32-C – CWE-680 =

- Signed integer overflows that do not lead to buffer overflows

### CWE-191 and INT32-C

Union( CWE-190, CWE-191) = Union( INT30-C, INT32-C)

Intersection( INT30-C, INT32-C) == Ø

Intersection(CWE-191, INT32-C) =

- Underflow of signed integer operation

CWE-191 – INT32-C =

- Underflow of unsigned integer operation

INT32-C – CWE-191 =

- Overflow of signed integer operation

### CWE-190 and INT32-C

Union( CWE-190, CWE-191) = Union( INT30-C, INT32-C)

Intersection( INT30-C, INT32-C) == Ø

Intersection(CWE-190, INT32-C) =

- Overflow (wraparound) of signed integer operation

CWE-190 – INT32-C =

- Overflow of unsigned integer operation

INT32-C – CWE-190 =

- Underflow of signed integer operation

## Bibliography

|  |  |
|----|----|
| \[[Dowd 2006](/confluence/display/c/AA.+Bibliography#AA.Bibliography-Dowd06)\] | Chapter 6, "C Language Issues" ("Arithmetic Boundary Conditions," pp. 211–223) |
| \[[ISO/IEC 9899:2024](/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2024)\] | Subclause 6.5.8, "Bitwise shift operators" |
| \[[Seacord 2013b](/confluence/display/c/AA.+Bibliography#AA.Bibliography-Seacord2013)\] | Chapter 5, "Integer Security" |
| \[[Viega 2005](/confluence/display/c/AA.+Bibliography#AA.Bibliography-Viega05)\] | Section 5.2.7, "Integer Overflow" |
| \[[Warren 2002](/confluence/display/c/AA.+Bibliography#AA.Bibliography-Warren02)\] | Chapter 2, "Basics" |

  

------------------------------------------------------------------------

[SEI CERT C Coding Standard \> button_arrow_left.png" data-location="SEI
CERT C Coding Standard \> SEI CERT C Coding Standard \>
button_arrow_left.png" data-image-height="20"
data-image-width="20"\>](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152211)
[SEI CERT C Coding Standard \> button_arrow_up.png" data-location="SEI
CERT C Coding Standard \> SEI CERT C Coding Standard \>
button_arrow_up.png" data-image-height="20"
data-image-width="20"\>](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152052)
[SEI CERT C Coding Standard \> button_arrow_right.png"
data-location="SEI CERT C Coding Standard \> SEI CERT C Coding Standard
\> button_arrow_right.png" data-image-height="20"
data-image-width="20"\>](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152254)

 
