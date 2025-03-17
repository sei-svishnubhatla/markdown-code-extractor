-   Page:
    [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](/confluence/display/c/ARR30-C.+Do+not+form+or+use+out-of-bounds+pointers+or+array+subscripts)
-   Page:
    [ARR32-C. Ensure size arguments for variable length arrays are in a valid range](/confluence/display/c/ARR32-C.+Ensure+size+arguments+for+variable+length+arrays+are+in+a+valid+range)
-   Page:
    [ARR36-C. Do not subtract or compare two pointers that do not refer to the same array](/confluence/display/c/ARR36-C.+Do+not+subtract+or+compare+two+pointers+that+do+not+refer+to+the+same+array)
-   Page:
    [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](/confluence/display/c/ARR37-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+to+a+non-array+object)
-   Page:
    [ARR38-C. Guarantee that library functions do not form invalid pointers](/confluence/display/c/ARR38-C.+Guarantee+that+library+functions+do+not+form+invalid+pointers)
-   Page:
    [ARR39-C. Do not add or subtract a scaled integer to a pointer](/confluence/display/c/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [arr](https://confluence/label/seccode/arr) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR30-C | High | Likely | High | P9 | L2 |
| ARR32-C | High | Probable | High | P6 | L2 |
| ARR36-C | Medium | Probable | Medium | P8 | L2 |
| ARR37-C | Medium | Probable | Medium | P8 | L2 |
| ARR38-C | High | Likely | Medium | P18 | L1 |
| ARR39-C | High | Probable | High | P6 | L2 |

## Related Rules and Recommendations

|  |
| ----|
| MEM33-C.  Allocate and copy structures containing a flexible array member dynamically |
| MEM33-C.  Allocate and copy structures containing a flexible array member dynamically |
| MEM33-C.  Allocate and copy structures containing a flexible array member dynamically |
| STR11-C. Do not specify the bound of a character array initialized with a string literal |
| STR11-C. Do not specify the bound of a character array initialized with a string literal |
| STR11-C. Do not specify the bound of a character array initialized with a string literal |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| VOID ARR31-CPP. Use consistent array notation across all source files |
| VOID CTR00-CPP. Understand when to prefer vectors over arrays |
| VOID CTR01-CPP. Do not apply the sizeof operator to a pointer when taking the size of an array |
| VOID CTR02-CPP. Explicitly specify array bounds, even if implicitly defined by an initializer |
| VOID CTR35-CPP. Do not allow loops to iterate beyond the end of an array or container |
| VOID CTR37-CPP. Do not add or subtract an integer to a pointer to a non-array object |
| VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array |
| VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array |
| VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array |

------------------------------------------------------------------------
[](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152322)
## Comments:

|  |
| ----|
| When I use GCC version 4.1 to compile a program with a variable declared to have an incomplete type (i.e., int[]), I get a compile time error unless the variable is initialized in the same statement.
What compilers accept this type of declaration and is it part of the standard?
                                        Posted by adahmad at Apr 12, 2008 19:56
                                     |

