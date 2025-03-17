> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+store+an+address+into+an+object+with+a+longer+lifetime?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Ensure+array+offsets+properly+align+in+variable-sized+arrays+of+unions+and+structs?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Same comment as FIO45-C. Valid rule, but you prob should make it a rec.
                                        Posted by svoboda at Mar 26, 2009 11:34
                                     |
| I see this rule looks a bit more fleshed out. Please consult the style guide I announced last week. Also, this rule sould be in the POSIX sdection because it relies on pthreads, which aren't part of the C standard.
                                        Posted by svoboda at Apr 01, 2009 18:08
                                     |
| Janice, this rule still needs a lot of work.
    Add a link from POSIX page, also code indentation needs cleaned up (as I explained in my styleguide announcement)
    Need a NCCE actually declaring flag to be volatile. Text that says 'if flag is volatile' doesn't cut it.
    No risk assessment or references???
                                        Posted by svoboda at Apr 03, 2009 21:08
                                     |
| I have moved this to the POSIX section.
                                        Posted by jdsa at Apr 03, 2009 22:30
                                     |

