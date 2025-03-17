> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+assume+the+destination+array+of+strncpy()+is+null-terminated?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+create+temporary+files+in+shared+directories?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| The risk is higher than the risk assessment indicates.; The longjmp tries to use a defunct stack frame, which has probably been overwritten by the atexit handler's stack frame; almost anything could happen, including restarting part of the main program with inappropriate values for some variables.
Another reason this is a bad idea is that it prevents some of the other atexit handlers from being invoked.
                                        Posted by dagwyn at Apr 17, 2008 20:57
                                     |
| Yes. I think we should require that atexit() callbacks only ever exit with a return (including end-of-function).
                                        Posted by keylevel at May 30, 2008 12:21
                                     |

