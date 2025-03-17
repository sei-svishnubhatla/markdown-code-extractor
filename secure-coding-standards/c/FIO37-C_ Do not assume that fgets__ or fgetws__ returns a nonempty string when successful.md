Errors can occur when incorrect assumptions are made about the type of data being read. These assumptions may be violated, for example, when binary data has been read from a file instead of text from a user's terminal or the output of a process is piped to `stdin.` (See [FIO14-C. Understand the difference between text mode and binary mode with file streams](FIO14-C_%20Understand%20the%20difference%20between%20text%20mode%20and%20binary%20mode%20with%20file%20streams).) On some systems, it may also be possible to input a null byte (as well as other binary codes) from the keyboard.
Subclause 7.23.7.2 of the C Standard paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\] says,
> The fgets function returns s if successful. If end-of-file is encountered and no characters have been read into the array, the contents of the array remain unchanged and a null pointer is returned. If a read error occurs during the operation, the members of the array have unspecified values and a null pointer is returned.

The wide-character function `fgetws()` has the same behavior. Therefore, if `fgets()` or `fgetws()` returns a non-null pointer, it is safe to assume that the array contains data. However, it is erroneous to assume that the array contains a nonempty string because the data may contain null characters.
## Noncompliant Code Example
This noncompliant code example attempts to remove the trailing newline (`\n`) from an input line. The `fgets()` function is typically used to read a newline-terminated line of input from a stream. It takes a size parameter for the destination buffer and copies, at most, `size - 1` characters from a stream to a character array.
``` c
#include <stdio.h>
#include <string.h>
enum { BUFFER_SIZE = 1024 };
void func(void) {
  char buf[BUFFER_SIZE];
  if (fgets(buf, sizeof(buf), stdin) == NULL) {
    /* Handle error */
  }
  buf[strlen(buf) - 1] = '\0';
}
```
The `strlen()` function computes the length of a string by determining the number of characters that precede the terminating null character. A problem occurs if the first character read from the input by `fgets()` happens to be a null character. This may occur, for example, if a binary data file is read by the `fgets()` call \[[Lai 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Lai06)\]. If the first character in `buf` is a null character, `strlen(buf)` returns 0, the expression `strlen(buf) - 1` wraps around to a large positive value, and a write-outside-array-bounds error occurs.
## Compliant Solution
This compliant solution uses `strchr()` to replace the newline character in the string if it exists:
``` c
#include <stdio.h>
#include <string.h>
enum { BUFFER_SIZE = 1024 };
void func(void) {
  char buf[BUFFER_SIZE];
  char *p;
  if (fgets(buf, sizeof(buf), stdin)) {
    p = strchr(buf, '\n');
    if (p) {
      *p = '\0';
    }
  } else {
    /* Handle error */
  }
}
```
## Risk Assessment
Incorrectly assuming that character data has been read can result in an out-of-bounds memory write or other flawed logic.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO37-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports defects due to returned (empty) strings. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO37 |  |
| CodeSonar | 8.3p0 | (general) | Considers the possibility that fgets() and fgetws() may return empty strings (Warnings of various classes may be triggered depending on subsequent operations on those strings. For example, the noncompliant code example cited above would trigger a buffer underrun warning.) |
| Compass/ROSE |  |  | Could detect some violations of this rule (In particular, it could detect the;noncompliant code example by searching for fgets(), followed by strlen() - 1, which could be −1. The crux of this rule is that a string returned by fgets() could still be empty, because the first char is '\0'. There are probably other code examples that violate this guideline; they would need to be enumerated before ROSE could detect them.) |
| Cppcheck Premium | 24.11.0 | premium-cert-fio37-c |  |
| Helix QAC | 2024.4 | DF4911, DF4912, DF4913 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO37-a | Avoid accessing arrays out of bounds |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO37-C | Checks for use of indeterminate string (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO37-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | FIO14-C. Understand the difference between text mode and binary mode with file streams | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-241, Improper Handling of Unexpected Data Type | 2017-07-05: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-241 and FIO37-C
CWE-241 = Union( FIO37-C, list) where list =
-   Improper handling of unexpected data type that does not come from the fgets() function.
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.23.7.2, "The fgets Function"Subclause 7.31.3.2, "The fgetws Function" |
| [Lai 2006] |  |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151948) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152442)
## Comments:

|  |
| ----|
| On POSIX systems it is also easy to input a null byte (and some other "binary" codes) from the keyboard, usually as ctrl-SPACE or ctrl-@.
In fact I used this trick once to unlock a password-protected screen saver.
                                        Posted by dagwyn at Apr 17, 2008 18:05
                                     |
| While this specific NCCE/CCE pair is certainly checkable by ROSE, I feel that the general case is not...I suspect there are just too many ways in which one can try to remove the imaginary last newline char in a string.
                                        Posted by svoboda at Jun 21, 2008 08:19
                                     |
| added how to catch the NCCE/CCE pair.
                                        Posted by svoboda at Jul 25, 2008 11:03
                                     |
| I was surprised at the mention of gets() in this new text.  My immediate reaction was "surely ROSE would flag all uses of gets() as unsafe".  Then I realised there doesn't seem to be a rule anywhere about never using gets().  At least, not one I could find.  If that's true, it seems like a glaring omission.
                                        Posted by geoffclare at Jul 25, 2008 12:06
                                     |
| This rule was meant to be covered under STR35-C. Do not copy data from an unbounded source to a fixed-length array.
This was an attempt to document the general principle and not create a rule that only applied to one function.  The gets() function is shown as the NCE.
                                        Posted by rcs at Jul 25, 2008 13:12
                                     |
| Oops, right, never use gets(). I took it out of the ROSE paragraph.
                                        Posted by svoboda at Jul 25, 2008 13:24
                                     |
| Thanks for the pointer.  I was expecting to find it under FIO, but I should have thought to look in STR as well.  (I also tried a search for "gets" but that was no use as the wiki, no doubt trying to be helpful but not succeeding in this case, returned a large number of hits for the singular "get" as well.)
                                        Posted by geoffclare at Jul 26, 2008 04:57
                                     |
| This is a good rule, but I feel that the title could use some strenghtening. The main vul is that fgets() can read X bytes, producing a Y-character string where X>Y (Y may even be 0). The GNU C programming tutorial actually deprecates fgets() in favor of getline() because of this issue.
The rule could probably use more NCCEs, which would rely on the mistaken assumption that X==Y.
                                        Posted by svoboda at May 14, 2009 19:58
                                     |
| Changed the title, and added some background on fgets(). Since C99 promises that fgets() fills the array when successful, it is easy to jump to conclusions and assume the array is a nonempty NTBS.  Which the NCCE shows, but the explanation needed refinement.
                                        Posted by svoboda at Jan 28, 2010 10:42
                                     |

