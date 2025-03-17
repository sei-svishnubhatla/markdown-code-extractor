The CERT C Secure Coding Standard was developed specifically for versions of the C programming language defined by
-   ISO/IEC 9899:2011 ISO/IEC, Programming Languages—C, 3rd ed. \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]
-   ISO/IEC 9899:2011/Cor.1:2012, Technical Corrigendum 1
Although the guidelines for this standard were developed for C11, they can also be applied to earlier versions of the C programming language, including C99. Variations between versions of the C Standard that would affect the proper application of these guidelines are noted where applicable.
Most guidelines have a noncompliant code example that is a C11-conforming program to ensure that the problem identified by the guideline is within the scope of the standard. However, the best solutions to secure coding problems are often platform specific. In many cases, this standard provides appropriate compliant solutions for both POSIX and Windows operating systems. Language and library extensions that have been published as ISO/IEC technical reports or technical specifications are frequently given precedence, such as those described by ISO/IEC TR 24731-2, *Extensions to the C Library—Part II: Dynamic Allocation Functions* \[ ISO/IEC TR 24731-2:2010 \]. In many cases, compliant solutions are also provided for specific platforms such as Linux or OpenBSD. Occasionally, interesting or illustrative implementation-specific behaviors are described.
## Rationale
A coding standard for the C programming language can create the highest value for the longest period of time by focusing on the C Standard (C11) and the relevant post- C11 technical reports.
The C Standard documents existing practice where possible. That is, most features must be tested in an  implementation before being included in the standard. The CERT C Coding Standard has a different purpose: to establish a set of best practices, which sometimes requires introducing new practices that may not be widely known or used when existing practices are inadequate. To put it a different way, the CERT C Coding Standard attempts to drive change rather than just document it.
For example, the optional but normative Annex K, “Bounds-Checking Interfaces,” introduced in C11, is gaining support but at present is implemented by only a few vendors. It introduces functions such as `memcpy_s()`, which serve the purpose of security by adding the destination buffer size to the API. A forward-looking document could not reasonably ignore these functions simply because they are not yet widely implemented. The base C Standard is more widely implemented than Annex K, but even if it were not, it is the direction in which the industry is moving. Developers of new C code, especially, need guidance that is usable, on and makes the best use of, the compilers and tools that are now being developed and are being supported into the future.
Some vendors have extensions to C, and some also have implemented only part of the C Standard before stopping development. Consequently, it is not possible to back up and discuss only C95, C90, or C99. The vendor support equation is too complicated to draw a line and say that a certain compiler supports exactly a certain standard. Whatever demarcation point is selected, different vendors are on opposite sides of it for different parts of the language. Supporting all possibilities would require testing the cross-product of each compiler with each language feature. Consequently, we have selected a demarcation point that is the most recent in time so that the rules and recommendations defined by the standard will be applicable for as long as possible. As a result of the variations in support, source-code portability is enhanced when the programmer uses only the features specified by C99. This is one of many trade-offs between security and portability inherent to C language programming.
The value of forward-looking information increases with time before it starts to decrease. The value of backward-looking information starts to decrease immediately.
For all of these reasons, the priority of this standard is to support new code development using C11 and the post-C11 technical reports that have not been incorporated into the C Standard. A close-second priority is supporting remediation of old code using C99 and the technical reports.
This coding standard does make contributions to support older compilers when these contributions can be significant and doing so does not compromise other priorities. The intent is not to capture all deviations from the standard but to capture only a few important ones.
## Issues Not Addressed
A number of issues are not addressed by this secure coding standard.
### Coding Style
Coding style issues are subjective, and it has proven impossible to develop a consensus on appropriate style guidelines. Consequently, the CERT C Secure Coding Standard does not require the enforcement of any particular coding style but only suggests that development organizations define or adopt style guidelines and apply these guidelines consistently. The easiest way to apply a coding style consistently is to use a code-formatting tool. Many interactive development environments (IDEs) provide such capabilities.
### Controversial Rules
In general, the CERT coding standards try to avoid the inclusion of controversial rules that lack a broad consensus.
## Comments:

|  |
| ----|
| This claim that there is more value in supporting C99 is a curious one that I don't see the logic in.; Future coding is trending towards C++ and other languages, and C99 has not had widespread adoption, even 8 years after its introduction (the two most important vendors: Microsoft and GNU have not adopted it).  If the standard instead focussed on C89, which C99 remains mostly backward compatible with, then this standard would be more valuable, in that it could be applied to nearly any application written in C (either today, or in the past.)
                                        Posted by websnarf at Mar 31, 2008 00:34
                                     |
| I think using the current standard as a basis is appropriate.
                                        Posted by dagwyn at Apr 11, 2008 13:30
                                     |
| TR 24731-2 is not yet finalized.; However, it is not as complex as, nor as controversial as, TR 24731-1.
                                        Posted by jonathan.leffler@gmail.com at Dec 19, 2008 00:57
                                     |
| I am surprised by the assertion in the first paragraph on this page that "because considerably more money and effort is devoted to developing new code than maintaining existing code." Several studies have shown the cost of software maintenance to far exceed that of its development. See for example, Hunt, B.; Turner, B.; McRitchie, K. Software Maintenance Implications on Cost and Schedule.
                                        Posted by martinsebor at Nov 30, 2009 21:33
                                     |
| Fair enough, I removed that assertion.
                                        Posted by rcs_mgr at Nov 30, 2009 22:18
                                     |
| We now need to expand the scope to include the emerging C1X standard.
                                        Posted by rcs_mgr at Nov 30, 2009 22:18
                                     |
| It's not true (or at least no longer true) that GNU has not adopted C99. gcc's C99 conformance is not perfect, but it's reasonably good:http://gcc.gnu.org/c99status.htmlNote that some of the features marked "Missing" are not actually required.There's also a web page tracking gcc support for C11:http://gcc.gnu.org/wiki/C11StatusLibrary support is, to some extent, a separate issue. gcc provides the compiler and;some of the library; most of the C standard library is provided by the OS (GNU libc on most Linux-based systems, the "native" library on others). 
                                        Posted by keith.s.thompson at Sep 12, 2013 15:04
                                     |
| This page lists the scope as both C11 and C99.; This version is really for C11, so I'm going to remove all the C99 bits.  This will now be covered under "Most of the material included in this standard can also be applied to earlier versions of the C programming language."
                                        Posted by rcs at Oct 04, 2013 10:35
                                     |

