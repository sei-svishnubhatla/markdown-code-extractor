Many file-related security vulnerabilities result from a program accessing an unintended file object because file names are only loosely bound to underlying file objects. File names provide no information regarding the nature of the file object itself. Furthermore, the binding of a file name to a file object is reasserted every time the file name is used in an operation. File descriptors and `FILE` pointers are bound to underlying file objects by the operating system. (See [FIO03-C. Do not make assumptions about fopen() and file creation](FIO03-C_%20Do%20not%20make%20assumptions%20about%20fopen__%20and%20file%20creation).)
Accessing files via file descriptors or `FILE` pointers rather than file names provides a greater degree of certainty as to which object is actually acted upon. It is recommended that files be accessed through file descriptors or `FILE` pointers where possible.
The following C functions rely solely on file names for file identification:
-   `remove()`
-   `rename()`
-   `fopen()`
-   `freopen()`
Use these functions with caution. See [FIO10-C. Take care when using the rename() function](FIO10-C_%20Take%20care%20when%20using%20the%20rename__%20function), and [FIO08-C. Take care when calling remove() on an open file](FIO08-C_%20Take%20care%20when%20calling%20remove__%20on%20an%20open%20file).
## Noncompliant Code Example
In this noncompliant code example, the file identified by `file_name` is opened, processed, closed, and removed. However, it is possible that the file object identified by `file_name` in the call to `remove()` is not the same file object identified by `file_name` in the call to `fopen()`.
``` c
char *file_name;
FILE *f_ptr;
/* Initialize file_name */
f_ptr = fopen(file_name, "w");
if (f_ptr == NULL) {
  /* Handle error */
}
/*... Process file ...*/
if (fclose(f_ptr) != 0) {
  /* Handle error */
}
if (remove(file_name) != 0) {
  /* Handle error */
}
```
## Compliant Solution
Not much can be done programmatically to ensure the file removed is the same file that was opened, processed, and closed except to make sure that the file is opened in a secure directory with privileges that would prevent the file from being manipulated by an untrusted user. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
## Noncompliant Code Example (POSIX)
In this noncompliant code example, the function `chmod()` is called to set the permissions of a file. However, it is not clear whether the file object referred to by `file_name` refers to the same object in the call to `fopen()` and in the call to `chmod()`.
``` c
char *file_name;
FILE *f_ptr;
/* Initialize file_name */
f_ptr = fopen(file_name, "w");
if (f_ptr == NULL)  {
  /* Handle error */
}
/* ... */
if (chmod(file_name, S_IRUSR) == -1) {
  /* Handle error */
}
```
## Compliant Solution (POSIX)
This compliant solution uses the POSIX `fchmod()` and `open()` functions \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. Using these functions guarantees that the file opened is the same file that is operated on.
``` c
char *file_name;
int fd;
/* Initialize file_name */
fd = open(
  file_name,
  O_WRONLY | O_CREAT | O_EXCL,
  S_IRWXU
);
if (fd == -1) {
  /* Handle error */
}
/* ... */
if (fchmod(fd, S_IRUSR) == -1) {
  /* Handle error */
}
```
## Mitigation Strategies (POSIX)
Many file-related race conditions can be eliminated by using
-   `fchown()` rather than `chown()`
-   `fstat()` rather than `stat()`
-   `fchmod()` rather than `chmod()`
or simply by ensuring the security of the working directory per [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).
POSIX functions that have no file descriptor counterpart should be used with caution:
-   `link()` and `unlink()`
-   `mkdir()` and `rmdir()`
-   `mount()` and `unmount()`
-   `lstat()`
-   `mknod()`
-   `symlink()`
-   `utime()`
## Risk Assessment
Many file-related vulnerabilities, such as [time-of-check, time-of-use (TOCTOU)](BB.-Definitions_87152273.html#BB.Definitions-TOCTOU) race conditions, can be exploited to cause a program to access an unintended file. Using `FILE` pointers or file descriptors to identify files instead of file names reduces the chance of accessing an unintended file. Remediation costs are medium because, although insecure functions can be easily identified, simple drop-in replacements are not always available.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO01-C | Medium | Likely | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | IO.RACEIO.TAINT.FNAMEBADFUNC.TEMP.*BADFUNC.TMPFILE_SBADFUNC.TMPNAM_S | File System Race ConditionTainted FilenameA collection of warning classes that report uses of library functions associated with temporary file vulnerabilities (including name issues).Use of tmpfile_sUse of tmpnam_s |
| Compass/ROSE |  |  | Can detect some violations of this recommendation. In particular, it warns when chown(), stat(), or chmod() are called on an open file |
| Coverity | 6.5 | TOCTOU | Fully implemented |
| Helix QAC | 2024.4 | C5011 |  |
| Klocwork | 2024.4 | SV.TOCTOU.FILE_ACCESS |  |
| LDRA tool suite | 9.7.1 | 592 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO01-aCERT_C-FIO01-c | Don't use chmod(), chown(), chgrp()Be careful using functions that use file names for identification |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO01-CPP. Be careful using functions that use file names for identification |
| MITRE CWE | CWE-73, External control of file name or pathCWE-367, Time-of-check, time-of-use race condition
CWE-676, Use of potentially dangerous function |

## Bibliography

|  |  |
| ----|----|
| [Apple Secure Coding Guide] | "Avoiding Race Conditions and Insecure File Operations" |
| [Drepper 2006] | Section 2.2.1 "Identification when Opening" |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, fchmodXSH, System Interfaces, open |
| [Seacord 2013] | Chapter 8, "File I/O" |

------------------------------------------------------------------------
[](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152398)
## Comments:

|  |
| ----|
| Is it worth noting that fopen() only provides the bluntest of controls over file permissions and creation and so on, whereas open() provides a lot of control?; Of course, the downside of open() is that it is not part of C99; it is only in POSIX officially.
Is it worth noting that fdopen() provides a way to use open() to open the file but create a file pointer that can be used by the stream I/O functions?  Should there be a recommendation about that, by any chance?  What about deprecating creat() in favour of always using a 3-argument open()?
Should the compliant POSIX solution use 0 in place of the undefined file_mode?  Since there is an explicit fchmod() afterwards, that prevents any non-root process from tampering with the file itself (though there are always questions about renaming etc - which requires directory permission only, even with unreadable files) until the permissions are set explicitly. 
                                        Posted by jonathan.leffler@gmail.com at Mar 17, 2008 23:15
                                     |
| Partial answer: see FIO03.
                                        Posted by jonathan.leffler@gmail.com at Mar 17, 2008 23:36
                                     |
| POSIX also supports fd=fileno(fp) which can be used with stdio streams to access fd-based functions like fchmod.
The only way on a Unix-based system to prevent non-root filename tampering is to protect the directory tree, including turning off the "x" bit.; Check the MDQS spooling system for an example.
                                        Posted by dagwyn at Apr 17, 2008 11:51
                                     |
| The first NCCE appears verbatim in one other rec, so it is somewhat redundant.
I think ROSE will enforce compliance with this rule by preferring fchmod() over chmod() for open files, with similar preferences for other file-related operations.
                                        Posted by svoboda at Jun 22, 2008 09:42
                                     |
| that rec is FIO15-C. Ensure that file operations are performed in a secure directory, the example was copied over there after an email from you.  Should we delete this one even though it is still appropriate?
                                        Posted by avolkovi at Jun 23, 2008 09:18
                                     |
| No, it's OK to have some redundancy where it supports the arguments being made.
                                        Posted by rcs at Jun 23, 2008 09:20
                                     |
| other than catching chmod(), stat(), and chown(), should the ROSE rule do anything else?
                                        Posted by avolkovi at Jul 09, 2008 13:03
                                     |

