-   Page:
    [EXP30-C. Do not depend on the order of evaluation for side effects](/confluence/display/c/EXP30-C.+Do+not+depend+on+the+order+of+evaluation+for+side+effects)
-   Page:
    [EXP32-C. Do not access a volatile object through a nonvolatile reference](/confluence/display/c/EXP32-C.+Do+not+access+a+volatile+object+through+a+nonvolatile+reference)
-   Page:
    [EXP33-C. Do not read uninitialized memory](/confluence/display/c/EXP33-C.+Do+not+read+uninitialized+memory)
-   Page:
    [EXP34-C. Do not dereference null pointers](/confluence/display/c/EXP34-C.+Do+not+dereference+null+pointers)
-   Page:
    [EXP35-C. Do not modify objects with temporary lifetime](/confluence/display/c/EXP35-C.+Do+not+modify+objects+with+temporary+lifetime)
-   Page:
    [EXP36-C. Do not cast pointers into more strictly aligned pointer types](/confluence/display/c/EXP36-C.+Do+not+cast+pointers+into+more+strictly+aligned+pointer+types)
-   Page:
    [EXP37-C. Call functions with the correct number and type of arguments](/confluence/display/c/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments)
-   Page:
    [EXP39-C. Do not access a variable through a pointer of an incompatible type](/confluence/display/c/EXP39-C.+Do+not+access+a+variable+through+a+pointer+of+an+incompatible+type)
-   Page:
    [EXP40-C. Do not modify constant objects](/confluence/display/c/EXP40-C.+Do+not+modify+constant+objects)
-   Page:
    [EXP42-C. Do not compare padding data](/confluence/display/c/EXP42-C.+Do+not+compare+padding+data)
-   Page:
    [EXP43-C. Avoid undefined behavior when using restrict-qualified pointers](/confluence/display/c/EXP43-C.+Avoid+undefined+behavior+when+using+restrict-qualified+pointers)
-   Page:
    [EXP44-C. Do not rely on side effects in operands to sizeof, \_Alignof, or \_Generic](/confluence/display/c/EXP44-C.+Do+not+rely+on+side+effects+in+operands+to+sizeof%2C+_Alignof%2C+or+_Generic)
-   Page:
    [EXP45-C. Do not perform assignments in selection statements](/confluence/display/c/EXP45-C.+Do+not+perform+assignments+in+selection+statements)
-   Page:
    [EXP46-C. Do not use a bitwise operator with a Boolean-like operand](/confluence/display/c/EXP46-C.+Do+not+use+a+bitwise+operator+with+a+Boolean-like+operand)
-   Page:
    [EXP47-C. Do not call va_arg with an argument of the incorrect type](/confluence/display/c/EXP47-C.+Do+not+call+va_arg+with+an+argument+of+the+incorrect+type)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [exp](https://confluence/label/seccode/exp) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP30-C | Medium | Probable | Medium | P8 | L2 |
| EXP32-C | Low | Likely | Medium | P6 | L2 |
| EXP33-C | High | Probable | Medium | P12 | L1 |
| EXP34-C | High | Likely | Medium | P18 | L1 |
| EXP35-C | Low | Probable | Medium |  P4  |  L3  |
| EXP36-C | Low | Probable | Medium | P4 | L3 |
| EXP37-C | Medium | Probable | High | P4 | L3 |
| EXP39-C | Medium | Unlikely | High |  P2  |   L3  |
| EXP40-C | Low | Unlikely | Medium | P2 | L3 |
| EXP42-C | Medium | Probable | Medium | P8 | L2 |
| EXP43-C | Medium | Probable | High | P4 | L3 |
| EXP44-C | Low | Unlikely | Low | P3 | L3 |
| EXP45-C | Low | Likely | Medium | P6 | L2 |
| EXP46-C | Low | Likely | Low | P9 | L2 |
| EXP47-C | Medium | Likely | High | P6 | L2 |

## Related Rules and Recommendations

|  |
| ----|
| FLP01-C. Take care in rearranging floating-point expressions |
| FLP01-C. Take care in rearranging floating-point expressions |
| FLP01-C. Take care in rearranging floating-point expressions |
| PRE01-C. Use parentheses within macros around parameter names |
| PRE01-C. Use parentheses within macros around parameter names |
| PRE01-C. Use parentheses within macros around parameter names |
| PRE02-C. Macro replacement lists should be parenthesized |
| PRE02-C. Macro replacement lists should be parenthesized |
| PRE02-C. Macro replacement lists should be parenthesized |

------------------------------------------------------------------------
[](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152202)
## Comments:

|  |
| ----|
| The risk assesment summary is not up to date with the introduced rules and recommendations
                                        Posted by oliver.holzkamp at Aug 01, 2014 04:49
                                     |

