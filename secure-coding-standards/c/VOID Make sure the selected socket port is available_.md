> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Limit+depth+of+nesting?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+No+implicit+conversion+shall+change+the+signed+nature+of+an+object+or+reduce+the+number+of+bits+in+that+object?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Jose, this does not sound like a security problem. If a Java program attempts to open an unavailable port, then an IOException is thrown, preventing the program from continuing. Granted, a programmer can suppress this by catching & ignoring IOException, but we have rules against ignoring exceptions.
                                        Posted by svoboda at Mar 24, 2009 11:31
                                     |
| Also, the implementing side can always fix it by disabling the other software that uses the port. The exception itself might help the user to figure out what's wrong, in this case. Having the OS select the incoming/outgoing port may sometimes be counterproductive since many people prefer to specify the port numbers in the user manuals (eases debugging etc.).
                                        Posted by dmohindr at Mar 24, 2009 11:55
                                     |

