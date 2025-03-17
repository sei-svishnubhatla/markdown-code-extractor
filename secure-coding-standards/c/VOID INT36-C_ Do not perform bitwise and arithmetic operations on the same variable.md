C has two distinct purposes for integer data types. One use for integers is to treat them as mathematical values. The other use is to treat them as simple bit-vectors. Both usages are well-supported by the language.
The C standard supports sign magnitude, ones-complement, and twos-complement representations. Usage of an integer as mathematical value does not require underlying knowledge of how the integer is represented, but using an integer as both mathematical values and a bit-vector requires this underlying knowledge to prevent unexpected behavior.
Using bitwise operators on a mathematical value is often done on the belief that it will be faster than using only mathematical operators. However, modern optimizers are able substitute bitwise operations for mathematical operations when bitwise operators would be faster.
Consequently, no integer variable should have both mathematical and bitwise operations performed on it.
For the purpose of this rule, the following list indicates which operators should not be used on mathematical values and which operators should not be used on integers used as bit-vectors.
-   **Arithmetic operators**: `+`, `++`, unary `+, -`,` ``--`, unary -, \*, /, %, \<, \<=, \>, \>=
-   Bitwise operators: &, \|, ^, ~
Other operators, such as comparison `==` may be used on both mathematical values and bit-vectors. Note that the shift operators (`<<` and `>>`) may be used on both mathematical values and bit-vectors.
## Noncompliant Code Example
In this noncompliant code example, `x` is an `int`. This code increments the variable, and then tries to zero out all but the least significant 8 bits of `x`. To comply with [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow), the code handles the case where incrementing `x` would wrap specially.
``` c
#include <limits.h>
int func(int x) {
  return (x == INT_MAX) ? 0 : (x + 1) & 0xff;
}
```
However, there is a simpler way to perform this operation.
## Compliant Solution
This compliant solution uses only mathematical operations to achieve the same result.
``` c
#include <limits.h>
int func(int x) {
  return (x == INT_MAX) ? 0 : (x + 1) % (1 << 8);
}
```
Note that if `x < 0`, then using `%` will produce a negative value; this is a slight difference in behavior from using `&`.
## Exceptions
**INT36-EX1**: Routines may treat integers as bit vectors for I/O purposes. That is, they may treat an integer as a series of bits to write it to a file or socket. They may also read a series of bits from a file or socket and create an integer from the bits.
## Risk Assessment
Performing bit manipulation and arithmetic operations on the same variable obscures the programmer's intentions and reduces readability. It also makes it more difficult for a security auditor or maintainer to determine which checks must be performed to eliminate [security flaws](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) and ensure data integrity.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT36-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this recommendation. However, it can detect only those violations where both bitwise and arithmetic operators are used in the same expression |
| Fortify SCA | 5.0 | ; | Can detect violations of this recommendation with the CERT C Rule Pack |
| LDRA tool suite | 9.7.1 | 585 S | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT36-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT Oracle Secure Coding Standard for Java | NUM01-J. Do not perform bitwise and arithmetic operations on the same data |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Rule 6.1 (required)Rule 6.2 (required) |

## Bibliography

|  |
| ----|
| [Steele 1977] |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/INT13-C.+Use+bitwise+operators+only+on+unsigned+operands?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=270) [](https://www.securecoding.cert.org/confluence/display/seccode/INT15-C.+Use+intmax_t+or+uintmax_t+for+formatted+IO+on+programmer-defined+integer+types?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I don't see this as a rule.Also, I would include left and right shift in bitwise operators.
                                        Posted by rcs_mgr at Nov 12, 2013 00:23
                                     |

