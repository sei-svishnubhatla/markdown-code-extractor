According to the C Standard, 7.23.3, paragraph 6 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> The address of the `FILE` object used to control a stream may be significant; a copy of a `FILE` object is not required to serve in place of the original.

Consequently, do not copy a `FILE` object.
## Noncompliant Code Example
This noncompliant code example can fail because a by-value copy of `stdout` is being used in the call to `fputs()`:
``` c
#include <stdio.h>
int main(void) {
  FILE my_stdout = *stdout;
  if (fputs("Hello, World!\n", &my_stdout) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
When compiled under Microsoft Visual Studio 2013 and run on Windows, this noncompliant example results in an "access violation" at runtime.
## Compliant Solution
In this compliant solution, a copy of the `stdout` pointer to the `FILE` object is used in the call to `fputs()`:
``` c
#include <stdio.h>
int main(void) {
  FILE *my_stdout = stdout;
  if (fputs("Hello, World!\n", my_stdout) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
## Risk Assessment
Using a copy of a `FILE` object in place of the original may result in a crash, which can be used in a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO38-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | file-dereference | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO38 | Fully implemented |
| Clang | 3.9 | misc-non-copyable-objects | Checked with clang-tidy |
| Compass/ROSE |  |  | Can detect simple violations of this rule |
| Coverity | 2017.07 | MISRA C 2012 Rule 22.5 | Partially implemented |
| Cppcheck Premium | 24.11.0
 | premium-cert-fio38-c |  |
| Helix QAC | 2024.4 | C1485, C5028C++3113, C++3114 |  |
| Klocwork | 2024.4 | MISRA.FILE_PTR.DEREF.2012MISRA.FILE_PTR.DEREF.CAST.2012
MISRA.FILE_PTR.DEREF.INDIRECT.2012
MISRA.FILE_PTR.DEREF.RETURN.2012 |  |
| LDRA tool suite | 9.7.1 | 591 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO38-a | A pointer to a FILE object shall not be dereferenced |
| PC-lint Plus | 1.4 | 9047 | Partially supported: reports when a FILE pointer is dereferenced |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO38-C | Checks for misuse of a FILE object (rule fully covered) |
| RuleChecker | 24.04 | file-dereference | Partially checked |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO38-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961:2013 | Copying a FILE object [filecpy] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.23.3, "Files" |

------------------------------------------------------------------------
[](../c/FIO37-C_%20Do%20not%20assume%20that%20fgets__%20or%20fgetws__%20returns%20a%20nonempty%20string%20when%20successful) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152175)
