Mutexes are used to protect shared data structures being concurrently accessed. If a mutex is destroyed while a thread is blocked waiting for that mutex, [critical sections](BB.-Definitions_87152273.html#BB.Definitions-criticalsections) and shared data are no longer protected.
The C Standard, 7.28.4.1, paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> The `mtx_destroy` function releases any resources used by the mutex pointed to by `mtx`. No threads can be blocked waiting for the mutex pointed to by `mtx`.

This statement implies that destroying a mutex while a thread is waiting on it is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
This noncompliant code example creates several threads that each invoke the `do_work()` function, passing a unique number as an ID. The `do_work()` function initializes the `lock` mutex if the argument is 0 and destroys the mutex if the argument is `max_threads - 1`. In all other cases, the `do_work()` function provides normal processing. Each thread, except the final cleanup thread, increments the atomic `completed` variable when it is finished.
Unfortunately, this code contains several race conditions, allowing the mutex to be destroyed before it is unlocked. Additionally, there is no guarantee that `lock` will be initialized before it is passed to `mtx_lock()`. Each of these behaviors is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
#include <stdatomic.h>
#include <stddef.h>
#include <threads.h>
mtx_t lock;
/* Atomic so multiple threads can modify safely */
atomic_int completed = ATOMIC_VAR_INIT(0);
enum { max_threads = 5 }; 
int do_work(void *arg) {
  int *i = (int *)arg;
  if (*i == 0) { /* Creation thread */
    if (thrd_success != mtx_init(&lock, mtx_plain)) {
      /* Handle error */
    }
    atomic_store(&completed, 1);
  } else if (*i < max_threads - 1) { /* Worker thread */
    if (thrd_success != mtx_lock(&lock)) {
      /* Handle error */
    }
    /* Access data protected by the lock */
    atomic_fetch_add(&completed, 1);
    if (thrd_success != mtx_unlock(&lock)) {
      /* Handle error */
    }
  } else { /* Destruction thread */
    mtx_destroy(&lock);
  }
  return 0;
}
int main(void) {
  thrd_t threads[max_threads];
  for (size_t i = 0; i < max_threads; i++) {
    if (thrd_success != thrd_create(&threads[i], do_work, &i)) {
      /* Handle error */
    }
  }
  for (size_t i = 0; i < max_threads; i++) {
    if (thrd_success != thrd_join(threads[i], 0)) {
      /* Handle error */
    }
  }
  return 0;
}
```
## Compliant Solution
This compliant solution eliminates the race conditions by initializing the mutex in `main()` before creating the threads and by destroying the mutex in `main()` after joining the threads:
``` c
#include <stdatomic.h>
#include <stddef.h>
#include <threads.h>
mtx_t lock;
/* Atomic so multiple threads can increment safely */
atomic_int completed = ATOMIC_VAR_INIT(0);
enum { max_threads = 5 }; 
int do_work(void *dummy) {
  if (thrd_success != mtx_lock(&lock)) {
    /* Handle error */
  }
  /* Access data protected by the lock */
  atomic_fetch_add(&completed, 1);
  if (thrd_success != mtx_unlock(&lock)) {
    /* Handle error */
  }
  return 0;
}
int main(void) {
  thrd_t threads[max_threads];
  if (thrd_success != mtx_init(&lock, mtx_plain)) {
    /* Handle error */
  }
  for (size_t i = 0; i < max_threads; i++) {
    if (thrd_success != thrd_create(&threads[i], do_work, NULL)) {
      /* Handle error */
    }
  }
  for (size_t i = 0; i < max_threads; i++) {
    if (thrd_success != thrd_join(threads[i], 0)) {
      /* Handle error */
    }
  }
  mtx_destroy(&lock);
  return 0;
}
```
## Risk Assessment
Destroying a mutex while it is locked may result in invalid control flow and data corruption.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON31-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | CONCURRENCY.LOCALARG | Local Variable Passed to Thread |
| Cppcheck Premium | 24.11.0 | premium-cert-con31-c |  |
| Helix QAC | 2024.4 | DF4961, DF4962 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON31-aCERT_C-CON31-b
CERT_C-CON31-c | Do not destroy another thread's mutexDo not use resources that have been freed
Do not free resources using invalid pointers |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON31-C | Checks for destruction of locked mutex (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-667, Improper Locking | 2017-07-10: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-667 and CON31-C/POS48-C
Intersection( CON31-C, POS48-C) = Ø
CWE-667 = Union, CON31-C, POS48-C, list) where list =
-   Locking & Unlocking issues besides unlocking another thread’s C mutex or pthread mutex.
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.28.4.1, "The mtx_destroy Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152258) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152069)
## Comments:

|  |
| ----|
| What happens if the worker thread dies while holding the mutex? This would cause the clean up thread to block forever... is there a fix for this? Should we mention it?
                                        Posted by avolkovi at Mar 04, 2008 11:26
                                     |
| This page seems to be in an inconsistent state.; It says "This solution requires the cleanup function to acquire the lock before destroying it" but then goes on to give a quote from POSIX that effectively forbids doing this ("Attempting  to destroy a locked mutex results in undefined behavior") and the code given as the solution does not lock the mutex in the cleanup function.  Instead the code assumes that pthread_mutex_lock() will return an error if the mutex has been destroyed, but this is no good either, because according to POSIX the behaviour is undefined ("A destroyed mutex object can be reinitialized using pthread_mutex_init(); the results of otherwise referencing the object after it has been destroyed are undefined.")
The proper solution is to design the application in such a way that the cleanup cannot be done while worker threads might still have the mutex locked.  For example, don't do the cleanup until all the worker threads have been joined. 
                                        Posted by geoffclare at Mar 19, 2008 13:28
                                     |
| This seems to be confused about processes and threads.; Linux doesn't help by making threads close to processes.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 03:45
                                     |
| This is correct.. the quote from POSIX kind of hoses this entire rule, as there is really no way to destroy another thread's mutex that would be problematic since pthread_mutex_destroy() acquires all necessary locks...
Looking at this now, the compliant and non-compliant solutions are actually the same
We should probably delete this rule since it is in contradiction with what POSIX says
another quote from the man page:
       pthread_mutex_destroy destroys a mutex object, freeing  the  resources
       it  might  hold. The mutex must be unlocked on entrance. In the Linux-
       Threads  implementation,  no  resources  are  associated  with   mutex
       objects,  thus  pthread_mutex_destroy  actually  does  nothing  except
       checking that the mutex is unlocked.
                                        Posted by avolkovi at Mar 25, 2008 11:16
                                     |
| I believe the issues are addressed now.
                                        Posted by dmk at Mar 31, 2008 00:45
                                     |
| There were still some things that implied an application could expect pthread_mutex_lock() to fail if the mutex has been destroyed.; The error is optional in POSIX, and on systems that don't detect it you get undefined behaviour.  There was also an incorrect statement about pthread_mutex_destroy() acquiring locks.  I have applied fixes.
The quote from POSIX before the compliant code now seems to be orphaned, but I wasn't sure what should be done with it.
                                        Posted by geoffclare at Mar 31, 2008 07:22
                                     |
| I agree.; The quote didn't seem to serve a purpose any more, so I removed it.
                                        Posted by dmk at Mar 31, 2008 09:33
                                     |
| I removed the unenforceable flag since this is enforceable via dynamic analysis.
                                        Posted by aballman at Sep 30, 2013 16:28
                                     |
| We appear to be referring to a static analysis checker in Fortify that can detect violations of this rule.; That suggests that this rule could also be checked through static analysis, or that this is a mistake.
                                        Posted by rcs at Oct 23, 2013 10:34
                                     |

