Developers should take steps to prevent sensitive information such as passwords, cryptographic keys, and other secrets from being inadvertently leaked. Preventive measures include attempting to keep such data from being written to disk.
Two common mechanisms by which data is inadvertently written to disk are *swapping* and *core dumps*.
Many general-purpose operating systems implement a virtual-memory-management technique called *paging* (also called *swapping*) to transfer pages between main memory and an auxiliary store, such as a disk drive. This feature is typically implemented as a task running in the kernel of the operating system, and its operation is invisible to the running program.
A core dump is the recorded state of process memory written to disk for later examination by a debugger. Core dumps are typically generated when a program has [terminated abnormally](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination), either through an error resulting in a crash or by receiving a signal that causes such a termination.
The POSIX standard system call for controlling resource limits, `setrlimit()`, can be used to disable the creation of core dumps, which prevents an attacker with the ability to halt the program from gaining access to sensitive data that might be contained in the dump.
## Noncompliant Code Example
In this noncompliant code example, sensitive information is supposedly stored in the dynamically allocated buffer, `secret`, which is processed and eventually cleared by a call to `memset_s()`. The memory page containing `secret` can be swapped out to disk. If the program crashes before the call to `memset_s()` completes, the information stored in `secret` may be stored in the core dump.
``` c
char *secret;
secret = (char *)malloc(size+1);
if (!secret) {
  /* Handle error */
}
/* Perform operations using secret... */
memset_s(secret, '\0', size+1);
free(secret);
secret = NULL;
```
## Compliant Solution (POSIX)
To prevent the information from being written to a core dump, the size of core dumps that the program will generate should be set to 0 using `setrlimit()`:
``` c
#include <sys/resource.h>
/* ... */
struct rlimit limit;
limit.rlim_cur = 0;
limit.rlim_max = 0;
if (setrlimit(RLIMIT_CORE, &limit) != 0) {
    /* Handle error */
}
char *secret;
secret = (char *)malloc(size+1);
if (!secret) {
  /* Handle error */
}
/* Perform operations using secret... */
memset_s(secret, '\0', size+1);
free(secret);
secret = NULL;
```
## Compliant Solution (Privileged Process, POSIX)
The added security from using `mlock()` is limited. (See the sidebar by Nick Stoughton.)
Processes with elevated privileges can disable paging by locking memory in place using the POSIX [`mlock()`](http://pubs.opengroup.org/onlinepubs/9699919799/) function \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. Disabling paging ensures that memory is never copied to the hard drive, where it may be retained indefinitely in nonvolatile storage.
This compliant solution not only disables the creation of core files but also ensures that the buffer is not swapped to hard disk:
``` c
#include <sys/resource.h>
/* ... */
struct rlimit limit;
limit.rlim_cur = 0;
limit.rlim_max = 0;
if (setrlimit(RLIMIT_CORE, &limit) != 0) {
    /* Handle error */
}
long pagesize = sysconf(_SC_PAGESIZE);
if (pagesize == -1) {
  /* Handle error */
}
char *secret_buf;
char *secret;
secret_buf = (char *)malloc(size+1+pagesize);
if (!secret_buf) {
  /* Handle error */
}
/* mlock() may require that address be a multiple of PAGESIZE */
secret = (char *)((((intptr_t)secret_buf + pagesize - 1) / pagesize) * pagesize);
if (mlock(secret, size+1) != 0) {
    /* Handle error */
}
/* Perform operations using secret... */
if (munlock(secret, size+1) != 0) {
    /* Handle error */
}
secret = NULL;
memset_s(secret_buf, '\0', size+1+pagesize);
free(secret_buf);
secret_buf = NULL;
```
## Compliant Solution (Windows)
Windows processes can disable paging by locking memory in place using `VirtualLock()`\[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-AA.CReferences-MSDN)\]:
``` c
char *secret;
secret = (char *)VirtualAlloc(0, size + 1, MEM_RESERVE | MEM_COMMIT, PAGE_READWRITE);
if (!secret) {
  /* Handle error */
}
if (!VirtualLock(secret, size+1)) {
    /* Handle error */
}
/* Perform operations using secret... */
SecureZeroMemory(secret, size + 1);
VirtualUnlock(secret, size + 1);
VirtualFree(secret, 0, MEM_RELEASE);
secret = NULL;
```
Note that locking pages of memory on Windows may fail because the operating system allows the process to lock only a small number of pages. If an application requires additional locked pages, the [SetProcessWorkingSetSize()](http://msdn.microsoft.com/en-us/library/windows/desktop/ms686234(v=vs.85).aspx) API can be used to increase the application's minimum working set size. Locking pages has severe performance consequences and should be used sparingly.
## Risk Assessment
Writing sensitive data to disk preserves it for future retrieval by an attacker, who may even be able to bypass the access restrictions of the operating system by using a disk maintenance program.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM06-C | Medium | Unlikely | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM06-C | Checks for sensitive data printed out (rec. partially covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM06-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM06-CPP. Ensure that sensitive data is not written out to disk |
| ISO/IEC TR 24772:2013 | Memory Locking [XZX] |
| MITRE CWE | CWE-591, Sensitive data storage in improperly locked memoryCWE-528, Information leak through core dump files |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interface, mlockXSH, System Interface, setrlimit |
| [Wheeler 2003] | Section 7.14Section 11.4 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152078) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](../c/MEM07-C_%20Ensure%20that%20the%20arguments%20to%20calloc__,%20when%20multiplied,%20do%20not%20wrap)
## Comments:

|  |
| ----|
| man ulimit says:
"Warning: this routine is obsolete. Use getrlimit(2), setrlimit(2), and sysconf(3) instead"
;So I'm removing all mention of it.
                                        Posted by avolkovi at Mar 18, 2008 10:03
                                     |
| The way mlock() is used here is not portable.; POSIX says "The implementation may require that addr be a multiple of {PAGESIZE}."  So on some systems the mlock() call will fail with EINVAL.
                                        Posted by geoffclare at Apr 04, 2008 12:37
                                     |
| The mlock() API makes no guarantee of preventing data from being written to a swap file or other secondary storage. It is also an optional API for POSIX conformance.
In security related applications, there may be sensitive data stored in various data structures, particularly while the program is running. There are many attack vectors that try to gain access to that data; looking at the swap file is indeed one of these attack vectors. In my experience, however, it is not one of the first! Many systems provide access to the physical and virtual memory associated with a system/process (e.g. /dev/mem, /proc/pid/mem, etc.). If a process is able to gain sufficient privilege to read a swap file (the original attack vector), it is more likely to have success with one of these alternatives anyway. Attaching a debugger to the process and reading its memory through this is even more common. Again, any attacking process that would be likely to succeed in reading the swap file is more likely to succeed by this means.
Consequently, security related applications try to ensure that such sensitive data is kept encrypted (and often obfuscated) wherever and whenever possible. Simply saying sensitive data shouldn't be in the swap file really doesn't solve the vulnerability. Add to that the fact that when you suspend or hibernate a laptop (or other computer), memory is frequently written to disk anyway, beyond the scope of memory locking. Add to this the overall system (i.e. the entirety of the platform, and not just the sensitive application) performance penalty paid for memory locking, coupled with the attendant need for elevated privileges to achieve it, and it is clear that mlock() solves such a small part of this problem as to be irrelevant.
However, memory locking does solve a major safety issue: predictable access times to critical data structures.
                                        Posted by nick at Apr 11, 2008 12:25
                                     |
| There really is no solution for this using current hardware, other than using a secure operating system.
                                        Posted by dagwyn at Apr 16, 2008 22:15
                                     |
| Even the compliant example likely leaves sensitive data around if the file is buffered.
                                        Posted by sgreen at Sep 02, 2009 08:11
                                     |
| This is a good point.  To prevent swapping out the stdio buffer, the code could use setvbuf() to designate a buffer to be used, and mlock() that buffer, but it would be simpler just to avoid using stdio.  The introductory text should talk about this issue, and should probably recommend avoiding the use of stdio functions to read and write sensitive data (with setvbuf()+mlock() mentioned as an alternative).
I have also noticed that all but the first example have a coding error where sizeof(secret) is used as if it is the size of the buffer, but secret is a pointer variable not an array.  They should be changed to allocate the buffer as in the first example and use a size variable instead of sizeof(secret).  To fix the mlock() problem I commented on earlier, the example that uses mlock() should allocate size+sysconf(_SC_PAGESIZE) bytes so that it can arrange for secret to be a multiple of PAGESIZE.
                                        Posted by geoffclare at Sep 03, 2009 05:05
                                     |
| Nick, I've adopted your suggestions wrt mlock, and size.
As for the problem of input being buffered, I weaseled around that by removing the fgets() call. This leaves unresolved the problem of how to get sensitive info from the user, such as a password. And your points about right and wrong ways of doing this are quite worthy. I just think they should probably go in a separate rule by themselves.
Heck, we could probably make a whole new section about how to handle sensitive data if we had the time. Ultimately I suspect it will down to Doug Gwynn's comment that the problem is intractible, except on a secure operating system.
                                        Posted by svoboda at Sep 03, 2009 16:17
                                     |
| I've updated the CS for Windows because it was previously mixing malloc and VirtualLock (which is dangerous to do).; Now it is using VirtualAlloc and friends.  Additionally, you do not require elevated privileges on Windows to lock pages in memory, so I removed that wording. However, I'm not really comfortable with this recommendation because I don't believe it's tenable without help from the operating system.
                                        Posted by aballman at Aug 15, 2013 15:44
                                     |
| Should the CS for this recommendation include the countermeasures from MEM03-C. Clear sensitive information stored in reusable resources since they make use of malloc/free for storing the secret? It is outside the scope of this particular recommendation, but may be good just for compliance purposes.
                                        Posted by jloo at Jan 23, 2014 14:46
                                     |
| Yes, I've added code to zero out sensitive memory in all CS's.
                                        Posted by svoboda at Jan 24, 2014 15:07
                                     |
| Isn't it good to call;memset_s() before calling munlock() to be fully complaint?
                                        Posted by jvvprasad78 at Feb 21, 2020 11:19
                                     |
| Yes it is a good idea.; Since munlock() is not an ISO standard function, it is oudside the scope of this recommendation (but still a good idea)
                                        Posted by svoboda at Feb 21, 2020 14:06
                                     |
| Disabling core dumps altogether is using a bazooka to kill a fly. It will unnecessarily make debugging crashes much harder. On Linux, you should instead use madvise with MADV_DONTDUMP to suppress just the sensitive data from being included in the dump.
                                        Posted by jcsible at Jun 30, 2020 12:04
                                     |

