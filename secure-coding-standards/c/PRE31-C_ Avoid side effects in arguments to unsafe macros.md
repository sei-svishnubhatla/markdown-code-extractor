An [unsafe function-like macro](BB.-Definitions_87152273.html#BB.Definitions-unsafefunction-likemacro) is one whose expansion results in evaluating one of its parameters more than once or not at all. Never invoke an unsafe macro with arguments containing an assignment, increment, decrement, volatile access, input/output, or other expressions with side effects (including function calls, which may cause side effects).
The documentation for unsafe macros should warn against invoking them with arguments with side effects, but the responsibility is on the programmer using the macro. Because of the risks associated with their use, it is recommended that the creation of unsafe function-like macros be avoided. (See [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros).)
This rule is similar to [EXP44-C. Do not rely on side effects in operands to sizeof, \_Alignof, or \_Generic](EXP44-C_%20Do%20not%20rely%20on%20side%20effects%20in%20operands%20to%20sizeof,%20_Alignof,%20or%20_Generic).
## Noncompliant Code Example
One problem with unsafe macros is [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) on macro arguments, as shown by this noncompliant code example:
``` c
#define ABS(x) (((x) < 0) ? -(x) : (x))
void func(int n) {
  /* Validate that n is within the desired range */
  int m = ABS(++n);
  /* ... */
}
```
The invocation of the `ABS()` macro in this example expands to
``` c
m = (((++n) < 0) ? -(++n) : (++n));
```
The resulting code is well defined but causes `n` to be incremented twice rather than once.
## Compliant Solution
In this compliant solution, the increment operation `++n` is performed before the call to the unsafe macro.
``` c
#define ABS(x) (((x) < 0) ? -(x) : (x)) /* UNSAFE */
void func(int n) {
  /* Validate that n is within the desired range */
  ++n;
  int m = ABS(n);
  /* ... */
}
```
Note the comment warning programmers that the macro is unsafe. The macro can also be renamed `ABS_UNSAFE()` to make it clear that the macro is unsafe. This compliant solution, like all the compliant solutions for this rule, has undefined behavior if the argument to `ABS()` is equal to the minimum (most negative) value for the signed integer type. (See [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow) for more information.)
## Compliant Solution
This compliant solution follows the guidance of [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros) by defining an inline function `iabs()` to replace the `ABS()` macro. Unlike the `ABS()` macro, which operates on operands of any type, the `iabs()` function will truncate arguments of types wider than `int` whose value is not in range of the latter type.
``` c
#include <complex.h>
#include <math.h>
static inline int iabs(int x) {
  return (((x) < 0) ? -(x) : (x));
}
void func(int n) {
  /* Validate that n is within the desired range */
int m = iabs(++n);
  /* ... */
}
```
## Compliant Solution
A more flexible compliant solution is to declare the `ABS()` macro using a `_Generic` selection. To support all arithmetic data types, this solution also makes use of inline functions to compute integer absolute values. (See [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros) and [PRE12-C. Do not define unsafe macros](PRE12-C_%20Do%20not%20define%20unsafe%20macros).)
According to the C Standard, 6.5.2.1, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\]:
> The controlling expression of a generic selection is not evaluated. If a generic selection has a generic association with a type name that is compatible with the type of the controlling expression, then the result expression of the generic selection is the expression in that generic association. Otherwise, the result expression of the generic selection is the expression in the `default` generic association. None of the expressions from any other generic association of the generic selection is evaluated. 

Because the expression is not evaluated as part of the generic selection, the use of a macro in this solution is guaranteed to evaluate the macro parameter `v` only once.
``` c
#include <complex.h>
#include <math.h>
static inline long long llabs(long long v) {
  return v < 0 ? -v : v;
}
static inline long labs(long v) {
  return v < 0 ? -v : v;
}
static inline int iabs(int v) {
  return v < 0 ? -v : v;
}
static inline int sabs(short v) {
  return v < 0 ? -v : v;
}
static inline int scabs(signed char v) {
  return v < 0 ? -v : v;
}
#define ABS(v)  _Generic(v, signed char : scabs, \
                            short : sabs, \
                            int : iabs, \
                            long : labs, \
                            long long : llabs, \
                            float : fabsf, \
                            double : fabs, \
                            long double : fabsl, \
                            double complex : cabs, \
                            float complex : cabsf, \
                            long double complex : cabsl)(v)
void func(int n) {
  /* Validate that n is within the desired range */
  int m = ABS(++n);
  /* ... */
}
```
Generic selections were introduced in C11 and are not available in C99 and earlier editions of the C Standard.
## Compliant Solution (GCC)
GCC's [\_\_typeof](http://gcc.gnu.org/onlinedocs/gcc/Typeof.html) extension makes it possible to declare and assign the value of the macro operand to a temporary of the same type and perform the computation on the temporary, consequently guaranteeing that the operand will be evaluated exactly once. Another GCC extension, known as [statement expression](http://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html), makes it possible for the block statement to appear where an expression is expected:
``` c
#define ABS(x) __extension__ ({ __typeof (x) tmp = x; \
                    tmp < 0 ? -tmp : tmp; })
```
Note that relying on such extensions makes code nonportable and violates [MSC14-C. Do not introduce unnecessary platform dependencies](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies).
## Noncompliant Code Example (`assert()`)
The `assert()` macro is a convenient mechanism for incorporating diagnostic tests in code. (See [MSC11-C. Incorporate diagnostic tests using assertions](MSC11-C_%20Incorporate%20diagnostic%20tests%20using%20assertions).) Expressions used as arguments to the standard `assert()` macro should not have side effects. The behavior of the `assert()` macro depends on the definition of the object-like macro `NDEBUG`. If the macro `NDEBUG` is undefined, the `assert()` macro is defined to evaluate its expression argument and, if the result of the expression compares equal to 0, call the `abort()` function. If `NDEBUG` is defined, `assert` is defined to expand to `((void)0)`. Consequently, the expression in the assertion is not evaluated, and no side effects it may have had otherwise take place in non-debugging executions of the code.
This noncompliant code example includes an `assert()` macro containing an expression (`index++`) that has a side effect:
``` c
#include <assert.h>
#include <stddef.h>
void process(size_t index) {
  assert(index++ > 0); /* Side effect */
  /* ... */
}
```
## Compliant Solution (`assert()`)
This compliant solution avoids the possibility of side effects in assertions by moving the expression containing the side effect outside of the `assert()` macro.
``` c
#include <assert.h>
#include <stddef.h>
void process(size_t index) {
  assert(index > 0); /* No side effect */
  ++index;
  /* ... */
}
```
## Exceptions
**PRE31-C-EX1:** An exception can be made for invoking an [unsafe macro](BB.-Definitions_87152273.html#BB.Definitions-unsafefunction-likemacro) with a function call argument provided that the function has no [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect). However, it is easy to forget about obscure side effects that a function might have, especially library functions for which source code is not available; even changing `errno` is a side effect. Unless the function is user-written and does nothing but perform a computation and return its result without calling any other functions, it is likely that many developers will forget about some side effect. Consequently, this exception must be used with great care.
## Risk Assessment
Invoking an unsafe macro with an argument that has side effects may cause those side effects to occur more than once. This practice can lead to [unexpected program behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE31-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | expanded-side-effect-multipliedexpanded-side-effect-not-evaluated
side-effect-not-expanded | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE31 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.PREPROC.FUNCMACROLANG.STRUCT.SE.DEC
LANG.STRUCT.SE.INC | Function-Like MacroSide Effects in Expression with Decrement
Side Effects in Expression with Increment |
| Coverity | 2017.07 | ASSERT_SIDE_EFFECTS | Partially implementedCan detect the specific instance where assertion contains an operation/function call that may have a side effect |
| Cppcheck Premium; | 24.11.0 | premium-cert-pre31-c |  |
| ECLAIR | 1.2 | CC2.EXP31CC2.PRE31 | Fully implemented |
| Helix QAC | 2024.4 | C3462,;C3463, C3464,C3465,C3466,C3467C++3225, C++3226, C++3227, C++3228, C++3229  | Fully implemented |
| Klocwork | 2024.4 | PORTING.VAR.EFFECTS | Fully implemented |
| LDRA tool suite | 9.7.1 | 9 S, 562 S, 572 S, 35 D, 1 Q | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE31-bCERT_C-PRE31-c
CERT_C-PRE31-d | Assertions should not contain assignments, increment, or decrement operatorsAssertions should not contain function calls nor function-like macro calls
Avoid side effects in arguments to unsafe macros |
| PC-lint Plus | 1.4 | 666, 2666 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule PRE31-C | Checks for side effect in arguments to unsafe macro (rule partially covered) |
| RuleChecker | 24.04 | expanded-side-effect-multipliedexpanded-side-effect-not-evaluated
side-effect-not-expanded | Partially checked |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|

## Bibliography

|  |  |
| ----|----|
| [Dewhurst 2002] | Gotcha #28, "Side Effects in Assertions" |
| [ISO/IEC 9899:2024] | Subclause 6.5.2.1, "Generic Selection"; |
| [Plum 1985] | Rule 1-11 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152465) [](../c/Rule%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152331)
## Comments:

|  |
| ----|
| I have no arguments with this as a rule. But I must point out that enforceability of macro-related rules is very difficult for all software we use to write rule checkers. Moreover, there is significant overlap between this rule and EXP30-C (depending on order of evaluation between sequence points.)
In the noncompliant example, the expanded macro (which is normally all Fortify or Rose will ever see) yields an expression with three invocations of ++n.  Multiple instances of an increment or decrement of a variable, or of an assignment to a variable within one expression seems like a violation of EXP30-C, which our checkers should be easily able to handle.
The upshot being than any unsafe macro containing an expression with side effects will yield an expression that violates EXP30-C, which our checkers can catch, even if they can't identify that the unsafe macro is to blame.
                                        Posted by svoboda at Mar 12, 2008 15:08
                                     |
| From comp.lang.c:
These are all the kinds of side effects:
1 object modification
2 volatile access
3 file write
4 function call that results in one or more of the previous three.
Also, it should be OK to invoke a function in an unsafe macro, provided the function call has no side effects, yes?
                                        Posted by rcs at Apr 01, 2008 10:03
                                     |
| (1); The last two sentences in the first paragraph ("Any input or output ...") seem to be versions of what should have been a single sentence.
(2) In the interface documentation describing the macro, or in case that doesn't exist, in a comment attached to the macro definition, a rule should be to flag the macro as "UNSAFE", as a warning to programmers using the macro.  E.g.
#define ABS(a) ((a) <0?-(a) :(a) ) // UNSAFE
That doesn't need to be a separate rule, but should be mentioned here.
                                        Posted by dagwyn at Apr 15, 2008 11:30
                                     |
| fixed and fixed
                                        Posted by svoboda at Apr 15, 2008 12:21
                                     |
| Macros that never evaluate their argument, or sometimes evaluate their arg, sometimes not, are also unsafe, since the programmer generally expects macro args to evaluate once.
Added this info to 1st paragraph, and added link to EXP39-C, which deals with assert, the archetypal example.
                                        Posted by svoboda at Apr 17, 2008 10:55
                                     |
| ROSE cannot enforce this rule, because it can not identify usage of a macro (though it can identify macro definitions). Besides, violation of this rule will generally cause a violation of other rules, usually EXP30-C.
                                        Posted by svoboda at May 27, 2008 13:36
                                     |
| This rule effectively requires users to inspect the definition of every macro before using it (and inspect the declaration of every function to make sure it's not masked by an unsafe macro). I have a feeling that might be too much to expect.
I would like to see a guideline to avoid writing unsafe macros (PRE00-C. Prefer inline or static functions to function-like macros notwithstanding).
Also, wouldn't Avoid side-effects in arguments to unsafe macros be a better name for this rule (more consistent with EXP31-C. Avoid side effects in assertions)?
                                        Posted by martinsebor at Jan 19, 2010 20:50
                                     |
| I agree that writing unsafe macros is the real problem, but what is wrong with PRE00-C. Prefer inline or static functions to function-like macros?  Is it too strong?  The first noncompliant code example involves passing an expression that contains side effects.  
I also thinking that having a static analysis tool flag every macro is a non-starter, which is why PRE00-C is a recommendation.  
I recently used PCLINT to uncover the following problem:
uint32_t _x = g_htonl(time(NULL)); 

`g_htonl()` is a GLib unsafe byte order macro that converts a 32-bit integer value from host to network byte order (but you probably already knew this).
So anyway there are some tools that can help enforce this, or you can dump your preprocessor output to a file and look for nasty surprises.
I sort of agree with your title change. I sort of recall that David Keaton preferred this title, but it may only have been to try to use normal programming speak instead of standardese, which is probably a lost cause at this point and possibly counter-productive. We should check with him about changing.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 20, 2010 16:44
\| \|
PRE00-C is great as far as it goes, but it does allow for 5 classes of exceptions. Since there are valid uses for function-like macros even in new code, a guideline for how to write them safely is called for.
The `g_htonl()` macro problem is exacerbated by the fact that its [documentation](http://library.gnome.org/devel/glib/stable/glib-Byte-Order-Macros.html#g-ntohl) doesn't mention that its argument is evaluated more than once. This IMO, underscores the need for a guideline discouraging the coding of such macros. There are efficient ways to do it without evaluating the argument more than once, either by relying on language extensions (such as gcc's [Statements and Declarations In Expressions](http://gcc.gnu.org/onlinedocs/gcc-4.4.2/gcc/Statement-Exprs.html#Statement-Exprs) ) or by introducing a \[possibly inline\] function (such as OpenSolaris [`htonl()`](http://src.opensolaris.org/source/xref/onnv/onnv-gate/usr/src/uts/intel/asm/byteorder.h#66)), so the burden to do the right thing should be on the implementer rather than on the user (although users should be aware of how to avoid getting bitten by badly written macros as well, which is where PRE31-C comes in).
I know little about the internals of static analysis tools but I would expect the better ones to be able to examine the definitions of macros and flag violations of the guideline I'm proposing even more effectively than is possible after preprocessing.
I'll wait for you to let me know how to proceed with the title change after you get feedback from David.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 20, 2010 20:46
\| \|
OK, I'm convinced. Please go ahead and draft a new guideline for review.
Thanks.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 21, 2010 06:57
\| \|
Okay, I'll work on it. Btw., I note that you've already renamed the rule as I suggested – thanks!
------------------------------------------------------------------------
I've added [PRE12-C. Do not define unsafe macros](PRE12-C_%20Do%20not%20define%20unsafe%20macros).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 04, 2010 20:56
\| \|
The Remediation Cost of medium seems rather high given the relative simplicity of the available solutions:
-   replace definitions of unsafe macros with those of inline functions (or compiler extensions), or
-   provide inline wrapper functions for unsafe macros and replace invocations of such macros with those to the wrapper, or
The first approach is by far easier to implement but it relies on the ability to modify the source code of the macro which may not be possible when the macro is defined in a third party library.
The second approach is more involved but can be automated via a simple script.
I changed the Cost to low and adjusted Priority and Level accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Sep 05, 2011 18:02
\| \|
I just noticed that the last paragraph in the first NCCE and the comment in the code are wrong. The `ABS()` macro has well-defined semantics and does not depend on the order of evaluation of operands between two consecutive sequence points. (As specified in 6.15.5, p4, there is a sequence point between the evaluation of the first operand of the conditional expression and the evaluation of the second or third operand (whichever is evaluated)).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 07, 2013 15:47
\| \|
Fixed, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 08, 2013 10:04
\| \|
Now that [PRE12-C](PRE12-C_%20Do%20not%20define%20unsafe%20macros) exists, I think the second and third compliant solutions should be removed, since they strictly speaking don't follow the requirement to
> Never invoke an unsafe macro with arguments containing an assignment, increment, ...

but rather change the macro definition to be safe.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 08, 2013 12:32
\| \|
I added a reference to PRE12-C to the 2nd CS. We do like our rules (of which this is one) to exist somewhat independently of our recommendations (PRE12-C, for instance), so a little redundancy is OK.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 08, 2013 15:48
\| \|
I think that the typeof example violates [DCL37-C. Do not declare or define a reserved identifier](DCL37-C_%20Do%20not%20declare%20or%20define%20a%20reserved%20identifier).; The example declares a variable named "\_\_tmp" that starts with two underscores and DCL37-C indicates that "\[a\]ll identifiers that begin with an underscore and ... another underscore are always reserved for any use."
![](images/icons/contenttypes/comment_16.png) Posted by kraai at Jun 11, 2013 11:34
\| \|
You're right. Furthermore, this code is...passable. I wouldn't call it 'good', but it is the best you can do under some circumstances. I've added an exception to DCL37-C to allow this example, and also overhauled this example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 12, 2013 15:04
\| \|
Perhaps this is a terrible idea, but you could use the \_\_LINE\_\_ predefined macro to generate a likely-unique identifier without requiring the identifier to stray into the reserved namespace.
``` java
#define DEF_IDENT3(X, Y)  X##Y
#define DEF_IDENT2(X, Y) DEF_IDENT3(X, Y)
#define DEF_IDENT(X) DEF_IDENT2(X, __LINE__)
;
int DEF_IDENT(Test);
int DEF_IDENT(Test);
```
That will create two identifiers named TestXXX where the XXX is whatever line number the declaration is on.  It strays quite a bit from the goal of this guideline, but then again, there's a whole lot of words talking about why not to do what's being done already.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 24, 2013 10:39
\| \|
I think we should add a type generic solution because this is a C11 standard.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Nov 11, 2013 09:46
\| \|
Honestly, I'm not certain that'd be worth the effort.; Off the top of my head, it would be:
``` java
#include <complex.h>
#include <math.h>
static long long llabs(long long v) {
  return v < 0 ? -v : v;
}
static long labs(long v) {
  return v < 0 ? -v : v;
}
static int iabs(int v) {
  return v < 0 ? -v : v;
}
static short sabs(short v) {
  return v < 0 ? -v : v;
}
static signed char scabs(signed char v) {
  return v < 0 ? -v : v;
}
#define ABS(v)  _Generic(v, signed char : scabs \
                            short : sabs \
                            int : iabs \
                            long : labs \
                            long long : llabs \
                            float : fabsf \
                            double : fabs \
                            long double : fabsl \
                            double complex : cabs \
                            float complex : cabsf \
                            long double complex : cabsl)
```
That's a pretty big mess of code to write for a generic abs function, and would require updating were another type to come along for which abs could be well-defined.  At least with the macro, anything for which \< and - are defined operators will suffice.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 10:31
\| \|
i don't know, I think it is beautiful.; 8^)
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Nov 11, 2013 10:34
\| \|
Hmm, you could argue that it's safer since any usage of the ABS macro based on \_Generic for a type not listed would generate a compile error (since there's no default selection), which would give the programmer better diagnostics if used with a type not listed, unlike the current macro.; An immediate case that springs to mind are pointers...
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 10:43
\| \|
Shouldn't there be a (v) after the_Generic(v, generic assoc list)?
**;** 
![](images/icons/contenttypes/comment_16.png) Posted by eaevans at Nov 11, 2013 10:47
\| \|
Yes, there should be!; Good catch.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 10:48
\| \|
The more I think about it, the more I like it.; I will add it as an additional compliant solution.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 10:49
\| \|
A simplified rule could be "a function-like macro can only have (a) constants and (b) identifiers as parameters. That way, the whole notion of unsafe macros can be buried in motivation and explanation part. With modern compilers, I would expect no performance/footprint penalty.
![](images/icons/contenttypes/comment_16.png) Posted by arkhas at Aug 28, 2015 15:00
\|
