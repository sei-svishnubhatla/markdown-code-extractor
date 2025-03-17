Using the `vfork` function introduces many portability and security issues. There are many cases in which [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and implementation-specific behavior can occur, leading to a denial-of-service [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
According to the `vfork` man page,
> The `vfork()` function has the same effect as `fork()`, except that the behavior is undefined if the process created by `vfork()` either modifies any data other than a variable of type `pid_t` used to store the return value from `vfork()`, or returns from the function in which `vfork()` was called, or calls any other function before successfully calling `_exit()` or one of the `exec` family of functions.

Furthermore, older versions of Linux are vulnerable to a race condition, occurring when a privileged process calls vfork(), and then the child process lowers its privileges and calls execve(). The child process is executed with the unprivileged user's UID before it calls execve().
Because of the implementation of the `vfork()` function, the parent process is suspended while the child process executes. If a user sends a signal to the child process, delaying its execution, the parent process (which is privileged) is also blocked. This means that an unprivileged process can cause a privileged process to halt, which is a privilege inversion resulting in a denial of service.
This code example shows how difficult it is to use `vfork()` without triggering undefined behavior. The lowering of privileges in this case requires a call to `setuid()`, the behavior of which is undefined because it occurs between the `vfork()` and the `execve()`.
``` java
pid_t pid = vfork();
if (pid == 0) /* child */ {
  setuid(unprivileged_user);  /* undefined behavior */
  /*
   * Window of vulnerability to privilege inversion on
   * older versions of Linux
   */
  if (execve(filename, NULL, NULL) == -1) {
    /* Handle error */
  }
  /*
   * In normal operations, execve() might fail; if it does,
   * vfork() behavior is undefined.
   */
  _exit(1);  /* in case execve() fails */
}
```
Use `fork()` instead of `vfork()` in all circumstances.
## Noncompliant Code Example
This noncompliant code example calls `vfork()` and then `execve()`. As previously discussed, a `vfork()`/`execve()` pair contains an inherent race window on some [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation).
``` c
char *filename = /* something */;
pid_t pid = vfork();
 if (pid == 0 )  /* child */ {
   if (execve(filename, NULL, NULL) == -1) {
     /* Handle error */
   }
   _exit(1);  /* in case execve() fails */
}
```
## Compliant Solution
This compliant solution replaces the call to `vfork()` with a call to `fork()`, which does not contain a race condition, and eliminates the denial-of-service vulnerability:
``` c
char *filename = /* something */;
pid_t pid = fork();
if (pid == 0) /* child */ {
  if (execve(filename, NULL, NULL) == -1) {
    /* Handle error */
  }
  _exit(1);  /* in case execve() fails */
}
```
## Risk Assessment
Using the `vfork` function can result in a denial-of-service vulnerability.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS33-C | low | probable | low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS33 |  |
| CodeSonar | 8.3p0 | BADFUNC.VFORK | Use of vfork |
| Coverity | 2017.07 | DONTCALL | Implemented |
| LDRA tool suite | 9.7.1 | 44 S | Fully implemented |
| Compass/ROSE |  |  |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS33-a | Avoid using the 'vfork()' function |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS33-C | Checks for use of obsolete standard function (rule fully covered) |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 5023 | Fully implemented |
| SonarQube C/C++ Plugin | 3.11 | ObsoletePosixFunction |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-242, Use of inherently dangerous function | 2017-07-05: CERT: Rule subset of CWE |
| MITRE CWE | CWE-676 | Prior to 2018-01-12:CERT:Relationship Unspecified |
| CWE 3.1 | CWE-676, Use of Potentially Dangerous Function | 2018-10-18:CERT:None |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-242 and POS33-C
CWE-242 = Union( POS33-C, list) where list =
-   Use of dangerous functions besides vfork
### CWE-676 and POS33-C
INTERSECTION(CWE-676, POS33-C) = ∅
## Bibliography

|  |  |
| ----|----|
| [Wheeler 2003] | Section 8.6 |

------------------------------------------------------------------------
[](../c/POS30-C_%20Use%20the%20readlink__%20function%20properly) [](../c/Rule%2050_%20POSIX%20_POS_) [](../c/POS34-C_%20Do%20not%20call%20putenv__%20with%20a%20pointer%20to%20an%20automatic%20variable%20as%20the%20argument)
## Comments:

|  |
| ----|
| Should have a "POSIX" label.
vfork was an invention of BSD, with the claim that fork was too expensive for simple spawn (fork/exec), since it copied the whole program only to overlay it with a new one, and the BSD developers claimed that the obvious solution on the VAX, use;"copy-on-write" tags in the page table, didn't work right.  (However, AT&T UNIX didn't have a problem with that.)  Modern systems have figured out how to fork efficiently.
Plan 9 from Bell Labs has a more general rfork facility which provides considerable control over how much of the environment is shared and how much is copied.
                                        Posted by dagwyn at Apr 18, 2008 15:29
                                     |
| This recommendation is already in the POSIX section, so the POSIX label is implicit.
                                        Posted by rcs_mgr at Apr 19, 2008 14:18
                                     |
| The problem that remains with fork (even with COW) is that the page tables need to be cloned and this can result in 100's of MB's of memory being required to duplicate a process with a large VM layout. Therefore fork continues to suffer for large processes from page table copying latency and duplicate page table memory load. You can avoid all of this with vfork, but you have to be very careful how you use it.
                                        Posted by codonell at Nov 09, 2015 19:39
                                     |
| Is there actually a problem with vfork() itself? Why isn't this rule "don't call setuid() (or any other arbitrary function) between vfork() and execve()"? Why does all of vfork() need to be banned?
                                        Posted by jcsible at Jul 07, 2020 16:18
                                     |
| "In normal operations, execve() might fail; if it does, vfork() behavior is undefined." I don't see how, since it's followed by a call to _exit().
                                        Posted by jcsible at Jul 07, 2020 16:21
                                     |
| Actually, vfork() is not in the POSIX standard. So we could nix this rule claiming it is 'out of scope'.The [Wheeler 2002] reference provides most of the background for this rule.
                                        Posted by svoboda at Jul 09, 2020 09:19
                                     |
| Actually, vfork() is not in the POSIX standard. So we could nix this rule claiming it is 'out of scope'.I'm in favor of that.The [Wheeler 2002] reference provides most of the background for this rule.I'm inclined to disagree with that reference. It looks like it boils down to two points: a bug in the Linux kernel, and it being hard to use correctly. The bug in the Linux kernel has been fixed for twenty years now, so I can't see any argument that it's still relevant. And in general, I don't like the argument "hard to use correctly == must never be used at all".
                                        Posted by jcsible at Jul 09, 2020 15:37
                                     |
| For the CERT rules, we focus on the C standard, with a distant focus on how C programs behave on major implementations. While we may reference famous bugs or design warts on various platforms, we don't like to base rules on them. Because the bugs will get fixed, and new bugs will arise later. And there are public bug databases and reporting mechanisms for the biggest platforms. The CERT standard shouldn't just be "a better Bugzilla".There is probably a more authoritative link, but right now I am relying on this page for vfork():https://man7.org/linux/man-pages/man2/vfork.2.htmlWhile it does not mention any historical bugs in Linux, it does hint at the difficulties in using vfork() in general. But more importantly, it suggests that the performance improvements that vfork() has over fork() are historical and no longer relevant. And it suggests that, on some platforms at least, vfork() would be deprecated. So it is probably worthwhile for us to still say "don't use vfork()", although more due to its deprecation than due to historical bugs. So I'd prefer to keep this rule but change the intro to focus on deprecation. The NCCE/CS are still good though.
                                        Posted by svoboda at Jul 10, 2020 10:56
                                     |
| But more importantly, it suggests that the performance improvements that vfork() has over fork() are historical and no longer relevant.This isn't quite true, as Carlos O'Donell commented above. Also, as another point against its deprecation, posix_spawn() is usually implemented in terms of it (or its clone() equivalent).
                                        Posted by jcsible at Jul 10, 2020 11:17
                                     |
| OK, I have voided this rule. It is still a useful subject, but out-of-scope of strict POSIX, and it clearly needs a lot of work detailing the (few) conditions when vfork() would be acceptable to use.
                                        Posted by svoboda at Jul 10, 2020 11:58
                                     |

