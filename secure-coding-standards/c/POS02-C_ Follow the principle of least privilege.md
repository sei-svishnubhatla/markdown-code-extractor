The principle of least privilege states that every program and every user of the system should operate using the least set of privileges necessary to complete the job \[[Saltzer 1974](AA.-Bibliography_87152170.html#AA.Bibliography-Saltzer74), [Saltzer 1975](AA.-Bibliography_87152170.html#AA.Bibliography-Saltzer75)\]. The Build Security In website \[[DHS 2006](AA.-Bibliography_87152170.html#AA.Bibliography-DHS06)\] provides additional definitions of this principle. Executing with minimal privileges mitigates against exploitation in case a vulnerability is discovered in the code.
## Noncompliant Code Example
Privileged operations are often required in a program, though the program might not need to retain the special privileges. For instance, a network program may require superuser privileges to capture raw network packets but may not require the same set of privileges for carrying out other tasks such as packet analysis. Dropping or elevating privileges alternately according to program requirements is a good design strategy. Moreover, assigning only the required privileges limits the window of exposure for any privilege escalation exploit to succeed.
Consider a custom service that must bind to a well-known port (below 1024). To prevent malicious entities from hijacking client connections, the kernel imposes a condition so that only the superuser can use the `bind()` system call to bind to these ports.
This noncompliant code example is configured as setuid-superuser. It calls `bind()` and later forks out a child to perform the bookkeeping tasks. The program continues to run with superuser privileges even after the `bind()` operation is completed.
``` c
int establish(void) {
  struct sockaddr_in sa; /* listening socket's address */
  int s; /* listening socket */
  /*  Fill up the structure with address and port number  */
  sa.sin_port = htons(portnum);
  /*  Other system calls like socket()  */
  if (bind(s, (struct sockaddr *)&sa,
        sizeof(struct sockaddr_in)) < 0) {
    /* Perform cleanup */
  }
  /* Return */
}
int main(void) {
  int s = establish();
  /*  Block with accept() until a client connects  */
  switch (fork()) {
    case -1 :  /* Error, clean up and quit */
    case  0 :  /* This is the child, handle the client */
    default :  /* This is the parent, continue blocking */
  }
  return 0;
}
```
If a vulnerability is exploited in the main body of the program that allows an attacker to execute arbitrary code, this malicious code will run with elevated privileges.
## Compliant Solution
The program must follow the principle of least privilege while carefully separating the binding and bookkeeping tasks. To minimize the chance of a flaw in the program from compromising the superuser-level account, it should drop superuser privileges as soon as the privileged operations are completed. In the following code, privileges are permanently dropped as soon as the `bind()` operation is carried out. The code also ensures privileges may not be regained after being permanently dropped, as in [POS37-C. Ensure that privilege relinquishment is successful](POS37-C_%20Ensure%20that%20privilege%20relinquishment%20is%20successful).
``` c
/*  Code with elevated privileges  */
int establish(void) {
  struct sockaddr_in sa; /* listening socket's address */
  int s; /* listening socket */
  /* Fill up the structure with address and port number */
  sa.sin_port = htons(portnum);
  /* Other system calls like socket() */
  if (bind(s, (struct sockaddr *)&sa,
        sizeof(struct sockaddr_in)) < 0) {
    /* Perform cleanup */
  }
  /* Return */
}
int main(void) {
  int s = establish();
  /* Drop privileges permanently */
  if (setuid(getuid()) == -1) {
     /*  Handle the error  */
  }
  if (setuid(0) != -1) {
    /* Privileges can be restored, handle error */
  }
  /* Block with accept() until a client connects */
  switch (fork()) {
    case -1: /* Error, clean up and quit */
    case  0: /* Close all open file descriptors
              * This is the child, handle the client
              */
    default: /* This is the parent, continue blocking */
  }
  return 0;
}
```
## Risk Assessment
Failure to follow the principle of least privilege may allow exploits to execute with elevated privileges.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS02-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Klocwork | 2024.4 | SV.BRM.HKEY_LOCAL_MACHINESV.USAGERULES.PERMISSIONS |  |

### Related Vulnerabilities
[CVE-2009-2031](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-2031) results from a violation of this recommendation. OpenSolaris, in smbfs snv_84 through snv_110, sets permissions based on mount-point options and not actual user information (obtained from the `getuid()` and `getgid()` functions). An attacker can exploit this to achieve higher permissions. Also, in a certain initialization mode, the code grants read, write, and execute permissions to users other than the owner, which can be exploited to make files world readable \[[xorl 2009](http://xorl.wordpress.com/2009/06/14/opensolaris-cifssmb-invalid-file-flags/)\].
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabilit) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS02-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772 | Adherence to Least Privilege [XYN] |
| MITRE CWE | CWE-250, Execution with unnecessary privilegesCWE-272, Least privilege violation |

## Bibliography

|  |  |
| ----|----|
| [DHS 2006] | Least Privilege  |
| [Saltzer 1974] |  |
| [Saltzer 1975] |  |
| [Wheeler 2003] | Section 7.4, "Minimize Privileges" |
| [xorl 2009] | "OpenSolaris CIFS/SMB Invalid File Flags" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152372) [](../c/Rec_%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152062)
## Comments:

|  |
| ----|
| Wouldn't there be a more secure & portable way to drop privileges than;setuid()? We probably should be pushing setresuid() or at least seteuid() here.
                                        Posted by svoboda at Dec 06, 2012 14:34
                                     |
| 
                                        Posted by kina at Dec 06, 2012 14:48
                                     |
| If you want to drop privileges permanently,;setuid() is the most portable way; setresuid() can do it but is less portable, and seteuid() doesn't do what's required because it allows privileges to be regained.  See POS37.
                                        Posted by geoffclare at Dec 07, 2012 09:47
                                     |
| I don't think the principle of least privilege is the best option in all cases. A software that does not mix privileges is harder to exploit than the one that tries to gain and drop privileges. For example, if all the components and sources of input require administrative access to execute and there is very little network exposure, then it may be better to just run as a superuser to limit the possibility of local privilege escalation. Such software does not usually require any user input but may depend on (untrusted) environment variables, temporary / shared files etc but superuser permissions are required in most cases to tamper with these.Any counter arguments?;
                                        Posted by dmohindr at Aug 08, 2014 03:25
                                     |
| Yes, there is a tradeoff between keeping the program simple and maximizing security. That's why this is a recommendation, not a rule.It may be better to redesign your program so that the actions that require privs can all be done near the beginning of the program...or near the end. Which leaves a large middle where privs can be dropped, and maybe regained later. But this is not always possible.
                                        Posted by svoboda at Aug 08, 2014 10:25
                                     |
| The compliant solution could be improved further on Linux. Instead of starting with full root privileges, it could start with just the CAP_NET_BIND_SERVICE capability.
                                        Posted by jcsible at Jun 30, 2020 13:00
                                     |
| As I said in an earlier comment, there is a trade-off between maintainability / portability and security. You can use CAP_NET_BIND_SERVICE but that constrains your code to Linux.I would welcome a Linux-specific compliant solution with this feature.
                                        Posted by svoboda at Aug 19, 2020 08:11
                                     |
| Indeed. One concrete example of this is a privileged parent process that spawns unprivileged children. It's really common to do this incorrectly in such a way that a race condition temporarily gives the unprivileged user access to the parent process's address space.
                                        Posted by jcsible at Aug 19, 2020 10:10
                                     |

