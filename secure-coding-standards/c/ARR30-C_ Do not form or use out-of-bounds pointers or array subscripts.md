The C Standard identifies the following distinct situations in which undefined behavior (UB) can arise as a result of invalid pointer operations:

| UB | Description | Example Code |
| ----|----|----|
| 43 | Addition or subtraction of a pointer into, or just beyond, an array object and an integer type produces a result that does not point into, or just beyond, the same array object. | Forming Out-of-Bounds Pointer, Null Pointer Arithmetic |
| 44 | Addition or subtraction of a pointer into, or just beyond, an array object and an integer type produces a result that points just beyond the array object and is used as the operand of a unary * operator that is evaluated. | Dereferencing Past the End Pointer, Using Past the End Index |
| 46 | An array subscript is out of range, even if an object is apparently accessible with the given subscript, for example, in the lvalue expression a[1][7] given the declaration int a[4][5]). | Apparently Accessible Out-of-Range Index |
| 59 | An attempt is made to access, or generate a pointer to just past, a flexible array member of a structure when the referenced object provides no elements for that array. | Pointer Past Flexible Array Member |

## Noncompliant Code Example (Forming Out-of-Bounds Pointer)
In this noncompliant code example, the function `f()` attempts to validate the `index` before using it as an offset to the statically allocated `table` of integers. However, the function fails to reject negative `index` values. When `index` is less than zero, the behavior of the addition expression in the return statement of the function is [undefined behavior 43](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_43). On some implementations, the addition alone can trigger a hardware trap. On other implementations, the addition may produce a result that when dereferenced triggers a hardware trap. Other implementations still may produce a dereferenceable pointer that points to an object distinct from `table`. Using such a pointer to access the object may lead to information exposure or cause the wrong object to be modified.
``` c
enum { TABLESIZE = 100 };
static int table[TABLESIZE];
int *f(int index) {
  if (index < TABLESIZE) {
    return table + index;
  }
  return NULL;
}
```
## Compliant Solution
One compliant solution is to detect and reject invalid values of `index` if using them in pointer arithmetic would result in an invalid pointer:
``` c
enum { TABLESIZE = 100 };
static int table[TABLESIZE];
int *f(int index) {
  if (index >= 0 && index < TABLESIZE) {
    return table + index;
  }
  return NULL;
}
```
## Compliant Solution
Another slightly simpler and potentially more efficient compliant solution is to use an unsigned type to avoid having to check for negative values while still rejecting out-of-bounds positive values of `index`:
``` c
#include <stddef.h>
enum { TABLESIZE = 100 };
static int table[TABLESIZE];
int *f(size_t index) {
  if (index < TABLESIZE) {
    return table + index;
  }
  return NULL;
}
```
## Noncompliant Code Example (Dereferencing Past-the-End Pointer)
This noncompliant code example shows the flawed logic in the Windows Distributed Component Object Model (DCOM) Remote Procedure Call (RPC) interface that was exploited by the W32.Blaster.Worm. The error is that the `while` loop in the `GetMachineName()` function (used to extract the host name from a longer string) is not sufficiently bounded. When the character array pointed to by `pwszTemp` does not contain the backslash character among the first `MAX_COMPUTERNAME_LENGTH_FQDN + 1` elements, the final valid iteration of the loop will dereference past the end pointer, resulting in exploitable  [undefined behavior 44](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_47). In this case, the actual exploit allowed the attacker to inject executable code into a running program. Economic damage from the Blaster worm has been estimated to be at least $525 million \[[Pethia 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Pethia03)\].
For a discussion of this programming error in the Common Weakness Enumeration database, see [CWE-119](http://cwe.mitre.org/data/definitions/119.html), "Improper Restriction of Operations within the Bounds of a Memory Buffer," and [CWE-121](http://cwe.mitre.org/data/definitions/121.html), "Stack-based Buffer Overflow" \[[MITRE 2013](AA.-Bibliography_87152170.html#AA.Bibliography-MITRE)\].
``` c
error_status_t _RemoteActivation(
      /* ... */, WCHAR *pwszObjectName, ... ) {
   *phr = GetServerPath(
              pwszObjectName, &pwszObjectName);
    /* ... */
}
HRESULT GetServerPath(
  WCHAR *pwszPath, WCHAR **pwszServerPath ){
  WCHAR *pwszFinalPath = pwszPath;
  WCHAR wszMachineName[MAX_COMPUTERNAME_LENGTH_FQDN+1];
  hr = GetMachineName(pwszPath, wszMachineName);
  *pwszServerPath = pwszFinalPath;
}
HRESULT GetMachineName(
  WCHAR *pwszPath,
  WCHAR wszMachineName[MAX_COMPUTERNAME_LENGTH_FQDN+1])
{
  pwszServerName = wszMachineName;
  LPWSTR pwszTemp = pwszPath + 2;
  while (*pwszTemp != L'\\')
    *pwszServerName++ = *pwszTemp++;
  /* ... */
}
```
## Compliant Solution
In this compliant solution, the `while` loop in the `GetMachineName()` function is bounded so that the loop terminates when a backslash character is found, the null-termination character (`L'\0'`) is discovered, or the end of the buffer is reached. Or, as coded, the while loop continues as long as each character is neither a backslash nor a null character and is not at the end of the buffer. This code does not result in a buffer overflow even if no backslash character is found in `wszMachineName`.
``` c
HRESULT GetMachineName(
  wchar_t *pwszPath,
  wchar_t wszMachineName[MAX_COMPUTERNAME_LENGTH_FQDN+1])
{
  wchar_t *pwszServerName = wszMachineName;
  wchar_t *pwszTemp = pwszPath + 2;
  wchar_t *end_addr
    = pwszServerName + MAX_COMPUTERNAME_LENGTH_FQDN;
  while ((*pwszTemp != L'\\') &&
         (*pwszTemp != L'\0') &&
         (pwszServerName < end_addr))
  {
    *pwszServerName++ = *pwszTemp++;
  }
  /* ... */
}
```
This compliant solution is for illustrative purposes and is not necessarily the solution implemented by Microsoft. This particular solution may not be correct because there is no guarantee that a backslash is found.
## Noncompliant Code Example (Using Past-the-End Index)
Similar to the [dereferencing-past-the-end-pointer](#ARR30C.Donotformoruseoutofboundspointersorarraysubscripts-DereferencingPasttheEndPointer) error, the function `insert_in_table()` in this noncompliant code example uses an otherwise valid index to attempt to store a value in an element just past the end of an array.
First, the function incorrectly validates the index `pos` against the size of the buffer. When `pos` is initially equal to `size`, the function attempts to store `value` in a memory location just past the end of the buffer.
Second, when the index is greater than `size`, the function modifies `size` before growing the size of the buffer. If the call to `realloc()` fails to increase the size of the buffer, the next call to the function with a value of `pos` equal to or greater than the original value of `size` will again attempt to store `value` in a memory location just past the end of the buffer or beyond.
Third, the function violates [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap), which could lead to wrapping when 1 is added to `pos` or when `size` is multiplied by the size of `int`.
For a discussion of this programming error in the Common Weakness Enumeration database, see [CWE-122](http://cwe.mitre.org/data/definitions/122.html), "Heap-based Buffer Overflow," and [CWE-129](http://cwe.mitre.org/data/definitions/129.html), "Improper Validation of Array Index" \[[MITRE 2013](AA.-Bibliography_87152170.html#AA.Bibliography-MITRE)\].
``` c
#include <stdlib.h>
static int *table = NULL;
static size_t size = 0;
int insert_in_table(size_t pos, int value) {
  if (size < pos) {
    int *tmp;
    size = pos + 1;
    tmp = (int *)realloc(table, sizeof(*table) * size);
    if (tmp == NULL) {
      return -1;   /* Failure */
    }
    table = tmp;
  }
  table[pos] = value;
  return 0;
}
```
## Compliant Solution
This compliant solution correctly validates the index `pos` by using the `<=` relational operator, ensures the multiplication will not overflow, and avoids modifying `size` until it has verified that the call to `realloc()` was successful:
``` c
#include <stdint.h>
#include <stdlib.h>
static int *table = NULL;
static size_t size = 0;
int insert_in_table(size_t pos, int value) {
  if (size <= pos) {
    if ((SIZE_MAX - 1 < pos) ||
        ((pos + 1) > SIZE_MAX / sizeof(*table))) {
      return -1;
    }
    int *tmp = (int *)realloc(table, sizeof(*table) * (pos + 1));
    if (tmp == NULL) {
      return -1;
    }
    /* Modify size only after realloc() succeeds */
    size  = pos + 1;
    table = tmp;
  }
  table[pos] = value;
  return 0;
}
```
## Noncompliant Code Example (Apparently Accessible Out-of-Range Index)
This noncompliant code example declares `matrix` to consist of 7 rows and 5 columns in row-major order. The function `init_matrix` iterates over all 35 elements in an attempt to initialize each to the value given by the function argument `x`. However, because multidimensional arrays are declared in C in row-major order, the function iterates over the elements in column-major order, and when the value of `j` reaches the value `COLS` during the first iteration of the outer loop, the function attempts to access element `matrix[0][5]`. Because the type of `matrix` is `int[7][5]`, the `j` subscript is out of range, and the access has [undefined behavior 46](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_49).
``` c
#include <stddef.h>
#define COLS 5
#define ROWS 7
static int matrix[ROWS][COLS];
void init_matrix(int x) {
  for (size_t i = 0; i < COLS; i++) {
    for (size_t j = 0; j < ROWS; j++) {
      matrix[i][j] = x;
    }
  }
}
```
## Compliant Solution
This compliant solution avoids using out-of-range indices by initializing `matrix` elements in the same row-major order as multidimensional objects are declared in C:
``` c
#include <stddef.h>
#define COLS 5
#define ROWS 7
static int matrix[ROWS][COLS];
void init_matrix(int x) {
  for (size_t i = 0; i < ROWS; i++) {
    for (size_t j = 0; j < COLS; j++) {
      matrix[i][j] = x;
    }
  }
}
```
## Noncompliant Code Example (Pointer Past Flexible Array Member)
In this noncompliant code example, the function `find()` attempts to iterate over the elements of the flexible array member `buf`, starting with the second element. However, because function `g()` does not allocate any storage for the member, the expression `first++` in `find()` attempts to form a pointer just past the end of `buf` when there are no elements. This attempt is [undefined behavior 59](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_). (See [MSC21-C. Use robust loop termination conditions](MSC21-C_%20Use%20robust%20loop%20termination%20conditions) for more information.)
``` c
#include <stdlib.h>
struct S {
  size_t len;
  char buf[];  /* Flexible array member */
};
const char *find(const struct S *s, int c) {
  const char *first = s->buf;
  const char *last  = s->buf + s->len;
  while (first++ != last) { /* Undefined behavior */
    if (*first == c) {
      return first;
    }
  }
  return NULL;
}
void g(void) {
  struct S *s = (struct S *)malloc(sizeof(struct S));
  if (s == NULL) {
    /* Handle error */
  }
  s->len = 0;
  find(s, 'a');
}
```
## Compliant Solution
This compliant solution avoids incrementing the pointer unless a value past the pointer's current value is known to exist:
``` c
#include <stdlib.h>
struct S {
  size_t len;
  char buf[];  /* Flexible array member */
};
const char *find(const struct S *s, int c) {
  const char *first = s->buf;
  const char *last  = s->buf + s->len;
  while (first != last) { /* Avoid incrementing here */
    if (*++first == c) {
      return first;
    }
  }
  return NULL;
}
void g(void) {
  struct S *s = (struct S *)malloc(sizeof(struct S));
  if (s == NULL) {
    /* Handle error */
  }
  s->len = 0;
  find(s, 'a');
}
```
## Noncompliant Code Example (Null Pointer Arithmetic)
This noncompliant code example is similar to an [Adobe Flash Player vulnerability](http://www.iss.net/threats/289.html) that was first exploited in 2008. This code allocates a block of memory and initializes it with some data. The data does not belong at the beginning of the block, which is left uninitialized. Instead, it is placed `offset` bytes within the block. The function ensures that the data fits within the allocated block. 
``` c
#include <string.h>
#include <stdlib.h>
char *init_block(size_t block_size, size_t offset,
                 char *data, size_t data_size) {
  char *buffer = malloc(block_size);
  if (data_size > block_size || block_size - data_size < offset) {
    /* Data won't fit in buffer, handle error */
  }
  memcpy(buffer + offset, data, data_size);
  return buffer;
}
```
This function fails to check if the allocation succeeds, which is a violation of [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors). If the allocation fails, then `malloc()` returns a null pointer. The null pointer is added to `offset` and passed as the destination argument to `memcpy()`. Because a null pointer does not point to a valid object, the result of the pointer arithmetic is [undefined behavior 43](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_43).
An attacker who can supply the arguments to this function can exploit it to execute arbitrary code. This can be accomplished by providing an overly large value for `block_size`, which causes `malloc()` to fail and return a null pointer. The `offset` argument will then serve as the destination address to the call to `memcpy()`. The attacker can specify the `data` and `data_size` arguments to provide the address and length of the address, respectively, that the attacker wishes to write into the memory referenced by `offset`. The overall result is that the call to `memcpy()` can be exploited by an attacker to overwrite an arbitrary memory location with an attacker-supplied address, typically resulting in arbitrary code execution.
## Compliant Solution  (Null Pointer Arithmetic)
This compliant solution ensures that the call to `malloc()` succeeds:
``` c
#include <string.h>
#include <stdlib.h>
char *init_block(size_t block_size, size_t offset,
                 char *data, size_t data_size) {
  char *buffer = malloc(block_size);
  if (NULL == buffer) {
    /* Handle error */
  }
  if (data_size > block_size || block_size - data_size < offset) {
    /* Data won't fit in buffer, handle error */
  }
  memcpy(buffer + offset, data, data_size);
  return buffer;
}
```
## Risk Assessment
Writing to out-of-range pointers or array subscripts can result in a buffer overflow and the execution of arbitrary code with the permissions of the vulnerable process. Reading from out-of-range pointers or array subscripts can result in unintended information disclosure.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR30-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | array-index-rangearray-index-range-constant
null-dereferencing
pointered-deallocation
return-reference-local | Partially checkedCan detect all accesses to invalid pointers as well as array index out-of-bounds accesses and prove their absence.This rule is only partially checked as invalid but unused pointers may not be reported. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR30 | Can detect out-of-bound access to array / buffer |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.BU
LANG.MEM.TBA
LANG.MEM.TO
LANG.MEM.TU
LANG.STRUCT.PARITH
LANG.STRUCT.PBB
LANG.STRUCT.PPE
BADFUNC.BO.* | Buffer overrunBuffer underrun
Tainted buffer access
Type overrun
Type underrun
Pointer Arithmetic
Pointer before beginning of object
Pointer past end of object
A collection of warning classes that report uses of library functions prone to internal buffer overflows. |
| Compass/ROSE |  |  | Could be configured to catch violations of this rule. The way to catch the;noncompliant code example is to first hunt for example code that follows this pattern:   for (LPWSTR pwszTemp = pwszPath + 2; *pwszTemp != L'\\';
   *pwszTemp++;)

In particular, the iteration variable is a pointer, it gets incremented, and the loop condition does not set an upper bound on the pointer. Once this case is handled, ROSE can handle cases like the real noncompliant code example, which is effectively the same semantics, just different syntax
\| \|
[Coverity](Coverity)
\|
2017.07
\|
**OVERRUN**
**NEGATIVE_RETURNS**
**ARRAY_VS_SINGLETON**
**BUFFER_SIZE**
\|
Can detect the access of memory past the end of a memory buffer/array
Can detect when the loop bound may become negative
Can detect the out-of-bound read/write to array allocated statically or dynamically
Can detect buffer overflows
\| \| [Cppcheck](Cppcheck) \|
;2.15
\|
**arrayIndexOutOfBounds, outOfBounds, negativeIndex, arrayIndexThenCheck, arrayIndexOutOfBoundsCond,; possibleBufferAccessOutOfBounds**
\|
\| \| [Cppcheck Premium](Cppcheck%20Premium) \|
24.11.0
\|
**arrayIndexOutOfBounds, outOfBounds, negativeIndex, arrayIndexThenCheck, arrayIndexOutOfBoundsCond,; possibleBufferAccessOutOfBounds**
**premium-cert-arr30-c**
\|
\| \| [Helix QAC](Helix%20QAC) \|
2024.4
\|
**C2840**
**DF2820, DF2821, DF2822, DF2823, DF2840, DF2841, DF2842, DF2843, DF2930, DF2931, DF2932, DF2933, DF2935, DF2936, DF2937, DF2938, DF2950, DF2951, DF2952, DF2953**
\| \| \| [Klocwork](Klocwork) \|
2024.4
\|
**ABV.GENERALABV.GENERAL.MULTIDIMENSION**  
**NPD.FUNC.CALL.MIGHT**  
**ABV.ANY_SIZE_ARRAY**  
**ABV.STACK**  
**ABV.TAINTED**  
**ABV.UNICODE.BOUND_MAP**  
**ABV.UNICODE.FAILED_MAP**  
**ABV.UNICODE.NNTS_MAP**  
**ABV.UNICODE.SELF_MAP**  
**ABV.UNKNOWN_SIZE**  
**NNTS.MIGHT**  
**NNTS.MUST**  
**NNTS.TAINTED**  
**SV.TAINTED.INDEX_ACCESS**  
**SV.TAINTED.LOOP_BOUND**
\| \| \| [LDRA tool suite](LDRA) \|
;9.7.1
\|
**45 D, 47 S, 476 S, 489 S, 64 X, 66 X, 68 X, 69 X, 70 X, 71 X, 79 X**
\| Partially implemented \| \| [Parasoft C/C++test](Parasoft) \|
2024.2
\| **CERT_C-ARR30-a** \| Avoid accessing arrays out of bounds \| \| [Parasoft Insure++](Parasoft) \| \| \| Runtime analysis \| \| [PC-lint Plus](PC-lint%20Plus) \|
1.4
\|
**413, 415, 416, 613, 661, 662, 676**
\|
Fully supported
\| \| [Polyspace Bug Finder](Polyspace%20Bug%20Finder) \|
R2024a
\|
[CERT C: Rule ARR30-C](https://www.mathworks.com/help/bugfinder/ref/certcrulearr30c.html)
\|
Checks for:
-   Array access out of bounds
-   Pointer access out of bounds
-   Array access with tainted index
-   Use of tainted pointer
-   Pointer dereference with tainted offset
Rule partially covered.
\| \| [PVS-Studio](https://wiki.sei.cmu.edu/confluence/display/c/PVS-Studio) \|
7.35
\| [V512](https://pvs-studio.com/en/docs/warnings/v512/), [V557](https://pvs-studio.com/en/docs/warnings/v557/), [V582](https://pvs-studio.com/en/docs/warnings/v582/), [V594](https://pvs-studio.com/en/docs/warnings/v594/), [V643](https://pvs-studio.com/en/docs/warnings/v643/), [V645](https://pvs-studio.com/en/docs/warnings/v645/), **[V694](https://pvs-studio.com/en/docs/warnings/v694/)** \| \| \| [RuleChecker](RuleChecker) \|
24.04
\| **array-index-range-constantreturn-reference-local** \| Partially checked \| \| [TrustInSoft Analyzer](TrustInSoft%20Analyzer) \|
1.38
\| **index_in_address** \|
Exhaustively verified (see [one compliant and one non-compliant example](https://taas.trust-in-soft.com/tsnippet/t/3a7bd506)).
\|
### Related Vulnerabilities
[CVE-2008-1517](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2008-1517) results from a violation of this rule. Before Mac OSX version 10.5.7, the XNU kernel accessed an array at an unverified user-input index, allowing an attacker to execute arbitrary code by passing an index greater than the length of the array and therefore accessing outside memory \[[xorl 2009](http://xorl.wordpress.com/2009/06/09/cve-2008-1517-apple-mac-os-x-xnu-missing-array-index-validation/)\].
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | Arithmetic Wrap-Around Error [FIF] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Unchecked Array Indexing [XYZ] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Forming or using out-of-bounds pointers or array subscripts [invptr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-123, Write-what-where Condition | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-125, Out-of-bounds Read | 2017-05-18: CERT: Partial overlap |
| MISRA C:2012 | Rule 18.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-119 and ARR30-C
Independent( ARR30-C, ARR38-C, ARR32-C, INT30-C, INT31-C, EXP39-C, EXP33-C, FIO37-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
CWE-119 = Union( ARR30-C, ARR38-C)
Intersection( ARR30-C, ARR38-C) = Ø
### CWE-394 and ARR30-C
Intersection( ARR30-C, CWE-394) = Ø
CWE-394 deals with potentially-invalid function return values. Which may be used as an (invalid) array index, but validating the return value is a separate operation.
### CWE-125 and ARR30-C
Independent( ARR30-C, ARR38-C, EXP39-C, INT30-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
CWE-125 = Subset( CWE-119) = Union( ARR30-C, ARR38-C)
Intersection( ARR30-C, CWE-125) =
-   Reading from an out-of-bounds array index, or off the end of an array
ARR30-C – CWE-125 =
-   Writing to an out-of-bounds array index, or off the end of an array
CWE-125 – ARR30-C =
-   Reading beyond a non-array buffer
<!-- -->
-   Using a library function to achieve an out-of-bounds read.
### CWE-123 and ARR30-C
Independent(ARR30-C, ARR38-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
Intersection( CWE-123, ARR30-C) =
-   Write of arbitrary value to arbitrary (probably invalid) array index
ARR30-C – CWE-123 =
-   Read of value from arbitrary (probably invalid) array index
<!-- -->
-   Construction of invalid index (pointer arithmetic)
CWE-123 – ARR30-C =
-   Arbitrary writes that do not involve directly constructing an invalid array index
### CWE-129 and ARR30-C
Independent( ARR30-C, ARR32-C, INT31-C, INT32-C)
ARR30-C = Union( CWE-129, list), where list =
-   Dereferencing an out-of-bounds array index, where index is a trusted value
<!-- -->
-   Forming an out-of-bounds array index, without dereferencing it, whether or not index is a trusted value. (This excludes the array’s TOOFAR index, which is one past the final element; this behavior is well-defined in C11.)
### CWE-120 and ARR30-C
See CWE-120 and MEM35-C
### CWE-122 and ARR30-C
Intersection( ARR30-C, CWE-122) = Ø
CWE-122 specifically addresses buffer overflows on the heap operations, which occur in the context of string-copying. ARR30 specifically addresses improper creation or references of array indices. Which might happen as part of a heap buffer overflow, but is on a lower programming level.
### CWE-20 and ARR30-C
See CWE-20 and ERR34-C
### CWE-687 and ARR30-C
Intersection( CWE-687, ARR30-C) = Ø
ARR30-C is about invalid array indices which are created through pointer arithmetic, and dereferenced through an operator (\* or \[\]). Neither involve function calls, thus CWE-687 does not apply.
### CWE-786 and ARR30-C
ARR30-C = Union( CWE-786, list) where list =
-   Access of memory location after end of buffer
<!-- -->
-   Construction of invalid arry reference (pointer). This does not include an out-of-bounds array index (an integer).
### CWE-789 and ARR30-C
Intersection( CWE-789, ARR30-C) = Ø
CWE-789 is about allocating memory, not array subscripting
## Bibliography

|  |  |
| ----|----|
| [Finlay 2003] |  |
| [Microsoft 2003] |  |
| [Pethia 2003] |  |
| [Seacord 2013b] | Chapter 1, "Running with Scissors" |
| [Viega 2005] | Section 5.2.13, "Unchecked Array Indexing" |
| [xorl 2009 ] | "CVE-2008-1517: Apple Mac OS X (XNU) Missing Array Index Validation" |

------------------------------------------------------------------------
[](../c/Rule%2006_%20Arrays%20_ARR_) [](../c/Rule%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152385)
## Comments:

|  |
| ----|
| The Compass/ROSE entry on this page is verbose and weird, relative to the other tool entries.
                                        Posted by rcs at Nov 06, 2013 11:33
                                     |
| The "Compliant Solution;(Using Past-the-End Index)" still violates "INT30-C. Ensure that unsigned integer operations do not wrap": if pos is exactly SIZE_MAX, (pos+1) will wrap to 0, and realloc(table,0) will be called. What happens next is implementation-defined ("MEM04-C. Beware of zero-length allocations"):If realloc(table,0) frees table and returns NULL, this will violate "MEM30-C. Do not access freed memory" the next time insert_in_table() is called (because the static variables table and size are not updated).If realloc(table,0) returns a 0-sized chunk of memory, table and size are correctly updated (size becomes 0), but there is an immediate out-of-bounds write when value is stored to table[pos] (pos is SIZE_MAX).If realloc(table,0) returns NULL as an error, but does not free table, nothing bad will happen because the static variables table and size are left untouched (does such an implementation actually exist?).
                                        Posted by qualys at May 31, 2015 13:37
                                     |
| The "Null Pointer Arithmetic" examples (both Noncompliant and Compliant) still violate "ARR30-C. Do not form or use out-of-bounds pointers or array subscripts": the;block_size - data_size > offset check should be block_size - data_size < offset. Right now, the memcpy() can overflow buffer because the check guarantees that offset + data_size >= block_size.
                                        Posted by qualys at May 31, 2015 13:53
                                     |
| You are correct, this was still missing a check for the case where;pos == SIZE_MAX. I've corrected now. Thank you!
                                        Posted by aballman at Jun 01, 2015 09:46
                                     |
| Thank you for pointing this out, I've corrected the mistake.
                                        Posted by aballman at Jun 01, 2015 18:29
                                     |
| Great, thanks to all of you for your hard work!
                                        Posted by qualys at Jun 02, 2015 03:36
                                     |
| Hello, I think that the compliant solution for the "GetMachineName" function in the example for "Dereferencing Past the End Pointer", has the incorrect logical operator && when the description says "...;or the end of the buffer is reached..".If I understand correctly, the correct operator should be ||.
Thanks for publishing this information!
                                        Posted by nahueld.sanchez at Aug 01, 2019 22:01
                                     |
| No.; The description and the code show the same contents in different ways."the loop terminates when a backslash character is found, the null-termination character is discovered, or the end of the buffer is reached"while (      (*pwszTemp != L'\\')         && ( *pwszTemp  != L'\0')         && (pwszServerName < end_addr)   )
the description can be rearranged according to the code:"the loop keeps only while the character is not a backslash, and not a null-termination, and the end of the buffer is not reached"
Or, the code can be rearranged according to the description:while ( ! (   (*pwszTemp == L'\\')               || ( *pwszTemp  == L'\0')               || (pwszServerName => end_addr)             )         )
I bet it's better to revise the description, because the current code looks simple and understandable for me.
BTW, I believe there's no meaning that the parens doubled  at the null char testing expression...
                                        Posted by yozo at Aug 01, 2019 23:16
                                     |
| Yozo TODAis correct. The code and the description are semantically the same. The code is simple and understandable for C code, and the English description is simple and understandable English. IMO the logic difference in the way C and English are expressed here is simply due to the inherent syntax of C vs English. That is, what makes good C code does not necessarily make good English;I've cleaned up the indentation and removed the redundant parentheses.
                                        Posted by svoboda at Aug 02, 2019 10:07
                                     |
| In the compliant solution (Pointer Past Flexible Array Member) the cast to unsigned char could potentially violate INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data. While likely not a code vulnerability per se it could result in unexpected behavior
                                        Posted by 0skellar at May 12, 2023 08:22
                                     |
| I took out the cast to unsigned char for both the noncompliant and compliant code examples. As you note, it *can* produceunexpected code behavior, and it distracts from the main point of the examples (i.e the invalid pointers).
                                        Posted by svoboda at May 12, 2023 10:32
                                     |

