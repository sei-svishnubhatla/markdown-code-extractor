Evaluating a pointer—including dereferencing the pointer, using it as an operand of an arithmetic operation, type casting it, and using it as the right-hand side of an assignment—into memory that has been deallocated by a memory management function is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Pointers to memory that has been deallocated are called *dangling pointers*. Accessing a dangling pointer can result in exploitable [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
According to the C Standard, using the value of a pointer that refers to space deallocated by a call to the `free()` or `realloc()` function is undefined behavior. (See [undefined behavior 177](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).)
Reading a pointer to deallocated memory is undefined behavior because the pointer value is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) and might be a [trap representation](BB.-Definitions_87152273.html#BB.Definitions-traprepresentation). Fetching a trap representation might perform a hardware trap (but is not required to).
It is at the memory manager's discretion when to reallocate or recycle the freed memory. When memory is freed, all pointers into it become invalid, and its contents might either be returned to the operating system, making the freed space inaccessible, or remain intact and accessible. As a result, the data at the freed location can appear to be valid but change unexpectedly. Consequently, memory must not be written to or read from once it is freed.
## Noncompliant Code Example
This example from Brian Kernighan and Dennis Ritchie \[[Kernighan 1988](AA.-Bibliography_87152170.html#AA.Bibliography-Kernighan88)\] shows both the incorrect and correct techniques for freeing the memory associated with a linked list. In their (intentionally) incorrect example, `p` is freed before `p->next` is executed, so that `p->next` reads memory that has already been freed.
``` c
#include <stdlib.h>
struct node {
  int value;
  struct node *next;
};
void free_list(struct node *head) {
  for (struct node *p = head; p != NULL; p = p->next) {
    free(p);
  }
}
```
## Compliant Solution
Kernighan and Ritchie correct this error by storing a reference to `p->next`  in `q` before freeing `p`:
``` c
#include <stdlib.h>
struct node {
  int value;
  struct node *next;
};
void free_list(struct node *head) {
  struct node *q;
  for (struct node *p = head; p != NULL; p = q) {
    q = p->next;
    free(p);
  }
}
```
## Noncompliant Code Example
In this noncompliant code example, `buf` is written to after it has been freed. Write-after-free vulnerabilities can be [exploited](BB.-Definitions_87152273.html#BB.Definitions-exploit) to run arbitrary code with the permissions of the vulnerable process. Typically, allocations and frees are far removed, making it difficult to recognize and diagnose these problems.
``` c
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]) {
  char *return_val = 0;
  const size_t bufsize = strlen(argv[0]) + 1;
  char *buf = (char *)malloc(bufsize);
  if (!buf) {
    return EXIT_FAILURE;
  }
  /* ... */
  free(buf);
  /* ... */
  strcpy(buf, argv[0]);
  /* ... */
  return EXIT_SUCCESS;
}
```
## Compliant Solution
In this compliant solution, the memory is freed after its final use:
``` c
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]) {
  char *return_val = 0;
  const size_t bufsize = strlen(argv[0]) + 1;
  char *buf = (char *)malloc(bufsize);
  if (!buf) {
    return EXIT_FAILURE;
  }
  /* ... */
  strcpy(buf, argv[0]);
  /* ... */
  free(buf);
  return EXIT_SUCCESS;
}
```
## Noncompliant Code Example
In this noncompliant example, `realloc()` may free `c_str1` when it returns a null pointer, resulting in `c_str1` being freed twice.  The C Standards Committee's proposed response to [Defect Report #400](http://www.open-std.org/jtc1/sc22/wg14/www/docs/dr_400.htm) makes it implementation-defined whether or not the old object is deallocated when `size` is zero and memory for the new object is not allocated. The current implementation of `realloc()` in the GNU C Library and Microsoft Visual Studio's Runtime Library will free `c_str1` and return a null pointer for zero byte allocations.  Freeing a pointer twice can result in a potentially exploitable vulnerability commonly referred to as a *double-free vulnerability* \[[Seacord 2013b](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\].
``` c
#include <stdlib.h>
void f(char *c_str1, size_t size) {
  char *c_str2 = (char *)realloc(c_str1, size);
  if (c_str2 == NULL) {
    free(c_str1);
  }
}
```
## Compliant Solution
This compliant solution does not pass a size argument of zero to the `realloc()` function, eliminating the possibility of `c_str1` being freed twice:
``` c
#include <stdlib.h>
void f(char *c_str1, size_t size) {
  if (size != 0) {
    char *c_str2 = (char *)realloc(c_str1, size); 
    if (c_str2 == NULL) {
      free(c_str1); 
    }
  }
  else {
    free(c_str1);
  }
}
```
If the intent of calling `f()` is to reduce the size of the object, then doing nothing when the size is zero would be unexpected; instead, this compliant solution frees the object.
## Noncompliant Code Example
In this noncompliant example ([CVE-2009-1364](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1364)) from `libwmf` version 0.2.8.4, the return value of `gdRealloc` (a simple wrapper around `realloc()` that reallocates space pointed to by `im->clip->list`) is set to `more`. However, the value of `im->clip->list` is used directly afterwards in the code, and the C Standard specifies that if `realloc()` moves the area pointed to, then the original block is freed. An attacker can then execute arbitrary code by forcing a reallocation (with a sufficient `im->clip->count`) and accessing freed memory \[[xorl 2009](http://xorl.wordpress.com/2009/05/05/cve-2009-1364-libwmf-pointer-use-after-free/)\].
``` c
void gdClipSetAdd(gdImagePtr im, gdClipRectanglePtr rect) {
  gdClipRectanglePtr more;
  if (im->clip == 0) {
   /* ... */
  }
  if (im->clip->count == im->clip->max) {
    more = gdRealloc (im->clip->list,(im->clip->max + 8) *
                      sizeof (gdClipRectangle));
    /*
     * If the realloc fails, then we have not lost the
     * im->clip->list value.
     */
    if (more == 0) return; 
    im->clip->max += 8;
  }
  im->clip->list[im->clip->count] = *rect;
  im->clip->count++;
}
```
## Compliant Solution
This compliant solution simply reassigns `im->clip->list` to the value of `more` after the call to `realloc()`:
``` c
void gdClipSetAdd(gdImagePtr im, gdClipRectanglePtr rect) {
  gdClipRectanglePtr more;
  if (im->clip == 0) {
    /* ... */
  }
  if (im->clip->count == im->clip->max) {
    more = gdRealloc (im->clip->list,(im->clip->max + 8) *
                      sizeof (gdClipRectangle));
    if (more == 0) return;
    im->clip->max += 8;
    im->clip->list = more;
  }
  im->clip->list[im->clip->count] = *rect;
  im->clip->count++;
}
```
## Risk Assessment
Reading memory that has already been freed can lead to abnormal program termination and denial-of-service attacks. Writing memory that has already been freed can additionally lead to the execution of arbitrary code with the permissions of the vulnerable process. 
Freeing memory multiple times has similar consequences to accessing memory after it is freed. Reading a pointer to deallocated memory is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because the pointer value is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) and might be a [trap representation](BB.-Definitions_87152273.html#BB.Definitions-traprepresentation). When reading from or writing to freed memory does not cause a trap, it may corrupt the underlying data structures that manage the heap in a manner that can be exploited to execute arbitrary code. Alternatively, writing to memory after it has been freed might modify memory that has been reallocated.
Programmers should be wary when freeing memory in a loop or conditional statement; if coded incorrectly, these constructs can lead to double-free vulnerabilities. It is also a common error to misuse the `realloc()` function in a manner that results in double-free vulnerabilities. (See [MEM04-C. Beware of zero-length allocations](MEM04-C_%20Beware%20of%20zero-length%20allocations).)

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM30-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | dangling_pointer_use | SupportedAstrée reports all accesses to freed allocated memory. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM30 | Detects memory accesses after its deallocation and double memory deallocations |
| CodeSonar | 8.3p0 | ALLOC.UAF | Use after free |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | USE_AFTER_FREE | Can detect the specific instances where memory is deallocated more than once or read/written;to the target of a freed pointer |
| Cppcheck | ;2.15 | doubleFreedeallocret
deallocuse |  |
| Cppcheck Premium | 24.11.0 | doubleFreedeallocret
deallocuse |  |
| Helix QAC | 2024.4 | DF4866, DF4867, DF4868, DF4871, DF4872, DF4873C++3339, C++4303, C++4304 |  |
| Klocwork | 2024.4 | UFM.DEREF.MIGHTUFM.DEREF.MUST
UFM.FFM.MIGHT
UFM.FFM.MUST
UFM.RETURN.MIGHT
UFM.RETURN.MUST
UFM.USE.MIGHT
UFM.USE.MUST |  |
| LDRA tool suite | 9.7.1 | 51 D, 484 S, 112 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM30-a | Do not use resources that have been freed |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 449, 2434 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule MEM30-C | Checks for:Accessing previously freed pointerFreeing previously freed pointerRule partially covered. |
| PVS-Studio | 7.35 | V586, V774 |  |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | dangling_pointer | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
[VU#623332](http://www.kb.cert.org/vuls/id/623332) describes a double-free vulnerability in the MIT Kerberos 5 function [krb5_recvauth()](http://web.mit.edu/kerberos/www/advisories/MITKRB5-SA-2005-003-recvauth.txt). 
Search for [vulnerabilities](https://www.securecoding.cert.org/confluence/display/c/BB.+Definitions#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | MEM01-C. Store a new value in pointers immediately after free() | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | MEM50-CPP. Do not access freed memory | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Dangling References to Stack Frames [DCM] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Dangling Reference to Heap [XYK] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Accessing freed memory [accfree] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Freeing memory multiple times [dblfree] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 18.6 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-416, Use After Free | 2017-07-07: CERT: Exact |
| CWE 2.11 | CWE-672 | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-672 and MEM30-C
Intersection( MEM30-C, FIO46-C) = Ø CWE-672 = Union( MEM30-C, list) where list =
-   Use of a resource, other than memory after it has been released (eg: reusing a closed file, or expired mutex)
### CWE-666 and MEM30-C
Intersection( MEM30-C, FIO46-C) = Ø
CWE-672 = Subset( CWE-666)
### CWE-758 and MEM30-C
CWE-758 = Union( MEM30-C, list) where list =
-   Undefined behavior that is not covered by use-after-free errors
### CWE-415 and MEM30-C
MEM30-C = Union( CWE-456, list) where list =
-   Dereference of a pointer after freeing it (besides passing it to free() a second time)
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 7.24.3, "Memory Management Functions" |
| [Kernighan 1988] | Section 7.8.5, "Storage Management" |
| [OWASP Freed Memory] |  |
| [MIT 2005] |  |
| [Seacord 2013b] | Chapter 4, "Dynamic Memory Management" |
| [Viega 2005] | Section 5.2.19, "Using Freed Memory" |
| [VU#623332] |  |
| [xorl 2009] | CVE-2009-1364: LibWMF Pointer Use after free() |

------------------------------------------------------------------------
[](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152152)
## Comments:

|  |
| ----|
| It may worth noting that there are other means of "free"ing memory other than free().
For example, memory allocated with alloca() is freed automatically at the end of the block. And static memory is freed with then module that contains the static definition if unloaded from memory (a big deal with programs that dynamically load/unload shared objects/libraries).
In all of these cases, referencing (R or W) the deallocated memory is an error,; regardless of whether it works or not.
                                        Posted by wlf@cert.org at Nov 01, 2006 08:54
                                     |
| Something else to look for that falls within these lines is being careful about passing already free()'d pointers to realloc() and calling functions that call free() twice with the same arguments, i.e. double fclose()
                                        Posted by jf at Aug 20, 2007 09:16
                                     |
| In the first Compliant Example, I'd make it a point to add
head = 0;

to the code after the loop - otherwise this variable is left with a pointer to invalid memory (this may not be necessary depending on the surrounding code).
This is just highly defensive programming that will provoke an earlier assertion failure than otherwise.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 00:42
\| \|
Good point.; This is necessary to comply with [MEM01-C. Store a new value in pointers immediately after free()](MEM01-C_%20Store%20a%20new%20value%20in%20pointers%20immediately%20after%20free__).  It's fixed now.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 14, 2008 08:22
\| \|
Does the book set head to zero?; (Answer: no - see p167).  If not, you have to do more major surgery on this.  Either use an example that is not claiming to come from K&R or live with the fact that our preceptors did not follow every one of these guidelines.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Apr 20, 2008 01:07
\| \|
I've added a rather contrived example to point out usage of automatic storage, and a bit of wording related to object lifetime.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 08, 2013 10:30
\|
