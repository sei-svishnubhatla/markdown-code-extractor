According to [MISRA 2008](AA.-Bibliography_87152170.html#AA.Bibliography-MISRA08), concatenation of wide and narrow string literals leads to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). This was once considered implicitly undefined behavior until C90 \[[ISO/IEC 9899:1990](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-1990)\]. However, C99 defined this behavior \[[ISO/IEC 9899:1999](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-1999)\], and C11 further explains in subclause 6.4.5, paragraph 5 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
> In translation phase 6, the multibyte character sequences specified by any sequence of adjacent character and identically-prefixed string literal tokens are concatenated into a single multibyte character sequence. If any of the tokens has an encoding prefix, the resulting multibyte character sequence is treated as having the same prefix; otherwise, it is treated as a character string literal. Whether differently-prefixed wide string literal tokens can be concatenated and, if so, the treatment of the resulting multibyte character sequence are implementation-defined.

Nonetheless, it is recommended that string literals that are concatenated should all be the same type so as not to rely on [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) or [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if compiled on a platform that supports only C90.
## Noncompliant Code Example (C90)
This noncompliant code example concatenates wide and narrow string literals. Although the behavior is undefined in C90, the programmer probably intended to create a wide string literal.
``` c
wchar_t *msg = L"This message is very long, so I want to divide it "
                "into two parts.";
```
## Compliant Solution (C90, Wide String Literals)
If the concatenated string needs to be a wide string literal, each element in the concatenation must be a wide string literal, as in this compliant solution:
``` c
wchar_t *msg = L"This message is very long, so I want to divide it "
               L"into two parts.";
```
## Compliant Solution (C90, Narrow String Literals)
If wide string literals are unnecessary, it is better to use narrow string literals, as in this compliant solution:
``` c
char *msg = "This message is very long, so I want to divide it "
            "into two parts.";
```
## Risk Assessment
The concatenation of wide and narrow string literals could lead to undefined behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR10-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | encoding-mismatch | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR10 |  |
| ECLAIR | 1.2 | CC2.STR10 | Fully implemented. |
| Helix QAC | 2024.4 | C0874 |  |
| LDRA tool suite | 9.7.1 | 450 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR10-a | Narrow and wide string literals shall not be concatenated |
| PC-lint Plus | 1.4 | 707 | Fully supported |
| SonarQube C/C++ Plugin | 3.11 | NarrowAndWideStringConcat |  |
| RuleChecker | 24.04 | encoding-mismatch | Fully checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR10-C).
## Related Guidelines

|  |  |
| ----|----|
| MISRA C++:2008 | Rule 2-13-5 |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 6.4.5, "String Literals" |

------------------------------------------------------------------------
[](../c/STR09-C_%20Don't%20assume%20numeric%20values%20for%20expressions%20with%20type%20plain%20character) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152096)
## Comments:

|  |
| ----|
| Is this explicit or implicit undefined behavior according to C99?  I think you should clarify which, and if explicit, reference a section number.
                                        Posted by rcs_mgr at Nov 05, 2009 18:10
                                     |
| I think you should point out in the first compliant solution (wide string literals) that it is likely that this is what the programmer meant to do.
                                        Posted by rcs_mgr at Nov 05, 2009 18:11
                                     |
| someone post a comment to our japanese version of STR10-c.In C99, concatenation of a simple string literal and a wide string literal is clearly defined;"If any of the tokens has an encoding prefix, the resulting multibyte character sequence is treated as having the same prefix; otherwise,; it is treated as a character string literal."C99 Rationale says that this kind of concatenation is undefined behavior in C89 and a new feature in C99. C11 has added two more prefixes ('u' and 'U') for wide character string, andconcatenation of differently-prefixed wide string literals are implementation-defined.I think this recommendation should explain these prefixes and recommend to avoid concatenation of differently-prefixed wide string,because that leads to implementation-defined behavior.And, I wonder why no recommendation in C++ secure coding standard? 
                                        Posted by yozo at Oct 18, 2012 05:55
                                     |
| Yozo-san:It does appear that MISRA is out-of-date wrt behavior of wide-char strings as you suggest. (I think they purposefully only support C90.) I've amended the rule as you suggest.We haven't updated C++ with all the rules of C (nor with our gradual transformation to C11); that's why this rule doesn't appear there yet.
                                        Posted by svoboda at Oct 18, 2012 11:00
                                     |
| thanks, David!; I added a little more revision to clarify the history of this treatment and added "C90" to the headings of the NCCE and CCEs. 
                                        Posted by yozo at Oct 23, 2012 00:48
                                     |

