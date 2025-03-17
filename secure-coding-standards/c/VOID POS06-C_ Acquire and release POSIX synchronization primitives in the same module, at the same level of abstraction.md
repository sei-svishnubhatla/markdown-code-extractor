All locking and unlocking of mutexes should be performed in the same module and at the same level of abstraction. Failure to follow this recommendation can lead to some lock or unlock operations not being executed by the multithreaded program as designed, eventually resulting in deadlock, race conditions, or other security vulnerabilities, depending on the mutex type. This recommendation is a specific instance of CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction using POSIX threads.
A common consequence of improper locking would be for a mutex to be unlocked twice, via two calls to `pthread_mutex_unlock()`. If the mutex is of type `PTHREAD_MUTEX_NORMAL` or `PTHREAD_MUTEX_DEFAULT`, the result is undefined behavior. The types `PTHREAD_MUTEX_ERRORCHECK` and `PTHREAD_MUTEX_RECURSIVE` will cause the unlock operation to return errors. In the case of `PTHREAD_MUEX_RECURSIVE`, an error is returned only if the lock count is zero (making the mutex available to other threads) and a call to `pthread_mutex_unlock()` is made.
## Noncompliant Code Example
In this noncompliant code example for a simplified multithreaded banking system, imagine an account with a required minimum balance. The code would need to verify that all debit transactions are allowable. Suppose there is a call to `debit()` asking to withdraw funds that would bring `account_balance` below `MIN_BALANCE`, which would result in two calls to `pthread_mutex_unlock()`. In this example, because the mutex is defined statically, the mutex type is implementation-defined.
``` c
#include <pthread.h>
enum { MIN_BALANCE = 50 };
int account_balance;
pthread_mutex_t mp = PTHREAD_MUTEX_INITIALIZER;
int verify_balance(int amount) {
  if (account_balance - amount < MIN_BALANCE) {
    /* Handle Error Condition */
    if (pthread_mutex_unlock(&mp) != 0) {
      /* Handle Error */
    }
    return -1;
  }
  return 0;
}
void debit(int amount) {
  if (pthread_mutex_lock(&mp) != 0) {
    /* Handle Error */
  }
  if (verify_balance(amount) == -1) {
    if (pthread_mutex_unlock(&mp) != 0) {
      /* Handle Error */
    }
    return;
  }
  account_balance -= amount;
  if (pthread_mutex_unlock(&mp) != 0) {
    /* Handle Error */
  }
}
```
## Compliant Solution
This compliant solution only unlocks the mutex only in the same module and at the same level of abstraction at which it is locked. This technique ensures that the code will not attempt to unlock the mutex twice.
``` c
#include <pthread.h>
enum { MIN_BALANCE = 50 };
static int account_balance;
static pthread_mutex_t mp = PTHREAD_MUTEX_INITIALIZER;
static int verify_balance(int amount) {
  if (account_balance - amount < MIN_BALANCE)
    return -1;   /* indicate error to caller */
  return 0;
}
int debit(int amount) {
  if (pthread_mutex_lock(&mp))
    return -1;   /* indicate error to caller */
  if (verify_balance(amount)) {
    pthread_mutex_unlock(&mp);
    return -1;   /* indicate error to caller */
  }
  account_balance -= amount;
  if (pthread_mutex_unlock(&mp))
    return -1;   /* indicate error to caller */
  return 0;   /* indicate success */
}
```
## Exceptions
**POS06-EX1:** Programs that use threads that can be canceled often provide a cleanup function that gets invoked if the thread is canceled. When such threads lock mutexes, they should provide a cleanup function to unlock the mutexes if the thread gets canceled. Thus, the mutexes can be unlocked at a different level of abstraction.
``` c
void release_global_lock(void* dummy) {
  if (pthread_mutex_unlock(&global_lock) != 0) {
    /* handle error */
  }
}
/* ... */
if (pthread_mutex_lock(&global_lock) != 0) {
  /* handle error */
}
pthread_cleanup_push( release_global_lock, NULL);
/* do work with data protected by the global lock */
pthread_cleanup_pop(1); /* releases the global lock */
```
## Risk Assessment
Improper use of mutexes can result in denial-of-service attacks or the unexpected termination of a multithreaded program.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS06-C | low | probable | medium | P4 | L3 |

## Sources
\[[Open Group 2008](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup08)\] [pthread_mutex_lock()/pthread_mutex_unlock()](http://www.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_lock.html), [pthread_mutex_init()](http://www.opengroup.org/onlinepubs/9699919799/functions/pthread_mutex_init.html), [pthread_mutexattr_init()](http://www.opengroup.org/onlinepubs/9699919799/functions/pthread_mutexattr_init.html)
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/CON00-C.+Avoid+race+conditions+with+multiple+threads?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=46498126) [](https://www.securecoding.cert.org/confluence/display/seccode/POS30-C.+Use+the+readlink%28%29+function+properly)
