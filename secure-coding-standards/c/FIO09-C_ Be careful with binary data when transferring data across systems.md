Portability is a concern when using the `fread()` and `fwrite()` functions across multiple, heterogeneous systems. In particular, it is never guaranteed that reading or writing of scalar data types such as integers, let alone aggregate types such as arrays or structures, will preserve the representation or value of the data. Implementations may differ in structure padding, floating-point model, number of bits per byte, endianness, and other attributes that cause binary data formats to be incompatible.
## Noncompliant Code Example
This noncompliant code example reads data from a file stream into a data structure:
``` c
struct myData {
  char c;
  long l;
};
/* ... */
FILE *file;
struct myData data;
/* Initialize file */
if (fread(&data, sizeof(struct myData), 1, file) < sizeof(struct myData)) {
  /* Handle error */
}
```
However, the code makes assumptions about the layout of `myData`, which may be represented differently on a different platform.
## Compliant Solution
The best solution is to use either a text representation or a special library that ensures data integrity:
``` c
struct myData {
  char c;
  long l;
};
/* ... */
FILE *file;
struct myData data;
char buf[25];
char *end_ptr;
/* Initialize file */
if (fgets(buf, 1, file) == NULL) {
  /* Handle error */
}
data.c = buf[0];
if (fgets(buf, sizeof(buf), file) == NULL) {
  /* Handle Error */
}
data.l = strtol(buf, &end_ptr, 10);
if ((ERANGE == errno)
 || (end_ptr == buf)
 || ('\n' != *end_ptr && '\0' != *end_ptr)) {
    /* Handle Error */
}
```
## Risk Assessment
Reading binary data that has a different format than expected may result in unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO09-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Could flag possible violations of this rule by noting any pointer to struct that is passed to fread(), as the;noncompliant code example demonstrates |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO09-CPP. Be careful with binary data when transferring data across systems |

## Bibliography

|  |  |
| ----|----|
| [Summit 1995] | 20.5 on C-FAQ |

------------------------------------------------------------------------
[](../c/FIO08-C_%20Take%20care%20when%20calling%20remove__%20on%20an%20open%20file) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO10-C_%20Take%20care%20when%20using%20the%20rename__%20function)
## Comments:

|  |
| ----|
| If I understand this rec, it sounds like it is warning against using fread() at all, and is recommending storing numbers & other data in textual format, rather in the implementation-defined & nonportable binary format used by fread(). If so, this rule should probably be more explicit about preferring textual formats over fread() and nonportable binary formats in general.
It is easy for Rose to eschew fread().
                                        Posted by svoboda at Jun 22, 2008 09:17
                                     |
| fread() is only a problem if you save on platform on A and restore on platform B, as long as read/write is performed on the same machine, code that uses fread() can still be portable (it can run on both platform A and platform B, just not simultaneously)
                                        Posted by avolkovi at Jun 23, 2008 09:23
                                     |

