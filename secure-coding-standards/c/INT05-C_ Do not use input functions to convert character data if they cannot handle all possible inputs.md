Do not use functions that input characters and convert them to integers if the functions cannot handle all possible inputs. For example, formatted input functions such as `scanf()`, `fscanf()`, `vscanf()`, and `vfscanf()` can be used to read string data from `stdin` or (in the cases of `fscanf()` and `vfscanf()`) other input streams. These functions work fine for valid integer values but lack robust error handling for invalid values.
Alternatively, input character data as a null-terminated byte string and convert to an integer value using `strtol()` or a related function. (See [ERR34-C. Detect errors when converting a string to a number](ERR34-C_%20Detect%20errors%20when%20converting%20a%20string%20to%20a%20number).)
## Noncompliant Code Example
This noncompliant code example uses the `scanf()` function to read a string from `stdin` and convert it to a `long`. The `scanf()` and `fscanf()` functions have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if the value of the result of this operation cannot be represented as an integer.
``` c
long num_long;
if (scanf("%ld", &num_long) != 1) {
  /* Handle error */
}
```
In general, do not use `scanf()` to parse integers or floating-point numbers from input strings because the input could contain numbers not representable by the argument type.
## Compliant Solution (Linux)
This compliant example uses the Linux `scanf()` implementation's built-in error handling to validate input. On Linux platforms, `scanf()` sets `errno` to `ERANGE` if the result of integer conversion cannot be represented within the size specified by the format string \[[Linux 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Linux08)\]. Note that this solution is platform dependent, so it should be used only where portability is not a concern.
``` c
long num_long;
errno = 0;
if (scanf("%ld", &num_long) != 1) {
  /* Handle error */
}
else if (ERANGE == errno) {
  if (puts("number out of range\n") == EOF) {
      /* Handle error */
  }
}
```
## Compliant Solution
This compliant example uses `fgets()` to input a string and `strtol()` to convert the string to an integer. Error checking is provided to make sure the value is a valid integer in the range of `long`.
``` c
char buff[25];
char *end_ptr;
long num_long;
if (fgets(buff, sizeof(buff), stdin) == NULL) {
  if (puts("EOF or read error\n") == EOF) {
    /* Handle error */
  }
} else {
  errno = 0;
  num_long = strtol(buff, &end_ptr, 10);
  if (ERANGE == errno) {
    if (puts("number out of range\n") == EOF) {
      /* Handle error */
    }
  }
  else if (end_ptr == buff) {
    if (puts("not valid numeric input\n") == EOF) {
      /* Handle error */
    }
  }
  else if ('\n' != *end_ptr && '\0' != *end_ptr) {
    if (puts("extra characters on input line\n") == EOF) {
      /* Handle error */
    }
  }
}
```
Note that this solution treats any trailing characters, including whitespace characters, as an error condition.
## Risk Assessment
Although it is relatively rare for a violation of this recommendation to result in a security [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), it can easily result in lost or misinterpreted data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT05-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT05 |  |
| CodeSonar | 8.3p0 | MISC.NEGCHAR | Negative Character Value |
| Compass/ROSE |  |  | Can detect violations of this recommendation. In particular, it notes uses of the scanf() family of functions where on the type specifier is a floating-point or integer type |
| Helix QAC | 2024.4 | C5005 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-INT05-a | Avoid using unsafe string functions that do not check bounds |
| PC-lint Plus | 1.4 | 586 | Fully supported |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT05-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT05-CPP. Do not use input functions to convert character data if they cannot handle all possible inputs |
| MITRE CWE | CWE-192, Integer coercion errorCWE-197, Numeric truncation error |

## Bibliography

|  |  |
| ----|----|
| [Klein 2002] |  |
| [Linux 2008] | scanf(3) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152245) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152386)
## Comments:

|  |
| ----|
| This rule needs to make clearer exactly what is verbotem in the scanf() family. My interpretation is that one must not pass as input parameter a pointer to any integer smaller than intmax_t (signed or unsigned), because a smaller integer might not be able to hold the object read in, resulting in undefined behavior.
On second thought, both intmax_t and uintmax_t are also insufficient, because uintmax_t can't hold -1 and intmax_t can't hold UINT_MAX. So maybe this vul is unavoidable and we should forbid using scanf() on all ints, like the CCE illustrates.
So can scanf() be done securely on ints?
                                        Posted by svoboda at Jul 17, 2008 09:49
                                     |
| rcs sez:
> i think we are telling people not to use scanf() because you can't check for invalid values, and its > a rule.  at least the remediation cost is appropriately given as "high".

                                        Posted by svoboda at Jul 17, 2008 10:10
                                     |
| Removing my comment as it does not apply.
                                        Posted by aballman at Sep 20, 2013 13:06
                                     |

