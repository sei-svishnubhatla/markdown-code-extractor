> [!info]  
>
> This section is under construction.

This appendix contains guidelines for functions that are defined as part of the Microsoft Windows API \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/hh447209(v=vs.85).aspx)\] and the Microsoft Visual C++ compiler \[[MSDN](http://msdn.microsoft.com/en-us/library/vstudio/60k1461a.aspx)\]. These rules and recommendations are not part of the core standard because they do not apply in all C language applications. The intent of providing these guidelines is to demonstrate how rules and recommendations for other standards or specific [BB. Definitions#implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) may be integrated with the core C recommendations.
-   Page:
    [WIN00-C. Be specific when dynamically loading libraries](/confluence/display/c/WIN00-C.+Be+specific+when+dynamically+loading+libraries)
-   Page:
    [WIN01-C. Do not forcibly terminate execution](/confluence/display/c/WIN01-C.+Do+not+forcibly+terminate+execution)
-   Page:
    [WIN02-C. Restrict privileges when spawning child processes](/confluence/display/c/WIN02-C.+Restrict+privileges+when+spawning+child+processes)
-   Page:
    [WIN03-C. Understand HANDLE inheritance](/confluence/display/c/WIN03-C.+Understand+HANDLE+inheritance)
-   Page:
    [WIN04-C. Consider encrypting function pointers](/confluence/display/c/WIN04-C.+Consider+encrypting+function+pointers)
> [!info]  
>
> **Information for Editors** In order to have a new guideline automatically listed above be sure to label it [win](https://confluence/label/seccode/win) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN00-C | High | Unlikely | Low | P9 | L2 |
| WIN01-C | High | Likely | High | P9 | L2 |
| WIN02-C | High | Likely | High | P9 | L2 |
| WIN03-C | High | Unlikely | Low | P9 | L2 |
| WIN04-C | High | Unlikely | Low | P9 | L2 |

## Related Rules and Recommendations

|  |
| ----|
| Rec. 51. Microsoft Windows (WIN) |
| Rec. 51. Microsoft Windows (WIN) |
| Rec. 51. Microsoft Windows (WIN) |
| Rule 51. Microsoft Windows (WIN) |
| Rule 51. Microsoft Windows (WIN) |
| Rule 51. Microsoft Windows (WIN) |
| WIN00-C. Be specific when dynamically loading libraries |
| WIN00-C. Be specific when dynamically loading libraries |
| WIN00-C. Be specific when dynamically loading libraries |
| WIN01-C. Do not forcibly terminate execution |
| WIN01-C. Do not forcibly terminate execution |
| WIN01-C. Do not forcibly terminate execution |
| WIN02-C. Restrict privileges when spawning child processes |
| WIN02-C. Restrict privileges when spawning child processes |
| WIN02-C. Restrict privileges when spawning child processes |
| WIN03-C. Understand HANDLE inheritance |
| WIN03-C. Understand HANDLE inheritance |
| WIN03-C. Understand HANDLE inheritance |
| WIN04-C. Consider encrypting function pointers |
| WIN04-C. Consider encrypting function pointers |
| WIN04-C. Consider encrypting function pointers |
| WIN30-C. Properly pair allocation and deallocation functions |
| WIN30-C. Properly pair allocation and deallocation functions |
| WIN30-C. Properly pair allocation and deallocation functions |

------------------------------------------------------------------------
[](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152030)
