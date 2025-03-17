Integer constants are often used as masks or specific bit values. Frequently, these constants are expressed in hexadecimal form to indicate to the programmer how the data might be represented in the machine. However, hexadecimal integer constants are frequently used in a nonportable manner.
## Noncompliant Code Example
In this pedagogical noncompliant code example, the `flipbits()` function complements the value stored in `x` by performing a bitwise exclusive OR against a mask with all bits set to 1. For [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) where `unsigned long` is represented by a 32-bit value, each bit of `x` is correctly complemented.
``` c
/* (Incorrect) Set all bits in mask to 1 */
const unsigned long mask = 0xFFFFFFFF;
unsigned long flipbits(unsigned long x) {
  return x ^ mask;
}
```
However, on implementations where values of type `unsigned long` are represented by greater than 32 bits, `mask` will have leading 0s. For example, on implementations where values of type `unsigned long` are 64 bits long, `mask` is assigned the value `0x00000000FFFFFFFF`. Consequently, only the lower-order bits of `x` are complemented.
## Compliant Solution (−1)
In this compliant solution, the integer constant `-1` is used to set all bits in `mask` to 1. The integer constant `-1` is of type `signed int`. Because `-1` cannot be represented by a variable of type `unsigned long`, it is converted to a representable number according to the rule in subclause 6.3.1.3, paragraph 2, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
> \[If the value can't be represented by the new type and\] if the new type is unsigned, the value is converted by repeatedly adding or subtracting one more than the maximum value that can be represented in the new type until the value is in the range of the new type.

"One more than the maximum value that can be represented in the new type," `ULONG_MAX + 1`, is added to `-1`, resulting in a right-side value of `ULONG_MAX`. The representation of `ULONG_MAX` is guaranteed to have all bits set to 1 by subclause 6.2.6.2, paragraph 1:
> For unsigned integer types other than `unsigned char`, the bits of the object representation shall be divided into two groups: value bits and padding bits (there need not be any of the latter). If there are *N* valuebits, each bit shall represent a different power of 2 between 1 and 2<sup>*N* −\ 1</sup>, so that objects of that type shall be capable of representing values from 0 to 2<sup>*N*</sup> − 1 using a **pure binary representation**; this shall be known as the value representation. The values of any padding bits are unspecified.

By the same reasoning, `-1` is suitable for setting all bits to one of any unsigned integer variable. Subclause 6.2.6.1, paragraph 3, guarantees the same results for `unsigned char`:
> Values stored in unsigned bit-fields and objects of type `unsigned char` shall be represented using a **pure binary notation**.

``` c
/* (Correct) Set all bits in mask to 1 */
const unsigned long mask = -1;
unsigned long flipbits(unsigned long x) {
  return x ^ mask;
}
```
## Noncompliant Code Example
In this noncompliant code example, a programmer attempts to set the most significant bit:
``` c
const unsigned long mask = 0x80000000;
unsigned long x;
/* Initialize x */
x |= mask;
```
This code has the desired effect for implementations where `unsigned long` has a precision of 32 bits but not for implementations where `unsigned long` has a precision of 64 bits.
## Compliant Solution
A portable (and safer) way of setting the high-order bit is to use a shift expression, as in this compliant solution:
``` c
const unsigned long mask = ~(ULONG_MAX >> 1);
unsigned long x;
/* Initialize x */
x |= mask;
```
## Risk Assessment
[Vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) are frequently introduced while porting code. A buffer overflow vulnerability may result, for example, if an incorrectly defined integer constant is used to determine the size of a buffer. It is always best to write portable code, especially when there is no performance overhead for doing so.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT17-C | High | Probable | Low | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT17 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT17-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT17-CPP. Define integer constants in an implementation-independent manner |

## Bibliography

|  |  |
| ----|----|
| [Dewhurst 2002] | Gotcha #25, "#define Literals" |
| [ISO/IEC 9899:2011] | Subclause 6.2.6, "Representations of Types"Subclause 6.3.1.3, "Signed and Unsigned Integers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152334) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152419)
## Comments:

|  |
| ----|
| The NCE/CS about using ~0 to set all bits to 1 is incorrect for some implementations.  Instead, the programmer should use -1.  The best explanation I found for why ~0 is wrong was in the comments to this answer:
The simplest example is on a one's-complement platform. On such a platform "~x == -x" is true for signed integers. Therefore, "~0 == -0" is true. On that platform, "flags = ~0" is the same as "flags = -0", which in turn is the same as "flags = 0". So on a one's-complement platform "flags = ~0" results in no bits being set.
                                        Posted by akeeton at Jun 14, 2011 09:43
                                     |
| That's what you get when you violate INT14-C. Avoid performing bitwise and arithmetic operations on the same data. The ~ operator performs as you expect, but casting the value from an int to an unsigned long preserves the value, not the bits. So the 0xFFF... AKA 0 on one's-complement machines) value becomes 0x000...AKA 0. I fixed this by using ~0UL rather than ~0, thereby preventing any conversion from taking place.
Unfortunately this is theoretical, as we don't have a ones-complement machine for testing 
                                        Posted by svoboda at Jun 14, 2011 12:03
                                     |
| On the one hand, ~0UL is more intuitive than -1, i.e. "Flipping all zeros gives me all ones."  However, this thinking can lead you to forgetting the UL and ending up with ~0.
On the other hand, while -1 is less intuitive, it's easier to get right.
So, should we endorse ~0U/~0UL/~0ULL or -1?
EDIT:
To clarify what's going on with -1, according to C99, Section 6.3.1.3, Paragraph 2:
Otherwise, if the new type is unsigned, the value is converted by repeatedly adding or
subtracting one more than the maximum value that can be represented in the new type
until the value is in the range of the new type.
So, for example,
unsigned int a = -1;      // -1 is converted to UINT_MAX + 1 + (-1) = UINT_MAX
unsigned long b = -1;     // -1 is converted to ULONG_MAX + 1 + (-1) = ULONG_MAX

and so on, for each unsigned integer type.
The C99 standard guarantees that unsigned integers are represented in binary in Section 6.2.6.2, Paragraph 1:
> For unsigned integer types other than unsigned char, the bits of the object  
> representation shall be divided into two groups: value bits and padding bits (there need  
> not be any of the latter). If there are N value bits, each bit shall represent a different  
> power of 2 between 1 and 2^(N ? 1) , so that objects of that type shall be capable of  
> representing values from 0 to 2^N ? 1 using a pure binary representation; this shall be  
> known as the value representation. The values of any padding bits are unspecified.

Assuming "pure binary representation" means that a `1` means that bit is "on," then a maximal unsigned integer has all bits set to `1`. /pedantry
All of this means that `-1` converted to an unsigned integer results in all bits set to `1`.
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Jun 14, 2011 12:17
\| \|
The fact that 99% of platforms today use twos-complement heavily skews this question. My recommendation is:
-   In the most portable code, the type of 0 must match the type of integer:
``` java
int num1 = ~0;
unsigned long num2 = ~0UL;
long long num3 = ~0LL;
```
-   But unless you think your code might ever run on signed-magnitude or ones-complement platform, use `~0`
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 14, 2011 13:11
\| \|
If I'm interpreting the C99 standard correctly, I think we can recommend using `~0ULL` for any resultant type. For example, assume I have
``` java
unsigned char mask = ~0ULL;
```
Applying Section 6.3.1.3, Paragraph 2:
> \[If the value can't be represented by the new type and\] if the new type is unsigned, the value is converted by repeatedly adding or subtracting one more than the maximum value that can be represented in the new type until the value is in the range of the new type.

So, with `UCHAR_MAX + 1` = 2 <sup>8</sup> = 0x100, we keep subtracting 0x100 from `~0ULL` = `ULLONG_MAX` = 0xFFFFFFFFFFFFFFFF until all of the bits above 0xFF are eliminated. 0xFF is the first value that will fit in an `unsigned char` and is conveniently `UCHAR_MAX`.
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Jun 14, 2011 13:40
\| \|
But won't a ones-complement system still convert -0ULL to 0?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 14, 2011 15:01
\| \|
Because `~0ULL` is unsigned, one's complement shouldn't even come into play. You will just have an unsigned binary number of all ones whose value is `ULLONG_MAX` (on any system).
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Jun 14, 2011 15:08
\| \|
The first compliant solution gives signed/unsigned mismatch warnings at /W4 in Visual Studio.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 19, 2013 16:18
\| \|
Well, we have a rule saying "compile with high warnings". But the behavior in the CS is guaranteed by the C standard. We also have rules about suppressing warnings (in Java, not sure about C), saying "suppress as specific and as narrowly as possible". I would conclude that using the 1st CS in real code is still recommended by CERT even if the compiler complains...suppressing that compiler warning is OK, as long as you are very narrow and specific about where the warning is suppressed.
BTW this quote has a different problem:
> By the same reasoning, -1 is suitable for setting all bits to one of any unsigned integer variable

This applies only to twos-complement systems (which all modern machines happen to be). So doing this saccrifices some portability. The text should reflect this.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 26, 2013 13:50
\|
