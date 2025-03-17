When you have a choice of two functions to accomplish the same task, prefer the one with better error checking and reporting.
The following table shows a list of C standard library functions that provide limited or no error checking and reporting along with preferable alternatives:

| Function | Preferable
Alternative | Comments |
| ----|----|----|
| atof | strtod | No error indication, undefined behavior on error |
| atoi | strtol | No error indication, undefined behavior on error |
| atol | strtol | No error indication, undefined behavior on error |
| atoll | strtoll | No error indication, undefined behavior on error |
| rewind | fseek | No error indication, silent failure on error |
| setbuf | setvbuf | No error indication, silent failure on error |
| ctime | asctime/localtime; | Undefined behavior;if localtime fails  |

## Noncompliant Code Example (`atoi()`)
This noncompliant code example converts the string token stored in the static array `buff` to a signed integer value using the `atoi()` function:
``` c
int si;
if (argc > 1) {
  si = atoi(argv[1]);
}
```
The `atoi()`, `atol()`, and `atoll()` functions convert the initial portion of a string token to `int`, `long int`, and `long long int` representation respectively. Except for the behavior on error, they are equivalent as follows:

| Call | Equivalent on Success |
| ----|----|
| atoi(nptr) | (int)strtol(nptr, (char **)NULL, 10) |
| atol(nptr) | strtol(nptr, (char **)NULL, 10) |
| atoll(nptr) | strtoll(nptr, (char **)NULL, 10) |

Unfortunately, `atoi()` and related functions lack a mechanism for reporting errors for invalid values. Specifically, the `atoi()`, `atol()`, and `atoll()` functions
-   Do not need to set `errno` on an error.
-   Have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if the value of the result cannot be represented. (See [undefined behavior 118](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_118) of Annex J of the C Standard.)
-   Return 0 if the string does not represent an integer (which is indistinguishable from a correctly formatted, zero-denoting input string), but the C Standard only specifies the behavior of these functions on success.
See also [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions).
## Compliant Solution (`strtol()`)
The `strtol()`, `strtoll()`, `strtoul()`, and `strtoull()` functions convert a null-terminated byte string to `long int`, `long long int`, `unsigned long int`, and `unsigned long long int` representation respectively.
This compliant solution uses `strtol()` to convert a string token to an integer and ensures that the value is in the range of `int`:
``` c
long sl;
int si;
char *end_ptr;
if (argc > 1) {
  errno = 0;
  sl = strtol(argv[1], &end_ptr, 10);
  if ((sl == LONG_MIN || sl == LONG_MAX)
   && errno != 0)
  {
    perror("strtol error");
  }
  else if (end_ptr == argv[1]) {
    if (puts("error encountered during conversion") == EOF) {
      /* Handle error */
    }
  }
  else if (sl > INT_MAX) {
    printf("%ld too large!\n", sl);
  }
  else if (sl < INT_MIN) {
    printf("%ld too small!\n", sl);
  }
  else if ('\0' != *end_ptr) {
    if (puts("extra characters on input line\n") == EOF) {
      /* Handle error */
    }
  }
  else {
    si = (int)sl;
  }
}
```
Both the noncompliant code example and the compliant solution are taken from [ERR34-C. Detect errors when converting a string to a number](ERR34-C_%20Detect%20errors%20when%20converting%20a%20string%20to%20a%20number).
## Noncompliant Code Example (`rewind()`)
This noncompliant code example sets the file position indicator of an input stream back to the beginning using `rewind()`:
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "r");
if (fp == NULL) {
  /* Handle open error */
}
/* Read data */
rewind(fp);
/* Continue */
```
It is impossible to determine if `rewind()` succeeded.
## Compliant Solution (`fseek()`)
This compliant solution uses `fseek()` instead of `rewind()` and checks to see if the operation succeeded:
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "r");
if (fp == NULL) {
  /* Handle open error */
}
/* Read data */
if (fseek(fp, 0L, SEEK_SET) != 0) {
  /* Handle repositioning error */
}
/* Continue */
```
## Noncompliant Code Example (`setbuf()`)
This noncompliant code example calls `setbuf()` with a `buf` argument of `NULL`:
``` c
FILE *file;
/* Setup file */
setbuf(file, NULL);
/* ... */
```
It is not possible to determine if the call to `setbuf()` succeeded.
### Implementation Details
On 4.2BSD and 4.3BSD systems, `setbuf()` always uses a suboptimal buffer size and should be avoided.
## Compliant Solution (`setvbuf()`)
This compliant solution calls `setvbuf()`, which returns nonzero if the operation failed:
``` c
FILE *file;
char *buf = NULL;
/* Setup file */
if (setvbuf(file, buf, buf ? _IOFBF : _IONBF, BUFSIZ) != 0) {
  /* Handle error */
}
/* ... */
```
## Risk Assessment
Although it is rare for a violation of this rule to result in a security [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), it can easily result in lost or misinterpreted data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR07-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection
This rule in general cannot be detected, although various examples can be detected by simply scanning for functions that have equivalent functions with better error handling.

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bad-function | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ERR07 |  |
| LDRA tool suite | 9.7.1 | 44 S, 593 S, 594 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR07-aCERT_C-ERR07-b | The 'atof', 'atoi', 'atol' and 'atoll' functions from the 'stdlib.h' or 'cstdlib' library should not be usedThe library functions 'rewind', 'setbuf' and 'ctime' should not be used |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| RuleChecker | 24.04 | bad-function | Fully checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT06-C).
## Related Guidelines

|  |  |
| ----|----|
| MITRE CWE | CWE-20, Improper Input ValidationCWE-79, Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
CWE-89, Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
CWE-91, XML Injection (aka Blind XPath Injection)
CWE-94, Improper Control of Generation of Code ('Code Injection')
CWE-114, Process Control
CWE-601, URL Redirection to Untrusted Site ('Open Redirect')
CWE-676, Use of potentially dangerous function |

## Bibliography

|  |  |
| ----|----|
| [Klein 2002] | "Bullet Proof Integer Input Using strtol()" |

------------------------------------------------------------------------
[](../c/ERR06-C_%20Understand%20the%20termination%20behavior%20of%20assert__%20and%20abort__) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](../c/Rec_%2003_%20Expressions%20_EXP_)
## Comments:

|  |
| ----|
| I think we've adopted the solution elsewhere of having a black list of functions such as atoi() for which better functions are available and flagging these invocations.  This is not a complete solution as you state, but it is a partial solution, and if implemented in an extensible manner should be fairly robust in practice.
                                        Posted by rcs at Feb 16, 2009 13:47
                                     |
| Out of curiosity, where is this assertion supported (bullet 3 in Noncompliant Code Example (atoi())):
...the atoi(), atol(), and atoll() functions ... return 0 if the string does not represent an integer... 
AFAICS, the behavior of these functions is only specified on success (Except for the behavior on error, they are equivalent to...).
                                        Posted by martinsebor at Jan 27, 2010 23:20
                                     |
| This page says that:
If the conversion cannot be performed, then atoi() will return zero:
And this page which might be the same source.
The MSDN documentation says:
Each function returns the double, int, __int64, or long value produced by interpreting the input characters as a number. The return value is 0 (for atoi, _atoi64, _wtoi, and _wtoi64), 0L (for atol and _wtol), or 0.0 (for atof and _wtof) if the input cannot be converted to a value of that type. The return value is undefined in case of overflow.
Beats me how converting a string into a number can "overflow".
Probably safer/more correct to say "Some implementations return 0 if the string does not represent an integer but C99 only specifies the behavior of these functions on success"
I would be surprised to learn of an implementation that does anything besides return 0, but obviously this behavior is not guaranteed.
                                        Posted by rcs_mgr at Jan 28, 2010 03:21
                                     |
| I always assumed that overflow during a string-to-int conversion occurs if the string contains a valid mathematical number, but the number is out of range. eg trying to read 100000 into a 16-bit (short) int. I suppose in that case, an implementation of atoi() might return 100000 % 2^16.
                                        Posted by svoboda at Jan 28, 2010 09:03
                                     |
| undefined behavior 113  applies to atof, atoi, atol, and atoll. (Calling strtol is safe and cannot overflow or lead to undefined behavior.)
For atof(nptr), the reason is because the function returns (float)strtod(nptr, (char **)NULL) and the conversion from double to float can cause undefined behavior 16 .
atoi(nptr) returns (int)strtol(nptr, (char **)NULL, 10) so I assume the reason is similar, although rather than undefined behavior when during the conversion from long to int "[...] the value cannot be represented [...] either the result is implementation-defined or an implementation-defined signal is raised." (6.3.1.3, para 3).
As for the various documentation pages promising 0, I'm guessing that's because strtol() is required to return 0 on conversion error so an implementation where atoi(nptr) just returns (int)strtol(nptr, (char **)NULL, 10) a conversion error will return 0. But, as Robert says, the spec doesn't guarantee it.
                                        Posted by martinsebor at Jan 28, 2010 22:13
                                     |
| This rule overlaps with recommendation INT06-C. Use strtol() or a related function to convert a string token to an integer
                                        Posted by rcs at May 04, 2012 13:31
                                     |
| Agreed. We might decide that rec is an instance of this rec...do we have any similar instances of this rec?
                                        Posted by svoboda at May 07, 2012 08:39
                                     |

