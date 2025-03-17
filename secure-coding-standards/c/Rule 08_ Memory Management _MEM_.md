-   Page:
    [MEM30-C. Do not access freed memory](/confluence/display/c/MEM30-C.+Do+not+access+freed+memory)
-   Page:
    [MEM31-C. Free dynamically allocated memory when no longer needed](/confluence/display/c/MEM31-C.+Free+dynamically+allocated+memory+when+no+longer+needed)
-   Page:
    [MEM33-C. Allocate and copy structures containing a flexible array member dynamically](/confluence/display/c/MEM33-C.++Allocate+and+copy+structures+containing+a+flexible+array+member+dynamically)
-   Page:
    [MEM34-C. Only free memory allocated dynamically](/confluence/display/c/MEM34-C.+Only+free+memory+allocated+dynamically)
-   Page:
    [MEM35-C. Allocate sufficient memory for an object](/confluence/display/c/MEM35-C.+Allocate+sufficient+memory+for+an+object)
-   Page:
    [MEM36-C. Do not modify the alignment of objects by calling realloc()](../c/MEM36-C_%20Do%20not%20modify%20the%20alignment%20of%20objects%20by%20calling%20realloc__)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [mem](https://confluence/label/seccode/mem) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM30-C | High | Likely | Medium | P18 | L1 |
| MEM31-C | Medium | Probable | Medium | P8 | L2 |
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
[](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152153)
## Comments:

|  |
| ----|
| 
I think we should add a recommendation here concerning clearing sensitive information (such as passwords) stored in dynamic memory before calling free() because the memory can be recycled leading to an unintentional disclosure.  Also, it may not be possible to call realloc() on dynamic memory containing senstive information because realloc may allocate storage elsewhere and copy the sensitive data but not clear the original memory which is then also recycled.  
This recommendation should also reference:
http://samate.nist.gov/docs/SAMATE_source_code_analysis_tool_spec_09_15_06.pdf
However, the rule as recorded there only references realloc() and as a result is incomplete/misleading.
                                        Posted by rcs at Jan 06, 2007 09:25
                                     |
| For some reason, my copy of Adobe's reader refuses to open that PDF.; The solution seems pretty clear to me: don't call realloc, just malloc/calloc/whatever, copy the data yourself, and clear the original.
On the other claw, if we start down the road of "how to protect sensitive data", there will probably need to be LOTS of additions to this site.
                                        Posted by davearonson at Jan 10, 2008 15:57
                                     |
| Dave,  That was old comment (from last year around this time).  I believe MEM03-A was added to address this concern.
                                        Posted by rcs at Jan 12, 2008 12:40
                                     |
| I think we should go through some of the rules and recommendations in this section and talk about how they can be mitigated through the use of tools such as valgrind and purify, possibly others.
                                        Posted by rcs at Feb 23, 2008 11:53
                                     |
| Most programmer's tend to use malloc/free for variable length arrays within functions. This is a bit of an overkill and typically leads to memory leaks and what not. Either use alloca or the GCC extension for the variable array initializers.This goes something like this:
void
foo(uint32_t nelements)
{
uint32_t array[nelements];
...
}
Internally this uses alloca and is pretty safe and you have no memory leaks whatsoever. I do have to say that usage of this is when you know that the nelements is not controlled by someone outside the program. This obviously can lead to a stack overflow if the attacker controls this. It's a trade off, nevertheless.
                                        Posted by k0wsik at Mar 14, 2008 01:57
                                     |
| There probably needs to be a recommendation on how to deal with security models (such as mandatory access controls) with regards memory management. I would suggest extending the recommendation of not writing sensitive data to disk (MEM06-A) to the more general recommendation of using the appropriate set of security methods for sensitive data, where pagelocking (to prevent swapping to disk) and other methods of keeping the data in memory are the core security methods that apply to all sensitive data. Other methods - such as not allocating from shared memory, using system-supplied access controls, etc - would then be extensions to this according to some specified criteria.
I'm also going to suggest a recommendation on transparency. Do programmers/maintainers really need to know if the memory is allocated by the system or the application? Whether it is truly dynamic, from a pre-allocated pool, or contained within a wholly static object? Where programmers do not need to know how or where memory is obtained, merely that it is and that it's the correct size, then the existing requirements and recommendations can be largely enforced and the variability be made safe by prohibiting the direct use of system memory management functions except within an abstraction layer.
                                        Posted by jcday at Mar 14, 2008 21:58
                                     |
| I looked over the site and couldn't find one, but I think there should be a rule or recommendation:; Do not store direct pointers to elements of a dynamic array (or string) that is subject to resizing via the realloc() function.  Use offsets/indices instead.  If the array is reallocated, it might be moved to a different location in memory, invalidating those pointers and causing program unreliability (some things might continue to coincidentally work until the original memory block is reused).
This can become especially tricky when a dynamic array of structures is involved (as opposed to a dynamic array of pointers to structures).
                                        Posted by gbeeley at Mar 18, 2008 04:05
                                     |
| There is actually a recommendation above, MEM05-A, which advises against the use of large stack allocations and mentions that alloca() should be avoided.; I concur with the recommendation against large stack allocations, though I have not reviewed the reference on alloca() (but I don't use it myself).  As far as I can tell, these recommendations do avoid dependencies on gcc extensions.
                                        Posted by gbeeley at Mar 18, 2008 04:17
                                     |
| realloc was created to handle large allocations, where unnecessary copying takes too much time and also where there might not be room for a copy.
As to clearing data before realloc/free, we don't clear data on the stack when returning from a function.; Generally neither is a problem unless there is a bug in the code.
                                        Posted by dagwyn at Apr 16, 2008 21:52
                                     |
| Never use alloca.; (See my comments in the Gnu source for alloca.)  Under C99, you can use VLAs.  Cince they require a FIFO lifetime model, neither is as general as dynamic allocation.
                                        Posted by dagwyn at Apr 16, 2008 21:54
                                     |

