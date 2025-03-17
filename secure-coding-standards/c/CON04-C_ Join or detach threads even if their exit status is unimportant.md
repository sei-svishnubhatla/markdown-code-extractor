The` thrd_detach()` function is used to tell the underlying system that resources allocated to a particular thread can be reclaimed once it terminates. This function should be used when a thread's exit status is not required by other threads (and no other thread needs to use `thrd_join()` to wait for it to complete).
Whenever a thread terminates without detaching, the thread's stack is deallocated, but some other resources, including the thread ID and exit status, are left until it is destroyed by either `thrd_join()` or `thrd_detach()`. These resources can be vital for systems with limited resources and can lead to various "resource unavailable" errors, depending on which critical resource gets used up first. For example, if the system has a limit (either per-process or system wide) on the number of thread IDs it can keep track of, failure to release the thread ID of a terminated thread may lead to `thrd_create() being unable to` create another thread.
## Noncompliant Code Example
This noncompliant code example shows a pool of threads that are not exited correctly:
``` c
#include <stdio.h>
#include <threads.h>
const size_t thread_no = 5;
const char mess[] = "This is a test";
int message_print(void *ptr){
  const char *msg = (const char *) ptr;
  printf("THREAD: This is the Message %s\n", msg);
  return 0;
}
int main(void){
  /* Create a pool of threads */
  thrd_t thr[thread_no];
  for (size_t i = 0; i < thread_no; ++i) {
    if (thrd_create(&(thr[i]), message_print,
                    (void *)mess) != thrd_success) {
      fprintf(stderr, "Creation of thread %zu failed\n", i);
      /* Handle error */
    }
  }
  printf("MAIN: Thread Message: %s\n", mess);
  return 0;
}
```
## Compliant Solution
In this compliant solution, the `message_print()` function is replaced by a similar function that correctly detaches the threads so that the associated resources can be reclaimed on exit:
``` c
#include <stdio.h>
#include <threads.h>
const size_t thread_no = 5;
const char mess[] = "This is a test";
int message_print(void *ptr){
  const char *msg = (const char *)ptr;
  printf("THREAD: This is the Message %s\n", msg);
  /* Detach the thread, check the return code for errors */
  if (thrd_detach(thrd_current()) != thrd_success) {
    /* Handle error */
  }
  return 0;
}
int main(void) {
  /* Create a pool of threads */
  thrd_t thr[thread_no];
  for(size_t i = 0; i < thread_no; ++i) {
    if (thrd_create(&(thr[i]), message_print,
                    (void *)mess) != thrd_success) {
      fprintf(stderr, "Creation of thread %zu failed\n", i);
      /* Handle error */
    }
  }
  printf("MAIN: Thread Message: %s\n", mess);
  return 0;
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON04-C | Low | Unlikely | High | P1 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON04-C).
## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, pthread_detach |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152314) [](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151981)
## Comments:

|  |
| ----|
| The severity is wrong. I'm guessing the problem with not calling detach is essentially resource exhaustion aka denial-of-service, right?
The material in the Risk Assessment should be repeated earlier in the rule, either in the intro or in the NCCE, as it proves that this is a security issue and not just "good programming style".
                                        Posted by svoboda at Nov 05, 2009 16:48
                                     |
| Don't declare two variables on the same line (violates a recommendation).
Your loop counter i should be declared as size_t and not as a signed type.
You should declare THREAD_NO in both the nce and cs, preferably as an enum.
I don't care if you have the includes or not, but it should be the same for each example.
The cs and nce should be exactly the same, except for the specific problem that you are addressing.
                                        Posted by rcs_mgr at Nov 05, 2009 18:19
                                     |
| 
all other resources, including the heap and OS-level objects are left until it is destroyed by either pthread_join() or pthread_detach()
Are there really any implementations where additional resources other than the thread ID and exit status are retained when a joinable thread exits?  Those are the only things needed by pthread_join().  The reference to the heap is definitely wrong: memory allocated on the heap by a thread before it exits could subsequently be used by another thread.  Therefore memory allocated on the heap by a detached thread cannot be deallocated when it exits.  (Unless the reference is intended to be only about memory allocated on the heap internally by the implementation - e.g. the thread ID could be on the heap.  In which case it should say so.) My advice would be to reword the discussion to be primarily about the thread ID.  The resource that matters is the maximum number of threads per process.
Also the discussion should cover the use of pthread_attr_setdetachstate() with PTHREAD_CREATE_DETACHED to create threads in the detached state.  (I would have thought this is the more usual way to do it, rather than having the thread detach itself in its start function as done in the compliant solution.)
                                        Posted by geoffclare at Nov 09, 2009 07:23
                                     |
| If this is unenforceable, shouldn't it be a rec instead of a rule?
                                        Posted by svoboda at Nov 09, 2009 17:27
                                     |
| I switched it to being a recommendation instead of a rule for just this reason.
                                        Posted by aballman at Sep 24, 2013 19:51
                                     |
| I have made some changes to address the first part of my previous comment, and to remove left-over POSIX specifics.; I also tidied up a few minor things at the same time.One left-over POSIX item that I did not change is the reference to POSIX/SUS and pthread_detach() in the Bibliography. These need to be changed to appropriate C11 references.
                                        Posted by geoffclare at Oct 30, 2013 07:59
                                     |

