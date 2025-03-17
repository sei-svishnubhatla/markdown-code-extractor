> [!warning]  
>
> This guideline has been deprecated by
>
> -   SIG30-C. Call only asynchronous-safe functions within signal handlers

The C standard disallows recursive invocation of the `raise()` function. Section 7.14.1.1, para. 4, of the C standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] states:
> If the signal occurs as the result of calling the `abort` or `raise` function, the signal handler shall not call the `raise` function.

(See also [undefined behavior 131](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISO/IEC%209899:2011) of Annex J.)
## Noncompliant Code Example
In this noncompliant code example, the `int_handler()` function is used to carry out `SIGINT`-specific tasks and then raises a `SIGTERM`. However, there is a nested call to the `raise()` function, which results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
void term_handler(int signum) {
  /* SIGTERM handling specific */
}
void int_handler(int signum) {
  /* SIGINT handling specific */
  if (raise(SIGTERM) != 0) {  // diagnostic required
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
In this compliant solution, the call to the `raise()` function inside `handler()` has been replaced by a direct call to `log_msg()`.
``` c
#include <signal.h>
void log_msg(int signum) {
  /* Log error message in some asynchronous-safe manner */
}
void handler(int signum) {
  /* Do some handling specific to SIGINT */
  log_msg(SIGUSR1);
}
int main(void) {
  if (signal(SIGUSR1, log_msg) == SIG_ERR) {
    /* Handle error */
  }
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* handle error */
  }
  /* program code */
  if (raise(SIGINT) != 0) {
    /* Handle error */
  }
  /* More code */
  return 0;
}
```
## Compliant Solution (POSIX)
If a signal handler is assigned using the POSIX `sigaction()` function, the signal handler may safely call `raise()`.
The POSIX standard is contradictory regarding `raise()` in signal handlers. The POSIX standard \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] prohibits signal handlers installed using `signal()` from calling the `raise()` function if the signal occurs as the result of calling the `raise()`, `kill()`, `pthread_kill()`, or `sigqueue()` functions. However, it also requires that the `raise()` function may be safely called within any signal handler. (See [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers).) Consequently, it is not clear whether it is safe for POSIX applications to call `raise()` in signal handlers installed using `signal()`, but it is safe to call `raise()` in signal handlers installed using `sigaction()`.
``` c
#include <signal.h>
void log_msg(int signum) {
  /* Log error message in some asynchronous-safe manner */
}
void handler(int signum) {
  /* Do some handling specific to SIGINT */
  if (raise(SIGUSR1) != 0) {
    /* Handle error */
  }
}
int main(void) {
  struct sigaction act;
  act.sa_flags = 0;
  if (sigemptyset(&act.sa_mask) != 0) {
    /* Handle error */
  }
  act.sa_handler = log_msg;
  if (sigaction(SIGUSR1, &act, NULL) != 0) {
    /* Handle error */
  }
  act.sa_handler = handler;
  if (sigaction(SIGINT, &act, NULL) != 0) {
    /* Handle error */
  }
  /* program code */
  if (raise(SIGINT) != 0) {
    /* Handle error */
  }
  /* More code */
  return 0;
}
```
POSIX recommends `sigaction()` and deprecates `signal()`. Unfortunately, `sigaction()` is not defined in the C Standard and is consequently not as portable a solution.
## Risk Assessment
Undefined behavior arises if a signal occurs as the result of a call to `abort()` or `raise()`, the signal handler in turn calls the `raise()` function.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG33-C | low | unlikely | medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 89 D | Fully implemented. |
| Compass/ROSE | ; | ; | Can detect violations of this rule for single-file programs. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG33-C).
### Related Guidelines
[SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682): [VOID SIG33-CPP. Do not recursively invoke the raise() function](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+SIG33-CPP.+Do+not+recursively+invoke+the+raise%28%29+function)
[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011) Section 7.14.1.1, "The `signal` function"
[ISO/IEC TS 17961](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISO/IEC%20TR%2017961) (Draft) Calling functions in the C Standard Library other than abort, \_Exit, and signal from within a signal handler \[asyncsig\]
[MITRE CWE](http://cwe.mitre.org/): [CWE ID 479](http://cwe.mitre.org/data/definitions/479.html), "Unsafe function call from a signal handler"
## Bibliography
\[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\] Chapter 13, "Synchronization and State"  
\[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\]  
\[[OpenBSD](AA.-Bibliography_87152170.html#AA.Bibliography-OpenBSD)\] [signal() Man Page](http://www.openbsd.org/cgi-bin/man.cgi?query=signal)
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/SIG32-C.+Do+not+call+longjmp()+from+inside+a+signal+handler?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=3903) [](https://www.securecoding.cert.org/confluence/display/seccode/SIG34-C.+Do+not+call+signal()+from+within+interruptible+signal+handlers?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| The use of the term "recursively" is not correct in this context. Signal handlers are not properly function calls that result directly from raise(). They can occur for many other reasons. Therefore, describing the use of raise() within a signal handler is not properly a recursive invocation of raise().
                                        Posted by wlf@cert.org at Jul 10, 2007 11:22
                                     |
| Yes, strictly speaking, all raise() does is generate a signal. However, we discussed this, and decided that the language should stay as it is. In the NCCE example, the raise(SIGINT) has the intended effect of running the code in the signal handler, which calls raise() a second time (the behavior which the standard disallows). So although it isn't recursion to the letter, that is how it appears, and more people would (presumably) be comfortable with this explanation then going through the details of exactly how raise generates signals. 
                                        Posted by jpincar at Jul 10, 2007 11:45
                                     |
| Two points.
In a threaded environment, there is no requirement that signal handlers even run in the same thread where the signal is raised. In fact, it's rarely the case. I think that implying that raise() calls the signal handler (as the use of the term recursively certainly does) is very misleading. The vast majority of signals are raised without raise() being called. That is, after all, the point of signals. If all you wanted to do with raise() was call the signal handler, you could just call it directly.
Secondly, you should point out that some standard library calls call raise() as well (abort() being an example) and that cannot call those either. Raise() cannot be called directly or indirectly.
                                        Posted by wlf@cert.org at Jul 11, 2007 09:00
                                     |
| Yes, I suppose it is misleading. And yeah, most signals are generated without raise() being called. The point of the article is about not calling raise() while the signal that a previous raise() called is being handled. Signals coming from other sources aren't really relevant here. In any case, can you think of an example where you would want to do something with raise() other than to just call the signal handler?
I'll add something in about library functions calling raise().
                                        Posted by jpincar at Jul 11, 2007 09:58
                                     |
| The line from the standard states that the handler can not call raise() ("the signal handler shall not call the raise function"). Would library functions which call raise() then technically be safe, as the handler does not explicitly make the call in these cases?
                                        Posted by jpincar at Jul 11, 2007 11:51
                                     |
| Regarding "The POSIX standard [Open Group 04]  also prohibits the signal handler from calling the raise() function ...", This appears to be a defect in POSIX.; It contradicts the requirement in XSH 2.4.3 that all async-signal-safe functions can be invoked without restriction from signal handlers.  (The list of async-signal-safe functions includes raise().)  I have submitted a defect report to the Austin Group:
   http://www.opengroup.org/austin/mailarchives/ag-review/msg02567.html
Unfortunately it is too late to get a fix into POSIX.1-2008, but hopefully it will be fixed in TC1.
In any case since the restriction is stated on the signal() page, it would only apply to signal handlers installed using signal(), not to handlers installed using sigaction(), and POSIX applications should always use sigaction().
The simplest way to get round the issue in this rule might be just to say the restriction does not apply to signal handlers installed using the POSIX sigaction() function.
                                        Posted by geoffclare at Apr 11, 2008 10:33
                                     |
| Did so, and added a compliant solution involving raise() and sigaction().
                                        Posted by svoboda at Apr 14, 2008 10:53
                                     |
| On second thought, any handler that can be invoked via raise() can also be invoked via kill(). So it's never completely safe for a handler to call raise() itself. Took out sigaction() example again.
                                        Posted by svoboda at Apr 14, 2008 10:56
                                     |
| Huh?; Why is kill() a problem?  If raise() is async-safe, then it is safe to call it from a signal handler, regardless of what caused the signal handler to be invoked.
                                        Posted by geoffclare at Apr 14, 2008 11:18
                                     |
| > The POSIX standard Open Group 04 also prohibits the signal handler from calling the raise() function if the signal occurs as the result of calling the kill(), pthread_kill(), or sigqueue() functions.
                                        Posted by svoboda at Apr 14, 2008 11:29
                                     |
| My initial comment in this thread covers that as well.; The quote is from the signal() page, and therefore does not apply to signal handlers installed using sigaction() (and is questionable for handlers installed using signal(), since it contradicts the async-signal-safe requirement for raise()).
                                        Posted by geoffclare at Apr 14, 2008 11:48
                                     |
| Sigh. I am in a twisty maze of standards, all contradictory.
ok, added back the sigaction() example, plus outlined the POSIX paradox. I'd like a bit more certainty about implementations implementing async-safe raise(), but that will have to wait for a TR on POSIX.2008.
                                        Posted by svoboda at Apr 14, 2008 13:32
                                     |
| Looks good.; I made a few clarifications to the statements about POSIX.
                                        Posted by geoffclare at Apr 15, 2008 04:26
                                     |

