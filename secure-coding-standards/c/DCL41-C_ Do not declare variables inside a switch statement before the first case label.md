According to the C Standard, 6.8.5.3, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> A switch statement causes control to jump to, into, or past the statement that is the switch body, depending on the value of a controlling expression, and on the presence of a default label and the values of any case labels on or in the switch body. A case or default label is accessible only within the closest enclosing switch statement.

If a programmer declares variables, initializes them before the first case statement, and then tries to use them inside any of the case statements, those variables will have scope inside the `switch` block but will not be initialized and will consequently contain indeterminate values.  Reading such values also violates [EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory).
## Noncompliant Code Example
This noncompliant code example declares variables and contains executable statements before the first case label within the `switch` statement:
``` c
#include <stdio.h>
extern void f(int i);
void func(int expr) {
  switch (expr) {
    int i = 4;
    f(i);
  case 0:
    i = 17;
    /* Falls through into default code */
  default:
    printf("%d\n", i);
  }
}
```
### Implementation Details
When the preceding example is executed on GCC 4.8.1, the variable `i` is instantiated with automatic storage duration within the block, but it is not initialized. Consequently, if the controlling expression `expr` has a nonzero value, the call to `printf()` will access an indeterminate value of `i`. Similarly, the call to `f()` is not executed.

| Value of expr
 | Output |
| ----|----|
| 0 | 17 |
| Nonzero | Indeterminate |

## Compliant Solution
In this compliant solution, the statements before the first case label occur before the `switch` statement:
``` c
#include <stdio.h>
extern void f(int i);
int func(int expr) {
  /*
   * Move the code outside the switch block; now the statements
   * will get executed.
   */
  int i = 4;
  f(i);
  switch (expr) {
    case 0:
      i = 17;
      /* Falls through into default code */
    default:
      printf("%d\n", i);
  }
  return 0;
}
```
## Risk Assessment
Using test conditions or initializing variables before the first case statement in a `switch` block can result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL41-C | Medium | Unlikely | Medium | P4 | L3 |

## Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | switch-skipped-code | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL41 | Fully implemented |
| Clang | 3.9 | -Wsometimes-uninitialized |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.SW.BAD | Malformed switch Statement |
| Coverity | 2017.07 | MISRA C 2004 Rule 15.0MISRA C 2012 Rule 16.1 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl41-c |  |
| Helix QAC | 2024.4 | C2008, C2882, C3234 | Fully implemented |
| Klocwork | 2024.4 | CERT.DCL.SWITCH.VAR_BEFORE_CASE | Fully implemented |
| LDRA tool suite | ;9.7.1 | 385 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL41-a | A switch statement shall only contain switch labels and switch clauses, and no other code |
| PC-lint Plus | 1.4 | 527 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL41-C | Checks for ill-formed switch statements (rule partially covered) |
| PVS-Studio | 7.35 | V622 |  |
| RuleChecker | 24.04 | switch-skipped-code | Fully checked |
| TrustInSoft Analyzer | 1.38 | initialisation | Exhaustively detects undefined behavior (see the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL41-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| MISRA C:2012 | Rule 16.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.8.5.3, "The switch Statement" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151998) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](../c/Rule%2003_%20Expressions%20_EXP_)
## Comments:

|  |
| ----|
| Should this be cross referenced with avoid dead code?
                                        Posted by rcs_mgr at Nov 05, 2009 18:26
                                     |
| Offhand, I think this should be incorporated into that rule. MSC07-C. Detect and remove dead code.  (I'd still consider this a complete rule for the purposes of this assignment.)
Also the 'Implmenetation Details' section needs  to specify which platform produced the results shown here.
                                        Posted by svoboda at Nov 06, 2009 06:52
                                     |
| Under Implementation Details, should this sentence
Similarly, the call to the function will never be executed either.
say
Similarly, the call to function f will never be executed either.
instead? 
                                        Posted by pw at Dec 08, 2009 13:46
                                     |
| He is definitely referring to the function f().  I'm not sure about the sentence.  Maybe something like "Similarly, the call to f() is not executed.".  
                                        Posted by rcs_mgr at Dec 08, 2009 15:13
                                     |
| This rule seems to be written more broadly than the actual problem. Consider this silly example:switch(x) {    int y;
case 1:
    y = 10;
    f(&y);
    /* FALLTHROUGH */
case 2:
    y = 20;
    g(&y);
}

That's perfectly fine, though a bit strange-looking. Shouldn't our rule just be to not initialize variables before the first case statement, rather than to not declare them there?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 13:01
\| \|
Well, we have a rule [EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory).; I've cited EXP33-C in the introduction.
I'd say this is still a rule because no one has seriously tried to argue that declaring variables before the first case label is useful. Your code example is safe, but also silly, and it is easy to fix. Do you have a non-silly instance of code that would justify demoting this to a recommendation?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 12:32
\| \|
Is it easy to fix, though? The "obvious" fix of moving `y` out of the switch;statement would violate [DCL19-C. Minimize the scope of variables and functions](DCL19-C_%20Minimize%20the%20scope%20of%20variables%20and%20functions). (I'll also try to come up with a less silly example, but I don't have one offhand.)
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 02, 2020 12:37
\| \|
Also, to clarify, my first choice with this rule wouldn't be to demote it to recommendation. I'd rather keep it a rule, but change it to only ban initialization there, and to allow declaration without initialization.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 02, 2020 12:42
\| \|
The rules are more important than the recommendations. Violating a recommendation is permitted, especially if the alternative is to violate a rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 13:20
\| \|
Personally, upon seeing your comment, my impulse was to fold this rule into EXP33-C, because if your code is not safe, then it violates that rule. This rule suggests that safe code, such as your silly example, is still insecure, because it could easy lead to reading uninitialized memory. Again, I would want to see a serious argument (aka non-silly code example) that would justify changing or demoting this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 13:25
\|
