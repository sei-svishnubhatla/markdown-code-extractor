When two pointers are subtracted, both must point to elements of the same array object or just one past the last element of the array object (C Standard, 6.5.7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]); the result is the difference of the subscripts of the two array elements. Otherwise, the operation is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 45](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_45).)
Similarly, comparing pointers using the relational operators `<`, `<=`, `>=`, and `>` gives the positions of the pointers relative to each other. Subtracting or comparing pointers that do not refer to the same array is undefined behavior. (See [undefined behavior 45](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_45) and [undefined behavior 50](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_50).)
Comparing pointers using the equality operators `==` and `!=` has well-defined semantics regardless of whether or not either of the pointers is null, points into the same object, or points one past the last element of an array object or function.
## Noncompliant Code Example
In this noncompliant code example, pointer subtraction is used to determine how many free elements are left in the `nums` array:
``` c
#include <stddef.h>
enum { SIZE = 32 };
void func(void) {
  int nums[SIZE];
  int end;
  int *next_num_ptr = nums;
  size_t free_elements;
  /* Increment next_num_ptr as array fills */
  free_elements = &end - next_num_ptr;
}
```
This program incorrectly assumes that the `nums` array is adjacent to the `end` variable in memory. A compiler is permitted to insert padding bits between these two variables or even reorder them in memory.
## Compliant Solution
In this compliant solution, the number of free elements is computed by subtracting `next_num_ptr` from the address of the pointer past the `nums` array. While this pointer may not be dereferenced, it may be used in pointer arithmetic.
``` c
#include <stddef.h>
enum { SIZE = 32 };
void func(void) {
  int nums[SIZE];
  int *next_num_ptr = nums;
  size_t free_elements;
  /* Increment next_num_ptr as array fills */
  free_elements = &(nums[SIZE]) - next_num_ptr;
}
```
## Exceptions
**ARR36-C-EX1: **Comparing two pointers to distinct members of the same `struct` object is allowed. Pointers to structure members declared later in the structure compare greater-than pointers to members declared earlier in the structure.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR36-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-subtraction | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR36 | Can detect operations on pointers that are unrelated |
| CodeSonar | 8.3p0 | LANG.STRUCT.CUPLANG.STRUCT.SUP | Comparison of Unrelated PointersSubtraction of Unrelated Pointers |
| Coverity | 2017.07 | MISRA C 2004 17.2MISRA C 2004 17.3MISRA C 2012 18.2MISRA C 2012 18.3 | Implemented |
| Cppcheck | ;2.15 | comparePointers |  |
| Cppcheck Premium | 24.11.0 | comparePointers |  |
| Helix QAC | 2024.4 | C0487, C0513DF2668, DF2669, DF2761, DF2762, DF2763, DF2766, DF2767, DF2768, DF2771, DF2772, DF2773 |  |
| Klocwork | 2024.4 | MISRA.PTR.ARITH |  |
| LDRA tool suite | 9.7.1 | 437 S, 438 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR36-aCERT_C-ARR36-b
 | Do not subtract two pointers that do not address elements of the same arrayDo not compare two unrelated pointers |
| Polyspace Bug Finder | R2024a | CERT C: Rule ARR36-C | Checks for subtraction or comparison between pointers to different arrays (rule partially covered) |
| PVS-Studio | 7.35 | V736, V782 |  |
| RuleChecker | 24.04 | pointer-subtraction | Partially checked |
| TrustInSoft Analyzer | 1.38 | differing_blocks | Exhaustively verified (see the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR36-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | CTR54-CPP. Do not subtract iterators that do not refer to the same container | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Subtracting or comparing two pointers that do not refer to the same array [ptrobj] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-469, Use of Pointer Subtraction to Determine Size | 2017-07-10: CERT: Exact |
| CWE 3.11 | CWE-469, Use of Pointer Subtraction to Determine Size | 2018-10-18:CERT:CWE subset of rule |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-469 and ARR36-C
CWE-469 = Subset(ARR36-C)
ARR36-C = Union(CWE-469, list) where list =
-   Pointer comparisons using the relational operators `<`, `<=`, `>=`, and `>`, where the pointers do not refer to the same array
## Bibliography

|  |  |
| ----|----|
| [Banahan 2003] | Section 5.3, "Pointers"Section 5.7, "Expressions Involving Pointers" |
| [ISO/IEC 9899:2024] | 6.5.7, "Additive Operators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152385) [](../c/Rule%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152085)
## Attachments:
![](images/icons/bullet_blue.gif) [ARR36-C. Do not subtract or compare two pointers that do not refer to the same array.html](../87152341/) (text/html)  
## Comments:

|  |
| ----|
| Larry Jones says, via email:
> > So from what we can tell, it's OK to compare pointers to members within
> > the same struct, but not OK to subtract pointers in the same situation.
> > True or false?

True (unless they happen to be pointers to char, since the content of
the struct can be treated as an array of char).  Consider a struct with
an int member, a char member, and another int member, with no padding. 
If you subtract pointers to the two ints, the correct result would be
something like 1.25, which is nonsensical.
                                        Posted by svoboda at May 01, 2009 09:51
                                     |

