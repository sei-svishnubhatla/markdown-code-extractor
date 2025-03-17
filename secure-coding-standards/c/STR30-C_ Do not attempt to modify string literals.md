According to the C Standard, 6.4.5, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]:
> A character string literal is a sequence of zero or more multibyte characters enclosed in double-quotes, as in "xyz". A UTF-8 string literal is the same, except prefixed by u8. A wchar_t string literal is the same, except prefixed by L. A UTF-16 string literal is the same, except prefixed by u. A UTF-32 string literal is the same, except prefixed by U. Collectively, wchar_t, UTF-16, and UTF-32 string literals are called wide string literals.

At compile time, string literals are used to create an array of static storage duration of sufficient length to contain the character sequence and a terminating null character. String literals are usually referred to by a pointer to (or array of) characters. Ideally, they should be assigned only to pointers to (or arrays of) `const char` or `const wchar_t`. It is unspecified whether these arrays of string literals are distinct from each other. The behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if a program attempts to modify any portion of a string literal. Modifying a string literal frequently results in an access violation because string literals are typically stored in read-only memory. (See [undefined behavior 32](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_32).)
Avoid assigning a string literal to a pointer to non-`const` or casting a string literal to a pointer to non-`const`. For the purposes of this rule, a pointer to (or array of) `const` characters must be treated as a string literal. Similarly, the returned value of the following library functions must be treated as a string literal if the first argument is a string literal:
-   `strpbrk(), strchr(), strrchr(), strstr()`
-   `wcspbrk(), wcschr(), wcsrchr(), wcsstr()`
-   `memchr(), wmemchr()`
This rule is a specific instance of [EXP40-C. Do not modify constant objects](EXP40-C_%20Do%20not%20modify%20constant%20objects).
## Noncompliant Code Example
In this noncompliant code example, the `char` pointer `str` is initialized to the address of a string literal. Attempting to modify the string literal is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
char *str  = "string literal";
str[0] = 'S';
```
## Compliant Solution
As an array initializer, a string literal specifies the initial values of characters in an array as well as the size of the array. (See [STR11-C. Do not specify the bound of a character array initialized with a string literal](STR11-C_%20Do%20not%20specify%20the%20bound%20of%20a%20character%20array%20initialized%20with%20a%20string%20literal).) This code creates a copy of the string literal in the space allocated to the character array `str`. The string stored in `str` can be modified safely.
``` c
char str[] = "string literal";
str[0] = 'S';
```
## Noncompliant Code Example (POSIX)
In this noncompliant code example, a string literal is passed to the (pointer to non-`const`) parameter of the POSIX function [`mkstemp()`](http://pubs.opengroup.org/onlinepubs/9699919799/functions/mkstemp.html), which then modifies the characters of the string literal:
``` c
#include <stdlib.h>
void func(void) {
  mkstemp("/tmp/edXXXXXX");
}
```
The behavior of `mkstemp()` is described in more detail in [FIO21-C. Do not create temporary files in shared directories](FIO21-C_%20Do%20not%20create%20temporary%20files%20in%20shared%20directories).
## Compliant Solution (POSIX)
This compliant solution uses a named array instead of passing a string literal:
``` c
#include <stdlib.h>
void func(void) {
  static char fname[] = "/tmp/edXXXXXX";
  mkstemp(fname);
}
```
## Noncompliant Code Example (Result of `strrchr()`)
In this noncompliant example, the `char *` result of the `strrchr()` function is used to modify the object pointed to by `pathname`. Because the argument to `strrchr()` points to a string literal, the effects of the modification are undefined.
``` c
#include <stdio.h>
#include <string.h>
const char *get_dirname(const char *pathname) {
  char *slash;
  slash = strrchr(pathname, '/');
  if (slash) {
    *slash = '\0'; /* Undefined behavior */
  }
  return pathname;
}
int main(void) {
  puts(get_dirname(__FILE__));
  return 0;
}
```
## Compliant Solution (Result of `strrchr()`)
This compliant solution avoids modifying a `const` object, even if it is possible to obtain a non-`const` pointer to such an object by calling a standard C library function, such as `strrchr()`. To reduce the risk to callers of `get_dirname()`, a buffer and length for the directory name are passed into the function. It is insufficient to change `pathname` to require a `char *` instead of a `const char *` because conforming compilers are not required to diagnose passing a string literal to a function accepting a `char *`.
``` c
#include <stddef.h>
#include <stdio.h>
#include <string.h>
char *get_dirname(const char *pathname, char *dirname, size_t size) {
  const char *slash;
  slash = strrchr(pathname, '/');
  if (slash) {
    ptrdiff_t slash_idx = slash - pathname;
    if ((size_t)slash_idx < size) {
      memcpy(dirname, pathname, slash_idx);
      dirname[slash_idx] = '\0';      
      return dirname;
    }
  }
  return 0;
}
int main(void) {
  char dirname[260];
  if (get_dirname(__FILE__, dirname, sizeof(dirname))) {
    puts(dirname);
  }
  return 0;
}
```
## Risk Assessment
Modifying string literals can lead to [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) and possibly [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR30-C | Low | Likely | Low | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | string-literal-modficationwrite-to-string-literal | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR30 | Fully implemented |
| Compass/ROSE |  |  | Can detect simple violations of this rule |
| Coverity | 2017.07 | PW | Deprecates conversion from a string literal to "char *" |
| Helix QAC | 2024.4 | C0556, C0752, C0753, C0754C++3063, C++3064, C++3605, C++3606, C++3607 |  |
| Klocwork | 2024.4 | CERT.STR.ARG.CONST_TO_NONCONSTCERT.STR.ASSIGN.CONST_TO_NONCONST |  |
| LDRA tool suite | 9.7.1 | 157 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR30-aCERT_C-STR30-b | A string literal shall not be modifiedDo not modify string literals |
| PC-lint Plus | 1.4 | 489, 1776 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR30-C | Checks for writing to const qualified object (rule fully covered) |
| PVS-Studio | 7.35 | V675 |  |
| RuleChecker | 24.04 | string-literal-modfication | Partially checked |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | mem_access | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnurability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | EXP05-C. Do not cast away a const qualification | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | STR11-C. Do not specify the bound of a character array initialized with a string literal | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Modifying string literals [strmod] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.4.5, "String Literals" |
| [Plum 1991] | Topic 1.26, "Strings—String Literals" |
| [Summit 1995] | comp.lang.c FAQ List, Question 1.32 |

------------------------------------------------------------------------
[](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152048)
## Comments:

|  |
| ----|
| The mktemp() CS is only safe if the template name must be used just once.; On subsequent passes through the code, the mktemp() function will do nothing because the template passed to it contains no X's.  Using mktemp() correctly is harder than it seems!  And that's before you deal with the real security issue with it - that is addressed by the mkstemp() function.
I was (and am) bitterly disappointed that the Safe C supplement doesn't provide safe versions of mktemp() that actually open the file to guarantee that there are no TOCTOU (time of check, time of use) issues.  That is the real security issue for mktemp() and maybe the example is ill-chosen - or needs more work.
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 19:13
                                     |
| There is a standard function "tmpfile" that opens an automatically deleted temp file, which on reasonable POSIX systems is implemented by unlinking the entry immediately after file creation, having created its own name incorporating the PID and;having created the file in exclusive-open mode, retrying with another name until it gets a file.
                                        Posted by dagwyn at Apr 16, 2008 21:27
                                     |
| static is wrong here, unless you want to create file once (because XXXXXX will be replaced, and never restored).
#include <stdlib.h>
#include <stdio.h>
void temp_wrong(void) {
    static char fname[] = "/tmp/edXXXXXX";
    mkstemp(fname);
    puts(fname);
}
void temp_correct(void) {
    char fname[] = "/tmp/edXXXXXX";
    mkstemp(fname);
    puts(fname);
}
void repeat(int times, void (*callback)(void)) {
    int i;
    for (i = 0; i < times; i++) {
        callback();
    }
}
int main(void) {
    repeat(3, temp_wrong);
    repeat(3, temp_correct);
    return 0;
}

![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Dec 10, 2013 12:45
\| \|
You are correct; I've rectified it.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Dec 11, 2013 08:33
\| \|
"This rule is a specific instance of [EXP40-C. Do not modify constant objects](https://wiki.sei.cmu.edu/confluence/display/c/EXP40-C.+Do+not+modify+constant+objects)." Is this true? Aren't string literals in C not `const` despite the fact that you're not allowed to modify them?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 06, 2020 15:08
\| \|
I think that's splitting hairs. It's UB to attempt to modify a string literal per C17 6.4.5p7 because the array is logically const, even if the underlying type of the elements are not;`const char`. That said, you're technically correct (which is the best kind of correct) so maybe a mention about that is worthwhile (however, I'm not convinced it adds a ton of value for the reader as opposed to being trivia).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 06, 2020 15:19
\| \|
Right. There is, unfortunately, a schism between what C considers constant and what human beings consider constant, and string literals fall inside that schism.
FTM that was my first proposal to WG14, to make string literals be const (as they are in C++). The proposal was rejected on the grounds that it would break too much old code.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 06, 2020 15:44
\| \|
Why is the Rem Cost low here? I suspect the theory is that many such examples, such as the first two, can be repaired by taking a char\* and changing it to a char\[\]. That is, a char\* (presuambly where the pointer is on the stack) initialized to a string literal becomes a char array, and the literal simply gets initialized on the stack, not the global segment. Strings on the stack can be changed easily.
But the last compliant solution throws that all to hell. Mainly because the strchr() and strrchr() functions take a const char\* string and return an element within it with the const cast away. ;This is a std C library problem, but the compliant solution can clearly not be automatically generated by repairing the NCCE.
So perhaps the rem cost should be "usually low, but occasionally medium"?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 22, 2023 16:48
\|
