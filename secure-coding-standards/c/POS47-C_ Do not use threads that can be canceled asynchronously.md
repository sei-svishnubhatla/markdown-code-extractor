In threading, pthreads can optionally be set to cancel immediately or defer until a specific cancellation point. Canceling asynchronously (immediately) is dangerous, however, because most threads are in fact not safe to cancel immediately.
The [IEEE standards page](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04) states that
> only functions that are cancel-safe may be called from a thread that is asynchronously cancelable.

Canceling asynchronously would follow the same route as passing a signal into the thread to kill it, posing problems similar to those in [CON37-C. Do not call signal() in a multithreaded program](CON37-C_%20Do%20not%20call%20signal__%20in%20a%20multithreaded%20program), which is strongly related to [SIG02-C. Avoid using signals to implement normal functionality](SIG02-C_%20Avoid%20using%20signals%20to%20implement%20normal%20functionality). POS44-C and SIG02-C expand on the dangers of canceling a thread suddenly, which can create a [data race condition](BB.-Definitions_87152273.html#BB.Definitions-datarace).
## Noncompliant Code Example
In this noncompliant code example, the worker thread is doing something as simple as swapping `a` and `b` repeatedly.
This code uses one lock. The `global_lock` mutex ensures that the worker thread and main thread do not collide in accessing the `a` and `b` variables.
The worker thread repeatedly exchanges the values of `a` and `b` until it is canceled by the main thread. The main thread then prints out the current values of `a` and `b`. Ideally, one should be 5, and the other should be 10.
``` c
volatile int a = 5;
volatile int b = 10;
/* Lock to enable threads to access a and b safely */
pthread_mutex_t global_lock = PTHREAD_MUTEX_INITIALIZER;
void* worker_thread(void* dummy) {
  int i;
  int c;
  int result;
  if ((result = pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS,&i)) != 0) {
    /* handle error */
  }
  while (1) {
    if ((result = pthread_mutex_lock(&global_lock)) != 0) {
      /* handle error */
    }
    c = b;
    b = a;
    a = c;
    if ((result = pthread_mutex_unlock(&global_lock)) != 0) {
      /* handle error */
    }
  }
  return NULL;
}
int main(void) {
  int result;
  pthread_t worker;
  if ((result = pthread_create( &worker, NULL, worker_thread, NULL)) != 0) {
    /* handle error */
  }
  /* .. Do stuff...meanwhile worker thread runs for some time */
  /* since we don't know when the character is read in, the program could continue at any time */
  if ((result = pthread_cancel(worker)) != 0) {
    /* handle error */
  }
  /* pthread_join waits for the thread to finish up before continuing */
  if ((result = pthread_join(worker, 0)) != 0) {
    /* handle error */
  }
  if ((result = pthread_mutex_lock(&global_lock)) != 0) {
    /* handle error */
  }
  printf("a: %i | b: %i", a, b);
  if ((result = pthread_mutex_unlock(&global_lock)) != 0) {
    /* handle error */
  }
  return 0;
}
```
![](plugins/servlet/confluence/placeholder/unknown-macro)
However, this program is subject to a race condition because an asynchronous cancel can happen at any time. If the worker thread is canceled while the `global_lock` mutex is held, it is never actually released. In this case, the main thread will wait forever trying to acquire the `global_lock`, and the program will deadlock.
It is also possible that the main thread cancels the worker thread before it has invoked `pthread_setcanceltype()`. If this happens, the cancellation will be delayed until the worker thread calls `pthread_setcanceltype()`.
## Noncompliant Code Example
In this example, the worker thread arranges to release the `global_lock` mutex if it gets interrupted:
``` c
void release_global_lock(void* dummy) {
  int result;
  if ((result = pthread_mutex_unlock(&global_lock)) != 0) {
    /* handle error */
  }
}
void* worker_thread(void* dummy) {
  int i;
  int c;
  int result;
  if ((result = pthread_setcanceltype(PTHREAD_CANCEL_ASYNCHRONOUS,&i)) != 0) {
    /* handle error */
  }
  while (1) {
    if ((result = pthread_mutex_lock(&global_lock)) != 0) {
      /* handle error */
    }
    pthread_cleanup_push( release_global_lock, NULL);
    c = b;
    b = a;
    a = c;
    pthread_cleanup_pop(1);
  }
  return NULL;
}
```
The global variables are still subject to a race condition because an asynchronous cancel can happen at any time. For instance, the worker thread could be canceled just before the last line (`a = c`) and thereby lose the old value of `b`. Consequently, the main thread might print that `a` and `b` have the same value.
The program is still subject to the race condition where the main thread cancels the worker thread before it has invoked `pthread_setcanceltype()`. If this happens, the cancelation will be delayed until the worker thread calls `pthread_setcanceltype()`.
Furthermore, though less likely, the program can still deadlock if the worker thread gets canceled after the `global_lock` is acquired but before `pthread_cleanup_push()` is invoked. In this case, the worker thread is canceled while holding `global_lock`, and the program will deadlock.
## Compliant Solution
From [IEEE standards page](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04):
> The cancelability state and type of any newly created threads, including the thread in which main() was first invoked, shall be PTHREAD_CANCEL_ENABLE and PTHREAD_CANCEL_DEFERRED respectively.

Because the default condition for POSIX, according to the IEEE standards, is `PTHREAD_CANCEL_DEFERRED`, it is not necessary to invoke `pthread_setcanceltype()` in the compliant solution:
``` c
void* worker_thread(void* dummy) {
  int c;
  int result;
  while (1) {
    if ((result = pthread_mutex_lock(&global_lock)) != 0) {
      /* handle error */
    }
    c = b;
    b = a;
    a = c;
    if ((result = pthread_mutex_unlock(&global_lock)) != 0) {
      /* handle error */
    }
    /* now we're safe to cancel, creating cancel point */
    pthread_testcancel();
  }
  return NULL;
}
```
Because this code limits cancellation of the worker thread to the end of the `while` loop, the worker thread can preserve the data invariant that `a != b`. Consequently, the program might print that `a` is 5 and `b` is 10 or that `a` is 10 and `b` is 5, but they will always be revealed to have different values when the worker thread is canceled.
The other race conditions that plague the noncompliant code examples are not possible here. Because the worker thread does not modify its cancel type, it cannot be canceled before being improperly initialized. And because it cannot be canceled while the `global_lock` mutex is held, there is no possibility of deadlock, and the worker thread does not need to register any cleanup handlers.
## Risk Assessment
Incorrectly using threads that asynchronously cancel may result in silent corruption, resource leaks, and, in the worst case, unpredictable interactions.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS47-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bad-macro-usebad-macro-expansion | Supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS47 |  |
| Helix QAC | 2024.4 | C5035 |  |
| Klocwork | 2024.4 | CERT.POS.THREAD.ASYNC_CANCEL |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS47-a | The function 'pthread_setcanceltype()' should not be called with 'PTHREAD_CANCEL_ASYNCHRONOUS' argument |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS47-C | Checks for asynchronously cancellable thread (rule fully covered) |
| RuleChecker | 24.04 | bad-macro-usebad-macro-expansion | Supported |

## Bibliography
### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS47-C).
### Related Guidelines
[SEI CERT Oracle Coding Standard for Java](https://wiki.sei.cmu.edu/confluence/display/java/SEI+CERT+Oracle+Coding+Standard+for+Java): [THI05-J. Do not use Thread.stop() to terminate threads](https://wiki.sei.cmu.edu/confluence/display/java/THI05-J.+Do+not+use+Thread.stop%28%29+to+terminate+threads)  
In Java, similar reasoning resulted in the deprecation of `Thread.stop()`.
## Bibliography

|  |  |
| ----|----|
| [MKS] | pthread_cancel() Man Page |
| [Open Group 2004 | Threads Overview |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152034) [](../c/Rule%2050_%20POSIX%20_POS_) [](../c/POS48-C_%20Do%20not%20unlock%20or%20destroy%20another%20POSIX%20thread's%20mutex)
## Comments:

|  |
| ----|
| Comments:
    The latter two paragraphs in the intro need work. I'm not sure what the 2nd paragraph is trying to say. The 3rd paragraph belongs in the 'Other Languages' section. Check other rules to see our convention for handling the 'Other Languages' section.
    The NCCE currently does not compile. For instance 'done' is undefined.
    'asynchronously cancel-safe' is not a recongized term   I would revise this sentence to use the term 'data race', which is in our Definitions section (use a hyperlink to cite its definition).
    The IEEE quote is good; add an appropriate reference to it in the References section
                                        Posted by svoboda at Apr 06, 2010 14:38
                                     |
| Done, though "data race" seems close but not quite there. IEEE uses 'asynchronously cancelable', would that seem to make more sense, or do the current revised sentences express the same thoughts?
                                        Posted by kaichong at Apr 07, 2010 00:21
                                     |
| Good question. We have several definitions, but I don't think any are a great fit...'data race' is the best I could find.  
I'd suggest providing a definition for 'asynchronously cancellable'...I think IEEE defines it, right?  You can just define it in POS47 itself.
                                        Posted by svoboda at Apr 07, 2010 13:46
                                     |
| The terms defined by POSIX are:
    Async-cancel safe function
    Cancellation point
I think the risk with cancellation that should be demonstrated in the NCCE is perhaps some sort of a resource leak, e.g., due to the thread allocating a resource but being canceled before having a chance to release it.
                                        Posted by martinsebor at Apr 07, 2010 22:42
                                     |
| That's a good idea...simply using malloc/free would do the job. But any such resource would introduce a lot more complexity to the code...what if the cancel occurs during malloc() or during free()?  Alternately, creating a 'lock' file, and subsequently deleting it might be a better instance, because a remaining lock file can survive the program's shutdown.  But the current NCCE/CS is a fine demonstration of the hazard, even if its consequences are less severe.
Also, the brace style of the code samples needs cleaned up (we use K&R brace style by convention).
                                        Posted by svoboda at Apr 08, 2010 16:06
                                     |
| If the cancellation occurs in a call to malloc() or free() the behavior is undefined, which is what I assume the NCCE aims to show. As it is, the behavior of the NCCE is well-defined since the child thread is simply canceled at whatever point the scheduler gains control. Since nothing in the rest of the program depends on the state of the variables manipulated by the canceled thread there are no ill effects.
Btw., it looks to me like there is a race condition in the CS between the call to pthread_cancel() and the time the child thread starts executing (but before the time it calls pthread_setcanceltype()). If the child thread is preempted/suspended before that call the parent may be able to cancel it before the child has had a chance to set its cancellation type. I.e., the CS will have the same behavior as the NCCE.
                                        Posted by martinsebor at Apr 08, 2010 23:08
                                     |
| I just noticed...the Risk Assessment needs the usual table of Severity/Probability/Remediation, etc.
Good catch wrt the race condition, Martin. There is a simple low-tech solution...have the thread ptint something when it has set its cancellation status, and instruct the user to not flush input until she sees the printout. Of course, you have to trust the user   Using a mutex is more trustworthy.
                                        Posted by svoboda at Apr 09, 2010 10:22
                                     |
| I decided to use a pthreads condition variable to signal that the canceltype flag was set. That seemed like the cleanest solution for the mentioned race condition.
Instead of demonstrating resource leak, this actually demonstrates data corruption, as the NCCE can actually result in a equaling b. Perhaps a resource leak can be demonstrated separately, but I think this is just as bad.
                                        Posted by kaichong at Apr 13, 2010 14:07
                                     |
| The code examples modify the global variables a and b without any locking.  This isn't a problem in these simple examples because there is no possibility of concurrent use of the variables (since main() only uses them before starting the other thread and after it has terminated).  However, in real code there could be other threads accessing those variables, so I think the examples should use a mutex to protect them.  (A different mutex from the one used for the condition variable.)
Adding this mutex will mean that the thread doing the swapping will hold the mutex when cancelled, which means that it needs to use pthread_cleanup_push() and pthread_cleanup_pop() to set up a cleanup handler that unlocks the mutex.
                                        Posted by geoffclare at Apr 23, 2010 04:56
                                     |
| I've addressed all the issues in the rule, including adding the global mutex and pthread_cleanup_push|pop.
                                        Posted by svoboda at Apr 23, 2010 13:06
                                     |
| Introducing a mutex to the thread function nicely demonstrates a resource leak in the NCCE, possibly even better than calling malloc() would have. Unfortunately, since, as Geoff notes, the mutex is unnecessary, it in my view only confuses things for the reader ("Why is the lock here when only one thread can access the variables?"). Finding a way to make the mutex necessary would greatly improve the example.
The changes also introduced a couple of new problems:
    Calling pthread_cleanup_pop(1) unconditionally means that the child thread may attempt to unlock global_lock twice in succession: once by directly calling pthread_mutex_unlock(), and once again if it is canceled in the short window when the mutex is unlocked by invoking the cleanup handler.
    There is no need to lock the mutex after the child thread has exited (i.e., after the call to pthread_join() in main() has returned).
                                        Posted by martinsebor at Apr 24, 2010 15:00
                                     |
| I think the simplest way to cure most of these problems would be to remove a lot of unnecessary baggage from the example code.
The reason the code was originally written with a main() function and the condition variable stuff and getc() call is so that it could be compiled and run to obtain output that demonstrates the problem.  However, for the purposes of this rule most of that is not needed.  (In fact it probably gets in the way of the point being made because it is a distraction.)  So I would suggest deleting main() and the condition variable stuff.
The double-unlock problem that Martin raises could be solved by moving the pthread_cleanup_push/pop calls inside the while loop and removing the pthread_mutex_unlock call.
                                        Posted by geoffclare at Apr 26, 2010 07:47
                                     |
| Let's see. The global lock is, in fact, unnecessary, b/c the program's design has accesses to a and b in mutually exclusive windows. Getting rid of the global_lock also eliminates the pthread_cleanup_pop() problem, and the potential double pthread_unlock() scenario (which is undefined behavior).
I think we need everything else for a working NCCE. We could choose to leave out some details, such as getc() and thread initialization, for illustration purposes, but you need those for a working NCCE. The init_lock prevents the main thread from cancelling the worker thread before it has set its cancel type.  The getc() is useful in order to let the worker thread run for an unspecified period of time.  So I've removed the getc() call (it is now visible in a hidden comment only if you Edit the page.), and adjusted the rest of the code accordingly.
                                        Posted by svoboda at Apr 26, 2010 11:28
                                     |
| We seem to have come full circle.  You added the global lock in response to my first comment.  Are you now saying you disagree with that comment?
The reason the example code doesn't need the global lock is because it is a simple contrived example.  Getting rid of main() and the condition variable stuff would make it look more like something that could occur in a larger application where the global lock would be needed.
                                        Posted by geoffclare at Apr 26, 2010 11:56
                                     |
| 
We seem to have come full circle. You added the global lock in response to my first comment. Are you now saying you disagree with that comment?
Yes. When you made the comment I assumed that we could provide an example that was both:
    illustrative of typical behavior, and
    was also a standalone program that exhibited the good & bad behavior the rule was pointing out.
    guaranteed thread-safety of functions & data.
My last edit came of my deciding that the program could not satisfy all three preferences. That is, satisfying the last two preferences made the code confusing and complex, failing the first preference.  So, I opted to focus on the 2nd preference, with a nod to the 1st.
The global lock is a good idea in general. It is not strictly necessary for the NCCE or CCE. And it can get easily distracted in how to handle the mutex cleanup.  Hence I took out the global lock, and provided comments expalining why.
I'm not sure I agree that eliminating the condition variable makes the example more 'typical'. The cond. var is necesasry to ensure that the worker thread is properly initialized. Which you will need if your thread modifies its cancellation policy.
                                        Posted by svoboda at Apr 26, 2010 15:10
                                     |
| 
The global lock is a good idea in general. It is not strictly necessary for the NCCE or CCE. And it can get easily distracted in how to handle the mutex cleanup. Hence I took out the global lock, and provided comments expalining why.
This rule is about thread cancellation.  Mutex cleanup is an important consideration in thread cancellation, so removing it reduces the example's value.
It is very unusual for threads to modify global data without locking (unless lock-free techniques are being used, but I don't think that's appropriate here).  As I said before, the only reason it is not needed in these examples is because they are simple and artificial.  If you want to keep the example complete, then how about making it start two threads (both running the same code).  Then locking would be needed and the example would be more representative of real world code.
The cond. var is necessary to ensure that the worker thread is properly initialized. Which you will need if your thread modifies its cancellation policy.
True, but only the NCCE modifies its cancellation policy.  The CS calls pthread_setcanceltype() but the call has no effect since the type requested by the call is the default.  The text before the example explains why the call is made by saying:
However, since not all compilers are necessarily guaranteed to follow standards, you should also explicitly call pthread_setcanceltype()  with PTHREAD_CANCEL_DEFERRED.
I disagree very strongly with this "advice".  If this is applied generally, it would be ridiculously hard, if not impossible, to follow.  If there are known divergences from the standard on some specific systems, then I have no problem with those being mentioned in a section giving implementation-specific details.  But a general policy of defensive programming against the possibility of systems not following the standard is simply unworkable.
Therefore I would recommend removing the pthread_setcanceltype() from the CS code.  In which case the condition variable also would not be needed there.
                                        Posted by geoffclare at Apr 27, 2010 04:32
                                     |
| I've changed the NCCE to use the global lock. And I've split the NCCE into two NCCEs; one that does no cleanup-handling (to show the deadlock that can result), and one that does cleanup handling (which reduces the possiblity of deadlock, but does not eliminate it, and illustrates the data race).  I took out the init lock from the NCCEs figuring it would be clearer to just explain the race condition textually than to prevent it.  At this point, my hope is that the compliant solution becomes compelling by being much simpler than making an async-cancellable worker thread thread-safe.  Finally, I also removed the advice about nonstandard implementations as you suggest. Anyone who knows a case where its necessary can file a bug report 
                                        Posted by svoboda at Apr 27, 2010 12:02
                                     |
| Starting to look good.  I made a few correction to various details.
                                        Posted by geoffclare at Apr 27, 2010 12:42
                                     |
| I see you eliminated the race condition where the worker thread is interrupted between pthread_cleanup_pop() and pthread_mutex_unlock(). (by having the former invoke the latter.)   I'm not convinced that the race condition is eliminated...it depends on the internal structure of pthread_cleanup_pop().  If a cancellation occurs during the exeuction of pthread_cleanup_pop(), is it possible for the global lock to be retained?  Or is it possible for the global lock to be freed twice (which is officially undefined behavior), by a double invocation of release_global_lock()?  My pthread_cleanup_pop(3) manpage isn't clear on this point.
                                        Posted by svoboda at Apr 27, 2010 13:17
                                     |
| You are right that there is no guarantee what happens if cancellation occurs during the call to pthread_cleanup_pop(). It is not an  async-cancel safe function.  But nor is pthread_mutex_lock(). So this is just another aspect of the problems caused by trying to use asynchronous cancellation. 
                                        Posted by geoffclare at Apr 28, 2010 02:50
                                     |
| Writing code that's safe to cancel asynchronously, while difficult, isn't impossible. Why completely ban it instead of just banning the unsafe practices?
                                        Posted by jcsible at Jul 07, 2020 16:58
                                     |
| Writing code that is cancel-safe is *extremely* difficult, and the pthread_testcancel() turns a difficult problem into a manageable problem.It is analogous to async-safe signal handlers, where WG14 decided the only safe things a signal handler could do was to read or write a variable of type volatile sig_atomic_t...because a signal handler could interrupt anything and find memory in an inconsistent state. It is also analogous to Java's Thread.stop() method, which was deprecated because it could stop a thread while memory was in an inconsistent state.
                                        Posted by svoboda at Jul 31, 2020 16:37
                                     |

