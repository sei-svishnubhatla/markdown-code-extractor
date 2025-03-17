Creating a jail isolates a program from the rest of the file system. The idea is to create a sandbox, so entities the program does not need to access under normal operation are made inaccessible. This makes it much harder to abuse any vulnerability that can otherwise lead to unconstrained system compromise and consequently functions as a defense-in-depth strategy. A jail may consist of world-viewable programs that require fewer resources to execute than those that exist on that system. Jails are useful only when there is no way to elevate privileges in the event of program failure.
Additionally, care must be taken to ensure that all the required resources (libraries, files, and so on) are replicated within the jail directory and that no reference is made to other parts of the file system from within this directory. It is also advisable to administer restrictive read/write permissions on the jail directories and resources on the basis of the program's privilege requirements. Although creating jails is an effective security measure when used correctly, it is not a surrogate for compliance with the other rules and recommendations in this standard.
## Noncompliant Code Example
A security flaw exists in this noncompliant code example resulting from the absence of proper canonicalization measures on the file path. This allows an attacker to traverse the file system and possibly write to a file of the attacker's choice with the privileges of the vulnerable program. For example, it may be possible to overwrite the password file (such as the `/etc/passwd`, common to many POSIX-based systems) or a device file, such as the mouse, which in turn can aid further exploitation or cause a denial of service to occur.
``` c
enum { array_max = 100 };
/*
 * Program running with elevated privileges where argv[1]
 * and argv[2] are supplied by the user
 */
char x[array_max];
FILE *fp = fopen(argv[1], "w");
strncpy(x, argv[2], array_max);
x[array_max - 1] = '\0';
/*
 * Write operation to an unintended file such as /etc/passwd
 * gets executed
 */
if (fwrite(x, sizeof(x[0]), sizeof(x)/sizeof(x[0]), fp) <
    sizeof(x)/sizeof(x[0])) {
  /* Handle error */
}
```
An attacker can control the value of `argv[1]` and consequently access any resource on the file system.
This noncompliant code example also violates [FIO02-C. Canonicalize path names originating from tainted sources](FIO02-C_%20Canonicalize%20path%20names%20originating%20from%20tainted%20sources) and [FIO03-C. Do not make assumptions about fopen() and file creation](FIO03-C_%20Do%20not%20make%20assumptions%20about%20fopen__%20and%20file%20creation).
## Compliant Solution (UNIX)
Some UNIX-based systems (such as OpenBSD) can restrict file system access by creating a `chroot()` jail. The `chroot()` jail requires care to implement securely \[[Wheeler 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Wheeler03)\]. It is achieved by passing a predefined directory name as an argument to `chroot()`. The call to `chroot()` requires superuser privileges. However, this call does not *leave* the process inside the jail directory as might be expected. A subsequent `chdir()` is required to restrict access to the jail boundaries.
Another essential step is to drop superuser privileges permanently after these calls (see [POS02-C. Follow the principle of least privilege](POS02-C_%20Follow%20the%20principle%20of%20least%20privilege)). The `chroot()` system call is not secure against the superuser changing the current root directory (if privileges are not dropped). Successful jail creation prevents unintentional file system access even if an attacker gives malicious input, such as through command-line arguments.
``` c
/*
 * Make sure that the chroot/jail directory exists within
 * the current working directory. Also assign appropriate
 * permissions to the directory to restrict access. Close
 * all file system descriptors to outside resources lest
 * they escape the jail.
 */
if (setuid(0) == -1) {
  /* Handle error */
}
if (chroot("chroot/jail") == -1) {
  /* Handle error */
}
if (chdir("/") == -1) {
  /* Handle error */
}
/* Drop privileges permanently */
if (setgid(getgid()) == -1) {
  /* Handle error */
}
if (setuid(getuid()) == -1) {
  /* Handle error */
}
/* Perform unprivileged operations */
enum {array_max = 100};
FILE *fp = fopen(argv[1], "w");
char x[array_max];
strncpy(x, argv[2], array_max);
x[array_max - 1] = '\0';
/* Write operation is safe within jail */
if (fwrite(x, sizeof(x[0]), sizeof(x)/sizeof(x[0]), fp) <
    sizeof(x)/sizeof(x[0])) {
  /* Handle error */
}
```
An alternative sequence is to first call `chdir("chroot/jail")` and then call `chroot(".")`. However, calling `chdir("/some/path")`, then `chroot("/some/path")`, should be avoided because this sequence may be susceptible to a race condition: an attacker with sufficient privileges can arrange for `/some/path` to refer to different directories in the two system calls. Consequently, the program will not have its current working directory set to the new root directory. Using either `chdir("/")` after `chroot()` or `chroot(".")` after `chdir()` guarantees that the current working directory will be the same directory as the new root.
## Risk Assessment
Failing to follow this recommendation may lead to full-system compromise if a file system vulnerability is discovered and exploited.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS05-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.CHROOTMISC.CHROOT.NOCHDIR
 | Use of chrootchroot without chdir
 |
| Polyspace Bug Finder | R2024a | CERT C: Rec. POS05-C | Checks for file manipulation after chroot() without chdir("/") (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO16-C).
## Bibliography

|  |  |
| ----|----|
| [Wheeler 2003] | Section 7.4, "Minimize Privileges" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152062)[](../c/Rec_%2050_%20POSIX%20_POS_)[](../c/Rec_%2001_%20Preprocessor%20_PRE_)
## Comments:

|  |
| ----|
| so I have several issues with this new rule...
    This comment in [VOID FIO15-A. Do not create temporary files in shared directories] seems very relevant
    The NCCE is really honestly just a violation of [FIO02-C. Canonicalize path names originating from untrusted sources]... there is no need for a jail if you address that problem
    This rule seems confused over what's it's recommending... it talks about overwriting /etc/passwd and then drops privileges in the CS, this begs of the question of why do you need a jail if you know how to drop privileges?
    We should remove references to OS-specific file names
    The location of the jail is hardwired into the code, this would allow an attacker to replace /chroot/jail with a link to, oh say... /, we should mention mkdtemp as in FIO15-A
    more as i think of them...
                                        Posted by avolkovi at May 19, 2008 09:56
                                     |
| 
    Yes, this one and the other comments are certainly relevant. But, we should not go into the realms of system administration and start discussing permissions within this recommendation, imo.
    I was expecting that one. The idea is to point out some flaw in the code which may accidentally/unintentionally leak (or worse over write) information from beyond the current working directory (or the chroot'ed dir). This may be replaced with a better flaw such as a buffer overflow in conjunction with a directory traversal, that may even escalate privileges in some way.; (Queued for now)
    The /etc/passwd example in NCCE is there to show that 1. You should not be running a program with superuser privileges if you want to use chroot() and 2. Any resource can be accessed with the same privileges as those ones that the program is currently executing with. The NCCE can be less serious such as modification of files in some other directory that belong to the same program owner. Moreover, privilege drops are not always successful and are sometimes implementation defined. I think the principle of least privilege (which is coming soon) will supplement this. Note that the jail is a fail-safe strategy in case some other programming errors, such as an improper canonicalization, have occurred. Also, /etc/foo is a valid path name, we just want to make things harder by making the FS structure ~invisible~. That's why it is a recommendation but not a rule, especially for daemons that need to run in world viewable directories.
    Done. The NCCE just cites /etc/passwd as an example now.
    Again, this recommendation is not meant to be touted for of all programs, but special world viewable ones. Generally, it is good advice to check for links before running such a program. After chroot() executes and drops privileges, the program is immune to symlink attacks. As for hard links, it is good advice to use different filesystems as hard links can't span across them (for highly sensitive environments). How would mkdtemp() be useful here...? We already have the /chroot/jail directory as a prerequisite where this program is saved (unless you want to store the program in a completely separate location).
    There are caveats to using chroot(), that's why it does not make other security best practices unnecessary. See this . I believe CWE also has a similar rule under privileges although it is more to do with dropping privileges after using chroot().
    References are under compilation currently
                                        Posted by dmohindr at May 20, 2008 07:34
                                     |
| on a slightly different note, is chroot() out of scope? i don't see it defined in POSIX and the man page specifically mentions " This function is not part of POSIX.1"... is it part of the new POSIX?
Nice link to the discussion with Alan Cox... but I got the feel that chroot() is mostly a debugging tool and that the non-BSD security applications of it are mostly a hack
                                        Posted by avolkovi at May 20, 2008 09:32
                                     |
| chroot() is not in POSIX, nor has it ever been.; It was in SUSv2 (marked LEGACY) and was removed when SUSv2 and POSIX.1-1996 were merged to form SUSv3/POSIX.1-2001.
                                        Posted by geoffclare at May 20, 2008 09:56
                                     |
| OK, then this rule likely does not belong in POSIX. It can be moved elsewhere, probably MSC, maybe ENV or FIO.
As per offline discussion with Alex, usage of chroot() as a security measure is a fairly well-known security measure, and difficult to get right. Therefore we should have a rec to discuss it. If we find it unusable (eg we decide that one should never use chroot() in lieu of other methods, or the security it adds is dubious at best), we can include that in our rec and change it to 'don't use chroot()'.
Also, it seems that a chroot() jail is not the first-stop solution to any vul, it is merely a stopgap measure to prevent the damage doable by a rogue program. So it is likely that any NCCE in this rec will also violate some other rec/rule (eg pathname canonicalization), and mitigating the vul w/o using chroot will always be possible (and usually also recommended). However, the fact that other methods are available to solve vuls does not invalidate the use of chroot...it is, after all, another layer of security, which is helpful, if not strictly necessary. It is (theoretically) true that chroot() is unnecessary if all your other code is secure, but never forget Murphy's law.
Finally, chroot() is probably most useful when you are running an app that uses very little of the filesystem...if you can do without any other executable scripts, your jail can be smaller after all. It is prob least useful when you want your jail to come with lots of UNIX functionality...just including Perl requires adding about 2000 files to your jail, as Alex mentioned.
                                        Posted by svoboda at May 20, 2008 11:22
                                     |
| True, it has no mention in POSIX. Notice why the line "Some Unix based systems..." has been used instead of POSIX. This recommendation was originally meant to be a discussion about dropping privileges after doing a chroot() (inspired from CWE) but it seemed that separating it as a recommendation would be a better idea since it does have some benefits as David summarizes. It's slightly controversial and the argument comes up every second year but careful/responsible use should do more good than harm, imo. I agree that this could possibly be moved to Misc.
                                        Posted by dmohindr at May 20, 2008 12:39
                                     |
| This rec is now MSC16-A
                                        Posted by svoboda at May 20, 2008 14:06
                                     |
| I do not think this rule really has a place in the standard. I believe it is completely out of scope.
For starters, at an aesthetic level, it has the words "filesystem" and "jail" in the title--two things of which C99 has no concept.
I realize that we have plenty of rules containing implementation-specific components, but I believe this is the only recommendation or rule which is entirely about something specific to an implementation (less POS).
I may have the reading of our scope wrong, but I think a good dividing line would be to not include a rule whose entire purpose is outside of C99 (again, except for things in POS). In short, I feel that when the argument reached the point that we decided it was even beyond POSIX that it should have been sent to the VOID instead of placed deeper into the standard.
I truly think that it's an important secure coding rule and appears to be well thought out (though I do not know much about how to properly jail), but I think that it opens a can of worms as to where the scope-dividing-line is.
                                        Posted by shaunh at Jun 06, 2008 14:10
                                     |
| Perhaps moving this rec out of POS was not such a good idea after all.  Although POSIX.1 does not include chroot(), it does at least have the concept of per-process root directories.  It defines the term "root directory" as:
A directory, associated with a process, that is used in pathname resolution for pathnames that begin with a slash.
And the rationale for that definition even mentions chroot():
This definition permits the operation of chroot(), even though that function is not in POSIX.1
                                        Posted by geoffclare at Jun 09, 2008 05:54
                                     |
| I'm not sure it is that far out of scope.
C99 has the concept of files.  Probably better to change the title to 
"Limit access to files by creating a jail"
anyway.
Our rule for being in scope is that the NCCE has to be in scope.  This one totally is.  It is OK if we cannot provide a compliant solution for all platforms.
I keep wondering about where this goes too, but I think the best place is FIO. We have lots of rules like this in FIO where the NCCE is C99 but the compliant solutions are platform specific.
                                        Posted by rcs at Jun 09, 2008 16:06
                                     |
| This is now FIO17 since it has more to do with files than either C99 or POSIX... also, the name has been changed to reflect the fact that C99 has no understanding of file systems.
                                        Posted by avolkovi at Jun 09, 2008 16:32
                                     |
| 
Moved this comment from Jon Leffler here, because this is where the chroot() discussion ended up:
Using a chroot() jail to limit the files that a (usually untrusted) process can access is only tangentially relevant to temporary files. If the chroot() jail is publicly accessible, the temporary files are just as vulnerable there as in any other location.
This is not to say the a discussion of chroot jails is not appropriate - it should be handled more fully. I believe that one of the ways out of a chroot jail is by fchdir() to a directory outside the jail, for example. This means that the process that initiates the jail must be careful not to have any directories outside the jail open for reading. There are a lot of arcane issues with setting up the jail too - like which devices are needed (/dev/tty?...) and which programs, and so on.
                                        Posted by rcs at Jun 19, 2008 09:53
                                     |
| I believe this comment got addressed when we separated FIO15 and FIO16
                                        Posted by avolkovi at Jun 19, 2008 10:00
                                     |
| Minor typo in Compliant Solution (*NIX):
enum 
Unknown macro: {array_mex = 100} 
;
should be
enum 
Unknown macro: {array_max = 100} 
;
                                        Posted by masaki at Sep 30, 2008 06:22
                                     |
| Fixed, thanks
                                        Posted by svoboda at Sep 30, 2008 11:18
                                     |
| A more compact form suggested by Rule AA. References#Chess 07 is:
if ((chroot("chroot/jail") != 0) || (chdir("/") != 0)) {
exit(-1);
}

![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Mar 11, 2009 00:41
\| \|
This recommendation doesn't apply to standard C since all of the elements;behind the guideline (chroot, setuid, setgid, and chdir) are not part of the C standard.  While the part of the guideline which makes things work (chroot) is also not part of the POSIX standard, this is the closest fit in terms of a home for the recommendation, so I've moved this out of FIO and into POS.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 14, 2013 15:34
\| \|
Can we update and rename this to use a term other than "jail"? That term is more strongly associated with [the extra stuff that FreeBSD gives you on top of chroot](https://www.freebsd.org/doc/handbook/jails.html), so it's kind of confusing to use it when you're just talking about normal chroot.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Aug 19, 2020 14:05
\| \|
What would you suggest as a better term? ;Personally, I've heard of chroot() jails long before I knew about FreeBSD's jail() systemcall...I've never heard another term for them.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 19, 2020 15:33
\|
