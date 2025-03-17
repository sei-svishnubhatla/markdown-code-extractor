The C Standard, 7.1.4 paragraph 1, \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\] states
> Any function declared in a header may be additionally implemented as a function-like macro defined in the header, so if a library function is declared explicitly when its header is included, one of the techniques shown later in the next subclause can be used to ensure the declaration is not affected by such a macro. Any macro definition of a function can be suppressed locally by enclosing the name of the function in parentheses, because the name is then not followed by the left parenthesis that indicates expansion of a macro function name. For the same syntactic reason, it is permitted to take the address of a library function even if it is also defined as a macro. 220) The use of #undef to remove any macro definition will also ensure that an actual function is referred to.
>
> 220)This means that an implementation is required to provide an actual function for each library function, even if it also provides a macro for that function.
>
>  

However, the C Standard enumerates specific exceptions in which the behavior of accessing an object or function expanded to be a standard library macro definition is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The macros are `assert`, `errno`, `math_errhandling`, `setjmp`, `va_arg`, `va_copy`, `va_end`, and `va_start`. These cases are described by [undefined behaviors](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) [109](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_109), [113](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_113), [122](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_122), [124](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_124), and [138](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_138). Programmers must not suppress these macros to access the underlying object or function.
## Noncompliant Code Example (`assert`)
In this noncompliant code example, the standard `assert()` macro is suppressed in an attempt to pass it as a function pointer to the  `execute_handler()` function. Attempting to suppress the `assert()` macro is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
#include <assert.h>
typedef void (*handler_type)(int);
void execute_handler(handler_type handler, int value) {
  handler(value);
}
void func(int e) {
  execute_handler(&(assert), e < 0);
} 
```
## Compliant Solution (`assert`)
In this compliant solution, the `assert()` macro is wrapped in a helper function, removing the [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <assert.h>
typedef void (*handler_type)(int);
void execute_handler(handler_type handler, int value) {
  handler(value);
}
static void assert_handler(int value) {
  assert(value);
}
void func(int e) {
  execute_handler(&assert_handler, e < 0);
}
```
## Noncompliant Code Example (Redefining `errno`)
Legacy code is apt to include an incorrect declaration, such as the following in this noncompliant code example:
``` c
extern int errno;
```
## Compliant Solution (Declaring `errno`)
This compliant solution demonstrates the correct way to declare `errno` by including the header `<errno.h>`:
``` c
#include <errno.h>
```
[C-conforming](BB.-Definitions_87152273.html#BB.Definitions-conformingprogram) [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) are required to declare `errno` in `<errno.h>`, although some historic implementations failed to do so.
## Risk Assessment
Accessing objects or functions underlying the specific macros enumerated in this rule is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC38-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | BADMACRO.STDARG_H | Use of <stdarg.h> Feature |
| Cppcheck Premium | 24.11.0 | premium-cert-msc38-c |  |
| Helix QAC | 2024.4 | C3437, C3475C++3127, C++5039 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC38-a | ;A function-like macro shall not be invoked without all of its arguments |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC38-C | Checks for predefined macro used as an object (rule fully covered) |
| RuleChecker | 24.04 |  | Supported, but no explicit checker |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC38-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | DCL37-C. Do not declare or define a reserved identifier | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| ISO/IEC 9899:2024 | 7.1.4, "Use of Library Functions" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152283) [](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](../c/MSC39-C_%20Do%20not%20call%20va_arg__%20on%20a%20va_list%20that%20has%20an%20indeterminate%20value)
## Comments:

|  |
| ----|
| 
My current feeling is that this rule can remain distinct from DCL37-C, as that rule specifically deals with classes of reserved identifiers (eg ids that start with _). This rule should swallow ERR31-C.
A couple of comments on your assert NCCE/CS:
    Is this 'known assert.h' available on a current platform? GCC? MSVC?  Where is it used?
    The NCCE needs an 'implementation details' section which shows the actual behavior of the code on a particular platform, using the known assert.h.
    I'm not sure the compliant solution solves the problem, as the myassert() function would still do nothing on non-debug builds, which is what the NCCE was trying to accomplish.
                                        Posted by svoboda at Feb 28, 2010 11:03
                                     |
| There are two preconditions for undefined behavior 104:
    the assert() macro definitions is suppressed
    the function assert() is accessed
The NCCE meets the first precondition but since the code never references an assert() function, it doesn't necessarily exhibit undefined behavior. (Would the behavior of the example change if the #undef directive were removed? If not, it's probably not a valid NCCE.)
FWIW, I think the undefined behavior applies to something like the following:
#include <assert.h>
// suppose the following is the definition of the assert()
// macro in <assert.h> and there is no function with the
// same name:
// #define assert(expr)   \
//   ((expr) ? (void)0 \
//           : (void)fprintf(stderr, "Assertion failed: %s:%d (%s): %s\n", \
//                            __FILE__, __LINE__, __func__, #expr))
//
void f(int i) {
  (assert)(0 < i);   // assert() macro suppressed, calling function assert()
}
#undef assert        // assert() macro suppressed
void g(int i) {
  assert(0 < i);     // calling function assert()
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 28, 2010 14:16
\| \|
Ah, I thought the standard meant referring to the function underlying the assert macro, but looking at it again, it does seem to mean using a function called assert.
But then, wouldn't your code above necessarily not compile because the assert function identifier is undefined? I feel like ub14 would be triggered by something like this:
``` java
#include <assert.h>
// suppose the following is the definition of the assert()
// macro in <assert.h> and there is no function with the
// same name:
// #define assert(expr)   \
//   ((expr) ? (void)0 \
//           : (void)fprintf(stderr, "Assertion failed: %s:%d (%s): %s\n", \
//                            __FILE__, __LINE__, __func__, #expr))
//
#undef assert        // assert() macro suppressed
// Define a function assert
void assert(int i) {
     /* verifacation... */
}
void g(int i) {
  assert(i);     // calling function assert()
}
```
![](images/icons/contenttypes/comment_16.png) Posted by fec at Mar 01, 2010 16:12
\| \|
C allows calls to functions without function prototypes in scope so the NCCE I gave would compile but (most likely) fail to link. Failing to link is one possible manifestation of undefined behavior. The closest match I can find in Annex J is UB [38](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-38).
Your example above doesn't have undefined behavior per se because you defined `assert(int)`. The code simply calls the user-defined `assert()` function, just as it would if `<assert.h>` hadn't been included (and assuming no other definition of the `assert()` function existed in the program). That's well-defined.
I should add: if there is another definition of `assert()` in the program, your program would certainly have undefined behavior – UB [36](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-36). But the C standard doesn't allow implementations to define such a function: `assert()` must be a macro.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 01, 2010 18:50
\| \|
The assert NCCE looks informative, but the contents of assert.h can be described in prose (rather than code comments) something like "defines an assert() macro and does not define an assert() function". Also it needs to define a (user-suplised?) assert() function. Consequently the CS should declare a myassert() function, and it (obviously) can't come from \<assert.h\>
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 03, 2010 12:03
\| \|
The first NCCE may exemplify highly questionable practice but it doesn't have undefined behavior because it includes `<myassert.h>` which defines a function named `assert()`. Suppressing the `assert` macro in `fullAssert()` will just end up calling this function. As I said before, the problem is when no such function exists (e.g., as in the example I gave in my [comment](https://www.securecoding.cert.org/confluence/display/seccode/MSC38-C.++Do+not+treat+as+an+object+any+predefined+identifier+that+might+be+implemented+as+a+macro?focusedCommentId=42729480#comment-42729480) above).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 04, 2010 20:48
\| \|
C99 (n1256), S7.2 says:
> The assert macro shall be implemented as a macro, not as an actual function. If the macro definition is suppressed in order to access an actual function, the behavior is undefined.

As I see it, the question of whether the 1st NCCE invokes undefined behavior is open to interpretation. Does the text "in order to access an actual function" imply that
1\. the dveloper thinks the assert() macro is covering an implementation-defined assert function, and they wish to access the function w/o using the macro?
or
2\. the developer creates their own assert() function and suppresses the assert() macro in order to access their own function.
The 1st NCCE falls under case (2), and I suspect (but am not sure that) the standard meant case (1).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 11, 2010 11:21
\| \|
C99 makes a distinction between suppressing a macro (which is explicitly allowed except in a few cases such as `assert` and `errno`) and defining an identifier with the same name (which is disallowed in general except when C99 doesn't define the identifier to have linkage). This difference is exemplified in the specification of `assert` and `errno` (and a handful of other cases). For `assert`:
> If the \[`assert`\] macro definition is suppressed in order to access an actual function, the behavior is undefined.

For `errno`:
> If a \[`errno`\] macro definition is suppressed in order to access an actual object, or a program defines an identifier with the name `errno`, the behavior is undefined.

It's certainly possible that this distinction is unintended. Let's see what the response is from WG14.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 11, 2010 14:08
\| \|
Certainly a subtle point, but it looks like we finally have a consensus.
Defining and using an object named assert (e.g. `int assert`) is conforming, even if it suppresses the standard `assert()` macro to access that object. Defining and using a function `assert()` is conforming in a translation unit that does not include `<assert.h>`. However, if the standard assert header is included, suppressing the `assert()` macro to access a function is not strictly conforming. (This is a summary of information from Derek Jones.)
So, the current assert NCCE above does demonstrate undefined behavior.
![](images/icons/contenttypes/comment_16.png) Posted by fec at Mar 17, 2010 13:42
\| \|
I concede that the feedback we got from WG14 does indeed put the NCCE in the realm of undefined behavior, even though no one was able to produce a plausible example of effects other than calling the user-defined `assert()` function. That being said, I certainly agree that defining a function `assert()` is a bad idea regardless of whether `<assert.h>` is included and should be strongly discouraged, if only because it is confusing.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 17, 2010 15:11
\| \|
This is a good rule, but I'm not impressed with the title...its terribly vague. A better title would be something along the lines of:
Don't redefine assert, errno, or any other object or function that might be a macro.
I realize this is, strictly speaking, less accurate than the currnet title, but it is more indicative of what the rule is about. IMHO accuracy is more suited for the intro paragraph than the title. Comments?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2010 16:12
\| \|
The problem this guideline attempts to warn against is accessing (not just redefining) the symbols underlying the handful of identifiers that may only be implemented as macros (and not necessarily as functions/objects with the same name). The problem, in all cases, is the same as the one mentioned in my comment [Re: MSC38-C. Do not treat as an object any predefined identifier that might be implemented as a macro](https://www.securecoding.cert.org/confluence/display/seccode/MSC38-C.++Do+not+treat+as+an+object+any+predefined+identifier+that+might+be+implemented+as+a+macro?focusedCommentId=42729480#comment-42729480): that the underlying object or function may not exist. The effect of accessing it is a compilation or linker error. It is a compilation when no matching declaration exists, and it is a linker error when a matching declaration exists for which the program (or the C library) does not provide a definition.
An example involving `errno` is:
``` java
#include <errno.h>
#undef errno
int error() {
  // accessing the underlying object when it may not exist
  return errno;
}
```
Note that neither NCCE in this guideline demonstrates the problem the guideline is about. They both declare an identifier with the same name as one of the reserved names (which may be a bad idea but it will not cause a problem on any implementation).
As I have been trying to say all along, the noncompliant examples should demonstrate the real risks of violating the language rules and they should be reproducible with popular compilers. The NCCE involving `errno` I give above clearly illustrates the problem when compiled with gcc on Linux:
> [!note]
>
>     z.c: In function â€˜errorâ€™:
>     z.c:5: error: â€˜errnoâ€™ undeclared (first use in this function)
>     z.c:5: error: (Each undeclared identifier is reported only once
>     z.c:5: error: for each function it appears in.)

The `assert` example I gave in my earlier comments produces similar output:
> [!note]  
>
>     z.c: In function â€˜fâ€™:
>     z.c:13: error: â€˜assertâ€™ undeclared (first use in this function)
>     z.c:13: error: (Each undeclared identifier is reported only once
>     z.c:13: error: for each function it appears in.)

A slightly modified example involving `errno` that demonstrates a linker error looks like this:
``` java
#include <errno.h>
#undef errno
extern int errno;
int error() {
  return errno;
}
```
Compiling and linking it with gcc on Linux/x64 produces the following output:
> [!note]  
>
>     /usr/bin/ld: errno: TLS definition in /lib64/libc.so.6 section .tbss mismatches non-TLS reference in /tmp/ccg4BUxc.o
>     /lib64/libc.so.6: could not read symbols: Bad value
>     collect2: ld returned 1 exit status

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 24, 2010 14:18
\| \|
The NCCEs both demonstrate undefined behavior, which has traditionally been enough to categorize them as noncompliant. (even if your implementation handles them benignly, such as by refusing to compile the code.) Furthermore, code that **always** produces a compiler error is not, in our experience, a valid NCCE, because such code would never escape a developer team or QA...it is code that compilers compile that you must watch out for.
Examples of code that produce compiler or linker errors is not particularly scary. If you can show a NCCE that compiles into a program that does something unexpected, that would be a worthy implementation detail for this rule.
However, you're right that the rule is about accessing macro-hidden objects rather than redefining them. I don't have a good alternate title for this rule...perhaps this one?
Don't treat as an object any predefined identifier that might be implemented as a macro
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 26, 2010 15:52
\| \|
The examples exhibit undefined behavior only in theory, and only because that's what the experts insisted on. In reality, they are benign on all implementations that I am aware of. I.e., there is no risk that this will lead to any kind of scary effects on any existing implementation:
``` java
#include <assert.h>
#include <stdio.h>
void (assert)(int expr) { printf("Assertion: %d\n", expr); }
int main() {
  (assert)(0);
}
```
I agree that compiler or linker errors are much less interesting from the point of view of exploits than other cases of undefined behavior (those that manifest themselves at program runtime). Unfortunately (for the purposes of our efforts to come up with such examples), there is nothing scary about accessing the functions or objects underlying the definitions of `assert()` or `errno`, or even redefining them. The scariest undefined behavior you can hope to find is the linker error.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 26, 2010 22:29
\| \|
The way the title reads, to me, is incorrect.; The standard explicitly says that you can suppress library-defined function macros in the general case (7.1.4p1):
> Any function declared in a header may be additionally implemented as a function-like macro deﬁned in the header, so if a library function is declared explicitly when its header is included, one of the techniques shown below can be used to ensure the declaration is not affected by such a macro. Any macro deﬁnition of a function can be suppressed locally by enclosing the name of the function in parentheses, because the name is then not followed by the left parenthesis that indicates expansion of a macro function name. For the same syntactic reason, it is permitted to take the address of a library function even if it is also deﬁned as a macro.<sup>185</sup>
>
> 185\) This means that an implementation shall provide an actual function for each library function, even if it also provides a macro for that function.

The title seems to prohibit this behavior generally instead of in the few specific cases outlined in the rule.  However, I'm at a loss for an improved title.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 20, 2013 11:33
\| \|
I couldn't figure out a better name for a title, but posed the question internally. However, I did clarify the contents of the rule and update the `assert` code example to be a bit more compelling (hopefully).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 19, 2013 13:47
\|
