If an attacker can overwrite memory containing function pointers, they may be able to execute arbitrary code. To mitigate the effects of such attacks, pointers to functions can be encrypted at runtime on the basis of some characteristics of the execution process so that only a running process will be able to decode them.  This is only required for stored function pointers stored to writable memory, including the stack.  The Microsoft SDL \[Microsoft 2012\] recommends encoding long-lived pointers in your code.
## Noncompliant Code Example
This noncompliant code example assigns the address of the `printf()` function to the `log_fn` function pointer, which can be allocated in the stack or data segment:
``` c
int (*log_fn)(const char *, ...) = printf;
/* ... */
log_fn("foo");
```
If a vulnerability exists in this program that allows an attacker to overwrite the `log_fn` function pointer, such as a buffer overflow or arbitrary memory write, the attacker may be able to overwrite the value of `printf` with the location of an arbitrary function.
## Compliant Solution (Windows)
Microsoft Windows provides the [EncodePointer()](http://msdn.microsoft.com/en-us/library/bb432254(VS.85).aspx) and [DecodePointer()](http://msdn.microsoft.com/en-us/library/bb432242(VS.85).aspx) functions that encrypt and decrypt pointers using a secret that is unique to the given process:
``` c
#include <Windows.h>
void *log_fn = EncodePointer(printf);
/* ... */
int (*fn)(const char *, ...) = (int (*)(const char *, ...))DecodePointer(log_fn);
fn("foo");
```
Note that `DecodePointer()` does not return success or failure.  If an attacker has overwritten the pointer contained in `log_fn`, the pointer returned will be invalid and cause your application to crash.  However, this is preferable to giving an attacker the ability to execute arbitrary code. 
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN04-C | High | Unlikely | Low | P9 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabi) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC16-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC16-CPP. Consider encrypting function pointers |
| MITRE CWE | CWE-311, Missing encryption of sensitive dataCWE-319, Cleartext Transmission of Sensitive Information |

## Bibliography

|  |  |
| ----|----|
| [MSDN] | EncodePointer()DecodePointer() |
| Microsoft Corporation 2012 | Microsoft Security Development Lifecycle (SDL) – version 5.2 Phase 3: Implementation |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152035) [](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929)
## Comments:

|  |
| ----|
| Since the overhead to use these functions (in Windows) is sizable - it is typically recommended that these functions be used only for "long-lived" or global; pointers. Another option is to use EncodeSystemPointer/DecodeSystemPointer - these functions are faster, though relatively more vulnerable, than EncodePointer/DecodePointer. 
                                        Posted by abhi at Aug 13, 2008 09:20
                                     |
| This is a very poor recommendation. Let me count the ways:
(1) Address space layout randomization (ASLR) already does this, requires no code modifications, and is widely supported (often in the default environment) on most modern operating systems.
(2) The reference API (and anything similar) requires additional, explicit casting, because standard C does not support implicit conversion of void pointers to/from function pointers.
(3) Extra code - either non-standard code simply assigning to/from intermediary function pointer objects, or standard C-compatible explicit casting - will likely lead to more [security] bugs than this recommendation could mitigage. Casting especially is bug prone, and any standard C-conforming application would have to employ additional casting.
Indeed, this recommendation asks developers to further blur the line between code and data objects. That's entirely the wrong message to send.
                                        Posted by william@25thandclement.com at Aug 24, 2008 18:46
                                     |
| A proposal to support these function was considered for C11 but it was decided this it would be better for the compilers to encrypt/decrypt pointers instead without the addition of these library calls so it was determined that this was a quality of implementation issue.To respond to your specific points(1) ASLR is a useful security technology, but is not going to be useful in the advent of overflows at a relative offset to a function pointer as opposed to an absolute position.(2) Lack of a standard API is a problem, but that is why this is in the Windows section.(3) agreed, extra code always sucks.;
                                        Posted by rcs at Jun 06, 2015 08:25
                                     |
| I think it would be worth adding a compliant solution that took this approach.
                                        Posted by rcs at Jun 06, 2015 08:32
                                     |
| Relatively more vulnerable is being kind, IMO. The difference between the System and non-System APIs is that EncodePointer uses a per-application salt, while EncodeSystemPointer uses a per-machine salt. Since these are really only useful for function pointers stored as data, and sensitive functions should not typically be on the hot path, the extra overhead for added security is almost always worth the cost. That being said, we should at least call out the existence of the System APIs and explain the differences.
                                        Posted by aballman at Jun 07, 2015 10:32
                                     |

