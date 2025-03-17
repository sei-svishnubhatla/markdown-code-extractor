Macro replacement lists should be parenthesized to protect any lower-precedence operators from the surrounding expression. See also [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros) and [PRE01-C. Use parentheses within macros around parameter names](PRE01-C_%20Use%20parentheses%20within%20macros%20around%20parameter%20names).
## Noncompliant Code Example
This `CUBE()` macro definition is noncompliant because it fails to parenthesize the replacement list:
``` c
#define CUBE(X) (X) * (X) * (X)
int i = 3;
int a = 81 / CUBE(i);
```
As a result, the invocation
``` c
int a = 81 / CUBE(i);
```
expands to
``` c
int a = 81 / i * i * i;
```
which evaluates as
``` c
int a = ((81 / i) * i) * i);  /* Evaluates to 243 */
```
which is not the desired behavior.
## Compliant Solution
With its replacement list parenthesized, the `CUBE()` macro expands correctly for this type of invocation.
``` c
#define CUBE(X) ((X) * (X) * (X))
int i = 3;
int a = 81 / CUBE(i);
```
This compliant solution violates [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros). Consequently, this solution would be better implemented as an inline function.
## Noncompliant Code Example
In this noncompliant code example, `END_OF_FILE` is defined as `-1`. The macro replacement list consists of a unary negation operator followed by an integer literal 1:
``` c
#define END_OF_FILE -1
/* ... */
if (getchar() END_OF_FILE) {
   /* ... */
}
```
In this example, the programmer has mistakenly omitted the comparison operator from the conditional statement, which should be `getchar() != END_OF_FILE`. (See [void MSC02-C. Avoid errors of omission](void%20MSC02-C_%20Avoid%20errors%20of%20omission).) After macro expansion, the conditional expression is incorrectly evaluated as a binary operation: `getchar()-1`. This statement is syntactically correct, even though it is certainly not what the programmer intended. Note that this example also violates [DCL00-C. Const-qualify immutable objects](DCL00-C_%20Const-qualify%20immutable%20objects).
Parenthesizing the `-1` in the declaration of `END_OF_FILE` ensures that the macro expansion is evaluated correctly:
``` java
#define END_OF_FILE (-1)
```
Once this modification is made, the noncompliant code example no longer compiles because the macro expansion results in the conditional expression `getchar() (-1)`, which is no longer syntactically valid. Note that there must be a space after `END_OF_FILE` because, otherwise, it becomes a [function-like macro](BB.-Definitions_87152273.html#BB.Definitions-function-likemacro) (and one that is incorrectly formed because −1 cannot be a formal parameter).
## Compliant Solution
In this compliant solution, the macro definition is replaced with an enumeration constant in compliance with [DCL00-C. Const-qualify immutable objects](DCL00-C_%20Const-qualify%20immutable%20objects). In addition, because `EOF` is a reserved macro defined in the `<stdio.h>` header, the compliant solution must also use a different indentifier in order to comply with [DCL37-C. Do not declare or define a reserved identifier](DCL37-C_%20Do%20not%20declare%20or%20define%20a%20reserved%20identifier).
``` c
enum { END_OF_FILE = -1 };
/* ... */
if (getchar() != END_OF_FILE) {
   /* ... */
}
```
## Exceptions
**PRE02-C-EX1:** A macro that expands to a single identifier or function call is not affected by the precedence of any operators in the surrounding expression, so its replacement list need not be parenthesized.
``` java
#define MY_PID getpid()
```
**PRE02-C-EX2:** A macro that expands to an array reference using the array-subscript operator `[]`, or an expression designating a member of a structure or union object using either the member-access `.` or `->` operators is not affected by the precedence of any operators in the surrounding expression, so its replacement list need not be parenthesized.
``` java
#define NEXT_FREE block->next_free
#define CID customer_record.account.cid
#define TOOFAR array[MAX_ARRAY_SIZE]
```
## Risk Assessment
Failing to parenthesize macro replacement lists can cause unexpected results.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE02-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE02 |  |
| CodeSonar | 8.3p0 | LANG.PREPROC.MACROENDLANG.PREPROC.MACROSTART | Macro Does Not End With ) or }Macro Does Not Start With ( or;{ |
| ECLAIR | 1.2 | CC2.PRE02 | Fully implemented |
| Helix QAC | 2024.4 | C3409 |  |
| Klocwork | 2024.4 | MISRA.DEFINE.BADEXP |  |
| LDRA tool suite | 9.7.1 | 77 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE02-a | Enclose the entire definition of a function-like macro in parentheses |
| PC-lint Plus | 1.4 | 773, 973 | Fully supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE02-CPP. Macro replacement lists should be parenthesized |
| ISO/IEC TR 24772:2013 | Operator Precedence/Order of Evaluation [JCW]Pre-processor Directives [NMP] |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] | Rule 1-1 |
| [Summit 2005] | Question 10.1 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152393) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152383)
## Comments:

|  |
| ----|
| This will disable use of macros which are intended to produce concatenable tokens, for the purposes of name generation.
;The reason why we want this, is because sometimes we /have/ to use more than one layer of concatenating macros, just to be able to get the parameter->value mapping we desire.
                                        Posted by _deepfire at Mar 15, 2008 12:26
                                     |
| I'm sympathetic to this comment.  Can you write an example demonstrating this usage?
                                        Posted by rcs at May 04, 2008 05:26
                                     |
| By defining EOF (reserved in <stdio.h>), the second Compliant Solution violates DCL37-C. Do not use identifiers that are reserved for the implementation, bullet 3.
Regarding PRE02-EX1: I'm inclined to discourage the practice of defining object macros that expand to function calls because doing so makes it easy to confuse the macro for an object and introduce subtle bugs. Consider:
#define MY_PID getpid()
int *pid = &MY_PID;   /* error: cannot take the address of rvalue */
#define val compute_value(bunch, of, arguments)
#define min(a, b) ((a) < (b) ? (a) : (b))   /* unsafe macro */
int min_value = min(val, x);   /* whoops! argument 1 has (hidden) side effects */

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 19, 2010 22:15
\| \|
EOF is definitely a problem. Ideally we can replace this with some other function that returns -1 and `#define FUNC_ERROR -1`.
Still thinking about the second part of your comment. We have other guidelines which all suggest alternatives to macros. This one is sort of a "defense-in-depth" guideline about parenthesizing macro replacement lists (consistent with the CSCG SG decision that guidelines should be independent).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 21, 2010 08:04
\| \|
The subtle bugs in Martin's sample code can be fixed by using a no-arg function macro:
``` java
#define MY_PID() getpid()
int *pid = &MY_PID();   /* clearly an error: cannot take the address of rvalue */
#define val() compute_value(bunch, of, arguments)
#define min(a, b) ((a) < (b) ? (a) : (b))   /* unsafe macro, but conventional */
int min_value = min(val(), x);   /* clearly unsafe macro called with side effects */
```
Perhaps we should warn against using non-function macros to represent functions? Recommend that macros whose definitions involve side effects or function calls be implemented as f unction macros (possibly with zero arguments).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 21, 2010 11:30
\| \|
The solution of parenthesizing suggested in the second NCE (EOF example) could perhaps be separated as a CS because it prevents the vulnerability? That way the NCE can only talk about the problem and the CS can also insert the missing =.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Mar 06, 2010 00:55
\| \|
Another reason to remove the exceptions and require that the definitions of all macros be parenthesized is [Defect Report #017](http://www.open-std.org/jtc1/sc22/wg14/docs/rr/dr_017.html) which clarifies that
> If a fully expanded macro replacement list contains a function-like macro name as its last preprocessing token, it is unspecified whether this macro name may be subsequently replaced. If the behavior of the program depends upon this unspecified behavior, then the behavior is undefined.

Consider the following snippet:
``` java
#define getpid() pid
#define MY_PID getpid()
#define pid() huh?
void f() {
  int id = MY_PID();
}
```
Since the `MY_PID` macro expands to the name of the function-like macro `pid` and the next token is `(` the behavior of the program is undefined.
This would not be the case if the definition of `MY_PID` (or the definition of `getpid()`) were enclosed in parentheses.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 06, 2011 14:53
\|
