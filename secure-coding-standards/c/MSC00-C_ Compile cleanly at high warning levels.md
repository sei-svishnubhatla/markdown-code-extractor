Compile code using the highest warning level available for your compiler and eliminate warnings by modifying the code.
According to the C Standard, subclause 5.1.1.3 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> A conforming implementation shall produce at least one diagnostic message (identified in an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) manner) if a preprocessing translation unit or translation unit contains a violation of any syntax rule or constraint, even if the behavior is also explicitly specified as [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) or implementation-defined. Diagnostic messages need not be produced in other circumstances.

Assuming a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation), eliminating diagnostic messages will eliminate any syntactic or constraint violations.
If suitable source-code-checking tools are available, use them regularly.
Compilers can produce diagnostic messages for correct code, as is permitted by C. It is usually preferable to rewrite code to eliminate compiler warnings, but if the code is correct, it is sufficient to provide a comment explaining why the warning message does not apply. Some compilers provide ways to suppress warnings, such as suitably formatted comments or pragmas, which can be used sparingly when the programmer understands the implications of the warning but has good reason to use the flagged construct anyway.
Do not simply quiet warnings by adding type casts or other means. Instead, understand the reason for the warning and consider a better approach, such as using matching types and avoiding type casts whenever possible.
## Noncompliant Code Example (Windows)
Using the `default` warning specifier with  `#pragma warning `resets the behavior of a warning to its default value, which may not be the same as its previous behavior.  Programmers commonly, but incorrectly, use the `default` warning specifier to restore previous warning messages after a message is temporarily disabled.  
``` c
#pragma warning(disable:4705) 
#pragma warning(disable:4706) 
#pragma warning(disable:4707) 
/* Unnecessarily flagged code */
#pragma warning(default:4705) 
#pragma warning(default:4706) 
#pragma warning(default:4707) 
```
## Compliant Solution (Windows)
Instead of using the `default` warning specifier, the current state of the warnings should be saved and then restored after the unnecessarily flagged code.
``` c
#pragma warning(push) 
#pragma warning(disable:4705) 
#pragma warning(disable:4706) 
#pragma warning(disable:4707) 
/* Unnecessarily flagged code */
#pragma warning(pop) 
```
The `pragma warning(push) `stores the current warning state for every warning. The `pragma warning(pop)`pops the last warning state pushed onto the stack. Any changes made to the warning state between the push and pop are undone.
## Risk Assessment
Eliminating violations of syntax rules and other constraints can eliminate serious software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) that can lead to the execution of arbitrary code with the permissions of the vulnerable process.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC00-C | Medium | Probable | Medium | P8 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC00-C).
## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BUILD.WALLBUILD.WERROR | Not All Warnings Are EnabledWarnings Not Treated As Errors |
| PVS-Studio | 7.35 | V665 |  |
| SonarQube C/C++ Plugin | ;3.11 | S1762S973 | Warns when the default warning specifier is used with; #pragma warning. Requires documentation of #pragma uses |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC00-CPP. Compile cleanly at high warning levels |
| MITRE CWE | CWE-563, Unused variableCWE-570, Expression is always false
CWE-571, Expression is always true |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 5.1.1.3, "Diagnostics" |
| [Seacord 2013] | Chapter 9, "Recommended Practices" |
| [Sutter 2005] | Item 1 |

------------------------------------------------------------------------
[](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152198)
## Comments:

|  |
| ----|
| On many compilers, the highest warning levels produces diagnostic messages for perfectly legitimate, reasonable code, just because that code has a feature that worries the compiler, which isn't smart enough to figure out why the worry is unnecessary. This is legal: the C standard allows a compiler to produce a diagnostic for any reason it wants. This item should be worded as a guideline, not a requirement.
                                        Posted by  at Aug 31, 2006 18:13
                                     |
| This is already a recommendation.; This is indicated by the numbering system (items numbered 00-29 are recommendations) as well as the A designation which stands for "Advisory".  The numbering scheme is described at https://www.securecoding.cert.org/confluence/display/seccode/Identifiers in case you have further questions.
                                        Posted by rcs at Aug 31, 2006 19:03
                                     |
| Well, be it rule or recommendation, with some compilers it's still nonsense.
Consider gcc's warnings that the code would work differently if compiled as
C++ code or traditional K&R code, for example.
Also it's simply bad advise to kill warnings indiscriminately.  Certainly
one should make use of the compiler's warnings and study them carefully.
And it's good to have few warnings, of course.
But a too routine - and likely boring - warning cleanup can easily remove
the symptom of a bug instead of the bug, thus actually hiding the bug from
someone more experienced or more awake who could catch it.
I've seen warning cleanups introduce bugs too.
Sometimes it's good to leave a warning where it is [edit: as an alert that...] that a piece of code is
fragile.  "You touched this code, see that you don't break it" kind of thing.
Sometimes cleaning up a warning makes the code more fragile.  My pet complaint is otherwise unnecessary casts.  Casts short-circuit type checking, thus
opening the door for far more serious bugs to go undetected.  I wish C had
C++-style, less powerful casts.
                                        Posted by hbf at Apr 17, 2008 20:06
                                     |
| Should add "If lint or similar code-checking tools are available, use them regularly."
Should add "Some compiler provide ways to suppress warnings, e.g. suitably-formatted comments or #pragmas, which can be used sparingly when the programmer understands the implications of the warning but has good reason to use the flagged construct anyway."
I agree that there should be adivce to not simply patch up warnings (e.g. by adding typecasts), but rather to understand the reason for the warning and to consider a better approach (e.g. use matching types).; There should also be a general caution to use typecasts sparingly and only when there is no sensible alternative.
                                        Posted by dagwyn at Apr 18, 2008 13:29
                                     |
| > Do not simply quiet warnings, for example, by adding typecasts. Instead, understand the reason for the warning and to consider a better approach, for example, use matching types. Use typecasts sparingly, and only when there is no sensible alternative.
I believe this quote addresses your concern wrt suppressing warnings.
I would say the only good case for leaving a compiler warning 'unfixed' is if
    you completely understand why the compiler is complaining
    you are certain your code is good, and have explained why in a nearby comment
    there is no way to eliminate the warning without 'worsening' the code.
    the compiler does NOT allow you to suppress warnings automatically via #pragmas or some similar feature.
Basically the hurdle for allowing compiler warnings should be very high, because lots more people will compile the code than actually debug it; they don't want to wonder if the build failed.
And I feel your pain wrt typecasting. Look on the bright side...at least C now has C++'s const keyword 
                                        Posted by svoboda at Apr 21, 2008 15:59
                                     |
| Yes, the "do not simply quiet warnings" note covers it, except I just thinks this recommendation is worded too strongly.
Compile using "the highest warning level available", no way.; I've already mentioned warnings that do not indicate problems with the code.  This recommendation has an "Exceptions" section for that, but in this case the exception is the rule.  Or it can be, depending on the compiler.
Compile with high warning levels, certainly.  And use other tools, as Gwyn says.
Whether to leave warnings around depends on lots of things, among others whether you've inherited a project or are starting from scratch.  And what's this about "the" compiler?  If I switch compiler and the new one offers a lot of new warnings, am I suddenly obliged to patch up perfectly good code to shut them up?  In a living project with other problems to deal with, that's likely a low-priority task.
About leaving a warning unfixed, I might certainly do that if I didn't understand why the compiler was complaining - at least until I found someone who did
Yes, more people compile the code than debug it - so that's likely a reason to develop with a higher warning level than you distribute with. 
                                        Posted by hbf at Apr 24, 2008 13:44
                                     |
| I've been reviewing this rule but the title "Compile cleanly at high warning levels" and the overall description doesn't seem to quite fit together. The description is rather geared toward "how to deal with irrelevant/unwanted warning".There are only Windows specific NCCE/CCE in this rule. Those pair could be moved to Win category. In that case, the title would better be change to something like "Correctly use #pragma warning to control compiler warning" or "Understand the behaviour of #pragma warning".;
                                        Posted by masaki at Aug 27, 2014 01:33
                                     |
| Yes, I added those bits recently and my other idea was that this information could go into a Windows specific example.; Do you want to move it, or are you going to make me do all the work?  8^)
                                        Posted by rcs_mgr at Aug 27, 2014 11:17
                                     |

