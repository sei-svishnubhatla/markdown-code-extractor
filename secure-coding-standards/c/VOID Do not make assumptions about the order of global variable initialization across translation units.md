> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+create+temporary+files+in+shared+directories?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=534)
## Comments:

|  |
| ----|
| I could be wrong.  However, I think this guidelines is superfluous.  The ISO standard requires global object initializers be constant expressions or string literals.  As such, no standardized code could possibly violate this guideline.  Have I missed something?  Does Anyone know of a compiler which supports such code?
                                        Posted by xuinkrbin. at Feb 27, 2009 15:01
                                     |
| You are right.  I am going to move this to the void section.
                                        Posted by rcs_mgr at Feb 27, 2009 21:19
                                     |
| Agreed, this rule should be voided for C. C99 6.7.8, paragraph 4 says exactly what Franke says.
This is a valid rule for C++, which allows initializers to be extern variables or functions, and thus the order of initialization is important, and left implementation-defined.  (I still have scars from this problem.) 
                                        Posted by svoboda at Mar 02, 2009 17:03
                                     |

