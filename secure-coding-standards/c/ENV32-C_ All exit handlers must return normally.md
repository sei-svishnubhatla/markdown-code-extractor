The C Standard provides three functions that cause an application to terminate normally: `_Exit()`, `exit()`, and `quick_exit()`. These are collectively called *exit functions*. When the `exit()` function is called, or control transfers out of the `main()` entry point function, functions registered with `atexit()` are called (but not `at_quick_exit()`). When the `quick_exit()` function is called, functions registered with `at_quick_exit()` (but not `atexit()`) are called. These functions are collectively called *exit handlers*.  When the `_Exit()` function is called, no exit handlers or signal handlers are called.
Exit handlers must terminate by returning. It is important and potentially safety-critical for all exit handlers to be allowed to perform their cleanup actions. This is particularly true because the application programmer does not always know about handlers that may have been installed by support libraries. Two specific issues include nested calls to an exit function and terminating a call to an exit handler by invoking `longjmp`.
A nested call to an exit function is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 182](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).) This behavior can occur only when an exit function is invoked from an exit handler or when an exit function is called from within a signal handler. (See [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers).)
If a call to the `longjmp()` function is made that would terminate the call to a function registered with `atexit()`, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
In this noncompliant code example, the `exit1()` and `exit2()` functions are registered by `atexit()` to perform required cleanup upon program termination. However, if `some_condition` evaluates to true, `exit()` is called a second time, resulting in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
#include <stdlib.h>
void exit1(void) {
  /* ... Cleanup code ... */
  return;
}
void exit2(void) {
  extern int some_condition;
  if (some_condition) {
    /* ... More cleanup code ... */
    exit(0);
  }
  return;
}
int main(void) {
  if (atexit(exit1) != 0) {
    /* Handle error */
  }
  if (atexit(exit2) != 0) {
    /* Handle error */
  }
  /* ... Program code ... */
  return 0;
}
```
Functions registered by the `atexit()` function are called in the reverse order from which they were registered. Consequently, if `exit2()` exits in any way other than by returning, `exit1()` will not be executed. The same may also be true for `atexit()` handlers installed by support libraries.
## Compliant Solution
A function that is registered as an exit handler by `atexit()` must exit by returning, as in this compliant solution:
``` c
#include <stdlib.h>
void exit1(void) {
  /* ... Cleanup code ... */
  return;
}
void exit2(void) {
  extern int some_condition;
  if (some_condition) {
    /* ... More cleanup code ... */
  }
  return;
}
int main(void) {
  if (atexit(exit1) != 0) {
    /* Handle error */
  }
  if (atexit(exit2) != 0) {
    /* Handle error */
  }
  /* ... Program code ... */
  return 0;
}
```
## Noncompliant Code Example
In this noncompliant code example, `exit1()` is registered by `atexit()` so that upon program termination, `exit1()` is called. The `exit1()` function jumps back to `main()` to return, with undefined results.
``` c
#include <stdlib.h>
#include <setjmp.h>
jmp_buf env;
int val;
void exit1(void) {
  longjmp(env, 1);
}
int main(void) {
  if (atexit(exit1) != 0) {
    /* Handle error */
  }
  if (setjmp(env) == 0) {
    exit(0);
  } else {
    return 0;
  }
}
```
## Compliant Solution
This compliant solution does not call `longjmp()``but instead returns from the exit handler normally:`
``` c
#include <stdlib.h>
void exit1(void) {
  return;
}
int main(void) {
  if (atexit(exit1) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Risk Assessment
Terminating a call to an exit handler in any way other than by returning is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and may result in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) or other unpredictable behavior. It may also prevent other registered handlers from being invoked.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV32-C | Medium | Likely | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | user_definedbad-functionbad-function-use | Soundly supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ENV32 |  |
| CodeSonar | 8.3p0 | BADFUNC.ABORTBADFUNC.EXIT
BADFUNC.LONGJMP | Use of abortUse of exit
Use of longjmp |
| Compass/ROSE |  |  | Can detect violations of this rule. In particular, it ensures that all functions registered with atexit() do not call functions such as exit() |
| Cppcheck Premium | 24.9.0 | premium-cert-env32-c |  |
| Helix QAC | 2024.4 | DF4856, DF4857, DF4858 |  |
| Klocwork | 2024.4 | CERT.EXIT.HANDLER_TERMINATE |  |
| LDRA tool suite | 9.7.1 | 122 S7 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV32-a | Properly define exit handlers |
| Polyspace Bug Finder | R2024a | CERT C: Rule ENV32-C | Checks for abnormal termination of exit handler (rule fully covered) |
| RuleChecker | 24.04 | bad-functionbad-function-use | Supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | SIG30-C. Call only asynchronous-safe functions within signal handlers | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Structured Programming [EWD] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Termination Strategy [REU] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-705, Incorrect Control Flow Scoping | 2017-07-10: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-705 and ENV32-C
CWE-705 = Union( ENV32-C, list) where list =
-   Improper control flow besides a non-returning exit handler
------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152100) [](../c/Rule%2010_%20Environment%20_ENV_) [](../c/ENV33-C_%20Do%20not%20call%20system__)
## Comments:

|  |
| ----|
| I think we have other exit-related rules in the Error Handling section.
                                        Posted by svoboda at Nov 04, 2008 15:07
                                     |

