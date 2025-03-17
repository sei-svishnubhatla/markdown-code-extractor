Copying data into an array that is not large enough to hold that data results in a buffer overflow. To prevent such errors, data copied to the destination array must be restricted on the basis of the size of the destination array, or, preferably, the destination array must be guaranteed to be large enough to hold the data to be copied.
[Vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) that result from copying data to an undersized buffer often involve character strings. Consult [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator) for specific examples of this rule that involve character strings.
## Noncompliant Code Example
Improper use of functions that limit copies with a size specifier, such as `memcpy()`, can result in a buffer overflow. In this noncompliant code example, an array of integers is copied from `src` to `dest` using `memcpy()`. The function `func()` has a function signature in which the first parameter is an array of `const int`, and the second parameter represents the array bounds (that is, the number of elements in the array) and not the array size.
The programmer correctly multiplies `num_elem` by the `sizeof(int)` to calculate the size of the `src` array but fails to check that the source array is not larger than the destination array. If `num_elem` is greater than 256, a buffer overflow occurs. Furthermore, if `num_elem` is sufficiently large, the multiplication can wrap. (See [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).) If this happens, the product becomes smaller than expected, causing `memcpy()` to copy much less memory than expected.
``` c
#include <string.h>
enum { WORKSPACE_BOUND = 256 };
void func(const int *src, size_t num_elem) {
  int dest[WORKSPACE_BOUND];
  memcpy(dest, src, num_elem * sizeof(int));
}
```
## Compliant Solution (Bounds Checking)
The number of characters to copy must be limited on the basis of the size of the destination buffer. This compliant solution adds a check to ensure the number of elements being copied does not exceed the bounds of the destination array:
``` c
#include <string.h>
enum { WORKSPACE_BOUND = 256 };
void func(const int *src, size_t num_elem) {
  int dest[WORKSPACE_BOUND];
  if (num_elem > WORKSPACE_BOUND) {
    /* Handle error */
  }
  memcpy(dest, src, sizeof(int) * num_elem);
}
```
Note that this solution does not consider wrapping from the multiplication because `num_elems` is guaranteed to be less than 256.
## Compliant Solution (Dynamic Allocation)
Alternatively, memory for the destination buffer (`dest`) can be dynamically allocated to ensure it is large enough to hold the data in the source buffer (`src`). This solution must check for wrapping in the multiplication because no other guarantees are provided on `num_elem`:
``` c
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
void func(const int *src, size_t num_elem) {
  int *dest;
  if (num_elem > SIZE_MAX / sizeof(int)) {
   /* Handle integer overflow */
  }
  dest = (int *)malloc(sizeof(int) * num_elem);
  if (dest == NULL) {
     /* Couldn't get the memory—recover */
  }
  memcpy(dest, src, sizeof(int) * num_elem);
  free(dest);
}
```
## Risk Assessment
Copying data to a buffer that is too small to hold that data results in a buffer overflow. Attackers can exploit this condition to execute arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR33-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| Coverity | 6.5 | BUFFER_SIZE | Fully Implemented |
| Fortify SCA | 5.0 | ; | Can detect violations of this rule with CERT C Rule Pack |
| Splint | 3.1.1 | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR33-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminatorINT30-C. Ensure that unsigned integer operations do not wrap |
| SEI CERT C++ Coding Standard | CTR52-CPP. Guarantee that library functions do not overflow |
| ISO/IEC TR 24772:2013 | Buffer Boundary Violation (Buffer Overflow) [HCB]Unchecked Array Copying [XYW]Unchecked Array Indexing [XYZ] |
| MITRE CWE | CWE-119, Failure to constrain operations within the bounds of an allocated memory buffer |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/ARR32-C.+Ensure+size+arguments+for+variable+length+arrays+are+in+a+valid+range?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=263) [](https://www.securecoding.cert.org/confluence/display/seccode/ARR34-C.+Ensure+that+array+types+in+expressions+are+compatible?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I eliminated the array notation in the first argument.  Although I think think it is generally a good idea to communicate that the function takes an array, I think the use of array notation is misleading because it leads a developer to think that an actual array is passed and not just a pointer to the first element in the array.
This is probably a stylistic issue that doesn't require a separate guideline.
                                        Posted by rcs_mgr at Aug 20, 2009 09:05
                                     |
| appears to be subsumed byARR38-C. Guarantee that library functions do not form invalid pointersand is a candidate for the void.; might want to review automated detection, related guidelines, etc. before removal.
                                        Posted by rcs_mgr at Nov 19, 2013 08:56
                                     |

