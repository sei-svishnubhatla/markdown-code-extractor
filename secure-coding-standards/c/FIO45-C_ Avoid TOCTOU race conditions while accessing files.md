A TOCTOU (time-of-check, time-of-use) race condition is possible when two or more concurrent processes are operating on a shared file system \[[Seacord 2013b](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\]. Typically, the first access is a check to verify some attribute of the file, followed by a call to use the file. An attacker can alter the file between the two accesses, or replace the file with a symbolic or hard link to a different file. These TOCTOU conditions can be exploited when a program performs two or more file operations on the same file name or path name.
A program that performs two or more file operations on a single file name or path name creates a race window between the two file operations. This race window comes from the assumption that the file name or path name refers to the same resource both times. If an attacker can modify the file, remove it, or replace it with a different file, then this assumption will not hold.
## Noncompliant Code Example
If an existing file is opened for writing with the `w` mode argument, the file's previous contents (if any) are destroyed. This noncompliant code example tries to prevent an existing file from being overwritten by first opening it for reading before opening it for writing. An attacker can exploit the race window between the two calls to `fopen()` to overwrite an existing file.
``` c
#include <stdio.h>
void open_some_file(const char *file) {
  FILE *f = fopen(file, "r");
  if (NULL != f) {
    /* File exists, handle error */
  } else {
    f = fopen(file, "w");
    if (NULL == f) {
      /* Handle error */
    }
    /* Write to file */
    if (fclose(f) == EOF) {
      /* Handle error */
    }
  }
}
```
## Compliant Solution
This compliant solution invokes `fopen()` at a single location and uses the `x` mode of `fopen()`, which was added in C11. This mode causes `fopen()` to fail if the file exists. This check and subsequent open is performed without creating a race window. The `x` mode provides exclusive access to the file only if the host environment provides this support.
``` c
#include <stdio.h>
void open_some_file(const char *file) {
  FILE *f = fopen(file, "wx");
  if (NULL == f) {
    /* Handle error */
  }
  /* Write to file */
  if (fclose(f) == EOF) {
    /* Handle error */
  }
}
```
## Compliant Solution (POSIX)
This compliant solution uses the `O_CREAT` and `O_EXCL` flags of POSIX's `open()` function. These flags cause `open()` to fail if the file exists.
``` c
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
void open_some_file(const char *file) {
  int fd = open(file, O_CREAT | O_EXCL | O_WRONLY);
  if (-1 != fd) {
    FILE *f = fdopen(fd, "w");
    if (NULL != f) {
      /* Write to file */
      if (fclose(f) == EOF) {
        /* Handle error */
      }
    } else {
      if (close(fd) == -1) {
        /* Handle error */
      }
    }
  }
}
```
## Exceptions
**FIO45-C-EX2:** Accessing a file name or path name multiple times is permitted if the file referenced resides in a secure directory. (For more information, see [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
**FIO45-C-EX3:** Accessing a file name or path name multiple times is permitted if the program can verify that every operation operates on the same file.
This POSIX code example verifies that each subsequent file access operates on the same file. In POSIX, every file can be uniquely identified by using its device and i-node attributes. This code example checks that a file name refers to a regular file (and not a directory, symbolic link, or other special file) by invoking `lstat()`. This call also retrieves its device and i-node. The file is subsequently opened. Finally, the program verifies that the file that was opened is the same one (matching device and i-nodes) as the file that was confirmed as a regular file.
An attacker can still exploit this code if they have the ability to delete the benign file and create the malicious file within the race window between lstat() and open(). It is possible that the OS kernel will reuse the same device and i-node for both files. This can be mitigated by making sure that the attacker lacks the permissions to delete the benign file.
``` c
#include <sys/stat.h>
#include <fcntl.h>
int open_regular_file(char *filename, int flags) {
  struct stat lstat_info;
  struct stat fstat_info;
  int f;
  if (lstat(filename, &lstat_info) == -1) {
    /* File does not exist, handle error */
  }
  if (!S_ISREG(lstat_info.st_mode)) {
    /* File is not a regular file, handle error */
  }
  if ((f = open(filename, flags)) == -1) {
    /* File has disappeared, handle error */
  }
  if (fstat(f, &fstat_info) == -1) {
    /* Handle error */
  }
  if (lstat_info.st_ino != fstat_info.st_ino  ||
      lstat_info.st_dev != fstat_info.st_dev) {
    /* Open file is not the expected regular file, handle error */
  }
  /* f is the expected regular open file */
  return f;
}
```
## Risk Assessment
TOCTOU race conditions can result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior), including privilege escalation.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO45-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | IO.RACE | File system race condition |
| Coverity | 2017.07 | TOCTOU | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-fio45-c |  |
| Helix QAC | 2024.4 | DF4851, DF4852, DF4853 |  |
| Klocwork | 2024.4 | SV.TOCTOU.FILE_ACCESS |  |
| LDRA tool suite | 9.7.1 | 75 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO45-a | Avoid race conditions while accessing files |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO45-C | Checks for file access between time of check and use (rule partially covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO45-C).
## Bibliography

|  |  |
| ----|----|
| [Seacord 2013b] | Chapter 7, "Files" |

------------------------------------------------------------------------
[](../c/FIO44-C_%20Only%20use%20values%20for%20fsetpos__%20that%20are%20returned%20from%20fgetpos__) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151937)
## Comments:

|  |
| ----|
| The example in FIO45-EX3 is flawed. Consider this test:$ echo abc >foo && stat foo && echo xyz >bar && rm foo && ln -s bar foo && stat foo  File: ‘foo’
  Size: 4             Blocks: 8          IO Block: 4096   regular file
Device: fd02h/64770d    Inode: 17706253    Links: 1
Access: (0664/-rw-rw-r--)  Uid: ( 1000/  msebor)   Gid: ( 1000/  msebor)
Context: unconfined_u:object_r:user_home_t:s0
Access: 2014-04-04 14:09:50.000780213 -0600
Modify: 2014-04-04 14:09:50.000780213 -0600
Change: 2014-04-04 14:09:50.000780213 -0600
 Birth: -
  File: ‘foo’ -> ‘bar’
  Size: 3            Blocks: 0          IO Block: 4096   symbolic link
Device: fd02h/64770d   Inode: 17706253    Links: 1
Access: (0777/lrwxrwxrwx)  Uid: ( 1000/  msebor)   Gid: ( 1000/  msebor)
Context: unconfined_u:object_r:user_home_t:s0
Access: 2014-04-04 14:09:50.003780171 -0600
Modify: 2014-04-04 14:09:50.003780171 -0600
Change: 2014-04-04 14:09:50.003780171 -0600
 Birth: -

It shows that there is a window between the call to access and open when it's possible to remove the original file operated on by access and replace it with a link to a different file without the `open_regular_file` function detecting the change, thus making it susceptible to the TOCTOU race condition discussed above.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 04, 2014 16:14
\| \|
Fascinating. AFAICT this race exploit works because Martin's script relies on the fact that the malicious foo is created immediately after the benign foo is deleted. Which means the OS is presumably reusing the same inode for both files. IOW the exploit script has its own race window :) It seems to fail if you create a second file between the rm and ln commands, and it fails if you merely move foo rather than delete it.
So the exploit is useless if the attacker is unable to delete the file in question. I've amended the exception to specify this.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 07, 2014 11:08
\| \|
I think we can get rid of our race condition altogether. Wouldn't we just need to get rid of the `lstat()`, call `open()` with `O_NOFOLLOW`, and then check `S_ISREG` on the result of `fstat()` where we currently check `st_dev` and `st_ino`?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 16:13
\| \|
"This can be mitigated by making sure that the attacker lacks the permissions to delete the benign file." Isn't that redundant, since it's equivalent to EX2?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 13:12
\| \|
In this specific code example, yes, we could eliminate the race condition as you suggest. This is because O_NOFOLLOW makes for an operation that both checks (for symlink) and opens the file atomically. There are lots of other tests that you might want to do that cannot be atomically combined with open(). Seeing if the filename ends with ".txt" for instance.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 13:13
\| \|
EX2 is considerably stronger than that. See;[FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory) for our definition of a 'secure directoroy'.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 13:14
\| \|
You can cause a DoS attack by replacing the regular file with a FIFO instead of with a symlink, since opening a FIFO for reading blocks until something else opens it for writing, and vice versa. And in this case, the attack would work even if another file did get created that took the reused inode, since the blocking happens before the inode check.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 13:18
\|
