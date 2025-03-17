Invoking `remove()` on an open file is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). Removing an open file is sometimes recommended to hide the names of temporary files that may be prone to attack. (See [FIO21-C. Do not create temporary files in shared directories](FIO21-C_%20Do%20not%20create%20temporary%20files%20in%20shared%20directories).)
In cases requiring the removal of an open file, a more strongly defined function, such as the POSIX `unlink()` function, should be considered. To be strictly conforming and portable, `remove()` should *not* be called on an open file.
## Noncompliant Code Example
This noncompliant code example shows a case where a file is removed while it is still open:
``` c
char *file_name;
FILE *file;
/* Initialize file_name */
file = fopen(file_name, "w+");
if (file == NULL) {
  /* Handle error condition */
}
/* ... */
if (remove(file_name) != 0) {
  /* Handle error condition */
}
/* Continue performing I/O operations on file */
fclose(file);
```
Some [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) will not remove the file specified by `file_name` because the stream is still open.
### Implementation Details
Code compiled for Microsoft Windows prevents the `remove()` call from succeeding when the file is open, meaning that the file link will remain after execution completes.
## Compliant Solution (POSIX)
This compliant solution uses the POSIX `unlink()` function to remove the file. The `unlink()` function is guaranteed to unlink the file from the file system hierarchy but keep the file on disk until all open instances of the file are closed \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
``` c
FILE *file;
char *file_name;
/* Initialize file_name */
file = fopen(file_name, "w+");
if (file == NULL) {
  /* Handle error condition */
}
if (unlink(file_name) != 0) {
  /* Handle error condition */
}
/* Continue performing I/O operations on file */
fclose(file);
```
Note that there is a race window between the `fopen()` call and the `unlink()` call, which could be exploited. This exploitation can be mitigated if the operations occur in a secure directory; see [FIO45-C. Avoid TOCTOU race conditions while accessing files](FIO45-C_%20Avoid%20TOCTOU%20race%20conditions%20while%20accessing%20files) for more information.
## Risk Assessment
Calling `remove()` on an open file has different implications for different implementations and may cause [abnormal termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) if the removed file is written to or read from, or it may result in unintended information disclosure from files not deleted as intended.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO08-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users can implement a custom check for calls to remove() on a file that is currently open. |
| Compass/ROSE |  |  |  |
| Helix QAC | 2024.4 | C5014 |  |
| LDRA tool suite | 9.7.1 | 81 D | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO08-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO08-CPP. Take care when calling remove() on an open file |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | unlink() |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152391) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152342)
## Comments:

|  |
| ----|
| We must be careful to explain this because unlinking an open file is very commonly recommended as a security feature of UNIX and is widely used to that effect. We don't want to be making recommendations against practices that are widely regarded as good security practices without careful explanation under exactly which conditions our recommendation should be preferred over the existing security practice.
                                        Posted by wlf@cert.org at Apr 30, 2007 07:59
                                     |
| I agree with what William Fithen said.  In fact, we suggest doing just that in FI039-C. Create temporary files securely.
Update content to acknowledge unlink() as well.  remove() is ISO while unlink() is POSIX, so remove() can remain the focus, but many people still use unlink().
Minor:
    Fix the rule name is risk assessment.
    Add link to 7.9.14.1 of C standard.
    Add a reference to the man page to say which manual page that comes from (GNU, Cygwin, Sun, whomever is responsible).  I'm certain there's multiple man pages for unlink (on one of my systems, there's two).
                                        Posted by hburch at Apr 30, 2007 08:59
                                     |
| I believe the unlink() example is still subject to a race condition...the unlink() function could fail if an attacker moves the file elsewhere b/f the unlink() call but after fopen().
I presume the suggestion to use unlink() exists b/c unlink() is guaranteed to work on open files while remove() is not, n'est-ce pas?
                                        Posted by svoboda at Sep 03, 2008 12:13
                                     |

