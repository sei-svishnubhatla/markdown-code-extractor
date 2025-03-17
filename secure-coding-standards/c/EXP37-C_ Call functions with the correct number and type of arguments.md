Do not call a function with the wrong number or type of arguments. 
The C Standard identifies two distinct situations in which [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) (UB) may arise as a result of invoking a function using a declaration that is incompatible with its definition or by supplying incorrect types or numbers of arguments:

|  |  |
| ----|----|
| UB | Description |
| 25 | A pointer is used to call a function whose type is not compatible with the;referenced type (6.3.2.3).  |
| 37 | A function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function (6.5.2.2).  |

Functions that are appropriately declared (as in [DCL40-C. Do not create incompatible declarations of the same function or object](DCL40-C_%20Do%20not%20create%20incompatible%20declarations%20of%20the%20same%20function%20or%20object)) will typically generate a compiler diagnostic message if they are supplied with the wrong number or types of arguments. However, there are cases in which supplying the incorrect arguments to a function will, at best, generate compiler [warnings](BB.-Definitions_87152273.html#BB.Definitions-warning). Although such warnings should be resolved, they do not prevent program compilation. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)
## Noncompliant Code Example
The header `<tgmath.h>` provides type-generic macros for math functions. Although most functions from the `<math.h>` header have a complex counterpart in `<complex.h>`, several functions do not. Calling any of the following type-generic functions with complex values is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
**Functions That Should Not Be Called with Complex Values**

|  |  |  |  |  |  |  |  |  |  |
| ----|----|----|----|----|----|----|----|----|----|
| atan2() | erf() | fdim() | fmin() | ilogb() | llround() | logb() | nextafter() | rint() | tgamma() |
| cbrt() | erfc() | floor() | fmod() | ldexp() | log10() | lrint() | nexttoward() | round() | trunc() |
| ceil() | exp2() | fma() | frexp() | lgamma() | log1p() | lround() | remainder() | scalbn() |  |
| copysign() | expm1() | fmax() | hypot() | llrint() | log2() | nearbyint() | remquo() | scalbln() |  |

This noncompliant code example attempts to take the base-2 logarithm of a complex number, resulting in undefined behavior:
``` c
#include <tgmath.h>
void func(void) {
  double complex c = 2.0 + 4.0 * I;
  double complex result = log2(c);
}
```
## Compliant Solution (Complex Number)
If the `clog2()` function is not available for an implementation as an extension, the programmer can take the base-2 logarithm of a complex number, using `log()` instead of `log2()`, because `log()` can be used on complex arguments, as shown in this compliant solution:
``` c
#include <tgmath.h>
void func(void) {
  double complex c = 2.0 + 4.0 * I;
  double complex result = log(c)/log(2);
}
```
## Compliant Solution (Real Number)
The programmer can use this compliant solution if the intent is to take the base-2 logarithm of the real part of the complex number:
``` c
#include <tgmath.h>
void func(void) {
  double complex c = 2.0 + 4.0 * I;
  double complex result = log2(creal(c));
}
```
## Noncompliant Code Example
In this noncompliant example, the C standard library function `strchr()` is called through the function pointer `fp` declared with a prototype with incorrectly typed arguments. According to the C Standard, 6.3.2.3, paragraph 8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]
> A pointer to a function of one type may be converted to a pointer to a function of another type and back again; the result shall compare equal to the original pointer. If a converted pointer is used to call a function whose type is not compatible with the referenced type, the behavior is undefined.

See [undefined behavior 25.](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_25)
``` c
#include <stdio.h>
#include <string.h>
char *(*fp)();
int main(void) {
  const char *c;
  fp = strchr;
  c = fp('e', "Hello");
  printf("%s\n", c);
  return 0;
}
```
## Compliant Solution
In this compliant solution, the function pointer `fp`, which points to the C standard library function `strchr()`, is declared with the correct parameters and is invoked with the correct number and type of arguments:
``` c
#include <stdio.h>
#include <string.h>
char *(*fp)(const char *, int);
int main(void) {
  const char *c;
  fp = strchr;
  c = fp("Hello",'e');
  printf("%s\n", c);
  return 0;
}
```
## Noncompliant Code Example
In this noncompliant example, the function `f()` is defined to take an argument of type `long` but `f()` is called from another file with an argument of type `int`:
``` c
/* In another source file */
long f(long x) {
  return x < 0 ? -x : x;
}
/* In this source file, no f prototype in scope */
long f();
long g(int x) {
  return f(x);
}
```
## Compliant Solution
In this compliant solution, the prototype for the function `f()` is included in the source file in the scope of where it is called, and the function `f()` is correctly called with an argument of type `long`:
``` c
/* In another source file */
long f(long x) {
  return x < 0 ? -x : x;
}
/* f prototype in scope in this source file */
long f(long x); 
long g(int x) {
  return f((long)x);  
}
```
## Noncompliant Code Example (POSIX)
The POSIX function `open()` \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] is a variadic function with the following prototype:
``` java
int open(const char *path, int oflag, ... );
```
The `open()` function accepts a third argument to determine a newly created file's access mode. If `open()` is used to create a new file and the third argument is omitted, the file may be created with unintended access permissions. (See [FIO06-C. Create files with appropriate access permissions](FIO06-C_%20Create%20files%20with%20appropriate%20access%20permissions).)
In this noncompliant code example from a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in the `useradd()` function of the `shadow-utils` package [CVE-2006-1174](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-1174), the third argument to `open()` is accidentally omitted:
``` c
fd = open(ms, O_CREAT | O_EXCL | O_WRONLY | O_TRUNC);
```
Technically, it is incorrect to pass a third argument to open() when not creating a new file (that is, with the O_CREAT flag not set).
## Compliant Solution (POSIX)
In this compliant solution, a third argument is specified in the call to `open()`:
``` c
#include <fcntl.h>
void func(const char *ms, mode_t perms) {
  /* ... */
  int fd;
  fd = open(ms, O_CREAT | O_EXCL | O_WRONLY | O_TRUNC, perms);
  if (fd == -1) {
    /* Handle error */
  }
}
```
## Risk Assessment
Calling a function with incorrect arguments can result in [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) or unintended program behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP37-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | incompatible-argument-typeparameter-matchparameter-match-computedparameter-match-type | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP37 |  |
| CodeSonar | 8.3p0 | LANG.FUNCS.APM | Array parameter mismatch |
| Compass/ROSE |  |  | Can detect some violations of this rule. In particular, it ensures that all calls to open() supply exactly two arguments if the second argument does not involve O_CREAT, and exactly three arguments if the second argument does involve O_CREAT |
| Coverity | 2017.07 | MISRA C 2012 Rule 8.2MISRA C 2012 Rule 17.3 | ImplementedRelies on functions declared with prototypes, allow compiler to check |
| Cppcheck Premium | 24.11.0 | premium-cert-exp37-c |  |
| ECLAIR | 1.2 | CC2.EXP37 | Partially implemented |
| EDG |  |  |  |
| GCC | 4.3.5 |  | Can detect violation of this rule when the -Wstrict-prototypes flag is used. However, it cannot detect violations involving variadic functions, such as the open() example described earlier |
| Helix QAC | 2024.4 | C1331, C1332, C1333, C3002, C3320, C3335C++0403 |  |
| Klocwork | 2024.4 | MISRA.FUNC.UNMATCHED.PARAMS |  |
| LDRA tool suite | 9.7.1 | 41 D, 21 S, 98 S, 170 S, 496 S, 576 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP37-aCERT_C-EXP37-b
CERT_C-EXP37-d | Conversions shall not be performed between non compatible pointer to a function typesSpecify the access permission bits if a file is created using the 'open' or 'openat' system call
Functions shall always have visible prototype at the function call |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP37-C | Checks for:Implicit function declarationBad file access mode or statusUnreliable cast of function pointerStandard function call with incorrect argumentsRule partially covered. |
| PVS-Studio | 7.35 | V540, V541, V549, V575, V632, V639, V666, V671, V742, V743, V764, V1004 |  |
| SonarQube C/C++ Plugin | 3.11 | S930 | Detects incorrect argument count |
| RuleChecker | 24.04 | parameter-matchparameter-match-type | Partially checked |
| TrustInSoft Analyzer | 1.38 | unclassified ("function type matches") | Partially verified (see one compliant and one non-compliant example). |

## Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP37-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL07-C. Include the appropriate type information in function declarators | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | MSC00-C. Compile cleanly at high warning levels | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | FIO06-C. Create files with appropriate access permissions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Subprogram Signature Mismatch [OTR] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Calling functions with incorrect arguments [argcomp] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 8.2 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 17.3 (mandatory) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-628, Function Call with Incorrectly Specified Arguments | 2017-07-05: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-685 and EXP37-C
EXP37-C = Union( CWE-685, CWE-686) Intersection( CWE-685, CWE-686) = Ø
### CWE-686 and EXP37-C
Intersection( EXP37-C, FIO47-C) =
-   Invalid argument types passed to format I/O function
EXP37-C – FIO47-C =
-   Invalid argument types passed to non-format I/O function
FIO47-C – EXP37-C =
-   Invalid format string, but correctly matches arguments in number and type
EXP37-C = Union( CWE-685, CWE-686)
Intersection( CWE-685, CWE-686) = Ø
### CWE-628 and EXP37-C
CWE-628 = Union( EXP37-C, list) where list =
-   Improper ordering of function arguments (that does not violate argument types)
-   Wrong argument values or references
## Bibliography

|  |  |
| ----|----|
| [CVE] | CVE-2006-1174 |
| [ISO/IEC 9899:2011] | 6.5.2.2, "Function Calls" |
| [ISO/IEC 9899:2024] | 6.3.2.3, "Pointers" |
| [IEEE Std 1003.1:2013] | open() |
| [Spinellis 2006] | Section 2.6.1, "Incorrect Routine or Arguments" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152059) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152294)
## Comments:

|  |
| ----|
| The example is rather forced and consequently non-compelling, but I'm not sure I have a good alternative to hand.; The rule to ensure there is always a prototype in scope (and to use full prototypes for function pointers) deals with most problems - and permits most C code to be compiled with a C++ compiler. More accurately, if C code can be compiled with a C++ compiler, then you have avoided most of the problems such as the one highlighted by this example.  I use that as a validity check on my own code; the main problem area is that C++ requires explicit casts from 'void *' (mainly an issue for memory management).
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 23:08
                                     |
| While the reader can likely infer this information from the code samples, it may be useful to provide a little more explanation of the distinction between old fashion function declarations with empty parentheses and function declarations with function prototypes.; I think some readers may not be familiar with this.
                                        Posted by adahmad at Apr 12, 2008 13:32
                                     |
| The second argument to open() should match between the examples.
The real problem with open() was that POSIX made it variadic rather than having a sometimes-unused third argument, as is usual for many other;Unix system calls.  That in turn was the result of the original 2-argument open() being extended well before POSIX without sufficient redesign of the interface at that time.
                                        Posted by dagwyn at Apr 15, 2008 15:26
                                     |
| second argument (and first) now matches.
                                        Posted by rcs at Apr 16, 2008 10:23
                                     |
| The explanation you cite is provided in DCL07-A, which is linked from this rule.
                                        Posted by svoboda at Apr 17, 2008 10:32
                                     |
| 
Compass/ROSE can detect some violations of this rule. In particular, it ensures that all calls to open() supply three arguments.
If it really expects three arguments on all calls, then it's broken.  The behaviour of open() when a third argument is supplied and O_CREAT is not set is unspecified by POSIX.
                                        Posted by geoffclare at Jul 21, 2008 11:42
                                     |
| changed to require 3 arguments if the first arg involves O_CREAT and 2 args if the first arg doe snot have O_CREAT.
                                        Posted by svoboda at Jul 21, 2008 12:17
                                     |
| There's no way for us to check O_CREAT without macro support...
                                        Posted by avolkovi at Jul 21, 2008 14:39
                                     |
| With that algorithm, what would Compass/ROSE make of this code:
int open0700(const char *file, int flags)
{
    if (flags & O_CREAT)
        return open(file, flags, (mode_t)0700);
    else
        return open(file, flags);
}

![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jul 22, 2008 04:17
\| \|
Compass/ROSE stays quiet, it sees a variable in the second argument and quits out of the checker because it likes to avoid dynamic/overly complicated analysis when possible.
Also, that little code bit exposed two small bugs that I just fixed, one related to your original question (Rose would incorrectly flag the first call to open because it was not looking for variables), the second was in a different checker that assumed all calls to open where of the form `fd = open(...)`
![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 22, 2008 09:33
\| \|
This rule has several NCCE/CS pairs, and they strike me as somewhat redundant:
-   I don't think the first NCCE is noncompliant. By supplying no arguments to `fp`, `fp` can take any arguments, including the correct ones. The NCCE works correctly on my Ubuntu box (printing "ello"). The real danger is that `fp` can take an incorrect set of arguments. The CS makes it an error to invoke `fp` with an incorrect set of arguments.
<!-- -->
-   In fact the 2nd NCCE/CS pair illustrate this principle much better than the first. I think we should drop the 1st NCCE/CS examples.
<!-- -->
-   The 3rd NCCE also looks OK to me. Paragraph 6 cited from the standard says nothing that the code violates, so it looks to be well-defined.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 04, 2013 15:45
\| \|
The first NCE violations UB 26.; This is also covered under DCL40-C. Do not create incompatible declarations of the same function or object
I'm not sure why we should have this in two places.  I don't think we should have this in two places, so I'm OK removing this NCE/CS pair, but the description of the rule will need to change as well.
Yeah, I don't understand the 3rd NCE either. 
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 04, 2013 16:49
\| \|
The difference between this rule and DCL40-C is that all the function declrations here have undetermined arguments `f()` vs `f(void)`. Is a function pointer with undetermined arguments incompatible with a function pointer with specified arguments? I thought so.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 05, 2013 09:03
\| \|
IMO DCL40-C was about making incompatible \*declarations\*, whereas this rule is about calling functions with incompatible arguments. It's a little tricky to violate this rule w/o also violating DCL40-C; you have to use parameterless prototypes. Which all the NCCEs here do.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 08, 2013 16:59
\| \|
The first NCCE (both forms);show it calling with the wrong argument order.  It should be `const char *` first, then `int` second.  However, the second form of the first NCCE does violate [DCL40-C. Do not create incompatible declarations of the same function or object](DCL40-C_%20Do%20not%20create%20incompatible%20declarations%20of%20the%20same%20function%20or%20object) and probably should be mentioned or removed.
The third NCCE is a violation of the POSIX standard because of the `O_CREAT` flag being present. Specifically:
> ...and the access permission bits (see[](http://pubs.opengroup.org/onlinepubs/009695299/basedefs/sys/stat.h.html)) of the file mode shall be set to the value of the third argument...  

![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 08:59
\| \|
Ah, with regards to the first NCCE/CS pair, I may be looking at the updated version of the rule while you were likely talking about its previous form. ![](images/icons/emoticons/wink.svg)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 09:16
\| \|
Hi there,
i have a question about this rule.
The table at the beginning of this rule lists 5 kinds of UBs, and in 38,39 and 40 UB, all of them have this precondition:;*For a call to a function without a function prototype in scope,* so my question is whether this precondition is a must condition that we should consider to detect a violation of this rule? Given the rule's title: ***Do not call a function with the wrong number or type of arguments.*** and the sentence in  "Risk Assessment" : ***Calling a function with incorrect arguments can result in [unexpected](https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-unexpectedbehavior) or unintended program behavior.***
***  
***
Take the 3rd NCCE as an example, if we change it to 
`/* In another source file */`  
`long` `f(``long` `x) {`  
`  ``return` `x < 0 ? -x : x;`  
`}`  
`/* In this source file, `***`has f prototype in scope`***` */`  
`long` `f(long x);`  
` `   
`long` `g(``int` `x) {`  
`  ``return` `f(x);`  
`}`
does it still violate this rule? and more specifically
    void f(int a);
    vois test() {
        float b;
        f(b);   //defect or no defect?
    }
does this violate this rule?
please help clarify, many thanks!
![](images/icons/contenttypes/comment_16.png) Posted by zhuochen at Sep 16, 2019 22:24
\| \|
> ...so my question is whether this precondition is a must condition that we should consider to detect a violation of this rule?

For those particular UBs, yes. When there is no prototype in scope, the compiler has no information about what the expected types are for the function arguments, so those UBs mostly relate to situations where the parameters for the actual function definition do not match the call site. This can be due to mismatched numbers of arguments or type incompatibilities, etc.
> does it still violate this rule?

No. By introducing the prototype for f(), you're giving the compiler enough information to know how to promote from the int in g() to the long needed by f(). FWIW, this code is equivalent to what you'd get if the declaration of f() were in a header file and you included that header file in the source file containing g().
> does this violate this rule?

For the 3rd NCCE, yes, I believe it does. You declare f() as taking an int when it actually takes a long in the original source file.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 17, 2019 07:56
\|
