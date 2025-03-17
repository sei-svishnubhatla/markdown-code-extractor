This coding standard consists of *rules* and *recommendations*. Rules are meant to provide normative requirements for code; recommendations are meant to provide guidance that, when followed, should improve the safety, reliability, and security of software systems. However, a violation of a recommendation does not necessarily indicate the presence of a defect in the code. Rules and recommendations are collectively referred to as *guidelines*.
## Rules
Rules must meet the following criteria:
1.  Violation of the guideline is likely to result in a defect that may adversely affect the safety, reliability, or security of a system, for example, by introducing a  [security flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) that may result in an exploitable [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
2.  The guideline does not rely on source code annotations or assumptions.
3.  Conformance to the guideline can be determined through automated analysis (either static or dynamic), formal methods, or manual inspection techniques.
## Recommendations
Recommendations are suggestions for improving code quality. Guidelines are defined to be recommendations when all of the following conditions are met:
1.  Application of a guideline is likely to improve the safety, reliability, or security of software systems.
2.  One or more of the requirements necessary for a guideline to be considered a rule cannot be met.
The set of recommendations that a particular development effort adopts depends on the requirements of the final software product. Projects with stricter requirements may decide to dedicate more resources to ensuring the safety, reliability, and security of a system and consequently are likely to adopt a broader set of recommendations.
## Attachments:
![](images/icons/bullet_blue.gif) [numbers.jpg](attachments/87152043/88018502.jpg) (image/jpeg)  
## Comments:

|  |
| ----|
| It seems to me that deciding what is a rule and what is a recommendation is a matter of policy.; This should be left to the developer, not dictated here.  This would be more in line with how tools like Lint operate (you can tell it to shut off certain rules, and it just gives a diagnosis rather than telling you that what you are doing is wrong.) 
What makes more sense is if you labeled each rule/recommendation instead by severity of the problem, much like a warning level in a compiler.  This would make it more amenable to current practice today.  I.e., some development policies demand that code be compiler warning free, or LINT-clean (with possible exceptions), etc.  What you want to is for code to be "CERT guideline compliant" to some level, and let development houses figure out what level they want to support.
                                        Posted by websnarf at Mar 31, 2008 00:43
                                     |
| In skimming through the rules/guidelines, I see that many of them amount to warning not to code a bug (meaning code that shouldn't be expected to "work" on any platform except by accident).; I think it would be better to segregate the "common bugs that the compiler might not diagnose" from "nonportable practices" from "risky practices".
                                        Posted by dagwyn at Apr 08, 2008 17:51
                                     |
| I'd like to see a recommendation#1 "don't be too slavish about all this,
use common sense".  The document as it stands focuses too much on what
a safe program looks like in isolation.  Too much focus on compliance
can harm the development process and thus the program in various ways.
Examples: Routinely shutting up warnings can mean removing the symptom
instead of the bug, preventing a more experienced programmer on the team
from noticing the bug.  Moving code around to fix some minor compliance
problem can make it harder to keep multiple releases in sync in source
control, and reduce the time spent do fix real problems.
                                        Posted by hbf at Apr 17, 2008 19:48
                                     |
| A lot of the rules and recommendations are special cases of "don't write buggy code", or maybe "write valid C programs with well-defined semantics".; Rules like "only free dynamically allocated memory."  For someone who is already routined at that and wants to follow this standard, it would be immensely useful if rules and recommendations which add something more are separated out from the rest.  Or if the rules are ordered from less to more "merely what the C standard says"-rules.  E.g. avoiding buffer overruns is something in between, since it's a common problem and merely derived from knowing the C language, not directly taken from the standard.
                                        Posted by hbf at Apr 18, 2008 06:39
                                     |
| As (originally) mentioned in comment Re: FIO00-C. Take care when creating format strings...
The management of guidelines as well as references to them from both within the Wiki #2 and outside #1 would be easier if their identifiers didn't imply an ordering within a category or necessarily even membership in it and the same identifier could be maintained regardless of changing a guideline from rule to recommendation or moving it from one section to another.
I propose changing the identification scheme to something like:
    C-#### for C
    CPP-#### for C++
    J-### for Java
with the #### part being unique and monotonically increasing (i.e., no number would ever be recycled, even after a given guideline has been eliminated).
 [1] Such as references to TMP00-A or TMP30-C on the VOID C Rules Implemented in Fortify SCA page.
 [2] Such as references to MEM00-A, OBJ32-C, or RES35-C in Evaluation of CERT Secure Coding Rules through Integration with Source Code Analysis Tools, none of which appears to exist on the Wiki.
                                        Posted by martinsebor at Feb 06, 2010 21:49
                                     |
| IMO, rules should be for things that if not followed, mean that your code is always broken, is undefined, or is unnecessarily relying on platform-specific behavior to work correctly. For example, I think FIO18-C. Never expect fwrite() to terminate the writing process at a null character should be a rule instead of a recommendation, since not heeding it means that your program will write a null byte and arbitrary data after it, that you didn't want or expect. Recommendations should be for things that if not followed, merely make the code harder to understand, easier for bugs to hide in, or more likely to be broken by an innocuous-seeming change. For example, I think DCL41-C. Do not declare variables inside a switch statement before the first case label should be a recommendation instead of a rule, since not heeding it is fine as long as you're sure to initialize the jumped-over variables in the cases before they're actually used.
                                        Posted by jcsible at Jun 30, 2020 16:24
                                     |
| There have been plenty of coding guidelines, the CERT set was the first to focus on security. As you might guess, changing our criteria for rules vs recommendations has been resolved for a long time.FIO18-C is a rec because it cannot be automatically determined if the contents written are intended to be null-terminated. Many recommendations, including this one, fail the rule criteria because enforcing them requires knowing the intent of the programmer.I'll address DCL41-C there since you left a comment there.
                                        Posted by svoboda at Jul 02, 2020 12:22
                                     |

