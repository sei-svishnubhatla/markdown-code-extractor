File operations should be performed in a *secure directory*. In most cases, a secure directory is a directory in which no one other than the user, or possibly the administrator, has the ability to create, rename, delete, or otherwise manipulate files. (Other users may read or search the directory but generally may not modify the directory's contents in any way.) Also, other users must not be able to delete or rename files in the parent of the secure directory and all higher directories, although creating new files or deleting or renaming files they own is permissible.
Performing file operations in a secure directory eliminates the possibility that an attacker might tamper with the files or file system to [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) a file system [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in a program. These vulnerabilities often exist because there is a loose binding between the file name and the actual file. (See [FIO01-C. Be careful using functions that use file names for identification](FIO01-C_%20Be%20careful%20using%20functions%20that%20use%20file%20names%20for%20identification).) In some cases, file operations can be performed securely anywhere. In other cases, the only way to ensure secure file operations is to perform the operation within a secure directory.
Ensuring that file systems are configured in a safe manner is typically a system administration function. However, programs can often check that a file system is securely configured before performing file operations that may lead to security vulnerabilities if the system is misconfigured. There is a slight possibility that file systems will be reconfigured in an insecure manner while a process is running and after the check has been made. As a result, it is always advisable to implement your code in a secure manner (that is, consistent with the other rules and recommendations in this section) even when running in a secure directory.
## Noncompliant Code Example
In this noncompliant code example, the file identified by `file_name` is opened, processed, closed, and removed:
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "w");
if (fp == NULL) {
  /* Handle error */
}
/* ... Process file ... */
if (fclose(fp) != 0) {
  /* Handle error */
}
if (remove(file_name) != 0) {
  /* Handle error */
}
```
An attacker can replace the file object identified by `file_name` with a link to an arbitrary file before the call to `fopen()`. It is also possible that the file object identified by `file_name` in the call to `remove()` is not the same file object identified by `file_name` in the call to `fopen()`. If the file is not in a secure directory, for example, `/tmp/app/tmpdir/passwd`, then an attacker can manipulate the location of the file as follows:
``` java
% cd /tmp/app/ 
% rm -rf tmpdir
% ln -s /etc tmpdir
```
Not much can be done programmatically to ensure the file removed is the same file that was opened, processed, and closed, except to make sure that the file is opened in a secure directory with privileges that would prevent the file from being manipulated by an untrusted user.
## Compliant Solution (POSIX)
This sample [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) of the function `secure_dir()` ensures that the directory `fullpath` and all directories above it are owned by either the user or the superuser and that other users do not have write access to the directories. When checking directories, it is important to traverse from the root to the leaf to avoid a dangerous race condition in which an attacker who has privileges to at least one of the directories can rename and re-create a directory after the privilege verification.
`fullpath` need not be canonicalized (see [FIO02-C. Canonicalize path names originating from tainted sources](FIO02-C_%20Canonicalize%20path%20names%20originating%20from%20tainted%20sources)). If the path contains a symbolic link, this routine recursively invokes itself on the linked-to directory and ensures it is also secure. A symbolically linked directory may be secure if both its source and linked-to directory are secure.
Note that this function is effective only on file systems that are fully compatible with UNIX permissions, and it may not behave normally for file systems with other permission mechanisms, such as AFS (Andrew File System).
``` c
#include <stdlib.h>
#include <limits.h>
#include <string.h>
#include <libgen.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
enum { MAX_SYMLINKS = 5 };
/* Returns nonzero if directory is secure, zero otherwise */
int secure_dir(const char *fullpath) {
  static unsigned int num_symlinks = 0;
  char *path_copy = NULL;
  char **dirs = NULL;
  int num_of_dirs = 1;
  int secure = 1;
  int i, r;
  struct stat buf;
  uid_t my_uid = geteuid();
  size_t linksize;
  char* link;
  if (!fullpath || fullpath[0] != '/') {
    /* Handle error */
  }
  if (num_symlinks > MAX_SYMLINKS) {  /* Could be a symlink loop */
    /* Handle error */
  }
  if (!(path_copy = strdup(fullpath))) {
    /* Handle error */
  }
  /* Figure out how far it is to the root */
  char* path_parent = path_copy;
  for (; ((strcmp(path_parent, "/") != 0) &&
          (strcmp(path_parent, "//") != 0) &&
          (strcmp(path_parent, ".") != 0));
       path_parent = dirname(path_parent)) {
    num_of_dirs++;
  } /* Now num_of_dirs indicates # of dirs we must check */
  free(path_copy);
  path_copy = NULL;
  if (!(dirs = (char **)malloc(num_of_dirs * sizeof(char *)))) {
    /* Handle error */
  }
  if (!(dirs[num_of_dirs - 1] = strdup(fullpath))) {
    /* Handle error */
  }
  if (!(path_copy = strdup(fullpath))) {
    /* Handle error */
  }
  /* Now fill the dirs array */
  path_parent = path_copy;
  for (i = num_of_dirs - 2; i >= 0; i--) {
    path_parent = dirname(path_parent);
    if (!(dirs[i] = strdup(path_parent))) {
      /* Handle error */
    }
  }
  free(path_copy);
  path_copy = NULL;
  /*
   * Traverse from the root to the fullpath,
   * checking permissions along the way.
   */
 for (i = 0; i < num_of_dirs; i++) {
    if (lstat(dirs[i], &buf) != 0) {
      /* Handle error */
    }
    if (S_ISLNK(buf.st_mode)) { /* Symlink, test linked-to file */
      linksize = buf.st_size + 1;
      if (!(link = (char *)malloc(linksize))) {
        /* Handle error */
      }
      r = readlink(dirs[i], link, linksize);
      if (r == -1) {
        /* Handle error */
      } else if (r >= linksize) {
        /* Handle truncation error */
      }
      link[r] = '\0';
      num_symlinks++;
      r = secure_dir(link);
      num_symlinks--;
      if (!r) {
        secure = 0;
        free(link);
        link = NULL;
        break;
      }
      free(link);
      link = NULL;
      continue;
    }
    if (!S_ISDIR(buf.st_mode)) { /* Not a directory */
      secure = 0;
      break;
    }
    if ((buf.st_uid != my_uid) && (buf.st_uid != 0)) {
      /* Directory is owned by someone besides user or root */
      secure = 0;
      break;
    }
    if (buf.st_mode & (S_IWGRP | S_IWOTH)) { /* dir is writable by others */
      secure = 0;
      break;
    }
  }
  for (i = 0; i < num_of_dirs; i++) {
    free(dirs[i]);
    dirs[i] = NULL;
  }
  free(dirs);
  dirs = NULL;
  return secure;
}
```
This compliant solution uses the `secure_dir()` function to ensure that an attacker may not tamper with the file to be opened and subsequently removed. Note that once the path name of a directory has been checked using `secure_dir()`, all further file operations on that directory must be performed using the same path.
``` c
char *dir_name;
const char *file_name = "passwd"; /* File name within the secure directory */
FILE *fp;
/* Initialize dir_name */
if (!secure_dir(dir_name)) {
  /* Handle error */
}
if (chdir(dir_name) == -1) {
  /* Handle error */
}
fp = fopen(file_name, "w");
if (fp == NULL) {
  /* Handle error */
}
/* ... Process file ... */
if (fclose(fp) != 0) {
  /* Handle error */
}
if (remove(file_name) != 0) {
  /* Handle error */
}
```
## Risk Assessment
Failing to perform file I/O operations in a secure directory that cannot otherwise be securely performed can result in a broad range of file system vulnerabilities.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO15-C | Medium | Probable | High | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO15-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO15-CPP. Ensure that file operations are performed in a secure directory |
| MITRE CWE | CWE-379, Creation of temporary file in directory with insecure permissionsCWE-552, Files or directories accessible to external parties |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, dirnameXSH, System Interfaces, realpath |
| [Viega 2003] | Section 2.4, "Determining Whether a Directory Is Secure" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152146) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO17-C_%20Do%20not%20rely%20on%20an%20ending%20null%20character%20when%20using%20fread__)
## Comments:

|  |
| ----|
| 
In most cases, a secure directory is a directory no one other than the user, or possibly the administrator, has the ability to read, write, execute, create, move, delete files or otherwise manipulate files.
Insisting that a a directory is insecure if someone besides yourself & root can read it is impractical. All your toplevel dirs (eg /etc /home, even / itself) are world-readable. I think the above sentence sans "read" is still secure. If you don't want others snooping on your data, a file readable only by you inside a directory that is world-readable, but modifiable only by you & root is IMHO sufficiently secure.
                                        Posted by svoboda at Jun 20, 2008 11:31
                                     |
| David, can you make this change?
                                        Posted by rcs at Jun 20, 2008 13:46
                                     |
| done
                                        Posted by svoboda at Jun 20, 2008 15:27
                                     |
| There is a mismatch between the description and the code.  The description says that other users can't create files in a secure directory, but the secure_dir() function treats directories that have the sticky bit set as secure.  Other users can create files in such directories, they just can't remove or rename existing files.
Either the description or the code needs to change (or both).  Perhaps the best solution would be for the code not to check S_ISVTX for the final directory, only for its parent and above.  This means a directory created within a shared directory that has the sticky bit set (e.g. using mkdtemp() with the template /tmp/fooXXXXXX) would qualify as secure.  The decision on how to fix this problem should also take into account FIO43.
                                        Posted by geoffclare at Jun 23, 2008 04:54
                                     |
| The secure_dir() function should not use realpath() internally.  Checking that the canonicalized pathname is secure does not provide any assurance that the pathname passed to secure_dir() is secure.  (It could traverse a symlink in a world-writable directory).  Instead the caller should first canonicalize the pathname, pass the canonicalized pathname to secure_dir(), and then use the canonicalized pathname in subsequent operations.
                                        Posted by geoffclare at Jun 23, 2008 05:21
                                     |
| fixed
                                        Posted by avolkovi at Jun 23, 2008 09:09
                                     |
| fixed (if I understood you correctly, that is)
                                        Posted by avolkovi at Jun 23, 2008 11:23
                                     |
| I've modified the is_secure() function to handle symbolic links properly. This is important if there are symlinks in common dirs, eg: /home/you -> /usr54/you.  It still requires an absolute path, but the path need not be canonicalized.
                                        Posted by svoboda at Nov 24, 2009 18:37
                                     |
| It appears as if the code to handle symlinks mallocs link but never frees it.
                                        Posted by mjkoo@cmu.edu at Jan 14, 2011 00:51
                                     |
| It also needs to add a null-terminator to link before passing it to secure_dir().
                                        Posted by geoffclare at Jan 14, 2011 05:41
                                     |
| fixed and fixed.
                                        Posted by svoboda at Jan 14, 2011 10:07
                                     |
| Looking at the is_secure_dir code now, I wonder why it bothers to check for the sticky bit? A secure dir, and all its parents are writable only by root or the user. The sticky bit only modifies permissions for dirs like /tmp which allow others to write to it. So AFAICT if the other conditions for secure dir are met, there's no point in checking the sticky bit.
                                        Posted by svoboda at Apr 28, 2011 15:09
                                     |
| See the last part of the first paragraph: "other users must not be able to delete or rename files in the parent of the secure directory and all higher directories, although creating new files, deleting or renaming files they own is permissible".
                                        Posted by geoffclare at Apr 29, 2011 03:10
                                     |
| The changes to secure_dir made by Andrew Keeton removed the sticky bit check. This means the code no longer matches the description of the compliant solution.
Either the sticky bit check should be reinstated in the code, or the description should be updated.
                                        Posted by geoffclare at Aug 17, 2011 07:06
                                     |
| IIRC the sticky bit check was actually not neessary in the code (I remember testing it on Linux). So Andrew took it out of the code and I just took it out of the description.
                                        Posted by svoboda at Aug 17, 2011 11:52
                                     |
| You removed the specific mention of the sticky bit, but the description still does not match the code.  It still talks about doing different permission checks for leaf directories and other directories.
                                        Posted by geoffclare at Aug 18, 2011 04:30
                                     |
| OK, the description should now match the code.
                                        Posted by svoboda at Aug 24, 2011 10:55
                                     |
| J Lewis Muir says, via email:I just wanted to report that the secure_dir function doesn't work for
me when I use it; it crashes trying to free path_copy.  The code seems
broken in that it assigns to path_copy after a strdup in more than one
place and then frees path_copy which will not be the pointer returned by
strdup.  I was able to get it to work by introducing another variable
path_copy_tmp that I used in place of path_copy, thus allowing the free
of path_copy to succeed since it still equals the pointer returned by
strdup.

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 13:03
\| \|
Yes. On many platforms, dirname() returns the argument string, having modified it in-place, and the code relied on this behavior. But this behavior is not guaranteed by the C standard, so the code was not portable. ;I've modified the code as you suggest, so it should be more portable now.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 13:04
\| \|
The added check for `strcmp``(path_parent, ``"."``) != 0` is not needed, as this would only occur for relative pathnames, but the first thing the function does is check that the supplied pathname starts with a '/'.
;
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 27, 2014 13:41
\| \|
agreed, i removed the compare.;
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 27, 2014 13:57
\| \|
I'm wondering if we should add the error handling to the; `secure_dir`() function.  One way to do this would be to equate the inability to determine that directory name is secure with it being insecure and return 0 (fail secure).  Otherways would probably require more extensive changes.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 27, 2014 14:01
\| \|
I added the comparison with `.` to keep my example code from inflooping on my OS 10.9.2 box. Compiled with Clang-500.2.79, this code:
``` java
  char* path_copy = "/etc";
  char* path_parent = path_copy;
  for (; ((strcmp(path_parent, "/") != 0) &&
          (strcmp(path_parent, "//") != 0));
       path_parent = dirname(path_parent)) {
    puts(path_parent);
    num_of_dirs++;
  } /* Now num_of_dirs indicates # of dirs we must check */
```
prints:
``` java
/etc
private/etc
private
.
.
```
This is because /etc is a symlink to /private/etc. And my `dirname(3)` manpage says:
> If path is a null pointer, the empty string, or contains no \`/' characters, dirname() returns a pointer to the string ".", signifying  
> the current directory.

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 15:32
\| \|
ok.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 27, 2014 17:35
\| \|
That's a bug in dirname(), and a nasty one at that. The returned string should always be an initial substring of the input string if the input string starts with a '/'.; I.e. calling dirname("/etc") should return "/" regardless of what "/etc" is.
I can see two possible solutions.
One would be to put something like this inside the loop:
        path_parent = dirname(path_parent))
        if (path_parent[0] != '/')
            abort();  /* should never happen */
The other is to avoid using dirname().  Perhaps this would be best since it's an optional (XSI) function in POSIX anyway.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 28, 2014 06:22
\| \|
The first paragraph distinguishes between the directory (nobody else can write), and parent directories (/tmp style sticky bit directories OK). But secure_dir doesn't seem to implement that distinction.
![](images/icons/contenttypes/comment_16.png) Posted by jheiss at Jan 09, 2020 17:13
\| \|
The description and code do match. They ignore sticky bits (see above discussions), and merely check that directories are owned by the user or root, and no one besides the user and root can modify them.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 10, 2020 09:14
\| \|
The code does ignore sticky bits, and rejects a parent directory like /tmp. But the last sentence of the first paragraph seems to perfectly describe a directory that is world writable with the sticky bit set:
Also, other users must not be able to delete or rename files in the parent of the secure directory and all higher directories, although creating new files or deleting or renaming files they own is permissible.
![](images/icons/contenttypes/comment_16.png) Posted by jheiss at Jan 10, 2020 10:25
\| \|
Correct. The code no longer checks the sticky bit. So while it will report whether a directory is secure or not, it does not handle the additional complexities of the sticky bit.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 10, 2020 13:43
\| \|
Edd04
![](images/icons/contenttypes/comment_16.png) Posted by danteed89 at May 01, 2020 14:13
\|
