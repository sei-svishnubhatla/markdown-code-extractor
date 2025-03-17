C defines `<`, `>`, `<=`, and `>=` to be *relational operators*, and it defines `==` and `!=` to be *equality operators*.
If a `for` or `while` statement uses a loop counter, than it is safer to use a relational operator (such as `<`) to terminate the loop than to use an equality operator (such as `!=`).
## Noncompliant Code Example (Equality Operators)
This noncompliant code example appears to have five iterations, but in fact, the loop never terminates:
``` c
size_t i;
for (i = 1; i != 10; i += 2) {
  /* ... */
}
```
## Compliant Solution (Relational Operators)
Using the relational operator `<=` instead of an equality operator guarantees loop termination:
``` c
size_t i;
for (i = 1; i <= 10; i += 2 ) {
  /* ... */
}
```
## Noncompliant Code Example (Equality Operators)
It is also important to ensure termination of loops where the start and end values are variables that might not be properly ordered. The following function assumes that `begin < end`; if this is not the case, the loop will never terminate:
``` c
void f(size_t begin, size_t end) {
  size_t i;
  for (i = begin; i != end; ++i) {
    /* ... */
  }
}
```
## Compliant Solution (Relational Operators)
Again, using a relational operator instead of equivalence guarantees loop termination. If `begin >= end`, the loop never executes its body.
``` c
void f(size_t begin, size_t end) {
  size_t i;
  for (i = begin; i < end; ++i) {
    /* ... */
  }
}
```
## Noncompliant Code Example (Boundary Conditions)
Numerical comparison operators do not always ensure loop termination when comparing against the minimum or maximum representable value of a type, such as `SIZE_MAX`:
``` c
void f(size_t begin, size_t step) {
  size_t i;
  for (i = begin; i <= SIZE_MAX; i += step) {
    /* ... */
  }
}
```
## Compliant Solution (Boundary Conditions)
A compliant solution is to compare against the difference between the maximum representable value of a type and the increment:
``` c
void f(size_t begin, size_t step) {
  if (0 < step) {
    size_t i;
    for (i = begin; i <= SIZE_MAX - step; i += step) {
      /* ... */
    }
  }
}
```
## Exceptions
**MSC21-C-EX1:** If the loop counter is incremented by 1 on each iteration, and it is known that the starting value of a loop is less than or equal to the ending value, then an equality operator may be used to terminate the loop. Likewise, if the loop counter is decremented by 1 on each iteration, and it is known that the starting value of the loop is greater than or equal to the ending value, then an equality operator may be used to terminate the loop.
``` c
size_t i;
for (i = 1; i != 5; ++i) {
  /* ... */
}
```
## Risk Assessment
Testing for exact values runs the risk of a loop terminating much longer than expected or never terminating at all.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC21-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports potential infinite loops. |
| CodeSonar | 8.3p0 | LANG.STRUCT.LOOP.HRLANG.STRUCT.LOOP.UB | High risk loopPotential unbounded loop |
| Compass/ROSE |  |  |  |
| LDRA tool suite | 9.7.1 | 510 S | Partially implemented |
| PC-lint Plus | 1.4 | 440, 442, 443,444, 445, 2650 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC21-C | Checks for loop bounded with tainted value (rec. partially covered) |
| PVS-Studio | 7.35 | V621 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC21-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC21-CPP. Use inequality to terminate a loop whose counter changes by more than one |
| CERT Oracle Secure Coding Standard for Java | MSC54-J. Avoid inadvertent wrapping of loop counters |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152333) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/MSC22-C_%20Use%20the%20setjmp__,%20longjmp__%20facility%20securely)
## Comments:

|  |
| ----|
| A related problem I've seen is in cases where the controlling expression of a loop assumes the lower bound of the loop is less than or equal to the upper bound but where this assumtion doesn't hold.
void f(int begin, int end) {
  int i;
  for (i = begin; i != end; ++i) {
    /* ... */
  }
}
void g() {
  f(2, 1);   /* leads to undefined behavior if f() */
}

The solution in such cases is also to use a relational operator rather than inequality, regardless of the increment:
``` java
void f(int begin, int end) {
  int i;
  for (i = begin; i < end; ++i) {
    /* ... */
  }
}
void g() {
  f(2, 1);   /* okay, no problem */
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 03, 2010 20:04
\| \|
Good point. I added your NCCE/CS code samples to the rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 04, 2010 09:02
\| \|
In the last CS there is a formatting problem - &lt instead of \<.
Another problem can arise when comparing with INT_MAX, and having a step size more than 1. For example, see the last NCE in the corresponding Java guideline [MSC54-J. Avoid inadvertent wrapping of loop counters](https://wiki.sei.cmu.edu/confluence/display/java/MSC54-J.+Avoid+inadvertent+wrapping+of+loop+counters).
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Feb 08, 2010 16:26
\| \|
Fixed/added, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 08, 2010 22:35
\| \|
There seems to be some confusion between "inequality" and "equality-expression"
"a != b" is one of the equality expressions in C. "a \< b" is an inequality statement in math and relational expression in C.
So the first "Noncompliant Code Example (inequality)" should be corrected to "Noncompliant Code Example (equality !=)" for example?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Apr 05, 2010 04:13
\| \|
I s/inequality/equivalence/g for this rule. Inequality can mean either != or \< \> \<= =\> in English.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 05, 2010 09:57
\| \|
C doesn't define or use the term equivalence. For clarity I think we should stay with the standard (as in ISO/IEC 9899) terminology:
-   Equality operators include both `==` and `!=` (i.e., the inequality operator)
-   Relational operators include `<`, `>`, `<=`, and `>=`.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 05, 2010 21:13
\| \|
I was thinking the same thing.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 06, 2010 03:25
\| \|
That's fine, but we should then define the terms we are using, since inequality has two meanings in mathematics, and, unless you're intimately familiar with the C standard, you don't know that they ignore one of the meanings.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 06, 2010 13:53
\| \|
Having an education strong in algebra, where "inequalities" are often formulas like a \<= b, I was \*very\* confused when I read the title of this recommendation and saw the example. I beg for a change on the title, like "Use robust loop termination conditions". English is not my mother tongue, though.
![](images/icons/contenttypes/comment_16.png) Posted by eduardo.silva.lopez@hotmail.com at Aug 28, 2011 10:48
\| \|
Changed the title.
The rule still uses the terminology of the C standard, which can confuse a mathematician, so the intro now also defines the terminology used.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 29, 2011 14:03
\|
