Two or more incompatible declarations of the same function or object must not appear in the same program because they result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The C Standard, 6.2.7, mentions that two types may be distinct yet compatible and addresses precisely when two distinct types are compatible.
The C Standard identifies four situations in which [undefined behavior (UB)](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) may arise as a result of incompatible declarations of the same function or object:

| UB | Description | Code |
| ----|----|----|
| 14 | Two declarations of the same object or function specify types that are not compatible (6.2.7). | All noncompliant code in this guideline |
| 30 | Two identifiers differ only in nonsignificant characters (6.4.2.1). | Excessively Long Identifiers |
| 36 | An object has its stored value accessed other than by an lvalue of an allowable type (6.5). | Incompatible Object DeclarationsIncompatible Array Declarations |
| 37 | A function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function (6.5.2.2). | Incompatible Function Declarations; 
Excessively Long Identifiers |

Although the effect of two incompatible declarations simply appearing in the same program may be benign on most [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation), the effects of invoking a function through an expression whose type is incompatible with the function definition are typically catastrophic. Similarly, the effects of accessing an object using an [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) of a type that is incompatible with the object definition may range from unintended information exposure to memory overwrite to a hardware trap.
## Noncompliant Code Example (Incompatible Object Declarations)
In this noncompliant code example, the variable `i` is declared to have type `int` in file `a.c` but defined to be of type `short` in file `b.c`. The declarations are incompatible, resulting in [undefined behavior 14](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_14). Furthermore, accessing the object using an [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) of an incompatible type, as shown in function `f()`, is [undefined behavior 36](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_36) with possible observable results ranging from unintended information exposure to memory overwrite to a hardware trap.
``` c
/* In a.c */
extern int i;   /* UB 14 */
int f(void) {
  return ++i;   /* UB 36 */
}
/* In b.c */
short i;   /* UB 14 */
```
## Compliant Solution (Incompatible Object Declarations)
This compliant solution has compatible declarations of the variable `i`:
``` c
/* In a.c */
extern int i;   
int f(void) {
  return ++i;   
}
/* In b.c */
int i;   
```
## Noncompliant Code Example (Incompatible Array Declarations)
In this noncompliant code example, the variable `a` is declared to have a pointer type in file `a.c` but defined to have an array type in file `b.c`. The two declarations are incompatible, resulting in [undefined behavior 14](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_13). As before, accessing the object in function `f()` is [undefined behavior 36](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_36) with the typical effect of triggering a hardware trap.
``` c
/* In a.c */
extern int *a;   /* UB 14 */
int f(unsigned int i, int x) {
  int tmp = a[i];   /* UB 36: read access */
  a[i] = x;         /* UB 36: write access */
  return tmp;
}
/* In b.c */
int a[] = { 1, 2, 3, 4 };   /* UB 14 */
```
## Compliant Solution (Incompatible Array Declarations)
This compliant solution declares `a` as an array in `a.c` and `b.c`:
``` c
/* In a.c */
extern int a[];   
int f(unsigned int i, int x) {
  int tmp = a[i];   
  a[i] = x;         
  return tmp;
}
/* In b.c */
int a[] = { 1, 2, 3, 4 };  
```
## Noncompliant Code Example (Incompatible Function Declarations)
In this noncompliant code example, the function `f()` is declared in file `a.c` with one prototype but defined in file `b.c` with another. The two prototypes are incompatible, resulting in [undefined behavior 14](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_14). Furthermore, invoking the function is [undefined behavior 37](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_37) and typically has catastrophic consequences.
``` c
/* In a.c */
extern int f(int a);   /* UB 14 */
int g(int a) {
  return f(a);   /* UB 37 */
}
/* In b.c */
long f(long a) {   /* UB 14 */
  return a * 2;
}
```
## Compliant Solution (Incompatible Function Declarations)
This compliant solution has compatible prototypes for the function `f()`:
``` c
/* In a.c */
extern int f(int a);   
int g(int a) {
  return f(a);   
}
/* In b.c */
int f(int a) {   
  return a * 2;
}
```
## Noncompliant Code Example (Incompatible Variadic Function Declarations)
In this noncompliant code example, the function `buginf()` is defined to take a variable number of arguments and expects them all to be signed integers with a sentinel value of `-1`:
``` c
/* In a.c */
void buginf(const char *fmt, ...) {
   /* ... */
}
/* In b.c */
void buginf();
```
Although this code appears to be well defined because of the prototype-less declaration of `buginf()`, it exhibits [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in accordance with the C Standard, 6.7.7.4, paragraph 14 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> For two function types to be compatible, both shall specify compatible return types. Moreover, the parameter type lists shall agree in the number of parameters and in use of the final ellipsis; corresponding parameters shall have compatible types. In the determination of type compatibility and of a composite type, each parameter declared with function or array type is taken as having the adjusted type and each parameter declared with qualified type is taken as having the unqualified version of its declared type.

## Compliant Solution (Incompatible Variadic Function Declarations)
In this compliant solution, the prototype for the function `buginf()` is included in the scope in the source file where it will be used:
``` c
/* In a.c */
void buginf(const char *fmt, ...) {
   /* ... */
}
/* In b.c */
void buginf(const char *fmt, ...);
```
## Noncompliant Code Example (Excessively Long Identifiers)
In this noncompliant code example, the length of the identifier declaring the function pointer `bash_groupname_completion_function()` in the file `bashline.h` exceeds by 3 the minimum implementation limit of 31 significant initial characters in an external identifier. This introduces the possibility of colliding with the `bash_groupname_completion_funct` integer variable defined in file `b.c`, which is exactly 31 characters long. On an implementation that exactly meets this limit, this is [undefined behavior 30](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_30). It results in two incompatible declarations of the same function. (See [undefined behavior 14](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_14).) In addition, invoking the function leads to [undefined behavior 37](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_37) with typically catastrophic effects.
``` c
/* In bashline.h */
/* UB 14, UB 30 */
extern char * bash_groupname_completion_function(const char *, int);
/* In a.c */
#include "bashline.h"
void f(const char *s, int i) {
  bash_groupname_completion_function(s, i);  /* UB 37 */
}
/* In b.c */
int bash_groupname_completion_funct;  /* UB 14, UB 30 */
```
NOTE: The identifier `bash_groupname_completion_function` referenced here was taken from GNU [Bash](http://www.gnu.org/software/bash/), version 3.2.
## Compliant Solution (Excessively Long Identifiers)
In this compliant solution, the length of the identifier declaring the function pointer `bash_groupname_completion()` in `bashline.h` is less than 32 characters. Consequently, it cannot clash with `bash_groupname_completion_funct` on any compliant platform.
``` c
/* In bashline.h */
extern char * bash_groupname_completion(const char *, int);   
/* In a.c */
#include "bashline.h"
void f(const char *s, int i) {
  bash_groupname_completion(s, i);  
}
/* In b.c */
int bash_groupname_completion_funct; 
```
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL40-C | Low | Unlikely | Medium | P2 | L3 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | type-compatibilitytype-compatibility-linkdistinct-extern | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL40 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.DECL.IFLANG.STRUCT.DECL.IO
 | Inconsistent function declarationsInconsistent object declarations |
| Coverity | 2017.07 | MISRA C 2012 Rule 8.4 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl40-c |  |
| Helix QAC | 2024.4 | C0776, C0778, C0779, C0789, C1510C++1510 | Fully implemented |
| Klocwork | 2024.4 | MISRA.FUNC.NOPROT.DEF.2012MISRA.FUNC.PARAMS.IDENT | Fully implemented |
| LDRA tool suite | 8.5.4 | 1 X, 17 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL40-aCERT_C-DCL40-b | All declarations of an object or function shall have compatible typesIf objects or functions are declared more than once their types shall be compatible |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 18, 621, 793, 4376 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL40-C
 | Checks for declaration mismatch (rule fully covered) |
| RuleChecker | 24.04 | type-compatibilitytype-compatibility-linkdistinct-extern  | Fully checked |
| TrustInSoft Analyzer | 1.38 | incompatible declaration | Exhaustively verified. |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961 | Declaring the same function or object in incompatible ways [funcdecl] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 8.4 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.8.3 |
| [ISO/IEC 9899:2011] | J.2, "Undefined Behavior" |
| [ISO/IEC 9899:2024] | 6.7.7.4 "Function Declarators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151978) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152307)
## Comments:

|  |
| ----|
| I'm going to leave a comment here before I do anything.; The "Excessively Long Identifiers" portion of this rule (DCL40-C) has much in common with:DCL32-C. Guarantee that mutually visible identifiers are uniqueMinimally it should be referenced, possibly replaced.  This rule covers UB 41 which is not covered by DCL32-C.  This rule does not mention UB 31, which is odd.There are various solutions.  The one that holds the most promise in my mind right now is that we make some small improvements to this rule, such as mentioning UB 31:If two identifiers differ only in nonsignificant characters, the behavior is undefined.And then make the other rule a recommendation.  Or perhaps the excessively long identifiers can be used as an example for DCL32-C.What bothers me a bit is that UB 31 seems to contradict this rule stating that the existence of these two identifiers creates undefined behavior, while this rule insists it is only their use.  All the UB's seem to imply this, so I'm guessing their is a section of the standard that says it doesn't matter until you try to use these identifiers.
                                        Posted by rcs_mgr at Nov 02, 2013 08:41
                                     |
| I think the main difference between DCL32-C and DCL40-C boils down to intent.; DCL32-C focuses on the programmer thinking they have two identifiers which are unique due to their spelling, but are actually identical due to environmental limits imposed by the vendor.  It's name-based.  DCL40-C generally focuses on the programmer not realizing they have conflicting types when identifiers span translation units.  It's type-based.  So it makes sense, at least to me, that these are different guidelines.However, I would like to see proof that DCL32-C exists in the wild.  I remember MPW's C compiler had this problem, but that was decades ago.  Are there any modern vendors which have an environmental limit that goes undiagnosed with an error?  If so, then I agree this should be a rule.  None of the vendors I have access to appear to have environmental limits for identifiers.  For instance, gcc, clang and msvc all seem to be fine with 1600+ character identifiers.UB31 is more related to DCL32-C (in fact, it's the basis for DCL32-C).While I personally do not find the exception in DCL40-C to be useful, I think it is valid because 6.7p4 only applies to declarations that are in the same scope and refer to the same object being unique.  In this guideline, the objects are in different translation units.  When discussed over email, it was decided that this was a "no harm, no foul" situation, even though remediation was trivial.  This highlights the difference with UB31 – that UB is related to the name, and presence is enough to trigger the UB.  The UB mostly discussed by this rule relates to the type of a given object, and usage of the object is what triggers the UB.I think my suggestion is to test DCL32-C against modern implementations to determine whether it's actually a useful guideline.  If it isn't, I'd say we should combine it with DCL02-C. Use visually distinct identifiers, and remove the excessively long identifiers example from this rule.  If it is still useful, then I could see merging it in with this rule, keeping the excessively long identifiers and formally referencing UB31.
                                        Posted by aballman at Nov 04, 2013 10:03
                                     |
| I'm going to move DCL32-C to a recommendation for now and then we can decide later if it should stand along or be combined with another recommendation.Then I think we should add UB31 to here and keep the Excessively Long Example or not add it and remove the example.
                                        Posted by rcs_mgr at Nov 04, 2013 11:53
                                     |
| I think it's a good idea to move DCL32-C into a rec.; I think excessively long still deserves some research to see whether it's a problem with modern implementations or not.  31 characters is in the realm of plausible identifiers.  But if all of the modern vendors we can find handle 1500+ character identifiers, I think we can safely leave the information off.
                                        Posted by aballman at Nov 04, 2013 13:34
                                     |
| I think the wording "incompatible" is a little bit confusing here.C specification defines (two types are) "COMPATIBLE". ;"incompatible" used in this guideline is meant to be "not COMPATIBLE".Can we replace the all phrases with "incompatible" with the phrases using "compatible"?For  example, the title should be "All declarations of the same function or object must be compatible".The first sentence should be "All declarations of the same function or object must be compatible. If the types of two declarations for a function or object is not compatible, they result in undefined behaviour." 
                                        Posted by yozo at Nov 06, 2013 13:53
                                     |
| The term "incompatible" shows up a couple of times in C11:In Annex J2:An object is assigned to an inexactly overlapping object or to an exactly overlapping object with incompatible type (6.5.16.1).And in Annex L— A store is performed to an object that has two incompatible declarations (6.2.7),These terms are also antonyms, so I don't see this use as being confusing.
                                        Posted by rcs_mgr at Nov 06, 2013 17:29
                                     |

