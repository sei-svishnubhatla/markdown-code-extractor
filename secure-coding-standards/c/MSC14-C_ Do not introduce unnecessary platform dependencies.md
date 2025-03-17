Platform dependencies may be introduced to improve performance on a particular platform. This can be a dangerous practice, particularly if these dependencies are not appropriately documented during development and addressed during porting. Platform dependencies that have no performance or other benefits should consequently be avoided because they may introduce errors during porting.
The C Standard identifies four different kinds of nonportable behavior. Each section of Annex J of the C Standard enumerates distinct instances of behaviors of each kind.

| Nonportable Behavior | Definition | Annex J Section |
| ----|----|----|
| Unspecified behavior | Behavior for which the standard provides two or more possibilities and imposes no further requirements on which is chosen in any instance. | J.1 |
| Undefined behavior | Behavior, upon use of a nonportable or erroneous program construct or of erroneous data, for which the standard imposes no requirements. An example of undefined behavior is the behavior on signed integer overflow. | J.2 |
| Implementation-defined behavior | Unspecified behavior whereby each implementation documents how the choice is made. | J.3 |
| Locale-specific behavior | Behavior that depends on local conventions of nationality, culture, and language that each implementation documents. | J.4 |

An example of [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) is passing a null `char*` pointer as an argument to the `printf` function corresponding to the `%s` format specification. Although some [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) (such as the [GNU C Library](http://www.gnu.org/software/libc/)) provide well-defined semantics for this case, others do not, causing programs that rely on this behavior to fail abnormally.
An example of [unspecified behavior](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior) is the order in which the arguments to a function are evaluated.
An example of [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) is the propagation of the high-order bit when a signed integer is shifted right.
Most legitimate platform dependencies can and should be isolated in separate modules that expose portable, platform-agnostic interfaces to platform-specific implementations. Portable applications that cannot avoid relying on platform-specific details should always provide a generic, portable, standards-based solution as a fallback mechanism for the platform-specific alternative. That way, such an application can be more easily ported to new platforms without an excessive risk of [security flaws](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) caused by assumptions that do not hold in the new environment.
## Noncompliant Code Example
This noncompliant code example uses the complement operator in the test for integer overflow. It assumes both numbers are nonnegative:
``` c
signed int si;
signed int si2;
signed int sum;
if (si < 0 || si2 < 0) {
  /* Handle error condition */
}
if (~si < si2) {
  /* Handle error condition */
}
sum = si + si2;
```
This code assumes that the implementation uses two's complement representation. This assumption is commonly true but is not guaranteed by the standard.
This code sample also violates [INT14-C. Avoid performing bitwise and arithmetic operations on the same data](INT14-C_%20Avoid%20performing%20bitwise%20and%20arithmetic%20operations%20on%20the%20same%20data).
## Compliant Solution
This compliant solution implements a [strictly conforming](BB.-Definitions_87152273.html#BB.Definitions-strictlyconforming) test for overflow:
``` c
unsigned int si;
unsigned int si2;
unsigned int sum;
if (si < 0 || si2 < 0) {
  /* Handle error condition */
}
if (INT_MAX - si < si2) {
  /* Handle error condition */
}
sum = si + si2;
```
If the noncompliant form of this test is truly faster, talk to your compiler vendor because, if these tests are equivalent, optimization should occur. If both forms have the same performance, prefer the portable form.
## Noncompliant Code Example (`strerror_r`)
The GNU libc implementation of [strerror_r](http://linux.die.net/man/3/strerror_r) declares the function to return `char*`, in conflict with the POSIX specification. This noncompliant code example relies on this return type to pass the return value as an argument to the `%s` formatting directive to `fprintf`. The behavior of the example will be [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) on a platform that declares the return type of `strerror_r()` to be `int`, in accordance with POSIX.
``` c
void f() {
  char buf[BUFSIZ];
  fprintf(stderr, "Error: %s\n",
          strerror_r(errno, buf, sizeof buf));
}
```
## Compliant Solution (`strerror_r`)
The compliant solution disables the nonconforming declaration of `strerror_r()` by explicitly requesting POSIX conformance before including the `<string.h>` header that declares the function and handles the function's failure by copying the `"Unknown error"` string into the buffer. An alternate solution is to use the `strerror_s()` function defined by Annex K.
Note that the function assigns the result of the call to `strerror_r()` to a variable of type `int`. This assignment is a defense-in-depth strategy guarding against inadvertently invoking `strerror_r()` that returns `char*`: a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) compiler is required to issue a diagnostic for the ill-formed conversion from `char*` to `int`.
``` c
#define _XOPEN_SOURCE 600
#include <string.h>
#include <stdio.h>
#include <errno.h>
void f() {
  char buf[BUFSIZ];
  int result;
  result = strerror_r(errno, buf, sizeof buf);
  if (0 != result) {
    strcpy(buf, "Unknown error");
  }
  fprintf(stderr, "Error: %s\n", buf);
}
```
## Risk Assessment
Unnecessary platform dependencies are, by definition, unnecessary. Avoiding these dependencies can eliminate porting errors resulting from invalidated assumptions.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC14-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Helix QAC | 2024.4 | C0202, C0240, C0241, C0242, C0243, C0246, C0284, C0551, C0581, C0601, C0633, C0634, C0635, C0660, C0662, C0830, C0831, C0840, C0899, C1001, C1002, C1003, C1006, C1008, C1012, C1014, C1015, C1019, C1020, C1021, C1022, C1026, C1028, C1029, C1034, C1035, C1036, C1037, C1038, C1041, C1042, C1043, C1044, C1045, C1046, C1434, C3664 |  |
| LDRA tool suite | 9.7.1 | 17 D, 69 S, 42 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC14-aCERT_C-MSC14-b
 | Evaluation of constant unsigned integer expressions should not lead to wrap-aroundEvaluation of constant unsigned integer expressions in preprocessor directives should not lead to wraparound |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC14-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC14-CPP. Do not introduce unnecessary platform dependencies |
| ISO/IEC TR 24772 | Unspecified Behaviour [BQF] |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Arithmetic Boundary Conditions," pp. 211–223) |
| [Seacord 2013] | Chapter 5, "Integer Security" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152095) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152050)
## Comments:

|  |
| ----|
| I think this rule should be analyzable.  Finding the noncompliant code example should be relatively easy, provided that someone thought this was worth the time to do.  More importantly, this is a catch all for eliminating all implementation-defined and unspecified behaviors that can be replicated in a portable manner.  It would probably help if we created more NCE/CS pairs to illustrate other examples.
                                        Posted by rcs_mgr at Feb 17, 2009 10:17
                                     |
| Exactly. I'll agree that the NCCE is easily analyzeable. What isn't analyzeable is 'platform dependencies'...eg what this rule is supposed to be about.
I'll be happy to change this to 'rose-possible' if we can enumerate all the 'unnecessary platform dependencies' the rule alludes to.
                                        Posted by svoboda at Feb 18, 2009 14:35
                                     |
| How does the first NCCE rely on two's complement? Isn't everything it's doing being done on unsigned values? When exactly would it be wrong?
                                        Posted by jcsible at Jan 04, 2021 14:44
                                     |
| You're right...the NCCE behaves the same on a signed-magnitude or ones-complement machine. It is still noncompliant because of the INT14-C violation.; I've adjusted the text.
                                        Posted by svoboda at Jan 04, 2021 16:03
                                     |
| But why is an example that only violates INT14-C on the MSC14-C page?
                                        Posted by jcsible at Jan 04, 2021 16:11
                                     |
| It seems this example has been unchanged since this guideline was first conceived. I changed it to use signed positive integers, which means the NCCE does truly rely on twos-complement representation.
                                        Posted by svoboda at Jan 05, 2021 09:19
                                     |

