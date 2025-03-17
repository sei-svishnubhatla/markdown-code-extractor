> [!info]  
>
> This practice has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard: It has been superseded by rule [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts). The practice has not been erased in case it contains information that might be useful in the future.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2687100) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+allow+loops+to+iterate+beyond+the+end+of+an+array?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| As noted in the description of this rule:
If both the pointer operand and the result point to elements of the same array object, or one past the last element of the array object...
Thus, to avoid misinterpreting the rule in an unintentionally restrictive way, the rule ought to be renamed to Do not add or subtract an integer to a pointer if the result is not valid pointer .
                                        Posted by martinsebor at Jan 09, 2010 18:08
                                     |

