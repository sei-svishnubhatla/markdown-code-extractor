Never call a formatted I/O function with a format string containing a [tainted value ](BB.-Definitions_87152273.html#BB.Definitions-taintedvalue).  An attacker who can fully or partially control the contents of a format string can crash a vulnerable process, view the contents of the stack, view memory content, or write to an arbitrary memory location. Consequently, the attacker can execute arbitrary code with the permissions of the vulnerable process \[[Seacord 2013b](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\]. Formatted output functions are particularly dangerous because many programmers are unaware of their capabilities. For example, formatted output functions can be used to write an integer value to a specified address using the `%n` conversion specifier.
## Noncompliant Code Example
The `incorrect_password()` function in this noncompliant code example is called during identification and authentication to display an error message if the specified user is not found or the password is incorrect. The function accepts the name of the user as a string referenced by `user`. This is an exemplar of [untrusted data](BB.-Definitions_87152273.html#BB.Definitions-untrusteddata) that originates from an unauthenticated user. The function constructs an error message that is then output to `stderr` using the C Standard `fprintf()` function.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void incorrect_password(const char *user) {
  int ret;
  /* User names are restricted to 256 or fewer characters */
  static const char msg_format[] = "%s cannot be authenticated.\n";
  size_t len = strlen(user) + sizeof(msg_format);
  char *msg = (char *)malloc(len);
  if (msg == NULL) {
    /* Handle error */
  }
  ret = snprintf(msg, len, msg_format, user);
  if (ret < 0) { 
    /* Handle error */ 
  } else if (ret >= len) { 
    /* Handle truncated output */ 
  }
  fprintf(stderr, msg);
  free(msg);
}
```
The `incorrect_password()` function calculates the size of the message, allocates dynamic storage, and then constructs the message in the allocated memory using the `snprintf()` function. The addition operations are not checked for integer overflow because the string referenced by `user` is known to have a length of 256 or less. Because the `%s` characters are replaced by the string referenced by `user` in the call to `snprintf()`, the resulting string needs 1 byte less than is allocated. The `snprintf()` function is commonly used for messages that are displayed in multiple locations or messages that are difficult to build. However, the resulting code contains a format-string [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) because the `msg` includes untrusted user input and is passed as the format-string argument in the call to `fprintf()`.
## Compliant Solution (`fputs()`)
This compliant solution fixes the problem by replacing the `fprintf()` call with a call to `fputs()`, which outputs `msg` directly to `stderr` without evaluating its contents:
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void incorrect_password(const char *user) {
  int ret;
  /* User names are restricted to 256 or fewer characters */
  static const char msg_format[] = "%s cannot be authenticated.\n";
  size_t len = strlen(user) + sizeof(msg_format);
  char *msg = (char *)malloc(len);
  if (msg == NULL) {
    /* Handle error */
  }
  ret = snprintf(msg, len, msg_format, user);
  if (ret < 0) { 
    /* Handle error */ 
  } else if (ret >= len) { 
    /* Handle truncated output */ 
  }
  fputs(msg, stderr);
  free(msg);
}
```
## Compliant Solution (`fprintf()`)
This compliant solution passes the untrusted user input as one of the variadic arguments to `fprintf()` and not as part of the format string, eliminating the possibility of a format-string vulnerability:
``` c
#include <stdio.h>
void incorrect_password(const char *user) {
  static const char msg_format[] = "%s cannot be authenticated.\n";
  fprintf(stderr, msg_format, user);
}
```
## Noncompliant Code Example (POSIX)
This noncompliant code example is similar to the first noncompliant code example but uses the POSIX function `syslog()` \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] instead of the `fprintf()` function. The `syslog()` function is also susceptible to format-string vulnerabilities.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <syslog.h>
void incorrect_password(const char *user) {
  int ret;
  /* User names are restricted to 256 or fewer characters */
  static const char msg_format[] = "%s cannot be authenticated.\n";
  size_t len = strlen(user) + sizeof(msg_format);
  char *msg = (char *)malloc(len);
  if (msg == NULL) {
    /* Handle error */
  }
  ret = snprintf(msg, len, msg_format, user);
  if (ret < 0) { 
    /* Handle error */ 
  } else if (ret >= len) { 
    /* Handle truncated output */ 
  }
  syslog(LOG_INFO, msg);
  free(msg);
}
```
The `syslog()` function first appeared in BSD 4.2 and is supported by Linux and other modern UNIX implementations. It is not available on Windows systems.
## Compliant Solution (POSIX)
This compliant solution passes the untrusted user input as one of the variadic arguments to `syslog()` instead of including it in the format string:
``` c
#include <syslog.h>
void incorrect_password(const char *user) {
  static const char msg_format[] = "%s cannot be authenticated.\n";
  syslog(LOG_INFO, msg_format, user);
}
```
## Risk Assessment
Failing to exclude user input from format specifiers may allow an attacker to crash a vulnerable process, view the contents of the stack, view memory content, or write to an arbitrary memory location and consequently execute arbitrary code with the permissions of the vulnerable process.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO30-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | ; | Supported via stubbing/taint analysis |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO30 | Partially implemented |
| CodeSonar | 8.3p0 | IO.INJ.FMTMISC.FMT | Format string injectionFormat string |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | TAINTED_STRING | Implemented |
| Cppcheck Premium | 24.11.0
 | premium-cert-fio30-c |  |
| GCC | 4.3.5 |  | Can detect violations of this rule when the -Wformat-security flag is used |
| Helix QAC | 2024.4 | DF4916, DF4917, DF4918 |  |
| Klocwork | 2024.4 | SV.FMTSTR.GENERICSV.TAINTED.FMTSTR |  |
| LDRA tool suite | 9.7.1 | 86 D | Partially Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO30-aCERT_C-FIO30-b
CERT_C-FIO30-c | Avoid calling functions printf/wprintf with only one argument other than string constantAvoid using functions fprintf/fwprintf with only two parameters, when second parameter is a variable
Never use unfiltered data from an untrusted user as the format parameter |
| PC-lint Plus | 1.4 | 592 | Partially supported: reports non-literal format strings |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO30-C | Checks for tainted string format (rule partially covered) |
| PVS-Studio | 7.35 | V618 |  |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Two examples of format-string vulnerabilities resulting from a violation of this rule include [Ettercap](AA.-Bibliography_87152170.html#AA.Bibliography-VU286468) and [Samba](AA.-Bibliography_87152170.html#AA.Bibliography-VU649732).
In Ettercap v.NG-0.7.2, the `ncurses` user interface suffers from a format-string defect. The `curses_msg()` function in `ec_curses.c` calls `wdg_scroll_print()`, which takes a format string and its parameters and passes it to `vw_printw()`. The `curses_msg()` function uses one of its parameters as the format string. This input can include user data, allowing for a format-string vulnerability.
The Samba AFS ACL mapping VFS plug-in fails to properly [sanitize](BB.-Definitions_87152273.html#BB.Definitions-sanitize) user-controlled file names that are used in a format specifier supplied to `snprintf()`. This [security flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) becomes exploitable when a user can write to a share that uses Samba's `afsacl.so` library for setting Windows NT access control lists on files residing on an AFS file system.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT Oracle Secure Coding Standard for Java | IDS06-J. Exclude unsanitized user input from format strings | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Perl Secure Coding Standard | IDS30-PL. Exclude user input from format strings | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Injection [RST] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Including tainted or out-of-domain input in a format string [usrfmt] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-134, Uncontrolled Format String | 2017-05-16: CERT: Exact |
| CWE 2.11 | CWE-20, Improper Input Validation | 2017-05-17: CERT: Rule subset of CWE |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, syslog |
| [Seacord 2013b] | Chapter 6, "Formatted Output" |
| [Viega 2005] | Section 5.2.23, "Format String Problem" |

------------------------------------------------------------------------
[](../c/Rule%2009_%20Input%20Output%20_FIO_) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152343)
## Comments:

|  |
| ----|
| I rewrote this rule because the old formulation was bothering me for a variety of reasons.  Please let me know if you see any problems with this new revision.  Thanks.
                                        Posted by rcs at Mar 30, 2008 09:51
                                     |
| (1) It's actually -2 not -1 (but the wasted byte doesn't hurt).; sizeof counts the terminator too.
(2) The format string should end in newline.
(3) A quicker fix would have been to change fprintf(stderr,msg) to fputs(msg,stderr), which directly addresses the real bug.
                                        Posted by dagwyn at Apr 17, 2008 16:38
                                     |
| (1) fixed
(2) fixed, but I'm not sure the code is portable...should it be \r on Windows?
(3) Added an example that uses fputs as  you suggest. The previous correct example is simpler, but the fputs example illustrates the bugfix better, as you pointed out.
                                        Posted by svoboda at Apr 22, 2008 15:55
                                     |
| I'm not really sure this rule deserves to be a "likely" probability and "low" remediation cost... "probable" probability is better since it is not very common to snprintf() into a buffer before printing... most people will just use printf() from the start instead of dealing with intermediate buffers... also, automatic correction? seems doubtful unless the checker can figure out why a buffer was being used, and why a call to snprintf() followed by printf() is not absolutely necessary
                                        Posted by avolkovi at Jun 09, 2008 11:26
                                     |
| this has been addressed
                                        Posted by avolkovi at Jun 17, 2008 09:42
                                     |
| In the Noncompliant Code Example, sizeof(msg_format) should always return 4 in IA-32 architecture, which is not what you want?
                                        Posted by masaki at Aug 25, 2008 08:22
                                     |
| 
Wow, that was ugly. I think I got it fixed.  Please have another look and let me know if you see any problems.
                                        Posted by rcs at Aug 25, 2008 21:42
                                     |
| The incorrect_password() function constructs by calculating the size of the message...
should be corrected back to something like
The incorrect_password() function constructs msg in dynamically allocated memory by calculating the size of the message...
                                        Posted by masaki at Oct 16, 2008 09:17
                                     |
| I've made this change, thanks.
                                        Posted by svoboda at Oct 22, 2008 12:12
                                     |
| The non-compliant POSIX example has incorrect malloc() error handling.
                                        Posted by tedj at Mar 28, 2018 11:11
                                     |
| Fixed, thanks.
                                        Posted by svoboda at Mar 29, 2018 08:48
                                     |

