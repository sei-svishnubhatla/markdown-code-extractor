Variadic functions accept a variable number of arguments but are problematic. Variadic functions define an implicit contract between the function writer and the function user that allows the function to determine the number of arguments passed in any particular invocation. Failure to enforce this contract may result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). See [undefined behavior 141](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_141) of Appendix J of the C Standard.
## Argument Processing
In the following code example, the variadic function `average()` calculates the average value of the positive integer arguments passed to the function \[[Seacord 2013](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\]. The function processes arguments until it encounters an argument with the value of `va_eol` (`-1`).
``` java
enum { va_eol = -1 };
unsigned int average(int first, ...) {
  unsigned int count = 0;
  unsigned int sum = 0;
  int i = first;
  va_list args;
  va_start(args, first);
  while (i != va_eol) {
    sum += i;
    count++;
    i = va_arg(args, int);
  }
  va_end(args);
  return(count ? (sum / count) : 0);
}
```
Note that `va_start()` must be called to initialize the argument list and that `va_end()` must be called when finished with a variable argument list.
## Noncompliant Code Example
In this noncompliant code example, the `average()` function is called as follows:
``` c
int avg = average(1, 4, 6, 4, 1);
```
The omission of the `va_eol` terminating value means that the function will continue to process values from the stack until it encounters a `va_eol` by coincidence or an error occurs.
## Compliant Solution
This compliant solution enforces the contract by adding `va_eol` as the final argument:
``` c
int avg = average(1, 4, 6, 4, 1, va_eol);
```
## Noncompliant Code Example
Another common mistake is to use more conversion specifiers than supplied arguments, as shown in this noncompliant code example:
``` c
const char *error_msg = "Resource not available to user.";
/* ... */
printf("Error (%s): %s", error_msg);
```
This code results in nonexistent arguments being processed by the function, potentially leaking information about the process.
## Compliant Solution
This compliant solution matches the number of format specifiers with the number of variable arguments:
``` c
const char *error_msg = "Resource not available to user.";
/* ... */
printf("Error: %s", error_msg);
```
### Argument List Caveats
C functions that accept the variadic primitive `va_list` as an argument pose an additional risk. Calls to `vfprintf()`, `vfscanf()`, `vprintf()`, `vscanf()`, `vsnprintf()`, `vsprintf()`, and `vsscanf()` use the `va_arg()` macro, invalidating the parameterized `va_list`. Consequently, once a `va_list` is passed as an argument to any of these functions, it cannot be used again without a call to `va_end()` followed by a call to `va_start()`.
## Risk Assessment
Incorrectly using a variadic function can result in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) or unintended information disclosure.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL10-C | High | Probable | High | P6 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL10-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| Helix QAC | 2024.4 | C0185, C0184 |  |
| Klocwork | 2024.4 | SV.FMT_STR.PRINT_PARAMS_WRONGNUM.FEWSV.FMT_STR.PRINT_PARAMS_WRONGNUM.MANY
SV.FMT_STR.SCAN_PARAMS_WRONGNUM.FEW
SV.FMT_STR.SCAN_PARAMS_WRONGNUM.MANY |  |
| LDRA tool suite | 9.7.1 | 41 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL10-a | The number of format specifiers in the format string and the number of corresponding arguments in the invocation of a string formatting function should be equal |
| PC-lint Plus | 1.4 | 558, 719 | Assistance provided: reports issues involving format strings |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL10-C | Checks for format string specifiers and arguments mismatch (rec. partially covered) |

## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Subprogram Signature Mismatch [OTR] |
| MISRA C:2012 | Rule 17.1 (required) |
| MITRE CWE | CWE-628, Function call with incorrectly specified arguments |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 6, "Formatted Output" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152089) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152357)
## Comments:

|  |
| ----|
| Some compilers, such as GCC, offer the ability to annotate variadic functions with one of a few common contracts, including execl-style (arg, arg, arg, NULL) and printf-style (fmt, arg1_from_fmt, arg2_from_fmt).  Please consider noting this in the standard and suggesting the use of it if available.
                                        Posted by josh@freedesktop.org at Mar 16, 2008 06:26
                                     |
| "marker" should be "args" since it has nothing to do with the marker as such.
"sum" and the return type should probably be unsigned and the test for a marker should be i >= 0.
Also, #define EOL (-1) // end-of-list marker
                                        Posted by dagwyn at Apr 15, 2008 12:27
                                     |
| Tightened up average() function as suggested. As defined, average() would work on any list of positive or negative ints that didn't include -1. But for example purposes, it's easier to restrict the function to positive ints than to handle negative ints (and therefore redesign the -1 sentinel.)
                                        Posted by svoboda at Apr 15, 2008 14:03
                                     |
| We could enforce the contracts of the printf() and scanf() function families because their contracts are well-known (and some compilers already enforce them). I believe they are enforced by other rules.
Enforcing vararg contracts is generally unenforceable unless the contracts are rigorously defined.
                                        Posted by svoboda at Jul 16, 2008 09:40
                                     |
| In addition to this guideline, I think it would be worthwhile to add at the least the following rules:
    Use va_copy to initialize copies of va_list objects (undefined behavior #128 )
    Pair each invocation of va_start and va_copy with a corresponding va_end in the same function (undefined behavior #131 )
If there are no objections I'll go ahead and add them.
                                        Posted by martinsebor at Jan 12, 2010 15:34
                                     |

