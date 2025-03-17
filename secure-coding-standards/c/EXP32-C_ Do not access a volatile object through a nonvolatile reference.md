An object that has volatile-qualified type may be modified in ways unknown to the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) or have other unknown [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect). Referencing a volatile object by using a non-volatile lvalue is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The C Standard, 6.7.4 paragraph 7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> If an attempt is made to refer to an object defined with a volatile-qualified type through use of an lvalue with non-volatile-qualified type, the behavior is undefined.

See [undefined behavior 62](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_62).
## Noncompliant Code Example
In this noncompliant code example, a volatile object is accessed through a non-volatile-qualified reference, resulting in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <stdio.h>
void func(void) {
  static volatile int **ipp;
  static int *ip;
  static volatile int i = 0;
  printf("i = %d.\n", i);
  ipp = &ip; /* May produce a warning diagnostic */
  ipp = (int**) &ip; /* Constraint violation; may produce a warning diagnostic */
  *ipp = &i; /* Valid */
  if (*ip != 0) { /* Valid */
    /* ... */
  }
}
```
The assignment `ipp = &ip` is not safe because it allows the valid code that follows to reference the value of the volatile object `i` through the non-volatile-qualified reference `ip`. In this example, the compiler may optimize out the entire `if` block because `*ip != 0` must be false if the object to which `ip` points is not volatile.
### Implementation Details
This example compiles without warning on Microsoft Visual Studio 2013 when compiled in C mode (`/TC`) but causes errors when compiled in C++ mode (`/TP`).
GCC 4.8.1 generates a warning but compiles successfully.
## Compliant Solution
In this compliant solution, `ip` is declared `volatile`:
``` c
#include <stdio.h>
void func(void) {
  static volatile int **ipp;
  static volatile int *ip;
  static volatile int i = 0;
  printf("i = %d.\n", i);
  ipp = &ip;
  *ipp = &i;
  if (*ip != 0) {
    /* ... */
  }
}
```
## Risk Assessment
Accessing an object with a volatile-qualified type through a reference with a non-volatile-qualified type is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP32-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-qualifier-cast-volatilepointer-qualifier-cast-volatile-implicit | Supported indirectly via MISRA C 2012 Rule 11.8 |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP32 | Fully implemented |
| Clang | 3.9 | -Wincompatible-pointer-types-discards-qualifiers |  |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISRA C 2012 Rule 11.8 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-exp32-c |  |
| GCC | 4.3.5 |  | Can detect violations of this rule when the -Wcast-qual flag is used |
| Helix QAC | 2024.4 | C0312, C0562, C0563, C0673, C0674 | Fully implemented |
| Klocwork | 2024.4 | CERT.EXPR.VOLATILE.ADDRCERT.EXPR.VOLATILE.ADDR.PARAM
CERT.EXPR.VOLATILE.PTRPTR | Fully implemented |
| LDRA tool suite | 9.7.1 | 344 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP32-a | A cast shall not remove any 'const' or 'volatile' qualification from the type of a pointer or reference |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP32-C | Checks for cast to pointer that removes const or volatile qualification (rule fully covered) |
| RuleChecker | 24.04 | pointer-qualifier-cast-volatilepointer-qualifier-cast-volatile-implicit | Supported indirectly via MISRA C 2012 Rule 11.8 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Type System [IHN] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 11.8 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | EXP55-CPP. Do not access a cv-qualified object through a cv-unqualified type | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.7.4, "Type Qualifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152202) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152129)
## Comments:

|  |
| ----|
| One problem, this is a rule but EXP05-C. Do not cast away a const qualification is a recommendation.  It seems to me that they should both be rules, or both be recommendations.  We could replace  EXP40-C. Do not modify constant values with EXP05-C. Do not cast away a const qualification as this EXP31-C should probably be eliminated.  This opens up a hole in the recommendation IDs, but this can be fixed.
                                        Posted by rcs at May 14, 2008 19:54
                                     |
| C++ has the 'mutable' keyword and the const_cast template, which is precisely meant to handle cases where one would (otherwise) need to cast away const. IOW in the C++ world casting away const is so common that it has been accepted as necesasry. 
For example, suppose you have a static dictionary object (declared const), but for optimization purposes, you add to it a most-recently-used cache. The cache changes with each lookup, but it is part of a const dictionary...how to handle? Typically, you declare the cache mutable in the Dictionary::lookup() function, or you use const_cast just when you update the cache (and otherwise, leave it const).
So, IMHO casting away const is a rec, not a rule.
I'd be happy to put 'cast-away-volatile' as a rec not a rule, if there is any similar experience (or at least a code sample) illustrating the usefulness. I don't think casting away volatile actually buys you anything. So I'm (currently) happy with this as a rule, but the const analogue being a rec.
                                        Posted by svoboda at May 15, 2008 14:54
                                     |
| I find Myself slightly confused.; The rule text states "Do not cast away a volatile qualification".  However, the example involving the cast of &ip does not constitute a syntactic casting away of volatile qualification.  How does this cast constitute a violation of EXP32-C?  The explanatory text seems inconsistent with respect to the guideline text.
Additionally, if "The assignment ipp = &ip is unsafe", would this assignment also constitute a  guideline violation?
Lastly, does the guideline apply to all variables or just pointers?
Thanks in advance.
                                        Posted by xuinkrbin. at Jan 29, 2009 12:10
                                     |
| C99, Section 6.7.3, paragraph 5, sez:
If an attempt is made to modify an object defined with a const-qualified type through use of an lvalue with non-const-qualified type, the behavior is undefined. If an attempt is made to refer to an object defined with a volatile-qualified type through use of an lvalue with non-volatile-qualified type, the behavior is undefined.)
I agree with Frank. The NCCE does display bad code.  Not because volatile is cast away, but rather because a volatile object is assigned to a non-volatile pointer, yielding what the standard calls 'undefined behavior', and the compiler is free to optimize the subsequent comparison, as explained in the NCCE.
Recent discussion on the wg14 mailing list suggests that while 'volatile' is a type-qualifier, which applies to type of a variable, the volatile-ness atribute applies to the memory. (eg the int in the NCCE.
Perhaps this rule should be titled "Do not access a volatile object via a non-volatile reference" instead. I suspect that casting away volatile on a varialble is not always a problem (what if the variable's object was not volatile to begin with?)
                                        Posted by svoboda at Jan 30, 2009 11:35
                                     |
| 
Lastly, does the guideline apply to all variables or just pointers?
The guideline would apply to all variables. All relevant examples use pointers because to have multiple variables referring to the same object you either need to use typecasting & multiple scopes (via function calls) or use pointers.
                                        Posted by svoboda at Jan 30, 2009 11:37
                                     |
| Just so we're on the same page – mutable keyword is not at all like casting away const.; In C++, if you cast away const and then mutate the object, you cause undefined behavior.  Eg)
const char *str = "Huttah!";
char *str2 = const_cast<char *>(str);
*str2 = 'B';  // Undefined behavior

 See \[expr.const.cast\]p7 and \[dcl.type.cv\]p4 for more information.
The mutable keyword is different in that it is used for logical constness (this is why you can only apply it to members).  The encapsulating class can provide a const interface to the user when there are no *externally visible* changes.  In your case with a cached dictionary object, the caller sees a completely const interface; the fact that there is a cache under the hood is an implementation detail the caller is not privy to.  So mutable is applied to the *container* in terms of its constness, not the field.
Not that this has anything to do with this particular rule.  ![](images/icons/emoticons/wink.svg)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 17, 2013 11:57
\| \|
On GCC 10.x the warning detecting the issue is "incompatible-pointer-types", not "cast-qual"
![](images/icons/contenttypes/comment_16.png) Posted by prose at Mar 08, 2023 09:00
\|
