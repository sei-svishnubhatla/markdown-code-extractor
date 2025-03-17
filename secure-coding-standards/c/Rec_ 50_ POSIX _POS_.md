This appendix contains guidelines for functions that are defined as part of the POSIX family of standards but are not included in the C Standard. These rules and recommendations are not part of the core standard because they do not apply in all C language applications and because they represent an incomplete set. The intent of providing these guidelines is to demonstrate how rules and recommendations for other standards or specific implementations may be integrated with the core C recommendations.
-   Page:
    [POS01-C. Check for the existence of links when dealing with files](/confluence/display/c/POS01-C.+Check+for+the+existence+of+links+when+dealing+with+files)
-   Page:
    [POS02-C. Follow the principle of least privilege](/confluence/display/c/POS02-C.+Follow+the+principle+of+least+privilege)
-   Page:
    [POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks](/confluence/display/c/POS04-C.+Avoid+using+PTHREAD_MUTEX_NORMAL+type+mutex+locks)
-   Page:
    [POS05-C. Limit access to files by creating a jail](/confluence/display/c/POS05-C.+Limit+access+to+files+by+creating+a+jail)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [pos](https://confluence/label/seccode/pos) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS01-C | Medium | Likely | High | P6 | L2 |
| POS02-C | High | Likely | High | P9 | L2 |
| POS04-C | Low | Unlikely | Medium | P2 | L3 |
| POS05-C | Medium | Probable | High | P4 | L3 |

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
[](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152372)
