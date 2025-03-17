If a relation exists between constants, you should encode the relationship in the definitions. Do not give two independent definitions, because a maintainer may fail to preserve that relationship when modifying the code. As a corollary, do not encode an impermanent or false relationship between constants, because future modifications may result in an incorrect definition for the dependent constant.
## Noncompliant Code Example
In this noncompliant code example, the definition for `OUT_STR_LEN` must always be two greater than the definition of `IN_STR_LEN`. The following definitions fail to embody this relationship:
``` c
enum { IN_STR_LEN=18, OUT_STR_LEN=20 };
```
A programmer performing maintenance on this program would need to identify the relationship and modify both definitions accordingly. Although this sort of error appears relatively benign, it can easily lead to serious security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), such as buffer overflows.
## Compliant Solution
The declaration in this compliant solution embodies the relationship between the two definitions:
``` c
enum { IN_STR_LEN=18, OUT_STR_LEN=IN_STR_LEN+2 };
```
As a result, a programmer can reliably modify the program by changing the definition of `IN_STR_LEN`.
## Noncompliant Code Example
In this noncompliant code example, a relationship is established between two constants where none exists:
``` c
enum { ADULT_AGE=18 };
/* Misleading; relationship established when none exists */
enum { ALCOHOL_AGE=ADULT_AGE+3 };
```
A programmer performing maintenance on this program may modify the definition for `ADULT_AGE` but fail to recognize that the definition for `ALCOHOL_AGE` has also been changed as a consequence.
## Compliant Solution
This compliant solution does not assume a relationship where none exists:
``` c
enum { ADULT_AGE=18 };
enum { ALCOHOL_AGE=21 };
```
## Risk Assessment
Failing to properly encode relationships in constant definitions may lead to the introduction of defects during maintenance. These defects could potentially result in [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), for example, if the affected constants were used for allocating or accessing memory.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL08-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL08-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL08-CPP. Properly encode relationships in constant definitions |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] | Rule 1-4 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152364) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152089)
## Comments:

|  |
| ----|
| This is common when encoding the limit of enumerations:
enum { TYPE_READ=1, TYPE_WRITE, TYPE_SYMBOL, TYPE_BLAH, TYPE_MAX = 5 }; // badÂ;

``` java
enum { TYPE_READ=1, TYPE_WRITE, TYPE_SYMBOL, TYPE_BLAH, TYPE_MAX = TYPE_BLAH }; // better
```
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 13, 2008 20:12
\| \|
`TYPE_MAX = TYPE_BLAH` is subject to being wrong if someone inserts another type past `BLAH` and doesn't notice they need to adjust `MAX`. My typical enumeration is like this:
``` java
typedef enum {
  TYPE_INVALID = 0,
  TYPE_FOO,
  /* ... */
  TYPE_BLAH,
  TYPE_COUNT  /\* MUST BE LAST\! \*/
} myType_t;
```
Of course, `COUNT` isn't always an accurate count, as some values may be skipped, but it will generally do for such purposes, and of course range-checking (`valid` must be `> INVALID` and `< COUNT`).
The assignment of 0 to `INVALID` achieves the same thing that I suspect you're trying to do, but makes it explicit. (That is, avoid valid values in uninitialized memory. This can't be completely achieved, but at least making the most common uninitialized value invalid, will help.)
![](images/icons/contenttypes/comment_16.png) Posted by davearonson at Mar 14, 2008 08:37
\| \|
In the compliant solution, 3\*OUT_STR_LEN will not be the same as OUT_STR_LEN\*3 since the expression is expanded and then evaluated.; A dependent definition with arithmetic needs to be enclosed in parentheses.
![](images/icons/contenttypes/comment_16.png) Posted by cbrowne@cbcs-usa.com at Jul 27, 2009 15:43
\| \|
What you are suggesting would be true if we had used preprocessor macros rather than enumeration types. (Which is why we recommend parentheses around macro expansions). But enumerator initializers are compile-time constants; that is, they are evaluated by the compiler and the resulting value is used in subsequent locations. See C99 Section 6.6 and 6.7.2.2 for more background information.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 28, 2009 17:46
\| \|
Minor point: there is no descriptive text in the risk assessment section.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Oct 20, 2009 15:16
\|
