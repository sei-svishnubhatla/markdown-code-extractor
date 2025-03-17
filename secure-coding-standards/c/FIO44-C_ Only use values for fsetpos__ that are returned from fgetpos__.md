The C Standard, 7.23.9.3 paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines the following behavior for `fsetpos()`:
> The `fsetpos` function sets the `mbstate_t` object (if any) and file position indicator for the stream pointed to by `stream` according to the value of the object pointed to by `pos`, which shall be a value obtained from an earlier successful call to the `fgetpos` function on a stream associated with the same file.

Invoking the `fsetpos()` function with any other values for `pos` is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
This noncompliant code example attempts to read three values from a file and then set the file position pointer back to the beginning of the file:
``` c
#include <stdio.h>
#include <string.h>
int opener(FILE *file) {
  int rc;
  fpos_t offset;
  memset(&offset, 0, sizeof(offset));
  if (file == NULL) { 
    return -1;
  }
  /* Read in data from file */
  rc = fsetpos(file, &offset);
  if (rc != 0 ) {
    return rc;
  }
  return 0;
}
```
Only the return value of an `fgetpos()` call is a valid argument to `fsetpos()`; passing a value of type `fpos_t` that was created in any other way is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Compliant Solution
In this compliant solution, the initial file position indicator is stored by first calling `fgetpos()`, which is used to restore the state to the beginning of the file in the later call to `fsetpos()`:
``` c
#include <stdio.h>
#include <string.h>
int opener(FILE *file) {
  int rc;
  fpos_t offset;
  if (file == NULL) {
    return -1;
  }
  rc = fgetpos(file, &offset);
  if (rc != 0 ) {
    return rc;
  }
  /* Read in data from file */
  rc = fsetpos(file, &offset);
  if (rc != 0 ) {
    return rc;
  }
  return 0;
}
```
## Risk Assessment
Misuse of the `fsetpos()` function can position a file position indicator to an unintended location in the file.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO44-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users can add a custom check for violations of this constraint. |
| Compass/ROSE |  |  | Can detect common violations of this rule. However, it;cannot handle cases in which the value returned by fgetpos() is copied between several variables before being passed to fsetpos() |
| Cppcheck Premium | 24.11.0 | premium-cert-fio44-c |  |
| Helix QAC | 2024.4 | DF4841, DF4842, DF4843 |  |
| Klocwork | 2024.4 | CERT.FSETPOS.VALUE |  |
| LDRA tool suite | 9.7.1 | 82 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO44-a | Only use values for fsetpos() that are returned from fgetpos() |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO44-C | Checks for invalid file position (rule partially covered) |
| PVS-Studio | 7.35 | V1035 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO44-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961:2013 | Using a value for fsetpos other than a value returned from fgetpos [xfilepos] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.23.9.3, "The fsetpos Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151938) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151941)
