A signal handler should not reassert its desire to handle its own signal. This is often done on *nonpersistent* platforms—that is, platforms that, upon receiving a signal, reset the handler for the signal to SIG_DFL before calling the bound signal handler. Calling` signal()` under these conditions presents a race condition. (See [SIG01-C. Understand implementation-specific details regarding signal handler persistence](SIG01-C_%20Understand%20implementation-specific%20details%20regarding%20signal%20handler%20persistence).)
A signal handler may call `signal()` only if it does not need to be [asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safefunction) (that is, if all relevant signals are masked so that the handler cannot be interrupted).
## Noncompliant Code Example (POSIX)
On nonpersistent platforms, this noncompliant code example contains a race window, starting when the host environment resets the signal and ending when the handler calls `signal()`. During that time, a second signal sent to the program will trigger the default signal behavior, consequently defeating the persistent behavior implied by the call to `signal()` from within the handler to reassert the binding.
If the environment is persistent (that is, it does not reset the handler when the signal is received), the `signal()` call from within the `handler()` function is redundant.
``` c
#include <signal.h>
void handler(int signum) {
  if (signal(signum, handler) == SIG_ERR) {
    /* Handle error */
  }
  /* Handle signal */
}
void func(void) {
  if (signal(SIGUSR1, handler) == SIG_ERR) {
    /* Handle error */
  }
}
```
## Compliant Solution (POSIX)
Calling the `signal()` function from within the signal handler to reassert the binding is unnecessary for persistent platforms, as in this compliant solution:
``` c
#include <signal.h>
void handler(int signum) {
  /* Handle signal */
}
void func(void) {
  if (signal(SIGUSR1, handler) == SIG_ERR) {
    /* Handle error */
  }
}
```
## Compliant Solution (POSIX)
POSIX defines the `sigaction()` function, which assigns handlers to signals in a similar manner to `signal()` but allows the caller to explicitly set persistence. Consequently, the `sigaction()` function can be used to eliminate the race window on nonpersistent platforms, as in this compliant solution:
``` c
#include <signal.h>
#include <stddef.h>
void handler(int signum) {
  /* Handle signal */
}
void func(void) {
  struct sigaction act;
  act.sa_handler = handler;
  act.sa_flags = 0;
  if (sigemptyset(&act.sa_mask) != 0) {
    /* Handle error */
  }
  if (sigaction(SIGUSR1, &act, NULL) != 0) {
    /* Handle error */
  }
}
```
Although the handler in this example does not call `signal()`, it could do so safely because the signal is masked and the handler cannot be interrupted. If the same handler is installed for more than one signal, the signals must be masked explicitly in `act.sa_mask` to ensure that the handler cannot be interrupted because the system masks only the signal being delivered.
POSIX recommends that new applications should use `sigaction()` rather than `signal()`. The `sigaction()` function is not defined by the C Standard and is not supported on some platforms, including Windows.
## Compliant Solution (Windows)
There is no safe way to implement persistent signal-handler behavior on Windows platforms, and it should not be attempted. If a design depends on this behavior, and the design cannot be altered, it may be necessary to claim a deviation from this rule after completing an appropriate risk analysis.
The reason for this is that Windows is a nonpersistent platform as discussed above.  Just before calling the current handler function, Windows resets the handler for the next occurrence of the same signal to `SIG_DFL`. If the handler calls `signal()` to reinstall itself, there is still a race window. A signal might occur between the start of the handler and the call to `signal()`, which would invoke the default behavior instead of the desired handler.
## Exceptions
**SIG34-C-EX1:** For implementations with persistent signal handlers, it is safe for a handler to modify the behavior of its own signal. Behavior modifications include ignoring the signal, resetting to the default behavior, and having the signal handled by a different handler. A handler reasserting its binding is also safe but unnecessary.
The following code example resets a signal handler to the system's default behavior:
``` c
#include <signal.h>
void handler(int signum) {
#if !defined(_WIN32)
  if (signal(signum, SIG_DFL) == SIG_ERR) {
    /* Handle error */
  }
#endif
  /* Handle signal */
}
void func(void) {
  if (signal(SIGUSR1, handler) == SIG_ERR) {
    /* Handle error */
  }
}
```
## Risk Assessment
Two signals in quick succession can trigger a race condition on nonpersistent platforms, causing the signal's default behavior despite a handler's attempt to override it.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG34-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | signal-handler-signal-call | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-SIG34 |  |
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| Compass/ROSE |  |  | Can detect violations of this rule. However, false positives may occur on systems with persistent handlers |
| Cppcheck Premium | 24.11.0 | premium-cert-sig34-c |  |
| Helix QAC | 2024.4 | C5021C++5022 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.SIGNAL
 |  |
| LDRA tool suite | 9.7.1 | 97 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG34-a | Properly define signal handlers |
| PC-lint Plus | 1.4 | 2762, 2763 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule SIG34-C | Checks for signal call from within signal handler (rule partially covered) |
| RuleChecker | 24.04 | signal-handler-signal-call | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | SIG01-C. Understand implementation-specific details regarding signal handler persistence | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Calling signal from interruptible signal handlers [sigcall] | Prior to 2018-01-12: CERT: Unspecified Relationship |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152213) [](../c/Rule%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152239)
## Comments:

|  |
| ----|
| This rule still permits unsafe practices.; In particular, where it says
"A signal handler may call signal() to reset the signal, or change the
current way signals are handled." On non-persistent platforms the only
safe use for signal() in a signal handler is signal(signum, SIG_DFL).
(It's safe because it's a no-op, and therefore redundant.)  For any
other use there is still the same race window between entry to the
handler and the call to signal() when the default handler is in effect.
                                        Posted by geoffclare at Apr 14, 2008 10:33
                                     |
| Agreed...calling signal() inside a handler is safe only if the handler may not be interrupted. Adjusted rule accordingly.
                                        Posted by svoboda at Apr 14, 2008 11:05
                                     |
| Now the rule is too strong.; It would forbid the second compliant solution in SIG01-A (which calls signal(signum, SIG_DFL) in a handler).
Also, if the rule is going to do more than just forbid handler re-assertion then the title of the rule needs changing.
                                        Posted by geoffclare at Apr 14, 2008 11:31
                                     |
| Added the SIG01-A compliant solution to this rule as an exception.
                                        Posted by svoboda at Apr 14, 2008 13:45
                                     |
| I still think the title of the rule needs changing.; Now that the rule specifies an exception for persistent systems, the title could be "Do not call signal() from within signal handlers".
                                        Posted by geoffclare at Apr 15, 2008 04:37
                                     |
| title changed, added 'interruptible'
                                        Posted by svoboda at Apr 15, 2008 09:39
                                     |
| This rule is simply wrong, and the right part of it is redundant with another rule.
The reason for invoking signal within the handler is to reset the handler with as small a race window as possible, on platforms where that is the best that one can do.; Not resetting the handler makes the process vulnerable to that signal.
                                        Posted by dagwyn at Apr 18, 2008 11:54
                                     |
| The 'redundancy' is with SIG01-A which discusses signal handler persistence. This rule is a special case of SIG01-A (which is a recommendation, not a rule). The overall gist is that the race window, no matter how small, is still a security vul, and should be avoided.
                                        Posted by svoboda at Apr 18, 2008 14:17
                                     |

