The C Standard, 7.23.5.3, paragraph 7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], places the following restrictions on update streams:
> When a file is opened with update mode . . ., both input and output may be performed on the associated stream. However, output shall not be directly followed by input without an intervening call to the `fflush` function or to a file positioning function (`fseek`, `fsetpos`, or `rewind`), and input shall not be directly followed by output without an intervening call to a file positioning function, unless the input operation encounters end-of-file. Opening (or creating) a text file with update mode may instead open (or create) a binary stream in some implementations.

The following scenarios can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 156](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_156).)
-    Receiving input from a stream directly following an output to that stream without an intervening call to `fflush()`, `fseek()`, `fsetpos()`, or `rewind()` if the file is not at end-of-file
-    Outputting to a stream after receiving input from that stream without a call to `fseek()`, `fsetpos()`, or `rewind()` if the file is not at end-of-file
Consequently, a call to `fseek()`, `fflush()`, or `fsetpos()` is necessary between input and output to the same stream. See [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't) for more information on why `fseek()` is preferred over `rewind()`.
## Noncompliant Code Example
This noncompliant code example appends data to a file and then reads from the same file:
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
extern void initialize_data(char *data, size_t size);
void func(const char *file_name) {
  char data[BUFFERSIZE];
  char append_data[BUFFERSIZE];
  FILE *file;
  file = fopen(file_name, "a+");
  if (file == NULL) {
    /* Handle error */
  }
  initialize_data(append_data, BUFFERSIZE);
  if (fwrite(append_data, 1, BUFFERSIZE, file) != BUFFERSIZE) {
    /* Handle error */
  }
  if (fread(data, 1, BUFFERSIZE, file) < BUFFERSIZE) {
    /* Handle there not being data */
  }
  if (fclose(file) == EOF) {
    /* Handle error */
  }
}
```
Because there is no intervening flush or positioning call between the calls to `fread()` and `fwrite()`, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Compliant Solution
In this compliant solution, `fseek()` is called between the output and input, eliminating the undefined behavior:
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
extern void initialize_data(char *data, size_t size);
void func(const char *file_name) {
  char data[BUFFERSIZE];
  char append_data[BUFFERSIZE];
  FILE *file;
  file = fopen(file_name, "a+");
  if (file == NULL) {
    /* Handle error */
  }
  initialize_data(append_data, BUFFERSIZE);
  if (fwrite(append_data, BUFFERSIZE, 1, file) != BUFFERSIZE) {
    /* Handle error */
  }
  if (fseek(file, 0L, SEEK_SET) != 0) {
    /* Handle error */
  }
  if (fread(data, BUFFERSIZE, 1, file) != 0) {
    /* Handle there not being data */
  }
  if (fclose(file) == EOF) {
    /* Handle error */
  }
}
```
## Risk Assessment
Alternately inputting and outputting from a stream without an intervening flush or positioning call is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO39-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO39 |  |
| CodeSonar | 8.3p0 | IO.IOWOPIO.OIWOP | Input After Output Without PositioningOutput After Input Without Positioning |
| Compass/ROSE |  |  | Can detect simple violations of this rule |
| Cppcheck | ;2.15 | IOWithoutPositioning |  |
| Cppcheck Premium | 24.11.0 | IOWithoutPositioning |  |
| Helix QAC | 2024.4 | DF4711, DF4712, DF4713 |  |
| Klocwork | 2024.4 | CERT.FIO.NO_FLUSH |  |
| LDRA tool suite | 9.7.1 | 84 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO39-a | Do not alternately input and output from a stream without an intervening flush or positioning call |
| PC-lint Plus | 1.4 | 2478, 2479 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO39-C | Checks for alternating input and output from a stream without flush or positioning call (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO39-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | FIO50-CPP. Do not alternately input and output from a file stream without an intervening positioning call | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Interleaving stream inputs and outputs without a flush or positioning call [ioileave] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-664 | 2017-07-10: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-664 and FIO39-C
CWE-664 = Union( FIO39-C, list) where list =
-   Improper use of an object (besides alternating reading/writing a file stream without an intervening flush
This CWE is vague on what constitutes “improper control of a resource”. It could include any violation of an object’s method constraints (whether they are documented or not). Or it could be narrowly interpreted to mean object creation and object destruction (which are covered by other CWEs).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.23.5.3, "The fopen Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152442) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](../c/FIO40-C_%20Reset%20strings%20on%20fgets__%20%20or%20fgetws__%20failure)
## Comments:

|  |
| ----|
| Some random memory is telling me that you also need to do an fseek() between a write and subsequent read...at least if you want to read the data you formerly wrote. I believe that the read in the 2nd CCE will fail b/c the file position is at EOF, right?
                                        Posted by svoboda at Jun 20, 2008 16:14
                                     |
| Correct, I just tried running the code
                                        Posted by avolkovi at Jun 20, 2008 16:18
                                     |
| wait, you took out the fflush() call...isn't that necessary to ensure the data gets written (and subsequently read by fread()?
                                        Posted by svoboda at Jun 20, 2008 17:17
                                     |
| The file positioning call is enough.However, output shall not be directly followed by input without an intervening call to the fflush function or to a file positioning function...
                                        Posted by aballman at Sep 27, 2013 11:12
                                     |

