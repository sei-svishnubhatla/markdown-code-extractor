Pthread mutual exclusion (mutex) locks are used to avoid simultaneous usage of common resources. Several types of mutex locks are defined by pthreads: `NORMAL`, `ERRORCHECK`, `RECURSIVE`, and `DEFAULT`.
POSIX describes `PTHREAD_MUTEX_NORMAL` locks as having the following undefined behavior \[[Open Group 2004](https://www.securecoding.cert.org/confluence/display/seccode/AA.+C+References#AA.CReferences-OpenGroup04)\]:
> This type of mutex does not provide deadlock detection. A thread attempting to relock this mutex without first unlocking it shall deadlock. An error is not returned to the caller. Attempting to unlock a mutex locked by a different thread results in undefined behavior. Attempting to unlock an unlocked mutex results in undefined behavior.

The `DEFAULT` mutex pthread is also generally mapped to `PTHREAD_MUTEX_NORMAL` but is known to vary from platform to platform \[[SOL 2010](http://docs.sun.com/app/docs/doc/816-5137/sync-28983?a=view)\]. Consequently, `NORMAL` locks should not be used, and `ERRORCHECK` or `RECURSIVE` locks should be defined explicitly when mutex locks are used.
## Noncompliant Code Example
This noncompliant code example shows a simple mutex being created using `PTHREAD_MUTEX_NORMAL`. Note that the caller does not expect a return code when `NORMAL` mutex locks are used.
``` c
pthread_mutexattr_t attr;
pthread_mutex_t mutex;
size_t const shared_var = 0;
int main(void) {
  int result;
  if ((result = pthread_mutexattr_init(&attr)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_NORMAL)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_init(&mutex, &attr)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle Error */
  }
  /* Critical Region*/
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle Error */
  }
  return 0;
}
```
## Compliant Solution
This compliant solution shows an `ERRORCHECK` mutex lock being created so that return codes will be available during locking and unlocking:
``` c
pthread_mutexattr_t attr;
pthread_mutex_t mutex;
size_t const shared_var = 0;
int main(void) {
  int result;
  if ((result = pthread_mutexattr_init(&attr)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutexattr_settype(&attr, PTHREAD_MUTEX_ERRORCHECK)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_init(&mutex, &attr)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle Error */
  }
  /* Critical Region*/
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle Error */
  }
  return 0;
}
```
## Risk Assessment
Using `NORMAL` mutex locks can lead to deadlocks or abnormal program termination.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS04-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| PC-lint Plus | 1.4 | 586 | Fully supported |

## Bibliography

|  |
| ----|
| [Open Group 2004] |
| [SOL 2010] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152194)[](../c/Rec_%2050_%20POSIX%20_POS_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152316)
## Comments:

|  |
| ----|
| Much better rule. Comments:
Our style (instead of /* Check Eror Code */) has always been:
  if (cc != ) {
    /* Handle Error */
  }

-   Your current code is well illustrative, but please change this bit for consistency with our rules.
<!-- -->
-   The Risk Assessment should have some text describing what happens when the rule is violated. I suspect the severity isn't really high, if the worst that can happen is deadlock.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 08, 2009 08:12
\| \|
This rule is now complete.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 08, 2009 17:34
\| \|
Recommending that secure programs use error checking (or recursive) mutexes seems reasonable (even though it means they will suffer a performance penalty). However, I disagree with the use of the word "likely" in the risk assessment. The situations in which using normal mutexes results in undefined behaviour are all caused by programming errors. In a well written program (which secure programs ought to be), such situations are therefore not "likely".
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Nov 09, 2009 05:45
\| \|
Changed liklihood to 'unlikely'.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 09, 2009 17:23
\| \|
Would the NCE even compile, given the "{{}}" sequence?
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Dec 14, 2012 14:14
\| \|
No. I've fixed the code, it at least;**compiles** now ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 14, 2012 14:30
\| \|
I wonder if this rule has an analog using C11 threads.
C11 mutexes support recursive vs. non-recursive locks, and recursive locks seem to offer the same tradeoff in C11 that they do in POSIX...for a small performance cost, they let one thread re-acquire a mutex.
OTOH C11 has no analogue for 'error-checking mutexes'.
So is this rule more useful for requiring recursive mutexes, or is it more for requiring mutexes with error-checking?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 26, 2013 16:01
\| \|
I was using the compliant solution as an example for initializing a mutex, but \`pthread_mutex_init\` was failing and returning "Operation not supported". When I called pthread_mutexattr_init() on the pthread_mutexattr_t before calling pthread_mutexattr_settype(), I was able to initialize the mutex successfully.
![](images/icons/contenttypes/comment_16.png) Posted by aschettenhelm at Jan 25, 2019 14:16
\| \|
I amended both code examples to use pthread_mutexattr_init(), because working with uninitialized attributes violates [EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 28, 2019 13:12
\| \|
Recursive mutexes are not safe to use with condition variables. As Posix explains in the *APPLICATION USAGE* section of the;**pthread_mutexattr_settype** docs [here](https://pubs.opengroup.org/onlinepubs/9699919799/functions/pthread_mutexattr_settype.html):
> It is advised that an application should not use a PTHREAD_MUTEX_RECURSIVE mutex with condition variables because the implicit unlock performed for a pthread_cond_timedwait() or pthread_cond_wait() may not actually release the mutex (if it had been locked multiple times). If this happens, no other thread can satisfy the condition of the predicate.

Furthermore, in my opinion, the perceived necessity to use recursive mutexes often suggests a lack of understanding on the part of the author of their locking strategy, which can lead to more problems than a deadlock that is possible (and is indicative of a bug) by using a non-recursive mutex. i.e. problems related to using recursive mutexes can be more subtle and difficult to detect than a bug that results in a deadlock condition.
Aside from the performance implications, I don't see any problem with the recommendation to use error checking mutexes though.
![](images/icons/contenttypes/comment_16.png) Posted by drafnel at Apr 06, 2020 15:01
\|
