Accessing or modifying shared objects in signal handlers can result in race conditions that can leave data in an inconsistent state. The two exceptions (C Standard, 5.1.2.3, paragraph 5) to this rule are the ability to read from and write to lock-free atomic objects and variables of type `volatile sig_atomic_t`. Accessing any other type of object from a signal handler is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 131](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_131).)
The need for the `volatile` keyword is described in [DCL22-C. Use volatile for data that cannot be cached](DCL22-C_%20Use%20volatile%20for%20data%20that%20cannot%20be%20cached).
The type `sig_atomic_t` is the integer type of an object that can be accessed as an atomic entity even in the presence of asynchronous interrupts. The type of `sig_atomic_t` is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior), though it provides some guarantees. Integer values ranging from `SIG_ATOMIC_MIN` through `SIG_ATOMIC_MAX`, inclusive, may be safely stored to a variable of the type. In addition, when `sig_atomic_t` is a signed integer type, `SIG_ATOMIC_MIN` must be no greater than `−127` and `SIG_ATOMIC_MAX` no less than `127`. Otherwise, `SIG_ATOMIC_MIN` must be `0` and `SIG_ATOMIC_MAX` must be no less than `255`. The macros `SIG_ATOMIC_MIN` and `SIG_ATOMIC_MAX` are defined in the header `<stdint.h>`.
According to the C99 Rationale \[[C99 Rationale 2003](AA.-Bibliography_87152170.html#AA.Bibliography-C992003)\], other than calling a limited, prescribed set of library functions,
> the C89 Committee concluded that about the only thing a [strictly conforming](BB.-Definitions_87152273.html#BB.Definitions-strictlyconforming) program can do in a signal handler is to assign a value to a `volatile static` variable which can be written uninterruptedly and promptly return.

However, this issue was discussed at the April 2008 meeting of ISO/IEC WG14, and it was agreed that there are no known [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) in which it would be an error to read a value from a `volatile sig_atomic_t` variable, and the original intent of the committee was that both reading and writing variables of `volatile sig_atomic_t` would be strictly conforming.
The signal handler may also call a handful of functions, including `abort().` (See [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers) for more information.)
## Noncompliant Code Example
In this noncompliant code example, `err_msg` is updated to indicate that the `SIGINT` signal was delivered.  The `err_msg` variable is a character pointer and not a variable of type `volatile sig_atomic_t`.
``` c
#include <signal.h>
#include <stdlib.h>
#include <string.h>
enum { MAX_MSG_SIZE = 24 };
char *err_msg;
void handler(int signum) {
  strcpy(err_msg, "SIGINT encountered.");
}
int main(void) {
  signal(SIGINT, handler);
  err_msg = (char *)malloc(MAX_MSG_SIZE);
  if (err_msg == NULL) {
    /* Handle error */
  }
  strcpy(err_msg, "No errors yet.");
  /* Main code loop */
  return 0;
}
```
## Compliant Solution (Writing `volatile sig_atomic_t`)
For maximum portability, signal handlers should only unconditionally set a variable of type `volatile sig_atomic_t` and return, as in this compliant solution:
``` c
#include <signal.h>
#include <stdlib.h>
#include <string.h>
enum { MAX_MSG_SIZE = 24 };
volatile sig_atomic_t e_flag = 0;
void handler(int signum) {
  e_flag = 1;
}
int main(void) {
  char *err_msg = (char *)malloc(MAX_MSG_SIZE);
  if (err_msg == NULL) {
    /* Handle error */
  }
  signal(SIGINT, handler);
  strcpy(err_msg, "No errors yet.");
  /* Main code loop */
  if (e_flag) {
    strcpy(err_msg, "SIGINT received.");
  } 
  return 0;
}
```
## Compliant Solution (Lock-Free Atomic Access)
Signal handlers can refer to objects with static or thread storage durations that are lock-free atomic objects, as in this compliant solution:
``` c
#include <signal.h>
#include <stdlib.h>
#include <string.h>
#include <stdatomic.h>
#ifdef __STDC_NO_ATOMICS__
#error "Atomics are not supported"
#elif ATOMIC_INT_LOCK_FREE == 0
#error "int is never lock-free"
#endif
atomic_int e_flag = ATOMIC_VAR_INIT(0);
void handler(int signum) {
  e_flag = 1;
}
int main(void) {
  enum { MAX_MSG_SIZE = 24 };
  char err_msg[MAX_MSG_SIZE];
#if ATOMIC_INT_LOCK_FREE == 1
  if (!atomic_is_lock_free(&e_flag)) {
    return EXIT_FAILURE;
  }
#endif
  if (signal(SIGINT, handler) == SIG_ERR) {
    return EXIT_FAILURE;
  }
  strcpy(err_msg, "No errors yet.");
  /* Main code loop */
  if (e_flag) {
    strcpy(err_msg, "SIGINT received.");
  }
  return EXIT_SUCCESS;
}
```
## Exceptions
**SIG31-C-EX1:**  The C Standard, 7.14.1.1 paragraph 5 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\], makes a special exception for `errno` when a valid call to the `signal()` function results in a `SIG_ERR` return, allowing `errno` to take an indeterminate value. (See [ERR32-C. Do not rely on indeterminate values of errno](#).)
> the signal function with the first argument equal to the signal number corresponding to the signal that caused the invocation of the handler. Furthermore, if such a call to the signal function results in a SIG_ERR return, the object designated by errno has an indeterminate representation.

## Risk Assessment
Accessing or modifying shared objects in signal handlers can result in accessing data in an inconsistent state. Michal Zalewski's paper "Delivering Signals for Fun and Profit" \[[Zalewski 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Zalewski01)\] provides some examples of [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) that can result from violating this and other signal-handling rules.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG31-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | signal-handler-shared-access | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-SIG31 |  |
| CodeSonar | 8.3p0 | CONCURRENCY.DATARACE | Data race |
| Compass/ROSE |  |  | Can detect violations of this rule for single-file programs |
| Cppcheck Premium | 24.9.0 | premium-cert-sig31-c |  |
| Helix QAC | 2024.4 | C2029, C2030C++3854, C++3855 |  |
| LDRA tool suite | 9.7.1 | 87 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG31-a | Properly define signal handlers |
| PC-lint Plus | 1.4 | 2765 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule SIG31-C | Checks for shared data access within signal handler (rule partially covered) |
| RuleChecker | 24.04 | signal-handler-shared-access | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961:2013 | Accessing shared objects in signal handlers [accsig] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-662, Improper Synchronization | 2017-07-10: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-828, Signal Handler with Functionality that is not Asynchronous-Safe | 2017-10-30:MITRE:Unspecified Relationship2018-10-19:CERT:Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-662 and SIG31-C
CWE-662 = Union( SIG31-C, list) where list =
-   Improper synchronization of shared objects between threads
<!-- -->
-   Improper synchronization of files between programs (enabling TOCTOU race conditions
### CWE-828 and SIG31-C
CWE-828 = SIG31-C + non-async-safe things besides shared objects.
## Bibliography

|  |  |
| ----|----|
| [C99 Rationale 2003] | 5.2.3, "Signals and Interrupts" |
| [ISO/IEC 9899:2024] | Subclause 7.14.1.1, "The signal Function" |
| [Zalewski 2001] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152178) [](../c/Rule%2011_%20Signals%20_SIG_) [](../c/SIG34-C_%20Do%20not%20call%20signal__%20from%20within%20interruptible%20signal%20handlers)
## Comments:

|  |
| ----|
| Yes, that's right.  A signal handler can store into a volatile sig_atomic_t of static storage duration but cannot read it.  SIG00-A has one such access and it documents its violation of SIG31-C.  If an NCCE surfaces that doesn't violate SIG31-C, so much the better.
Signal handlers can access all of their parameters and local variables.  Only objects of static storage duration are off limits.  For the purposes of this restriction, objects in the heap count as having static storage duration.  The purpose is to allow all accesses in the signal handler's stack frame, and disallow everything but a store to a volatile sig_atomic_t everywhere else.
Of course, this is just for maximally portable code.  Most systems allow their own set of additional actions.
                                        Posted by dmk at Mar 28, 2008 12:32
                                     |
| Mitigation Strategies
Static Analysis
Compliance with this rule can be checked using structural static analysis checkers using the following algorithm:
    Traverse the abstract syntax tree (AST) to identify function calls to the signal function signal(int, void (*f)(int)).
    At each function call to signal(int, void (*f)(int)) get the second argument from the argument list. To make sure that this is not an overloaded function the function type signature is evaluated and/or the location of the declaration of the function is verified to be from the correct file (because this is not a link-time analysis it is not possible to test the library implementation).  Any definition for signal() in the application is suspicious, because it should be in a library.
    Perform a nested query to identify all referenced objects with static storage duration. Verify that none of these objects are referenced as an rvalue, and that for each object referenced as an lvalue, the underlying type is sig_atomic_t.
    Report any violations detected.
                                        Posted by rcs at Apr 13, 2008 21:29
                                     |
| Text and compliant example now both get & set static volatile sig_atomic_t values
                                        Posted by svoboda at Apr 15, 2008 09:45
                                     |
| It should be mentioned that _Exit (and probably abort) are not advisable, because atexit-registered handlers should be allowed to perform their intended functions before the program is terminated.
Also, there;seems to be no real reason for a signal handler to want to read a flag; setting it is sufficient.
                                        Posted by dagwyn at Apr 18, 2008 11:47
                                     |
| re: _Exit()/abort(). Didn't we have this conversation on SIG30-C?
re: handlers reading flags. True, the examples didn't use to read flags. SIG00-C has example code that reads flags (implementing a finite state machine with them). The examples here do illustrate that reading sig_atomic_t flags is perfectly safe (if not particularly useful 
                                        Posted by svoboda at Apr 18, 2008 14:07
                                     |
| should we remove the note about "This may be necessary to ensure that the handler persists" since the cited recommendation tells us not to do this because of the race condition?
                                        Posted by avolkovi at May 20, 2008 13:33
                                     |
| Yes, I updated that paragraph, mainly deferring to SIG30, which discusses safe functions to call in signal handlers.
                                        Posted by svoboda at May 20, 2008 13:43
                                     |
| Why is the Rem Cost high here? It should be easy to inspect a signal handler source code to see if it references any static data, and whether that data is volatile sig_atomic_t. It would still be hard to repair. So the Remediation Cost should be Medium.
                                        Posted by svoboda at Mar 27, 2023 13:54
                                     |

