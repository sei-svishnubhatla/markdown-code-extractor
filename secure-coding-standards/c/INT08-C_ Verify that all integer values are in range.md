Integer operations must result in an integer value within the range of the integer type (that is, the resulting value is the same as the result produced by unlimited-range integers). Frequently, the range is more restrictive depending on the use of the integer value, for example, as an index. Integer values can be verified by code review or by [static analysis](http://BB.%20Definitions#static%20analysis).
Integer overflow is [undefined behavior](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions), so a compiled program can do anything, including go off to play the Game of Life. Furthermore, a compiler may perform optimizations that assume an overflow will never occur, which can easily yield unexpected results. Compilers can optimize away `if` statements that check whether an overflow occurred. See [MSC15-C. Do not depend on undefined behavior](MSC15-C_%20Do%20not%20depend%20on%20undefined%20behavior) for an example.
Verifiably in-range operations are often preferable to treating out-of-range values as an error condition because the handling of these errors has been repeatedly shown to cause [denial-of-service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) problems in actual applications. The quintessential example is the failure of the Ariane 5 launcher, which occurred because of an improperly handled conversion error that resulted in the processor being shut down \[[Lions 1996](AA.-Bibliography_87152170.html#AA.Bibliography-Lions96)\].
A program that detects an integer overflow to be imminent may do one of two things: (1) signal some sort of error condition or (2) produce an integer result that is within the range of representable integers on that system. Some situations can be handled by an error condition, where an overflow causes a change in control flow (such as the system complaining about bad input and requesting alternative input from the user). Others are better handled by the latter option because it allows the computation to proceed and generate an integer result, thereby avoiding a denial-of-service attack. However, when continuing to produce an integer result in the face of overflow, the question of what integer result to return to the user must be considered.
The saturation and modwrap algorithms and the technique of restricted range usage, defined in the following subsections, produce integer results that are always within a defined range. This range is between the integer values `MIN` and `MAX` (inclusive), where `MIN` and `MAX` are two representable integers with `MIN < MAX`.
## Saturation Semantics
For saturation semantics, assume that the mathematical result of the computation is `result`. The value actually returned to the user is set out in the following table:

| Range of Mathematical Result | Result Returned |
| ----|----|
| MAX < result | MAX |
| MIN <= result <= MAX | result |
| result < MIN | MIN |

## Modwrap Semantics
In modwrap semantics (also called *modulo* arithmetic), integer values "wrap round." That is, adding 1 to `MAX` produces `MIN`. This is the defined behavior for unsigned integers in the C Standard, subclause 6.2.5, paragraph 9. It is frequently the behavior of signed integers, as well. However, it is more sensible in many applications to use saturation semantics instead of modwrap semantics. For example, in the computation of a size (using unsigned integers), it is often better for the size to stay at the maximum value in the event of overflow rather than to suddenly become a very small value.
## Restricted Range Usage
Another technique for avoiding integer overflow is to use only half the range of signed integers. For example, when using an `int`, use only the range \[`INT_MIN/2`, `INT_MAX/2`\]. This practice has been a trick of the trade in Fortran for some time, and now that optimizing C compilers are more sophisticated, it can be valuable in C.
Consider subtraction. If the user types the expression `a - b`, where both `a` and `b` are in the range `[INT_MIN/2, INT_MAX/2]`, the result will be in the range `(INT_MIN, INT_MAX]` for a typical two's complement machine.
Now, if the user types `a < b`, an implicit subtraction often occurs. On a machine without condition codes, the compiler may simply issue a subtract instruction and check whether the result is negative. This behavior is allowed because the compiler is allowed to assume there is no overflow. If all explicitly user-generated values are kept in the range `[INT_MIN/2, INT_MAX/2]`, then comparisons will always work even if the compiler performs this optimization on such hardware.
## Noncompliant Code Example
In this noncompliant example, `i + 1` will overflow on a 16-bit machine. The C Standard allows signed integers to overflow and produce incorrect results. Compilers can take advantage of this to produce faster code by assuming an overflow will not occur. As a result, the `if` statement that is intended to catch an overflow might be optimized away.
``` c
int i = /* Expression that evaluates to the value 32767 */;
/* ... */
if (i + 1 <= i) {
  /* Handle overflow */
}
/* Expression involving i + 1 */
```
## Compliant Solution
Using a `long` instead of an `int` is guaranteed to accommodate the computed value:
``` c
long i = /* Expression that evaluates to the value 32767 */;
/* ... */
/* No test is necessary; i is known not to overflow */
/* Expression involving i + 1 */
```
## Risk Assessment
Out-of-range integer values can result in reading from or writing to arbitrary memory locations and the execution of arbitrary code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT08-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | integer-overflow | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT08 |  |
| CodeSonar | 8.3p0 | ALLOC.SIZE.ADDOFLOWALLOC.SIZE.IOFLOWALLOC.SIZE.MULOFLOWALLOC.SIZE.SUBUFLOWMISC.MEM.SIZE.ADDOFLOWMISC.MEM.SIZE.BADMISC.MEM.SIZE.MULOFLOWMISC.MEM.SIZE.SUBUFLOW | Addition Overflow of Allocation SizeInteger Overflow of Allocation SizeMultiplication Overflow of Allocation SizeSubtraction Underflow of Allocation SizeAddition Overflow of SizeUnreasonable Size ArgumentMultiplication Overflow of SizeSubtraction Underflow of Size |
| Compass/ROSE |  |  | Could detect violations of this recommendation by flagging any comparison expression involving addition that could potentially overflow.;For example, instead of comparing a + b < c (where b and c are compile-time constants) and b > c, the code should compare a < c - b. (This assumes a, b, c are unsigned ints. Usually b is small and c is an upper bound such as INT_MAX.) |
| Helix QAC | 2024.4 | C2800,; C2910DF2801, DF2802, DF2803, DF2911, DF2912, DF2913 |  |
| LDRA tool suite | 9.7.1 | 488 S, 493 S, 493 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT08-aCERT_C-INT08-b
CERT_C-INT08-c
CERT_C-INT08-d
 | Avoid data loss when converting between integer typesAvoid signed integer overflows
Avoid value change when converting between integer types
Avoid wraparounds when performing arithmetic integer operations |
| PC-lint Plus | 1.4 | 648, 650, 679, 680, 776,952, 2704 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT08-C | Checks for integer overflow or integer constant overflow (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT08-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT08-CPP. Verify that all integer values are in range |
| ISO/IEC TR 24772:2013 | Numeric Conversion Errors [FLC] |

## Bibliography

|  |
| ----|
| [Lions 1996] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152386) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152467)
## Comments:

|  |
| ----|
| Any good application will have an error recovery scheme, and it is much better to use that than to silently substitute *different values* and proceed with the computation.; Saturating arithmetic has uses, for example to avoid driving mechanical systems beyond hard limits, but it's not a substitute for detecting errors or malicious input and taking more appropriate measures.
                                        Posted by dagwyn at Apr 15, 2008 16:16
                                     |
| True, but this begs the question. The recovery scheme could divert control flow to an error recovery mechanism, or it could proceed with the calculation...which to do is a choice for the developer. I have (hopefully) made this more clear in the intro paragraphs.
Also added a bit of background and details on restricted range checking, from email from David Keaton.
                                        Posted by svoboda at May 19, 2008 15:34
                                     |
| Regarding ROSE algorithm, who's to say that b-c can't underflow?  Also, am I right to understand that we end up flagging just about every addition inside of a comparison? Seems silly...
                                        Posted by avolkovi at Jul 29, 2008 15:21
                                     |
| The pattern in the 'a + b < c' comparison is that a and b are the same type (or are promoted to the same type), and c > b. Ideally c is the maximal value of its type, at the very least b is known at compile time, and c > b.
The general case may be unenforceable, but there are lots of enforceable sub-cases. The NCCE for example is: a + b < a, where b > 0. That is automatically a violation, since it presumes modular behavior.
                                        Posted by svoboda at Jul 29, 2008 17:28
                                     |
| This rule is still rose-possible, although a checker for INT30-C will pretty much catch all violations of this rule.
                                        Posted by svoboda at Aug 06, 2008 15:22
                                     |
| this sentence doesn't make sense to me:
"eg instead of comparing 'a + b < c', where b and c are compile-time constants and b > c, the code should compare 'a < c - b'."
                                        Posted by masaki at May 05, 2009 01:26
                                     |
| Added some background assumptions to the paragraph. The idea is you generally don't know if a+b might overflow but you can guarantee that c-b won't underflow, so you do that subtraction instead of the addition.
                                        Posted by svoboda at May 06, 2009 09:25
                                     |
| The 2nd paragraph of "Restricted Range Usage",
(INT_MIN, INT_MAX] should be corrected to [INT_MIN, INT_MAX]? I think INT_MIN is inclusive.
                                        Posted by masaki at May 12, 2009 01:10
                                     |
| No, I think this is right.  For example, take the 8-bit case.  -128 / 2 = -64  127 / 2 = 63 r 1
The restricted range is [-64, 63]  -64 - 63 = -127 which is exclusive of -128.
                                        Posted by rcs_mgr at May 12, 2009 02:55
                                     |
| Good point!
                                        Posted by masaki at May 15, 2009 04:05
                                     |
| "Now, if the user types a < b, there is often an implicit subtraction happening. On a machine without condition codes, the compiler may simply issue a subtract instruction and check whether the result is negative. This is allowed, because the compiler is allowed to assume there is no overflow. If all explicitly user-generated values are kept in the range INT_MIN/2, INT_MAX/2, then comparisons will always work even if the compiler performs this optimization on such hardware."
Is this really claiming that a compiler can legally convert a<b to (a-b)<0 (assuming a and b are ints)? If so, then 0<INT_MIN would fail if the machine uses two's complement arithmetic and modwrap semantics, as 0-INT_MIN would evaluate to INT_MIN (-INT_MIN == INT_MIN on such a machine). Besides, if one were following this (useful) idea of using half the int range, intermediate expressions would still fall outside this half range, and if one of them were compared with another, a compiler performing the above (broken) rewriting would break such code.
                                        Posted by sgreen at Aug 25, 2009 00:18
                                     |
| From Tim Wilson:
This is not how comparisons work. The statement a < b is translated into something like the following assembly code:
cmp   %eax, %ebx
jl    .less_label

A jl (jump if less) instruction does not jump simply when the sign flow has been set indicating the subtraction produced a result less than 0.
Instead, a jl instruction jumps when the sign flag does not equal the overflow flag. In normal cases when there is no overflow, the sign flag does indicate whether a is less than b. When there is overflow, the opposite of the sign flag indicates whether a is less than b.
The compiler is completely justified in converting a \< b into (a - b) \< 0 because such a conversion is always correct.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 29, 2009 21:04
\| \|
The situation you cite only works on machines that have condition codes. For example, the Cray-2 had no condition codes, and the compiler took advantage of the standard's allowed assumption of no overflow, saving four instructions per comparison by testing (a - b) \< 0 instead of a \< b. Therefore, the comparison a \< b sometimes got the wrong result, and this was allowed by the standard.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Sep 08, 2009 14:40
\| \|
Consider adding the following example (which I find non-trivial).
The example is similar to the first noncompliant code here: [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](INT01-C_%20Use%20rsize_t%20or%20size_t%20for%20all%20integer%20values%20representing%20the%20size%20of%20an%20object), but for the `char` case.;
\`\`\`c  
unsigned char max = CHAR_MAX + 1;
int main()  
{  
signed char i = 0;  
for (i = 0 ; i \< max ; ++i)  
{  
    printf("i=0x%08x max=0x%08x\n", i, max);  
}  
return 0;  
}  
\`\`\`
The above code defines max as 128.
Because of the comparision, both i, max  are promoted to signed int  type, hence making a signed comparision (unlike the int  case). 
This leads to an infinite loop. 
Note that in case the types were \`unsigned int, int\`, the loop would terminate - as no promotion would be taking place, hence making an unsigned comparision. 
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Jan 16, 2023 11:02
\| \|
Itay:
Thanks for the code example. ;The code is subtle because it compares signed chars with unsigned chars. You could make it even more subtle by using plain char (which is signed on x86).
The code example could be added to several recommendations, and perhaps a few rules. We prefer adding to rules because the rules are more precise and enforceable. Perhaps STR34-C?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 17, 2023 09:03
\| \|
Yup, I think it can match to STR34-C (as explicit casting does fix this issue).
However, we should state that a better coding fix would be comparing objects of the same type, meaning the correct solution for this case would be declaring `i`; as some `unsigned`  type (whether a `char`  or an `int` ). 
I suggest we add this to [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules). What do you think?
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Jan 17, 2023 12:48
\| \|
Agreed. I added your code example to that recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 17, 2023 13:23
\|
