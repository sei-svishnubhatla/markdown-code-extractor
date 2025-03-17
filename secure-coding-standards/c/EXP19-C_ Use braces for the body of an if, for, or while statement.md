Opening and closing braces for `if`, `for`, and `while` statements should always be used even if the statement's body contains only a single statement.
If an `if`, `while`, or `for` statement is used in a macro, the macro definition should not conclude with a semicolon. (See [PRE11-C. Do not conclude macro definitions with a semicolon](PRE11-C_%20Do%20not%20conclude%20macro%20definitions%20with%20a%20semicolon).)
Braces improve the uniformity and readability of code. More important, when inserting an additional statement into a body containing only a single statement, it is easy to forget to add braces because the indentation gives strong (but misleading) guidance to the structure.
Braces also help ensure that macros with multiple statements are properly expanded. Such a macro should be wrapped in a `do-while` loop. (See [PRE10-C. Wrap multistatement macros in a do-while loop](PRE10-C_%20Wrap%20multistatement%20macros%20in%20a%20do-while%20loop).) However, when the `do-while` loop is not present, braces can still ensure that the macro expands as intended.
## Noncompliant Code Example
This noncompliant code example uses an `if` statement without braces to authenticate a user:
``` c
int login;
if (invalid_login())
  login = 0;
else
  login = 1;
```
A developer might add a debugging statement to determine when the login is valid but forget to add opening and closing braces:
``` c
int login;
if (invalid_login())
  login = 0;
else
  printf("Login is valid\n");  /* Debugging line added here */
  login = 1;                   /* This line always gets executed
                               /* regardless of a valid login! */
```
Because of the indentation of the code, it is difficult to tell that the code will not function as intended by the programmer, potentially leading to a security breach.
## Compliant Solution
In the compliant solution, opening and closing braces are used even when the body is a single statement:
``` c
int login;
if (invalid_login()) {
  login = 0;
} else {
  login = 1;
}
```
## Noncompliant Code Example
This noncompliant code example has an `if` statement nested in another `if` statement without braces around the `if` and `else` bodies:
``` c
int privileges;
if (invalid_login())
  if (allow_guests())
    privileges = GUEST;
else
  privileges = ADMINISTRATOR;
```
The indentation could lead the programmer to believe that a user is given administrator privileges only when the user's login is valid. However, the `else` statement actually attaches to the inner `if` statement:
``` c
int privileges;
if (invalid_login())
  if (allow_guests())
    privileges = GUEST;
  else
    privileges = ADMINISTRATOR;
```
This is a security loophole: users with invalid logins can still obtain administrator privileges.
## Compliant Solution
In the compliant solution, adding braces removes the ambiguity and ensures that privileges are correctly assigned:
``` c
int privileges;
if (invalid_login()) {
  if (allow_guests()) {
    privileges = GUEST;
  } 
} else {
  privileges = ADMINISTRATOR;
}
```
## Noncompliant Code Example (empty block)
This noncompliant code example has a `while` statement with no block:
``` c
while (invalid_login());
```
Note that if `invalid_login()` has no side effects (such as warning the user if their login failed), this code also violates [MSC12-C. Detect and remove code that has no effect or is never executed](MSC12-C_%20Detect%20and%20remove%20code%20that%20has%20no%20effect%20or%20is%20never%20executed).
## Compliant Solution (empty block)
This compliant solution features an explicit empty block, which clarifies the developer's intent:
``` c
while (invalid_login()) {}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP19-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 | compound-ifelsecompound-loop | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP19 | Fully implemented |
| Helix QAC | 2024.4 | C2212 |  |
| Klocwork | 2024.4 | MISRA.IF.NO_COMPOUNDMISRA.STMT.NO_COMPOUND |  |
| LDRA tool suite | 9.7.1 | 11 S,; 12 S, 428 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP19-a | The statement forming the body of a 'switch', 'while', 'do...while' or 'for' statement shall be a compound statement |
| PC-lint Plus | 1.4 | 9012 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP19-C | Checks for iteration or selection statement body not enclosed in braces (rec. fully covered) |
| PVS-Studio | 7.35 | V563, V628, V640, V705 |  |
| RuleChecker | 24.04 | compound-ifelsecompound-loop | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S121 |  |

### Related Vulnerabilities
[CVE-2014-1266](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-1266) was due, in large part, to failing to follow this recommendation. There is a spurious "goto fail" statement on line 631 of [sslKeyExchange.c](http://opensource.apple.com/source/Security/Security-55471/libsecurity_ssl/lib/sslKeyExchange.c?txt). This "goto" gets executed unconditionally, even though it is indented as if it were part of the preceding "if" statement.  As a result, the call to sslRawVerify (which performs the actual signature verification) is rendered dead code.  \[[ImperialViolet 2014](https://www.imperialviolet.org/2014/02/22/applebug.html)\]. If the body of the "if" statement had been enclosed in braces, then this defect likely would not have happened.
## Related Guidelines

|  |  |
| ----|----|
| MISRA C:2012 | Rule 15.6 (required) |

##  Bibliography

|  |  |
| ----|----|
| [GNU 2010] | Coding Standards, Section 5.3, "Clean Use of C Constructs" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152223) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](../c/EXP20-C_%20Perform%20explicit%20tests%20to%20determine%20success,%20true%20and%20false,%20and%20equality)
## Comments:

|  |
| ----|
| 
    To show how nefarious the 1st NCCE is, I would switch the then-body and else-body, so that the NCCE with debug statement inadverntaly  allows an invalid user to log in.
    The 1st NCCE is compelling in demonstrating that this is a security issue. The 2nd NCCE is theoretical hence not compelling...please provide a real-world example (you could use logins/passwords again). Also mention how C99 treats the NCCE (IIRC the else attaches to the outermost if).
    The third NCCE is already covered by PRE10-C. Wrap multi-statement macros in a do-while loop.
    Need Risk Assessment and References sections.
                                        Posted by svoboda at Mar 05, 2010 10:45
                                     |
| A better term than a single body line is a single statement: there could be more than one statement on a line:
if (a == 1)
  b = 2; c = 3;   // two statements on one line

This guideline is especially relevant when [PRE11-C. Do not conclude macro definitions with a semicolon](PRE11-C_%20Do%20not%20conclude%20macro%20definitions%20with%20a%20semicolon) isn't being followed. It would be nice to tie the two together on both ends (and do the same for [PRE10-C. Wrap multi-statement macros in a do-while loop](/confluence/pages/createpage.action?spaceKey=seccode&title=PRE10-C.+Wrap+multi-statement+macros+in+a+do-while+loop) that you already mentioned here).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 05, 2010 10:58
\| \|
By tying the two together on both ends, do you mean that I should edit PRE11-C and PRE10-C too?
![](images/icons/contenttypes/comment_16.png) Posted by josephlu at Mar 13, 2010 14:46
\| \|
-   The 1st NCCE already allows an invalid user to log in; however, do you mean to switch the bodies as such:
``` java
if (valid_login())
  login = 1;
else
  login = 0;
```
In that case adding a debugging statement would throw an error when compiling, because of a dangling `else` statement not paired with a corresponding `if` statement:
``` java
if (valid_login())
  printf(&quot;Login Successful\n&quot;);  /* debugging statement added here */
  login = 1;
else                             /* unpaired else statement */
  login = 0;
```
-   The else actually attaches to the innermost if, hence I modified the 2nd NCCE to include an additional statement in the body of the first `if` statement.
<!-- -->
-   I recognize my code for the 3rd NCCE is similar to that of [PRE10-C. Wrap multi-statement macros in a do-while loop](/confluence/pages/createpage.action?spaceKey=c&title=PRE10-C.+Wrap+multi-statement+macros+in+a+do-while+loop). However, PRE10-C does not specify using braces. I was trying to show that even if one did not follow PRE10-C's recommendation to wrap multi-statement macros in a do-while statement, the situation can still be salvaged if braces are used in the code itself. How can I best do this?
![](images/icons/contenttypes/comment_16.png) Posted by josephlu at Mar 14, 2010 09:01
\| \|
That's what I meant, yes. Have each of them reference this guideline, and have this one reference the other two, for completeness.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 14, 2010 16:55
\| \|
The definition of the `SWAP()` macro in PRE10-C is suboptimal since it tacitly assumes that the `tmp` variable is declared and of the same type as the arguments but for the purposes of this exercise it could be defined as a single expression (note that this definition violates [PRE12-C. Do not define unsafe macros](PRE12-C_%20Do%20not%20define%20unsafe%20macros)):
``` java
#define SWAP(x, y) ((tmp = a), ((a) = (b)), ((b) = tmp))
```
In my opinion, using a `swap` function would be better (although not entirely without problems either):
``` java
#define SWAP(x, y)  swap(&x, &y, sizeof x)
inline void swap(void *x, void *y, size_t nbytes) {
  unsigned char tmp [nbytes];
  memcpy(tmp, x, nbytes);
  memcpy(x, y, nbytes);
  memcpy(y, tmp, nbytes);
}
```
Another possible solution is to rely on a language extension such as gcc's `typeof` operator and [Statements in Expressions](http://gcc.gnu.org/onlinedocs/gcc/Statement-Exprs.html#Statement-Exprs) (although this one skirts [MSC14-C. Do not introduce unnecessary platform dependencies](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies) in addition to violating PRE33-C):
``` java
#define SWAP(x, y) ({ typeof x tmp = (x); (x) = (y); (y) = tmp; })
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 14, 2010 17:31
\| \|
In addition to my earlier comments, can you provide a hyperlink to the GNU coding standards?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2010 10:05
\| \|
Can I also provide hyperlinks to non-authoritative, personal web pages that discuss using braces in `if` statements?
Also, does my recommendation fulfil your earlier comments?
![](images/icons/contenttypes/comment_16.png) Posted by josephlu at Mar 18, 2010 17:19
\| \|
> Can I also provide hyperlinks to non-authoritative, personal web pages that discuss using braces in if statements?

Yes, but only if you can't find any 'authoritative' pages. Books discussing C would prob be best, followed by official standards (eg MISRA) followed by well-known webpages (eg famous bloggers or stackoverflow.com).
-   Your third NCCE is already covered by [PRE10-C. Wrap multi-statement macros in a do-while loop](/confluence/pages/createpage.action?spaceKey=c&title=PRE10-C.+Wrap+multi-statement+macros+in+a+do-while+loop). You should probably just drop it as it is redundant.
<!-- -->
-   I was hoping to see a NCCE based in the inherent ambiguity of an else clause. Consider this surprising NCCE:
``` java
if (valid_login())
  if (is_normal())
    privileges = NORMAL;
else
  privileges = NONE;
```
which grants no privileges to the administrator. (The binding of an else clause to the innermost if statement is an arbitrary decision made by the standards committee long ago...back in the ANSI days I think.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2010 19:57
\| \|
Where do you get the information in "Automated detection" table from? Is it from the tool vendors? Or are you building this list on your own?
I ask this because I just found that this precise rule can be scanned using Coverity (tested with v8.5.0). You simply need to run a MISRA C 2012 scan using rule 15.6 checker. Could this information;be added in the "Automated detection" table?
![](images/icons/contenttypes/comment_16.png) Posted by philippe.mazet at Aug 28, 2017 11:52
\| \|
Before we can publish any commercial SA tool capabilities, we need permission from the vendors. Most of the AD information you cite is added by the vendors themselves. Which constitutes permission, in my book;![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 31, 2017 15:55
\| \|
In the newly added exception, the keywords should be in code font. Also, was;`do` left off that list purposefully?
FWIW, I'm not a fan of the new exception though I understand why it was added. I think empty compound statements should be encouraged because it calls out the oddity of the code.
    if (something()); // Hard to spot
    if (something()) {} // Easier to spot
    if (something()) { /* Explanation */ } // Even better
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Feb 06, 2019 11:03
\| \|
At a minimum, I think the new exception should be expanded to make explicit that an "empty body" means a trailing;`;` (altho 9 times out of 10 that trailing `;` is probably actually a bug).
![](images/icons/contenttypes/comment_16.png) Posted by ann.campbell at Feb 06, 2019 11:58
\| \|
I excluded do statements b/c the rec did. Since they are typically do...while statements, I assumed that they are a subset of while statements.
I'm now leaning against the exception...that is, empty statements should require an explicit {} block for clarity. I'll make this change tomorrow if I don't hear otherwise.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 06, 2019 16:28
\| \|
About the exception i would specify that test condition must have effect (MSC12-C).
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Feb 07, 2019 01:41
\| \|
I support removing the exception entirely.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Feb 07, 2019 07:53
\| \|
I support this last proposition : execute test condition for doing nothing seems strange. It is the meaning; of my post after. ("About the exception i would specify that test condition must have effect (MSC12-C).")
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Feb 07, 2019 08:47
\| \|
I've replaced the exception with a NCCE/CS pair, which mandates explicit empty blocks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 07, 2019 09:12
\|
