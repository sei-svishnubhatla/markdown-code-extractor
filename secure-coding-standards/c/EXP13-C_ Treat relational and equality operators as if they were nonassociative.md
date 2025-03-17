The relational and equality operators are left-associative in C. Consequently, C, unlike many other languages, allows chaining of relational and equality operators. Subclause 6.5.8, footnote 107, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], says:
> The expression `a<b<c` is not interpreted as in ordinary mathematics. As the syntax indicates, it means `(a<b)<c`; in other words, "if `a` is less than `b`, compare 1 to `c`; otherwise, compare 0 to `c`."

These operators are *left-associative*, which means the leftmost comparison is performed first, and the result is compared with the rightmost comparison. This syntax allows a programmer to write an expression (particularly an expression used as a condition) that can be easily misinterpreted.
## Noncompliant Code Example
Although this noncompliant code example compiles correctly, it is unlikely that it means what the author of the code intended:
``` c
int a = 2;
int b = 2;
int c = 2;
/* ... */
if (a < b < c) /* Misleading; likely bug */
/* ... */
if (a == b == c) /* Misleading; likely bug */
```
The expression `a < b < c` evaluates to true rather than, as its author probably intended, to false, and the expression `a == b == c` evaluates to false rather than, as its author probably intended, to true.
## Compliant Solution
Treat relational and equality operators as if it were invalid to chain them:
``` c
if ( (a < b) && (b < c) ) /* Clearer and probably what was intended */
/* ... */
if ( (a == b) && (a == c) ) /* Ditto */
```
## Risk Assessment
Incorrect use of relational and equality operators can lead to incorrect control flow.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP13-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | chained-comparison | Fully checked |
| ECLAIR | 1.2 | CC2.EXP13 | Fully implemented |
| GCC | 4.3.5 |  | Option -Wparentheses warns if a comparison like x<=y<=z appears; this warning is also enabled by -Wall |
| Helix QAC | 2024.4 | C3392, C3401, C4111, C4112, C4113 |  |
| LDRA tool suite | 9.7.1 | 433 S | Fully implemented |
| PC-lint Plus | 1.4 | 503, 731 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP13-C | Checks for possibly unintended evaluation of expression because of operator precedence rules (rec. fully covered) |
| PVS-Studio | 7.35 | V709 |  |
| RuleChecker | 24.04 | chained-comparison | Fully checked |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP17-CPP. Treat relational and equality operators as if they were nonassociative |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.5.8, "Relational Operators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152282) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152251)
## Comments:

|  |
| ----|
| A couple of questions:
1. What does "left-associatvie" mean in C? What's the definition in C spec?
2. Is is true that in other languages, relational (or equality) operators are associative?
                                        Posted by masaki at Apr 28, 2009 01:13
                                     |
| Added some text to address your first question..
I think most operators are left-associative in most languages by default; that's the easiest way to parse source code. (Some languages choose features to be right-associative, but that's a conscious decision).
But Java doesn't allow relation chaining (eg a<b<c). It's not forbidden by 'associativity', but rather by Java being more strongly typed than C. It's still parsed as ((a<b)<c), but (a<b) is a boolean type, and the relation operators cannot be applied to boolean types, so a<b<c generates a type mismatch error. I'd guess most langauges that disallow chaining use a similar strategy.  C allows this because (a<b) returns an int type (which has the value 0 or 1).
                                        Posted by svoboda at Apr 28, 2009 10:15
                                     |

