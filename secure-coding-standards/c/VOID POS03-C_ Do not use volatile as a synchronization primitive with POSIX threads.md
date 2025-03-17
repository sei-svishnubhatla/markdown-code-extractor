It is a misconception that the `volatile` qualifier provides the following desired properties necessary for a multithreaded program:
-   **Atomicity:** Indivisible memory operations.
-   **Visibility:** The effects of a write action by a thread are visible by other threads.
-   **Ordering:** Sequences of memory operations by a thread are guaranteed to be seen in the same order by other threads.
Unfortunately, the `volatile` qualifier does not provide guarantees for any of these properties, neither by definition nor by the way it is implemented in various platforms. For more information on how volatile is implemented, consult [DCL17-C. Beware of miscompiled volatile-qualified variables](DCL17-C_%20Beware%20of%20miscompiled%20volatile-qualified%20variables).
This recommendation is a specific instance of CON02-C. Do not use volatile as a synchronization primitive in the context of POSIX threads.
The C Standard, section 5.1.2.3, paragraph 2 \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\], says
> Accessing a volatile object, modifying an object, modifying a file, or calling a function that does any of those operations are all side effects, which are changes in the state of the execution environment. Evaluation of an expression may produce side effects. At certain specified points in the execution sequence called sequence points, all side effects of previous evaluations shall be complete, and no side effects of subsequent evaluations shall have taken place.

In a nutshell, all this keyword does is inform the compiler that this variable may change in ways that cannot be determined; therefore, the compiler should not perform optimizations in memory areas marked as volatile. In other words, the compiler should not store the value in a register and use the register instead of doing expensive memory accesses. This concept is closely related to multithreading because if a shared variable is cached, a thread may change it, and the other threads may read stale data.
This property of the `volatile` keyword is sometimes misunderstood to provide atomicity of a variable that is shared between threads in a multithreaded program. A variable declared as `volatile` is not cached in a register, leading to this confusion that it can be used safely as a synchronization primitive. When a variable is declared `volatile`, the compiler does not reorder the sequence of reads and writes to that memory location. However, the compiler might reorder these reads and writes with those to other memory locations. This might result in nonatomic operations on the synchronization variable, causing errors.
## Noncompliant Code Example
This noncompliant code example uses `flag` as a synchronization primitive.
``` c
bool flag = false;
void test() {
  while (!flag) {
    sleep(1000);
  }
}
void wakeup(){
  flag = true;
}
void debit(unsigned int amount){
  test();
  account_balance -= amount;
}
```
In this example, the value of `flag` is used to determine whether the critical section can be executed. Because the `flag` variable is not declared `volatile`, it may be cached in registers. Before the value in the register is written to memory, another thread might be scheduled to run, resulting in that thread reading stale data.
## Noncompliant Code Example
This noncompliant code example uses `flag` as a synchronization primitive but qualifies flag as a `volatile` type.
``` c
volatile bool flag = false;
void test() {
  while (!flag){
    sleep(1000);
  }
}
void wakeup(){
  flag = true;
}
void debit(unsigned int amount) {
  test();
  account_balance -= amount;
}
```
Declaring `flag` volatile solves the problem of reading stale data but still does not provide atomicity guarantees needed for synchronization primitives to work correctly. The `volatile` keyword does not promise to provide the guarantees needed for synchronization primitives.
## Compliant Solution
This code uses a mutex to protect critical sections.
``` c
#include <pthread.h>
int account_balance;
pthread_mutex_t flag  = PTHREAD_MUTEX_INITIALIZER;
void debit(unsigned int amount) {
  pthread_mutex_lock(&flag);
  account_balance -= amount; /* Inside critical section */
  pthread_mutex_unlock(&flag);
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS03-C | Medium | Probable | Medium | P8 | L2 |

## Related Guidelines
[SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682): [VOID CON01-CPP. Do not use volatile as a synchronization primitive](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+CON01-CPP.+Do+not+use+volatile+as+a+synchronization+primitive)
[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011) Section 5.1.2.3, "Program execution"
## Sources
\[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] Section 4.11, "Memory synchronization"
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/POS02-C.+Follow+the+principle+of+least+privilege?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1336) [](https://www.securecoding.cert.org/confluence/display/seccode/POS04-C.+Avoid+using+PTHREAD_MUTEX_NORMAL+type+mutex+locks?showChildren=false&showComments=false)
