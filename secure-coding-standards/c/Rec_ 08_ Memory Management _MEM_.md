-   Page:
    [MEM00-C. Allocate and free memory in the same module, at the same level of abstraction](/confluence/display/c/MEM00-C.+Allocate+and+free+memory+in+the+same+module%2C+at+the+same+level+of+abstraction)
-   Page:
    [MEM01-C. Store a new value in pointers immediately after free()](../c/MEM01-C_%20Store%20a%20new%20value%20in%20pointers%20immediately%20after%20free__)
-   Page:
    [MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](/confluence/display/c/MEM02-C.+Immediately+cast+the+result+of+a+memory+allocation+function+call+into+a+pointer+to+the+allocated+type)
-   Page:
    [MEM03-C. Clear sensitive information stored in reusable resources](/confluence/display/c/MEM03-C.+Clear+sensitive+information+stored+in+reusable+resources)
-   Page:
    [MEM04-C. Beware of zero-length allocations](/confluence/display/c/MEM04-C.+Beware+of+zero-length+allocations)
-   Page:
    [MEM05-C. Avoid large stack allocations](/confluence/display/c/MEM05-C.+Avoid+large+stack+allocations)
-   Page:
    [MEM06-C. Ensure that sensitive data is not written out to disk](/confluence/display/c/MEM06-C.+Ensure+that+sensitive+data+is+not+written+out+to+disk)
-   Page:
    [MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap](/confluence/display/c/MEM07-C.+Ensure+that+the+arguments+to+calloc%28%29%2C+when+multiplied%2C+do+not+wrap)
-   Page:
    [MEM10-C. Define and use a pointer validation function](/confluence/display/c/MEM10-C.+Define+and+use+a+pointer+validation+function)
-   Page:
    [MEM11-C. Do not assume infinite heap space](/confluence/display/c/MEM11-C.+Do+not+assume+infinite+heap+space)
-   Page:
    [MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources](/confluence/display/c/MEM12-C.+Consider+using+a+goto+chain+when+leaving+a+function+on+error+when+using+and+releasing+resources)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [mem](https://confluence/label/seccode/mem) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM00-C | High | Probable | Medium | P12 | L1 |
| MEM01-C | High | Unlikely | Low | P9 | L2 |
| MEM02-C | Low | Unlikely | Low | P3 | L3 |
| MEM03-C | Medium | Unlikely | High | P2 | L3 |
| MEM04-C | Low | Likely | Medium | P6 | L2 |
| MEM05-C | Low | Likely | Medium | P6 | L2 |
| MEM06-C | Medium | Unlikely | High | P2 | L3 |
| MEM07-C | High | Unlikely | Medium | P6 | L2 |
| MEM10-C | High | Unlikely | High | P3 | L3 |
| MEM11-C | Low | Probable | High | P2 | L3 |
| MEM12-C | Low | Probable | Medium | P4 | L3 |
| MEM30-C | High | Likely | Medium | P18 | L1 |
| MEM31-C | High | Probable | Medium | P8 | L2 |
| MEM33-C | Low | Unlikely | Low | P3 | L3 |
| MEM34-C | High | Likely | Medium | P18 | L1 |
| MEM35-C | High | Probable | High | P6 | L2 |
| MEM36-C | Low | Probable | High | P2 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| EXP33-C. Do not read uninitialized memory |
| EXP33-C. Do not read uninitialized memory |
| EXP33-C. Do not read uninitialized memory |
| EXP34-C. Do not dereference null pointers |
| EXP34-C. Do not dereference null pointers |
| EXP34-C. Do not dereference null pointers |
| INT01-C. Use rsize_t or size_t for all integer values representing the size of an object |
| INT01-C. Use rsize_t or size_t for all integer values representing the size of an object |
| INT01-C. Use rsize_t or size_t for all integer values representing the size of an object |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| VOID EXP01-C. Do not take the size of a pointer to determine the size of the pointed-to type |
| VOID EXP01-C. Do not take the size of a pointer to determine the size of the pointed-to type |
| VOID EXP01-C. Do not take the size of a pointer to determine the size of the pointed-to type |

------------------------------------------------------------------------
[](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](../c/MEM00-C_%20Allocate%20and%20free%20memory%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction)
