An empty infinite loop that does nothing within the loop body is a suboptimal solution because it consumes CPU cycles but performs no useful operations. An optimizing compiler can remove such a loop, which can lead to unexpected results. According to the C Standard, subclause 6.8.5, paragraph 6 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> An iteration statement whose controlling expression is not a constant expression, that performs no input/output operations, does not access volatile objects, and performs no synchronization or atomic operations in its body, controlling expression, or (in the case of a for statement) its expression-3, may be assumed by the implementation to terminate.157157) This is intended to allow compiler transformations, such as removal of empty loops, even when termination cannot be proven.

## Noncompliant Code Example
This noncompliant code example implements an idle task that continuously executes a loop without executing any instructions within the loop. An optimizing compiler could remove the `while` loop in the example.
``` c
static int always = 1;
int main(void) {
  while (always) { }
}
```
## Compliant Solution (`while`)
To avoid the loop being optimized away, this compliant solution uses a constant expression `(1)` as the controlling expression in the `while` loop:
``` c
int main(void) {
  while (1) { }
}
```
## Compliant Solution (`for)`
According to the C Standard, subclause 6.8.5.3, paragraph 2, omitting the *expression-2* from a `for` loop will replace that expression with a nonzero constant.
``` c
int main(void) {
  for (;;) { }
}
```
## Exceptions
**MSC40-EX1:** In rare cases, use of an empty infinite loop may be unavoidable. For example, an empty loop may be necessary on a platform that does not support `sleep(3)` or an equivalent function. Another example occurs in OS kernels. A task started before normal scheduler functionality is available may not have access to `sleep(3)` or an equivalent function.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC40-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ECLAIR | 1.2 | CC2.MSC40 | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC40-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT Oracle Secure Coding Standard for Java | MSC01-J. Do not use an empty infinite loop |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.8.5, "Iteration Statements" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MSC39-C.+Do+not+call+va_arg()+on+a+va_list+that+has+indeterminate+value?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=362) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1336)
## Comments:

|  |
| ----|
| Joshua Wise says, via email:;

    I disagree with your interpretation of the C specification; I think you
    have the sense of their statement reversed.  In particular, the
    specification says:
    "An iteration statement whose controlling expression is *not* a constant
    expression [...and-clause including some other things...] may be assumed
    by the implementation to terminate." [1]
    You interpret this to mean that the following fragment: |
     while (1)
       ;
    | can be optimized out.
    I do not believe this to be the case.  In this case, the controlling
    expression is |1|; |1| is a constant expression.  We can verify this with
    the following sequence:
    joshua@bruges:~$ cat test.c
    int test[1];
    int main(int argc, char **argv) { return 0; }
    joshua@bruges:~$ cc -o /dev/null test.c -Wall -ansi -std=c1x
    joshua@bruges:~$ cc -v
    Apple clang version 4.1 (tags/Apple/clang-421.11.66) (based on LLVM
    3.1svn)
    "Constant expression" has a specific meaning in the specification (see
    section 6.6).  Notably, some things that one might expect to be constant
    expressions are not -- for instance, the expression |"foo"[0]|, although
    one might intuitively expect it to be a constant of |'f'|, is not:
    joshua@bruges:~$ cat test.c
    int test["foo"[0]];
    int main(int argc, char **argv) { return 0; }
    joshua@bruges:~$ cc -o /dev/null test.c -Wall -ansi -std=c1x
    test.c:1:5: error: variable length array declaration not allowed at file
    scope
    int test["foo"[0]];
       ^    ~~~~~~~~
    1 error generated.
    For more fun with compile-time constants, consider the last brainteaser on
    my page:
     http://joshuawise.com/c-brainteasers
    You may wish to consider appropriately updating this page.  In particular,
    the insinuation that it is sound for a compiler to optimize out a loop of
    the above form is dangerous, and should be corrected.
    Thanks!
    joshua
    [1] For convenience, I cite
    http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf; PDF page 168,
    real page 150.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 22, 2013 14:06
\| \|
I agree with your interpretation, and have adjusted the code samples accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 22, 2013 14:54
\| \|
I find the exception confusing; in the first code example, there is no reason for using the volatile variable since a constant expression would be acceptable.; In the second code example, a constant expression is used and so disabling optimizations isn't necessary.  I believe the exception can be removed entirely.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 20, 2013 11:08
\| \|
I lied.; The exception should remain, the examples in the exception were what could be (and have been) removed.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 24, 2013 12:18
\| \|
So I'm largely confused by this rule.;  The rule is "MSC40-C. Do not use an empty infinite loop" but the examples are all about how to code an empty infinite loop that isn't optimized out.
Shouldn't the title be something like "Beware of compiler optimizations when using an empty infinite loop"?
In other English related news, I'm wondering if all our "be aware" rules should be "beware" rules, because we are trying to warn the user of something.
I think I still question the value of this rule.  First, it is probably of interest to several programmers in the world.  Second, I doubt that anyone could fail to notice that their infinite loop wasn't working.  Perhaps we could keep it because it is small, but it still adds to our rule count.
The other beware of compiler optimizations rule is actually a recommendation, and a much more interesting one at that.  Maybe this should be a recommendation as well, because not all compilers are going to perform this optimization, so the noncompliant code example may be valid on some implementations.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 03, 2013 05:58
\| \|
I agree that the title does not match the contents and should be rectified if we retain the guideline.; Whether this is a rule, a recommendation, or a VOID is up in the air.  Non-terminating loops are not UB, the only information here is how to write a non-terminating loop.  We don't really have any other guidelines like that (at least not that I can find).  So I think my feeling is that this should be VOIDed.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 04, 2013 10:15
\|
