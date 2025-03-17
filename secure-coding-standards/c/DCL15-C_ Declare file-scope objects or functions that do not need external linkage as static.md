If a file-scope object or a function does not need to be visible outside of the file, it should be hidden by being declared as `static`. This practice creates more modular code and limits pollution of the global name space.
Subclause 6.2.2 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] states:
> If the declaration of a file scope identifier for an object or a function contains the storage-class specifier `static`, the identifier has internal linkage.

and
> If the declaration of an identifier for an object has file scope and no storage-class specifier, its linkage is external.

## Noncompliant Code Example
This noncompliant code example includes a `helper()` function that is implicitly declared to have external linkage:
``` c
enum { MAX = 100 };
int helper(int i) {
  /* Perform some computation based on i */
}
int main(void) {
  size_t i;
  int out[MAX];
  for (i = 0; i < MAX; i++) {
    out[i] = helper(i);
  }
  /* ... */
}
```
## Compliant Solution
This compliant solution declares `helper()` to have internal linkage, thereby preventing external functions from using it:
``` c
enum {MAX = 100};
static int helper(int i) {
  /* Perform some computation based on i */
}
int main(void) {
  size_t i;
  int out[MAX];
  for (i = 0; i < MAX; i++) {
    out[i] = helper(i);
  }
  /* ... */
}
```
## Risk Assessment
Allowing too many objects to have external linkage can use up descriptive identifiers, leading to more complicated identifiers, violations of abstraction models, and possible name conflicts with libraries. If the compilation unit implements a data abstraction, it may also expose invocations of private functions from outside the abstraction.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL15-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | global-object-scope | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL15 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.SCOPE.FILE | Scope could be file static |
| ECLAIR | 1.2 | CC2.DCL15 | Fully implemented |
| Helix QAC | 2024.4 | C1504, C1531 |  |
| LDRA tool suite | 9.7.1 | 27 D61 D
553 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL15-a | Objects or functions with external linkage shall be declared in a header file |
| PC-lint Plus | 1.4 | 765 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL15-C | Checks for situations where function or object with external linkage is referenced in only one translation unit (rec. fully covered) |
| RuleChecker | 24.04 | global-object-scope | Fully checked |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL15-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL15-CPP. Declare file-scope objects or functions that do not need external linkage in an unnamed namespace |
| MISRA C:2012 | Rule 8.7 (advisory)Rule 8.8 (required) |

## Bibliography

|  |  |
| ----|----|
| ISO/IEC 9899:2011 | Subclause 6.2.2, "Linkages of Identifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152301) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152241)
## Comments:

|  |
| ----|
| How can this rule be labeled as unenforceable when "Splint Version 3.1.1 can detect violations of this rule."?
I'm not sure I'll approve of any definition of "unenforceable" that permits this to be OK.
                                        Posted by rcs at Jul 06, 2008 13:27
                                     |
| Inenforceable by ROSE... not sure why, but we no longer have a rose-nonapplicable tag
                                        Posted by avolkovi at Jul 07, 2008 09:11
                                     |
| I have been (slowly) tagging 'unenforceable' to all rules that we couldn't add a rose checker for.
I realize that this is actually ambiguous, as there are at least two interesting meanings of 'unenforceable', (1) can't be checked by ROSE now, and (2) can't be checked automatically on a theoretical basis. There are probably more. But I figured that tagging everything that might fall under one of these definitions now enables us to refine the tags as a later step.
I also changed 'rose-nonapplicable' to unenforceable for now. Like I said, we can split off the tags soon.
                                        Posted by svoboda at Jul 07, 2008 11:03
                                     |
| Yeah, that's what I thought... but it certainly is not clear.  
I think "unenforceable" should mean generally unenforceable... for examples, recommendations that state "Understand that..."
If the label is rose specific, it should contain rose in the name.
                                        Posted by rcs at Jul 07, 2008 12:49
                                     |
| At this point we have both 'rose-nonapplicable' and 'unenforceable' tags.
This rule is 'rose-nonapplicable' because it would require examining your entire program to see that a function (implicitly) declared external isn't actually used anywhere. Rose does have some provisions for using an external database to store data when doing multi-file analysis, but we don't have the infrastructure to support that yet. Hence the tag.
                                        Posted by svoboda at Jul 16, 2008 12:20
                                     |

