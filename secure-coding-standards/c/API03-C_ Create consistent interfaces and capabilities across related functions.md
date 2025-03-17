Related functions, such as those that make up a library, should provide consistent and usable interfaces. Ralph Waldo Emerson said, "A foolish consistency is the hobgoblin of little minds," but inconsistencies in functional interfaces or behavior can lead to erroneous use, so we understand this to be a "wise consistency." One aspect of providing a consistent interface is to provide a consistent and usable error-checking mechanism. For more information, see [API04-C. Provide a consistent and usable error-checking mechanism](API04-C_%20Provide%20a%20consistent%20and%20usable%20error-checking%20mechanism).
## Noncompliant Code Example (Interface)
It is not necessary to go beyond the standard C library to find examples of inconsistent interfaces: the standard library is a fusion of multiple libraries with various styles and levels of rigor. For example, the `fputs()` defined in the C Standard, subclause 7.21.7.4, is closely related to the `fprintf()` defined in subclause 7.21.6.1. However, `fputs()`'s file handle is at the end, and `fprintf()`'s is at the beginning, as shown by their function declarations:
``` c
int fputs(const char * restrict s, FILE * restrict stream);
int fprintf(FILE * restrict stream, const char * restrict format, ...);
```
The argument order can be easily rearranged using macros; for example:
``` c
#include <stdio.h>
#define fputs(X,Y) fputs(Y,X)
```
However, according to subclause 7.1.3 of the C Standard, the behavior of a program that defines a symbol, including a macro, with the same name as that of a standard library function, type, macro, or other reserved identifier is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
Using inconsistent interfaces makes the code difficult to read, for example, by causing confusion when moving between code that follows this convention and code that does not. In effect, it becomes impossible to modify an interface once that interface has been broadly adopted. Consequently, it is important to get the interface design right the first time.
## Compliant Solution (Interface)
The POSIX threads library \[[Butenhof 1997](AA.-Bibliography_87152170.html#AA.Bibliography-Butenhof97)\] defines an interface that is both consistent and fits in with established conventions from the rest of the POSIX library. For example, all initialization functions follow the same consistent pattern of the first argument being a pointer to the object to initialize with the subsequent arguments, if any, optionally providing additional attributes for the initialization:
``` c
/* Initialization of pthread attribute objects */
int pthread_condattr_init(pthread_condattr_t *);
int pthread_mutexattr_init(pthread_mutexattr_t *);
int pthread_rwlockattr_init(pthread_rwlockattr_t *);
...
/* Initialization of pthread objects using attributes */
int pthread_cond_init(pthread_cond_t * restrict, const pthread_condattr_t * restrict);
int pthread_mutex_init(pthread_mutex_t * restrict, const pthread_mutexattr_t * restrict);
int pthread_rwlock_init(pthread_rwlock_t * restrict, const pthread_rwlockattr_t * restrict);
...
```
Function arguments that refer to objects that are not modified are declared `const`. Because the object pointed to by the first argument is modified by the function, it is not `const`. For functions that implement a data abstraction, it is reasonable to define the handle for the data abstraction as the initial parameter. (See [DCL12-C. Implement abstract data types using opaque types](DCL12-C_%20Implement%20abstract%20data%20types%20using%20opaque%20types).) Finally, initialization functions that accept a pointer to an attribute object allow it to be `NULL` as an indication that a reasonable default should be used.
## Noncompliant Code Example (Behavior)
The shared folder and file copy functions in the VMware virtual infrastructure (VIX) API are inconsistent in the set of characters they allow in folder names. As a result, you can create a shared folder that you subsequently cannot use in a file copy function such as `VixVM_CopyFileFromHostToGuest()`.
## Compliant Solution (Behavior)
Try to be consistent in the behavior of related functions that perform operations on common objects so that an object created or modified by one function can be successfully processed by a downstream invocation of a related function.
## Risk Assessment
Failure to maintain consistency in interfaces and capabilities across functions can result in type errors in the program.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API03-C | Medium | Unlikely | Medium | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+API04-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC 9945:2003 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC 23360-1:2006 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24731-1 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24731-2 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 21.3 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Directive 4.12 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [Burch 2006] |  |
| [CERT 2006c] |  |
| [Miller 1999] |  |
| [Seacord 2013] | Chapter 2, "Strings" |
| [VMware 2007] | VIX API Version 1.1.1 (for Workstation 6.0.1) Release Notes |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152290) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152244)
## Comments:

|  |
| ----|
| Many of the managed string library declarations appear to suffer from a const-correctness problem that is perpetuated in the compliant solution above. The library defines the type string_m in the header <string.m.h> as follows:
typedef void *string_m;

As discussed in [PRE03-C. Prefer typedefs to defines for encoding types](/confluence/pages/createpage.action?spaceKey=c&title=PRE03-C.+Prefer+typedefs+to+defines+for+encoding+types), when using a `typedef`, declaring an object of pointer type `const` (as in `const string_m s;`) declares the pointer (`s`) itself to be const, not the object the pointer points to. Thus it is possible to modify the object through such a pointer without a cast. I.e., this will compile without a warning:
``` java
void foo(const string_m s) {
    cstrcpy_s(s, "foobar");
}
```
While this problem doesn't necessarily diminish the value of the recommendation it seems that it would be an improvement to find a different example of a consistent API, one that doesn't suffer from a design problem.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 06, 2010 13:28
\| \|
Your complaint about the managed string library is truly a design flaw. 'const string_m' forbids you from changing the pointer, but does not forbid you from changing the pointed-to memory contents. A suitable fix would be to add something like:
``` java
typedef const struct string_mx *string_m_const;
```
IIRC the C++ STL does this with iterators: they have const_iterators which are iterators that prevent you from changing their pointed-to contents (even though they allow you to make them point elsewhere.). But we can't discuss C++ designs in this section :/
However, at this point I can weasel, and claim that this design flaw is irrelevant to the rule. You'll note that the API examples in the rule are valid; they do not change the string_m's contents, and when we fix the string_m library we don't need to change the examples. \>![](images/icons/emoticons/biggrin.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 07, 2010 14:54
\| \|
I agree that for the purposes of this rule the Managed String API is fine. Still, there are other examples of consistent APIs that do not suffer from design problems and aren&#39;t subject to violations of other secure rules (the Pthreads APIs come to mind – see below).
In general, I feel that every Compliant Solution should comply not just with the rule under which it&#39;s listed but should also avoid violating any other rules and recommendations in this document. I.e., it should be a shining example demonstrating how this document as a whole is intended to applied in practice ![](images/icons/emoticons/smile.svg) (Otherwise, a novice engineer applying the advice given in one rule might easily be lead to inadvertently introduce a violation of another rule.)
``` java
/* initialization of Pthread attribute objects */
int pthread_condattr_init(pthread_condattr_t*);
int pthread_mutexattr_init(pthread_mutexattr_t*);
int pthread_rwlockattr_init(pthread_rwlockattr_t*);
...
/* initialization of Pthread objects using attributes */
int pthread_cond_init(pthread_cond_t* restrict, const pthread_condattr_t* restrict);
int pthread_mutex_init(pthread_mutex_t* restrict, const pthread_mutexattr_t* restrict);
int pthread_rwlock_init(pthread_rwlock_t* restrict, const pthread_rwlockattr_t* restrict);
...
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 07, 2010 15:45
\| \|
> In general, I feel that every Compliant Solution should comply not just with the rule under which it's listed but should also avoid violating any other rules and recommendations in this document. I.e., it should be a shining example demonstrating how this document as a whole is intended to applied in practice

On this point, we agree. I still hold that the string_m example does qualify as it is illustrated in the code, and the design flaw is irrelevant as far as this rule is concerned. But if you would like to replace the string_m CS with your pthreads example, feel free to do so.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 07, 2010 16:12
\|
