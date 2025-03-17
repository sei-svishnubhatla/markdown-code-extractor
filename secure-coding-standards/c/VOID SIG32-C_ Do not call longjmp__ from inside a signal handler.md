> [!warning]  
>
> This guideline has been deprecated by
>
> -   SIG30-C. Call only asynchronous-safe functions within signal handlers

Invoking the `longjmp()` function from within a signal handler can lead to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if it results in the invocation of any non-[asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safe) functions, likely compromising the integrity of the program. Consequently, neither `longjmp()` nor the POSIX `siglongjmp()` should ever be called from within a signal handler.
This rule is closely related to [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers).
## Noncompliant Code Example
This noncompliant code example is similar to a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in an old version of Sendmail \[[VU #834865](http://www.kb.cert.org/vuls/id/834865)\]. The intent is to execute code in a `main()` loop, which also logs some data. Upon receiving a `SIGINT`, the program transfers out of the loop, logs the error, and terminates.
However, an attacker can exploit this noncompliant code example by generating a `SIGINT` just before the second `if` statement in `log_message()`. This results in `longjmp()` transferring control back to `main()`, where `log_message()` is called again. However, the first `if` statement would not be executed this time (because `buf` is not set to `NULL` as a result of the interrupt), and the program would write to the invalid memory location referenced by `buf0`.
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
   *  Try to fit a message into buf, else re-allocate
   *  it on the heap and then log the message.
   */
/*** VULNERABILITY IF SIGINT RAISED HERE ***/
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
  }
  else {
    log_message(info1, info2);
  }
  return 0;
}
```
## Compliant Solution
In this compliant solution, the call to `longjmp()` is removed; the signal handler sets an error flag of type `volatile sig_atomic_t` instead.
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
   *  Try to fit a message into buf, else re-allocate
   *  it on the heap and then log the message.
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
## Risk Assessment
Invoking `longjmp()` from a signal handler causes the code after the `setjmp()` to be called under the same conditions as the signal handler itself. That is, the code must be called while global data may be in an inconsistent state and must be able to interrupt itself (in case it is itself interrupted by a second signal). So the risks in calling `longjmp()` from a signal handler are the same as the risks in a signal handler calling non-asynchronous-safe functions.
Invoking functions that are not asynchronous-safe from within a signal handler may result in privilege escalation and other attacks.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG32-C | high | likely | medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 88 D | Fully implemented. |
| Splint | 3.1.1 | ; | ; |
| Compass/ROSE | ; | ; | Can detect violations of this rule for single-file programs. |

### Related Vulnerabilities
For an overview of some software vulnerabilities, see Zalewski's paper on understanding, exploiting, and preventing signal-handling related vulnerabilities \[[Zalewski 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Zalewski01)\]. [VU #834865](http://www.kb.cert.org/vuls/id/834865) describes a vulnerability resulting from a violation of this rule.
Another notable case where using the `longjmp()` function in a signal handler caused a serious vulnerability is [wu-ftpd 2.4](http://seclists.org/bugtraq/1997/Jan/0011.html) \[[Greenman 1997](AA.-Bibliography_87152170.html#AA.Bibliography-Greenman97)\]. The effective user ID is set to zero in one signal handler. If a second signal interrupts the first, a call is made to `longjmp()`, returning the program to the main thread but without lowering the user's privileges. These escalated privileges can be used for further exploitation.
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG32-C).
## Related Guidelines
[MISRA 2004](AA.-Bibliography_87152170.html#AA.Bibliography-MISRA04): Rule 20.7
[MITRE CWE](http://cwe.mitre.org/): [CWE-479](http://cwe.mitre.org/data/definitions/479.html), "Unsafe function call from a signal handler"
## Bibliography
\[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\] Chapter 13, "Synchronization and State"  
\[[Greenman 1997](AA.-Bibliography_87152170.html#AA.Bibliography-Greenman97)\]  
\[[ISO/IEC PDTR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECPDTR24772)\] "EWD Structured programming"  
\[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] [longjmp](http://www.opengroup.org/onlinepubs/000095399/functions/longjmp.html)  
\[[OpenBSD](AA.-Bibliography_87152170.html#AA.Bibliography-OpenBSD)\] [signal() Man Page](http://www.openbsd.org/cgi-bin/man.cgi?query=signal)  
\[[Zalewski 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Zalewski01)\]  
\[[VU #834865](http://www.kb.cert.org/vuls/id/834865)\]
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/SIG31-C.+Do+not+access+shared+objects+in+signal+handlers) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=3903) [](https://www.securecoding.cert.org/confluence/display/seccode/SIG33-C.+Do+not+recursively+invoke+the+raise()+function?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| 
According to the C99 Rationale, Version 5.10:
Some implementations leave a process in a special state while a signal is being handled. Explicit
reassurance must be given to the environment when the signal handler returns. To keep this job
manageable, the C89 Committee agreed to restrict longjmp to only one level of signal
handling.
                                        Posted by rcs at May 07, 2007 13:49
                                     |
| As longjmp is a non-reentrant function, this is covered by SIG00-C. Do not call non-reentrant functions within signal handlers.
However, as the standard used to contradict itself about using longjmp within signal handlers, and it seems to be a fairly common practice to use this function, I think this article should remain here.
                                        Posted by jpincar at May 29, 2007 10:42
                                     |
| The details about the sendmail vulnerability are a little off. The vulnerability was as a result of a SIGALRM signal being generated (to indicate an input timeout). It occurred in the collect() function, not in main(). The generated signal would however log a message (with the sm_syslog() function) and return to the main SMTP processing loop (the smtp() function).
                                        Posted by mdowd at Jul 10, 2007 19:52
                                     |
| Hold on, is the problem here really with the longjmp? or is it declaring variables as static? Seems to me like if we removed the 'static' keyword the functionality would not change too much and the vulnerability would go away.; I feel like there are plenty of safe uses for longjmp() in signal handlers, in particular for catching things like SIGSEG or SIGFPE which you cannot handle by just setting an error flag since it would cause an infinite loop.
                                        Posted by avolkovi at Mar 06, 2008 11:36
                                     |
| Yup, the problem is with the longjmp.  The problem is that the signal could interrupt a non-asynchronous safe function.  If you longjmp back into the main body of the code again you can introduce a race condition.
I agree using signal handlers to handle SIGSEG or SIGFPE is not counter-productive unless you want to log an error followed by _Exit().
                                        Posted by rcs at Mar 06, 2008 16:42
                                     |
| POSIX has sigsetjmp() and siglongjmp().; It also says that returning from a signal handler for exceptional conditions like SIGSEG or SIGFPE is undefined behaviour - so don't do it.
Classically, using longjmp() out of a signal handler was illustrated in seminal works - consider Kernighan & Pike "The UNIX Programming Environment". 
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 01:40
                                     |
| Remember that the functions it "interrupt" are the entire call chain above the setjmp() caller (or that caller itself, if the code is in the same function).; Often the most likely async-unsafe functions to interrupt could thus be the program's own functions.  If the program has halfway updated some pointer or data structure or whatever when the signal arrives, it may be screwed.
For this reason I think the mention of async-safe functions up front is likely to be more misleading than useful.  Could turn it around and say a user program could be written to be async-safe where setjmp is concerned.  (If that is enough, I haven't thought it through.)
Anyway, setjmp/longjmp out of signal handlers seem most useful as an emergency measure to me, like most nontrivial things one may want to do in signal handlers.  Though it depends on how serious an occational crash or hang or whatever would be, of course. 
                                        Posted by hbf at Apr 18, 2008 21:11
                                     |

