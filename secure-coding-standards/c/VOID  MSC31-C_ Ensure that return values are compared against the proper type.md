> [!warning]  
>
> This guideline has been deprecated.  It has been superseded by:
>
> -   [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](INT31-C_%20Ensure%20that%20integer%20conversions%20do%20not%20result%20in%20lost%20or%20misinterpreted%20data)
> -   [FLP07-C. Cast the return value of a function that returns a floating-point type](FLP07-C_%20Cast%20the%20return%20value%20of%20a%20function%20that%20returns%20a%20floating-point%20type)
> -   [INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](INT18-C_%20Evaluate%20integer%20expressions%20in%20a%20larger%20size%20before%20comparing%20or%20assigning%20to%20that%20size)

Functions must compare their return value against literal constants of the same type when those types are only partially specified by the standard. If a type is partially specified as an "arithmetic type" or an "unsigned integer," the C Standard allows that type to be implemented using a range of underlying types. When a partially specified type is implemented as `unsigned char` or `unsigned short`, values of that type will not compare equal to integer literals such as `-1` on certain architectures.
## Noncompliant Code Example (`time_t`)
The `time()` function returns a `(time_t)(-1)` to indicate that the calendar time is not available. The C Standard requires only that the `time_t` type is an arithmetic type capable of representing time. It is left to the implementor to decide the best arithmetic type to use to represent time. If `time_t` is implemented as an unsigned integer type smaller than a signed `int`, the return value of `time()` will never compare equal to the integer literal `-1`.
``` c
#include <time.h>
void func(void) {
  time_t now = time(NULL);
  if (now != -1) {
    /* Continue processing */
  }
}
```
## Compliant Solution (`time_t`)
To ensure the comparison is properly performed, the return value of `time()` should be compared against `-1` cast to type `time_t`:
``` c
#include <time.h>
void func(void) {
  time_t now = time(NULL);
  if (now != (time_t)-1) {
    /* Continue processing */
  }
}
```
This solution is in accordance with [INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](INT18-C_%20Evaluate%20integer%20expressions%20in%20a%20larger%20size%20before%20comparing%20or%20assigning%20to%20that%20size).
## Noncompliant Code Example (`size_t`)
The `mbstowcs()` function converts a multibyte string to a wide character string, returning the number of characters converted. If an invalid multibyte character is encountered, `mbstowcs()` returns `(size_t)(-1)`. Depending on how `size_t` is implemented, comparing the return value of `mbstowcs()` to signed integer literal `-1` may not evaluate as expected.
``` c
#include <stdlib.h>
void func(wchar_t *pwcs, const char *restrict s, size_t n) {
  size_t count_modified = mbstowcs(pwcs, s, n);
  if (count_modified == -1) {
    /* Handle error */
  }
}
```
## Compliant Solution (`size_t`)
To ensure the comparison is properly performed, the return value of `mbstowcs()` should be compared against `-1` cast to type `size_t`:
``` c
#include <stdlib.h>
void func(wchar_t *pwcs, const char *restrict s, size_t n) {
  size_t count_modified = mbstowcs(pwcs, s, n);
  if (count_modified == (size_t)-1) {
    /* Handle error */
  }
}
```
This solution is in accordance with [INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](INT18-C_%20Evaluate%20integer%20expressions%20in%20a%20larger%20size%20before%20comparing%20or%20assigning%20to%20that%20size).
## Risk Assessment
Comparing return values against a value of a different type can result in incorrect calculations, leading to unintended program behavior and possibly abnormal program termination.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC31-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| LDRA tool suite | 9.7.1 | 456 S | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 1253 | Partially implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC31-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size; |
| SEI CERT C++ Coding Standard | VOID MSC31-CPP. Ensure that return values are compared against the proper type |
| MITRE CWE | CWE-697, Insufficient comparisonCWE-704, Incorrect type conversion or cast |

## Bibliography

|  |  |
| ----|----|
| [Kettlewell 2002] | Section 4, "Type Assumptions" |
| [Pfaff 2004] | ; |
| [SecuriTeam 2007] | ; |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MSC30-C.+Do+not+use+the+rand()+function+for+generating+pseudorandom+numbers?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=362) [](https://www.securecoding.cert.org/confluence/display/seccode/MSC32-C.+Ensure+your+random+number+generator+is+properly+seeded?showChildren=false&showComments=false)
