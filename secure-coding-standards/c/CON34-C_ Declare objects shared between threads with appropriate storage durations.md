Accessing the automatic or thread-local variables of one thread from another thread is [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) and can cause invalid memory accesses because the execution of threads can be interwoven within the constraints of the synchronization model. As a result, the referenced stack frame or thread-local variable may no longer be valid when another thread tries to access it. Shared static variables can be protected by thread synchronization mechanisms.
However, automatic (local) variables cannot be shared in the same manner because the referenced stack frame's thread would need to stop executing, or some other mechanism must be employed to ensure that the referenced stack frame is still valid. Do not access automatic or thread-local objects from a thread other than the one with which the object is associated. See [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations) for information on how to declare objects with appropriate storage durations when data is not being shared between threads.
Noncompliant Code Example (Automatic Storage Duration)
This noncompliant code example passes the address of a variable to a child thread, which prints it out. The variable has automatic storage duration. Depending on the execution order, the child thread might reference the variable after the variable's lifetime in the parent thread. This would cause the child thread to access an invalid memory location.
``` c
#include <threads.h>
#include <stdio.h>
int child_thread(void *val) {
  int *res = (int *)val;
  printf("Result: %d\n", *res);
  return 0;
}
void create_thread(thrd_t *tid) {
  int val = 1;
  if (thrd_success != thrd_create(tid, child_thread, &val)) {
    /* Handle error */
  }
}
int main(void) {
  thrd_t tid;
  create_thread(&tid);
  if (thrd_success != thrd_join(tid, NULL)) {
    /* Handle error */
  }
  return 0;
}
```
## Noncompliant Code Example (Automatic Storage Duration)
One practice is to ensure that all objects with automatic storage duration shared between threads are declared such that their lifetime extends past the lifetime of the threads. This can be accomplished using a thread synchronization mechanism, such as `thrd_join()`. In this code example, `val` is declared in `main()`, where `thrd_join()` is called. Because the parent thread waits until the child thread completes before continuing its execution, the shared objects have a lifetime at least as great as the thread. 
``` c
#include <threads.h>
#include <stdio.h>
int child_thread(void *val) {
  int *result = (int *)val;
  printf("Result: %d\n", *result);  /* Correctly prints 1 */
  return 0;
}
void create_thread(thrd_t *tid, int *val) {
  if (thrd_success != thrd_create(tid, child_thread, val)) {
    /* Handle error */
  }
}
int main(void) {
  int val = 1;
  thrd_t tid;
  create_thread(&tid, &val);
  if (thrd_success != thrd_join(tid, NULL)) {
    /* Handle error */
  }
  return 0;
}
```
However, the C Standard, 6.2.4 paragraphs 4 and 5 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\], states:
> The result of attempting to indirectly access an object with thread storage duration from a thread other than the one with which the object is associated is implementation-defined. . . .
>
> The result of attempting to indirectly access an object with automatic storage duration from a thread other than the one with which the object is associated is implementation-defined.

Therefore this example relies on [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) and is nonportable.
## Compliant Solution (Static Storage Duration)
This compliant solution stores the value in an object having static storage duration. The lifetime of this object is the entire execution of the program; consequently, it can be safely accessed by any thread.
``` c
#include <threads.h>
#include <stdio.h>
int child_thread(void *v) {
  int *result = (int *)v;
  printf("Result: %d\n", *result);  /* Correctly prints 1 */
  return 0;
}
void create_thread(thrd_t *tid) {
  static int val = 1;
  if (thrd_success != thrd_create(tid, child_thread, &val)) {
    /* Handle error */
  }
}
int main(void) {
  thrd_t tid;
  create_thread(&tid);
  if (thrd_success != thrd_join(tid, NULL)) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (Allocated Storage Duration)
This compliant solution stores the value passed to the child thread in a dynamically allocated object. Because this object will persist until explicitly freed, the child thread can safely access its value.
``` c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>
int child_thread(void *val) {
  int *result = (int *)val;
  printf("Result: %d\n", *result); /* Correctly prints 1 */
  return 0;
}
void create_thread(thrd_t *tid, int *value) {
  *value = 1;
  if (thrd_success != thrd_create(tid, child_thread,
                                  value)) {
    /* Handle error */
  }
}
int main(void) {
  thrd_t tid;
  int *value = (int *)malloc(sizeof(int));
  if (!value) {
    /* Handle error */
  }
  create_thread(&tid, value);
  if (thrd_success != thrd_join(tid, NULL)) {
    /* Handle error */
  }
  free(value);
  return 0;
}
```
## Noncompliant Code Example (Thread-Specific Storage)
In this noncompliant code example, the value is stored in thread-specific storage of the parent thread. However, because thread-specific data is available only to the thread that stores it, the `child_thread()` function will set `result` to a null value.
``` c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>
static tss_t key; 
int child_thread(void *v) {
  void *result = tss_get(*(tss_t *)v);
  printf("Result: %d\n", *(int *)result);
  return 0;
}
int create_thread(void *thrd) {
  int *val = (int *)malloc(sizeof(int));
  if (val == NULL) {
    /* Handle error */
  }
  *val = 1;
  if (thrd_success != tss_set(key, val)) {
    /* Handle error */
  }
  if (thrd_success != thrd_create((thrd_t *)thrd,
                                  child_thread, &key)) {
    /* Handle error */
  }
  return 0;
}
int main(void) {
  thrd_t parent_tid, child_tid;
  if (thrd_success != tss_create(&key, free)) {
    /* Handle error */
  }
  if (thrd_success != thrd_create(&parent_tid, create_thread,
                                  &child_tid)) {
    /* Handle error */
  }
  if (thrd_success != thrd_join(parent_tid, NULL)) {
    /* Handle error */
  }
  if (thrd_success != thrd_join(child_tid, NULL)) {
    /* Handle error */
  }
  tss_delete(key);
  return 0;
} 
```
## Compliant Solution (Thread-Specific Storage)
This compliant solution illustrates how thread-specific storage can be combined with a call to a thread synchronization mechanism, such as `thrd_join()`. Because the parent thread waits until the child thread completes before continuing its execution, the child thread is guaranteed to access a valid live object.
``` c
#include <threads.h>
#include <stdio.h>
#include <stdlib.h>
static tss_t key;
int child_thread(void *v) {
  int *result = v;
  printf("Result: %d\n", *result); /* Correctly prints 1 */
  return 0;
}
int create_thread(void *thrd) {
  int *val = (int *)malloc(sizeof(int));
  if (val == NULL) {
    /* Handle error */
  }
  *val = 1;
  if (thrd_success != tss_set(key, val)) {
    /* Handle error */
  }
  /* ... */
  void *v = tss_get(key);
  if (thrd_success != thrd_create((thrd_t *)thrd,
                                   child_thread, v)) {
    /* Handle error */
  }
  return 0;
}
int main(void) {
  thrd_t parent_tid, child_tid;
  if (thrd_success != tss_create(&key, free)) {
  /* Handle error */
  }
  if (thrd_success != thrd_create(&parent_tid, create_thread,
                                  &child_tid)) {
    /* Handle error */
  }
  if (thrd_success != thrd_join(parent_tid, NULL)) {
    /* Handle error */
  }
  if (thrd_success != thrd_join(child_tid, NULL)) {
    /* Handle error */
  }
  tss_delete(key);
return 0;
} 
```
## Compliant Solution (Thread-Local Storage, Windows, Visual Studio)
Similar to the preceding compliant solution, this compliant solution uses thread-local storage combined with thread synchronization to ensure the child thread is accessing a valid live object. It uses the Visual Studio–specific [\_\_declspec(thread)](http://msdn.microsoft.com/en-us/library/9w1sdazb.aspx) language extension to provide the thread-local storage and the [`WaitForSingleObject()`](http://msdn.microsoft.com/en-us/library/windows/desktop/ms687032(v=vs.85).aspx) API to provide the synchronization.
``` c
#include <Windows.h>
#include <stdio.h>
DWORD WINAPI child_thread(LPVOID v) {
  int *result = (int *)v;
  printf("Result: %d\n", *result);  /* Correctly prints 1 */
  return NULL;
}
int create_thread(HANDLE *tid) {
  /* Declare val as a thread-local value */
  __declspec(thread) int val = 1;
  *tid = create_thread(NULL, 0, child_thread, &val, 0, NULL);
  return *tid == NULL;
}
int main(void) {
  HANDLE tid;
  if (create_thread(&tid)) {
    /* Handle error */
  }
  if (WAIT_OBJECT_0 != WaitForSingleObject(tid, INFINITE)) {
    /* Handle error */
  }
  CloseHandle(tid);
  return 0;
}
```
## Noncompliant Code Example (OpenMP, parallel)
It is important to note that local data can be used securely with threads when using other thread interfaces, so the programmer need not always copy data into nonlocal memory when sharing data with threads. For example, the `shared` keyword in *[The OpenMP® API Specification for Parallel Programming](http://openmp.org/wp/)* \[[OpenMP](http://openmp.org/wp/)\] can be used in combination with OpenMP's threading interface to share local memory without having to worry about whether local automatic variables remain valid.
In this noncompliant code example, a variable `j` is declared outside a `parallel` `#pragma` and not listed as a private variable. In OpenMP, variables outside a `parallel #pragma` are shared unless designated as `private`.
``` c
#include <omp.h>
#include <stdio.h>
int main(void) {
  int j = 0;
  #pragma omp parallel
  {
    int t = omp_get_thread_num();
    printf("Running thread - %d\n", t);
    for (int i = 0; i < 5050; i++) {
    j++; /* j not private; could be a race condition */
    }
    printf("Just ran thread - %d\n", t);
    printf("loop count %d\n", j);
  }
return 0;
}
```
## Compliant Solution (OpenMP, `parallel`, `private`)
In this compliant solution, the variable `j` is declared outside of the `parallel` `#pragma` but is explicitly labeled as `private`:
``` c
#include <omp.h>
#include <stdio.h>
int main(void) {
  int j = 0;
  #pragma omp parallel private(j)
  {
    int t = omp_get_thread_num();
    printf("Running thread - %d\n", t);
    for (int i = 0; i < 5050; i++) {
    j++;
    }
    printf("Just ran thread - %d\n", t);
    printf("loop count %d\n", j);
  }
return 0;
}
```
## Risk Assessment
Threads that reference the stack of other threads can potentially overwrite important information on the stack, such as function pointers and return addresses. The compiler may not generate warnings if the programmer allows one thread to access another thread's local variables, so a programmer may not catch a potential error at compile time. The remediation cost for this error is high because analysis tools have difficulty diagnosing problems with concurrency and race conditions. 

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON34-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, resulting undefined behavior is reported by the runtime error analysis |
| CodeSonar | 8.3p0 | CONCURRENCY.LOCALARGCONCURRENCY.C_THREAD.ISD
 | Local Variable Passed to ThreadInappropriate Storage Duration |
| Cppcheck Premium | 24.11.0 | premium-cert-con34-c |  |
| Helix QAC | 2024.4 | DF4926, DF4927, DF4928 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON34-a | Declare objects shared between POSIX threads with appropriate storage durations |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON34-C | Checks for automatic or thread local variable escaping from a C11 thread (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL30-C. Declare objects with appropriate storage durations | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.2.4, "Storage Durations of Objects" |
| [OpenMP] | The OpenMP® API Specification for Parallel Programming |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152247) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152261)
## Comments:

|  |
| ----|
| The rationale for this guideline doesn't seem completely sound:
Accessing the stack of a thread from another thread may result in invalid memory accesses because the execution of threads can be interwoven within the constraints of the synchronization model. As a result, the referenced stack frame may not be valid when the other thread tries to access it. When the programmer wants to share data between threads, the data should be copied into non-local memory.
If I understand it correctly, the text refers to problems due to data races which are independent of how memory is allocated. The problem and a solution for it are discussed in CON32-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed.
In addition, there are many common valid use cases where having multiple threads access another thread's automatic data is safe. Take the following example from Using OpenMP: Portable Shared Memory Parallel Programming, for instance. The local array a is safely shared among all threads. Such programs are becoming increasingly commonplace especially on multicore architectures that make using threads efficient even with relatively small data sets. Requiring programs to dynamically allocate memory in such cases could easily defeat the benefits of using multiple threads.
int main()
{
   int i, n = 7;
   int a[n];
   for (i = 0; i < n; i++)
      a[i] = i + 1;
   #pragma omp parallel for shared(a)
   for (i = 0; i < n; i++) {
       a[i] += i;
   }
   printf("In main program after parallel for:\n");
   for (i = 0; i < n; i++)
      printf("a[%d] = %d\n", i, a[i]);
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 04, 2010 21:50
\| \|
Thanks, I've modified the opening paragraph to more accurately describe the problem that this rule is trying to address.
For the OpenMP example, I believe that it is a good point. I will add to this page that there are many valid cases of using local automatic variables with threads, and that the programmer should not automatically copy shared data into non-local memory when using threads.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 05, 2010 02:35
\| \|
-   The title is a bit awkward...could be clearer. I like Martin's suggested title.
<!-- -->
-   As a rule, you need to enumerate all exceptions to this rule. That is, precisely when is it safe for one thread to access another thread's local variables, and when is it unsafe? Include a link to POS32-C, as it is relevant. If you can't enumerate all such exceptions, then this should be a recommendation, not a rule. Or it should be scrapped.
I suppose that to share local data while complying with POS32-C, you need a mutex, and the mutex should not be local (lest you have race conditions accessing the mutex).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 05, 2010 11:11
\| \|
I don't believe that Martin suggested a title, but I will change the title to something like this.
POS42-C. Ensure that posix threads do not share local variables.
Regarding the exceptions, I don't believe that there are any good exceptions with respect to posix threads. However, I would not be able to enumerate all the exceptions if we include other thread APIs. Because this rule/recommendation is in the posix section, should exceptions like the OpenMP example be considered valid exceptions that would change this rule into a recommendation?
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 05, 2010 14:25
\| \|
Good point. Martin's example may be good for OpenMP, but this rule is specifically limiting itself to posix threads. So any exceptions should only be within the realm of pthreads, and need not be concerned with other multithreading APIs.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 05, 2010 16:37
\| \|
On POSIX platforms OpenMP is almost always going to be implemented on top of POSIX threads, and provide ineroperability with it, under a more convenient interface that makes it easy to employ low level parallelization in previously serial programs. An equivalent effect of many OpenMP pragmas can be achieved by wrapping POSIX threads calls in higher level primitives such as those provided by Intel [Threading Building Blocks](http://www.threadingbuildingblocks.org/) or the GNU libstdc++ [Parallel Mode](http://gcc.gnu.org/onlinedocs/libstdc++/manual/parallel_mode.html).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 05, 2010 17:36
\| \|
I think I will limit the scope of this page to just include posix threads that use the posix interface for threading. Although other APIs are implemented using posix threads, I will explicitly state in this page that there are exceptions for programs that ultimately end up using a different interface for threading.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 07, 2010 02:37
\| \|
"threads can run in any order" is overstated; i'm sure they are constrained by the memory model in some ways.
You shouldn't include "/\* Incorrectly prints 0 when compiled with gcc -lpthread on linux.\*/" om the example because this is implementation specific example. You could include some more generic comments about what is wrong with the program, and then in the description say:
For example, the childThread() incorrectly prints 0 when compiled with gcc -lpthread on linux.
I don't like the phrase "val may no longer be on the stack". Instead, I think you want to talk about "an object being referred to outside of its lifetime". You should probably familiarize yourself with and reference [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations)
This statement "Because memory stored on the heap does not become freed until free is called" has similar problems.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 07, 2010 04:38
\| \|
Instead of "threads can run in any order", how about "the programmer should not make assumptions on a thread's execution order"? I've also modified the wording in this page according to your suggestions.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 08, 2010 23:11
\| \|
-   Any keywords such as OpenNMP's `shared` should be in braces like so. Also please provide a reference to the OpenMP framework, as we don't normally address it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 09, 2010 11:54
\| \|
> Regarding the exceptions, I don't believe that there are any good exceptions with respect to posix threads

An obvious exception is where the function which contains the local variable has a `pthread_join()` call for the thread that uses the variable. E.g. the problem with the NCCE could be fixed either by moving the line
``` java
int val = 1;
```
from `createThread()` into `main()` and passing its address to `createThread()`, or by moving the `pthread_join()` call from `main()` into `createThread()` (and removing the `tid` argument from `createThread()`).
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 11, 2010 05:40
\| \|
Thanks, I've applied your suggestions to this page.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 12, 2010 16:37
\| \|
That's a good point, I've added a compliant solution illustrating this exception.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 12, 2010 16:38
\| \|
I'm thinking this guideline should be more precisely stated to exclude this obvious use case. Something like "don't access an automatic variable declared allocated in one thread from a separate thread".
Consequently your new compliant solution would not be an exception, just a compliant solution.
Your compliant solution for that allocates sizeof(int) is noncompliant because it fails to check for a memory allocation failure.
I think you should label the three compliant solutions as static, automatic, and allocated storage duration.
I'm wondering if there shouldn't also be a compliant solution involving thread storage duration for C1X?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Mar 12, 2010 21:30
\| \|
For what it's worth, the usual term for non-deterministic execution order of threads or processes is interleaved. See, for example, [A.4.11 Memory Synchronization](http://www.opengroup.org/onlinepubs/9699919799/xrat/V4_xbd_chap04.html#tag_21_04_11) in POSIX. The C++ memory model also (informally) refers to an interleaved execution of threads. For instance, in a Note in `[intro.multithread]`, paragraph 14:
> \[Note: It can be shown that programs that correctly use simple locks to prevent all data races and use no other synchronization operations behave as though the executions of their constituent threads were simply interleaved, with each observed value of an object being the last value assigned in that interleaving. This is normally referred to as â€œsequential consistencyâ€?. — end note\]

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 14, 2010 14:41
\| \|
Regarding a compliant solution involving thread storage duration (the `_Thread_local` keyword) for C1X, I don't think compilers support thread storage duration yet, so I'm not sure that writing a compliant solution is a good idea.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 14, 2010 21:23
\| \|
The vast majority of today's compilers support thread-local storage as an extension such as `__thread` ([gcc](http://gcc.gnu.org/onlinedocs/gcc-3.3.1/gcc/Thread-Local.html), HP [acc](http://h21007.www2.hp.com/portal/download/files/unprot/aCxx/Online_Help/threads.htm), Sun [cc](http://docs.sun.com/source/819-3688/sun.specific.html#46507), and IBM [XLC](http://publib.boulder.ibm.com/infocenter/comphelp/v101v121/topic/com.ibm.xlcpp101.aix.doc/language_ref/thread.html)), or `__declspec(thread)` ([Visual C/C++](http://msdn.microsoft.com/en-us/library/9w1sdazb%28VS.80%29.aspx) compilers including Intel C).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 15, 2010 22:57
\| \|
> Ensure that posix threads do not share automatic variables outside of their lifetime

-   I don't like this phrasing. It took me a while to realize that "their" refers to threads rather than automatic variables. I personally prefer the old title and phrasing (although I presume there is a good reason why you changed it.) The intro suggests that the rule is still about threads referencing vars on other threads' stacks.
<!-- -->
-   The 1st NCCE has implementation details about how the program runs on linux. This info is interesting, but belongs in a separate 'Implementation Details' section.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 16, 2010 17:11
\| \|
I changed the title such that the automatic storage compliant solution would not be an exception. After adding the noncompliant thread-local example, this rule is starting to sound like the rule, [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations), so I renamed this rule, "POS42-C. Ensure that objects shared between posix threads are declared with appropriate storage durations". If this title is still awkward, I can change it to something else.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 17, 2010 00:39
\| \|
i de-awkwarded your title a bit.
I would move this sentence:
> See DCL30-C. Declare objects with appropriate storage durations for information on how to declare objects with appropriate storage durations when data is not being shared between threads.

up to the main description of the guideline and not hide it in the first NCE.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 17, 2010 09:28
\| \|
My only remaining comments are: the implementation details section should be immediately after the NCCEs. Also, which version of gcc is being used?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2010 08:33
\| \|
Thanks, I've made the changes.
![](images/icons/contenttypes/comment_16.png) Posted by mswang at Mar 18, 2010 17:26
\| \|
I take it the last 'implementation details' section can be removed, as it is after the CS's and contains no info about what happens.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2010 19:46
\| \|
;
The first NCE says "However, the order of thread execution is interleaved".  It could be that the main execution thread is at the join waiting for tihs thread to start/finish, so "interleaved" seems like too strong a term here.  I think it shoud just be something like "executed concurrently".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 29, 2013 08:35
\| \|
For the Compliant Solution (Static Storage), couldn't the variable be declared static within the scope of the function, instead of at file scope?
The storage should still persist, and it is closer to the original intent of the code.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 29, 2013 08:44
\| \|
It could be, yes. I think that would more closely match the original code as well.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 29, 2013 09:28
\| \|
;
Now I'm confused about the allocated storage solution, because it goes out of it's way to allocate the memory in main instead of from the create_thread() function like in all the other solutions.  I think all these solutions need to be consistent in thier approach.  I'll start on this next.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 30, 2013 15:00
\| \|
There is a very random paragraph in this rule that I'm not sure what to do with, and I'm thinking about removing:
It is important to note that local data can be used securely with threads when using other thread interfaces, so the programmer need not always copy data into nonlocal memory when sharing data with threads. For example, the `shared` keyword in [The OpenMP® API Specification for Parallel Programming](http://openmp.org/wp/) \[[OpenMP](http://openmp.org/wp/)\] can be used in combination with OpenMP's threading interface to share local memory without having to worry about whether local automatic variables remain valid. Furthermore, copying the shared data into dynamic memory may completely negate the performance benefits of multithreading.
I guess I could putting this code along side an OpenMP example, but we don't have one.; Comments?  Suggestions?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Oct 30, 2013 21:40
\| \|
So, are you thinking about adding something like: #include \<omp.h\>  
#include \<stdio.h\>  
int main() {  
int t, j, i;  
#pragma omp parallel private(t, i) shared(j)  
{  
t = omp_get_thread_num();  
printf("running %d\n", t);  
for (i = 0; i \< 5050; i++)
Unknown macro: { j++; /\* race! \*/ }
printf("ran %d\n", t);  
}  
printf("%i\n", j);  
return 0;  
}
Or, maybe just remove the OpenMP reference?
![](images/icons/contenttypes/comment_16.png) Posted by bluepilot at Oct 31, 2013 08:22
\| \|
John,
Please go ahead and add an example using OpenMP.; You can either create a CS for one of the existing NCEs using OpenMP, or create an NCE/CS pair.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 31, 2013 09:12
\| \|
OK, done.
![](images/icons/contenttypes/comment_16.png) Posted by bluepilot at Oct 31, 2013 11:19
\| \|
In the example that was recently changed from noncompliant to compliant, the description ends with "However, this example relies on;[implementation-defined behavior](https://www.securecoding.cert.org/confluence/display/c/BB.+Definitions#BB.Definitions-implementation-definedbehavior) and is nonportable."  I assume this was the reason the example was classed as noncompliant.
It's not obvious to me what implementation-defined behaviour the code relies on.  Please either add an explanation (and consider changing the example back to noncompliant) or remove that last sentence.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 15, 2016 04:32
\| \|
We changed this CS back to an NCCE and added a C11 citation explaining why this behavior is implementation-defined.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 19, 2016 15:10
\| \|
The compliant solution "Compliant Solution (Thread-Specific Storage)" has a note underneath stating
\> This compliant solution uses pointer-to-integer and integer-to-pointer conversions, which have implementation-defined behavior. (See;[INT36-C. Converting a pointer to integer or integer to pointer](https://wiki.sei.cmu.edu/confluence/display/c/INT36-C.+Converting+a+pointer+to+integer+or+integer+to+pointer).)
I cannot for the life of me see such a conversion. Looking at the page history it does look like there was a version which had this problem years ago but no longer (changed circa 2016). Am I missing something?
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at Jun 23, 2023 11:18
\| \|
Agreed. The code used to require the comment and lacked it. Now it does not merit the INT36-C comment, so I took it out.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 23, 2023 12:00
\|
