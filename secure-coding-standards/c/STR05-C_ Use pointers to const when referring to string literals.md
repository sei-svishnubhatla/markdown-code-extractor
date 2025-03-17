The type of a narrow string literal is an array of `char`, and the type of a wide string literal is an array of `wchar_t`. However, string literals (of both types) are notionally constant and should consequently be protected by `const` qualification. This recommendation is a specialization of [DCL00-C. Const-qualify immutable objects](DCL00-C_%20Const-qualify%20immutable%20objects) and also supports [STR30-C. Do not attempt to modify string literals](STR30-C_%20Do%20not%20attempt%20to%20modify%20string%20literals).
Adding `const` qualification may propagate through a program; as `const` qualifiers are added, still more become necessary. This phenomenon is sometimes called *const-poisoning*. Const-poisoning can frequently lead to violations of [EXP05-C. Do not cast away a const qualification](EXP05-C_%20Do%20not%20cast%20away%20a%20const%20qualification). Although `const` qualification is a good idea, the costs may outweigh the value in the remediation of existing code.
## Noncompliant Code Example (Narrow String Literal)
In this noncompliant code example, the `const` keyword has been omitted:
``` c
char *c = "Hello";
```
If a statement such as `c[0] = 'C'` were placed following the declaration in the noncompliant code example, the code is likely to compile cleanly, but the result of the assignment would be [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because string literals are considered constant.
## Compliant Solution (Immutable Strings)
In this compliant solution, the characters referred to by the pointer `c` are `const`-qualified, meaning that any attempt to assign them to different values is an error:
``` c
const char *c = "Hello";
```
## Compliant Solution (Mutable Strings)
In cases where the string is meant to be modified, use initialization instead of assignment. In this compliant solution, `c` is a modifiable `char` array that has been initialized using the contents of the corresponding string literal:
``` c
char c[] = "Hello";
```
Consequently, a statement such as `c[0] = 'C'` is valid and behaves as expected.
## Noncompliant Code Example (Wide String Literal)
In this noncompliant code example, the `const` keyword has been omitted:
``` c
wchar_t *c = L"Hello";
```
If a statement such as `c[0] = L'C'` were placed following this declaration, the code is likely to compile cleanly, but the result of the assignment would be [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because string literals are considered constant.
## Compliant Solution (Immutable Strings)
In this compliant solution, the characters referred to by the pointer `c` are `const`-qualified, meaning that any attempt to assign them to different values is an error:
``` c
wchar_t const *c = L"Hello";
```
## Compliant Solution (Mutable Strings)
In cases where the string is meant to be modified, use initialization instead of assignment. In this compliant solution, `c` is a modifiable `wchar_t` array that has been initialized using the contents of the corresponding string literal:
``` c
wchar_t c[] = L"Hello";
```
Consequently, a statement such as `c[0] = L'C'` is valid and behaves as expected.
## Risk Assessment
Modifying string literals causes [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), resulting in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) and [denial-of-service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR05-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | literal-assignment | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR05 |  |
| Clang | 3.9 | -Wwrite-strings | Not enabled by -Weverything |
| CodeSonar | 8.3p0 | LANG.TYPE.NCS | Non-const string literal |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.STR05 | Fully implemented |
| GCC | 4.3.5 | -Wwrite-strings |  |
| Helix QAC | 2024.4 | C0752, C0753 |  |
| Klocwork | 2024.4 | MISRA.STRING_LITERAL.NON_CONST.2012 |  |
| LDRA tool suite | 9.7.1 | 623 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR05-a | A string literal shall not be modified |
| PC-lint Plus | 1.4 | 1776 | Fully supported |
| RuleChecker | 24.04 | literal-assignment | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR05-C).
## Bibliography

|  |  |
| ----|----|
| [Corfield 1993] |  |
| [Lockheed Martin 2005] | ; AV Rule 151.1 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152350) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](../c/STR06-C_%20Do%20not%20assume%20that%20strtok__%20leaves%20the%20parse%20string%20unchanged)
## Comments:

|  |
| ----|
| Shouldn't this be "Prefer making pointers to string literals const-qualified"?
                                        Posted by rcs_mgr at May 05, 2008 22:05
                                     |
| No, the title is correct. You are declaring the pointed-to chars const, not the pointer itself.
Frankly I think you should use:
const char* const x = "hello";
as that prevents you from changing either the pointer or the pointed-to values, which is probably what you want.
                                        Posted by svoboda at May 05, 2008 22:59
                                     |
| That doesn't make the title correct.; String literals aren't const-qualified in C, and you can't affect that.
"Prefer pointers to const for string literals", maybe.
And prepend "However," to the sentence "Adding const qualification may propagate...", and let that start a new paragraph.
Personally I'd not let that stand alone though. That is, I decide whether to constify something (whether pointing at a string literal or not) from how it'll be used.
Instead of your const char *x, I might instead write const char x[] which saves a pointer dereferencing at each access.
                                        Posted by hbf at May 06, 2008 01:49
                                     |
| I changed the title and added an example using wide character strings, just for clarification.
                                        Posted by rcs_mgr at May 26, 2008 18:20
                                     |
| The first Compliant Solution (mutable strings) seems to have a contradiction between code example and its description. The second Compliant Solution (mutable strings) looks almost the same as the first one thus one of them can be cleared?
                                        Posted by masaki at Oct 30, 2009 05:55
                                     |
| In the second CS shouldn't it use
Const wchar_tâ€¢
Rather than 
Wchar_t constâ€¢
?
                                        Posted by svoboda_mgr at Oct 07, 2010 10:43
                                     |
| It's equivalent. You can use the "read const from right to left" rule to check:wchar_t const * is a pointer to const wchar_tconst wchar_t * is a pointer to wchar_t constThat is, it modifies what precedes it, unless it is in the left most position. In fact the narrow char example could also be written as:char const; *c = "Hello";which might be more appropriate (technically speaking) but most people find it less natural.
                                        Posted by asolano at Apr 04, 2013 13:34
                                     |
| GCC and Clang have the flag -Wwrite-strings to warn when this recommendation isn't followed. Note that since it works under the hood by changing the type of string literals, rather than by directly enabling a warning, this won't be enabled by combination warning flags, not even Clang's -Weverything.
                                        Posted by jcsible at Jun 30, 2020 14:34
                                     |
| I added GCC and Clang to the Automated Detection sections to promote these features.
                                        Posted by svoboda at Aug 19, 2020 08:22
                                     |

