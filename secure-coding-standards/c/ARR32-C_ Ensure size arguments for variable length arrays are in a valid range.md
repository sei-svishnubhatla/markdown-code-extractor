Variable length arrays (VLAs), a conditionally supported language feature, are essentially the same as traditional C arrays except that they are declared with a size that is not a constant integer expression and can be declared only at block scope or function prototype scope and no linkage. When supported, a variable length array can be declared
``` java
{ /* Block scope */
  char vla[size];
}
```
where the integer expression `size` and the declaration of `vla` are both evaluated at runtime. If the size argument supplied to a variable length array is not a positive integer value, the behavior is undefined. (See [undefined behavior 72](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_72).)  Additionally, if the magnitude of the argument is excessive, the program may behave in an unexpected way. An attacker may be able to leverage this behavior to overwrite critical program data \[[Griffiths 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Griffiths06)\]. The programmer must ensure that size arguments to variable length arrays, especially those derived from untrusted data, are in a valid range.
Because variable length arrays are a conditionally supported feature of C11, their use in portable code should be guarded by testing the value of the macro \_\_STDC_NO_VLA\_\_. Implementations that do not support variable length arrays indicate it by setting \_\_STDC_NO_VLA\_\_ to the integer constant 1.
## Noncompliant Code Example
In this noncompliant code example, a variable length array of size `size` is declared. The `size` is declared as `size_t` in compliance with [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](INT01-C_%20Use%20rsize_t%20or%20size_t%20for%20all%20integer%20values%20representing%20the%20size%20of%20an%20object).
``` c
#include <stddef.h>
extern void do_work(int *array, size_t size);
void func(size_t size) {
  int vla[size];
  do_work(vla, size);
}
```
However, the value of `size` may be zero or excessive, potentially giving rise to a security [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
## Compliant Solution
This compliant solution ensures the `size` argument used to allocate `vla` is in a valid range (between 1 and a programmer-defined maximum); otherwise, it uses an algorithm that relies on dynamic memory allocation. The solution also avoids unsigned integer wrapping that, given a sufficiently large value of `size`, would cause `malloc` to allocate insufficient storage for the array.
``` c
#include <stdint.h>
#include <stdlib.h>
enum { MAX_ARRAY = 1024 };
extern void do_work(int *array, size_t size);
void func(size_t size) {
  if (0 == size || SIZE_MAX / sizeof(int) < size) {
    /* Handle error */
    return;
  }
  if (size < MAX_ARRAY) {
    int vla[size];
    do_work(vla, size);
  } else {
    int *array = (int *)malloc(size * sizeof(int));
    if (array == NULL) {
      /* Handle error */
    }
    do_work(array, size);
    free(array);
  }
}
```
## Noncompliant Code Example (`sizeof`)
The following noncompliant code example defines `A` to be a variable length array and then uses the `sizeof` operator to compute its size at runtime. When the function is called with an argument greater than `SIZE_MAX / (N1 * sizeof (int))`, the runtime `sizeof` expression may wrap around, yielding a result that is smaller than the mathematical product `N1 * n2 * sizeof (int)`. The call to `malloc()`, when successful, will then allocate storage for fewer than `n2` elements of the array, causing one or more of the final `memset()` calls in the `for` loop to write past the end of that storage.
``` c
#include <stdlib.h>
#include <string.h>
enum { N1 = 4096 };
void *func(size_t n2) {
  typedef int A[n2][N1];
  A *array = malloc(sizeof(A));
  if (!array) {
    /* Handle error */
    return NULL;
  }
  for (size_t i = 0; i != n2; ++i) {
    memset(array[i], 0, N1 * sizeof(int));
  }
  return array;
}
```
Furthermore, this code also violates [ARR39-C. Do not add or subtract a scaled integer to a pointer](ARR39-C_%20Do%20not%20add%20or%20subtract%20a%20scaled%20integer%20to%20a%20pointer), where `array` is a pointer to the two-dimensional array, where it should really be a pointer to the latter dimension instead. This means that the `memset() `call does out-of-bounds writes on all of its invocations except the first.
## Compliant Solution (`sizeof`)
This compliant solution prevents `sizeof` wrapping by detecting the condition before it occurs and avoiding the subsequent computation when the condition is detected. The code also uses an additional typedef to fix the type of `array` so that `memset()` never writes past the two-dimensional array.
``` c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
enum { N1 = 4096 };
void *func(size_t n2) {
  if (n2 > SIZE_MAX / (N1 * sizeof(int))) {
    /* Prevent sizeof wrapping */
    return NULL;
  }
  typedef int A1[N1];
  typedef A1 A[n2];
  A1 *array = (A1*) malloc(sizeof(A));
  if (!array) {
    /* Handle error */
    return NULL;
  } 
  for (size_t i = 0; i != n2; ++i) {
    memset(array[i], 0, N1 * sizeof(int));
  }
  return array;
}
```
### Implementation Details
#### Microsoft
Variable length arrays are not supported by Microsoft compilers.
## Risk Assessment
Failure to properly specify the size of a variable length array may allow arbitrary code execution or result in stack exhaustion.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR32-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | ALLOC.SIZE.IOFLOWALLOC.SIZE.MULOFLOW
MISC.MEM.SIZE.BAD | Integer Overflow of Allocation SizeMultiplication Overflow of Allocation Size
Unreasonable Size Argument |
| Coverity | 2017.07 | REVERSE_NEGATIVE | Fully implemented |
| Cppcheck | ;2.15 | negativeArraySize |  |
| Cppcheck Premium | 24.11.0 | negativeArraySizepremium-cert-arr32-c |  |
| Helix QAC | 2024.4 | C1051 |  |
| Klocwork | 2024.4 | MISRA.ARRAY.VAR_LENGTH.2012 |  |
| LDRA tool suite | ;9.7.1 | 621 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR32-a | Ensure the size of the variable length array is in valid range |
| PC-lint Plus | 1.4 | 9035 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rule ARR32-C | Checks for:Memory allocation with tainted sizeTainted size of variable length arrayRule fully covered. |
| TrustInSoft Analyzer | 1.38 | alloca_bounds | Exhaustively verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | INT01-C. Use rsize_t or size_t for all integer values representing the size of an object | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Unchecked Array Indexing [XYZ] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Tainted, potentially mutilated, or out-of-domain integer values are used in a restricted sink [taintsink] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-758 | 2017-06-29: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-129 and ARR32-C
Intersection( CWE-188, EXP39-C) = Ø
ARR32-C addresses specifying the size of a variable-length array (VLA). CWE-129 addresses invalid array indices, not array sizes.
### CWE-758 and ARR32-C
Independent( INT34-C, INT36-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( ARR32-C, list) where list =
-   Undefined behavior that results from anything other than too large a VLA dimension.
### CWE-119 and ARR32-C
-   Intersection( CWE-119, ARR32-C) = Ø
-   ARR32-C is not about providing a valid buffer but reading/writing outside it. It is about providing an invalid buffer, or one that exhausts the stack.
## Bibliography

|  |
| ----|
| [Griffiths 2006] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152322) [](../c/Rule%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152341)
## Comments:

|  |
| ----|
| I don't see why the NCCE is bad. the array is declared to be of size s which is automatically unsigned, so it can't be negative. I suppose it could be 0, and it could be > RSIZE_MAX, but you could mitigate that by declaring it type rsize_t.
                                        Posted by svoboda at Jul 23, 2008 11:48
                                     |
| s/negative value/0 or too-big positive value/;
                                        Posted by svoboda at Jul 23, 2008 15:26
                                     |
| Please note that the last compliant solution contains a serious vuln, which is actually a great example (I suggest keeping it within the original code, just fix it in the compliant solution):
A *array = malloc(sizeof(A)); 
...
for (size_t i = 0; i != n2; ++i) {
    memset(array[i], 0, N1 * sizeof(int));
  }

The core vulnerability resides within the indexing of `array[i]. `Since this is pointers arithmetic, the actual accessed address is `array + i * sizeof(A)` .
Recall that `array`; is allocated to point towards a **single** element of type `typedef A` , and not an array of them. 
This means that after the first iteration of the loop, OOB-write would occur! 
The correct iteration body should look similar to the following:
``` java
uintptr_t dest = (uintptr_t)array + i * N1 * sizeof(int);
memset((char *)dest, 0, N1 * sizeof(int));
```
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Jan 20, 2023 08:23
\| \|
Itay:Good catch! As you suggested, I fixed the compliant solution, but kept the noncompliant code example unchanged. But I did describe the vulnerability in both coding examples, because ARR39-C covers this kind of coding error.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 20, 2023 11:07
\|
