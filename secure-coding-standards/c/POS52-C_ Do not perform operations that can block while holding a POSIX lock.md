If a lock is being held and an operation that can block is performed, any other thread that needs to acquire that lock may also block. This condition can degrade the performance of a system or cause a deadlock to occur.
Blocking calls include, but are not limited to: network, file, and console I/O. This rule is a specific instance of [CON05-C. Do not perform operations that can block while holding a lock](CON05-C_%20Do%20not%20perform%20operations%20that%20can%20block%20while%20holding%20a%20lock) using POSIX threads.
## Noncompliant Code Example
This noncompliant code example demonstrates an occurrence of a blocking call that waits to receive data on a socket while a mutex is locked. The `recv()` call blocks until data arrives on the socket. While it is blocked, other threads that are waiting for the lock are also blocked.
Although this example is specific to network I/O, the `recv()` call could be replaced with any blocking call, and the same behavior would occur.
``` c
pthread_mutexattr_t attr;
pthread_mutex_t mutex;
void thread_foo(void *ptr) {
  uint32_t num;
  int result;
  int sock;
  /* sock is a connected TCP socket */
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle Error */
  }
  if ((result = recv(sock, (void *)&num, sizeof(uint32_t), 0)) < 0) {
    /* Handle Error */
  }
  /* ... */
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle Error */
  }
}
int main() {
  pthread_t thread;
  int result;
  if ((result = pthread_mutexattr_settype(
      &mutex, PTHREAD_MUTEX_ERRORCHECK)) != 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_init(&mutex, &attr)) != 0) {
    /* Handle Error */
  }
  if (pthread_create(&thread, NULL,(void *)& thread_foo, NULL) != 0) {
    /* Handle Error */
  }
  /* ... */
  pthread_join(thread, NULL);
  if ((result = pthread_mutex_destroy(&mutex)) != 0) {
    /* Handle Error */
  }
  return 0;
}
```
## Compliant Solution (Block while Not Locked)
This compliant solution performs the `recv()` call when the lock has not been acquired. The blocking behavior consequently affects only the thread that called the blocking function.
``` c
void thread_foo(void *ptr) {
  uint32_t num;
  int result;
  int sock;
  /* sock is a connected TCP socket */
  if ((result = recv(sock, (void *)&num, sizeof(uint32_t), 0)) < 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle Error */
  }
  /* ... */
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle Error */
  }
}
```
## Compliant Solution (Use a Nonblocking Call)
This compliant solution performs the `recv()` call with the parameter `o_nonblock`, which causes the call to fail if no messages are available on the socket:
``` c
void thread_foo(void *ptr) {
  uint32_t num;
  int result;
  /* sock is a connected TCP socket */
  if ((result = recv(sock, (void *)&num, sizeof(uint32_t), O_NONBLOCK)) < 0) {
    /* Handle Error */
  }
  if ((result = pthread_mutex_lock(&mutex)) != 0) {
    /* Handle Error */
  }
  /* ... */
  if ((result = pthread_mutex_unlock(&mutex)) != 0) {
    /* Handle Error */
  }
}
```
## Exceptions
**POS52-C-EX1:** A thread may block while holding one or more locks and waiting to acquire another lock. When acquiring multiple locks, the order of locking must avoid deadlock, as specified in [CON35-C. Avoid deadlock by locking in a predefined order](CON35-C_%20Avoid%20deadlock%20by%20locking%20in%20a%20predefined%20order).
## Risk Assessment
Blocking or lengthy operations performed within synchronized regions could result in a deadlocked or an unresponsive system.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS52-C | Low | Probable | High | P2 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | CONCURRENCY.STARVE.BLOCKING | Blocking in Critical Section |
| Helix QAC | 2024.4 | DF4966, DF4967 |  |
| Klocwork | 2024.4 | CONC.SLEEP |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS52-a | Do not use blocking functions while holding a lock |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS52-C | Checks for blocking operation while holding lock (rule fully covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | LCK09-J. Do not perform operations that can block while holding a lock | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-557 | 2017-07-10: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-557 and POS52-C
CWE-557 = Union( POS52-C, list) where list =
-   Concurrency issues besides blocking while holding a POSIX lock
## Bibliography

|  |  |
| ----|----|
| [Barney 2010] | POSIX Threads Programming |
| [Open Group] | pthread_cancel()recv() |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152018)[](../c/Rule%2050_%20POSIX%20_POS_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151984)
## Comments:

|  |
| ----|
| This compliant solution performs the;recv() call with the parameter o_nonblockHi, I have a question about the compliant solution, according to the Linux programmer's manual of function recv(), it seems we should call recv() with parameter MSG_DONWAIT. They are a little different. The flags argument:

```
MSG_DONTWAIT (since Linux 2.2)
      Enables nonblocking operation; if the operation would block,
      the call fails with the error EAGAIN or EWOULDBLOCK.  This
      provides similar behavior to setting the O_NONBLOCK flag (via
      the fcntl(2) F_SETFL operation)
```
And I have done a simple test, function recv() with parameter O_NONBLOCK still waits to get a request from the server. And with MSG_DONWAIT, no blocking call happens.
And besides, should we consider about **spinlock** in this rule?
Could you please help to clarify this? Many thanks!
![](images/icons/contenttypes/comment_16.png) Posted by zhaohui at Jun 16, 2020 00:01
\| \|
It seems that O_NONBLOCK and MSG_DONTWAIT have two differences:
-   O_NONBLOCK is in the;[POSIX standard](https://pubs.opengroup.org/onlinepubs/9699919799/toc.htm), while MSG_DONTWAIT is Linux-specific.
-   O_NONBLOCK is set once for any open streams or socket; MSG_DONTWAIT can differ for each recv() call.
We generally do not recommend using spin locks because they waste resources asking if a lock is free. It is general for the locking mechanism to provide its own notification when the lock is finally unlocked.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 16, 2020 09:47
\| \|
Why is this a rule if [CON05-C. Do not perform operations that can block while holding a lock](CON05-C_%20Do%20not%20perform%20operations%20that%20can%20block%20while%20holding%20a%20lock) is only a recommendation? Also, aren't there a lot of times when you need to do a blocking operation under a lock?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 16:57
\| \|
Mainly because this rule predates CON05-C. There is an analogous rule (not recommendation) for Java ([LCK09-J. Do not perform operations that can block while holding a lock](https://wiki.sei.cmu.edu/confluence/display/java/LCK09-J.+Do+not+perform+operations+that+can+block+while+holding+a+lock)). It seems [Aaron Ballman](https://wiki.sei.cmu.edu/confluence/display/~aballman) made CON05-C into a recommendation (from a rule)...see his comment there:<https://wiki.sei.cmu.edu/confluence/display/c/CON05-C.+Do+not+perform+operations+that+can+block+while+holding+a+lock?focusedCommentId=87152625#comment-87152625>
He may have other reasons for doing so, but his stated reason is that ISO C does not provide standard non-locking operations for files. But POSIX does. So that reason does not justify demoting this rule to a recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 29, 2020 08:24
\| \|
I was thinking more along the lines of the last sentence of his comment: "Or blocking other threads from accessing a resource is desirable." That's still completely true even with POSIX.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 29, 2020 09:56
\| \|
It was a long while ago when I demoted this, but yes, it's the fact that we have to judge programmer intent that caused me to downgrade to a recommendation more than anything.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 29, 2020 10:00
\| \|
Can either of you suggest a case where it is desirable to acquire some kind of thread lock and then block? While there may be instances, I'm hard-pressed to believe there are enough of a pattern of cases to demote this to a rec. If there are only 1-2 such cases, it would be better to keep this as a rule, and flag the cases as exceptions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 29, 2020 14:49
\| \|
Off the top of my head, a common implementation pattern for servers using BSD sockets is to spawn off a new thread per connection and then use blocking socket operations to communicate over that socket. Depending on the purpose to the server, you may wish to hold a lock even though you're using blocking operations, and it's not harmful (though I'd guess it probably has terrible performance for a server) because the socket will stop blocking eventually (i.e., eventually you'll hit a network layer timeout that closes the socket connection which causes the socket to stop blocking). (Literally, the situation in the NCCE for this rule.)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 29, 2020 14:59
\| \|
Spawning a thread to recv() socket data is a fine thing. But neither you nor the NCCE you cite't go into design or \*why\* you might want to block while holding the lock.
The Java rule LCK09-J has two exceptions which might justify this rule if we add them.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 29, 2020 15:19
\| \|
Protecting access to a shared resource that is being recv'ed into. For instance, say each socket is contributing some bytes to a single file (e.g., you have different sockets downloading different parts of the same file, and the receiving end is writing those contents out).
I suspect all of the examples are likely to feel contrived because the reasons why you may wish to lock access to a resource while doing;**anything** are pretty varied.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 30, 2020 12:40
\|
