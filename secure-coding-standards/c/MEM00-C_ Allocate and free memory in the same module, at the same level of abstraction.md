Dynamic memory management is a common source of programming flaws that can lead to security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Poor memory management can lead to security issues, such as heap-buffer overflows, dangling pointers, and double-free issues \[[Seacord 2013](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\]. From the programmer's perspective, memory management involves allocating memory, reading and writing to memory, and deallocating memory.
Allocating and freeing memory in different modules and levels of abstraction may make it difficult to determine when and if a block of memory has been freed, leading to programming defects, such as memory leaks, double-free [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), accessing freed memory, or writing to freed or unallocated memory.
To avoid these situations, memory should be allocated and freed at the same level of abstraction and, ideally, in the same code module. This includes the use of the following memory allocation and deallocation functions described in subclause 7.23.3 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]:
``` java
void *malloc(size_t size);
void *calloc(size_t nmemb, size_t size);
void *realloc(void *ptr, size_t size);
void *aligned_alloc(size_t alignment, size_t size);
void free(void *ptr);
```
Failing to follow this recommendation has led to real-world vulnerabilities. For example, freeing memory in different modules resulted in a vulnerability in MIT Kerberos 5 \[[MIT 2004](AA.-Bibliography_87152170.html#AA.Bibliography-MIT04)\]. The MIT Kerberos 5 code in this case contained error-handling logic, which freed memory allocated by the ASN.1 decoders if pointers to the allocated memory were non-null. However, if a detectable error occurred, the ASN.1 decoders freed the memory that they had allocated. When some library functions received errors from the ASN.1 decoders, they also attempted to free the same memory, resulting in a double-free vulnerability.
## Noncompliant Code Example
This noncompliant code example shows a double-free vulnerability resulting from memory being allocated and freed at differing levels of abstraction. In this example, memory for the `list` array is allocated in the `process_list()` function. The array is then passed to the `verify_size()` function that performs error checking on the size of the list. If the size of the list is below a minimum size, the memory allocated to the list is freed, and the function returns to the caller. The calling function then frees this same memory again, resulting in a double-free and potentially exploitable vulnerability.
``` c
enum { MIN_SIZE_ALLOWED = 32 };
int verify_size(char *list, size_t size) {
  if (size < MIN_SIZE_ALLOWED) {
    /* Handle error condition */
    free(list);
    return -1;
  }
  return 0;
}
void process_list(size_t number) {
  char *list = (char *)malloc(number);
  if (list == NULL) {
    /* Handle allocation error */
  }
  if (verify_size(list, number) == -1) {
      free(list);
      return;
  }
  /* Continue processing list */
  free(list);
}
```
The call to free memory in the `verify_size()` function takes place in a subroutine of the `process_list()` function, at a different level of abstraction from the allocation, resulting in a violation of this recommendation. The memory deallocation also occurs in error-handling code, which is frequently not as well tested as "green paths" through the code.
## Compliant Solution
To correct this problem, the error-handling code in `verify_size()` is modified so that it no longer frees `list`. This change ensures that `list` is freed only once, at the same level of abstraction, in the `process_list()` function.
``` c
enum { MIN_SIZE_ALLOWED = 32 };
int verify_size(const char *list, size_t size) {
  if (size < MIN_SIZE_ALLOWED) {
    /* Handle error condition */
    return -1;
  }
  return 0;
}
void process_list(size_t number) {
  char *list = (char *)malloc(number);
  if (list == NULL) {
    /* Handle allocation error */
  }
  if (verify_size(list, number) == -1) {
      free(list);
      return;
  }
  /* Continue processing list */
  free(list);
}
```
## Risk Assessment
The mismanagement of memory can lead to freeing memory multiple times or writing to already freed memory. Both of these coding errors can result in an attacker executing arbitrary code with the permissions of the vulnerable process. Memory management errors can also lead to resource depletion and [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM00-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | ALLOC.DFALLOC.LEAK
 | Double freeLeak |
| Compass/ROSE |  |  | Could detect possible violations by reporting any function that has malloc() or free() but not both. This would catch some false positives, as there would be no way to tell if malloc() and free() are at the same level of abstraction if they are in different functions |
| Coverity | 6.5 | RESOURCE_LEAK | Fully implemented |
| Klocwork | 2024.4 | FREE.INCONSISTENTUFM.FFM.MIGHT
UFM.FFM.MUST
UFM.DEREF.MIGHT
UFM.DEREF.MUST
UFM.RETURN.MIGHT
UFM.RETURN.MUST
UFM.USE.MIGHT
UFM.USE.MUST
MLK.MIGHT
MLK.MUST
MLK.RET.MIGHT
MLK.RET.MUST
FNH.MIGHT
FNH.MUST
FUM.GEN.MIGHT
FUM.GEN.MUST
RH.LEAK |  |
| LDRA tool suite | 9.7.1 | 50 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM00-aCERT_C-MEM00-b
CERT_C-MEM00-c
CERT_C-MEM00-d
CERT_C-MEM00-e | Do not allocate memory and expect that someone else will deallocate it laterDo not allocate memory and expect that someone else will deallocate it later
Do not allocate memory and expect that someone else will deallocate it later
Do not use resources that have been freed
Ensure resources are freed |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 449, 2434 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM00-C | Checks for:Invalid free of pointerDeallocation of previously deallocated pointerUse of previously freed pointerRec. partially covered. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM11-CPP. Allocate and free memory in the same module, at the same level of abstraction |
| ISO/IEC TR 24772:2013 | Memory Leak [XYL] |
| MITRE CWE | CWE-415, Double freeCWE-416, Use after free |

## Bibliography

|  |  |
| ----|----|
| [MIT 2004] |  |
| [Plakosh 2005] |  |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |

------------------------------------------------------------------------
[](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](../c/MEM01-C_%20Store%20a%20new%20value%20in%20pointers%20immediately%20after%20free__)
## Comments:

|  |
| ----|
| originally posted by by pete filandro at Aug 01, 2007 21:08 
One method of allocation recommended by the rabble on news:comp.lang.c is :
#include <stdlib.h>
ptr = malloc(NMEMB * sizeof *ptr);
That, plus the related expression, (ptr = malloc(sizeof *ptr)), and also:
ptr = malloc(string_length + 1);
can take care of most malloc call situations.
                                        Posted by rcs at Aug 07, 2007 14:11
                                     |
| The narratives seem to assume that "Handle Error" does not include "return".; If that also applies to "Handle Allocation Error", then both examples (NCCE and CS) are vulnerable to trying to free NULL.  A quick check of "man 3 free" says that nothing happens, but I could swear I've seen that cause a crash.  Maybe that's implementation-defined, in which case it's still worth a mention.
                                        Posted by davearonson at Jan 10, 2008 16:10
                                     |
| Pretty close. One point of information is that calling free on a null pointer is perfectly kosher; it does a noop.
The first /* Handle Allocation Error */, which operates if malloc() fails is therefore free to do anything, including return, goto, longjmp, exit() ..., or none of these. If it does not exit, the free operates on a null pointer, which does nothing.
The second /* Handle Error /, as well as the / Continue Processing */ are both constrained from any non-local exits. So one cannot do return, goto, longjmp, exit()..., without leaking the allocated memory.
                                        Posted by svoboda at Feb 08, 2008 16:15
                                     |
| Some pre-C89 compilers (strictly, the libraries) objected to freeing null pointers (usually by crashing).
All compilers/libraries compliant with C89 or later accept free(0) as a no-op.
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 23:27
                                     |
| The realpath() function (defined in stdlib.h) takes a pathname and returns a canonicalized pathname. The point here is that it can (depending on the parameters) return its own malloc'ed result string, which must then be freed by the caller. Many other standard library functions that must return a new string have the option to allocate it and expect the user to free the result string when done with it. Doesn't this design pattern violate this recommendation?
C++ can sidestep this issue with RAII. A function can return an object that malloc's a string upon creation and free's it upon destruction.
I vaguely remember reading somewhere that the main reason Java implemented garbage collection was this particular problem; how do you handle malloc'ed data returned by a library function? and how do you know WHEN you are responsible for free()ing data returned by a library function?
                                        Posted by svoboda at Apr 10, 2008 09:33
                                     |
| There should be no realpath() function declaration in <stdlib.h>.
                                        Posted by dagwyn at Apr 16, 2008 21:57
                                     |
| This rule cannot be followed when dynamic allocation is used for linked data structures, which is probably its most important application.; A better rule is "have only one node freeing function and ensure that it maintains the integriry of the data structure."  It is also wise to use "handles" (volatile pointer to pointer to allocated chunk) that get NULLified by the freeing function.  Generally speaking, a lot of thought should go into the design.
                                        Posted by dagwyn at Apr 16, 2008 22:01
                                     |
| Under Standard C, there would be no realpath() in <stdlib.h>.; Under POSIX, there would.
                                        Posted by jonathan.leffler@gmail.com at Apr 19, 2008 23:26
                                     |
| Doesn't this design pattern violate this recommendation?
Yes, but as long as the responsibility for which function is responsible for freeing the allocated space is properly documented and then acted on, it is legitimate.  I would suspect that one reason this is a recommendation rather than a rule is issues such as this.
Also, according to the POSIX description of realpath():
    If resolved_name is a null pointer, the behavior of realpath() is implementation-defined.
I take it that the implementation you are familiar with documents the implementation-defined behaviour as "realpath() will allocate enough space for the path via malloc() and the caller is responsible for freeing the allocated space".
                                        Posted by jonathan.leffler@gmail.com at Apr 19, 2008 23:32
                                     |
| Why volatile?
                                        Posted by rcs at Apr 21, 2008 05:11
                                     |
| I disagree with the ROSE suggestion for this rule, what if a program has wrappers for malloc() and free()?  The wrappers may be called within the same function, but each wrapper only calls malloc() OR free() accordingly.
                                        Posted by avolkovi at Jun 17, 2008 09:40
                                     |
| Alex and I discussed this today. I have removed the 'rose-possible' tag, but am not convinced that writing a rose rule is worthless...what do others think? Here is the conclusion that Alex and I came to:
The tool Compass / ROSE does not currently detect violations of this recommendation, but it could. One merely has to search a function's local block for a call to either malloc() or free(), but not both. A function could have multiple calls to free() for each malloc() call, as the compliant solution illustrates. This would catch cases such as the non-compliant example above. However, there is a common coding style where malloc() is called inside an init function, and free() is called inside a destroy function, which mimicks C++ constructors and destructors. ROSE would flag these as false positives, and there is no good heuristic to train ROSE to identify and accept these patterns. 
                                        Posted by svoboda at Jun 17, 2008 12:22
                                     |
| Currently marked as rose-nonapplicable. How do LDRA and Fortify catch violations? How do they avoid false positives on malloc in an init function or free in a destroy function?
This might be a good argument to have ROSE flag such rules, but only if in a 'sensitive' mode where false positives are less severe.
                                        Posted by svoboda at Jul 23, 2008 15:56
                                     |
| Added back rose algo section, marked as 'rose-false-positive'.
                                        Posted by svoboda at Jul 23, 2008 16:15
                                     |
| The advice here should apply equally well to other kinds of resources besides memory, including file pointers and descriptors, threads, processes, and synchronization primitives, etc. Would it make sense to generalize this guideline to encompass all types of resources or should there be a separate guideline for resources other than memory?
                                        Posted by martinsebor at Mar 06, 2010 16:48
                                     |
| Agreed. (I think we do have a rule about closing open files, in the FIO section somewhere.)
                                        Posted by svoboda at Mar 09, 2010 09:58
                                     |
| verify_list() in the description should probably be verify_size().
                                        Posted by dmohindr at Jun 17, 2010 20:30
                                     |
| fixed
                                        Posted by svoboda at Jun 18, 2010 15:43
                                     |
| I removed a sentence (which looks to me redundant) from the beginning paragraph.Revert to the previous version if it lose the original intended meaning...
                                        Posted by yozo at Aug 07, 2013 05:27
                                     |
| Wouldn't this rule ban functions like strdup, getline, and asprintf? In particular, isn't it often best for the callee to allocate its own memory, since the caller can't know how much will be needed?
                                        Posted by jcsible at Jun 30, 2020 14:20
                                     |
| Strictly as written, this recommendation does not account for functions like strdup() which returns a block of memory that must be subsequently freed. This is a recommendation, not a rule, and this means you can violate it while still having secure coding.We could always add an exception allowing functions to produce allocated chunks like malloc() does, or to consume them like free() does. There are lots of other exceptions we would have to excuse, such as smart pointers, garbage collection, and other techniques.More sophisticated techniques for modelling memory allocation exist, too. I'll recommend the Pointer Ownership Model (https://resources.sei.cmu.edu/library/asset-view.cfm?assetid=55000) as an example.
                                        Posted by svoboda at Aug 13, 2020 15:10
                                     |

