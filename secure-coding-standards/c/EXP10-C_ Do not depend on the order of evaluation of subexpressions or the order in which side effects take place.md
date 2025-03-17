The order of evaluation of subexpressions and the order in which [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) take place are frequently defined as [unspecified behavior](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior) by the C Standard. Counterintuitively, [unspecified behavior](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior) in behavior for which the standard provides two or more possibilities and imposes no further requirements on which is chosen in any instance. Consequently, unspecified behavior can be a portability issue because different [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) can make different choices. If dynamic scheduling is used, however, there may not be a fixed-code execution sequence over the life of a process. Operations that can be executed in different sequences may in fact be executed in a different order.
According to the C Standard, subclause 6.5 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> Except as specified later, side effects and value computations of subexpressions are unsequenced.

Following are specific examples of situations in which the order of evaluation of subexpressions or the order in which [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) take place is unspecified:
-   The order in which the arguments to a function are evaluated (C Standard, subclause 6.5.2.2, "Function Calls")
-   The order of evaluation of the operands in an assignment statement (C Standard, subclause 6.5.16, "Assignment Operators")
-   The order in which any side effects occur among the initialization list expressions is unspecified. In particular, the evaluation order need not be the same as the order of subobject initialization (C Standard, subclause 6.7.9, "Initialization")
This recommendation is related to [EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects), but it focuses on behavior that is nonportable or potentially confusing.
## Noncompliant Code Example
The order of evaluation of the function designator, the actual arguments, and subexpressions within the actual arguments are unspecified, but there is a sequence point before the actual call. For example, in the function call
``` java
(*pf[f1()]) (f2(), f3() + f4())
```
the functions `f1()`, `f2()`, `f3()`, and `f4()` may be called in any order. All side effects have to be completed before the function pointed to by `pf[f1()]` is called.
Consequently, the result of this noncompliant code example depends on [unspecified behavior](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior):
``` c
#include <stdio.h>
int g;
int f(int i) {
  g = i;
  return i;
}
int main(void) {
  int x = f(1) + f(2);
  printf("g = %d\n", g);
  /* ... */
  return 0;
}
```
This code may result in `g` being assigned the value `1`, or equally likely, being assigned the value `2`.
## Compliant Solution
This compliant solution is independent of the order of evaluation of the operands and can be interpreted in only one way:
``` c
#include <stdio.h>
int g;
int f(int i) {
  g = i;
  return i;
}
int main(void) {
  int x = f(1); 
  x += f(2);
  printf("g = %d\n", g);
  /* ... */
  return 0;
}
```
This code always results in `g` being assigned the value `2`.
## Exceptions
**EXP10-C-EX1:** The `&&` and `||` operators guarantee left-to-right evaluation; there is a sequence point after the evaluation of the first operand.
**EXP10-C-EX2:** The first operand of a condition expression is evaluated; there is a sequence point after its evaluation. The second operand is evaluated only if the first compares unequal to 0; the third operand is evaluated only if the first compares equal to 0.
**EXP10-C-EX3:** There is a sequence point before function calls, meaning that the function designator, the actual arguments, and subexpressions within the actual arguments are evaluated before the function is invoked.
**EXP10-C-EX4:** The left operand of a comma operator is evaluated before the right operand is evaluated. There is a sequence point in between.
Note that whereas commas serve to delimit multiple arguments in a function call, these commas are not considered comma operators. Multiple arguments of a function call may be evaluated in any order, with no sequence points between each other.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP10-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | evaluation-ordermultiple-volatile-accesses | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP10 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.SE.IOE | Indeterminate Order of Evaluation |
| Compass/ROSE |  |  | Could detect violations of this recommendation by searching for the following pattern:Any expression that calls two functions between the same sequence pointsThose two functions both modify the value of a static variableThat static variable's value is referenced by code following the expression |
| Coverity | 2017.07 | EVALUATION_ORDER | Can detect the specific instance where a statement contains multiple side effects on the same value with an undefined evaluation order because the statement may behave differently;with different compiler flags or different compilers or platforms |
| Helix QAC | 2024.4 | C0400, C0401, C0402, C0403, C0404, C0405, C3226, C3326 |  |
| LDRA tool suite | 9.7.1 | 35 D, 72 D, 1 Q, 134 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP10-aCERT_C-EXP10-b
CERT_C-EXP10-c
CERT_C-EXP10-d | The value of an expression shall be the same under any order of evaluation that the standard permitsDon't write code that depends on the order of evaluation of function arguments
Don't write code that depends on the order of evaluation of function designator and function arguments
Don't write code that depends on the order of evaluation of expression that involves a function call |
| PC-lint Plus | 1.4 | 564, 931 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP10-C | Checks for situations where expression value depends on order of evaluation or side effects (rec. fully covered) |
| PVS-Studio | 7.35 | V521, V681 |  |
| RuleChecker | 24.04 | evaluation-ordermultiple-volatile-accesses | Partially checked |

A programmer could also violate the recommendation using dynamic memory passed to both functions, but that would be extremely difficult to detect using [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis).
### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP10-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | EXP50-CPP. Do not depend on the order of evaluation for side effects |
| ISO/IEC TR 24772:2013 | Operator Precedence/Order of Evaluation;[JCW]
Side-effects and Order of Evaluation [SAM] |
| MISRA C:2012 | Rule 13.5 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.5, "Expressions" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152073) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152352)
