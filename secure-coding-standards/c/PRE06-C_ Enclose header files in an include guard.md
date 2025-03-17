Until the early 1980s, large software development projects had a continual problem with the inclusion of headers. One group might have produced a `graphics.h`, for example, which started by including `io.h`. Another group might have produced `keyboard.h`, which also included `io.h`. If `io.h` could not safely be included several times, arguments would break out about which header should include it. Sometimes an agreement was reached that each header should include no other headers, and as a result, some application programs started with dozens of `#include` lines, and sometimes they got the ordering wrong or forgot a required header.
## Compliant Solution
All these complications disappeared with the discovery of a simple technique: each header should `#define` a symbol that means "I have already been included." The entire header is then enclosed in an include guard:
``` c
#ifndef HEADER_H
#define HEADER_H
/* ... Contents of <header.h> ... */
#endif /* HEADER_H */
```
Consequently, the first time `header.h` is `#include`'d, all of its contents are included. If the header file is subsequently `#include`'d again, its contents are bypassed.
Because solutions such as this one make it possible to create a header file that can be included more than once, the C Standard guarantees that the standard headers are safe for multiple inclusion.
Note that it is a common mistake to choose a reserved name (such as `_HEADER_H_` or `__HEADER_H__`) for the name of the macro used in the include guard. See [DCL37-C. Do not declare or define a reserved identifier](DCL37-C_%20Do%20not%20declare%20or%20define%20a%20reserved%20identifier) for more information.
## Risk Assessment
Failure to include header files in an include guard can result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE06-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | include-guard-missinginclude-guard-pragma-once | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE06 |  |
| ECLAIR | 1.2 | CC2.PRE06 | Fully implemented |
| Helix QAC | 2024.4 | C0883 |  |
| Klocwork | 2024.4 | MISRA.INCGUARD |  |
| LDRA tool suite | 9.7.1 | 243 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE06-a | Use multiple include guards |
| PC-lint Plus | 1.4 | 967 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE06-C | Checks for content of header file not guarded from multiple inclusions (rec. fully covered) |
| RuleChecker | 24.04 | include-guard-missinginclude-guard-pragma-once | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE06-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE06-CPP. Enclose header files in an include guard |
| MISRA C:2012 | Directive 4.10 (required) |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] | Rule 1-14 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152353) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152056)
## Comments:

|  |
| ----|
| I think you have an exclusion here for the cases when you do want to include headers more than once.
Some headers do need to be included more than once (e.g. the standard header assert.h).
Sometimes, generated code can result in headers that need to be included multiply too.
                                        Posted by stewartb at Mar 13, 2008 20:12
                                     |
| This is a double-edged sword. Including the same file multiple times has it's benefits when you know what you are doing. I realize that you are trying to set up a common set of rules to make people compliant and safe, but in some cases there are are much broader applicability for including the header file multiple times like here. One of the common problems with C/C++ code is the repeated switch statements where a given "enum" type is being used in multiple contexts. Multiple-header-inclusion solves this to be lazy and auto generated.
YMMV. ;
                                        Posted by k0wsik at Mar 14, 2008 01:39
                                     |

