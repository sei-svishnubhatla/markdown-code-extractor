A signal is a mechanism for transferring control that is typically used to notify a process that an event has occurred. That process can then respond to the event accordingly. The C Standard provides functions for sending and handling signals within a C program.
Processes handle signals by registering a signal handler using the `signal()` function, which is specified as
``` java
void (*signal(int sig, void (*func)(int)))(int);
```
This signal handler is conceptually equivalent to
``` java
typedef void (*sighandler_t)(int signum);
extern sighandler_t signal(
  int signum, 
  sighandler_t handler
);
```
Signal handlers can be interrupted by signals, including their own. If a signal is not reset before its handler is called, the handler can interrupt its own execution. A handler that always successfully executes its code despite interrupting itself or being interrupted is [async-signal-safe](BB.-Definitions_87152273.html#BB.Definitions-async-signal-safe).
Some platforms provide the ability to mask signals while a signal handler is being processed. If a signal is masked while its own handler is processed, the handler is noninterruptible and need not be async-signal-safe. However, even when a signal is masked while its own handler is processed, the handler must still avoid invoking async-signal-safe unsafe functions because their execution may be (or have been) interrupted by another signal.
[Vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) can arise if a signal handler that is not async-signal-safe is interrupted with any unmasked signal, including its own.
## Noncompliant Code Example
This noncompliant code example registers a single signal handler to process both `SIGUSR1` and `SIGUSR2`. The variable `sig2` should be set to `1` if one or more `SIGUSR1` signals are followed by `SIGUSR2`, essentially implementing a finite state machine within the signal handler.
``` c
#include <signal.h>
volatile sig_atomic_t sig1 = 0;
volatile sig_atomic_t sig2 = 0;
void handler(int signum) {
  if (signum == SIGUSR1) {
    sig1 = 1;
  }
  else if (sig1) {
    sig2 = 1;
  }
}
int main(void) {
  if (signal(SIGUSR1, handler) == SIG_ERR) {
    /* Handle error */
  }
  if (signal(SIGUSR2, handler) == SIG_ERR) {
    /* Handler error */
  }
  while (sig2 == 0) {
    /* Do nothing or give up CPU for a while */
  }
  /* ... */
  return 0;
}
```
Unfortunately, a race condition occurs in the implementation of `handler()`. If `handler()` is called to handle `SIGUSR1` and is interrupted to handle `SIGUSR2`, it is possible that `sig2` will not be set.
## Compliant Solution (POSIX)
The POSIX `sigaction()` function assigns handlers to signals in a similar manner to the C `signal()` function, but it also allows signal masks to be set explicitly. Consequently, `sigaction()` can be used to prevent a signal handler from interrupting itself.
``` c
#include <signal.h>
#include <stdio.h>
volatile sig_atomic_t sig1 = 0;
volatile sig_atomic_t sig2 = 0;
void handler(int signum) {
  if (signum == SIGUSR1) {
    sig1 = 1;
  }
  else if (sig1) {
    sig2 = 1;
  }
}
int main(void) {
  struct sigaction act;
  act.sa_handler = &handler;
  act.sa_flags = 0;
  if (sigemptyset(&act.sa_mask) != 0) {
    /* Handle error */
  }
  if (sigaddset(&act.sa_mask, SIGUSR1)) {
    /* Handle error */
  }
  if (sigaddset(&act.sa_mask, SIGUSR2)) {
    /* Handle error */
  }
  if (sigaction(SIGUSR1, &act, NULL) != 0) {
    /* Handle error */
  }
  if (sigaction(SIGUSR2, &act, NULL) != 0) {
    /* Handle error */
  }
  while (sig2 == 0) {
    /* Do nothing or give up CPU for a while */
  }
  /* ... */
  return 0;
}
```
POSIX recommends `sigaction()` and deprecates the use of `signal()` to register signal handlers. Unfortunately, `sigaction()` is not defined in the C Standard and is consequently not as portable a solution.
## Risk Assessment
Interrupting a noninterruptible signal handler can result in a variety of vulnerabilities \[[Zalewski 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Zalewski01)\].

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG00-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| Helix QAC | 2024.4 | C5019 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG00-a | The signal handling facilities of <signal.h> shall not be used |
| PC-lint Plus | 1.4 | 586 | Assistance provided: reports use of the signal function |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID SIG00-CPP. Mask signals handled by noninterruptible signal handlers |
| MITRE CWE | CWE-662, Insufficient synchronization |

## Bibliography

|  |  |
| ----|----|
| [C99 Rationale 2003] | Subclause 5.2.3, "Signals and Interrupts" |
| [Dowd 2006] | Chapter 13, "Synchronization and State" ("Signal Interruption and Repetition") |
| [IEEE Std 1003.1:2013] | XSH, System Interface, longjmp |
| [OpenBSD] | signal() Man Page |
| [Zalewski 2001] | "Delivering Signals for Fun and Profit" |

------------------------------------------------------------------------
[](../c/Rec_%2011_%20Signals%20_SIG_) [](../c/Rec_%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152103)
## Comments:

|  |
| ----|
| The compliant solution has a window of vulnerability between the delivery of a SIGUSR1 and when SIGUSR2 has a handler registered -- it is quite possible that SIGUSR2 will be delivered before handler is registered.; Since unhandled SIGUSR2 signals terminate the process, the compliant solution is not secure.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 01:19
                                     |
| Plugged security hole in compliant code.
Compliant code should not crash unless signal is sent before either signal() function is called; can't fix that 
                                        Posted by svoboda at Mar 20, 2008 11:23
                                     |
| The "fixed" compliant code has a timing hole, between the first while loop and the signal() call that sets the SIGUSR2 handler, during which a SIGUSR2 could arrive but be ignored.
                                        Posted by geoffclare at Apr 07, 2008 12:29
                                     |
| Replaced compliant code with two compliant solutions, which prevent race conditions in two ways. The first one moves the finite state machine out of the signal handler, so the handler merely sets a flag (which flag depends on the signal). The second one uses sigaction(2) which prevents interrupting signal handlers.
                                        Posted by svoboda at Apr 10, 2008 14:27
                                     |
| Should we also be concerned in this recommendation about signal handlers that can be interrupted by other signals, and not just "interrupt itself"?  
                                        Posted by rcs at Apr 13, 2008 12:08
                                     |
| Are you sure the definition of reentrant given here is consistent with the definition we provide here BB. Definitions?  It is certainly spelled differently.  ;^)
Most of the rules about signal handlers talk about them being asynchronous-safe and not just reentrant.  I suspect that same distinction may apply here.
                                        Posted by rcs at Apr 13, 2008 12:12
                                     |
| True, whan I said 're-entrant' in this rule, I meant 'asynchronous-safe'.
The real issue with 'async-safe' functions is not that they can interrupt themselves, or other signal handlers. There are two closely-related aspects to async safety:
    Any function can be interrupted without leaving global data in an inconsistent state.
    A signal handler can work properly despite the fact that it may have interrupted a function that left global data in an inconsistent state.
A good asynch-safe handler must satisfy both of these constraints. Most functions satisfy neither.
Re-entrence refers to multi-threading environments, which is outside the scope of signal handling.
                                        Posted by svoboda at Apr 13, 2008 13:17
                                     |
| I s/re-entrent/async-safe/g; in this rule BTW. But we may wish to refine the def for 'async-safe'.
                                        Posted by svoboda at Apr 13, 2008 13:18
                                     |
| If you can think of a better way to phrase it, go for it.
                                        Posted by rcs at Apr 13, 2008 18:38
                                     |
| Added a few phrases to include handlers getting interrupted by signals other than their own. Also the def of 'async-safe' now includes a handler's ability to work with a globally inconsistent state, prob because it interrupted a function busy doing something sensitive.
                                        Posted by svoboda at Apr 14, 2008 09:42
                                     |
| In email you guys discussed how there is no good way to fix the reset issue in Windows, should we talk about this here as well?; It seems like we should explain why our only Compliant solution is POSIX...
                                        Posted by avolkovi at Apr 15, 2008 09:26
                                     |
| I've asked MS to review this issue.  Let's hold off a bit and see what they have to say.
                                        Posted by rcs at Apr 15, 2008 09:28
                                     |
| I don't see the value in keeping the Non-Compliant Code Example (External finite state machine) section in this recommendation.  It doesn't really bring you any closer to the solution.  Unless there is a good reason to keep it, I recommend removing it entirely.
                                        Posted by rcs at May 20, 2008 09:18
                                     |
| The external finite state machine example was once considered compliant, because the handler was async-safe, until we realized the TOCTOU race condition still applied. IOW the handler was async-safe but not interruptible. But you're right, since its non-compliant, it has nothing to do with the compliant solution, which uses sigaction(). So I took out the EFSM example.
                                        Posted by svoboda at May 20, 2008 13:03
                                     |
| I think we should remove everything up to "Signal handlers can be interrupted by signals..." since it's just an introduction to signals and has nothing to do with this rule in particular
                                        Posted by avolkovi at May 20, 2008 13:16
                                     |
| For the integrity of this rule, I agree.
But the 'intro to signals' paragraphs you are targetting was orphaned from the Signals section page (all section pages with intro material generally got the material put into its own rec).  So we shouldn't delete it from this rule unless we 'move' it to some other rule...perhaps SIG01 would be a better habitat for this section?
For that matter, maybe we should swap SIG00 and SIG01?
                                        Posted by svoboda at May 20, 2008 13:56
                                     |
| Marked as 'unenforceable' because I'm not sure we can use static analysis to identify if a signal handler is interruptible or not.
                                        Posted by svoboda at Jul 14, 2008 13:15
                                     |
| 
If a signal is masked while its own handler is processed, the handler is noninterruptible and need not be asynchronous-safe.
I think that's not true if "asynchronous-safe" is defined as here;[seccode:BB. Definitions] :
"A function is asynchronous-safe, or asynchronous-signal safe, if it can be called safely and without side effects from within a signal handler context (...) It must also function properly when global data might itself be in an inconsistent state."
For example, calling malloc(3) from within a handler is unsafe, even if the handler is noninterruptible, because the heap might be in an inconsistent state if the process was interrupted in the middle of a malloc/free call. 
                                        Posted by neologix at Jan 08, 2011 09:40
                                     |
| You're correct. Quoting from section 2.4.2 Signal Concepts of ISO/IEC 9945:2008 (AKA POSIXÂ® AKA SUSv3 Issue 7) online:
In the presence of signals, all functions defined by this volume of POSIX.1-2008 shall behave as defined when called from or interrupted by a signal-catching function, with a single exception: when a signal interrupts an unsafe function and the signal-catching function calls an unsafe function, the behavior is undefined.
However, I suspect the intent of the sentence may have been to indicate that the signal handler need not protect its own data from becoming inconsistent since the handler cannot be re-entered. I tried to clarify the text to this effect. Let me know if you still see a problem.
                                        Posted by martinsebor at Jan 09, 2011 17:14
                                     |
| By a strict reading of the C standard, even the compliant solution contains undefined behavior. The problem is that it does if (sig1) inside of handler, and the standard only gives allowance to write to volatile sig_atomic_t in async-signal context, not to read from them.
                                        Posted by jcsible at Jun 30, 2020 13:33
                                     |
| ISO WG14 did at one point state that the only thing a signal handler can do is write to a volatile sig_atomic_t variable and return. However, upon further questioning, they agreed that it is also safe to *read* to a variable of type volatile sig_atomic_t.BTW thanks for your wordsmithing edit!
                                        Posted by svoboda at Aug 11, 2020 12:43
                                     |

