Reading a shared primitive variable in one thread may not yield the value of the most recent write to the variable from another thread. Consequently, the thread may observe a stale value of the shared variable. To ensure the visibility of the most recent update, the write to the variable must *happen before* the read (C Standard, subclause 5.1.2.4, paragraph 18 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]). Atomic operations—other than relaxed atomic operations—trivially satisfy the happens before relationship. Where atomic operations are inappropriate, protecting both reads and writes with a mutex also satisfies the happens before relationship.
## \*\*\*\*\*\*\*\*\*\*\* Text below this note not yet converted from Java to C! \*\*\*\*\*\*\*\*\*\*\*\*
## Noncompliant Code Example (Non-volatile Flag)
This noncompliant code example uses a `shutdown()` method to set the non-volatile `done` flag that is checked in the `run()` method.
``` java
final class ControlledStop implements Runnable {
  private boolean done = false;
  @Override public void run() {
    while (!done) {
      try {
        // ...
        Thread.currentThread().sleep(1000); // Do something
      } catch(InterruptedException ie) { 
        Thread.currentThread().interrupt(); // Reset interrupted status
      } 
    }    
  }
  public void shutdown() {
    done = true;
  }
}
```
If one thread invokes the `shutdown()` method to set the flag, a second thread might not observe that change. Consequently, the second thread might observe that `done` is still `false` and incorrectly invoke the `sleep()` method. Compilers and just-in-time compilers (JITs) are allowed to optimize the code when they determine that the value of `done` is never modified by the same thread, resulting in an infinite loop.
## Compliant Solution (`Volatile`)
In this compliant solution, the `done` flag is declared volatile to ensure that writes are visible to other threads.
``` java
final class ControlledStop implements Runnable {
  private volatile boolean done = false;
  @Override public void run() {
    while (!done) {
      try {
        // ...
        Thread.currentThread().sleep(1000); // Do something
      } catch(InterruptedException ie) { 
        Thread.currentThread().interrupt(); // Reset interrupted status
      } 
    }    
  }
  public void shutdown() {
    done = true;
  }
}
```
## Compliant Solution (`AtomicBoolean`)
In this compliant solution, the `done` flag is declared to be of type `java.util.concurrent.atomic.AtomicBoolean`. Atomic types also guarantee that writes are visible to other threads.
``` java
final class ControlledStop implements Runnable {
  private final AtomicBoolean done = new AtomicBoolean(false);
  @Override public void run() {
    while (!done.get()) {
      try {
        // ...
        Thread.currentThread().sleep(1000); // Do something
      } catch(InterruptedException ie) { 
        Thread.currentThread().interrupt(); // Reset interrupted status
      } 
    }    
  }
  public void shutdown() {
    done.set(true);
  }
}
```
## Compliant Solution (`synchronized`)
This compliant solution uses the intrinsic lock of the `Class` object to ensure that updates are visible to other threads.
``` java
final class ControlledStop implements Runnable {
  private boolean done = false;
  @Override public void run() {
    while (!isDone()) {
      try {
        // ...
        Thread.currentThread().sleep(1000); // Do something
      } catch(InterruptedException ie) { 
        Thread.currentThread().interrupt(); // Reset interrupted status
      } 
    }    
  }
  public synchronized boolean isDone() {
    return done;
  }
  public synchronized void shutdown() {
    done = true;
  }
}
```
While this is an acceptable compliant solution, intrinsic locks cause threads to block and may introduce contention. On the other hand, volatile-qualified shared variables do not block. Excessive synchronization can also make the program prone to deadlock.
Synchronization is a more secure alternative in situations where the `volatile` keyword or a `java.util.concurrent.atomic.Atomic*` field is inappropriate, such as when a variable's new value depends on its current value. See rule [VNA02-J. Ensure that compound operations on shared variables are atomic](https://wiki.sei.cmu.edu/confluence/display/java/VNA02-J.+Ensure+that+compound+operations+on+shared+variables+are+atomic) for more information.
Compliance with rule [LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code](https://wiki.sei.cmu.edu/confluence/display/java/LCK00-J.+Use+private+final+lock+objects+to+synchronize+classes+that+may+interact+with+untrusted+code) can reduce the likelihood of misuse by ensuring that untrusted callers cannot access the lock object.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON03-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/CON02-C.+Do+not+use+volatile+as+a+synchronization+primitive) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=46498126) [](https://www.securecoding.cert.org/confluence/display/seccode/CON04-C.+Join+or+detach+threads+even+if+their+exit+status+is+unimportant)
## Comments:

|  |
| ----|
| This example should be converted to C language as soon as is possible. The reason is because the compliant code example using the `volatile` keyword is extremely misleading for a C language audience, as `volatile` in Java brings both the idea of `volatile` from the C language realm as well as the idea of being synchronized (from the Java sense), meaning that it is cross-thread visible. But in C language, the volatile keyword does not have any sense of being synchronized (visible) across threads. In C language, neither does the `volatile` keyword even convey atomicity or memory ordering. In C language, the effect of a volatile access is only guaranteed to have occurred by the next sequence point within the same thread of execution.
                                        Posted by morano at Jul 17, 2018 16:44
                                     |
| Thank you for the suggestion. We quite agree that volatile;means subtly different things in C and Java, and we have several rules and recommendations about it, including CON02-C. Do not use volatile as a synchronization primitive. We will update the code examples when we can, but updating the recommendations is a lower priority than updating the rules.
                                        Posted by svoboda at Jul 18, 2018 14:23
                                     |

