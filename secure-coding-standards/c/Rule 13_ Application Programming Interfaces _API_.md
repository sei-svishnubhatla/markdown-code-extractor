> [!info]  
>
> This section is under construction.

**Content by label**
There is no content with the specified labels
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [api](https://confluence/label/seccode/api) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|

------------------------------------------------------------------------
[](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](../c/Rule%2014_%20Concurrency%20_CON_)
## Comments:

|  |
| ----|
| The guidelines API05-C. Support compile-time checking and API06-C. Make failures obvious don't exist. Should they be deleted?
                                        Posted by martinsebor at Jan 18, 2010 20:27
                                     |
| or further developed.  This section was an attempt to codify some rules at interface design in C that didn't really get the attention it deserved before we became distracted by other things.
                                        Posted by rcs at Jan 18, 2010 21:25
                                     |
| I'd be happy to contribute but I'm afraid I'm not sure I know how one would go about supporting compile time checking in C other than by following DCL03-C. Use a static assertion to test the value of a constant expression, and while making failures obvious (as opposed to hard to detect?) sounds like a good design principle I struggle coming up with a simple code example demonstrating how.
                                        Posted by martinsebor at Jan 19, 2010 19:56
                                     |

