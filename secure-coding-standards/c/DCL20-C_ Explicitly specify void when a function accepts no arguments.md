According to the C Standard, subclause 6.7.6.3, paragraph 14 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> An identifier list declares only the identifiers of the parameters of the function. An empty list in a function declarator that is part of a definition of that function specifies that the function has no parameters. The empty list in a function declarator that is not part of a definition of that function specifies that no information about the number or types of the parameters is supplied.

Subclause 6.11.6 states that
> The use of function declarators with empty parentheses (not prototype-format parameter type declarators) is an obsolescent feature.

Consequently, functions that accept no arguments should explicitly declare a `void` parameter in their parameter list. This holds true in both the declaration and definition sections (which should match).
Defining a function with a `void` argument list differs from declaring it with no arguments because, in the latter case, the compiler will not check whether the function is called with parameters at all \[[TIGCC, void usage](http://tigcc.ticalc.org/)\]. Consequently, function calling with arbitrary parameters will be accepted without a warning at compile time.
Failure to declare a `void` parameter will result in
-   An ambiguous functional interface between the caller and callee.
-   Sensitive information outflow.
A similar recommendation deals with parameter type in a more general sense: [DCL07-C. Include the appropriate type information in function declarators](DCL07-C_%20Include%20the%20appropriate%20type%20information%20in%20function%20declarators).
## Noncompliant Code Example (Ambiguous Interface)
In this noncompliant code example, the caller calls `foo()` with an argument of 3. The caller expects `foo()` to accept a single `int` argument and to output the argument as part of a longer message. Because `foo()` is declared without the `void` parameter, the compiler will not perform any caller check. It is therefore possible that the caller may not detect the error. In this example, for instance, `foo()` might output the value 3 as expected.
Because no function parameter has the same meaning as an arbitrary parameter, the caller can provide an arbitrary number of arguments to the function.
``` c
/* In foo.h */
void foo();
/* In foo.c */
void foo() {
  int i = 3;
  printf("i value: %d\n", i);
}
/* In caller.c */
#include "foo.h"
foo(3);
```
## Compliant Solution (Ambiguous Interface)
In this compliant solution, `void` is specified explicitly as a parameter in the declaration of `foo`'s prototype:
``` c
/* In foo.h */
void foo(void);
/* In foo.c */
void foo(void) {
  int i = 3;
  printf("i value: %d\n", i);
}
/* In caller.c */
#include "foo.h"
foo(3);
```
## Implementation Details (Ambiguous Interface)
When the compliant solution is used and `foo(3)` is called, the GCC compiler issues the following diagnostic, which alerts the programmer about the misuse of the function interface:
``` java
error: too many arguments to function "foo"
```
## Noncompliant Code Example (Information Outflow)
Another possible vulnerability is the leak of privileged information. In this noncompliant code example, a user with high privileges feeds some secret input to the caller that the caller then passes to `foo()`. Because of the way `foo()` is defined, we might assume there is no way for `foo()` to retrieve information from the caller. However, because the value of `i` is really passed into a stack (before the return address of the caller), a malicious programmer can change the internal implementation and copy the value manually into a less privileged file.
``` c
/* Compile using gcc4.3.3 */
void foo() {
  /* 
   * Use assembly code to retrieve i
   * implicitly from caller
   * and transfer it to a less privileged file.
   */
}
...
/* Caller */
foo(i); /* i is fed from user input */
```
## Compliant Solution (Information Outflow)
``` c
void foo(void) {
  int i = 3;
  printf("i value: %d\n", i);
}
```
Again, the simplest solution is to explicitly specify `void` as the only parameter.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL20-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | empty-parameter-list | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL20 |  |
| CodeSonar | 8.3p0 | LANG.FUNCS.PROT | Incomplete function prototype |
| Helix QAC | 2024.4 | C3001, C3007 |  |
| Klocwork | 2024.4 | MISRA.FUNC.NO_PARAMS |  |
| LDRA tool suite | ;9.7.1 | 63 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL20-a | The number of arguments passed to a function shall match the number of parameters |
| PC-lint Plus | 1.4 | 937 | Partially supported |
| RuleChecker | 24.04 | empty-parameter-list | Fully checked |
| SonarQube C/C++ Plugin | ;3.11 | ;S929 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL30-C).
## Related Guidelines
In C++, `foo()` and `foo(void)` have exactly the same meaning and effect, so this rule doesn't apply to C++. However, `foo(void)` should be declared explicitly instead of `foo()` to distinguish it from `foo(...)`, which accepts an arbitrary number and type of arguments.

|  |  |
| ----|----|
| MISRA C:2012 | Rule 8.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.7.6.3, "Function Declarators (including Prototypes)"Subclause 6.11.6, "Function Declarators" |
| [TIGCC, void usage] | Manual, "C Language Keywords": void |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152335) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152320)
## Comments:

|  |
| ----|
| You don't want to explain this rule only in terms of what GCC may or may not do, but in terms of what the standard allows and disallows and what implementations may or may not do.  For example:
If the caller calls foo(3) again, a warning message will be issued as follows:
Not all compilers will issue a warning message, especially this particular warning message.
If you want to back this up with specific examples about what a particular implementation does, you should put this into an "implementation details" section.
                                        Posted by rcs_mgr at Nov 05, 2009 18:00
                                     |
| I think you did the math wrong in calculating the priority.  Also, I think this is a low / unlikely / low rule.
The related vulnerabilities does not mean links to related guidelines.  This is a very formulaic section that searches for vulnerabilities related to violations of this coding guideline in the CERT vulnerability notes knowledge base.
                                        Posted by rcs_mgr at Nov 05, 2009 18:07
                                     |
| If it is medium / probable / low, shouldn't it be 2*2*3 = 12?
I label it as medium in severity because of possible information outflow which matches with "unintentional information disclosure". 
I will revert the vul part.
                                        Posted by fhe at Nov 05, 2009 18:15
                                     |
| Thanks for your input. I've looked at C99-TC2 and it only says "type void as the only item in the list specifies that the function has no parameters." So it actually has no requirement on what compiler should do in case void is specified and foo(3) is called (like require a warning msg).
So my question is what can I say in this case given the fact the warning msg should not be referenced?
Thanks
                                        Posted by fhe at Nov 05, 2009 18:30
                                     |
| 
    I wonder if this rule should be merged into DCL17-C? (It's a valid rule for this assignment, this is just a quandary for the long-term.)
    The text in the NCCE and CCE sections should precede the code.
    In the 2nd NCCE, I wonder about the validity of doing static analysis on a function that performs assembly code. Assembly code pretty much invalidates any static analysis.
    Normally the 'Other Languages' section is for citing versions of this rule in C++ or Java, not saying 'no rule is necessary'. I like the text that is currently there, but this text should probably move to the Introduction section. I'll agree we need no corresponding C++ rule, but only because people don't habitually mix foo(...) and foo(void) in C++.
    If you have information about how GCC or some other compiler handles the NCCEs, you can provide it in an 'Implementation Details' section. This helps lend credence to the rule.
    Also if you know the section of C99 that discusses foo() vs foo(void), a citation and quote of the relevant text also lends credence to the rule.
                                        Posted by svoboda at Nov 06, 2009 07:19
                                     |
| I've changed the rule accordingly. Unfortunately, I was not able to find detailed explanation of foo() vs foo(void) in C99 standard, but from some other website (see citation).
                                        Posted by fhe at Nov 06, 2009 11:16
                                     |
| Thanks for the citation...I'm not surprised this isn't explicitly stated in C99. I'd say this rule is now complete.
                                        Posted by svoboda at Nov 06, 2009 15:36
                                     |
| The following sentence quoted from the description of this guideline isn't quite accurate:
Many compilers today still allow implicitly declared functions, even though C99 has eliminated them.
C99 still allows calling functions without a prototype. For example, 6.5.2.2 Function calls, says:
If the expression that denotes the called function has a type that does not include a prototype, the integer promotions are performed on each argument, and arguments that have type float are promoted to double.
I suspect the sentence meant to refer to an empty list in a function declarator that is not part of a definition as discussed below.
The difference between f(void) and f() is described in 6.7.5.3 Function declarators (including prototypes), paragraph 14:
An identifier list declares only the identifiers of the parameters of the function. An empty list in a function declarator that is part of a definition of that function specifies that the function has no parameters. The empty list in a function declarator that is not part of a definition of that function specifies that no information about the number or types of the parameters is supplied.124)
124) See "future language directions" (6.11.6).
Section 6.11.6 Function declarators, states that
The use of function declarators with empty parentheses (not prototype-format parameter type declarators) is an obsolescent feature.
                                        Posted by martinsebor at Mar 04, 2010 23:32
                                     |
| Since this page is not tagged with the "not-for-cpp" label, and this recommendation does not appear on the Relation to the CERT C Coding Standard;page, it seems implied that this standard is meant to apply to C++.I was unable to find any language in the Working Draft of the "Standard for Programming Language C++" similar to the C Standard quoted in this article, and I couldn't find any. In fact, the C++ Standard itself often uses declarations likeint main() {  C a;  C b = a;  b = a;}Given this, shouldn't this article be given the "not-for-cpp" label?
                                        Posted by brian.szuter at Oct 30, 2014 15:04
                                     |

