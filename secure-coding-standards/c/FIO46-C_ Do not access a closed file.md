Using the value of a pointer to a `FILE` object after the associated file is closed is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 153](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_153).) Programs that close the standard streams (especially `stdout` but also `stderr` and `stdin`) must be careful not to use these streams in subsequent function calls, particularly those that implicitly operate on them (such as `printf()`, `perror()`, and `getc()`).
This rule can be generalized to other file representations.
## Noncompliant Code Example
In this noncompliant code example, the `stdout` stream is used after it is closed:
``` c
#include <stdio.h>
int close_stdout(void) {
  if (fclose(stdout) == EOF) {
    return -1;
  }
  printf("stdout successfully closed.\n");
  return 0;
}
```
## Compliant Solution
In this compliant solution, `stdout` is not used again after it is closed. This must remain true for the remainder of the program, or `stdout` must be assigned the address of an open file object. 
``` c
#include <stdio.h>
int close_stdout(void) {
  if (fclose(stdout) == EOF) {
    return -1;
  }
  fputs("stdout successfully closed.", stderr);
  return 0;
}
```
## Risk Assessment
Using the value of a pointer to a `FILE` object after the associated file is closed is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO46-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| CodeSonar | 8.3p0 | IO.UAC | Use after close |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | USE_AFTER_FREE | Implemented |
| Helix QAC | 2024.4 | DF2696, DF2697, DF2698 |  |
| Klocwork | 2024.4 | SV.INCORRECT_RESOURCE_HANDLING.URH |  |
| LDRA tool suite | 9.7.1 | 48 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO46-a | Do not use resources that have been freed |
| PC-lint Plus | 1.4 | 2471 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO46-C | Checks for use of previously closed resource (rule partially covered) |
| SonarQube C/C++ Plugin | 3.11 | S3588 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO46-C).
## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, open |
| [ISO/IEC 9899:2024]; | Subclause 7.23.3, "Files"Subclause 7.23.5.1, "The fclose Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151941) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152167)
