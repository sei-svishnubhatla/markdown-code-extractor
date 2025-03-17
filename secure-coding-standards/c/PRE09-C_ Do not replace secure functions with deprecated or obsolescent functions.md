Macros are frequently used in the remediation of existing code to globally replace one identifier with another, for example, when an existing API changes. Although some risk is always involved, this practice becomes particularly dangerous if a function name is replaced with the function name of a deprecated or obsolescent function. Deprecated functions are defined by the C Standard and Technical Corrigenda. Obsolescent functions are defined by [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions).
Although compliance with rule [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions) guarantees compliance with this recommendation, the emphasis of this recommendation is the extremely risky and deceptive practice of replacing functions with less secure alternatives.
## Noncompliant Code Example
The Internet Systems Consortium's (ISC) Dynamic Host Configuration Protocol (DHCP) contained a vulnerability that introduced several potential buffer overflow conditions \[[VU#654390](AA.-Bibliography_87152170.html#AA.Bibliography-VU#654390)\]. ISC DHCP makes use of the `vsnprintf()` function for writing various log file strings; `vsnprintf()` is defined in the Portable Operating System Interface (POSIX<sup>®</sup>), Base Specifications, Issue 7 \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] as well as in the C Standard. For systems that do not support `vsnprintf()`, a C include file was created that defines the `vsnprintf()` function to `vsprintf()`, as shown in this noncompliant code example:
``` c
#define vsnprintf(buf, size, fmt, list) \
vsprintf(buf, fmt, list)
```
The `vsprintf()` function does not check bounds. Consequently, `size` is discarded, creating the potential for a buffer overflow when untrusted data is used.
## Compliant Solution
The solution is to include an implementation of the missing function `vsnprintf()` to eliminate the dependency on external library functions when they are not available. This compliant solution assumes that `__USE_ISOC11` is not defined on systems that fail to provide a `vsnprintf()` implementation:
``` c
#include <stdio.h>
#ifndef __USE_ISOC11
  /* Reimplements vsnprintf() */
  #include "my_stdio.h"
#endif
```
## Risk Assessment
Replacing secure functions with less secure functions is a very risky practice because developers can be easily fooled into trusting the function to perform a security check that is absent. This may be a concern, for example, as developers attempt to adopt more secure functions, such as the C11 Annex K functions, that might not be available on all platforms. (See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).)

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE09-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE09 |  |
| Cppcheck Premium | 24.11.0 | premium-cert-pre09-c |  |
| Helix QAC | 2024.4 | C5003 |  |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE09-C | Checks for:Use of dangerous standard functionInsufficient destination buffer sizeRec. fully covered. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE09-CPP. Do not replace secure functions with less secure functions |
| ISO/IEC TR 24772:2013 | Executing or Loading Untrusted Code [XYS] |
| MITRE CWE | CWE-684, Failure to provide specified functionality |

##  Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, vsnprintf, vsprintf |
| [Seacord 2013] | Chapter 6, "Formatted Output" |
| [VU#654390] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152355) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152293)
## Comments:

|  |
| ----|
| This rule is was tagged 'rose-possible', because, given an ontology of secure functions and less-secure functions, one could identify macros that replaced secure functions with their less-secure counterparts. Other than the bad & good examples, we have no such ontology, and would need to create one before checking this with ROSE.
Currently marked 'unenforceable'.
                                        Posted by svoboda at Jun 17, 2008 12:25
                                     |
| There is a good chance I'll move the table over to a new guideline, MSC34-C.
                                        Posted by rcs at Jul 10, 2009 11:24
                                     |
| The wording of this rule is inconsistent with MSC24-C. In here,;vsnprintf() is shown as safe and allowed. In MSC24-C, it is marked as "Unchecked Obsolescent Function".
                                        Posted by lvella at Oct 08, 2020 07:22
                                     |
| The vsnprintf() function is obsolesced by the vsnprintf_s() function from Annex K in C11 (and newer editions). However, Annex K is conditionally normative...if your platform supports Annex K and general and vsnprintf_s() in particular, use it instead. But if your platform does not support Annex K, you must still use vsnprintf().
                                        Posted by svoboda at Oct 08, 2020 10:30
                                     |

