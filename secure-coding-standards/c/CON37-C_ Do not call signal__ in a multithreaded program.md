Calling the `signal()` function in a multithreaded program is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 135](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_135).)
## Noncompliant Code Example
This noncompliant code example invokes the `signal()` function from a multithreaded program:
``` c
#include <signal.h>
#include <stddef.h>
#include <threads.h>
volatile sig_atomic_t flag = 0;
void handler(int signum) {
  flag = 1;
}
/* Runs until user sends SIGUSR1 */
int func(void *data) {
  while (!flag) {
    /* ... */
  }
  return 0;
}
int main(void) {
  signal(SIGUSR1, handler); /* Undefined behavior */
  thrd_t tid;
  if (thrd_success != thrd_create(&tid, func, NULL)) {
    /* Handle error */
  }
  /* ... */
  return 0;
}
```
NOTE: The `SIGUSR1` signal value is not defined in the C Standard; consequently, this is not a C-compliant code example.
## Compliant Solution
This compliant solution uses an object of type `atomic_bool` to indicate when the child thread should terminate its loop:
``` c
#include <stdatomic.h>
#include <stdbool.h>
#include <stddef.h>
#include <threads.h>
atomic_bool flag = ATOMIC_VAR_INIT(false);
int func(void *data) {
  while (!flag) {
    /* ... */
  }
  return 0;
}
int main(void) {
  thrd_t tid;
  if (thrd_success != thrd_create(&tid, func, NULL)) {
    /* Handle error */
  }
  /* ... */
  /* Set flag when done */
  flag = true;
  return 0;
}
```
## Exceptions
**CON37-C-EX1:** Implementations such as POSIX that provide defined behavior when multithreaded programs use custom signal handlers are exempt from this rule \[[IEEE Std 1003.1-2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
## Risk Assessment
Mixing signals and threads causes [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON37-C | Low | Probable | Low | P6 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON37-C).
## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stdlib-use-signal | Fully checked |
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| Coverity | 2017.07 | MISRA C 2012 Rule 21.5 | Over-constraining |
| Cppcheck Premium | 24.11.0 | premium-cert-con37-c |  |
| Helix QAC | 2024.4 | C5021C++5022 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.SIGNAL |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-CON37-a | The signal handling facilities of <signal.h> shall not be used |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON37-C | Checks for signal call in multithreaded program (rule fully covered) |
| RuleChecker | 24.04 | stdlib-use-signal | Fully checked |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1-2013] | XSH 2.9.1, "Thread Safety" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151940) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152023)
## Comments:

|  |
| ----|
| 
In the thread function we set the cancel type to asynchronous, so as to ensure an immediate cancel.
This appears to be advocating asynchronous cancellation for general use, whereas it can only be used safely in very limited circumstances.  POSIX only requires three functions (pthread_cancel(), pthread_setcancelstate(), and pthread_setcanceltype()) to be async-cancel safe.  A conforming application cannot call any other standard functions while the calling thread has asynchronous cancellation enabled.
                                        Posted by geoffclare at Mar 16, 2010 12:20
                                     |
| 
This is rather vague:
If the cancellation type is set to asynchronous, the thread is terminated immediately, however in most cases it is not safe to do so, and should be generally avoided.
Geoff provided some good information, why don't you incorporate it?
                                        Posted by rcs at Mar 18, 2010 09:26
                                     |
| Is the issue in the first example the call to "pthread_kill()", the use of "SIGKILL", or both?
                                        Posted by xuinkrbin. at Jan 10, 2013 14:22
                                     |
| I'd say that sending KILL is the primary problem. I'm not sure what the effect is of sending signals other than SIGKILL to individual threads...presumably POSIX defines these cases.
                                        Posted by svoboda at Jan 10, 2013 14:45
                                     |
| The point of this rule is that an uncaught signal terminates the whole process, not just the selected thread.; Using SIGKILL in the example confuses things because of its uncatchablility, and distracts from the main point.  So I have changed the example to use SIGTERM.  I also noticed the code comment after the pthread_kill() call implied that the process terminates some time after pthread_kill() returns, whereas in fact pthread_kill() will not return, and I have changed the comment.
                                        Posted by geoffclare at Jan 11, 2013 04:23
                                     |
| ;"Do not use signals in multithreaded programs. This is undefined behavior in C11 (Section 7.14.1.1, paragraph 7)."False.  7.14.1.1 para 7 says use of the signal() function is undefined behavior, not use of signals.I think moving this from POSIX to CON was a mistake, since the whole point of the rule is all tied up with behaviour relating to signals that is required by POSIX but not by the C Standard.  A non-POSIX implementation where raise(SIGTERM) terminates the calling thread and does not terminate the process would actually be allowed by the C Standard.I would recommend moving this back and undoing all the recent changes, then adding a rule to CON which says don't use the signal() function in multithreaded programs.
                                        Posted by geoffclare at Feb 28, 2013 07:18
                                     |
| I took this advice; this is now a distinct rule from;POS44-C. Do not use signals to terminate threads
                                        Posted by svoboda at Feb 28, 2013 14:29
                                     |
| But it would be nice to have a specific reference to the POSIX exception, so people can see where this exception is given instead of just believing us.; 
                                        Posted by rcs at Oct 31, 2013 09:39
                                     |
| comment submitted by email:I just read CON37-C, which instructs not to use signal() in a multithreaded;environment, since C11 does not specify how signals are supposed to be dispatched among threads.Say I have an application with a pool of C11 threads reading from a single POSIX message queue. This queue is filled with commands coming from various other applications (a web server, ad-hoc TCP connections to automated command senders, etc.).If the queue is blocking, threads will block on mq_receive() and cannot be told to exit cleanly: only one thread will receive the TERMINATE command from the message queue. The others will still be blocked on mq_receive(), because mq_close() + mq_unlink() do not let other threads blocked on mq_receive() to return.If the queue is non-blocking, I would use a conditional variable to wait for a message, and send a single signal when a message arrives. One waiting thread will be woken up and call mq_receive().The question is, how to be notified when a message arrives? mqueue.h has mq_notify(), which can deliver a notification either by calling a signal handler or by creating a new thread. This sounds promising: a "main" thread could launch all receiving threads, and then call mq_notify() which will launch a signalling thread when a message arrives.However, mq_notify() requires the use of a structure defined in signal.h. Is this a sign that mq_notify() should not be used with C11 threads? Or is this just a coincidence to be ignored?More generally, is the "threadpool" pattern appropriate here? Should I rather spawn one thread per message, or does the overhead associated with thread creation prevent scalability?
                                        Posted by rcs_mgr at Oct 20, 2014 13:48
                                     |
| Very good points.; Obviously a lot of thought went into that comment.It turns out there is a simpler solution.  POSIX advises that software developers abandon signal() in favor of sigaction() because the latter is specially designed to work well with threads.
                                        Posted by dmk at Oct 21, 2014 14:39
                                     |
| You are right that POSIX applications should use sigaction() instead of signal(), but the reason you give is wrong.; From 1988 to 2000, POSIX did not require implementations to provide signal() at all.  If conforming POSIX applications wanted to handle signals they had to use sigaction().  Threads were added to POSIX in 1995; signal() was not added until 2001 (via the merge with the Single UNIX Specification).  So threads had nothing to do with the preference for sigaction() over signal().  Furthermore, in multithreaded programs sigwait(), which was added as part of the threads amendment, is preferred over sigaction().
                                        Posted by geoffclare at Oct 22, 2014 07:21
                                     |
| This rule cites the C11 standard which should make clear that usage of signal() with multiple threads is Undefined Behavior...the platform is free to do anything in such cases.Other standards, like POSIX, impose greater constraints. If your program is only going to run on POSIX systems, then your program might be well-defined (by the POSIX standard, not by C11).We have one rule:;POS44-C. Do not use signals to terminate threads to address signals & pthreads. (perhaps we need more) 
                                        Posted by svoboda at Oct 22, 2014 14:54
                                     |
| (Hi, this is the author of the email comment who just figured out how to sign up)The motivation behind my comment was to find a way to manage a threadpool using only C11 threading primitives. This is probably an exercise in futility since I'm using POSIX message queues anyway, but that explains why POS44-C did not provide a satisfying answer (it solves the problem by using;pthread_cancel(), which has no equivalent in C11).I eventually went with mq_notify()'s SIGEV_THREAD option. mqueue.h actually provides struct sigevent (by including bits/siginfo.h), so signal.h is not needed, contrary to what I originally thought.Since in terms of features, I see pthread.h as a superset of threads.h, the bottomline is that POS44-C has another solution which does not involve pthread_cancel() (though it relies on threads watching the termination predicate and returning of their own accord, so this might not count as "terminating").
                                        Posted by klegouguec at Oct 23, 2014 03:39
                                     |

