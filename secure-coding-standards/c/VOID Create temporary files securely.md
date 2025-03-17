> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1376327) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Define+numeric+constants+in+a+portable+way?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Perhaps it should be noted that mkstemp() creates files with access permissions based on the umask(). 
                                        Posted by jsg at Jan 10, 2007 14:17
                                     |
| The compliant solution on Windows won't work on Vista with limited user accounts, or in other locked-down windows systems. tmpfile() and tmpfile_s() write to the root directory on windows, not TMP as you'd expect (see MSDN), so you get access denied errors. 
                                        Posted by brian.ewins at Dec 22, 2007 07:25
                                     |

