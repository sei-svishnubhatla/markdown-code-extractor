> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Use+variables+of+type+size_t+for+size+parameters+to+memory+allocation+routines?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Using+ROSE+Checkers?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I don't think this recommendation says what I hope you mean.
It is not necessary to mark all auto variables volatile between a setjmp and longjump. The only time it matters is if the variables exist in the stack frame with the setjmp call and were declared (allocated) before the setjmp call. If they were declared later in the same stack frame or were part of a later stack frame, they won't even exist after the longjmp.
                                        Posted by wlf@cert.org at Apr 29, 2007 11:23
                                     |
| This is OK, but you should still incorporate information from additional sources such as the the POSIX standard http://www.opengroup.org/onlinepubs/009695399/toc.htm and what the C99 standard has to say.
                                        Posted by rcs at Apr 29, 2007 13:25
                                     |
| Should this be combined with:
https://www.securecoding.cert.org/confluence/display/seccode/DCL34-C.+Use+volatile+for+data+that+may+be+accessed+or+modified+asynchronously
It seems like this is a specific case of DCL34-C.
                                        Posted by jpincar at May 24, 2007 16:36
                                     |

