> [!warning]  
>
> This guideline has been deprecated.  It is not relevant to standards-conforming compilers, just pre-standards K&R C compilers.

The `offsetof()` macro provides a portable mechanism to determine the offset of an element name within a structure. The `offsetof()` macro is defined in the standard header `stddef.h` as follows:
``` java
offsetof(type, member-designator)
```
The macro expands to an integer constant expression that has type `size_t`, the value of which is the offset, in bytes, to the structure member (designated by member designator) from the beginning of its structure (designated by type).
Behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when the member designator parameter of an `offsetof()` macro designates a bit-field or is an invalid right operand of the `.` operator for the `type` parameter. See also [undefined behavior 144](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_144)  in Annex J of the C standard.
Subclause 7.19 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] requires that
> The type and member designator shall be such that given
>
> `static type t;`
>
> then the expression `&(t.member-designator)` evaluates to an address constant. (If the specified member is a bit field, the behavior is undefined.)

## Noncompliant Code Example (Bit-Field Members)
This noncompliant code example calls `offsetof()` on a bit-field structure member, resulting in undefined behavior:
``` c
#include <stddef.h>  /* For offsetof macro */
#include <stdio.h>
struct S {
  unsigned int a: 8;
} bits = {255};
int main(void) {
  size_t offset = offsetof(struct S, a);  /* Error */
  printf("offsetof(bits, a) = %zu.\n", offset );
  return 0;
}
```
### Implementation Details
The Microsoft Visual Studio 2012 compiler generates the following diagnostic message when the `offsetof()` macro is passed a bit-field as the member designate:
``` java
error C2104: '&' on bit field ignored
```
## Compliant Solution (Bit-Field Members)
This compliant solution calls `offsetof()` on a structure member of a type other than a bit-field, which in this case is `unsigned int`:
``` c
#include <stddef.h>  /* For offsetof macro */
#include <stdio.h>
struct S {
    unsigned int a;
} bits = {255};
int main(void) {
  size_t offset = offsetof(struct S, a);
  printf("offsetof(bits, a) = %zu.\n", offset );
  return 0;
}
```
## Noncompliant Code Example (Invalid Structures)
Some older compilers allow specification of a member that does not correspond to the type being used, as in this example:
``` c
struct S {
  int i;
  int j;
} s;
struct T {
  float f;
} t;
int main(void) {
  return t.j;
}
```
This can lead to undiagnosed errors when combined with the most straightforward implementation of the `offsetof()` macro:
``` java
#define offsetof(type, field) ((size_t)&(((type *)0)->field))
```
Compilers that use this definition of `offsetof()` and permit incorrect members to be used would be unable to diagnose the following (incorrect) use of `offsetof().`  A conforming compiler should issue a diagnostic that `T` has no member `j`:
``` c
#include <stddef.h>
struct S {
  int i;
  int j;
} s;
struct T {
  float f;
} t;
int main(void) {
  size_t x = offsetof(struct T, j);
  /* ... */
  return 0;
}
```
This problem can still exist, for example, with older embedded compilers.
## Automated Detection
`t.member-designator` is invalid if member-designator is not a member of `t`, so that part is caught by the language definition and need not be caught by the analyzer. It is not undefined behavior.
For the bit-field case, it is undefined behavior. However, the typical macro implementation is as follows (where a flat address space is available):
``` java
#define offsetof(type, member) ((size_t)&(((type *)0)->member))
```
Taking the address of the member in this macro is invalid if the member is a bit-field, because that would be a constraint violation for the `&` operator.
For address spaces that are not flat, typically a specially named object is used instead of address 0, and the address of the beginning of the structure is subtracted from the address of the member, so the macro still looks almost the same as shown previously. The language also prevents this from being a problem in the same way as in this example.
Modern compilers usually move more of the work into the compiler, with a definition like the following, where `_Offsetof` is a compiler built in:
``` java
#define offsetof(type, member) _Offsetof(type, member)
```
Either way, the compiler can see clearly when an attempt is being made to perform the operation on a bit-field.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP38-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| EDG | ; | ; | ; |
| GCC | 4.3.5 | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP38-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Rule 1.3 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.19, "Common Definitions <stddef.h>" |
| [Jones 2004] | ; |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/EXP37-C.+Call+functions+with+the+correct+number+and+type+of+arguments) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=358) [](https://www.securecoding.cert.org/confluence/display/seccode/EXP39-C.+Do+not+access+a+variable+through+a+pointer+of+an+incompatible+type?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| NCCE (bit-field members) generates compiler error, so how will that be a threat? The compliant solution has no "bit-field" in it. If there is a compiler that will let this NCCE compile - we should perhaps list it.
In NCCE (invalid structures)  it has "Some older compilers allow..." - how "old" are we referring to? Few examples might help.
MISRA04 says no to not only offsetof but also dynamic memory allocation - the reader must be encouraged to understand the rationale behind MISRA's suggestions and not jump to a conclusion that offsetof is evil. The Jones 04 explains situations where offsetof is very useful.
                                        Posted by abhi at Mar 10, 2008 02:46
                                     |
| I find the examples of incorrect elements non-compelling.; Before the C standard, some compilers used a single namespace for all structure elements, and I assume that the example with element .j in a structure that is not defined to contain .j works on such compilers - but AFAIAC, such compilers have been dead for (computing) aeons, circa 1990 from my experience.  (That is, the last time I encountered such a compiler pre-dates 1990, though I would be hard-pressed to say how much before hand - based on a shaky memory, I'd estimate more than 5 years prior to 1990.)
I wondered about 'incomplete' types instead of 'invalid' types, but the code won't compile with them, either.  I feel this is close to clutching at straws - apart from the bit-fields issues.  Is there a 'Do not use bit-fields' prescription anywhere?  Why not?  They're portability (and often performance) liabilities, even if not security liabilities.  They have a place, perhaps, in device drivers, but writing those is a minority occupation and not the primary target audience.
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 23:18
                                     |
| This rule came about in an odd way.  We were trying to figure out why MISRA 04 has Rule 20.6, "The macro offsetof, in library <stddef.h>, shall not be used." We decided that they were trying to avoid offsetof() from being called on bit-field members or invalid types, but threw the baby out with the bathwater, so to speak.
                                        Posted by rcs at Mar 16, 2008 10:12
                                     |
| A lot of the MISRA guidelines, at least long ago when I saw the first edition of them, made little or no sense.
It could be that they wanted to discourage code from trying to make use of generally irrelevant details of data layout.
                                        Posted by dagwyn at Apr 15, 2008 15:30
                                     |

