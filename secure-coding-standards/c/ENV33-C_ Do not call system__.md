The C Standard `system()` function executes a specified command by invoking an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) command processor, such as a UNIX shell or `CMD.EXE` in Microsoft Windows. The POSIX [popen()](http://pubs.opengroup.org/onlinepubs/9699919799/) and Windows [`_popen()`](https://msdn.microsoft.com/en-us/library/96ayss4b(v=vs.140).aspx) functions also invoke a command processor but create a pipe between the calling program and the executed command, returning a pointer to a stream that can be used to either read from or write to the pipe \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. 
Use of the system() function can result in exploitable vulnerabilities, in the worst case allowing execution of arbitrary system commands. Situations in which calls to system() have high risk include the following: 
-   When passing an unsanitized or improperly sanitized command string originating from a tainted source
-   If a command is specified without a path name and the command processor path name resolution mechanism is accessible to an attacker
-   If a relative path to an executable is specified and control over the current working directory is accessible to an attacker
-   If the specified executable program can be spoofed by an attacker
Do not invoke a command processor via system() or equivalent functions to execute a command. 
## Noncompliant Code Example
In this noncompliant code example, the `system()` function is used to execute `any_cmd` in the host environment.
``` c
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
enum { BUFFERSIZE = 512 };
void func(const char *input) {
  char cmdbuf[BUFFERSIZE];
  int len_wanted = snprintf(cmdbuf, BUFFERSIZE,
                            "any_cmd '%s'", input);
  if (len_wanted >= BUFFERSIZE) {
    /* Handle error */
  } else if (len_wanted < 0) {
    /* Handle error */
  } else if (system(cmdbuf) == -1) {
    /* Handle error */
  }
}
```
If this code is compiled and run with elevated privileges on a Linux system, for example, an attacker can create an account by entering the following string:
``` java
happy'; useradd 'attacker
```
The shell would interpret this string as two separate commands:
``` java
any_cmd 'happy';
useradd 'attacker'
```
and create a new user account that the attacker can use to access the compromised system.
This noncompliant code example also violates [STR02-C. Sanitize data passed to complex subsystems](STR02-C_%20Sanitize%20data%20passed%20to%20complex%20subsystems).
## Compliant Solution (POSIX)
In this compliant solution, the call to `system()` is replaced with a call to `execve()`. The `exec` family of functions does not use a full shell interpreter, so it is not vulnerable to command-injection attacks, such as the one illustrated in the noncompliant code example.
The `execlp()`, `execvp()`, and (nonstandard) `execvP()` functions duplicate the actions of the shell in searching for an executable file if the specified file name does not contain a forward slash character (`/`). As a result, they should be used without a forward slash character (`/`) only if the `PATH` environment variable is set to a safe value, as described in [ENV03-C. Sanitize the environment when invoking external programs](ENV03-C_%20Sanitize%20the%20environment%20when%20invoking%20external%20programs).
The `execl()`, `execle()`, `execv()`, and `execve()` functions do not perform path name substitution.
Additionally, precautions should be taken to ensure the external executable cannot be modified by an untrusted user, for example, by ensuring the executable is not writable by the user.
``` c
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <errno.h>
#include <stdlib.h>
void func(char *input) {
  pid_t pid;
  int status;
  pid_t ret;
  char *const args[3] = {"any_exe", input, NULL};
  char **env;
  extern char **environ;
  /* ... Sanitize arguments ... */
  pid = fork();
  if (pid == -1) {
    /* Handle error */
  } else if (pid != 0) {
    while ((ret = waitpid(pid, &status, 0)) == -1) {
      if (errno != EINTR) {
        /* Handle error */
        break;
      }
    }
    if ((ret == 0) ||
        !(WIFEXITED(status) && !WEXITSTATUS(status))) {
      /* Report unexpected child status */
    }
  } else {
    /* ... Initialize env as a sanitized copy of environ ... */
    if (execve("/usr/bin/any_cmd", args, env) == -1) {
      /* Handle error */
      _Exit(127);
    }
  }
}
```
This compliant solution is significantly different from the preceding noncompliant code example. First, `input` is incorporated into the `args` array and passed as an argument to `execve()`, eliminating concerns about buffer overflow or string truncation while forming the command string. Second, this compliant solution forks a new process before executing `"/usr/bin/any_cmd"` in the child process. Although this method is more complicated than calling `system()`, the added security is worth the additional effort.
The exit status of 127 is the value set by the shell when a command is not found, and POSIX recommends that applications should do the same. XCU, Section 2.8.2, of *Standard for Information Technology—Portable Operating System Interface (POSIX®), Base Specifications, Issue 7* \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\], says
> If a command is not found, the exit status shall be 127. If the command name is found, but it is not an executable utility, the exit status shall be 126. Applications that invoke utilities without using the shell should use these exit status values to report similar errors.

## Compliant Solution (Windows)
This compliant solution uses the Microsoft Windows [CreateProcess()](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682425(v=vs.85).aspx) API:
``` c
#include <Windows.h>
void func(TCHAR *input) {
  STARTUPINFO si = { 0 };
  PROCESS_INFORMATION pi;
  si.cb = sizeof(si);
  if (!CreateProcess(TEXT("any_cmd.exe"), input, NULL, NULL, FALSE,
                     0, 0, 0, &si, &pi)) {
    /* Handle error */
  }
  CloseHandle(pi.hThread);
  CloseHandle(pi.hProcess);
}
```
This compliant solution relies on the `input` parameter being non-`const`. If it were `const`, the solution would need to create a copy of the parameter because the `CreateProcess()` function can modify the command-line arguments to be passed into the newly created process.
This solution creates the process such that the child process does not inherit any handles from the parent process, in compliance with [WIN03-C. Understand HANDLE inheritance](WIN03-C_%20Understand%20HANDLE%20inheritance).
## Noncompliant Code Example (POSIX)
This noncompliant code invokes the C `system()` function to remove the `.config` file in the user's home directory.
``` c
#include <stdlib.h>
void func(void) {
  system("rm ~/.config");
}
```
If the vulnerable program has elevated privileges, an attacker can manipulate the value of the `HOME` environment variable such that this program can remove any file named `.config` anywhere on the system.
## Compliant Solution (POSIX)
An alternative to invoking the `system()` call to execute an external program to perform a required operation is to implement the functionality directly in the program using existing library calls. This compliant solution calls the POSIX [`unlink()`](http://pubs.opengroup.org/onlinepubs/9699919799/) function to remove a file without invoking the `system()` function \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)[\]](http://pubs.opengroup.org/onlinepubs/9699919799/)
``` c
#include <pwd.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
void func(void) {
  const char *file_format = "%s/.config";
  size_t len;
  char *pathname;
  struct passwd *pwd;
  /* Get /etc/passwd entry for current user */
  pwd = getpwuid(getuid());
  if (pwd == NULL) {
    /* Handle error */
  }
  /* Build full path name home dir from pw entry */
  len = strlen(pwd->pw_dir) + strlen(file_format) + 1;
  pathname = (char *)malloc(len);
  if (NULL == pathname) {
    /* Handle error */
  }
  int r = snprintf(pathname, len, file_format, pwd->pw_dir);
  if (r < 0 || r >= len) {
    /* Handle error */
  }
  if (unlink(pathname) != 0) {
    /* Handle error */
  }
  free(pathname);
}
```
The `unlink()` function is not susceptible to a symlink attack where the final component of `pathname `(the file name) is a symbolic link because `unlink()` will remove the symbolic link and not affect any file or directory named by the contents of the symbolic link. (See [FIO01-C. Be careful using functions that use file names for identification](FIO01-C_%20Be%20careful%20using%20functions%20that%20use%20file%20names%20for%20identification).)  While this reduces the susceptibility of the `unlink()` function to symlink attacks, it does not eliminate it.  The `unlink()` function is still susceptible if one of the directory names included in the `pathname` is a symbolic link.  This could cause the `unlink()` function to delete a similarly named file in a different directory.
## Compliant Solution (Windows)
This compliant solution uses the Microsoft Windows [SHGetKnownFolderPath()](http://msdn.microsoft.com/en-us/library/windows/desktop/bb762188(v=vs.85).aspx) API to get the current user's My Documents folder, which is then combined with the file name to create the path to the file to be deleted. The file is then removed using the [DeleteFile()](http://msdn.microsoft.com/en-us/library/windows/desktop/aa363915(v=vs.85).aspx) API.
``` c
#include <Windows.h>
#include <ShlObj.h>
#include <Shlwapi.h>
#if defined(_MSC_VER)
  #pragma comment(lib, "Shlwapi")
#endif
void func(void) {
  HRESULT hr;
  LPWSTR path = 0;
  WCHAR full_path[MAX_PATH];
  hr = SHGetKnownFolderPath(&FOLDERID_Documents, 0, NULL, &path);
  if (FAILED(hr)) {
    /* Handle error */
  }
  if (!PathCombineW(full_path, path, L".config")) {
    /* Handle error */
  }
  CoTaskMemFree(path);
  if (!DeleteFileW(full_path)) {
    /* Handle error */
  }
}
```
## Exceptions
ENV33-C-EX1: It is permissible to call `system()` with a null pointer argument to determine the presence of a command processor for the system.
##  Risk Assessments
If the command string passed to `system()`, `popen()`, or other function that invokes a command processor is not fully [sanitized](BB.-Definitions_87152273.html#BB.Definitions-sanitize), the risk of [exploitation](BB.-Definitions_87152273.html#BB.Definitions-exploit) is high. In the worst case scenario, an attacker can execute arbitrary system commands on the compromised machine with the privileges of the vulnerable process.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV33-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stdlib-use-system | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ENV33 |  |
| Clang | 3.9 | cert-env33-c | Checked by clang-tidy |
| CodeSonar | 8.3p0 | BADFUNC.PATH.SYSTEMIO.INJ.COMMAND | Use of systemCommand injection |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | DONT_CALL | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-env33-c |  |
| Helix QAC | 2024.4 | C5018C++5031 |  |
| Klocwork | 2024.4 | SV.CODE_INJECTION.SHELL_EXEC
 |  |
| LDRA tool suite | 9.7.1 | 588 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV33-a | The 'system()' function from the 'stdlib.h' or 'cstdlib' library should not be used with an argument other than '0' (null pointer) |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule ENV33-C | Checks for unsafe call to a system function (rule fully covered) |
| RuleChecker | 24.04 | stdlib-use-system | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S990 | Detects uses of "abort", "exit", "getenv" and "system" from <stdlib.h>; |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | ENV03-C. Sanitize the environment when invoking external programs. | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C++ Coding Standard | ENV02-CPP. Do not call system() if you do not need a command processor | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | IDS07-J. Sanitize untrusted data passed to the Runtime.exec() method | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Unquoted Search Path or Element [XZQ] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Calling system [syscall] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-88, Argument Injection or Modification | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-676 | 2017-05-18: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-88 and ENV33-C
Intersection( CWE-88, ENV33-C) =
Allowing an argument to be injected during a call to system()
CWE-88 = Intersection( CWE-88, ENV33-C, list) where list =
-   Allowing an argument to be injected during a call to a command interpreter besides system()
ENV33-C = Intersection( CWE-88, ENV33-C, list) where list =
-   Other exploits to a call to system(), which include:
-   Altering the pathname of the command to invoke (argv\[0\])
-   Injection of a second command
-   Redirection of standard input, output, or error
### CWE-78 and ENV33-C
ENV33-C = Union( CWE-78, list), where list =
-   Invoking system() with completely trusted arguments
### CWE-676 and ENV33-C
-   Independent( ENV33-C, CON33-C, STR31-C, EXP33-C, MSC30-C, ERR34-C)
-   ENV33-C forbids calling system().
-   CWE-676 does not indicate what functions are ‘potentially dangerous’; it only addresses strcpy() in its examples. Any C standard library function could be argued to be dangerous, and rebutted by saying that the function is safe when used properly. We will assume that CERT rules mapped to CWE-676 specify dangerous functions. So:
-   CWE-676 = Union( ENV33-C, list) where list =
-   Invocation of other dangerous functions, besides system().
## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, execXSH, System Interfaces, popen
XSH, System Interfaces, unlink |
| [Wheeler 2004] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152169) [](../c/Rule%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152370)
## Comments:

|  |
| ----|
| An empty environment is unfair to any_exe; it should include PATH, HOME, TZ and maybe a few more, at minimum.
We should not be using implicit int functions - like the compliant solution is.
Isn't there a rule about cleaning user input before using it -- this code violates that (that might be STR02-A).
There's still a puts() that would be better as perror().
Should the solution have the parent wait like the system() call does?
Should the solution deal with signals like system() probably does?
The non-compliant solution doesn't check the return from snprintf() as it should - which is just another thing that makes it non-compliant.
Suffice to say - more work needed before this is ready for prime time.;
                                        Posted by jonathan.leffler@gmail.com at Mar 19, 2008 15:42
                                     |
| Fixed all your issues. A few comments:
Sanitizing the environment or arguments is indeed covered more generally by STR02-A. Exactly how the env or args should be sanitized depends on the overall program design. Also consider that an attacker with shell access can always invoke programs directly with 'hostile' args and env, so sanitization may buy you nothing...it all depends ont the program design. As such, I added the 'sanitize parms' comment instead of doing anything more substantial 
Re signals: Good question. I guess if the exec'd command has special behavior wrt signals, and that special behavior is part of the design, then the example should catch signals & pass them to the child. Unless there is a specific vul wrt signals and 'exec', I don't think the examples should 'handle' signals.
                                        Posted by svoboda at Mar 20, 2008 13:01
                                     |
| Wietse Venema sez:
    if ((pid = fork()) == -1) {
    perror("fork error");
    }
    else if (pid != 0) {
    if (wait(0) == -1) {
        perror("Error waiting for child process");
    }

The example has two bugs:
1\) It may pick up the status from the wrong child. An attacker could exploit this race condition by 'exec'-ing the program from  
a process that already has a child, and have that child exit first.
2\) It ignores the child exit status. One could argue that this  
violates "ERR00-A. Detect errors by checking return values".
To fix:
``` java
    int status;
    pid_t waitpid;
    do {
    if (((waitpid = wait(&status)) < 0)
        /* error... */
    } while (waitpid != child_pid);
```
Use WIFEXITED() etc. to examine the status result.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2008 10:33
\| \|
Not sure where the "Wietse Venema sez" quote is from, since there's no comment on this page by anyone called Wietse Venema and the quote doesn't match the code on the actual page itself, which uses a waitpid() call and passes it the pid returned by fork().
The suggested "fix" is poor practice as it obtains and throws away the status for other children.
However, adding code to check the exit status with WIFEXITED() and WEXITSTATUS() is a good idea.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 17, 2008 07:30
\| \|
we sometimes get comments sent in by email.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 17, 2008 07:41
\| \|
Getting signals right is tricky.; For example, before the waitpid should be a reset of SIGINT, SIGQUIT, and any other signals that might have a signal handler function established, to SIG_IGN; but reset SIGCLD to SIG_DFL; restore the original state after the waitpid.  The execed process inherits the SIG_IGN and SIG_DFL states.  It is almost certainly an error to forward signals to the child process.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 17, 2008 20:39
\| \|
In terms of the CWE references: CWE 78 and 88 are indirect but you probably could make an argument for these references.; But the main reference here should probably be CWE 77.
![](images/icons/contenttypes/comment_16.png) Posted by azukich at Feb 21, 2010 14:18
\| \|
Why not just use popen()?
![](images/icons/contenttypes/comment_16.png) Posted by zhu_robin at Dec 25, 2012 01:44
\| \|
The POSIX [popen()](http://www.opengroup.org/onlinepubs/009695399/functions/popen.html) function also invokes a command processor.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 02, 2013 10:27
\| \|
The following recently updated paragraph is not correct:
Click here to expand...
The `unlink()` function is not susceptible to `file`-related race conditions (see [FIO01-C. Be careful using functions that use file names for identification](https://www.securecoding.cert.org/confluence/display/seccode/FIO01-C.+Be+careful+using+functions+that+use+file+names+for+identification)) because if `file` names a symbolic link, `unlink()` will remove the symbolic link named by `file` and not affect any file or directory named by the contents of the symbolic link.
The fact that;`unlink()` operates on symbolic links only reduces its susceptibility to FIO01-C, it does not eliminate it.  It is not susceptible as regards the final component of the pathname being a symbolic link, but it is still susceptible if the pathname contains a symbolic link in an earlier component, e.g. `/tmp/symlink_to_dir/somefile`.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 07, 2014 12:13
\| \|
A compliant solution using <http://pubs.opengroup.org/onlinepubs/9699919799/functions/posix_spawn.html>;may be helpful. Unix implementers are more likely to get details such as signal handlers and file descriptors correct if they use the modern API where such details are explicit. It also would provide more symmetry with the compliant Windows solution.
![](images/icons/contenttypes/comment_16.png) Posted by chris.newman at Apr 24, 2015 23:47
\| \|
I fixed some of this language.; Todo is to revisit the compliant solution.  In general, the appropriate solution to this problem is to drop privileges to the RUID.  Alternatively, we could canonicalize the filename and validate.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 28, 2015 09:46
\| \|
To get this to work without a 127 error code on Linux, I had to replace:
    char **env;
With:
    char * const env[] = {NULL};
![](images/icons/contenttypes/comment_16.png) Posted by samuelmarks at Apr 15, 2020 02:55
\| \|
The compliant solution does not explicitly initialize env, but does comment that env should be initialized to point to a sanitized copy of environ. That is, all environment variables in env that are not trusted should be eliminated or replaced with trusted values.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 15, 2020 10:55
\| \|
This feels a bit too strong to me. Other than functions that are complete disasters that can't be used safely at all (e.g., `gets()`), completely banning a standard function like this seems unnecessary, especially since it's safe if you control the command line and environment, and there's not a portable replacement for it.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:43
\| \|
So you're saying we shouldn't ban system() because it is not a \*complete\* disaster? :)
BTW controlling the environment is very hard, unless you simply erase all env vars first.
Not only that, but you must also control the default shell which is used to interpret your command. Using the exec system functions (or their Windows equivalents) at least bypasses the non-portability of how your platform's shell works.
We went over the 'should-this-be-a-rule' debate about 8 years ago when doing software audits. We definitely wanted static-analysis tools to catch every \*call\* to system(), even the ones that were (theoretically) secure. Partially because it is actually uncommon, and scanning all of them was tractible (far easier than hunting for buffer overflows). So we decided that we could make exceptions for the (relatively) few cases where system() was being called securely.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 09, 2020 09:00
\| \|
It's effectively impossible to use;`system()` securely because the programmer writing the call has no control over the environment in which the call is executed. So the code can look eminently reasonable, but (for instance) the PATH environment variable causes it to behave entirely differently without someone auditing the code being able to tell that's the case.
I don't typically like the "ban all uses of \<X\>" rules because they sometimes throw the baby out with the bath water, but hosted systems typically provide a more secure interface with greater degrees of control than `system()` allows for, so I think this blanket ban is reasonable given the security issues.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 09, 2020 09:18
\| \|
Perhaps we should add an exception similar to [FIO45-C-EX1](FIO45-C_%20Avoid%20TOCTOU%20race%20conditions%20while%20accessing%20files) then, to allow it where it can't weaken security because there's no security boundary to weaken. Maybe worded like this: a process that calls `system()` with the same privileges as the user who provided its environment, and where the non-hardcoded portion of its argument (if any) also came from the same user.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 09, 2020 15:29
\| \|
I guess I originally considered these two rules a bit differently. With;`system()`, the command interpreter can be different from what the programmer expected (depending on the OS) because it's possible to influence it outside of program code (e.g., symlink /bin/sh to something else). This means that the programmer writing the code and an auditor reading the code cannot know what the call to `system()` will **actually** do.
Re-reading FIO45-C-EX1, I sort of think the same issue applies there and maybe that exception should go away. For instance, the programmer and the auditor have no way to know whether the user executing the program will give the program additional privileges that make the TOCTOU bugs a security concern. So I think this exception makes that rule uncheckable (which we usually demote to being a recommendation).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 10, 2020 07:16
\| \|
First, FIO45-C is a very good analogy to this rule, so I'll consider that exception here:
FIO45-C-EX1 is correct in that you can often mitigate TOCTOU vulnerabilities by privilege minimization. But that doesn't make your program secure, it just makes it a less attractive target. If an auditor can discern this privilege minimization somehow, then they can verify that TOCTOU is not a problem...but they can't discern that from the code itself. So, in an audit, such code would still violate FIO45-C but be considered acceptable when run with minimal privileges.
So I've decided to remove FIO45-C-EX1. Thanks for the discussion.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 10, 2020 10:35
\| \|
Andrew Fuller says, via email:
> There is a bug in ENV33-C Compliant Solution (POSIX).Currently the POSIX compliant solution has this snippet:
>
> if ((ret != -1) &&  
> (!WIFEXITED(status) \|\| !WEXITSTATUS(status)) ) {  
> /\* Report unexpected child status \*/  
> }
>
> However, exit status 0 is actually the happy case, which in C equates to false. So an unexpected child status would be if WEXITSTATUS(status) is true (non-zero).
>
> Changing it to either "WEXITSTATUS(status)" (drop the "!") or "WEXITSTATUS(status) != EXIT_SUCCESS" would fix it.

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 30, 2020 12:33
\| \|
My response:
> You are correct that exit status 0 indicates no error, so our first ifcondition is wrong. As for the rest, my waitpid() manpage (for POSIX  
> Issue 7, 2018) says:
>
> WIFEXITED(stat_val)  
> Evaluates to a non-zero value if status was returned for a child  
> process that terminated normally.
>
> WEXITSTATUS(stat_val)  
> If the value of WIFEXITED(stat_val) is non-zero, this macro  
> evaluates to the low-order 8 bits of the status argument that the  
> child process passed to \_exit() or exit(), or the value the child  
> process returned from main().
>
> I would infer from the definition of WEXITSTATUS() that if WIFEXITED()  
> returns 0, the value of WEXITSTATUS() is unspecified (if specified it  
> should have been in an else clause in the paragraph). So we should  
> definitely call WIFEXITED() first. That said, WEXITSTATUS() returning  
> 0 indicates that the child process had no error to report. So we can  
> ignore an error only if WIFEXITED returns non-zero (child process  
> exited) and WEXITSTATUS() is 0 (child process reports no error).
>
> Furthermore, before calling waitpid(), we should set errno to 0,  
> according to CERT rule ERR30-C.
>
> I have updated the code example based on your feedback. Thanks!

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 30, 2020 12:34
\| \|
Andrew Fuller responded:
> Thanks for the thorough reply, David.
>
> I concur with your analysis of WIFEXITED and WEXITSTATUS. And thanks for catching the errno not being set, too.
>
> In the edit I see that:
>
> if ((ret != -1) &&
>
> has been changed to:
>
> if ((ret != 0) \|\|
>
>   
> which isn't quite the same. According to the waitpid manpage (as shipped on Ubuntu):
>
> RETURN VALUE  
> waitpid(): on success, returns the process ID of the child whose state has changed; if WNOHANG was specified and one or more child(ren) specified by pid exist, but have not yet  
> changed state, then 0 is returned. On error, -1 is returned.
>
> So in the success case the return value should be non-zero. In this example we're not setting WNOHANG, so presumably a return value of 0 would be out-of-spec. And a return value of -1 would have continued the loop above. Right now on successful exit we'll short circuit into the error handling. This could instead be:
>
> if ((ret == 0) \|\|
>
>   
> Oh, and thanks for the whole SEI CERT resource in general. Much appreciated!

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 30, 2020 12:35
\| \|
My response:
> Thanks for your response.; WRT the return value of waitpid(), my POSIX standard concurs with your Ubuntu manpage. After more study, I agree with your assessment of the first if clause, and I have updated the code as you suggest. 

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 30, 2020 12:36
\| \|
Hi there,
It seems all the examples are about \`system\` function, but the rule also mentions functions like \`popen\` and \`\_popen\`,; so shall we also report defects for these functions? Please help clarify, thanks in advance!
![](images/icons/contenttypes/comment_16.png) Posted by zhuoc at Jun 02, 2021 22:46
\| \|
The popen() and \_popen() functions are specific to POSIX. Which is technically outside the scope of this rule (It is specific to standard C). If you are reporting defects in functions that may run on a POSIX system, then by all means report calls to peopen() and \_popen()...otherwise you can ignore them.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 03, 2021 08:58
\|
