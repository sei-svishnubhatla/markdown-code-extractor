-   Page:
    [MSC30-C. Do not use the rand() function for generating pseudorandom numbers](/confluence/display/c/MSC30-C.+Do+not+use+the+rand%28%29+function+for+generating+pseudorandom+numbers)
-   Page:
    [MSC32-C. Properly seed pseudorandom number generators](/confluence/display/c/MSC32-C.+Properly+seed+pseudorandom+number+generators)
-   Page:
    [MSC33-C. Do not pass invalid data to the asctime() function](/confluence/display/c/MSC33-C.+Do+not+pass+invalid+data+to+the+asctime%28%29+function)
-   Page:
    [MSC37-C. Ensure that control never reaches the end of a non-void function](/confluence/display/c/MSC37-C.+Ensure+that+control+never+reaches+the+end+of+a+non-void+function)
-   Page:
    [MSC38-C. Do not treat a predefined identifier as an object if it might only be implemented as a macro](/confluence/display/c/MSC38-C.+Do+not+treat+a+predefined+identifier+as+an+object+if+it+might+only+be+implemented+as+a+macro)
-   Page:
    [MSC39-C. Do not call va_arg() on a va_list that has an indeterminate value](/confluence/display/c/MSC39-C.+Do+not+call+va_arg%28%29+on+a+va_list+that+has+an+indeterminate+value)
-   Page:
    [MSC40-C. Do not violate constraints](/confluence/display/c/MSC40-C.+Do+not+violate+constraints)
-   Page:
    [MSC41-C. Never hard code sensitive information](/confluence/display/c/MSC41-C.+Never+hard+code+sensitive+information)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [msc](https://confluence/label/seccode/msc) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC30-C | Medium | Unlikely | Low | P6 | L2 |
| MSC32-C | Medium | Likely | Low | P18 | L1 |
| MSC33-C | High | Likely | Low | P27 | L1 |
| MSC37-C | High | Unlikely | Low | P9 | L2 |
| MSC38-C | Low | Unlikely | Medium | P2 | L3 |
| MSC39-C | Low | Unlikely | Low | P3 | L3 |
| MSC40-C | Low | Unlikely | Medium | P2 | L3 |
| MSC41-C | High | Probable | Medium | P12 | L1 |

------------------------------------------------------------------------
[](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](../c/MSC30-C_%20Do%20not%20use%20the%20rand__%20function%20for%20generating%20pseudorandom%20numbers)
## Comments:

|  |
| ----|
| This feels like the right section to encourage use of compiler helpers such as GNU _attribute_() to add helpers or diagnostics to the code. For instance, writing your own variadic function die(const char *format, ...) can be tagged to have GCC check the params just like it would for the "native" printf.
Ref: http://www.unixwiz.net/techtips/gnu-c-attributes.html
                                        Posted by steve at Mar 14, 2008 11:01
                                     |
| We tend to advocate standard solutions here, as discussed in Scope.
Although we occasionally mention implementation-specific details, this particular one would be problematic because the C committee is debating whether to add some sort of attribute specification to the language, and if so, in what form.; If this document advocated the GCC-specific method and then the C committee chose a different one, the conflict could cause difficulties for people. 
                                        Posted by dmk at Mar 14, 2008 12:46
                                     |
| Would it be possible to have an entire section of the C secure coding standard dedicated to rules and recommendations for API design?; A lot of problems in C were created due to poorly designed API's and/or API's with missing functionality.
                                        Posted by gbeeley at Mar 17, 2008 17:09
                                     |
| Sure, anything is possible.  Generally speaking we would create a new section for an area if we had a significantly sized cluster of rules in one area.
What other rules/recommendations would you like to see?
                                        Posted by rcs at Mar 17, 2008 21:37
                                     |
| Here are a few, I'm sure we could think of more...
I believe that rule MSC08-A here would fit (which is what actually brought the subject to mind), although I would include such things as:
"When designing a new function which copies or generates data, the function should take a parameter to specify the size constraints of the destination"
"When designing a new function which copies or generates data, the function should provide a clear indication when truncation has occurred due to inadequate space in the destination"
I believe the rule MEM00-A would also fit, from the perspective of designing the API so that memory is allocated and free'd at the same level of abstraction.
Also, rule MEM01-A may imply designing API's which automatically set pointers to NULL on a free() operation, by taking a pointer to the pointer for the free() function's parameter.
                                        Posted by gbeeley at Mar 18, 2008 05:03
                                     |
| Many standards for safety and security critical standards also strongly recommend that the McCabe cyclomatic complexity of functions by limited to less than or equal to 10 (I believe both the DO-178B and NIST SP 500-235 standards recommend this value). Limiting functions to this makes the code easier to evaluate and test (although not easier to code).
                                        Posted by eric.decker@itt.com at Nov 24, 2009 19:30
                                     |
| While simpler, smaller functions are universally recognized as easier to build & maintain, they are not always possible. Many functions, especially for parsers and compilers, will contain long switch statements that really cannot easily be broken up into smaller functions. There is a good example of such a function in the Linux kernel that is described in this rule: MEM12-C. Consider using a Goto-Chain when leaving a function on error when using and releasing resources.  Furthermore, reducing function complexity addresses good software engineering, not security (although it is indirectly addressed, as vuls tend to hide better in complex code.)
I think for a rule addressing complexity to survive on this wiki it has to be:
    rigorous
    easily defensible
    universally agreed-upon
The first two are easy, but I suspect you'll have a hard time getting everyone to agree where to draw the line.
                                        Posted by svoboda at Nov 25, 2009 09:53
                                     |
| Only for completeness: Please add MSC41-C also in table; "Risk Assessment Summary"
                                        Posted by volker.erben at Nov 29, 2018 08:17
                                     |

