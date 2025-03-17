Flexible array members are a special type of array in which the last element of a structure with more than one named member has an incomplete array type; that is, the size of the array is not specified explicitly within the structure. This "struct hack" was widely used in practice and supported by a variety of compilers. Consequently, a variety of different syntaxes have been used for declaring flexible array members. For conforming C implementations, use the syntax guaranteed to be valid by the C Standard.
Flexible array members are defined in the C Standard, 6.7.3.2, paragraph 20 \[[ISO/IEC 9899:2024](https://wiki.sei.cmu.edu/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2024)\], as follows:
> As a special case, the last element of a structure with more than one named member may have an incomplete array type; this is called a *flexible array member*. In most situations, the flexible array member is ignored. In particular, the size of the structure is as if the flexible array member were omitted except that it may have more trailing padding than the omission would imply. However, when a **`.`**` `(or **`->`**) operator has a left operand that is (a pointer to) a structure with a flexible array member and the right operand names that member, it behaves as if that member were replaced with the longest array (with the same element type) that would not make the structure larger than the object being accessed; the offset of the array shall remain that of the flexible array member, even if this would differ from that of the replacement array. If this array would have no elements, it behaves as if it had one element but the behavior is undefined if any attempt is made to access that element or to generate a pointer one past it.

Structures with a flexible array member can be used to produce code with defined behavior. However, some restrictions apply:
1.  The incomplete array type *must* be the last element within the structure.
2.  There cannot be an array of structures that contain a flexible array member.
3.  Structures that contain a flexible array member cannot be used as a member of another structure.
4.  The structure must contain at least one named member in addition to the flexible array member.
## Noncompliant Code Example
Before the introduction of flexible array members in the C Standard, structures with a one-element array as the final member were used to achieve similar functionality. This noncompliant code example illustrates how `struct flexArrayStruct` is declared in this case.
This noncompliant code example attempts to allocate a flexible array-like member with a one-element array as the final member. When the structure is instantiated, the size computed for `malloc()` is modified to account for the actual size of the dynamic array.
``` c
#include <stdlib.h>
struct flexArrayStruct {
  int num;
  int data[1];
};
void func(size_t array_size) {
  /* Space is allocated for the struct */
  struct flexArrayStruct *structP
    = (struct flexArrayStruct *)
     malloc(sizeof(struct flexArrayStruct)
          + sizeof(int) * (array_size - 1));
  if (structP == NULL) {
    /* Handle malloc failure */
  }
  structP->num = array_size;
  /*
   * Access data[] as if it had been allocated
   * as data[array_size].
   */
  for (size_t i = 0; i < array_size; ++i) {
    structP->data[i] = 1;
  }
}
```
This example has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when accessing any element other than the first element of the `data` array. (See the C Standard, 6.5.7.) Consequently, the compiler can generate code that does not return the expected value when accessing the second element of data.
This approach may be the only alternative for compilers that do not yet implement the standard C syntax.
## Compliant Solution
This compliant solution uses a flexible array member to achieve a dynamically sized structure:
``` c
#include <stdlib.h>
struct flexArrayStruct{
  int num;
  int data[];
};
void func(size_t array_size) {
  /* Space is allocated for the struct */
  struct flexArrayStruct *structP 
    = (struct flexArrayStruct *)
    malloc(sizeof(struct flexArrayStruct) 
         + sizeof(int) * array_size);
  if (structP == NULL) {
    /* Handle malloc failure */
  }
  structP->num = array_size;
  /*
   * Access data[] as if it had been allocated
   * as data[array_size].
   */
  for (size_t i = 0; i < array_size; ++i) {
    structP->data[i] = 1;
  }
}
```
This compliant solution allows the structure to be treated as if its member `data[]` was declared to be `data[array_size]` in a manner that conforms to the C Standard.
## Risk Assessment
Failing to use the correct syntax when declaring a flexible array member can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), although the incorrect syntax will work on most implementations.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL38-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | array_out_of_bounds | SupportedAstrée reports all out-of-bounds array access. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL38 | Detects if the final member of struct which is declared as an array of small bound, is used as a flexible array member. |
| Compass/ROSE |  |  | Can detect some violations of this rule. In particular, it warns if the last element of a struct is an array with a small index (0 or 1) |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl38-c |  |
| Helix QAC | 2024.4 | C1037, C1039 | Fully implemented |
| Klocwork | 2024.4 | CERT.STRUCT.FLEXIBLE_ARRAY_MEMBER | Fully implemented |
| LDRA tool suite | ;9.7.1 | 648 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL38-a | The final member of a structure should not be an array of size '0' or '1' |
| PC-lint Plus | 1.4 | 9040 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL38-C | Checks for incorrect syntax of flexible array member size (rule fully covered) |
| TrustInSoft Analyzer | 1.38 | index_bound | Exhaustively detects out-of-bounds array access (see the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL38-C).
## Related Guidelines
This rule supplements [MEM33-C. Allocate and copy structures containing a flexible array member dynamically](MEM33-C_%20%20Allocate%20and%20copy%20structures%20containing%20a%20flexible%20array%20member%20dynamically)
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.5.7, "Additive Operators"6.7.3.2, "Structure and Union Specifiers" |
| [McCluskey 2001] | "Flexible Array Members and Designators in C9X" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152308) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151978)
## Comments:

|  |
| ----|
| The numbered list at the beginning of this article says3. Structures that contain a flexible array member cannot be used as a member of another structure except as the last element of that structure.The exception in the bolded text seems to directly contradict both the C99 and C11 standards: 6.7.2.1 paragraph 3 says3. (...) the last member of a structure (...) may have incomplete array type; such a structure (...) shall not be a member of a structure or an element of an array.I can see no text in the standard for the mentioned exception, so some pointer would be very useful.Also note that such exception is considered a compiler extension by GCC and IBM: https://gcc.gnu.org/onlinedocs/gcc/Zero-Length.html (4th bullet in the list)https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_72/rzarg/flexible.htm 
                                        Posted by hmijail at Oct 16, 2016 20:21
                                     |
| Furthermore, as of September 2016 that exception is being considered by the standards body:;http://www.open-std.org/jtc1/sc22/wg14/www/docs/n2083.htmSo it's pretty clear that such exception is not currently in the standard.
                                        Posted by hmijail at Oct 16, 2016 20:48
                                     |
| You are correct, this is a compiler extension rather than a standard feature in C11.
                                        Posted by aballman at Oct 17, 2016 09:24
                                     |
| Both code examples appear to violate EXP03-C. Do not assume the size of a structure is the sum of the sizes of its members
                                        Posted by svoboda at Aug 15, 2019 11:44
                                     |
| I don't see it for the CS, or if it does, then EXP03-C is wrong. Flexible array members do not contribute to the size of the structure (that's why you cannot have a structure with only one member which is a flexible array;– you'd have a zero-sized struct then), so you're not assuming anything about the size of the structure based on calculating the flexible array member size needs. The CS is showing the correct way to allocate a structure with a flexible array member.
                                        Posted by aballman at Aug 15, 2019 12:10
                                     |
| Oh, you're right. Both examples correctly compute the size of an object by adding the size of the struct with the expected additional elements in the array. Sigh. Been looking at too much code that does this wrongly...
                                        Posted by svoboda at Aug 15, 2019 13:45
                                     |

