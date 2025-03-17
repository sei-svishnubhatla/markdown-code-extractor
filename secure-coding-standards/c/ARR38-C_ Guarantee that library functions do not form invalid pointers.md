C library functions that make changes to arrays or objects take at least two arguments: a pointer to the array or object and an integer indicating the number of elements or bytes to be manipulated. For the purposes of this rule, the element count of a pointer is the size of the object to which it points, expressed by the number of elements that are valid to access. Supplying arguments to such a function might cause the function to form a pointer that does not point into or just past the end of the object, resulting in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
Annex J of the C Standard \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\] states that it is undefined behavior if the "pointer passed to a library function array parameter does not have a value such that all address computations and object accesses are valid." (See undefined behavior 108.)
In the following code,
``` java
int arr[5];
int *p = arr;
unsigned char *p2 = (unsigned char *)arr;
unsigned char *p3 = arr + 2;
void *p4 = arr;
```
the element count of the pointer `p` is `sizeof(arr) / sizeof(arr[0])`, that is, `5`. The element count of the pointer `p2` is `sizeof(arr)`, that is, `20`, on implementations where `sizeof(int) == 4`. The element count of the pointer `p3` is `12` on implementations where `sizeof(int) == 4`, because `p3` points two elements past the start of the array `arr`.  The element count of `p4` is treated as though it were `unsigned char *` instead of `void *`, so it is the same as `p2`.
## Pointer + Integer
The following standard library functions take a pointer argument and a size argument, with the constraint that the pointer must point to a valid memory object of at least the number of elements indicated by the size argument.

|  |  |  |  |
| ----|----|----|----|
| fgets() | fgetws() | mbstowcs()1; | wcstombs()1 |
| mbrtoc16()2; | mbrtoc32()2 | mbsrtowcs()1 | wcsrtombs()1 |
| mbtowc()2; | mbrtowc()2 | mblen() | mbrlen() |
| memchr() | wmemchr() | memset() | wmemset() |
| strftime() | wcsftime() | strxfrm()1 | wcsxfrm()1 |
| strncat()2; | wcsncat()2 | snprintf() | vsnprintf() |
| swprintf() | vswprintf() | setvbuf() | tmpnam_s() |
| snprintf_s() | sprintf_s(); | vsnprintf_s() | vsprintf_s() |
| gets_s(); | getenv_s() | wctomb_s() | mbstowcs_s()3 |
| wcstombs_s()3 | memcpy_s()3 | memmove_s()3 | strncpy_s()3 |
| strncat_s()3 | strtok_s()2 | strerror_s() | strnlen_s() |
| asctime_s() | ctime_s() | snwprintf_s() | swprintf_s() |
| vsnwprintf_s() | vswprintf_s() | wcsncpy_s()3 | wmemcpy_s()3 |
| wmemmove_s()3 | wcsncat_s()3 | wcstok_s()2 | wcsnlen_s() |
| wcrtomb_s() | mbsrtowcs_s()3 | wcsrtombs_s()3 | memset_s()4 |

<sup>1</sup> Takes two pointers and an integer, but the integer specifies the element count only of the output buffer, not of the input buffer.  
<sup>2</sup> Takes two pointers and an integer, but the integer specifies the element count only of the input buffer, not of the output buffer.  
<sup>3</sup> Takes two pointers and two integers; each integer corresponds to the element count of one of the pointers.  
4 Takes a pointer and two size-related integers; the first size-related integer parameter specifies the number of bytes available in the buffer; the second size-related integer parameter specifies the number of bytes to write within the buffer.
For calls that take a pointer and an integer size, the given size should not be greater than the element count of the pointer.
###  Noncompliant Code Example (Element Count)
In this noncompliant code example, the incorrect element count is used in a call to `wmemcpy()`. The `sizeof` operator returns the size expressed in bytes, but `wmemcpy()` uses an element count based on `wchar_t *`.
``` java
#include <string.h>
#include <wchar.h>
static const char str[] = "Hello world";
static const wchar_t w_str[] = L"Hello world";
void func(void) {
  char buffer[32];
  wchar_t w_buffer[32];
  memcpy(buffer, str, sizeof(str)); /* Compliant */
  wmemcpy(w_buffer, w_str, sizeof(w_str)); /* Noncompliant */
}
```
### Compliant Solution (Element Count)
When using functions that operate on pointed-to regions, programmers must always express the integer size in terms of the element count expected by the function. For example, `memcpy()` expects the element count expressed in terms of `void *`, but `wmemcpy()` expects the element count expressed in terms of `wchar_t *`.  Instead of the `sizeof` operator, functions that return the number of elements in the string are called, which matches the expected element count for the copy functions. In the case of this compliant solution, where the argument is an array `A` of type `T`, the expression `sizeof(A) / sizeof(T)`, or equivalently `sizeof(A) / sizeof(*A)`, can be used to compute the number of elements in the array.
``` java
#include <string.h>
#include <wchar.h>
static const char str[] = "Hello world";
static const wchar_t w_str[] = L"Hello world";
void func(void) {
  char buffer[32];
  wchar_t w_buffer[32];
  memcpy(buffer, str, strlen(str) + 1);
  wmemcpy(w_buffer, w_str, wcslen(w_str) + 1);
} 
```
### Noncompliant Code Example (Pointer + Integer)
This noncompliant code example assigns a value greater than the number of bytes of available memory to `n`, which is then passed to `memset()`:
``` java
#include <stdlib.h>
#include <string.h>
void f1(size_t nchars) {
  char *p = (char *)malloc(nchars);
  /* ... */
  const size_t n = nchars + 1;
  /* ... */
  memset(p, 0, n);
}
```
### Compliant Solution (Pointer + Integer)
This compliant solution ensures that the value of `n` is not greater than the number of bytes of the dynamic memory pointed to by the pointer `p`:
``` java
#include <stdlib.h>
#include <string.h>
void f1(size_t nchars) {
  char *p = (char *)malloc(nchars);
  /* ...  */
  const size_t n = nchars;
  /* ...  */
  memset(p, 0, n);
}
```
### Noncompliant Code Example (Pointer + Integer)
In this noncompliant code example, the element count of the array `a` is `ARR_SIZE` elements. Because `memset()` expects a byte count, the size of the array is scaled incorrectly by `sizeof(int)` instead of `sizeof(long)`, which can form an invalid pointer on architectures where `sizeof(int) != sizeof(long)`.
``` java
#include <string.h>
void f2(void) {
  const size_t ARR_SIZE = 4;
  long a[ARR_SIZE];
  const size_t n = sizeof(int) * ARR_SIZE;
  void *p = a;
  memset(p, 0, n);
}
```
### Compliant Solution (Pointer + Integer)
In this compliant solution, the element count required by `memset()` is properly calculated without resorting to scaling:
``` java
#include <string.h>
void f2(void) {
  const size_t ARR_SIZE = 4;
  long a[ARR_SIZE];
  const size_t n = sizeof(a);
  void *p = a;
  memset(p, 0, n);
}
```
## Two Pointers + One Integer
The following standard library functions take two pointer arguments and a size argument, with the constraint that both pointers must point to valid memory objects of at least the number of elements indicated by the size argument. 

|  |  |  |  |
| ----|----|----|----|
| memcpy() | wmemcpy() | memmove() | wmemmove() |
| strncpy() | wcsncpy() | memcmp() | wmemcmp() |
| strncmp() | wcsncmp() | strcpy_s() | wcscpy_s() |
| strcat_s() | wcscat_s() |  |  |

For calls that take two pointers and an integer size, the given size should not be greater than the element count of either pointer.
### Noncompliant Code Example (Two Pointers + One Integer)
In this noncompliant code example, the value of `n` is incorrectly computed, allowing a read past the end of the object referenced by `q`:
``` java
#include <string.h>
void f4() {
  char p[40];
  const char *q = "Too short";
  size_t n = sizeof(p);
  memcpy(p, q, n);
}
```
### Compliant Solution (Two Pointers + One Integer)
This compliant solution ensures that `n` is equal to the size of the character array:
``` java
#include <string.h>
void f4() {
  char p[40];
  const char *q = "Too short";
  size_t n = sizeof(p) < strlen(q) + 1 ? sizeof(p) : strlen(q) + 1;
  memcpy(p, q, n);
}
```
## One Pointer + Two Integers
The following standard library functions take a pointer argument and two size arguments, with the constraint that the pointer must point to a valid memory object containing at least as many bytes as the product of the two size arguments.

|  |  |  |  |
| ----|----|----|----|
| bsearch() | bsearch_s() | qsort() | qsort_s() |
| fread() | fwrite() | ; |  |

For calls that take a pointer and two integers, one integer represents the number of bytes required for an individual object, and a second integer represents the number of elements in the array. The resulting product of the two integers should not be greater than the element count of the pointer were it expressed as an unsigned char \*.  
### Noncompliant Code Example (One Pointer + Two Integers)
This noncompliant code example allocates a variable number of objects of type `struct obj`. The function checks that `num_objs` is small enough to prevent wrapping, in compliance with [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap). The size of `struct obj` is assumed to be 16 bytes to account for padding to achieve the assumed alignment of `long long`. However, the padding typically depends on the target architecture, so this object size may be incorrect, resulting in an incorrect element count.
``` java
#include <stdint.h>
#include <stdio.h>
struct obj {
  char c;
  long long i;
};
void func(FILE *f, struct obj *objs, size_t num_objs) {
  const size_t obj_size = 16;
  if (num_objs > (SIZE_MAX / obj_size) ||
      num_objs != fwrite(objs, obj_size, num_objs, f)) {
    /* Handle error */
  }
}
```
### Compliant Solution (One Pointer + Two Integers)
This compliant solution uses the sizeof operator to correctly provide the object size and num_objs to provide the element count:
``` java
#include <stdint.h>
#include <stdio.h>
struct obj {
  char c;
  long long i;
};
void func(FILE *f, struct obj *objs, size_t num_objs) {
  const size_t obj_size = sizeof *objs;
  if (num_objs > (SIZE_MAX / obj_size) ||
      num_objs != fwrite(objs, obj_size, num_objs, f)) {
    /* Handle error */
  }
}
```
### Noncompliant Code Example (One Pointer + Two Integers)
In this noncompliant code example, the function `f()` calls `fread()` to read `nitems` of type `wchar_t`, each `size` bytes in size, into an array of `BUFFER_SIZE` elements, `wbuf`. However, the expression used to compute the value of `nitems` fails to account for the fact that, unlike the size of `char`, the size of `wchar_t` may be greater than 1. Consequently, `fread()` could attempt to form pointers past the end of `wbuf` and use them to assign values to nonexistent elements of the array. Such an attempt is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See undefined behavior 109.)  A likely consequence of this undefined behavior is a buffer overflow. For a discussion of this programming error in the Common Weakness Enumeration database, see [CWE-121](http://cwe.mitre.org/data/definitions/121.html), "Stack-based Buffer Overflow," and [CWE-805](http://cwe.mitre.org/data/definitions/805.html), "Buffer Access with Incorrect Length Value."
``` c
#include <stddef.h>
#include <stdio.h>
void f(FILE *file) {
  enum { BUFFER_SIZE = 1024 };
  wchar_t wbuf[BUFFER_SIZE];
  const size_t size = sizeof(*wbuf);
  const size_t nitems = sizeof(wbuf);
  size_t nread = fread(wbuf, size, nitems, file);
  /* ... */
}
```
### Compliant Solution (One Pointer + Two Integers)
This compliant solution correctly computes the maximum number of items for `fread()` to read from the file:
``` c
#include <stddef.h>
#include <stdio.h>
void f(FILE *file) {
  enum { BUFFER_SIZE = 1024 };
  wchar_t wbuf[BUFFER_SIZE];
  const size_t size = sizeof(*wbuf);
  const size_t nitems = sizeof(wbuf) / size;
  size_t nread = fread(wbuf, size, nitems, file);
  /* ... */
}
```
### Noncompliant Code Example (Heartbleed)
CERT vulnerability [720951](http://www.kb.cert.org/vuls/id/720951) describes a vulnerability in OpenSSL versions 1.0.1 through 1.0.1f, popularly known as "Heartbleed." This vulnerability allows an attacker to steal information that under normal conditions would be protected by Secure Socket Layer/Transport Layer Security (SSL/TLS) encryption.
Despite the seriousness of the vulnerability, Heartbleed is the result of a common programming error and an apparent lack of awareness of secure coding principles. Following is the vulnerable code:
``` c
int dtls1_process_heartbeat(SSL *s) {         
  unsigned char *p = &s->s3->rrec.data[0], *pl;
  unsigned short hbtype;
  unsigned int payload;
  unsigned int padding = 16; /* Use minimum padding */
  /* Read type and payload length first */
  hbtype = *p++;
  n2s(p, payload);
  pl = p;
  /* ... More code ... */
  if (hbtype == TLS1_HB_REQUEST) {
    unsigned char *buffer, *bp;
    int r;
    /* 
     * Allocate memory for the response; size is 1 byte
     * message type, plus 2 bytes payload length, plus
     * payload, plus padding.
     */
    buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    bp = buffer;
    /* Enter response type, length, and copy payload */
    *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);
    memcpy(bp, pl, payload);
    /* ... More code ... */
  }
  /* ... More code ... */
}
```
This code processes a "heartbeat" packet from a client. As specified in [RFC 6520](https://tools.ietf.org/html/rfc6520), when the program receives a heartbeat packet, it must echo the packet's data back to the client. In addition to the data, the packet contains a length field that conventionally indicates the number of bytes in the packet data, but there is nothing to prevent a malicious packet from lying about its data length.
The `p` pointer, along with `payload` and `p1`, contains data from a packet. The code allocates a `buffer` sufficient to contain `payload` bytes, with some overhead, then copies `payload` bytes starting at `p1` into this buffer and sends it to the client. Notably absent from this code are any checks that the payload integer variable extracted from the heartbeat packet corresponds to the size of the packet data. Because the client can specify an arbitrary value of `payload`, an attacker can cause the server to read and return the contents of memory beyond the end of the packet data, which violates [INT04-C. Enforce limits on integer values originating from tainted sources](INT04-C_%20Enforce%20limits%20on%20integer%20values%20originating%20from%20tainted%20sources). The resulting call to `memcpy()` can then copy the contents of memory past the end of the packet data and the packet itself, potentially exposing sensitive data to the attacker. This call to `memcpy()` violates [ARR38-C. Guarantee that library functions do not form invalid pointers](ARR38-C_%20Guarantee%20that%20library%20functions%20do%20not%20form%20invalid%20pointers). A version of ARR38-C also appears in [ISO/IEC TS 17961:2013](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTS17961), "Forming invalid pointers by library functions \[libptr\]." This rule would require a conforming analyzer to diagnose the Heartbleed vulnerability.
### Compliant Solution (Heartbleed)
OpenSSL version 1.0.1g contains the following patch, which guarantees that `payload` is within a valid range. The range is limited by the size of the input record.
``` c
int dtls1_process_heartbeat(SSL *s) {         
  unsigned char *p = &s->s3->rrec.data[0], *pl;
  unsigned short hbtype;
  unsigned int payload;
  unsigned int padding = 16; /* Use minimum padding */
  /* ... More code ... */
  /* Read type and payload length first */
  if (1 + 2 + 16 > s->s3->rrec.length)
    return 0; /* Silently discard */
  hbtype = *p++;
  n2s(p, payload);
  if (1 + 2 + payload + 16 > s->s3->rrec.length)
    return 0; /* Silently discard per RFC 6520 */
  pl = p;
  /* ... More code ... */
  if (hbtype == TLS1_HB_REQUEST) {
    unsigned char *buffer, *bp;
    int r;
    /* 
     * Allocate memory for the response; size is 1 byte
     * message type, plus 2 bytes payload length, plus
     * payload, plus padding.
     */
    buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    bp = buffer;
    /* Enter response type, length, and copy payload */
    *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);
    memcpy(bp, pl, payload);
    /* ... More code ... */
  }
  /* ... More code ... */
}
```
## Risk Assessment
Depending on the library function called, an attacker may be able to use a heap or stack overflow [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) to run arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR38-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | array_out_of_bounds | SupportedAstrée reports all out-of-bound accesses within library analysis stubs. The user may provide additional stubs for arbitrary (library) functions. |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.BU
BADFUNC.BO.* | Buffer overrunBuffer underrun
A collection of warning classes that report uses of library functions prone to internal buffer overflows |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | BUFFER_SIZEBAD_SIZEOFBAD_ALLOC_STRLENBAD_ALLOC_ARITHMETIC | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-arr38-c |  |
| Fortify SCA | 5.0 |  | Can detect violations of this rule with CERT C Rule Pack |
| Helix QAC | 2024.4 | C2840DF2840, DF2841, DF2842, DF2843, DF2845, DF2846, DF2847, DF2848, DF2935, DF2936, DF2937, DF2938, DF4880, DF4881, DF4882, DF4883 |  |
| Klocwork | 2024.4 | ABV.GENERALABV.GENERAL.MULTIDIMENSION |  |
| LDRA tool suite | 9.7.1 | 64 X, 66 X, 68 X, 69 X, 70 X, 71 X, 79 X | Partially Implmented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR38-aCERT_C-ARR38-b
CERT_C-ARR38-c
CERT_C-ARR38-d | Avoid overflow when reading from a bufferAvoid overflow when writing to a buffer
Avoid buffer overflow due to defining incorrect format limits
Avoid overflow due to reading a not zero terminated string |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 419, 420 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule ARR38-C | Checks for:Mismatch between data length and sizeInvalid use of standard library memory routinePossible misuse of sizeofBuffer overflow from incorrect string format specifierInvalid use of standard library string routineDestination buffer overflow in string manipulationDestination buffer underflow in string manipulationRule partially covered. |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | out of bounds read | Partially verified. |

### Related Vulnerabilities
[CVE-2016-2208](https://bugs.chromium.org/p/project-zero/issues/detail?id=820) results from a violation of this rule. The attacker can supply a value used to determine how much data is copied into a buffer via `memcpy()`, resulting in a buffer overlow of attacker-controlled data.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR38-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| C Secure Coding Standard | API00-C. Functions should validate their parameters | Prior to 2018-01-12: CERT: Unspecified Relationship |
| C Secure Coding Standard | ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array | Prior to 2018-01-12: CERT: Unspecified Relationship |
| C Secure Coding Standard | INT30-C. Ensure that unsigned integer operations do not wrap | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Forming invalid pointers by library functions [libptr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Buffer Boundary Violation (Buffer Overflow) [HCB] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Unchecked Array Copying [XYW] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-121, Stack-based Buffer Overflow | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-123, Write-what-where Condition | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-125, Out-of-bounds Read | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-805, Buffer Access with Incorrect Length Value | 2017-05-18: CERT: Partial overlap |
| CWE 3.1 | CWE-129, Improper Validation of Array Index | 2017-10-30:MITRE:Unspecified Relationship2018-10-18:CERT:Partial Overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-121 and ARR38-C
Intersection( CWE-121, ARR38-C) =
-   Stack buffer overflow from passing invalid arguments to library function
CWE-121 – ARR38-C =
-   Stack buffer overflows from direct out-of-bounds write
ARR38-C – CWE-121 =
-   Out-of-bounds read from passing invalid arguments to library function
<!-- -->
-   Buffer overflow on heap or data segment from passing invalid arguments to library function
### CWE-119 and ARR38-C
See CWE-119 and ARR30-C
### CWE-125 and ARR38-C
Independent( ARR30-C, ARR38-C, EXP39-C, INT30-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
Intersection( ARR38-C, CWE-125) =
-   Reading from an out-of-bounds array index or off the end of an array via standard library function
ARR38-C – CWE-125 =
-   Writing to an out-of-bounds array index or off the end of an array via standard library function
CWE-125 – ARR38-C =
-   Reading beyond a non-array buffer
<!-- -->
-   Reading beyond an array directly (using pointer arithmetic, or \[\] notation)
### CWE-805 and ARR38-C
Intersection( CWE-805, ARR38-C) =
-   Buffer access with incorrect length via passing invalid arguments to library function
CWE-805 – ARR38-C =
-   Buffer access with incorrect length directly (such as a loop construct)
ARR38-C – CWE-805 =
-   Out-of-bounds read or write that does not involve incorrect length (could use incorrect offset instead), that uses library function
### CWE-123 and ARR38-C
Independent(ARR30-C, ARR38-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
CWE-123 includes any operation that allows an attacker to write an arbitrary value to an arbitrary memory location. This could be accomplished via overwriting a pointer with data that refers to the address to write, then when the program writes to a pointed-to value, supplying a malicious value. Vulnerable pointer values can be corrupted by:
-   Stack return address
<!-- -->
-   Buffer overflow on the heap (which typically overwrites back/next pointer values)
<!-- -->
-   Write to untrusted array index (if it is also invalid)
<!-- -->
-   Format string exploit
<!-- -->
-   Overwriting a C++ object with virtual functions (because it has a virtual pointer)
<!-- -->
-   Others?
Intersection( CWE-123, ARR38-C) =
-   Buffer overflow via passing invalid arguments to library function
ARR38-C – CWE-123 =
-   Buffer overflow to “harmless” memory from passing invalid arguments to library function
<!-- -->
-   Out-of-bounds read from passing invalid arguments to library function
CWE-123 – ARR38-C =
-   Arbitrary writes that do not involve standard C library functions
### CWE-129 and ARR38-C
ARR38-C - CWE-129 = making library functions create invalid pointers without using untrusted data.
E.g. : `char[3] array;`
`strcpy(array, "123456");`
CWE-129 - ARR38-C = not validating an integer used as an array index or in pointer arithmetic
E.g.: `void foo(int i) {`
`  char array[3];`
`  array[i];`
`}`
Intersection(ARR38-C, CWE-129) = making library functions create invalid pointers using untrusted data.
`eg: void foo(int i) {`
`  char src[3], dest[3];`
`  memcpy(dest, src, i);`
`}`
## Bibliography

|  |  |
| ----|----|
| [Cassidy 2014] | Existential Type Crisis : Diagnosis of the OpenSSL Heartbleed Bug |
| [IETF: RFC 6520] |  |
| [ISO/IEC TS 17961:2013] |  |
| [VU#720951] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152085) [](../c/Rule%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152330) 
## Comments:

|  |
| ----|
| Why not include this example?
EXAMPLE 4 In the following function definition, assume that the effective size of *p and the effective size of *q are not determinable. Furthermore, the effective type of *p (that is, char) is compatible with effective type of *q (also char). However, effective type of *p (char) is not compatible with derived type of the expression n (pointer to char) and consequently the call to memcpy is diagnosed.
void f5(char p[], const char *q) {
  const size_t n = sizeof(p);   // diagnostic required
  memcpy(p, q, n);
  /* ... */
}

For an assignment expression `E` whose right operand is a call to a memory allocation function taking an integer argument `n`, and the type of whose left operand is `T*`, or the equivalent initialization expression the expression `E` where `(n < sizeof (T))` shall be diagnosed.
For an assignment expression `E` whose right operand is a call to a memory allocation function taking an integer argument `n`, and the type of whose left operand is `T *`, or the equivalent initialization expression the expression `E` where `T` is compatible with neither the derived type of the expression `n` nor `unsigned char` shall be diagnosed.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 30, 2011 10:33
\| \|
I've included the full definitions of "derived type" and "effective size" from CSGR and I left the simplified versions as well. This is probably incorrect, but I'm not sure which approach makes more sense.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 30, 2011 10:36
\| \|
I'm very uncertain about the following notes:
> Note: While still noncompliant, this code does not constitute a vulnerability on implementations where sizeof(int) is equal to sizeof(float).

Here are my concerns:
1.  If our goal is to make this version of the standard consistent with CSCR, diagnosing these violations is inconsistent with the San Francisco rule, particularly because this is being proposed as a rule and not a recommendation.
2.  These violations will need to be discovered manually if conforming analyzers are not required to diagnose.
3.  This sort of sets a precedence to identify all situations under which the noncompliant example is not dangerous.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 30, 2011 11:39
\| \|
I seem to remember one of the final things we did in TS 17961 was to break out Allocating insufficient memory;                                                                                                                    \[insufmem\] from this rule because this rule was too hard to express otherwise.  I think we need to remove the memory allocation functions from this rule (there are no examples) and probably create a new rule based on \[insufmem\] in the dynamic memory section of this standard.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Oct 02, 2013 07:03
\| \|
I think we should reorganized this section more or less as follows.
;
To guarantee that a standard library function does not construct an out-of-bounds pointer, programmers must heed the following rules when using functions that operate on pointed-to regions:
-   Always express the integer size in terms of the effective size expected by the function.
    -   Eg) `memcpy()` expects the effective size expressed in terms of `void *`, but `wmemcpy()` expects the effective size expressed in terms of `wchar_t *`.
use the above as an example of effective size.  the guarantee language is too strong for this.
-   For calls that take a pointer and an integer size, the given size should not be greater than the effective size of the pointer.
-   For calls that take a two pointers and an integer size, the given size should not be greater than the effective size of either pointer.
-   For calls that take a pointer and two integers, generally accept one integer representing the size of an individual object, and a second integer representing the number of objects in the array.  The resulting product of the two integers should not be greater than the effective size of the pointer were it expressed as an `unsigned char *`.   See [INT30-C. Ensure that unsigned integer operations do not wrap](https://www.securecoding.cert.org/confluence/display/seccode/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap) for more information.
move the above to the subsections for each case.
-   For standard memory allocation functions, the size (possibly scaled, as in the case of `calloc()`) should not be less than the desired effective size of the object being allocated were it expressed as an `unsigned char *`.  See [MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap](https://www.securecoding.cert.org/confluence/display/seccode/MEM07-C.+Ensure+that+the+arguments+to+calloc%28%29%2C+when+multiplied%2C+do+not+wrap) for more information about `calloc()`.
remove this  / or move to the new rule based on \[insufmem\]
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Oct 02, 2013 07:08
\| \|
In each CS/NCE pair we make some generalization about functions that take certain parameters, but I think this might be better if move the function tables into each section and then say "for the following functions, x and y hold true".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 19, 2013 16:42
\| \|
How does the new layout look to you?
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 21, 2013 09:38
\| \|
me like.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 01, 2013 12:13
\| \|
This second sentence was deleted from the book:
"For the purposes of this rule, the element count of a pointer is the size of the object to which it points, expressed by the number of elements that are valid to access."
Does anyone think it needs to be here?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 22, 2014 08:03
\| \|
Well, this term is used heavily throughout this rule, so we need to reword the rule. (I presume we did this in the book, right?)
A quick search for "element count" reveals that it occurs in no other rules, but in 2 recommendations:;[API02-C. Functions that read or write to or from an array should take an argument to specify the source or target size](API02-C_%20Functions%20that%20read%20or%20write%20to%20or%20from%20an%20array%20should%20take%20an%20argument%20to%20specify%20the%20source%20or%20target%20size) and [EXP08-C. Ensure pointer arithmetic is used correctly](EXP08-C_%20Ensure%20pointer%20arithmetic%20is%20used%20correctly). They should be reworded.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2014 08:49
\| \|
I added the sentence back here.; The version in the book was not reworded.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 22, 2014 09:34
\| \|
The examples and explaining text on the "Two pointers and one integer" could be made better. Here are some thoughts:
The non-compliant code fragment does not really demonstrate the problem at hand, but rather the ARR01-C problem. The function parameter type char\[\] is actually a char\* in the function body, thus the sizeof(p) is the size of the pointer, not the array. If we want to keep this example, the explanation of the problem could highlight this problem.
One of the issues mentioned is that both the arrays need to have enough space for the memcpy. This could be illustrated e.g. with this piece of code:
;
``` java
#include <string.h>
void f5()
{
  char p[40];
  const char *q = "Too short";
  memcpy(p, q, sizeof(p));
}
```
Compliant code could be
``` java
#include <string.h>
void f5()
{
  char p[40];
  const char *q = "Too short";
  const size_t smallersize = sizeof(p) < strlen(q)+1 ? sizeof(p) : strlen(q)+1;
  memcpy(p, q, smallersize);
}
```
Furthermore the current compliant code does not really solve the programmer's problem that the memcpy size should be determined inside the function. In the current code, the whole function is useless; memcpy can be directly called with the function arguments.
I do not know any good solution to this problem, but one way to have the function determine the size could be to wrap the array into a struct:
``` java
#include <string.h>
typedef char myarr[40]; 
struct wrapperStruct
{
  myarr wrappedArray;
};
void f6(wrapperStruct *p, const char *q) {
  const size_t smallersize = sizeof(*p) < strlen(q)+1 ? sizeof(*p) : strlen(q)+1;
  memcpy(p->wrappedArray, q, smallersize);
}
```
![](images/icons/contenttypes/comment_16.png) Posted by jussi.auvinen at Nov 13, 2015 04:44
\| \|
You are correct that our example is a bit;**too** contrived. I've updated the example based on your suggestion, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 17, 2015 11:03
\| \|
Some of the code snippets for compliant code contain library functions that are considered unsafe (strlen() and wcslen()).
    static const char str[] = "Hello world";
    static const wchar_t w_str[] = L"Hello world";
    void func(void) {
      char buffer[32];
      wchar_t w_buffer[32];
      memcpy(buffer, str, strlen(str) + 1);
      wmemcpy(w_buffer, w_str, wcslen(w_str) + 1);
    } 
I do understand that the point of this example here is the `wmemcpy` behavior, not the complex topic of safely copying C-style strings. I don't know how to provide a better example that doesn't go too deeply into string copy issues.As far as I know the safest way to copy C-style strings (in regards of buffer overrun and 0-termination) is to use `snprintf`. So I would solve that this way:
    static const char str[] = "Hello world";
    static const wchar_t w_str[] = L"Hello world";
    void func(void) {
      char buffer[32];
      wchar_t w_buffer[32];
      snprintf(buffer, sizeof(buffer), "%s", str); 
      swprintf(w_buffer, sizeof(w_buffer)/sizeof(wchar_t), L"%ls", w_str);
    } 
For the other "compliant" code snippet example:
    void f4() {
      char p[40];
      const char *q = "Too short";
      size_t n = sizeof(p) < strlen(q) + 1 ? sizeof(p) : strlen(q) + 1;
      memcpy(p, q, n);
    }
there is no safe solution replacing `strlen` with `strnlen`, unless the source string is declared differently:
    void f4() {
      char p[40];
      const char q[] = "Too short";
      size_t n = std::min(sizeof(p), sizeof(q));
      memcpy(p, q, n);
    }
But this is still having trouble with the 0-termination (see above). But I think the key is to declare `q` as array, not as pointer. Otherwise there is no safe way to solve that if the actual length of the source string is unknown.
![](images/icons/contenttypes/comment_16.png) Posted by peter.conrad at Feb 05, 2021 03:26
\| \|
The strlen() and wcslen() functions are not considered inherently unsafe in the CERT standards. They are only unsafe if you pass them an invalid pointer, or a pointer to a character array that might not be null-terminated. Doing such a thing actually vioates this rule (and perhaps other rules (like STR32-C).
Using snprintf or swprintf() has the same liabilities...they are safe only if you pass a safe value of n to those functions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 05, 2021 09:43
\| \|
Yes, I'm aware that there is no safe C-style string handling.
My concern is that the "compliant" code snippet is only compliant because the strings are defined like that. If someone uses this as a solution for the actual problem (wmemcpy and sizeof(pointer)), but with potentially invalid string pointers (parameter from somewhere), he is in trouble again.
![](images/icons/contenttypes/comment_16.png) Posted by peter.conrad at Feb 05, 2021 11:00
\| \|
In table "Pointer + Integer" the footnote for "mbrtowc()"; should be the same as for "mbtowc()" namely 2 (and not 1). Both write a single wide character and the size argument is the "limit on the number of bytes in s that can be examined" where "s" is the  (pointer to the multibyte character) input buffer. Could this be corrected in the above table? (see <https://en.cppreference.com/w/c/string/multibyte/mbrtowc>)
![](images/icons/contenttypes/comment_16.png) Posted by maeder at Jan 10, 2023 03:56
\| \|
Fixed, thanks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 10, 2023 08:35
\|
