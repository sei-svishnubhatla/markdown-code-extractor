> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+perform+certain+operations+on+questionably+signed+results?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+shift+values+farther+than+their+type+width?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| 
    I'm wondering if this should be a rule, rather than a recommendation.
    While it is much more secure and useful than signal(3), sigaction(3) is not standard C.  So your code samples should use signal(3). (If sigaction() is necessary for your solution, you can provide a POSIX-only compliant solution.)
    Explain what code does before or after the code sample; don't use comments.
    The link to SIG32-C should be active, and not appear in 'Related Vulnerabilities'...you can drop that section.
    The Risk Assessment section should provide the same metrics as other rules' risk assessment sections.
    While the NCCE/CS are correct, they beg the question. You presumably want to do useful things in your program after a divide-by-zero, and this rule forbids that. So you need a CS that aborts anyway (never doing the useful things). Also a CS that lets you do useful things somehow (most likely by preventing division-by-zero).
                                        Posted by svoboda at Mar 05, 2010 12:44
                                     |
| This rule is a strict subset of SIG35-C. Do not return from SIGSEGV, SIGILL, or SIGFPE signal handlers. The two should be merged.
                                        Posted by martinsebor at Mar 15, 2010 17:41
                                     |
| I agree with Martin. But let's proceed and complete this rule for the purpose of this assignment, and when the assignment is over we can merge the rules later. So here are my current comments on the rule:
    The CS needs to abide by SIG30-C. Call only asynchronous-safe functions within signal handlers.
    I disagree with the Risk Assessment info...moreover it is inconsistent.
                                        Posted by svoboda at Mar 17, 2010 16:10
                                     |

