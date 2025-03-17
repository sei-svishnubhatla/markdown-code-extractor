The arguments to a macro must not include preprocessor directives, such as `#define`, `#ifdef`, and `#include`. Doing so results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), according to the C Standard, 6.10.5, paragraph 11 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]:
> The sequence of preprocessing tokens bounded by the outside-most matching parentheses forms the list of arguments for the function-like macro. The individual arguments within the list are separated by comma preprocessing tokens, but comma preprocessing tokens between matching inner parentheses do not separate arguments. **If there are sequences of preprocessing tokens within the list of arguments that would otherwise act as preprocessing directives, the behavior is undefined.**

See also [undefined behavior 92](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_92).
This rule also applies to the use of preprocessor directives in arguments to any function where it is unknown whether or not the function is implemented using a macro. This includes all standard library functions, such as `memcpy()`, `printf()`, and `assert()`, because any standard library function may be implemented as a macro. (C24, 7.1.4, paragraph 1).
## Noncompliant Code Example
In this noncompliant code example \[[GCC Bugs](http://gcc.gnu.org/bugs.html#nonbugs_c)\], the programmer uses preprocessor directives to specify platform-specific arguments to `memcpy()`. However, if `memcpy()` is implemented using a macro, the code results in undefined behavior.
``` c
#include <string.h>
void func(const char *src) {
  /* Validate the source string; calculate size */
  char *dest;
  /* malloc() destination string */ 
  memcpy(dest, src,
    #ifdef PLATFORM1
      12
    #else
      24
    #endif
  );
  /* ... */
}
```
## Compliant Solution
In this compliant solution \[[GCC Bugs](http://gcc.gnu.org/bugs.html#nonbugs_c)\], the appropriate call to `memcpy()` is determined outside the function call:
``` c
#include <string.h>
void func(const char *src) {
  /* Validate the source string; calculate size */
  char *dest;
  /* malloc() destination string */ 
  #ifdef PLATFORM1
    memcpy(dest, src, 12);
  #else
    memcpy(dest, src, 24);
  #endif
  /* ... */
}
```
## Risk Assessment
Including preprocessor directives in macro arguments is undefined behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE32-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | macro-argument-hash | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE32 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.PREPROC.MACROARG | Preprocessing directives in macro argument |
| ECLAIR | 1.2 | CC2.PRE32 | Fully implemented |
| Helix QAC | 2024.4 | C0853C++1072 | Fully implemented |
| Klocwork | 2024.4 | MISRA.EXPANSION.DIRECTIVE | Fully implemented |
| LDRA tool suite | 9.7.1 | 341 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE32-a | Arguments to a function-like macro shall not contain tokens that look like preprocessing directives |
| PC-lint Plus | 1.4 | 436, 9501 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule PRE32-C | Checks for preprocessor directive in macro argument (rule fully covered) |
| RuleChecker | 24.04 | macro-argument-hash | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE32-C).
## Bibliography

|  |  |
| ----|----|
| [GCC Bugs] | "Non-bugs" |
| [ISO/IEC 9899:2024] | 6.10.5, "Macro Replacement" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152163) [](../c/Rule%2001_%20Preprocessor%20_PRE_) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_)
## Comments:

|  |
| ----|
| For example, standard library functions, such as;memcpy(), printf(), and assert(), may be implemented as macros.I think this is not stated strongly enough. Strictly speaking, ALL C library functions can be implemented as a function-like macro in addition to a real function definition, so for maximal portability you would need to not use a preprocessor directive in the invocation of any C Standard Library function. See C17 7.1.4p1.
                                        Posted by aballman at Aug 29, 2019 19:08
                                     |
| Aaron:This has far-reaching implications, and I don't see much in the way of guarantees if every standard library function could be implemented as a function-like macro, as is suggested in C11,s7.1.4:Any function declared in a header may be additionally implemented as a function-like macro defined in the header, so if a library function is declared explicitly when its header is included, one of the techniques shown below can be used to ensure the declaration is not affected by such a macro.For example, is there any guarantee these macros evaluate their arguments exactly once? If not, then you could not nest standard library function calls, such as printf("%d", atoi(string)).I know our research depends on the ability to nest #ifdefs within arguments to a function call, and I've seen it in lots of source code...if the functions could be macros instead, that would be a Big Mess(tm).
                                        Posted by svoboda at Sep 03, 2019 13:19
                                     |
| Yeah, I was recently questioning the utility of this rule because of this. What's more sad is that the best solution I thought of to portably deal with this... isn't allowed in conforming C:
_Static_assert(!defined(memcpy), "memcpy implemented as a macro");

Because \`defined\` cannot be used outside of a preprocessor conditional inclusion directive. You basically have to write:
``` java
#ifdef memcpy
_Static_assert(false, "memcpy implemented as a macro");
#endif
```
> For example, is there any guarantee these macros evaluate their arguments exactly once?;

There is such a guarantee in 7.1.4p1: "Any invocation of a library function that is implemented as a macro shall expand to code that evaluates each of its arguments exactly once, fully protected by parentheses where necessary, so it is generally safe to use arbitrary expressions as arguments." though there is a footnote attached to it that says such macros might not contain the same sequence points as a function call, however (which seems like a separate issue not explicitly discussed in any of the rules).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 03, 2019 13:30
\| \|
I've reworded the rule's intro to clarify that **any** standard C library function must not have preprocessor directives in its arguments.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 14, 2019 15:06
\|
