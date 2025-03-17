The C Standard, 7.28.5.6 paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states that a thread shall not be joined once it was previously joined or detached.
> The termination of the other thread synchronizes with the completion of the thrd_join function. The thread identified by thr shall not have been previously detached or joined with another thread.

Similarly, subclause 7.28.5.3 paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states that a thread shall not be detached once it was previously joined or detached. 
> The thrd_detach function tells the operating system to dispose of any resources allocated to the thread identified by thr when that thread terminates. The thread identified by thr shall not have been previously detached or joined with another thread.

Violating either of these subclauses results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
This noncompliant code example detaches a thread that is later joined.
``` c
#include <stddef.h>
#include <threads.h>
int thread_func(void *arg) {
  /* Do work */
  thrd_detach(thrd_current());
  return 0;
}
int main(void) {
  thrd_t t;
  if (thrd_success != thrd_create(&t, thread_func, NULL)) {
    /* Handle error */
    return 0;
  }
  if (thrd_success != thrd_join(t, 0)) {
    /* Handle error */
    return 0;
  }
  return 0;
}
```
## Compliant Solution
 This compliant solution does not detach the thread. Its resources are released upon successfully joining with the main thread:
``` c
#include <stddef.h>
#include <threads.h>
int thread_func(void *arg) {
  /* Do work */
  return 0;
}
int main(void) {
  thrd_t t;
  if (thrd_success != thrd_create(&t, thread_func, NULL)) {
    /* Handle error */
    return 0;
  }
  if (thrd_success != thrd_join(t, 0)) {
    /* Handle error */
    return 0;
  }
  return 0;
} 
```
## Risk Assessment
Joining or detaching a previously joined or detached thread is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON39-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | CONCURRENCY.TNJ | Thread is not Joinable |
| Cppcheck Premium | 24.11.0 | premium-cert-con39-c |  |
| Helix QAC | 2024.4 | C1776 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON39-a | Do not join or detach a thread that was previously joined or detached |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON39-C | Checks for join or detach of a joined or detached thread (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON39-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.28.5.3, "The thrd_detach Function"Subclause 7.28.5.6, "The thrd_join Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152023) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151922)
## Comments:

|  |
| ----|
| There seem to be alot of undefined behaviors in C11 dealing with threading that aren't explicitlly listed in Annex J:The C Standard, subclause 7.26.5.6 [ISO/IEC 9899:2011], specifically states that a thread shall not be joined once it was previously joined or detached. Similarly, subclause 7.26.5.3 states that a thread shall not be detached once it was previously joined or detached.
                                        Posted by rcs at Oct 31, 2013 11:27
                                     |

