The C Standard, 6.7.3.2 paragraph 19 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> There may be unnamed padding within a structure object, but not at its beginning. . . . There may be unnamed padding at the end of a structure or union.

Subclause 6.7.11, paragraph 10, states that
> unnamed members of objects of structure and union type do not participate in initialization. Unnamed members of structure objects have indeterminate representation even after initialization.

The only exception is that padding bits are set to zero when a static or thread-local object is implicitly initialized (paragraph 11): 
> If an object that has static or thread storage duration is not initialized explicitly, or any object is initialized with an empty initializer, then it is subject to default initialization, which initializes an object as follows:
>
> —  if it is an aggregate, every member is initialized (recursively) according to these rules, and any padding is initialized to zero bits;
>
> —  if it is a union, the first named member is initialized (recursively) according to these rules, and any padding is initialized to zero bits. 
>
>   

Because these padding values are unspecified, attempting a byte-by-byte comparison between structures can lead to incorrect results \[[Summit 1995](AA.-Bibliography_87152170.html#AA.Bibliography-Summit95)\]. 
## Noncompliant Code Example
In this noncompliant code example, `memcmp()` is used to compare the contents of two structures, including any padding bytes:
``` c
#include <string.h>
struct s {
  char c;
  int i;
  char buffer[13];
};
void compare(const struct s *left, const struct s *right) {  
  if ((left && right) &&
      (0 == memcmp(left, right, sizeof(struct s)))) {
    /* ... */
  }
}
```
## Compliant Solution
In this compliant solution, all of the fields are compared manually to avoid comparing any padding bytes:
``` c
#include <string.h>
struct s {
  char c;
  int i;
  char buffer[13];
};
void compare(const struct s *left, const struct s *right) {  
  if ((left && right) &&
      (left->c == right->c) &&
      (left->i == right->i) &&
      (0 == memcmp(left->buffer, right->buffer, 13))) {
    /* ... */
  }
}
```
## Exceptions
**EXP42-C-EX1**: A structure can be defined such that the members are aligned properly or the structure is packed using implementation-specific packing instructions. This is true only when the members' data types have no padding bits of their own and when their object representations are the same as their value representations. This frequently is not true for the `_Bool` type or floating-point types and need not be true for pointers. In such cases, the compiler does not insert padding, and use of functions such as `memcmp()` is acceptable.
This compliant example uses the [#pragma pack](http://msdn.microsoft.com/en-us/library/2e70t5y1.aspx) compiler extension from Microsoft Visual Studio to ensure the structure members are packed as tightly as possible:
``` c
#include <string.h>
#pragma pack(push, 1)
struct s {
  char c;
  int i;
  char buffer[13];
};
#pragma pack(pop)
void compare(const struct s *left, const struct s *right) {  
  if ((left && right) &&
      (0 == memcmp(left, right, sizeof(struct s)))) {
    /* ... */
  }
}
```
## Risk Assessment
Comparing padding bytes, when present, can lead to [unexpected program behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP42-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | memcpy-with-padding | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP42 |  |
| CodeSonar | 8.3p0 | BADFUNC.MEMCMP | Use of memcmp |
| Cppcheck Premium | 24.11.0 | premium-cert-exp42-c |  |
| Helix QAC | 2024.4 | DF4726, DF4727, DF4728, DF4729 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.MEMCMP.PTR_ARG_TYPES |  |
| LDRA tool suite | 9.7.1 | 618 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP42-a | Don't memcpy or memcmp non-PODs |
| PC-lint Plus | 1.4 | 958, 959 | Assistance provided: reports structures which require padding between members or after the last member |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP42-C | Checks for memory comparison of padding data (rule fully covered) |
| PVS-Studio | 7.35 | V1103 |  |
| RuleChecker | 24.04 | memcpy-with-padding | Partially checked |
| TrustInSoft Analyzer | 1.38 | comparable_char_blocks | Exhaustively verified (see the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP42-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961 | Comparison of padding data [padcomp] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | EXP62-CPP. Do not access the bits of an object representation that are not part of the object's value representation | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.7.3.2, "Structure and Union Specifiers"6.7.11, "Initialization" |
| [Summit 1995] | Question 2.8Question 2.12 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152401) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151927)
## Comments:

|  |
| ----|
| Question: Would we allow bitwise serlization of a struct, given that the padding data might contain sensitive info (eg: password from its previous use as a char string)?;
                                        Posted by svoboda at Nov 01, 2013 14:54
                                     |
| I think that's what DCL39-C. Avoid information leak in structure padding covers, unless I misunderstand.
                                        Posted by aballman at Nov 01, 2013 18:04
                                     |
| To me it seems that the "compliant" solution is dangerous and uncompliant.It assumes there is no padding inside the struct, for instance between c and i.Then it is dangerous, because if there is padding then that code will not compare the members completely.;
                                        Posted by daniel.marjamaki at Aug 19, 2015 02:51
                                     |
| as far as I see... if you don't want to compare padding data at all then memcmp should not be used. the struct members should be compared individually then.
                                        Posted by daniel.marjamaki at Aug 19, 2015 03:01
                                     |
| The compliant solution is comparing the struct members individually. The exception compliant solution is doing a memcmp();only because the structure is packed with an implementation-defined #pragma. Can you expound on what you find dangerous?
                                        Posted by aballman at Aug 19, 2015 12:28
                                     |
| sorry I misread the code. it is safe.
                                        Posted by daniel.marjamaki at Aug 20, 2015 07:07
                                     |
| The Compliant Solution checks left and right for NULL while the Noncompliant;Code Example and EXP42-C-EX1 do not. I don't think this difference is intended to illustrate anything about this rule so I would suggest making them all consistent for clarity. Passing NULL to memcmp is undefined behavior.
                                        Posted by alex at Sep 27, 2018 11:00
                                     |
| Agreed, I changed the code as you suggest.
                                        Posted by svoboda at Sep 28, 2018 18:13
                                     |

