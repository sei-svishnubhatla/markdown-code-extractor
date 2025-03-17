Pointer arithmetic is appropriate only when the pointer argument refers to an array (see [ARR37-C. Do not add or subtract an integer to a pointer to a non-array object](ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object)), including an array of bytes. When performing pointer arithmetic, the size of the value to add to or subtract from a pointer is automatically scaled to the size of the type of the referenced array object. Adding or subtracting a scaled integer value to or from a pointer is invalid because it may yield a pointer that does not point to an element within or one past the end of the array. (See [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts).)
Adding a pointer to an array of a type other than character to the result of the `sizeof` operator or `offsetof` macro, which returns a size and an offset, respectively, violates this rule. However, adding an array pointer to the number of array elements, for example, by using the `arr[sizeof(arr)/sizeof(arr[0])])` idiom, is allowed provided that `arr` refers to an array and not a pointer.
## Noncompliant Code Example
In this noncompliant code example, `sizeof(buf)` is added to the array `buf`. This example is noncompliant because `sizeof(buf)` is scaled by `int` and then scaled again when added to `buf`.
``` c
enum { INTBUFSIZE = 80 };
extern int getdata(void);
int buf[INTBUFSIZE];
void func(void) {
  int *buf_ptr = buf;
  while (buf_ptr < (buf + sizeof(buf))) {
    *buf_ptr++ = getdata();
  }
}
```
## Compliant Solution
This compliant solution uses an unscaled integer to obtain a pointer to the end of the array:
``` c
enum { INTBUFSIZE = 80 };
extern int getdata(void);
int buf[INTBUFSIZE];
void func(void) {
  int *buf_ptr = buf;
  while (buf_ptr < (buf + INTBUFSIZE)) {
    *buf_ptr++ = getdata();
  }
}
```
## Noncompliant Code Example
In this noncompliant code example, `skip` is added to the pointer `s`. However, `skip` represents the byte offset of `ull_b` in `struct big`. When added to `s`, `skip` is scaled by the size of `struct big`.
``` c
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
struct big {
  unsigned long long ull_a;
  unsigned long long ull_b;
  unsigned long long ull_c;
  int si_e;
  int si_f;
};
void func(void) {
  size_t skip = offsetof(struct big, ull_b);
  struct big *s = (struct big *)malloc(sizeof(struct big));
  if (s == NULL) {
    /* Handle malloc() error */
  }
  memset(s + skip, 0, sizeof(struct big) - skip);
  /* ... */
  free(s);
  s = NULL;
}
```
## Compliant Solution
This compliant solution uses an `unsigned char *` to calculate the offset instead of using a `struct big *`, which would result in scaled arithmetic:
``` c
#include <string.h>
#include <stdlib.h>
#include <stddef.h>
struct big {
  unsigned long long ull_a;
  unsigned long long ull_b;
  unsigned long long ull_c;
  int si_d;
  int si_e;
};
void func(void) {
  size_t skip = offsetof(struct big, ull_b);
  unsigned char *ptr = (unsigned char *)malloc(
    sizeof(struct big)
  );
  if (ptr == NULL) {
     /* Handle malloc() error */
  }
  memset(ptr + skip, 0, sizeof(struct big) - skip);
  /* ... */
  free(ptr);
  ptr = NULL;
}
```
## Noncompliant Code Example
In this noncompliant code example, `wcslen(error_msg) * sizeof(wchar_t)` bytes are scaled by the size of `wchar_t` when added to `error_msg`:
``` c
#include <wchar.h>
#include <stdio.h>
enum { WCHAR_BUF = 128 };
void func(void) {
  wchar_t error_msg[WCHAR_BUF];
  wcscpy(error_msg, L"Error: ");
  fgetws(error_msg + wcslen(error_msg) * sizeof(wchar_t), 
         WCHAR_BUF - 7, stdin);
  /* ... */
}
```
## Compliant Solution
This compliant solution does not scale the length of the string; `wcslen()` returns the number of characters and the addition to `error_msg` is scaled:
``` c
#include <wchar.h>
#include <stdio.h>
enum { WCHAR_BUF = 128 };
const wchar_t ERROR_PREFIX[7] = L"Error: ";
void func(void) {
  const size_t prefix_len = wcslen(ERROR_PREFIX);
  wchar_t error_msg[WCHAR_BUF];
  wcscpy(error_msg, ERROR_PREFIX);
  fgetws(error_msg + prefix_len,
        WCHAR_BUF - prefix_len, stdin);
  /* ... */
}
```
## Risk Assessment
Failure to understand and properly use pointer arithmetic can allow an attacker to execute arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR39-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | scaled-pointer-arithmetic  | Partially checkedBesides direct rule violations, Astrée reports all (resulting) out-of-bound array accesses. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR39 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.BU
LANG.MEM.TBA
LANG.MEM.TO
LANG.MEM.TU
LANG.STRUCT.PARITH
LANG.STRUCT.PBB
LANG.STRUCT.PPE | Buffer overrunBuffer underrun
Tainted buffer access
Type overrun
Type underrun
Pointer Arithmetic
Pointer before beginning of object
Pointer past end of object |
| Coverity | 2017.07 | BAD_SIZEOF; | Partially implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-arr39-c |  |
| Helix QAC | 2024.4 | DF4955, DF4956, DF4957 |  |
| Klocwork | 2024.4 | MISRA.PTR.ARITH.2012 |  |
| LDRA tool suite | ;9.7.1 | 47 S, 489 S, 567 S,64 X, 66 X, 68 X,
69 X, 70 X, 71 X | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR39-aCERT_C-ARR39-b
CERT_C-ARR39-c | Avoid accessing arrays out of boundsPointer arithmetic should not be used
Do not add or subtract a scaled integer to a pointer |
| Polyspace Bug Finder | R2024a | CERT C: Rule ARR39-C | Checks for incorrect pointer scaling (rule fully covered). |
| RuleChecker | 24.04 | scaled-pointer-arithmetic | Partially checked |
| TrustInSoft Analyzer | 1.38 | index_in_address | Exhaustively detects undefined behavior (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP41-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | ARR30-C. Do not form or use out-of-bounds pointers or array subscripts | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | ARR37-C. Do not add or subtract an integer to a pointer to a non-array object | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Pointer Arithmetic [RVG] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 18.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 18.2 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 18.3 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 18.4 (advisory) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-468, Incorrect Pointer Scaling | 2017-07-07: CERT: Exact |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [Murenin 07] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151963) [](../c/Rule%2006_%20Arrays%20_ARR_) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_)
## Comments:

|  |
| ----|
| For reference, this is a stricter version of EXP08-C. Ensure pointer arithmetic is used correctly.  The comments on that rec are worth saving, once this rule settles down. IOW we should revise that rec into EXP40 rather than a new rule, but we won't know for sure until we finalize this rule.
                                        Posted by svoboda at Jun 04, 2009 14:49
                                     |
| I think I fixed the rest of the problems and I corrected the title.; The next thing we need is an exception for when we have sizeof(*ptr) == 1 and ptr + sizeof(something), typically found with char *ptr.
                                        Posted by akeeton at Jun 04, 2009 16:16
                                     |
| I believe this is implicit in the current description and does not need to be further elaborated.
                                        Posted by rcs_mgr at Jun 07, 2009 09:50
                                     |
| Hi,;we get a question for this rule, could you kindly help clarify, thanks!if we use `sizeof` or `offset` as a divisor,  is it compliant or non-compliant, for example:
#include <stdio.h>
#include <stdlib.h>
unsigned int arr[16];
int main(int argc, char **argv)
{
    int size;
    size = atoi(argv[1]);
    int *p = (int *)(&arr[(size / sizeof(unsigned int))]);  // compliant or non-compliant?
    return 0;
}

IMO,  \`size / sizeof(unsigned int)\` is a scaled integer(right?)  and it's not the exceptional idiom \``` arr[sizeof(arr)/sizeof(arr[0])]` permitted by this rule, so strictly speaking, it's non-compliant. However, this pattern  ``**`seems less likely`**``  cause scaling bugs than using `sizeof` as operand of `+` or `*` operator, so shall we report violations for this kind of cases? ``
Many thanks in advance!
![](images/icons/contenttypes/comment_16.png) Posted by zhuoc at May 06, 2021 22:16
\| \|
First, while atoi() is clear in your code example, you don't want to use it in production code...see;[ERR34-C. Detect errors when converting a string to a number](ERR34-C_%20Detect%20errors%20when%20converting%20a%20string%20to%20a%20number) for details.
As for your code example, it \*could\* be compliant if it assumes that argv\[1\] indicates a byte offset from ((char\*) arr). If that is the case, then the code is compliant. Or would be if it made sure that 0\<=size\<16. Reading a byte offset from a program argument strikes me as strange, but there are other cases where an integer that measured bytes (rather than ints) was useful, perhaps when deserializing network data.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2021 15:47
\|
