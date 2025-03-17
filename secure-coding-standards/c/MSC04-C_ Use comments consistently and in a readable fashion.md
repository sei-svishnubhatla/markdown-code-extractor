## Noncompliant Code Example
Do not use the character sequence `/*` within a comment:
``` c
/* Comment with end comment marker unintentionally omitted
security_critical_function();
/* Some other comment */
```
In this example, the call to the security-critical function is not executed. A reviewer examining this page could incorrectly assume that the code is executed.
If execution failure is the result of an accidental omission, it is useful to use an editor that provides syntax highlighting or formats the code to help identify issues like missing end-comment delimiters.
Because missing end delimiters are error prone and often viewed as a mistake, this approach is not recommended for commenting out code.
## Compliant Solution (Preprocessor)
Instead of using `/*` and `*/` to comment out blocks of code, use conditional compilation (for example, `#if`, `#ifdef`, or `#ifndef`):
``` c
#if 0  /*
        * Use of critical security function no
        * longer necessary.
        */
security_critical_function();
/* Some other comment */
#endif
```
The text inside a block of code commented out using `#if`, `#ifdef`, or `#ifndef` must still consist of *valid preprocessing tokens*. This means that the characters `"` and `'` must each be paired just as in real C code, and the pairs must not cross line boundaries. In particular, an apostrophe within a contracted word looks like the beginning of a character constant. Consequently, natural-language comments and pseudocode should always be written between the comment delimiters `/*` and `*/` or following `//`.
## Compliant Solution (Compiler)
This compliant solution takes advantage of the compiler's ability to remove unreachable (dead) code. The code inside the `if` block must remain acceptable to the compiler. If other parts of the program, such as macros, types, or function prototypes, later change in a way that would cause syntax errors, the unexecuted code must be brought up to date to correct the problem. Then, if it is needed again in the future, the programmer need only remove the surrounding `if` statement and the `NOTREACHED` comment.
The `NOTREACHED` comment tells some compilers and [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis) tools not to complain about this unreachable code. It also serves as documentation.
``` c
if (0) {  /*
           * Use of critical security function no
           * longer necessary, for now.
           */
  /*NOTREACHED*/
  security_critical_function();
  /* Some other comment */
}
```
This code is an instance of exception MSC07-C-EX2 to [MSC07-C. Detect and remove dead code](MSC07-C_%20Detect%20and%20remove%20dead%20code).
## Noncompliant Code Example
Following are some additional examples of comment styles that are confusing and should be avoided:
``` c
// */          /* Comment, not syntax error */
f = g/**//h;   /* Equivalent to f = g / h; */
//\
i();           /* Part of a two-line comment */
/\
/ j();         /* Part of a two-line comment */
/*//*/ l();    /* Equivalent to l(); */
m = n//**/o
+ p;           /* Equivalent to m = n + p; */
a = b //*divisor:*/c
+d;            /*
                * Interpreted as a = b/c + d; in c90
                * compiler and a = b + d; in c99 compiler.
                */
```
## Compliant Solution
Use a consistent style of commenting:
``` c
/* Nice simple comment */
int i; /* Counter */
```
## Risk Assessment
Confusion over which instructions are executed and which are not can lead to serious programming errors and vulnerabilities, including [denial of service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack), [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination), and data integrity violation. This problem is [mitigated](BB.-Definitions_87152273.html#BB.Definitions-mitigation) by the use of interactive development environments (IDEs) and editors that use fonts, colors, or other mechanisms to differentiate between comments and code. However, the problem can still manifest, for example, when reviewing source code printed on a black-and-white printer.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC04-C | Medium | Unlikely | Medium |  P4  |  L3  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | mmline-commentsline-comment
sline-splicing
smline-comment | Partially checked |
| GCC | 4.3.5 |  | Can detect violations of this rule when the -Wcomment flag is used |
| ECLAIR | 1.2 | CC2.MSC04 | Fully implemented |
| Helix QAC | 2024.4 | C3108 |  |
| LDRA tool suite | 9.7.1 | 119 S, 302 S, 611 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC04-aCERT_C-MSC04-b
CERT_C-MSC04-c
CERT_C-MSC04-d | The character sequence /* shall not be used within a C-style commentThe character sequence // shall not be used within a C-style comment
The character sequence /* shall not be used within a C++-style comment
Line-splicing shall not be used in // comments |
| PC-lint Plus | 1.4 | 1, 427, 602, 689, 853,9059, 9060, 9066, 9259 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC04-C | Checks for use of /* and // within a comment (rule partially covered) |
| RuleChecker | 24.04 | mmline-commentsline-comment
sline-splicing
smline-comment | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC04-CPP. Use comments consistently and in a readable fashion |
| MISRA C:2012 | Rule 1.2 (advisory)Rule 3.1 (required)
Directive 4.4 (advisory) |

## Bibliography

|  |  |
| ----|----|
| [Summit 2005] | Question 11.19 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152198) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152083)
## Comments:

|  |
| ----|
| WHile I agree with the recommendation, comments have nothing to do with the preprocessor.; They are replaced by a space before preprocessing begins.
                                        Posted by ron at Aug 31, 2006 18:29
                                     |
| OK, I'll move this to misc.
                                        Posted by rcs at Sep 01, 2006 15:35
                                     |
| Valuable info;!!Agree with all the facts.Only The Fitness
                                        Posted by mybusinessemail095 at Sep 06, 2018 08:27
                                     |

