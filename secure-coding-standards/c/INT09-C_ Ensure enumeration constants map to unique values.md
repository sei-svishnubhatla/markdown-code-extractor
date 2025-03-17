A C enumeration defines a type with a finite set of values represented by identifiers known as *enumeration constants*, or enumerators. An enumerator is a constant integer expression whose value is representable as an `int`. Although the language allows multiple enumerators of the same type to have the same value, it is a common expectation that all enumerators of the same type have distinct values. However, defining two or more enumerators of the same type to have the same value can lead to some nonobvious errors.
## Noncompliant Code Example
In this noncompliant code example, two enumerators of type `Color` are assigned explicit values. It may not be obvious to the programmer that `yellow` and `indigo` have been declared to be identical values (6), as are `green` and `violet` (7). Probably the least dangerous error that can result from such a definition is attempting to use the enumerators as labels of a `switch` statement. Because all labels in a `switch` statement are required to be unique, the following code violates this semantic constraint and is required to be diagnosed by a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) compiler:
``` c
enum Color { red=4, orange, yellow, green, blue, indigo=6, violet };
const char* color_name(enum Color col) {
  switch (col) {
  case red: return "red";
  case orange: return "orange";
  case yellow: return "yellow";
  case green: return "green";
  case blue: return "blue";
  case indigo: return "indigo";   /* Error: duplicate label (yellow) */
  case violet: return "violet";   /* Error: duplicate label (green) */
  }
}
```
## Compliant Solution
To prevent the error discussed of the noncompliant code example, enumeration type declarations must take one of the following forms:
-   Provide no explicit integer assignments, as in this example:
``` c
enum Color { red, orange, yellow, green, blue, indigo, violet };
```
-   Assign a value to the first member only (the rest are then sequential), as in this example:
``` c
enum Color { red=4, orange, yellow, green, blue, indigo, violet };
```
-   Assign a value to all members so any equivalence is explicit, as in this example:
``` c
enum Color {
  red=4, 
  orange=5, 
  yellow=6, 
  green=7, 
  blue=8, 
  indigo=6, 
  violet=7
};
```
It is also advisable to provide a comment explaining why multiple enumeration type members are being assigned the same value so that future maintainers do not mistakenly identify this form as an error.
Of these three options, providing no explicit integer assignments is the simplest and consequently the preferred approach unless the first enumerator must have a nonzero value.
## Exceptions
**INT09-C-EX1:** In cases where defining an enumeration with two or more enumerators with the same value is intended, the constant expression used to define the value of the duplicate enumerator should reference the enumerator rather than the original enumerator's value. This practice makes the intent clear to both human readers of the code and automated code analysis tools that detect violations of this guideline and would diagnose them otherwise. Note, however, that it does not make it possible to use such enumerators in contexts where unique values are required (such as in a `switch` statement, as discussed earlier).
``` c
enum Color { red, orange, yellow, green, blue, indigo, violet=indigo };
```
## Risk Assessment
Failing to ensure that constants within an enumeration have unique values can result in unexpected results.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT09-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | enum-implicit-value | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT09 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.INIT.ENUM | Inconsistent Enumerator Initialization |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.INT09 | Fully implemented |
| Helix QAC | 2024.4 | C0724 |  |
| Klocwork | 2024.4 | MISRA.ENUM.IMPLICIT.VAL.NON_UNIQUE.2012 |  |
| LDRA tool suite | 9.7.1 | 85 S, 630 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT09-a | In an enumerator list, the "=" construct shall not be used to explicitly initialise members other than the first, unless all items are explicitly initialised |
| PC-lint Plus | 1.4 | 488, 9148 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT09-C | Checks for situations where enumeration constants map to same value (rec. fully covered) |
| RuleChecker | 24.04 | enum-implicit-value | Fully checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT09-CPP. Ensure enumeration constants map to unique values |
| CERT Oracle Secure Coding Standard for Java | DCL56-J. Do not attach significance to the ordinal associated with an enum |
| ISO/IEC TR 24772:2013 | Enumerator Issues [CCB] |
| MISRA C:2012 | Rule 8.12 (required) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152450) [](../c/Rec_%2004_%20Integers%20_INT_) [](../c/INT10-C_%20Do%20not%20assume%20a%20positive%20remainder%20when%20using%20the%20%%20operator)
## Comments:

|  |
| ----|
| As mentioned elsewhere, there are valid cases where two or more enumeration-constant have identical values by design. For example:
enum { red, orange, yellow, green, blue, indigo, violet, purple = violet };

This guideline ought to make room for such designs. I propose that it be permissible to declare multiple enumerators of the same type to have the same value provided the *constant-expression* that defines the value of the *enumeration-constant* is itself a previously defined *enumeration-constant* of the same type (as in the `purple = violet` case above).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 29, 2010 22:22
\| \|
I've added [#INT09-EX1](INT09-C.-Ensure-enumeration-constants-map-to-unique-values_87152467.html#INT09C.Ensureenumerationconstantsmaptouniquevalues-INT09-EX1).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 23, 2010 17:32
\|
