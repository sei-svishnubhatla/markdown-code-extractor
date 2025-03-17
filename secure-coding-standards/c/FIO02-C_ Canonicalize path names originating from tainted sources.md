Path names, directory names, and file names may contain characters that make [validation](BB.-Definitions_87152273.html#BB.Definitions-validation) difficult and inaccurate. Furthermore, any path name component can be a symbolic link, which further obscures the actual location or identity of a file. To simplify file name validation, it is recommended that names be translated into their *canonical* form. Canonicalizing file names makes it much easier to verify a path, directory, or file name by making it easier to compare names.
Because the canonical form can vary between operating systems and file systems, it is best to use operating-system-specific mechanisms for canonicalization.
As an illustration, here is a function that ensures that a path name refers to a file in the user's home directory on POSIX systems:
``` c
#include <pwd.h>
#include <unistd.h>
#include <string.h>
int verify_file(char *const filename) {
  /* Get /etc/passwd entry for current user */
  struct passwd *pwd = getpwuid(getuid());
  if (pwd == NULL) {
    /* Handle error */
    return 0;
  }
  const size_t len = strlen( pwd->pw_dir);
  if (strncmp( filename, pwd->pw_dir, len) != 0) {
    return 0;
  }
  /* Make sure there is only one '/', immediately after homedir */
  if (strrchr( filename, '/') == filename + len) {
    return 1;
  }
  return 0;
}
```
The `verify_file()` function requires that the file name be an absolute path name. Furthermore, it can be deceived if the file name being referenced is actually a symbolic link to a file name not in the users's home directory.
## Noncompliant Code Example
In this noncompliant example, `argv[1]` contains a file name that originates from a [tainted source](BB.-Definitions_87152273.html#BB.Definitions-taintedsource) and is opened for writing. Before this file name is used in file operations, it should be validated to ensure that it refers to an expected and valid file. Unfortunately, the file name referenced by `argv[1]` may contain special characters, such as directory characters, that make [validation](BB.-Definitions_87152273.html#BB.Definitions-validation) difficult if not impossible. Furthermore, any path name component in `argv[1]` may be a symbolic link, resulting in the file name referring to an invalid file even though it passes validation.
If validation is not performed correctly, the call to `fopen()` may result in an unintended file being accessed.
``` c
/* Verify argv[1] is supplied */
if (!verify_file(argv[1]) {
  /* Handle error */
}
if (fopen(argv[1], "w") == NULL) {
  /* Handle error */
}
/* ... */
```
## Compliant Solution (POSIX)
Canonicalizing file names is difficult and involves an understanding of the underlying file system.
The POSIX `realpath()` function can assist in converting path names to their canonical form. According to *Standard for Information Technology—Portable Operating System Interface (POSIX®), Base Specifications, Issue 7* (IEEE Std 1003.1, 2013 Edition) \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\],
> The `realpath()` function shall derive, from the pathname pointed to by `file_name`, an absolute pathname that names the same file, whose resolution does not involve '`.`', '`..`', or symbolic links.

Further verification, such as ensuring that two successive slashes or unexpected special files do not appear in the file name, must be performed. See [Section 4.12, "Pathname Resolution,"](http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap04.html#tag_04_12) of IEEE Std 1003.1, 2013 Edition, for more details on how path name resolution is performed \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
Many manual pages for the `realpath()` function come with an alarming warning, such as this one from the *Linux Programmer's Manual* \[[Linux 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Linux08)\]:
> Avoid using this function. It is broken by design since (unless using the non-standard `resolved_path == NULL` feature) it is impossible to determine a suitable size for the output buffer, `resolved_path`. According to POSIX a buffer of size `PATH_MAX` suffices, but `PATH_MAX` need not be a defined constant, and may have to be obtained using `pathconf(3)`. And asking `pathconf(3)` does not really help, since on the one hand POSIX warns that the result of `pathconf(3)` may be huge and unsuitable for mallocing memory. And on the other hand `pathconf(3)` may return −1 to signify that `PATH_MAX` is not bounded.
>
> The libc4 and libc5 implementation contains a buffer overflow (fixed in libc-5.4.13). As a result, set-user-ID programs like `mount(8)` need a private version.

The `realpath()` function was changed in POSIX.1-2008. Older versions of POSIX allow [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) in situations where the `resolved_name` is a null pointer. The current POSIX revision and many current [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) (led by glibc and Linux) allocate memory to hold the resolved name if a null pointer is used for this argument.
The following statement can be used to conditionally include code that depends on this revised form of the `realpath()` function:
``` java
#if _POSIX_VERSION >= 200809L || defined (linux)
```
Consequently, despite the alarming warnings, it is safe to call `realpath()` with `resolved_name` assigned the value `NULL` (on systems that support it), as shown in this compliant solution:
``` c
char *realpath_res = NULL;
/* Verify argv[1] is supplied */
realpath_res = realpath(argv[1], NULL);
if (realpath_res == NULL) {
  /* Handle error */
}
if (!verify_file(realpath_res) {
  /* Handle error */
}
if (fopen(realpath_res, "w") == NULL) {
  /* Handle error */
}
/* ... */
free(realpath_res);
realpath_res = NULL;
```
It is also safe to call `realpath()` with a non-null `resolved_path` provided that `PATH_MAX` is defined as a constant in `<limits.h>`. In this case, the `realpath()` function expects `resolved_path` to refer to a character array that is large enough to hold the canonicalized path. If `PATH_MAX` is defined, allocate a buffer of size `PATH_MAX` to hold the result of `realpath()`, as shown in this compliant solution:
``` c
char *realpath_res = NULL;
char *canonical_file name = NULL;
size_t path_size = 0;
/* Verify argv[1] is supplied */
path_size = (size_t)PATH_MAX;
if (path_size > 0) {
  canonical_filename = malloc(path_size);
  if (canonical_filename == NULL) {
    /* Handle error */
  }
  realpath_res = realpath(argv[1], canonical_filename);
}
if (realpath_res == NULL) {
  /* Handle error */
}
if (!verify_file(realpath_res) {
  /* Handle error */
}
if (fopen(realpath_res, "w") == NULL ) {
  /* Handle error */
}
/* ... */
free(canonical_filename);
canonical_filename = NULL;
```
Care still must be taken to avoid creating a [time-of-check, time-of-use (TOCTOU)](BB.-Definitions_87152273.html#BB.Definitions-TOCTOU) condition by using `realpath()` to check a file name.
## Noncompliant Code Example (POSIX)
Calling the `realpath()` function with a non-null `resolved_path` when `PATH_MAX` is not defined as a constant is not safe. IEEE Std 1003.1, 2013 Edition \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\], effectively forbids such uses of `realpath()`:
> If *resolved_name* is not a null pointer and {PATH_MAX} is not defined as a constant in the **\<limits.h\>** header, the behavior is undefined.

The rationale from IEEE Std 1003.1, 2013 Edition, explains why this case is unsafe:
> Since *realpath*( ) has no *length* argument, if {PATH_MAX} is not defined as a constant in **\<limits.h\>**, applications have no way of determining how large a buffer they need to allocate for it to be safe to pass to *realpath*( ). A {PATH_MAX} value obtained from a prior *pathconf*( ) call is out-of-date by the time *realpath*( ) is called. Hence the only reliable way to use *realpath*( ) when {PATH_MAX} is not defined in **\<limits.h\>** is to pass a null pointer for *resolved_name* so that *realpath*( ) will allocate a buffer of the necessary size.

`PATH_MAX` can vary among file systems (which is the reason for obtaining it with `pathconf()` and not `sysconf()`). A `PATH_MAX` value obtained from a prior `pathconf()` call can be invalidated, for example, if a directory in the path is replaced with a symlink to a different file system or if a new file system is mounted somewhere along the path.
``` c
char *realpath_res = NULL;
char *canonical_filename = NULL;
size_t path_size = 0;
long pc_result;
/* Verify argv[1] is supplied */
errno = 0;
/* Query for PATH_MAX */
pc_result = pathconf(argv[1], _PC_PATH_MAX);
if ( (pc_result == -1) && (errno != 0) ) {
  /* Handle error */
} else if (pc_result == -1) {
  /* Handle error */
} else if (pc_result <= 0) {
  /* Handle error */
}
path_size = (size_t)pc_result;
if (path_size > 0) {
  canonical_filename = malloc(path_size);
  if (canonical_filename == NULL) {
    /* Handle error */
  }
  realpath_res = realpath(argv[1], canonical_filename);
}
if (realpath_res == NULL) {
  /* Handle error */
}
if (!verify_file(realpath_res) {
  /* Handle error */
}
if (fopen(realpath_res, "w") == NULL) {
  /* Handle error */
}
/* ... */
free(canonical_filename);
canonical_filename = NULL;
```
### Implementation Details (Linux)
The `libc4` and `libc5` implementations of `realpath()` contain a buffer overflow (fixed in libc-5.4.13) \[[VU#743092](AA.-Bibliography_87152170.html#AA.Bibliography-743092)\]. Consequently, programs need a private version of this function in which this issue is known to be fixed.
## Compliant Solution (glibc)
The `realpath()` function can be difficult to use and inefficient. Another solution, available as a GNU extension, is `canonicalize_file_name()`. This function has the same effect as `realpath()`, but the result is always returned in a newly allocated buffer \[[Drepper 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Drepper06)\].
``` c
/* Verify argv[1] is supplied */
char *canonical_filename = canonicalize_file_name(argv[1]);
if (canonical_filename == NULL) {
  /* Handle error */
}
/* Verify file name */
if (fopen(canonical_filename, "w") == NULL) {
  /* Handle error */
}
/* ... */
free(canonical_filename);
canonical_filename = NULL;
```
Because memory is allocated by `canonicalize_file_name()`, the programmer must remember to free the allocated memory.
## Noncompliant Code Example (Windows)
This noncompliant code example uses the Windows function `GetFullPathName()` for canonicalization \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\]:
``` c
/* ... */
enum { INITBUFSIZE = 256 };
DWORD ret = 0;
DWORD new_ret = 0;
char *canonical_filename;
char *new_file;
char *file_name;
/* ... */
file_name = (char *)malloc(strlen(argv[1])+1);
canonical_filename = (char *)malloc(INITBUFSIZE);
if ( (file_name != NULL) && (canonical_filename != NULL) ) {
  strcpy(file_name, argv[1]);
  strcpy(canonical_filename, "");
} else {
  /* Handle error */
}
ret = GetFullPathName(
  file_name,
  INITBUFSIZE,
  canonical_filename,
  NULL
);
if (ret == 0) {
  /* Handle error */
}
else if (ret > INITBUFSIZE) {
  new_file = (char *)realloc(canonical_filename, ret);
  if (new_file == NULL) {
    /* Handle error */
  }
  canonical_filename = new_file;
  new_ret = GetFullPathName(
    file_name,
    ret,
    canonical_filename,
    NULL
  );
  if (new_ret > ret) {
    /*
     * The length of the path changed between calls
     * to GetFullPathName(); handle error.
     */
  }
  else if (new_ret == 0) {
    /* Handle error */
  }
}
if (!verify_file(canonical_filename) {
  /* Handle error */
}
/* Verify file name before using */
```
The `GetFullPathName()` function can be used to eliminate the `..` and `/./` components from a path name, but there are numerous other canonicalization issues that are not addressed by use of `GetFullPathName()`, including universal naming convention (UNC) shares, short (8.3) names, long names, Unicode names, trailing dots, forward slashes, backslashes, short cuts, and so on.
Care also must be taken to avoid creating a [TOCTOU](BB.-Definitions_87152273.html#BB.Definitions-TOCTOU) condition by using `GetFullPathName()` to check a file name.
## Compliant Solution (Windows)
Producing canonical file names for Windows operating systems is extremely complex and beyond the scope of this standard. The best advice is to try to avoid making decisions based on a path, directory, or file name \[[Howard 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Howard02)\]. Alternatively, use operating-system-based mechanisms, such as access control lists (ACLs) or other authorization techniques.
## Risk Assessment
File-related [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) can often be [exploited](BB.-Definitions_87152273.html#BB.Definitions-exploit) to cause a program with elevated privileges to access an unintended file. Canonicalizing a file path makes it easier to identify the reference file object.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO02-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | IO.TAINT.FNAMEBADFUNC.PATH.* | Tainted FilenameA collection of checks that report uses of library functions that require securely-specified path parameters. |
| Compass/ROSE |  |  | Could catch violations of this rule by enforcing that any call to open() or fopen() is preceded by a canonicalization routine—that is, a call to realpath() or canonicalize_file_name(). This call will catch some false positives, as ROSE cannot tell when canonicalization is warranted.;False positives can be reduced (but not eliminated) by only reporting instances of fopen() or open() where the file name string has some other processing done to it. This reflects the fact that canonicalization is only necessary for doing verification based on the file name string |
| Klocwork | 2024.4 | SV.DLLPRELOAD.NONABSOLUTE.DLLSV.TOCTOU.FILE_ACCESS |  |
| LDRA tool suite | 9.7.1 | 85 D | Partially implemented |
| Polyspace Bug Finder | R2024a | CERT C: Rec. FIO02-C | Checks for vulnerable path manipulation (rule fully covered) |

## Related Vulnerabilities
[CVE-2009-1760](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1760) results from a violation of this recommendation. Until version 0.4.13, `libtorrent` attempts to rule out unsafe file paths by checking only against the `".."` string. An attacker can exploit this to access any file on the system by using more complex relative paths \[[xorl 2009](http://xorl.wordpress.com/2009/06/09/cve-2009-1760-libtorrent-arbitrary-file-overwrite/)\].
[CVE-2014-9390](https://access.redhat.com/security/cve/CVE-2014-9390) results from a violation of this recommendation. When git is used on a case-insensitive file system (e.g., NTFS under Windows, HFS+ under Mac OS X), a file named ".Git/config" in the repository would overwrite the user's local ".git/config" file.  This config file can define external commands (e.g., a custom diff utility), and it can lead to arbitrary code execution.  The commit that fixes this vulnerability is <https://github.com/git/git/commit/77933f4449b8d6aa7529d627f3c7b55336f491db>.  The [release notes](https://github.com/git/git/blob/master/Documentation/RelNotes/1.8.5.6.txt) briefly discuss other canonicalization issues, in addition to case-insensitiivity, under Windows and Mac OS X.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO02-CPP. Canonicalize path names originating from untrusted sources |
| CERT Oracle Secure Coding Standard for Java | FIO16-J. Canonicalize path names before validating them |
| ISO/IEC TR 24772:2013 | Path Traversal [EWR] |
| MITRE CWE | CWE-22, Path traversalCWE-23, Relative Path Traversal
CWE-28, Path Traversal: '..\filedir'
CWE-40, Path Traversal: '\\UNC\share\name\' (Windows UNC Share)
CWE-41, Failure to resolve path equivalence
CWE-59, Failure to resolve links before file access (aka "link following")
CWE-73, External control of file name or path |

## Bibliography

|  |  |
| ----|----|
| [Drepper 2006] | Section 2.1.2, "Implicit Memory Allocation" |
| [Howard 2002] | Chapter 11, "Canonical Representation Issues" |
| [Linux 2008] | realpath(3)pathconf(3) |
| [MSDN] | "GetFullPathName Function" |
| [IEEE Std 1003.1:2013] | Section 4.12, "Pathname Resolution"System Interfaces: realpath |
| [Seacord 2013] | Chapter 8, "File I/O" |
| [VU#743092] |  |
| [xorl 2009] | CVE-2009-1760: libtorrent Arbitrary File Overwrite |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152403) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO03-C_%20Do%20not%20make%20assumptions%20about%20fopen__%20and%20file%20creation)
## Attachments:
![](images/icons/bullet_blue.gif) [fio02.c](attachments/87152398/88025673.c) (text/x-csrc)  
## Comments:

|  |
| ----|
| Most applications should not accept pathnames from the user.; If they need to name a file (in a directory assigned to the application) based on a user-supplied text string, instead of canonicalizing it a better approach is to sanitize it (convert to safe characters) or at least validate that only safe characters are used.  Another rule addresses that.
                                        Posted by dagwyn at Apr 17, 2008 12:00
                                     |
| First, I thought we were going to avoid using fopen() to verify the existence of a file.
Second, the code examples need work, because they muddle one important principle: The purpose of realpath() and the other canonicalization functions is to ensure that the filename string can be properly validated using string functions. Putting a "/* validate filename */" before realpath() is the wrong ordering of the code. And there is no point in calling realpath() if your means of validation involve only fopen(), since fopen() works fine on non-canonical paths.
The rose applicability hinges on the presence of string functions on the filename...if no string functions are involved, this rec isn't applicable. I guess rose should hunt for string functions on a filename before fopen, and ensure that realpath() is called before those string functions. But we need more fleshed-out examples to see just what we would be looking for.
                                        Posted by svoboda at Jun 22, 2008 09:36
                                     |
| > First, I thought we were going to avoid using fopen() to verify the existence of a file.
i don't see where fopen() is being used for this purpose.
> Putting a "/* validate filename */" before realpath() is the wrong ordering of the code.

i can't find where we have done this.  in each case, the validate filename comment appears to come after the call to realpath()
the "/* validate filename */" is meant to suggest that some more sophisticate filename validation (not shown) is being performed here.
                                        Posted by rcs_mgr at Jun 22, 2008 09:46
                                     |
| OK, after further studying this rule, I see that I misinterpreted it. The coding examples don't actually have any verification of the files, either string-based or based on fopen()...they are all handled by comments saying  /* Verify file name */
I still think the rule needs to be clearer in that realpath() & co. is meant to canonicalize the filename string so that string-based methods will provide accurate validation methods. For instnace, in verifying that a file indeed lives in the user's home directory. Perhaps a code example demonstrating this would be useful.
At any rate, I need some code example like that so I can estimate the viability of a ROSE checker 
                                        Posted by svoboda at Jun 22, 2008 10:13
                                     |
| It's still not quite right.  The statement
It is important to remember that realpath() only resolves symbolic links and the . and .. special files.
is not true (because it also converts relative paths to absolute).
Also that paragraph is now rather cryptic - it says "Further verification must be performed" and gives a reference to the description of pathname resolution in POSIX, leaving the reader to try and figure out from that description what additional verification it could be alluding to.
                                        Posted by geoffclare at Jun 23, 2008 11:27
                                     |
| ok, just quoted posix straight up and tried to list a few examples of other things to look out for
                                        Posted by avolkovi at Jun 23, 2008 13:49
                                     |
| It's an improvement, but I'm still concerned about this statement:
Further verification, such as ensuring that two successive slashes or unexpected special files do not appear in the file name, must be performed
Why would two successive slashes be a problem?  I assume this is referring to two leading slashes being interpreted in an implementation-defined manner.  This only affects how the pathname is resolved (i.e. where the file it refers to is located).  All file operations still behave the same - for example, the secure_dir() function in FIO15 will still work correctly with such pathnames.  If an application wants to create a file in the user's home directory, disallowing two leading slashes would mean that a user whose home directory begins with two leading slashes would not be able to use the application.
As for "special files", in POSIX this term means device files, which probably isn't what you intended.
Where the CS code example has the comment /* Verify file name */ I assumed this meant some specific check of the file name string should be performed (such as ensuring it begins with the user's home directory).  If there are additional generic checks that are intended here, the code should show them.
                                        Posted by geoffclare at Jun 24, 2008 05:13
                                     |
| Ok, I guess I misunderstood what that comment was for.  We should probably change that sentence to say "further verification to ensure the file matches application defined criteria such as having proper permissions and being in a proper directory" or similar
                                        Posted by avolkovi at Jun 24, 2008 09:26
                                     |
| I'm guessing further issues may include what we would broadly refer to as "equivalence errors".
I don't think anyone would be confused about realpath() checking for permissions or in a proper directory or anything, so I don't think that needs to be discussed here, and probably should not as it would muddle the discussion.
I think the equivalence issues we are worried about here is anything to do with a strcmp() or strncmp() call that may not match correctly because of an equivalent form of the name is used.  
Equivalence issues include:
    Trailing characters
    Single dot directory: /./
    Case sensitivity
    Apple File System Forks
    Leading or trailing white space
    Leading or trailing slash(es)
    Internal space: file(SPACE)name
    Asterisk wildcard: pathname*
                                        Posted by rcs at Jun 24, 2008 10:13
                                     |
| Added a verify_file() function into the examples. This rule should be emphasizing that file name canonicalization is intended to enable one to verify the file name via string processing...that is the file is indeed descended from the directory preceding it in the string (and is not a symlink elsewhere).
                                        Posted by svoboda at Jun 24, 2008 11:25
                                     |
| Looks good.  I removed the references to hard links, since that is a different issue that is dealt with elsewhere.
                                        Posted by geoffclare at Jun 25, 2008 05:59
                                     |
| I have removed the statement "Solaris may return a relative pathname when the path argument is relative."  I believe this was based on a mistake in the realpath(3) man page on older Solaris releases.  The Solaris 8 man page said:
For absolute path names and the relative names whose resolved name  cannot  be  expressed  relatively (for  example,  ../../reldir), it returns the resolved absolute name. For the other relative path names, it returns the resolved relative name.
However, I checked the Solaris 8 source code and found that it did not do that; it always returned an absolute path name (or NULL on error).
The quote above does not appear in the Solaris 10 man page.
                                        Posted by geoffclare at Aug 05, 2008 04:31
                                     |
| The idea of canonicalizing path names may have some inherent flaws and may need to be abandoned.  (One of) the problems is that there is an inherent race condition between the time you create the canonical name, perform the validation, and open the file during which time the canonical path name may have been modified and may no longer be referencing a valid file.
                                        Posted by rcs_mgr at Nov 19, 2009 05:20
                                     |
| Note that strlen() return type is size_t, and strncmp() takes size_t as it's third argument, not unsigned int as used in the examples.
                                        Posted by terrywilson@gmail.com at Oct 29, 2010 00:39
                                     |
| Fixed
                                        Posted by svoboda at Oct 31, 2010 13:36
                                     |
| I am preparing a course in C and C++ secure coding at my University in Italy. I wonder that there is not an easy way to canonicalize a path under Windows environment. Did the authors take into consideration to use PathCchCanonicalize() from <Pathcch.h>? It could be a better option than nothing at all... Microsoft documentation says that itConverts a path string into a canonical form.Note that this function recognizes backslashes (e.g., in "\.."), but it does not recognize slashes (e.g., in "/.."), which are permitted as well in Microsoft file systems. This is apparently a bug, as explained in detail here (May 2020), but it can be worked around by replacing all the "/" with "\" BEFORE calling PathCchCanonicalize(). Microsoft documentation itself says:This function does not convert forward slashes (/) into back slashes (\). With untrusted input, this function by itself, cannot be used to convert paths into a form that can be compared with other paths for sub-path or identity. Callers that need that ability should convert forward to back slashes before using this function.If I don't forget anything, an example of secure code could be the following.wchar_t untrusted_path[] = /* ... */wchar_t canon_path[MAX_PATH];
wchar_t *p = NULL;
do{
   p = wcschr(untrusted_path, L'/');
   if(p) *p = L'\\'; // replacing all / with \
}while(p);
if(PathCchCanonicalize(canon_path, MAX_PATH, untrusted_path) != S_OK) { /* Handle error */ }
FILE* f = fopen(canon_path, "r");
/* ... */

![](images/icons/contenttypes/comment_16.png) Posted by pericle.perazzo at Aug 25, 2020 17:43
\| \|
I'm going to guess that this recommendation predates PathCchCanonicalize(), so it might be a useful addition.
A good canonicalization function must account for all features and idiosyncracies that a filesystem might offer. You have already noted that PathCchCanonicalize() does not handle forward slashes in Windows paths. And the various MS filesystems (NTFS, FAT32, FAT, etc) each have their own idiosyncracies. For example, PathCchCanonicalize() does it handle reserved device names like AUX, COM7, LPT7?
The myriad ways of referring to files in Windows made Michael Howard abandon bundling a canonicalization function into Windows XP. Unless Windows has stopped supporting some of these filesystem features, I'm afraid any canonicalization function will be incomplete in Windows.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 26, 2020 09:36
\|
