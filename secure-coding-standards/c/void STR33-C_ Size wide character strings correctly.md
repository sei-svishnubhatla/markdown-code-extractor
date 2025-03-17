> [!warning]  
>
> This guideline has been deprecated by
>
> -   [STR38-C. Do not confuse narrow and wide character strings and functions](STR38-C_%20Do%20not%20confuse%20narrow%20and%20wide%20character%20strings%20and%20functions)
> -   [MEM35-C. Allocate sufficient memory for an object](MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object)

Wide character strings may be improperly sized when they are mistaken for *narrow* strings or for multibyte character strings. Incorrect string sizes can lead to buffer overflows when used, for example, to allocate an inadequately sized buffer.
## Noncompliant Code Example (Improper Function Call)
In this noncompliant code example, the `strlen()` function is used to determine the size of a wide character string:
``` c
wchar_t wide_str1[] = L"0123456789";
wchar_t *wide_str2 = (wchar_t *)malloc(strlen(wide_str1) + 1);
if (wide_str2 == NULL) {
  /* Handle error */
}
/* ... */
free(wide_str2);
wide_str2 = NULL;
```
The `strlen()` function counts the number of characters in a null-terminated byte string preceding the terminating null byte. However, wide characters contain null bytes, particularly when taken from the ASCII character set, as in this example. As a result, the `strlen()` function will return the number of bytes preceding the first null byte in the string.
### Implementation Details
Microsoft Visual Studio 2010 generates an incompatible type warning, so this code does not compile. GCC 4.6.1 also generates an incompatible type warning, but the code will still compile. GCC 4.3.2 on Linux also generates an incompatible type warning.
## Noncompliant Code Example (Size Improperly Scaled)
In this noncompliant code example, the `wcslen()` function is used to determine the size of a wide character string, but the length is not multiplied by the `sizeof(wchar_t)`:
``` c
wchar_t wide_str1[] = L"0123456789";
wchar_t *wide_str3 = (wchar_t *)malloc(wcslen(wide_str1) + 1);
if (wide_str3 == NULL) {
  /* Handle error */
}
/* ... */
free(wide_str3);
wide_str3 = NULL;
```
## Compliant Solution
This compliant solution correctly calculates the number of bytes required to contain a copy of the wide string (including the termination character):
``` c
wchar_t wide_str1[] = L"0123456789";
wchar_t *wide_str2 = (wchar_t *)malloc(
  (wcslen(wide_str1) + 1) * sizeof(wchar_t)
);
if (wide_str2 == NULL) {
  /* Handle error */
}
/* ... */
free(wide_str2);
wide_str2 = NULL;
```
## Risk Assessment
Failure to correctly determine the size of a wide character string can lead to buffer overflows and the execution of arbitrary code by an attacker.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR33-C | high | likely | medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this rule. Rose catches assignments between char and wchar_t. EXP09-C. Use sizeof to determine the size of a type or variable catches uses of malloc() that do not use sizeof when building a string using wchar_t |
| Splint | 3.1.1 | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR33-C).
## Related Guidelines

|  |  |
| ----|----|
| MITRE CWE | CWE-119, Failure to constrain operations within the bounds of an allocated memory bufferCWE-135, Incorrect calculation of multi-byte string length
CWE-805, Buffer access with incorrect length value |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 2, "Strings" |
| [Viega 2005] | Section 5.2.15, "Improper String Length Checking" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/STR32-C.+Null-terminate+byte+strings+as+required?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=271) [](https://www.securecoding.cert.org/confluence/display/seccode/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Aren't the code examples here covered by rule EXP09-A? (use sizeof to determine type of variables)
This rule seems to be more adept at saying "do not use wchars where chars are expected + do not use chars where wchars are expected"
                                        Posted by svoboda at Feb 08, 2008 13:44
                                     |
| The first example generates a warning from GCC (4.3.0 tested, but I'd expect no less from most earlier versions).
David's comment about using sizeof is apposite.; It also implies that it can be a good idea to include 'sizeof(char)' in the calculation, even though it is by definition 1; doing so shows that you've thought about the correct multiplier.
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 22:32
                                     |
| Rob and I talked about removing this rule since it seems to be covered by STR38-C. Do not use wide-char functions on narrow-char strings and vice versa and MEM35-C. Allocate sufficient memory for an object.; Are there cases not covered by other rules?
                                        Posted by akeeton at May 05, 2009 11:09
                                     |
| I would agree; any cases of a violation of this rule should probably be listed under STR38-C.
The NCCEs/CCE here should also go to STR38-C. (MEM35-C is about sophisticated routines that calculate the size of the object; the examples are significantly more complex than the math in the CCE.)
                                        Posted by svoboda at May 06, 2009 09:51
                                     |

