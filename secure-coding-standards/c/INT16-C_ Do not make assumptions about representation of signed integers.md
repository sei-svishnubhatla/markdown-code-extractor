Although many common implementations use a two's complement representation of signed integers, the C Standard declares such use as [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) and allows all of the following representations:
-   Sign and magnitude
-   Two's complement
-   One's complement
This is a specific example of [MSC14-C. Do not introduce unnecessary platform dependencies](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies).
## Noncompliant Code Example
One way to check whether a number is even or odd is to examine the least significant bit, but the results will be inconsistent. Specifically, this example gives unexpected behavior on all one's complement implementations:
``` c
int value;
if (scanf("%d", &value) == 1) {
  if (value & 0x1 != 0) {
    /* Take action if value is odd */
  }
}
```
## Compliant Solution
The same thing can be achieved compliantly using the modulo operator:
``` c
int value;
if (scanf("%d", &value) == 1) {
  if (value % 2 != 0) {
    /* Take action if value is odd */
  }
}
```
## Compliant Solution
Using bitwise operators is safe on unsigned integers:
``` c
unsigned int value;
if (scanf("%u", &value) == 1) {
  if (value & 0x1 != 0) {
    /* Take action if value is odd */
  }
}
```
## Risk Assessment
Incorrect assumptions about integer representation can lead to execution of unintended code branches and other unexpected behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT16-C | Medium | Unlikely | High |  P2  |  L3  |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | bitop-type | Partially checked |
| Helix QAC | 2024.4 | C2940, C2945;DF2941, DF2942, DF2943, DF2946, DF2947, DF2948 |  |
| LDRA tool suite | 9.7.1 | 50 S, 120 S | Partially Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT16-aCERT_C-INT16-b
 | Bitwise operators shall only be applied to operands of unsigned underlying type (with exceptions)Bitwise operators shall not use positive integer literals as operands |
| PC-lint Plus | 1.4 | 502, 2704, 9088 | Partially supported: reports bitwise not of signed quantity, declaration of named signed single-bit bitfields, and negation of the minimum negative integer |
| RuleChecker | 24.04 | bitop-type | Partially checked |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152366) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152319)
## Comments:

|  |
| ----|
| If you check subtraction under INT32-C. Ensure that operations on signed integers do not result in overflow you can find another example of a twos' complement solution.  
                                        Posted by rcs at Apr 01, 2009 20:28
                                     |
| I'd say this rule is now complete.
                                        Posted by svoboda at Apr 04, 2009 08:36
                                     |
| I'm beginning to suspect this rec is a variant of
INT14-C. Avoid performing bitwise and arithmetic operations on the same data
However, the NCCE doesn't violate INT14-C only because nothing else is done with the variable; it is merely input and then a bitwise operation is performed. Sort of a corner case not covered by INT14-C. So this rec is still valid on its own (outside INT14-C)
I do think this rec is unenforceable, however, because you can't infer that the programmer assumes 2s-complement whenever they perform a bitwise op.
                                        Posted by svoboda at Apr 08, 2009 14:17
                                     |
| If value is -3 then this result is wrong. This should be written as (value % 2;!= 0).
                                        Posted by naito@alife-lab.co.jp at Aug 02, 2011 05:27
                                     |
| Huh? When is value ever -3?
                                        Posted by svoboda at Aug 02, 2011 08:38
                                     |
| I think Yusuke is referring to INT10-C: Never assume the result of % is nonnegative.; If value (of type int) is -3, value % 2 could be -1.
                                        Posted by douglas ice at Sep 21, 2011 15:50
                                     |
| Agreed, I fixed the code as as suggested.
                                        Posted by svoboda at Sep 22, 2011 12:56
                                     |
| Both code samples violate;INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs.
                                        Posted by svoboda at Dec 16, 2013 15:56
                                     |
| To make it more obvious that this restriction is only for signed integers, we should add another compliant solution that still uses &, but changes value to be unsigned.
                                        Posted by jcsible at Jun 30, 2020 15:11
                                     |

