Do not invoke `getc()` or `putc()` or their wide-character analogues `getwc()` and `putwc()` with a stream argument that has side effects. The stream argument passed to these macros may be evaluated more than once if these functions are implemented as unsafe macros. (See [PRE31-C. Avoid side effects in arguments to unsafe macros](PRE31-C_%20Avoid%20side%20effects%20in%20arguments%20to%20unsafe%20macros) for more information.)
This rule does not apply to the character argument in `putc()` or the wide-character argument in `putwc()`, which is guaranteed to be evaluated exactly once.
## Noncompliant Code Example (`getc()`)
This noncompliant code example calls the `getc()` function with an expression as the stream argument. If `getc()` is implemented as a macro, the file may be opened multiple times. (See [FIO24-C. Do not open a file that is already open](FIO24-C_%20Do%20not%20open%20a%20file%20that%20is%20already%20open).)
``` c
#include <stdio.h>
void func(const char *file_name) {
  FILE *fptr;
  int c = getc(fptr = fopen(file_name, "r"));
  if (feof(fptr) || ferror(fptr)) {
    /* Handle error */
  }
  if (fclose(fptr) == EOF) {
    /* Handle error */
  }
}
```
This noncompliant code example also violates [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) because the value returned by `fopen()` is not checked for errors.
## Compliant Solution (`getc()`)
In this compliant solution, `fopen()` is called before `getc()` and its return value is checked for errors:
``` c
#include <stdio.h>
void func(const char *file_name) {
  int c;
  FILE *fptr;
  fptr = fopen(file_name, "r");
  if (fptr == NULL) {
    /* Handle error */
  }
  c = getc(fptr);
  if (c == EOF) {
    /* Handle error */
  }
  if (fclose(fptr) == EOF) {
    /* Handle error */
  }
}
```
## Noncompliant Code Example (`putc()`)
In this noncompliant example, `putc()` is called with an expression as the stream argument. If `putc()` is implemented as a macro, this expression might be evaluated multiple times.
``` c
#include <stdio.h>
void func(const char *file_name) {
  FILE *fptr = NULL;
  int c = 'a';
  while (c <= 'z') {
    if (putc(c++, fptr ? fptr :
         (fptr = fopen(file_name, "w"))) == EOF) {
      /* Handle error */
    }
  }
  if (fclose(fptr) == EOF) {
    /* Handle error */
  }
}
```
This noncompliant code example might appear safe even if the `putc()` macro evaluates its stream argument multiple times, as the ternary conditional expression ostensibly prevents multiple calls to `fopen()`. However, the assignment to `fptr` and the evaluation of `fptr` as the controlling expression of the ternary conditional expression can take place between the same sequence points, resulting in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) (a violation of [EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects)). This code also violates [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) because it fails to check the return value from `fopen()`.
## Compliant Solution (`putc()`)
In this compliant solution, the stream argument to `putc()` no longer has side effects:
``` c
#include <stdio.h>
void func(const char *file_name) {
  int c = 'a'; 
  FILE *fptr = fopen(file_name, "w");
  if (fptr == NULL) {
    /* Handle error */
  }
  while (c <= 'z') {
    if (putc(c++, fptr) == EOF) {
      /* Handle error */
    }
  }
  if (fclose(fptr) == EOF) {
    /* Handle error */
  }
}
```
The expression `c++` is perfectly safe because `putc()` guarantees to evaluate its character argument exactly once.
NOTE: The output of this compliant solution differs depending on the character set. For example, when run on a machine using an ASCII-derived code set such as ISO-8859 or Unicode, this solution will print out the 26 lowercase letters of the English alphabet. However, if run with an EBCDIC-based code set, such as Codepage 037 or Codepage 285, punctuation marks or symbols may be output between the letters.
## Risk Assessment
Using an expression that has side effects as the stream argument to `getc()`, `putc()`, or `getwc()` can result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO41-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stream-argument-with-side-effects | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO41 |  |
| Cppcheck Premium | 24.11.0 | premium-cert-fio41-c |  |
| Helix QAC | 2024.4 | C5036C++3225, C++3229 |  |
| LDRA tool suite | 9.7.1 | 35 D, 1 Q, 9 S,30 S, 134 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO41-aCERT_C-FIO41-b | Do not call 'getc()', 'putc()', 'getwc()', or 'putwc()' with a stream argument containing assignments, increment or decrement operatorsDo not call 'getc()', 'putc()', 'getwc()', or 'putwc()' with a stream argument containing function calls or function-like macro calls |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO41-C | Checks for stream arguments with possibly unintended side effects (rule fully covered) |
| RuleChecker | 24.04 | stream-argument-with-side-effects | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO41-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | FIO24-C. Do not open a file that is already open | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | EXP30-C. Do not depend on the order of evaluation for side effects | Prior to 2018-01-12: CERT: Unspecified Relationship |

------------------------------------------------------------------------
[](../c/FIO40-C_%20Reset%20strings%20on%20fgets__%20%20or%20fgetws__%20failure) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151938)
## Comments:

|  |
| ----|
| The compliant version for getc() should be fixed like below, for correct management of fopen potential issue :#include <stdio.h>  
void func(const char *file_name) {
    int c;
    FILE *fptr;
    fptr = fopen(file_name, "r");
    if (fptr == NULL) {
        /* Handle error */
    }        else { 
        c = getc(fptr);
        if (c == EOF) {
            /* Handle error */
        }
        if (fclose(fptr) == EOF) {
            /* Handle error */
        }        }
}
                                        Posted by obinnert at Apr 13, 2021 03:55
                                     |
| Our convention for "Handle Error" originated in the mists of time. It was borne out of our realization that each application (and library) has its own way of handling errors. While we have a section of rules & recommendations about error handling, we do not dictate how code should handle errors.Our convention is that "handle error" (which appears in all our coding standards) either does not return, or (if it does) it "fixes" the problem somehow. For example, in the "getc()" compliant solution, you may assume that if the first "Handle Error" falls through, then it has somehow assigned fptr to a valid input stream.Your proposed solution for getc() is a valid (partial) interpretation of what might actually happen in the "handle error" code.
                                        Posted by svoboda at Apr 13, 2021 11:56
                                     |
| I have documented our "Handle Error" convention here:;How this Coding Standard is Organized#CodingConventions
                                        Posted by svoboda at Apr 13, 2021 13:25
                                     |
| Thanks.
                                        Posted by obinnert at Apr 13, 2021 13:44
                                     |
| A minor issue in the non compliant code for getc():The code refers to stdin while checking for EOF or error condition, I think it should be fptr.While technically "correct" code, it makes no sense to check for stdin in this context.
                                        Posted by fezm at Jun 04, 2021 05:58
                                     |
| Agreed, fixed.
                                        Posted by svoboda at Jun 04, 2021 08:04
                                     |

