> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Using+ROSE+Checkers?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+sciSpider?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| make sure you identify possible security consequences of non-compliance.
                                        Posted by rcs at Apr 07, 2007 09:59
                                     |
| In what situations does output not get written in the absence of a call to fflush()?  
                                        Posted by rcs at Apr 25, 2007 08:24
                                     |
| Every implementation of the C runtime I have ever seen does guarantee to call fflush() when fclose() is called. The only situation in which data does not get written to disk is if the program terminates abnormally. It is unclear in the case of a program terminating normally without calling fclose(). I have no idea what the standards say about open streams at normal program termination.
It is a bad practice to call sync() from user programs. It has a global effect on the performance of the entire system. It forces the OS to begin the process of writing all dirty buffers to disk. However, it is not synchronous. It returns to the caller before dirty buffers are written. Calling it does not have the effect it seems. However, fsync() does do what you seem to want to do. And it does not return until the data is committed to permanent storage.
                                        Posted by wlf@cert.org at Apr 25, 2007 10:30
                                     |
| I stated above that the danger is in the event of abnormal program termination.; The assumption here is that a call to fflush() itself should not ever cause abnormal program termination, and you can in a way look at the write()/flush() pair as an "atomic" operation--atomic in the sense that if one occurs the other should as well (assuming that either they do not occur in a multithreaded program, have some means of atomic protection within a multithreaded program, or are not killed by other means in that narrow window).  In the event of normal program termination, exit() is called and by definition of ISO/IEC 9899:1999 (see sections 5.1.2.2.3 and 7.20.4.3) all streams are flushed and closed.
 I agree that sync() is overkill, so I'll remove its call from the compliant code.  fsync() operates on file descriptors so it cannot be used in this example.
                                        Posted by shaunh at Apr 25, 2007 13:14
                                     |
| The "write/fflush()/fsync(fileno(file))" sequence is a frequently used idiom.It is the ONLY way to make sure your sensitive data actually gets to disk. fflush() does not call fsync(). It only calls write() which does not guarantee the data made it to disk. All write() does is schedule the write operation with the kernel. You still don't know when it will get written to disk.
We need to be aware, and point out, when we are recommending things with known negative performance implications. Both fflush() and fsync() have negative performance implications for the process, but only minor implications for the system as a whole.
I also think that if the only place this recommendation has value is in the case of abnormal termination, that should be in the very first paragraph, not in the prelude to an example.;
                                        Posted by wlf@cert.org at Apr 26, 2007 09:43
                                     |
| I agree with Bill that you need to make it clear when this is applicable.  In particular, did you really mean to say "even if it terminates abnormally" in the NCCE?
                                        Posted by rcs at May 06, 2007 08:35
                                     |
| We should acknowledge that fsync() and fileno() are POSIX, not C99.
Even within POSIX, what fsync does is implementation defined (it only promises the data is "transferred to the storage device"), so there's still no true guarantee (by the POSIX standard) that the data is really committed.  For example, if the data is network mounted with redundant servers, my reading of POSIX allows for fsync() to transfer the data to at least one server.  It doesn't appear to be required that the server itself has committed the data to disk.  Even if one server has committed the data, the other one may not have.
                                        Posted by hburch at May 23, 2007 11:11
                                     |
| POSIX has the options O_DSYNC, O_RSYNC and O_SYNC to open() that can influence data integrity on a specific open file.
The call to fclose() in the NCCE ensures that the data is as flushed as fflush() would make it - that is, the write() system call has returned.; In the absence of the O_*SYNC flags, it doesn't do as much as the fsync() does.
Calling _exit() suppresses the normal file flushing operations. 
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:37
                                     |

