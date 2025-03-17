Evaluation of an expression may produce [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect). At specific points during execution, known as [sequence points](BB.-Definitions_87152273.html#BB.Definitions-sequencepoint), all side effects of previous evaluations are complete, and no side effects of subsequent evaluations have yet taken place. Do not depend on the order of evaluation for side effects unless there is an intervening sequence point.
The C Standard, 6.5, paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> If a side effect on a scalar object is unsequenced relative to either a different side effect on the same scalar object or a value computation using the value of the same scalar object, the behavior is undefined. If there are multiple allowable orderings of the subexpressions of an expression, the behavior is undefined if such an unsequenced side effect occurs in any of the orderings.

This requirement must be met for each allowable ordering of the subexpressions of a full expression; otherwise, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 34](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_34).)
The following sequence points are defined in the C Standard, Annex C \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
-   Between the evaluations of the function designator and actual arguments in a function call and the actual call
-   Between the evaluations of the first and second operands of the following operators:
    -   Logical AND: `&&`
    -   Logical OR: `||`
    -   Comma: **`,`**
-   Between the evaluations of the first operand of the conditional `?:` operator and whichever of the second and third operands is evaluated
-   The end of a full declarator
-   Between the evaluation of a full expression and the next full expression to be evaluated; the following are full expressions:
    -   An initializer that is not part of a compound literal
    -   The expression in an expression statement
    -   The controlling expression of a selection statement (`if `or `switch`)
    -   The controlling expression of a `while` or `do` statement
    -   Each of the (optional) expressions of a `for` statement
    -   The (optional) expression in a `return` statement
-   Immediately before a library function returns
-   After the actions associated with each formatted input/output function conversion specifier
-   Immediately before and immediately after each call to a comparison function, and also between any call to a comparison function and any movement of the objects passed as arguments to that call
Furthermore, Section 6.5.17.1, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\] says (regarding assignment operations):
> The side effect of updating the stored value of the left operand is sequenced after the value computations of the left and right operands. 

This rule means that statements such as
``` c
i = i + 1;
a[i] = i;
```
have defined behavior, and statements such as the following do not:
``` c
/* i is modified twice between sequence points */
i = ++i + 1;  
/* i is read other than to determine the value to be stored */
a[i++] = i;   
```
Not all instances of a comma in C code denote a usage of the comma operator. For example, the comma between arguments in a function call is not a sequence point. However, according to the C Standard, 6.5.3.3, paragraph 8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]
> Every evaluation in the calling function (including other function calls) that is not otherwise specifically sequenced before or after the execution of the body of the called function is indeterminately sequenced with respect to the execution of the called function.

This rule means that the order of evaluation for function call arguments is unspecified and can happen in any order.
## Noncompliant Code Example
Programs cannot safely rely on the order of evaluation of operands between sequence points. In this noncompliant code example, `i` is evaluated twice without an intervening sequence point, so the behavior of the expression is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <stdio.h>
void func(int i, int *b) {
  int a = i + b[++i];
  printf("%d, %d", a, i);
}
```
## Compliant Solution
These examples are independent of the order of evaluation of the operands and can be interpreted in only one way:
``` c
#include <stdio.h>
void func(int i, int *b) {
  int a;
  ++i;
  a = i + b[i];
  printf("%d, %d", a, i);
}
```
Alternatively:
``` java
#include <stdio.h>
void func(int i, int *b) {
  int a = i + b[i + 1];
  ++i;
  printf("%d, %d", a, i);
}
```
## Noncompliant Code Example
The call to `func()` in this noncompliant code example has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because there is no sequence point between the argument expressions:
``` c
extern void func(int i, int j);
void f(int i) {
  func(i++, i);
}
```
The first (left) argument expression reads the value of `i` (to determine the value to be stored) and then modifies `i`. The second (right) argument expression reads the value of `i` between the same pair of sequence points as the first argument, but not to determine the value to be stored in `i`. This additional attempt to read the value of `i` has undefined behavior.
## Compliant Solution
This compliant solution is appropriate when the programmer intends for both arguments to `func()` to be equivalent:
``` c
extern void func(int i, int j);
void f(int i) {
  i++;
  func(i, i);
}
```
This compliant solution is appropriate when the programmer intends for the second argument to be 1 greater than the first:
``` c
extern void func(int i, int j);
void f(int i) {
  int j = i++;
  func(j, i);
}
```
## Noncompliant Code Example
The order of evaluation for function arguments is unspecified. This noncompliant code example exhibits [unspecified behavior](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior) but not [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
extern void c(int i, int j);
int glob;
int a(void) {
  return glob + 10;
}
int b(void) {
  glob = 42;
  return glob;
}
void func(void) {
  c(a(), b());
}
```
It is unspecified what order `a()` and `b()` are called in; the only guarantee is that both `a()` and `b()` will be called before `c()` is called. If `a()` or `b()` rely on shared state when calculating their return value, as they do in this example, the resulting arguments passed to `c()` may differ between compilers or architectures.
## Compliant Solution
In this compliant solution, the order of evaluation for `a()` and `b()` is fixed, and so no unspecified behavior occurs:
``` c
extern void c(int i, int j);
int glob;
int a(void) {
  return glob + 10;
}
int b(void) {
  glob = 42;
  return glob;
}
void func(void) {
  int a_val, b_val;
  a_val = a();
  b_val = b();
  c(a_val, b_val);
}
```
## Risk Assessment
Attempting to modify an object multiple times between sequence points may cause that object to take on an unexpected value, which can lead to [unexpected program behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP30-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | evaluation-ordermultiple-volatile-accesses | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP30 |  |
| Clang | 3.9 | -Wunsequenced | Detects simple violations of this rule, but does not diagnose unsequenced function call arguments. |
| CodeSonar | 8.3p0 | LANG.STRUCT.SE.DECLANG.STRUCT.SE.INC
LANG.STRUCT.SE.INIT | Side Effects in Expression with DecrementSide Effects in Expression with Increment
Side Effects in Initializer List |
| Compass/ROSE |  |  | Can detect simple violations of this rule. It needs to examine each expression and make sure that no variable is modified twice in the expression.;It also must check that no variable is modified once, then read elsewhere, with the single exception that a variable may appear on both the left and right of an assignment operator |
| Coverity | 2017.07 | EVALUATION_ORDER | Can detect the specific instance where a statement contains multiple side effects on the same value with an undefined evaluation order because, with different compiler flags or different compilers or platforms, the statement may behave differently |
| Cppcheck | ;2.15 | unknownEvaluationOrder |  |
| Cppcheck Premium | 24.11.0 | unknownEvaluationOrder |  |
| ECLAIR | 1.2 | CC2.EXP30 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violations of this rule when the -Wsequence-point flag is used |
| Helix QAC | 2024.4 | C0400, C0401, C0402, C0403, C0404, C0405 | Fully implemented |
| Klocwork | 2024.4 | PORTING.VAR.EFFECTSMISRA.INCR_DECR.OTHER | Fully implemented |
| LDRA tool suite | 9.7.1 | 35 D, 1 Q, 9 S, 30 S, 134 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP30-aCERT_C-EXP30-b
CERT_C-EXP30-c
CERT_C-EXP30-d | The value of an expression shall be the same under any order of evaluation that the standard permitsDon't write code that depends on the order of evaluation of function arguments
Don't write code that depends on the order of evaluation of function designator and function arguments
Don't write code that depends on the order of evaluation of expression that involves a function call |
| PC-lint Plus | 1.4 | 564 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP30-C | Checks for situations when expression value depends on order of evaluation or of side effects (rule partially covered) |
| PVS-Studio | 7.35 | V532,;V567 |  |
| RuleChecker | 24.04 | evaluation-ordermultiple-volatile-accesses | Fully checked |
| Splint | 3.1.1 |  |  |
| SonarQube C/C++ Plugin | 3.11 | IncAndDecMixedWithOtherOperators |  |
| TrustInSoft Analyzer | 1.38 | separated | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | EXP50-CPP. Do not depend on the order of evaluation for side effects | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | EXP05-J. Do not follow a write by a subsequent write or read of the same object within an expression | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Operator Precedence/Order of Evaluation [JCW] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Side-effects and Order of Evaluation [SAM] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 13.2 (required) | CERT cross-reference in MISRA C:2012 – Addendum 3 |
| CWE 2.11 | CWE-758 | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-758 and EXP30-C
Independent( INT34-C, INT36-C, MEM30-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( EXP30-C, list) where list =
-   Undefined behavior that results from anything other than reading and writing to a variable twice without an intervening sequence point.
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Annex C, "Sequence Points" |
| [ISO/IEC 9899:2024] | 6.5, "Expressions"6.5.17.1, "Assignment Operators"6.5.3.3, "Function Calls" |
| [Saks 2007] |  |
| [Summit 2005] | Questions 3.1, 3.2, 3.3, 3.3b, 3.7, 3.8, 3.9, 3.10a, 3.10b, and 3.11 |

------------------------------------------------------------------------
[](../c/Rule%2003_%20Expressions%20_EXP_) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152412)
## Comments:

|  |
| ----|
| HiI dont get the reason why this is a rule and not only a rec.Jérôme
                                        Posted by jerome.guy at Mar 27, 2018 04:51
                                     |
| Because this satisfies all the requirements of a rule (see;Rules versus Recommendations for these requirements):  Violating this rule leads to undefined behavior. And violations of the rule can typically be detected by static-analysis tools.
                                        Posted by svoboda at Mar 27, 2018 09:01
                                     |
| Hi.There is a similar situation regarding evaluation, for example:
void *foo(char *p) {
  void *bar;
  if (!p)
    return NULL;
  if (!(bar = malloc(/* ... */)))
    /* handle out of memory */
  return bar;
}

I've used it, but I'm not sure if it is OK for best practices. :-/ The code below has the same effects:
    void *foo(char *p) {
      void *bar;
      if (!p)
        return NULL;
      bar = malloc(/* ... */);
      if (!bar)
        /* handle out of memory */
      return bar;
    }
![](images/icons/contenttypes/comment_16.png) Posted by silvioprog at Aug 20, 2018 00:10
\| \|
The MISRA reference to 12.1 (advisory) is wrong and should be replaced with 13.2 (required).
The topic of MISRA rule 12.1 is precedence while 13.2 deals with side effects and orders of evaluations.
![](images/icons/contenttypes/comment_16.png) Posted by stefanct at Aug 22, 2018 07:55
\| \|
Fixed
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 22, 2018 11:13
\| \|
In this example of undefined behavior:
`/* i is modified twice between sequence points */`
`i = ++i + 1;`
Would it constitute valid defined behavior if it were written like this instead? :
i = (++i, i+1);
Similarly the following example:
`/* i is read other than to determine the value to be stored */`
`a[i++] = i;`
if it were instead written as:
a\[i++\] = (0, i);
Does the usage of the comma operator now allow both of these to execute with defined behavior?
(The question is to ensure my understanding, not to indicate that someone should actually code it like this).
![](images/icons/contenttypes/comment_16.png) Posted by stevecom2 at May 18, 2020 12:39
\| \|
> Would it constitute valid defined behavior if it were written like this instead? :
>
> i = (++i, i+1);

In this case you have a sequence point between the ++i and i+1. However there is nothing to dictate the sequence between these two expressions and the assignment. So this expression is still undefined behavior.
> if it were instead written as:
>
> a\[i++\] = (0, i);
>
> Does the usage of the comma operator now allow both of these to execute with defined behavior?

The answer is the same, your , operator has sequenced two expressions, but has not sequenced the 'i' with the i++. So this expression is also undefined.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2020 12:56
\| \|
Thank your for your quick reply.
I think the problem with the assignment portion of this is still unclear to me.
Had the first statement instead have been:
int j = ++i +1;
or even:
int j = (++i, i+1);
Then these have defined behavior and the result is equivalent to having written:
++i;
int j = i + 1;
We expect j to have the correct value after the statement. May I phrase it as "The value to assign to j is determined before it is assigned to j"? Why is it that if we also have i on the left of the assignment that it is possible that the "value to assign to it" is assigned before it is "determined"?
![](images/icons/contenttypes/comment_16.png) Posted by stevecom2 at May 18, 2020 13:26
\| \|
The important idea is that there is no sequence point between the left and right sides of an assignment expression. This means you can't write to i on both sides, and doing a read on one side and a write on the other is also undefined behavior.
As you suggest, if you replace i with j on one side of the assignment, your code becomes well-defined.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2020 13:29
\| \|
Okay.; Although we probably can't exactly state the second part of the generalization: "doing a read on one side and a write on the other is also undefined behavior" since this has defined behavior:
`i = i + 1;`
Thank you again for your help.
![](images/icons/contenttypes/comment_16.png) Posted by stevecom2 at May 18, 2020 13:52
\| \|
In expression "i = (++i, i+1)"
> 6.5.16/3;The side effect of updating the stored value of the left operand is  
> sequenced after the value computations of the left and right operands.

According to this, value of (++i, i+1) should be computed before the side effect of update. Value of this expession is equal to second operand's value. Evaluation of second operand which includes value computation and initiation of side effects is sequenced after the evalutation of first operand of comma operator. That means before value computation of right operand of assignment expression, side effects of "++i" will occur. Which means that before updating the left operand of assigment operator will be incremented. That means there isn't a undefined behaviour.
![](images/icons/contenttypes/comment_16.png) Posted by ulutaseray at Dec 02, 2020 04:13
\| \|
Thanks. I added the C citation to the intro for clarity.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 02, 2020 08:45
\|
