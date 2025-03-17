Opening a file that is already open has [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior), according to the C Standard, 7.21.3, paragraph 8 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
> Functions that open additional (nontemporary) ﬁles require a file name, which is a string. The rules for composing valid ﬁle names are implementation-deﬁned. Whether the same file can be simultaneously open multiple times is also implementation-deﬁned.

Some implementations do not allow multiple copies of the same file to be open at the same time. Consequently, portable code cannot depend on what will happen if this rule is violated. Even on implementations that do not outright fail to open an already-opened file, a [TOCTOU](BB.-Definitions_87152273.html#BB.Definitions-TOCTOU) (time-of-check, time-of-use) race condition exists in which the second open could operate on a different file from the first due to the file being moved or deleted (see [FIO45-C. Avoid TOCTOU race conditions while accessing files](FIO45-C_%20Avoid%20TOCTOU%20race%20conditions%20while%20accessing%20files) for more details on TOCTOU race conditions).
## Noncompliant Code Example
This noncompliant code example logs the program's state at runtime:
``` c
#include <stdio.h>
void do_stuff(void) {
  FILE *logfile = fopen("log", "a");
  if (logfile == NULL) {
    /* Handle error */
  }
  /* Write logs pertaining to do_stuff() */
  fprintf(logfile, "do_stuff\n");
}
int main(void) {
  FILE *logfile = fopen("log", "a");
  if (logfile == NULL) {
    /* Handle error */
  }
  /* Write logs pertaining to main() */
  fprintf(logfile, "main\n");
  do_stuff();
  if (fclose(logfile) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
Because the file `log` is opened twice (once in `main()` and again in `do_stuff()`), this program has [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior).
## Compliant Solution
In this compliant solution, a reference to the file pointer is passed as an argument to functions that need to perform operations on that file. This reference eliminates the need to open the same file multiple times.
``` c
#include <stdio.h>
void do_stuff(FILE *logfile) {
  /* Write logs pertaining to do_stuff() */
  fprintf(logfile, "do_stuff\n");
}
int main(void) {
  FILE *logfile = fopen("log", "a");
  if (logfile == NULL) {
    /* Handle error */
  }
  /* Write logs pertaining to main() */
  fprintf(logfile, "main\n");
  do_stuff(logfile);
  if (fclose(logfile) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
## Risk Assessment
Simultaneously opening a file multiple times can result in unexpected errors and nonportable behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO24-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | IO.RACE(customization)IO.BRAW | File system race conditionUsers can implement a custom check that triggers a warning if a file-opening function is called on a file that is already openFile Open for Both Read and Write |
| LDRA tool suite | 9.7.1 | 75 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO24-a | Avoid race conditions while accessing files |
| Polyspace Bug Finder | R2024a | CERT C: Rec. FIO24-C | Checks for situations where previously opened resources are reopened (rec. fully covered) |

## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | FIO45-C. Avoid TOCTOU race conditions while accessing files |
| SEI CERT C++ Coding Standard | VOID FIO21-CPP. Do not simultaneously open the same file multiple times |
| MITRE CWE | CWE-362, Concurrent Execution Using Shared Resource with Improper Synchronization ("Race Condition")CWE-675, Duplicate Operations on Resource |

##  Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011]; | Subclause 7.21.3, "Files" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151957) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/Rec_%2005_%20Floating%20Point%20_FLP_)
## Comments:

|  |
| ----|
| This isn't a problem on POSIX compliant systems (read Unix et al), so it must be a potential problem on Windows...Or was there somewhere else that you were thinking of?
Of course, on Unix, the "a" for append is critical for appending coherently (without one file pointer/descriptor trampling over data previously written by the other).; However, there are database-related systems (I'm thinking C-ISAM; you might thinjk of the DBM packages) where this is all properly controlled.
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 02:45
                                     |
| This rule is talking about the fact that the behavior is implementation-defined according to the C standard.; Therefore, portable code cannot depend on what will happen if this is attempted.
                                        Posted by dmk at Mar 21, 2008 20:45
                                     |
| This is one of the very few (only?) rules we have about implementation-defined behavior.
                                        Posted by rcs at Dec 02, 2013 15:40
                                     |
| This is FIO24-C but risk assement is written in FIO31-C. Need to correct.
                                        Posted by lima36 at Feb 08, 2023 01:50
                                     |
| Fixed.
                                        Posted by svoboda at Feb 10, 2023 17:52
                                     |

