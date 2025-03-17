The C23 Standard requires type specifiers and forbids implicit function declarations. The C90 Standard allows implicit typing of variables and functions. Consequently, some existing legacy code uses implicit typing. Some C compilers still support legacy code by allowing implicit typing, but it should not be used for new code. Such an [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) may choose to assume an implicit declaration and continue translation to support existing programs that used this feature.
## Noncompliant Code Example (Implicit `int`)
C no longer allows the absence of type specifiers in a declaration. The C Standard, 6.7.3 paragraph 2 \[ [ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024) \], states
> Except where the type is inferred (6.7.10), at least one type specifier shall be given in the declaration specifiers in each declaration, and in the specifier-qualifier list in each member declaration and type name.

This noncompliant code example omits the type specifier:
``` c
extern foo;
```
Some C [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) do not issue a diagnostic for the violation of this constraint. These nonconforming C translators continue to treat such declarations as implying the type `int`.
## Compliant Solution (Implicit `int`)
This compliant solution explicitly includes a type specifier:
``` c
extern int foo;
```
## Noncompliant Code Example (Implicit Function Declaration)
Implicit declaration of functions is not allowed; every function must be explicitly declared before it can be called. In C90, if a function is called without an explicit prototype, the compiler provides an implicit declaration.
The C90 Standard \[[ISO/IEC 9899:1990](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-1990)\] includes this requirement:
> If the expression that precedes the parenthesized argument list in a function call consists solely of an identifier, and if no declaration is visible for this identifier, the identifier is implicitly declared exactly as if, in the innermost block containing the function call, the declaration `extern int identifier();` appeared.

If a function declaration is not visible at the point at which a call to the function is made, C90-compliant platforms assume an implicit declaration of `extern int identifier();`.
This declaration implies that the function may take any number and type of arguments and return an `int`. However, to conform to the current C Standard, programmers must explicitly prototype every function before invoking it. An implementation that conforms to the C Standard may or may not perform implicit function declarations, but C does require a conforming implementation to issue a diagnostic if it encounters an undeclared function being used.
In this noncompliant code example, if `malloc()` is not declared, either explicitly or by including `stdlib.h`, a compiler that conforms only to C90 may implicitly declare `malloc()` as `int malloc()`. If the platform's size of `int` is 32 bits, but the size of pointers is 64 bits, the resulting pointer would likely be truncated as a result of the implicit declaration of `malloc()`, returning a 32-bit integer.
``` c
#include <stddef.h>
/* #include <stdlib.h> is missing */
int main(void) {
  for (size_t i = 0; i < 100; ++i) {
    /* int malloc() assumed */
    char *ptr = (char *)malloc(0x10000000);
    *ptr = 'a';
  }
  return 0;
}
```
### Implementation Details
When compiled with Microsoft Visual Studio 2013 for a 64-bit platform, this noncompliant code example will eventually cause an access violation when dereferencing `ptr` in the loop.
## Compliant Solution (Implicit Function Declaration)
This compliant solution declares `malloc()` by including the appropriate header file:
``` c
#include <stdlib.h>
int main(void) {
  for (size_t i = 0; i < 100; ++i) {
    char *ptr = (char *)malloc(0x10000000);
    *ptr = 'a';
  }
  return 0;
}
```
For more information on function declarations, see [DCL07-C. Include the appropriate type information in function declarators](DCL07-C_%20Include%20the%20appropriate%20type%20information%20in%20function%20declarators).
## Noncompliant Code Example (Implicit Return Type)
Do not declare a function with an implicit return type. For example, if a function returns a meaningful integer value, declare it as returning `int`. If it returns no meaningful value, declare it as returning `void`.
``` c
#include <limits.h>
#include <stdio.h>
foo(void) {
  return UINT_MAX;
}
int main(void) {
  long long int c = foo();
  printf("%lld\n", c);
  return 0;
}
```
Because the compiler assumes that `foo()` returns a value of type `int` for this noncompliant code example, `UINT_MAX` is incorrectly converted to `−1`.
## Compliant Solution (Implicit Return Type)
This compliant solution explicitly defines the return type of `foo()` as `unsigned int`. As a result, the function correctly returns ` ``UINT_MAX`` `.
``` c
#include <limits.h>
#include <stdio.h>
unsigned int foo(void) {
  return UINT_MAX;
}
int main(void) {
  long long int c = foo();
  printf("%lld\n", c);
  return 0;
}
```
## Risk Assessment
Because implicit declarations lead to less stringent type checking, they can introduce [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and erroneous behavior. Occurrences of an omitted type specifier in existing code are rare, and the consequences are generally minor, perhaps resulting in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL31-C | Low | Unlikely | Low |  P3  |  L3  |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | type-specifierfunction-return-typeimplicit-function-declarationundeclared-parameter | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL31 | Fully implemented |
| Clang | 3.9 | -Wimplicit-int |  |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISRA C 2012 Rule 8.1 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl31-c |  |
| ECLAIR | 1.2 | CC2.DCL31 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violations of this rule when the -Wimplicit and -Wreturn-type flags are used |
| Helix QAC | 2024.4 | C0434, C2050, C2051, C3335 | Fully implemented |
| Klocwork | 2024.4 | CWARN.IMPLICITINTMISRA.DECL.NO_TYPE
MISRA.FUNC.NOPROT.CALL
RETVOID.IMPLICIT | Fully implemented |
| LDRA tool suite | 9.7.1 | 24 D, 41 D, 20 S, 326 S, 496 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL31-a | All functions shall be declared before use |
| PC-lint Plus | 1.4 | 601, 718, 746, 808 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL31-C | Checks for:Types not explicitly specifiedImplicit function declarationRule fully covered. |
| PVS-Studio | 7.35 | V1031 |  |
| SonarQube C/C++ Plugin | 3.11 |  S819, S820  ; | Partially implemented; implicit return type not covered. |
| RuleChecker | 24.04 | type-specifierfunction-return-typeimplicit-function-declarationundeclared-parameter | Fully checked |
| TrustInSoft Analyzer | 1.38 | type specifier missing | Partially verified (exhaustively detects undefined behavior). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL07-C. Include the appropriate type information in function declarators | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Subprogram Signature Mismatch [OTR] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 8.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:1990] |  |
| [ISO/IEC 9899:2024] | Subclause 6.7.3, "Type Specifiers" |
| [Jones 2008] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152466) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152132)
## Comments:

|  |
| ----|
| In the automated detection section, it says "The EDG Front End to Compass/ROSE can detect violations of this rule." where it usually says "Compass/ROSE can detect violations of this rule." Does "The EDG Front End" have significant meaning in this rule? If not, it should be omitted.
                                        Posted by masaki at Dec 08, 2008 22:50
                                     |
| I agree with Masaki's comment here.  David?
                                        Posted by rcs_mgr at Dec 10, 2008 08:56
                                     |
| Fixed.
Geeky Details: ROSE caught violations of this rule without any rules being written for it. The EDG frontend, which is part of ROSE, was responsible for issuing the warning. The 'rose-gcc' tag is my standard way of identifying rules detected by the EDG frontend.
                                        Posted by svoboda at Dec 16, 2008 14:06
                                     |
| While the assertion
The C99 standard requires type identifiers and forbids implicit function declarations. After issuing the diagnostic, an implementation may choose to assume an implicit declaration and continue translation to support existing programs that used this feature.
is correct, it applies to all ill-formed programs in general. It seems that there ought to be a single blanket requirement for all programs to be well-formed in order to comply with this standard. Otherwise the set of rules covering all possible ill-formed programs is unbounded.
Incidentally, I came across this page while looking for a rule requiring that auto variables be initialized before they are used (in order to avoid undefined behavior described in bullet 10  of Appendix J). If there isn't one yet there ought to be.
                                        Posted by martinsebor at Jan 07, 2010 21:02
                                     |
| I don't know of a rule specifying that a program must be well-formed. We do have rules to make compilers stricter: MSC00-C. Compile cleanly at high warning levels, for instance.
In general, we avoid specifying rules that compilers routinely catch. In order to be flagged by one of these rules, we generally require that a NCCE pass at least one major compiler...if all compilers issue at least a warning, we don't permit a bad piece of code to serve as a NCCE.
Also, I believe you are looking for EXP33-C. Do not reference uninitialized memory.
                                        Posted by svoboda at Jan 08, 2010 09:50
                                     |
| Thanks for the pointer to EXP33-C!
Regarding well-formedness, what I had in mind was more than another rule. Rather, what I was referring to was the set of fundamental prerequisites and assumptions that all these rules take for granted. One such assumption is stated in the Scope section: it is that the program be written in C99 (and not, for example, in Objective C, C++, or even K&R C). If a program isn't written in C99 (or its superset), this document cannot very well apply.
OTOH, I see no harm in highlighting commonly accepted deviations from C99 (such as omitting the type in an object declaration). It just seems that rules covering such deviations don't really fit in with rules intended to apply to C99 conforming programs. I suppose I would feel more comfortable if they were listed in a section of their own (e.g., Obsolescent Features or something like that).
                                        Posted by martinsebor at Jan 08, 2010 13:50
                                     |
| New sections are possible but problematic.  First, there must be enough guidelines to justify a new section (more than a few).  Second, we'll need to move existing guidelines to the new section which means that the unique guideline IDs (which find there way into tools and other documents) will end up changing.
In this particular case, I think we should also consider where a possibly non-expert user is likely to look for a given guideline.  Presumably, someone who might benefit from this rule would be unaware that implicit function declarations are not allowed in C99.
Instead, I think the solution may be to state in the introduction to this and similar guidelines that  "Programs which violate this recommendation are ill-formed with respect to the C99 standard.  We could also create a list of these someone in the introductory material.  I think we already have a list of guidelines which do not apply when the the c source code is "machine-generated, machine-maintained".
                                        Posted by rcs at Jan 09, 2010 14:34
                                     |
| Now that a year has passed, I've sort of changed my mind about this.  Now I think it would be interesting to know which guidelines can be diagnosed by EDG.  I would put this on a separate line (that is, treat EDG like any other analyzer).
                                        Posted by rcs at Jan 09, 2010 14:39
                                     |
| Understood. I like your idea of collecting references to all these rules in table somewhere (e.g., in the appendix).
                                        Posted by martinsebor at Jan 09, 2010 17:01
                                     |
| This rule can be satisfied by either a forward declaration of an identifier or a definition. What about a practice specifically recommending the former. I.e., one that would make this example non-compliant:
int i = 0;
int g(void) { return i; }

and required that each extern identifier be declared in a single header before it can be used or before it's defined. The goal of this practice is to prevent the risk of specifying multiple incompatible declarations of the same indentifier (such as UB [39](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_39)).
``` java
/* header.h */
extern int i;
extern int g(void);
/* ... */
int i = 0;
int g(void) { return i; }
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Oct 24, 2010 18:18
\| \|
I think UB39 is covered by [DCL36-C. Do not declare an identifier with conflicting linkage classifications](DCL36-C_%20Do%20not%20declare%20an%20identifier%20with%20conflicting%20linkage%20classifications)
Your suggestion is a good coding practice that would address both that rule and this one. So we could suggest it as a compliant solution. I don't think we could mandate it as a secure coding rule, since it is possible to code securely without using .h files at all (eg your program is one .c file).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 25, 2010 12:24
\| \|
Since Kona I have been thinking we should have a rule / recommendation not to use obsolescent features.
This was prompted by the response to DR #400:
Add to subsection 7.31.12 a new paragraph (paragraph 2):
▪Invoking realloc with a size argument equal to zero is an obsolescent feature.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 03, 2012 08:45
\| \|
We already have;[MSC34-C. Do not use deprecated or obsolescent functions](https://www.securecoding.cert.org/confluence/display/seccode/MSC34-C.+Do+not+use+deprecated+or+obsolescent+functions). Perhaps we should just add a NCCE based on DR400 to that rule?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 07, 2012 08:55
\| \|
"obsolescent functions" is a term we made up for a list of functions we identified for which better alternative functions existed.; We might need a different word to avoid confusion with "obsolescent features" from the C standard.
if we just modify a rule for DR400, it should be in memory management somewhere.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 07, 2012 09:05
\| \|
How about 'obsolete'? ;Isn't that a more clear, succinct way to say 'obsolescent'?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 08, 2012 08:33
\| \|
ok, i made that change. that rule needs a ton of work, and that wasn't even the rule i was talking about.; 8^(
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 08, 2012 09:19
\| \|
According to the dictionary...
> things that are no longer used or needed are obsolete; things that are becoming obsolete are obsolescent;

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at May 08, 2012 10:57
\| \|
i think obsolete is the right word.; we want to say it is, not that it's heading that way.  also, this further differentiates from the C standard ""obsolescent features" which has more the meaning of heading that way.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 08, 2012 14:05
\| \|
I understand the intent of this sentence:
The old C90 standard, which is no longer in force, did allow such implicit typing.
But it seems overly strong.; There are presumably lots of people still using C90 conforming compilers, so for them it is in force.
We should probably explain the history of the C standard once in the scope section, to provide context.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 09, 2013 10:05
\| \|
I happened to see a non-compliant code example in SquidGuard, which was discussed on OpenBSD ports mailing list.
<http://marc.info/?t=137632761100002&r=1&w=2>
;
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Aug 14, 2013 01:31
\| \|
Indeed. This seems to be a particular hazard for 64-bit platforms. It doesn't occur on 32-bit platforms because it implicitly converts pointers to ints, which are the same size on 32-bit platforms but different sizes on 64-bit platforms.
There is a long discussion in the [MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](MEM02-C_%20Immediately%20cast%20the%20result%20of%20a%20memory%20allocation%20function%20call%20into%20a%20pointer%20to%20the%20allocated%20type)comments about this (people thought it had to do with casting the return value of malloc()).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 14, 2013 10:06
\|
