The principle of least privilege states that every program and every user of the system should operate using the least set of privileges necessary to complete the job \[[Saltzer 1974](AA.-Bibliography_87152170.html#AA.Bibliography-Saltzer74), [Saltzer 1975](AA.-Bibliography_87152170.html#AA.Bibliography-Saltzer75)\]. The Build Security In website \[[DHS 2006](AA.-Bibliography_87152170.html#AA.Bibliography-DHS06)\] provides additional definitions of this principle. Executing with minimal privileges mitigates against exploitation in case a vulnerability is discovered in the code.
## Noncompliant Code Example
An application may spawn another process as part of its normal course of action. On Windows, the newly-spawned process automatically receives the same privileges as the parent process \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425(v=vs.85).aspx)\]. By allowing the child process to run in the same security context as the parent process, the attack surface for the application is extended to the child process. Furthermore, this example allows the child process to inherit handles from the parent process by passing `TRUE` to the `bInheritsHandles` parameter.
``` c
#include <Windows.h>
void launch_notepad(void) {
  PROCESS_INFORMATION pi;
  STARTUPINFO si;
  ZeroMemory(&si, sizeof(si));
  si.cb = sizeof( si );
  if (CreateProcess(TEXT("C:\\Windows\\Notepad.exe"), NULL, NULL, NULL, TRUE,
                    0, NULL, NULL, &si, &pi )) {
    /* Process has been created; work with the process and wait for it to
       terminate. */
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
  }
}
```
It is possible that the act of calling `launch_notepad()` will give the user an elevated Notepad application (from which the user could execute Explorer.exe), allowing the user access to all user's files, change system settings, and so on.
## Compliant Solution
By using the Windows Integrity Mechanism \[[MSDN](http://msdn.microsoft.com/en-us/library/bb625963.aspx)\] when creating the process, you can assign an integrity level to the launched child process. Doing so allows you to execute the child process with a specific set of privileges instead of defaulting to the parent process's security level.
``` c
#include <Windows.h>
#include <sddl.h>
static void launch_notepad_as_user(HANDLE token) {
  PROCESS_INFORMATION pi;
  STARTUPINFO si;
  ZeroMemory(&si, sizeof(si));
  si.cb = sizeof( si );
  if (CreateProcessAsUser(token, TEXT("C:\\Windows\\Notepad.exe"), NULL, NULL,
                          NULL, FALSE, 0, NULL, NULL, &si, &pi )) {
    /* Process has been created; work with the process and wait for it to
       terminate. */
    WaitForSingleObject(pi.hProcess, INFINITE);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
  }
}
static BOOL adjust_token_integrity_level(HANDLE token, const char *sid) {
  /* Convert the string SID to a SID *, then adjust the token's
     privileges. */
  BOOL ret;
  PSID psd = NULL;
  if (ConvertStringSidToSidA(sid, &psd)) {
    TOKEN_MANDATORY_LABEL tml;
    ZeroMemory(&tml, sizeof(tml));
    tml.Label.Attributes = SE_GROUP_INTEGRITY;
    tml.Label.Sid = psd;
    ret = SetTokenInformation(token, TokenIntegrityLevel, &tml,
                              sizeof(tml) + GetLengthSid(psd));
    LocalFree(psd);
  }
  return ret;
}
void launch_notepad(void) {
  /* Low level; see table for integrity level string names */
  const char *requested_sid = "S-1-16-4096";
  HANDLE token_cur, token_dup;
  /* Get the current process' security token as a starting point, then modify
     a duplicate so that it runs with a fixed integrity level. */
  if (OpenProcessToken(GetCurrentProcess(), TOKEN_DUPLICATE |
                                            TOKEN_ADJUST_DEFAULT |
                                            TOKEN_QUERY |
                                            TOKEN_ASSIGN_PRIMARY,
                                            &token_cur)) {
    if (DuplicateTokenEx(token_cur, 0, NULL, SecurityImpersonation,
                         TokenPrimary, &token_dup)) {
      if (adjust_token_integrity_level(token_dup, requested_sid))
        launch_notepad_as_user(token_dup);
      CloseHandle(token_dup);
    }
    CloseHandle(token_cur);
  }
}
```
The compliant solution demonstrates how to launch notepad.exe using a low integrity level, regardless of what privilege level the parent process is running from. It also disallows handle inheritance by passing `FALSE` to the `bInheritsHandles` parameter, because notepad.exe does not require access to any of the process's handles.
Possible values for the integrity level SID strings are listed in the following table:

| Integrity level SID | Name |
| ----|----|
| S-1-16-4096 | Mandatory Label\Low Mandatory Level |
| S-1-16-8192 | Mandatory Label\Medium Mandatory Level |
| S-1-16-12288 | Mandatory Label\High Mandatory Level |
| S-1-16-16384 | Mandatory Label\System Mandatory Level |

## Risk Assessment
Failure to follow the principle of least privilege may allow exploits to execute with elevated privileges.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN02-C | High | Likely | High | P9 | L2 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.CREATEPROCESSBADFUNC.CREATETHREAD | Use of CreateProcessUse of CreateThread |
| PC-lint Plus | 1.4 | 586 | Fully supported |

## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772 | Adherence to Least Privilege [XYN] |
| MITRE CWE | CWE-250, Execution with unnecessary privilegesCWE-272, Least privilege violation |

## Bibliography

|  |  |
| ----|----|
| [Saltzer 1974] |  |
| [Saltzer 1975] |  |
| [DHS 2006] | Least Privilege  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152032)[](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152035)
## Comments:

|  |
| ----|
| If I recall correctly, the integrity levels solution would only work on Windows Vista and up. If this is the case, would it be worth mentioning the OS requirement?Windows XP is pretty close to end of extended support, so it might not be necessary.
                                        Posted by jloo at Jul 09, 2013 12:04
                                     |
| You are correct, but as for mentioning it, I think the comments are fine.; XP is so antiquated and the APIs are documented.  I am not strongly tied one way or the other though.
                                        Posted by aballman at Jul 09, 2013 12:14
                                     |
| Aaron Ballman "Follow the principle of least privilege" is a very vague sort of recommendation. It is better to have more specific, actionable guidelines. At least based on the example here, I think your rule might be "assign an integrity level to the launched child process".; I'm guessing, however, that this advice is not universally applicable & that there are particular circumstances in which this applies, probably something along the lines of "when spawning a child process that does not require the same privileges as the parent process".I'm on the fence about if this should be a rule or a guideline.  To be a rule, an automated analysis tool or manual auditor must be able to tell if the rule has been violated.  I suppose one way to do this would be to inspect the code for the spawned process to determine if it requires the privileges of the parent process.  That is probably not viable in the general case, because you probably don't have the source for the program you are spawning.  Guideline?
                                        Posted by rcs at Aug 01, 2013 10:31
                                     |
| There's basically no way we can automate this guideline because we have no way of knowing what privileges the child process requires.; So recommendation probably makes more sense than rule. As for the title, I agree that it's a bit vague.  But the guideline encompasses two distinct situations (privileges of the child process, process handle inheritance).  I was toying with splitting handle inheritance out into its own guideline, but it'd be awfully small and the code example would not be drastically different (basically, the guideline is telling the user to pass FALSE to bInheritsHandles when spawning off a child process, unless the child needs to inherit handles for some reason (which is rather rare).  In both cases, it's related to least privileges guidance.
                                        Posted by aballman at Aug 01, 2013 10:37
                                     |
| Restrict privileges when spawning child processes?If someone were getting ready to spawn a child process, you would want it obvious from the title that the guideline might contain some relevant advice.;
                                        Posted by rcs at Aug 01, 2013 11:06
                                     |
| I like it!; Changed to the new title.
                                        Posted by aballman at Aug 01, 2013 11:14
                                     |

