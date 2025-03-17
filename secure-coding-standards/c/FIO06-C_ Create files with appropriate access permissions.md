Creating a file with insufficiently restrictive access permissions may allow an unprivileged user to access that file. Although access permissions are heavily dependent on the file system, many file-creation functions provide mechanisms to set (or at least influence) access permissions. When these functions are used to create files, appropriate access permissions should be specified to prevent unintended access.
When setting access permissions, it is important to make sure that an attacker cannot alter them. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
## Noncompliant Code Example (`fopen()`)
The `fopen()` function does not allow the programmer to explicitly specify file access permissions. In this noncompliant code example, if the call to `fopen()` creates a new file, the access permissions are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior):
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "w");
if (!fp){
  /* Handle error */
}
```
### Implementation Details
On POSIX-compliant systems, the permissions may be restricted by the value of the POSIX `umask()` function \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
The operating system modifies the access permissions by computing the intersection of the inverse of the umask and the permissions requested by the process \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\]. For example, if the variable `requested_permissions` contained the permissions passed to the operating system to create a new file, the variable `actual_permissions` would be the actual permissions that the operating system would use to create the file:
``` java
requested_permissions = 0666;
actual_permissions = requested_permissions & ~umask();
```
For OpenBSD and Linux operating systems, any file created will have mode `S_IRUSR|S_IWUSR|S_IRGRP|S_IWGRP|S_IROTH|S_IWOTH` (0666), as modified by the process's umask value. (See [fopen(3)](http://www.openbsd.org/cgi-bin/man.cgi?query=open&apropos=0&sektion=0&manpath=OpenBSD+Current&arch=i386&format=html) in the OpenBSD Manual Pages \[[OpenBSD](AA.-Bibliography_87152170.html#AA.Bibliography-OpenBSD)\].)
## Compliant Solution (`fopen_s()`, C11 Annex K)
The C11 Annex K function `fopen_s()` can be used to create a file with restricted permissions \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
> If the file is being created, and the first character of the mode string is not 'u', to the extent that the underlying system supports it, the file shall have a file permission that prevents other users on the system from accessing the file. If the file is being created and the first character of the mode string is 'u', then by the time the file has been closed, it shall have the system default file access permissions.

The *u* character can be thought of as standing for "umask," meaning that these are the same permissions that the file would have been created with had it been created by `fopen()`. In this compliant solution, the `u` mode character is omitted so that the file is opened with restricted privileges (regardless of the umask):
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
errno_t res = fopen_s(&fp, file_name, "wx");
if (res != 0) {
  /* Handle error */
}
```
On Windows, `fopen_s()` will create the file with security permissions based on the user executing the application. For more controlled permission schemes, consider using the [`CreateFile()`](http://msdn.microsoft.com/en-us/library/windows/desktop/aa363858(v=vs.85).aspx) function and specifying the [`SECURITY_ATTRIBUTES`](http://msdn.microsoft.com/en-us/library/windows/desktop/aa379560(v=vs.85).aspx) parameter.
## Noncompliant Code Example (`open()`, POSIX)
Using the POSIX `open()` function to create a file but failing to provide access permissions for that file may cause the file to be created with overly permissive access permissions. This omission has been known to lead to [vulnerabilities](http://BB.%20Definitions#vulnerability)—for example, [CVE-2006-1174](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-1174).
``` c
char *file_name;
int fd;
/* Initialize file_name */
fd = open(file_name, O_CREAT | O_WRONLY);
/* Access permissions were missing */
if (fd == -1){
  /* Handle error */
}
```
This example also violates [EXP37-C. Call functions with the correct number and type of arguments](EXP37-C_%20Call%20functions%20with%20the%20correct%20number%20and%20type%20of%20arguments).
## Compliant Solution (`open()`, POSIX)
Access permissions for the newly created file should be specified in the third argument to `open()`. Again, the permissions are modified by the value of `umask()`.
``` c
char *file_name;
int file_access_permissions;
/* Initialize file_name and file_access_permissions */
int fd = open(
  file_name,
  O_CREAT | O_WRONLY,
  file_access_permissions
);
if (fd == -1){
  /* Handle error */
}
```
John Viega and Matt Messier also provide the following advice \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\]:
> Do not rely on setting the umask to a "secure" value once at the beginning of the program and then calling all file or directory creation functions with overly permissive file modes. Explicitly set the mode of the file at the point of creation. There are two reasons to do this. First, it makes the code clear; your intent concerning permissions is obvious. Second, if an attacker managed to somehow reset the umask between your adjustment of the umask and any of your file creation calls, you could potentially create sensitive files with wide-open permissions.

## Risk Assessment
Creating files with weak access permissions may allow unintended access to those files.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO06-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.CREATEFILE(customization) | Use of CreateFileCodeSonar's custom checking infrastructure allows users to implement checks such as the following.A check for all uses of fopen().A check for calls to open() with only two arguments.A check for calls to;open() where the third argument does not satisfy some specified requirement. |
| Helix QAC | 2024.4 | C5013 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO06-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO06-CPP. Create files with appropriate access permissions |
| CERT Oracle Secure Coding Standard for Java | FIO01-J. Create files with appropriate access permissions |
| ISO/IEC TR 24772:2013 | Missing or Inconsistent Access Control [XZN] |
| MITRE CWE | CWE-276, Insecure default permissionsCWE-279, Insecure execution-assigned permissions
CWE-732, Incorrect permission assignment for critical resource |

## Bibliography

|  |  |
| ----|----|
| [CVE] |  |
| [Dowd 2006] | Chapter 9, "UNIX 1: Privileges and Files" |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, openXSH, System Interfaces, umask |
| [ISO/IEC 9899:2011] | Subclause K.3.5.2.1, "The;fopen_s Function" |
| [OpenBSD] |  |
| [Viega 2003] | Section 2.7, "Restricting Access Permissions for New Files on UNIX" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152439) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO08-C_%20Take%20care%20when%20calling%20remove__%20on%20an%20open%20file)
## Comments:

|  |
| ----|
|   The fopen() function does not provide a mechanism to specify file access permissions.  In the example below, if the call to fopen() creates a new file, the access permissions for that file will be implementation defined.
While techniquely true, aren't you guaranteed to obey umask if you are on a POSIX-compliant system?  
The compliant code doesn't behave significantly better if the underlying file system is AFS, as UNIX file permissions are, for the most part, not relevant.  I have not information on how much those flags matter in Window's security model.
                                        Posted by hburch at Nov 07, 2006 15:13
                                     |
| Hal's concern is valid for all "modern" filesystems that support Access Control Lists, including: NTFS, HFS, any of the UNIX filesystems that support POSIX ACLs, and AFS.; There is no transparent way to map "modes" onto ACLs or vice versa, though POSIX ACLs make a complex attempt to do so.
                                        Posted by wlf@cert.org at Nov 08, 2006 12:53
                                     |
| I should add that all of the ACL-based filesystem have some automatic ACL propagation policy that extends the idea of umask() to ACLs. That means, that ultimate access to newly created files is influenced both by the creating program and by the existing ACL propagation policy, which is usually a special ACE in the parent directory (this is true for NTFS, HFS, and POSIX ACLs, but it is not true for AFS, which has a cheesier propagation policy).
                                        Posted by wlf@cert.org at Nov 08, 2006 12:56
                                     |
| Is there any merit in recommending that code should always using the 3-argument form of open()?; It avoids the ambiguity, and you can specify 0 as the 3rd argument on read-only open calls.  OTOH, there are likely to be those who don't like that idea - which is why this is a comment/question and not (yet) and edited in item.
Also, are there any Unix-like systems where fopen() permissions are not affected by umask()?  I can't imagine that there are.  What about the alternative - Windows? 
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:18
                                     |
| Arjun Bijanki from MS sez:
> the fopen_s solution will work for Visual Studio 2005/2008.  If you're looking to add a general Windows-compliant solution, then you should mention the CreateFile function, which has built-in support for access restrictions based on the underlying OS security descriptors.  I'm not sure if that's inside or outside the scope of the wiki.

                                        Posted by svoboda at Apr 15, 2008 12:52
                                     |
| In theory, calling open with three arguments is an error unless the third argument is actually required by the spec.
However, the implementation (library) would have trouble testing for the extra argument on most platforms, and anyway why would it bother to do so?
What really should happen is for POSIX to phase over to a non-variadic form of open() that always has the extra argument.
                                        Posted by dagwyn at Apr 17, 2008 12:23
                                     |
| On Windows, fopen (and friends) all gain the same access privileges of the executing code context by default (and do not have documented support for the u mode parameter).; If you want to do anything more fancy than that, you have to drop into the security APIs with ACLs and whatnot.  I think that'd be outside of the scope of this wiki.  If you want to know more though, you will want to look at the SECURITY_ATTRIBUTES parameter of CreateFile; specifically, the SECURITY_DESCRIPTOR portion of it.
                                        Posted by aballman at Jun 06, 2013 09:10
                                     |
| Hm, something like this paragraph prob should go into this rule, if only to say "Consult CreateFile's SECURITY_ATTRIBUTES for how to do this securely on Windows".Windows simply lacks the provisions for having multiple, untrusted users on the filesystem. (FWIW POSIX is also far from secure wrt untrusted users).
                                        Posted by svoboda at Jun 07, 2013 14:40
                                     |
| Actually, I think Windows does very well with multiple, untrusted users on the file system since each user gets independent ACLs to different system resources.; It's an incredibly powerful, though rather complex, system. That being said, I've updated the content to include information about using CreateFile.
                                        Posted by aballman at Jun 07, 2013 14:50
                                     |

