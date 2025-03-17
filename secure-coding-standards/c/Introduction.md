-   [Scope](Scope)
-   [Audience](Audience)
-   [How this Coding Standard is Organized](How%20this%20Coding%20Standard%20is%20Organized)
-   [History](History)
-   [ISO/IEC TS 17961 C Secure Coding Rules](ISO_IEC%20TS%2017961%20C%20Secure%20Coding%20Rules)
-   [Tool Selection and Validation](Tool%20Selection%20and%20Validation)
-   [Taint Analysis](Taint%20Analysis)
-   [Rules versus Recommendations](Rules%20versus%20Recommendations)
-   [Conformance Testing](Conformance%20Testing)
-   [Development Process](Development%20Process)
-   [Usage](Usage)
-   [System Qualities](System%20Qualities)
-   [Automatically Generated Code](Automatically%20Generated%20Code)
-   [Government Regulations](Government%20Regulations)
-   [Acknowledgments](Acknowledgments)
This standard provides rules for secure coding in the C programming language. The goal of these rules and recommendations is to develop safe, reliable, and secure systems, for example by eliminating undefined behaviors that can lead to undefined program behaviors and exploitable vulnerabilities. Conformance to the coding rules defined in this standard are necessary (but not sufficient) to ensure the safety, reliability, and security of software systems developed in the C programming language. It is also necessary, for example, to have a safe and secure design. Safety-critical systems typically have stricter requirements than are imposed by this coding standard, for example requiring that all memory be statically allocated. However, the application of this coding standard will result in high-quality systems that are reliable, robust, and resistant to attack.
Each rule consists of a *title*, a *description*, and *noncompliant code examples* and *compliant solutions*, as well as other information as described in [How this Coding Standard is Organized](How%20this%20Coding%20Standard%20is%20Organized). The title is a concise, but sometimes imprecise, description of the rule. The description specifies the normative requirements of the rule. The noncompliant code examples are examples of code that would constitute a violation of the rule. The accompanying compliant solutions demonstrate equivalent code that does not violate the rule or any other rules in this coding standard.
A well-documented and enforceable coding standard is an essential element of coding in the C programming language. Coding standards encourage programmers to follow a uniform set of rules determined by the requirements of the project and organization rather than by the programmers’ individual preferences. Once established, these standards can be used as a metric to evaluate source code (using manual or automated processes).
CERT’s coding standards are being widely adopted by industry. Cisco Systems, Inc. announced its adoption of the CERT C Secure Coding Standard as a baseline programming standard in its product development in October 2011 at Cisco’s annual SecCon conference. Recently, Oracle has integrated all of CERT’s secure coding standards into its existing secure coding standards. This adoption is the most recent step of a long collaboration: CERT and Oracle previously worked together in authoring *The CERT Oracle Secure Coding Standard for Java* (Addison-Wesley, 2011).
This wiki contains ongoing updates of the standard between official published releases. If you are interested in contributing to the rules, create an account on the wiki and then request contributor privileges by sending a request to <info@sei.cmu.edu>.
The [Secure Coding eNewsletter](http://www.cert.org/secure-coding/publications/secure-coding-enewsletter.cfm) contains news from the CERT Secure Coding Initiative as well as summaries of recent updates to the standard rules. If you are interested in receiving updates directly, subscribe to the eNewsletter through [our website](http://cert.org/secure-coding/contact.cfm) or send a request to <u><info@sei.cmu.edu></u> . 
## Comments:

|  |
| ----|
| please don't use the phrase "resistant to attack" as justification for promoting good programming practices.; in fact, one could argue that the c programming language is rarely the language or the cause for software "insecurity".
                                        Posted by etkinsd@battelle.org at Jun 18, 2009 09:07
                                     |
| Since the C language is primarily focused on;efficiency, always has always will, and the primary systems language out there, I am not sure what you mean.  A safer sub setting of the language for a subset of applications that must sacrifice "good programming practices" in areas outside of those that are "resistant to attack" must be made.
                                        Posted by clayton_weimer@programmingsresearch.com at Jun 29, 2010 01:26
                                     |
| In my view, in the case of C language, it's the use made of it that cause security issues, not the language itself. I believe this is what is referred to the text, which focuses on the use of language to make the code "more secure" (resistant to attack).
                                        Posted by paioniu at Jul 30, 2013 02:28
                                     |

