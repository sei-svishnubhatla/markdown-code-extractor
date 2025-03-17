The POSIX `setuid()` function has complex semantics and platform-specific behavior \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\].
> If the process has appropriate privileges, `setuid()` shall set the real user ID, effective user ID, and the saved set-user-ID of the calling process to `uid`.
>
> If the process does not have appropriate privileges, but `uid` is equal to the real user ID or the saved set-user-ID, `setuid()` shall set the effective user ID to `uid`; the real user ID and saved set-user-ID shall remain unchanged.

The meaning of "appropriate privileges" varies from platform to platform. For example, on Solaris, appropriate privileges for `setuid()` means that the `PRIV_PROC_SETID` privilege is in the effective privilege set of the process. On BSD, it means that the effective user ID (EUID) is zero (that is, the process is running as root) or that `uid=geteuid()`. On Linux, it means that the process has `CAP_SETUID` capability and that `setuid(geteuid())` will fail if the EUID is not equal to 0, the real user ID (RUID), or the saved set-user ID (SSUID).
Because of this complex behavior, desired privilege drops sometimes may fail. For example, the range of Linux Kernel versions (2.2.0–2.2.15) is vulnerable to an insufficient privilege attack wherein `setuid(getuid()` did not drop privileges as expected when the capability bits were set to zero. As a precautionary measure, subtle behavior and error conditions for the targeted implementation must be carefully noted.
## Noncompliant Code Example
This noncompliant code example compiles cleanly on most POSIX systems, but no explicit checks are made to ensure that privilege relinquishment has succeeded. This may be dangerous depending on the sequence of the preceding privilege changes.
``` c
/* Code intended to run with elevated privileges */
/* Temporarily drop privileges */
if (seteuid(getuid()) != 0) {
  /* Handle error */
}
/* Code intended to run with lower privileges */
if (need_more_privileges) {
  /* Restore privileges */
  if (seteuid(0) != 0) {
    /* Handle error */
  }
  /* Code intended to run with elevated privileges */
}
/* ... */
/* Permanently drop privileges */
if (setuid(getuid()) != 0) {
  /* Handle error */
}
/*
 * Code intended to run with lower privileges,
 * but if privilege relinquishment failed,
 * attacker can regain elevated privileges!
 */
```
If the program is run as a setuid root program, over time, the state of the UIDs might look like the following:

| Description | Code | EUID | RUID | SSUID |
| ----|----|----|----|----|
| Program startup |  | 0 | User | 0 |
| Temporary drop | seteuid(getuid()) | User | User | 0 |
| Restore | seteuid(0) | 0 | User | 0 |
| Permanent drop | setuid(getuid()) | User | User | User |
| Restore (attacker) | setuid(0) (fails) | User | User | User |

If the program fails to restore privileges, it will be unable to permanently drop them later:

| Description | Code | EUID | RUID | SSUID |
| ----|----|----|----|----|
| program startup |  | 0 | User | 0 |
| Temporary drop | seteuid(getuid()) | User | User | 0 |
| Restore | seteuid(0) | User | User | 0 |
| Permanent drop | setuid(getuid()) | User | User | 0 |
| Restore (attacker) | setuid(0) | 0 | 0 | 0 |

## Compliant Solution
This compliant solution was implemented in sendmail, a popular mail transfer agent, to determine if superuser privileges were successfully dropped \[[Wheeler 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Wheeler03)\]. If the `setuid()` call succeeds after (supposedly) dropping privileges permanently, then the privileges were not dropped as intended.
``` c
/* Code intended to run with elevated privileges   */
/* Temporarily drop privileges */
if (seteuid(getuid()) != 0) {
  /* Handle error */
}
/* Code intended to run with lower privileges */
if (need_more_privileges) {
  /* Restore Privileges */
  if (seteuid(0) != 0) {
    /* Handle error */
  }
  /* Code intended to run with elevated privileges */
}
/* ... */
/* Permanently drop privileges */
if (setuid(getuid()) != 0) {
  /* Handle error */
}
if (setuid(0) != -1) {
  /* Privileges can be restored, handle error */
}
/*
 * Code intended to run with lower privileges;
 * attacker cannot regain elevated privileges
 */
```
## Compliant Solution
A better solution is to ensure that proper privileges exist before attempting to perform a permanent drop:
``` c
/* Store the privileged ID for later verification */
uid_t privid = geteuid();
/* Code intended to run with elevated privileges   */
/* Temporarily drop privileges */
if (seteuid(getuid()) != 0) {
  /* Handle error */
}
/* Code intended to run with lower privileges  */
if (need_more_privileges) {
  /* Restore Privileges */
  if (seteuid(privid) != 0) {
    /* Handle error */
  }
  /* Code intended to run with elevated privileges   */
}
/* ... */
/* Restore privileges if needed */
if (geteuid() != privid) {
  if (seteuid(privid) != 0) {
    /* Handle error */
  }
}
/* Permanently drop privileges */
if (setuid(getuid()) != 0) {
  /* Handle error */
}
if (setuid(0) != -1) {
  /* Privileges can be restored, handle error */
}
/*
 * Code intended to run with lower privileges;
 * attacker cannot regain elevated privileges
 */
```
## Supplementary Group IDs
A process may have a number of supplementary group IDs, in addition to its effective group ID, and the supplementary groups can allow privileged access to files. The `getgroups()` function returns an array that contains the supplementary group IDs and can also contain the effective group ID. The `setgroups()` function can set the supplementary group IDs and can also set the effective group ID on some systems. Using `setgroups()` usually requires privileges. Although POSIX defines the `getgroups()` function, it does not define `setgroups()`.
Under normal circumstances, `setuid()` and related calls do not alter the supplementary group IDs. However, a setuid-root program can alter its supplementary group IDs and then relinquish root privileges, in which case, it maintains the supplementary group IDs but lacks the privilege necessary to relinquish them. Consequently, it is recommended that a program immediately relinquish supplementary group IDs before relinquishing root privileges.
[POS36-C. Observe correct revocation order while relinquishing privileges](POS36-C_%20Observe%20correct%20revocation%20order%20while%20relinquishing%20privileges) discusses how to drop supplementary group IDs. To ensure that supplementary group IDs are indeed relinquished, you can use the following `eql_sups` function:
``` c
/* Returns nonzero if the two group lists are equivalent (taking into
   account that the lists may differ wrt the egid */
int eql_sups(const int cursups_size, const gid_t* const cursups_list,
         const int targetsups_size, const gid_t* const targetsups_list) {
  int i;
  int j;
  const int n = targetsups_size;
  const int diff = cursups_size - targetsups_size;
  const gid_t egid = getegid();
  if (diff > 1 || diff < 0 ) {
    return 0;
  }
  for (i=0, j=0; i < n; i++, j++) {
    if (cursups_list[j] != targetsups_list[i]) {
      if (cursups_list[j] == egid) {
    i--; /* skipping j */
      } else {
    return 0;
      }
    }
  }
  /* If reached here, we're sure i==targetsups_size. Now, either
     j==cursups_size (skipped the egid or it wasn't there), or we didn't
     get to the egid yet because it's the last entry in cursups */
  return j == cursups_size ||
    (j+1 == cursups_size && cursups_list[j] == egid);
}
```
## System-Specific Capabilities
Many systems have nonportable privilege capabilities that, if unchecked, can yield privilege escalation vulnerabilities. The following section describes one such capability.
### File System Access Privileges (Linux)
Processes on Linux have two additional values called `fsuid` and `fsgid`. These values indicate the privileges used when accessing files on the file system. They normally shadow the effective user ID and effective group ID, but the `setfsuid()` and `setfsgid()` functions allow them to be changed. Because changes to the `euid` and `egid` normally also apply to `fsuid` and `fsgid`, a program relinquishing root privileges need not be concerned with setting `fsuid` or `fsgid` to safe values. However, there has been at least one kernel bug that violated this invariant (\[[Chen 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Chen02)\] and \[[Tsafrir 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Tsafrir08)\]). Consequently, a prudent program checks that `fsuid` and `fsgid` have harmless values after relinquishing privileges.
## Risk Assessment
If privilege relinquishment conditions are left unchecked, any flaw in the program may lead to unintended system compromise corresponding to the more privileged user or group account.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS37-C | high | probable | low | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | user_defined | Soundly supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS37 |  |
| Helix QAC | 2024.4 | DF4876, DF4877, DF4878 |  |
| Klocwork | 2024.4 | SV.USAGERULES.PERMISSIONS
 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS37-a | Ensure that privilege relinquishment is successful |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS37-C | Checks for priviledge drop not verified (rule fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS37-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772 | Privilege Sandbox Issues [XYO] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-273, Failure to check whether privileges were dropped successfully | 2017-07-07: CERT: Exact |

## Bibliography

|  |  |
| ----|----|
| [Chen 2002] | "Setuid Demystified" |
| [Dowd 2006] | Chapter 9, "Unix I: Privileges and Files" |
| [Open Group 2004] | setuid()getuid()seteuid() |
| [Tsafrir 2008] | "The Murky Issue of Changing Process Identity: Revising 'Setuid Demystified'" |
| [Wheeler 2003] | Section 7.4, "Minimize Privileges" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152295) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152299)
## Comments:

|  |
| ----|
| The motivation for this one is very different from error checking. For one, the described calls' behavior tends to vary on different POSIX based implementations. It is always good practice to ensure that privileges cannot be restored since a setuid() may actually succeed (and not return a -1) but still fail to change all the three IDs (esp. the saved-set-uid). Hope that clarifies it a bit.
The 'Setuid Demystified' paper is a good place to look up things like that, though there are no seemingly concrete examples of the remediation anywhere, except for the sendmail example that I put up.
                                        Posted by dmohindr at Jun 04, 2008 07:59
                                     |
| Let's see, POSIX says
If the process has appropriate privileges, setuid() shall set the real user ID, effective user ID, and the saved set-user-ID of the calling process to uid.
and
Upon successful completion, 0 shall be returned. Otherwise, -1 shall be returned and errno set to indicate the error.
The only time when setuid() can return 0 and fail to drop privileges is when "the process does not have appropriate privileges."
So any conforming POSIX implementation (which this article assumes) should return -1 in the first call if it was not able to successfully drop privileges... if for some reason the implementation does not do this, it is either not POSIX compliant and we don't need worry about it or the process already has low privileges.
Also, if you don't trust the first call to do the right thing and let you know when it failed to drop privileges, how can you trust the second call? They are both part of the same implementation, and if you don't trust it, calling it a second time won't help.
                                        Posted by avolkovi at Jun 04, 2008 09:22
                                     |
| That's correct and that's why it's not pure error checking. Since as you state correctly -
'The only time when setuid() can return 0 and fail to drop privileges is when "the process does not have appropriate privileges."'
This rule captures just that in the top NCCE/CS pair. If the programmer has dropped privileges previously say temporarily/something prevents a successful privilege drop like the capability bits, then the setuid will not affect the saved-set-uid while still affecting the euid. However, by some chance if some control flow causes another setuid to get executed, privileges shall be restored. This is not what the programmer desired esp. after reading the man page which says all three IDs would be set.
Notice the words "This may be dangerous depending on the sequence of the preceding privilege changes." in the rule.
Maybe that should be elaborated if it is not intuitive enough.
The second call is trusted since if you have dropped privileges permanently, a setuid(0) should never succeed. If it does, there's trouble and you need to fix it.
The reference to David Wheeler's book chapter covers a brief explanation on the sendmail vuln and an immediate remediation that followed. This rule is also somewhat a cousin of a listing in CWE which talks about insufficient privileges.
Again, note that setuid may affect only 1 ID and thus succeed whereas the programmer wants to drop privileges permanently by setting all the three IDs. 
                                        Posted by dmohindr at Jun 04, 2008 10:24
                                     |
| Ok, I added some discussion and more code to illustrate this better... is there any reason to still keep around the second CCE/NCCE pair now that the first one is more detailed and covers basically the same idea?
                                        Posted by avolkovi at Jun 04, 2008 11:20
                                     |
| The second compliant solution doesn't look right to me anyway. The only way the
if (!geteuid())

can be true is if the real uid is zero (since at this point the effective uid has been set to the real uid).
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jun 05, 2008 12:23
\| \|
I did not get what that means. EUID can be 0 irrespective of the real uid (such as in setuid-superuser programs). Isn't it? The same thing happens with mail transfer agents.
I saw the changes to the pair above which seem to be coherent. The reason why this was separated was to avoid complexity in showing just one (complex) code fragment. But I suppose, that was for providing clearer understanding. Good enough with the change, just that it is easy to miss which part of the code we want to emphasize. (Can't we just highlight the necessary conditions somewhat differently to make them more obvious?)
Also, good work with the tables.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Jun 05, 2008 15:11
\| \|
> I did not get what that means. EUID can be 0 irrespective of the real uid (such as in setuid-superuser programs). Isn't it?

The problem has gone away now that the second NCCE/CS pair has been replaced with a variant of the first CS.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jun 06, 2008 04:21
\| \|
This rule may be secure, but I don't think it can be detected automatically anymore, because there is no way, upon encountering setuid() if the programmer is trying to acquire elevated privs or drop them. Perhaps this should therefore be a recommendation, not a rule?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 16, 2008 15:59
\| \|
Failure to automatically detect a violation would not suggest that this be classified as a recommendation, right? According to the rules vs recommendations page, manual inspection also qualifies.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Jan 29, 2009 18:13
\| \|
Ah, yes, you're right. Withdrawn.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 30, 2009 11:47
\| \|
There's a serious problem with the code above: it only takes care of the uid, but it neglects to take care of the gid (setgid) and the supplementary groups (setgroups). Alas, dropping the privileges associated with only the user does not ensure privileges relinquishment. The following paper explains the problem in detail and attempts to solve it:
;   Dan Tsafrir, Dilma Da Silva, and David Wagner  
    *["The murky issue of changing process identity: revising setuid demystified"](http://www.eecs.berkeley.edu/~daw/papers/setuid-login08b.pdf)*  
    Usenix ;login, June 2008, pages 55-66  
    <http://www.eecs.berkeley.edu/~daw/papers/setuid-login08b.pdf>
The complete solution (C code) can be found here:
    <http://code.google.com/p/change-process-identity/>
![](images/icons/contenttypes/comment_16.png) Posted by paleshadows at May 03, 2009 04:31
\| \|
Haven't looked at these newer papers yet but I believe the guideline was written to only focus on how to **check** whether privilege relinquishment was successful (more than ensuring; misleading title perhaps). So it takes only one example of setuid. There is more related information in [POS36-C. Observe correct revocation order while relinquishing privileges](POS36-C_%20Observe%20correct%20revocation%20order%20while%20relinquishing%20privileges). I don't think currently there is a guideline that describes how to drop all privileges safely. Thanks for the links.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at May 03, 2009 10:36
\| \|
Both this page and the link you provided are overlooking important, non-standard, nontrivial, and subtle interactions between the various  
system calls that must be used in order to (1) drop all privileges and  
(2) verify that they were dropped correctly.
For example, if you are not very careful, when you invoke setgroups()  
(to set the supplementary groups array of a process), you might  
erroneously override the effective gid. (And vice versa, namely, when  
setting the effective gid you might mess up the supplementary groups  
if you're not careful.) This might invalidate checks (that the  
identity is as it should be) you may have performed earlier.
Another example is that, due to the unfortunate POSIX definition of  
getgroups() (which you must use when verifying that the supplementary  
groups of a process are as they should be), you may or may not get the  
effective gid bundled in with the returned array, which makes the  
verification routine surprisingly challenging. Also, in general,  
verifying that the supplementary group array is as it should, is  
fundamentally different than just verifying the user and group ids.
The bottom line is that your statement that
*    "this guideline was written to only focus on how to*  
*    check whether privilege relinquishment was successful*  
*    (more than ensuring; misleading title perhaps). So it*  
*    takes only one example of setuid"*
is, I believe, misleadingly naive and so extremely dangerous. This is  
explained in detail in *[this paper](http://www.eecs.berkeley.edu/~daw/papers/setuid-login08b.pdf)*.
![](images/icons/contenttypes/comment_16.png) Posted by paleshadows at May 11, 2009 19:09
\| \|
Having studied the referenced paper, I note the following:
-   Supplemental group ids are ignored by many systems, including our secure coding rules.
<!-- -->
-   A setuid program does not introduce new vuls via supplemental group ids if it does not alter the supplemental groups. This is because it inherits supp gids from the (unprivileged) user who ran it, rather than receiving a set of 'root' supp gids.
<!-- -->
-   So the danger wrt supp. gids occurs only when a root program has root-only supplemental groups, either by modifying them itself, or by being run from root with supp. gids. The program then drops privileges (temporarily or permenantly). The 'unprivileged' program then still has access to the supplemental groups. (Furthermore, the program cannot relinquish supp.gids after it has relinquished the root uid.)
<!-- -->
-   Therefore, to update our rules, we should mandate that any program with root privileges (regardless of how it got them) should adopt 'unprivileged' supplemental groups when relinquishing privs. IMHO this info belongs in POS36-C rather than this rule.
<!-- -->
-   The paper complains that subtle portability issues and bugs make difficult the process of changing identities. It also acknolwedges that its solution only handles 'standardized' capabilities, and cannot address all system-specific capabilities, such as Linux FS-ID capabilities (Yes, I know it provides code for this specific example, but there are others). In summary, there is still no 'one-size-fits-all' solution.
The way to solve the last point would be standardization...if a drop_privs_permenantly() function was in the POSIX standard, platforms could extend it to handle system-specific settings, such as Linux FS-ID. What is the current status on POSIX standardization of set\*id()-related syscalls?
Comments?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 12, 2009 15:37
\| \|
> The way to solve the last point would be standardization...if a drop_privs_permenantly() function was in the POSIX standard, platforms could extend it to handle system-specific settings

The POSIX developers prefer to standardise existing practice rather than invent things. Do any existing systems have a function like that?
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 13, 2009 04:24
\| \|
I have added to this rule instructions for how to check that supplemental group privileges are valid, and I have added to POS36-C instructions for how to relinquish supplemental group privileges. Both are lifted from the Tsafrir/Da Silva/Wagner paper.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 14, 2009 12:08
\|
