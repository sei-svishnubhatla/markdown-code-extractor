> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Ensure+array+offsets+properly+align+in+variable-sized+arrays+of+unions+and+structs?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Ensure+that+source+and+destination+pointers+in+function+arguments+do+not+point+to+overlapping+objects?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This problem pointed out by this guideline is just one of many that can be caused by failing to check and handle errors. The general class of problems is discussed in CWE-391 and, more broadly, its parent CWE-389, and avoiding them is the subject of the following guidelines:
    EXP12-C. Do not ignore values returned by functions
    FIO04-C. Detect and handle input and output errors
    FIO33-C. Detect and handle input output errors resulting in undefined behavior
    MEM32-C. Detect and handle memory allocation errors
I don't think it's practical to have a separate guideline for each function that may fail, or even for each category of functions (such as FIO04-C or MEM32-C) or for different severities of the consequences (FIO33-C). All errors should always be detected and handled appropriately. Exceptions can be made on a case by case basis when code review determines the consequences of ignoring the error to be benign.
                                        Posted by martinsebor at Mar 19, 2010 19:58
                                     |
| I agree.  At one point we considered having only one guideline for "Detect and handle errors" which presumably would be in 12. Error Handling (ERR).
Then we decided to write one rule and one recommendation for file i/o handling to differentiate between error checking failures that should be diagnosed and those which were fairly common place but not particularly critical and probably should not.
The plan was to write a pair of these for each section, but we got lazy.  We should probably revisit that plan, and if we keep it, it may make sense to have one rule and one recommendation for the entire pthreads library.  I agree that we don't one a guideline like this for each function.
                                        Posted by rcs_mgr at Mar 19, 2010 20:13
                                     |
| From Geoff Clare:
I would suggest removing the "otherwise ..." part of the title.
In the first paragraph it says
    "So failing to lock the mutex before a call to pthread_cond_wait()
    may cause the thread not to wait"
The problem is more serious than that; it results in undefined behavior, unless the mutex type is PTHREAD_MUTEX_ERRORCHECK (or it is a robust mutex).
There is a similar problem in the intro to the NCCE.  It needs to talk about the two different cases based on mutex type.  What it says at the moment about attempting to unlock the mutex if it hasn't been acquired is relevant for errorcheck mutexes, but for
(non-robust) recursive mutexes the pthread_cond_wait() call has undefined behavior and the pthread_mutex_unlock() might never be reached.
                                        Posted by rcs at Mar 22, 2010 16:30
                                     |
| I only mentioned errorcheck and recursive mutexes here because of POS04-C, but I've just realised that it is only a recommendation not a rule, so I suppose normal mutexes should also be considered here.  What I said about recursive mutexes also applies to normal mutexes.
                                        Posted by geoffclare at Mar 23, 2010 04:36
                                     |

