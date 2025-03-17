Do not send an uncaught signal to kill a thread because the signal kills the entire process, not just the individual thread. This rule is a specific instance of [SIG02-C. Avoid using signals to implement normal functionality](SIG02-C_%20Avoid%20using%20signals%20to%20implement%20normal%20functionality).
In POSIX systems, using the `signal()` function in a multithreaded program falls under exception **CON37C-C-EX0** of rule [CON37-C. Do not call signal() in a multithreaded program](CON37-C_%20Do%20not%20call%20signal__%20in%20a%20multithreaded%20program).
## Noncompliant Code Example
This code uses the `pthread_kill()` function to send a `SIGTERM` signal to the created thread. The thread receives the signal, and the entire process is terminated.
``` c
void func(void *foo) {
  /* Execution of thread */
}
int main(void) {
  int result;
  pthread_t thread;
  if ((result = pthread_create(&thread, NULL, func, 0)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_kill(thread, SIGTERM)) != 0) {
    /* Handle Error */
  }
  /* This point is not reached because the process terminates in pthread_kill() */
  return 0;
}
```
## Compliant Solution
This compliant code uses instead the `pthread_cancel()` function to terminate the thread. The thread continues to run until it reaches a cancellation point. See [The Open Group Base Specifications Issue 6, IEEE Std 1003.1, 2004 Edition](http://www.opengroup.org/onlinepubs/009695399/toc.htm) \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] for lists of functions that are required and allowed to be cancellation points. If the cancellation type is set to asynchronous, the thread is terminated immediately. However, POSIX requires only the `pthread_cancel()`, `pthread_setcancelstate()`, and `pthread_setcanceltype()` functions to be async-cancel safe. An application that calls other POSIX functions with asynchronous cancellation enabled is nonconforming. Consequently, we recommend disallowing asynchronous cancellation, as explained by [POS47-C. Do not use threads that can be canceled asynchronously](POS47-C_%20Do%20not%20use%20threads%20that%20can%20be%20canceled%20asynchronously).
``` c
void func(void *foo) {
  /* Execution of thread */
}
int main(void) {
  int result;
  pthread_t thread;
  if ((result = pthread_create(&thread, NULL, func, 0)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_cancel(thread)) != 0) {
    /* Handle Error */
  }
  /* Continue executing */
  return 0;
}
```
## Risk Assessment
Sending the signal to a process causes it to be [abnormally terminated](BB.-Definitions_87152273.html#BB.Definitions-abnormalend).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS44-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | CONCURRENCY.BADFUNC.PTHREAD_KILL | Use of pthread_kill |
| Helix QAC | 2024.4 | C5034 |  |
| Klocwork | 2024.4 | MISRA.INCL.SIGNAL.2012
 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS44-a | The 'pthread_kill', 'pthread_sigqueue' and 'tgkill' functions should not be used to send signals to threads |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS44-C | Checks for use of signal to kill thread (rule fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS35-C).
## Bibliography

|  |  |
| ----|----|
| [OpenBSD] | signal();Man Page |
| [MKS] | pthread_cancel();Man Page |
| [Open Group 2004] | ;Threads Overview |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152329) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152298)
