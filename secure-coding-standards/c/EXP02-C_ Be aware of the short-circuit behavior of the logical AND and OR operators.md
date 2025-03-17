The logical AND and logical OR operators (`&&` and `||`, respectively) exhibit "short-circuit" operation. That is, the second operand is not evaluated if the result can be deduced solely by evaluating the first operand.
Programmers should exercise caution if the second operand contains [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) because it may not be apparent whether the side effects actually occur.
In the following code, the value of `i` is incremented only when `i >= 0`:
``` java
enum { max = 15 };
int i = /* Initialize to user-supplied value */;
if ( (i >= 0) && ( (i++) <= max) ) {
  /* Code */
}
```
Although the behavior is well defined, it is not immediately obvious whether or not `i` gets incremented.
## Noncompliant Code Example
In this noncompliant code example, the second operand of the logical OR operator invokes a function that results in side effects:
``` c
char *p = /* Initialize; may or may not be NULL */
if (p || (p = (char *) malloc(BUF_SIZE)) ) {
  /* Perform some computation based on p */
  free(p);
  p = NULL;
} else {
  /* Handle malloc() error */
  return;
}
```
Because `malloc()` is called only if `p` is `NULL` when entering the `if` clause, `free()` might be called with a pointer to local data not allocated by `malloc()`. (See [MEM34-C. Only free memory allocated dynamically](MEM34-C_%20Only%20free%20memory%20allocated%20dynamically).) This behavior is partially due to the uncertainty of whether or not `malloc()` is actually called.
## Compliant Solution
In this compliant solution, a second pointer, `q`, is used to indicate whether `malloc()` is called; if not, `q` remains set to `NULL`. Passing `NULL` to `free()` is guaranteed to safely do nothing.
``` c
char *p = /* Initialize; may or may not be NULL */
char *q = NULL;
if (p == NULL) {
  q = (char *) malloc(BUF_SIZE);
  p = q;
}
if (p == NULL) {
  /* Handle malloc() error */
  return;
}
/* Perform some computation based on p */
free(q);
q = NULL;
```
## Risk Assessment
Failing to understand the short-circuit behavior of the logical OR or AND operator may cause unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP02-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | logop-side-effect | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP02 | Fully implemented |
| Compass/ROSE |  |  | Could detect possible violations of this recommendation by reporting expressions with side effects, including function calls, that appear on the right-hand side of an && or || operator |
| Helix QAC | 2024.4 | C3415 |  |
| Klocwork | 2024.4 | MISRA.LOGIC.SIDEEFF |  |
| LDRA tool suite | 9.7.1 | 35 D1 Q
133 S
406 S
408 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP02-a | The right-hand operand of a logical && or || operator shall not contain side effects |
| PC-lint Plus | 1.4 | 9007 | Fully supported |
| RuleChecker | 24.04 | logop-side-effect | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | SideEffectInRightHandSideOfLogical |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP02-CPP. Be aware of the short-circuit behavior of the logical AND and OR operators |
| MITRE CWE | CWE-768, Incorrect short circuit evaluation |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152225) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152053)
## Comments:

|  |
| ----|
| I'm not sure I buy this universally, because though it can certainly be confusing, the rules are rock-solid clear on what's done when.
if ( p || (p = malloc(100)) )
{
Â;Â Â  /* do stuff with p */
}
else
{
Â Â Â  /* cannot do stuff with p */
}

I am pretty sure I've done plenty of things like this that are readable and reliable.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 13, 2008 21:05
\| \|
Seconded.; I have also seen code like:
> [!note]  
>
>     Â if ((rc = function1(...)) == FUNCSUCC &&
>         (rc = function2(...)) == FUNCSUCC &&
>         (rc = function3(...)) == FUNCSUCC)
>     {
>         ...safe - all functions succeeded...
>     }
>     else
>     {
>         ...one function failed, and rc contains its non-success return code...
>     }Â 

Again, perfectly safe because of the sequence points, and if the same error will be generated regardless of which of the functions failed.  (We can debate the error reporting in this function - perhaps the called functions reported the error themselves.)
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 15, 2008 21:59
\| \|
Would this be clearer as:
``` java
if (p == NULL) p = malloc(100);
if (p == NULL) {
  /* handle error */
  return;
}
/* do stuff with p */
```
If so, then maybe we shouldn't make an exception to this recommendation for this reason.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 16, 2008 12:50
\| \|
Both these comments suggest that it should be OK to have side effects in the second operands of the logical AND and OR operators, if the side effects are caused by a function invocation.
Still, I think there are clearer ways to write each example that doesn't require violating this recommendation. Also, this is only a recommendation (that is, a suggestion as to how code can be written more clearly).
We've also been contemplating a recommendation not to allow assignment in a conditional, as this construction has clearly been a cause of program error, and disallowing it would allow static analysis tools to check for the problems caused by using '=' instead of '=='.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 16, 2008 12:55
\| \|
I disagree with this as a general rule.; It is okay to caution about this, but I've written and seen a lot of code where the best way to express something involves a side effect in the second operand, and not always as a function call.  E.g.
while (i \< MAX && ++i \< j) ...
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 14:20
\| \|
I'm afraid I must concur with the naysayers on this rule. Unlike our other rules that also 'verge on coding style', this rule is condemning properties of C behavior that are well-defined, well-behaved, and well-understood. So this rule exists not because of ambiguity in compiler implementations or the C standards but because of psychology...we are scared that programmers don't understand the short-circuiting of && and \|\|.
I agree that the first non-compliant code example is bad, but then I don't like ++ inside if-clauses in general, due to the vaguries of sequence points. Why was the NCCE written that way in the first place? It seems contrived and artificial.
The 2nd NCCE is bad, but mainly because you can't separate the cases of p already being defined, and malloc failing...both dump you into the else clause. (Also p isn't initialized, but that's easily fixed.)
There are several reasonable-looking counterexamples in the comments. They are all fairly abstract; we would need to flesh one out to cite it in the rule.
I think the basic problem with this rule is, what constitutes a 'side effect'? I know 'side effect' has a precise definition in C, but that definition diverges from the English definition of something changing outside our focus. Saying `i++` in the if clause in the first NCCE may be a side effect in the C sense, but not in the English sense, since the if clause is all about the value of i, so a programmer will be focused on i and be aware of its change.
In summary, this rule belongs in a style guideline, not a secure coding standard. I could be convinced that this rule is valid by a sufficient 'in the wild' NCCE, esp. if it led to a vul.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2008 14:49
\| \|
This rec is now weaker, it no longer prohibits side effects in && or \|\|, just warns the user about their short-circuit behavior.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 09, 2008 16:14
\| \|
Code structures should not be unrolled into nested conditions.; For verification (e.g. at the highest levels of criticality, DO-178B Level A) we need to show that every condition has an effect on its outcome. Unrolling the conditions makes it more difficult to see the effect each individual condition has on the outcome, and some combinations are difficult to unroll.  (try recoding: if (a \|\| b) && c { ...,  and another construct   if (a && b)  \|\| c {...
Substituting arithmetic operators for logical ones compounds the problem because the order of evaluation is not fixed and with side effects the results depend on compiler choices. These choices are effected by code instrumentation typically used for measurement of code coverage while testing. What you test may not be what finally runs.
By the way, don't assume that the compiler will evaluate your conditions in short circuit order just because you have used short circuit forms.  Often compilers will change logical operators to arithmetic operators because it reduces the number of branches in the code and this reduces the number of times the pipeline is stalled.  Thankfully these optimizations are turned off, if possible side effects are detected.
![](images/icons/contenttypes/comment_16.png) Posted by romanski@verocel.com at Feb 06, 2009 15:09
\| \|
Are you recommending a change to this rule, or the creation of one or more additional rules? If so, could you flesh these out a little?
I'm not concerned about the optimizations of the short circuit order... sounds like a reasonable application of the "as if" rule provided their are no side effects.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 07, 2009 04:12
\| \|
> By the way, don't assume that the compiler will evaluate your conditions in short circuit order just because you have used short circuit forms. Often compilers will change logical operators to arithmetic operators because it reduces the number of branches in the code and this reduces the number of times the pipeline is stalled. Thankfully these optimizations are turned off, if possible side effects are detected.

According to C99 6.5.13:
> Unlike the bitwise binary & operator, the && operator guarantees left-to-right evaluation; there is a sequence point after the evaluation of the first operand. If the first operand compares equal to 0, the second operand is not evaluated.

and 6.5.14 has a similar paragraph regarding \|\|.
Reordering of \|\|/&& expressions is only permitted as long as they don't change the outcome; the 'as if' rule Rob cites.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 09, 2009 10:45
\| \|
This is covered by MISRA rule 13.5 (2012 edition), information shall be updated
![](images/icons/contenttypes/comment_16.png) Posted by jeromedern at Jan 25, 2018 10:30
\|
