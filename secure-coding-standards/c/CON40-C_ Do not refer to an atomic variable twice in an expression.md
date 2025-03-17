A consistent locking policy guarantees that multiple threads cannot simultaneously access or modify shared data. Atomic variables eliminate the need for locks by guaranteeing thread safety when certain operations are performed on them. The thread-safe operations on atomic variables are specified in the C Standard, subclauses 7.17.7 and 7.17.8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\]. While atomic operations can be combined, combined operations do not provide the thread safety provided by individual atomic operations.
Every time an atomic variable appears on the left side of an assignment operator, including a compound assignment operator such as `*=`, an atomic write is performed on the variable. The use of the increment (++`)` or decrement `(--)` operators on an atomic variable constitutes an atomic read-and-write operation and is consequently thread-safe. Any reference of an atomic variable anywhere else in an expression indicates a distinct atomic read on the variable.
If the same atomic variable appears twice in an expression, then two atomic reads, or an atomic read and an atomic write, are required. Such a pair of atomic operations is not thread-safe, as another thread can modify the atomic variable between the two operations. Consequently, an atomic variable must not be referenced twice in the same expression.
## Noncompliant Code Example (`atomic_bool`)
This noncompliant code example declares a shared atomic_bool flag variable and provides a toggle_flag() method that negates the current value of flag:
``` c
#include <stdatomic.h>
#include <stdbool.h>
static atomic_bool flag = ATOMIC_VAR_INIT(false);
void init_flag(void) {
  atomic_init(&flag, false);
}
void toggle_flag(void) {
  bool temp_flag = atomic_load(&flag);
  temp_flag = !temp_flag;
  atomic_store(&flag, temp_flag);
}
bool get_flag(void) {
  return atomic_load(&flag);
}
```
Execution of this code may result in unexpected behavior because the value of `flag` is read, negated, and written back. This occurs even though the read and write are both atomic.
Consider, for example, two threads that call `toggle_flag()`. The expected effect of toggling `flag` twice is that it is restored to its original value. However, the scenario in the following table leaves `flag` in the incorrect state.
###### `toggle_flag()` without Compare-and-Exchange

| Time | flag | Thread | Action |
| ----|----|----|----|
| 1 | true | t1 | Reads the current value of;flag, which is true, into a cache |
| 2 | true | t2 | Reads the current value of;flag, which is still true, into a different cache |
| 3 | true | t1 | Toggles the temporary variable in the cache to;false |
| 4 | true | t2 | Toggles the temporary variable in the different cache to;false |
| 5 | false | t1 | Writes the cache variable's value to;flag |
| 6 | false | t2 | Writes the different cache variable's value to;flag |

As a result, the effect of the call by *t*<sub>2</sub> is not reflected in `flag`; the program behaves as if `toggle_flag()` was called only once, not twice.
## Compliant Solution (atomic_compare_exchange_weak())
This compliant solution uses a compare-and-exchange to guarantee that the correct value is stored in `flag`. All updates are visible to other threads. The call to `atomic_compare_exchange_weak()` is in a loop in conformance with CON41-C. Wrap functions that can fail spuriously in a loop.
``` c
#include <stdatomic.h>
#include <stdbool.h>
static atomic_bool flag = ATOMIC_VAR_INIT(false);
void init_flag(void) {
  atomic_init(&flag, false);
}
void toggle_flag(void) {
  bool old_flag = atomic_load(&flag);
  bool new_flag;
  do {
    new_flag = !old_flag;
  } while (!atomic_compare_exchange_weak(&flag, &old_flag, new_flag));
}
bool get_flag(void) {
  return atomic_load(&flag);
}
```
An alternative solution is to use the `atomic_flag` data type for managing Boolean values atomically. However, `atomic_flag` does not support a toggle operation.
## Compliant Solution (Compound Assignment)
This compliant solution uses the `^=`  assignment operation to toggle `flag`. This operation is guaranteed to be atomic, according to the C Standard, 6.5.17.5, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\]. This operation performs a bitwise-exclusive-or between its arguments, but for Boolean arguments, this is equivalent to negation.
``` c
#include <stdatomic.h>
#include <stdbool.h>
static atomic_bool flag = ATOMIC_VAR_INIT(false);
void toggle_flag(void) {
  flag ^= 1;
}
bool get_flag(void) {
  return flag;
}
```
An alternative solution is to use a mutex to protect the atomic operation, but this solution loses the performance benefits of atomic variables.
## Noncompliant Code Example
This noncompliant code example takes an atomic global variable `n` and computes `n + (n - 1) + (n - 2) + ... + 1`, using the formula `n * (n + 1) / 2`:
``` c
#include <stdatomic.h>
atomic_int n = ATOMIC_VAR_INIT(0);
int compute_sum(void) {
  return n * (n + 1) / 2;
}
```
The value of `n` may change between the two atomic reads of `n` in the expression, yielding an incorrect result.
## Compliant Solution
This compliant solution passes the atomic variable as a function argument, forcing the variable to be copied and guaranteeing a correct result. Note that the function's formal parameter need not be atomic, and the atomic variable can still be passed as an actual argument.
``` c
#include <stdatomic.h>
int compute_sum(int n) {
  return n * (n + 1) / 2;
}
```
## Risk Assessment
When operations on atomic variables are assumed to be atomic, but are not atomic, surprising data races can occur, leading to corrupted data and invalid control flow.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON40-C | Medium | Probable | Medium | P8 | L2 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | multiple-atomic-accesses | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-CON40 |  |
| CodeSonar | 8.3p0 | CONCURRENCY.MAA | Multiple Accesses of Atomic |
| Coverity | 2017.07 | EVALUATION_ORDER (partial)MISRA 2012 Rule 13.2VOLATILE_ATOICITY (possible) | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-con40-c |  |
| Helix QAC | 2024.4 | C1114, C1115, C1116C++3171, C++4150 |  |
| Klocwork | 2024.4 | CERT.CONC.ATOMIC_TWICE_EXPR |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON40-a | Do not refer to an atomic variable twice in an expression |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON40-C | Checks for:Atomic variable accessed twice in an expressionAtomic load and store sequence not atomicRule fully covered. |
| RuleChecker | 24.04 | multiple-atomic-accesses | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON40-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-366, Race Condition within a Thread | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-366 and CON40-C
CON40-C = Subset( CON43-C) Intersection( CON32-C, CON40-C) = Ø
CWE-366 = Union( CON40-C, list) where list =
-   C data races that do not involve an atomic variable used twice within an expression
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.5.17.3, "Compound Assignment"7.17, "Atomics" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151919) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151936)
## Comments:

|  |
| ----|
| from Jürgen Schäfer:; The compliant solutionvoid toggle_flag(void) {

      bool old_flag = atomic_load(&flag);
      bool new_flag;
      do {
        new_flag = !old_flag; 
      } while (!atomic_compare_exchange_weak(&flag,&old_flag, new_flag)); 
    } 
migt be changed to ...
    void toggle_flag(void) {
      bool new_flag;
      bool old_flag;
      do { 
        old_flag = atomic_load(&flag);
        new_flag = !old_flag; 
      } while (!atomic_compare_exchange_weak(&flag, &old_flag, new_flag)); 
    } 
The load/reload must be placed within the loop. Am I wrong? With kind regards Jürgen
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 05, 2014 09:32
\| \|
No, the loop is simply because the atomic_compare_exchange_weak() function is permitted to *fail spuriously,* so we have to call it repeatedly until it succeeds.; The atomic_load() only needs to be called once, before the loop.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 05, 2014 09:39
\| \|
The following sentence below the first NCCE isn't correct:
Execution of this code may result in a;[data race](https://www.securecoding.cert.org/confluence/display/c/BB.+Definitions#BB.Definitions-datarace) because the value of `flag` is read, negated, and written back. This occurs even though the read and write are both atomic.
C defines a *data race* like this:
The execution of a program contains a data race if it contains two conflicting actions in different threads, at least one of which is not atomic, and neither happens before the other.
Since the `flag` variable is atomic and `temp_flag` is a local (i.e., distinct in each thread, and thus not subject to conflicting accesses), there is no data race.  (The program just may not have the intended effect.)
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 10, 2016 11:36
\| \|
I think you're correct, and so I've changed the wording to remove mention of data race.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 10, 2016 13:44
\|
