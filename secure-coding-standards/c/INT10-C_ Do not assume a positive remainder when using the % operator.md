In C89 (and historical K&R [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation)), the meaning of the remainder operator for negative operands was [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementationdefinedbehavior). This behavior was changed in C99, and the change remains in C11.
Because not all C compilers are strictly C-conforming, programmers cannot rely on the behavior of the `%` operator if they need to run on a wide range of platforms with many different compilers.
The C Standard, subclause 6.5.5 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], states:
> The result of the `/` operator is the quotient from the division of the first operand by the second; the result of the `%` operator is the remainder. In both operations, if the value of the second operand is zero, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

and
> When integers are divided, the result of the `/` operator is the algebraic quotient with any fractional part discarded. If the quotient `a/b` is representable, the expression `(a/b)*b + a%b` shall equal `a`.

Discarding the fractional part of the remainder is often called *truncation toward zero*.
The C definition of the `%` operator implies the following behavior:
``` java
 11 %  5  ->  1
 11 % -5  ->  1
-11 %  5  -> -1
-11 % -5  -> -1
```
The result has the same sign as the dividend (the first operand in the expression).
## Noncompliant Code Example
In this noncompliant code example, the `insert()` function adds values to a buffer in a modulo fashion, that is, by inserting values at the beginning of the buffer once the end is reached. However, both `size` and `index` are declared as `int` and consequently are not guaranteed to be positive. Depending on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) and on the sign of `size` and `index`, the result of `(index + 1) % size` may be negative, resulting in a write outside the bounds of the `list` array.
``` c
int insert(int index, int *list, int size, int value) {
  if (size != 0) {
    index = (index + 1) % size;
    list[index] = value;
    return index;
  }
  else {
    return -1;
  }
}
```
This code also violates [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).
## Noncompliant Code Example
Taking the absolute value of the modulo operation returns a positive value:
``` c
int insert(int index, int *list, int size, int value) {
  if (size != 0) {
    index = abs((index + 1) % size);
    list[index] = value;
    return index;
  }
  else {
    return -1;
  }
}
```
However, this noncompliant code example violates [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](INT01-C_%20Use%20rsize_t%20or%20size_t%20for%20all%20integer%20values%20representing%20the%20size%20of%20an%20object). There is also a possibility that `(index + 1)` could result in a signed integer overflow in violation of [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow).
## Compliant Solution (Unsigned Types)
The most appropriate solution in this case is to use unsigned types to eliminate any possible [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior), as in this compliant solution. For compliance with [ERR02-C. Avoid in-band error indicators](https://www.securecoding.cert.org/confluence/display/seccode/ERR02-C.+Avoid+in-band+error+indicators), this solution fills a result argument with the mathematical result and returns nonzero only if the operation succeeds.
``` c
int insert(size_t* result, size_t index, int *list, size_t size, int value) {
  if (size != 0 && size != SIZE_MAX) {
    index = (index + 1) % size;
    list[index] = value;
    *result = index;
    return 1;
  }
  else {
    return 0;
  }
}
```
## Risk Assessment
Incorrectly assuming that the result of the remainder operator for signed operands will always be positive can lead to an out-of-bounds memory accessor other flawed logic.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT10-C | High | Unlikely | High | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  | Could detect the specific noncompliant code example. It could identify when the result of a % operation might be negative and flag usage of that result in an array index. It could conceivably flag usage of any such result without first checking that the result is positive, but;it would likely introduce many false positives |
| Helix QAC | 2024.4 | C3103 |  |
| LDRA tool suite | 9.7.1 | 584 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT10-a | The operands of the remainder operator '%' should be of unsigned integer types |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT10-C | Checks for tainted modulo operand (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+contains+INT10-A).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT10-CPP. Do not assume a positive remainder when using the % operator |
| CERT Oracle Secure Coding Standard for Java | NUM02-J. Ensure that division and remainder operations do not result in divide-by-zero errors |
| MITRE CWE | CWE-682, Incorrect calculationCWE-129, Unchecked array indexing |

## Bibliography

|  |  |
| ----|----|
| [Beebe 2005] |  |
| [ISO/IEC 9899:2011] | Subclause 6.5.5, "Multiplicative Operators" |
| [Microsoft 2007] | C Multiplicative Operators |
| [Sun 2005] | Appendix E, "Implementation-Defined ISO/IEC C90 Behavior" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152467) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152212)
## Comments:

|  |
| ----|
| 
All of these implementions appear to implement the C99 behavior:
Implementation Details
Microsoft Visual Studio
In division where either operand is negative, the direction of truncation is toward 0.
If either operation is negative in division with the remainder operator, the result has the same sign as the dividend (the first operand in the expression). For example:
50 % -6 = 2
-50 % 6 = -2

In each case, 50 and 2 have the same sign.
#### Sun Studio 10 C 5.7 Compiler
The result is the same sign as the dividend; thus, the remainder of -23/4 is -3.
#### gcc
GCC always follows the C99 requirement that the result of division is truncated towards zero.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Dec 20, 2007 13:19
\| \|
C99 imposed a Fortran-compatible requirement in an attempt to attract more Fortran programmers and to aid in converting Fortran code to C.; Frankly, I think that if it was going to be nailed down, it should have been to produce a strict step behavior (see Knuth's discussion of "mod" in \_*The Art of Computer Programming*), which has better mathematical properties.  It is almost never the case that a calculation should be using `minus % X` or `X % minus`, and when it should, truncating toward zero is probably the wrong behavior.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 16:29
\| \|
This recommendation is labeled "unenforceable" which is counter-indicated by the automated detection section which states:
Fortify SCA Version 5.0 with the CERT C Rule Pack can detect violations of this recommendation.
One way to analyze this would be to determine if the signed result of a % expression was used as an array index or other manner requiring a non-negative value.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 12, 2009 10:22
\| \|
Adjusted the tags accordingly. I don't think we can catch all instances of a negative mod result, but we can certainly catch the one example described here.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 12, 2009 10:59
\| \|
In the compliant code section, the definition of "a true (never negative) modulo operation" looks a bit weird to me. eg. imod(-5, 3) returns 1, which sort of contradicts my intuition. (which might not be the point of this recommendation though...)
![](images/icons/contenttypes/comment_16.png) Posted by masaki at May 12, 2009 03:22
\| \|
Good point. Negative modulo has two 'intuitive' answers: -5%3=-2 vs -5%3=1. So it's fallacious to speak of a 'true' mod operator. Adjusted paragraph accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 12, 2009 09:44
\| \|
The compliant solution produces signed overflow due to integer promotion. You guys are dumb.
![](images/icons/contenttypes/comment_16.png) Posted by anon3301 at Dec 08, 2009 00:33
\| \|
I appreciate the comment, but not the insults. Please try to behave in a professional manner in keeping with the terms and conditions on this website.
The compliant solution has no signed overflow because it uses unsigned types.
Both noncompliant solutions have the potential for signed integer overflow when adding `(index + 1)`. I'm going to clarify that this is also a problem.
I don't see any possibility of overflow from the expression `abs((index + 1) % size)` because the modulo operation cannot return `INT_MIN`.
``` java
INT_MIN = -2147483648.
0 % INT_MIN = 0.
1 % INT_MIN = 1.
(INT_MIN - 1) % INT_MIN = 2
(INT_MIN) % INT_MIN = 0.
```
Integer promotions are not a factor in this example because it only applies to the small integer types `char` and `short`.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Dec 08, 2009 09:31
\| \|
Integer promotion applies to integer types whose integer conversion rank is less than or equal to an int and
unsigned int. The compliant solution wrongly assumes that size_t has a rank greater than an int.
The modulo is irrelevant. It cannot undo signed overflow. Have you guys even read a third of the standard?
I'm at like 20 percent of the draft - so yes - you guys are dumb.
![](images/icons/contenttypes/comment_16.png) Posted by anon3301 at Dec 08, 2009 16:21
\| \|
If sizeof(size_t) == sizeof(int), then the expression (index + 1) converts the +1 to unsigned int. Which has no effect on the calculation, as the bits are preserved. Index may wrap, There might also be a conversion of index to an int when it is returned, but again, the bits are preserved
I don't know of any platform where sizeof(size_t) \< sizeof(int), but it is permitted by C99. If we assume all sizes are powers of 2, then sizeof(size_t) \<= sizeof(int) / 2. Then a promotion occurs on (index + 1), where index gets promoted to (signed) int. No overflow is possible, since index \<= SIZE_MAX \< INT_MAX. And a promotion occurs when returning index, again with all bits preserved.
The only other interesting scenario would be if SIZE_MAX == INT_MAX. IOW size_t has the same number of value bits as (signed) int, but int has a signed bit, whereas size_t does not. If index == SIZE_MAX, then index+1 might be expected to wrap, but would not wrap due to the promotion to int. Consequently the modulo produces an unexpected result (then again, it depends on what you are expecting, I guess.) Technically this is not overflow or wrapping, but it is weird, and I know of no platforms with this cockeyed configuration...do you?
An easy fix would be to ensure that index != SIZE_MAX. Which is a good idea if you don't want wrapping on any platform.
There is a problem with this compliant example, but it has nothing to do with math. Returning either index, which represents an unsigned size, or returning -1 represents an in-bound error condition, which is forbidden by [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 09, 2009 09:19
\| \|
Made both of the fixes I suggested.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 09, 2009 09:31
\| \|
I don't see this mapping to cwe 129?
![](images/icons/contenttypes/comment_16.png) Posted by azukich at Feb 22, 2010 12:48
\| \|
The fix could be made by simply adding a unsigned integer one.
So the expression would be:; \*`index = (index + 1U) % size;`\*
Assuming those weird conditions, you described, index will get promoted, using integer promotions, to unsigned int, and will wrap normally if SIZE_MAX == UINT_MAX.
![](images/icons/contenttypes/comment_16.png) Posted by curious_integer at Aug 25, 2015 11:10
\|
