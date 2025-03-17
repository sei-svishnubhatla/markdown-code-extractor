An [unsafe function-like macro](BB.-Definitions_87152273.html#BB.Definitions-unsafefunction-likemacro) is one that, when expanded, evaluates its argument more than once or does not evaluate it at all. Contrasted with function calls, which always evaluate each of their arguments exactly once, unsafe function-like macros often have unexpected and surprising effects and lead to subtle, hard-to-find defects (see [PRE31-C. Avoid side effects in arguments to unsafe macros](PRE31-C_%20Avoid%20side%20effects%20in%20arguments%20to%20unsafe%20macros)). Consequently, every [function-like macro](BB.-Definitions_87152273.html#BB.Definitions-function-likemacro) should evaluate each of its arguments exactly once. Alternatively and preferably, defining function-like macros should be avoided in favor of inline functions (see [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros)).
## Noncompliant Code Example (Multiple Argument Evaluation)
The most severe problem with [unsafe function-like macros](BB.-Definitions_87152273.html#BB.Definitions-unsafefunction-likemacro) is side effects of macro arguments, as shown in this noncompliant code example:
``` c
#define ABS(x) (((x) < 0) ? -(x) : (x))
void f(int n) {
  int m;
  m = ABS(++n);
  /* ... */
}
```
The invocation of the `ABS()` macro in this noncompliant code example expands to the following code. The resulting code has well-defined behavior but causes `n` to be incremented twice rather than once, which may be surprising to those unfamiliar with the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) of the macro or unaware that they are using a macro in the first place.
``` c
m = (((++n) < 0) ? -(++n) : (++n));
```
## Compliant Solution (Inline Function)
A possible and preferable compliant solution is to define an inline function with equivalent but unsurprising semantics:
``` c
inline int Abs(int x) {
  return x < 0 ? -x : x;
}
```
## Compliant Solution (Language Extension)
Some implementations provide language extensions that make it possible to define safe function-like macros, such as the macro `ABS()`, that would otherwise require evaluating their arguments more than once. For example, the GCC extension [Statements and Declarations in Expressions](http://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html#Statement-Exprs) makes it possible to implement the macro `ABS()` in a safe way. Note, however, that because relying on implementation-defined extensions introduces undesirable platform dependencies that may make the resulting code nonportable, such solutions should be avoided in favor of portable ones wherever possible (see [MSC14-C. Do not introduce unnecessary platform dependencies](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies)).
Another GCC extension known as *statement expression* makes it possible for the block statement to appear where an expression is expected. The statement expression extension establishes a scope (note the curly braces) and any declarations in it are distinct from those in enclosing scopes.
``` c
#define ABS(x) __extension__ ({ __typeof (x) __tmp = x; __tmp < 0 ? - __tmp : __tmp; })
```
## Risk Assessment
Defining an unsafe macro leads to invocations of the macro with an argument that has [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect), causing those side effects to occur more than once. [Unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) or [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) program behavior can result.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE12-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | macro-parameter-multipliedmacro-parameter-unused
 | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE12 |  |
| ECLAIR | 1.2 | CC2.PRE12 | Fully implemented |
| Helix QAC | 2024.4 | C3456 |  |
| LDRA tool suite | 9.7.1 | 562 S, 572 S, 35 D, 1 Q | Partially implemented |
| RuleChecker | 24.04 | macro-parameter-multipliedmacro-parameter-unused | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE33-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE10-CPP. Do not define unsafe macros |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152265) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151942)
## Comments:

|  |
| ----|
| I made this new guideline a rule but in hindsight I'm not confident that it meets all the criteria for a rule: notably, that violation of the coding practice is likely to result in a security flaw that may result in an exploitable vulnerability. I suspect an example could be devised such that it does result in an exploitable vulnerability but I haven't put any effort into coming up with one. If anyone is aware of such an example in the wild it'd be great to add it. Similarly, if someone feels strongly that this guideline should be a recommendation I won't object to changing its classification.
                                        Posted by martinsebor at Feb 05, 2010 11:28
                                     |
| I'll suggest that this be a recommendation. assert() is a good example of a useful, but unsafe macro. Furthermore, it is not the definition of an unsafe macro that produces a vul, but rather the usage of an unsafe macro (as described in [PRE31-C. Avoid side-effects in arguments to unsafe macros  PRE31-C. Avoid side-effects in arguments to unsafe macros].  As long as a developer knows a macro is unsafe, you're OK.
This would be a good recommendation, as we would prefer that new macros be safe.
                                        Posted by svoboda at Feb 05, 2010 13:29
                                     |
| Okay, I've relabeled it as recommendation. I haven't renamed it yet: the same question/suggestion as the one I made in comment Re: FIO00-C. Take care when creating format strings applies here.
                                        Posted by martinsebor at Feb 06, 2010 17:29
                                     |
| This new recommendation is not correctly linked into the arrow navigation. It's not possible to get to this page using navigation arrows (left, up and right arrows located after References section).
                                        Posted by esolosh@gmail.com at Apr 10, 2010 10:17
                                     |
| this should be fixed now. i also changed the id to be consistent with a recommendation.
                                        Posted by rcs_mgr at Apr 10, 2010 10:31
                                     |
| "#define ABS(x) ({__typeof (x) tmp = (x); tmp < 0 ? -tmp : tmp; })"This macro can be surprising if you have a local variable named tmp:"int tmp = -4;printf("%d\n", ABS(tmp));"ABS(tmp) expanded as:"({__typeof (tmp) tmp = (tmp); tmp < 0 ? -tmp : tmp; })"The declared variable tmp is used before initialization.
                                        Posted by ntysdd at Jan 21, 2014 13:58
                                     |
| I made a couple of quick changes including putting it in a block and using the reserved identifier.; We're focused on the rules right now (id's over 30).  Please review these first as they need to be completed this week!  We'll swing back to the recommendations once we are done....
                                        Posted by rcs_mgr at Jan 21, 2014 14:59
                                     |
| I can't find anything surprising any more.Maybe __tmp < 0 ? - __tmp : __tmpcan be rewritten as __tmp <= 0 ? 0 - __tmp : __tmpin case floating point minus zero is a concern.;
                                        Posted by ntysdd at Jan 25, 2014 05:01
                                     |
| The initialization problem can be fixed without infringing on the reserved namespace by introducing a struct, like so:#define ABS(x) ({ struct { __typeof__ (x) x; } y; =  { x }; y.x < 0 ? -y.x : y.x; })
                                        Posted by martinsebor at Jan 26, 2014 22:18
                                     |

