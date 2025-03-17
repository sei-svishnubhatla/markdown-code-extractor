Accessing the stack or thread-local variables of a thread from another thread can cause invalid memory accesses because the execution of threads can be interwoven within the constraints of the synchronization model. As a result, the referenced stack frame or thread-local variable may not be valid when the other thread tries to access it. Regular shared variables should be protected by thread synchronization mechanisms. However, local variables should not be shared in the same fashion because the referenced stack frame's thread would have to stop executing, or some other way must be found to ensure that the referenced stack frame is still valid. See [CON32-C. Prevent data races when accessing bit-fields from multiple threads](CON32-C_%20Prevent%20data%20races%20when%20accessing%20bit-fields%20from%20multiple%20threads) for information on how to securely share nonautomatic and non-thread-local variables. See [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations) for information on how to declare objects with appropriate storage durations when data is not being shared between threads. Note that this is a specific instance of CON34-C. Declare objects shared between threads with appropriate storage durations for POSIX threads.
It is important to note that local data can be used securely with threads when using other non-POSIX thread interfaces, so the programmer should not always copy data into nonlocal memory when sharing data with threads. For example, the `shared` keyword in [OpenMP](http://openmp.org/wp/) can be used in combination with OpenMP's threading interface to share local memory without having to worry about whether local automatic variables remain valid. Furthermore, copying the shared data into dynamic memory may completely negate the performance benefits of multithreading.
## Noncompliant Code Example (Automatic Storage)
The `createThread()` function allocates an integer on the stack and passes a void pointer, spawning off a new thread, `childThread()`. The order of thread execution is interleaved, so `val` can reference an object outside of its lifetime, causing the child thread to access an invalid memory location.
``` c
void *childThread(void *val) {
  /*
   * Depending on the order of thread execution, the object
   * referred to by val may be out of its lifetime, resulting
   * in a potentially incorrect result being printed out.
   */
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return NULL;
}
void createThread(pthread_t *tid) {
  /* Store 1 in val on the stack. */
  int val = 1;
  int result;
  if ((result = pthread_create(tid, NULL, childThread, &val)) != 0) {
    /* Handle error */
  }
}
int main(void) {
  pthread_t tid;
  int result;
  createThread(&tid);
  if ((result = pthread_join(tid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Implementation Details
The automatic storage noncompliant code example incorrectly prints 0 when compiled with GCC 4.1.2 with the `-lpthread` flag on Linux.
## Noncompliant Code Example (Thread-Local Storage)
This noncompliant code example is incorrect because `createThread()` can finish running before `childThread()`, so `childThread()` may not access a valid object:
``` c
__thread int val;
void *childThread(void *val) {
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return NULL;
}
void *createThread(void *childTid) {
  pthread_t *tid = (pthread_t *)childTid;
  int result;
  val = 1;
  if ((result = pthread_create(tid, NULL, childThread, &val)) != 0) {
    /* Handle error */
  }
  return NULL;
}
void *empty(void *arg) {
  /* Function that does nothing */
  val = 0;
  return NULL;
}
int main(void) {
  pthread_t parentTid, childTid, emptyTid;
  int result;
  /*
   * createThread() may complete before childThread(), and
   * the thread-local variable, val, belonging to createThread(),
   * may no longer be valid when childThread() runs.
   */
  if ((result = pthread_create(&parentTid, NULL, createThread, &childTid)) != 0) {
    /* Handle error */
  }
  if ((result = pthread_join(parentTid, NULL)) != 0) {
    /* Handle error */
  }
  if ((result = pthread_create(&emptyTid, NULL, empty, NULL)) != 0) {
    /* Handle error */
  }
  if ((result = pthread_join(emptyTid, NULL)) != 0) {
    /* Handle error */
  }
  if ((result = pthread_join(childTid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Implementation Details
This thread-local storage noncompliant code example incorrectly prints 0 when compiled with GCC 4.1.2 with the `-lpthread` flag on Linux.
## Compliant Solution (Allocated Storage)
Instead of passing the pointer to the stack of the parent thread, one solution is to allocate space on the heap, copying the data to dynamic memory. Because the lifetime of an object stored in dynamic memory lasts until it is freed, the child thread ensures that memory accesses are valid.
``` c
void *childThread(void *val) {
  /* Correctly prints 1 */
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  free(res);
  return NULL;
}
void createThread(pthread *tid) {
  int result;
  /* Copy data into dynamic memory */
  int *val = malloc(sizeof(int));
  if (!val) {
    /* Handle error */
  }
  *val = 1;
  if ((result = pthread_create(&id, NULL, childThread, val)) != 0) {
    /* Handle error */
  }
}
int main(void) {
  pthread_t tid;
  int result;
  createThread(&tid);
  if ((result = pthread_join(tid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (Static Storage)
Another solution is to store the data as a global static variable. Unlike local automatic variables, which are stored on the stack, static variables are stored in the data section of memory. Static variables last for the execution of the entire program, so a thread can safely access global static variables.
``` c
/* Declare val as a global static variable */
int val;
void *childThread(void *val) {
  /* Correctly prints 1 */
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return NULL;
}
void createThread(pthread_t *tid) {
  val = 1;
  int result;
  if ((result = pthread_create(tid, NULL, childThread, &val)) != 0) {
    /* Handle error */
  }
}
int main(void) {
  pthread_t tid;
  createThread(&tid);
  int result;
  if ((result = pthread_join(tid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (Automatic Storage)
Another solution is to ensure that local variables shared between threads are declared in the same or previous stack frame as a call to a thread synchronization mechanism, such as `pthread_join()`. For example, in this compliant solution, `val` is declared in `main()`, where `pthread_join()` is called. Because the parent thread will wait until the child thread completes before continuing its execution, the child thread is guaranteed to access an object that is still within its lifetime.
``` c
void *childThread(void *val) {
  /* Correctly prints 1 */
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return NULL;
}
void createThread(pthread_t *tid, int *val) {
  int result = pthread_create(tid, NULL, childThread, val);
  if (result != 0) {
    /* Handle error */
  }
}
int main(void) {
  /* Declare val in the same function as pthread_join */
  int val = 1;
  int result;
  pthread_t tid;
  createThread(&tid, &val);
  if ((result = pthread_join(tid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (Thread-Local Storage)
Another solution is to declare `val` a thread-local variable combined with a call to a thread synchronization mechanism, such as `pthread_join()`. Because the parent thread will wait until the child thread completes before continuing its execution, the child thread is guaranteed to access an object that is still within its lifetime.
``` c
/* Declare val as a thread-local value */
__thread int val;
void *childThread(void *val) {
  /* Correctly prints 1 */
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return NULL;
}
void createThread(pthread_t *tid) {
  val = 1;
  int result = pthread_create(tid, NULL, childThread, &val);
  if (result != 0) {
    /* Handle error */
  }
}
int main(void) {
  pthread_t tid;
  int result;
  createThread(&tid);
  if ((result = pthread_join(tid, NULL)) != 0) {
    /* Handle error */
  }
  return 0;
}
```
## Risk Assessment
Threads that reference the stack of other threads can potentially overwrite important information on the stack, such as function pointers and return addresses. However, it would be difficult for an attacker to exploit this code from this error alone. The compiler will not generate warnings if the programmer decides to give another thread access to one thread's local variables, so a programmer may not catch a potential error at compile time. The remediation cost for this error is high because analysis tools have difficulty diagnosing problems with concurrency and race conditions.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS50-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Helix QAC | 2024.4 | DF4926, DF4927, DF4928 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS50-a | Declare objects shared between POSIX threads with appropriate storage durations |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS50-C | Checks for automatic or thread local variable escaping from a POSIX thread (rule fully covered) |

##  Bibliography

|  |  |
| ----|----|
| [Bryant 2003] | Chapter 13, "Concurrent Programming" |
| [OpenMP] |  |

------------------------------------------------------------------------
[](../c/POS49-C_%20When%20data%20must%20be%20accessed%20by%20multiple%20threads,%20provide%20a%20mutex%20and%20guarantee%20no%20adjacent%20data%20is%20also%20accessed)[](../c/Rule%2050_%20POSIX%20_POS_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152018)
