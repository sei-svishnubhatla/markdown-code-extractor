> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+shift+values+farther+than+their+type+width?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+use+volatile+as+a+synchronization+primitive?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This rule is very similar to DCL30-C. Declare objects with appropriate storage durations.
Maybe these two rules should be combined? 
Alternatively, maybe this should be moved to the DCL section?
As written, it may also be possible that this should be a recommendation and not a rule.
                                        Posted by rcs at Mar 05, 2008 11:26
                                     |
| This is the first example I recall with a multi-threaded solution offered.; However, it seems to me likely that you would have to coordinate access to the buffer -- at least for the allocation and assignment, but probably for use too -- via appropriate threading controls - mutexes and the like.  The example code does not show this - and given that there are at least two (Windows, POSIX) thread libraries to worry about, I'm not surprised.  Without a section on threading, I think the example is stepping out of bounds.
                                        Posted by jonathan.leffler@gmail.com at Mar 17, 2008 09:24
                                     |
| Yes, interlocks are needed.; I agree that addressing thread issues is outside the scope of the guidelines, unless a rather large section is added about thread safety.  (I find that many programmers of threaded applications really don't understand the issues and their solutions.)
                                        Posted by dagwyn at Apr 16, 2008 22:39
                                     |

