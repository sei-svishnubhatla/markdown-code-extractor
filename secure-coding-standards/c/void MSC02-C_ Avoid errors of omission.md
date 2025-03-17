> [!warning]  
>
> This guideline has been deprecated by
>
> -   [EXP16-C. Do not compare function pointers to constant values](EXP16-C_%20Do%20not%20compare%20function%20pointers%20to%20constant%20values)
> -   [EXP46-C. Do not use a bitwise operator with a Boolean-like operand](EXP46-C_%20Do%20not%20use%20a%20bitwise%20operator%20with%20a%20Boolean-like%20operand)
> -   [EXP45-C. Do not perform assignments in selection statements](EXP45-C_%20Do%20not%20perform%20assignments%20in%20selection%20statements)

Errors of omission occur when necessary characters are omitted, and the resulting code still compiles cleanly but behaves in an unexpected fashion.
This recommendation is related to [void MSC03-C. Avoid errors of addition](void%20MSC03-C_%20Avoid%20errors%20of%20addition) and [EXP00-C. Use parentheses for precedence of operation](EXP00-C_%20Use%20parentheses%20for%20precedence%20of%20operation).
## Noncompliant Code Example
This conditional block is executed only if `b` does not equal zero.
``` c
if (a = b) {
 /* ... */
}
```
Although this behavior might be intended, it is almost always a case of the programmer mistakenly using the assignment operator `=` instead of the equals operator `==`. Consequently, many compilers will warn about this condition. By following [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels), the analyzer can readily detect this coding mistake.
## Compliant Solution
This conditional block is now executed when `a` is equal to `b`.
``` c
if (a == b) {
 /* ... */
}
```
Following is an alternative compliant solution:
``` java
if ((a = b) != 0) {
 /* ... */
}
```
It is less desirable, in general, depending on what was intended, because it mixes the assignment in the condition, but it is clear that the programmer intended the assignment to occur.
## Noncompliant Code Example
This noncompliant code example was taken from an actual [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) ([VU#837857](http://www.kb.cert.org/vuls/id/837857)) discovered in some versions of the X Window System server. The vulnerability exists because the programmer neglected to provide the open and close parentheses following the `geteuid()` function identifier. As a result, the `geteuid` token returns the address of the function, which is never equal to zero. Consequently, the `or` condition of this `if` statement is always true and access is provided to the protected block for all users. Many compilers issue a warning noting such pointless expressions. By following [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels), the analyzer can readily detect this coding mistake.
``` c
/* First the options that are only allowed for root */
if (getuid() == 0 || geteuid != 0) {
  /* ... */
}
```
### Implementation-Specific Details
This error can often be detected through the analysis of compiler warnings. For example, when this code is compiled with some versions of the GCC compiler:
``` java
#include <unistd.h>
#include <stdlib.h>
int main(void) {
  geteuid ? exit(0) : exit(1);
}
```
the following warning is generated:
``` java
example.c: In function 'main':
example.c:6: warning: the address of 'geteuid', will always
  evaluate as 'true'
```
## Compliant Solution
The solution is to provide the open and close parentheses following the `geteuid` token so that the function is properly invoked.
``` c
/* First the options that are only allowed for root */
if (getuid() == 0 || geteuid() != 0) {
  /* ... */
}
```
## Noncompliant Code Example
A similar mistake can occur if you use `&` instead of `&&`.
``` c
if (!(getuid() & geteuid() == 0)) {
  /* ... */
}
```
This example attempts to rewrite the previous compliant solution by negating the `if` condition; however, it errs by using `&`, instead of `&&`. Consequently, if the effective UID is 0, and the real UID is also 0, the `if` condition will unexpectedly pass.
## Compliant Solution
The best solution is to use `&` or `|` only for bitwise operations and to use `&&` or `||` only for logical operations.
``` c
if (!(getuid() && geteuid() == 0)) {
  /* ... */
}
```
## Risk Assessment
Errors of omission can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC02-C | low | likely | medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Coverity | 2017.07 | BAD_COMPARE | Can detect the specific instance where the address of a function is compared against 0, such as in the case of geteuid versus getuid() in the implementation-specific details. |
| Coverity | 6.5 | MISSING_RETURN | Fully Implemented |
| LDRA tool suite | 9.7.1 | 99 S132 S | Fully implemented. |
| GCC | 4.3.5 | ; | Can detect violations of this recommendation when the -Wall flag is used. |
| Compass/ROSE | ; | ; | Could detect violations of this recommendation by identifying any assignment expression as the top-level expression in an if or while statement. To identify the geteuid example, ROSE should search forany "address of function" expression, where the address is implicit (e.g., the function is not preceded by &).The function expression is used in any expression exceptas an argument to another function (signal(), for instance)as an assignment to a function pointer |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 04280536 0537331432263326 | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC02-C).
## Related Guidelines
[SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682): [VOID MSC02-CPP. Avoid errors of omission](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+MSC02-CPP.+Avoid+errors+of+omission)
[ISO/IEC TS 17961](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISO/IEC%20TR%2017961) (Draft) No assignment in conditional expressions \[boolagn\]
[ISO/IEC TR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24772) "KOA Likely incorrect expressions"
[MITRE CWE](http://cwe.mitre.org/): [CWE-482](http://cwe.mitre.org/data/definitions/482.html), "Comparing instead of assigning"
[MITRE CWE](http://cwe.mitre.org/): [CWE-480](http://cwe.mitre.org/data/definitions/480.html), "Use of incorrect operator"
## Sources
\[[Hatton 1995](AA.-Bibliography_87152170.html#AA.Bibliography-Hatton95)\] Section 2.7.2, "Errors of omission and addition"
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MSC01-C.+Strive+for+logical+completeness?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=362) [](https://www.securecoding.cert.org/confluence/display/seccode/MSC03-C.+Avoid+errors+of+addition?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Well the converse of the compliant if statement would be RUID != 0 && EUID == 0. That is, the user running the process is not root, but the effective ID is root. I believe that is possible only if the program has the setuid bit set to root. So the clause fails to execute the program is setuid-root and is invoked by an unpriveleged user.
In the non-compliant code, the clause executes even for the unpriveleged user and setuid-root. Presumably it does something that root can do but an unprivileged user shouldn't, thereby causing the vulnerability.
                                        Posted by svoboda at Apr 15, 2008 10:15
                                     |
| It should be noted that many compilers will warn about if(a=b), which can be recoded as if((a=b)!=0) to eliminate the warning.
The "alternate compliant solutions" have different semantics, and neither is "less desirable" (one is plain wrong, but we don't know which without more context).; It should show both, separated by "or" and followed by "depending on what was intended".
Another real-world example, probably more important (and to some extent covered by another rule) is
if (a & b == 0)
which almost certainly should have been
if ((a & b) == 0)
That's an error that I still have to struggle to avoid, despite decades of C programming experience.
                                        Posted by dagwyn at Apr 18, 2008 13:43
                                     |
| Another example of critical missing code:
if (var1 == value1 & var2 == value2) ...

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 19, 2008 13:45
\| \|
AFAICT the 1st NCCE isn't covered by either of the EXP rules that are listed as deprecating this rule. Do we intend the 1st NCCE to now be perfectly kosher code?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 08, 2010 15:15
\| \|
It's addressed in [EXP18-C. Do not perform assignments in selection statements](/confluence/pages/createpage.action?spaceKey=c&title=EXP18-C.+Do+not+perform+assignments+in+selection+statements)
It looks like this guideline was renamed but the link didn't update for some reason.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Dec 08, 2010 18:39
\|
