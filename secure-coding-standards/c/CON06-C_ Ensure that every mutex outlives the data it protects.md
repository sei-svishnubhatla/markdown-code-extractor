## \*\*\*\*\*\*\*\*\*\* Text below this note not yet converted from Java to C! \*\*\*\*\*\*\*\*\*\*\*\*
Programs must not use instance locks to protect static shared data because instance locks are ineffective when two or more instances of the class are created. Consequently, failure to use a static lock object leaves the shared state unprotected against concurrent access. Lock objects for classes that can interact with untrusted code must also be private and final, as shown in rule [LCK00-J. Use private final lock objects to synchronize classes that may interact with untrusted code](https://www.securecoding.cert.org/confluence/display/java/LCK00-J.+Use+private+final+lock+objects+to+synchronize+classes+that+may+interact+with+untrusted+code).
## Noncompliant Code Example (Nonstatic Lock Object for Static Data)
This noncompliant code example attempts to guard access to the static `counter` field using a non-static lock object. When two `Runnable` tasks are started, they create two instances of the lock object and lock on each instance separately.

|  |
| ----|
| public final class CountBoxes implements Runnable {; private static volatile int counter;  // ...  private final Object lock = new Object();   @Override public void run() {    synchronized (lock) {      counter++;      // ...    }  }   public static void main(String[] args) {    for (int i = 0; i < 2; i++) {    new Thread(new CountBoxes()).start();    }  }} |

This example fails to prevent either thread from observing an inconsistent value of `counter` because the increment operation on volatile fields fails to be atomic in the absence of proper synchronization. (See rule [VNA02-J. Ensure that compound operations on shared variables are atomic](https://www.securecoding.cert.org/confluence/display/java/VNA02-J.+Ensure+that+compound+operations+on+shared+variables+are+atomic) for more information.)
## Noncompliant Code Example (Method Synchronization for Static Data)
This noncompliant code example uses method synchronization to protect access to a static class `counter` field.

|  |
| ----|
| public final class CountBoxes implements Runnable {; private static volatile int counter;  // ...   public synchronized void run() {    counter++;    // ...  }  // ...} |

In this case, the method synchronization uses the intrinsic lock associated with each instance of the class rather than the intrinsic lock associated with the class itself. Consequently, threads constructed using different `Runnable` instances may observe inconsistent values of `counter`.
## Compliant Solution (Static Lock Object)
This compliant solution ensures the atomicity of the increment operation by locking on a static object.

|  |
| ----|
| public class CountBoxes implements Runnable {; private static int counter;  // ...  private static final Object lock = new Object();   public void run() {    synchronized (lock) {      counter++;      // ...    }  }  // ...} |

It is unnecessary to declare the `counter` variable volatile when using synchronization.
## Risk Assessment
Using an instance lock to protect static shared data can result in nondeterministic behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON06-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | ; | Supported, but no explicit checker |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-667, Improper Locking | Prior to 2018-01-12: CERT: |

## Bibliography

|  |
| ----|
| [API 2006] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151981) [](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151920)
