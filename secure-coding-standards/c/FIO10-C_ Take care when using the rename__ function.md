The `rename()` function has the following prototype:
``` java
int rename(const char *src_file, const char *dest_file);
```
If the file referenced by `dest_file` exists prior to calling `rename()`, the behavior is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). On POSIX systems, the destination file is removed. On Windows systems, the `rename()` fails. Consequently, issues arise when trying to write portable code or when trying to implement alternative behavior.
# Preserve Existing Destination File
If the desired behavior is to ensure that the destination file is not erased or overwritten, POSIX programmers must implement additional safeguards.
## Noncompliant Code Example (POSIX)
This code example is noncompliant because any existing destination file is removed by `rename()`:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (rename(src_file, dest_file) != 0) {
  /* Handle error */
}
```
## Compliant Solution (POSIX)
If the programmer's intent is not to remove an existing destination file, the POSIX `access()` function can be used to check for the existence of a file \[[IEEE Std 1003.1:2013](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-IEEEStd1003.1-2013)\]. This compliant solution renames the source file only if the destination file does not exist:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (access(dest_file, F_OK) != 0) {
  if (rename(src_file, dest_file) != 0) {
    /* Handle error condition */
  }
} 
else {
  /* Handle file-exists condition */
}
```
This code contains an unavoidable race condition between the call to `access()` and the call to `rename()` and can consequently be safely executed only when the destination file is located within a secure directory. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
On file systems where the program does not have sufficient permissions in the directory to view the file, `access()` may return `-1` even when the file exists. In such cases, `rename()` will also fail because the program lacks adequate permissions to perform the operation.
In situations where the source file is supposed not to be a directory or symbolic link, an alternative solution is to use `link()` to link the source file to the destination file and then use `unlink()` (or `remove()`) to delete the source file. Because `link()` fails if the destination file exists, the need for calling `access()` is avoided. However, this solution has two race conditions related to the source file. First, before calling `link()`, the program must use `lstat()` to check that the source file is not a directory or symbolic link. Second, the source file could change during the time window between the `link()` and the `unlink()`. Consequently, this alternative solution can be safely executed only when the source file is located within a secure directory.
## Compliant Solution (Windows)
On Windows, the [rename()](http://msdn.microsoft.com/en-us/library/zw5t957f(VS.80).aspx) function fails if a
> file or directory specified by `newname` already exists or could not be created (invalid path). \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\]

Consequently, it is unnecessary to explicitly check for the existence of the destination file before calling `rename()`.
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (rename(src_file, dest_file) != 0) {
  /* Handle error */
}
```
# Remove Existing Destination File
If the desired behavior is to ensure that the destination file is erased by the `rename()` operation, Windows programmers must write additional code.
## Noncompliant Code Example (Windows)
If the intent of the programmer is to remove the file referenced by `dest_file` if it exists prior to calling `rename()`, this code example is noncompliant on Windows platforms because `rename()` will fail:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (rename(src_file, dest_file) != 0) {
  /* Handle error */
}
```
## Compliant Solution (Windows)
On Windows systems, it is necessary to explicitly remove the destination file before calling `rename()` if the programmer wants the file to be overwritten and the `rename()` operation to succeed:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (_access_s(dest_file, 0) == 0) {
  if (remove(dest_file) != 0) {
    /* Handle error condition */
  }
}
if (rename(src_file, dest_file) != 0) {
  /* Handle error condition */
}
```
This code contains unavoidable race conditions between the calls to `_access_s()`, `remove()`, and `rename()` and can consequently be safely executed only within a secure directory. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)  Another option would be to use the [MoveFileEx](http://msdn.microsoft.com/en-us/library/windows/desktop/aa365240(v=vs.85).aspx) API and pass in the `MOVEFILE_REPLACE_EXISTING` flag:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (!MoveFileEx(src_file, dest_file, MOVEFILE_REPLACE_EXISTING)) {
  /* Handle error condition */
}
```
Although this code is not portable, it does avoid the race condition when using \_access_s(), `remove()`, and `rename()`.
## Compliant Solution (POSIX)
On POSIX systems, if the destination file exists prior to calling `rename()`, the file is automatically removed:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (rename(src_file, dest_file) != 0) {
  /* Handle error condition */
}
```
# Portable Behavior
A programmer who wants an application to behave the same on any C [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) must first determine what behavior to implement.
## Compliant Solution (Remove Existing Destination File)
This compliant solution ensures that any destination file is portably removed:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
(void)remove(dest_file);
if (rename(src_file, dest_file) != 0) {
  /* Handle error condition */
}
```
This code contains an unavoidable race condition between the call to `remove()` and the call to `rename()` and consequently can be safely executed only within a secure directory. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
The return value of `remove()` is deliberately not checked because it is expected to fail if the file does not exist. If the file exists but cannot be removed, the `rename()` call will also fail, and the error will be detected at that point. This is a valid exception (EXP12-C-EX1) to [EXP12-C. Do not ignore values returned by functions](EXP12-C_%20Do%20not%20ignore%20values%20returned%20by%20functions).
## Compliant Solution (Preserve Existing Destination File)
This compliant solution renames the source file only if the destination file does not exist:
``` c
const char *src_file = /* ... */;
const char *dest_file = /* ... */;
if (!file_exists(dest_file)) {
  if (rename(src_file, dest_file) != 0) {
    /* Handle error condition */
  }
} 
else {
  /* Handle file-exists condition */
}
```
This code contains an unavoidable race condition between the call to `file_exists()` and the call to `rename()` and can consequently be safely executed only within a secure directory. (See [FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory).)
The `file_exists()` function is provided by the application and is not shown here because it must be implemented differently on different platforms. (On POSIX systems, it would use `access()`; on Windows, `_access_s()`; and on other platforms, whatever function is available to test file existence.)
## Risk Assessment
Calling `rename()` has [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) behavior when the new file name refers to an existing file. Incorrect use of `rename()` can result in a file being unexpectedly overwritten or other [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO10-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users can add a custom check for all uses of rename(). |
| Helix QAC | 2024.4 | C5015 |  |
| LDRA tool suite | 9.7.1 | 592 S | Fully Implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO10-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO10-CPP. Take care when using the rename() function |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, access |
| [MSDN] | rename() |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152342) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO11-C_%20Take%20care%20when%20specifying%20the%20mode%20parameter%20of%20fopen__)
## Comments:

|  |
| ----|
| The 'compliant solution' fails to rename the fail when the old file does not exist, and invokes implementation-defined behaviour when it does exist.; The comment after the rename() call implies that the function was supposed to be remove(), but then the rename() is gone altogether.  Please can someone (else) work out what was intended and make the code do what was intended.
The POSIX specification for rename() is fairly clear about what happens when the new name already exists.  That suggests that the wishy-washy system is Windows.
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:43
                                     |
| fopen() can fail for reasons other than the file not existing.
For example it could fail because FOPEN_MAX streams are already open.
Thus the CCE does not actually ensure that the file does not exist.
On POSIX systems the code could check that errno is ENOENT, but the
existence check is not needed on POSIX anyway (because the behaviour
of rename() when "new" exists is well defined in POSIX).
                                        Posted by geoffclare at Apr 04, 2008 12:59
                                     |
| The actual synopsis from C99 is:
int rename(const char *old, const char *new);

I'm wondering if we shouldn't use the same argument names for consistency?
Also "pre-existing" is not a word.... "existing" is fine.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 22, 2008 09:37
\| \|
We can use 'old' and 'new' in the rename decl, but I don't like those names. First they are hard to search for in the text, second, they are often used in prose where they can be confusing, and third 'new' is a reserved keyword in C++.
I hard a hard time understanding the intentions of the programmer in the examples, which is why I did 'pre-existing' and reorganized the rule. Now I understand it, even if others don't ![](images/icons/emoticons/smile.svg) I'm happy as long as the intentions here specify that the issue is about what rename() does when the target / destination / new file already exists prior to the rename.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 22, 2008 09:51
\| \|
I may like `src_file` and `dest_file` as well. If this function was called "move" instead of "rename" these names would have been used.
Calling the second argument `dest_file` allows the explanatory text to refer to the destination file.
If the second argument is called `new`, I think it is harder to refer to the new file in text as this seems more ambiguous.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 22, 2008 10:00
\| \|
Under "This creates issues when trying to write portable code or when trying to implement alternative behavior.", what "alternative behavior" means is not so clear to me. Could it be elaborated a bit more?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Mar 29, 2010 03:56
\| \|
Not sure what the original writer meant, but I'd guess that "trying to implement alternative behavior" means "trying to handle cases where rename() failed".
This rule needs a bit of cleanup work b/c the same code sample appears in the first Windows CS and last POSIX CS and also several NCCEs for Windows and POSIX.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 31, 2010 11:07
\|
