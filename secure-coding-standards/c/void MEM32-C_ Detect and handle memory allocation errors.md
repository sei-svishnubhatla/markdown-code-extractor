> [!warning]  
>
> This guideline has been deprecated by
>
> -   [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors)

The return values for memory allocation functions indicate the failure or success of the allocation. The standard C `calloc()`, `aligned_alloc()`, `malloc()`, and `realloc()` return null pointers if the requested memory allocation fails. As discussed in [MEM11-C. Do not assume infinite heap space](MEM11-C_%20Do%20not%20assume%20infinite%20heap%20space), memory allocation may fail because of heap exhaustion as a result of unconstrained use of the heap by the calling process or other processes or because of the exhaustion of other system resources. Failure to detect and properly handle memory allocation errors can lead to unpredictable and unintended program behavior. As a result, it is necessary to check the final status of memory management functions and handle errors appropriately and in accordance with [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy).
The following table shows the possible outcomes of the memory allocation functions defined by the C standard library.

| Function | Successful Return | Error Return | errno #1 |
| ----|----|----|----|
| malloc() | pointer to allocated space | NULL | ENOMEM |
| aligned_alloc() | pointer to allocated space | NULL | ENOMEM |
| calloc() | pointer to allocated space | NULL | ENOMEM |
| realloc() | pointer to the new object | NULL | ENOMEM |

In addition to the C standard library functions above, POSIX defines the following functions designed specifically to dynamically allocate memory.

| Function | Successful Return | Error Return | errno |
| ----|----|----|----|
| fmemopen() | pointer to a FILE object | NULL | ENOMEM |
| open_memstream() | pointer to a FILE object | NULL | ENOMEM |
| posix_memalign() | 0 | non-zero #2 | unchanged #2 |

1.  Setting `errno` is a POSIX \[[ISO/IEC 9945:2008](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9945-2008)\] extension to the C Standard.
2.  On error, `posix_memalign()` returns a value that corresponds to one of the constants defined in the `<errno.h>` header. The function does not set `errno`. The `posix_memalign()` function is optional and is not required to be provided by conforming implementations.
## Noncompliant Code Example (`malloc()`)
In this noncompliant code example, `input_string` is copied into dynamically allocated memory referenced by `str`. However, the result of `malloc()` is not checked before `str` is referenced. Consequently, if `malloc()` fails, the program has undefined behavior. (See [undefined behavior 109](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_109) in Annex J of the C Standard.) In practice, this typically leads to an abnormal termination of the process, providing an opportunity for a [denial-of-service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) attack. In some cases, it may be the source of other vulnerabilities as well. (See the [Related Vulnerabilities](#voidMEM32C.Detectandhandlememoryallocationerrors-RelatedVulnerabilities) section.)
``` c
void f(char *input_string) {
  size_t size = strlen(input_string) + 1;
  char *str = (char *)malloc(size);
  strcpy(str, input_string);
  /* ... */
}
```
## Compliant Solution (`malloc()`)
The `malloc()` function, as well as the other memory allocation functions, returns either a null pointer or a pointer to the allocated space. Always test the returned pointer to ensure it is not `NULL` before referencing the pointer. Handle the error condition appropriately when the returned pointer is `NULL`. When recovery from the allocation failure is not possible, propagate the failure to the caller.
``` c
int f(char *input_string) {
  size_t size = strlen(input_string) + 1;
  char *str = (char *)malloc(size);
  if (str == NULL) {
    /* Handle allocation failure and return error status */
    return -1;
  }
  strcpy(str, input_string);
  /* ... */
  free(str);
  return 0;
}
```
## Risk Assessment
Failing to detect allocation failures can lead to abnormal program termination and denial-of-service attacks.
If the vulnerable program references memory offset from the return value, an attacker can exploit the program to read or write arbitrary memory. This method has been used to execute arbitrary code \[[VU#159523](http://www.kb.cert.org/vuls/id/159523)\].

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM32-C | high | likely | medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this rule. In particular, it ensures that variables are compared to NULL before being used, as in EXP34-C. Do not dereference null pointers. |
| Coverity | 2017.07 | CHECKED_RETURN | Finds inconsistencies in how function call return values are handled. Coverity Prevent cannot discover all violations of this recommendation, so further verification is necessary. |
| Fortify SCA | 5.0 | ; | ; |

### Related Vulnerabilities
The vulnerability in Adobe Flash \[[VU#159523](AA.-Bibliography_87152170.html#AA.Bibliography-VU#159523)\] arises because Flash neglects to check the return value from `calloc()`. Even when `calloc()` returns `NULL`, Flash writes to an offset from the return value. Dereferencing `NULL` usually results in a program crash, but dereferencing an offset from `NULL` allows an exploit to succeed without crashing the program.
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM32-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | MEM52-CPP. Detect and handle memory allocation errors |
| MITRE CWE | CWE-252, Unchecked return valueCWE-476, NULL pointer dereference
CWE-754, Improper check for unusual or exceptional conditions |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2005] | Chapter 4, "Dynamic Memory Management" |
| [VU#159523] | ; |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MEM31-C.+Free+dynamically+allocated+memory+exactly+once?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=437) [](https://www.securecoding.cert.org/confluence/display/seccode/MEM33-C.++Allocate+and+copy+structures+containing+flexible+array+members+dynamically?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Since this rule has been deprecated, I think we should find a new home for the realloc example since the API is easy to misuse.
                                        Posted by aballman at Jun 13, 2013 12:42
                                     |
| this example was moved to ERR33-C. Detect and handle standard library errors.i deleted it from here, so we don't waste more time on it.maybe this should be the way we deal with salvaging examples from deprecated rules?
                                        Posted by rcs at Jun 17, 2013 09:57
                                     |

