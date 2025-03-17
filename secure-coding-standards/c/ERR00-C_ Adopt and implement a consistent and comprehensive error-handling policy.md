A secure system is invariably subject to stresses, such as those caused by attack, erroneous or malicious inputs, hardware or software faults, unanticipated user behavior, and unexpected environmental changes that are outside the bounds of "normal operation." Yet the system must continue to deliver essential services in a timely manner, safely and securely. To accomplish this, the system must exhibit qualities such as [robustness](BB.-Definitions_87152273.html#BB.Definitions-robustness), [reliability](BB.-Definitions_87152273.html#BB.Definitions-reliability), [error tolerance](BB.-Definitions_87152273.html#BB.Definitions-errortolerance), [fault tolerance](BB.-Definitions_87152273.html#BB.Definitions-faulttolerance), performance, and security. All of these system-quality attributes depend on consistent and comprehensive error handling that supports the goals of the overall system.
ISO/IEC TR 24772, section 6.39.1 \[[ISO/IEC TR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24772-2013)\], says:
> Expectations that a system will be dependable are based on the confidence that the system will operate as expected and not fail in normal use. The dependability of a system and its fault tolerance can be measured through the component part's reliability, availability, safety and security. Reliability is the ability of a system or component to perform its required functions under stated conditions for a specified period of time \[[IEEE 1990 glossary](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd610.121990)\]. Availability is how timely and reliable the system is to its intended users. Both of these factors matter highly in systems used for safety and security. In spite of the best intentions, systems may encounter a failure, either from internally poorly written software or external forces such as power outages/variations, floods, or other natural disasters. The reaction to a fault can affect the performance of a system and in particular, the safety and security of the system and its users.

Effective error handling (which includes error reporting, report aggregation, analysis, response, and recovery) is a central aspect of the design, implementation, maintenance, and operation of systems that exhibit survivability under stress. Survivability is the capability of a system to fulfill its mission, in a timely manner, despite an attack, accident, or other stress that is outside the bounds of normal operation \[[Lipson 2000](AA.-Bibliography_87152170.html#AA.Bibliography-Lipson00)\]. If full services cannot be maintained under a given stress, survivable systems degrade gracefully, continue to deliver essential services, and recover full services as conditions permit.
Error reporting and error handling play a central role in the engineering and operation of survivable systems. Survivability is an emergent property of a system as a whole \[[Fisher 1999](AA.-Bibliography_87152170.html#AA.Bibliography-Fisher99)\] and depends on the behavior of all of the system's components and the interactions among them. From the viewpoint of error handling, every system component, down to the smallest routine, can be considered to be a sensor capable of reporting on some aspect of the health of the system. Any error or anomaly, ignored or improperly handled, can threaten delivery of essential system services and, as a result, put at risk the organizational or business mission that the system supports.
The key characteristics of survivability include the 3 Rs: resistance, recognition, and recovery. Resistance refers to measures that *harden* a system against particular stresses, recognition refers to situational awareness with respect to instances of stress and their impact on the system, and recovery is the ability of a system to restore services after (and possibly during) an attack, accident, or other event that has disrupted those services.
Recognition of the full nature of adverse events and the determination of appropriate measures for recovery and response are often not possible in the context of the component or routine in which a related error first manifests. Aggregation of multiple error reports and the interpretation of those reports in a higher context may be required both to understand what is happening and to decide on the appropriate action to take. Of course, the domain-specific context in which the system operates plays a huge role in determining proper recovery strategies and tactics. For safety-critical systems, simply halting the system (or even just terminating an offending process) in response to an error is rarely the best course of action and may lead to disaster. From a system perspective, error-handling strategies should map directly into survivability strategies, which may include recovery by activating fully redundant backup services or by providing alternative sets of roughly equivalent services that fulfill the mission with sufficient diversity to greatly improve the odds of survival against common mode failures.
An error-handling policy must specify a comprehensive approach to error reporting and response. Components and routines should always generate status indicators, and all called routines should have their error returns checked. All input should be checked for compliance with the formal requirements for such input rather than be blindly trusted. Moreover, never assume, on the basis of specific knowledge about the system or its domain, that the success of a called routine is guaranteed. The failure to report or properly respond to errors or other anomalies from a system perspective can threaten the survivability of the system as a whole.
ISO/IEC TR 24772:2013, section 6.39.5 \[[ISO/IEC TR 24772:2013](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24772-2013)\], describes the following mitigation strategies:
> Software developers can avoid the vulnerability or mitigate its ill effects in the following ways:
>
> -   A strategy for fault handling should be decided. Consistency in fault handling should be the same with respect to critically similar parts.
> -   A multi-tiered approach of fault prevention, fault detection, and fault reaction should be used.
> -   System-defined components that assist in uniformity of fault handling should be used when available. For one example, designing a "runtime constraint handler" (as described in Annex K of \[the [C Standard](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]) permits the application to intercept various erroneous situations and perform one consistent response, such as flushing a previous transaction and restarting at the next one.
> -   When there are multiple tasks, a fault-handling policy should be specified whereby a task may
>     -   halt, and keep its resources available for other tasks (perhaps permitting restarting of the faulting task)
>     -   halt, and remove its resources (perhaps to allow other tasks to use the resources so freed, or to allow a recreation of the task)
>     -   halt, and signal the rest of the program to likewise halt

## Risk Assessment
Failure to adopt and implement a consistent and comprehensive error-handling policy is detrimental to system survivability and can result in a broad range of [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) depending on the operational characteristics of the system.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR00-C | Medium | Probable | High | P4 | L3 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR00-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Polyspace Bug Finder | R2024a | CERT C: Rec. ERR00-C | Checks for situations where error information is not checked (rec. partially covered) |

## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Termination Strategy [REU] |
| MISRA C:2012 | Rule 17.1 (required) |
| MITRE CWE | CWE-391, Unchecked error conditionCWE-544, Missing standardized error handling mechanism |

## Bibliography

|  |  |
| ----|----|
| [Fisher 1999] |  |
| [Horton 1990] | Section 11, p. 168Section 14, p. 254 |
| [Koenig 1989] | Section 5.4, p. 73 |
| [Lipson 2000] |  |
| [Lipson 2006] |  |
| [Summit 2005] | C-FAQ Question 20.4 |

------------------------------------------------------------------------
[](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_) [](../c/ERR01-C_%20Use%20ferror__%20rather%20than%20errno%20to%20check%20for%20FILE%20stream%20errors)
## Comments:

|  |
| ----|
| Some library functions make multiple system calls, and some system calls might fail (e.g. an open() call without O_CREAT) and then the function might make a call to creat() or open() including O_CREAT and be successful.; The failed operation sets errno - and even if you set errno to zero before calling the library function, errno might be non-zero on return even though the function succeeded - and clearly indicated that it succeeded.  So testing just errno and not the function status can lead to 'errors' being detected when there are none.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 01:51
                                     |
| There should be some discussion of ways to implement this guideline.; For example, errno should be cited as a poor practice to emulate.  Returning integer error codes requires some registry of codes and their meanings (typically as message strings), but has the advantage that a common error printer can be conveniently used.  Generally, functions should be designed to return error indications, and "in-band" indicators like NULL or EOF are not recommended (although NULL is not so bad since the language supports it).  Per another rule, function error returns should always be tested.
Another approach is to use nested exception handling, which allows procedures to recover at convenient places in the computation.  Unfortunately, there is no standard specification for this in C, but there are several implementations available, generally using setjmp/longjmp.
                                        Posted by dagwyn at Apr 18, 2008 13:14
                                     |
| This has been totally rewritten since my March 20th visit.; The notes from then are no longer relevant.
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 00:45
                                     |

