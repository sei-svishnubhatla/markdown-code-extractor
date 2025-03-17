-   Page:
    [SIG30-C. Call only asynchronous-safe functions within signal handlers](/confluence/display/c/SIG30-C.+Call+only+asynchronous-safe+functions+within+signal+handlers)
-   Page:
    [SIG31-C. Do not access shared objects in signal handlers](/confluence/display/c/SIG31-C.+Do+not+access+shared+objects+in+signal+handlers)
-   Page:
    [SIG34-C. Do not call signal() from within interruptible signal handlers](/confluence/display/c/SIG34-C.+Do+not+call+signal%28%29+from+within+interruptible+signal+handlers)
-   Page:
    [SIG35-C. Do not return from a computational exception signal handler](/confluence/display/c/SIG35-C.+Do+not+return+from+a+computational+exception+signal+handler)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [sig](https://confluence/label/seccode/sig) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG30-C | High | Likely | Medium | P18 | L1 |
| SIG31-C | High | Likely | High | P9 | L2 |
| SIG34-C | Low | Unlikely | Low | P3 | L3 |
| SIG35-C | Low | Unlikely | High | P1 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| CON37-C. Do not call signal() in a multithreaded program |
| CON37-C. Do not call signal() in a multithreaded program |
| CON37-C. Do not call signal() in a multithreaded program |
| ERR32-C. Do not rely on indeterminate values of errno |
| ERR32-C. Do not rely on indeterminate values of errno |
| ERR32-C. Do not rely on indeterminate values of errno |

------------------------------------------------------------------------
[](../c/Rule%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152178)
## Comments:

|  |
| ----|
| Robert and I discussed adding a recommendation here to replace ALL default handlers when working with crypto.; The default handlers call abort which forces a coredump, now all of your plaintext is sitting on the hard drive and all because you got a SIGALRM or somesuch
                                        Posted by avolkovi at Mar 06, 2008 11:21
                                     |
| SIGNAL(7) contains a list of signals for which the default action is to terminate the process and dump core.
Replace "crypto"->sensitive information.
Maybe also comment on how this interplays with rlimit
See http://www.dwheeler.com/secure-programs/Secure-Programs-HOWTO.html
Section 7.14. Self-limit Resources
                                        Posted by rcs at Mar 06, 2008 17:04
                                     |
| According to DCL05-A, the specification of the signal function could probably be written more clearly using typedef void (*sighandler_t)(int) for the type of the second parameter and return value.
                                        Posted by adahmad at Apr 14, 2008 10:28
                                     |
| Changed code to reflect typedef from DCL05-A. But the signal handler type name is probably implementation-dependent. On Linux it is __sighandler_t, which doesn't render properly on this wiki 
                                        Posted by svoboda at Apr 14, 2008 11:16
                                     |
| I'm a little uncomfortable with this change, because the definition from C99 is character for character:
[code}
void (*signal(int sig, void (*func)(int)))(int);

![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 15, 2008 03:26
\| \|
Added back old signal() declaration, leaving in new 'typedef' declaration as conceptual simplification
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 15, 2008 09:49
\| \|
There is often some way to prevent core dumps, for example setting a resource limit for them to max 0.; Some POSIX systems don't produce core dumps for set-UID programs.  
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 11:29
\| \|
signal() is so problematic that mention should be made up front of POSIX sigaction/sigvec.; The best policy is to not use signals for IPC, only (at most) to field a manual interrupt (SIGINT) and set a flag that can be tested in the main control loop.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 11:31
\| \|
Rob and I discussed this. The problem being that sigaction/sigvec are not in C99 and are not supported outside of POSIX (such as on Windows).
Nearly every rule/rec here has a POSIX-only compliant code example using sicgaction(). Many rules lack comparable solutions for Windows.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 18, 2008 11:41
\| \|
It should be mentioned somewhere that if one is using assert(), it would be wise to catch SIGABRT and do something like call exit(EXIT_FAILURE) so that the atexit-registered handlers are not bypassed.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 11:56
\| \|
Often enough people just don't believe the Standard about how limited signal handers are.; So I think you should rearrange the signal handing section a bit and change emphasis.  Something like this:
Let the quote from the Standard about what signal handlers can do, be the first rule or recommendation, amended by the point you added that the C Committee agreed they can read volatile sig_atomic_t, and they can use async-safe functions.
"Yes, safe standard C signal handlers really are that limited.  The C standard doesn't say that just to be difficult, but because that was all vendors could agree they'd all implement. If you want a handler to do more safely, you need OS extensions."
 (\[Edited comment, had dropped some parts\]  Plus I imagine there may be special cases which were just hard or pointless to list.  in particular since people will want to do more in signal handers anyway, and signal handlers may be a desperation measure.  E.g. I doubt I'll ever meet a computer where it's unsafe to read a const static-storage variable short of in debugging environments like valgrind, but maybe someone should tell me to read my previous paragraph.  Not sure what, if anything, to say about that.  But signal handlers in particular may be set up just to say something sensible before crashing, in which case it may be acceptable if reality breaks expectaions.  Is there a general exception to the rules in this standard which allows "I know this may break, but it's best to do it anyway"-kind of code?)
(Edit again: Took me all of 3 minutes to think of an example of my "doubt" I may already have met.  make a
``` java
 struct { const char x; char y; }
```
on a machine without atomic char writes, only atomic word writes. Or where the compiler prefers word writes. x gets written when updating y. Maybe the compiler would be allowed to do that in strange ways between sequence points, if it should find it useful.  I'm too tired to think straight now, but I at least proved my point about not believing![](images/icons/emoticons/smile.svg)  
anyway, continuing with my suggested text:
 "E.g. it may be unsafe to update an int - that may not be an atomic operation.  This is why the sig_atomic_t type is needed. Even if an int can be accessed atomically, the compiler might not always choose that way to access it.
Adding volatile need not help - that ensures modifications are complete at sequence points, but signals do not have the courtesy of arriving at sequence points.
If a function is thread-safe, that's not merely insufficient to let a signal handler call it, it may make it worse.  The function may be thread-safe because it locks a resource before accessing it.  If a thread is signalled while it is currently using that resource and thus holds the lock, the thread can freeze - it sits down to wait for itself to free the lock.  This means, among other things, that printing to stderr in a signal handler can deadlock the program.  Use an async-safe OS function instead, like write() on Posix."
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 18, 2008 21:50
\| \|
implemented as [ERR06-C. Understand the termination behavior of assert() and abort()](ERR06-C_%20Understand%20the%20termination%20behavior%20of%20assert__%20and%20abort__)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 20, 2008 14:00
\|
