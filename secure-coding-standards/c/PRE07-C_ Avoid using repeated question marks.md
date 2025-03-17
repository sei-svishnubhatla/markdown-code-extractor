Two consecutive question marks signify the start of a trigraph sequence. According to the C Standard, subclause 5.2.1.1 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> All occurrences in a source file of the following sequences of three characters (that is, *trigraph sequences*) are replaced with the corresponding single character.
>
> |       |     |     |       |     |     |       |     |
> |-------|-----|-----|-------|-----|-----|-------|-----|
> | `??=` | `#` | ` ` | `??)` | `]` | ` ` | `??!` | \|  |
> | `??(` | `[` | ` ` | `??'` | `^` | ` ` | `??>` | `}` |
> | `??/` | `\` | ` ` | `??<` | `{` | ` ` | `??-` | `~` |
>
>   

## Noncompliant Code Example
In this noncompliant code example, `a++` is not executed because the trigraph sequence `??/` is replaced by `\`, logically putting `a++` on the same line as the comment:
``` c
// What is the value of a now??/
a++;
```
## Compliant Solution
This compliant solution eliminates the accidental introduction of the trigraph by separating the question marks:
``` c
// What is the value of a now? ?/
a++;
```
## Noncompliant Code Example
This noncompliant code example includes the trigraph sequence `??!`, which is replaced by the character `|`:
``` c
size_t i = /* Some initial value */;
if (i > 9000) {
   if (puts("Over 9000!??!") == EOF) {
     /* Handle error */
   }
}
```
This example prints `Over 9000!|` if a C-compliant compiler is used.
## Compliant Solution
This compliant solution uses string concatenation to concatenate the two question marks; otherwise, they are interpreted as beginning a trigraph sequence:
``` c
size_t i = /* Some initial value */;
/* Assignment of i */
if (i > 9000) {
   if (puts("Over 9000!?""?!") == EOF) {
     /* Handle error */
   }
}
```
This code prints `Over 9000!??!`, as intended.
## Risk Assessment
Inadvertent trigraphs can result in unexpected behavior. Some compilers provide options to warn when trigraphs are encountered or to disable trigraph expansion. Use the warning options, and ensure your code compiles cleanly. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE07-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | trigraph | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE07 |  |
| ECLAIR | 1.2 | CC2.PRE07 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violation of this recommendation when the -Wtrigraphs flag is used |
| Helix QAC | 2024.4 | C3601 |  |
| LDRA tool suite | 9.7.1 | 81 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE07-a | Trigraphs shall not be used |
| PC-lint Plus | 1.4 | 584, 854, 9060 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE07-C | Checks for use of trigraphs (rec. fully covered) |
| RuleChecker | 24.04 | trigraph | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | TrigraphUsage |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE07-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE07-CPP. Avoid using repeated question marks |
| MISRA C:2012 | Rule 4.2 (advisory) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 5.2.1.1, "Trigraph Sequences" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152155) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152355)
## Comments:

|  |
| ----|
| Chris Tapp sez:
> What about the digraph sequences?

C99 sez, in section 6.4.6, point 3:
  In all aspects of the language, the six tokens:
           <:    :>    <%    %>    %:     %:%:
  behave, respectively, the same as the six tokens
           [     ]     {     }     #      ##
  except for their spelling.
These 6 digraph tokens, unlike trigraphs, are unlikely to appear in C code, outside strings, because they are not syntactically valid. They may appear in strings, but as they are only mentioned as part of tokenization, they are not processed. Therefore misinterpretation of these digraphs is highly unlikely, and IMHO not worth worrying about.
                                        Posted by svoboda at Jun 05, 2008 16:21
                                     |
| As of C99, the escape sequence \? in character and string constants maps to ? (just as \' and \" map to ' and ") (6.4.4.4)
Hence "Over 9000!??!" can be corrected with "Over 9000!?\?!", which is more concise that adding the sequence "" or " " between question marks.  This effect is magnified if many question marks need to be escaped in a single string.
                                        Posted by konrad.schwarz at May 12, 2023 07:58
                                     |

