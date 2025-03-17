When a given thread waits (`pthread_cond_wait()` or `pthread_cond_timedwait()`) on a condition variable, it can be awakened as result of a signal operation (`pthread_cond_signal()`). However, if multiple threads are waiting on the same condition variable, any of those threads can be picked up by the scheduler to be awakened (assuming that all threads have the same priority level and also that they have only one mutex associated with the condition variable). See [POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable](POS53-C_%20Do%20not%20use%20more%20than%20one%20mutex%20for%20concurrent%20waiting%20operations%20on%20a%20condition%20variable).
The user is forced to create a predicate-testing loop around the wait condition to guarantee that each thread executes only if its predicate test is true (recommendation in IEEE Std 1003.1 since 2001 release \[[IEEE Std 1003.1-2004](https://www.securecoding.cert.org/confluence/pages/editpage.action?pageId=414)\]). As a consequence, if a given thread finds the predicate test to be false, it waits again, eventually resulting in a deadlock situation.
Consequently, the use of `pthread_cond_signal()` is safe only if the following conditions are met:
-   The condition variable is the same for each waiting thread.
-   All threads must perform the same set of operations after waking up, which means that any thread can be selected to wake up and resume for a single invocation of `pthread_cond_signal()`.
-   Only one thread is required to wake upon receiving the signal.
The use of `pthread_cond_signal()` can also be safe in the following situation:
-   Each thread uses a unique condition variable.
-   Each condition variable is associated with the same mutex (lock).
The use of `pthread_cond_broadcast()` solves the problem since it wakes up all the threads associated with the respective condition variable, and since all (must) re-evaluate the predicate condition, one should find its test to be true, avoiding the deadlock situation.
This rule is a specific instance of CON38-C. Notify all threads waiting on a condition variable instead of a single thread using POSIX threads.
## Noncompliant Code Example (`pthread_cond_signal()`)
The following noncompliant code example consists of a given number of threads (5) that should execute one after another according to the step level that is assigned to them when they are created (serialized processing). The `current_step` variable holds the current step level and is incremented as soon as the respective thread finishes its processing. Finally, another thread is signaled so that the next step can be executed.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#define NTHREADS  5
pthread_mutex_t mutex;
pthread_cond_t cond;
void *run_step(void *t) {
  static int current_step = 0;
  int my_step = (int)t;
  int result;
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle error condition */
  }
  printf("Thread %d has the lock\n", my_step);
  while (current_step != my_step) {
    printf("Thread %d is sleeping...\n", my_step);
    if ((result = pthread_cond_wait(&cond, &mutex)) != 0) {
      /* Handle error condition */
    }
    printf("Thread %d woke up\n", my_step);
  }
  /* Do processing... */
  printf("Thread %d is processing...\n", my_step);
  current_step++;
  /* Signal a waiting task */
  if ((result = pthread_cond_signal(&cond)) != 0) {
    /* Handle error condition */
  }
  printf("Thread %d is exiting...\n", my_step);
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle error condition */
  }
  pthread_exit(NULL);
}
int main(int argc, char** argv) {
  int i;
  int result;
  pthread_attr_t attr;
  pthread_t threads[NTHREADS];
  int step[NTHREADS];
  if ((result = pthread_mutex_init(&mutex, NULL)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_cond_init(&cond, NULL)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_attr_init(&attr)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE)) != 0) {
    /* Handle error condition */
  }
  /* Create threads */
  for (i = 0; i < NTHREADS; i++) {
    step[i] = i;
    if ((result = pthread_create(&threads[i], &attr, run_step, (void *)step[i])) != 0) {
      /* Handle error condition */
    }
  }
  /* Wait for all threads to complete */
  for (i = NTHREADS-1; i >= 0; i--) {
    if ((result = pthread_join(threads[i], NULL)) != 0) {
      /* Handle error condition */
    }
  }
  if ((result = pthread_mutex_destroy(&mutex)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_cond_destroy(&cond)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_attr_destroy(&attr)) != 0) {
    /* Handle error condition */
  }
  pthread_exit(NULL);
}
```
In this example, each thread has its own predicate because each requires `current_step` to have a different value before proceeding. Upon the signal operation (`pthread_cond_signal()`), any of the waiting threads can wake up. If, by chance, it is not the thread with the next step value, that thread will wait again (`pthread_cond_wait()`), resulting in a deadlock situation because no more signal operations will occur.
Consider the following example:

| Time | Thread #
(my_step) | current_step | Action |
| ----|----|----|----|
| 0 | 3 | 0 | Thread 3 executes first time: predicate is FALSE -> wait() |
| 1 | 2 | 0 | Thread 2 executes first time: predicate is FALSE -> wait() |
| 2 | 4 | 0 | Thread 4 executes;first time: predicate is FALSE -> wait() |
| 3 | 0 | 0 | Thread 0 executes first time: predicate is TRUE -> current_step++; signal() |
| 4 | 1 | 1 | Thread 1 executes first time: predicate is TRUE -> current_step++; signal() |
| 5 | 3 | 2 | Thread 3 wakes up (scheduler choice): predicate is FALSE -> wait() |
| 6 | — | — | Deadlock situation! No more threads to run, and a signal is needed to wake up the others. |

This noncompliant code example violates the [liveness](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.%20Definitions#liveness) property.
## Compliant Solution (Using `pthread_cond_broadcast()`)
This compliant solution uses the `pthread_cond_broadcast()` method to signal all waiting threads instead of a single random one. Only the `run_step()` thread code from the noncompliant code example is modified, as follows:
``` c
void *run_step(void *t) {
  static int current_step = 0;
  int my_step = (int)t;
  int result;
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle error condition */
  }
  printf("Thread %d has the lock\n", my_step);
  while (current_step != my_step) {
    printf("Thread %d is sleeping...\n", my_step);
    if ((result = pthread_cond_wait(&cond, &mutex)) != 0) {
      /* Handle error condition */
    }
    printf("Thread %d woke up\n", my_step);
  }
  /* Do processing... */
  printf("Thread %d is processing...\n", my_step);
  current_step++;
  /* Signal ALL waiting tasks */
  if ((result = pthread_cond_broadcast(&cond)) != 0) {
    /* Handle error condition */
  }
  printf("Thread %d is exiting...\n", my_step);
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle error condition */
  }
  pthread_exit(NULL);
}
```
The fact that all threads will be awake solves the problem because each one ends up executing itspredicate test; therefore, one will find it to be true and continue the execution until the end.
## Compliant Solution (Using `pthread_cond_signal()` but with a Unique Condition Variable per Thread)
Another way to solve the signal issue is to use a unique condition variable for each thread (maintaining a single mutex associated with it). In this case, the signal operation (`pthread_cond_signal()`) will wake up the only thread waiting on it. 
NOTE: The predicate of the signaled thread must be true; otherwise, a deadlock can occur anyway.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#define NTHREADS  5
pthread_mutex_t mutex;
pthread_cond_t cond[NTHREADS];
void *run_step(void *t) {
  static int current_step = 0;
  int my_step = (int)t;
  int result;
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle error condition */
  }
  printf("Thread %d has the lock\n", my_step);
  while (current_step != my_step) {
    printf("Thread %d is sleeping...\n", my_step);
    if ((result = pthread_cond_wait(&cond[my_step], &mutex)) != 0) {
      /* Handle error condition */
    }
    printf("Thread %d woke up\n", my_step);
  }
  /* Do processing... */
  printf("Thread %d is processing...\n", my_step);
  current_step++;
  /* Signal next step thread */
  if ((my_step + 1) < NTHREADS) {
    if ((result = pthread_cond_signal(&cond[my_step+1])) != 0) {
      /* Handle error condition */
    }
  }
  printf("Thread %d is exiting...\n", my_step);
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle error condition */
  }
  pthread_exit(NULL);
}
int main(int argc, char** argv) {
  int i;
  int result;
  pthread_attr_t attr;
  pthread_t threads[NTHREADS];
  int step[NTHREADS];
  if ((result = pthread_mutex_init(&mutex, NULL)) != 0) {
    /* Handle error condition */
  }
  for (i = 0; i< NTHREADS; i++) {
    if ((result = pthread_cond_init(&cond[i], NULL)) != 0) {
      /* Handle error condition */
    }
  }
  if ((result = pthread_attr_init(&attr)) != 0) {
    /* Handle error condition */
  }
  if ((result = pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE)) != 0) {
    /* Handle error condition */
  }
  /* Create threads */
  for (i = 0; i < NTHREADS; i++) {
    step[i] = i;
    if ((result = pthread_create(&threads[i], &attr, run_step, (void *)step[i])) != 0) {
      /* Handle error condition */
    }
  }
  /* Wait for all threads to complete */
  for (i = NTHREADS-1; i >= 0; i--) {
    if ((result = pthread_join(threads[i], NULL)) != 0) {
      /* Handle error condition */
    }
  }
  if ((result = pthread_mutex_destroy(&mutex)) != 0) {
    /* Handle error condition */
  }
  for (i = 0; i < NTHREADS; i++) {
    if ((result = pthread_cond_destroy(&cond[i])) != 0) {
      /* Handle error condition */
    }
  }
  if ((result = pthread_attr_destroy(&attr)) != 0) {
    /* Handle error condition */
  }
  pthread_exit(NULL);
}
```
In this compliant code, each thread has associated a unique condition variable which is signaled when that particular thread needs to be awakened. This solution turns out to be more efficient because only the desired thread is awakened.
## Risk Assessment
Signaling a single thread instead of all waiting threads can pose a threat to the liveness property of the system.

| Guideline | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS54-C | low | unlikely | medium | P2 | L3 |

## Related Guidelines
[SEI CERT Oracle Coding Standard for Java](https://wiki.sei.cmu.edu/confluence/display/java/SEI+CERT+Oracle+Coding+Standard+for+Java): [THI04-J. Notify all waiting threads rather than a single thread](https://www.securecoding.cert.org/confluence/display/java/THI04-J.+Notify+all+waiting+threads+rather+than++a+single+thread)
## Sources
\[[Open Group](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] [pthread_cond_signal() pthread_cond_broadcast()](http://www.opengroup.org/onlinepubs/7990989775/xsh/pthread_cond_signal.html)
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/CON37-C.+Do+not+use+more+than+one+mutex+for+concurrent+waiting+operations+on+a+condition+variable?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=46498126) [](https://www.securecoding.cert.org/confluence/display/seccode/CON39-C.+Avoid+the+ABA+problem+with+lock-free+programming?showChildren=false&showComments=false)
