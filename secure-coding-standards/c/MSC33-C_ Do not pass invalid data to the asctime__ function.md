The C Standard, 7.29.3.1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], provides the following sample implementation of the `asctime()` function:
``` java
char *asctime(const struct tm *timeptr) {
  static const char wday_name[7][3] = {
    "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
  };
  static const char mon_name[12][3] = {
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
  };
  static char result[26];
  sprintf(
    result, 
    "%.3s %.3s%3d %.2d:%.2d:%.2d %d\n",
    wday_name[timeptr->tm_wday],
    mon_name[timeptr->tm_mon],
    timeptr->tm_mday, timeptr->tm_hour,
    timeptr->tm_min, timeptr->tm_sec,
    1900 + timeptr->tm_year
  );
  return result;
}
```
This function is supposed to output a character string of 26 characters at most, including the terminating null character. If we count the length indicated by the format directives, we arrive at 25. Taking into account the terminating null character, the array size of the string appears sufficient.
However, this [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) assumes that the values of the `struct tm` data are within normal ranges and does nothing to enforce the range limit. If any of the values print more characters than expected, the `sprintf()` function may overflow the `result` array. For example, if `tm_year` has the value `12345,` then 27 characters (including the terminating null character) are printed, resulting in a buffer overflow.
The *POSIX<sup>®</sup> Base Specifications* \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] says the following about the `asctime()` and `asctime_r()` functions:
> These functions are included only for compatibility with older implementations. They have undefined behavior if the resulting string would be too long, so the use of these functions should be discouraged. On implementations that do not detect output string length overflow, it is possible to overflow the output buffers in such a way as to cause applications to fail, or possible system security violations. Also, these functions do not support localized date and time formats. To avoid these problems, applications should use `strftime()` to generate strings from broken-down times.

The `asctime()` function appears in the list of obsolescent functions in [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions).
## Noncompliant Code Example
This noncompliant code example invokes the `asctime()` function with potentially unsanitized data:
``` c
#include <time.h>
void func(struct tm *time_tm) {
  char *time = asctime(time_tm);
  /* ... */
}
```
## Compliant Solution (`strftime()`)
The `strftime()` function allows the programmer to specify a more rigorous format and also to specify the maximum size of the resulting time string:
``` c
#include <time.h>
enum { maxsize = 26 };
void func(struct tm *time) {
  char s[maxsize];
  /* Current time representation for locale */
  const char *format = "%c";
  size_t size = strftime(s, maxsize, format, time);
}
```
This call has the same effects as `asctime()` but also ensures that no more than `maxsize` characters are printed, preventing buffer overflow.
## Risk Assessment
On [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) that do not detect output-string-length overflow, it is possible to overflow the output buffers.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC33-C | High | Likely | Low | P27 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MSC33 |  |
| CodeSonar | 8.3p0 | BADFUNC.TIME_H | Use of <time.h> Time/Date Function |
| Cppcheck Premium | 24.11.0 | premium-cert-msc33-c |  |
| Helix QAC | 2024.4 | C5032C++5030 |  |
| Klocwork | 2024.4 | CERT.MSC.ASCTIME |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC33-a | The 'asctime()' and 'asctime_r()' functions should not be used |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC33-C | Checks for use of obsolete standard function (rule partially covered) |
| RuleChecker | 24.04 |  | Supported, but no explicit checker |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | MSC24-C. Do not use deprecated or obsolescent functions | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, asctime |
| [ISO/IEC 9899:2024] | 7.29.3.1, "The asctime Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152219) [](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152283)
## Comments:

|  |
| ----|
| Since asctime is obsolete a la MSC34-C. Do not use deprecated or obsolete functions, does this rule still apply?; Also, the CS probably should not be using the obsolete function and either suggest asctime_s() or just strftime() if Annex K is not implemented for the platform.
                                        Posted by aballman at Aug 19, 2013 10:33
                                     |
| For normal obsolete functions, I would agree...this rule would go. (I am assuming the NCCE becomes fixed if you use asctime_s().)But asctime_s lives in Annex K which is conditionally normative. So if you are on a platform that doesn't implement Annex K, you are stuck with asctime(). So I wouldn't obsolesce this rule just yet. But it should have a CS promoting asctime_s().
                                        Posted by svoboda at Aug 26, 2013 12:17
                                     |

