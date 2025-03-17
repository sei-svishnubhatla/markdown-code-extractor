-   Page:
    [PRE30-C. Do not create a universal character name through concatenation](/confluence/display/c/PRE30-C.+Do+not+create+a+universal+character+name+through+concatenation)
-   Page:
    [PRE31-C. Avoid side effects in arguments to unsafe macros](/confluence/display/c/PRE31-C.+Avoid+side+effects+in+arguments+to+unsafe+macros)
-   Page:
    [PRE32-C. Do not use preprocessor directives in invocations of function-like macros](/confluence/display/c/PRE32-C.+Do+not+use+preprocessor+directives+in+invocations+of+function-like+macros)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [pre](https://confluence/label/seccode/pre) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE30-C | Low | Unlikely | Medium | P2 | L3 |
| PRE31-C | Low | Unlikely | Low | P3 | L3 |
| PRE32-C | Low | Unlikely | Medium | P2 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| DCL00-C. Const-qualify immutable objects |
| DCL00-C. Const-qualify immutable objects |
| DCL00-C. Const-qualify immutable objects |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152465)
## Comments:

|  |
| ----|
| PCLint has error 553 (see http://gimpel-online.com/MsgRef.html), which identifies undefined preprocessor macros that are used in a macro context, such as #if.  Do we need a secure coding rule about this?
                                        Posted by svoboda at Dec 09, 2010 10:22
                                     |
| It's not uncommon to reference an undefined macro in the #if directive:
#if HAVE_SOME_FEATURE
  /* use SOME feature */
#else
  /* work around the absence of SOME feature */
#endif

When `HAVE_SOME_FEATURE` is not defined by the configuration script it's treated as if its value was 0. That said, some compilers (EDG eccp being one) have an option to make it possible to diagnose these usually benign cases.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 11, 2010 18:40
\|
