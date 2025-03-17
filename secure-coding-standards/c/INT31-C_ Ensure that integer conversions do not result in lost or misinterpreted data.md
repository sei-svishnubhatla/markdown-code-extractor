Integer conversions, both implicit and explicit (using a cast), must be guaranteed not to result in lost or misinterpreted data. This rule is particularly true for integer values that originate from untrusted sources and are used in any of the following ways:
-   Integer operands of any pointer arithmetic, including array indexing
-   The assignment expression for the declaration of a variable length array
-   The postfix expression preceding square brackets `[]` or the expression in square brackets `[]` of a subscripted designation of an element of an array object
-   Function arguments of type `size_t` or `rsize_t` (for example, an argument to a memory allocation function)
This rule also applies to arguments passed to the following library functions that are converted to `unsigned char`:
-   `memset()`
-   `memset_s()`
-   `fprintf()` and related functions (For the length modifier `c`, if no `l` length modifier is present, the `int` argument is converted to an `unsigned char`, and the resulting character is written.)
-   `fputc()`
-   `ungetc()`
-   `memchr()`
and to arguments to the following library functions that are converted to `char`:
-   `strchr()`
-   `strrchr()`
-   All of the functions listed in 
The only integer type conversions that are guaranteed to be safe for all data values and all possible conforming implementations are conversions of an integral value to a wider type of the same signedness.
The C Standard, subclause 6.3.1.3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2024)\], says
> When a value with integer type is converted to another integer type other than `_Bool`, if the value can be represented by the new type, it is unchanged.
>
> Otherwise, if the new type is unsigned, the value is converted by repeatedly adding or subtracting one more than the maximum value that can be represented in the new type until the value is in the range of the new type.
>
> Otherwise, the new type is signed and the value cannot be represented in it; either the result is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) or an implementation-defined signal is raised.

Typically, converting an integer to a smaller type results in truncation of the high-order bits.
## Noncompliant Code Example (Unsigned to Signed)
Type range errors, including loss of data (truncation) and loss of sign (sign errors), can occur when converting from a value of an unsigned integer type to a value of a signed integer type. This noncompliant code example results in a truncation error on most [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation):
``` c
#include <limits.h>
void func(void) {
  unsigned long int u_a = ULONG_MAX;
  signed char sc;
  sc = (signed char)u_a; /* Cast eliminates warning */
  /* ... */
}
```
## Compliant Solution (Unsigned to Signed)
Validate ranges when converting from an unsigned type to a signed type. This compliant solution can be used to convert a value of `unsigned long int` type to a value of `signed char `type:
``` c
#include <limits.h>
void func(void) {
  unsigned long int u_a = ULONG_MAX;
  signed char sc;
  if (u_a <= SCHAR_MAX) {
    sc = (signed char)u_a;  /* Cast eliminates warning */
  } else {
    /* Handle error */
  }
}
```
## Noncompliant Code Example (Signed to Unsigned)
Type range errors, including loss of data (truncation) and loss of sign (sign errors), can occur when converting from a value of a signed type to a value of an unsigned type. This noncompliant code example results in a negative number being misinterpreted as a large positive number.
``` c
#include <limits.h>
void func(signed int si) {
  /* Cast eliminates warning */
  unsigned int ui = (unsigned int)si;
  /* ... */
}
/* ... */
func(INT_MIN);
```
## Compliant Solution (Signed to Unsigned)
Validate ranges when converting from a signed type to an unsigned type. This compliant solution converts a value of a `signed int` type to a value of an `unsigned int` type:
``` c
#include <limits.h>
void func(signed int si) {
  unsigned int ui;
  if (si < 0) {
    /* Handle error */
  } else {
    ui = (unsigned int)si;  /* Cast eliminates warning */
  }
  /* ... */
}
/* ... */
func(INT_MIN + 1);
```
Subclause 6.2.5, paragraph 11, of the C Standard \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2024)\] provides the necessary guarantees to ensure this solution works on a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conformingprogram) [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation):
> The range of nonnegative values of a signed integer type is a subrange of the corresponding unsigned integer type, and the representation of the same value in each type is the same.

## Noncompliant Code Example (Signed, Loss of Precision)
A loss of data (truncation) can occur when converting from a value of a signed integer type to a value of a signed type with less precision. This noncompliant code example results in a truncation error on most [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation):
``` c
#include <limits.h>
void func(void) {
  signed long int s_a = LONG_MAX;
  signed char sc = (signed char)s_a; /* Cast eliminates warning */
  /* ... */
}
```
## Compliant Solution (Signed, Loss of Precision)
Validate ranges when converting from a signed type to a signed type with less precision. This compliant solution converts a value of a `signed long int` type to a value of a `signed char` type:
``` c
#include <limits.h>
void func(void) {
  signed long int s_a = LONG_MAX;
  signed char sc;
  if ((s_a < SCHAR_MIN) || (s_a > SCHAR_MAX)) {
    /* Handle error */
  } else {
    sc = (signed char)s_a; /* Use cast to eliminate warning */
  }
  /* ... */
}
```
Conversions from a value of a signed integer type to a value of a signed integer type with less precision requires that both the upper and lower bounds are checked.
## Noncompliant Code Example (Unsigned, Loss of Precision)
A loss of data (truncation) can occur when converting from a value of an unsigned integer type to a value of an unsigned type with less precision. This noncompliant code example results in a truncation error on most [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation):
``` c
#include <limits.h>
void func(void) {
  unsigned long int u_a = ULONG_MAX;
  unsigned char uc = (unsigned char)u_a; /* Cast eliminates warning */
  /* ... */
}
```
## Compliant Solution (Unsigned, Loss of Precision)
Validate ranges when converting a value of an unsigned integer type to a value of an unsigned integer type with less precision. This compliant solution converts a value of an `unsigned long int` type to a value of an `unsigned char` type:
``` c
#include <limits.h>
void func(void) {
  unsigned long int u_a = ULONG_MAX;
  unsigned char uc;
  if (u_a > UCHAR_MAX) {
    /* Handle error */
  } else {
    uc = (unsigned char)u_a; /* Cast eliminates warning */
  }
  /* ... */
}
```
Conversions from unsigned types with greater precision to unsigned types with less precision require only the upper bounds to be checked.
## Noncompliant Code Example (`time_t` Return Value)
The `time()` function returns the value `(time_t)(-1)` to indicate that the calendar time is not available. The C Standard requires that the `time_t` type is only a *real type* capable of representing time. (The integer and real floating types are collectively called real types.) It is left to the implementor to decide the best real type to use to represent time. If `time_t` is implemented as an unsigned integer type with less precision than a signed `int`, the return value of `time()` will never compare equal to the integer literal `-1`.
``` c
#include <time.h>
void func(void) {
  time_t now = time(NULL);
  if (now != -1) {
    /* Continue processing */
  }
}
```
## Compliant Solution (`time_t` Return Value)
To ensure the comparison is properly performed, the return value of `time()` should be compared against `-1` cast to type `time_t`:
``` c
#include <time.h>
void func(void) {
  time_t now = time(NULL);
  if (now != (time_t)-1) {
    /* Continue processing */
  }
}
```
This solution is in accordance with [INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](INT18-C_%20Evaluate%20integer%20expressions%20in%20a%20larger%20size%20before%20comparing%20or%20assigning%20to%20that%20size). Note that `(time_+t)-1` also complies with **INT31-C-EX3**.
## Noncompliant Code Example (`memset()`)
For historical reasons, certain C Standard functions accept an argument of type `int` and convert it to either `unsigned char` or plain `char`. This conversion can result in unexpected behavior if the value cannot be represented in the smaller type. The second argument to `memset()` is an example; it indicates what byte to store in the range of memory indicated by the first and third arguments.  If the second argument is outside the range of a `signed char` or plain `char`, then its higher order bits will typically be truncated. Consequently, this noncompliant solution unexpectedly sets all elements in the array to 0, rather than 4096:
``` c
#include <string.h>
#include <stddef.h>
int *init_memory(int *array, size_t n) {
  return memset(array, 4096, n); 
} 
```
## Compliant Solution (memset())
In general, the `memset()` function should not be used to initialize an integer array unless it is to set or clear all the bits, as in this compliant solution:
``` c
#include <string.h>
#include <stddef.h>
int *init_memory(int *array, size_t n) {
  return memset(array, 0, n); 
} 
```
## Exceptions
**INT31-C-EX1:** The C Standard defines minimum ranges for standard integer types. For example, the minimum range for an object of type `unsigned short int` is 0 to 65,535, whereas the minimum range for `int` is −32,767 to +32,767. Consequently, it is not always possible to represent all possible values of an `unsigned short int` as an `int`. However, on the IA-32 architecture, for example, the actual integer range is from −2,147,483,648 to +2,147,483,647, meaning that it is quite possible to represent all the values of an `unsigned short int` as an `int` for this architecture. As a result, it is not necessary to provide a test for this conversion on IA-32. It is not possible to make assumptions about conversions without knowing the precision of the underlying types. If these tests are not provided, assumptions concerning precision must be clearly documented, as the resulting code cannot be safely ported to a system where these assumptions are invalid. A good way to document these assumptions is to use static assertions. (See [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression).)
**INT31-C-EX2:** Conversion from any integer type with a value between `SCHAR_MIN` and `UCHAR_MAX` to a character type is permitted provided the value represents a character and not an integer.
Conversions to unsigned character types are well defined by C to have modular behavior. A character's value is not misinterpreted by the loss of sign or conversion to a negative number. For example, the Euro symbol `€` is sometimes represented by bit pattern `0x80` which can have the numerical value 128 or −127 depending on the signedness of the type.
Conversions to signed character types are more problematic.
The C Standard, subclause 6.3.1.3, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\], says, regarding conversions
> Otherwise, the new type is signed and the value cannot be represented in it; either the result is implementation-defined or an implementation-defined signal is raised.

Furthermore, subclause 6.2.6.2, paragraph 2, says, regarding integer modifications
> Each bit that is a value bit shall have the same value as the same bit in the object representation of the corresponding unsigned type. If the sign bit is zero, it shall not affect the resulting value. If the sign bit is one, it has value −(2N−1). There may or may not be any padding bits signed char shall not have any padding bits. 

Consequently, the standard allows for this code to trap:
``` java
int i = 128; /* 1000 0000 in binary */
assert(SCHAR_MAX == 127);
signed char c = i; /* can trap */
```
However, platforms where this code traps or produces an unexpected value are rare. According to *[The New C Standard: An Economic and Cultural Commentary](http://www.knosof.co.uk/cbook/cbook.html)* by Derek Jones \[[Jones 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Jones08)\],
> Implementations with such trap representations are thought to have existed in the past. Your author was unable to locate any documents describing such processors.

**INT31-C-EX3:** The C Standard, subclause 7.29.2.5, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\] says:
> The time function returns the implementation’s best approximation to the current calendar time. The value (time_t)(-1) is returned if the calendar time is not available.

If `time_t` is an unsigned type, then the expression `((time_t) (-1))` is guaranteed to yield a large positive value.
Therefore, conversion of a negative compile-time constant to an unsigned value with the same or larger width is permitted by this rule. This exception does not apply to conversion of unsigned to signed values, nor does it apply if the resulting value would undergo truncation.
## Risk Assessment
Integer truncation errors can lead to buffer overflows and the execution of arbitrary code by an attacker.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT31-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported via MISRA C:2012 Rules 10.1, 10.3, 10.4, 10.6 and 10.7 |
| CodeSonar | 8.3p0 | LANG.CAST.PC.AVLANG.CAST.PC.CONST2PTR
LANG.CAST.PC.INTLANG.CAST.COERCE
LANG.CAST.VALUEALLOC.SIZE.TRUNC
MISC.MEM.SIZE.TRUNCLANG.MEM.TBA
 | Cast: arithmetic type/void pointerConversion: integer constant to pointer
Conversion: pointer/integerCoercion alters value
Cast alters valueTruncation of allocation size
Truncation of sizeTainted buffer access |
| Compass/ROSE |  |  | Can detect violations of this rule. However, false warnings may be raised if limits.h is included |
| Coverity* | 2017.07 | NEGATIVE_RETURNSREVERSE_NEGATIVEMISRA_CAST | Can find array accesses, loop bounds, and other expressions that may contain dangerous implied integer conversions that would result in unexpected behaviorCan find instances where a negativity check occurs after the negative value has been used for something elseCan find instances where an integer expression is implicitly converted to a narrower integer type, where the signedness of an integer value is implicitly converted, or where the type of a complex expression is implicitly converted |
| ;Cppcheck | ; 2.15 | memsetValueOutOfRange |  |
| Cppcheck Premium | 24.11.0 | memsetValueOutOfRangepremium-cert-int31-c |  |
| Helix QAC | 2024.4 | C2850, C2855, C2890, C2895, C2900, C2905, C++2850, C++2855, C++2890, C++2895, C++2900, C++2905,; C++3000, C++3010
DF2851, DF2852, DF2853,  DF2856, DF2857, DF2858, DF2891, DF2892, DF2893, DF2896, DF2897, DF2898, DF2901, DF2902, DF2903, DF2906, DF2907, DF2908 |  |
| Klocwork | 2024.4 | PORTING.CAST.SIZE |  |
| LDRA tool suite | 9.7.1 | 93 S, 433 S, 434 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT31-aCERT_C-INT31-b
CERT_C-INT31-c
CERT_C-INT31-d
CERT_C-INT31-e
CERT_C-INT31-f
CERT_C-INT31-g
CERT_C-INT31-h
CERT_C-INT31-i
CERT_C-INT31-j
CERT_C-INT31-k
CERT_C-INT31-l
CERT_C-INT31-m
CERT_C-INT31-n
CERT_C-INT31-o
CERT_C-INT31-p
 | An expression of essentially Boolean type should always be used where an operand is interpreted as a Boolean valueAn operand of essentially Boolean type should not be used where an operand is interpreted as a numeric value
An operand of essentially character type should not be used where an operand is interpreted as a numeric value
An operand of essentially enum type should not be used in an arithmetic operation
Shift and bitwise operations should not be performed on operands of essentially signed or enum type
An operand of essentially signed or enum type should not be used as the right hand operand to the bitwise shifting operator
An operand of essentially unsigned type should not be used as the operand to the unary minus operator
The value of an expression shall not be assigned to an object with a narrower essential type
The value of an expression shall not be assigned to an object of a different essential type category
Both operands of an operator in which the usual arithmetic conversions are performed shall have the same essential type category
The second and third operands of the ternary operator shall have the same essential type category
The value of a composite expression shall not be assigned to an object with wider essential type
If a composite expression is used as one operand of an operator in which the usual arithmetic conversions are performed then the other operand shall not have wider essential type
If a composite expression is used as one (second or third) operand of a conditional operator then the other operand shall not have wider essential type
Avoid data loss when converting between integer types
Avoid value change when converting between integer types |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT31-C | Checks for:Integer conversion overflowCall to memset with unintended value Sign change integer conversion overflowTainted sign change conversionUnsigned integer conversion overflowRule partially covered. |
| PVS-Studio | 7.35 | V562,;V569, V642, V676, V716, V721, V724, V732, V739, V784, V793, V1019,  V1029, V1046
 |  |
| RuleChecker | 24.04 |  | Supported via MISRA C:2012 Rules 10.1, 10.3, 10.4, 10.6 and 10.7 |
| TrustInSoft Analyzer | 1.38 | signed_downcast | Exhaustively verified. |

\* Coverity Prevent cannot discover all violations of this rule, so further [verification](BB.-Definitions_87152273.html#BB.Definitions-verification) is necessary.
### Related Vulnerabilities
[CVE-2009-1376](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1376) results from a violation of this rule. In version 2.5.5 of Pidgin, a `size_t` offset is set to the value of a 64-bit unsigned integer, which can lead to truncation \[[xorl 2009](http://xorl.wordpress.com/2009/05/28/cve-2009-1376-pidgin-msn-slp-integer-truncation/)\] on platforms where a `size_t` is implemented as a 32-bit unsigned integer. An attacker can execute arbitrary code by carefully choosing this value and causing a buffer overflow.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabi) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | DCL03-C. Use a static assertion to test the value of a constant expression | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | FIO34-C. Distinguish between characters read from a file and EOF or WEOF | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | NUM12-J. Ensure conversions of numeric types to narrower types do not result in lost or misinterpreted data | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Numeric Conversion Errors [FLC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 10.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 10.3 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 10.4 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 10.6 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 10.7 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-192, Integer Coercion Error | 2017-07-17: CERT: Exact |
| CWE 2.11 | CWE-197, Numeric Truncation Error | 2017-06-14: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-681, Incorrect Conversion between Numeric Types | 2017-07-17: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-704 | 2017-07-17: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-195 and INT31-C
CWE-195 = Subset( CWE-192)
INT31-C = Union( CWE-195, list) where list =
-   Unsigned-to-signed conversion error
<!-- -->
-   Truncation that does not change sign
### CWE-197 and INT31-C
See CWE-197 and FLP34-C
### CWE-194 and INT31-C
CWE-194 = Subset( CWE-192)
INT31-C = Union( CWE-194, list) where list =
-   Integer conversion that truncates significant data, but without loss of sign
### CWE-20 and INT31-C
See CWE-20 and ERR34-C
### CWE-704 and INT31-C
CWE-704 = Union( INT31-C, list) where list =
-   Improper type casts where either the source or target type is not an integral type
### CWE-681 and INT31-C
CWE-681 = Union( INT31-C, FLP34-C)
Intersection( INT31-C, FLP34-C) = Ø
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Type Conversions," pp. 223–270) |
| [ISO/IEC 9899:2024] | 6.3.1.3, "Signed and Unsigned Integers"6.2.5, "Types"7.29.2.5, "The time function" |
| [Jones 2008] | Section 6.2.6.2, "Integer Types" |
| [Seacord 2013b] | Chapter 5, "Integer Security" |
| [Viega 2005] | Section 5.2.9, "Truncation Error"Section 5.2.10, "Sign Extension Error"
Section 5.2.11, "Signed to Unsigned Conversion Error"
Section 5.2.12, "Unsigned to Signed Conversion Error" |
| [Warren 2002] | Chapter 2, "Basics" |
| [xorl 2009] | "CVE-2009-1376: Pidgin MSN SLP Integer Truncation" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152236) [](../c/Rule%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152210)
## Comments:

|  |
| ----|
| There's one more signed to unsigned type conversion that might be worth mentioning. Basically, when you go from a narrow signed type to a wider unsigned type, it somewhat counter-intuitively performs sign-extension, and it's necessarily value changing. Something like:
unsigned int bob;
signed char fred = -1;
bob = (unsigned int)fred; /* sign extension occurs, bob is 0xffffffff */

![](images/icons/contenttypes/comment_16.png) Posted by jm at Dec 25, 2006 12:39
\| \|
I should mention I've seen this in code a few times. One example was trying to fix code relying on older `ctype` libs with lookup tables:
``` java
char jim=get_input();
jim=my_toupper(jim);
```
The `toupper()` function took an int argument and used it to lookup the correct value in a table, and an attacker could cause it to look behind the table in memory. They tried to fix this with:
``` java
jim=my_toupper((unsigned int)jim);
```
But that didn't work since sign-extension still happened. Another good example was from `antisniff`, where they tried to fix a problem caused by a signed char having negative values with this:
``` java
unsigned int count;
unsigned char *indx;
count = (char) *indx;
```
So, `*indx` is an unsigned char with a range of 0-255. However, it's converted to a `char` by the type cast, so it then has a range of -128-127. Then, it's converted to an `unsigned int`, which will do sign-extension. Oops.
![](images/icons/contenttypes/comment_16.png) Posted by jm at Dec 26, 2006 18:41
\| \|
My comment on INT30 also applies here. I don't believe we actually have written ROSE code to handle this, I think ROSE does some of these checks automatically.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 18, 2008 15:00
\| \|
In related vulnerability you wrote "An unsigned integer (offset) is set to the value of a 64-bit unsigned integer". You may have meant an unsigned int, which may be smaller than a 64-bit unsigned integer. Anyway, you probably want to refer to the type in each case, and maybe the sizes on a particular platform as a specific example.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 15, 2009 21:46
\| \|
I've fixed the wording to be more accurate; it was a `size_t` that was being given a 64-bit value, which overflows on platforms where a `size_t` is treated as a 32-bit value.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 11, 2013 12:45
\| \|
A reference to [The New C Standard: An Economic and Cultural Commentary](http://www.knosof.co.uk/cbook/cbook.html);by Derek Jones will need to be added to the Bibliography.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 27, 2013 14:27
\| \|
Looking at some real-world code, I think we need to be more precise about "misinterpretation-of-sign"; and when it constitutes violation of this rule. Here are some examples:
Does this code violate this rule? `((time_t)-1)`
It is included in the time_t compliant solution, but if time_t is unsigned (which is permitted by both ISO C18 and POSIX), then it gets misinterpreted as a large integer.  The time() function can return `((time_t)-1)`.
How about this code? `((size_t)-1)`
Some systems define SIZE_MAX this way.
And what about this code?` ((unsigned int)INT_MIN)`
This code comes from the signed-to-unsigned noncompliant code example, and this rule advocates on converting nonnegative values to unsigned int in the compliant solution.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 12, 2019 14:24
\| \|
Some background on my above comment:
Each CERT rule should be independent of user intent. That is, each code example (compliant or non-) should be discernible from the rule's title, intro text, and exceptions. Whatever the developer intended should be irrelevant; the code is all that matters. My previous post shows three very similar code examples. But, according to the rule, the first is compliant, the third is noncompliant, and it is not obvious whether the second is compliant or noncompliant.
The concept of "misinterpreted data" (from the title) is precise, although it could be explained better in the intro. Misinterpreted data specifically refers to the most significant non-padding bit in the integer. For unsigned types, this is a value bit, and for signed types, this bit indicates the sign.; So "misinterpreted data" means that a conversion does not lose the bit pattern but causes a negative number to be misinterpreted as a large positive number, or vice versa.  The expression ((time_t) -1) is an intentional instance of misinterpreted data.
So in theory, ((time_t) -1) should violate this rule. But then ISO C violates the rule quite often, in having time() return ((time_t) -1). There is no standard way to reference the maximum time_t value (assuming it is unsigned) except by saying ((time_t) -1).
Our options are either:
-   Demote this rule to a recommendation, which saves us from answering this question
-   Provide some normative wording to address whether my three code examples violate the rule. This wording could go in the introduction, or into an exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 12, 2019 16:50
\| \|
Having slept on this for a few days, I am now thinking that we can solve this problem by adding an exception.
The exception would specifically allow signed-to-unsigned conversion of negative compile-time constants to large positive values.; So ((time_t) -1) is allowed, but ((time_t) x) is forbidden if x is a signed int, even if it happens to be -1.  In fact, all three of my code examples become compliant with this rule.
We still want to forbid truncation, and most misinterpretation-of-sign errors. And we don't want to permit unsigned-to-signed conversion because that can trap (C17 s6.3.1.3, p3). But signed-to-unsigned conversion is well-defined behavior, and used by the standard occasionally, as in ((time_t) -1).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 14, 2019 14:17
\| \|
According to the Linux manpage for audit_log_acct_message(), it takes an "unsigned int id" parameter, but it encourages developers to pass it -1 if the user id is unknown:<http://man7.org/linux/man-pages/man3/audit_log_acct_message.3.html>  
It is unclear if this currently violates INT31-C, but it would not violate my proposed resolution to INT31-C if the code contains a literal -1. (granted that passing UINT_MAX would be better).  
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 14, 2019 15:26
\| \|
I have added the exception I suggested earlier, and tweaked the code examples wrt the exception for clarity. Questions & comments welcome.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 15, 2019 09:44
\| \|
According to [Rule 03. Integers (INT)](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046333), INT31-C seems to be applicable to CPP source code as well. I can see the only MISRA-C rules related to this rule from this page. Could you provide information on the related MISRA-CPP rules? Additionally, do you have any plans to create the same rule for CPP? (ex. INT31-CPP).
![](images/icons/contenttypes/comment_16.png) Posted by jenna.jungsun.goh at Jul 17, 2023 03:09
\| \|
The link you cited lists all CERT C rules (all the Integer rules) that we believe apply to C++ with no changes. That means we have no C++ analogous rule to INT31-C, since INT31-C applies to C++ as well as C. Therefore we have no plans to create a "INT31-CPP" rule.
My quick reading of the MISRA standards shows a similar strategy. MISRA C has analogous rules to INT31-C. MISRA C++ has a few new integer rules specific to C++ (as does CERT), but does not cite specifically the MISRA C rules. ;I am guessing there is test in MISRA C++ that says "unless otherwise specified, all the MISRA C rules apply to MISRA C++".
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 18, 2023 09:38
\|
