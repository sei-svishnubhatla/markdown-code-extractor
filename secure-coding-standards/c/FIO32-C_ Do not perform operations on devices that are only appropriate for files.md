File names on many operating systems, including Windows and UNIX, may be used to access *special files*, which are actually devices. Reserved Microsoft Windows device names include `AUX`, `CON`, `PRN`, `COM1`, and `LPT1` or paths using the `\\.\` device namespace. Device files on UNIX systems are used to apply access rights and to direct operations on the files to the appropriate device drivers.
Performing operations on device files that are intended for ordinary character or binary files can result in crashes and [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service). For example, when Windows attempts to interpret the device name as a file resource, it performs an invalid resource access that usually results in a crash \[[Howard 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Howard02)\].
Device files in UNIX can be a security risk when an attacker can access them in an unauthorized way. For example, if attackers can read or write to the `/dev/kmem` device, they may be able to alter the priority, UID, or other attributes of their process or simply crash the system. Similarly, access to disk devices, tape devices, network devices, and terminals being used by other processes can lead to problems \[[Garfinkel 1996](AA.-Bibliography_87152170.html#AA.Bibliography-Garfinkel96)\].
On Linux, it is possible to lock certain applications by attempting to open devices rather than files. Consider the following example:
``` java
/dev/mouse
/dev/console
/dev/tty0
/dev/zero
```
A Web browser that failed to check for these devices would allow an attacker to create a website with image tags such as `<IMG src="file:///dev/mouse">` that would lock the user's mouse \[[Howard 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Howard02)\].
## Noncompliant Code Example
In this noncompliant code example, the user can specify a locked device or a FIFO (first-in, first-out) file name, which can cause the program to hang on the call to `fopen()`:
``` c
#include <stdio.h>
void func(const char *file_name) {
  FILE *file;
  if ((file = fopen(file_name, "wb")) == NULL) {
    /* Handle error */
  }
  /* Operate on the file */
  if (fclose(file) == EOF) {
    /* Handle error */
  }
}
```
## Compliant Solution (POSIX)
POSIX defines the `O_NONBLOCK` flag to `open()`, which ensures that delayed operations on a file do not hang the program \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
> When opening a FIFO with `O_RDONLY` or `O_WRONLY` set:
>
> -   If `O_NONBLOCK` is set, an `open()` for reading-only returns without delay. An `open()` for writing-only returns an error if no process currently has the file open for reading.
> -   If `O_NONBLOCK` is clear, an `open()` for reading-only blocks the calling thread until a thread opens the file for writing. An `open()` for writing-only blocks the calling thread until a thread opens the file for reading.
>
> When opening a block special or character special file that supports nonblocking opens:
>
> -   If `O_NONBLOCK` is set, the `open()` function returns without blocking for the device to be ready or available; subsequent behavior is device-specific.
> -   If `O_NONBLOCK` is clear, the `open()` function blocks the calling thread until the device is ready or available before returning.
>
> Otherwise, the behavior of `O_NONBLOCK` is unspecified.

Once the file is open, programmers can use the POSIX `lstat()` and `fstat()` functions to obtain information about a file and the `S_ISREG()` macro to determine if the file is a regular file. 
Because the behavior of `O_NONBLOCK` on subsequent calls to `read()` or `write()` is [unspecified](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior), it is advisable to disable the flag after it has been determined that the file in question is not a special device.
When available (Linux 2.1.126+, FreeBSD, Solaris 10, POSIX.1-2008), the `O_NOFOLLOW` flag should also be used. (See [POS01-C. Check for the existence of links when dealing with files](POS01-C_%20Check%20for%20the%20existence%20of%20links%20when%20dealing%20with%20files).) When `O_NOFOLLOW` is not available, symbolic link checks should use the method from [POS35-C. Avoid race conditions while checking for the existence of a symbolic link](POS35-C_%20Avoid%20race%20conditions%20while%20checking%20for%20the%20existence%20of%20a%20symbolic%20link).
``` c
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#ifdef O_NOFOLLOW
  #define OPEN_FLAGS O_NOFOLLOW | O_NONBLOCK
#else
  #define OPEN_FLAGS O_NONBLOCK
#endif
void func(const char *file_name) {
  struct stat orig_st;
  struct stat open_st;
  int fd;
  int flags;
  if ((lstat(file_name, &orig_st) != 0) ||
      (!S_ISREG(orig_st.st_mode))) {
    /* Handle error */
  }
  /* Race window */
  fd = open(file_name, OPEN_FLAGS | O_WRONLY);
  if (fd == -1) {
    /* Handle error */
  }
  if (fstat(fd, &open_st) != 0) {
    /* Handle error */
  }
  if ((orig_st.st_mode != open_st.st_mode) ||
      (orig_st.st_ino  != open_st.st_ino) ||
      (orig_st.st_dev  != open_st.st_dev)) {
    /* The file was tampered with */
  }
  /* 
   * Optional: drop the O_NONBLOCK now that we are sure
   * this is a good file.
   */
  if ((flags = fcntl(fd, F_GETFL)) == -1) {
    /* Handle error */
  }
  if (fcntl(fd, F_SETFL, flags & ~O_NONBLOCK) == -1) {
    /* Handle error */
  }
  /* Operate on the file */
  if (close(fd) == -1) {
    /* Handle error */
  }
}
```
This code contains an intractable [TOCTOU (time-of-check, time-of-use)](BB.-Definitions_87152273.html#BB.Definitions-TOCTOU) race condition under which an attacker can alter the file referenced by `file_name` following the call to `lstat()` but before the call to `open()`. The switch will be discovered after the file is opened, but opening the file cannot be prevented in the case where this action itself causes undesired behavior. (See [FIO45-C. Avoid TOCTOU race conditions while accessing files](FIO45-C_%20Avoid%20TOCTOU%20race%20conditions%20while%20accessing%20files) for more information about TOCTOU race conditions.)
Essentially, an attacker can switch out a file for one of the file types shown in the following table with the specified effect.
###### File Types and Effects

| Type | Note on Effect |
| ----|----|
| Another regular file | The fstat() verification fails. |
| FIFO | Either open() returns -1 and sets errno to ENXIO, or open() succeeds and the fstat() verification fails. |
| Symbolic link | open() returns -1 if O_NOFOLLOW is available; otherwise, the fstat() verification fails. |
| Special device | Usually the fstat() verification fails on st_mode. This can still be a problem if the device is one for which just opening (or closing) it causes a side effect. If st_mode compares equal, then the device is one that, after opening, appears to be a regular file. It would then fail the fstat() verification on st_dev and st_ino (unless it happens to be the same file, as can happen with /dev/fd/* on Solaris, but this would not be a problem). |

To be compliant with this rule and to prevent this TOCTOU race condition, `file_name` must refer to a file in a secure directory. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
## Noncompliant Code Example (Windows)
This noncompliant code example uses the `GetFileType()` function to attempt to prevent opening a special file: 
``` c
#include <Windows.h>
void func(const TCHAR *file_name) {
  HANDLE hFile = CreateFile(
    file_name,
    GENERIC_READ | GENERIC_WRITE, 0, 
    NULL, OPEN_EXISTING,
    FILE_ATTRIBUTE_NORMAL, NULL
  );
  if (hFile == INVALID_HANDLE_VALUE) {
    /* Handle error */
  } else if (GetFileType(hFile) != FILE_TYPE_DISK) {
    /* Handle error */
    CloseHandle(hFile);
  } else {
    /* Operate on the file */
    CloseHandle(hFile);
  }
}
```
Although tempting, the Win32 `GetFileType()` function is dangerous in this case. If the file name given identifies a named pipe that is currently blocking on a read request, the call to `GetFileType()` will block until the read request completes. This provides an effective attack vector for a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) on the application. Furthermore, the act of opening a file handle may cause side effects, such as line states being set to their default voltage when opening a serial device.
## Compliant Solution (Windows)
Microsoft documents a list of reserved identifiers that represent devices and have a device namespace to be used specifically by devices \[[MSDN](http://msdn.microsoft.com/en-us/library/aa365247%28v=vs.85%29.aspx)\]. In this compliant solution, the isReservedName() function can be used to determine if a specified path refers to a device. Care must be taken to avoid a TOCTOU race condition when first testing a path name using the isReservedName() function and then later operating on that path name.
``` c
#include <ctype.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
static bool isReservedName(const char *path) {
  /* This list of reserved names comes from MSDN */
  static const char *reserved[] = {
    "nul", "con", "prn", "aux", "com1", "com2", "com3",
    "com4", "com5", "com6", "com7", "com8", "com9",
    "lpt1", "lpt2", "lpt3", "lpt4", "lpt5", "lpt6",
    "lpt7", "lpt8", "lpt9"
  };
  bool ret = false;
/*
 * First, check to see if this is a device namespace, which
 * always starts with \\.\, because device namespaces are not
 * valid file paths.
 */
  if (!path || 0 == strncmp(path, "\\\\.\\", 4)) {
    return true;
  }
  /* Compare against the list of ancient reserved names */
  for (size_t i = 0; !ret &&
       i < sizeof(reserved) / sizeof(*reserved); ++i) {
   /*
    * Because Windows uses a case-insensitive file system, operate on
    * a lowercase version of the given filename. Note: This ignores
    * globalization issues and assumes ASCII characters.
    */
    if (0 == _stricmp(path, reserved[i])) {
      ret = true;
    }
  }
  return ret;
}
```
## Risk Assessment
Allowing operations that are appropriate only for regular files to be performed on devices can result in [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) or more serious [exploits](BB.-Definitions_87152273.html#BB.Definitions-exploit) depending on the platform.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO32-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  | Could detect some violations of this rule. This rule applies only;to untrusted file name strings, and ROSE cannot tell which strings are trusted and which are not. The best heuristic is to note if there is any verification of the file name before or after the fopen() call. If there is any verification, then the file opening should be preceded by an lstat() call and succeeded by an fstat() call. Although that does not enforce the rule completely, it does indicate that the coder is aware of the lstat-fopen-fstat idiom |
| Cppcheck Premium | 24.11.0 | premium-cert-fio32-c |  |
| Helix QAC | 2024.4 | DF4921, DF4922, DF4923 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO32-a | Protect against file name injection |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO32-C | Checks for inappropriate I/O operation on device files (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | FIO05-C. Identify files using multiple file attributes | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | FIO15-C. Ensure that file operations are performed in a secure directory | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | POS01-C. Check for the existence of links when dealing with files | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | POS35-C. Avoid race conditions while checking for the existence of a symbolic link | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | FIO00-J. Do not operate on files in shared directories | Prior to 2018-01-12: CERT: Unspecified Relationship |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-67 and FIO32-C
FIO32-C = Union( CWE-67, list) where list =
-   Treating trusted device names like regular files in Windows.
-   Treating device names (both trusted and untrusted) like regular files in POSIX
## Bibliography

|  |  |
| ----|----|
| [Garfinkel 1996] | Section 5.6, "Device Files" |
| [Howard 2002] | Chapter 11, "Canonical Representation Issues" |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, open |
| [MSDN] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152197) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151948)
## Comments:

|  |
| ----|
| I'm not sure that this really hits the point: obviously I shouldn't try to do file-esque stuff with the serial port, but isn't the larger point to accept carefully any user input that might name a special file?
If I'm writing a careful system for UNIX/Linux, I may well forbid slashes in any user-entered filename (which forestalls a large amount of write-on-somebody-else's-file shenanigans), but that same code on Windows will allow all the bad stuf (AUX, etc.).
It seems that the advice here (or perhaps somewhere else) is to perform platform-specific sanitization of file inputs even if the path is sanitized.;
                                        Posted by steve at Mar 14, 2008 01:43
                                     |
| It looks like there are two points being attempted here.; The introduction seems to be saying something like "don't fseek() on a keyboard," while the example talks about not giving users access to devices.  It would be better to pick one and run with it.
                                        Posted by dmk at Mar 14, 2008 09:14
                                     |
| Another possible way of jamming up software is to ask it to open a FIFO for reading, say.; Generally, that will block until there is a process that has the FIFO open for writing - and the attacker probably wouldn't provide that process.  That's a simple DoS attack, but it requires an O_NONBLOCK flag to prevent the process being hung in the open() call -- you can't call fstat() until you've got the file descriptor open.
                                        Posted by jonathan.leffler@gmail.com at Mar 19, 2008 02:30
                                     |
| I think this combination is what I was after.  It is mainly an input validation recommendation to be careful to make sure that the file name you are given is not the name of a device, if you are going to perform operations on it that are not appropriate for a device.  Perhaps an fseek() on a keyboard is a good example of a non-compliant coding example.
Anyway, Alex is going to take a look at this on Tuesday.
                                        Posted by rcs at Mar 22, 2008 08:58
                                     |
| Added a non compliant piece of code with a fifo that is easily DoSed
I didn't like the fseek/keyboard example because most systems require root access to access devices, whereas fifos are much more common
Also, it seems like the issue is worst in MS-DOS systems where mucking around with LPT1 can cause a crash, but I'm too unfamiliar with it to give a good example
                                        Posted by avolkovi at Mar 25, 2008 11:24
                                     |
| Updated the compliant solution and eliminated a race condition a la POS01-A
;Not sure what to do about the Windows solution as I don't really understand it
                                        Posted by avolkovi at Mar 25, 2008 11:45
                                     |
| The race condition is troubling.
As I commented elsewhere, very few applications have any business letting the user specify files other than ordinary files that are maintained by the app in its own protected directory.; That completely avoids this problem.
                                        Posted by dagwyn at Apr 17, 2008 16:48
                                     |
| > The race condition is troubling.
Yes, FIO45-C foxues on the race condition.
While disallowing a user from specifying files does avoid the problem, you've just eliminated any app with a file dialog box (although such apps generally will filter out anything they don't explicitly handle...but you get the idea; it's too common a feature to eliminate.
                                        Posted by svoboda at Apr 22, 2008 16:09
                                     |
| Do we really need to be checking before and after the open()? I don't think so... I added the O_NONBLOCK flag, so really we just need to check after the open, and then maybe fcntl() to drop the flag.
so something like:
struct stat stat_info;
int fildes;
int flags;
if (!fgets(filename, sizeof(filename), stdin)) {
  /* handle error */
}
if ((fildes = open(filename, O_NONBLOCK, O_WRONLY)) == -1) {
  /* handle error */
}
if ((fstat(fildes, &stat_info) != 0) || (!S_ISREG(stat_info.st_mode))) {
  /* handle error */
}
/* Optional: drop the O_NONBLOCK now that we are sure this is a good file */
if ((flags = fcntl(fildes, F_GETFL)) == -1) {
  /* handle error */
}
if ((fcntl(fildes, F_SETFL, flags & ~O_NONBLOCK) != 0) {
  /* handle error */
}
/* operate on file */

voila! no race condition
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 15, 2008 10:10
\| \|
The stat-open-fstat mechanism is generally sufficient to prevent race conditions without actually opening the file; that's why we are relying on it here.
If you don't mind opening the file, and then abandoning it, then yes, your code does avoid a race condition. I'm not sure if opening a device file with NONBLOCK is adequate or even possible.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 15, 2008 11:11
\| \|
what about an attacker switching the file out for a link between the stat and open? this would cause the open to block and now we're back to square one and getting DOSed
as far as O_NONBLOCK we have from the manpage:
> This mode need not have any effect on files other than FIFOs.

Why would we need to abandon the file? It seems to me like there are three possibilities
-   the file is regular, we open() with O_NONBLOCK, ensure it is regular, change the flags to allow read/write
-   the file is a FIFO, open() errors out with ENXIO or IS_REG fails, we don't hang since we haven't done any i/o
-   the file is a device, the open succeeds, but IS_REG fails, we don't hang since we haven't done any i/o
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 15, 2008 11:21
\| \|
I think the initial stat() and the O_NONBLOCK are both needed.; Dropping the stat() and just relying on O_NONBLOCK is insufficient because:
1.  POSIX says that open() with O_NONBLOCK doesn't block for a device "that supports non-blocking opens".  This leaves open the possibility that devices can exist which don't support non-blocking opens, and open() would block despite being called with O_NONBLOCK.
2.  Some devices might exist for which just opening it causes something to happen.
3.  Solaris has device files in the /dev/fd directory which, when opened, cause an open file descriptor to be duplicated (as if by dup()).  E.g. open("/dev/fd/3", O_WRONLY) is equivalent to dup(3). Doing an fstat() on the new fd reports the file type of the file that was open on the duplicated fd, not the file type of the /dev/fd/3 file.  Suppose the app has a database open on fd 3, and then opens and writes to an output file.  If the initial stat() is not done and the app can be made to use /dev/fd/3 (or any device file with the same major and minor numbers) as the name of the output file then fstat() will report that the file is a regular file, and the output will be written to the database, corrupting it.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 15, 2008 12:43
\| \|
How do we deal with a race condition between stat and open then?
imagine:
-   check with stat to ensure IS_REG
-   attacker switches out for a link to /dev/fd
-   open()
Would adding O_NOFOLLOW be enough?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 15, 2008 12:56
\| \|
Now we're into territory covered by POS35-C.
There is a certain amount of overlap between the solutions, so perhaps it would make sense to include the appropriate code from each (merged) in both places.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 15, 2008 13:33
\| \|
ok... I believe I have addressed as many of the problems as possible... there is a nice little table now and links to the appropriate POSxx rules
Also, the solution now contains all the elements that we have discussed because each attempts to mitigate a different problem
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 15, 2008 14:04
\| \|
Yes, much improved.; I changed it to use `lstat()` as per POS35-C, and also made some changes to the table.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 16, 2008 05:28
\| \|
this issue has been addressed
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 16, 2008 09:32
\| \|
So the windows solution doesn't actually open the file... it just looks at the file type. If we add the code to open (like we have in the POSIX CS), we'll introduce a TOCTOU...
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 20, 2008 14:48
\| \|
ROSE algorithm says
> ensuring that every fopen() call with a variable as the file name should be preceded by an lstat()

However, almost of our examples involving `fopen()` have a `const char * filename` as the argument... however, that's not a problem since the value is trusted. I believe we need tainting to be able to tell whether the filename came from a user and therefore needs to be vetted by this rule.
In other words, without variable tainting, this is not rose-possible
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 29, 2008 11:21
\| \|
Hm. Determining that a filename is properly checked via lstat/open/fstat is possible, the impossible part is knowing if a filename is trusted or not. Adjusted rose paragraph accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 29, 2008 13:03
\| \|
The Windows solution is opening the file – the call to CreateFile is passing in the OPEN_EXISTING flag – without opening the file, you cannot tell what type of file it is using GetFileType.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 05, 2013 16:20
\|
