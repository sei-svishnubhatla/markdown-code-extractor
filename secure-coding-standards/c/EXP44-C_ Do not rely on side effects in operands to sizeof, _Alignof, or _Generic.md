Some operators do not evaluate their operands beyond the type information the operands provide. When using one of these operators, do not pass an operand that would otherwise yield a side effect since the side effect will not be generated.
The `sizeof` operator yields the size (in bytes) of its operand, which may be an expression or the parenthesized name of a type.  In most cases, the operand is not evaluated.  A possible exception is when the type of the operand is a variable length array type (VLA); then the expression is evaluated. When part of the operand of the sizeof operator is a VLA type and when changing the value of the VLA's size expression would not affect the result of the operator, it is [unspecified](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior) whether or not the size expression is evaluated. (See [unspecified behavior 22](DD.-Unspecified-Behavior_87152246.html#DD.UnspecifiedBehavior-usb_22).)
The operand passed to`_Alignof` is never evaluated, despite not being an expression. For instance, if the operand is a VLA type and the VLA's size expression contains a side effect, that side effect is never evaluated.
The operand used in the controlling expression of a `_Generic` selection expression is never evaluated.
Providing an expression that appears to produce side effects may be misleading to programmers who are not aware that these expressions are not evaluated, and in the case of a VLA used in `sizeof`, have unspecified results. As a result, programmers may make invalid assumptions about program state, leading to errors and possible software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
This rule is similar to [PRE31-C. Avoid side effects in arguments to unsafe macros](PRE31-C_%20Avoid%20side%20effects%20in%20arguments%20to%20unsafe%20macros).
## Noncompliant Code Example (`sizeof`)
In this noncompliant code example, the expression `a++` is not evaluated:
``` c
#include <stdio.h>
void func(void) {
  int a = 14;
  int b = sizeof(a++);
  printf("%d, %d\n", a, b);
}
```
Consequently, the value of `a` after `b` has been initialized is 14.
## Compliant Solution (`sizeof`)
In this compliant solution, the variable `a` is incremented outside of the `sizeof` operation:
``` c
#include <stdio.h>
void func(void) {
  int a = 14;
  int b = sizeof(a);
  ++a;
  printf("%d, %d\n", a, b);
}
```
## Noncompliant Code Example (`sizeof`, VLA)
In this noncompliant code example, the expression `++n` in the initialization expression of `a` must be evaluated because its value affects the size of the VLA operand of the `sizeof` operator. However, in the initialization expression of `b`, the expression `++n % 1` evaluates to `0.` This means that the value of `n` does not affect the result of the `sizeof` operator. Consequently, it is unspecified whether or not `n` will be incremented when initializing `b`.
``` c
#include <stddef.h>
#include <stdio.h>
void f(size_t n) {
  /* n must be incremented */ 
  size_t a = sizeof(int[++n]);
  /* n need not be incremented */
  size_t b = sizeof(int[++n % 1 + 1]);
  printf("%zu, %zu, %zu\n", a, b, n);
  /* ... */
}
```
## Compliant Solution (`sizeof`, VLA)
This compliant solution avoids changing the value of the variable `n` used in each `sizeof` expression and instead increments `n` safely afterwards:
``` c
#include <stddef.h>
#include <stdio.h>
void f(size_t n) {
  size_t a = sizeof(int[n + 1]);
  ++n;
  size_t b = sizeof(int[n % 1 + 1]);
  ++n;
  printf("%zu, %zu, %zu\n", a, b, n);
  /* ... */
}
```
## Noncompliant Code Example (`_Generic`)
This noncompliant code example attempts to modify a variable's value as part of the `_Generic` selection control expression. The programmer may expect that `a` is incremented, but because `_Generic` does not evaluate its control expression, the value of `a` is not modified.
``` c
#include <stdio.h>
#define S(val) _Generic(val, int : 2, \
                             short : 3, \
                             default : 1)
void func(void) {
  int a = 0;
  int b = S(a++);
  printf("%d, %d\n", a, b);
}
```
## Compliant Solution (`_Generic`)
In this compliant solution, a is incremented outside of the `_Generic` selection expression:
``` c
#include <stdio.h>
#define S(val) _Generic(val, int : 2, \
                             short : 3, \
                             default : 1)
void func(void) {
  int a = 0;
  int b = S(a);
  ++a;
  printf("%d, %d\n", a, b);
} 
```
## Noncompliant Code Example (`_Alignof`)
This noncompliant code example attempts to modify a variable while getting its default alignment value. The user may have expected `val` to be incremented as part of the `_Alignof` expression, but because `_Alignof` does not evaluate its operand, `val` is unchanged.
``` c
#include <stdio.h>
void func(void) {
  int val = 0; 
  /* ... */ 
  size_t align = _Alignof(int[++val]);
  printf("%zu, %d\n", align, val);
  /* ... */
}
```
## Compliant Solution (`_Alignof`)
 This compliant solution moves the expression out of the `_Alignof` operator:
``` c
#include <stdio.h>
void func(void) {
  int val = 0; 
  /* ... */ 
  ++val;
  size_t align = _Alignof(int[val]);
  printf("%zu, %d\n", align, val);
  /* ... */
}
```
## Exceptions
**EXP44-C-EX1**: Reading a `volatile`-qualified value is a side-effecting operation. However, accessing a value through a `volatile`-qualified type does not guarantee side effects will happen on the read of the value unless the underlying object is also `volatile`-qualified. Idiomatic reads of a `volatile`-qualified object are permissible as an operand to a `sizeof()`, `_Alignof()`, or `_Generic` expression, as in the following example:
``` c
void f(void) {
  int * volatile v;
  (void)sizeof(*v);
}
```
## Risk Assessment
If expressions that appear to produce side effects are supplied to an operator that does not evaluate its operands, the results may be different than expected. Depending on how this result is used, it can lead to unintended program behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP44-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | alignof-side-effectgeneric-selection-side-effect
sizeof
 | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP44 |  |
| Clang | 3.9 | -Wunevaluated-expression | Can diagnose some instance of this rule, but not all (such as the _Alignof NCCE). |
| CodeSonar | 8.3p0 | LANG.STRUCT.SE.SIZEOFLANG.STRUCT.SE.CGEN
 | Side effects in sizeofSide Effects in C Generic Selection |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISRA C 2004 Rule 12.3 | Partially implemented |
| ECLAIR | 1.2 | CC2.EXP06 | Fully implemented |
| Helix QAC | 2024.4 | C3307 |  |
| Klocwork | 2024.4 | MISRA.SIZEOF.SIDE_EFFECT |  |
| LDRA tool suite | 9.7.1 | 54 S, 653 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP44-aCERT_C-EXP44-b | Object designated by a volatile lvalue should not be accessed in the operand of the sizeof operatorThe function call that causes the side effect shall not be the operand of the sizeof operator |
| PC-lint Plus | 1.4 | 9006 | Partially supported: reports use of sizeof with an expression that would have side effects |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP44-C | Checks for situations when side effects of specified expressions are ignored (rule fully covered) |
| PVS-Studio | 7.35 | V568 |  |
| RuleChecker | 24.04 | alignof-side-effectgeneric-selection-side-effect
sizeof | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP44-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | EXP52-CPP. Do not rely on side effects in unevaluated operands | Prior to 2018-01-12: CERT: Unspecified Relationship |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151927) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152228)
## Comments:

|  |
| ----|
| This is an example of a bug, since nobody would intentionally code a side effect in that context.; Indeed it would be nice for compilers to warn about side-effects in sizeof operands.
                                        Posted by dagwyn at Apr 15, 2008 14:35
                                     |
| dumb question.; most of the examples in the standard which take the sizeof a unary expression and not a type don't use parenthesis.  Should we follow suite?
                                        Posted by rcs_mgr at Nov 12, 2013 00:01
                                     |
| Personally, I don't like that style.;I find it to be confusing and inconsistent (and potentially error-prone if you don't remember that only a unary expression is valid). 
                                        Posted by aballman at Nov 12, 2013 08:21
                                     |
| The string argument in the call to printf in Compliant Solution (_Alignof) is missing a closing right quote.
                                        Posted by alex at Sep 27, 2018 09:41
                                     |
| Fixed, thanks
                                        Posted by svoboda at Sep 28, 2018 17:59
                                     |
| I am concerned that the risk assessment values are incorrect. The severity is currently Low, indicating DOS or hang. And the probability is Unlikely (the lowest setting). I am thinking that perhaps the severity should be high, and liklihood at least Probable (medium setting).Here is code example that has a buffer overflow b/c of violating this rule:int main(void) {  char src[100];
  size_t size = sizeof(src-1);  // oops should be sizeof(str) - 1.
  // Expected: 99, got 8 (on ILP64)
  char *dest = calloc(size, sizeof(char));
  if (dest == NULL) {
    abort(); /* handle error */
  }
  printf("What is your name?\n");
  fgets( src, sizeof(src), stdin);
  strcpy(dest, src); // buffer overflow!
  printf("Hello, %s\n", dest);
  free(dest);
  return 0;
}

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 15, 2019 12:09
\| \|
Will Klieber says:
In your example, I don't see any side effects in the operand of sizeof.; (And I don't see any use of  \_Alignof or \_Generic.)  Am I missing something?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 15, 2019 14:36
\| \|
I'm with Will on this one;– I don't think the code you posted violates this rule as written (nor do I think the rule should be modified to cover this case).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Feb 15, 2019 14:47
\| \|
So which rule covers (or should cover) my code example?; (There are analysis tools that flag any arithmetic expression in a sizeof operation.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 15, 2019 15:20
\| \|
I'd go with;ARR38-C ("Guarantee that library functions do not form invalid pointers").
![](images/icons/contenttypes/comment_16.png) Posted by weklieber at Feb 15, 2019 15:32
\| \|
That would catch my code example, but what if I had said sizeof(src + 1)?; That would have complied with ARR38-C, and still produced a buffer overflow in my code.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 15, 2019 15:35
\| \|
I think both your original and revised examples are covered by MEM35-C (Allocate sufficient memory for an object).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Feb 15, 2019 15:44
\| \|
I think your "oops" comment should also use "src" not "str" as well.; But, I don't think we have any rules on misleading comments.  ![](images/icons/emoticons/wink.svg)
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Feb 15, 2019 16:42
\|
