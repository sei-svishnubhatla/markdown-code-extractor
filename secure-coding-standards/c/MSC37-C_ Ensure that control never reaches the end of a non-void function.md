If control reaches the closing curly brace (`}`) of a non-`void` function without evaluating a `return` statement, using the return value of the function call is [undefined behavior.](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) (See [undefined behavior 86](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_86).)
## Noncompliant Code Example
In this noncompliant code example, control reaches the end of the `checkpass()` function when the two strings passed to `strcmp()` are not equal, resulting in undefined behavior. Many compilers will generate code for the `checkpass()` function, returning various values along the execution path where no `return` statement is defined.
``` c
#include <string.h>
#include <stdio.h>
int checkpass(const char *password) {
  if (strcmp(password, "pass") == 0) {
    return 1;
  }
}
void func(const char *userinput) {
  if (checkpass(userinput)) {
    printf("Success\n");
  }
}
```
This error is frequently diagnosed by compilers. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)
## Compliant Solution
This compliant solution ensures that the `checkpass()` function always returns a value:
``` c
#include <string.h>
#include <stdio.h>
int checkpass(const char *password) {
  if (strcmp(password, "pass") == 0) {
    return 1;
  }
  return 0;
}
void func(const char *userinput) {
  if (checkpass(userinput)) {
    printf("Success!\n");
  }
}
```
## Noncompliant Code Example
In this noncompliant code example, control reaches the end of the `getlen()` function when `input` does not contain the integer `delim`. Because the potentially undefined return value of `getlen()` is later used as an index into an array, a buffer overflow may occur.
``` c
#include <stddef.h>
size_t getlen(const int *input, size_t maxlen, int delim) {
  for (size_t i = 0; i < maxlen; ++i) {
    if (input[i] == delim) {
      return i;
    }
  }
}
void func(int userdata) {
  size_t i;
  int data[] = { 1, 1, 1 };
  i = getlen(data, sizeof(data), 0);
  data[i] = userdata;
}
```
### Implementation Details (GCC)
Violating this rule can have unexpected consequences, as in the following example:
``` c
#include <stdio.h>
size_t getlen(const int *input, size_t maxlen, int delim) {
  for (size_t i = 0; i < maxlen; ++i) {
    if (input[i] == delim) {
      return i;
    }
  }
}
int main(int argc, char **argv) {
  size_t i;
  int data[] = { 1, 1, 1 };
  i = getlen(data, sizeof(data), 0);
  printf("Returned: %zu\n", i);
  data[i] = 0;
  return 0;
}
```
When this program is compiled with `-Wall` on most versions of the GCC compiler, the following warning is generated:
``` java
example.c: In function 'getlen':
example.c:12: warning: control reaches end of non-void function
```
None of the inputs to the function equal the delimiter, so when run with GCC 5.3 on Linux, control reaches the end of the `getlen()` function, which is undefined behavior and in this test returns `3`, causing an out-of-bounds write to the `data` array.
## Compliant Solution
This compliant solution changes the interface of `getlen()` to store the result in a user-provided pointer and returns a status indicator to report success or failure. The best method for handling this type of error is specific to the application and the type of error. (See [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy) for more on error handling.)
``` c
#include <stddef.h>
int getlen(const int *input, size_t maxlen, int delim,
           size_t *result) {
  if (result == NULL) {
    return -1;
  }
  for (size_t i = 0; i < maxlen; ++i) {
    if (input[i] == delim) {
      *result = i;
      return 0;
    }
  }
  return -1;
}
void func(int userdata) {
  size_t i;
  int data[] = {1, 1, 1};
  if (getlen(data, sizeof(data), 0, &i) != 0) {
    /* Handle error */
  } else {
    data[i] = userdata;
  }
}
```
## Exceptions
**MSC37-C-EX1:** According to the C Standard, 5.1.2.3.4, paragraph 1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], "Reaching the `}` that terminates the main function returns a value of 0." As a result, it is permissible for control to reach the end of the main() function without executing a return statement.
**MSC37-C-EX2: **It is permissible for a control path to not return a value if that code path is never taken and a function marked `_Noreturn` is called as part of that code path. For example:
``` c
#include <stdio.h>
#include <stdlib.h>
_Noreturn void unreachable(const char *msg) {
  printf("Unreachable code reached: %s\n", msg);
  exit(1);
}
enum E {
  One,
  Two,
  Three
};
int f(enum E e) {
  switch (e) {
  case One: return 1;
  case Two: return 2;
  case Three: return 3;
  }
  unreachable("Can never get here");
}
```
## Risk Assessment
Using the return value from a non-`void` function where control reaches the end of the function without evaluating a `return` statement can lead to buffer overflow [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) as well as other [unexpected program behaviors](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC37-C | High | Unlikely | Low | P9 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC37-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | return-implicit | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MSC37 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.MRS | Missing return statement |
| Coverity | 2017.07 | MISSING_RETURN | Implemented |
| Cppcheck | ;2.15 | missingReturn |  |
| Cppcheck Premium | 24.11.0 | missingReturn |  |
| Helix QAC | 2024.4 | C++4022DF2888 |  |
| Klocwork | 2024.4 | FUNCRET.GENFUNCRET.IMPLICIT |  |
| LDRA tool suite | 9.7.1 | 2 D, 36 S, 66 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC37-a | All exit paths from a function, except main(), with non-void return type shall have an explicit return statement with an expression |
| PC-lint Plus | 1.4 | 533 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC37-C | Checks for missing return statement (rule fully covered) |
| RuleChecker | 24.04 | return-implicit | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S935 |  |
| TrustInSoft Analyzer | 1.38 | Body of function falls-through | Exhaustively verified. |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | MSC01-C. Strive for logical completeness | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-758 | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-758 and MSC37-C
Independent( INT34-C, INT36-C, MEM30-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( MSC37-C, list) where list =
Undefined behavior that results from anything other than failing to return a value from a function that expects one
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 5.1.2.3.4, "Program Termination" |

------------------------------------------------------------------------
[](../c/MSC33-C_%20Do%20not%20pass%20invalid%20data%20to%20the%20asctime__%20function) [](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152297)
## Comments:

|  |
| ----|
| So I have a (perhaps) interesting question.; Should there be a mention of cases involving _Noreturn functions?
_Noreturn void die();  // Implemented somewhere
int do_something(/*params*/) {
  _Bool ok = true;
  /* Code that does the calculation and possibly sets 'ok' to false */
  if (ok)
    return 42;
  die();
  /* Can never get here because die is _Noreturn */
}

In this case, I would say that control never reaches the end of the function, and so it's fine.  However, some compilers may still warn (especially if they don't understand `_Noreturn` particularly well, or if the `_Noreturn` is abstracted away behind a macro and the compiler doesn't support `_Noreturn` at all).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 19, 2013 10:47
\| \|
Offhand, no. The {{\_Noreturn}} keyword indicates that a function \*never\* returns. Your code has the function returning a value sometimes and not returning anything otherwise. (Yes, I am ignoring the fact that {{ok}} is always true in your code....this code violates our rec about not having dead code.)
We could have rules saying when to use noreturn (eg your noreturn function must always be void), but they are prob best left distinct from this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 26, 2013 12:12
\| \|
Hmm, my code has a function returning a value sometimes, and otherwise not returning at all (hence, control never reaches the **end** of the function without returning a value). This is actually a very common code pattern that you see in the wild, especially with fully-covered switch statements. e.g.,;<http://clang.llvm.org/doxygen/SemaInit_8cpp_source.html#l05311> (llvm_unreachable eventually calls a `_Noreturn`-marked function).
I actually think this makes for a reasonable exception, or some other form of mention that specifically makes this code pattern conforming to this rule.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 25, 2016 16:32
\| \|
Hah, glad to see I am self-consistent. See;**MSC54-CPP-EX2**. ![](images/icons/emoticons/wink.svg) I will add a similar exception here.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Apr 25, 2016 16:50
\| \|
This warning is as the admonition portrayed In kind with no value. If control arrives at the end of a function and no return is encountered, GCC accepts an arrival with no arrival value. However, for this, the capacity requires an arrival value. Toward the finish of the function, return suitable value, regardless of whether control never comes there.Also you can solve that by doing follows:  
The problem is that other compilers have a warning about "unreachable code". If every switch case is handled, the compiler detects that the return statement cannot be reached. I have to suppress this warning or use the preprocessor to only have that return statement on certain compilers. Something like this piece of code.   Link to the code.https://kodlogs.com/blog/852/warning-control-reaches-end-non-void-function-wreturn-type
![](images/icons/contenttypes/comment_16.png) Posted by danikiw542 at Nov 21, 2020 14:46
\| \|
Doesn't MSC37-C-EX2 already cover all of this?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Nov 23, 2020 10:18
\|
