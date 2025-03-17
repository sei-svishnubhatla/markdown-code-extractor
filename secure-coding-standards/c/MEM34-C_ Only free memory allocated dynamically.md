The C Standard, Annex J (184) \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states that the behavior of a program is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when
> The pointer argument to the `free` or `realloc` function does not match a pointer earlier returned by a memory management function, or the space has been deallocated by a call to `free` or `realloc`.

See also [undefined behavior 184](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_14).
Freeing memory that is not allocated dynamically can result in heap corruption and other serious errors. Do not call `free()` on a pointer other than one returned by a standard memory allocation function, such as `malloc()`, `calloc()`, `realloc()`, or `aligned_alloc()`.
A similar situation arises when `realloc()` is supplied a pointer to non-dynamically allocated memory. The `realloc()` function is used to resize a block of dynamic memory. If `realloc()` is supplied a pointer to memory not allocated by a standard memory allocation function, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). One consequence is that the program may [terminate abnormally](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).
This rule does not apply to null pointers. The C Standard guarantees that if `free()` is passed a null pointer, no action occurs.
## Noncompliant Code Example
This noncompliant code example sets `c_str` to reference either dynamically allocated memory or a statically allocated string literal depending on the value of `argc`. In either case, `c_str` is passed as an argument to `free()`. If anything other than dynamically allocated memory is referenced by `c_str`, the call to `free(c_str)` is erroneous.
``` c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
enum { MAX_ALLOCATION = 1000 };
int main(int argc, const char *argv[]) {
  char *c_str = NULL;
  size_t len;
  if (argc == 2) {
    len = strlen(argv[1]) + 1;
    if (len > MAX_ALLOCATION) {
      /* Handle error */
    }
    c_str = (char *)malloc(len);
    if (c_str == NULL) {
      /* Handle error */
    }
    strcpy(c_str, argv[1]);
  } else {
    c_str = "usage: $>a.exe [string]";
    printf("%s\n", c_str);
  }
  free(c_str);
  return 0;
}
```
## Compliant Solution
This compliant solution eliminates the possibility of `c_str` referencing memory that is not allocated dynamically when passed to `free()`:
``` c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
enum { MAX_ALLOCATION = 1000 };
int main(int argc, const char *argv[]) {
  char *c_str = NULL;
  size_t len;
  if (argc == 2) {
    len = strlen(argv[1]) + 1;
    if (len > MAX_ALLOCATION) {
      /* Handle error */
    }
    c_str = (char *)malloc(len);
    if (c_str == NULL) {
      /* Handle error */
    }
    strcpy(c_str, argv[1]);
  } else {
    printf("%s\n", "usage: $>a.exe [string]");
    return EXIT_FAILURE;
  }
  free(c_str);
  return 0;
}
```
## Noncompliant Code Example (`realloc()`)
In this noncompliant example, the pointer parameter to `realloc()`, `buf`, does not refer to dynamically allocated memory:
``` c
#include <stdlib.h>
enum { BUFSIZE = 256 };
void f(void) {
  char buf[BUFSIZE];
  char *p = (char *)realloc(buf, 2 * BUFSIZE);
  if (p == NULL) {
    /* Handle error */
  }
}
```
## Compliant Solution (`realloc()`)
In this compliant solution, `buf` refers to dynamically allocated memory:
``` c
#include <stdlib.h>
enum { BUFSIZE = 256 };
void f(void) {
  char *buf = (char *)malloc(BUFSIZE * sizeof(char));
  char *p = (char *)realloc(buf, 2 * BUFSIZE);
  if (p == NULL) {
    /* Handle error */
  }
}
```
Note that `realloc()` will behave properly even if `malloc()` failed, because when given a null pointer, `realloc()` behaves like a call to `malloc()`.
## Risk Assessment
The consequences of this error depend on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation), but they range from nothing to arbitrary code execution if that memory is reused by `malloc()`. 

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM34-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | invalid-free | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM34 | Can detect memory deallocations for stack objects |
| Clang | 3.9 | clang-analyzer-unix.Malloc | Checked by clang-tidy; can detect some instances of this rule, but does not detect all |
| CodeSonar | 8.3p0 | ALLOC.TM | Type Mismatch |
| Compass/ROSE |  |  | Can detect some violations of this rule |
| Coverity | 2017.07 | BAD_FREE | Identifies calls to free() where the argument is a pointer to a function or an array. It also detects the cases where free() is used on an address-of expression, which can never be heap allocated. Coverity Prevent cannot discover all
violations of this rule, so further verification is necessary |
| Cppcheck | ;2.15 | autovarInvalidDeallocationmismatchAllocDealloc |  |
| Cppcheck Premium | 24.11.0 | autovarInvalidDeallocationmismatchAllocDealloc |  |
| Helix QAC | 2024.4 | DF2721, DF2722, DF2723 |  |
| Klocwork | 2024.4 | FNH.MIGHTFNH.MUST |  |
| LDRA tool suite | 9.7.1 | 407 S, 483 S, 644 S, 645 S, 125 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM34-a | Do not free resources using invalid pointers |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 424, 673 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule MEM34-C | Checks for:Invalid free of pointerInvalid reallocation of pointerRule fully covered. |
| PVS-Studio | 7.35 | V585, V726 |  |
| RuleChecker | 24.04 | invalid-free | Partially checked |
| TrustInSoft Analyzer | 1.38 | unclassified ("free expects a free-able address") | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
[CVE-2015-0240](https://securityblog.redhat.com/2015/02/23/samba-vulnerability-cve-2015-0240/) describes a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in which an uninitialized pointer is passed to `TALLOC_FREE()`, which is a Samba-specific memory deallocation macro that wraps the `talloc_free()` function. The implementation of  `talloc_free()` would access the uninitialized pointer, resulting in a remote [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit).
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | MEM31-C. Free dynamically allocated memory when no longer needed | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | MEM51-CPP. Properly deallocate dynamically allocated resources | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Reallocating or freeing memory that was not dynamically allocated [xfree] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-590, Free of Memory Not on the Heap | 2017-07-10: CERT: Exact |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause J.2, "Undefined Behavior" |
| [Seacord 2013b] | Chapter 4, "Dynamic Memory Management" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152183) [](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152128)
## Comments:

|  |
| ----|
| Is it fair to grumble that copying arguments to main() is done far more often than is actually necessary?; I've certainly seen far too many programs that copy arguments into fixed size buffers (without checking lengths, of course).  My experience is that it is very seldom necessary to copy command-line arguments.
                                        Posted by jonathan.leffler@gmail.com at Apr 20, 2008 01:23
                                     |
| Sure.  Combined with some discussion on how to handle arguments correctly might even make a reasonable recommendation.
                                        Posted by rcs at Apr 21, 2008 04:58
                                     |

