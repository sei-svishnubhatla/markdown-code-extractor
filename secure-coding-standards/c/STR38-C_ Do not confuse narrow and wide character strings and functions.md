Passing narrow string arguments to wide string functions or wide string arguments to narrow string functions can lead to [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Scaling problems are likely because of the difference in size between wide and narrow characters. (See [ARR39-C. Do not add or subtract a scaled integer to a pointer.)](ARR39-C_%20Do%20not%20add%20or%20subtract%20a%20scaled%20integer%20to%20a%20pointer) Because wide strings are terminated by a null wide character and can contain null bytes, determining the length is also problematic.
Because `wchar_t` and `char` are distinct types, many compilers will produce a warning diagnostic if an inappropriate function is used. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)
## Noncompliant Code Example (Wide Strings with Narrow String Functions) 
This noncompliant code example incorrectly uses the `strncpy()` function in an attempt to copy up to 10 wide characters. However, because wide characters can contain null bytes, the copy operation may end earlier than anticipated, resulting in the truncation of the wide string.
``` c
#include <stddef.h>
#include <string.h>
void func(void) {
  wchar_t wide_str1[]  = L"0123456789";
  wchar_t wide_str2[] =  L"0000000000";
  strncpy(wide_str2, wide_str1, 10);
}
```
## Noncompliant Code Example (Narrow Strings with Wide String Functions)
This noncompliant code example incorrectly invokes the `wcsncpy()` function to copy up to 10 wide characters from `narrow_str1` to `narrow_str2`. Because `narrow_str2` is a narrow string, it has insufficient memory to store the result of the copy and the copy will result in a buffer overflow.
``` c
#include <wchar.h>
void func(void) {
  char narrow_str1[] = "01234567890123456789";
  char narrow_str2[] = "0000000000";
  wcsncpy(narrow_str2, narrow_str1, 10);
}
```
## Compliant Solution
This compliant solution uses the proper-width functions. Using `wcsncpy()` for wide character strings and `strncpy()` for narrow character strings ensures that data is not truncated and buffer overflow does not occur.
``` c
#include <string.h>
#include <wchar.h>
void func(void) {
  wchar_t wide_str1[] = L"0123456789";
  wchar_t wide_str2[] = L"0000000000";
  /* Use of proper-width function */ 
  wcsncpy(wide_str2, wide_str1, 10);
  char narrow_str1[] = "0123456789";
  char narrow_str2[] = "0000000000";
  /* Use of proper-width function */ 
  strncpy(narrow_str2, narrow_str1, 10);
}
```
## Noncompliant Code Example (`strlen()`)
In this noncompliant code example, the `strlen()` function is used to determine the size of a wide character string:
``` c
#include <stdlib.h>
#include <string.h>
void func(void) {
  wchar_t wide_str1[] = L"0123456789";
  wchar_t *wide_str2 = (wchar_t*)malloc(strlen(wide_str1) + 1);
  if (wide_str2 == NULL) {
    /* Handle error */
  }
  /* ... */
  free(wide_str2);
  wide_str2 = NULL;
}
```
The `strlen()` function determines the number of characters that precede the terminating null character. However, wide characters can contain null bytes, particularly when expressing characters from the ASCII character set, as in this example. As a result, the `strlen()` function will return the number of bytes preceding the first null byte in the wide string. 
## Compliant Solution
This compliant solution correctly calculates the number of bytes required to contain a copy of the wide string, including the terminating null wide character:
``` c
#include <stdlib.h>
#include <wchar.h>
void func(void) {
  wchar_t wide_str1[] = L"0123456789";
  wchar_t *wide_str2 = (wchar_t *)malloc(
    (wcslen(wide_str1) + 1) * sizeof(wchar_t));
  if (wide_str2 == NULL) {
    /* Handle error */
  }
  /* ... */
  free(wide_str2);
  wide_str2 = NULL;
}
```
## Risk Assessment
Confusing narrow and wide character strings can result in buffer overflows, data truncation, and other defects.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR38-C | High | Likely | Low | P27 | L1 |

### Automated Detection
Modern compilers recognize the difference between a `char *` and a `wchar_t *`, so compiling code that violates this rule will generate warnings. It is feasible to have automated software that recognizes functions of improper width and replaces them with functions of proper width (that is, software that uses `wcsncpy()` when it recognizes that the parameters are of type `wchar_t *`).

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | wide-narrow-string-castwide-narrow-string-cast-implicit | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR38 | Fully implemented |
| Clang | 3.9 | -Wincompatible-pointer-types |  |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.TBA | Buffer OverrunTainted Buffer Access |
| Coverity | 2017.07 | PW | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-str38-c |  |
| Helix QAC | 2024.4 | C0432C++0403; |  |
| Klocwork | 2024.4 | CXX.DIFF.WIDTH.STR_AND_FUNC |  |
| Parasoft C/C++test | 2024.2 | CERT_C-STR38-a | Do not confuse narrow and wide character strings and functions |
| PC-lint Plus | 1.4 | 2454, 2480, 2481 | Partially supported: reports illegal conversions involving pointers to char or wchar_t as well as byte/wide-oriented stream inconsistencies |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR38-C | Checks for misuse of narrow or wide character string (rule fully covered) |
| RuleChecker | 24.04 | wide-narrow-string-castwide-narrow-string-cast-implicit | Partially checked |
| TrustInSoft Analyzer | 1.38 | pointer arithmetic | Partially verified. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR38-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.26.2.5, "The strncpy Function"7.31.4.2.2, "The wcsncpy Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152388) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](../c/Rule%2008_%20Memory%20Management%20_MEM_)
## Comments:

|  |
| ----|
| Good start. Here's what you need to do to complete the rules:
    Need implementation details on the NCCEs. Should say something like "on platform X with compiler Y, this code produces the following output...".
    Need some simple text in the compliant solution to introduce the code
    Is the remediation cost 'Medium'? or can code that can be automtically detected as noncompliant be automatically fixed (by a suitably complex static analyzer)?
    The 'automated detection' section has useful info, but it belongs in an 'implementation details' section. Also, do all compilers catch this problem or just gcc? And which version ? ( I bet older versions don't)
                                        Posted by svoboda at Apr 01, 2009 12:47
                                     |
| So when I try and run this with newest GCC and no flags on an i386 linux box, it compiles with warnings, and when running it segfaults in the strncpy/wcsncpy functions.; Is this the kind of information you're looking for in implementation details?
As for remediation cost, I do believe that an adequate analysis tool could automatically replace the wcsncpy/strncpy calls based on the argument pointer type.  That being said, if a program was built to run correctly around this bug (i.e. it was using strncpy to only copy so many bytes of a wide-char string) then it would affect functionality.  Given that this is a rare corner case (and still an egregious way of going about it) can I bump it down to low-cost?
                                        Posted by agidwani at Apr 01, 2009 16:00
                                     |
| Don't bother listing a segfault. I was hoping to see something like "only 5 of the 10 chars are copied". Only list output if it is predictable (eg doesn't rely on unitialized memory or undefined behavior)
I think the answer to your second queswtion is yes, if all an automatic rewriter has to do is repalce a wide-char fn with the appropriate narrow-char fn, (and vice versa), then the cost is low.
                                        Posted by svoboda at Apr 01, 2009 18:26
                                     |
| Ok...I added the solution description and fixed the remediation cost.
I'm still unsure what else to do about the automated detection/implementation.  Given that it is unpredictable, is there anything else that you feel needs listing?
                                        Posted by agidwani at Apr 01, 2009 19:14
                                     |
| In 1st NCCE, exactly how many chars get copied? After the copy what is the value of wide_str2? Or does buffer overflow occur (which renders the other questions moot)?  Same questions for 2nd NCCE.
I'm pretty sure both code samples are well-defined wrt the C standard (unless buffer overflow occurs). So you can just build a program and run it (possibly with a debugger) to see what actually happens, then report the output.
                                        Posted by svoboda at Apr 01, 2009 20:57
                                     |
| Ok, I toyed around with it in GDB after compiling in GCC on linux.andrew.
The first example segfaults, but no copying takes place and the target string is still filled with L"0".; Presumably this is because it encounters a null-byte and thus strncpy closes out.
What I end up with for the second NCCE is pretty bland; the program hits a segfault before any actual copying takes place and the target is filled with 0's.
Is this worth reporting?
                                        Posted by agidwani at Apr 01, 2009 21:37
                                     |
| It's my guess that doing strcpy on wide-char ASCII strings does no coping bince the first byte is 0 eg null.  I'd also guess that doing wcscpy on narrow-char ASCII strings overflows the buffer since it needs two null chars in a row to stop, which doesn't occur in a sring literal. If you're getting a segfault because wcscpy or strcpy go beyond the string, just report buffer overflow. If you're getting a segfault afterwards, that's your bug to fix.
Also report compiler warnings on the specific compiler versions you can (gcc, MSVC), as Rob suggests.
                                        Posted by svoboda at Apr 01, 2009 22:46
                                     |
| Ok, after poking around in GDB a bit more I found that it was going out of range of the string.; The function didn't finish, which caused the segfault.
I don't have MSVC, but since there's an extension I'll use that time to find it and run the code through to see what happens.
                                        Posted by agidwani at Apr 01, 2009 22:59
                                     |
| Good, the implementation details are IMHO complete. My only comment is that the Imp. Details section should go after the NCCE, as they are about the NCCEs, not the CS.
                                        Posted by svoboda at Apr 04, 2009 09:11
                                     |
| The rule is now complete, good job.
                                        Posted by svoboda at Apr 05, 2009 10:09
                                     |
| The CCE appears to segfault on the *cpy functions because the parameters are pointers to string literals (which are constants on most compilers).
I think the example should be be:
wchar_t wide_str1[] = L"0123456789";
wchar_t wide_str2[] = L"0000000000";
wcsncpy(wide_str2, wide_str1, 10);   /* Use of proper-width function */
char narrow_str1[] = "0123456789";
char narrow_str2[] = "0000000000";
strncpy(narrow_str2, narrow_str1, 10); /* Use of proper-width function */

The literal is then copied into an array which is able to be modified by \*cpy.
![](images/icons/contenttypes/comment_16.png) Posted by abrowne at Sep 23, 2010 19:08
\| \|
Agreed, I've made this change.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 24, 2010 09:39
\|
