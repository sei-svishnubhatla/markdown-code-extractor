Avoid performing bitwise and arithmetic operations on the same data. In particular, bitwise operations are frequently performed on arithmetic values as a form of premature optimization. Bitwise operators include the unary operator `~` and the binary operators `<<`, `>>`, `&`, `^`, and `|`. Although such operations are valid and will compile, they can reduce code readability. Declaring a variable as containing a numeric value or a bitmap makes the programmer's intentions clearer and the code more maintainable.
Bitmapped types may be defined to further separate bit collections from numeric types. Doing so may make it easier to verify that bitwise operations are performed only on variables that represent bitmaps.
``` java
typedef uint32_t bitmap32_t;
bitmap32_t x = 0x000007f3;
x = (x << 2) | 3; /* Shifts in two 1-bits from the right */
```
The `typedef` name `uintN_t` designates an unsigned integer type with width `N`. Consequently, `uint32_t` denotes an unsigned integer type with a width of exactly 32 bits. Bitmaps should be declared as unsigned. See [INT13-C. Use bitwise operators only on unsigned operands](INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands).
Left- and right-shift operators are often employed to multiply or divide a number by a power of 2. However, using shift operators to represent multiplication or division is an optimization that renders the code less portable and less readable. Furthermore, most compilers routinely optimize multiplications and divisions by constant powers of 2 with bit-shift operations, and they are more familiar with the implementation details of the current platform.
## Noncompliant Code Example (Left Shift)
In this noncompliant code example, both bit manipulation and arithmetic manipulation are performed on the integer `x`. The result is a (prematurely) optimized statement that assigns `5x + 1` to `x` for [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) where integers are represented as two's complement values.
``` c
unsigned int x = 50;
x += (x << 2) + 1;
```
Although this is a valid manipulation, the result of the shift depends on the underlying representation of the integer type and is consequently [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementationdefinedbehavior). Additionally, the readability of the code is reduced.
## Compliant Solution (Left Shift)
In this compliant solution, the assignment statement is modified to reflect the arithmetic nature of `x`, resulting in a clearer indication of the programmer's intentions:
``` c
unsigned int x = 50;
x = 5 * x + 1;
```
A reviewer may now recognize that the operation should also be checked for wrapping. This might not have been apparent in the original, noncompliant code example.
## Noncompliant Code Example (Right Shift)
In this noncompliant code example, the programmer prematurely optimizes code by replacing a division with a right shift:
``` c
int x = -50;
x >>= 2;
```
Although this code is likely to perform the division correctly, it is not guaranteed to. If `x` has a signed type and a negative value, the operation is implementation-defined and can be implemented as either an arithmetic shift or a logical shift. In the event of a logical shift, if the integer is represented in either one's complement or two's complement form, the most significant bit (which controls the sign for both representations) will be set to 0, causing a once negative number to become a possibly very large, positive number. For more details, see [INT13-C. Use bitwise operators only on unsigned operands](INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands).
For example, if the internal representation of `x` is `0xFFFF FFCE` (two's complement), an arithmetic shift results in `0xFFFF FFF3` (−13 in two's complement), whereas a logical shift results in `0x3FFF FFF3` (1,073,741,811 in two's complement).
## Compliant Solution (Right Shift)
In this compliant solution, the right shift is replaced by division:
``` c
int x = -50;
x /= 4;
```
The resulting value is now more likely to be consistent with the programmer's expectations.
## Exceptions
**INT14-C-EX0**: Routines may treat integers as bit vectors for I/O purposes. That is, they may treat an integer as a series of bits in order to write it to a file or socket. They may also read a series of bits from a file or socket and create an integer from the bits.
## Risk Assessment
Performing bit manipulation and arithmetic operations on the same variable obscures the programmer's intentions and reduces readability. It also makes it more difficult for a security auditor or maintainer to determine which checks must be performed to eliminate [security flaws](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) and ensure data integrity.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT14-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  | Can detect violations of this recommendation. However, it can detect only those violations where both bitwise and arithmetic operators are used in the same expression |
| LDRA tool suite | 9.7.1 | 585 S | Fully implemented |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT14-C | Checks for bitwise and arithmetic operation on the same data;(rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT14-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT14-CPP. Avoid performing bitwise and arithmetic operations on the same data |
| CERT Oracle Secure Coding Standard for Java | NUM01-J. Do not perform bitwise and arithmetic operations on the same data |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Rule 6.1 (required)Rule 6.2 (required) |

## Bibliography

|  |
| ----|
| [Steele 1977] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152374) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152366)
## Comments:

|  |
| ----|
| I just came across the following code. It is notportable, but portability was explicitly not a requirement here, and I think it is a reasonable mixture of bitwise operators and math, and cannot be easily computed using pure math. How does this affect this rule?
  unsigned long long one = 1;
  unsigned long long signed_max = (one << 63) - one;

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 06, 2008 09:47
\| \|
Another snippet of non-portable code. The `g_ntohs` macro of GLIB2 uses this code to swap low and high-order bytes of a 16-bit unsigned int:
``` java
__v = (__v >> 8) | (__v << 8)
```
Definitely could use some security enhancements (to prevent overflow), but the point is: our rec here needs some way of indicating legit exceptions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 12, 2009 17:07
\| \|
In the automated detection section, Fortify: "... but cannot distinguish between operations of positive and negative numbers." doesn't make sense to me.
![](images/icons/contenttypes/comment_16.png) Posted by masaki at May 14, 2009 01:58
\| \|
Most of the rest of that sentence didn't make sense to me either so I trimmed it down quite a lot.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 14, 2009 08:29
\| \|
Another exception to this rec: The code examples in [INT17-C. Define integer constants in an implementation-independent manner](INT17-C_%20Define%20integer%20constants%20in%20an%20implementation-independent%20manner) combine bitwise operators and addition to change the sign on a number using twos-complement arithmetic.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 23, 2009 13:30
\| \|
Having found counterexamples over the years, I think we can limit them to two exceptions:
-   It's ok to use shift & math operators for contant-time expressions (eg max = 1 \<\< 10 - 1)
-   It's ok to use shift operators on 'mathematical integers' for the purpose of serialization. That is, integers treated mathematically elsewhere may be bit-shifted for the purpose of doing file or network I/O.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 14, 2011 12:06
\| \|
[INT36-C. Do not perform bitwise and arithmetic operations on the same variable](/confluence/pages/createpage.action?spaceKey=c&title=INT36-C.+Do+not+perform+bitwise+and+arithmetic+operations+on+the+same+variable) renders this rule obsolete.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 11, 2013 15:50
\|
