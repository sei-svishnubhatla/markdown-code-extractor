Securable resources such as access tokens, events, files, threads, and others are represented via `HANDLE` objects on Windows \[[MSDN](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-MSDN)\]. Handle inheritance is a two-step process.  When obtaining a `HANDLE`, an option is given to specify whether the object is inheritable or not. This option is usually in the form of a `BOOL` parameter (as in the case of `OpenMutex()`), or a `SECURITY_DESCRIPTOR` parameter (as in the case of `CreateFile()`). When creating a process via the `CreateProcess()` family of APIs, a parameter is given specifying whether the spawned process will inherit handles previously flagged as being inheritable. Any handles that were opened as being inheritable will be opened in the child process using the same handle value and access privileges as in the parent process. The parent process can then alert the child process of the handle values via an inter-process communication mechanism, and the child process can use those values as though it had opened the handle \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/ms724466(v=vs.85).aspx)\].
When opening handles to securable resources or spawning child processes, prohibit handle inheritance by default to prevent accidental information leakage. If obtaining an inherited handle from a parent process, prevent leakage to subsequent child processes by duplicating the handle without inheritance.
## Noncompliant Code Example (Mutex)
This noncompliant code example attempts to open an existing mutex handle that can be inherited by a child process:
``` c
#include <Windows.h>
void func(void) {
  HANDLE hMutex = OpenMutex(MUTEX_ALL_ACCESS, TRUE, TEXT("Global\\CommonMutex"));
  if (!hMutex) {
    /* Handle error */
  }
}
```
Even if the process does not currently spawn child processes, this code example is noncompliant because future changes involving child processes could leak this handle accidentally.
## Compliant Solution (Mutex)
This compliant solution opens the same mutex without specifying the handle can be inherited by a child process:
``` c
#include <Windows.h>
void func(void) {
  HANDLE hMutex = OpenMutex(MUTEX_ALL_ACCESS, FALSE, TEXT("Global\\CommonMutex"));
  if (!hMutex) {
    /* Handle error */
  }
}
```
## Noncompliant Code Example (Further Inheritance)
In this noncompliant example, the child process is spawned and inherits a single file handle from its parent process. The first argument to the main function is the handle's integer value as a hexadecimal string. However, the child process is not validating that the handle is a valid file handle, and it is not restricting further inheritance of the handle. Additionally, a portability concern arises if the parent process and the child process are the same architecture (for example, if one is 32-bit and the other is 64-bit).
``` c
#include <Windows.h>
int CALLBACK WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR cmdLine, int show) {
  HANDLE hFile = (HANDLE)_strtoui64(cmdLine, NULL, 16);
  /* Continue working with the file */
}
```
## Compliant Solution (Further Inheritance)
This compliant solution receives the inherited handle via the command line but prevents further inheritance by duplicating the handle. It also ensures that the value passed is a valid `HANDLE` value. Then it validates the handle as a proper file handle by calling [`GetFileInformationByHandle()`](http://msdn.microsoft.com/en-us/library/windows/desktop/aa364952(v=vs.85).aspx). This solution also properly handles cross-architecture situations between the processes.
``` c
#include <Windows.h>
int CALLBACK WinMain(HINSTANCE hInstance, HINSTANCE hPrev, LPSTR cmdLine, int show) {
  HANDLE hUntrusted = (HANDLE)_strtoui64(cmdLine, NULL, 16);
  HANDLE hFile = NULL;
  BY_HANDLE_FILE_INFORMATION info;
  if (!DuplicateHandle(GetCurrentProcess(), hUntrusted, GetCurrentProcess(), &hFile,
                       0, FALSE, DUPLICATE_SAME_ACCESS | DUPLICATE_CLOSE_SOURCE)) {
    /* Handle error; possibly not even a valid handle */
  }
  if (!GetFileInformationByHandle(hFile, &info)) {
    /* Handle error; likely not a valid file handle */
    // Close the file handle since we no longer trust it.
    CloseHandle(hFile);
    hFile = NULL;
  }
  /* Continue working with the file */
}
```
## Noncompliant Code Example (`fopen()`)
By default, all files on Windows that are opened using `fopen()` will allow handle inheritance, and processes spawned via the `system()` API automatically inherit handles. In this noncompliant code example, `SomeProcess.exe` inherits the file handle for `SomeFile.txt`:
``` c
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  FILE *fp = fopen("SomeFile.txt", "rw");
  if (!fp) {
    return -1;
  }
  system("SomeProcess.exe");
  fclose(fp);
  return 0;
}
```
## Compliant Solution (`fopen()`)
In this compliant solution, the Windows-specific `'N'` mode parameter is passed  to the call to `fopen()`, which ensures the file is opened without allowing handle inheritance:
``` c
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  FILE *fp = fopen("SomeFile.txt", "rwN");
  if (!fp) {
    return -1;
  }
  system("SomeProcess.exe");
  fclose(fp);
  return 0;
}
```
## Risk Assessment
Leaking handles across process boundaries can leak information or cause denial-of-service attacks.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN03-C | High | Unlikely | Low | P9 | L2 |

## Related Guidelines

|  |  |
| ----|----|
| ; | ; |

## Bibliography

|  |  |
| ----|----|
| ; | ; |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151928) [](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152222)
