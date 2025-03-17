Make sure compatible values have the same type. For example, when the return value of one function is used as an argument to another function, make sure they are the same type. Ensuring compatible values have the same type allows the return value to be passed as an argument to the related function without conversion, reducing the potential for conversion errors.
## Noncompliant Code Example
A source of potential errors may be traced to POSIX's tendency to overload return codes, using −1 to indicate an error condition but 0 for success and positive values as a result indicator (see [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators)). A good example is the `read()` system call. This leads to a natural mixing of unsigned and signed quantities, potentially leading to conversion errors.
OpenSSH performs most I/O calls through a "retry on interrupt" function, `atomicio()`. The following is a slightly simplified version of `atomicio.c`, v 1.12 2003/07/31. The function `f()` is either `read()` or `vwrite()`:
``` c
ssize_t atomicio(f, fd, _s, n)
  ssize_t (*f) (int, void *, size_t);
  int fd;
  void *_s;
  size_t n;
{
  char *s = _s;
  ssize_t res, pos = 0;
  while (n > pos) {
    res = (f) (fd, s + pos, n - pos);
    switch (res) {
      case -1:
         if (errno == EINTR || errno == EAGAIN)
         continue;
      case 0:
        return (res);
      default:
        pos += res;
     }
   }
   return (pos);
}
```
This function has a large number of flaws. Pertinent to this recommendation, however, are the following:
-   The `atomicio()` function returns an `ssize_t` (which must be a signed type). The `ssize_t` type is a clear indication of poor interface design because a size should never be negative.
-   Both `res` and `pos` are declared as `ssize_t`.
-   The expression `n - pos` results in the conversion of `pos` from a signed to an unsigned type because of the usual arithmetic conversions (see [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules)).
## Compliant Solution
The `atomicio()` function from `atomicio.c`, v 1.25 2007/06/25, was modified to always return an unsigned quantity and to instead report its error via `errno`:
``` c
size_t atomicio(ssize_t (*f) (int, void *, size_t),
                int fd, void *_s, size_t n) {
  char *s = _s;
  size_t pos = 0;
  ssize_t res;
  struct pollfd pfd;
  pfd.fd = fd;
  pfd.events = f == read ? POLLIN : POLLOUT;
  while (n > pos) {
    res = (f) (fd, s + pos, n - pos);
    switch (res) {
      case -1:
        if (errno == EINTR)
          continue;
        if (errno == EAGAIN) {
          (void)poll(&pfd, 1, -1);
          continue;
        }
        return 0;
      case 0:
        errno = EPIPE;
        return pos;
      default:
        pos += (size_t)res;
      }
    }
  return (pos);
}
```
Changes to this version of the `atomicio()` function include the following:
-   The `atomicio()` function now returns a value of type `size_t`.
-   `pos` is now declared as `size_t`.
-   The assignment `pos += (size_t)res` now requires an explicit cast to convert from the signed return value of `f()` to `size_t`.
-   The expression `n - pos` no longer requires an implicit conversion.
Reducing the need to use signed types makes it easier to enable the compiler's signed/unsigned comparison warnings and fix all of the issues it reports (see [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels)).
## Risk Assessment
The risk in using [in-band error indicators](BB.-Definitions_87152273.html#BB.Definitions-in-banderrorindicator) is difficult to quantify and is consequently given as low. However, if the use of in-band error indicators results in programmers' failing to check status codes or incorrectly checking them, the consequences can be more severe.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API09-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| PC-lint Plus | 1.4 | 737 | Partially supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR02-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|

## Bibliography

|  |  |
| ----|----|
| [Miller 2007] | "Security Measures in OpenSSH" |

------------------------------------------------------------------------
[](API07-C_%20Enforce%20type%20safety) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151961)
## Comments:

|  |
| ----|
| The compliant solution creates a difficult-to-use API due to issues described in;ERR30-C. A better compliant solution would explicitly set errno to 0 before returning pos.
                                        Posted by chris.newman at Jun 04, 2015 12:50
                                     |

