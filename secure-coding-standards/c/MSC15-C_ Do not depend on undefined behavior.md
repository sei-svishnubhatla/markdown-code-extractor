The C Standard, subclause 3.5.3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines *undefined behavior* as
> behavior, upon use of a nonportable or erroneous program construct or of erroneous data, for which this document imposes no requirements

Subclause 4 explains how the standard identifies undefined behavior (see also [undefined behavior 1](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_1) of Annex J).
> If a "shall" or "shall not" requirement that appears outside of a constraint or runtime-constraint is violated, the behavior is undefined. Undefined behavior is otherwise indicated in this document by the words "undefined behavior" or by the omission of any explicit definition of behavior. There is no difference in emphasis among these three; they all describe "behavior that is undefined".

Annex J, subclause J.2, "Undefined behavior," enumerates the circumstances under which the behavior of a program is undefined. This list is duplicated on the [CC. Undefined Behavior](CC_%20Undefined%20Behavior) page.
Behavior can be classified as undefined by the C standards committee for the following reasons:
-   To give the implementor license not to catch certain program errors that are difficult to diagnose
-   To avoid defining obscure corner cases that would favor one [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) strategy over another
-   To identify areas of possible [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) language extension: the implementor may augment the language by providing a definition of the officially [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior)
Conforming implementations can deal with undefined behavior in a variety of fashions, such as ignoring the situation completely, with unpredictable results; translating or executing the program in a documented manner characteristic of the environment (with or without the issuance of a diagnostic message); or terminating a translation or execution (with the issuance of a diagnostic message). Because compilers are not obligated to generate code for undefined behavior, these behaviors are candidates for optimization. By assuming that undefined behaviors will not occur, compilers can generate code with better performance characteristics.
Increasingly, compiler writers are taking advantage of undefined behaviors in the C programming languages to improve optimizations. These optimizations frequently interfere with the ability of developers to perform cause-effect analysis on their source code—that is, to analyze the dependence of downstream results on prior results. Consequently, these optimizations are eliminating causality in software and are increasing the probability of software faults, defects, and [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
All of this puts the onus on the programmer to develop code that is free from undefined behaviors, with or without the help of the compiler.
## Noncompliant Code Example
An example of [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in C is the behavior on signed integer overflow (see also [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow)). This noncompliant code example depends on this behavior to catch the overflow:
``` c
#include <assert.h>
#include <limits.h>
#include <stdio.h>
int foo(int a) {
  assert(a + 100 > a);
  printf("%d %d\n", a + 100, a);
  return a;
}
int main(void) {
  foo(100);
  foo(INT_MAX);
  return 0;
}
```
This code checks for signed integer overflow by testing whether `a + 100 > a`. This test cannot evaluate to false unless an integer overflow occurs. However, because a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) is not required to generate code for undefined behavior, and signed integer overflow is undefined behavior, this code may be compiled out. For example, GCC 4.1.1 optimizes out the assertion for all optimization levels, and GCC 4.2.3 optimizes out the assertion for programs compiled with `-O2`-level optimization and higher.
On some platforms, the integer overflow causes the program to terminate (before it has an opportunity to test).
## Compliant Solution
This compliant solution does not depend on undefined behavior:
``` c
#include <assert.h>
#include <limits.h>
#include <stdio.h>
int foo(int a) {
  assert(a < (INT_MAX - 100));
  printf("%d %d\n", a + 100, a);
  return a;
}
int main(void) {
  foo(100);
  foo(INT_MAX);
  return 0;
}
```
## Risk Assessment
Although it is rare that the entire application can be [strictly conforming](BB.-Definitions_87152273.html#BB.Definitions-strictlyconforming), the goal should be that almost all the code is allowed for a strictly conforming program (which among other things means that it avoids [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior)), with the implementation-dependent parts confined to modules that the programmer knows are needed to adapt to the platform when it changes.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC15-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports undefined behavior. |
| Helix QAC | 2024.4 | C0160, C0161, C0162, C0163, C0164, C0165, C0166, C0167, C0168, C0169, C0170, C0171, C0172, C0173, C0174, C0175, C0176, C0177, C0178, C0179, C0184, C0185, C0186, C0190, C0191, C0192, C0193, C0194, C0195, C0196, C0197, C0198, C0199, C0200, C0201, C0203, C0204, C0206, C0207, C0208, C0235, C0275, C0301, C0302, C0304, C0307, C0309, C0323, C0327, C0337, C0400, C0401, C0402, C0403, C0475, C0543, C0544, C0545, C0602, C0603, C0623, C0625, C0626, C0630, C0632, C0636, C0654, C0658, C0661, C0667, C0668, C0672, C0676, C0678, C0680, C0706, C0745, C0777, C0779, C0813, C0814, C0821, C0836, C0837, C0848, C0853, C0854, C0864, C0865, C0867, C0872, C0874, C0885, C0887, C0888, C0914, C0915, C0942, C1509, C1510, C3113, C3114, C3239, C3311, C3312, C3319, C3437, C3438 |  |
| LDRA tool suite | 9.7.1 | 48 D, 63 D, 84 D, 113 D, 5 Q, 64 S, 65 S, 100 S, 109 S, 156 S, 296 S, 324 S, 335 S, 336 S, 339 S, 412 S, 427 S, 465 S, 482 S, 497 S, 545 S, 587 S, 608 S, 642 S, 62 X, 63 X | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC15-aCERT_C-MSC15-b
 | Evaluation of constant unsigned integer expressions should not lead to wrap-aroundEvaluation of constant unsigned integer expressions in preprocessor directives should not lead to wraparound |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC15-C | Checks for undefined behavior (rec. partially covered) |
| PVS-Studio | 7.35 | V772 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC15-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC15-CPP. Do not depend on undefined behavior |
| ISO/IEC TR 24772 | Unspecified Behaviour [BQF]Undefined Behaviour [EWF]
Implementation-Defined Behaviour [FAB] |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 3.5.3, "Undefined Behavior"Subclause 4, "Conformance"
Subclause J.2, "Undefined Behavior" |
| [Seacord 2013] | Chapter 5, "Integer Security" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152340) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152277)
## Comments:

|  |
| ----|
| I'm wondering whether this guideline is necessary given that:
    we have MSC14-C. Do not introduce unnecessary platform dependencies, and
    unless an implementation provides well-defined semantics for the specific case of "undefined behavior" (and thus relying on it falls under MSC14-C), we tend to have a specific rule for each class of undefined behavior (referenced in CC. Undefined Behavior), and
    the only NCCE presented here is the subject of INT32-C. Ensure that operations on signed integers do not result in overflow
Since there is no way to depend on truly undefined behavior (subject to #2 above), no well-intentioned programmer would deliberately introduce such behavior into their code, the value of this guideline seems questionable.
I propose we roll it into MSC14-C.
Alternatively (but IMO less preferably), we might want to make it a rule and rename it to something like Avoid introducing undefined behavior.
                                        Posted by martinsebor at Apr 21, 2010 16:23
                                     |
| Many of our rules address specific UB's, they are listed in our UB section. A single rule saying "avoid UB" is necessary as a token gesture, and as a 'grandaddy' rule to generalize the principle.
I do expect that any NCCE for this rule would violate some other rule as well (if it violated no other rule, we would need to add one 
We could roll the NCCE/CS samples into MSC14-C, although that would extend MSC14-C's scope a bit. I'm right now about 70/30 against doing this.
                                        Posted by svoboda at Apr 21, 2010 17:08
                                     |
| I agree with David, but possibly more like 90/10 against.
Possibly a better example for this rule is the NCE from ARR38-C. Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element:
char *buf;
size_t len = 1 << 30;
/* Check for overflow */
if (buf + len < buf) {
  len = -(uintptr_t)buf-1;
}

This code resembles the test for wraparound from the `sprint()` function as implemented for the Plan 9 operating system. If `buf + len < buf` evaluates to true, `len` is assigned the remaining space minus 1 byte. However, because the expression `buf + len < buf` constitutes undefined behavior, compilers can assume this condition will never occur and optimize out the entire conditional statement. In gcc versions 4.2 and later, for example, code that performs checks for wrapping that depend on undefined behavior (such as the code in this noncompliant code example) are optimized away; no object code to perform the check appears in the resulting executable program \[[VU#162289](AA.-Bibliography_87152170.html#AA.Bibliography-VU#162289)\]. This is of special concern because it often results in the silent elimination of code that was inserted to provide a safety or security check.\\
This is a good example of where an experience programmer might incorrectly assume "hardware behavior" which has always been a good assumption in the past and develop code that depends upon undefined behavior that initially works but then fails when a newer version of the compiler implements more aggressive optimizations.
I don't see a large distinction between the existing title and the proposed new title. Avoid "introducing" sounds a little bit like its OK if you have already done this.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 22, 2010 08:57
\| \|
I certainly do not disagree with the thrust of the guideline. But unless there are specific cases and noncompliant examples that are not already the subject of other, more specific guidelines, I see little value in advising readers to "avoid writing buggy code" and duplicating examples already discussed elsewhere in more detail. As I said, no one deliberately introduces bugs so telling people to avoid doing it will not stop it from happening. In addition, the material discussed in this guideline is already the subject of MSC14-C.
To David's point that this guideline exists for organizational reasons: that makes sense to me, but only if we also add guidelines for the other kinds of behavior, i.e., unspecified, implementation-defined, and locale-specific (as discussed in MSC14-C). I actually find this categorization very useful (it is one of the reasons why I introduced section [CC. Undefined Behavior](CC_%20Undefined%20Behavior)). As it is, though, we have a guideline that specifically targets undefined behavior, and then another one that lumps undefined behavior in with the other three potentially problematic kinds.
In summary, if we do keep this guideline I propose we also:
-   add a guideline for each of the four kinds of behavior discussed in MSC14-C (i.e., unspecified, undefined, implementation-defined, and locale-specific)
-   rather than discussing specific cases of each kind of behavior in these high level guidelines add links to each of them pointing to the individual guidelines that already do discuss those specific cases (or add such guidelines where they do not)
-   either remove MSC14-C or rename/restructure it such that it become hierarchically a parent of the newly added behavior-specific newly added guidelines
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 24, 2010 13:21
\| \|
I agree with you that there are not compelling examples for this guidelines and there is unlikely to ever be any, because any compelling example would be consumed by a more specific guideline.
How about we just reuse the introductory material up to the first noncompliant code example as the introduction to [CC. Undefined Behavior](CC_%20Undefined%20Behavior) and move the rest into the Void?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 25, 2010 09:40
\| \|
After thinking about this for a while I think David's suggestion to have a general "grandaddy" rule for all cases of undefined behavior and specific child rules for each common class of it is a useful way of organizing the material. The CWE database is structured exactly this way and I am finding its organization most natural and very helpful.
In general, every instance of undefined behavior must be avoided. But as you suggest, not every instance is common enough to justify adding a guideline of its own (e.g., UB [2](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_2) or [4](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_4)). However, the lack of specific guidelines for such instances must not be interpreted as permission to exploit such cases. Avoiding such misinterpretation of intent is another purpose of this general rule.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at May 02, 2010 19:12
\|
