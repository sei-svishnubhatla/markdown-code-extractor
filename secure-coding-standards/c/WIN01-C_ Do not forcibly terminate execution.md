When a thread terminates under normal conditions, thread-specific resources such as the initial stack space and thread-specific `HANDLE` objects are released automatically by the system and notifications are sent to other parts of the application, such as `DLL_THREAD_DETACH` messages being sent to DLLs.  However, if a thread is forcibly terminated by calling [TerminateThread()](http://msdn.microsoft.com/en-us/library/windows/desktop/ms686717(v=vs.85).aspx), the cleanup and notifications do not have the chance to run.  MSDN states
> **TerminateThread** is a dangerous function that should only be used in the most extreme cases. You should call **TerminateThread** only if you know exactly what the target thread is doing, and you control all of the code that the target thread could possibly be running at the time of the termination. For example, **TerminateThread** can result in the following problems:
>
> -   If the target thread owns a critical section, the critical section will not be released.
> -   If the target thread is allocating memory from the heap, the heap lock will not be released.
> -   If the target thread is executing certain kernel32 calls when it is terminated, the kernel32 state for the thread's process could be inconsistent.
> -   If the target thread is manipulating the global state of a shared DLL, the state of the DLL could be destroyed, affecting other users of the DLL.

 On some platforms (such as Microsoft Windows XP and Microsoft Windows Server 2003), the thread's initial stack is not freed, causing a resource leak.
Processes behave similar to threads, and so share the same concerns.  Do not use the `TerminateThread()` or [`TerminateProcess()`](http://msdn.microsoft.com/en-us/library/windows/desktop/ms686714(v=vs.85).aspx) APIs.  Instead, you should prefer to exit threads and processes by returning from the entrypoint, by calling [`ExitThread()`](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682659(v=vs.85).aspx), or by calling [`ExitProcess()`](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682658(v=vs.85).aspx).
## Noncompliant Code Example
In the following example, `TerminateThread()` is used to forcibly terminate another thread, which can leak resources and leave the application in an indeterminate state.
``` c
#include <Windows.h>
DWORD ThreadID;  /* Filled in by call to CreateThread */
/* Thread 1 */
DWORD WINAPI ThreadProc(LPVOID param) {
  /* Performing work */
}
/* Thread 2 */
HANDLE hThread = OpenThread(THREAD_TERMINATE, FALSE, ThreadID);
if (hThread) {
  TerminateThread(hThread, 0xFF);
  CloseHandle(hThread);
}
```
##  Compliant Solution
The compliant solution avoids calling `TerminateThread()` by requesting the thread terminate itself by exiting its entrypoint.  It does so in a lock-free, thread-safe manner by using the `InterlockedCompareExchange()` and `InterlockedExchange()` Win32 APIs.
``` c
#include <Windows.h>
DWORD ThreadID;  /* Filled in by call to CreateThread */
LONG ShouldThreadExit = 0;
/* Thread 1 */
DWORD WINAPI ThreadProc(LPVOID param) {
  while (1) {
    /* Performing work */
    if (1 == InterlockedCompareExchange(&ShouldThreadExit, 0, 1))
      return 0xFF;
  }
}
/* Thread 2 */
InterlockedExchange(&ShouldThreadExit, 1);
```
## Risk Assessment
Incorrectly using threads that asynchronously cancel may result in silent corruption, resource leaks, and, in the worst case, unpredictable interactions.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN01-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bad-function | Partially checked |
| CodeSonar | 8.3p0 | (customization) | Users can add a custom check for all uses of; TerminateThread() and TerminateProcess(). |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| RuleChecker | 24.04 | bad-function | Partially checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS47-C).
### Related Guidelines
TODO (notably, should be one about using `ExitThread()` from C++ code.
## Bibliography

|  |  |
| ----|----|
|  |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152030)[](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151928)
## Comments:

|  |
| ----|
| The compliant solution becomes difficult to handle when the thread might sleep indefinitely whilst performing work, and therefore not return. A typical example is a thread waiting for network data, but many more exist.A compliant solution would have to use a timeout on any situation where it might sleep, and basically wake up repeatedly just to see whether it should commit suicide. This tends to become clumsy, and it is difficult to balance responsiveness with CPU load.
                                        Posted by wouter.vlothuizen at Jul 19, 2013 11:20
                                     |
| Threads should not indiscriminately sleep (using Sleep(), SleepEx(), etc).; Instead, they usually sleep using one of the wait functions (WaitForSingleObject(), WaitForMulitpleObjects(), etc) which are considerably more thread-friendly.  This, in turn, allows for easy thread termination – instead of using a counter variable, you use an event object.  The thread adds it to the list in WaitForMultipleObjects() when it wants to yield time, and the thread initiating the termination uses SetEvent()to signal the termination.
                                        Posted by aballman at Jul 19, 2013 11:56
                                     |

