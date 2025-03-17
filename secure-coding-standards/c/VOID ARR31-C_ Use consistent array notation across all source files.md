> [!warning]  
>
> This guideline has been deprecated.  It has been superseded by:
>
> -   [DCL40-C. Do not create incompatible declarations of the same function or object](DCL40-C_%20Do%20not%20create%20incompatible%20declarations%20of%20the%20same%20function%20or%20object)

Using a consistent notation to declare variables, including arrays, across multiple files or translation units is essential. Failing to do so results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) (see [undefined behavior 15](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_15)  in Annex J of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]).
This requirement is not always obvious because, within the same file, arrays are converted to pointers when passed as arguments to functions, which means that the function prototype definitions
``` java
void func(char *a);
```
and
``` java
void func(char a[]);
```
are exactly equivalent.
However, outside of function prototypes, these notations are not equivalent if an array is declared using pointer notation in one file and array notation in a different file.
## Noncompliant Code Example
The variable `a` is declared as a pointer to `char` in `main.c`. Storage for the array is allocated, and the `insert_a()` function is called:
``` c
/* main.c source file */
#include <stdlib.h>
enum { ARRAYSIZE = 100 };
char *a;
extern void insert_a(void);
int main(void) {
  a = (char *)malloc(ARRAYSIZE);
  if (a == NULL) {
    /* Handle allocation error */
  }
  insert_a();
  return 0;
}
```
The same identifier is declared as an array of `char` of unspecified size in the `insert_a.c` file. In C, this is considered an [incomplete type](BB.-Definitions_87152273.html#BB.Definitions-incompletetype), the storage for which is defined elsewhere. Because the definitions of `a` are inconsistent, the assignment to `a[0]` results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
/* insert_a.c source file */
char a[];
void insert_a(void) {
  a[0] = 'a';
}
```
## Compliant Solution
Use consistent notation in both files. This is best accomplished by defining variables in a single source file, declaring variables as `extern` in a header file and including the header file where required. This practice eliminates the possibility of creating multiple, conflicting declarations and ensures that the intent of the code is clearly demonstrated. This is particularly important during maintenance, when a programmer may modify one declaration but fail to modify others.
The solution for this example now includes three files. The include file `insert_a.h` provides declarations of the `insert_a()` function and the variable `a`.
``` c
/* insert_a.h include file */
#ifndef INSERT_A_H
#define INSERT_A_H
enum { ARRAYSIZE = 100 };
extern char *a;
void insert_a(void);
#endif 
```
The `insert_a.h` header file is included in the source file `insert_a.c`. The source file provides the definition for `insert_a()`.
``` c
/* insert_a.c source file */
#include "insert_a.h"
char *a;
void insert_a(void) {
   a[0] = 'a';
}
```
The `main.c` source file includes the `insert_a.h` header file to provide a definition for the `insert_a()` function and the variable `a`.
``` c
/* main.c source file */
#include <stdlib.h>
#include "insert_a.h"
int main(void) {
  a = (char *)malloc(ARRAYSIZE);
  if (a == NULL) {
    /* Handle allocation error */
  }
  insert_a();
  return 0;
}
```
## Risk Assessment
Using different array notation across source files may result in the overwriting of system memory.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR31-C | low | unlikely | medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 1 X | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 1510 | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR31-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ARR31-CPP. Use consistent array notation across all source files |
| ISO/IEC TS 17961 | Declaring the same function or object in incompatible ways [funcdecl] |

## Bibliography

|  |  |
| ----|----|
| ISO/IEC 9899:2011] | Annex J, subclause J.2, "Undefined Behavior"; |
| [Hatton 1995] | Section 2.8.3 |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/ARR30-C.+Do+not+form+or+use+out+of+bounds+pointers+or+array+subscripts?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=263) [](https://www.securecoding.cert.org/confluence/display/seccode/ARR32-C.+Ensure+size+arguments+for+variable+length+arrays+are+in+a+valid+range?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| > The best defense on this is to put the declaration in a header file and define the variable in exactly one source file in the program.
One of my programming paradigms is to never do "extern" in a .c file: not only must the declarations go in a header file, but they *must* be included by the definition module so that mismatches are detected.
Perhaps: "All extern declarations in header files must be visible to the defining variable to detect mismatches" ?
                                        Posted by steve at Mar 13, 2008 23:48
                                     |
| This rule appears to be subsumed by:DCL40-C. Incompatible declarations of the same function or objectAnd is a strong candidate to be eliminated and/or merged consistent with ISO/IEC TR 17961 (Draft) Declaring the same function or object in incompatible ways [funcdecl]Please let me know ASAP if you have any objections.
                                        Posted by rcs at Jan 09, 2013 14:48
                                     |

