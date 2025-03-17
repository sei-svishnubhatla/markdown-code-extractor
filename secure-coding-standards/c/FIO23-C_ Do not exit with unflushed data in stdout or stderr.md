The C standard makes no guarantees as to when output to `stdout` (standard output) or `stderr` (standard error) is actually flushed. On many platforms, output to `stdout` is buffered unless `stdout` outputs to a terminal, and `stderr` output is typically not buffered. However, programs are free to modify the buffering rules for either `stdout` or `stderr`. Programs are also free to explicitly close `stdout` or `stderr`; if they do not do so, these streams will be closed upon program termination.
Closing any output stream requires flushing any data that has not yet been written to the stream. The flushing operation (manually handled by the `fflush()` function) can fail for several reasons. The output stream may be directed to a file in a filesystem with no remaining free space, or to a network socket that fails. Checking for the success of a `fflush()` operation is mandatory for a secure program, and hence checking the result of a `fclose()` operation is also required.
Consequently, any program that sends data to `stdout` or `stderr` must take care to flush the data before it terminates. Failing to flush the data (with a call to `fflush()` or `fclose()`), may cause the data to fail to be written and become lost.
## Noncompliant Code Example
This noncompliant code example sends some data to standard output. If standard output is directed to a file and an error occurs while flushing the data (after program termination), then the output may be lost.
``` c
#include <stdio.h>
int main(void) {
  printf("Hello, world!\n");
  return 0;
}
```
## Compliant Solution
This compliant solution explicitly closes `stdout`, and handles any errors that arise.
``` c
#include <stdio.h>
int main(void) {
  printf("Hello, world!\n");
  if (fclose(stdout) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
## Noncompliant Code Example (`atexit()`)
This noncompliant code example closes standard output before exiting `main()`, but then tries to print to standard output in an exit handler.
``` c
#include <stdio.h>
void cleanup(void) {
  /* Do cleanup */
  printf("All cleaned up!\n");
}
int main(void) {
  atexit(cleanup);
  printf("Doing important stuff\n");
  /* Do important stuff */
  if (fclose(stdout) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (`atexit()`)
This compliant solution uses `fflush()` instead of `fclose()`, and the exit handler also uses `fflush()` to flush its output:
``` c
#include <stdio.h>
void cleanup(void) {
  /* Do cleanup */
  printf("All cleaned up!\n");
  if (fflush(stdout) == EOF) {
    /* Handle error */
  }
}
int main(void) {
  atexit(cleanup);
  printf("Doing important stuff\n");
  /* Do important stuff */
  if (fflush(stdout) == EOF) {
    /* Handle error */
  }
  return 0;
}
```
## Exceptions
**FIO23-C-EX1:** Programs that do not send data to either output stream need not close them.  
**FIO23-C-EX2:** Programs that never run with buffered output streams need not close them.
## Risk Assessment
Failing to flush data buffered for standard output or standard error may result in lost data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO23-C | Medium | Unlikely | Medium | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO23-C).
------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152114) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152138)
