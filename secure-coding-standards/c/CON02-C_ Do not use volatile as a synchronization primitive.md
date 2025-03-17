The C Standard, subclause 5.1.2.3, paragraph 2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], says,
> Accessing a volatile object, modifying an object, modifying a file, or calling a function that does any of those operations are all side effects, which are changes in the state of the execution environment. Evaluation of an expression in general includes both value computations and initiation of side effects. Value computation for an lvalue expression includes determining the identity of the designated object.

The `volatile` keyword informs the compiler that the qualified variable may change in ways that cannot be determined; consequently, compiler optimizations must be restricted for memory areas marked as `volatile`. For example, the compiler is forbidden to load the value into a register and subsequently reuse the loaded value rather than accessing memory directly. This concept relates to multithreading because incorrect caching of a shared variable may interfere with the propagation of modified values between threads, causing some threads to view stale data.
The `volatile` keyword is sometimes misunderstood to provide atomicity for variables that are shared between threads in a multithreaded program. Because the compiler is forbidden to either cache variables declared as `volatile` in registers or to reorder the sequence of reads and writes to any given volatile variable, many programmers mistakenly believe that volatile variables can correctly serve as synchronization primitives. Although the compiler is forbidden to reorder the sequence of reads and writes to a particular volatile variable, it may legally reorder these reads and writes with respect to reads and writes to *other* memory locations. This reordering alone is sufficient to make volatile variables unsuitable for use as synchronization primitives.
Further, the `volatile` qualifier lacks any guarantees regarding the following desired properties necessary for a multithreaded program:
-   **Atomicity:** Indivisible memory operations.
-   **Visibility:** The effects of a write action by a thread are visible to other threads.
-   **Ordering:** Sequences of memory operations by a thread are guaranteed to be seen in the same order by other threads.
The `volatile` qualifier lacks guarantees for any of these properties, both by definition and by the way it is implemented in various platforms. For more information on how `volatile` is implemented, consult [DCL17-C. Beware of miscompiled volatile-qualified variables](DCL17-C_%20Beware%20of%20miscompiled%20volatile-qualified%20variables).
## Noncompliant Code Example
This noncompliant code example attempts to use `flag` as a synchronization primitive:
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
This noncompliant code example uses `flag` as a synchronization primitive but qualifies `flag` as a `volatile` type:
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
Declaring `flag` as `volatile` solves the problem of values being cached, which causes stale data to be read. However, `volatile flag` still fails to provide the atomicity and visibility guarantees needed for synchronization primitives to work correctly. The `volatile` keyword does not promise to provide the guarantees needed for synchronization primitives.
## Compliant Solution
This code uses a mutex to protect critical sections:
``` c
#include <threads.h>
int account_balance;
mtx_t flag;
/* Initialize flag */
int debit(unsigned int amount) {
  if (mtx_lock(&flag) == thrd_error) {
    return -1;  /* Indicate error */
  }
  account_balance -= amount; /* Inside critical section */
  if (mtx_unlock(&flag) == thrd_error) {
    return -1;  /* Indicate error */
  }
  return 0;
}
```
## Compliant Solution (Critical Section, Windows)
This compliant solution uses a Microsoft Windows critical section object to make operations involving `account_balance` atomic \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682530(v=vs.85).aspx)\].
``` c
#include <Windows.h>
static volatile LONG account_balance;
CRITICAL_SECTION flag;
/* Initialize flag */
InitializeCriticalSection(&flag);
int debit(unsigned int amount) {
  EnterCriticalSection(&flag); 
  account_balance -= amount; /* Inside critical section */
  LeaveCriticalSection(&flag);
  return 0;
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON02-C | Medium | Probable | Medium | P8 | L2 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Parasoft C/C++test | 2024.2 | CERT_C-CON02-a | Do not use the volatile keyword |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | CON01-CPP. Do not use volatile as a synchronization primitive | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | Section 4.11, "Memory Synchronization" |
| [ISO/IEC 9899:2011] | Subclause 5.1.2.3, "Program Execution" |
| [MSDN] |  |

------------------------------------------------------------------------
[](../c/CON01-C_%20Acquire%20and%20release%20synchronization%20primitives%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction) [](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152305)
## Comments:

|  |
| ----|
| 
    Still needs a references section
    DCL17-C. Beware of miscompiled volatile-qualified variables is a rule that is quite pertinent to this rule, please provide a link & discuss its relation to your rule.
    The C++ version of this rule has a better introduction section, by quoting several references.and by listing the properties necessary for thread-safety, which volatile lacks.  Your introduction section should contain as much of that data is makes sense for a C rule.
                                        Posted by svoboda at Apr 03, 2009 22:25
                                     |
| In the compliant example, why is account_balance declared volatile?  I don't think that's necessary, and it confuses things because this rule is about not using volatile.
                                        Posted by geoffclare at Apr 06, 2009 04:38
                                     |
| IMHO volatile is necessary but not sufficient for safe threading code. You can take it out if you can ensure that the compiler will not optimize away accesses or modifications to account_balance. I suppose for the sample code this is true, but is it always true?
                                        Posted by svoboda at Apr 06, 2009 11:32
                                     |
| When memory accesses are protected by a mutex, POSIX guarantees that memory is synchronized between threads and therefore volatile is not needed.  See XBD 4.11 Memory Synchronization.  There are very many (probably thousands) of existing pthread applications that rely on this.  It's worth remembering that when pthreads were added to POSIX, it did not require implementations to support the C Standard (they had the option of supporting standard C or "common usage C", i.e. K&R), so there was no way it could require applications to use volatile.
                                        Posted by geoffclare at Apr 06, 2009 12:28
                                     |
| OK, I took 'volatile' out of the compliant solution.
                                        Posted by svoboda at Apr 07, 2009 09:26
                                     |
| I believe all the above comments have now been addressed.
                                        Posted by svoboda at Apr 14, 2009 16:55
                                     |
| Correct me if I'm wrong, but IMHO account_balance must be volatile. If it's not you risk your compiler optimizing it wrong. E.g. thread one, while (1);debit (1); ..... while thread two does something similar.... the mutex makes sure the debit operation is executed correctly, the volatile is there to ensure value is global between threads. .... again, IMHO
                                        Posted by mp6058@gmail.com at Oct 15, 2011 18:07
                                     |
| The presence of the mutex lock and unlock calls prevents the compiler from "optimizing it wrong".  There is definitely no need to use volatile in the compliant solution.
See also my reply to David Svoboda on Apr 06, 2009.
                                        Posted by geoffclare at Oct 17, 2011 06:37
                                     |
| Thank you for correcting me. Is this true for all compilers and all mutex implementation or only specific ones? Would the compiler do the right thing even if I implemented my own mutex? e.g. using some super-cool hardware dependendent method that only exists on my processor X.
                                        Posted by mp6058@gmail.com at Oct 17, 2011 22:32
                                     |
| It derives from a POSIX requirement on memory synchronisation (XBD section 4.11) so it should be true for all POSIX threads implementations.  I suppose in theory there could be an implementation that only provides this guarantee when a certain compiler is used, but I doubt it. My knowledge of this comes from the POSIX side, not the compiler side, so I'm not sure what would happen with mutex functions you write yourself.
                                        Posted by geoffclare at Oct 18, 2011 03:04
                                     |

