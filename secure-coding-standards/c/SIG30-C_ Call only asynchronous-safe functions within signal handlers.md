Call only [asynchronous-safe functions](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safefunction) within signal handlers. For [strictly conforming](BB.-Definitions_87152273.html#BB.Definitions-strictlyconforming) programs, only the C standard library functions `abort()`, `_Exit()`, `quick_exit()`, and `signal()` can be safely called from within a signal handler. 
The C Standard, 7.14.1.1, paragraph 5 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states that if the signal occurs other than as the result of calling the `abort()` or `raise()` function, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if
> If the signal occurs other than as the result of calling the abort or raise function, the behavior is undefined if the signal handler refers to any object with static or thread storage duration that is not a lock-free atomic object and that is not declared with the constexpr storage-class specifier other than by assigning a value to an object declared as volatile sig_atomic_t, or the signal handler calls any function in the standard library other than
>
> —  the abort function,
>
> —  the \_Exit function,
>
> —  the quick_exit function,
>
> —  the functions in (except where explicitly stated otherwise) when the atomic arguments are lock-free,
>
> —  the atomic_is_lock_free function with any atomic argument, or
>
> —  the signal function with the first argument equal to the signal number corresponding to the signal that caused the invocation of the handler. Furthermore, if such a call to the signal function results in a SIG_ERR return, the object designated by errno has an indeterminate representation.294)

Implementations may define a list of additional asynchronous-safe functions. These functions can also be called within a signal handler. This restriction applies to library functions as well as application-defined functions.
According to the C Rationale, 7.14.1.1 \[[C99 Rationale 2003](AA.-Bibliography_87152170.html#AA.Bibliography-C992003)\],
> When a signal occurs, the normal flow of control of a program is interrupted. If a signal occurs that is being trapped by a signal handler, that handler is invoked. When it is finished, execution continues at the point at which the signal occurred. This arrangement can cause problems if the signal handler invokes a library function that was being executed at the time of the signal.

In general, it is not safe to invoke I/O functions from within signal handlers. Programmers should ensure a function is included in the list of an implementation's asynchronous-safe functions for all implementations the code will run on before using them in signal handlers.
## Noncompliant Code Example
In this noncompliant example, the C standard library functions `fputs()` and `free()` are called from the signal handler via the function `log_message()`. Neither function is [asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safefunction).
``` c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
enum { MAXLINE = 1024 };
char *info = NULL;
void log_message(void) {
  fputs(info, stderr);
}
void handler(int signum) {
  log_message();
  free(info);
  info = NULL;
}
int main(void) {
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* Handle error */
  }
  info = (char *)malloc(MAXLINE);
  if (info == NULL) {
    /* Handle Error */
  }
  while (1) {
    /* Main loop program code */
    log_message();
    /* More program code */
  }
  return 0;
}
```
## Compliant Solution
Signal handlers should be as concise as possible—ideally by unconditionally setting a flag and returning. This compliant solution sets a flag of type `volatile sig_atomic_t` and returns; the `log_message()` and `free()` functions are called directly from `main()`:
``` c
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
enum { MAXLINE = 1024 };
volatile sig_atomic_t eflag = 0;
char *info = NULL;
void log_message(void) {
  fputs(info, stderr);
}
void handler(int signum) {
  eflag = 1;
}
int main(void) {
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* Handle error */
  }
  info = (char *)malloc(MAXLINE);
  if (info == NULL) {
    /* Handle error */
  }
  while (!eflag) {
    /* Main loop program code */
    log_message();
    /* More program code */
  }
  log_message();
  free(info);
  info = NULL;
  return 0;
}
```
## Noncompliant Code Example (`longjmp()`)
Invoking the `longjmp()` function from within a signal handler can lead to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if it results in the invocation of any non-[asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safe) functions. Consequently, neither `longjmp()` nor the POSIX `siglongjmp()` functions should ever be called from within a signal handler.
This noncompliant code example is similar to a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in an old version of Sendmail \[[VU #834865](http://www.kb.cert.org/vuls/id/834865)\]. The intent is to execute code in a `main()` loop, which also logs some data. Upon receiving a `SIGINT`, the program transfers out of the loop, logs the error, and terminates.
However, an attacker can [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) this noncompliant code example by generating a `SIGINT` just before the second `if` statement in `log_message()`. The result is that `longjmp()` transfers control back to `main()`, where `log_message()` is called again. However, the first `if` statement would not be executed this time (because `buf` is not set to `NULL` as a result of the interrupt), and the program would write to the invalid memory location referenced by `buf0`.
``` c
#include <setjmp.h>
#include <signal.h>
#include <stdlib.h>
enum { MAXLINE = 1024 };
static jmp_buf env;
void handler(int signum) {
  longjmp(env, 1);
}
void log_message(char *info1, char *info2) {
  static char *buf = NULL;
  static size_t bufsize;
  char buf0[MAXLINE];
  if (buf == NULL) {
    buf = buf0;
    bufsize = sizeof(buf0);
  }
  /*
   * Try to fit a message into buf, else reallocate
   * it on the heap and then log the message.
   */
  /* Program is vulnerable if SIGINT is raised here */
  if (buf == buf0) {
    buf = NULL;
  }
}
int main(void) {
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* Handle error */
  }
  char *info1;
  char *info2;
  /* info1 and info2 are set by user input here */
  if (setjmp(env) == 0) {
    while (1) {
      /* Main loop program code */
      log_message(info1, info2);
      /* More program code */
    }
  } else {
    log_message(info1, info2);
  }
  return 0;
}
```
## Compliant Solution
In this compliant solution, the call to `longjmp()` is removed; the signal handler sets an error flag instead:
``` c
#include <signal.h>
#include <stdlib.h>
enum { MAXLINE = 1024 };
volatile sig_atomic_t eflag = 0;
void handler(int signum) {
  eflag = 1;
}
void log_message(char *info1, char *info2) {
  static char *buf = NULL;
  static size_t bufsize;
  char buf0[MAXLINE];
  if (buf == NULL) {
    buf = buf0;
    bufsize = sizeof(buf0);
  }
  /*
   * Try to fit a message into buf, else reallocate
   * it on the heap and then log the message.
   */
  if (buf == buf0) {
    buf = NULL;
  }
}
int main(void) {
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* Handle error */
  }
  char *info1;
  char *info2;
  /* info1 and info2 are set by user input here */
  while (!eflag) {
    /* Main loop program code */
    log_message(info1, info2);
    /* More program code */
  }
  log_message(info1, info2);
  return 0;
}
```
## Noncompliant Code Example (raise())
In this noncompliant code example, the `int_handler()` function is used to carry out tasks specific to `SIGINT` and then raises `SIGTERM`. However, there is a nested call to the `raise()` function, which is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
#include <signal.h>
#include <stdlib.h>
void term_handler(int signum) {
  /* SIGTERM handler */
}
void int_handler(int signum) {
  /* SIGINT handler */
  if (raise(SIGTERM) != 0) {
    /* Handle error */
  }
}
int main(void) {
  if (signal(SIGTERM, term_handler) == SIG_ERR) {
    /* Handle error */
  }
  if (signal(SIGINT, int_handler) == SIG_ERR) {
    /* Handle error */
  }
  /* Program code */
  if (raise(SIGINT) != 0) {
    /* Handle error */
  }
  /* More code */
  return EXIT_SUCCESS;
}
```
## Compliant Solution
In this compliant solution, `int_handler()` invokes `term_handler()` instead of raising `SIGTERM`: 
``` c
#include <signal.h>
#include <stdlib.h>
void term_handler(int signum) {
  /* SIGTERM handler */
}
void int_handler(int signum) {
  /* SIGINT handler */
  /* Pass control to the SIGTERM handler */
  term_handler(SIGTERM);
}
int main(void) {
  if (signal(SIGTERM, term_handler) == SIG_ERR) {
    /* Handle error */
  }
  if (signal(SIGINT, int_handler) == SIG_ERR) {
    /* Handle error */
  }
  /* Program code */
  if (raise(SIGINT) != 0) {
    /* Handle error */
  }
  /* More code */
  return EXIT_SUCCESS;
}
```
## Implementation Details
### POSIX
The following table from the POSIX standard \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] defines a set of functions that are [asynchronous-signal-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safefunction). Applications may invoke these functions, without restriction, from a signal handler.

|  |  |  |  |
| ----|----|----|----|
| _Exit() | fexecve() | posix_trace_event() | sigprocmask() |
| _exit() | fork() | pselect() | sigqueue() |
| abort() | fstat() | pthread_kill() | sigset() |
| accept() | fstatat() | pthread_self() | sigsuspend() |
| access() | fsync() | pthread_sigmask() | sleep() |
| aio_error() | ftruncate() | raise() | sockatmark() |
| aio_return() | futimens() | read() | socket() |
| aio_suspend() | getegid() | readlink() | socketpair() |
| alarm() | geteuid() | readlinkat() | stat() |
| bind() | getgid() | recv() | symlink() |
| cfgetispeed() | getgroups() | recvfrom() | symlinkat() |
| cfgetospeed() | getpeername() | recvmsg() | tcdrain() |
| cfsetispeed() | getpgrp() | rename() | tcflow() |
| cfsetospeed() | getpid() | renameat() | tcflush() |
| chdir() | getppid() | rmdir() | tcgetattr() |
| chmod() | getsockname() | select() | tcgetpgrp() |
| chown() | getsockopt() | sem_post() | tcsendbreak() |
| clock_gettime() | getuid() | send() | tcsetattr() |
| close() | kill() | sendmsg() | tcsetpgrp() |
| connect() | link() | sendto() | time() |
| creat() | linkat() | setgid() | timer_getoverrun() |
| dup() | listen() | setpgid() | timer_gettime() |
| dup2() | lseek() | setsid() | timer_settime() |
| execl() | lstat() | setsockopt() | times() |
| execle() | mkdir() | setuid() | umask() |
| execv() | mkdirat() | shutdown() | uname() |
| execve() | mkfifo() | sigaction() | unlink() |
| faccessat() | mkfifoat() | sigaddset() | unlinkat() |
| fchdir() | mknod() | sigdelset() | utime() |
| fchmod() | mknodat() | sigemptyset() | utimensat() |
| fchmodat() | open() | sigfillset() | utimes() |
| fchown() | openat() | sigismember() | wait() |
| fchownat() | pause() | signal() | waitpid() |
| fcntl() | pipe() | sigpause() | write() |
| fdatasync() | poll() | sigpending() | ; |

All functions not listed in this table are considered to be unsafe with respect to signals. In the presence of signals, all POSIX functions behave as defined when called from or interrupted by a signal handler, with a single exception: when a signal interrupts an unsafe function and the signal handler calls an unsafe function, the behavior is undefined.
The C Standard, 7.14.1.1, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> If the signal occurs as the result of calling the abort or raise function, the signal handler shall not call the raise function.

However, in the description of `signal()`, POSIX \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] states
> This restriction does not apply to POSIX applications, as POSIX.1-2008 requires `raise()` to be async-signal-safe.

See also [undefined behavior 131.](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_131) 
### OpenBSD
The OpenBSD [signal()](http://www.openbsd.org/cgi-bin/man.cgi?query=signal) manual page lists a few additional functions that are asynchronous-safe in OpenBSD but "probably not on other systems" \[[OpenBSD](AA.-Bibliography_87152170.html#AA.Bibliography-OpenBSD)\], including `snprintf()`, `vsnprintf()`, and `syslog_r()` but only when the `syslog_data struct` is initialized as a local variable.
## Risk Assessment
Invoking functions that are not [asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safefunction) from within a signal handler is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG30-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | signal-handler-unsafe-call | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-SIG30 |  |
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| Compass/ROSE |  |  | Can detect violations of the rule for single-file programs |
| Cppcheck Premium | 24.11.0 | premium-cert-sig30-c |  |
| Helix QAC | 2024.4 | C2028, C2030 |  |
| LDRA tool suite | 9.7.1 | 88 D, 89 D; | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG30-a | Properly define signal handlers |
| PC-lint Plus | 1.4 | 2670, 2761 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule SIG30-C | Checks for function called from signal handler not asynchronous-safe (rule fully covered) |
| RuleChecker | 24.04 | signal-handler-unsafe-call | Partially checked |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
For an overview of software vulnerabilities resulting from improper signal handling, see Michal Zalewski's paper "Delivering Signals for Fun and Profit" \[[Zalewski 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Zalewski01)\].
CERT Vulnerability Note [VU #834865](http://www.kb.cert.org/vuls/id/834865), "Sendmail signal I/O race condition," describes a vulnerability resulting from a violation of this rule. Another notable case where using the `longjmp()` function in a signal handler caused a serious vulnerability is [wu-ftpd 2.4](http://seclists.org/bugtraq/1997/Jan/0011.html) \[[Greenman 1997](AA.-Bibliography_87152170.html#AA.Bibliography-Greenman97)\]. The effective user ID is set to 0 in one signal handler. If a second signal interrupts the first, a call is made to `longjmp()`, returning the program to the main thread but without lowering the user's privileges. These escalated privileges can be used for further exploitation.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961:2013 | Calling functions in the C Standard Library other than abort, _Exit, and signal from within a signal handler [asyncsig] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-479, Signal Handler Use of a Non-reentrant Function | 2017-07-10: CERT: Exact |

## Bibliography

|  |  |
| ----|----|
| [C99 Rationale 2003] | Subclause 5.2.3, "Signals and Interrupts"Subclause 7.14.1.1, "The signal Function" |
| [Dowd 2006] | Chapter 13, "Synchronization and State" |
| [Greenman 1997] |  |
| [IEEE Std 1003.1:2013]  | XSH, System Interfaces, longjmpXSH, System Interfaces, raise |
| [ISO/IEC 9899:2024] | 7.14.1.1, "The signal Function" |
| [OpenBSD] | signal() Man Page |
| [VU #834865] |  |
| [Zalewski 2001] | "Delivering Signals for Fun and Profit" |

------------------------------------------------------------------------
[](../c/Rule%2011_%20Signals%20_SIG_) [](../c/Rule%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152213)
adjust column widths
## Comments:

|  |
| ----|
| You might also want to note that threading and signal handling don't mix. The signal() or pthread() man page (I think signal's man page) specifically says that the use of threading mechanisms within a signal handler can essentially break the application
                                        Posted by mdowd at Jul 10, 2007 19:44
                                     |
| Mitigation Strategies
Static Analysis
Compliance with this rule can be checked using structural static analysis checkers using the following algorithm:
    Assume an initial list of asynchronous-safe functions. This list would be specific to each OS, although POSIX does require a set of functions to be asynchronous-safe.
    Add all application-defined functions that satisfy the asynchronous-safe property to the asynchronous-safe function list. Functions satisfy the asynchronous-safe property if they (a) call only functions in the list of asynchronous-safe functions and (b) do not reference or modify external variables except to assign a value to a volatile static variable of sig_atomic_t type which can be written uninterruptedly. This handles the interprocedural case of calling a function in a signal handler that is itself, an asynchronous-safe function.
    Traverse the abstract syntax tree (AST) to identify function calls to the signal function signal(int, void (*f)(int)).
    At each function call to signal(int, void (*f)(int)) get the second argument from the argument list. To make sure that this is not an overloaded function the function type signature is evaluated and/or the location of the declaration of the function is verified to be from the correct file (because this is not a link-time analysis it is not possible to test the library implementation).  Any definition for signal() in the application is suspicious, because it should be in a library.
    Perform a nested query on the registered signal handler to get the list of functions that are called.  Verify that each function being called is in the list of asynchronous-safe functions.  To avoid repeatedly reviewing each function, the result of the first test of the function should be stored.
    Report any violations detected.
                                        Posted by rcs at Apr 13, 2008 21:07
                                     |
| (1) Should specifically mention that standard I/O in a signal handler is a mistake.
(2) Please do not recommend _Exit for any use other than specific cases involving fork.; It is important that atexit-registered handlers be allowed to perform their clean-up actions, which may involve database integrity etc.
(3) The example isn't very good since it is better served by just allowing default treatment of SIGINT.  A looping example is better, where the handler sets a flag which is tested each iteration of the loop.
                                        Posted by dagwyn at Apr 18, 2008 11:44
                                     |
| 1. Done, in the Implementation / OpenBSD section.
2. exit(3) is not listed as async-safe in POSIX, while _Exit() and abort() are...but my Linux manpage on abort() doesn't indicate if it is more like exit() or _Exit(). At any rate exit handlers would have to be async-safe in order to be invoked from a signal handler. At any rate, the proper way to exit cleanly would prob be to have your signal handler set a flag and return w/o calling _Exit(), and then have your main program read the flag and gracefully shut down (it can call exit() with proper cleanup)
3. Agreed, but the compliant example does illustrate the 'corrected' version of the non-compliant example. I agree a better design would be to not use signals at all, or to have the signal handler set a flag, but those are less illustrative.
                                        Posted by svoboda at Apr 18, 2008 14:04
                                     |
| David, 
For (3) I think Doug's point is that we should use a different example, so that there is a reason for having a SIGINT handler to begin with, maybe something like SIG32-C. Do not call longjmp() from inside a signal handler but simpler.
                                        Posted by rcs at May 23, 2008 10:08
                                     |
| I replaced the code examples with an example derived from SIG32-C as suggested. Now the signal handler calls no functions except sleep(), which is async-safe.
                                        Posted by svoboda at May 23, 2008 19:18
                                     |
| Why do the NCCE and CS both call sleep()?  If we got rid of this, these would both be pure C99 right?   This and maybe get rid of the:
#include <unistd.h>

![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 27, 2008 00:00
\| \|
Sigh. The call to sleep() in both examples was gratuitous. I wanted the compliant signal handler to call **some** async-safe function, and that was the only useful one I could find. I took it out. The \<unistd.h\> include was only for importing `sleep()`.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 27, 2008 11:51
\| \|
What does "single-file programs" mean? Does this mean that the signal handler must be defined within the same compilation unit as the call to `signal()`, or does it really mean a single file or single compilation unit?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jul 16, 2008 15:37
\| \|
It means that ROSE can only look at one file at a time, and that file must contain enough information to indicate a violation of the rule.
(ROSE actually does have some functionality to bind to a database, one could theoretically use this db to handle programs written across multiple files, but we haven't used that yet.)
For this rule, ROSE can only identify a function as a signal handler if it is actually the argument to a signal() or sigaction() function. So the function must be defined in the same C file that assigns it as a signal handler for ROSE to work on it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 16, 2008 16:22
\| \|
POSIX has the same concept of 'asynchronous-safe', but it terms it 'async-signal-safe'. Should we s/asynchronous-safe/async-signal-safe/g; to align with POSIX or not?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 29, 2008 21:23
\| \|
I don't know if that is necessary. Perhaps we can just make mention of this in the glossary entry.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Nov 30, 2008 11:41
\| \|
The prohibition on use of;siglongjmp in signal handlers is incorrect and contradicts the design of Posix. Posix has sigsetjmp and siglongjmp specifically to recover from certain signals that cannot be avoided in all cases. A good example is SIGBUS of type BUS_OBJERR. This occurs when accessing a memory mapped file and the underlying file has become corrupt in some way (such as due to an external ftruncate or filesystem-layer corruption). It is relatively easy to write code where accesses to the memory map do not leave data structures in indeterminate state, and this is the only way Posix offers to detect and recover from these corruption errors without a process failure. So server engineers who both followed this misguided prohibition on siglongjmp and used memory mapped files would be subject to denial of service attacks that can only be avoided by use of sigsetjmp / siglongjmp. If you wish to limit use of siglongjmp for recovery from signals where recovery behavior is clear and application data structures can be kept reliably consistent, that would be a more appropriate rule.
![](images/icons/contenttypes/comment_16.png) Posted by chris.newman at Apr 24, 2015 23:13
\| \|
This rule matches the current requirements in POSIX (which does not include siglongjmp in the list of async-signal-safe functions).; However, there is a change planned for the next POSIX technical corrigendum (TC2) to add it to the list but with caveats about the way it can be used.  See <http://austingroupbugs.net/view.php?id=516#c1198> for details.  Once TC2 has been approved by IEEE, the POSIX section under "Implementation Details" in this rule should be updated to match.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 27, 2015 04:42
\| \|
Tool for runtime detection of violations of this rule: [https://github.com/yugr/sighandlercheck](https://github.com/yugr/sigcheck)
![](images/icons/contenttypes/comment_16.png) Posted by yugr at Mar 22, 2019 06:44
\| \|
This rule is currently marked not-for-cpp, but I wonder if that's an accident.;<http://eel.is/c++draft/support#signal-3> suggests that perhaps there is some C++ overlap here, but I'm not an expert on signals. This question came up as part of a code review for a new clang-tidy checker for this rule and we weren't certain whether it should apply in C++ as well. We had specific questions about whether code like this was a violation or not:
``` java
void some_signal_handler(int sig) {
  []{ puts("this should not be an escape hatch for the check); }();
}
// or
std::signal(SIGINT, [](int sig) {
  puts("I did the bad thing this way"); // should be diagnosed, yes?
});
```
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 07, 2020 09:45
\| \|
Doesn't;[MSC54-CPP. A signal handler must be a plain old function](https://wiki.sei.cmu.edu/confluence/display/cplusplus/MSC54-CPP.+A+signal+handler+must+be+a+plain+old+function) already cover this for C++, where it quotes from \[support.signal\], paragraph 3?
> — a call to any standard library function, except for plain lock-free atomic operations and functions explicitly identified as signal-safe.

![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Oct 07, 2020 10:06
\| \|
Ah, that explains the markings, thank you for the help!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 07, 2020 10:28
\| \|
In addition to what Joe said, the puts() function is definitely not asynchronous-safe.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 07, 2020 13:46
\|
