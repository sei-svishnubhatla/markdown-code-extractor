-   Page:
    [CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction](/confluence/display/c/CON01-C.+Acquire+and+release+synchronization+primitives+in+the+same+module%2C+at+the+same+level+of+abstraction)
-   Page:
    [CON02-C. Do not use volatile as a synchronization primitive](/confluence/display/c/CON02-C.+Do+not+use+volatile+as+a+synchronization+primitive)
-   Page:
    [CON03-C. Ensure visibility when accessing shared variables](/confluence/display/c/CON03-C.+Ensure+visibility+when+accessing+shared+variables)
-   Page:
    [CON04-C. Join or detach threads even if their exit status is unimportant](/confluence/display/c/CON04-C.+Join+or+detach+threads+even+if+their+exit+status+is+unimportant)
-   Page:
    [CON05-C. Do not perform operations that can block while holding a lock](/confluence/display/c/CON05-C.+Do+not+perform+operations+that+can+block+while+holding+a+lock)
-   Page:
    [CON06-C. Ensure that every mutex outlives the data it protects](/confluence/display/c/CON06-C.+Ensure+that+every+mutex+outlives+the+data+it+protects)
-   Page:
    [CON07-C. Ensure that compound operations on shared variables are atomic](/confluence/display/c/CON07-C.+Ensure+that+compound+operations+on+shared+variables+are+atomic)
-   Page:
    [CON08-C. Do not assume that a group of calls to independently atomic methods is atomic](/confluence/display/c/CON08-C.+Do+not+assume+that+a+group+of+calls+to+independently+atomic+methods+is+atomic)
-   Page:
    [CON09-C. Avoid the ABA problem when using lock-free algorithms](/confluence/display/c/CON09-C.+Avoid+the+ABA+problem+when+using+lock-free+algorithms)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [con](https://confluence/label/seccode/con) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON01-C | Low | Probable | Medium | P4 | L3 |
| CON02-C | Medium | Probable | Medium | P8 | L2 |
| CON04-C | Low | Unlikely | High | P1 | L3 |
| CON05-C | Low | Probable | High | P2 | L3 |
| CON06-C | Medium | Probable | Medium | P8 | L2 |
| CON07-C | Medium | Probable | Medium |  P8  |  L2  |
| CON08-C | Low | Probable | Medium | P4 | L3 |
| CON09-C | Medium | Unlikely | High | P2 | L3 |

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
[](../c/Rec_%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](../c/CON01-C_%20Acquire%20and%20release%20synchronization%20primitives%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction)
## Comments:

|  |
| ----|
| In table "Assessment Risk Summary" has no entry for CON03-C. Please add.
                                        Posted by volker.erben at Nov 29, 2018 08:57
                                     |
| Volker,CON03-C isn't included because it's an "incomplete" recommendation.Thanks.
                                        Posted by rschiela at Mar 20, 2019 11:12
                                     |

