Some errors, such as out-of-range values, might be the result of erroneous user input. Interactive programs typically handle such errors by rejecting the input and prompting the user for an acceptable value. Servers reject invalid user input by indicating an error to the client while at the same time continuing to service other clients' valid requests. All [robust](BB.-Definitions_87152273.html#BB.Definitions-robustness) programs must be prepared to gracefully handle resource exhaustion, such as low memory or disk space conditions, at a minimum by preventing the loss of user data kept in volatile storage. Interactive programs may give the user the option to save data on an alternative medium, whereas network servers may respond by reducing throughput or otherwise degrading the quality of service. However, when certain kinds of errors are detected, such as irrecoverable logic errors, rather than risk data corruption by continuing to execute in an indeterminate state, the appropriate strategy may be for the system to quickly shut down, allowing the operator to start it afresh in a determinate state.
ISO/IEC TR 24772:2013, Section 6.39, "Termination Strategy \[REU\]," \[[ISO/IEC TR 24772:2013](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24772-2013)\], says:
> When a fault is detected, there are many ways in which a system can react. The quickest and most noticeable way is to fail hard, also known as fail fast or fail stop. The reaction to a detected fault is to immediately halt the system. Alternatively, the reaction to a detected fault could be to fail soft. The system would keep working with the faults present, but the performance of the system would be degraded. Systems used in a high availability environment such as telephone switching centers, e-commerce, or other "always available" applications would likely use a fail soft approach. What is actually done in a fail soft approach can vary depending on whether the system is used for safety-critical or security critical purposes. For fail-safe systems, such as flight controllers, traffic signals, or medical monitoring systems, there would be no effort to meet normal operational requirements, but rather to limit the damage or danger caused by the fault. A system that fails securely, such as cryptologic systems, would maintain maximum security when a fault is detected, possibly through a denial of service.

And
> The reaction to a fault in a system can depend on the criticality of the part in which the fault originates. When a program consists of several tasks, each task may be critical, or not. If a task is critical, it may or may not be restartable by the rest of the program. Ideally, a task that detects a fault within itself should be able to halt leaving its resources available for use by the rest of the program, halt clearing away its resources, or halt the entire program. The latency of task termination and whether tasks can ignore termination signals should be clearly specified. Having inconsistent reactions to a fault can potentially be a vulnerability.

C provides several options for program termination, including `exit()`, returning from `main()`, `_Exit()`, and `abort()`.
## `exit()`
Calling `exit()` causes [normal program termination](BB.-Definitions_87152273.html#BB.Definitions-normaltermination) to occur. Other than returning from `main()`, calling `exit()` is the typical way to end a program. The function takes one argument of type `int`, which should be either `EXIT_SUCCESS` or `EXIT_FAILURE`, indicating successful or unsuccessful termination respectively. The value of `EXIT_SUCCESS` is guaranteed to be 0. The C Standard, subclause 7.22.4.4 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], says, "If the value of status is zero or `EXIT_SUCCESS`, an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-defined) form of the status successful termination is returned." The `exit()` function never returns.
``` c
#include <stdlib.h>
/* ... */
if (/* Something really bad happened */) {
  exit(EXIT_FAILURE);
}
```
Calling `exit()`
-   Flushes unwritten buffered data.
-   Closes all open files.
-   Removes temporary files.
-   Returns an integer exit status to the operating system.
The C Standard `atexit()` function can be used to customize `exit()` to perform additional actions at program termination.
For example, calling
``` c
atexit(turn_gizmo_off);
```
*registers* the `turn_gizmo_off()` function so that a subsequent call to `exit()` will invoke `turn_gizmo_off()` as it terminates the program. C requires that `atexit()` can register at least 32 functions.
Functions registered by the `atexit()` function are called by `exit()` or upon normal completion of `main()`.
Note that the behavior of a program that calls `exit()` from an `atexit` handler is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See undefined behavior [187](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_187) in Annex J of the C Standard. See also [ENV32-C. All exit handlers must return normally](ENV32-C_%20All%20exit%20handlers%20must%20return%20normally).)
## `return` from `main()`
Returning from `main()` causes [normal program termination](BB.-Definitions_87152273.html#BB.Definitions-normaltermination) to occur, which is the preferred way to terminate a program. Evaluating the `return` statement has the same effect as calling `exit()` with the same argument.
``` c
#include <stdlib.h>
int main(int argc, char **argv) {
  /* ... */
  if (/* Something really bad happened */) {
    return EXIT_FAILURE;
  }
  /* ... */
  return EXIT_SUCCESS;
}
```
The C Standard, subclause 5.1.2.2.3 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], has this to say about returning from `main()`:
> If the return type of the `main` function is a type compatible with `int`, a return from the initial call to the `main` function is equivalent to calling the `exit` function with the value returned by the `main` function as its argument; reaching the `}` that terminates the `main` function returns a value of 0. If the return type is not compatible with `int`, the termination status returned to the host environment is unspecified.

Consequently, returning from `main()` is equivalent to calling `exit()`. Many compilers implement this behavior with something analogous to
``` java
void _start(void) {
  /* ... */
  exit(main(argc, argv));
}
```
However, exiting from `main` is conditional on correctly handling all errors in a way that does not force premature termination. (See [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy) and [ERR05-C. Application-independent code should provide error detection without dictating error handling](ERR05-C_%20Application-independent%20code%20should%20provide%20error%20detection%20without%20dictating%20error%20handling).)
## `_Exit()`
Calling `_Exit()` causes [normal program termination](BB.-Definitions_87152273.html#BB.Definitions-normaltermination) to occur. Like the `exit()` function, `_Exit()` takes one argument of type `int` and never returns. However, unlike `exit()`, whether `_Exit()` closes open streams, flushes stream buffers,<sup>\[[1](#ERR04C.Chooseanappropriateterminationstrategy-1)\]</sup> or deletes temporary files is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). Functions registered by `atexit()` are not executed.
\[1\] Note that POSIX strengthens the specification for `_Exit()` by prohibiting the function from flushing stream buffers. See the documentation of the function in [The Open Group Base Specifications Issue 7,](http://www.opengroup.org/onlinepubs/9699919799) IEEE Std 1003.1, 2013 Edition \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
``` c
#include <stdlib.h>
/* ... */
if (/* Something really bad happened */) {
  _Exit(EXIT_FAILURE);
}
```
The `_exit()` function is an alias for `_Exit()`.
## `abort()`
Calling `abort()` causes [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) to occur unless the `SIGABRT` signal is caught and the signal handler calls `exit()` or `_Exit()`:
``` c
#include <stdlib.h>
/* ... */
if (/* Something really bad happened */) {
  abort();
}
```
As with `_Exit()`, whether open streams with unwritten buffered data are flushed,<sup>\[[2](#ERR04C.Chooseanappropriateterminationstrategy-2)\]</sup> open streams are closed, or temporary files are removed is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-defined). Functions registered by `atexit()` are not executed. (See [ERR06-C. Understand the termination behavior of assert() and abort()](ERR06-C_%20Understand%20the%20termination%20behavior%20of%20assert__%20and%20abort__).)
\[2\] Unlike in the case of `_Exit()`, POSIX explicitly permits but does not require [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) to flush stream buffers. See the documentation of the function in [The Open Group Base Specifications Issue 7,](http://www.opengroup.org/onlinepubs/9699919799) IEEE Std 1003.1, 2013 Edition \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].
## Summary
The following table summarizes the exit behavior of the program termination functions.

| Function | Closes 
Open 
Streams | Flushes 
Stream 
Buffers | Removes 
Temporary 
Files | Calls 
atexit() 
Handlers | Program 
Termination |
| ----|----|----|----|----|----|
| abort() |  | ;[2] |  |  | Abnormal |
| _Exit() |  | ;[1] |  |  | Normal |
| exit() |  |  |  |  | Normal |
| Return from main() |  |  |  |  | Normal |

Table legend:
-   ![](images/icons/emoticons/check.svg) – Yes. The specified action is performed.
-   ![](images/icons/emoticons/error.svg) – No. The specified action is not performed.
-   ![](images/icons/emoticons/information.svg) – [Implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). Whether the specified action is performed depends on the implementation.
## Noncompliant Code Example
The `abort()` function should not be called if it is important to perform application-specific cleanup before exiting. In this noncompliant code example, `abort()` is called after data is sent to an open file descriptor. The data may or may not be written to the file.
``` c
#include <stdlib.h>
#include <stdio.h>
int write_data(void) {
  const char *filename = "hello.txt";
  FILE *f = fopen(filename, "w");
  if (f == NULL) {
    /* Handle error */
  }
  fprintf(f, "Hello, World\n");
  /* ... */
  abort(); /* Oops! Data might not be written! */
  /* ... */
  return 0;
}
int main(void) {
  write_data();
  return EXIT_SUCCESS;
}
```
## Compliant Solution
In this compliant solution, the call to `abort()` is replaced with `exit()`, which guarantees that buffered I/O data is flushed to the file descriptor and the file descriptor is properly closed:
``` c
#include <stdlib.h>
#include <stdio.h>
int write_data(void) {
  const char *filename = "hello.txt";
  FILE *f = fopen(filename, "w");
  if (f == NULL) {
    /* Handle error */
  }
  fprintf(f, "Hello, World\n");
  /* ... */
  exit(EXIT_FAILURE); /* Writes data and closes f */
  /* ... */
  return 0;
}
int main(void) {
  write_data();
  return EXIT_SUCCESS;
}
```
Although this particular example benefits from calling `exit()` over `abort()`, in some situations, `abort()` is the better choice. Usually, `abort()` is preferable when a programmer does not need to close any file descriptors or call any handlers registered with `atexit()`, for instance, if the speed of terminating the program is critical.
For more details on proper usage of `abort()`, see [ERR06-C. Understand the termination behavior of assert() and abort()](ERR06-C_%20Understand%20the%20termination%20behavior%20of%20assert__%20and%20abort__).
## Risk Assessment
As an example, using `abort()` or `_Exit()` in place of `exit()` may leave written files in an inconsistent state and may also leave sensitive temporary files on the file system.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR04-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Parasoft C/C++test | 2024.2 | CERT_C-ERR04-aCERT_C-ERR04-b
CERT_C-ERR04-c
 | The 'abort()' function from the 'stdlib.h' or 'cstdlib' library shall not be usedThe 'exit()' function from the 'stdlib.h' or 'cstdlib' library shall not be used
The 'quick_exit()' and '_Exit()' functions from the 'stdlib.h' or 'cstdlib' library shall not be used |
| PC-lint Plus | 1.4 | 586 | Fully supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ERR04-CPP. Choose an appropriate termination strategy |
| CERT Oracle Secure Coding Standard for Java | FIO14-J. Perform proper cleanup at program termination |
| ISO/IEC TR 24772:2013 | Termination Strategy [REU] |
| MITRE CWE | CWE-705, Incorrect control flow scoping |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, exit |
| [ISO/IEC 9899:2011] | Subclause 5.1.2.2.3, "Program Termination"Subclause 7.22.4, "Communication with the Environment" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152140) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152136)
## Comments:

|  |
| ----|
| setjmp() and longjmp() doesn't provide a means to exit the program, they are just an advanced 'goto' within the program.
                                        Posted by svoboda at May 16, 2008 10:13
                                     |
| do we really need the NCCE/CCE for abort now that we have ERR06-C. Understand the termination behavior of assert() and abort()?
                                        Posted by avolkovi at Jun 03, 2008 14:58
                                     |
| I suppose the NCCE/CCE are covered more specifically by ERR06-C than by this rule. But I'd like to keep them here, mainly so this rule has a CCE/NCCE pair.
I added a citation to ERR06-C to the CCE.
                                        Posted by svoboda at Jul 25, 2008 16:43
                                     |

