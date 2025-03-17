Mixing bitwise and relational operators in the same full expression can be a sign of a logic error in the expression where a logical operator is usually the intended operator. Do not use the bitwise AND (`&`), bitwise OR (`|`), or bitwise XOR (`^`) operators with an operand of type `_Bool`, or the result of a *relational-expression* or *equality-expression*. If the bitwise operator is intended, it should be indicated with use of a parenthesized expression.
## Noncompliant Code Example
In this noncompliant code example, a bitwise `&` operator is used with the results of two *equality-expressions*:
``` c
if (getuid() == 0 & getgid() == 0) { 
  /* ... */ 
} 
```
## Compliant Solution
This compliant solution uses the `&&` operator for the logical operation within the conditional expression:
``` c
if (getuid() == 0 && getgid() == 0) {
  /* ... */
}
```
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP46-C | Low | Likely | Low | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | inappropriate-bool | Supported indirectly via MISRA C:2012 Rule 10.1 |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP46 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.IOT | Inappropriate operand type |
| Coverity | 2017.07 | CONSTANT_EXPRESSION_RESULT | Partially implemented |
| Cppcheck | ;2.15 | bitwiseOnBoolean |  |
| Cppcheck Premium | 24.11.0 | bitwiseOnBoolean |  |
| Helix QAC | 2024.4 | C3344, C4502C++3709 |  |
| Klocwork | 2024.4 | MISRA.LOGIC.OPERATOR.NOT_BOOL |  |
| LDRA tool suite | 9.7.1 | 136 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP46-b | Expressions that are effectively Boolean should not be used as operands to operators other than (&&, ||, !, =, ==, !=, ?:) |
| PC-lint Plus | 1.4 | 514 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP46-C | Checks for bitwise operations on boolean operands (rule fully covered) |
| PVS-Studio | 7.35 | V564, V1015 |  |
| RuleChecker | 24.04 | inappropriate-bool | Supported indirectly via MISRA C:2012 Rule 10.1 |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | Likely Incorrect Expression [KOA] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-480, Use of incorrect operator | 2017-07-05: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-569 | 2017-07-06: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-480 and EXP46-C
Intersection( EXP45-C, EXP46-C) = Ø
CWE-480 = Union( EXP46-C, list) where list =
-   Usage of incorrect operator besides s/&/&&/ or s/\|/\|\|/
## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.7.2, "Errors of Omission and Addition" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152228) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151991)
## Comments:

|  |
| ----|
| Is this really CWE 480?
                                        Posted by azukich at Feb 18, 2010 09:53
                                     |
| It doesn't look like CWE-480 to me. It seems closer to one of CWE-570: Expression is Always False, CWE-768: Incorrect Short Circuit Evaluation, or perhaps CWE-682: Incorrect Calculation. Although none of them looks like a perfect fit.
                                        Posted by martinsebor at Feb 19, 2010 00:04
                                     |
| It seems to me that this is more recommending against using bitwise operations when logical operations are expected.; There's nothing inherently wrong with using bitwise operations in conditionals when it's appropriate, right?  Eg)
unsigned int a = SOME_VALUE;
unsigned int b = SOME_VALUE;
if ((a & b) == SOME_VALUE) {
  /* This is acceptable */
}

![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 11, 2013 12:12
\| \|
No, there is isn't.; It is interesting that Coverity has check for this, although the description suggests it is prone to false positives.
As stated, this recommendation is clearly too strict.  One option is to send this to the void; the other is to make it more "informational"; a third is to more narrowly define the set of conditions under which this is an error.   
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 01, 2014 10:35
\| \|
EXP17-C. Do not perform bitwise operations in conditional expressions
I'll vote for the third, although I'm not sure we can completely enumerate the error conditions. One obvious error condition is to use bitwise ops on inequalities:
x = a & (b == 0); // should be &&
On second thought, I'd prefer making this informative, and creating a rule that enumerates the error conditions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 01, 2014 10:59
\| \|
I think the bitwise ops on inequalities could be summed up better as not performing bitwise operations on Boolean operands, since that's most likely to be an error in any situation, regardless of how you get the Boolean operand. That strikes me as possibly being strong enough to make a rule out of.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 01, 2014 14:52
\| \|
so if I understand you correctly, the noncompliant example in this recommendation would be compliant under this rule?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 14, 2014 20:46
\| \|
No, it would still be noncompliant because;`geteuid() == 0` would be evaluated first (to a Boolean), which would then be bitwise ANDed with the result of calling `getuid()`.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 14, 2014 21:20
\| \|
so in C parlance, I think we would write "one of the operands is of type \_Bool or the result of a relational-expression or equality-expression."
I don't see anywhere in the standard where it says these expressions return a Boolean.; They actually say: 
Each of the operators yields 1 if the specified relation is true and 0 if it is false. The result has type **int**.
All that being said, sounds like a plan. Do you want to promote to a rule and make these changes?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 15, 2014 10:24
\| \|
You're correct, they do return an;`int`, which I hadn't noticed before (this is a difference between C and C++). I'll work on turning this into a rule.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 15, 2014 11:24
\|
