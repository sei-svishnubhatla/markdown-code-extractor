Redundant testing by caller and by callee as a style of *defensive programming* is largely discredited in the C and C++ communities, the main problem being performance. The usual discipline in C and C++ is to require [validation](BB.-Definitions_87152273.html#BB.Definitions-validation) on only one side of each interface.
Requiring the caller to validate arguments can result in faster code because the caller may understand certain invariants that prevent invalid values from being passed. Requiring the callee to validate arguments allows the validation code to be encapsulated in one location, reducing the size of the code and making it more likely that these checks are performed in a consistent and correct fashion.
For safety and security reasons, this standard recommends that the called function validate its parameters. Validity checks allow the function to survive at least some forms of improper usage, enabling an application using the function to likewise survive. Validity checks can also simplify the task of determining the condition that caused the invalid parameter.
## Noncompliant Code Example
In this noncompliant code example, `setfile()` and `usefile()` do not validate their parameters. It is possible that an invalid file pointer can be used by the library, corrupting the library's internal state and exposing a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
``` c
/* Sets some internal state in the library */
extern int setfile(FILE *file);
/* Performs some action using the file passed earlier */
extern int usefile();
static FILE *myFile;
void setfile(FILE *file) {
    myFile = file;
}
void usefile(void) {
    /* Perform some action here */
}
```
The vulnerability can be more severe if the internal state references sensitive or system-critical data.
## Compliant Solution
Validating the function parameters and verifying the internal state leads to consistency of program execution and may eliminate potential vulnerabilities. In addition, implementing commit or rollback semantics (leaving program state unchanged on error) is a desirable practice for error safety.
``` c
/* Sets some internal state in the library */
extern errno_t setfile(FILE *file);
/* Performs some action using the file passed earlier */
extern errno_t usefile(void);
static FILE *myFile;
errno_t setfile(FILE *file) {
 if (file && !ferror(file) && !feof(file)) {
    myFile = file;
    return 0;
  }
  /* Error safety: leave myFile unchanged */
  return -1;
}
errno_t usefile(void) {
  if (!myFile) return -1;
    /*
     * Perform other checks if needed; return 
     * error condition.
     */
    /* Perform some action here */
    return 0;
}
```
## Risk Assessment
Failing to validate the parameters in library functions may result in an access violation or a data integrity violation. Such a scenario indicates a flaw in how the library is used by the calling code. However, the library itself may still be the vector by which the calling code's vulnerability is exploited.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| CodeSonar | 8.3p0 | LANG.STRUCT.UPD | Unchecked parameter dereference |
| Parasoft C/C++test | 2024.2 | CERT_C-API00-a | The validity of parameters must be checked inside each function |
| PC-lint Plus | 1.4 | 413, 613, 668 | Partially supported: reports use of null pointers including function parameters which are assumed to have the potential to be null |
| PVS-Studio | 7.35 | V781, V1111 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabilty) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC08-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | MSC08-CPP. Functions should validate their parameters | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-20, Insufficient input validation | Prior to 2018-01-12: CERT: |
| MITRE CWE | CWE-476 | Prior to 2018-01-12: |

## Bibliography

|  |  |
| ----|----|
| [Apple 2006] | Application Interfaces That Enhance Security |

------------------------------------------------------------------------
[](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151926)
## Comments:

|  |
| ----|
| I think you should use "extern functions" instead of "callable from outside functions" to be consistent with standard terminology.
                                        Posted by wlf@cert.org at Apr 19, 2007 08:10
                                     |
| I think setfile() should not always return 0; it should either be a void function or it should return an error indication (non-zero status) when it rejects the file.; Functions that always return zero are a hangover from the pre-void days of C.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 03:00
                                     |
| There are a couple of enforceable subrules trying to grow out of this rule. This rule is unenforceable because
    how is ROSE to identify a library function?
    What constitutes a valid parameter?
                                        Posted by svoboda at Jul 29, 2008 16:46
                                     |
| A suggestion regarding the error safety of the compliant solution (not related to this rule itself). A good design rule to strive for in all software is transaction (commit/rollback) semantics: a function either succeeds to achieve its specified effects, or it fails and has no observable effect on program state. In addition, unless INVALID_ARG is defined in one of the secure C library extensions, using a well-known errno value such as EINVAL might be more informative (although lumping the three distinct error conditions under the same error value would likely be problematic in practice). With this in mind, setfile() would be better implemented as follows:
errno_t setfile(FILE *file) {
 if (file && !ferror(file) && !feof(file)) {
    myFile = file;
    return 0;
  }
  /* no effects on error */
  return EINVAL;
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 06, 2010 13:01
\| \|
Should the definition of setfile() in the NCE have the "const" qualifier?
![](images/icons/contenttypes/comment_16.png) Posted by jimg at Dec 12, 2012 11:07
\| \|
Probably not, I've removed it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 14, 2012 11:30
\| \|
In the "compliant" version of usefile myFile may be evaluated without prior initalization.
`Change the example code from`
`static` `FILE` `*myFile;`
to
`static` `FILE` `*myFile = NULL;`
![](images/icons/contenttypes/comment_16.png) Posted by xypron at Jun 11, 2013 04:47
\| \|
Static variables are always zero-initialized, so the assignment is not strictly required.; Specifically, 6.7.9p10:
> 10 If an object that has automatic storage duration is not initialized explicitly, its value is indeterminate. If an object that has static or thread storage duration is not initialized explicitly, then:
>
> — if it has pointer type, it is initialized to a null pointer;
>
> — if it has arithmetic type, it is initialized to (positive or unsigned) zero;
>
> — if it is an aggregate, every member is initialized (recursively) according to these rules, and any padding is initialized to zero bits;
>
> — if it is a union, the ﬁrst named member is initialized (recursively) according to these rules, and any padding is initialized to zero bits;

![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 11, 2013 09:19
\| \|
Hy
There is a Java Rule MET00-J.
It seems to be te same aim.
Why here is a rec and not a rule ?
We may have the same recommandation level.
What do you think about that ?
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 21, 2018 03:37
\| \|
Guy:
As you might guess, API00-C predates;[MET00-J. Validate method arguments](https://wiki.sei.cmu.edu/confluence/display/java/MET00-J.+Validate+method+arguments) by several years. We often try to promote recommendations to rules if they qualify...see [Rules versus Recommendations](Rules%20versus%20Recommendations). So MET00-J does seem to be an attempt at promoting API00-C into a rule...note its list of exceptions, which could presumably apply to API00-C as well.
So to be consistent, either we should either promote API00-C to a rule, or demote MET00-J to a recommendation. I do have an opinion, but first I'm curious to hear yours?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 21, 2018 19:16
\| \|
Hi David ![](images/icons/emoticons/smile.svg)
Yes, we also could demote MET00-J to recommendation.
**As for me, I would; promote API00-C to rule**. For example, in SAFETY CRITICAL systems we may have API that are called from different kinds of  remote calls. It is important that the server side validate every data given by the callers.
More over, about reliability, parameters must be validated for defensive reasons
About security, we must not consider that  callers put valide parameters.
Hope to be clear
Jérôme
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 22, 2018 03:17
\| \|
Guy:
I agree with your recommendation of promoting API00-C to a rule. I will share this discussion with some other experts here at CERT, with the aim of converting this recommendation to a rule in a few days.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 25, 2018 20:59
\| \|
FWIW, I disagree with such a promotion;– there is no way to statically enforce this rule because there's no way to define what it means to "validate" arbitrary parameters, which makes this a low-value rule (IMHO) but a reasonable recommendation. What's more, I don't think every API **should** validate all of its parameters. For instance, given this function, what does it even **mean** to validate a parameter? 
``` java
int f(int a, int b) { return b - a; }
```
I could support this rule if it was restricted only to parameters of pointer type or a parameter value being used in pointer arithmetic, including array indexing. However, I don't see that rule covering anything that's not already covered under EXP, MEM, and ARR, so I'm not certain what value would be added.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 26, 2018 07:19
\| \|
Hi
The function given for instance should check for parameter's bounds; in order to insure that result will stay in the int ranges. As given, this function could produce bad results in some cases (ex : a near the min value of int and b near max value of int)
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 26, 2018 07:46
\| \|
That presumes the implementation-defined behavior is incorrect for the purposes of the function call. If you think reliance on implementation-defined behavior is objectively wrong, then you can easily devise an example using unsigned integers where the wrapping behavior is well-defined. You can use floating-point values where the expense of checking all the corner cases (infinities, NaNs, denormals, et al) is incredibly burdensome and non-trivial. There's no rule prohibiting the declaration of a parameter that's unused (which sometimes comes up when implementing runtime polymorphic dispatch through function pointers, for instance); how does one validate that parameter in that case?
Given that these situations don't expose vulnerabilities that aren't already covered by other rules, I don't see what value is added by promoting this to be a rule. As-written, it has more to do with coding style than it does vulnerability avoidance given the other rules already covering what happens when you;don't validate a parameter and use it.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 26, 2018 08:14
\| \|
Put a different way than Aaron, define "near" (as in "near the min value...near max value").; Your statement talks about "bad results", not bad inputs.  In Aaron's example, how do you validate a good value of a or b absolutely/objectively, since good input values depend on the operation and the value of the other parameter–in effect the result, not the parameter itself.  As Aaron says (or implies), if you are concerned that the result might be bad in his example ("bad" compared to the behavior you want), then you should have some error checking, but it would be defined on a case by case basis.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 26, 2018 08:31
\| \|
Put yet another way, I suppose you could argue that Aaron's example should follow INT32-C, and that would be "parameter validation".; But, then I think we're splitting hairs with regard to what the error checking/validation is working on–the parameters, or the operands, which in Aaron's example happen to be the same.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 26, 2018 08:41
\| \|
Aaron is correct in that this guideline cannot be enforced by automated static analysis tools, b/c they cannot (currently) know what constitutes validity. However, our conditions for a good rule permit a rule to be enforceable by manual analysis as well, and this guideline certainly can be enforced thusly.
If we made this a rule, we would also add the exceptions delineated in MET00-J. The first such exception addresses the "validation-by-caller" pattern...eg if the function's contract mandates that callers must only pass valid parameters for the sake of performance, then that function complies with the guideline.
This would apply to Guy's example. I would consider that function compliant if it documents that it does no validation, partially because what constitutes valid parameters is implementation-dependent.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 26, 2018 09:39
\| \|
If API00-C were promoted to a rule, we would also need an exception for pointers, because besides checking for NULL, there is no portable way to verify that a pointer is valid (eg, it points to not-freed memory, or within the bounds of an array).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 26, 2018 09:41
\| \|
> However, our conditions for a good rule permit a rule to be enforceable by manual analysis as well, and this guideline certainly can be enforced thusly.

My point is that this rule is not enforceable by manual analysis "as well";– it is *only* enforceable via manual analysis as it is currently written. Once you tighten the wording up to give it a chance at being machine enforceable, all you've really done is restate existing rules like "don't dereference a null pointer" and "check array bounds before doing array indexing."
Can you come up with a code example where following the guidance here would prevent a vulnerability that is not covered by any other existing rule? If so, then **that problem** should be turned into new rule because anything vulnerable to a parameter that's not been validated is equally as vulnerable to a global variable that's not been validated, or a TSS variable that's not been validated, or a lambda capture  (C++) that's not been validated, etc.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 26, 2018 09:54
\| \|
Aaron, I agree:The rest of our rules are meant to be comprehensive. If I could come up with a code example that violated API00-C but no other CERT C rule, I would consider that a gap in the other rules, and would need to add one. In that sense, API00-C is indeed superfluous as a rule. That said, we do have a few rules that are subsets of other rules.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 26, 2018 10:24
\| \|
If we agree that API00-C should remain a recommendation, we have to next decide if MET00-J should be demoted to a recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 26, 2018 10:25
\| \|
I agree for recommendation. We need to demote MET00-J for consistency.
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 26, 2018 10:50
\| \|
I don't know the Java side as well as I do the C and C++ side, but my intuition is that the Java rule should be a rec instead.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 26, 2018 13:04
\| \|
You have a good intuition, I think so ![](images/icons/emoticons/wink.svg)
We must have the same logic for Java (and every other language too).
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 27, 2018 02:09
\| \|
> My point is that this rule is not enforceable by manual analysis "as well";– it is *only*enforceable via manual analysis as it is currently written

I don't understand this sentence...can you elaborate?
My argument is that both API00-C and MET00-J are not enforceable by static analysis tools.  But MET00-J is enforceable by a skilled auditor, and doesn't require the auditor to examine the whole program...they can just examine the function and comments associated with the function. And API00-C would also be enforceable by an auditor if API00-C inherited the exceptions that are in MET00-J.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 27, 2018 09:50
\| \|
I think we're roughly on the same page with our rationale, but come to different conclusions.
I think API00-C and MET00-J are only enforceable via a skilled auditor who reads all of the source code. Comments are insufficient and dangerous to rely on because nothing says those comments are remotely true.
``` java
void f(int *ptr) {
  // Don't need to check that ptr isn't null because callers do that.
  *ptr = 12;
}
```
The comment gives the auditor a false sense of security; how do they know the callers all do that without looking at the call sites? Now, throw function pointers into the mix where f() is called through some function pointer and not directly;– the auditor has to look at all mentions of f() and not just calls.
I don't think this sort of thing qualifies as a rule – it requires an auditor to manually decide what should and should not be validated, confirming that something doesn't need validation can be extremely labor intensive, and it ultimately doesn't address the root cause of vulnerabilities (using invalid data in computations involved in a security context) because you can run into the same vulnerabilities by failing to validate global variables (for instance).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 27, 2018 10:25
\| \|
I argue that MET00-J qualifies as a rule because it can be enforced by an auditor. Being enforced by a SA tool is nice, but not a requirement for qualifying as a rule.
While I agree that comments can lie or be incorrect, they still serve an important purpose: to clarifying the developer's intention. Your code example complies with API00-C (and MET00-J), although it violates;[EXP34-C. Do not dereference null pointers](EXP34-C_%20Do%20not%20dereference%20null%20pointers).
In fact, EXP34-C is IME the hardest rule to manually enforce because of the problems you are citing with API00-C. I demonstrate most of these problems in [this video](https://www.youtube.com/watch?v=ECZZjvq9hZQ&list=PLSNlEg26NNpwagA8kj9WMMr9jg8awKqJF&index=11): 
So while API00-C & MET00-J are a PITA to enforce, and they flag code that already violates other rules, I still think they both qualify as rules themselves.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 27, 2018 10:56
\| \|
\>;While I agree that comments can lie or be incorrect, they still serve an important purpose: to clarifying the developer's intention.
It is my understanding that guidance that's based on an auditor trying to interpret a developer's intention do not qualify for rules. However, also I don't want to go around in circles on this any longer. I would find this to be a low-quality rule; my vote is to leave it alone in C and downgrade it to a recommendation in Java.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 27, 2018 12:13
\| \|
Finaly, i wonder if this recommendation is necessary.
It seems more a subject of architecture or design of API.
It is necessary to check incoming datas but that does not mean that each function has to validate his parameters.
What do you think about that ?
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jun 29, 2018 01:26
\| \|
I agree. This entire section (API) is geared towards architecture rather than coding itself. It has many recommendations but no rules.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 29, 2018 15:45
\|
