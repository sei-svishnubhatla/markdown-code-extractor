> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=3473523) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Temporary+files+must+be+removed+before+the+program+exits?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| There is quite a lot of work to be done on this item.
                                        Posted by jonathan.leffler@gmail.com at Mar 19, 2008 15:05
                                     |
| UNIX System V-derived systems such as Solaris provide very nice file and record locking support (see fcntl(2), lockf(3c)).; NFS supports this if the lockd daemon is running on the NFS server.
                                        Posted by dagwyn at Apr 17, 2008 19:44
                                     |

