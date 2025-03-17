Use `ferror()` rather than `errno` to check whether an error has occurred on a file stream (for example, after a long chain of `stdio` calls). The `ferror()` function tests the error indicator for a specified stream and returns nonzero if and only if the error indicator is set for the stream.
## Noncompliant Code Example
Many [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) of the `stdio` package adjust their behavior slightly if `stdout` is a terminal. To make the determination, these implementations perform some operation that fails (with `ENOTTY`) if `stdout` is not a terminal. Although the output operation goes on to complete successfully, `errno` still contains `ENOTTY`. This behavior can be mildly confusing, but it is not strictly incorrect because it is meaningful for a program to inspect the contents of `errno` only after an error has been reported. More precisely, `errno` is meaningful only after a library function that sets `errno` on error has returned an error code.
``` c
errno = 0;
printf("This\n");
printf("is\n");
printf("a\n");
printf("test.\n");
if (errno != 0) {
  fprintf(stderr, "printf failed: %s\n", strerror(errno));
}
```
## Compliant Solution
This compliant solution uses `ferror()` to detect an error. In addition, if an early call to `printf()` fails, later calls may modify `errno`, whether they fail or not, so the program cannot rely on being able to detect the root cause of the original failure if it waits until after a sequence of library calls to check.
``` c
printf("This\n");
printf("is\n");
printf("a\n");
printf("test.\n");
if (ferror(stdout)) {
  fprintf(stderr, "printf failed\n");
}
```
## Risk Assessment
Checking `errno` after multiple calls to library functions can lead to spurious error reporting, possibly resulting in incorrect program operation.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR01-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ECLAIR | 1.2 | CC2.ERR01 | Fully implemented |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR01-a | The error indicator 'errno' shall not be used |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ERR01-CPP. Use ferror() rather than errno to check for FILE stream errors |

## Bibliography

|  |  |
| ----|----|
| [Horton 1990] | Section 14, p. 254 |
| [Koenig 1989] | Section 5.4, p. 73 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152349) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152400)
## Comments:

|  |
| ----|
| While one could enforce this rule on the NCCE, I suspect any code between errno = 0 and if (errno != 0) will have a mix of statements that might tickle errno and statements that will trigger ferror(), so it would be impossible to infer that the programmer checked errno when they should have checked ferror(). Thus this rule is 'unenforceable'
                                        Posted by svoboda at Jul 14, 2008 14:43
                                     |
| While this rule may be unenforceable in general, I suspect most code that defies enforceability will also violate ERR30-C. Take care when reading errno. If we limit ourselves to code that passes ERR30-C, I suspect this rule is actually quite enforceable. (although a checker for ERR30-C would probably catch all violations of this rule anyway). Changing to 'rose-possible'.
                                        Posted by svoboda at Apr 22, 2009 07:32
                                     |

