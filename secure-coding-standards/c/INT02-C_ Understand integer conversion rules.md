Conversions can occur explicitly as the result of a cast or implicitly as required by an operation. Although conversions are generally required for the correct execution of a program, they can also lead to lost or misinterpreted data. Conversion of an operand value to a compatible type causes no change to the value or the representation.
The C integer conversion rules define how C compilers handle conversions. These rules include *integer promotions*, *integer conversion rank*, and the *usual arithmetic conversions*. The intent of the rules is to ensure that the conversions result in the same numerical values and that these values minimize surprises in the rest of the computation. Prestandard C usually preferred to preserve signedness of the type.
## Integer Promotions
Integer types smaller than `int` are promoted when an operation is performed on them. If all values of the original type can be represented as an `int`, the value of the smaller type is converted to an `int`; otherwise, it is converted to an `unsigned int`. Integer promotions are applied as part of the usual arithmetic conversions to certain argument expressions; operands of the unary `+`, `-`, and `~` operators; and operands of the shift operators. The following code fragment shows the application of integer promotions:
``` java
char c1, c2;
c1 = c1 + c2;
```
Integer promotions require the promotion of each variable (`c1` and `c2`) to `int` size. The two `int` values are added, and the sum is truncated to fit into the `char` type. Integer promotions are performed to avoid arithmetic errors resulting from the overflow of intermediate values:
``` java
signed char cresult, c1, c2, c3;
c1 = 100;
c2 = 3;
c3 = 4;
cresult = c1 * c2 / c3;
```
In this example, the value of `c1` is multiplied by `c2`. The product of these values is then divided by the value of `c3` (according to operator precedence rules). Assuming that `signed char` is represented as an 8-bit value, the product of `c1` and `c2` (300) cannot be represented. Because of integer promotions, however, `c1`, `c2`, and `c3` are each converted to `int`, and the overall expression is successfully evaluated. The resulting value is truncated and stored in `cresult`. Because the final result (75) is in the range of the `signed char` type, the conversion from `int` back to `signed char` does not result in lost data.
## Integer Conversion Rank
Every integer type has an integer conversion rank that determines how conversions are performed. The ranking is based on the concept that each integer type contains at least as many bits as the types ranked below it. The following rules for determining integer conversion rank are defined in the C Standard, subclause 6.3.1.1 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
-   No two signed integer types shall have the same rank, even if they have the same representation.
-   The rank of a signed integer type shall be greater than the rank of any signed integer type with less precision.
-   The rank of `long long int` shall be greater than the rank of `long int`, which shall be greater than the rank of `int`, which shall be greater than the rank of `short int`, which shall be greater than the rank of `signed char`.
-   The rank of any unsigned integer type shall equal the rank of the corresponding signed integer type, if any.
-   The rank of any standard integer type shall be greater than the rank of any extended integer type with the same width.
-   The rank of `char` shall equal the rank of `signed char` and `unsigned char`.
-   The rank of `_Bool` shall be less than the rank of all other standard integer types.
-   The rank of any enumerated type shall equal the rank of the compatible integer type.
-   The rank of any extended signed integer type relative to another extended signed integer type with the same precision is [implementation-defined](http://BB.%20Definitions#implementation-defined) but still subject to the other rules for determining the integer conversion rank.
-   For all integer types `T1`, `T2`, and `T3`, if `T1` has greater rank than `T2` and `T2` has greater rank than `T3`, then `T1` has greater rank than `T3`.
The integer conversion rank is used in the usual arithmetic conversions to determine what conversions need to take place to support an operation on mixed integer types.
## Usual Arithmetic Conversions
The usual arithmetic conversions are rules that provide a mechanism to yield a common type when both operands of a binary operator are balanced to a common type or the second and third operands of the conditional operator ( `? :` ) are balanced to a common type. Conversions involve two operands of different types, and one or both operands may be converted. Many operators that accept arithmetic operands perform conversions using the usual arithmetic conversions. After integer promotions are performed on both operands, the following rules are applied to the promoted operands:
1.  If both operands have the same type, no further conversion is needed.
2.  If both operands are of the same integer type (signed or unsigned), the operand with the type of lesser integer conversion rank is converted to the type of the operand with greater rank.
3.  If the operand that has unsigned integer type has rank greater than or equal to the rank of the type of the other operand, the operand with signed integer type is converted to the type of the operand with unsigned integer type.
4.  If the type of the operand with signed integer type can represent all of the values of the type of the operand with unsigned integer type, the operand with unsigned integer type is converted to the type of the operand with signed integer type.
5.  Otherwise, both operands are converted to the unsigned integer type corresponding to the type of the operand with signed integer type.
## Example
In the following example, assume the code is compiled using an implementation with 8-bit `char`, 32-bit `int`, and 64-bit `long long`:
``` java
signed char sc = SCHAR_MAX;
unsigned char uc = UCHAR_MAX;
signed long long sll = sc + uc;
```
Both the `signed char sc` and the `unsigned char uc` are subject to integer promotions in this example. Because all values of the original types can be represented as `int`, both values are automatically converted to `int` as part of the integer promotions. Further conversions are possible if the types of these variables are not equivalent as a result of the usual arithmetic conversions. The actual addition operation, in this case, takes place between the two 32-bit `int` values. This operation is not influenced by the resulting value being stored in a `signed long long` integer. The 32-bit value resulting from the addition is simply sign-extended to 64 bits after the addition operation has concluded.
Assuming that the precision of `signed char` is 7 bits, and the precision of `unsigned char` is 8 bits, this operation is perfectly safe. However, if the compiler represents the `signed char` and `unsigned char` types using 31- and 32-bit precision (respectively), the variable `uc` would need to be converted to `unsigned int` instead of `signed int`. As a result of the usual arithmetic conversions, the `signed int` is converted to unsigned, and the addition takes place between the two `unsigned int` values. Also, because `uc` is equal to `UCHAR_MAX`, which is equal to `UINT_MAX`, the addition results in an overflow in this example. The resulting value is then zero-extended to fit into the 64-bit storage allocated by `sll`.
## Noncompliant Code Example (Comparison)
The programmer must be careful when performing operations on mixed types. This noncompliant code example shows an idiosyncrasy of integer promotions:
``` c
int si = -1;
unsigned int ui = 1;
printf("%d\n", si < ui);
```
In this example, the comparison operator operates on a `signed int` and an `unsigned int`. By the conversion rules, `si` is converted to an `unsigned int`. Because −1 cannot be represented as an `unsigned int` value, the −1 is converted to `UINT_MAX` in accordance with the C Standard, subclause 6.3.1.3, paragraph 2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
> Otherwise, if the new type is unsigned, the value is converted by repeatedly adding or subtracting one more than the maximum value that can be represented in the new type until the value is in the range of the new type.

Consequently, the program prints 0 because `UINT_MAX` is not less than 1.
## Compliant Solution
The noncompliant code example can be modified to produce the intuitive result by forcing the comparison to be performed using `signed int` values:
``` c
int si = -1;
unsigned ui = 1;
printf("%d\n", si < (int)ui);
```
This program prints 1 as expected. Note that `(int)ui` is correct in this case only because the value of `ui` is known to be representable as an `int`. If it were not known, the compliant solution would need to be written as
``` c
int si = /* Some signed value */;
unsigned ui = /* Some unsigned value */;
printf("%d\n", (si < 0 || (unsigned)si < ui));
```
## Noncompliant Code Example
This noncompliant code example demonstrates how performing bitwise operations on integer types smaller than `int` may have unexpected results:
``` c
uint8_t port = 0x5a;
uint8_t result_8 = ( ~port ) >> 4;
```
In this example, a bitwise complement of `port` is first computed and then shifted 4 bits to the right. If both of these operations are performed on an 8-bit unsigned integer, then `result_8` will have the value `0x0a`. However, `port` is first promoted to a `signed int`, with the following results (on a typical architecture where type `int` is 32 bits wide):

| Expression | Type | Value | Notes |
| ----|----|----|----|
| port | uint8_t | 0x5a |  |
| ~port | int | 0xffffffa5 |  |
| ~port >> 4 | int | 0x0ffffffa | Whether or not value is negative is implementation-defined |
| result_8 | uint8_t | 0xfa |  |

## Compliant Solution
In this compliant solution, the bitwise complement of `port` is converted back to 8 bits. Consequently, `result_8` is assigned the expected value of `0x0aU`.
``` c
uint8_t port = 0x5a;
uint8_t result_8 = (uint8_t) (~port) >> 4;
```
## Noncompliant Code Example
In this example, a character is iterated from 0 to `CHAR_MAX`. However, on a platform where char is signed (such as 32-bit x86), `max`  is set to `0x80`  while `i`  increments from `0x79`  to {{0xffffff80} (aka -127):
``` c
#include <limits.h>
unsigned char max = CHAR_MAX + 1;
for (char i = 0; i < max; ++i) {
  printf("i=0x%08x max=0x%08x\n", i, max);
}
```
## Compliant Solution
There are several ways to rectify this example. One way is to treat both chars as unsigned, which prevents wraparound:
``` c
#include <limits.h>
unsigned char max = CHAR_MAX + 1;
for (unsigned char i = 0; i < max; ++i) {
  printf("i=0x%08x max=0x%08x\n", i, max);
}
```
## Noncompliant Code Example
This noncompliant code example, adapted from the [Cryptography Services blog](https://cryptoservices.github.io/fde/2018/11/30/undefined-behavior.html), demonstrates how signed overflow can occur even when it seems that only unsigned types are in use:
``` c
unsigned short x = 45000, y = 50000;
unsigned int z = x * y;
```
On implementations where `short` is 16 bits wide and `int` is 32 bits wide, the program results in undefined behavior due to signed overflow. This is because the `unsigned short`s become signed when they are automatically promoted to integer, and their mathematical product (2250000000) is greater than the largest signed 32-bit integer (2<sup>31</sup> - 1, which is 2147483647).
## Compliant Solution
In this compliant solution, by manually casting one of the operands to `unsigned int`, the multiplication will be unsigned and so will not result in undefined behavior:
``` c
unsigned short x = 45000, y = 50000;
unsigned int z = x * (unsigned int)y;
```
## Risk Assessment
Misunderstanding integer conversion rules can lead to errors, which in turn can lead to exploitable [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). The major risks occur when narrowing the type (which requires a specific cast or assignment), converting from unsigned to signed, or converting from negative to unsigned.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT02-C | Medium | Probable | Medium |  P8  |  L2  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| CodeSonar | 8.3p0 | ALLOC.SIZE.TRUNCLANG.CAST.COERCELANG.CAST.VALUEMISC.MEM.SIZE.TRUNC | Truncation of Allocation SizeCoercion Alters ValueCast Alters ValueTruncation of Size |
| ECLAIR | 1.2 | CC2.INT02 | Fully implemented |
| Helix QAC | 2024.4 | C1250, C1251, C1252, C1253, C1256, C1257, C1260, C1263, C1266, C1274, C1290, C1291, C1292, C1293, C1294, C1295, C1296, C1297, C1298, C1299, C1800, C1802, C1803, C1804, C1810, C1811, C1812, C1813, C1820, C1821, C1822, C1823, C1824, C1830, C1831, C1832, C1833, C1834, C1840, C1841, C1842, C1843, C1844, C1850, C1851, C1852, C1853, C1854, C1860, C1861, C1862, C1863, C1864, C1880, C1881, C1882, C2100, C2101, C2102, C2103, C2104, C2105, C2106, C2107, C2109, C2110, C2111, C2112, C2113, C2114, C2115, C2116, C2117, C2118, C2119, C2120, C2122, C2124, C2130, C2132, C2134, C4401, C4402, C4403, C4404, C4405, C4410, C4412, C4413, C4414, C4415, C4420, C4421, C4422, C4423, C4424, C4425, C4430, C4431, C4432, C4434, C4435, C4436, C4437, C4440, C4441, C4442, C4443, C4445, C4446, C4447, C4460, C4461, C4463, C4464, C4470, C4471, C4480, C4481 |  |
| Klocwork | 2024.4 | MISRA.CAST.INTMISRA.CAST.UNSIGNED_BITS
MISRA.CONV.INT.SIGN
MISRA.CVALUE.IMPL.CAST
MISRA.UMINUS.UNSIGNED
PRECISION.LOSS |  |
| LDRA tool suite | 9.7.1 |  52 S, 93 S, 96 S, 101 S, 107 S, 332 S, 334 S, 433 S, 434 S, 446 S, 452 S, 457 S, 458 S 
 | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT02-a CERT_C-INT02-b | Implicit conversions from wider to narrower integral type which may result in a loss of information shall not be usedAvoid mixing arithmetic of different precisions in the same expression |
| PC-lint Plus | 1.4 | 501, 502, 569, 570, 573,574, 701, 702, 732, 734,
737 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT02-C | Checks for sign change integer conversion overflow (rec. fully supported) |
| PVS-Studio | 7.35 | V555, V605,;V673, V5006 |  |

### Related Vulnerabilities
This [vulnerability](http://www.kb.cert.org/vuls/id/159523) in Adobe Flash arises because Flash passes a signed integer to `calloc()`. An attacker has control over this integer and can send negative numbers. Because `calloc()` takes `size_t`, which is unsigned, the negative number is converted to a very large number, which is generally too big to allocate, and as a result, `calloc()` returns `NULL`, causing the vulnerability to exist.
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT02-CPP. Understand integer conversion rules |
| ISO/IEC TR 24772:2013 | Numeric Conversion Errors [FLC] |
| MISRA C:2012 | Rule 10.1 (required)Rule 10.3 (required)
Rule 10.4 (required)
Rule 10.6 (required)
Rule 10.7 (required)
Rule 10.8 (required) |
| MITRE CWE | CWE-192, Integer coercion errorCWE-197, Numeric truncation error |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Type Conversions," pp.;223–270) |
| [Seacord 2013] | Chapter 5, "Integer Security" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152208) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152245)
## Comments:

|  |
| ----|
| In NCCE, why do you need to say "unsigned int is treated modularly" since unsigend in ui = 1 and there's no possibility of wraparound?
                                        Posted by masaki at May 07, 2009 02:40
                                     |
| Well, because there IS possibility of wraparound; it's just not mandated by the standard. On many platforms, including x86, signed ints do wrap. But the standard leaves this as undefined behavior, allowing other platforms to treat signed int overflow differently.
I changed the NCCE language you cite to reference the standard, and added the relevant quote from C99. It boils down to modular arithmetic, but is not defined in those terms, and we try to prefer the language used by the standard. HTH.
                                        Posted by svoboda at May 07, 2009 08:37
                                     |
| The explicit cast in the last line of the first compliant solution seems to be redundant:
printf("%d\n", (si < 0 || (unsigned)si < ui));

The automatic conversion in such a case is mentioned above and confirmed by C99, Section 6.3.1.8, paragraph 1.
![](images/icons/contenttypes/comment_16.png) Posted by sinic at May 23, 2011 18:06
\| \|
Yes it is technically redundant. It's still worthwhile IMHO as the conversion is not obvious to most programmers.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 24, 2011 13:14
\| \|
> Because −1 cannot be represented as an `unsigned int` value, the −1 is converted to `UINT_MAX` in accordance with the C Standard, subclause 6.3.1.3, paragraph 2 \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2011)\]:

This doesn't seem to be correct. IIUC the -1 is converted to an unsigned integer by adding UINT_MAX+1.
``` java
printf("%u\n", (unsigned)-10);
```
Outputs 4294967286, which is not the same as UINT_MAX.
![](images/icons/contenttypes/comment_16.png) Posted by bcvanduuren at Oct 13, 2014 11:35
\| \|
Did you mean to use -10 instead of -1?
A quick test of:
``` java
#include <stdio.h>
#include <limits.h>
int main(void) {
    printf("%u\n", (unsigned)-1);
    printf("%u\n", UINT_MAX);
    return 0;
}
```
Yields:
    4294967295
    4294967295
Which is what I would expect given the section quoted in the standard. Of special note, the footnote in that paragraph is not replicated. It reads:
> The rules describe arithmetic on the mathematical value, not the value of a given type of expression.

which helps explain how this conversion process works.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 13, 2014 12:34
\| \|
I understood the part I quoted to mean that every signed value that can't be represented as an unsigned value is converted to UINT_MAX. I used -10 to demonstrate that that is not correct.
For -1 the conversion will actually yield UINT_MAX, because -1+UINT_MAX+1 equals UINT_MAX. For every other value that cannot be represented by an unsigned this is not the case.
Am I misunderstanding the quoted part, or is it incorrect? ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by bcvanduuren at Oct 13, 2014 13:08
\| \|
I think you're misunderstanding the quoted part. It's saying that the signed value -10 cannot be represented as an unsigned int, so the value is converted to an unsigned int as described by the standard. The way the standard phrases that is rather obtuse. In this example, the new type is;unsigned int, and the maximum value for that is UINT_MAX. The way the conversion works is to take the original value and add/subtract UINT_MAX + 1 until you get a value that is in the range allowed by unsigned int. Eg) `unsigned int converted_value = -10 + UINT_MAX + 1;` which is how you arrive at the value 4294967286.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 14, 2014 10:38
\| \|
there is a strange sentence at the end of the usual arithmetic conversion rules:
;
> Specific operations can add to or modify the semantics of the usual arithmetic operations.

(added since revision 43)
I think it should be removed.  Or, any meaning for this sentence I didn't notice?
C11 and C++11 both have nothing like this around the usual arithmetic conversion rules...
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 25, 2014 06:10
\| \|
I don't think that text was meant to be part of a bullet point, but was meant to be a new paragraph after. I think the intent was to call out operations where the usual arithmetic conversions normally apply, but with slightly different semantics (the wording for;`?:` used to have something for that, IIRC). However, in a quick look through the C11 spec, I could not find any cases where the usual arithmetic conversions apply with different semantics, and so I've removed that text entirely.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Dec 26, 2014 11:58
\| \|
well, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 28, 2014 00:47
\| \|
Is that recommendation is also applicable for comparisons?;
Let's look into code:
uint8 a = 1;
uint8 b = 2;
if (a == b)
{
   \*/do something \*/
}
Do you think that in line if(a == b) INT02 is applicable? We compare the same types. I have met several indication about INT02 in similar cases and I am confused how to solve it. For me if((uint32) a == (uint32) b) looks strange, so may be you have better solution. 
best regards! 
![](images/icons/contenttypes/comment_16.png) Posted by filip.szymanski at Jun 21, 2019 05:27
\| \|
By the usual arithmetic conversions, a and b have the same type, so no conversion is necessary, and their comparison will produce the value you expect. (Both a and b will be promoted to int or unsigned int, but their types will still be identical).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 21, 2019 08:42
\| \|
One really insidious example we should call out:
    unsigned short x = 45000, y = 50000;unsigned int z = x * y;
The promotion will be to *signed* int, which then overflows and results in Undefined Behavior. This can come as a big surprise, since all of the variables' types are unsigned.
(Source: <https://cryptoservices.github.io/fde/2018/11/30/undefined-behavior.html>)
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 14:57
\| \|
When does case 5 in "Usual Arithmetic Conversions" apply? Thanks in advance.
![](images/icons/contenttypes/comment_16.png) Posted by hoda at Jul 08, 2020 11:58
\| \|
It applies when a signed type has greater rank than an unsigned type, but the signed type can't represent all of the values of the unsigned type. A concrete example is `signed long long int` and `unsigned long int` on a platform where those are both the same size (such as x86-64 Linux).
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 12:14
\| \|
In this case:
``` java
uint8_t a = 128;
int8_t ;b = -5;
if (a < b)
{
    printf("continue execution\n");
}
else
{
    printf("stop execution\n");
}
```
`a < b`  is a usual arithmetic conversion, so both would be promoted to int (I suppose whether it is int32_t or int64_t depends on the system kernel). So the result'd be `"stop execution"`. And the implicit type cast, like signed value converted to unsigned, wouldn't be occurred.
Is that correct?
Thanks,
![](images/icons/contenttypes/comment_16.png) Posted by yerin at Jan 27, 2023 04:29
\| \|
Yes, that is correct. The inequality operation will promote both types to int on any standards-compliant platform, since int must be at least 16 bits.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 27, 2023 12:40
\| \|
It seems that the contents are repeated from after the third Compliant Solution to before the last Noncompliant Code Example, since addition of "new NCCE/CS pair" in v. 152.
> unsigned short x = 45000, y = 50000;unsigned int z = x * (unsigned int)y;
>
> // Repeated contents start
>
> e C integer conversion rules define how C compilers handle conversions.
>
> // Repeated contents...
>
> uint8_t port = 0x5a;  
> uint8_t result_8 = (uint8_t) (~port) \>\> 4;
>
> // Repeated contents end
>
> Noncompliant Code Example  
>   
> In this example, a character is iterated from 0 to CHAR_MAX. However, on a platform where char is signed (such as 32-bit x86), max is set to 0x80 while i  increments from 0x79 to {{0xffffff80} (aka -127):

![](images/icons/contenttypes/comment_16.png) Posted by hkinoshita at Dec 02, 2024 03:07
\| \|
I've removed the redundant sections and code examples, thanks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 03, 2024 11:09
\| \|
nice. good job, kinoshita san!
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 07, 2024 02:17
\| \|
Thanks for your response.
Please remove the last paragraph before "Risk Assessment" as well. This is the same as the second paragraph on the page.
> e C integer conversion rules define how C compilers handle conversions. These rules include integer promotions, integer conversion rank, and the usual arithmetic conversions. The intent of the rules is to ensure that the conversions result in the same numerical values and that these values minimize surprises in the rest of the computation. Prestandard C usually preferred to preserve signedness of the type.

![](images/icons/contenttypes/comment_16.png) Posted by hkinoshita at Dec 09, 2024 03:15
\| \|
Fixed, thanks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 10, 2024 09:08
\|
