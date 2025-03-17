VOIDWhen multiple threads can read or modify the same data, use synchronization techniques to avoid software flaws that can lead to security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). This recommendation is a specific instance of [CON00-C. Avoid race conditions with multiple threads](https://www.securecoding.cert.org/confluence/display/seccode/CON00-C.+Avoid+race+conditions+with+multiple+threads) using POSIX threads. Concurrency problems can often result in abnormal termination or denial of service, but it is possible for them to result in more serious vulnerabilities.
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
## Compliant Solution
This compliant solution uses a mutex to make credits and debits atomic operations. All credits and debits will now affect the account balance, so an attacker cannot exploit the race condition to steal money from the bank. The mutex is created with the `pthread_mutex_create()` function. Note that the presence of the mutex makes declaring `account_balance` `volatile` unnecessary.
``` c
#include <pthread.h>
static int account_balance;
static pthread_mutex_t account_lock = PTHREAD_MUTEX_INITIALIZER;
int debit(int amount) {
  if (pthread_mutex_lock(&account_lock))
    return -1;   /* indicate error to caller */
  account_balance -= amount;
  if (pthread_mutex_unlock(&account_lock))
    return -1;   /* indicate error to caller */
  return 0;   /* indicate success */
}
int credit(int amount) {
  if (pthread_mutex_lock(&account_lock))
    return -1;   /* indicate error to caller */
  account_balance += amount;
  if (pthread_mutex_unlock(&account_lock))
    return -1;   /* indicate error to caller */
  return 0;   /* indicate success */
}
```
## Risk Assessment
Race conditions caused by multiple threads concurrently accessing and modifying the same data can lead to abnormal termination and denial-of-service attacks or data integrity violations.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS05-C | medium | probable | high | P4 | L3 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS00-C).
## Related Guidelines
[MITRE CWE](http://cwe.mitre.org/): [CWE-366](http://cwe.mitre.org/data/definitions/366.html), "Race condition within a thread"
## Sources
\[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\] Chapter 13, "Synchronization and State"  
\[[Seacord 2005a](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord05)\] Chapter 7, "File I/O"
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=46498126) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=46498126) [](https://www.securecoding.cert.org/confluence/display/seccode/POS06-C.+Acquire+and+release+POSIX+synchronization+primitives+in+the+same+module%2C+at+the+same+level+of+abstraction)
