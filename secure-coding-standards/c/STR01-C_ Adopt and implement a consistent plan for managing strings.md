There are two basic approaches for managing strings in C programs: the first is to maintain strings in statically allocated arrays; the second is to dynamically allocate memory as required. Each approach has advantages and disadvantages. However, it generally makes sense to select a single approach to managing strings and apply it consistently across a project. Otherwise, the decision is left to individual programmers who are likely to make different, inconsistent choices.
Statically allocated strings assume a fixed-size character array, meaning that it is impossible to add data after the buffer is filled. Because the static approach discards excess data, actual program data can be lost. Consequently, the resulting string must be fully validated.
Dynamically allocated buffers dynamically resize as additional memory is required. Dynamic approaches scale better and do not discard excess data. The major disadvantage is that, if inputs are not limited, they can exhaust memory on a machine and consequently be used in [denial-of-service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) attacks.
Dynamic allocation is often disallowed in safety-critical systems. For example, the MISRA standard requires that "dynamic heap memory allocation shall not be used" \[[MISRA 2004](AA.-Bibliography_87152170.html#AA.Bibliography-MISRA04)\]. Some safety-critical systems can take advantage of dynamic memory allocation during initialization but not during operations. For example, avionics software may dynamically allocate memory while initializing the aircraft but not during flight.
A number of existing libraries are available for managing string data; the library selected depends on the approach adopted for managing null-terminated byte strings. The functions defined by the C Standard, subclause 7.24, are primarily intended for managing statically allocated strings. However, these functions are problematic because many of them are insufficiently bounded. Consequently, this standard recommends using the C11 Annex K functions with statically allocated arrays. (See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).) These functions provide bounds-checking interfaces to protect against buffer overflows and other runtime constraint violations.
ISO/IEC TR 24731 Part II offers another approach, supplying functions that allocate enough memory for their results \[[ISO/IEC TR 24731-2](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\]. It provides an API that dynamically allocates the results of string functions as needed. Almost all of the APIs in this technical report are also in a current international standard. For example, TR 24731 Part II includes POSIX functions, such as `strdup()` \[[ISO/IEC 9945:2003](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9945-2003)\], as well as functions from the Linux Standard Base Core Specification such as `asprintf()` \[[ISO/IEC 23360-1:2006](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC23360-1-2006)\].
## Risk Assessment
Failing to adopt a consistent plan for managing strings within an application can lead to inconsistent decisions, which may make it difficult to ensure system properties, such as adhering to safety requirements.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR01-C | Low | Unlikely | High | P1 | L3 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR01-CPP. Adopt and implement a consistent plan for managing strings |
| ISO/IEC TR 24731-2:2010 | ; |
| MISRA C:2012 | Directive 4.12 (required) |

## Bibliography

|  |  |
| ----|----|
| [CERT 2006c] | ; |
| [ISO/IEC 9945:2003] | ; |
| [ISO/IEC 23360-1:2006] | ; |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152151) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152409)
## Comments:

|  |
| ----|
| This is probably a good example of a guideline that shouldn't be here;  this material is better suited for the training.
I'm also wondering if we shouldn't just give up recommending the CERT managed string library at this point, which hasn't been widely adopted to this point.
                                        Posted by rcs_mgr at Sep 02, 2011 08:08
                                     |
| Has any managed string library been widely adopted? (How does one measure adoption of a managed string library, esp an open-source one like CERT's?)
                                        Posted by svoboda at Sep 02, 2011 10:55
                                     |
| I agree it's difficult to gauge the level of adoption but I also think that modular programs are unlikely to adopt a single policy when their modules (shared libraries) are developed by independent teams or organizations. Only closed systems (where all modules are developed by the same team/organization) might realistically be able to adopt such a policy, or perhaps the few systems that are being developed completely from scratch and where the developers have the luxury of developing wrappers for modules that don't conform.
It's a nice recommendation in theory but it's unlikely to be viable in practice.
                                        Posted by martinsebor at Sep 15, 2011 12:17
                                     |

