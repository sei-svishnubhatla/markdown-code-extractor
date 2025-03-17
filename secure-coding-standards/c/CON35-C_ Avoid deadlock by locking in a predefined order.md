Mutexes are used to prevent multiple threads from causing a data race by accessing shared resources at the same time. Sometimes, when locking mutexes, multiple threads hold each other's lock, and the program consequently deadlocks. Four conditions are required for deadlock to occur:
-   Mutual exclusion
-   Hold and wait
-   No preemption
-   Circular wait
Deadlock needs all four conditions, so preventing deadlock requires preventing any one of the four conditions. One simple solution is to lock the mutexes in a predefined order, which prevents circular wait.
## Noncompliant Code Example
The behavior of this noncompliant code example depends on the runtime environment and the platform's scheduler. The program is susceptible to deadlock if thread `thr1 `attempts to lock `ba2`'s mutex at the same time thread `thr2` attempts to lock `ba1`'s mutex in the `deposit()` function.
``` c
#include <stdlib.h>
#include <threads.h>
typedef struct {
  int balance;
  mtx_t balance_mutex;
} bank_account;
typedef struct {
  bank_account *from;
  bank_account *to;
  int amount;
} transaction;
void create_bank_account(bank_account **ba,
                         int initial_amount) {
  bank_account *nba = (bank_account *)malloc(
    sizeof(bank_account)
  );
  if (nba == NULL) {
    /* Handle error */
  }
  nba->balance = initial_amount;
  if (thrd_success
      != mtx_init(&nba->balance_mutex, mtx_plain)) {
    /* Handle error */
  }
  *ba = nba;
}
int deposit(void *ptr) {
  transaction *args = (transaction *)ptr;
  if (thrd_success != mtx_lock(&args->from->balance_mutex)) {
    /* Handle error */
  }
  /* Not enough balance to transfer */
  if (args->from->balance < args->amount) {
    if (thrd_success
        != mtx_unlock(&args->from->balance_mutex)) {
      /* Handle error */
    }
    return -1; /* Indicate error */
  }
  if (thrd_success != mtx_lock(&args->to->balance_mutex)) {
    /* Handle error */
  }
  args->from->balance -= args->amount;
  args->to->balance += args->amount;
  if (thrd_success
      != mtx_unlock(&args->from->balance_mutex)) {
    /* Handle error */
  }
  if (thrd_success
      != mtx_unlock(&args->to->balance_mutex)) {
    /* Handle error */
  }
  free(ptr);
  return 0;
}
int main(void) {
  thrd_t thr1, thr2;
  transaction *arg1;
  transaction *arg2;
  bank_account *ba1;
  bank_account *ba2;
  create_bank_account(&ba1, 1000);
  create_bank_account(&ba2, 1000);
  arg1 = (transaction *)malloc(sizeof(transaction));
  if (arg1 == NULL) {
    /* Handle error */
  }
  arg2 = (transaction *)malloc(sizeof(transaction));
  if (arg2 == NULL) {
    /* Handle error */
  }
  arg1->from = ba1;
  arg1->to = ba2;
  arg1->amount = 100;
  arg2->from = ba2;
  arg2->to = ba1;
  arg2->amount = 100;
  /* Perform the deposits */
  if (thrd_success
     != thrd_create(&thr1, deposit, (void *)arg1)) {
    /* Handle error */
  }
  if (thrd_success
      != thrd_create(&thr2, deposit, (void *)arg2)) {
    /* Handle error */
  }
  return 0;
} 
```
## Compliant Solution
This compliant solution eliminates the circular wait condition by establishing a predefined order for locking in the `deposit()` function. Each thread will lock on the basis of the `bank_account` ID, which is set when the `bank_account struct` is initialized.
``` c
#include <stdlib.h>
#include <threads.h>
typedef struct {
  int balance;
  mtx_t balance_mutex;
  /* Should not change after initialization */
  unsigned int id;
} bank_account;
typedef struct {
  bank_account *from;
  bank_account *to;
  int amount;
} transaction;
unsigned int global_id = 1;
void create_bank_account(bank_account **ba,
                         int initial_amount) {
  bank_account *nba = (bank_account *)malloc(
    sizeof(bank_account)
  );
  if (nba == NULL) {
    /* Handle error */
  }
  nba->balance = initial_amount;
  if (thrd_success
      != mtx_init(&nba->balance_mutex, mtx_plain)) {
    /* Handle error */
  }
  nba->id = global_id++;
  *ba = nba;
}
int deposit(void *ptr) {
  transaction *args = (transaction *)ptr;
  int result = -1;
  mtx_t *first;
  mtx_t *second;
  if (args->from->id == args->to->id) {
    return -1; /* Indicate error */
  }
  /* Ensure proper ordering for locking */
  if (args->from->id < args->to->id) {
    first = &args->from->balance_mutex;
    second = &args->to->balance_mutex;
  } else {
    first = &args->to->balance_mutex;
    second = &args->from->balance_mutex;
  }
  if (thrd_success != mtx_lock(first)) {
    /* Handle error */
  }
  if (thrd_success != mtx_lock(second)) {
    /* Handle error */
  }
  /* Not enough balance to transfer */
  if (args->from->balance >= args->amount) {
    args->from->balance -= args->amount;
    args->to->balance += args->amount;
    result = 0;
  }
  if (thrd_success != mtx_unlock(second)) {
    /* Handle error */
  }
  if (thrd_success != mtx_unlock(first)) {
    /* Handle error */
  }
  free(ptr);
  return result;
} 
```
## Risk Assessment
Deadlock prevents multiple threads from progressing, halting program execution. A [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) is possible if the attacker can create the conditions for deadlock.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON35-C | Low | Probable | Medium | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON35-C).
## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | deadlock | Supported by sound analysis (deadlock alarm) |
| CodeSonar | 8.3p0 | CONCURRENCY.LOCK.ORDER | Conflicting lock order |
| Coverity | 2017.07 | ORDER_REVERSAL | Fully implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-con35-c |  |
| Helix QAC | 2024.4 | C1772, C1773 |  |
| Klocwork | 2024.4 | CONC.DLCONC.NO_UNLOCK |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON35-a | Do not acquire locks in different order |
| PC-lint Plus | 1.4 | 2462 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON35-C | Checks for deadlock (rule partially covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | LCK07-J. Avoid deadlock by requesting and releasing locks in the same order | Prior to 2018-01-12: CERT: Unspecified Relationship |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152300) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151940)
## Comments:

|  |
| ----|
| 1. i don't think thread execution is random, exactly. can you state this more precisely?
2. you don't need an introduction header, and the introductory section should state precisely what the guideline is:  the developer should do something or should not do something.  The guideline should be written to be enforceable.  The title and the intro is the statement of the guideline; everything else is an example.
3. The references are not correctly formatted.
4. I don't think that 4 is a level.  Take another look at how priority and level are calculated.
5. I'll try to look at the technical content in depth later.
                                        Posted by rcs_mgr at Mar 04, 2010 22:43
                                     |
| In addition to Rob's comments, I have one:
    The code snippets are technically correct, but they are clearly abstract. Also they should probably have a main() method that starts the threads. You can say something like "with the right timing, this code could deadlock."  But I would like to also see a more practical example of deadlock...consider the AccountBalance class from CON12-J, which you helpfully linked to, thanks.
                                        Posted by svoboda at Mar 05, 2010 12:59
                                     |
| I have updated my code to have a more concrete example, and I believe all the problems stated has been addressed.
                                        Posted by pengfeil at Mar 17, 2010 13:58
                                     |
| The example is better. More comments:
    The references section should be last in the order
    Please use code tags when discussing code snippets in prose, eg: the foo() function.
    need to check for malloc failure on arg1 and arg2 in NCCE. Also need to check for errors in the various pthread routines.
    In the CS the id field should be declared const.
    Given the length of both code examples, the CS should not repeat any functions that are identical to those in the CCE. (such as main()).
                                        Posted by svoboda at Mar 17, 2010 15:42
                                     |
| I was thinking about having id as const, but I don't think there is a way to dynamically allocate a struct and set its const variable. But I might be wrong.
                                        Posted by pengfeil at Mar 18, 2010 18:54
                                     |
| As far as struct initialization goes, I think you're right. The way to do it in C++ is to use a class (rather than a struct), and then your id can be const, and initialized by the constructor. Using a class is better than a struct, since you can make the fields private, improving encapsulation.
                                        Posted by svoboda at Mar 18, 2010 20:17
                                     |

