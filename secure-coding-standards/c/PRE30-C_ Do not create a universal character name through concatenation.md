The C Standard supports universal character names that may be used in identifiers, character constants, and string literals to designate characters that are not in the basic character set. The universal character name `\U`*nnnnnnnn* designates the character whose 8-digit short identifier (as specified by ISO/IEC 10646) is *nnnnnnnn*. Similarly, the universal character name `\u`*nnnn* designates the character whose 4-digit short identifier is *nnnn* (and whose 8-digit short identifier is `0000`*nnnn*).
The C Standard, 5.1.1.2, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], says
> If a character sequence that matches the syntax of a universal character name is produced by token concatenation (6.10.5.3), the behavior is undefined.

See also [undefined behavior 3](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_3).
In general, avoid universal character names in identifiers unless absolutely necessary.
## Noncompliant Code Example
This code example is noncompliant because it produces a universal character name by token concatenation:
``` c
#define assign(uc1, uc2, val) uc1##uc2 = val
void func(void) {
  int \u0401;
  /* ... */
  assign(\u04, 01, 4);
  /* ... */
}
```
### Implementation Details
This code compiles and runs with Microsoft Visual Studio 2013, assigning 4 to the variable as expected.
GCC 4.8.1 on Linux refuses to compile this code; it emits a diagnostic reading, "stray '\\ in program," referring to the universal character fragment in the invocation of the `assign` macro.
## Compliant Solution
This compliant solution uses a universal character name but does not create it by using token concatenation:
``` c
#define assign(ucn, val) ucn = val
void func(void) {
  int \u0401;
  /* ... */
  assign(\u0401, 4);
  /* ... */
}
```
## Risk Assessment
Creating a universal character name through token concatenation results in undefined behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE30-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | universal-character-name-concatenation | Fully implemented |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE30 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.PREPROC.PASTELANG.PREPROC.PASTEHASH | Macro uses ## operator## follows # operator |
| Cppcheck | ;2.15 | preprocessorErrorDirective |  |
| Cppcheck Premium | 24.11.0 | preprocessorErrorDirective |  |
| Helix QAC | 2024.4 | C0905;C++0064,C++0080 | Fully implemented |
| Klocwork | 2024.4 | MISRA.DEFINE.SHARP | Fully implemented |
| LDRA tool suite | 9.7.1 | 573 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE30-a | Avoid token concatenation that may produce universal character names |
| Polyspace Bug Finder | R2024a | CERT C: Rule PRE30-C | Checks for universal character name from token concatenation (rule fully covered) |
| RuleChecker | 24.04 | universal-character-name-concatenation | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE30-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 10646-2003] |  |
| [ISO/IEC 9899:2024] | Subclause 5.1.1.2, "Translation Phases" |

------------------------------------------------------------------------
[](../c/Rule%2001_%20Preprocessor%20_PRE_) [](../c/Rule%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152163)
## Comments:

|  |
| ----|
| Though the rule is correct, the example given here is not.
What is forbidden, to create a new UCN via concatenation. Like doing
assign(\u0001,0401,a,b,4)
just concatenating stuff that happens to contain UCNs anywhere is okay. 
(the standard does not say exactly when UCNs are replaced to characters, before or after the ## is done, UB comes from here)
                                        Posted by pasa at May 23, 2009 06:43
                                     |
| Yup, you're right. Revised the rule, citing chapter and verse in C99 that it is based on. Also changed the code example to reflect your suggestion, and added implementation details.
Incidentally GCC refuses to accept \U00010401 as a valid char for use as an identifier, so I used \u0401 instead, which it accepts.
                                        Posted by svoboda at May 26, 2009 11:52
                                     |
| With GCC 4.9.1 is necessary to add --std=c11 -fextended-identifiers in compilation options when using universal character names.
                                        Posted by geyslan at Aug 13, 2014 20:08
                                     |
| sorry if i misunderstood;but the first none compliant example does not compile using gcc 5.4misunderstood
                                        Posted by izak at Oct 13, 2018 08:05
                                     |

