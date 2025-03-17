Linkage can make an identifier declared in different scopes or declared multiple times within the same scope refer to the same object or function. Identifiers are classified as *externally linked*, *internally linked*, or *not linked*. These three kinds of linkage have the following characteristics \[[Kirch-Prinz 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Kirch-Prinz02)\]:
-   **External linkage:** An identifier with external linkage represents the same object or function throughout the entire program, that is, in all compilation units and libraries belonging to the program. The identifier is available to the linker. When a second declaration of the same identifier with external linkage occurs, the linker associates the identifier with the same object or function.
<!-- -->
-   **Internal linkage:** An identifier with internal linkage represents the same object or function within a given translation unit. The linker has no information about identifiers with internal linkage. Consequently, these identifiers are internal to the translation unit.
<!-- -->
-   **No linkage:** If an identifier has no linkage, then any further declaration using the identifier declares something new, such as a new variable or a new type.
According to the C Standard, 6.2.2 paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], linkage is determined as follows:
> If the declaration of a file scope identifier for:    - an object contains any of the storage-class specifiers static  or contexpr;
>
>     - or, a function contains the storage-class specifier static,
>
>  then the identifier has internal linkage.
>
> For an identifier declared with the storage-class specifier extern in a scope in which a prior declaration of that identifier is visible, if the prior declaration specifies internal or external linkage, the linkage of the identifier at the later declaration is the same as the linkage specified at the prior declaration. If no prior declaration is visible, or if the prior declaration specifies no linkage, then the identifier has external linkage.
>
> If the declaration of an identifier for a function has no storage-class specifier, its linkage is determined exactly as if it were declared with the storage-class specifier extern. If the declaration of an identifier for an object has file scope and does not contain the storage-class specifier static or contexpr, its linkage is external.
>
> The following identifiers have no linkage: an identifier declared to be anything other than an object or a function; an identifier declared to be a function parameter; a block scope identifier for an object declared without the storage-class specifier extern.

Use of an identifier (within one translation unit) classified as both internally and externally linked is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See also [undefined behavior 8](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_8).) A translation unit includes the source file together with its headers and all source files included via the preprocessing directive `#include`.
The following table identifies the linkage assigned to an object that is declared twice in a single translation unit. The column designates the first declaration, and the row designates the redeclaration.
![](attachments/87152132/88037711.png)
## Noncompliant Code Example
In this noncompliant code example, `i2` and `i5` are defined as having both internal and external linkage. Future use of either identifier results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
``` c
int i1 = 10;         /* Definition, external linkage */
static int i2 = 20;  /* Definition, internal linkage */
extern int i3 = 30;  /* Definition, external linkage */
int i4;              /* Tentative definition, external linkage */
static int i5;       /* Tentative definition, internal linkage */
int i1;  /* Valid tentative definition */
int i2;  /* Undefined, linkage disagreement with previous */
int i3;  /* Valid tentative definition */
int i4;  /* Valid tentative definition */
int i5;  /* Undefined, linkage disagreement with previous */
int main(void) {
  /* ... */
  return 0;
}
```
### Implementation Details
Microsoft Visual Studio 2013 issues no warnings about this code, even at the highest diagnostic levels.
GCC and Clang 14 both generate fatal diagnostics for the conflicting definitions of `i2` and `i5`.
## Compliant Solution
This compliant solution does not include conflicting definitions:
``` c
int i1 = 10;         /* Definition, external linkage */
static int i2 = 20;  /* Definition, internal linkage */
extern int i3 = 30;  /* Definition, external linkage */
int i4;              /* Tentative definition, external linkage */
static int i5;       /* Tentative definition, internal linkage */
int main(void) {
  /* ... */
  return 0;
}
```
## Risk Assessment
Use of an identifier classified as both internally and externally linked is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL36-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | static-function-declarationstatic-object-declaration | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL36 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.DECL.NOEXT | Missing External Declaration |
| Coverity | 2017.07 | PW.LINKAGE_CONFLICT | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl36-c |  |
| ECLAIR | 1.2 | CC2.DCL36 | Fully implemented |
| GCC | 4.3.5 |  |  |
| Helix QAC | 2024.4 | C0625 | Fully implemented |
| Klocwork | 2024.4 | MISRA.FUNC.STATIC.REDECL | Fully implemented |
| LDRA tool suite | 9.7.1 | 461 S, 575 S, 2 X | Fully implemented |
| PC-lint Plus | 1.4 | 401, 839, 1051 | Fully supported |
| Splint | 3.1.1 |  |  |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL36-a | Identifiers shall not simultaneously have both internal and external linkage in the same translation unit |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL36-C | Checks for inconsistent use of static and extern in object declarations (rule partially covered) |
| RuleChecker | 24.04 | static-function-declarationstatic-object-declaration | Partially checked |
| TrustInSoft Analyzer | 1.38 | non-static declaration follows static declaration | Partially verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL36-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| MISRA C:2012 | Rule 8.2 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 8.4 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 8.8 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 17.3 (mandatory) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Banahan 2003] | Section 8.2, "Declarations, Definitions and Accessibility" |
| [ISO/IEC 9899:2024] | 6.2.2, "Linkages of Identifiers" |
| [Kirch-Prinz 2002] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152112) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152308)
## Attachments:
![](images/icons/bullet_blue.gif) [DCL36-C_table.png](attachments/87152132/88037711.png) (image/png)  
## Comments:

|  |
| ----|
| When I compiled the Non-compliant code example using visual studio 2008 - I get 
......cpp(12) : error C2086: 'int i1' : redefinitionÂ;
......cpp(6) : see declaration of 'i1'Â 

The same message is displayed for the other 4 variables too.
Please consider revising the statement "...Microsoft Visual Studio compile this non-compliant code example without warning..."  I did not have to change the warning level.
![](images/icons/contenttypes/comment_16.png) Posted by abhi at Mar 06, 2008 06:14
\| \|
I only have access to MSVS 2005 right now. At Level 3 (/W3) and at Level 4 (/W4) I get:
------ Build started: Project: DCL36-C, Configuration: Debug Win32 ------ Compiling...  
stdafx.cpp  
Compiling...  
DCL36-C.cpp  
Compiling manifest to resources...  
Linking...  
Embedding manifest...  
Build log was saved at "file://c:\Documents and Settings\rcs\My Documents\Visual Studio\Projects\DCL36-C\DCL36-C\Debug\BuildLog.htm"  
DCL36-C - 0 error(s), 0 warning(s)  
========== Build: 1 succeeded, 0 failed, 0 up-to-date, 0 skipped ==========
But I'll take you word for 2008 and update.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 06, 2008 09:13
\| \|
Studying the standard, I disagree with the assessment of the NCCE. According to the standard, if a variable is declared static, and then declared with no storage-class specifier, it remains static. Thus in the NCCE both `i2` and `i5` should be valid, not invalid.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 25, 2013 15:17
\| \|
David Keaton saez:
> In your comment, I think you might have been confused between static and extern. 6.2.3p4 says "For an identifier with storage-class specifier extern in a scope in which a prior declaration of that identifier is visible, if the prior declaration specifies internal or external linkage, the linkage of the identifier at the later declaration is the same as the linkage specified at the prior declaration." However, there is nothing analogous for static.

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 26, 2013 09:51
\| \|
It only provides those warnings when compiling in C++ mode (/TP), but will not warn even with highest warnings (/Wall) enabled when compiling in C mode (/TC).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 16, 2013 17:20
\| \|
> GCC4.3.5

there is no GCC checker specified.; is is on by default?  if so, can you say that?
![](images/icons/contenttypes/comment_16.png) Posted by rcseacord at Nov 09, 2017 09:05
\| \|
the NCCE seems to come almost verbatim from the standard, see \[6.9.2 Example 1\](<https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1256.pdf>)
(edit: sorry posted then saw that actually MVSC is the one that allows this)
additionally - compiling the example (with clang version 14.0.0) - yields (so seems correct at least with clang): 
``` java
test.c:8:5: error: non-static declaration of 'i2' follows static declaration
int i2;  /* Undefined, linkage disagreement with previous */
    ^
test.c:2:12: note: previous definition is here
static int i2 = 20;  /* Definition, internal linkage */
           ^
test.c:11:5: error: non-static declaration of 'i5' follows static declaration
int i5;  /* Undefined, linkage disagreement with previous */
    ^
test.c:5:12: note: previous definition is here
static int i5;       /* Tentative definition, internal linkage */
```
![](images/icons/contenttypes/comment_16.png) Posted by knewbury01 at Jan 23, 2023 14:48
\| \|
hi ya'll , quick question when trying to create a NCCE from the table...
is the column/row heading that says "no linkage" truly meant to say "no linkage"?
I think it should possibly instead say "no specifier"?
from the standard: "The following identifiers have no linkage: an identifier declared to be anything other than an object or a function; an identifier declared to be a function parameter; a **block scope identifier for an object declared without the storage-class specifier extern**."
so in the current NCCE - int i5; actually has linkage - external linkage (via no specifier) : " If the declaration of an identifier for an object has file scope and no storage-class specifier, its linkage is external." 
this would agree with the table cell (0,1) (row,column) if it were to say (no specifier, static) == undefined.
following this logic a fully comprehensive NCCE would be (if someone wouldn't mind checking this - thanks!!!):
``` java
//-----row 0
static int i1; //internal linkage
static int i1; //COMPLIANT - internal linkage
int i2; //no specifier
//static int i2; //NON_COMPLIANT - undefined - compiler detected
extern int i3; //external linkage
//static int i3; ///NON_COMPLIANT - undefined - compiler detected
//-----row 1
static int i11; //internal linkage
//int i11; //NON_COMPLIANT - undefined - compiler detected
int i22; //no specifier
int i22; //COMPLIANT - no specifier
extern int i33; //external linkage
int i33; //NON_COMPLIANT according to table? (undefined) - BUT not compiler detected? maybe actually fine?
//-----row 2
static int i111; //internal linkage
extern int i111; //COMPLIANT - internal linkage
int i222; //no specifier
extern int i222; //COMPLIANT - external linkage
extern int i333; //external linkage
extern int i333; //COMPLIANT - external linkage
```
![](images/icons/contenttypes/comment_16.png) Posted by knewbury01 at Jan 23, 2023 15:01
\| \|
Kristen:
"No specifier" would also be a decent entry for the table. However there are specifiers other than linkage specifiers, so "no linkage" is more precise.
In the NCCE i5 has no linkage...remember it is outside of any block. If it were defined within main() it would have local linkage; that is, it would live on the stack and only persist until its function (main()) ended.  The re-declaration of i5 in the NCCE is truly undefined, since it was static in its first declaration and had no linkage in its second.
Your code example does correctly represent the table, including which declarations are compliant and which are non-compliant.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 25, 2023 09:30
\| \|
Kristen: Thanks. I've added Clang's behavior to the implementation details.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 25, 2023 09:34
\|
