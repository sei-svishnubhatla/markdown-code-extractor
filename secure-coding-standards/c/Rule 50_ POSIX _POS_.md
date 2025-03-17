This appendix contains guidelines for functions that are defined as part of the POSIX family of standards but are not included in the C Standard. These rules and recommendations are not part of the core standard because they do not apply in all C language applications and because they represent an incomplete set. The intent of providing these guidelines is to demonstrate how rules and recommendations for other standards or specific implementations may be integrated with the core C recommendations.
-   Page:
    [POS30-C. Use the readlink() function properly](/confluence/display/c/POS30-C.+Use+the+readlink%28%29+function+properly)
-   Page:
    [POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument](/confluence/display/c/POS34-C.+Do+not+call+putenv%28%29+with+a+pointer+to+an+automatic+variable+as+the+argument)
-   Page:
    [POS35-C. Avoid race conditions while checking for the existence of a symbolic link](/confluence/display/c/POS35-C.+Avoid+race+conditions+while+checking+for+the+existence+of+a+symbolic+link)
-   Page:
    [POS36-C. Observe correct revocation order while relinquishing privileges](/confluence/display/c/POS36-C.+Observe+correct+revocation+order+while+relinquishing+privileges)
-   Page:
    [POS37-C. Ensure that privilege relinquishment is successful](/confluence/display/c/POS37-C.+Ensure+that+privilege+relinquishment+is+successful)
-   Page:
    [POS38-C. Beware of race conditions when using fork and file descriptors](/confluence/display/c/POS38-C.+Beware+of+race+conditions+when+using+fork+and+file+descriptors)
-   Page:
    [POS39-C. Use the correct byte ordering when transferring data between systems](/confluence/display/c/POS39-C.+Use+the+correct+byte+ordering+when+transferring+data+between+systems)
-   Page:
    [POS44-C. Do not use signals to terminate threads](/confluence/display/c/POS44-C.+Do+not+use+signals+to+terminate+threads)
-   Page:
    [POS47-C. Do not use threads that can be canceled asynchronously](/confluence/display/c/POS47-C.+Do+not+use+threads+that+can+be+canceled+asynchronously)
-   Page:
    [POS48-C. Do not unlock or destroy another POSIX thread's mutex](/confluence/display/c/POS48-C.+Do+not+unlock+or+destroy+another+POSIX+thread%27s+mutex)
-   Page:
    [POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed](/confluence/display/c/POS49-C.+When+data+must+be+accessed+by+multiple+threads%2C+provide+a+mutex+and+guarantee+no+adjacent+data+is+also+accessed)
-   Page:
    [POS50-C. Declare objects shared between POSIX threads with appropriate storage durations](/confluence/display/c/POS50-C.+Declare+objects+shared+between+POSIX+threads+with+appropriate+storage+durations)
-   Page:
    [POS51-C. Avoid deadlock with POSIX threads by locking in predefined order](/confluence/display/c/POS51-C.+Avoid+deadlock+with+POSIX+threads+by+locking+in+predefined+order)
-   Page:
    [POS52-C. Do not perform operations that can block while holding a POSIX lock](/confluence/display/c/POS52-C.+Do+not+perform+operations+that+can+block+while+holding+a+POSIX+lock)
-   Page:
    [POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable](/confluence/display/c/POS53-C.+Do+not+use+more+than+one+mutex+for+concurrent+waiting+operations+on+a+condition+variable)
-   Page:
    [POS54-C. Detect and handle POSIX library errors](/confluence/display/c/POS54-C.+Detect+and+handle+POSIX+library+errors)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [pos](https://confluence/label/seccode/pos) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS30-C | High | Probable | Medium | P12 | L1 |
| POS34-C | High | Unlikely | Medium | P6 | L2 |
| POS35-C | High | Likely | Medium |  P18  |  L1  |
| POS36-C | High | Probable | Medium | P12 | L1 |
| POS37-C | High | Probable | Low | P18 | L1 |
| POS38-C | Medium | Unlikely | Medium | P4 | L3 |
| POS39-C | Medium | Likely | Low | P18 | L1 |
| POS44-C | Low | Probable | Low | P6 | L2 |
| POS47-C | Medium | Probable | Low | P12 | L1 |
| POS48-C | Medium | Probable | High | P4 | L3 |
| POS49-C | Medium | Probable | Medium | P8 | L2 |
| POS50-C | Medium | Probable | High | P4 | L3 |
| POS51-C | Low | Probable | Medium | P4 | L3 |
| POS52-C | Low | Probable | High | P2 | L3 |
| POS53-C | Medium | Probable | High | P4 | L3 |
| POS54-C | High | Likely | Medium | P18 | L1 |

## Related Rules and Recommendations

|  |
| ----|
| CON04-C. Join or detach threads even if their exit status is unimportant |
| CON04-C. Join or detach threads even if their exit status is unimportant |
| CON04-C. Join or detach threads even if their exit status is unimportant |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV33-C. Do not call system() |
| ENV33-C. Do not call system() |
| ENV33-C. Do not call system() |
| ERR32-C. Do not rely on indeterminate values of errno |
| ERR32-C. Do not rely on indeterminate values of errno |
| ERR32-C. Do not rely on indeterminate values of errno |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO05-C. Identify files using multiple file attributes |
| FIO05-C. Identify files using multiple file attributes |
| FIO05-C. Identify files using multiple file attributes |
| FIO08-C. Take care when calling remove() on an open file |
| FIO08-C. Take care when calling remove() on an open file |
| FIO08-C. Take care when calling remove() on an open file |
| FIO22-C. Close files before spawning processes |
| FIO22-C. Close files before spawning processes |
| FIO22-C. Close files before spawning processes |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS54-C. Detect and handle POSIX library errors |
| POS54-C. Detect and handle POSIX library errors |
| POS54-C. Detect and handle POSIX library errors |
| SIG00-C. Mask signals handled by noninterruptible signal handlers |
| SIG00-C. Mask signals handled by noninterruptible signal handlers |
| SIG00-C. Mask signals handled by noninterruptible signal handlers |
| SIG01-C. Understand implementation-specific details regarding signal handler persistence |
| SIG01-C. Understand implementation-specific details regarding signal handler persistence |
| SIG01-C. Understand implementation-specific details regarding signal handler persistence |
| SIG02-C. Avoid using signals to implement normal functionality |
| SIG02-C. Avoid using signals to implement normal functionality |
| SIG02-C. Avoid using signals to implement normal functionality |
| VOID Always check for errors when using threads |
| VOID Always check for errors when using threads |
| VOID Always check for errors when using threads |
| VOID Do not create temporary files in shared directories |
| VOID Do not create temporary files in shared directories |
| VOID Do not create temporary files in shared directories |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| void SIG33-C. Do not recursively invoke the raise() function |
| void SIG33-C. Do not recursively invoke the raise() function |
| void SIG33-C. Do not recursively invoke the raise() function |

------------------------------------------------------------------------
[](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](../c/POS30-C_%20Use%20the%20readlink__%20function%20properly)
## Comments:

|  |
| ----|
| I really think; POSIX issues should be a separate document.   C is used on things that are not POSIX
                                        Posted by ron at Aug 31, 2006 19:08
                                     |
| Oh, heck, I can defend leaving it here for now ... there's a reasonably strong affiliation between the C and POSIX communities, and until the POSIX section expands into a whole book-length topic by itself (if ever), it seems simpler to just keep it where it is now.
                                        Posted by tplum@plumhall.com at Sep 01, 2006 13:38
                                     |
| POSIX interfaces do serve as a guidline for extending Standard;C even on non-POSIX platforms.
                                        Posted by dagwyn at Apr 18, 2008 15:41
                                     |
| Would a rule saying "Mutexes should be locked and unlocked in the same level of abstraction" (eg similar to MEM00-C. Allocate and free memory in the same module, at the same level of abstraction be useful?
                                        Posted by svoboda at Aug 15, 2008 12:01
                                     |
| I think keeping a POSIX section is worthwhile since it does influence the direction of the C standard and occassionally changes the semantics and behavior of functions defined in the C standard. It is useful to know this type of information. 
                                        Posted by eric.decker@itt.com at Nov 25, 2009 12:02
                                     |
| A rule saying "pthread_cancel() should not be used" may be useful. I personally have come across a lot of code using pthread_cancel() to terminate a thread and rarely did I not find problems with that code. Even using pthread_cleanup_push() and/or pthread_setcancelstate() to control what happens when the thread is canceled or when we can cancel the thread tends to lead to disaster. There is always something missing in the thread cleanup handler, or something wasn't included in the non-cancelable block of code that should have been. I view pthread_cancel() as a ticking time bomb; even if the code is implemented correctly today, someone will break it later on. 
The primary problem I have with using pthread_cleanup_push() and pthread_cleanup_pop() is that you are, perhaps unknowingly, making the assumption that all of the functions you call within the thread were written to be cancellable. For instance lets say that the thread calls some kind of parser routine which ultimately calls read(). If the implementor of this function didn't expect the thread it is running to be canceled, then they probably didn't protect against it. If pthread_cancel() is called while the parser is calling read() than any resources inside that parser routine will be leaked. Another problem with these routines I've seen deals with mutexes — perhaps we have a cleanup routine which will ensure that we call pthread_mutex_unlock(). But what happens if we didn't actually still have that mutex locked when we hit our cancelation point? According to POSIX you can only unlock a mutex owned (locked) by that thread, therefore nothing bad happens, just the call to pthread_mutex_unlock() returns -1 and sets errno to EPERM. Now what happens to the same code on Linux? Well on at least some version of Linux the mutex will be unlocked regardless of which thread actually owned it.
Using pthread_setcancelstate() has its limitations as well. I'll avoid the details for now...
There are other means to get the desired effect of pthread_cancel() that typically are safer, however these techniques typically are less generic (i.e. the proper solution may depend on the type of "work" performed by the thread).
                                        Posted by eric.decker@itt.com at Nov 25, 2009 12:59
                                     |
| Just noticed that POS33-C was deleted completely on July 10, 2020...; Is there any reason? as one of our customers is asking for it. thanks
                                        Posted by zhuoc at Jul 15, 2020 22:52
                                     |
| It's not totally deleted. It's just moved to The Void: void POS33-C. Do not use vfork()Anyway, that was done for two reasons: vfork() isn't actually in POSIX, and the rule as written was a blanket ban on its use even though there's a lot of cases where it is safe to use.
                                        Posted by jcsible at Jul 15, 2020 23:05
                                     |
| Thanks for your quick response Joseph C. Sible
                                        Posted by zhuoc at Jul 15, 2020 23:19
                                     |

