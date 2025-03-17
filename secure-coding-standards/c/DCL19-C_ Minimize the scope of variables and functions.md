Variables and functions should be declared in the minimum scope from which all references to the identifier are still possible.
When a larger scope than necessary is used, code becomes less readable, harder to maintain, and more likely to reference unintended variables (see [DCL01-C. Do not reuse variable names in subscopes](DCL01-C_%20Do%20not%20reuse%20variable%20names%20in%20subscopes)).
## Noncompliant Code Example
In this noncompliant code example, the function `counter()` increments the global variable `count` and then returns immediately if this variable exceeds a maximum value:
``` c
unsigned int count = 0;
void counter() {
  if (count++ > MAX_COUNT) return;
  /* ... */
}
```
Assuming that the variable `count` is only accessed from this function, this example is noncompliant because it does not define `count` within the minimum possible scope.
## Compliant Solution
In this compliant solution, the variable `count` is declared within the scope of the `counter()` function as a static variable. The static modifier, when applied to a local variable (one inside of a function), modifies the lifetime (duration) of the variable so that it persists for as long as the program does and does not disappear between invocations of the function.
``` c
void counter() {
  static unsigned int count = 0;
  if (count++ > MAX_COUNT) return;
  /* ... */
}
```
The keyword `static` also prevents reinitialization of the variable.
## Noncompliant Code Example
The counter variable `i` is declared outside of the `for` loop, which goes against this recommendation because it is not declared in the block in which it is used. If this code were reused with another index variable `j`, but there was a previously declared variable `i`, the loop could iterate over the wrong variable.
``` c
size_t i = 0;
for (i=0; i < 10; i++){
  /* Perform operations */
}
```
## Compliant Solution
Complying with this recommendation requires that you declare variables where they are used, which improves readability and reusability. In this example, you would declare the loop's index variable `i` within the initialization of the `for` loop. This requirement was recently relaxed in the C Standard.
``` c
for (size_t i=0; i < 10; i++) {
  /* Perform operations */
}
```
## Noncompliant Code Example (Function Declaration)
In this noncompliant code example, the function `f()` is called only from within the function `g()`, which is defined in the same compilation unit. By default, function declarations are *extern*, meaning that these functions are placed in the global symbol table and are available from other compilation units.
``` c
int f(int i) {
  /* Function definition */
}
int g(int i) {
  int j = f(i);
  /* ... */
} 
```
## Compliant Solution
In this compliant solution, the function `f()` is declared with internal linkage. This practice limits the scope of the function declaration to the current compilation unit and prevents the function from being included in the external symbol table. It also limits cluttering in the global name space and prevents the function from being accidentally or intentionally invoked from another compilation unit. See [DCL15-C. Declare file-scope objects or functions that do not need external linkage as static](DCL15-C_%20Declare%20file-scope%20objects%20or%20functions%20that%20do%20not%20need%20external%20linkage%20as%20static) for more information.
``` c
static int f(int i) {
  /* Function definition */
}
int g(int i) {
  int j = f(i);
  /* ... */
} 
```
## Risk Assessment
Failure to minimize scope could result in less reliable, readable, and reusable code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL19-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | local-object-scopeglobal-object-scope | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL19 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.SCOPE.FILELANG.STRUCT.SCOPE.LOCAL | Scope could be file staticScope could be local static |
| ECLAIR | 1.2 | CC2.DCL19 | Fully implemented |
| Helix QAC | 2024.4 | C1504, C1505, C1531, C1532, C3210, C3218 |  |
| Klocwork | 2024.4 | MISRA.VAR.MIN.VISCXX.ID_VIS.GLOBAL_VARIABLE.EXTERN
CXX.ID_VIS.GLOBAL_VARIABLE.STATIC |  |
| LDRA tool suite | ;9.7.1 | 25 D, 61 D, 40 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL19-a | Declare variables as locally as possible |
| PC-lint Plus | 1.4 | 765, 9003 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL19-C | Checks for:Function or object declared without static specifier and referenced in only one fileObject defined beyond necessary scopeRec. partially covered. |
| PVS-Studio | 7.35 | V821 |  |
| RuleChecker | 24.04 | local-object-scopeglobal-object-scope | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL19-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL07-CPP. Minimize the scope of variables and methods |
| MISRA C:2012 | Rule 8.9 (advisory) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152234) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152311)
## Comments:

|  |
| ----|
| Just for clarification, can you provide an example of this recommendation applied to a function declaration?
                                        Posted by jimg at Jan 25, 2013 14:03
                                     |
| I suspect the answer is that a function declaration
int foo(int bar, char baz);

should not provide names for its parameters.
``` java
int foo(int, char);
```
Even better, it can provide them in comments.
``` java
int foo(int /* bar */, char /* baz */);
```
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 28, 2013 09:50
\| \|
I think it probably was just meant to suggest that functions that were only called from within the compilation unit should be declared as static.; I've added an example.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 30, 2013 04:34
\| \|
I recall seeing this before, but I don't remember the justification.; It is certainly common practice to name the parameters, see <http://stackoverflow.com/questions/8174886/put-name-of-parameters-in-c-function-prototypes>
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 30, 2013 04:38
\| \|
Agreed. While I've seen advice not to name the parms (or to name them in comments), I've never seen this used with much force (eg its very weak). On that StackOverflow page the best reason I can see to name the parms (as opposed to naming them in comments) is that they can be easily harvested by an IDE.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 31, 2013 11:14
\| \|
We should add an example of a loop counter being legitimately examined after the loop (such as if it contains a `break`), like this:
    int i;for(i = 0; i < 10; ++i) {
        /* ... */
        if(some condition) break;
        /* ... */
    }
    if(i == 10) {
        /* stuff to do if we didn't break */
    }
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 15:06
\| \|
Looks good...go ahead & add this compliant example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 20, 2020 10:28
\|
