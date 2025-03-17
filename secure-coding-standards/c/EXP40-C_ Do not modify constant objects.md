The C Standard, 6.7.4, paragraph 7 \[[IS](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)[O/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> If an attempt is made to modify an object defined with a `const`-qualified type through use of an [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) with non-`const`-qualified type, the behavior is undefined.

See also [undefined behavior 61](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_61).
There are existing compiler [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) that allow `const`-qualified objects to be modified without generating a warning message.
Avoid casting away `const` qualification because doing so makes it possible to modify `const`-qualified objects without issuing diagnostics. (See [EXP05-C. Do not cast away a const qualification](EXP05-C_%20Do%20not%20cast%20away%20a%20const%20qualification) and [STR30-C. Do not attempt to modify string literals](STR30-C_%20Do%20not%20attempt%20to%20modify%20string%20literals) for more details.)
## Noncompliant Code Example
This noncompliant code example allows a constant object to be modified:
``` c
const int **ipp;
int *ip;
const int i = 42;
void func(void) {
  ipp = &ip; /* Constraint violation */
  *ipp = &i; /* Valid */
  *ip = 0;   /* Modifies constant i (was 42) */
}
```
The first assignment is unsafe because it allows the code that follows it to attempt to change the value of the `const` object `i`.
### Implementation Details
If `ipp`, `ip`, and `i` are declared as automatic variables, this example compiles without warning with Microsoft Visual Studio 2013 when compiled in C mode (`/TC`) and the resulting program changes the value of `i`. GCC 4.8.1 generates a warning but compiles, and the resulting program changes the value of `i`.
If `ipp`, `ip`, and `i` are declared with static storage duration, this program compiles without warning and terminates abnormally with Microsoft Visual Studio 2013, and compiles with warning and terminates abnormally with GCC 4.8.1.
## Compliant Solution
The compliant solution depends on the intent of the programmer. If the intent is that the value of `i` is modifiable, then it should not be declared as a constant, as in this compliant solution:
``` c
int **ipp;
int *ip;
int i = 42;
void func(void) {
  ipp = &ip; /* Valid */
  *ipp = &i; /* Valid */
  *ip = 0; /* Valid */
}
```
If the intent is that the value of i is not meant to change, then do not write noncompliant code that attempts to modify it.  
## Risk Assessment
Modifying constant objects through nonconstant references is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP40-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | assignment-to-non-modifiable-lvaluepointer-qualifier-cast-constpointer-qualifier-cast-const-implicitwrite-to-constant-memory | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP40 |  |
| Coverity | 2017.07 | PWMISRA C 2004 Rule 11.5 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-exp40-c |  |
| Helix QAC | 2024.4 | C0563 |  |
| LDRA tool suite | 9.7.1 | 582 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP40-a | A cast shall not remove any 'const' or 'volatile' qualification from the type of a pointer or reference |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP40-C | Checks for write operations on const qualified objects (rule fully covered) |
| RuleChecker | 24.04 | assignment-to-non-modifiable-lvaluepointer-qualifier-cast-constpointer-qualifier-cast-const-implicit | Partially checked |
| TrustInSoft Analyzer | 1.38 | mem_access | Exhaustively verified (see the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP40-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | EXP05-C. Do not cast away a const qualification | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | STR30-C. Do not attempt to modify string literals | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 6.7.4, "Type Qualifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152294) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151934)
## Comments:

|  |
| ----|
| This is entirely spurious.; The posted example is NOT LEGAL C.  The compiler will not allow the line marked CONSTRAING VIOLATION.   There is nothing here that is not handled by the "DON'T CAST AWAY CONST" recommendation as a cast would have to be added to cause the above to be compilable.
                                        Posted by ron at Aug 31, 2006 18:40
                                     |
| ;This example will certainly compile... it even compiles without warning on MS VS with /W4.
 It is also not the same as do not cast away const, because there is no cast used in the example.  
                                        Posted by rcs at Sep 07, 2006 14:51
                                     |
| With MS VS 2008 - it generates an error - here is the portion of the error message
1>.... error C2440: '=' : cannot convert from 'char **' to 'const char **'
1>        Conversion loses qualifiers

It does not matter what the Warning level is.
I have a general suggestion - regarding the box (panel) that contains the code (NCCE or CS), is it possible that these boxes can be made to display the line number in them ? Thank you
![](images/icons/contenttypes/comment_16.png) Posted by abhi at Mar 07, 2008 12:44
\| \|
I agree that this is spurious: not even MSVC6 compiles this code.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 13, 2008 22:24
\| \|
We may want to eliminate this rule.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 13, 2008 08:19
\| \|
VS compiles this code, even 8.0, depends on VS version. Whether anyone is using that versions is a different story.
``` java
(work):/tmp>cat tmp.c
void foo()
{
    char const **cpp;
    char *cp;
    char const c = 'A';
    cpp = &cp; /* constraint violation */
    *cpp = &c; /* valid */
    *cp = 'B'; /* valid */
}
(work):/tmp>cl -c tmp.c
Microsoft (R) 32-bit C/C++ Optimizing Compiler Version 12.00.8804 for 80x86
Copyright (C) Microsoft Corp 1984-1998. All rights reserved.
tmp.c
(work):/tmp>cl -c tmp.c
Microsoft (R) 32-bit C/C++ Optimizing Compiler Version 13.10.3077 for 80x86
Copyright (C) Microsoft Corporation 1984-2002. All rights reserved.
tmp.c
(work):/tmp>cl -c tmp.c
Microsoft (R) 32-bit C/C++ Optimizing Compiler Version 14.00.50727.42 for 80x86
Copyright (C) Microsoft Corporation.  All rights reserved.
tmp.c
(work):/tmp>
```
![](images/icons/contenttypes/comment_16.png) Posted by piotrkrukowiecki at Sep 21, 2009 05:29
\| \|
This rule is dead..we decided it was unsustainable.
You might look at [03. Expressions (EXP)](/confluence/pages/createpage.action?spaceKey=c&title=03.+Expressions+%28EXP%29) for rules we still consider valid and supply comments there.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 21, 2009 09:47
\| \|
As discussed in the thread starting with this [comment](https://www.securecoding.cert.org/confluence/display/seccode/EXP05-C.+Do+not+cast+away+a+const+qualification?focusedCommentId=40075547#comment-40075547) in [EXP05-C. Do not cast away a const qualification](EXP05-C_%20Do%20not%20cast%20away%20a%20const%20qualification), this rule is valid and valuable despite there being non-compliant examples that conforming implementations accept and generate code that runs with no adverse effects. For instance, the well-formed but non-compliant example below abends with `SIGSEGV` when compiled with gcc on Linux x64. I will go ahead and restore this rule.
``` java
const char s[] = "foo";
int main() {
  *(char*)s = '\0';
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 12, 2010 21:27
\| \|
Restored to its original glory pursuant to the discussion [Re: EXP05-C. Do not cast away a const qualification](https://www.securecoding.cert.org/confluence/display/seccode/EXP05-C.+Do+not+cast+away+a+const+qualification?focusedCommentId=40075547#comment-40075547).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 05, 2010 19:25
\| \|
Values cannot be modified. This rule should be renamed to **Do not modify constant objects**.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Nov 08, 2010 22:00
\| \|
The assertion that Visual Studio warns is incorrect – it only warns if compiling in C++ mode (/TP).; When compiling in C mode (/TC) it never warns, even at the highest warning levels.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 21, 2013 11:03
\|
