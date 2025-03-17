Standard `FILE` objects and their underlying representation (file descriptors on POSIX platforms or handles elsewhere) are a finite resource that must be carefully managed. The number of files that an [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) guarantees may be open simultaneously is bounded by the `FOPEN_MAX` macro defined in `<stdio.h>`. The value of the macro is guaranteed to be at least 8. Consequently, portable programs must either avoid keeping more than `FOPEN_MAX` files at the same time or be prepared for functions such as `fopen()` to fail due to resource exhaustion.
Failing to close files when they are no longer needed may allow attackers to exhaust, and possibly manipulate, system resources. This phenomenon is sometimes called *file descriptor leakage*, although file pointers may also be used as an attack vector. In addition, keeping files open longer than necessary increases the risk that data written into in-memory file buffers will not be flushed in the event of [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination). To prevent file descriptor leaks and to guarantee that any buffered data will be flushed into permanent storage, files must be closed when they are no longer needed.
The behavior of a program is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when it uses the value of a pointer to a `FILE` object after the associated file is closed (see [undefined behavior 153](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_153).) Programs that close the standard streams (especially `stdout` but also `stderr` and `stdin`) must be careful not to use the stream objects in subsequent function calls, particularly those that implicitly operate on such objects (such as `printf()`, `perror()`, and `getc()`).
## Noncompliant Code Example
In this noncompliant code example, derived from a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in OpenBSD's `chpass` program \[[NAI 1998](AA.-Bibliography_87152170.html#AA.Bibliography-NAI98)\], a file containing sensitive data is opened for reading. The `get_validated_editor()` function retrieves the registered editor from the `EDITOR` environment variable and [sanitizes](BB.-Definitions_87152273.html#BB.Definitions-sanitize) it to be a valid editor in accordance with [FIO02-C. Canonicalize path names originating from tainted sources.](FIO02-C_%20Canonicalize%20path%20names%20originating%20from%20tainted%20sources) The function returns a command for invoking the editor  which is subsequently passed as a command `system()` function. If the `system()` function is implemented in a way that spawns a child process, then the child process could inherit the file descriptors opened by its parent. If this happens, as it does in POSIX systems, the child process will be able to access the contents of the potentially sensitive file called `file_name`.
``` c
#include <stdio.h>
#include <stdlib.h>
extern const char *get_validated_editor(void);
void func(const char *file_name) {
  FILE *f;
  const char *editor;
  f = fopen(file_name, "r");
  if (f == NULL) {
    /* Handle error */
  }
  editor = get_validated_editor();
  if (editor == NULL) {
    /* Handle error */
  }
  if (system(editor) == -1) {
    /* Handle error */
  }
}
```
If the command returned by get_validated_editor() will always be a simple path (such as /usr/bin/vim), and runs on a POSIX system, this program could be strengthened by using a call to execve() rather than system(), in accordance with ENV33-C. Do not call system().
On UNIX-based systems, child processes are typically spawned using a form of `fork()` and `exec()`, and the child process always inherits from its parent any file descriptors that do not have the close-on-exec flag set. Under Microsoft Windows, file-handle inheritance is determined on a per-file and per-spawned process basis. See [WIN03-C. Understand HANDLE inheritance](WIN03-C_%20Understand%20HANDLE%20inheritance) for more information.
## Compliant Solution
In this compliant solution, `file_name` is closed before launching the editor:
``` c
#include <stdio.h>
#include <stdlib.h>
extern const char *get_validated_editor(void);
void func(const char *file_name) {
  FILE *f;
  const char *editor;
  f = fopen(file_name, "r");
  if (f == NULL) {
    /* Handle error */
  }
  fclose(f);
  f = NULL;
  editor = get_validated_editor();
  if (editor == NULL) {
    /* Handle error */
  }
  /* Sanitize environment before calling system() */
  if (system(editor) == -1) {
    /* Handle error */
  }
}
```
## Compliant Solution (POSIX)
Sometimes it is not practical for a program to close all active file descriptors before issuing a system call such as `system()` or `exec()`. An alternative on POSIX systems is to use the `FD_CLOEXEC` flag, or `O_CLOEXEC` when available, to set the close-on-exec flag for the file descriptor:
``` c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
extern const char *get_validated_editor(void);
void func(const char *file_name) {
  int flags;
  char *editor;
  int fd = open(file_name, O_RDONLY);
  if (fd == -1) {
    /* Handle error */
  }
  flags = fcntl(fd, F_GETFD);
  if (flags == -1) {
    /* Handle error */
  }
  if (fcntl(fd, F_SETFD, flags | FD_CLOEXEC) == -1) {
    /* Handle error */
  }
  editor = get_validated_editor();
  if (editor == NULL) {
    /* Handle getenv() error */
  }
  if (system(editor) == -1) {
    /* Handle error */
  }
}
```
## Compliant Solution (Linux)
Some systems (such as those with Linux kernel versions 2.6.23 and later) have an `O_CLOEXEC` flag that provides the close-on-exec function directly in `open()`. This flag is required by IEEE Std 1003.1 \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. In multithreaded programs, this flag should be used, if possible, because it prevents a timing hole between `open()` and `fcntl()` when using `FD_CLOEXEC`, during which another thread can create a child process while the file descriptor does not have close-on-exec set.
``` c
#include <stdio.h>
#include <stdlib.h>
extern const char *get_validated_editor(void);
void func(const char *file_name) {
  char *editor;
  int fd = open(file_name, O_RDONLY | O_CLOEXEC);
  if (fd == -1) {
    /* Handle error */
  }
  editor = get_validated_editor();
  if (editor == NULL) {
    /* Handle error */
  }
  if (system(editor) == -1) {
    /* Handle error */
  }
}
```
## Risk Assessment
Failing to properly close files may allow unintended access to, or exhaustion of, system resources.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO22-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  |  |
| Klocwork | 2024.4 | RH.LEAK |  |
| LDRA tool suite | 9.7.1 | 49 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO22-a | Ensure resources are freed |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO22-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | WIN03-C. Understand HANDLE inheritance; |
| SEI CERT C++ Coding Standard | FIO51-CPP. Close files when they are no longer needed |
| CERT Oracle Secure Coding Standard for Java | FIO04-J. Release resources when they are no longer needed |
| MITRE CWE | CWE-403, UNIX file descriptor leakCWE-404, Improper resource shutdown or release
CWE-770, Allocation of resources without limits or throttling |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 10, "UNIX Processes" ("File Descriptor Leaks," pp.;582–587) |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, open |
| [MSDN] | Inheritance (Windows) |
| [NAI 1998] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152425) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151957)
## Comments:

|  |
| ----|
| Why wouldn't one extend this to reset all resources associated with the resource?
fclose(f); f = 0;Â;

How is a FILE pointer or a void\* malloc pointer or a file descriptor or anything else different?
It's clear that closing the file means that there is no handle to the resource available for a bad guy to fool with, but unless the statement after "fclose" is "return", it's wise to zero out the released resource.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 01:31
\| \|
Wietse Venema sez:
This provides incomplete advice (close files before spawning a child process).
In many systems, such as my own Postfix mail server, it is not  
practical to close files/sockets/etc. Instead, the program arranges  
that files/sockets have the close-on-exec flag set on UNIX, and its  
equivalent on Windows.
``` java
#include <fcntl.h>
#define PATTERN FD_CLOEXEC
/* close_on_exec - set/clear close-on-exec flag */
int     close_on_exec(int fd, int on)
{
    int     flags;
    if ((flags = fcntl(fd, F_GETFD, 0)) < 0)
        /* error... */
    if (fcntl(fd, F_SETFD, on ? flags | PATTERN : flags & ~PATTERN) < 0)
        /* error... */
    ...
}
```
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2008 10:23
\| \|
If threads are spawning processes then you have even bigger issues.
The open/fcntl interfaces, and the connections (or lack thereof) between their flag bits, are poorly designed (due to compatibility with early implementations) and really should be re-engineered (using different names, please).; Sort of like Plan 9 did with the fork-to-rfork redesign.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 17, 2008 18:32
\|
