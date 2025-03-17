> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Avoid+reopening+a+file+stream?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Beware+of+infinite+loops?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I'm having a hard time understanding this recommendation, which is sort of odd, since I wrote it initially.  Is it possible to provide a Non-Compliant Code Example and a Compliant Solution?  What are the right and wrong things to do here?
                                        Posted by rcs at Mar 20, 2008 22:35
                                     |
| I'm confused too.; The only thing I can think of is to make sure any multithreaded code that uses errno is not run on an old system from before the updated POSIX standard.
                                        Posted by dmk at Mar 21, 2008 23:21
                                     |
| To add more confusion to this, looks like Open Group redefined this as allowing macros, and that most implementations do just that.
Do we really want to recommend for people not use errno in multithreading?; Everything I have found online says that is OK since the thread libraries "take care of it"
                                        Posted by avolkovi at Mar 25, 2008 10:30
                                     |
| http://www.opengroup.org/onlinepubs/009695399/functions/errno.html
                                        Posted by avolkovi at Mar 25, 2008 10:39
                                     |
| On some systems you onlyget the thread-safe errno definition if you compile the code in a certain way. If you mix object files (or libraries) compiled both ways, and you call functions that were compiled the non-thread-safe way from multiple threads, then those functions will all try to use the same (global) errno instead of each using the thread-specific errno for the thread that called it.
So I think the issue here is not about how you write the code, but how you compile it.;
                                        Posted by geoffclare at Mar 25, 2008 12:08
                                     |
| I recommend removing this item.; If the system supports POSIX threads, errno will be safe (as long as you include <errno.h> and don't try to fake it with 'extern int errno;').  If the system doesn't support POSIX threads, you've got worse problems than 'your non-POSIX threads might access a non-thread-safe errno'.
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 02:00
                                     |

