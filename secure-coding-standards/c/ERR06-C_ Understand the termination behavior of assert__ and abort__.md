The C Standard, subclause 7.2.1.1 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], defines `assert()` to have the following behavior:
> The `assert` macro puts diagnostic tests into programs; it expands to a void expression. When it is executed, if `expression` (which shall have a scalar type) is false (that is, compares equal to 0), the `assert` macro writes information about the particular call that failed (including the text of the argument, the name of the source file, the source line number, and the name of the enclosing function—the latter are respectively the values of the pre-processing macros `__`*`FILE_`*`_` and `__`*`LINE_`*`_` and of the identifier `__`*`func_`*`_)` on the standard error stream in an implementation-defined format. It then calls the `abort` function.

Because `assert()` calls `abort()`, cleanup functions registered with `atexit()` are not called. If the intention of the programmer is to properly clean up in the case of a failed assertion, then runtime assertions should be replaced with static assertions where possible. (See [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression).) When the assertion is based on runtime data, the `assert` should be replaced with a runtime check that implements the adopted error strategy (see [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy)).
See [ERR04-C. Choose an appropriate termination strategy](ERR04-C_%20Choose%20an%20appropriate%20termination%20strategy) for more information on program termination strategies and [MSC11-C. Incorporate diagnostic tests using assertions](MSC11-C_%20Incorporate%20diagnostic%20tests%20using%20assertions) for more information on using the `assert()` macro.
## Noncompliant Code Example
This noncompliant code example defines a function that is called before the program exits to clean up:
``` c
void cleanup(void) {
  /* Delete temporary files, restore consistent state, etc. */
}
int main(void) {
  if (atexit(cleanup) != 0) {
    /* Handle error */
  }
  /* ... */
  assert(/* Something bad didn't happen */);
  /* ... */
}
```
However, the code also has an `assert`, and if the assertion fails, the `cleanup()` function is *not* called.
## Compliant Solution
In this compliant solution, the call to `assert()` is replaced with an `if` statement that calls `exit()` to ensure that the proper termination routines are run:
``` c
void cleanup(void) {
  /* Delete temporary files, restore consistent state, etc. */
}
int main(void) {
  if (atexit(cleanup) != 0) {
    /* Handle error */
  }
  /* ... */
  if (/* Something bad happened */) {
    exit(EXIT_FAILURE);
  }
  /* ... */
}
```
## Risk Assessment
Unsafe use of `abort()` may leave files written in an inconsistent state. It may also leave sensitive temporary files on the file system.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR06-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bad-functionbad-macro-use | Supported |
| Compass/ROSE |  |  | Can detect some violations of this rule. However, it can only detect violations involving abort() because assert() is implemented as a macro |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR06-a | Do not use assertions |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| PVS-Studio | 7.35 | V2021 |  |
| RuleChecker | 24.04 | bad-functionbad-macro-use | Supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabilty) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR06-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ERR06-CPP. Understand the termination behavior of assert() and abort() |
| ISO/IEC TR 24772:2013 | Termination Strategy [REU] |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.2.1.1, "The assert Macro" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152136) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](../c/ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't)
## Comments:

|  |
| ----|
| Still need some way to verify that the signal is raised by abort/assert and not something else... otherwise somebody could send us a SIGABRT asynchronously and we would still end up calling exit()
                                        Posted by avolkovi at May 19, 2008 12:10
                                     |
| AFAIK there is no standard way to know if a signal was sent by the program (say by an assertion failure) or externally. One can prevent external signals by using masks, and one can always provide some internal mechanism (eg set a global flag around assertions) to detect synchronous signals.
Assuming your cleanup() function does things not safe to do in a signal handler, you are basically asking attackers to kindly not send SIGABRT to your program...not a safe proposition.
                                        Posted by svoboda at May 20, 2008 14:13
                                     |
| I agree with David.  The only safe way to deal with signals is to implement an event-driven architecture with a main loop that occasionally polls the status of volatile sig_atomic_t flags and takes action appropriately (see SIG30-C. Call only asynchronous-safe functions within signal handlers) for example.  
I think some other solutions you should suggest as part of this recommendation are:
1) don't use assert() for detecting runtime errors in systems where terminating the system with a call to abort() is not an option.
2) use static assertions DCL03-C. Use a static assertion to test the value of a constant expression
The compliant solution, in fact, may say "replace runtime assertions with static assertions where possible, and when the assertion is based on runtime data, replace the assert with a runtime check that implements the adopted error strategy ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy.
                                        Posted by rcs_mgr at May 30, 2008 11:05
                                     |
| I changed the name of the rule and incorporated your suggestions.
                                        Posted by avolkovi at Jun 02, 2008 14:05
                                     |

