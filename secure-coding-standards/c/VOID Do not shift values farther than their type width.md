> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+return+from+SIGFPE+from+inside+a+signal+handler?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+store+an+address+into+an+object+with+a+longer+lifetime?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Hunter, I think the limits on bit-shifting operations are covered by INT32-C. Ensure that operations on signed integers do not result in overflow and INT30-C. Ensure that unsigned integer operations do not wrap. Does this rule have information not covered by those two rules?
                                        Posted by svoboda at Mar 23, 2009 17:00
                                     |

