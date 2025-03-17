Because floating-point numbers represent real numbers, it is often mistakenly assumed that they can represent any simple fraction exactly. Floating-point numbers are subject to representational limitations just as integers are, and binary floating-point numbers cannot represent all real numbers exactly, even if they can be represented in a small number of decimal digits.
In addition, because floating-point numbers can represent large values, it is often mistakenly assumed that they can represent all significant digits of those values. To gain a large dynamic range, floating-point numbers maintain a fixed number of precision bits (also called the significand) and an exponent, which limit the number of significant digits they can represent.
Different implementations have different precision limitations, and to keep code portable, floating-point variables must not be used as the loop induction variable. See Goldberg's work for an introduction to this topic \[[Goldberg 1991](https://www.securecoding.cert.org/confluence/display/java/Rule+AA.+References#RuleAA.References-Goldberg91)\].
For the purpose of this rule, a *loop counter* is an induction variable that is used as an operand of a comparison expression that is used as the controlling expression of a `do`, `while`, or `for` loop. An *induction variable* is a variable that gets increased or decreased by a fixed amount on every iteration of a loop \[[Aho 1986](AA.-Bibliography_87152170.html#AA.Bibliography-Aho1986)\]. Furthermore, the change to the variable must occur directly in the loop body (rather than inside a function executed within the loop).
## Noncompliant Code Example
In this noncompliant code example, a floating-point variable is used as a loop counter. The decimal number `0.1` is a repeating fraction in binary and cannot be exactly represented as a binary floating-point number. Depending on the implementation, the loop may iterate 9 or 10 times.
``` c
void func(void) {
  for (float x = 0.1f; x <= 1.0f; x += 0.1f) {
    /* Loop may iterate 9 or 10 times */
  }
}
```
For example, when compiled with GCC or Microsoft Visual Studio 2013 and executed on an x86 processor, the loop is evaluated only nine times.
## Compliant Solution
In this compliant solution, the loop counter is an integer from which the floating-point value is derived:
``` c
#include <stddef.h>
void func(void) {
  for (size_t count = 1; count <= 10; ++count) {
    float x = count / 10.0f;
    /* Loop iterates exactly 10 times */
  }
}
```
## Noncompliant Code Example
In this noncompliant code example, a floating-point loop counter is incremented by an amount that is too small to change its value given its precision:
``` c
void func(void) {
  for (float x = 100000001.0f; x <= 100000010.0f; x += 1.0f) {
    /* Loop may not terminate */
  }
}
```
On many implementations, this produces an infinite loop.
## Compliant Solution
In this compliant solution, the loop counter is an integer from which the floating-point value is derived. The variable `x` is assigned a computed value to reduce compounded rounding errors that are present in the noncompliant code example.
``` c
void func(void) {
  for (size_t count = 1; count <= 10; ++count) {
    float x = 100000000.0f + (count * 1.0f);
    /* Loop iterates exactly 10 times */
  }
}
```
## Risk Assessment
The use of floating-point variables as loop counters can result in  [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) .

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP30-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | for-loop-float | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-FLP30 | Fully implemented |
| Clang | 3.9 | cert-flp30-c | Checked by clang-tidy |
| CodeSonar | 8.3p0 | LANG.STRUCT.LOOP.FPC | Float-typed loop counter |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISRA C 2004 Rule 13.4MISRA C 2012 Rule 14.1 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-flp30-c |  |
| ECLAIR | 1.2 | CC2.FLP30 | Fully implemented |
| Helix QAC | 2024.4 | C3339, C3340, C3342C++4234 |  |
| Klocwork | 2024.4 | MISRA.FOR.COUNTER.FLT |  |
| LDRA tool suite | 9.7.1 | 39 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP30-a | Do not use floating point variables as loop counters |
| PC-lint Plus | 1.4 | 9009 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FLP30-C | Checks for use of float variable as loop counter (rule fully covered) |
| PVS-Studio | 7.35 | V1034 |  |
| RuleChecker | 24.04 | for-loop-float | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S2193 | Fully implemented |
| TrustInSoft Analyzer | 1.38 | non-terminating | Exhaustively detects non-terminating statements (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | FLP30-CPP. Do not use floating-point variables as loop counters | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT Oracle Secure Coding Standard for Java | NUM09-J. Do not use floating-point variables as loop counters | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Floating-Point Arithmetic [PLF] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Directive 1.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 14.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Aho 1986] |  |
| [Goldberg 1991] |  |
| [Lockheed Martin 05] | AV Rule 197 |

------------------------------------------------------------------------
[](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](../c/Rule%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152396)
## Comments:

|  |
| ----|
| is this line in the second CCE a violation of FLP33-C. Convert integers to floating point for floating point operations?
double x = 100000000.0 + count;

![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 30, 2008 09:33
\| \|
I don't think so. As long as one of the arguments is a floating point number, the calculation should be performed as a floating point operation.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jul 26, 2008 12:58
\| \|
As I commented elsewhere, I see no real problem with either noncompliant example since they both use the less-than or equal operator (i.e., the loops are guaranteed to terminate). An example that, IMO, demonstrates the problem better is one that uses \[in\]equality since, unlike integer arithmetic, floating point arithmetic is inexact:
``` java
for (float x = 0.1f; x != 1.0f; x += 0.1f) {   /* loop may not terminate */
  /* ... */
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 29, 2010 23:30
\| \|
I believe the rationale here is that a programmer might expect the loop to execute 10 times but it executes only 9 times. At least in Java and VC++ 2005. ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Jan 29, 2010 23:53
\| \|
I see – very tricky! That hadn't even occurred to me despite the fact that it's mentioned below the noncompliant example. I should read these guidelines before the CSCG ones!
Maybe the example could be enhanced to make this more obvious. How's this:
``` java
int main ()
{
    int i = 6;
    float x = 0.6;
    for (; x <= 1.0f; x += 0.1f, i += 1);
    assert(x > 1.0f);
    assert(i > 10);   /* may fail */
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 30, 2010 13:44
\| \|
This page doesn't really make it clear that cumulative rounding error is an issue that cannot be addressed by the usual advice for avoiding an exact comparison of floating point numbers.
Readers might think that the first noncompliant example could be 'fixed' by changing the termination condition to 'x \< 10.05' (as I did at first.) Here is a proposed replacement which makes it clear that this 'fix' would not be generally applicable:
``` cpp
void func(void) {
  for (float x = 0.1f; x < 1000.05f; x += 0.1f) {
    /* Loop may not iterate 10,000 times */
  }
}
```
When compiled on gcc for x86 this will iterate 10,001 times.
;
![](images/icons/contenttypes/comment_16.png) Posted by pjdennis at Jun 04, 2016 06:48
\| \|
Also, the solution for the second noncompliant example seems problematic. While it addresses the loop termination issue, we are still left with a value of x that may or may not be incrementing depending on the implementation, and if it is incrementing, will certainly be subject to cumulative rounding errors.
Here's an improved solution for the second noncompliant example:
``` cpp
void func(void) {
    for (size_t count = 1; count <= 10; ++count) {
        float x = 100000000.0f + 1.0f * count;
        /* Loop iterates exactly 10 times */
    }
}
```
![](images/icons/contenttypes/comment_16.png) Posted by pjdennis at Jun 04, 2016 07:07
\| \|
Added a reference to;\[[Goldberg 1991](https://www.securecoding.cert.org/confluence/display/java/Rule+AA.+References#RuleAA.References-Goldberg91)\] to provide background material for why fps should not be loop counters. (We also have recommendations addressing this like [FLP00-C. Understand the limitations of floating-point numbers](FLP00-C_%20Understand%20the%20limitations%20of%20floating-point%20numbers)).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 08, 2016 10:35
\| \|
Fixed the 2nd compliant solution as you suggest, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 08, 2016 10:36
\|
