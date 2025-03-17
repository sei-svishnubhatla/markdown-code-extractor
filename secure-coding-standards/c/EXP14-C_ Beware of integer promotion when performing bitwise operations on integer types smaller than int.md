> [!warning]  
>
> This guideline has been deprecated by
>
> -   [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules)

Integer types smaller than `int` are promoted when an operation is performed on them. If all values of the original type can be represented as an `int`, the value of the smaller type is converted to an `int`; otherwise, it is converted to an `unsigned int` (see [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules)). If the conversion is to a wider type, the original value is zero-extended for unsigned values or sign-extended for signed types. Consequently, bitwise operations on integer types smaller than `int` may have unexpected results.
## Noncompliant Code Example
This noncompliant code example demonstrates how performing bitwise operations on integer types smaller than `int` may have unexpected results.
``` c
uint8_t port = 0x5a;
uint8_t result_8 = ( ~port ) >> 4;
```
In this example, a bitwise complement of `port` is first computed and then shifted 4 bits to the right. If both of these operations are performed on an 8-bit unsigned integer, then `result_8` will have the value `0x0a`. However, `port` is first promoted to a `signed int`, with the following results (on a typical architecture where type `int` is 32 bits wide):

| Expression | Type | Value | Notes |
| ----|----|----|----|
| port | uint8_t | 0x5a |  |
| ~port | int | 0xffffffa5 |  |
| ~port >> 4 | int | 0x0ffffffa | Whether or not value is negative is implementation-defined. |
| result_8 | uint8_t | 0xfa |  |

## Compliant Solution
In this compliant solution, the bitwise complement of `port` is converted back to 8 bits. Consequently, `result_8` is assigned the expected value of `0x0aU`.
``` c
uint8_t port = 0x5a;
uint8_t result_8 = (uint8_t) (~port) >> 4;
```
## Risk Assessment
Bitwise operations on shorts and chars can produce incorrect data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP14-C | low | likely | high | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP14 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.CAST.RIP | Risky integer promotion |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.EXP14 | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP14-a | Avoid mixing arithmetic of different precisions in the same expression |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP14-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP15-CPP. Beware of integer promotion when performing bitwise operations on chars or shorts |
| MISRA-C | Rule 10.5 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152264) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](../c/EXP15-C_%20Do%20not%20place%20a%20semicolon%20on%20the%20same%20line%20as%20an%20if,%20for,%20or%20while%20statement)
## Comments:

|  |
| ----|
| Since this is a C guideline, the compliant example should be changed to:
uint8_t result_8 = (uint8_t) (~port) >> 4;

![](images/icons/contenttypes/comment_16.png) Posted by jtg at Nov 24, 2010 20:06
\| \|
Thanks, I fixed this problem and also tried to make this a little more precise.
I'm giving some thought as to if this should be a separate guideline, or if it should be eliminated and the example integrated with [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 25, 2010 12:25
\| \|
This has now been cleaned up (a bunch). If this is going to remain an "informational" recommendation then I would combine it with INT02-C.
If we keep it as a separate guideline it should be strengthened to "Do not perform bitwise operations on integer types smaller than int" and doing so should be diagnosed.
Of course, this is not right either because the compliant solution still violates this. At the end of the day, I think this guideline is just going to say "understand integer promotions/conversion rules" and consequently should be combined.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 29, 2010 05:36
\| \|
Since this is a subset of [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules) merging the two makes sense to me.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Nov 29, 2010 23:37
\| \|
I agree with combining them. I actually think the example given here was more of a gotcha due to the use of '~' in particular, and not really related to bitwise operations in general.
![](images/icons/contenttypes/comment_16.png) Posted by jtg at Dec 07, 2010 15:40
\| \|
I've merged this guideline with [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules) and marked it as deprecated.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Dec 08, 2010 12:31
\| \|
gcc 4.8.4 warns about `1u << 63ul` (assuming 64-bits long and 32-bits int) and computes;`0`. Rightfully so? No promotion from `1u` to `1ul`.
ISO/IEC 9899:201x, 6.3.1.8 (Usual arithmetic conversions): "Many operators that expect operands of arithmetic type cause conversions"; 6.5.7 (Bitwise shift operators): "The integer promotions are performed on each of the operands...". But I am not able conclude from that.
![](images/icons/contenttypes/comment_16.png) Posted by loic.etienne at Mar 14, 2017 09:11
\|
