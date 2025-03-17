Avoid using signals to implement normal functionality. Signal handlers are severely limited in the actions they can perform in a portably secure manner. Their use should be reserved for abnormal events that can be serviced by little more than logging.
## Noncompliant Code Example
This noncompliant code example uses signals as a means to pass state changes around in a multithreaded environment:
``` c
/* THREAD 1 */
int do_work(void) {
  /* ... */
  kill(THR2_PID, SIGUSR1);
}
/* THREAD 2 */
volatile sig_atomic_t flag;
void sigusr1_handler(int signum) {
  flag = 1;
}
int wait_and_work(void) {
  flag = 0;
  while (!flag) {}
  /* ... */
}
```
However, using signals for such functionality often leads to nonportable or otherwise complicated solutions.
This code illustrates one thread using a signal to wake up a second thread. Using an architecture's native thread library usually allows for a more sophisticated means of sending messages between threads.
## Compliant Solution (POSIX)
A better solution, in this case, is to use condition variables. This code example uses a condition variable from the POSIX `pthread` library \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]:
``` c
#include <pthread.h>
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
pthread_mutex_t mut = PTHREAD_MUTEX_INITIALIZER;
/* THREAD 1 */
int do_work(void) {
  int result;
  /* ... */
  if ((result = pthread_mutex_lock(&mut)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_cond_signal(&cond,&mut)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_mutex_unlock(&mut)) != 0) {
    /* Handle error condition */
  }
}
/* THREAD 2 */
int wait_and_work(void) {
  if ((result = pthread_mutex_lock(&mut)) != 0) {
    /* Handle error condition */
  }
  while (/* Condition does not hold */) {
    if ((result = pthread_cond_wait(&cond, &mut)) != 0) {
      /* Handle error condition */
    }
    /* ... */
  }
  if ((result = pthread_mutex_unlock(&mut)) != 0) {
    /* Handle error condition */
  }
  /* ... */
}
```
## Compliant Solution (Windows)
This compliant solution uses a condition variable from the Win32 API \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\]:
``` c
#include <windows.h>
/* 
 * Note that the CRITICAL_SECTION must be initialized with
 * InitializeCriticalSection, and the CONDITION_VARIABLE must
 * be initialized with InitializeConditionVariable prior to 
 * using them.
 */
CRITICAL_SECTION CritSection;
CONDITION_VARIABLE ConditionVar;
/* THREAD 1 */
int do_work(void) {
  /* ... */
  WakeConditionVariable(&ConditionVar);
}
/* THREAD 2 */
int wait_and_work(void) {
  EnterCriticalSection(&CritSection);
  SleepConditionVariableCS(&ConditionVar, &CritSection, INFINITE);
  LeaveCriticalSection(&CritSection);
  /* ... */
}
```
## Noncompliant Code Example
This noncompliant code example is from a [signal race vulnerability](http://seclists.org/bugtraq/1997/Jan/0011.html) in WU-FTPD v2.4 \[[Greenman 1997](AA.-Bibliography_87152170.html#AA.Bibliography-Greenman97)\]:
``` c
void dologout(status) {
  if (logged_in) {
    (void) seteuid((uid_t)0);
    logwtmp(ttyline, "", "");
    /* ... */
  }
  _exit(status);
}
static void lostconn(int signo) {
  if (debug)
    syslog(LOG_DEBUG, "lost connection");
  dologout(-1);
}
static void myoob(signo) {
  if (!transflag)
    return;
  /* ... */
  if (strcmp(cp, "ABOR\r\n") == 0) {
    tmpline[0] = '\0';
    reply(426, "Transfer aborted. Data connection closed.");
    reply(226, "Abort successful");
    longjmp(urgcatch, 1);
  }
  /* ... */
}
/* ... */
signal(SIGPIPE, lostconn);
signal(SIGURG, myoob);
```
A serious [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) can occur if `SIGURG` is caught immediately following the elevation of privileges in `dologout()`. If the `longjmp()` in the `SIGURG` handler `myoob()` is invoked, execution returns to the main processing loop with an effective UID of 0.
Please note that this code sample violates [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers) and [SIG31-C. Do not access shared objects in signal handlers](SIG31-C_%20Do%20not%20access%20shared%20objects%20in%20signal%20handlers).
An immediate fix is to ensure that `dologout()` cannot be interrupted by a `SIGURG`:
``` c
void dologout(status) {
 /*
  * Prevent reception of SIGURG from resulting in a resumption
  * back to the main program loop.
  */ 
  transflag = 0;
  if (logged_in) {
    (void) seteuid((uid_t)0);
    logwtmp(ttyline, "", "");
    /* ... */
  }
  _exit(status);
}
```
A better solution is for `myoob()` to set a failure flag of type `volatile sig_atomic_t` that is periodically checked within the main loop:
``` c
volatile sig_atomic_t xfer_aborted = 0;
static void myoob(signo) {
  /* ... */
  if (strcmp(cp, "ABOR\r\n") == 0) {
    xfer_aborted = 1;
  }
  /* ... */
}
```
This solution, however, still violates [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers) and [SIG31-C. Do not access shared objects in signal handlers](SIG31-C_%20Do%20not%20access%20shared%20objects%20in%20signal%20handlers).
## Compliant Solution
A compliant solution (not shown) is to not use signals to signify lost connections and to design the system to have a robust error-handling mechanism (see [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy)).
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG02-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG02-a | The signal handling facilities of <signal.h> shall not be used |
| PC-lint Plus | 1.4 | 586 | Assistance provided: reports use of the signal function |

### Related Vulnerabilities
Using signals to implement normal functionality frequently results in the violation of one or more secure coding rules for signal handling.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID SIG02-CPP. Avoid using signals to implement normal functionality |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 13, "Synchronization and State" |
| [Greenman 1997] |  |
| [IEEE Std 1003.1:2013] | XBD, Headers, <pthread> |
| [MSDN] | Using Condition Variables |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152103) [](../c/Rec_%2011_%20Signals%20_SIG_) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_)
## Comments:

|  |
| ----|
| The examples in this recommendation talk about Inter Process Communication, but the actual example is inter thread communication.  This is a bit of a mismatch that needs to be resolved.  
When I read the start of this rule, I always expect to see a sendmail example where user functionality is implement through signals. I think this would make a better primary example, with perhaps the threads example a secondary example.
                                        Posted by rcs_mgr at Jun 05, 2008 00:30
                                     |
| any idea where we can find some sendmail code to reference?
                                        Posted by avolkovi at Jun 05, 2008 10:49
                                     |
| www.sendmail.org springs to mind... Look for sm_signal() calls, used to set signal handlers.
OTOH their "milter", whatever that is, uses a signal handling thread, which is a nice way to handle the issue: Ensure signals are delivered to that thread. It waits for them with sigwait() and can thus react to them immediately even though it does so outside a signal handler.
                                        Posted by hbf at Jun 06, 2008 08:59
                                     |
| ok... have been groking through their code and I can't seem to find anything particularly bad about their implementation... sm_signal() is basically just sigaction() configured for the current system, and most of the signals are either set to either SIG_IGN, SIG_DFL, or a no-op... of the signals that are actually used they seem to just do basic signal handling things
are you guys are talking about their pend_signal()/sm_releasesignal()/sm_blocksignal() functions?
Edit: (after more groking)
sm_releasesignal()/sm_blocksignal() are just system specific versions of sigblock()/sigsetmask()
pend_signal() is a way to keep signals from interrupting critical sections of, if a signal event happens inside of a critical section, the signal will pend itself until the next SIGALRM, once a SIGALRM finally ticks outside of a critical section, it will run over all of the pending signals and execute them, since we are no longer in a critical section (by virtue of sm_tick() running), none of these should quit out and re-pend themselves
all in all pretty clever and nothing that I would deem inappropriate behavior for signals :/ 
                                        Posted by avolkovi at Jun 06, 2008 09:34
                                     |
| I would guess that sendmail's signal vuls (if any) were historical, and no longer in the current code.
                                        Posted by svoboda at Jun 06, 2008 11:15
                                     |
| The first compliant solution (POSIX) has two problems:
1) it's not;pthread_mutex_wait, but pthread_cond_wait
2) there should be a boolean predicate associated to the condition variable that's checked after return from pthread_cond_wait, because of the posibility of spurious wakeups:
Quoting man page:
When using condition variables there is always a boolean predicate involving shared variables associated with each condition wait that is true if the thread should proceed. Spurious wakeups from the pthread_cond_wait() or pthread_cond_timedwait() functions may occur. Since the return from pthread_cond_wait() or pthread_cond_timedwait() does not imply anything about the value of this predicate, the predicate should be re-evaluated upon such return.
                                        Posted by neologix at Jan 08, 2011 10:11
                                     |
| I've amended the code. Our Java wiki has this rule:
 THI03-J. Always invoke wait() and await() methods inside a loop
We don't yet have a C/pthreads analogue to this rule, and need one to fully address the point you raise.
                                        Posted by svoboda at Jan 10, 2011 10:39
                                     |

