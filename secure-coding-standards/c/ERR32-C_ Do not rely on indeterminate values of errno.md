According to the C Standard Annex J.2 (133) \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], the behavior of a program is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when
> the value of `errno` is referred to after a signal occurred other than as the result of calling the `abort` or `raise` function and the corresponding signal handler obtained a `SIG_ERR` return from a call to the `signal` function.

See [undefined behavior 133](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_133).
A signal handler is allowed to call `signal();` if that fails, `signal()` returns `SIG_ERR` and sets `errno` to a positive value. However, if the event that caused a signal was external (not the result of the program calling `abort()` or `raise()`), the only functions the signal handler may call are `_Exit()` or `abort()`, or it may call `signal()` on the signal currently being handled; if `signal()` fails, the value of `errno` is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue).
This rule is also a special case of [SIG31-C. Do not access shared objects in signal handlers](SIG31-C_%20Do%20not%20access%20shared%20objects%20in%20signal%20handlers). The object designated by `errno` is of static storage duration and is not a `volatile sig_atomic_t`. As a result, performing any action that would require `errno` to be set would normally cause [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The C Standard, 7.14.1.1, paragraph 5, makes a special exception for `errno` in this case, allowing `errno` to take on an indeterminate value but specifying that there is no other [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). This special exception makes it possible to call `signal()` from within a signal handler without risking [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), but the handler, and any code executed after the handler returns, must not depend on the value of `errno` being meaningful.
## Noncompliant Code Example
The `handler()` function in this noncompliant code example attempts to restore default handling for the signal indicated by `signum`. If the request to set the signal to default can be honored, the `signal()` function returns the value of the signal handler for the most recent successful call to the `signal()` function for the specified signal. Otherwise, a value of `SIG_ERR` is returned and a positive value is stored in `errno`. Unfortunately, the value of `errno` is indeterminate because the `handler()` function is called when an external signal is raised, so any attempt to read `errno` (for example, by the `perror()` function) is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
typedef void (*pfv)(int);
void handler(int signum) {
  pfv old_handler = signal(signum, SIG_DFL);
  if (old_handler == SIG_ERR) {
    perror("SIGINT handler"); /* Undefined behavior */
    /* Handle error */
  }
}
int main(void) {
  pfv old_handler = signal(SIGINT, handler);
  if (old_handler == SIG_ERR) {
    perror("SIGINT handler");
    /* Handle error */
  }
  /* Main code loop */
  return EXIT_SUCCESS;
}
```
The call to `perror()` from `handler()` also violates [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers).
## Compliant Solution
This compliant solution does not reference `errno` and does not return from the signal handler if the `signal()` call fails:
``` c
#include <signal.h>
#include <stdlib.h>
#include <stdio.h>
typedef void (*pfv)(int);
void handler(int signum) {
  pfv old_handler = signal(signum, SIG_DFL);
  if (old_handler == SIG_ERR) {
    abort();
  }
}
int main(void) {
  pfv old_handler = signal(SIGINT, handler);
  if (old_handler == SIG_ERR) {
    perror("SIGINT handler");
    /* Handle error */
  }
  /* Main code loop */
  return EXIT_SUCCESS;
}
```
## Noncompliant Code Example (POSIX)
POSIX is less restrictive than C about what applications can do in signal handlers. It has a long list of [asynchronous-safe](BB.-Definitions_87152273.html#BB.Definitions-asynchronous-safe) functions that can be called. (See [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers).) Many of these functions set `errno` on error, which can lead to a signal handler being executed between a call to a failed function and the subsequent inspection of `errno`. Consequently, the value inspected is not the one set by that function but the one set by a function call in the signal handler. POSIX applications can avoid this problem by ensuring that signal handlers containing code that might alter `errno`; always save the value of `errno` on entry and restore it before returning.
The signal handler in this noncompliant code example alters the value of `errno`. As a result, it can cause incorrect error handling if executed between a failed function call and the subsequent inspection of `errno`:
``` c
#include <signal.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>
void reaper(int signum) {
  errno = 0;
  for (;;) {
    int rc = waitpid(-1, NULL, WNOHANG);
    if ((0 == rc) || (-1 == rc && EINTR != errno)) {
      break;
    }
  }
  if (ECHILD != errno) {
    /* Handle error */
  }
}
int main(void) {
  struct sigaction act;
  act.sa_handler = reaper;
  act.sa_flags = 0;
  if (sigemptyset(&act.sa_mask) != 0) {
    /* Handle error */
  }
  if (sigaction(SIGCHLD, &act, NULL) != 0) {
    /* Handle error */
  }
  /* ... */
  return EXIT_SUCCESS;
}
```
## Compliant Solution (POSIX)
This compliant solution saves and restores the value of `errno` in the signal handler:
``` c
#include <signal.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/wait.h>
void reaper(int signum) {
  errno_t save_errno = errno;
  errno = 0;
  for (;;) {
    int rc = waitpid(-1, NULL, WNOHANG);
    if ((0 == rc) || (-1 == rc && EINTR != errno)) {
      break;
    }
  }
  if (ECHILD != errno) {
    /* Handle error */
  }
  errno = save_errno;
}
int main(void) {
  struct sigaction act;
  act.sa_handler = reaper;
  act.sa_flags = 0;
  if (sigemptyset(&act.sa_mask) != 0) {
    /* Handle error */
  }
  if (sigaction(SIGCHLD, &act, NULL) != 0) {
    /* Handle error */
  }
  /* ... */
  return EXIT_SUCCESS;
}
```
## Risk Assessment
Referencing indeterminate values of `errno` is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR32-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | chained-errno-function-callserrno-test-after-wrong-call | Supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ERR32 |  |
| Compass/ROSE |  |  | Could detect violations of this rule by looking for signal handlers that themselves call signal(). A violation is reported if the call fails and the handler therefore checks errno. A violation also exists if the signal handler modifies errno without first copying its value elsewhere |
| Coverity | 2017.07 | MISRA C 2012 Rule 22.8MISRA C 2012 Rule 22.9MISRA C 2012 Rule 22.10 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-err32-c |  |
| Helix QAC | 2024.4 | C2031DF4781, DF4782, DF4783 |  |
| Klocwork | 2024.4 | MISRA.INCL.SIGNAL.2012MISRA.STDLIB.SIGNAL |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR32-b | Properly define signal handlers |
| Polyspace Bug Finder | R2024a | CERT C: Rule ERR32-C | Checks for misuse of errno in a signal handler (rule fully covered) |
| RuleChecker | 24.04 | chained-errno-function-callserrno-test-after-wrong-call
 | Supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | SIG30-C. Call only asynchronous-safe functions within signal handlers | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | SIG31-C. Do not access shared objects in signal handlers | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.14.1.1, "The signal Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152351) [](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152272)
## Comments:

|  |
| ----|
| The compliant code example violates SIG32, which dictates that only volatile sig_atomic_t variables should be accessed from within a signal handler.
The non-compliant code example violates both SIG32 and SIG31, too.
Right now this rule looks to me more like it belongs in the SIG section. I think it should be transferred there OR a coding example (compliant or non-compliant) that does not involve signals should be added to this rule.
                                        Posted by svoboda at Mar 26, 2008 17:03
                                     |
| I still see a problem with the CCE... what happens when the signal() inside of handler fails and trashes errno for some other function?
int main(void) {
  /* register handler() */
  if(somefunction() != 0) {
    /**** SIGNAL EVENT ****/
    perror("SomeFunction Error:");
  }
}

The `perror()` might print the wrong message if `errno` was changed by the signal handler...
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 01, 2008 09:41
\| \|
I have fixed this by making the handler abort if the signal() call fails.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 11, 2008 12:39
\| \|
Isn't it possible that in this reference to `errno` in the compliant solution for POSIX:
``` java
void reaper(int signum) {
  int save_errno = errno;
```
that the value of `errno` is indeterminate? if it is, how would this effect the execution of this code?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 20, 2008 09:15
\| \|
The value of `errno` at that point would only be indeterminate if a signal handler has previously been executed which did not save and restore errno (and which contains code that might alter `errno`).
Would it help if the text said "POSIX applications can avoid this problem by ensuring that all signal handlers ..."?
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 20, 2008 10:07
\| \|
Is it really safe and compliant to save errno when entering a signal handler and then restore errno when leaving the handler; e.g. do something like this :
``` java
void handle(int signum)
{
  int saved_errno = errno;
  /* Handler code that may alter errno */
  /* Restore original errno before leaving */
  errno = saved_errno;
} // (cleaned up spacing ~DS)
```
Not that sure since only volatile sig_atomic_t global variables can be safely set from a signal handler and I'm not sure errno is required to be volatile sig_atomic_t by C99 or POSIX... If it's not, what's the safe solution ?
![](images/icons/contenttypes/comment_16.png) Posted by jlc at Jul 24, 2008 12:52
\| \|
Good question!
[1999](#) Section 7.14.1.1, "The signal function", paragraph 5 sez:
> If the signal occurs other than as the result of calling the abort or raise function, the behavior is undefined if the signal handler refers to any object with static storage duration other than by assigning a value to an object declared as volatile sig_atomic_t, or the signal handler calls any function in the standard library other than the abort function, the \_Exit function, or the signal function with the first argument equal to the signal number corresponding to the signal that caused the invocation of the handler. Furthermore, if such a call to the signal function results in a ,SIG_ERR return, the value of errno is indeterminate.

The POSIX standard contains a nearly identical paragraph.
I see nothing about a 'special exception' for working with `errno` in a signal handler. At the very least we need to update the reference.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 24, 2008 14:00
\| \|
The `signal()` page in POSIX is basically a legacy page which closely matches the C Standard. POSIX applications should not use `signal()`, they should use `sigaction()`.
The rules for signal handling when `sigaction()` is used are in XSH 2.4.3, which says (in the new 2008 revision):
> Operations which obtain the value of errno and operations which assign a value to errno shall be async-signal-safe.

![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jul 25, 2008 04:56
\| \|
According to POSIX, "The symbol *errno*, defined by including the \<errno.h\> header, expands to a modifiable lvalue of type **int**"
But there is no requirement for errno to be volatile sig_atomic_t.
On many plateforms, sig_atomic_t is actually an int; so on those plateforms errno is sig_atomic_t. However, this is still not "volatile sig_atomic_t" as required for global variables set in signal handlers ... So what ?
![](images/icons/contenttypes/comment_16.png) Posted by jlc at Jul 25, 2008 09:14
\| \|
Right. Hence the need for the explicit requirement about `errno` in XSH 2.4.3 that I quoted above.
This was added in the latest revision precisely because it was known that saving and restoring errno in signal handlers is recommended practice, but it was not previously clear whether POSIX allowed it.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jul 25, 2008 10:09
\| \|
I agree; this rule belongs in the SIG section.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 29, 2013 10:49
\| \|
The use of `errno_t` in the last **Compliant Solution (POSIX)** is not strictly conforming (i.e., it's unportable). First, `errno_t` is not a POSIX type (the latest POSIX, SUSv4, is based on C99, not C11). Second, even when POSIX adopts C11 (unless it mandates Annex K, which is unlikely), `errno_t` will be a conditionally defined type.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 04, 2014 19:34
\| \|
;
Yup.  [DCL09-C. Declare functions that return errno with a return type of errno_t](https://www.securecoding.cert.org/confluence/display/seccode/DCL09-C.+Declare+functions+that+return+errno+with+a+return+type+of+errno_t) describes the use of errno_t.  There is a very long sequence of code that can be written to use errno_t if conditionally defined or define it if it is not, e.g.: 
`#``ifdef __STDC_LIB_EXT1__`
`#define __STDC_WANT_LIB_EXT1__ 1`
`#include <errno.h>`
`#elif`
`  ``typedef` `int` `errno_t;`
`#endif`
Doing this for each example would be a distraction, but in a real program this would all be performed in a single header file and errno_t could be used freely.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 06, 2014 07:18
\| \|
POSIX extends the C standard with a special exception just for `errno`, for the very purpose of making that safe:
> the behavior is undefined if the signal handler refers to any object <sup>\[[CX](https://pubs.opengroup.org/onlinepubs/9699919799/help/codes.html#CX)\]</sup> ![](https://pubs.opengroup.org/onlinepubs/9699919799/images/opt-start.gif) ;other than *errno* ![](https://pubs.opengroup.org/onlinepubs/9699919799/images/opt-end.gif)  with static storage duration other than by assigning a value to an object declared as **volatile sig_atomic_t**

![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:54
\| \|
Hi, I had a question about the specific wording "value of;`errno` is referred to after a signal occurred other than as the result of calling the **`abort` or `raise` function**"   
does this mean that the whole rule does not apply to signal handlers registered to handle `SIGABRT` , and those signal handlers are safe to refer to \`errno\`?  
to confirm/make it clear, the following would be appropriately labelled?:  
``` java
void handler1(int signum) {
  pfv old_handler = signal(signum, SIG_DFL);
  if (old_handler != SIG_ERR) {
    perror(""); // COMPLIANT
  } else {
    perror(""); // COMPLIANT
  }
}
void handler2(int signum) {
  pfv old_handler = signal(signum, SIG_DFL);
  if (old_handler == SIG_ERR) {
    perror(""); // NON_COMPLIANT
  }
}
int main(void) {
  old_handler = signal(SIGABRT, handler1);
  old_handler = signal(SIGINT, handler2);
  FILE *fp1 = fopen("something", "r");
  if (fp1 == NULL) {
    perror("Error: "); // NON_COMPLIANT (because of handler2 but not because of handler1)
  }
```
    Thanks for the consideration!
![](images/icons/contenttypes/comment_16.png) Posted by knewbury01 at Jan 16, 2023 14:10
\| \|
Kristen:
To answer your question, we need a few more citations from ISO C:
Section 7.14.1.1, paragraph 5 says:
> If the signal occurs other than as the result of calling the abort or raise function, the behavior is undefined if the signal handler refers to any object with static or thread storage duration that is not a lock-free atomic object other than by assigning a value to an object declared as volatile sig_atomic_t...

Paragraph 7 says:
> Use of the signal() function in a multi-threaded program results in undefined behavior

Furthermore, errno is a modifiable lvalue of type int (section 7.5 paragraph 2). Which means that a signal handler must not read or write errno if it is not executed as a result of calling abort() or raise().
Armed with that info, we now turn to your code. As written, the code is compliant if no external process ever sends a SIGABRT or SIGINT, because then the signal handlers are never invoked.
Now to your question: ;If the program receives SIGINT, then handler2 is invoked and undefined behavior occurs because it implicitly handles errno via perror().
If the program receives SIGABRT, then handler1 is invoked. The code does not violate the rule in handling errno, but it might still violate the rule elsewhere in perror()...such as accessing stderr.  A more compliant example would be:
    volatile sig_atomic_t error_value = 0;
    void handler1(int signum) {
      pfv old_handler = signal(signum, SIG_DFL);
      if (old_handler != SIG_ERR) {
        error_value = errno; // DEFINITELY COMPLIANT
      }
    }
In conclusion, signals are very underspecified in ISO C. POSIX is a bit more complete in specifying behavior if you use sigaction(2). However, you will be better off using threads and IPC to address such cases. If you must use signals, use a volatile sig_atomic_t value to record that a signal was sent...see the SIG chapter of the CERT Secure Coding standard.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 17, 2023 09:37
\| \|
I just realized that there is a simpler rationale behind signal handlers being mostly undefined:
s7.24.4.1p2 describes the behavior of abort():
;   The abort function causes abnormal program termination to occur,  
    unless the signal SIGABRT is being caught and the signal handler  
    does not return. Whether open streams with unwritten buffered data  
    are flushed, open streams are closed, or temporary files are  
    removed is implementation- defined. An implementation-defined form  
    of the status unsuccessful termination is returned to the host  
    environment by means of the function call raise(SIGABRT).
While this is rather circumspect, it does strongly imply that calling abort() is equivalent to calling raise(SIGABRT).
The whole reason for signal handlers being dangerous is that they can interrupt sensitive code. For example, a signal handler that is invoked while the program was originally in the middle of the malloc() function might discover that the heap is currently in an inconsistent state (because malloc() hasn't finished yet). Even in a single-threaded program.   However, if that program invokes a signal handler via raise() or abort(), then that program can not be in the middle of a call to malloc() or some other sensitive function.
So to re-interpret your program; again it is OK as written if the signal handlers are never invoked. But if either handler1 or handler2 are invoked as the result of a signal being sent from some external source, then either one results in undefined behavior, since they might have interrupted something sensitive.   And finally if your program calls raise() or abort() and uses those to invoke either handler, then the behavior is well-defined.  Conclusion: the actual signal that was sent is irrelevant; What is relevant is whether or not the program was interrupted from doing something potentially sensitive.
My last paragraph (about signals being underspecified) is still correct however.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 20, 2023 09:27
\|
