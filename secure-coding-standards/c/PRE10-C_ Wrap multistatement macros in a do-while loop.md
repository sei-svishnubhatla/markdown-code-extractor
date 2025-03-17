Macros are often used to execute a sequence of multiple statements as a group.
Inline functions are, in general, more suitable for this task (see [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros)). Occasionally, however, they are not feasible (when macros are expected to operate on variables of different types, for example).
When multiple statements are used in a macro, they should be bound together in a `do-while` loop syntactically, so the macro can appear safely inside `if` clauses or other places that expect a single statement or a statement block. Note that this is only effective if none of the multiple statements are `break` or `continue`, as they would be captured by the `do-while` loop. (Alternatively, when an `if`, `for`, or `while` statement uses braces even for a single body statement, then multiple statements in a macro will expand correctly even without a `do-while` loop (see [EXP19-C. Use braces for the body of an if, for, or while statement](EXP19-C_%20Use%20braces%20for%20the%20body%20of%20an%20if,%20for,%20or%20while%20statement)).
## Noncompliant Code Example
This noncompliant code example contains multiple, unbound statements:
``` c
/*
 * Swaps two values and requires
 * tmp variable to be defined.
 */
#define SWAP(x, y) \
  tmp = x; \
  x = y; \
  y = tmp
```
This macro expands correctly in a normal sequence of statements but not as the `then` clause in an `if` statement:
``` c
int x, y, z, tmp;
if (z == 0)
  SWAP(x, y);
```
It expands to the following, which is certainly not what the programmer intended:
``` c
int x, y, z, tmp;
if (z == 0)
  tmp = x;
x = y;
y = tmp;
```
Furthermore, this macro violates [PRE02-C. Macro replacement lists should be parenthesized](PRE02-C_%20Macro%20replacement%20lists%20should%20be%20parenthesized).
## Noncompliant Code Example
This noncompliant code example parenthesizes its macro arguments, but inadequately bounds multiple statements:
``` c
/*
 * Swaps two values and requires
 * tmp variable to be defined.
 */
#define SWAP(x, y) { tmp = (x); (x) = (y); (y) = tmp; }
```
This macro fails to expand correctly in some case, such as the following example, which is meant to be an `if` statement with two branches:
``` c
if (x > y)
  SWAP(x, y);          /* Branch 1 */
else  
  do_something();     /* Branch 2 */
```
Following macro expansion, however, this code is interpreted as an `if` statement with only one branch:
``` c
if (x > y) { /* Single-branch if-statement!!! */
  tmp = x;   /* The one and only branch consists */
  x = y;     /* of the block. */
  y = tmp;
}
;            /* Empty statement */
else         /* ERROR!!! "parse error before else" */
  do_something();
```
The problem is the semicolon (`;`) following the block.
## Compliant Solution
Wrapping the macro inside a `do-while` loop mitigates the problem:
``` c
/*
 * Swaps two values and requires
 * tmp variable to be defined.
 */
#define SWAP(x, y) \
  do { \
    tmp = (x); \
    (x) = (y); \
    (y) = tmp; } \
  while (0)
```
The `do-while` loop will always be executed exactly once.
This macro still violates the recommendation [PRE12-C. Do not define unsafe macros](PRE12-C_%20Do%20not%20define%20unsafe%20macros), because both macro arguments are evaluated twice. It is expected that the arguments are simple lvalues.
## Risk Assessment
Improperly wrapped statement macros can result in unexpected and difficult to diagnose behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE10-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE10 |  |
| Helix QAC | 2024.4 | C3412, C3458 |  |
| Klocwork | 2024.4 | MISRA.DEFINE.BADEXP |  |
| LDRA tool suite | 9.7.1 | 79 S | Enhanced enforcement |
| PC-lint Plus | 1.4 | 9502 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE10-C | Checks for macros with multiple statements (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE10-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Pre-processor Directives [NMP] |

## Bibliography

|  |  |
| ----|----|
| Linux Kernel Newbies FAQ | FAQ/DoWhile0 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152166) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152265)
## Comments:

|  |
| ----|
| We could probably cite http://kernelnewbies.org/FAQ/DoWhile0
                                        Posted by avolkovi at Jun 09, 2008 15:36
                                     |
| One problem with this rule is the MSVC2008 issues a warning about a constant conditional expression (the 'while(0)' makes it think you did something wrong.)
I suppose this isn't a problem for Linux kernel developers, but how should Windows devs handle it?
                                        Posted by svoboda at Feb 18, 2009 15:57
                                     |
| Much simpler solution.; Require the usage of brackets around the if -else clauses.  Then, this poblem goes away (plus, the if-else clauses are easier to read anyways.)
                                        Posted by schilling at Mar 02, 2009 11:25
                                     |
| This is a good solution if you can enforce bracketed-clauses on everyone who uses your macros. For instance. if you are developing in-house software, or closed-source software, then your company can enforce bracketed clauses for the software's lifetime.
But if you cannot guarantee bracketed clauses from future devs, (which might happen if your company has no such policy, or you develop open-source software), this rule will still protect your multi-statement macros.
                                        Posted by svoboda at Mar 02, 2009 17:15
                                     |
| Many developers understand why the first noncompliant example is wrong, but still think that e.g. #define SWAP(x,y) {tmp=x; x=y; y=tmp;} is fine, even though it fails as described at the kernelnewbies.org link above. It'd be useful to show a second noncompliant example that demonstrates why do...while is necessary, and not just { }.
                                        Posted by sgreen at Aug 20, 2009 16:43
                                     |
| OK, done.
                                        Posted by rcs at Aug 28, 2009 13:38
                                     |
| To be fair, MSVC only emits a diagnostic at /W4 or /Wall, which is rarely used in practice due to the verbosity vs quality of the diagnostics.; That being said, Microsoft turns this warning off in their header files when using this construct by doing #pragma warning(disable: 4127).
                                        Posted by aballman at Jun 06, 2013 11:30
                                     |
| Well, one of our rules is;MSC00-C. Compile cleanly at high warning levels. We could always list this is an exception to the rule. Or instruct devs to suppress the warning using your #pragma.
                                        Posted by svoboda at Jun 07, 2013 14:45
                                     |
| Would it make sense for a more comprehensive look at the list of warnings in /W4 and /Wall to list ones we feel are exceptions to the rule (or exceptional cases to the rule)?; Another one that immediately springs to mind is the conversion to bool performance warning with something like: 
bool func() { return 12; }

![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 07, 2013 14:53
\| \|
Probably not.;  1)  MSC00-C is a recommendation, not a rule.   2) it states "high warning levels", not necessarily the "highest warning levels".  3) It might make to add your observations concerning the usefulness of /W4 or /Wall on MSVC to MSC00-C.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 07, 2013 15:30
\| \|
The `SWAP()` macro example seems a bit contrived.; Such a macro would either declare a temporary (and use an extension like `__typeof__`  to determine its type from the arguments) or be implemented as an (inline) function.  Similarly, rather than enclosing the macro body in a `do { } while (0)` statement, a macro that didn't introduce a temporary would preferably be written as an expression: `(void)((tmp = (x)), ((x) = (y)), ((y) = tmp))`.  In fact, I'm having trouble thinking of a macro that couldn't be implemented as a series of comma expressions if it didn't need to introduce a temporary.  In addition, the compliant solution violates [PRE02-C](PRE02-C_%20Macro%20replacement%20lists%20should%20be%20parenthesized) by failing to parenthesize its macro arguments, and [PRE12-C](PRE12-C_%20Do%20not%20define%20unsafe%20macros) by evaluating each of the macro arguments twice.
Is there an example of a multistatement macro that has a fully compliant solution that cannot be replaced by either an inline function or a comma expression? (I.e., a solution that doesn't violate any other CERT rules?)
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 08, 2017 11:28
\| \|
I added some text regarding PRE02-C and PRE12-C compliance. Since they are both recommendations, compliance is a good idea but not strictly mandatory. ;I don't think the SWAP macro can be made compliant with PRE12-C.
Many C++ features, and C11 features, such as inline functions, seemed to be designed to replace and obsolete macros. Including SWAP().  Certainly, SWAP() would be better implemented as a type-generic inline function for C11 (and C++11). EDIT: This would lose the works-on-any-type part of SWAP, but you could wrap an int-SWAP, float-SWAP, etc. into one macro or inline-function. You could have true type genericity if you are willing to use memcpy() rather than assignment.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 09, 2017 12:12
\| \|
The text doesn't seem to warn that it's impossible to use `do;{ ... } while (0)` if the multi-line statement wrapped includes a `break` or `continue` statement which is intended to leave an enclosing loop.
(I acknowledge Martin Bonner who made me aware of this).
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 16, 2020 05:23
\| \|
What makes you think a 'break' or 'continue' statement breaks things?They do violate the spirit of the solution....the do...while is not intended to loop or permit early termination; it is merely a wrapper for code that should execute exactly once.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 16, 2020 09:56
\| \|
Consider this multi-line macro and its usage:
    _Bool isWorkDone(void);unsigned int sleep(unsigned int);
    #define CHEXIT() {\
      if (isWorkDone()) { \
        break; \
      } \
    }
    void f(void) {
      while (1) {
        CHEXIT();
        sleep(1);
      }
    }
The effect of work completion is that the eternal loop in `f()` terminates.
However, if the construct advocated here is employed, the code quietly fails, because the `break` exits the artificial `do`-loop used to group statements, rather than the loop enclosing the macro use:
    _Bool isWorkDone(void);
    unsigned int sleep(unsigned int);
    #define CHEXIT() do {\
      if (isWorkDone()) { \
        break; \
      } \
    } while (0)
    void f(void) {
      while (1) {
        CHEXIT();
        sleep(1);
      }
    }
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 16, 2020 10:27
\| \|
OK, I see your point. A multi-statement list that contains break or continue will have its semantics disrupted if placed within a do...while loop.; I added a statement in the intro qualifying that this solution is not intended for statements containing break or continue.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 17, 2020 11:53
\|
