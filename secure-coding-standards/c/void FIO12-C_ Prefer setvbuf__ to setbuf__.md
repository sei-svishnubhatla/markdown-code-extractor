> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't)

The `setbuf()` function can be replaced by the `setvbuf()` function because
``` java
(void) setbuf(stream, buf);
```
is equivalent to
``` java
int setvbuf(stream, buf, _IOFBF, BUFSIZ);
```
or
``` java
int setvbuf(stream, buf, _IONBF, BUFSIZ);
```
if `buf` is a null pointer.
Section 7.21.5.5 of the C Standard defines `setbuf()` as follows \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\]:
> Except that it returns no value, the `setbuf` function is equivalent to the `setvbuf` function invoked with the values `_IOFBF` for `mode` and `BUFSIZ` for `size`, or (if `buf` is a null pointer), with the value `_IONBF` for `mode`.

Consequently, `setvbuf()` should be used instead of `setbuf()` to validate that the stream was successfully altered.
## Noncompliant Code Example
This noncompliant code example calls `setbuf()` with a `buf` argument of `NULL`:
``` c
FILE *file;
/* Setup file */
setbuf(file, NULL);
/* ... */
```
It is not possible to determine if the call to `setbuf()` succeeded.
### Implementation Details
On 4.2BSD and 4.3BSD systems, `setbuf()` always uses a suboptimal buffer size and should be avoided.
## Compliant Solution
This compliant solution calls `setvbuf()`, which returns nonzero if the operation failed:
``` c
FILE *file;
char *buf = NULL;
/* Setup file */
if (setvbuf(file, buf, buf ? _IOFBF : _IONBF, BUFSIZ) != 0) {
  /* Handle error */
}
/* ... */
```
## Risk Assessment
Using `setbuf()` may result in a failure to catch errors, potentially causing improper control flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO12-C | low | unlikely | medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| ECLAIR | 1.2 | CC2.FIO12 | Fully implemented |
| LDRA tool suite | 9.7.1 | 594 S | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | Warncall -wc setbuf | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO12-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO12-CPP. Prefer setvbuf() to setbuf() |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.21.5.5, "The setbuf Function" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=3473587) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040) [](https://www.securecoding.cert.org/confluence/display/seccode/FIO13-C.+Never+push+back+anything+other+than+one+read+character?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This is a fairly innocuous error, which appears more related to performance than security.  We are also ignoring the potentially interesting case where setbuf() sets the buffer too small. 
                                        Posted by rcs at Mar 11, 2008 09:38
                                     |
| ... how can you tell that your view of BUFSIZ is the same as known by every other version of the library on the system (not all of which may have been compiled on your particular system) ?
                                        Posted by steve at Mar 14, 2008 02:09
                                     |
| Why does the NCCE bother with the variable buf?; Why not just pass NULL directly to setbuf().
Is there a problem worth mentioning that if the buffer passed to these routines has automatic scope (even in main()) and the file is not closed before returning from main, then you get undefined behaviour when atexit() or the rest of exit() tries to flush the buffer (or am I not reading ahead again)?  
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:51
                                     |
| Actually setbuf cannot fail.
A slight;advantage of setvbuf is that it can allocate the buffer.  Its main purpose is to set no buffering or line buffering.
                                        Posted by dagwyn at Apr 17, 2008 12:33
                                     |
| This doesn't seem like a particularly useful recommendation to me, and I'll probably delete it unless anyone can argue for why it should stay.
                                        Posted by rcs at Jun 01, 2008 04:25
                                     |
| there is nothing in the standard that guarantees that setbuf() does not fail, it says it is equivalent to a call to setvbuf(), which is allowed to error when "the request cannot be honored"
while I agree that there is probably no implementation in which setbuf() can fail, this document is about C99, and in C99 this function could error and fail to report the error.
                                        Posted by avolkovi at Jun 02, 2008 16:03
                                     |
| The scope of this document is C99, but document itself is about secure coding.  There is a bit of a difference.  I think we should research this a bit more and see if there are implementations that can might fail, for example, if buf were a function pointer or something.
                                        Posted by rcs at Jun 18, 2008 10:52
                                     |
| I see two interesting failure modes for a call to setbuf(f, buf):
    fileno(f) is an invalid file descriptor
    fileno(f) is a valid file descriptor but (buf == NULL) evaluates to true
In both cases, the call is specified to have the same effects as setvbuf(stream, buf, _IONBF, BUFSIZ).
While C leaves the behavior unspecified in both cases, in (1) POSIX says the equivalent setvbuf call may fail with EBADF. Since setbuf() doesn't return a value this error is undetectable except by checking errno and only on POSIX systems.
In (2), although the setvbuf page doesn't explicitly say so, POSIX permits implementations to fail for reasons other than those listed. Since the only required effects of the call to setvbuf(stream, NULL, _IONBF, BUFSIZ) are to set the stream into an unbuffered state, it's possible for an implementation to try to allocate memory (as it does when (buf == NULL && type == _IOFBF)) and fail. In this case, a POSIX implementation may fail with ENOMEM. But again, since setbuf() doesn't return a value this error is undetectable except by checking errno and only on POSIX systems.
That being said, since this guideline is already covered by ERR07-C. Prefer functions that support error checking over equivalent functions that don't, I agree with removing it.
                                        Posted by martinsebor at Jan 27, 2010 22:56
                                     |

