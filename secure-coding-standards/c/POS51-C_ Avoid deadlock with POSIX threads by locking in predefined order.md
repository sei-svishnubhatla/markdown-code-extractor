Mutexes are often used to prevent multiple threads from accessing critical resources at the same time. Sometimes, when locking mutexes, multiple threads hold each other's lock, and the program consequently deadlocks. There are four requirements for deadlock:
-   Mutual exclusion
-   Hold and wait
-   No preemption
-   Circular wait
Deadlock requires all four conditions, so to prevent deadlock, prevent any one of the four conditions. This guideline recommends locking the mutexes in a predefined order to prevent circular wait. This rule is a specific instance of [CON35-C. Avoid deadlock by locking in predefined order](https://www.securecoding.cert.org/confluence/display/seccode/CON35-C.+Avoid+deadlock+by+locking+in+predefined+order) using POSIX threads.
## Noncompliant Code Example
This noncompliant code example has behavior that depends on the runtime environment and the platform's scheduler. However, with proper timing, the `main()` function will deadlock when running `thr1` and `thr2`, where `thr1` tries to lock `ba2`'s mutex, while `thr2` tries to lock on `ba1`'s mutex in the `deposit()` function, and the program will not progress.
``` c
typedef struct {
  int balance;
  pthread_mutex_t balance_mutex;
} bank_account;
typedef struct {
  bank_account *from;
  bank_account *to;
  int amount;
} deposit_thr_args;
void create_bank_account(bank_account **ba, int initial_amount) {
  int result;
  bank_account *nba = malloc(sizeof(bank_account));
  if (nba == NULL) {
    /* Handle error */
  }
  nba->balance = initial_amount;
  result = pthread_mutex_init(&nba->balance_mutex, NULL);
  if (result) {
    /* Handle error */
  }
  *ba = nba;
}
void *deposit(void *ptr) {
  int result;
  deposit_thr_args *args = (deposit_thr_args *)ptr;
  if ((result = pthread_mutex_lock(&(args->from->balance_mutex))) != 0) {
    /* Handle error */
  }
  /* Not enough balance to transfer */
  if (args->from->balance < args->amount) {
    if ((result = pthread_mutex_unlock(&(args->from->balance_mutex))) != 0) {
      /* Handle error  */
    }
    return NULL;
  }
  if ((result = pthread_mutex_lock(&(args->to->balance_mutex))) != 0) {
    /* Handle error */
  }
  args->from->balance -= args->amount;
  args->to->balance += args->amount;
  if ((result = pthread_mutex_unlock(&(args->from->balance_mutex))) != 0) {
    /* Handle error */
  }
  if ((result = pthread_mutex_unlock(&(args->to->balance_mutex))) != 0) {
    /* Handle error */
  }
  free(ptr);
  return NULL;
}
int main(void) {
  pthread_t thr1, thr2;
  int result;
  bank_account *ba1;
  bank_account *ba2;
  create_bank_account(&ba1, 1000);
  create_bank_account(&ba2, 1000);
  deposit_thr_args *arg1 = malloc(sizeof(deposit_thr_args));
  if (arg1 == NULL) {
    /* Handle error */
  }
  deposit_thr_args *arg2 = malloc(sizeof(deposit_thr_args));
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
  if ((result = pthread_create(&thr1, NULL, deposit, (void *)arg1)) != 0) {
    /* Handle error */
  }
  if ((result = pthread_create(&thr2, NULL, deposit, (void *)arg2)) != 0) {
    /* Handle error */
  }
  pthread_exit(NULL);
  return 0;
}
```
## Compliant Solution
The solution to the deadlock problem is to use a predefined order for the locks in the `deposit()` function. In this compliant solution, each thread will lock on the basis of the `bank_account` ID, defined in the struct initialization. This solution prevents the circular wait problem:
``` c
typedef struct {
  int balance;
  pthread_mutex_t balance_mutex;
  unsigned int id; /* Should never be changed after initialized */
} bank_account;
unsigned int global_id = 1;
void create_bank_account(bank_account **ba, int initial_amount) {
  int result;
  bank_account *nba = malloc(sizeof(bank_account));
  if (nba == NULL) {
    /* Handle error */
  }
  nba->balance = initial_amount;
  result = pthread_mutex_init(&nba->balance_mutex, NULL);
  if (result != 0) {
    /* Handle error */
  }
  nba->id = global_id++;
  *ba = nba;
}
void *deposit(void *ptr) {
  deposit_thr_args *args = (deposit_thr_args *)ptr;
  int result;
  if (args->from->id == args->to->id)
        return;
  /* Ensure proper ordering for locking */
  if (args->from->id < args->to->id) {
    if ((result = pthread_mutex_lock(&(args->from->balance_mutex))) != 0) {
      /* Handle error */
    }
    if ((result = pthread_mutex_lock(&(args->to->balance_mutex))) != 0) {
      /* Handle error */
    }
  } else {
    if ((result = pthread_mutex_lock(&(args->to->balance_mutex))) != 0) {
      /* Handle error */
    }
    if ((result = pthread_mutex_lock(&(args->from->balance_mutex))) != 0) {
      /* Handle error */
    }
  }
  /* Not enough balance to transfer */
  if (args->from->balance < args->amount) {
    if ((result = pthread_mutex_unlock(&(args->from->balance_mutex))) != 0) {
      /* Handle error */
    }
    if ((result = pthread_mutex_unlock(&(args->to->balance_mutex))) != 0) {
      /* Handle error */
    }
    return;
  }
  args->from->balance -= args->amount;
  args->to->balance += args->amount;
  if ((result = pthread_mutex_unlock(&(args->from->balance_mutex))) != 0) {
    /* Handle error */
  }
  if ((result = pthread_mutex_unlock(&(args->to->balance_mutex))) != 0) {
    /* Handle error */
  }
  free(ptr);
  return;
}
```
## Risk Assessment
Deadlock prevents multiple threads from progressing, thus halting the executing program. A [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) is possible because the attacker can force deadlock situations. Deadlock is likely to occur in multithreaded programs that manage multiple shared resources.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS51-C | Low | Probable | Medium | P4 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports all potential deadlocks. |
| CodeSonar | 8.3p0 | CONCURRENCY.LOCK.ORDER | Conflicting lock order |
| Helix QAC | 2024.4 | C1772, C1773 |  |
| Klocwork | 2024.4 | CONC.DLCONC.NO_UNLOCK |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS51-a | Do not acquire locks in different order |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS51-C | Checks for deadlock (rule fully covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | LCK07-J. Avoid deadlock by requesting and releasing locks in the same order | Prior to 2018-01-12: CERT: Unspecified Relationship |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-764 and POS51-C/POS35-C
Independent( CWE-764, POS51-C, POS35-C)
CWE-764 is about semaphores, or objects capable of being locked multiple times. Deadlock arises from multiple locks being acquired in a cyclic order, and generally does not arise from semaphores or recursive mutexes.
## Bibliography

|  |  |
| ----|----|
| [Barney 2010] | pthread_mutex tutorial |
| [Bryant 2003] | Chapter 13, "Concurrent Programming" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152015) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152025)
