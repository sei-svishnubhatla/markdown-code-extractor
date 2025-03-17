Use visually distinct identifiers with meaningful names to eliminate errors resulting from misreading the spelling of an identifier during the development and review of code. An identifier can denote an object; a function; a tag or a member of a structure, union, or enumeration; a typedef name; a label name; a macro name; or a macro parameter.
Depending on the fonts used, certain characters appear visually similar or even identical:

| Character | Similar Characters |
| ----|----|
| 0 (zero) | O (capital o), Q (capital q), D (capital d) |
| 1 (one) | I (capital i), l (lowercase L) |
| 2 (two) | Z (capital z) |
| 5 (five) | S (capital s) |
| 8 (eight) | B (capital b) |
| n (lowercase N) | h (lowercase H) |
| m (lowercase M) | rn (lowercase R, lowercase N) |

Do not define multiple identifiers that vary only with respect to one or more visually similar characters.
Make the initial portions of long identifiers unique for easier recognition and to help prevent errors resulting from nonunique identifiers. (See [DCL23-C. Guarantee that mutually visible identifiers are unique](DCL23-C_%20Guarantee%20that%20mutually%20visible%20identifiers%20are%20unique).)
In addition, the larger the scope of an identifier, the more descriptive its name should be. It may be perfectly appropriate to name a loop control variable `i`, but the same name would likely be confusing if it named a file scope object or a variable local to a function more than a few lines long. See also [DCL01-C. Do not reuse variable names in subscopes](DCL01-C_%20Do%20not%20reuse%20variable%20names%20in%20subscopes) and [DCL19-C. Use as minimal a scope as possible for all variables and functions](DCL19-C_%20Minimize%20the%20scope%20of%20variables%20and%20functions).
## Noncompliant Code Example (Source Character Set)
DCL02-C implicitly assumes *global scope*, which can be confused with *scope within the same file*. Although it may not generate any errors, a possible violation of the rule may occur, as in the following example. Note this example does not violate [DCL23-C. Guarantee that mutually visible identifiers are unique](DCL23-C_%20Guarantee%20that%20mutually%20visible%20identifiers%20are%20unique).
In file `foo.h`:
``` c
int id_O; /* (Capital letter O) */
```
In file `bar.h`:
``` c
int id_0; /* (Numeric digit zero) */
```
If a file `foobar.c` includes both `foo.h` and `bar.h`, then both `id_0` and `id_0` come in the same scope, violating this rule.
## Compliant Solution (Source Character Set)
In a compliant solution, use of visually similar identifiers should be avoided in the same project scope.
In file `foo.h`:
``` c
int id_a;
```
In file `bar.h`:
``` c
int id_b;
```
## Risk Assessment
Failing to use visually distinct identifiers can result in referencing the wrong object or function, causing unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL02-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL02 |  |
| CodeSonar | 8.3p0 | LANG.ID.AMBIG | Typographically ambiguous identifiers |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.DCL02 | Fully implemented |
| LDRA tool suite | 9.7.1 | 67 X | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL02-a | Use visually distinct identifiers |
| PC-lint Plus | 1.4 | 9046 | Partially supported: does not report ‘Q’ or ‘D’ vs ‘0’ or ‘O’ |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL02-C | Checks for use of typographically ambiguous identifiers (rec. fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL02-CPP. Use visually distinct identifiers |
| ISO/IEC TR 24772:2013 | Choice of Clear Names [NAI] |
| MISRA C:2012 | Directive 4.5 (advisory) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152192) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152090)
## Comments:

|  |
| ----|
| To how broad a range of identifiers does this guideline refer?; For example, should One, in attempting to adhere to the guideline, only concern Oneself with identifiers declared within the same block or should the concern extend to identifiers in global scope?  Should the concern extend to identifiers in neighboring scopes?
Thanks in advance.
                                        Posted by xuinkrbin. at Jan 29, 2009 10:03
                                     |
| That question has two answers, one based strictly on security and one based on readability. The security answer can be derived from DCL32-C. Guarantee that mutually visible identifiers are unique); that is, to comply with that rule, make sure that identifies that arre mutually visiable don't differ by a hard-to-read combination (eg i1 vs il). The answer based on readability depends much more on cognitive psychology and your program's associated style guidelines. Since it is not based on security, we can also avoid answering the question definitively  
I'll suggest that avoiding identifier names that differ by one letter (when the identifiers are more than three letters long) in the same file is a bad idea.  I suspect others will disagree though...
                                        Posted by svoboda at Jan 29, 2009 11:17
                                     |
| Does this guideline apply to all;identifiers as defined by the ISO C standard:
[!note]
6.2.1 Scopes of identifiers
1    An identifier can denote an object; a function; a tag or a member of a structure, union, or enumeration; a typedef name; a label name; a macro name; or a macro parameter.
or does it just apply to variables?
Thanks in advance.
                                        Posted by xuinkrbin. at Feb 11, 2009 12:37
                                     |
| My initial feeling is that it should apply to all identifiers.  Invoking a similarly named but incorrect function is just as bad or worse then referencing an unintended variable.  I think this applies to the other identifiers on this list as well. 
What do you think?
                                        Posted by rcs at Feb 11, 2009 15:02
                                     |
| I am merely an Observer of the guidelines. ;However, I can understand how such a possible confusion could lead to problems.
                                        Posted by xuinkrbin. at Feb 11, 2009 15:42
                                     |
| OK.  I made it a little more official by putting the definition into the guideline description.
                                        Posted by rcs at Feb 11, 2009 20:38
                                     |
| DCL02-C implicitly assumes 'Global Scope' which can be confused with 'Scope within the same file'. Though it may not generate any errors, but there may be a possible violation of the rule as in the example below:
In foo.h an identifier exists as idO - (captial letter O)
In bar.h an identifier exists as id0 - (numeric letter 0)
This is not a violation of DCL02-C
If foobar.h includes both foo.h and bar.h, that is also not a violation.
But if foobar.c uses both id0 and idO, that would be a violation.
                                        Posted by akumar2 at Nov 03, 2010 13:57
                                     |
| Nice work. I tweaked the rule; I think it looks good.
                                        Posted by svoboda at Nov 03, 2010 15:12
                                     |

