Subclause 7.21.7.10 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] defines `ungetc()` as follows:
> The `ungetc` function pushes the character specified by `c` (converted to an `unsigned char`) back onto the input stream pointed to by `stream`. Pushed-back characters will be returned by subsequent reads on that stream in the reverse order of their pushing. A successful intervening call (with the stream pointed to by `stream`) to a file positioning function (`fseek`, `fsetpos`, or `rewind`) discards any pushed-back characters for the stream. The external storage corresponding to the stream is unchanged.
>
> One character of pushback is guaranteed.

Consequently, multiple calls to `ungetc()` on the same stream must be separated by a call to a read function or a file-positioning function (which will discard any data pushed by `ungetc()`).
Likewise, for `ungetwc()`, C guarantees only one wide character of pushback (subclause 7.29.3.10). Consequently, multiple calls to `ungetwc()` on the same stream must be separated by a call to a read function or a file-positioning function (which will discard any data pushed by `ungetwc()`).
## Noncompliant Code Example
In this noncompliant code example, more than one character is pushed back on the stream referenced by `fp`:
``` c
FILE *fp;
char *file_name;
/* Initialize file_name */
fp = fopen(file_name, "rb");
if (fp == NULL) {
  /* Handle error */
}
/* Read data */
if (ungetc('\n', fp) == EOF) {
  /* Handle error */
}
if (ungetc('\r', fp) == EOF) {
  /* Handle error */
}
/* Continue */
```
## Compliant Solution
If more than one character needs to be pushed by `ungetc()`, then `fgetpos()` and `fsetpos()` should be used before and after reading the data instead of pushing it back with `ungetc()`. Note that this solution applies only if the input is seekable.
``` c
FILE *fp;
fpos_t pos;
char *file_name;
/* Initialize file_name */
fp = fopen(file_name, "rb");
if (fp == NULL) {
  /* Handle error */
}
/* Read data */
if (fgetpos(fp, &pos)) {
  /* Handle error */
}
/* Read the data that will be "pushed back" */
if (fsetpos(fp, &pos)) {
  /* Handle error */
}
/* Continue */
```
Remember to always call `fgetpos()` before `fsetpos()`. (See [FIO44-C. Only use values for fsetpos() that are returned from fgetpos()](FIO44-C_%20Only%20use%20values%20for%20fsetpos__%20that%20are%20returned%20from%20fgetpos__).)
## Risk Assessment
If used improperly, `ungetc()` and `ungetwc()` can cause data to be truncated or lost.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO13-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users can implement a custom check that triggers a warning when ungetc() is called twice on the same stream without an intervening call to a read function or a file-positioning function. |
| Compass/ROSE |  |  | Can detect simple violations of this recommendation. In particular, it warns when two calls to ungetc() on the same stream are not interspersed with a file-positioning or file-read function. It;cannot handle cases where ungetc() is called from inside a loop |
| LDRA tool suite | 9.7.1 | 83 D | Partially implemented |
| PC-lint Plus | 1.4 | 2470 | Fully supported |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO13-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.21.7.10, "The ungetc Function" |

------------------------------------------------------------------------
[](../c/FIO11-C_%20Take%20care%20when%20specifying%20the%20mode%20parameter%20of%20fopen__) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152146)
## Comments:

|  |
| ----|
| Does Compass/ROSE check ungetwc() calls as well?
                                        Posted by geoffclare at Jul 15, 2008 05:25
                                     |
| Not yet 
                                        Posted by svoboda at Jul 15, 2008 08:58
                                     |

