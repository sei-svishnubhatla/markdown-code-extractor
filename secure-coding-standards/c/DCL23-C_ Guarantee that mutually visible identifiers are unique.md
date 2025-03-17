According to subclause 6.2.7 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> All declarations that refer to the same object or function shall have compatible type; otherwise, the behavior is undefined.

(See also [undefined behavior 14](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_14) of Annex J.)
Further, according to subclause 6.4.2.1,
> Any identifiers that differ in a significant character are different identifiers. If two identifiers differ only in nonsignificant characters, the behavior is undefined.

(See also [undefined behavior 30](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_30) of Annex J.)
Identifiers in mutually visible scopes must be deemed unique by the compiler to prevent confusion about which variable or function is being referenced. [Implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) can allow additional nonunique characters to be appended to the end of identifiers, making the identifiers appear unique while actually being indistinguishable.
It is reasonable for scopes that are not visible to each other to have duplicate identifiers. For example, two functions can each have a local variable with the same name because their scopes cannot access each other. But a function's local variable names should be distinct from each other as well as from all static variables declared within the function's file (and from all included header files.)
To guarantee that identifiers are unique, the number of significant characters recognized by the most restrictive compiler used must be determined. This assumption must be documented in the code.
The standard defines the following minimum requirements:
-   63 significant initial characters in an internal identifier or a macro name. (Each universal character name or extended source character is considered a single character.)
-   31 significant initial characters in an external identifier. (Each universal character name specifying a short identifier of 0000FFFF or less is considered 6 characters; each universal character name specifying a short identifier of 00010000 or more is considered 10 characters; and each extended source character, if any exist, is considered the same number of characters as the corresponding universal character name.)
Restriction of the significance of an external name to fewer than 255 characters in the standard (considering each universal character name or extended source character as a single character) is an obsolescent feature that is a concession to existing implementations. As a result, it is not necessary to comply with this restriction as long as the identifiers are unique and the assumptions concerning the number of significant characters are documented.
## Noncompliant Code Example (Source Character Set)
On implementations that support only the minimum requirements for significant characters required by the standard, this code example is noncompliant because the first 31 characters of the external identifiers are identical:
``` c
extern int *global_symbol_definition_lookup_table_a;
extern int *global_symbol_definition_lookup_table_b;
```
## Compliant Solution (Source Character Set)
In a compliant solution, the significant characters in each identifier must differ:
``` c
extern int *a_global_symbol_definition_lookup_table;
extern int *b_global_symbol_definition_lookup_table;
```
## Noncompliant Code Example (Universal Character Names)
In this noncompliant code example, both external identifiers consist of four universal character names. Because the first three universal character names of each identifier are identical, both identify the same integer array on implementations that support only the minimum requirements for significant characters required by the standard:
``` c
extern int *\U00010401\U00010401\U00010401\U00010401;
extern int *\U00010401\U00010401\U00010401\U00010402;
```
## Compliant Solution (Universal Character Names)
For portability, the first three universal character name combinations used in an identifier must be unique:
``` c
extern int *\U00010401\U00010401\U00010401\U00010401;
extern int *\U00010402\U00010401\U00010401\U00010401;
```
## Risk Assessment
Nonunique identifiers can lead to abnormal program termination, denial-of-service attacks, or unintended information disclosure.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL23-C | Medium | Unlikely | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2012 Rules 5.1, 5.2, 5.3, 5.4 and 5.5. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL23 |  |
| CodeSonar | 8.3p0 | LANG.ID.ND.EXTLANG.ID.ND.MM
LANG.ID.ND.MO
LANG.ID.ND.NEST
LANG.ID.ND.SSLANG.ID.NU.EXT
LANG.ID.NU.INT
LANG.ID.NU.LIBFN
LANG.ID.NU.TAG
LANG.ID.NU.TYPE
LANG.STRUCT.DECL.MGT | Non-distinct identifiers: external namesNon-distinct identifiers: macro/macro
Non-distinct identifiers: macro/other
Non-distinct identifiers: nested scope
Non-distinct identifiers: same scopeNon-unique identifiers: external name
Non-unique identifiers: internal name
Library Function Override
Non-unique identifiers: tag
Non-unique identifiers: typedefGlobal variable declared with different types |
| Compass/ROSE |  |  | Can detect some violations of this rule but cannot flag violations involving universal names |
| Helix QAC | 2024.4 | C0627, C0776, C0777, C0778, C0779, C0789, C0791, C0793 |  |
| Klocwork | 2024.4 | MISRA.IDENT.DISTINCT.C99.2012 |  |
| LDRA tool suite | 9.7.1 | 17 D355 S
61 X | Fully implemented |
| PC-lint Plus | 1.4 | 621 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL23-C | Checks for:External identifiers not distinctIdentifiers in same scope and namespace not distinctMacro identifier not distinctName for macros and identifiers not distinctRec. fully covered. |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2012 Rules 5.1, 5.2, 5.3, 5.4 and 5.5. |
| SonarQube C/C++ Plugin | 3.11 | IdentifierLongerThan31 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL32-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Choice of Clear Names [NAI]Identifier Name Reuse [YOW] |
| MISRA C:2012 | Rule 5.1 (required)Rule 5.2 (required)
Rule 5.3 (required)
Rule 5.4 (required)
Rule 5.5 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.2.7, "Compatible Type and Composite Type"Subclause 6.4.1, "Keywords" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152049) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](../c/Rec_%2010_%20Environment%20_ENV_)
## Comments:

|  |
| ----|
| Really long identifiers are bad anyway, from a human-factors perspective.; Two 31-character identifiers that differ only in the 20th character are likely to be mistaken for each other, and take too long to comprehend when reading the code.
                                        Posted by dagwyn at Apr 15, 2008 13:55
                                     |
| I've updated this rule to reference bullet 14  of Appendix J but in hindsight I'm not 100% sure the two are necessarily related.
One insidious problem, one that could potentially be exploited, is with identifiers that aren't "visible" in the same scope but that are declared to have external linkage. For example, suppose file a.c contains the following definition of function square():
/* a.c */
int square(int x) { return x * x; }

while file `b.c` contains this definition:
``` java
/* b.c */
double square(double i) { return x * x; }
```
Linking these two translation units together causes a violation of bullet 14 regardless of whether the two functions are "visible" in the same scope. In fact, if they were visible, the violation would be easily detected by any compiler and diagnosed, but when they're not it typically couldn't be, which is where the undefined behavior comes in.
On the other hand, the cases described in this rule would, in all likelihood, lead to compiler or linker errors (and thus not represent a security flaw).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 10, 2010 01:23
\| \|
Dan Quinlan, who sometimes participates in this group, has a paper on "[Support for Whole-Program Analysis and the Verification of the One-Definition Rule in C++](http://vuduc.org/pubs/quinlan2006-odr.pdf)" The One-Definition Rule (ODR) violation states that types and functions appearing in multiple compilation units must be defined identically. So apparently, this is a problem in C++ but I'm not sure if it extends to C or not.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 10, 2010 08:42
\| \|
Yes, in C++, when permitted, multiple definitions must be token-by-token identical. For example, if `square()` were defined `inline`, it would have to expand to same set of lexical tokens in each translation unit.
The closest requirement I can find in C is:
> #### J.5.11 Multiple external definitions
>
> There may be more than one external definition for the identifier of an object, with or without the explicit use of the keyword extern; if the definitions disagree, or more than one is initialized, the behavior is undefined (6.9.2).

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 10, 2010 10:54
\| \|
Perhaps another NCCE would be opaque structures from different translation units.; Eg)
``` java
// Foo.h
typedef struct Foo_ Foo;
Foo *create_foo(int x, int y);
void print_foo(Foo *fp);
// Foo.c
#include "Foo.h"
#include <malloc.h>
struct Foo_ {
  int x;
  int y;
};
Foo *create_foo(int x, int y) {
  Foo *ret = (Foo *)malloc(sizeof(Foo));
  ret->x = x;
  ret->y = y;
  return ret;
}
// Bar.c
#include "Foo.h"
#include <stdio.h>
struct Foo_ {
  int y;
  int x;
};
void print_foo(Foo *fp) {
  printf("x: %d, y %d\n", fp->x, fp->y);
}
// main.c
#include "Foo.h"
int main(void) {
  Foo *fp = create_foo(10, 20);
  print_foo(fp);
  return 0;
}
```
This would (potentially, given the UB) print x: 20, y: 10 instead of x:10, y: 20 while not providing a linking error in C.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 22, 2013 15:13
\|
