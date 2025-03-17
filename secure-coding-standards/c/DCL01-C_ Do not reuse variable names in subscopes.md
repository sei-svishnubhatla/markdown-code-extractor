Do not use the same variable name in two scopes where one scope is contained in another. For example,
-   No other variable should share the name of a global variable if the other variable is in a subscope of the global variable.
-   A block should not declare a variable with the same name as a variable declared in any block that contains it.
Reusing variable names leads to programmer confusion about which variable is being modified. Additionally, if variable names are reused, generally one or both of the variable names are too generic.
## Noncompliant Code Example
This noncompliant code example declares the `msg` identifier at file scope and reuses the same identifier to declare a character array local to the `report_error()` function. The programmer may unintentionally copy the function argument to the locally declared `msg` array within the `report_error()` function. Depending on the programmer's intention, it either fails to initialize the global variable `msg` or allows the local `msg` buffer to overflow by using the global value `msgsize` as a bounds for the local buffer.
``` c
#include <stdio.h>
static char msg[100];
static const size_t msgsize = sizeof( msg);
void report_error(const char *str) {
  char msg[80];
  snprintf(msg, msgsize, "Error: %s\n", str);
  /* ... */
}
int main(void) {
  /* ... */
  report_error("some error");
  return 0;
}
```
## Compliant Solution
This compliant solution uses different, more descriptive variable names:
``` c
#include <stdio.h>
static char message[100];
static const size_t message_size = sizeof( message);
void report_error(const char *str) {
  char msg[80];
  snprintf(msg, sizeof( msg), "Error: %s\n", str);
  /* ... */
}
int main(void) {
  /* ... */
  report_error("some error");
  return 0;
}
```
When the block is small, the danger of reusing variable names is mitigated by the visibility of the immediate declaration. Even in this case, however, variable name reuse is not desirable. In general, the larger the declarative region of an identifier, the more descriptive and verbose should be the name of the identifier.
By using different variable names globally and locally, the compiler forces the developer to be more precise and descriptive with variable names.
## Noncompliant Code Example
This noncompliant code example declares two variables with the same identifier, but in slightly different scopes. The scope of the identifier `i` declared in the `for` loop's initial clause terminates after the closing curly brace of the for loop. The scope of the identifier i declared in the `for` loop's compound statement terminates before the closing curly brace. Thus, the inner declaration of `i` hides the outer declaration of `i`, which can lead to unintentionally referencing the wrong object.
``` c
void f(void) {
  for (int i = 0; i < 10; i++) {
    long i;
    /* ... */
  }
}
```
## Compliant Solution
This compliant solution uses a unique identifier for the variable declared within the `for` loop.
``` c
void f(void) {
  for (int i = 0; i < 10; i++) {
    long j;
    /* ... */
  }
}
```
## Exceptions
**DCL01-C-EX1:** A function argument in a function declaration may clash with a variable in a containing scope provided that when the function is defined, the argument has a name that clashes with no variables in any containing scopes.
``` c
extern int name;
void f(char *name);  /* Declaration: no problem here */
/* ... */
void f(char *arg) {  /* Definition: no problem; arg doesn't hide name */
  /* Use arg */
}
```
**DCL01-C-EX2:** A temporary variable within a new scope inside of a macro can override an identifier in a containing scope. However,this exception does not apply to to the arguments of the macro itself.
``` c
#define SWAP(type, a, b) do { type tmp = a; a = b; b = tmp; } while(0)
void func(void) {
  int tmp = 100;
  int a = 10, b = 20;
  SWAP(int, a, b); /* Hidden redeclaration of tmp is acceptable */
  SWAP(int, tmp, b); /* NONCOMPLIANT: Hidden redeclaration of tmp clashes with argument */
}
```
## Risk Assessment
Reusing a variable name in a subscope can lead to unintentionally referencing an incorrect variable.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL01-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2012 Rule 5.3. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL01 |  |
| CodeSonar | 8.3p0 | LANG.ID.ND.NEST | Non-distinct identifiers: nested scope |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.DCL01 | Fully implemented |
| Helix QAC | 2024.4 | C0795, C0796, C2547, C3334 |  |
| Klocwork | 2024.4 | MISRA.VAR.HIDDEN |  |
| LDRA tool suite | 9.7.1 | 131 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL01-aCERT_C-DCL01-b | Identifier declared in a local or function prototype scope shall not hide an identifier declared in a global or namespace scopeIdentifiers declared in an inner local scope should not hide identifiers declared in an outer local scope |
| PC-lint Plus | 1.4 | 578 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL01-C | Checks for variable shadowing (rule fully covered) |
| PVS-Studio | 7.35 | V561, V688, V703, V711, V2015 |  |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2012 Rule 5.3. |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL01-CPP. Do not reuse variable names in subscopes |
| MISRA C:2012 | Rule 5.3 (required) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152463) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152407)
## Comments:

|  |
| ----|
| The first NCE and CS should differ only in the specific violation being addressed by this guideline.
                                        Posted by rcs_mgr at Feb 10, 2010 20:51
                                     |
| Why aren't there any parentheses around msg in these two lines: 
static const size_t msgsize = sizeof msg;
snprintf(msg, sizeof msg, "Error: %s\n", str);

The variable names in the CS have changed as compared to the NCE.
Also, the sentence "either failing to initialize the assign global variable,..." doesn't seem to need the word "assign".
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Mar 08, 2010 00:00
\| \|
I rewrote the parragraph with the assign type you cite. While saying `sizeof msg` is syntactically valid C, our styling conventions typically use parentheses after sizeof, which makes it look like a C function (although it is an operator, not a function.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 09, 2010 12:03
\| \|
There are four kinds of scopes:
-   file scope
-   function prototype scope
-   function scope
-   block scope
With the last three scopes always being "nested" in the file scope. I think it would be worthwhile to mention them in the introduction and explain the differences so that we can then formally refer to them in the examples.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 10, 2010 10:24
\| \|
Agreed. I've no idea if this rule is meant to apply to names declared in both file scope and in a struct. (They could clash if the struct has methods, but that is not common inn C.)
;
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 07, 2012 13:31
\| \|
Exception 2 is dangerous. Doing `SWAP(``int``, tmp, b);` wouldn't work as intended.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 15:30
\| \|
Good point. I've amended the exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 20, 2020 10:24
\|
