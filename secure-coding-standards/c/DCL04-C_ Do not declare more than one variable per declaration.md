Every declaration should be for a single variable, on its own line, with an explanatory comment about the role of the variable. Declaring multiple variables in a single declaration can cause confusion regarding the types of the variables and their initial values. If more than one variable is declared in a declaration, care must be taken that the type and initialized value of the variable are handled correctly.
## Noncompliant Code Example
In this noncompliant code example, a programmer or code reviewer might mistakenly believe that the two variables `src` and `c` are declared as `char *`. In fact, `src` has a type of `char *`, whereas `c` has a type of `char`.
``` c
char *src = 0, c = 0;
```
## Compliant Solution
In this compliant solution, each variable is declared on a separate line:
``` c
char *src;    /* Source string */
char c;       /* Character being tested */
```
Although this change has no effect on compilation, the programmer's intent is clearer.
## Noncompliant Code Example
In this noncompliant code example, a programmer or code reviewer might mistakenly believe that both `i` and `j` have been initialized to 1. In fact, only `j` has been initialized, and `i` remains uninitialized.
``` c
int i, j = 1;
```
## Compliant Solution
In this compliant solution, it is readily apparent that both `i` and `j` have been initialized to 1:
``` c
int i = 1;
int j = 1;
```
## Exceptions
**DCL04-C-EX1:** Multiple loop control variables can be declared in the same `for` statement, as shown in the following function:
``` c
#include <limits.h>  /* For CHAR_BIT */
#include <stddef.h>  /* For size_t   */
extern size_t popcount(uintmax_t);
#define PRECISION(umax_value) popcount(umax_value) 
 size_t bitcount(size_t n) {
  const size_t limit = PRECISION(SIZE_MAX);
  size_t count = 0;
  for (size_t i = 0, j = 1; i < limit; ++i, j <<= 1) {
    if (n & j)
      ++count;
  }
  return count;
}
```
The `PRECISION()` macro provides the correct precision for any integer type and is defined in [INT35-C. Use correct integer precisions](https://www.securecoding.cert.org/confluence/display/seccode/INT35-C.+Use+correct+integer+precisions)—see that rule for more information.
**DCL04-C-EX2:** Multiple, simple variable declarations can be declared on the same line given that there are no initializations. A simple variable declaration is one that is not a pointer or array.
``` c
int i, j, k;
```
## Risk Assessment
Declaring no more than one variable per declaration can make code easier to read and eliminate confusion.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL04-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL04 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.DECL.ML | Multiple Declarations on Line |
| ECLAIR | 1.2 | CC2.DCL04 | Fully implemented |
| LDRA tool suite | 9.7.1 | 579 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL04-a | Each variable should be declared in a separate declaration statement |
| PC-lint Plus | 1.4 | 9146 | Partially supported: exceptions not supported |
| SonarQube C/C++ Plugin | 3.11 | SingleDeclarationPerStatement |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL04-CPP. Do not declare more than one variable per declaration |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152090) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152187)
## Comments:

|  |
| ----|
| I am sorry my comment was not complete- I meant
int j;
int i = j = 1;

![](images/icons/contenttypes/comment_16.png) Posted by abhi at Feb 22, 2008 03:48
\| \|
This style point relates to the same thing: many programmers like to (foolishly) bind the pointer-to \* to the basic type, and this makes the confusion even worse:
``` java
char*Â;Â  p, q;   /* confusing */
char    *p, q;  /* a bit less so */Â 
```
Avoid this practice
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 15, 2008 13:47
\| \|
The only time I can see that the second would be remotely beneficial is if the initializer is more complex, such as a function call, and even then, I would say that this:
> [!note]
>
>     int i = some_complex_function(p, q, r+3);
>
>     int j = i;

is preferable to the presumed alternative:
> [!note]  
>
>     int i;
>     int j = i = some_complex_function(p, q, r+3);

![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 15, 2008 14:51
\| \|
I think this is orthogonal to the current recommendation, because your examples are compliant with this recommendation and are consequently allowed by the standard. I don't think this is worth adding a separate recommendation to do this, so I'll probably just end it there for now.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 06, 2008 09:38
\| \|
Compass/ROSE automatically parses the AST into one variable/declaration... which is peculiar, b/c the interface makes it seems like a declaration contains a vector of variable :/
Oh well, tagging as rose-na for the meanwhile
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 16, 2008 14:03
\| \|
I disagree with this rule.
Declaring multiple variables in a single declaration makes sense if the rest of the code requires all these variables to have identical type.; If, in the course of maintenance, the type of these variables needs to be changed (e.g., from int to long), the number of locations in the code requiring changes is minimized.
If each variable is declared separately, then each declaration needs to be changed.  This decreases maintainability.
The problem is solvable by introducing a new typedef, but this is too heavyweight in most cases--i.e., I have never seen it in practice (except in my own code).
![](images/icons/contenttypes/comment_16.png) Posted by konrad.schwarz@gmail.com at Aug 25, 2008 05:04
\| \|
I see this as more of an exception to, rather than an invalidation, of the entire rule. What do you think?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 25, 2008 21:09
\| \|
What about an exception when the declared type is identical and no initialization is required?; Eg)
``` java
// Output parameters
void foo( int *i, int *j, int *k );
void func( void ) {
  int i, j, k;
  foo( &i, &j, &k );
}
```
 It seems that separating the declarations in this situation really provides limited benefits.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 13, 2013 16:07
\| \|
The variables have to be simple types and not arrays or pointers:
``` java
int *i, j, k; // oops, what did dev really mean?
```
For 'simple types' we allow multiple vars on one line in the analogous guideline in Java.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 14, 2013 10:18
\|
