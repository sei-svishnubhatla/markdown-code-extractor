> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Prefer+inline+or+static+functions+to+function-like+macros?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+ROSE+Checkers?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Arjun Bijanki from MS sez:
> the Windows solution is wrong for two reasons, and I have to wonder if the *nix solutions are unsafe as well.  As far as Windows goes, (1) setrlimit is not a Windows function, and (2) VirtualLock is meant as a performance tool, not a security tool (for example, if you hibernate your machine, the memory's going to be written to disk regardless of whether it's VirtualLock'd).  Wouldn't this occur on other OSes that support hibernation, as well?  A better solution is to use CryptProtectData to allow sensitive data to securely exist in memory.  Read more here: http://blogs.msdn.com/oldnewthing/archive/2007/11/06/5924058.aspx

                                        Posted by svoboda at Apr 15, 2008 12:54
                                     |

