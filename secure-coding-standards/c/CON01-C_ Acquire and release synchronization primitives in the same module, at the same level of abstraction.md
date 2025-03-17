All locking and unlocking of mutexes should be performed in the same module and at the same level of abstraction. Failure to follow this recommendation can lead to some lock or unlock operations not being executed by the multithreaded program as designed, eventually resulting in deadlock, race conditions, or other security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), depending on the mutex type.
A common consequence of improper locking is for a mutex to be unlocked twice, via two calls to` mtx_unlock()`. This can cause the unlock operation to return errors. In the case of recursive mutexes, an error is returned only if the lock count is 0 (making the mutex available to other threads) and a call to `mtx_unlock()` is made.
## Noncompliant Code Example
In this noncompliant code example for a simplified multithreaded banking system, imagine an account with a required minimum balance. The code would need to verify that all debit transactions are allowable. Suppose a call is made to `debit()` asking to withdraw funds that would bring `account_balance` below `MIN_BALANCE`, which would result in two calls to `mtx_unlock()`. In this example, because the mutex is defined statically, the mutex type is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior).
``` c
#include <threads.h>
enum { MIN_BALANCE = 50 };
int account_balance;
mtx_t mp;
/* Initialize mp */
int verify_balance(int amount) {
  if (account_balance - amount < MIN_BALANCE) {
    /* Handle error condition */
    if (mtx_unlock(&mp) ==  thrd_error) {
      /* Handle error */
    }
    return -1;
  }
  return 0;
}
void debit(int amount) {
  if (mtx_lock(&mp) == thrd_error) {
    /* Handle error */
  }
  if (verify_balance(amount) == -1) {
    if (mtx_unlock(&mp) == thrd_error) {
      /* Handle error */
    }
    return;
  }
  account_balance -= amount;
  if (mtx_unlock(&mp) == thrd_error) {
    /* Handle error */
  }
}
```
## Compliant Solution
This compliant solution unlocks the mutex only in the same module and at the same level of abstraction at which it is locked. This technique ensures that the code will not attempt to unlock the mutex twice.
``` c
#include <threads.h>
enum { MIN_BALANCE = 50 };
static int account_balance;
static mtx_t mp;
/* Initialize mp */
static int verify_balance(int amount) {
  if (account_balance - amount < MIN_BALANCE) {
    return -1;   /* Indicate error to caller */
  }
  return 0;  /* Indicate success to caller */
}
int debit(int amount) {
  if (mtx_lock(&mp) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  if (verify_balance(amount)) {
    mtx_unlock(&mp);
    return -1;   /* Indicate error to caller */
  }
  account_balance -= amount;
  if (mtx_unlock(&mp) == thrd_error) {
    return -1;   /* Indicate error to caller */
  }
  return 0;   /* Indicate success */
}
```
## Risk Assessment
Improper use of mutexes can result in [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) or the unexpected termination of a multithreaded program.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON01-C | Low | Probable | Medium | P4 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | CONCURRENCY.LOCK.NOLOCKCONCURRENCY.LOCK.NOUNLOCK | Missing Lock AcquisitionMissing Lock Release |
| Coverity | 6.5 | LOCK | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-CON01-a | Do not abandon unreleased locks |
| PC-lint Plus | 1.4 | 454, 455, 456 | Partially supported: acquire and release synchronization primitives within the same scope |
| Polyspace Bug Finder | R2024a | CERT C: Rec. CON01-C | Checks for:Missing lock and unlock functionsDouble lock or double unlockRec. fully covered. |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, pthread_mutex_initXSH, System Interfaces, pthread_mutex_lock, pthread_mutex_unlock
XSH, System Interfaces, pthread_mutexattr_init |

------------------------------------------------------------------------
[](../c/Rec_%2014_%20Concurrency%20_CON_) [](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152314)
## Comments:

|  |
| ----|
| Good rule so far. Comments:
    The intro needs more specific details of what can happen. (eg race codnitions/ deadlock)
    The NCCE intro paragraph needs grammar-checked. (I can't identify the verb in the 2nd sentence)
    In the NCCE intro paragraph, the mutex type info is interesting, but the code says nothing about different mutex types. So what is the behavior of the NCCE as it is currently written?
    You should list exceptions to this rule. There's one in POS47-C. Do not use threads that can be cancelled asynchronously, and I'll bet there are others.
                                        Posted by svoboda at May 26, 2010 15:33
                                     |
| Summary of the changes made:
    added the possibility of deadlock to the intro
    fixed the grammar errors in the NCCE paragraph
    indicated behavior of example as written
Is POS47-C really an exception? The CCE for that rule follows this recommendation, even though the NCCE's do not.
                                        Posted by krishant at May 26, 2010 17:58
                                     |
| I think it is, so I added the exception. Everything else looks good.
                                        Posted by svoboda at May 27, 2010 15:46
                                     |
| A few comments:
    I suggest to rename the guideline to include other types of synchronization primitives and for consistency with MEM00-C. Allocate and free memory in the same module, at the same level of abstraction. How about: Acquire and release synchronization primitives in the same module, at the same level of abstraction.
    The description says:
Failure to follow this recommendation can [...] result in deadlock or other security vulnerabilities, depending on the mutex type.
Can you elaborate on the other types of vulnerabilities besides deadlock (and undefined behavior) that violating this guideline has been known to result in? Do you happen to have pointers to relevant entries in the CVE of OSVDB databases for example? I ask because I haven't been able to find anything specific.
    If you do know of other types of vulnerabilities that are more severe than deadlock then I suggest updating Severity.
    I suggest moving the discussion of the different types of POSIX mutexes in the first NCCE into the description of the guideline.
    The volatile qualifier in the examples is unnecessary. I suggest to remove it for the sake of clarity (see also POS03-C. Do not use volatile as a synchronization primitive and DCL34-C. Use volatile for data that cannot be cached).
    I suggest referencing relevant CWE entries. They might include:
        CWE-404: Improper Resource Shutdown or Release
        CWE-664: Improper Control of a Resource Through its Lifetime
        CWE-667: Insufficient Locking
        CWE-675: Duplicate Operations on Resource
        CWE-764: Multiple Locks of a Critical Resource
        CWE-765: Multiple Unlocks of a Critical Resource.
                                        Posted by martinsebor at May 29, 2010 18:35
                                     |
| Martin, I made all the changes you suggested, except for the following:
      Can you elaborate on the other types of vulnerabilities besides deadlock (and undefined behavior) that violating this guideline has been known to result in? Do you happen to have pointers to relevant entries in the CVE of OSVDB databases for example? I ask because I haven't been able to find anything specific.
   3. If you do know of other types of vulnerabilities that are more severe than deadlock then I suggest updating Severity.
The two main hazards with locking bugs are deadlocks and race conditions AKA data races, which the locks are designed to prevent. I don't have any particular details of worse things that can happen. (I expect a double unlock might cause an out-of-bounds read or a null pointer dereference on some platform.)
   6. I suggest referencing relevant CWE entries. They might include:...
I think we've been using an external table to map CWE references and CERT rules. So this association belongs on the wiki, but not necessarily here.
                                        Posted by svoboda at Jun 01, 2010 15:01
                                     |
| Great! I suspect you might be right about double unlock potentially having the same effects as double free even though I don't see anything to support that hypothesis in the Solaris mutex_unlock() code or in glibc pthread_mutex_unlock().
Are you fine with renaming the practice?
                                        Posted by martinsebor at Jun 02, 2010 23:04
                                     |
| Yes, I adjusted the title as you suggested.
BTW double free() is considerably worse than I was suggesting...in the right circumstances, a double free() can permit an attacker to run shellcode.  I don't see how that is possible with a double unlock. AFAICT a double unlock is undefined behavior, so what happens next is up to the implementation.  I just suspect it might cause an out-of-bounds read or null pointer dereference.  Which might lead to a program crash.  Which is much less harmful than shellcode.
EDIT: I suppose a double-unlock could lead to executable shellcode if it caused a double-free. I still think its very unlikely.
                                        Posted by svoboda at Jun 03, 2010 10:41
                                     |
| Looks good, thanks!
Re: double unlock and double free, I was thinking that if pthread_mutex_unlock() resulted in unlinking the mutex from a linked list as it seems to in the Solaris implementation (see the call to queue_lock() in mutex_wakeup()) then it could have the same effect as double free (i.e., writing arbitrary values to arbitrary memory). It does seem like it would be pretty hard to control though.
It might be fun to try to produce an exploit – if only I had a few weeks of free time on my hands...
                                        Posted by martinsebor at Jun 05, 2010 16:50
                                     |
| I think the verify_balance function of the compliant solution is not OK because it is reading the account_balance global variable without first acquiring the mutex. POSIX avoids race conditions preventing memory conflicts (i.e. two threads cannot access the same memory location at the same time, and at least one is a write), so just locking the mutex from the writer thread is not enough: The reader must also lock the mutex before reading the shared variable to ensure this thread does not read it while being modified by other thread (is not guaranteed to be an atomic operation).
                                        Posted by suruena at Dec 23, 2010 12:29
                                     |
| I think the intent is that verify_balance() is a implementation function that can only be called from debit() when the mutex is locked. I tried to make it clearer by declaring the function static.
However, there was a race condition in the compliant solution in assigning to the global variable ret. Since the variable isn't necessary to demonstrate the problem or the solution I removed it.
                                        Posted by martinsebor at Dec 23, 2010 15:32
                                     |
| Thanks for the clarification, I though verify_balance() was meant to be called concurrently. No data race is possible then.
Good idea using static for private objects and functions!
                                        Posted by suruena at Dec 23, 2010 19:49
                                     |
| This is clearly good advice. ;Perhaps we should add the true requirement, which permits more possible placements than this.  That true requirement is this:Each mutex acquisition must dominate the matching mutex release, andEach mutex release must post-dominate the matching mutex acquisitionwhere the domination and post-domination properties are defined over the executing thread's global control-flow graph. Further, intervening acquisition or release of the mutex is permitted only for recursive mutexes and only when the acquisitions and releases are correctly balanced. Thinking a bit more, even that requirement isn't (quite) the true minimal requirement. We actually need a (set of) mutex acquisitions and a matching set of mutex releases where the acquisition(s) collectively dominate the release(s) and the releases collectively post-dominate the acquisitions (and the rule about intervening operations on the same mutex still holds). But that's getting rather baroque.
                                        Posted by dfsutherland at Aug 22, 2013 12:12
                                     |

