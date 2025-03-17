The types of integer expressions used as size arguments to `malloc()`, `calloc()`, `realloc()`, or `aligned_alloc()` must have sufficient range to represent the size of the objects to be stored. If size arguments are incorrect or can be manipulated by an attacker, then a buffer overflow may occur. Incorrect size arguments, inadequate range checking, integer overflow, or truncation can result in the allocation of an inadequately sized buffer.
Typically, the amount of memory to allocate will be the size of the type of object to allocate. When allocating space for an array, the size of the object will be multiplied by the bounds of the array. When allocating space for a structure containing a flexible array member, the size of the array member must be added to the size of the structure. (See [MEM33-C. Allocate and copy structures containing a flexible array member dynamically](MEM33-C_%20%20Allocate%20and%20copy%20structures%20containing%20a%20flexible%20array%20member%20dynamically).) Use the correct type of the object when computing the size of memory to allocate.
[STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator) is a specific instance of this rule.
## Noncompliant Code Example (Pointer)
In this noncompliant code example, inadequate space is allocated for a `struct tm` object because the size of the pointer is being used to determine the size of the pointed-to object:
``` c
#include <stdlib.h>
#include <time.h>
struct tm *make_tm(int year, int mon, int day, int hour,
                   int min, int sec) {
  struct tm *tmb;
  tmb = (struct tm *)malloc(sizeof(tmb));
  if (tmb == NULL) {
    return NULL;
  }
  *tmb = (struct tm) {
    .tm_sec = sec, .tm_min = min, .tm_hour = hour,
    .tm_mday = day, .tm_mon = mon, .tm_year = year
  };
  return tmb;
}
```
## Compliant Solution (Pointer)
 In this compliant solution, the correct amount of memory is allocated for the `struct tm` object. When allocating  space for a single object, passing the (dereferenced) pointer type to the `sizeof` operator is a simple way to allocate sufficient memory. Because the `sizeof` operator does not evaluate its operand, dereferencing an uninitialized or null pointer in this context is well-defined behavior.
``` c
#include <stdlib.h>
#include <time.h>
struct tm *make_tm(int year, int mon, int day, int hour,
                   int min, int sec) {
  struct tm *tmb;
  tmb = (struct tm *)malloc(sizeof(*tmb));
  if (tmb == NULL) {
    return NULL;
  }
  *tmb = (struct tm) {
    .tm_sec = sec, .tm_min = min, .tm_hour = hour,
    .tm_mday = day, .tm_mon = mon, .tm_year = year
  };
  return tmb;
}
```
## Noncompliant Code Example (Integer)
In this noncompliant code example, an array of `long` is allocated and assigned to `p`. The code attempts to check for unsigned integer overflow in compliance with INT30-C. Ensure that unsigned integer operations do not wrap and also ensures that `len` is not equal to zero. (See [MEM04-C. Beware of zero-length allocations](MEM04-C_%20Beware%20of%20zero-length%20allocations).) However, because sizeof(int) is used to compute the size, and not sizeof(long), an insufficient amount of memory can be allocated on implementations where sizeof(long) is larger than sizeof(int), and filling the array can cause a heap buffer overflow.
``` c
#include <stdint.h>
#include <stdlib.h>
void function(size_t len) {
  long *p;
  if (len == 0 || len > SIZE_MAX / sizeof(long)) {
    /* Handle overflow */
  }
  p = (long *)malloc(len * sizeof(int));
  if (p == NULL) {
    /* Handle error */
  }
  free(p);
}
```
## Compliant Solution (Integer)
This compliant solution uses `sizeof(long)` to correctly size the memory allocation:
``` c
#include <stdint.h>
#include <stdlib.h>
void function(size_t len) {
  long *p;
  if (len == 0 || len > SIZE_MAX / sizeof(long)) {
    /* Handle overflow */
  }
  p = (long *)malloc(len * sizeof(long));
  if (p == NULL) {
    /* Handle error */
  }
  free(p);
}
```
## Compliant Solution (Integer)
Alternatively, `sizeof(*p)` can be used to properly size the allocation:
``` c
#include <stdint.h>
#include <stdlib.h>
void function(size_t len) {
  long *p;
  if (len == 0 || len > SIZE_MAX / sizeof(*p)) {
    /* Handle overflow */
  }
  p = (long *)malloc(len * sizeof(*p));
  if (p == NULL) {
    /* Handle error */
  }
  free(p);
}
```
## Risk Assessment
Providing invalid size arguments to memory allocation functions can lead to buffer overflows and the execution of arbitrary code with the permissions of the vulnerable process.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM35-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | malloc-size-insufficient | Partially checkedBesides direct rule violations, all undefined behaviour resulting from invalid memory accesses is reported by Astrée. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM35 |  |
| CodeSonar | 8.3p0 | ALLOC.SIZE.ADDOFLOWALLOC.SIZE.IOFLOW
ALLOC.SIZE.MULOFLOW
ALLOC.SIZE.SUBUFLOW
ALLOC.SIZE.TRUNC
IO.TAINT.SIZE
MISC.MEM.SIZE.BAD
LANG.MEM.BO
LANG.MEM.BU
LANG.STRUCT.PARITH
LANG.STRUCT.PBB
LANG.STRUCT.PPE
LANG.MEM.TBA
LANG.MEM.TO
LANG.MEM.TU
 | Addition overflow of allocation sizeAddition overflow of allocation size
Multiplication overflow of allocation size
Subtraction underflow of allocation size
Truncation of allocation size
Tainted allocation size
Unreasonable size argument
Buffer Overrun
Buffer Underrun
Pointer Arithmetic
Pointer Before Beginning of Object
Pointer Past End of Object
Tainted Buffer Access
Type Overrun
Type Underrun |
| Compass/ROSE |  |  | Could check violations of this rule by examining the size expression to malloc() or memcpy() functions. Specifically, the size argument should be bounded by 0, SIZE_MAX, and, unless it is a variable of type size_t or rsize_t, it should be bounds-checked before the malloc() call. If the argument is of the expression a*b, then an appropriate check is
if (a < SIZE_MAX / b && a > 0) ...

\| \|
[Coverity](Coverity)
\|
2017.07
\|
**BAD_ALLOC_STRLEN**
**SIZECHECK (deprecated)**
\|
Partially implemented
Can find instances where string length is miscalculated (length calculated may be one less than intended) for memory allocation purposes. Coverity Prevent cannot discover all violations of this rule, so further verification is necessary
Finds memory allocations that are assigned to a pointer that reference objects larger than the allocated block
\| \| [Cppcheck Premium](Cppcheck%20Premium) \|
24.11.0
\| **premium-cert-mem35-c** \| \| \| [Helix QAC](Helix%20QAC) \|
2024.4
\|
**C0696, C0701, C1069, C1071, C1073, C2840**
**DF2840, DF2841, DF2842, DF2843, DF2935, DF2936, DF2937, DF2938**
\| \| \| [Klocwork](Klocwork) \|
2024.4
\|
**INCORRECT.ALLOC_SIZESV.TAINTED.ALLOC_SIZE**
\| \| \| [LDRA tool suite](LDRA) \|
9.7.1
\| **400 S, 487 S, 115 D** \| Enhanced enforcement \| \| [Splint](Splint) \| 3.1.1 \| \| \| \| [Parasoft C/C++test](Parasoft) \| 2024.2 \|
**CERT_C-MEM35-a**
\|
Do not use sizeof operator on pointer type to specify the size of the memory to be allocated via 'malloc', 'calloc' or 'realloc' function
\| \| [PC-lint Plus](PC-lint%20Plus) \|
1.4
\|
**433, 826**
\|
Partially supported
\| \| [Polyspace Bug Finder](Polyspace%20Bug%20Finder) \|
R2024a
\|
[CERT C: Rule MEM35-C](https://www.mathworks.com/help/bugfinder/ref/certcrulemem35c.html)
\|
Checks for:
-   Pointer access out of bounds
-   Memory allocation with tainted size
Rule partially covered.
\| \| [PVS-Studio](https://wiki.sei.cmu.edu/confluence/display/c/PVS-Studio) \|
7.35
\| [V531](https://pvs-studio.com/en/docs/warnings/v531/), [V635](https://pvs-studio.com/en/docs/warnings/v635/), **[V781](https://pvs-studio.com/en/docs/warnings/v781/)** \| \| \| [RuleChecker](RuleChecker) \|
24.04
\| **malloc-size-insufficient** \| Partially checked \| \| [TrustInSoft Analyzer](TrustInSoft%20Analyzer) \|
1.38
\| **mem_access** \|
Exhaustively detects undefined behavior (see [one compliant and one non-compliant example](https://taas.trust-in-soft.com/tsnippet/t/77590559)).
\|
### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM35-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an arrayINT31-C. Ensure that integer conversions do not result in lost or misinterpreted data | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | INT32-C. Ensure that operations on signed integers do not result in overflow | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | MEM04-C. Beware of zero-length allocations | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Buffer Boundary Violation (Buffer Overflow) [HCB] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Taking the size of a pointer to determine the size of the pointed-to type [sizeofptr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-131, Incorrect Calculation of Buffer Size | 2017-05-16: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-680 | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-789 | 2017-06-12: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-680 and MEM35-C
Intersection( INT32-C, MEM35-C) = Ø
CWE-680 = Union( MEM35-C, list) where list =
-   Overflowed buffers with inadequate sizes not produced by integer overflow
### CWE-467 and MEM35-C
CWE-467 = Subset( MEM35-C)
### CWE-789 and MEM35-C
Intersection( MEM35-C, CWE-789) =
-   Insufficient memory allocation on the heap
MEM35-C – CWE-789 =
-   Insufficient memory allocation with trusted value but incorrect calculation
CWE-789 - MEM35-C =
-   Sufficient memory allocation (possibly over-allocation) with untrusted value
### CWE-120 and MEM35-C
Intersection( MEM35-C, CWE-120) = Ø
CWE-120 specifically addresses buffer overflow operations, which occur in the context of string-copying. MEM35-C specifically addresses allocation of memory ranges (some of which may be for subsequent string copy operations).
Consequently, they address different sections of code, although one (or both) may be responsible for a single buffer overflow vulnerability.
### CWE-131 and MEM35-C
-   Intersection( INT30-C, MEM35-C) = Ø
-   CWE-131 = Union( MEM35-C, list) where list =
-   Miscalculating a buffer for a non-heap region (such as a variable-length array)
## Bibliography

|  |  |
| ----|----|
| [Coverity 2007] |  |
| [Drepper 2006] | Section 2.1.1, "Respecting Memory Bounds" |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management"Chapter 5, "Integer Security" |
| [Viega 2005] | Section 5.6.8, "Use of;sizeof() on a Pointer Type" |
| [xorl 2009] | CVE-2009-0587: Evolution Data Server Base64 Integer Overflows |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152156) [](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](../c/MEM36-C_%20Do%20not%20modify%20the%20alignment%20of%20objects%20by%20calling%20realloc__)
