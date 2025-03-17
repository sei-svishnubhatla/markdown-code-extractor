Do not use the assignment operator in the contexts listed in the following table because doing so typically indicates programmer error and can result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Operator | Context  |
| ----|----|
| if | Controlling expression |
| while | Controlling expression |
| do ... while | Controlling expression |
| for | Second operand |
| ?: | First operand |
| ?: | Second or third operands, where the ternary expression is used in any of these contexts |
| &&; | Either operand; |
| ||; | either operand; |
| , | Second operand, when the comma expression is used in any of these contexts |

Performing assignment statements in other contexts do not violate this rule. However, they may violate other rules, such as EXP30-C. Do not depend on the order of evaluation for side effects.
Noncompliant Code Example
In this noncompliant code example, an assignment expression is the outermost expression in an `if` statement:
``` c
if (a = b) {
  /* ... */
}
```
Although the intent of the code may be to assign `b` to `a` and test the value of the result for equality to 0, it is frequently a case of the programmer mistakenly using the assignment operator `=` instead of the equals operator `==`. Consequently, many compilers will warn about this condition, making this coding error detectable by adhering to [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).
## Compliant Solution (Unintentional Assignment)
When the assignment of `b` to `a` is not intended, the conditional block is now executed when `a` is equal to `b`:
``` c
if (a == b) {
  /* ... */
}
```
## Compliant Solution (Intentional Assignment)
When the assignment is intended, this compliant solution explicitly uses inequality as the outermost expression while performing the assignment in the inner expression:
``` c
if ((a = b) != 0) {
  /* ... */
}
```
It is less desirable in general, depending on what was intended, because it mixes the assignment in the condition, but it is clear that the programmer intended the assignment to occur.
## Noncompliant Code Example
In this noncompliant code example, the expression `x = y` is used as the controlling expression of the `while` statement:
``` c
 do { /* ... */ } while (foo(), x = y);
```
## Compliant Solution (Unintentional Assignment)
When the assignment of y to x is not intended, the conditional block should be executed only when x is equal to y, as in this compliant solution:
``` c
do { /* ... */ } while (foo(), x == y); 
```
## Compliant Solution (Intentional Assignment)
When the assignment is intended, this compliant solution can be used:
``` c
do { /* ... */ } while (foo(), (x = y) != 0);
```
## Compliant Solution (`for` statement)
The same result can be obtained using the `for` statement, which is specifically designed to evaluate an expression on each iteration of the loop, just before performing the test in its controlling expression. Remember that its controlling expression is the second operand, where the assignment occurs in its third operand:
``` c
 for (; x; foo(), x = y) { /* ... */ }
```
## Noncompliant Code Example
In this noncompliant example, the expression `p = q` is used as the controlling expression of the `while` statement:
``` c
 do { /* ... */ } while (x = y, p = q);
```
## Compliant Solution
In this compliant solution, the expression x = y is not used as the controlling expression of the while statement:
``` c
do { /* ... */ } while (x = y, p == q); 
```
## Noncompliant Code Example
This noncompliant code example has a typo that results in an assignment rather than a comparison.
``` c
while (ch = '\t' || ch == ' ' || ch == '\n') {
  /* ... */
}
```
Many compilers will warn about this condition. This coding error would typically be eliminated by adherence to [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels). Although this code compiles, it will cause [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) to an unsuspecting programmer. If the intent was to verify a string such as a password, user name, or group user ID, the code may produce significant [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) and require significant debugging.
## Compliant Solution (RHS Variable)
When comparisons are made between a variable and a literal or const-qualified variable, placing the variable on the right of the comparison operation can prevent a spurious assignment.
In this code example, the literals are placed on the left-hand side of each comparison. If the programmer were to inadvertently use an assignment operator, the statement would assign `ch` to `'\t'`, which is invalid and produces a diagnostic message.
``` c
while ('\t' = ch || ' ' == ch || '\n' == ch) {
  /* ... */
}
```
Due to the diagnostic, the typo will be easily spotted and fixed.
``` c
while ('\t' == ch || ' ' == ch || '\n' == ch) {
  /* ... */
}
```
As a result, any mistaken use of the assignment operator that could otherwise create a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) for operations such as string verification will result in a compiler diagnostic regardless of compiler, warning level, or [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation).
## Exceptions
**EXP45-C-EX1**:** **Assignment can be used where the result of the assignment is itself an operand to a comparison expression or relational expression. In this compliant example, the expression `x = y`  is itself an operand to a comparison operation:
``` c
if ((x = y) != 0) { /* ... */ } 
```
**EXP45-C-EX2**:** **Assignment can be used where the expression consists of a single primary expression. The following code is compliant because the expression  `x = y` is a single primary expression:
``` c
if ((x = y)) { /* ... */ } 
```
The following controlling expression is noncompliant because && is not a comparison or relational operator and the entire expression is not primary:
``` c
if ((v = w) && flag) { /* ... */ } 
```
When the assignment of v to w is not intended, the following controlling expression can be used to execute the conditional block when v is equal to w:
``` c
if ((v == w) && flag) { /* ... */ }; 
```
When the assignment is intended, the following controlling expression can be used:
``` c
if (((v = w) != 0) && flag) { /* ... */ }; 
```
EXP45-C-EX3: Assignment can be used in a function argument or array index. In this compliant solution, the expression `x = y` is used in a function argument:
``` c
if (foo(x = y)) { /* ... */ } 
```
## Risk Assessment
Errors of omission can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP45-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | assignment-conditional | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP45 |  |
| Clang | 3.9 | -Wparentheses | Can detect some instances of this rule, but does not detect all |
| CodeSonar | 8.3p0 | LANG.STRUCT.CONDASSIGLANG.STRUCT.SE.COND
LANG.STRUCT.USEASSIGN | Assignment in conditionalCondition contains side effects
Assignment result in expression |
| Compass/ROSE |  |  | Could detect violations of this recommendation by identifying any assignment expression as the top-level expression in an if or while statement |
| Cppcheck Premium | 24.11.0 | premium-cert-exp45-c |  |
| ECLAIR | 1.2 | CC2.EXP18CC2.EXP21 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violations of this recommendation when the -Wall flag is used |
| Helix QAC | 2024.4 | C3314, C3326, C3344, C3416C++4071, C++4074 |  |
| Klocwork | 2024.4 | ASSIGCOND.CALLASSIGCOND.GEN
MISRA.ASSIGN.COND |  |
| LDRA tool suite | 9.7.1 | 114 S, 132 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP45-bCERT_C-EXP45-d | Assignment operators shall not be used in conditions without bracketsAssignment operators shall not be used in expressions that yield a Boolean value |
| PC-lint Plus | 1.4 | 720 | Partially supported: reports Boolean test of unparenthesized assignment |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP45-C | Checks for invalid use of = (assignment) operator (rule fully covered) |
| PVS-Studio | 7.35 | V559, V633, V699 |  |
| RuleChecker | 24.04 | assignment-conditional | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | AssignmentInSubExpression |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP45-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | EXP19-CPP. Do not perform assignments in conditional expressions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | EXP51-J. Do not perform assignments in conditional expressions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Likely Incorrect Expression [KOA] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | No assignment in conditional expressions [boolasgn] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-480, Use of Incorrect Operator | 2017-07-05: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-481 | 2017-07-05: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-480 and EXP45-C
Intersection( EXP45-C, EXP46-C) = Ø
CWE-480 = Union( EXP45-C, list) where list =
-   Usage of incorrect operator besides s/=/==/
### CWE-569 and EXP45-C
CWE-480 = Subset( CWE-569)
## Bibliography

|  |  |
| ----|----|
| [Dutta 03] | "Best Practices for Programming in C" |
| [Hatton 1995] | Section 2.7.2, "Errors of Omission and Addition" |

------------------------------------------------------------------------
[](../c/EXP44-C_%20Do%20not%20rely%20on%20side%20effects%20in%20operands%20to%20sizeof,%20_Alignof,%20or%20_Generic) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152216)
## Comments:

|  |
| ----|
| The link to the C++ Secure Coding Standard equivalent is dead. I think this recommendation applies in C++ as well with the exception that C++ should allow for cases where a variable is declared in a conditional statement:
void f() {
  if (const char* const path = getenv("PATH")) {
    // use path
  }
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 25, 2010 13:18
\| \|
The C++ analogue to this rule never existed; that's why the link was dead ![](images/icons/emoticons/smile.svg) I have created the appropriate C++ rule (it is EXP19-CPP), and included your exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 25, 2010 14:09
\| \|
Thanks!
Btw., I changed the wording here a bit to align it with the terminology used by the standard since I believe we want to apply the rule to all selection statements (i.e., `if`, `switch`, `while`, `do`, and `for`).
If my assumption is correct I think we should rename the rule to "Do not perform assignments in selection statements."
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 25, 2010 22:49
\| \|
That seems right, so I went ahead and changed the title.
We also want to make sure these guidelines are written for developers and not for analyzer vendors.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 26, 2010 14:20
\| \|
The related for Java is a rec.
Why it is a rule here ?
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Mar 21, 2018 03:29
\| \|
Mainly because the Java analogue is much more limited in scope (you can only mistake = and == with boolean operands in Java).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 21, 2018 09:31
\| \|
Regarding; MISRA 2012 (13.2, 13.3 and 13.4) , i would enlarge this rule with assignement in sub-expression.
The risk here, is not the unintended program flow but would be undefined behavior.
It may also be dependent of the evaluation order of the expression.
What do you think about that ?
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Mar 21, 2018 10:26
\| \|
Conflating = with == usually does not produce undefined behavior. The few cases where it does are addressed in other CERT rules. Therefore this rule correctly focuses on unexpected control flow, rather than undefined behavior.
I would suggest that, in the right circumstances, unexpected control flow can be as dangerous as undefined behavior, or even more dangerous. See the noncompliant code in;[EXP16-C. Do not compare function pointers to constant values](EXP16-C_%20Do%20not%20compare%20function%20pointers%20to%20constant%20values) for a real-world example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 21, 2018 14:45
\| \|
I was not clear ![](images/icons/emoticons/wink.svg)
I did'nt write about the risk of assignments in selection statements, i totaly agree with this actual rule here.
In addition, assignements in sub-expressions (not in selection statements) could produce undefined behavior.
MISRA 2012, in Rule 13.4 give few examples like :
a\[x\]=a\[x=y\];
or
a\[b+=c\]=a\[b\]
We could also imagine cases where we use le result of an assignement has argument of functions
I wonder if some cases could produce vulnerabilities resulting of side effects.
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Mar 22, 2018 02:54
\| \|
As I mentioned above, undefined behavior is well covered by other CERT rules. The code examples you cite violate;[EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects).
I added a reference to EXP30-C to this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 22, 2018 10:15
\| \|
IMHO a good addition as an example to the *EXP45-C-EX1* exception would be the idiomatic...
     while ((c = fgetc(stream)) != EOF)
(or its getc variant).
![](images/icons/contenttypes/comment_16.png) Posted by stefanct at Aug 13, 2018 04:35
\| \|
The last three examples (`while`/`ch`) should probably use `||` instead of `&&`.
![](images/icons/contenttypes/comment_16.png) Posted by alex at Aug 16, 2018 09:52
\| \|
Agreed, fixed.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 16, 2018 10:12
\| \|
I was wondering why example above "for (; x; foo(), x = y) { /\* ... \*/ }" is considered as a violation as assignment is on the third operand?;
![](images/icons/contenttypes/comment_16.png) Posted by cbard at Jul 03, 2020 05:41
\| \|
You're right, that code example does not violate the rule, as the assignment is on the \*third\* operand of the for statement, not the second. I changed it to a compliant solution.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 06, 2020 12:22
\|
