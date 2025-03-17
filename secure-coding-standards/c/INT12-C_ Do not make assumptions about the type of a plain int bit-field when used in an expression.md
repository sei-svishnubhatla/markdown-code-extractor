Bit-fields can be used to allow flags or other integer values with small ranges to be packed together to save storage space.
It is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementationdefinedbehavior) whether the specifier `int` designates the same type as `signed int` or the same type as `unsigned int` for bit-fields. According to the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], C integer promotions also require that "if an `int` can represent all values of the original type (as restricted by the width, for a bit-field), the value is converted to an `int`; otherwise, it is converted to an `unsigned int`."
This issue is similar to the signedness of plain `char`, discussed in [INT07-C. Use only explicitly signed or unsigned char type for numeric values](INT07-C_%20Use%20only%20explicitly%20signed%20or%20unsigned%20char%20type%20for%20numeric%20values). A plain `int` bit-field that is treated as unsigned will promote to `int` as long as its field width is less than that of `int` because `int` can hold all values of the original type. This behavior is the same as that of a plain `char` treated as unsigned. However, a plain `int` bit-field treated as unsigned will promote to `unsigned int` if its field width is the same as that of `int`. This difference makes a plain `int` bit-field even trickier than a plain `char`.
Bit-field types other than `_Bool`, `int`, `signed int`, and `unsigned int` are implementation-defined. They still obey the integer promotions quoted previously when the specified width is at least as narrow as `CHAR_BIT*sizeof(int)`, but wider bit-fields are not portable.
## Noncompliant Code Example
This noncompliant code depends on [implementation-defined behavior](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). It prints either `-1` or `255`, depending on whether a plain `int` bit-field is signed or unsigned.
``` c
struct {
  int a: 8;
} bits = {255};
int main(void) {
  printf("bits.a = %d.\n", bits.a);
  return 0;
}
```
## Compliant Solution
This compliant solution uses an `unsigned int` bit-field and does not depend on implementation-defined behavior:
``` c
struct {
  unsigned int a: 8;
} bits = {255};
int main(void) {
  printf("bits.a = %d.\n", bits.a);
  return 0;
}
```
## Risk Assessment
Making invalid assumptions about the type of a bit-field or its layout can result in unexpected program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT12-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bitfield-type | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT12 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.BFSIGN | Bit-field signedness not explicit |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.INT12 | Fully implemented |
| Helix QAC | 2024.4 | C0634, C0635 |  |
| Klocwork | 2024.4 | MISRA.BITFIELD.TYPE |  |
| LDRA tool suite | 9.7.1 | 73 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT12-a | Bit fields shall only be defined to be of type unsigned int or signed int |
| PC-lint Plus | 1.4 | 846 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT12-C | Checks for bit-field declared without appropriate type (rec. fully covered) |
| RuleChecker | 24.04 | bitfield-type | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S814 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT12-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT12-CPP. Do not make assumptions about the type of a plain int bit-field when used in an expression |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Rule; 10.1 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.3.1.1, "Boolean, Characters, and Integers" |

------------------------------------------------------------------------
[](../c/INT10-C_%20Do%20not%20assume%20a%20positive%20remainder%20when%20using%20the%20%%20operator) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152374)
## Comments:

|  |
| ----|
| Is this the correct interpretation of the implementation-defined behavior?
I always thought the issue was similar to that associated with char, signed char and unsigned char. i.e. if a bit-field is of type int, then it is implementation defined if it is signed or unsigned. If the signedness is specified, the behavior (when used in an expression) is then appropriate for the type of the definition. e.g.
[!note]
struct {Â Â Â Â Â Â Â Â Â Â Â  int m : 8;Â Â  } a;
struct {Â Â  unsigned int m : 8;Â Â  } ua;
struct {Â Â Â Â  signed int m : 8;Â Â  } sa;
Â 

In the above, a.m has implementation defined signedness, ua.m is unsigned and sa.m is signed.
This is the interpretation that MISRA uses. 
![](images/icons/contenttypes/comment_16.png) Posted by keylevel at Mar 28, 2008 10:58
\| \|
The real issue is almost the same as that for plain `char`.; This rule originally contradicted itself by quoting the integer promotions in the second paragraph, and then later saying that it was implementation-defined whether an 8-bit `unsigned int` bit-field was promoted to `int` or `unsigned int`.  The integer promotions are the correct interpretation.  This is now fixed.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 31, 2008 18:17
\| \|
If it's signed int, the 255 initializer is invalid and should generate a diagnostic.
I don't have a good replacement, since my personal rule is "don't use bit fields, ever".
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 16:33
\|
