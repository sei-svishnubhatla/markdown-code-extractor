Many common operating systems, such as Windows and UNIX, support symbolic (soft) links. Symbolic links can be created in UNIX using the `ln -s` command or in Windows by using directory junctions in NTFS or the Linkd.exe (Win 2K resource kit) or "junction" freeware.
If not properly performed, checking for the existence of symbolic links can lead to race conditions.
This rule is a specific instance of rule [FIO45-C. Avoid TOCTOU race conditions while accessing files](FIO45-C_%20Avoid%20TOCTOU%20race%20conditions%20while%20accessing%20files).
## Noncompliant Code Example
The POSIX `lstat()` function collects information about a symbolic link rather than its target. This noncompliant code example uses the `lstat()` function to collect information about the file, checks the `st_mode` field to determine if the file is a symbolic link, and then opens the file if it is not a symbolic link:
``` c
char *filename = /* file name */;
char *userbuf = /* user data */;
unsigned int userlen = /* length of userbuf string */;
struct stat lstat_info;
int fd;
/* ... */
if (lstat(filename, &lstat_info) == -1) {
  /* Handle error */
}
if (!S_ISLNK(lstat_info.st_mode)) {
   fd = open(filename, O_RDWR);
   if (fd == -1) {
       /* Handle error */
   }
}
if (write(fd, userbuf, userlen) < userlen) {
  /* Handle error */
}
```
This code contains a time-of-check, time-of-use (TOCTOU) race condition between the call to `lstat()` and the subsequent call to `open()` because both functions operate on a file name that can be manipulated asynchronously to the execution of the program. (See [FIO01-C. Be careful using functions that use file names for identification](FIO01-C_%20Be%20careful%20using%20functions%20that%20use%20file%20names%20for%20identification).)
## Compliant Solution (POSIX.1-2008 or newer)
This compliant solution eliminates the race condition by using `O_NOFOLLOW` to cause `open()` to fail if passed a symbolic link, avoiding the TOCTOU by not having a separate "check" and "use":
``` c
char *filename = /* file name */;
char *userbuf = /* user data */;
unsigned int userlen = /* length of userbuf string */;
int fd = open(filename, O_RDWR|O_NOFOLLOW);
if (fd == -1) {
  /* Handle error */
}
if (write(fd, userbuf, userlen) < userlen) {
  /* Handle error */
}
```
## Compliant Solution (POSIX.1-2001 or older)
This compliant solution eliminates the race condition by
1.  Calling `lstat()` on the file name.
2.  Calling `open()` to open the file.
3.  Calling `fstat()` on the file descriptor returned by `open()`.
4.  Comparing the file information returned by the calls to `lstat()` and `fstat()` to ensure that the files are the same.
``` c
char *filename = /* file name */;
char *userbuf = /* user data */;
unsigned int userlen = /* length of userbuf string */;
struct stat lstat_info;
struct stat fstat_info;
int fd;
/* ... */
if (lstat(filename, &lstat_info) == -1) {
  /* handle error */
}
fd = open(filename, O_RDWR);
if (fd == -1) {
  /* handle error */
}
if (fstat(fd, &fstat_info) == -1) {
  /* handle error */
}
if (lstat_info.st_mode == fstat_info.st_mode &&
    lstat_info.st_ino == fstat_info.st_ino  &&
    lstat_info.st_dev == fstat_info.st_dev) {
  if (write(fd, userbuf, userlen) < userlen) {
    /* Handle Error */
  }
}
```
This code eliminates the TOCTOU condition because `fstat()` is applied to file descriptors, not file names, so the file passed to `fstat()` must be identical to the file that was opened. The `lstat()` function does not follow symbolic links, but `open()` does. Comparing modes using the `st_mode` field is sufficient to check for a symbolic link.
Comparing i-nodes, using the `st_ino` fields, and devices, using the `st_dev` fields, ensures that the file passed to `lstat()` is the same as the file passed to `fstat()`. (See [FIO05-C. Identify files using multiple file attributes](FIO05-C_%20Identify%20files%20using%20multiple%20file%20attributes).)
## Risk Assessment
TOCTOU race condition vulnerabilities can be exploited to gain elevated privileges.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS35-C | high | likely | medium |  P18  |  L1  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | user_defined | Soundly supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS35 |  |
| Compass/ROSE |  |  | Can detect some violations of this rule. In particular, it ensures that calls to open() that are preceded by a call to lstat() are also followed by a call to fstat(). |
| Coverity | 2017.07 | TOCTOU | Implemented |
| Helix QAC | 2024.4 | DF4886, DF4887, DF4888 |  |
| Klocwork | 2024.4 | SV.TOCTOU.FILE_ACCESSCERT.STR.ASSIGN.CONST_TO_NONCONST |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS35-b | Avoid race conditions while checking for the existence of a symbolic link |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS35-C | Checks for file access between time of check and use (TOCTOU) (rule fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS35-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-363, Race condition enabling link following | 2017-07-07: CERT: Exact |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-764 and POS51-C/POS35-C
Independent( CWE-764, POS51-C, POS35-C)
CWE-764 is about semaphores, or objects capable of being locked multiple times. Deadlock arises from multiple locks being acquired in a cyclic order, and generally does not arise from semaphores or recursive mutexes.
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 9, "UNIX 1: Privileges and Files" |
| [ISO/IEC 9899:2024] | Section 7.23, "Input/output <stdio.h>" |
| [Open Group 2004] | lstat() fstat() 
open() |
| [Seacord 2013] | Chapter 8, "File I/O" |

------------------------------------------------------------------------
[](../c/POS34-C_%20Do%20not%20call%20putenv__%20with%20a%20pointer%20to%20an%20automatic%20variable%20as%20the%20argument) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152295)
## Comments:

|  |
| ----|
| It sayeth:
The only function available on POSIX systems to collect information about a symbolic link rather than its target is the lstat() function.
What is readlink(), then?
Further, the compliant code seems to be missing the check that lstat() was not pointing at a symlink - which is expensive because you need the open() - costly - and fstat() - relatively cheap - calls.
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 02:09
                                     |
| Taking the two points separately:
    readlink() returns the contents of the link.; This is not "information about" the link, in the same sense that what read() returns from a file is its contents, not "information about" the file.  However, the statement that lstat() is the only function doesn't really serve any useful purpose, and will be wrong when POSIX.1-2008 is published (it adds fstatat(), which has an AT_SYMLINK_NOFOLLOW flag).  That sentence could just as well be "On POSIX systems the lstat() function collects information about a symbolic link rather than its target."
    The compliant code is not missing the symlink check.  As it says in the description, "Comparing modes using the st_mode field is sufficient to check for a symbolic link."  Regarding cost, the NCCE does an lstat() and an open() where the CS does an lstat(), an open() and an fstat().  The only extra cost is the fstat() which, as you say, is relatively cheap.
                                        Posted by geoffclare at May 12, 2008 05:32
                                     |
| OK, I believe all the required changes have been made to address these two points.
                                        Posted by rcs_mgr at May 12, 2008 12:33
                                     |
| Windows does not have an lstat function, so the compliant example does not help out there.; I believe you can use GetFileAttributesEx to check whether the FILE_ATTRIBUTE_REPARSE_POINT bit is set to determine whether a file is a symbolic link. 
                                        Posted by aballman at Jun 06, 2013 15:36
                                     |
| I thought Windows didn't have symbolic links either, just short cuts?
                                        Posted by rcs_mgr at Jun 07, 2013 15:41
                                     |
| In true Windows fashion, there are many things.; 1) Shortcuts, which aren't really links at all.  They're a physical file with data inside of them that point to where another file may or may not live.2) Symbol links, which are akin to UNIX symlinks.  You can create these with CreateSymbolicLink.3) Hard links, which only apply to files on the same volume, and basically allows you to have two names to the same filesystem identity.  You can create them with CreateHardLink.
                                        Posted by aballman at Jun 07, 2013 15:47
                                     |
| well the sym links and the hard links sound just like POSIX, except the function you use to create them.shortcuts sounds just like symlinks (separate file with the name of a file inside that may or may not exist).; however, i think the way other windows calls handle short cuts is very different then the way POSIX calls handle symlinks and possibly different than how Windows calls handle symlinks.  I think symlinks and hard links are infrequently used in Windows environments.
                                        Posted by rcs_mgr at Jun 07, 2013 16:03
                                     |
| Yes, shortcut files are different than symlinks.; For instance, when you attempt to resolve a shortcut where the target has moved, Windows will attempt to find the new file location (possibly even by displaying UI).  Symbolic links on Windows are handled very differently from shortcut files (they're NTFS metadata more than a physical file), and behave almost identical to symlinks on UNIX.  In fact, IIRC, the whole rationale behind symlinks on Windows is for their POSIX subsystem version.You are correct that symlinks and hard links are used infrequently on Windows.  They do exist, so programmers should be prepared to handle them.  But they're not a high priority item.  Shortcuts, on the other hand, are used frequently.  The difference here being: when you attempt to open a shortcut file (via fopen or CreateFile), the shortcut is not resolved.  You open the physical shortcut file itself.  If it were a symlink, the file would be resolved and the target would be opened.  So the race condition is still there for proper shortcut resolution on Windows both with symlinks as well as shortcut files.
                                        Posted by aballman at Jun 07, 2013 16:35
                                     |
| Unless I'm missing something, this all seems unnecessarily complicated. If you just don't want the file you're opening to be a symlink, can't you just pass O_NOFOLLOW to open()?
                                        Posted by jcsible at Jul 07, 2020 11:59
                                     |

