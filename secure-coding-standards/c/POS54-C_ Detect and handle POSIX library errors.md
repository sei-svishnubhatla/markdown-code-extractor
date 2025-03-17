All standard library functions, including I/O functions and memory allocation functions, return either a valid value or a value of the correct return type that indicates an error (for example, −1 or a null pointer). Assuming that all calls to such functions will succeed and failing to check the return value for an indication of an error is a dangerous practice that may lead to [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) or [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when an error occurs. It is essential that programs detect and appropriately handle all errors in accordance with an error-handling policy, as discussed in [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy).  In addition to the C standard library functions mentioned in [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors), the following functions defined in POSIX require error checking (list is not all-inclusive).
The successful completion or failure of each of the standard library functions listed in the following table shall be determined either by comparing the function’s return value with the value listed in the column labeled “Error Return” or by calling one of the library functions mentioned in the footnotes to the same column.

| Function | Successful Return | Error Return | errno |
| ----|----|----|----|
| fmemopen() | Pointer to a FILE object | NULL | ENOMEM |
| open_memstream() | Pointer to a FILE object | NULL | ENOMEM |
| posix_memalign() | 0 | Nonzero | Unchanged |

Setting `errno` is a POSIX \[[ISO/IEC 9945:2008](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9945-2008)\] extension to the C Standard.  On error, `posix_memalign()` returns a value that corresponds to one of the constants defined in the `<errno.h>` header. The function does not set `errno`. The `posix_memalign()` function is optional and is not required to be provided by POSIX-conforming implementations.
## Noncompliant Code Example (POSIX)
In this noncompliant code example, `fmemopen()` and` open_memstream()` are assumed to succeed. However, if the calls fail, the two file pointers `in` and `out` will be null and the program will have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[]) {
  FILE *out;
  FILE *in;
  size_t size;
  char *ptr;
  if (argc != 2) {
    /* Handle error */
  }
  in = fmemopen(argv[1], strlen(argv[1]), "r");
  /* Use in */
  out = open_memstream(&ptr, &size);
  /* Use out */
  return 0; 
}
```
## Compliant Solution (POSIX)
A compliant solution avoids assuming that `fmemopen()` and open_memstream() succeed regardless of its arguments and tests the return value of the function before using the file pointers `in` and `out`:
``` c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[]) {
  FILE *out;
  FILE *in;
  size_t size;
  char *ptr;
  if (argc != 2) {
    /* Handle error */
  }
  in = fmemopen(argv[1], strlen(argv[1]), "r");
  if (in == NULL){
    /* Handle error */
  }
  /* Use in */
  out = open_memstream(&ptr, &size);
  if (out == NULL){
    /* Handle error */
  }
  /* Use out */
  return 0;
}
```
## Exceptions
****POS54-C-EX1:**** *This exception has been removed.*
**POS54-C-EX2:** The exception from [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) (that is ERR33-C-EX1) applies to this rule. See that exception for more information.
## Risk Assessment
Failing to detect error conditions can lead to unpredictable results, including [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) and [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) or, in some situations, could even allow an attacker to run arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS54-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | error-information-unusederror-information-unused-computed | Supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS54 |  |
| CodeSonar | 8.3p0 | LANG.FUNCS.IRVLANG.ERRCODE.NOTEST
LANG.ERRCODE.NZ
 | Ignored return valueMissing Test of Error Code
Non-zero Error Code |
| Compass/ROSE |  |  | Can detect violations of this recommendation when checking for violations of EXP12-C. Do not ignore values returned by functions and EXP34-C. Do not dereference null pointers |
| Coverity | 2017.07 | CHECKED_RETURN | Finds inconsistencies in how function call return values are handled. Coverity Prevent cannot discover all violations of this recommendation, so further verification is necessary |
| Helix QAC | 2024.4 | C3200 |  |
| Klocwork | 2024.4 | SV.RVT.RETVAL_NOTTESTED |  |
| LDRA tool suite | 9.7.1 | 80 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-POS54-a | The value returned by a POSIX library function that may return an error should be used |
| PC-lint Plus | 1.4 | 413, 534, 613 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS54-C | Checks for situations where return value of a sensitive function is not checked (rule fully covered) |
| RuleChecker | 24.04 | error-information-unused | Supported |

### Related Vulnerabilities
The vulnerability in Adobe Flash \[[VU#159523](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-VU159523)\] arises because Flash neglects to check the return value from `calloc()`. Even when `calloc()` returns `NULL`, Flash writes to an offset from the return value. Dereferencing `NULL` usually results in a program crash, but dereferencing an offset from `NULL` allows an [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) to succeed without crashing the program.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | API04-C. Provide a consistent and usable error-checking mechanismERR00-C. Adopt and implement a consistent and comprehensive error-handling policyERR02-C. Avoid in-band error indicatorsERR05-C. Application-independent code should provide error detection without dictating error handlingEXP12-C. Do not ignore values returned by functionsEXP34-C. Do not dereference null pointersFIO10-C. Take care when using the rename() functionFIO13-C. Never push back anything other than one read characterFIO33-C. Detect and handle input output errors resulting in undefined behaviorFIO34-C. Distinguish between characters read from a file and EOF or WEOFFLP03-C. Detect and handle floating-point errorsFLP32-C. Prevent or detect domain and range errors in math functionsMEM04-C. Do not perform zero-length allocationsMEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ERR10-CPP. Check for error conditions FIO04-CPP. Detect and handle input and output errors | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Failing to detect and handle standard library errors [liberr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-252, Unchecked return value | 2017-07-06: CERT: Partial overlap |
| CWE 2.11 | CWE-253, Incorrect check of function return value | 2017-07-06: CERT: Partial overlap |
| CWE 2.11 | CWE-391, Unchecked error condition | 2017-07-06: CERT: Rule subset of CWE |

## Bibliography

|  |  |
| ----|----|
| [DHS 2006] | Handle All Errors Safely |
| [Henricson 1997] | Recommendation 12.1, "Check for All Errors Reported from Functions" |
| [ISO/IEC 9899:2024] | Subclause 7.23.7.10, "The ungetc Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151984) [](../c/Rule%2050_%20POSIX%20_POS_) [](../c/Rule%2051_%20Microsoft%20Windows%20_WIN_)
## Comments:

|  |
| ----|
| exception EX2 should be EX1?(just confirming that it's simply a kind of typo...)
                                        Posted by yozo at Feb 18, 2023 01:47
                                     |
| Confirmed. We just removed EX1 yesterday, but left EX2 and did not want to renumber it.
                                        Posted by svoboda at Feb 18, 2023 05:26
                                     |
| How do you think about to represent information from the description of a function like gettimeofday() in the section “Exceptions”?Would you become interested to filter API documentations for similar function properties?
                                        Posted by markus.elfring at May 01, 2023 10:03
                                     |
| Markus:I'm not sure what you are asking.
As you know, ERR33-C enumerates ISO C library functions that return exceptional values, and also enumerates the functions whose values may be ignored. This rule is analogous to ERR33-C but addresses POSIX library functions. However, this rule does not enumerate such functions either in its introduction or the exceptions. We felt that this task was too big at the time.  Are you volunteering to do this task?
                                        Posted by svoboda at May 01, 2023 10:30
                                     |
| This rule is analogous to ERR33-C but addresses POSIX library functions.There are further case distinctions to consider.Are you volunteering to do this task?No, not directly.I am still trying to adjust the corresponding development awareness (because I came along also special or “exceptional” cases like pause()).Can a systematic analysis of involved programming interfaces provide desired data automatically?
                                        Posted by markus.elfring at May 01, 2023 12:38
                                     |
| I'm not sure what you are asking. How many functions can you know which are documented in the way that they should provide only a fixed return value?
                                        Posted by markus.elfring at May 03, 2023 04:00
                                     |
| You mean like gettimeofday()? ;I haven't been over the list of POSIX functions. Again, we decided there are too many functions to enumerate them all. It is, however, a straightforward task to do so.
                                        Posted by svoboda at May 03, 2023 08:53
                                     |
| I haven't been over the list of POSIX functions. Again, we decided there are too many functions to enumerate them all.Do you know if anybody tried to transform specifications for the discussed programming interfaces into higher level data structures besides available manual pages?Can the querying of function properties become easier?
                                        Posted by markus.elfring at May 04, 2023 01:18
                                     |
| I suspect that your question is better posed to the Austin Group than us. The Austin Group maintains the POSIX standard. FWIW I was able to download an HTML version of the POSIX standard, and I'm sure you can use grep, or other search tools to simplify querying of POSIX functions.
                                        Posted by svoboda at May 08, 2023 09:25
                                     |
| FWIW I was able to download an HTML version of the POSIX standard, … Are other contributors in a better position to raise involved abstraction levels and to improve corresponding development tools?
                                        Posted by markus.elfring at May 08, 2023 09:42
                                     |

