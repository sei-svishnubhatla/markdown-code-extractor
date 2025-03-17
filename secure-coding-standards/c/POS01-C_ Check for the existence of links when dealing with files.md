Many common operating systems such as Windows and UNIX support file links, including hard links, symbolic (soft) links, and virtual drives. Hard links can be created in UNIX with the `ln` command or in Windows operating systems by calling the [CreateHardLink()](http://msdn.microsoft.com/en-us/library/aa363860(VS.85).aspx) function. Symbolic links can be created in UNIX using the `ln -s` command or in Windows by using directory junctions in NTFS or the Linkd.exe (Win 2K resource kit) or "junction" freeware. Virtual drives can also be created in Windows using the `subst` command.
File links can create security issues for programs that fail to consider the possibility that the file being opened may actually be a link to a different file. This is especially dangerous when the vulnerable program is running with elevated privileges.
Frequently, there is no need to check for the existence of symbolic links because this problem can be solved using other techniques. When opening an existing file, for example, the simplest solution is often to drop privileges to the privileges of the user. This solution permits the use of links while preventing access to files for which the user of the application is not privileged.
When creating new files, it may be possible to use functions that create a new file only where a file does not already exist. This prevents the application from overwriting an existing file during file creation. (See [FIO03-C. Do not make assumptions about fopen() and file creation](FIO03-C_%20Do%20not%20make%20assumptions%20about%20fopen__%20and%20file%20creation).)
In rare cases, it is necessary to check for the existence of symbolic or hard links to ensure that a program is reading from an intended file and not a different file in another directory. In these cases, avoid creating a race condition when checking for the existence of symbolic links. (See [POS35-C. Avoid race conditions while checking for the existence of a symbolic link](POS35-C_%20Avoid%20race%20conditions%20while%20checking%20for%20the%20existence%20of%20a%20symbolic%20link).)
## Noncompliant Code Example
This noncompliant code example opens the file specified by the string `file_name` for read/write access and then writes user-supplied data to the file:
``` c
char *file_name = /* something */;
char *userbuf = /* something */;
unsigned int userlen = /* length of userbuf string */;
int fd = open(file_name, O_RDWR);
if (fd == -1) {
   /* handle error */
}
write(fd, userbuf, userlen);
```
If the process is running with elevated privileges, an attacker can exploit this code, for example, by replacing the file with a symbolic link to the `/etc/passwd` authentication file. The attacker can then overwrite data stored in the password file to create a new root account with no password. As a result, this attack can be used to gain root privileges on a vulnerable system.
## Compliant Solution (Linux 2.1.126+, FreeBSD, Solaris 10, POSIX.1-2008 `O_NOFOLLOW`)
Some systems provide the `O_NOFOLLOW` flag to help mitigate this problem. The flag is required by the POSIX.1-2008 standard and so will become more portable over time \[[Open Group 2008](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography)\]. If the flag is set and the supplied `file_name` is a symbolic link, then the open will fail.
``` c
char *file_name = /* something */;
char *userbuf = /* something */;
unsigned int userlen = /* length of userbuf string */;
int fd = open(file_name, O_RDWR | O_NOFOLLOW);
if (fd == -1) {
  /* handle error */
}
write(fd, userbuf, userlen);
```
Note that this compliant solution does not check for hard links.
## Compliant Solution (`lstat`-`fopen`-`fstat`)
This compliant solution uses the `lstat`-`fopen`-`fstat` idiom illustrated in [FIO05-C. Identify files using multiple file attributes](FIO05-C_%20Identify%20files%20using%20multiple%20file%20attributes):
``` c
char *file_name = /* some value */;
struct stat orig_st;
if (lstat( file_name, &orig_st) != 0) {
  /* handle error */
}
if (!S_ISREG( orig_st.st_mode)) {
  /* file is irregular or symlink */
}
int fd = open(file_name, O_RDWR);
if (fd == -1) {
  /* handle error */
}
struct stat new_st;
if (fstat(fd, &new_st) != 0) {
  /* handle error */
}
if (orig_st.st_dev != new_st.st_dev ||
    orig_st.st_ino != new_st.st_ino) {
  /* file was tampered with during race window */
}
/* ... file is good, operate on fd ... */
```
This code is still subject to a time-of-check, time-of-use (TOCTOU) race condition, but before doing any operation on the file, it verifies that the file opened is the same file as was previously checked (by checking the file's device and i-node.) As a result, the code will recognize if an attacker has tampered with the file during the race window and can operate accordingly.
Note that this code does not check for hard links.
### Hard Links
Hard links are problematic because if a file has multiple hard links, it is impossible to distinguish the original link from one that might have been created by a malicious attacker.
One way to deal with hard links is simply to disallow opening of any file with two or more hard links. The following code snippet, when inserted into the previous example, will identify if a file has multiple hard links:
``` c
if (orig_st.st_nlink > 1) {
  /* file has multiple hard links */
}
```
Because a hard link may not be created if the link and the linked-to file are on different devices, many platforms place system-critical files on a different device from the one where user-editable files are kept. For instance, the `/` directory, which contains critical system files like `/etc/passwd`, would live on one hard drive, while the `/home` directory, which contains user-editable files, would reside on a separate hard drive. This prevents users, for example, from creating hard links to `/etc/passwd`.
## Risk Assessment
Failing to check for the existence of links can result in a critical system file being overwritten, leading to data integrity violations.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS01-C | medium | likely | high | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Could report possible violations of this rule by flagging calls to open() that do not have an O_NOFOLLOW flag and that are not preceded by a call to lstat() and succeeded by a call to fstat |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS01-C).
## Related Guidelines

|  |  |
| ----|----|
| MITRE CWE | CWE-59, Failure to resolve links before file access (aka "link following")CWE-362, Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
CWE-367, Time-of-check, time-of-use (TOCTOU) race condition |

## Bibliography

|  |  |
| ----|----|
| [Austin Group 2008] | ; |
| [Open Group 2004] | open() |
| [Open Group 2008] | ; |
| [Seacord 2013] | Chapter 8, "File I/O" |

------------------------------------------------------------------------
[](../c/Rec_%2050_%20POSIX%20_POS_) [](../c/Rec_%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152194)
## Comments:

|  |
| ----|
| The mode argument is useless here:if ((fd = open("some_file", O_EXCL|O_RDWR, 0600)) == -1)
In the case of the first non-compliant example, Â I think it should be mentioned that it is safer to drop privileges before
creating/writing files.Â 
The symlink check still needs to be done (especially if the program is setUID root), but there are additional steps that
can be taken to make such a program safer (such as the above).
                                        Posted by edwin at Mar 17, 2008 13:20
                                     |
| The statement "The lstat() function does not follow symbolic links, but fstat() does" is wrong.; Since fstat() doesn't process pathnames, it doesn't have anything to do with symbolic links.  The statement should be  " The lstat() function does not follow symbolic links, but open() does."
                                        Posted by geoffclare at Mar 19, 2008 12:31
                                     |
| There's a TOCTOU between the lstat() and the open(), I believe.; As suggested, privileged processes are better off dropping privileges - or forking and having the child drop privileges and deal with the file.
Beware, HP-UX prior to 11.31 does not support seteuid() and setegid() even though they are specified in POSIX.  HP-UX 11i does support setreuid() but not setregid(), even though both are specified in POSIX.  HP-UX does support setresuid() and setresgid(), even though neither is specified in POSIX.  (Information about all these functions on HP web site checked 2007-12).  HP reports that HP-UX 11.31 supports all three missing functions.
This makes writing to code to drop and reacquire privileges harder than it should be. 
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 03:41
                                     |
| HP-UX does have setregid().; Checked on an 11.23 system:
$ grep setre.id /usr/include/sys/unistd.h
#  pragma extern lchown, sbrk, setregid, setreuid, sync
        extern int setregid __((gid_t, gid_t));
        extern int setreuid __((uid_t, uid_t));
$ uname -sr
HP-UX B.11.23
                                        Posted by geoffclare at Mar 20, 2008 07:19
                                     |
| This page should mention O_NOFOLLOW which, I believe, was designed to address exactly this issue. It tells open() to fail if the file is a symbolic link.; Although not many implementations support it yet, it is going to be required by the new POSIX revision and so will become more portable over time. Probably the recommended approach should be to use O_NOFOLLOW if it is defined, otherwise use the lstat()+open()+fstat() method (or drop privileges).
                                        Posted by geoffclare at Mar 20, 2008 11:16
                                     |
| Why is using the O_EXCL flag not enough for creation?; Manpage says:
"When used with O_CREAT, if the file already  exists  it  is  an error  and the open will fail. In this context, a symbolic link exists, regardless of where its points to." 
                                        Posted by avolkovi at Mar 25, 2008 09:34
                                     |
| This section is about opening an existing file.; The code does not use O_CREAT.
In fact the use of O_EXCL here without O_CREAT is a bug.  POSIX says "If O_EXCL is set and O_CREAT is not set, the result is undefined."
                                        Posted by geoffclare at Mar 25, 2008 11:36
                                     |
| OK, I eliminated the mode argument and tried to add a better explanation for other things that can be done to eliminate the need to check for symlinks.  Let me know if you disagree.
                                        Posted by rcs at Mar 27, 2008 12:42
                                     |
| This change has been made.
                                        Posted by rcs at Mar 27, 2008 12:43
                                     |
| we have OS specific file names in the NCCE... is this a problem?
                                        Posted by avolkovi at Apr 22, 2008 10:12
                                     |
| I think OS-specific filenames are only a problem if they are part of a compliant example that claims portability (eg it is not claimed to be POSIX-only.) They are ok in NCCE's, esp. examples that come from real-world examples, which are often OS-specific.
Besides, this example could theoretically apply to Windows, if /home/rcs exists there 
                                        Posted by svoboda at Apr 22, 2008 14:23
                                     |
| This may also be vulnerable when running with normal user privileges.
                                        Posted by rcs at May 02, 2008 14:00
                                     |
| Weird - I definitely ran into problems on some HP-UX machine where we were building (and it was a link failure, not a compile warning), but I can find the functions on 11.00.; The machine we used was 11.11, I think, but it seems very odd that it would go missing from 11.11 having been in 11.00.  Dunno what happened here.  Getting the declaration included might be trickier - it seems to be protected by _INCLUDE_XOPEN_SOURCE_EXTENDED (in 11.00).
Digging in the source code in question, I noted:
** HP-UX 11i does not support seteuid() and setegid() even though they
** are specified in POSIX.  HP-UX 11i does support setreuid() but not
** setregid(), even though both are specified in POSIX.  HP-UX does
** support setresuid() and setresgid(), even though neither is specified
** in POSIX.  Other BSD-based platforms could be similarly recalcitrant.
** Information about all these functions on HP web site (2007-12).
** HP reports that HP-UX 11.31 supports all three missing functions.
** Validate, then remove this conditional code and use seteuid() and
** setegid() unconditionally when that (or a later version) is used for
** builds on HP-UX.
Empirical testing tonight suggests that setregid() is present, but seteuid() and setegid() are not, in HP-UX 11.00.
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 01:55
                                     |
| What about showing a 'drop privileges' solution.; Books sometimes (always?) say "do it", but don't show the code to do it.
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 01:57
                                     |
| We are working on a group of rules related to privileges.  Hopefully we'll get drafts of these up this week.
                                        Posted by rcs at May 11, 2008 05:53
                                     |
| seteuid() and setegid() were not in POSIX versions before POSIX.1-2001, so their omission from HP-UX systems before 11.31 (the first version to support POSIX.1-2001) is perfectly reasonable.
                                        Posted by geoffclare at May 12, 2008 05:43
                                     |
| this issue has been addressed (not by me)
                                        Posted by avolkovi at May 19, 2008 14:11
                                     |
| Marked as 'unenforceable' because the rule does not indicate when one should check for links. It indicates how to do so, and when one does not have to do so, but isn't clear on when it should be done.
                                        Posted by svoboda at Jul 14, 2008 15:24
                                     |

