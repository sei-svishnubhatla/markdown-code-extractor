The C Standard, 6.2.5, paragraph 11 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> A computation involving unsigned operands can never produce an overflow, because arithmetic for the unsigned type is performed modulo 2^N .

This behavior is more informally called [unsigned integer wrapping](BB.-Definitions_87152273.html#BB.Definitions-unsignedintegerwrapping). Unsigned integer operations can wrap if the resulting value cannot be represented by the underlying representation of the integer. The following table indicates which operators can result in wrapping:

| Operator | Wrap | Operator | Wrap | Operator | Wrap | Operator | Wrap |
| ----|----|----|----|----|----|----|----|
| + | Yes | -= | Yes | << | Yes | < | No |
| - | Yes | *= | Yes | >> | No | > | No |
| * | Yes | /= | No | & | No | >= | No |
| / | No | %= | No | | | No | <= | No |
| % | No | <<=< a> | Yes | ^ | No | == | No |
| ++ | Yes | >>= | No | ~ | No | != | No |
| -- | Yes | &= | No | ! | No | && | No |
| = | No | |= | No | un + | No | || | No |
| += | Yes | ^= | No | un - | Yes | ?: | No |

The following sections examine specific operations that are susceptible to unsigned integer wrap. When operating on integer types with less precision than `int`, integer promotions are applied. The usual arithmetic conversions may also be applied to (implicitly) convert operands to equivalent types before arithmetic operations are performed. Programmers should understand integer conversion rules before trying to implement secure arithmetic operations. (See [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules).)
Integer values must not be allowed to wrap, especially if they are used in any of the following ways:
-   Integer operands of any pointer arithmetic, including array indexing
-   The assignment expression for the declaration of a variable length array
-   The postfix expression preceding square brackets `[]` or the expression in square brackets `[]` of a subscripted designation of an element of an array object
-   Function arguments of type `size_t` or `rsize_t` (for example, an argument to a memory allocation function)
-   In security-critical code
The C Standard defines arithmetic on atomic integer types as read-modify-write operations with the same representation as regular integer types. As a result, wrapping of atomic unsigned integers is identical to regular unsigned integers and should also be prevented or detected.
## Addition
Addition is between two operands of arithmetic type or between a pointer to an object type and an integer type. This rule applies only to addition between two operands of arithmetic type. (See [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object) and [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts).)
Incrementing is equivalent to adding 1.
### Noncompliant Code Example
This noncompliant code example can result in an unsigned integer wrap during the addition of the unsigned operands `ui_a` and `ui_b`. If this behavior is [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior), the resulting value may be used to allocate insufficient memory for a subsequent operation or in some other manner that can lead to an exploitable [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int usum = ui_a + ui_b;
  /* ... */
}
```
### Compliant Solution (Precondition Test)
This compliant solution performs a precondition test of the operands of the addition to guarantee there is no possibility of unsigned wrap:
``` c
#include <limits.h>
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int usum;
  if (UINT_MAX - ui_a < ui_b) {
    /* Handle error */
  } else {
    usum = ui_a + ui_b;
  }
  /* ... */
}
```
### Compliant Solution (Postcondition Test)
This compliant solution performs a postcondition test to ensure that the result of the unsigned addition operation `usum` is not less than the first operand:
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int usum = ui_a + ui_b;
  if (usum < ui_a) {
    /* Handle error */
  }
  /* ... */
}
```
## Subtraction
Subtraction is between two operands of arithmetic type, two pointers to qualified or unqualified versions of compatible object types, or a pointer to an object type and an integer type. This rule applies only to subtraction between two operands of arithmetic type. (See [ARR36-C. Do not subtract or compare two pointers that do not refer to the same array](ARR36-C_%20Do%20not%20subtract%20or%20compare%20two%20pointers%20that%20do%20not%20refer%20to%20the%20same%20array), [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object), and [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts) for information about pointer subtraction.)
Decrementing is equivalent to subtracting 1.
### Noncompliant Code Example
This noncompliant code example can result in an unsigned integer wrap during the subtraction of the unsigned operands `ui_a` and `ui_b`. If this behavior is unanticipated, it may lead to an exploitable [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int udiff = ui_a - ui_b;
  /* ... */
}
```
### Compliant Solution (Precondition Test)
This compliant solution performs a precondition test of the unsigned operands of the subtraction operation to guarantee there is no possibility of unsigned wrap:
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int udiff;
  if (ui_a < ui_b){
    /* Handle error */
  } else {
    udiff = ui_a - ui_b;
  }
  /* ... */
}
```
### Compliant Solution (Postcondition Test)
This compliant solution performs a postcondition test that the result of the unsigned subtraction operation `udiff` is not greater than the minuend:
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int udiff = ui_a - ui_b;
  if (udiff > ui_a) {
    /* Handle error */
  }
  /* ... */
}
```
## Multiplication
Multiplication is between two operands of arithmetic type.
### Noncompliant Code Example
The Mozilla Foundation Security Advisory 2007-01 describes a heap buffer overflow vulnerability in the Mozilla Scalable Vector Graphics (SVG) viewer resulting from an unsigned integer wrap during the multiplication of the `signed int` value `pen->num_vertices` and the `size_t` value `sizeof(cairo_pen_vertex_t)` \[[VU#551436](AA.-Bibliography_87152170.html#AA.Bibliography-VU551436)\]. The `signed int` operand is converted to `size_t` prior to the multiplication operation so that the multiplication takes place between two `size_t` integers, which are unsigned. (See [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules).)
``` c
pen->num_vertices = _cairo_pen_vertices_needed(
  gstate->tolerance, radius, &gstate->ctm
);
pen->vertices = malloc(
  pen->num_vertices * sizeof(cairo_pen_vertex_t)
);
```
The unsigned integer wrap can result in allocating memory of insufficient size.
### Compliant Solution
This compliant solution tests the operands of the multiplication to guarantee that there is no unsigned integer wrap:
``` c
pen->num_vertices = _cairo_pen_vertices_needed(
  gstate->tolerance, radius, &gstate->ctm
);
if (pen->num_vertices > SIZE_MAX / sizeof(cairo_pen_vertex_t)) {
  /* Handle error */
}
pen->vertices = malloc(
  pen->num_vertices * sizeof(cairo_pen_vertex_t)
);
```
## Exceptions
**INT30-C-EX1:** Unsigned integers can exhibit modulo behavior (wrapping) when necessary for the proper execution of the program. It is recommended that the variable declaration be clearly commented as supporting modulo behavior and that each operation on that integer also be clearly commented as supporting modulo behavior.
**INT30-C-EX2:** Checks for wraparound can be omitted when it can be determined at compile time that wraparound will not occur. As such, the following operations on unsigned integers require no validation:
-   Operations on two compile-time constants
-   Operations on a variable and 0 (except division or remainder by 0)
-   Subtracting any variable from its type's maximum; for example, any `unsigned int` may safely be subtracted from `UINT_MAX`
-   Multiplying any variable by 1
-   Division or remainder, as long as the divisor is nonzero
-   Right-shifting any type maximum by any number no larger than the type precision; for example, `UINT_MAX >> x` is valid as long as `0 <=  x < 32` (assuming that the precision of `unsigned int` is 32 bits)
**INT30-C-EX3.** The left-shift operator takes two operands of integer type. Unsigned left shift `<<` can exhibit modulo behavior (wrapping).  This exception is provided because of common usage, because this behavior is usually expected by the programmer, and because the behavior is well defined. For examples of usage of the left-shift operator, see [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](INT34-C_%20Do%20not%20shift%20an%20expression%20by%20a%20negative%20number%20of%20bits%20or%20by%20greater%20than%20or%20equal%20to%20the%20number%20of%20bits%20that%20exist%20in%20the%20operand).
## Risk Assessment
Integer wrap can lead to buffer overflows and the execution of arbitrary code by an attacker.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT30-C | High | Likely | High | P9 | L2 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | integer-overflow | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT30 | Implemented |
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
| Compass/ROSE |  |  | Can detect violations of this rule by ensuring that operations are checked for overflow before being performed (Be mindful of exception INT30-EX2 because it excuses many operations from requiring validation, including all the operations that would validate a potentially dangerous operation. For instance, adding two unsigned ints together requires validation involving subtracting one of the numbers from UINT_MAX, which itself requires no validation because;it cannot wrap.) |
| Coverity | 2017.07 | INTEGER_OVERFLOW | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-int30-c |  |
| Helix QAC | 2024.4 | C2910, C3383, C3384, C3385, C3386C++2910DF2911, DF2912, DF2913,  |  |
| Klocwork | 2024.4 | NUM.OVERFLOWCWARN.NOEFFECT.OUTOFRANGE
NUM.OVERFLOW.DF |  |
| LDRA tool suite | 9.7.1 | 493 S, 494 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT30-aCERT_C-INT30-b
CERT_C-INT30-c | Avoid wraparounds when performing arithmetic integer operationsInteger overflow or underflow in constant expression in '+', '-', '*' operator
Integer overflow or underflow in constant expression in '<<' operator |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT30-C | Checks for:Unsigned integer overflowUnsigned integer constant overflowRule partially covered. |
| PVS-Studio | 7.35 | V658, V1012,;V1028, V5005, V5011 
 |  |
| TrustInSoft Analyzer | 1.38 | unsigned overflow | Exhaustively verified. |

### Related Vulnerabilities
[CVE-2009-1385](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1385) results from a violation of this rule. The value performs an unchecked subtraction on the `length` of a buffer and then adds those many bytes of data to another buffer \[[xorl 2009](http://xorl.wordpress.com/2009/06/10/cve-2009-1385-linux-kernel-e1000-integer-underflow/)\]. This can cause a buffer overflow, which allows an attacker to execute arbitrary code.
A Linux Kernel vmsplice [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit), described by Rafal Wojtczuk \[[Wojtczuk 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Wojtczuk08)\], documents a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) and exploit arising from a buffer overflow (caused by unsigned integer wrapping).
Don Bailey \[[Bailey 2014](AA.-Bibliography_87152170.html#AA.Bibliography-Bailey14)\] describes an unsigned integer wrap [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in the LZO compression algorithm, which can be exploited in some implementations.
[CVE-2014-4377](https://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-4377) describes a [vulnerability](http://blog.binamuse.com/2014/09/coregraphics-memory-corruption.html) in iOS 7.1 resulting from a multiplication operation that wraps, producing an insufficiently small value to pass to a memory allocation routine, which is subsequently overflowed.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT02-C. Understand integer conversion rules | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR30-C. Do not form or use out-of-bounds pointers or array subscripts | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR36-C. Do not subtract or compare two pointers that do not refer to the same array | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ARR37-C. Do not add or subtract an integer to a pointer to a non-array object | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | CON08-C. Do not assume that a group of calls to independently atomic methods is atomic | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Arithmetic Wrap-Around Error [FIF] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-190, Integer Overflow or Wraparound | 2016-12-02: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-131 | 2017-05-16: CERT: Partial overlap |
| CWE 2.11 | CWE-191 | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-680 | 2017-05-18: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-131 and INT30-C
-   Intersection( INT30-C, MEM35-C) = Ø
-   Intersection( CWE-131, INT30-C) =
-   Calculating a buffer size such that the calculation wraps. This can happen, for example, when using malloc() or operator new\[\] to allocate an array, multiplying the array item size with the array dimension. An untrusted dimension could cause wrapping, resulting in a too-small buffer being allocated, and subsequently overflowed when the array is initialized.
-   CWE-131 – INT30-C =
-   Incorrect calculation of a buffer size that does not involve wrapping. This includes off-by-one errors, for example.
INT30-C – CWE-131 =
-   Integer wrapping where the result is not used to allocate memory.
### CWE-680 and INT30-C
Intersection( CWE-680, INT30-C) =
-   Unsigned integer overflows that lead to buffer overflows
CWE-680 - INT30-C =
-   Signed integer overflows that lead to buffer overflows
INT30-C – CWE-680 =
-   Unsigned integer overflows that do not lead to buffer overflows
### CWE-191 and INT30-C
Union( CWE-190, CWE-191) = Union( INT30-C, INT32-C) Intersection( INT30-C, INT32-C) == Ø
Intersection(CWE-191, INT30-C) =
-   Underflow of unsigned integer operation
CWE-191 – INT30-C =
-   Underflow of signed integer operation
INT30-C – CWE-191 =
-   Overflow of unsigned integer operation
## Bibliography

|  |  |
| ----|----|
| [Bailey 2014] | Raising Lazarus - The 20 Year Old Bug that Went to Mars |
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Arithmetic Boundary Conditions," pp. 211–223) |
| [ISO/IEC 9899:2024] | Subclause 6.2.5, "Types" |
| [Seacord 2013b] | Chapter 5, "Integer Security" |
| [Viega 2005] | Section 5.2.7, "Integer Overflow" |
| [VU#551436] |  |
| [Warren 2002] | Chapter 2, "Basics" |
| [Wojtczuk 2008] |  |
| [xorl 2009] | "CVE-2009-1385: Linux Kernel E1000 Integer Underflow" |

------------------------------------------------------------------------
[](../c/Rule%2004_%20Integers%20_INT_) [](../c/Rule%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152211)
## Comments:

|  |
| ----|
| Enforcing this rule is possible, but I'm a little hesitant to recommend it, because of how disruptive it would be (just how much addition, etc. would need to be protected).
To enforce addition, one need merely check that any 'a + b' expr is preceded by a (max - b > a) expr. Subtraction, etc. are similar. There are probably many exceptions.
Hm...building a Rose checker would be a useful exercise mainly because it will help us learn the exceptions to this rule. I suspect there are many more than we realize.
                                        Posted by svoboda at Jun 18, 2008 14:57
                                     |
| Unary - can cause wrapping
unsigned int x;
x = - x;

Also, so can division/modulo by a negative number ...
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 09, 2008 16:09
\| \|
All true, but those are technically signed int operations. So the 'surprise' behavior occurs in converting signed to unsigned & back.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 11, 2008 11:04
\| \|
In that case, we should probably either not list them in the table, or mark them as capable of producing wrapping
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 11, 2008 11:18
\| \|
as far as automatic detection, this is a subset of [INT35-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](/confluence/pages/createpage.action?spaceKey=c&title=INT35-C.+Evaluate+integer+expressions+in+a+larger+size+before+comparing+or+assigning+to+that+size)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 24, 2008 14:26
\| \|
The second sentence under the heading **Noncompliant Code Example** in the **Multiplication** section states:
> The `signed int` operand is converted to `unsigned int` prior to the multiplication operation...

I don't believe that is completely accurate. In a multiplication expression involving operands of types `signed int` and `size_t`, the `signed int` operand is converted to `size_t`. The type of `size_t` may be the same as either `unsigned int` or `unsigned long` in ILP32 but is the same as `unsigned long` in LP64 where `sizeof(int) < sizeof(long)`.
The vulnerability in the example is unrelated to the signed-ness of the type of the first operand but rather to the possibility of arithmetic overflow of the product of the two operands after the usual arithmetic conversions. The same vulnerability exists when both operands are of an unsigned integer type.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 02, 2009 18:30
\| \|
I `s/unsigned int/size_t/` in the paragraph. I believe overflow is possible on a 32- or 64-bit architecture (though for 64-bits, the sizeof() operation would have to return a really big size.) While the conversion occurs, it is not that important, as overflow is still possible, and easy on ILP32 if an attacker can specify `num_vertices`.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 03, 2009 12:08
\| \|
I think there is a mistake in the Subtraction Compliant Solution (Post-condition Test)
The second condition in the if statement should not be there. Eg:  
ui1 = 10, ui2 = 2  
udiff = 8  
It is still valid with 8 \> 2.
It looks like this was a copy paste mistake from the addition's compliant post-condition test.
![](images/icons/contenttypes/comment_16.png) Posted by abrowne at Jan 20, 2010 01:43
\| \|
nice catch, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 20, 2010 08:46
\| \|
Also the description just above that code.
![](images/icons/contenttypes/comment_16.png) Posted by abrowne at Jan 20, 2010 17:43
\| \|
thanks, that should be fixed now too.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 06, 2010 03:37
\| \|
I think that there's a minor think-o in the example given in the second to last item in INT32-EX2:
" .... For instance, `UINT_MAX >> x` is valid as long as `x < sizeof(unsigned int)"`
The comparison should be to the number of bits, not the sizeof.; Rather than faff around with CHAR_BITS or INT_BITS, which will probably only serve to obscure the main point, it might be best to just drop the example.
![](images/icons/contenttypes/comment_16.png) Posted by nschellenberger at Apr 30, 2013 13:33
\| \|
Fixed, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 30, 2013 14:21
\| \|
The CS for Atomic Integers is somewhat misleading since it assumes that no writes have occurred between the atomic_fetch_add() and the subsequent atomic_load().; Given that the primary use case of atomics is environments where precisely that sort of thing can occur, safer (for selected values of "safer") might be something like (totally untested):
``` cpp
std::atomic<int> at_i_a;
// initialize at_i_a
int i_a {at_i_a.load()};
int i_b;
// initialize i_b
for (;;) {
    int i_sum {i_a + i_b};
    if (i_sum >= i_a) {
        if (at_i_a.compare_exchange_strong(i_a, i_sum)) {
            break;
        }
        // go around again with new i_a
    } else {
        // handle error
    }
}
```
A very minor nitpick: the variable naming in both the NCE and the CE appears to be wrong, as the (signed) type for ui_a doesn't seem to match the name (assuming ui_a is supposed to be a mnemonic for "an unsigned integer called a")
![](images/icons/contenttypes/comment_16.png) Posted by nschellenberger at Jul 18, 2013 13:23
\| \|
Neil, as far as I am know the names are not meant to be mnemonic. I changed them from ui1 to ui_a, just to rid them of the 'l' (ell) and '1' (one) confusion factor.
![](images/icons/contenttypes/comment_16.png) Posted by bluepilot at Jul 19, 2013 07:39
\| \|
So the multiplication example in this rule does not parallel the multiplication example in INT32-C.; For this rule, we use a real world example but we provide only the portable solution and not the "store the product in twice as many bits solution".  Consequently, this rule does not require the UWIDTH() macro, which actually works with unsigned numbers right now.  Right now my feeling is that these two rules should be a little more parallel, and maybe we should include a twice the bits solution here, or remove it from INT32-C.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 17, 2013 12:01
\| \|
    In Addition in "Compliant Solution (Postcondition Test)" shouldn't it be
`if` `(usum < ui_a || ``usum < ui_b``)`
?
Suppose we take 4 bit; representation, so we have 0-15 unsigned ints and `assume ui_a`=15  `ui_b`=2, then checking only for `usum < ui_a` seems is not enough.
![](images/icons/contenttypes/comment_16.png) Posted by zkutch at Feb 09, 2019 00:45
\| \|
In your example, ui_a + ui_b = 15+2%16 = 1, and 1\<15, so the code will "handle error", as it should.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 14, 2019 17:05
\| \|
Is this rule really something enforced to the letter in practice. For instance should every increment/decrement operation on a size_t be checked for wrapping when it is possible to wrap though exceedingly unlikely?
If so, I feel there are compliant code examples in other rules which violate this. As a quick example I found an couple of unchecked increments in CE "getchar()" of; [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](https://wiki.sei.cmu.edu/confluence/display/c/STR31-C.+Guarantee+that+storage+for+strings+has+sufficient+space+for+character+data+and+the+null+terminator). In this example the size_t are incremented every time getchar is called and no newline or eof is found. In this case it would be exceedingly unreasonable (though not impossible) for the stdin to have sufficient text to wrap the size_t vars.
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at May 18, 2023 08:19
\| \|
Samuel: First, you'll note there are several exceptions to this rule. I assume you are not talking about those.
Second, the STR31-C "Compliant Solution (getchar())" code example does prevent wrapping, in that it prevents both index and chars_read from exceeding sizeof(buf). Since sizeof(buf) cannot exceed SIZE_MAX by definition, wrapping cannot occur.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2023 09:56
\| \|
Thank you for your response.
In response to your second comment, I agree that index cannot exceed `sizeof(buf)`; but I do not see any similar control/restriction on `chars_read. `That value increments at every call of the while loop. If the loop iterates more than `UINT_MAX` the value will wrap, no?
I guess I am getting at the fact that this rule seems overly restrictive as there is a requirement to check bounds before any increment or decrement that does not fall in the exceptions noted. This seems unrealistic for production code but maybe I need to change my outlook. I do appreciate your prompt response and am writing to try to get a feel for how to incorporate secure coding standards in my code.
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at May 18, 2023 10:35
\| \|
It is an open question just how theoretical or practical integer wrapping can be. In the code example you cite, wrapping can only occur if getchar() returns more than SIZE_MAX (not necessarily UINT_MAX) characters. Today that usually means \> 2^64 characters without exhausting the file. Not an easy vulnerability to exploit :)
Still, in theory it could be possible, especially if getchar() is referencing not actual memory, but some stream process that is never exhausted (Linux probably has files in /dev with this property). ;So, primarily in the interests of preventing even theoretical exploits, I fixed that code example. In particular, I replaced chars_read with a 'truncated' boolean flag to indicate if truncation occurs.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 19, 2023 09:07
\|
