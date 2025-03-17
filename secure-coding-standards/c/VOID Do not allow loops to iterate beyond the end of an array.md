> [!info]  
>
> This practice has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard: It has been superseded by rule [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts). The practice has not been erased in case it contains information that might be useful in the future.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+assume+the+destination+array+of+strncpy()+is+null-terminated?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Computing an ending pointer value and doing away with the loop index is not only safer, but removes an induction variable that adds nothing to performance or safety.
                                        Posted by steve at Mar 13, 2008 23:51
                                     |
| I see the importance of having a real example for the NCCE/CS here, but I feel that we should also include simplified examples. This would maintain consistency with the rest of the document as well as make this particular article easier to read.
                                        Posted by jpincar at Jun 19, 2008 13:54
                                     |

