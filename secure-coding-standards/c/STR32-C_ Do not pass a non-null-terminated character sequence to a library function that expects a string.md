Many library functions accept a string or wide string argument with the constraint that the string they receive is properly null-terminated. Passing a character sequence or wide character sequence that is not null-terminated to such a function can result in accessing memory that is outside the bounds of the object. Do not pass a character sequence or wide character sequence that is not null-terminated to a library function that expects a string or wide string argument. 
## Noncompliant Code Example
This code example is noncompliant because the character sequence `c_str` will not be null-terminated when passed as an argument to `printf().` (See [STR11-C. Do not specify the bound of a character array initialized with a string literal](STR11-C_%20Do%20not%20specify%20the%20bound%20of%20a%20character%20array%20initialized%20with%20a%20string%20literal) on how to properly initialize character arrays.)
``` c
#include <stdio.h>
void func(void) {
  char c_str[3] = "abc";
  printf("%s\n", c_str);
}
```
## Compliant Solution
This compliant solution does not specify the bound of the character array in the array declaration. If the array bound is omitted, the compiler allocates sufficient storage to store the entire string literal, including the terminating null character.
``` c
#include <stdio.h>
void func(void) {
  char c_str[] = "abc";
  printf("%s\n", c_str);
}
```
## Noncompliant Code Example
This code example is noncompliant because the wide character sequence `cur_msg` will not be null-terminated when passed to `wcslen()`. This will occur if `lessen_memory_usage()` is invoked while `cur_msg_size` still has its initial value of 1024.
``` c
#include <stdlib.h>
#include <wchar.h>
wchar_t *cur_msg = NULL;
size_t cur_msg_size = 1024;
size_t cur_msg_len = 0;
void lessen_memory_usage(void) {
  wchar_t *temp;
  size_t temp_size;
  /* ... */
  if (cur_msg != NULL) {
    temp_size = cur_msg_size / 2 + 1;
    temp = realloc(cur_msg, temp_size * sizeof(wchar_t));
    /* temp &and cur_msg may no longer be null-terminated */
    if (temp == NULL) {
      /* Handle error */
    }
    cur_msg = temp;
    cur_msg_size = temp_size;
    cur_msg_len = wcslen(cur_msg); 
  }
}
```
## Compliant Solution
In this compliant solution, `cur_msg` will always be null-terminated when passed to `wcslen()`:
``` c
#include <stdlib.h>
#include <wchar.h>
wchar_t *cur_msg = NULL;
size_t cur_msg_size = 1024;
size_t cur_msg_len = 0;
void lessen_memory_usage(void) {
  wchar_t *temp;
  size_t temp_size;
  /* ... */
  if (cur_msg != NULL) {
    temp_size = cur_msg_size / 2 + 1;
    temp = realloc(cur_msg, temp_size * sizeof(wchar_t));
    /* temp and cur_msg may no longer be null-terminated */
    if (temp == NULL) {
      /* Handle error */
    }
    cur_msg = temp;
    /* Properly null-terminate cur_msg */
    cur_msg[temp_size - 1] = L'\0'; 
    cur_msg_size = temp_size;
    cur_msg_len = wcslen(cur_msg); 
  }
}
```
## Noncompliant Code Example (`strncpy()`)
Although the `strncpy()` function takes a string as input, it does not guarantee that the resulting value is still null-terminated. In the following noncompliant code example, if no null character is contained in the first `n` characters of the `source` array, the result will not be null-terminated. Passing a non-null-terminated character sequence to `strlen()` is undefined behavior.
``` c
#include <string.h>
enum { STR_SIZE = 32 };
size_t func(const char *source) {
  char c_str[STR_SIZE];
  size_t ret = 0;
  if (source) {
    c_str[sizeof(c_str) - 1] = '\0';
    strncpy(c_str, source, sizeof(c_str));
    ret = strlen(c_str);
  } else {
    /* Handle null pointer */
  }
  return ret;
}
```
## Compliant Solution (Truncation)
This compliant solution is correct if the programmer's intent is to truncate the string:
``` c
#include <string.h>
enum { STR_SIZE = 32 };
size_t func(const char *source) {
  char c_str[STR_SIZE];
  size_t ret = 0;
  if (source) {
    strncpy(c_str, source, sizeof(c_str) - 1);
    c_str[sizeof(c_str) - 1] = '\0';
    ret = strlen(c_str);
  } else {
    /* Handle null pointer */
  }
  return ret;
}
```
## Compliant Solution (Truncation, strncpy_s())
The C Standard, Annex K `strncpy_s()` function can also be used to copy with truncation. The `strncpy_s()` function copies up to `n` characters from the source array to a destination array. If no null character was copied from the source array, then the `n`th position in the destination array is set to a null character, guaranteeing that the resulting string is null-terminated.
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <string.h>
enum { STR_SIZE = 32 };
size_t func(const char *source) {
  char c_str[STR_SIZE];
  size_t ret = 0;
  if (source) {
    errno_t err = strncpy_s(
      c_str, sizeof(c_str), source, strnlen(source, sizeof(c_str))
    );
    if (err != 0) {
      /* Handle error */
    } else {
      ret = strnlen(c_str, sizeof(c_str));
    }
  } else {
     /* Handle null pointer */
  }
  return ret;
}
```
## Compliant Solution (Copy without Truncation)
If the programmer's intent is to copy without truncation, this compliant solution copies the data and guarantees that the resulting array is null-terminated. If the string cannot be copied, it is handled as an error condition.
``` c
#include <string.h>
enum { STR_SIZE = 32 };
size_t func(const char *source) {
  char c_str[STR_SIZE];
  size_t ret = 0;
  if (source) {
    if (strnlen(source, sizeof(c_str)) < sizeof(c_str)) {
      strcpy(c_str, source);
      ret = strlen(c_str);
    } else {
      /* Handle string-too-large */
    }
  } else {
    /* Handle null pointer */
  }
  return ret;
}
```
Note that this code is not bulletproof. It gracefully handles the case where `source`  is NULL, when it is a valid string, and when `source` is not null-terminated, but at least the first 32 bytes are valid. However, in cases where `source` is not NULL, but points to invalid memory, or any of the first 32 bytes are invalid memory, the first call to `strnlen() `will access this invalid memory, and the resulting behavior is undefined. Unfortunately, standard C provides no way to prevent or even detect this condition without some external knowledge about the memory `source` points to.
## Risk Assessment
Failure to properly null-terminate a character sequence that is passed to a library function that expects a string can result in buffer overflows and the execution of arbitrary code with the permissions of the vulnerable process. Null-termination errors can also result in unintended information disclosure.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR32-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | SupportedAstrée supports the implementation of library stubs to fully verify this guideline. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR32 | Partially implemented: can detect some violation of the rule |
| CodeSonar | 8.3p0 | MISC.MEM.NTERM.CSTRING | Unterminated C String |
| Compass/ROSE |  |  | Can detect some violations of this rule |
| Coverity | 2017.07 | STRING_NULL | Fully implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-str32-c |  |
| Helix QAC | 2024.4 | DF2835, DF2836, DF2839 |  |
| Klocwork | 2024.4 | NNTS.MIGHTNNTS.MUST
SV.STRBO.BOUND_COPY.UNTERM |  |
| LDRA tool suite | 9.7.1 | 404 S, 600 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR32-a | Avoid overflow due to reading a not zero terminated string |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR32-C | Checks for:Invalid use of standard library string routineTainted NULL or non-null-terminated stringRule partially covered. |
| PVS-Studio | 7.35 | V692 |  |
| TrustInSoft Analyzer | 1.38 | match format and arguments | Partially verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | String Termination [CMJ] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Passing a non-null-terminated character sequence to a library function that expects a string [strmod] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-123, Write-what-where Condition | 2017-06-12: CERT: Partial overlap |
| CWE 2.11 | CWE-125, Out-of-bounds Read | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-170, Improper Null Termination | 2017-06-13: CERT: Exact |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-119 and STR32-C
Independent( ARR30-C, ARR38-C, ARR32-C, INT30-C, INT31-C, EXP39-C, EXP33-C, FIO37-C) STR31-C = Subset( Union( ARR30-C, ARR38-C)) STR32-C = Subset( ARR38-C)
CWE-119 = Union( STR32-C, list) where list =
-   Out-of-bounds reads or writes that do not involve non-null-terminated byte strings.
### CWE-125 and STR32-C
Independent( ARR30-C, ARR38-C, EXP39-C, INT30-C) STR31-C = Subset( Union( ARR30-C, ARR38-C)) STR32-C = Subset( ARR38-C)
CWE-125 = Union( STR32-C, list) where list =
-   Out-of-bounds reads that do not involve non-null-terminated byte strings.
### CWE-123 and STR32-C
Independent(ARR30-C, ARR38-C) STR31-C = Subset( Union( ARR30-C, ARR38-C)) STR32-C = Subset( ARR38-C)
Intersection( CWE-123, STR32-C) =
-   Buffer overflow from passing a non-null-terminated byte string to a standard C library copying function that expects null termination, and that overwrites an (unrelated) pointer
STR32-C - CWE-123 =
-   Buffer overflow from passing a non-null-terminated byte string to a standard C library copying function that expects null termination, but it does not overwrite an (unrelated) pointer
CWE-123 – STR31-C =
-   Arbitrary writes that do not involve standard C library copying functions, such as strcpy()
## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | ;Chapter 2, "Strings"  |
| [Viega 2005] | Section 5.2.14, "Miscalculated NULL Termination" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152048) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152133)
## Comments:

|  |
| ----|
| > This only occurs if the index is less than the minimum size of the string.
ITYM "maximum", no?
                                        Posted by davearonson at Jan 10, 2008 14:31
                                     |
| I replaced the realloc() example with a similar example from TS 17961 [nonnullcs] that uses wchar_t.;Rewrote the rule intro as well.  TS 17961 [nonnullcs] omits the strncpy() example.  I'm wondering if we should follow suite? 
                                        Posted by rcs_mgr at Nov 30, 2013 08:55
                                     |
| I suggest a third compliant solution (with truncation) that uses the function strtcpy (t means truncation allowed).The prototype of strtcpy is:;        int   strtcpy( char * dst, size_t dstsize, const char * src) ;This function (in fact, it is a macro) copies the string src in the array dst where dstsize is the size of dst. It returns a negative value if dst or src is the NULL pointer or if dstsize is 0.The return value distinguishes if a truncation happened or not.#include <string.h>#include “str5.h”enum { STR_SIZE = 32 }; size_t func(const char *source) {  char c_str[STR_SIZE];  size_t ret = 0;    int err ;   err = strtcpy(c_str,
sizeof(c_str), source) ;  if ( err < 0 ) {    /* Handle error
*/  } else {      ret = strlen(c_str);  }   return ret;} The function strtcpy is easier to use than strncpy_s and more robust than strncpy or strlcpy.Like strlcpy, strtcpy is C90 compliant, open-source (same licence than glibc), easy to download and to include in C projects.[see http://aral.iut-rodez.fr/en/sanchis/miscellaneous/str5/str5.html  and  str5.h] 
                                        Posted by eric.sanchis at May 21, 2017 08:49
                                     |
| It appears unsafe to call strlen; on the input parameter source in the compliant solutions (seen in strcpy_s and copy w/o truncation). If the value comes from an untrusted/malicious party this seems to be a vulnerability in the compliant solutions which this very rule advises against.
                                        Posted by 0skellar at May 22, 2023 08:21
                                     |
| Agreed. I replaced strlen(source) with strnlen(source, <dest-sice>) in the compliant solutions.
                                        Posted by svoboda at Jun 06, 2023 10:07
                                     |
| It might be useful to supply a list of standard C functions that work with strings, but convert a NTBS into a possibly-non-NTBS. At one point, I assumed strncpy() was the only such function.Likewise, a list of functions that expect NTBS's might be useful. Mostly they begin with str, but there are exceptions, like system().Lots of functions, like realloc() can butcher NTBS's because they don't care if their arguments are NTBS's or not.
                                        Posted by svoboda at Aug 31, 2023 15:16
                                     |

