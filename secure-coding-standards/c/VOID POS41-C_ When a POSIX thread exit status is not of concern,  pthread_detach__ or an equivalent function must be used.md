The `pthread_detach()` function is used to tell the underlying system that resources allocated to a particular thread can be reclaimed once it terminates. This function should be used when an exit status is not required by other threads.
Whenever a thread exits without detaching, the thread's stack is deallocated, and all other resources, including the heap and OS-level objects, are left until it is destroyed by either `pthread_join()` or `pthread_detach()`. These resources can be vital for systems with limited resources and can finally lead to errors, depending on which critical resource gets used up first. One commonly occurring error is `EAGAIN` *(Resource unavailable, try again)* set by functions such as `fork()`, `pthread_create()`, or `pthread_mutex_init()` when the system lacks the necessary resources to create or initialize another process, thread, or mutex.
This rule is a specific instance of CON40-C. When a thread exit status is not of concern, thrd_detach() or an equivalent function must be used using POSIX threads.
## Noncompliant Code Example
This noncompliant code example shows a pool of threads that are not exited correctly.
``` c
size_t const thread_no = 5;
char mess[] = "This is a test";
void *message_print(void *ptr){
  char *msg;
  msg = (char *) ptr;
  printf("THREAD: This is the Message %s\n", msg);
}
int main(void){
  int error = 0;
  size_t i = 0;
  /* Create a pool of threads */
  pthread_t thr[thread_no];
  for (i = 0; i < thread_no; i++) {
    error = pthread_create( &(thr[i]), NULL, message_print, (void *) mess);
    /* Handle error */
  }
  printf("MAIN: Thread Message: %s\n", mess);
  pthread_exit(NULL);
}
```
## Compliant Solution
In this compliant solution, the `message_print()` function is replaced by a similar function that correctly detaches the threads so that the associated resources can be reclaimed on exit.
``` c
size_t const thread_no = 5;
char mess[] = "This is a test";
void *message_print(void *ptr){
  int error = 0;
  char *msg;
  /* Detach the thread */
  error = pthread_detach(pthread_self());
  /* Handle error if any */
  msg = (char *) ptr;
  printf("THREAD: This is the Message %s\n", msg);
}
int main(void) {
  int error = 0;
  size_t i = 0;
  /* Create a pool of threads */
  pthread_t thr[thread_no];
  for(i = 0; i < thread_no; i++) {
    error = pthread_create( &(thr[i]), NULL, message_print, (void *) mess);
    /* Handle error */
  }
  printf("MAIN: Thread Message: %s\n", mess);
  pthread_exit(NULL);
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS41-C | low | unlikely | high | P1 | L3 |

## Sources
\[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\]  
\[[pthread_detach](http://www.opengroup.org/onlinepubs/000095399/functions/pthread_detach.html)\]
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/POS39-C.+Use+the+correct+byte+ordering+when+transferring+data+between+systems?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1336) [](https://www.securecoding.cert.org/confluence/display/seccode/POS44-C.+Do+not+use+signals+to+terminate+threads?showChildren=false&showComments=false)
