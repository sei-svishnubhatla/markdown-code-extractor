If either of the C Standard `fgets()` or `fgetws()` functions fail, the contents of the array being written is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue). (See [undefined behavior 175](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_175).)  It is necessary to reset the string to a known value to avoid errors on subsequent string manipulation functions.
## Noncompliant Code Example
In this noncompliant code example, an error flag is set if `fgets()` fails. However, `buf` is not reset and has indeterminate contents:
``` c
#include <stdio.h>
enum { BUFFER_SIZE = 1024 };
void func(FILE *file) {
  char buf[BUFFER_SIZE];
  if (fgets(buf, sizeof(buf), file) == NULL) {
    /* Set error flag and continue */
  }
}
```
## Compliant Solution
In this compliant solution, `buf` is set to an empty string if `fgets()` fails. The equivalent solution for `fgetws()` would set `buf` to an empty wide string.
``` c
#include <stdio.h>
enum { BUFFER_SIZE = 1024 };
void func(FILE *file) {
  char buf[BUFFER_SIZE];
  if (fgets(buf, sizeof(buf), file) == NULL) {
    /* Set error flag and continue */
    *buf = '\0';
  }
}
```
## Exceptions
**FIO40-C-EX1:** If the string goes out of scope immediately following the call to `fgets()` or `fgetws()` or is not referenced in the case of a failure, it need not be reset.
## Risk Assessment
Making invalid assumptions about the contents of an array modified by `fgets()` or `fgetws()` can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO40-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.MEM.UVAR | Uninitialized Variable |
| Cppcheck Premium | 24.11.0 | premium-cert-fio40-c |  |
| Helix QAC | 2024.4 | DF4861, DF4862, DF4863 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO40-a | Reset strings on fgets() or fgetws() failure |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO40-C | Checks for use of indeterminate string (rule partially covered) |
| PVS-Studio | 7.35 | V1024 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO40-C).
------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152175) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](../c/FIO41-C_%20Do%20not%20call%20getc__,%20putc__,%20getwc__,%20or%20putwc__%20with%20a%20stream%20argument%20that%20has%20side%20effects)
## Comments:

|  |
| ----|
| We need some sort of exception on this rule, such as if fgets() is the last statement in a function, do we still need to zero out its buffer? Likewise, if the buffer never actually gets touched in the case of an error (suppose the if statement's then-clause logs an error message and then {{return}}s, or calls abort()), is clearing the buffer still worthwhile?
Also, the NCCE needs to clarify that the problem is that buf may be treated as if it has legit data. (eg after the then-clause is executed, the subsequent code may treat buf as legit data.)
                                        Posted by svoboda at Jul 07, 2008 14:44
                                     |
| I don't think this is rose-possible after all... we'd need to do flow analysis to figure out which branches are taken in the case of failure
                                        Posted by avolkovi at Jul 09, 2008 11:34
                                     |
| Is this truly different from ERR33-C. Detect and handle standard library errors?; At the end of the day, any time the library returns an error, you should detect and handle it without assuming the state of the buffers (unless they're specified to be in a particular state), so it seems like this rule is a specific case of a more general problem.
                                        Posted by aballman at Aug 15, 2013 15:01
                                     |
| Well, ERR33-C mentions fgets() but doesn't mention that it scrambles the input string. I suppose you could fold this rule into ERR33-C but you then have to add this rule's contents to that one.
                                        Posted by svoboda at Aug 15, 2013 17:16
                                     |
| I was thinking something more general than that.; A new ERR rule that lists all of the APIs which leave their arguments in an indeterminate state on error (fgets, fread, and so on).  This way we don't have to call out each API specifically in their own guidelines (so it would supersede FIO40-C, and possibly others).
                                        Posted by aballman at Aug 15, 2013 22:38
                                     |
| That would be a good idea. Not sure how many methods leave args in an 'indeterminate' state..coming up with that list will take a few hours of perusing the standard. But it would still be useful.
                                        Posted by svoboda at Aug 16, 2013 09:37
                                     |

