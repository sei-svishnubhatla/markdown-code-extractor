The `readlink()` function reads where a link points to. It makes **no** effort to null-terminate its second argument, `buffer`. Instead, it just returns the number of characters it has written.
## Noncompliant Code Example
If `len` is equal to `sizeof(buf)`, the null terminator is written 1 byte past the end of `buf`:
``` c
char buf[1024];
ssize_t len = readlink("/usr/bin/perl", buf, sizeof(buf));
buf[len] = '\0';
```
An incorrect solution to this problem is to try to make `buf` large enough that it can always hold the result:
``` c
long symlink_max;
size_t bufsize;
char *buf;
ssize_t len;
errno = 0;
symlink_max = pathconf("/usr/bin/", _PC_SYMLINK_MAX);
if (symlink_max == -1) {
  if (errno != 0) {
    /* handle error condition */
  }
  bufsize = 10000;
}
else {
  bufsize = symlink_max+1;
}
buf = (char *)malloc(bufsize);
if (buf == NULL) {
  /* handle error condition */
}
len = readlink("/usr/bin/perl", buf, bufsize);
buf[len] = '\0';
```
This modification incorrectly assumes that the symbolic link cannot be longer than the value of `SYMLINK_MAX` returned by `pathconf()`. However, the value returned by `pathconf()` is out of date by the time `readlink()` is called, so the off-by-one buffer-overflow risk is still present because, between the two calls, the location of `/usr/bin/perl` can change to a file system with a larger `SYMLINK_MAX` value. Also, if `SYMLINK_MAX` is indeterminate (that is, if `pathconf()` returned `-1` without setting `errno`), the code uses an arbitrary large buffer size (10,000) that it hopes will be sufficient, but there is a small chance that `readlink()` can return exactly this size.
An additional issue is that `readlink()` can return `-1` if it fails, causing an off-by-one underflow.
## Compliant Solution
This compliant solution ensures there is no overflow by reading in only `sizeof(buf)-1` characters. It also properly checks to see if an error has occurred:
``` c
enum { BUFFERSIZE = 1024 };
char buf[BUFFERSIZE];
ssize_t len = readlink("/usr/bin/perl", buf, sizeof(buf)-1);
if (len != -1) {
  buf[len] = '\0';
}
else {
  /* handle error condition */
}
```
## Risk Assessment
Failing to properly null-terminate the result of `readlink()` can result in abnormal program termination and buffer-overflow vulnerabilities.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS30-C | high | probable | medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Can be checked with appropriate analysis stubs. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS30 |  |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.TBA
MISC.MEM.NTERM.CSTRING | Buffer OverrunTainted Buffer Access
Unterminated C String |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | READLINK | Implemented |
| Helix QAC | 2024.4 | C5033 |  |
| Klocwork | 2024.4 | ABV.GENERALABV.GENERAL.MULTIDIMENSION |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS30-aCERT_C-POS30-b
CERT_C-POS30-c | Avoid overflow due to reading a not zero terminated stringThe values returned by functions 'read' and 'readlink' shall be used
Use of possibly not null-terminated string with functions expecting null-terminated string |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS30-C | Checks for misuse of readlink() (rule partially covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CWE 2.11 | CWE-170, Improper null termination | 2017-06-13: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-170 and POS30-C
CWE-170 = Union( POS30-C, list) where list =
-   Non-null terminated strings fed to functions other than POSIX readlink()
## Bibliography

|  |
| ----|
| [Ilja 2006] |
| [Open Group 1997a] |
| [Open Group 2004] |

------------------------------------------------------------------------
[](../c/Rule%2050_%20POSIX%20_POS_)[](../c/Rule%2050_%20POSIX%20_POS_)[](POS34-C_%20Do%20not%20call%20putenv__%20with%20a%20pointer%20to%20an%20automatic%20variable%20as%20the%20argument)
## Comments:

|  |
| ----|
| How is this rose-possible?
                                        Posted by avolkovi at Jul 21, 2008 14:38
                                     |

