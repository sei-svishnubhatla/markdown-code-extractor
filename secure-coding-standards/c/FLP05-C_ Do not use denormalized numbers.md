Most implementations of C use the IEEE 754 standard for floating-point representation. In this representation, floats are encoded using 1 sign bit, 8 exponent bits, and 23 mantissa bits. Doubles are encoded and used exactly the same way, except they use 1 sign bit, 11 exponent bits, and 52 mantissa bits. These bits encode the values of *s*, the sign; *M*, the significand; and *E*, the exponent. Floating-point numbers are then calculated as (−1)*<sup>s</sup>* \* *M* \* 2 *<sup>E</sup>*.
Ordinarily, all of the mantissa bits are used to express significant figures, in addition to a leading 1, which is implied and therefore left out. Consequently, floats ordinarily have 24 significant bits of precision, and doubles ordinarily have 53 significant bits of precision. Such numbers are called *normalized numbers*. All floating-point numbers are limited in the sense that they have fixed precision. See [FLP00-C. Understand the limitations of floating-point numbers](FLP00-C_%20Understand%20the%20limitations%20of%20floating-point%20numbers).
Mantissa bits are used to express extremely small numbers that are too small to encode normally because of the lack of available exponent bits. Using mantissa bits extends the possible range of exponents. Because these bits no longer function as significant bits of precision, the total precision of extremely small numbers is less than usual. Such numbers are called *denormalized,* and they are more limited than normalized numbers. However, even using normalized numbers where precision is required can pose a risk. See [FLP02-C. Avoid using floating-point numbers when precise computation is needed](FLP02-C_%20Avoid%20using%20floating-point%20numbers%20when%20precise%20computation%20is%20needed) for more information.
Denormalized numbers can severely impair the precision of floating-point numbers and should not be used.
## Noncompliant Code Example
This code attempts to reduce a floating-point number to a denormalized value and then restore the value. This operation is imprecise.
``` c
#include <stdio.h>
float x = 1/3.0;
printf("Original    : %e\n", x);
x = x * 7e-45;
printf("Denormalized: %e\n", x);
x = x / 7e-45;
printf("Restored    : %e\n", x);
```
This code produces the following output on [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) that use IEEE 754 floats:
``` java
Original    : 3.333333e-01
Denormalized: 2.802597e-45
Restored    : 4.003710e-01
```
## Compliant Solution
Do not allow code to produce denormalized numbers. If floats are producing denormalized numbers, use doubles instead.
``` c
#include <stdio.h>
double x = 1/3.0;
printf("Original    : %e\n", x);
x = x * 7e-45;
printf("Denormalized: %e\n", x);
x = x / 7e-45;
printf("Restored    : %e\n", x);
```
``` java
Original    : 3.333333e-01
Denormalized: 2.333333e-45
Restored    : 3.333333e-01
```
If using doubles also produces denormalized numbers, using long doubles may or may not help. (On some implementations, long double has the same exponent range as double.) If using long doubles produces denormalized numbers, some other solution must be found.
### Printing Denormalized Numbers
Denormalized numbers can also be troublesome because some functions have [implementation-defined](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions) behavior when used with denormalized values. For example, using the `%a` or `$%A` conversion specifier in a format string can produce implementation-defined results when applied to denormalized numbers.
Subclause 7.21.6.1, paragraph 8, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], states:
> A double argument representing a floating-point number is converted in the style `[-]0`*`x`*`h.hhhh p`*`±`*`d`, where there is one hexadecimal digit (which is nonzero if the argument is a normalized floating-point number and is otherwise unspecified) before the decimal-point character.

Relying on the `%a` and `%A` specifiers to produce values without a leading zero is error prone.
``` java
#include<stdio.h>
float x = 0x1p-125;
double y = 0x1p-1020;
printf("normalized float with %%e    : %e\n", x);
printf("normalized float with %%a    : %a\n", x);
x = 0x1p-140;
printf("denormalized float with %%e  : %e\n", x);
printf("denormalized float with %%a  : %a\n", x);
printf("normalized double with %%e   : %e\n", y);
printf("normalized double with %%a   : %a\n", y);
y = 0x1p-1050;
printf("denormalized double with %%e : %e\n", y);
printf("denormalized double with %%a : %a\n", y);
```
### Implementation Details
On a 32-bit Linux machine using GCC 4.3.2, this code produces the following output:
``` java
normalized float with %e    : 2.350989e-38
normalized float with %a    : 0x1p-125
denormalized float with %e  : 7.174648e-43
denormalized float with %a  : 0x1p-140
normalized double with %e   : 8.900295e-308
normalized double with %a   : 0x1p-1020
denormalized double with %e : 8.289046e-317
denormalized double with %a : 0x0.0000001p-1022
```
## Risk Assessment
Floating-point numbers are an approximation; using subnormal floating-point number are a worse approximation.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP05-C | Low | Probable | High | P2 | L3 |

### Automated Detection
TODO
### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FILP05-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT Oracle Secure Coding Standard for Java | NUM54-J. Do not use denormalized numbers |

## Bibliography

|  |  |
| ----|----|
| [Bryant 2003] | Section 2.4, "Floating Point" |
| [IEEE 754] | ; |
| [ISO/IEC 9899:2011] | Subclause 7.21.6.1, "The fprintf Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152304) [](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152079)
## Comments:

|  |
| ----|
| The code example assumes that normalized values will always be converted (by %a) to a string starting with "0x1." or "-0x1.", but this is not guaranteed by C99.  E.g. the strings "0x1.0p+8", "0x2.0p+7", "0x4.0p+6" and "0x8.0p+5" are all equally valid conversions of the value 256.
                                        Posted by geoffclare at Mar 27, 2009 05:34
                                     |
| Thanks for the code sample. i'm convinced this is a good rule. And thanks for addressing my other concerns. I have a few more concerns, plus you should address the issues raised by Rob and Geoff, too.
    Given the nature of your code sample, I'm not sure it should be called a NCCE, since your code correctly demonstrates the 'weird' behavior of %a. Your code sample should probably go into the intro section, and not be colored red. After that, you may have NCCE/CS if you wish, but they should illustrate the 'wrong' way and the 'right' way to interpret %a output. Given your current code sample, I'm not sure they are necessary.
    For illustrative purposes, your code sample should print the floats with %a as well as %e, to demonstrate to the user what output they actually get.
Finally, don't forget to fill in the TODO sections. (Except for Automated Detection...we'll worry about that later.)
                                        Posted by svoboda at Mar 27, 2009 10:32
                                     |
| 
    Include the full title when referencing FLP02-C
    The ccompliant solution code is exactly like the NCCE...perhaps you forgot to s/float/double/?
    The reference needs a bit more info (author, publisher?). If this book is not listed in the References page, please provide a complete bibliographic index for the book.
    Incidentally, what happened to %a?  Printig %a values might be illustrative (though not necessary).
                                        Posted by svoboda at Apr 01, 2009 08:03
                                     |
| i made the s/float/double/ changed david suggested.  correct us if we are wrong.
i also trimmed the includes and main() from the examples.  these are not needed (unless they influence the examples somehow).
rCs
                                        Posted by rcs at Apr 01, 2009 08:22
                                     |

