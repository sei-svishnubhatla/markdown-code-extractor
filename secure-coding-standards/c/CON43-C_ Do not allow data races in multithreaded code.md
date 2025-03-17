When multiple threads can read or modify the same data, use synchronization techniques to avoid software flaws that can lead to security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). [Data races](BB.-Definitions_87152273.html#BB.Definitions-datarace) can often result in [abnormal termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) or [denial of service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack), but it is possible for them to result in more serious vulnerabilities. The C Standard, section 5.1.2.5, paragraph 35 \[[ISO/IEC 9899:2024](https://www.securecoding.cert.org/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2024)\], says:
> The execution of a program contains a data race if it contains two conflicting actions in different threads, at least one of which is not atomic, and neither happens before the other. Any such data race results in undefined behavior.

## Noncompliant Code Example
Assume this simplified code is part of a multithreaded bank system. Threads call `credit()` and `debit()` as money is deposited into and withdrawn from the single account. Because the addition and subtraction operations are not atomic, it is possible that two operations can occur concurrently, but only the result of one would be saved—despite declaring the `account_balance` `volatile`. For example, an attacker can credit the account with a sum of money and make a large number of small debits concurrently. Some of the debits might not affect the account balance because of the race condition, so the attacker is effectively creating money.
``` c
static volatile int account_balance;
void debit(int amount) {
  account_balance -= amount;
}
void credit(int amount) {
  account_balance += amount;
}
```
## Compliant Solution (Mutex)
This compliant solution uses a mutex to make credits and debits atomic operations. All credits and debits will now affect the account balance, so an attacker cannot exploit the race condition to steal money from the bank. The mutex is created with the `mtx_init()` function. The presence of the mutex makes declaring `account_balance` `volatile` unnecessary.
``` c
#include <threads.h>
static int account_balance;
static mtx_t account_lock;
int debit(int amount) {
  if (mtx_lock(&account_lock) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  account_balance -= amount;
  if (mtx_unlock(&account_lock) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  return 0;   /* Indicate success */
}
int credit(int amount) {
  if (mtx_lock(&account_lock) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  account_balance += amount;
  if (mtx_unlock(&account_lock) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  return 0;   /* Indicate success */
}
int main(void) {
  if(mtx_init(&account_lock, mtx_plain) == thrd_error) {
    /* Handle error */
  }
  /* ... */
}
```
## Compliant Solution (Atomic)
This compliant solution uses an atomic variable to synchronize credit and debit operations. All credits and debits will now affect the account balance, so an attacker cannot exploit the race condition to steal money from the bank. The atomic integer does not need to be initialized because default (zero) initialization of an atomic object with static or thread-local storage is guaranteed to produce a valid state. The `+=` and `-=` operators behave atomically when used with an atomic variable.
``` c
#include <stdatomic.h>
atomic_int account_balance;
void debit(int amount) {
  account_balance -= amount;
}
void credit(int amount) {
  account_balance += amount;
}
```
## Noncompliant Code Example (Double-Fetch)
This noncompliant code example illustrates Xen Security Advisory CVE-2015-8550 / [XSA-155](https://xenbits.xen.org/xsa/advisory-155.html) In this example, the following code is vulnerable to a data race where the integer referenced by `ps` could be modified by a second thread that ran between the two reads of the variable.
``` c
#include <stdio.h>
void doStuff(int *ps) {
  switch (*ps) {
    case 0: { printf("0"); break; }
    case 1: { printf("1"); break; }
    case 2: { printf("2"); break; }
    case 3: { printf("3"); break; }
    case 4: { printf("4"); break; }
    default: { printf("default"); break; }
  }
}
```
Even though there is only one read of the `*ps` variable in the source code, the compiler is permitted to produce object code that performs multiple reads of the memory location. This is permitted by the "as-if" principle, as explained by section 5.1 of the [\[C99 Rationale 2003\]](AA.-Bibliography_87152170.html#AA.Bibliography-C992003):
> The /as if/ principle is invoked repeatedly in this Rationale. The C89 Committee found that describing various aspects of the C language, library, and environment in terms of concrete models best serves discussion and presentation. Every attempt has been made to craft these models so that implementations are constrained only insofar as they must bring about the same result, /as if/ they had implemented the presentation model; often enough the clearest model would make for the worst implementation.

### Implementation Details (GCC)
This code produces two reads of the `*ps` value using GCC 4.8.4 on x86, as well as GCC 5.3.0 on x86-64 ([Compiler-Introduced Double-Fetch Vulnerabilities – Understanding XSA-155](http://tkeetch.co.uk/blog/?p=58)).
## Noncompliant Code Example (Volatile)
The data race can be disabled by declaring the data to be volatile, because the `volatile` keyword forces the compiler to not produce two reads of the data. However, this violates [CON02-C. Do not use volatile as a synchronization primitive](CON02-C_%20Do%20not%20use%20volatile%20as%20a%20synchronization%20primitive).
``` c
#include <stdio.h>
void doStuff(volatile int *ps) {
  switch (*ps) {
    case 0: { printf("0"); break; }
    case 1: { printf("1"); break; }
    case 2: { printf("2"); break; }
    case 3: { printf("3"); break; }
    case 4: { printf("4"); break; }
    default: { printf("default"); break; }
  }
}
```
## Compliant Solution (C11, Atomic)
Declaring the data to be atomic also forces the compiler to produce only one read of the data.
``` c
#include <stdio.h>
#include <stdatomic.h>
void doStuff(atomic_int *ps) {
  switch (atomic_load(ps)) {
    case 0: { printf("0"); break; }
    case 1: { printf("1"); break; }
    case 2: { printf("2"); break; }
    case 3: { printf("3"); break; }
    case 4: { printf("4"); break; }
    default: { printf("default"); break; }
  }
}
```
## Compliant Solution (C11, Fences)
The bug was actually resolved by erecting fences around the `switch` statement.
``` c
#include <stdio.h>
#include <stdatomic.h>
void doStuff(int *ps) {
  atomic_thread_fence(memory_order_acquire);
  switch (*ps) {
    case 0: { printf("0"); break; }
    case 1: { printf("1"); break; }
    case 2: { printf("2"); break; }
    case 3: { printf("3"); break; }
    case 4: { printf("4"); break; }
    default: { printf("default"); break; }
  }
  atomic_thread_fence(memory_order_release);
}
```
## Risk Assessment
Race conditions caused by multiple threads concurrently accessing and modifying the same data can lead to abnormal termination and denial-of-service attacks or data integrity violations.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON43-C | Medium | Probable | High | P4 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | read_data_racewrite_data_race | Supported by sound analysis (data race alarm) |
| CodeSonar | 8.3p0 | CONCURRENCY.DATARACECONCURRENCY.MAA
 | Data raceMultiple Accesses of Atomic |
| Coverity | 2017.07 | MISSING_LOCK (partial) | Implemented |
| Helix QAC | 2024.4 | C1765, C1766, C1770, C1771C++1765, C++1766, C++1770, C++1771 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON43-a | Do not use global variable with different locks set |
| PC-lint Plus | 1.4 | 457 | Partially supported: access is detected at the object level (not at the field level) |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON43-C | Checks for data race (rule fully covered) |
| PVS-Studio | 7.35 | V1088 |  |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON43-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-366, Race condition within a thread | 2017-07-07: CERT: Exact |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 5.1.2.5, "Multi-threaded Executions and Data Races" |
| [C99 Rationale 2003] |  |
| [Dowd 2006] | Chapter 13, "Synchronization and State" |
| [Plum 2012] |  |
| [Seacord 2013] | Chapter 8, "File I/O" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151936) [](../c/Rule%2014_%20Concurrency%20_CON_) [](../c/Rule%2048_%20Miscellaneous%20_MSC_)
## Comments:

|  |
| ----|
| It may be beyond the scope of this entire effort to give meaningful advice for mutithreaded environments, but I believe that in addition to mutexes, some platforms require the variable that the mutex is protecting to be declared "volatile" to prevent the compiler from holding it in a register in a uniprocessor environment and/or managing the system caches properly in a multiprocessor environment.
We need to read the POSIX Threads documentation carefully to make sure our examples don't violate some other required programming practice.
                                        Posted by wlf@cert.org at Apr 26, 2007 09:51
                                     |
| I believe that volatile is not, in fact, part of the pthreads documentation, although it can be necessary to guarantee correctness.
                                        Posted by jpincar at May 21, 2007 16:46
                                     |
| "volatile" is essential, for the reason described in the text.; It is not the only component of thread safety, but it is an important one.  Note that the anti-caching measure could be applied via a local (volatile ...) cast, but that has to be done in writers as well as readers, so in most cases it might as well be permanently affixied via the declaration.
I also note that some (vocal) people has misinterpreted some of the POSIX thread specs to require that the implementation (compiler) guarantee safety for certain operations.  The actual meaning of the specs was that the programmer has to ensure the safety by explicit mutexes etc.
Since thread programming is so tricky (C wasn't designed for it) and so many people do it wrong, it may be worth advising: "Because the cached shared-memory nature of normal data objects makes safe, correct thread programming difficult, in many cases a solution using separate processes (which don't share memory except through intentional acts) is preferable."
                                        Posted by dagwyn at Apr 18, 2008 14:59
                                     |
| added a ref to DCL34-C. Use volatile for data that cannot be cached
                                        Posted by avolkovi at May 19, 2008 14:07
                                     |
| The volatile qualifier is not required, see POS03-C. Do not use volatile as a synchronization primitive, the pthread_mutex_lock and pthread_mutex_unlock should be enough to ensure there is no caching or prefetching.
                                        Posted by suruena at Dec 23, 2010 12:15
                                     |
| You're right. I corrected the compliant solution and moved the volatile to the noncompliant example to make it clear that the qualifier is neither necessary nor sufficient.
                                        Posted by martinsebor at Dec 23, 2010 15:09
                                     |
| I'm not convinced that the compliant solution with fences is actually guaranteed to fix the problem. I also don't think it's an accurate representation of how Xen actually fixed it.
                                        Posted by jcsible at Jul 07, 2020 11:31
                                     |

