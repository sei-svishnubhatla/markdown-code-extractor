The `cnd_wait()` and cnd_timedwait() functions temporarily cede possession of a mutex so that other threads that may be requesting the mutex can proceed. These functions must always be called from code that is protected by locking a mutex. The waiting thread resumes execution only after it has been notified, generally as the result of the invocation of the `cnd_signal()` or `cnd_broadcast()` function invoked by another thread. The `cnd_wait()` function must be invoked from a loop that checks whether a [condition predicate](BB.-Definitions_87152273.html#BB.Definitions-conditionpredicate) holds. A condition predicate is an expression constructed from the variables of a function that must be true for a thread to be allowed to continue execution. The thread pauses execution, via `cnd_wait()`, `cnd_timedwait()`, or some other mechanism, and is resumed later, presumably when the condition predicate is true and the thread is notified.
``` java
#include <threads.h>
#include <stdbool.h>
extern bool until_finish(void);
extern mtx_t lock;
extern cnd_t condition;
void func(void) {
  if (thrd_success != mtx_lock(&lock)) {
    /* Handle error */
  }
  while (until_finish()) {  /* Predicate does not hold */
    if (thrd_success != cnd_wait(&condition, &lock)) {
      /* Handle error */
    }
  }
  /* Resume when condition holds */
  if (thrd_success != mtx_unlock(&lock)) {
    /* Handle error */
  }
}
```
The notification mechanism notifies the waiting thread and allows it to check its condition predicate. The invocation of `cnd_broadcast()` in another thread cannot precisely determine which waiting thread will be resumed. Condition predicate statements allow notified threads to determine whether they should resume upon receiving the notification. 
## Noncompliant Code Example
This noncompliant code example monitors a linked list and assigns one thread to consume list elements when the list is nonempty. 
This thread pauses execution using `cnd_wait()` and resumes when notified, presumably when the list has elements to be consumed. It is possible for the thread to be notified even if the list is still empty, perhaps because the notifying thread used `cnd_broadcast()`, which notifies all threads. Notification using `cnd_broadcast()` is frequently preferred over using `cnd_signal().` (See [CON38-C. Preserve thread safety and liveness when using condition variables](CON38-C_%20Preserve%20thread%20safety%20and%20liveness%20when%20using%20condition%20variables) for more information.)
A condition predicate is typically the negation of the condition expression in the loop. In this noncompliant code example, the condition predicate for removing an element from a linked list is `(list->next != NULL)`, whereas the condition expression for the `while` loop condition is `(list->next == NULL)`.
This noncompliant code example nests the `cnd_wait()` function inside an `if` block and consequently fails to check the condition predicate after the notification is received. If the notification was spurious or malicious, the thread would wake up prematurely.
``` c
#include <stddef.h>
#include <threads.h>
struct node_t {
  void *node;
  struct node_t *next;
};
struct node_t list;
static mtx_t lock;
static cnd_t condition;
void consume_list_element(void) {
  if (thrd_success != mtx_lock(&lock)) {
    /* Handle error */
  }
  if (list.next == NULL) {
    if (thrd_success != cnd_wait(&condition, &lock)) {
      /* Handle error */
    }
  }
  /* Proceed when condition holds */
  if (thrd_success != mtx_unlock(&lock)) {
    /* Handle error */
  }
}
```
## Compliant Solution
This compliant solution calls the `cnd_wait()` function from within a `while` loop to check the condition both before and after the call to `cnd_wait()`:
``` c
#include <stddef.h>
#include <threads.h>
struct node_t {
  void *node;
  struct node_t *next;
};
struct node_t list;
static mtx_t lock;
static cnd_t condition;
void consume_list_element(void) {
  if (thrd_success != mtx_lock(&lock)) {
    /* Handle error */
  }
  while (list.next == NULL) {
    if (thrd_success != cnd_wait(&condition, &lock)) {
      /* Handle error */
    }
  }
  /* Proceed when condition holds */
  if (thrd_success != mtx_unlock(&lock)) {
    /* Handle error */
  }
}
```
## Risk Assessment
Failure to enclose calls to the `cnd_wait()` or `cnd_timedwait()` functions inside a `while` loop can lead to indefinite blocking and [denial of service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) (DoS).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON36-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.STRUCT.ICOLCONCURRENCY.BADFUNC.CNDWAIT | Inappropriate Call Outside LoopUse of Condition Variable Wait |
| Cppcheck Premium | 24.11.0 | premium-cert-con36-c |  |
| Helix QAC | 2024.4 | C2027 |  |
| Klocwork | 2024.4 | CERT.CONC.WAKE_IN_LOOP_C |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON36-a | Wrap functions that can spuriously wake up in a loop |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON36-C | Checks for situations where functions that can spuriously wake up are not wrapped in loop (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON36-C). 
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | THI03-J. Always invoke wait() and await() methods inside a loop | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Lea 2000] | 1.3.2, "Liveness"3.2.2, "Monitor Mechanics" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152261) [](../c/Rule%2014_%20Concurrency%20_CON_) [](../c/CON37-C_%20Do%20not%20call%20signal__%20in%20a%20multithreaded%20program)
