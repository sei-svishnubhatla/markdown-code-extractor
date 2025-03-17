Input and output are mapped into logical data streams whose properties are more uniform than their various inputs and outputs. Two forms of mapping are supported, one for text streams and one for binary streams. They differ in the actual representation of data as well as in the functionality of some C functions.
# Text Streams
## *Representation*
Characters may have to be altered to conform to differing conventions for representing text in the [host environment](BB.-Definitions_87152273.html#BB.Definitions-hostedenvironment). As a consequence, data read to or written from a text stream will not necessarily compare equal to the stream's byte content.
The following code opens the file `myfile` as a text stream:
``` java
char *file_name;
/* Initialize file_name */
FILE *file = fopen(file_name, "w");
/* Check for errors */
fputs("\n", file);
```
Environments may model line breaks differently. For example, on Windows, this code writes 2 bytes (a carriage return and then a newline) to the file, whereas on POSIX systems, this code writes only 1 byte (a newline).
## *`fseek()`*
For a text stream, the offset for `fseek()` must be either 0 or a value returned by an earlier successful call to the `ftell()` function (on a stream associated with the same file) with a mode of `SEEK_SET`.
## *`ungetc()`*
The `ungetc()` function causes the file position indicator to be *unspecified* until all pushed-back characters are read. As a result, care must be taken that file-position-related functions are not used while this is true.
# Binary Streams
## *Representation*
A binary stream is an ordered sequence of characters that can transparently record internal data. As a consequence, data read from or written to a binary stream will necessarily compare equal to the stream's byte content.
The following code opens the file `myfile` as a binary stream:
``` java
char *file_name;
/* Initialize file_name */
FILE *file = fopen(file_name, "wb");
/* Check for errors */
fputs("\n", file);
```
Regardless of environment, this code writes exactly 1 byte (a newline).
## *`fseek()`*
According to the C Standard, a binary stream may be terminated with an unspecified number of null characters and need not meaningfully support `fseek()` calls with a mode of `SEEK_END`. Consequently, do not call `fseek()` on a binary stream with a mode of `SEEK_END`.
## *`ungetc()`*
The `ungetc()` function causes the file-position indicator to be decremented by 1 for each successful call, with the value being [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) if it is 0 before any call. As a result, `ungetc()` must never be called on a binary stream where the file position indicator is 0.
## Risk Assessment
Failure to understand file stream mappings can result in unexpectedly formatted files.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO14-C | Low | Probable | High | P2 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO14-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO14-CPP. Understand the difference between text mode and binary mode with file streams |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152185) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152134)
