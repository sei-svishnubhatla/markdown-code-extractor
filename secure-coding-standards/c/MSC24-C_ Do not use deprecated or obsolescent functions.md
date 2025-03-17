Do not use deprecated or obsolescent functions when more secure equivalent functions are available. Deprecated functions are defined by the C Standard. Obsolescent functions are defined by this recommendation.
### Deprecated Functions
The `gets()` function was deprecated by Technical Corrigendum 3 to C99 and eliminated from C11.  The Annex K `gets_s()` function is a recommended alternative to `gets()`.
### Obsolescent Functions
Functions in the first column of the following table are hereby defined to be *obsolescent functions*. To remediate invocations of obsolescent functions, an application might use inline coding that, in all respects, conforms to this guideline, or an alternative library that, in all respects, conforms to this guideline, or alternative *non-obsolescent functions*.

| Obsolescent 
Function | Recommended 
Alternative | Rationale |
| ----|----|----|
| asctime() | asctime_s() | Non-reentrant |
| atof() | strtod() | No error detection |
| atoi() | strtol() | No error detection |
| atol() | strtol() | No error detection |
| atoll() | strtoll() | No error detection |
| ctime() | ctime_s() | Non-reentrant |
| fopen() | fopen_s() | No exclusive access to file |
| freopen() | freopen_s() | No exclusive access to file |
| rewind() | fseek() | No error detection |
| setbuf() | setvbuf() | No error detection |

The `atof``()``, atoi``()``, atol``()`, and `atoll``()` functions are obsolescent because the `strtod``()``, strtof``()``, strtol``()``, strtold``()``, strtoll``()``, strtoul``()`, and `strtoull``()` functions can emulate their usage and have more robust error handling capabilities. See [INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs](INT05-C_%20Do%20not%20use%20input%20functions%20to%20convert%20character%20data%20if%20they%20cannot%20handle%20all%20possible%20inputs).
The `fopen``()` and `freopen``()` functions are obsolescent because the `fopen_s``()` and `freopen_s``()` functions can emulate their usage and improve security by protecting the file from unauthorized access by setting its file protection and opening the file with exclusive access \[[ISO/IEC WG14 N1173](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECWG14N1173)\].
The `setbuf``()` function is obsolescent because `setbuf``()` does not return a value and can be emulated using `setvbuf``()`. See [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't).
The `rewind``()` function is obsolescent because `rewind``()` does not return a value and can be emulated using `fseek``()`. See [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't).
The `asctime``()` and `ctime``()` functions are obsolescent because they use non-reentrant static buffers and can be emulated using `asctime_s``()` and `ctime_s``()`.
### Unchecked Obsolescent Functions
If you are using platforms that support Annex K, then functions in the first column of the following table are hereby defined to be *obsolescent functions, with functions in the second column being the recommended alternatives from Annex K.*

| Obsolescent 
Function | Recommended 
Alternative |
| ----|----|
| bsearch() | bsearch_s() |
| fprintf() | fprintf_s() |
| fscanf() | fscanf_s() |
| fwprintf() | fwprintf_s() |
| fwscanf() | fwscanf_s() |
| getenv() | getenv_s() |
| gmtime() | gmtime_s() |
| localtime() | localtime_s() |
| mbsrtowcs() | mbsrtowcs_s() |
| mbstowcs() | mbstowcs_s() |
| memcpy() | memcpy_s() |
| memmove() | memmove_s() |
| printf() | printf_s() |
| qsort() | qsort_s() |
| scanf() | scanf_s() |
| snprintf() | snprintf_s() |
| sprintf() | sprintf_s() |
| sscanf() | sscanf_s() |
| strcat() | strcat_s() |
| strcpy() | strcpy_s() |
| strerror() | strerror_s() |
| strlen() | strnlen_s() |
| strncat() | strncat_s() |
| strncpy() | strncpy_s() |
| strtok() | strtok_s() |
| swprintf() | swprintf_s() |
| swscanf() | swscanf_s() |
| vfprintf() | vfprintf_s() |
| vfscanf() | vfscanf_s() |
| vfwprintf() | vfwprintf_s() |
| vfwscanf() | vfwscanf_s() |
| vprintf() | vprintf_s() |
| vscanf() | vscanf_s() |
| vsnprintf() | vsnprintf_s() |
| vsprintf() | vsprintf_s() |
| vsscanf() | vsscanf_s() |
| vswprintf() | vswprintf_s() |
| vswscanf() | vswscanf_s() |
| vwprintf() | vwprintf_s() |
| vwscanf() | vwscanf_s() |
| wcrtomb() | wcrtomb_s() |
| wcscat() | wcscat_s() |
| wcscpy() | wcscpy_s() |
| wcslen() | wcsnlen_s() |
| wcsncat() | wcsncat_s() |
| wcsncpy() | wcsncpy_s() |
| wcsrtombs() | wcsrtombs_s() |
| wcstok() | wcstok_s() |
| wcstombs() | wcstombs_s() |
| wctomb() | wctomb_s() |
| wmemcpy() | wmemcpy_s() |
| wmemmove() | wmemmove_s() |
| wprintf() | wprintf_s() |
| wscanf() | wscanf_s() |

For information on the `tmpfile()` and `tmpfile_s()` functions, see [FIO21-C. Do not create temporary files in shared directories](FIO21-C_%20Do%20not%20create%20temporary%20files%20in%20shared%20directories).  
For information on the `memset()` and `memset_s()` functions, see [MSC06-C. Beware of compiler optimizations](MSC06-C_%20Beware%20of%20compiler%20optimizations).
To remediate invocations of obsolescent functions, an application might use any of the following recommended functions from ISO/IEC TR 24731-2, Extensions to the C Library—Part II: Dynamic Allocation Functions \[[ISO/IEC TR 24731-2](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\]:

|  |  |  |  |  |  |  |
| ----|----|----|----|----|----|----|
| asprintf | aswprintf | fmemopen | fscanf | fwscanf | getdelim | getline |
| getwdelim | getwline | open_memstream | open_wmemstream | strdup | strndup |  |

## Noncompliant Code Example
In this noncompliant code example, the obsolescent functions `strcat()` and `strcpy()` are used:
``` java
#include <string.h>
#include <stdio.h>
enum { BUFSIZE = 32 };
void complain(const char *msg) {
  static const char prefix[] = "Error: ";
  static const char suffix[] = "\n";
  char buf[BUFSIZE];
  strcpy(buf, prefix);
  strcat(buf, msg);
  strcat(buf, suffix);
  fputs(buf, stderr);
}
```
## Compliant Solution
In this compliant solution, `strcat()` and `strcpy()` are replaced by `strcat_s()` and `strcpy_s()`:
``` c
#define __STDC_WANT_LIB_EXT1__
#include <string.h>
#include <stdio.h>
enum { BUFFERSIZE = 256 };
void complain(const char *msg) {
  static const char prefix[] = "Error: ";
  static const char suffix[] = "\n";
  char buf[BUFFERSIZE];
  strcpy_s(buf, BUFFERSIZE, prefix);
  strcat_s(buf, BUFFERSIZE, msg);
  strcat_s(buf, BUFFERSIZE, suffix);
  fputs(buf, stderr);
}
```
## Risk Assessment
The deprecated and obsolescent functions enumerated in this guideline are commonly associated with software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC24-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stdlib-use-atostdlib-macro-atostdlib-use-atollstdlib-macro-atoll | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MSC24 | Fully implemented |
| CodeSonar | 8.3p0 | BADFUNC.*
(customization) | A number of CodeSonar's "Use of *" checks are for deprecated/obsolescent functionsCodeSonar also provides a mechanism for users to create custom checks for uses of specified functions |
| ECLAIR | 1.2 | CC2.MSC34 | Fully implemented |
| LDRA tool suite | 9.7.1 | 44 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC24-aCERT_C-MSC24-b
CERT_C-MSC24-c
CERT_C-MSC24-d | The 'atof', 'atoi', 'atol' and 'atoll' functions from the 'stdlib.h' or 'cstdlib' library should not be usedThe 'getenv()' function from the 'stdlib.h' or 'cstdlib' library shall not be used
Avoid using unsafe string functions which may cause buffer overflows
Don't use unsafe C functions that do write to range-unchecked buffers |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC24-C | Checks for use of obsolete standard function (rec. fully covered) |
| PVS-Studio | 7.35 | V513, V2001, V2002 |  |
| RuleChecker | 24.04 | stdlib-use-atostdlib-macro-atostdlib-use-atollstdlib-macro-atoll | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC34-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | ERR07-C. Prefer functions that support error checking over equivalent functions that don'tINT05-C. Do not use input functions to convert character data if they cannot handle all possible inputsERR34-C. Detect errors when converting a string to a number
STR06-C. Do not assume that strtok() leaves the parse string unchanged
STR07-C. Use the bounds-checking interfaces for string manipulation |
| ISO/IEC TR 24772 | ;Use of Libraries [TRJ] |
| MISRA C:2012 | Rule 21.3 (required) |
| MITRE CWE | CWE-20, Insufficient input validationCWE-73, External control of file name or path
CWE-79, Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
CWE-89, Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
CWE-91, XML Injection (aka Blind XPath Injection)
CWE-94, Improper Control of Generation of Code ('Code Injection')
CWE-114, Process Control
CWE-120, Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
CWE-192, Integer coercion error
CWE-197, Numeric truncation error
CWE-367, Time-of-check, time-of-use race condition
CWE-464, Addition of data structure sentinel
CWE-601, URL Redirection to Untrusted Site ('Open Redirect')
CWE-676, Use of potentially dangerous function |

## Bibliography

|  |  |
| ----|----|
| [Apple 2006] | Apple Secure Coding Guide, "Avoiding Race Conditions and Insecure File Operations" |
| [Burch 2006] | Specifications for Managed Strings, Second Edition |
| [Drepper 2006] | Section 2.2.1 "Identification When Opening" |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, open |
| ISO/IEC 23360-1:2006 |  |
| [ISO/IEC WG14 N1173] | Rationale for TR 24731 Extensions to the C Library Part I: Bounds-checking interfaces |
| [Klein 2002] | "Bullet Proof Integer Input Using strtol()" |
| [Linux 2008] | strtok(3) |
| [Seacord 2013] | Chapter 2, "Strings"Chapter 8, "File I/O" |
| [Seacord 2005b] | "Managed String Library for C, C/C++" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152033) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=155615412)
## Comments:

|  |
| ----|
| 
Do not use deprecated or obsolsecent functions when more secure equivalent functions are available.
What happens when more secure equivalent functions are not available? Does this imply that legacy systems can continue to use deprecated functions? 
                                        Posted by dmohindr at Sep 24, 2009 14:28
                                     |
| It seems to me that we should either list the equivalent secure function for each of the obsolescent functions or show code that can achieve the corresponding effect. Without it, this rule is likely to be dismissed as impractical.
It's not clear to me that this is feasible for all the functions on the list. In particular, I'm not sure how to do that for remove() and rename() neither of which appears to have a secure alternative in TR 24731 or a portable equivalent.
I've expanded the table to list portable alternatives and secure equivalents.
                                        Posted by martinsebor at Jun 20, 2010 17:01
                                     |
| The remove() and rename() functions have no secure equivalents. Their inherent problem is that they operate on file names, allowing a TOCTOU race condition on file names. 
Most other filename-related functions eliminate TOCTOU by replacement functions that operate on file descriptors...chmod() vs fchmod() for instance. (in POSIX). This is possible because chmod() manipulates information in the file's inode...if it has that, it doesn't need the name.   The rename() and remove() functions need the file's name...the inode info won't cut it.
I think the current best advice is to go ahead & use remove() / rename() but only when in a secure directory...outside of a secure directory you can't prevent TOCTOU race conditions. I think we have other rules about these functions...if we don't, we should   So I would agree those functions don't belong here.
                                        Posted by svoboda at Jun 21, 2010 17:27
                                     |
| Why is strlen() not among the list of obsolescent functions?
    Calling strlen() on a non-NTBS can cause an out-of-bounds read. Quite possible if a NTBS gets corrupted, say, by a bad call to strncpy().
    C1x Annex K provides strnlen_s() (from TR24731-1) which mitigates this problem.
                                        Posted by svoboda at Oct 06, 2010 09:48
                                     |
| This rule needs a ton of work, including compliant solutions.
                                        Posted by rcs at May 08, 2012 09:18
                                     |
| Three of the Compliant Solutions in this rule do not have code examples.
                                        Posted by lallierc at Apr 10, 2013 17:00
                                     |
| The mkostemp() function is a glibc extension, with pros and cons (but it is not standardized in POSIX). Creation of temporary files is thoroughly addressed in FIO43-C. Do not create temporary files in shared directories, and I'd rather not duplicate the wisdom of that rule here. I suggest we simply take out the NCCEs that deal with temporary files.
                                        Posted by svoboda at May 01, 2013 10:22
                                     |
| I agree David.; Please take out or replace the NCCEs that you believe are redundant and I will see what remains to be done.
                                        Posted by bugseng at May 01, 2013 12:26
                                     |
| I took out all the NCCEs except for the first one, as they are better demonstrated in rules specific to those functions.;
                                        Posted by svoboda at May 01, 2013 12:44
                                     |
| Would it make sense to list strtok and wcstok under the list of obsolete functions due to their lack of re-entrancy?; The _s versions of those functions solve the problem.Is there meant to be a relationship between the top two tables in unchecked obsolete functions?  I notice there are entries in the second table that do not have an analogy in the first (such as abort_handler_s).
                                        Posted by aballman at Sep 20, 2013 13:34
                                     |
| I have a pretty big question about abort_handler_s appearing in the second table as well.; I would think that these tables should be combined, with the obsolete function on the left and the replacement function on the right. 
                                        Posted by rcs at Oct 29, 2013 04:36
                                     |
| ;I'm still confused as to why there are there are two categories of obsolescent functions.  Shouldn't we combine them?
                                        Posted by rcs at Oct 29, 2013 05:00
                                     |
| Yes, I think the two tables should be combined, eliminating entries like abort_handler_s.
                                        Posted by bluepilot at Oct 29, 2013 08:10
                                     |
| I agree, they should be combined.
                                        Posted by aballman at Oct 29, 2013 09:27
                                     |
| It seems a bit harsh to call functions "obsolescent" just because they have an Annex K replacement. Annex K is optional to implement, and since it was so poorly received, none of the mainstream Linux C libraries support it.
                                        Posted by jcsible at Jun 30, 2020 12:16
                                     |
| During the implementation of this check in clang-tidy, a few things came up that I would like to share. Most of it is just reiteration of previous comments.The two lists in 'Unchecked Obsolescent Functions' are inconsistent. Missing functions:;tmpfile/tmpfile_s, tmpnam/tmpnam_s, memset/memset_s, scanf, strlen, wcslen. There are functions in the second list which are not replacement functions: abort_handler_s, set_constraint_handler_s, strerrorlen_s.I think it would be much easier to comprehend the rule if there was only one list, containing the pairs unsafe function/replacement function, maybe the rationale.Calling these functions obsolescent could be confusing. Maybe it would be better call them unsafe, with possible safe replacements in modern versions of C.
                                        Posted by futogergely at Jan 04, 2022 03:49
                                     |
| Thank you for the feedback.I revamped the table into an 'obsolescent functions' vs 'Annex K alternatives' as you suggest. I also added scanf & scanf_s to the table, their omission seems to have been an oversight. I also added strlen & wcslen, although their Annex K equivalents are slightly differently names. (Note that ISO C defines no strnlen or strlen_s or wcsnlen or wcslen_s functions).At this point, "obsolescent functions" is not a standard term used by ISO C, so we can use it. While it is imperfect and vague, I don't see that vague-ness being resolved by calling these functions 'unsafe'. (IMO all functions are unsafe, some are just more unsafe than others :)
                                        Posted by svoboda at Jan 07, 2022 16:14
                                     |
| Why are asctime, ctime, fopen, and freopen still in the first table?
                                        Posted by jcsible at Jan 10, 2022 09:55
                                     |
| Because I didn't change the first table; I only changed the second.
                                        Posted by svoboda at Jan 10, 2022 10:35
                                     |

