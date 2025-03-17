The `EOF` macro represents a negative value that is used to indicate that the file is exhausted and no data remains when reading data from a file. `EOF` is an example of an [in-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-in-banderrorindicator). In-band error indicators are problematic to work with, and the creation of new in-band-error indicators is discouraged by [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).
The byte I/O functions `fgetc()`, `getc()`, and `getchar()` all read a character from a stream and return it as an `int.` (See [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type).) If the stream is at the end of the file, the end-of-file indicator for the stream is set and the function returns `EOF`. If a read error occurs, the error indicator for the stream is set and the function returns `EOF`. If these functions succeed, they cast the character returned into an `unsigned char`.
Because `EOF` is negative, it should not match any unsigned character value. However, this is only true for [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) where the `int` type is wider than `char`. On an implementation where `int` and `char` have the same width, a character-reading function can read and return a valid character that has the same bit-pattern as `EOF`. This could occur, for example, if an attacker inserted a value that looked like `EOF` into the file or data stream to alter the behavior of the program.
The C Standard requires only that the `int` type be able to represent a maximum value of +32767 and that a `char` type be no larger than an `int`. Although uncommon, this situation can result in the integer constant expression `EOF` being indistinguishable from a valid character; that is, `(int)(unsigned char)65535 == -1`. Consequently, failing to use `feof()` and `ferror()` to detect end-of-file and file errors can result in incorrectly identifying the `EOF` character on rare implementations where `sizeof(int) == sizeof(char)`.
This problem is much more common when reading wide characters. The `fgetwc()`, `getwc()`, and `getwchar()` functions return a value of type `wint_t`. This value can represent the next wide character read, or it can represent `WEOF`, which indicates end-of-file for wide character streams. On most implementations, the `wchar_t` type has the same width as `wint_t`, and these functions can return a character indistinguishable from `WEOF`.
In the UTF-16 character set, `0xFFFF` is guaranteed not to be a character, which allows `WEOF` to be represented as the value `-1`. Similarly, all UTF-32 characters are positive when viewed as a signed 32-bit integer. All widely used character sets are designed with at least one value that does not represent a character. Consequently, it would require a custom character set designed without consideration of the C programming language for this problem to occur with wide characters or with ordinary characters that are as wide as `int`.
The C Standard `feof()` and `ferror()` functions are not subject to the problems associated with character and integer sizes and should be used to verify end-of-file and file errors for susceptible implementations \[[Kettlewell 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Kettle02)\]. Calling both functions on each iteration of a loop adds significant overhead, so a good strategy is to temporarily trust `EOF` and `WEOF` within the loop but verify them with `feof()` and `ferror()` following the loop.
## Noncompliant Code Example
This noncompliant code example loops while the character `c` is not `EOF`:
``` c
#include <stdio.h>
void func(void) {
  int c;
  do {
    c = getchar();
  } while (c != EOF);
}
```
Although `EOF` is guaranteed to be negative and distinct from the value of any unsigned character, it is not guaranteed to be different from any such value when converted to an `int`. Consequently, when `int` has the same width as `char`, this loop may terminate prematurely.
## Compliant Solution (Portable)
This compliant solution uses `feof()` and `ferror()` to test whether the `EOF` was an actual character or a real `EOF` because of end-of-file or errors:
``` c
#include <stdio.h>
void func(void) {
  int c;
  do {
    c = getchar();
  } while (c != EOF || (!feof(stdin) && !ferror(stdin)));
}
```
## Noncompliant Code Example (Nonportable)
This noncompliant code example uses an assertion to ensure that the code is executed only on architectures where `int` is wider than `char` and `EOF` is guaranteed not to be a valid character value. However, this code example is noncompliant because the variable `c` is declared as a `char` rather than an `int`, making it possible for a valid character value to compare equal to the value of the `EOF` macro when `char` is signed because of sign extension:
``` c
#include <assert.h>
#include <limits.h>
#include <stdio.h>
void func(void) {
  char c;
  static_assert(UCHAR_MAX < UINT_MAX, "FIO34-C violation");
  do {
    c = getchar();
  } while (c != EOF);
}
```
Assuming that a `char` is a signed 8-bit type and an int is a 32-bit type, if `getchar()` returns the character value `'\xff` (decimal 255), it will be interpreted as `EOF` because this value is sign-extended to `0xFFFFFFFF` (the value of `EOF`) to perform the comparison. (See [STR34-C. Cast characters to unsigned char before converting to larger integer sizes](STR34-C_%20Cast%20characters%20to%20unsigned%20char%20before%20converting%20to%20larger%20integer%20sizes).)
## Compliant Solution (Nonportable)
This compliant solution declares `c` to be an `int`. Consequently, the loop will terminate only when the file is exhausted.
``` c
#include <assert.h>
#include <stdio.h>
#include <limits.h>
void func(void) {
  int c;
  static_assert(UCHAR_MAX < UINT_MAX, "FIO34-C violation");
  do {
    c = getchar();
  } while (c != EOF);
}
```
## Noncompliant Code Example (Wide Characters)
In this noncompliant example, the result of the call to the C standard library function `getwc()` is stored into a variable of type `wchar_t` and is subsequently compared with `WEOF`:
``` c
#include <stddef.h>
#include <stdio.h>
#include <wchar.h>
enum { BUFFER_SIZE = 32 };
void g(void) {
  wchar_t buf[BUFFER_SIZE];
  wchar_t wc;
  size_t i = 0;
  while ((wc = getwc(stdin)) != L'\n' && wc != WEOF) {
    if (i < (BUFFER_SIZE - 1)) {
      buf[i++] = wc;
    }
  }
  buf[i] = L'\0';
}
```
This code suffers from two problems. First, the value returned by `getwc()` is immediately converted to `wchar_t` before being compared with `WEOF`. Second, there is no check to ensure that `wint_t` is wider than `wchar_t`. Both of these problems make it possible for an attacker to terminate the loop prematurely by supplying the wide-character value matching `WEOF` in the file.
## Compliant Solution (Portable)
This compliant solution declares `wc` to be a `wint_t` to match the integer type returned by `getwc()`. Furthermore, it does not rely on `WEOF` to determine end-of-file definitively.
``` c
#include <stddef.h>
#include <stdio.h>
#include <wchar.h>
enum {BUFFER_SIZE = 32 }
void g(void) {
  wchar_t buf[BUFFER_SIZE];
  wint_t wc;
  size_t i = 0;
  while ((wc = getwc(stdin)) != L'\n' && wc != WEOF) {
    if (i < BUFFER_SIZE - 1) {
      buf[i++] = wc;
    }
  }
  if (feof(stdin) || ferror(stdin)) {
   buf[i] = L'\0';
  } else {
    /* Received a wide character that resembles WEOF; handle error */
  }
}
```
## Exceptions
**FIO34-C-EX1:** A number of C functions do not return characters but can return `EOF` as a status code. These functions include `fclose()`, `fflush()`, `fputs()`, `fscanf()`, `puts()`, `scanf()`, `sscanf()`, `vfscanf()`, and `vscanf()`. These return values can be compared to `EOF` without validating the result.
## Risk Assessment
Incorrectly assuming characters from a file cannot match `EOF` or `WEOF` has resulted in significant vulnerabilities, including command injection attacks. (See the [\*CA-1996-22](http://www.cert.org/historical/advisories/CA-1996-22.cfm) advisory.)

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO34-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | conversion_overflowessential-type-assign | Soundly supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO34 |  |
| CodeSonar | 8.3p0 | LANG.CAST.COERCE | Coercion alters value |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | CHAR_IO | Identifies defects when the return value of;fgetc(), getc(), or getchar() is incorrectly assigned to a char instead of an int. Coverity Prevent cannot discover all violations of this rule, so further verification is necessary |
| Cppcheck Premium | 24.11.0
 | premium-cert-fio34-c |  |
| ECLAIR | 1.2 | CC2.FIO34 | Partially implemented |
| Helix QAC | 2024.4 | C2676, C2678C++2676, C++2678, C++3001, C++3010, C++3051, C++3137, C++3717 |  |
| Klocwork | 2024.4 | CWARN.CMPCHR.EOF |  |
| LDRA tool suite | 9.7.1 | 662 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO34-a | The macro EOF should be compared with the unmodified return value from the Standard Library function |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO34-C | Checks for character values absorbed into EOF (rule partially covered) |
| Splint | 3.1.1 |  |  |
| RuleChecker | 24.04 | essential-type-assign | Supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | STR00-C. Represent characters using an appropriate type | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | FIO08-J. Use an int to capture the return value of methods that read a character or byte | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Using character values that are indistinguishable from EOF [chreof] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-197 | 2017-06-14: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-197 and FIO34-C
Independent( FLP34-C, INT31-C) FIO34-C = Subset( INT31-C)
Therefore: FIO34-C = Subset( CWE-197)
## Bibliography

|  |  |
| ----|----|
| [Kettlewell 2002] | Section 1.2, "<stdio.h> and Character Types" |
| [NIST 2006] | SAMATE Reference Dataset Test Case ID 000-000-088 |
| [Summit 2005] | Question 12.2 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152343) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](../c/FIO37-C_%20Do%20not%20assume%20that%20fgets__%20or%20fgetws__%20returns%20a%20nonempty%20string%20when%20successful)
## Comments:

|  |
| ----|
| Since int and char being the same width is so rare, I wonder if we should split a recommendation out of this: the rule would basically be "don't compare a char to EOF" (the second pair of examples), and the recommendation would basically be "don't assume int is wider than char" (the first pair of examples).
                                        Posted by jcsible at Jul 06, 2020 16:36
                                     |
| We used to have;void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char), but folded it into this rule because it was so arcane.
                                        Posted by svoboda at Jul 07, 2020 10:58
                                     |
| Looking at the old ones in The Void, I think I actually prefer them to this one.
                                        Posted by jcsible at Jul 07, 2020 11:17
                                     |

