Alternative functions that limit the number of bytes copied are often recommended to mitigate buffer overflow [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Examples include
-   `strncpy()` instead of `strcpy()`
-   `strncat()` instead of `strcat()`
-   `fgets()` instead of `gets()`
-   `snprintf()` instead of `sprintf()`
These functions truncate strings that exceed the specified limits. Additionally, some functions, such as `strncpy()`, do not guarantee that the resulting character sequence is null-terminated. (See [STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string](STR32-C_%20Do%20not%20pass%20a%20non-null-terminated%20character%20sequence%20to%20a%20library%20function%20that%20expects%20a%20string).)
Unintentional truncation results in a loss of data and in some cases leads to software vulnerabilities.
## Noncompliant Code Example
The standard functions `strncpy()` and `strncat()` copy a specified number of characters `n` from a source string to a destination array. In the case of `strncpy()`, if there is no null character in the first `n` characters of the source array, the result will not be null-terminated and any remaining characters are truncated.
``` c
char *string_data;
char a[16];
/* ... */
strncpy(a, string_data, sizeof(a));
```
## Compliant Solution (Adequate Space)
Either the `strcpy()` or `strncpy()` function can be used to copy a string and a null character to a destination buffer, provided there is enough space. The programmer must be careful to ensure that the destination buffer is large enough to hold the string to be copied and the null byte to prevent errors, such as data truncation and buffer overflow.
``` c
char *string_data = NULL;
char a[16];
/* ... */
if (string_data == NULL) {
  /* Handle null pointer error */
}
else if (strlen(string_data) >= sizeof(a)) {
  /* Handle overlong string error */
}
else {
  strcpy(a, string_data);
}
```
This solution requires that `string_data` is null-terminated; that is, a null byte can be found within the bounds of the referenced character array. Otherwise, `strlen()` will stray into other objects before finding a null byte.
## Compliant Solution (`strcpy_s()`, C11 Annex K)
The `strcpy_s()` function defined in C11 Annex K  \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] provides additional safeguards, including accepting the size of the destination buffer as an additional argument. (See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).) Also, `strnlen_s()` accepts a maximum-length argument for strings that may not be null-terminated.
``` c
char *string_data = NULL;
char a[16];
/* ... */
if (string_data == NULL) {
  /* Handle null pointer error */
}
else if (strnlen_s(string_data, sizeof(a)) >= sizeof(a)) {
  /* Handle overlong string error */
}
else {
  strcpy_s(a, sizeof(a), string_data);
}
```
If a runtime-constraint error is detected by the call to either `strnlen_s()` or `strcpy_s()`, the currently registered runtime-constraint handler is invoked. See [ERR03-C. Use runtime-constraint handlers when calling the bounds-checking interfaces](ERR03-C_%20Use%20runtime-constraint%20handlers%20when%20calling%20the%20bounds-checking%20interfaces) for more information on using runtime-constraint handlers with C11 Annex K functions.
## Exceptions
**STR03-C-EX1:** The intent of the programmer is to purposely truncate the string.
## Risk Assessment
Truncating strings can lead to a loss of data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR03-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | MISC.MEM.NTERM | No Space For Null Terminator |
| Compass/ROSE |  |  | Could detect violations in the following manner: all calls to strncpy() and the other functions should be followed by an assignment of a terminating character to null-terminate the string |
| GCC | 8.1 | -Wstringop-truncation | Detects string truncation by strncat and strncpy. |
| Klocwork | 2024.4 | NNTS.MIGHTNNTS.MUST |  |
| LDRA tool suite | 9.7.1 | 115 S, 44 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR03-a | Avoid overflow due to reading a not zero terminated string |
| Polyspace Bug Finder | R2024a | CERT C: Rec. STR03-C | Checks for invalid use of standard library string routine (rec. partially supported) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR03-CPP. Do not inadvertently truncate a null-terminated character array |
| ISO/IEC TR 24772:2013 | String Termination [CJM] |
| MITRE CWE | CWE-170, Improper null terminationCWE-464, Addition of data structure sentinel |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152409) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152350)
## Comments:

|  |
| ----|
| I noticed the same thing . One thing that should probably be mentioned for the *_s string functions is that if no parameter validation handler is installed, and the string length of the source string is longer than the length specified, an exception is thrown (0xC000000D, which I think is NTSTATUS_INVALID_PARAMETER). This is compliant with not truncating strings, but might result in an awful lot of random program crashing...
                                        Posted by mdowd at Jan 06, 2007 03:41
                                     |
| I question whether this is rose-possible... the checker for STR32 already handles the strncpy() case, and besides, how could we ever hope to catch an exception like the one in this rule, "The intent of the programmer is to intentionally truncate the null-terminated byte string."
                                        Posted by avolkovi at Jul 09, 2008 13:21
                                     |
| I marked the rule 'rose-possible' before the exception existed. Changed to 'unenforceable'.
                                        Posted by svoboda at Aug 06, 2008 11:23
                                     |
| Is this rule still considered "unenforceable"? I see no label saying such.
                                        Posted by xuinkrbin. at Jan 10, 2013 16:15
                                     |
| The rule is currently marked rose-false-positive. This means that we can write checkers to enforce the rule, but they will always find false positives. So it's technically enforceable, if you don't mind the false positives.
                                        Posted by svoboda at Jan 10, 2013 16:39
                                     |

