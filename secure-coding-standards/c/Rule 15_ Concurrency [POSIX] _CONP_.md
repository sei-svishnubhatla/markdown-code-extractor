-   Page:
    [CON30-C. Clean up thread-specific storage](/confluence/display/c/CON30-C.+Clean+up+thread-specific+storage)
-   Page:
    [CON31-C. Do not destroy a mutex while it is locked](/confluence/display/c/CON31-C.+Do+not+destroy+a+mutex+while+it+is+locked)
-   Page:
    [CON32-C. Prevent data races when accessing bit-fields from multiple threads](/confluence/display/c/CON32-C.+Prevent+data+races+when+accessing+bit-fields+from+multiple+threads)
-   Page:
    [CON33-C. Avoid race conditions when using library functions](/confluence/display/c/CON33-C.+Avoid+race+conditions+when+using+library+functions)
-   Page:
    [CON34-C. Declare objects shared between threads with appropriate storage durations](/confluence/display/c/CON34-C.+Declare+objects+shared+between+threads+with+appropriate+storage+durations)
-   Page:
    [CON35-C. Avoid deadlock by locking in a predefined order](/confluence/display/c/CON35-C.+Avoid+deadlock+by+locking+in+a+predefined+order)
-   Page:
    [CON36-C. Wrap functions that can spuriously wake up in a loop](/confluence/display/c/CON36-C.+Wrap+functions+that+can+spuriously+wake+up+in+a+loop)
-   Page:
    [CON37-C. Do not call signal() in a multithreaded program](/confluence/display/c/CON37-C.+Do+not+call+signal%28%29+in+a+multithreaded+program)
-   Page:
    [CON38-C. Preserve thread safety and liveness when using condition variables](/confluence/display/c/CON38-C.+Preserve+thread+safety+and+liveness+when+using+condition+variables)
-   Page:
    [CON39-C. Do not join or detach a thread that was previously joined or detached](/confluence/display/c/CON39-C.+Do+not+join+or+detach+a+thread+that+was+previously+joined+or+detached)
-   Page:
    [CON40-C. Do not refer to an atomic variable twice in an expression](/confluence/display/c/CON40-C.+Do+not+refer+to+an+atomic+variable+twice+in+an+expression)
-   Page:
    [CON41-C. Wrap functions that can fail spuriously in a loop](/confluence/display/c/CON41-C.+Wrap+functions+that+can+fail+spuriously+in+a+loop)
-   Page:
    [CON43-C. Do not allow data races in multithreaded code](/confluence/display/c/CON43-C.+Do+not+allow+data+races+in+multithreaded+code)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [con](https://confluence/label/seccode/con) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON00-C | medium | probable | high | P4 | L3 |
| CON01-C | low | probable | medium | P4 | L3 |


| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON31-C | medium | probable | high | P4 | L3 |
| CON32-C | medium | probable | medium | P8 | L2 |
| CON33-C | medium | probable | high | P4 | L3 |
| CON34-C | medium | probable | high | P4 | L3 |
| CON35-C | low | probable | medium | P4 | L3 |
| CON36-C | low | probable | high | P2 | L3 |
| CON37-C | medium | probable | high | P4 | L3 |
| CON38-C | low | unlikely | medium | P2 | L3 |
| CON39-C | Medium | unlikely | High | P2 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| CON04-C. Join or detach threads even if their exit status is unimportant |
| CON04-C. Join or detach threads even if their exit status is unimportant |
| CON04-C. Join or detach threads even if their exit status is unimportant |
| CON30-C. Clean up thread-specific storage |
| CON30-C. Clean up thread-specific storage |
| CON30-C. Clean up thread-specific storage |
| CON31-C. Do not destroy a mutex while it is locked |
| CON31-C. Do not destroy a mutex while it is locked |
| CON31-C. Do not destroy a mutex while it is locked |
| CON32-C. Prevent data races when accessing bit-fields from multiple threads |
| CON32-C. Prevent data races when accessing bit-fields from multiple threads |
| CON32-C. Prevent data races when accessing bit-fields from multiple threads |
| CON33-C. Avoid race conditions when using library functions |
| CON33-C. Avoid race conditions when using library functions |
| CON33-C. Avoid race conditions when using library functions |
| CON34-C. Declare objects shared between threads with appropriate storage durations |
| CON34-C. Declare objects shared between threads with appropriate storage durations |
| CON34-C. Declare objects shared between threads with appropriate storage durations |
| CON35-C. Avoid deadlock by locking in a predefined order |
| CON35-C. Avoid deadlock by locking in a predefined order |
| CON35-C. Avoid deadlock by locking in a predefined order |
| CON37-C. Do not call signal() in a multithreaded program |
| CON37-C. Do not call signal() in a multithreaded program |
| CON37-C. Do not call signal() in a multithreaded program |
| CON43-C. Do not allow data races in multithreaded code |
| CON43-C. Do not allow data races in multithreaded code |
| CON43-C. Do not allow data races in multithreaded code |
| CON50-CPP. Do not destroy a mutex while it is locked |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS44-C. Do not use signals to terminate threads |
| POS44-C. Do not use signals to terminate threads |
| POS44-C. Do not use signals to terminate threads |
| POS47-C. Do not use threads that can be canceled asynchronously |
| POS47-C. Do not use threads that can be canceled asynchronously |
| POS47-C. Do not use threads that can be canceled asynchronously |
| POS48-C. Do not unlock or destroy another POSIX thread's mutex |
| POS48-C. Do not unlock or destroy another POSIX thread's mutex |
| POS48-C. Do not unlock or destroy another POSIX thread's mutex |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS50-C. Declare objects shared between POSIX threads with appropriate storage durations |
| POS50-C. Declare objects shared between POSIX threads with appropriate storage durations |
| POS50-C. Declare objects shared between POSIX threads with appropriate storage durations |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS51-C. Avoid deadlock with POSIX threads by locking in predefined order |
| POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable |
| POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable |
| POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable |
| VOID CON04-CPP. Ensure objects are fully initialized before allowing access |
| VOID CON30-CPP. Ensure all threads exit before exiting main |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS05-C. Avoid race conditions with multiple POSIX threads |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| VOID POS41-C. When a POSIX thread exit status is not of concern,  pthread_detach() or an equivalent function must be used |
| VOID POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable with POSIX threads |
| VOID POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable with POSIX threads |
| VOID POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable with POSIX threads |
| WIN01-C. Do not forcibly terminate execution |
| WIN01-C. Do not forcibly terminate execution |
| WIN01-C. Do not forcibly terminate execution |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/DCL09-C.+Declare+functions+that+return+errno+with+a+return+type+of+errno_t?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=25034824) [](https://www.securecoding.cert.org/confluence/display/seccode/CON00-C.+Avoid+race+conditions+with+multiple+threads?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| There's something strange about this page. It declares a "CONP" prefix but lists "CON" rules.
                                        Posted by ann.campbell at Feb 19, 2016 14:37
                                     |
| This section is actually meant to be in the VOID. I will move it there now.
                                        Posted by aballman at Feb 22, 2016 11:36
                                     |

