The `tss_create()` function creates a thread-specific storage pointer identified by a key. Threads can allocate thread-specific storage and associate the storage with a key that uniquely identifies the storage by calling the `tss_set()` function. If not properly freed, this memory may be leaked. Ensure that thread-specific storage is freed.
## Noncompliant Code Example
In this noncompliant code example, each thread dynamically allocates storage in the `get_data()` function, which is then associated with the global key by the call to `tss_set()` in the `add_data()` function. This memory is subsequently leaked when the threads terminate.
``` c
#include <threads.h>
#include <stdlib.h>
/* Global key to the thread-specific storage */
tss_t key;
enum { MAX_THREADS = 3 };
int *get_data(void) {
  int *arr = (int *)malloc(2 * sizeof(int));
  if (arr == NULL) {
    return arr;  /* Report error  */
  }
  arr[0] = 10;
  arr[1] = 42;
  return arr;
}
int add_data(void) {
  int *data = get_data();
  if (data == NULL) {
    return -1;  /* Report error */
  }
  if (thrd_success != tss_set(key, (void *)data)) {
    /* Handle error */
  }
  return 0;
}
void print_data(void) {
  /* Get this thread's global data from key */
  int *data = tss_get(key);
  if (data != NULL) {
    /* Print data */
  } 
}
int function(void *dummy) {
  if (add_data() != 0) {
    return -1;  /* Report error */
  }
  print_data();
  return 0;
}
int main(void) {
  thrd_t thread_id[MAX_THREADS];
  /* Create the key before creating the threads */
  if (thrd_success != tss_create(&key, NULL)) {
    /* Handle error */
  }
  /* Create threads that would store specific storage */
  for (size_t i = 0; i < MAX_THREADS; i++) {
    if (thrd_success != thrd_create(&thread_id[i], function, NULL)) {
      /* Handle error */
    }
  }
  for (size_t i = 0; i < MAX_THREADS; i++) {
    if (thrd_success != thrd_join(thread_id[i], NULL)) {
      /* Handle error */
    }
  }
  tss_delete(key);
  return 0;
}
```
## Compliant Solution
In this compliant solution, each thread explicitly frees the thread-specific storage returned by the `tss_get()` function before terminating:
``` c
#include <threads.h>
#include <stdlib.h>
/* Global key to the thread-specific storage */
tss_t key;
int function(void *dummy) {
  if (add_data() != 0) {
    return -1;  /* Report error */
  }
  print_data();
  free(tss_get(key));
  return 0;
}
/* ... Other functions are unchanged */
```
## Compliant Solution
This compliant solution invokes a destructor function registered during the call to `tss_create()` to automatically free any thread-specific storage:
``` c
#include <threads.h>
#include <stdlib.h>
/* Global key to the thread-specific storage */
tss_t key;
enum { MAX_THREADS = 3 };
/* ... Other functions are unchanged */
void destructor(void *data) {
  free(data);
}
int main(void) {
  thrd_t thread_id[MAX_THREADS];
  /* Create the key before creating the threads */
  if (thrd_success != tss_create(&key, destructor)) {
    /* Handle error */
  }
  /* Create threads that would store specific storage */
  for (size_t i = 0; i < MAX_THREADS; i++) {
    if (thrd_success != thrd_create(&thread_id[i], function, NULL)) {
      /* Handle error */
    }
  }
  for (size_t i = 0; i < MAX_THREADS; i++) {
    if (thrd_success != thrd_join(thread_id[i], NULL)) {
      /* Handle error */
    }
  }
  tss_delete(key);
  return 0;
}
```
## Risk Assessment
Failing to free thread-specific objects results in memory leaks and could result in a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON30-C | Medium | Unlikely | Medium | P4 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | ALLOC.LEAK | Leak |
| Coverity | 2017.07 | ALLOC_FREE_MISMATCH | Partially implemented, correct implementation is more involved |
| Cppcheck Premium | 24.11.0 | premium-cert-con30-c |  |
| Helix QAC | 2024.4 | C1780, C1781, C1782, C1783, C1784 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON30-a | Ensure resources are freed |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON30-C | Checks for thread-specific memory leak (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON30-C).
------------------------------------------------------------------------
[](../c/Rule%2014_%20Concurrency%20_CON_) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152173)
## Comments:

|  |
| ----|
| From Geoff Clare:
The pthread_setspecific() call in the destructor() function in the CS is not needed.  The system automatically sets the value to NULL on thread exit if there is a destructor function associated with the key; there is no need to do it explicitly.
The statement "free(NULL) which most compilers might ignore" is incorrect.  The standard requires free() to accept a null pointer (and take no action).
Also the malloc.h includes should be stdlib.h.
                                        Posted by rcs at Mar 22, 2010 11:23
                                     |
| One more thing.; For the first compliant solution, should I add the following line: int function(void *dummy) {  if (add_data() != 0) {    return -1;  /* Report error */  }  print_data();  free(tss_get(key));  (void) tss_set(key, NULL)  return 0;}Geoff Clare suggests that pthreads does this automatically from the destructor, although I don't see any such guarantees in the C Standard.
                                        Posted by rcs at Oct 21, 2013 16:01
                                     |
| The standard is vague on tss destruction, but I would guess that it is harmless, but not helpful, to do that.;Once you call tss_delete(), calls to tss_get() for that key would return 0 in a sane implementation.
                                        Posted by aballman at Oct 21, 2013 16:28
                                     |
| OK, maybe I'll just omit it.
                                        Posted by rcs at Oct 22, 2013 11:10
                                     |
| At first glance, I thought this rule was about the tss_delete function (e.g. ensure you call tss_delete), but that isn't the case.; Rather, the gist of it seems to be, if you associate dynamically allocated memory with a thread-specific-storage pointer, make sure you free it.  I feel like this scenario is an instantiation of MEM31-C. Free dynamically allocated memory when no longer needed, and may not require a seperate rule.
                                        Posted by wsnavely at Dec 02, 2013 11:18
                                     |
| sorry for only commenting... (I don't have edit privilege now)the URL of Defect Report #416 should be;http://www.open-std.org/JTC1/SC22/WG14/www/docs/summary.htm#dr_416 
                                        Posted by yozo at Jun 05, 2015 08:27
                                     |
| I've corrected the link, thank you for pointing it out!
                                        Posted by aballman at Jun 05, 2015 09:15
                                     |
| Is there a reason that the second compliant example needs to write its own destructor function? Why can't it just do tss_create(&key, free)?
                                        Posted by jcsible at Jun 24, 2021 12:43
                                     |
| For that particular code example, yes, you could simply pass;free  to tss_create()  rather than creating a distinct destructor function. The destructor function is useful if it needs to do anything more than a simple free, though.
                                        Posted by svoboda at Jun 24, 2021 13:49
                                     |

