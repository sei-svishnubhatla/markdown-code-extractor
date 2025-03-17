If a lock is being held and an operation that can block is performed, any other thread that needs to acquire that lock may also block. This condition can degrade system performance or cause a deadlock to occur.  Blocking calls include, but are not limited to, network, file, and console I/O.
Using a blocking operation while holding a lock may be unavoidable for a portable solution. For instance, file access could be protected via a lock to prevent multiple threads from mutating the contents of the file. Or, a thread may be required to block while holding one or more locks and waiting to acquire another lock. In these cases, attempt to hold the lock for the least time required. Additionally, if acquiring multiple locks, the order of locking must avoid deadlock, as specified in [CON35-C. Avoid deadlock by locking in a predefined order](CON35-C_%20Avoid%20deadlock%20by%20locking%20in%20a%20predefined%20order).
## Noncompliant Code Example
This noncompliant example calls `fopen()` while a mutex is locked. The calls to `fopen()` and `fclose()` are blocking and may block for an extended period of time if the file resides on a network drive. While the call is blocked, other threads that are waiting for the lock are also blocked.
``` c
#include <stdio.h>
#include <threads.h>
mtx_t mutex;
int thread_foo(void *ptr) {
  int result;
  FILE *fp;
  if ((result = mtx_lock(&mutex)) != thrd_success) {
    /* Handle error */
  }
  fp = fopen("SomeNetworkFile", "r");
  if (fp != NULL) {
    /* Work with the file */
    fclose(fp);
  }
  if ((result = mtx_unlock(&mutex)) != thrd_success) {
    /* Handle error */
  }
  return 0;
}
int main(void) {
  thrd_t thread;
  int result;
  if ((result = mtx_init(&mutex, mtx_plain)) != thrd_success) {
    /* Handle error */
  }
  if (thrd_create(&thread, thread_foo, NULL) != thrd_success) {
    /* Handle error */
  }
  /* ... */
  if (thrd_join(thread, NULL) != thrd_success) {
    /* Handle error */
  }
  mtx_destroy(&mutex);
  return 0;
}
```
## Compliant Solution (Block while Not Locked)
This compliant solution performs the file operations when the lock has not been acquired. The blocking behavior consequently affects only the thread that called the blocking function.
``` c
#include <stdio.h>
#include <threads.h>
mtx_t mutex;
int thread_foo(void *ptr) {
  int result;
  FILE *fp = fopen("SomeNetworkFile", "r");
  if (fp != NULL) {
    /* Work with the file */
    fclose(fp);
  }
  if ((result = mtx_lock(&mutex)) != thrd_success) {
    /* Handle error */
  }
  /* ... */
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Risk Assessment
Blocking or lengthy operations performed within synchronized regions could result in a deadlocked or an unresponsive system.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON05-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | CONCURRENCY.STARVE.BLOCKING | Blocking in critical section |
| Klocwork | 2024.4 | CONC.SLEEP |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON05-a | Do not use blocking functions while holding a lock |
| Polyspace Bug Finder | R2024a | CERT C: Rec. CON05-C | Checks for blocking operation while holding lock (Rec. partially covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON05-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | LCK09-J. Do not perform operations that can block while holding a lock | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MITRE CWE | CWE-557 | Prior to 2018-01-12: |
| MITRE CWE | CWE-662 | Prior to 2018-01-12: |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152305) [](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151935)
## Comments:

|  |
| ----|
| Looking at the NCCE there is no notion of mutex being locked. Perhaps a call to mtx_lock(&mutex) before recv is called would be appropriate.;
                                        Posted by iasoule32 at Nov 08, 2012 21:53
                                     |
| Fixed, thanks.
                                        Posted by svoboda at Nov 09, 2012 10:21
                                     |
| I've changed this to be a recommendation instead of a rule because it is unenforceable in a practical sense – there are many cases where blocking operations while holding a lock is unavoidable in a portable fashion, or at all.; For instance, the C standard does not give a way to open or access file contents in a non-blocking manner.  Or blocking other threads from accessing a resource is desirable.
                                        Posted by aballman at Sep 25, 2013 10:42
                                     |

