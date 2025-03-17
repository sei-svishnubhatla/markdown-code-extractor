The C Standard allows an array variable to be declared both with a bound index and with an initialization literal. The initialization literal also implies an array size in the number of elements specified. For strings, the size specified by a string literal is the number of characters in the literal plus one for the terminating null character.
It is common for an array variable to be initialized by a string literal and declared with an explicit bound that matches the number of characters in the string literal. Subclause 6.7.9, paragraph 14, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], says:
> An array of character type may be initialized by a character string literal or UTF−8 string literal, optionally enclosed in braces. Successive bytes of the string literal (including the terminating null character if there is room or if the array is of unknown size) initialize the elements of the array.

However, if the string is intended to be used as a null-terminated byte string, then the array will have one too few characters to hold the string because it does not account for the terminating null character. Such a sequence of characters has limited utility and has the potential to cause [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) if a null-terminated byte string is assumed.
A better approach is to not specify the bound of a string initialized with a string literal because the compiler will automatically allocate sufficient space for the entire string literal, including the terminating null character. This rule is a specific exception to [ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer](ARR02-C_%20Explicitly%20specify%20array%20bounds,%20even%20if%20implicitly%20defined%20by%20an%20initializer).
## Noncompliant Code Example
This noncompliant code example initializes an array of characters using a string literal that defines one character more (counting the terminating `'\0'`) than the array can hold:
``` c
const char s[3] = "abc";
```
The size of the array `s` is 3, although the size of the string literal is 4. Any subsequent use of the array as a null-terminated byte string can result in a vulnerability, because `s` is not properly null-terminated. (See [STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string](STR32-C_%20Do%20not%20pass%20a%20non-null-terminated%20character%20sequence%20to%20a%20library%20function%20that%20expects%20a%20string).)
### Implementation Details
This code compiles with no warning with Visual Studio 2013 and GCC 4.8.1. It produces a three-character array with no terminating null character, as specified by the standard.
## Compliant Solution
This compliant solution does not specify the bound of a character array in the array declaration. If the array bound is omitted, the compiler allocates sufficient storage to store the entire string literal, including the terminating null character.
``` c
const char s[] = "abc";
```
This approach is preferred because the size of the array can always be derived even if the size of the string literal changes.
## Exceptions
**STR11-C-EX1:** If the intention is to create a character array and *not* a null-terminated byte string, initializing to fit exactly without a null byte is allowed but not recommended. The preferred approach to create an array containing just the three characters `'a'`, `'b'`, and `'c'`, for example, is to declare each character literal as a separate element as follows:
``` c
char s[3] = { 'a', 'b', 'c' }; /* NOT a string */
```
Also, you should make clear in comments or documentation if a character array is, in fact, not a null-terminated byte string.
**STR11-C-EX2:** If the character array must be larger than the string literal it is initialized with, you may explicitly specify an array bounds. This is particularly important if the array's contents might change during program execution.
``` c
#include <string.h>
void func(void) {
  char s[10] = "abc";
  strcpy(&s[3], "def");
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR11-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée can detect subsequent code defects that this rule aims to prevent. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR11 |  |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.STR36 | Fully implemented |
| Helix QAC | 2024.4 | C1312 |  |
| LDRA tool suite | 9.7.1 | 404 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR11-a | Do not specify the bound of a character array initialized with a string literal |
| PC-lint Plus | 1.4 | 784 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. STR11-C | Checks for missing null in string array (rec. partially covered) |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR36-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializerSTR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string |
| SEI CERT C++ Coding Standard | VOID STR08-CPP. Do not specify the bound of a character array initialized with a string literal |
| ISO/IEC TR 24772:2013 | String Termination [CJM] |

## Bibliography

|  |  |
| ----|----|
| [ECTC 1998] | Section A.8, "Character Array Initialization" |
| [ISO/IEC 9899:2011] | Subclause 6.7.9, "Initialization" |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152217) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_)
## Comments:

|  |
| ----|
| This seems to contradict ARR02-C!
                                        Posted by svoboda at Nov 21, 2008 14:43
                                     |
| Addressed. This rule is an exception to ARR02-C.
                                        Posted by svoboda at Jun 25, 2009 10:41
                                     |

