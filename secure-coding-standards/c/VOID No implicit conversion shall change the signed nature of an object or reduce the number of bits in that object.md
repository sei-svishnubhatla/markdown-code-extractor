> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=28737702) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Prefer+inline+or+static+functions+to+function-like+macros?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| 
    The 'Other Languages' section is for cross-linking this rule to its C++/Java versions if any. Your EC link in there should go in References.
    Go ahead & link this rule from the Integers page.
Other than those, I'd say this rule is done.
                                        Posted by svoboda at Nov 06, 2009 06:47
                                     |
| I'm inclined to move this into the void.  I think the part of this guideline that makes sense is covered by INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data.  The advice to cast for clarity is generally understood to be poor advice, because the cast will eliminate any potential diagnostic provided by the compiler or by may static / dynamic analysis tools.
Any objections?
                                        Posted by rcs at Dec 02, 2009 15:15
                                     |

