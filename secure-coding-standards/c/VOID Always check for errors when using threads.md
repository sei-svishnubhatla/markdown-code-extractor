> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Allocate+sufficient+memory+for+an+object?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Always+provide+feedback+about+the+resulting+value+of+a+method?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This rule looks like EXP12-C. Do not ignore values returned by functions just applied to the pthread functions. To be a valid rule, you have to provide some advice that is not just repetition of more general advice. 
                                        Posted by svoboda at Nov 05, 2009 16:43
                                     |
| Aborting a program on pthread_create() failure by calling abort() causes SIGABRT to be generated, with the default disposition of dropping core. Doing so would make a secure program susceptible to denial of service attacks and expose a security hole by leaving the state of the program's volatile memory on the disk. Secure programs must be able to handle resource exhaustion gracefully, usually by degrading quality of service. For the purposes of the example above, simply logging the error to stderr and avoiding calls to pthread_join() on pthread_t objects that do not correspond to successfully created threads (e.g., by decrementing num_threads for each failed call to pthread_create()) would demonstrate this approach.
                                        Posted by martinsebor at Dec 01, 2009 18:57
                                     |

