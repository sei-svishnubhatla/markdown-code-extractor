When the requested size is 0, the behavior of the memory allocation functions `malloc()`, `calloc()`, and `realloc()` is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). Subclause 7.22.3 of the C Standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] states:
> If the size of the space requested is zero, the behavior is implementation-defined: either a null pointer is returned, or the behavior is as if the size were some nonzero value, except that the returned pointer shall not be used to access an object.

In addition, the amount of storage allocated by a successful call to the allocation function when 0 bytes was requested is [unspecified](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior). See [unspecified behavior 41](DD.-Unspecified-Behavior_87152246.html#DD.UnspecifiedBehavior-usb_40) in subclause J.1 of the C Standard.
In cases where the memory allocation functions return a non-null pointer, reading from or writing to the allocated memory area results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Typically, the pointer refers to a zero-length block of memory consisting entirely of control structures. Overwriting these control structures damages the data structures used by the memory manager.
## Noncompliant Code Example (`malloc()`)
The result of calling `malloc(0)` to allocate 0 bytes is implementation-defined. In this example, a dynamic array of integers is allocated to store `size` elements. However, if `size` is 0, the call to `malloc(size)` may return a reference to a block of memory of size 0 instead of a null pointer. When (nonempty) data is copied to this location, a heap-buffer overflow occurs.
``` c
size_t size;
/* Initialize size, possibly by user-controlled input */
int *list = (int *)malloc(size);
if (list == NULL) {
  /* Handle allocation error */
}
else {
/* Continue processing list */
}
```
## Compliant Solution (`malloc()`)
To ensure that 0 is never passed as a size argument to `malloc()`, `size` is checked to confirm it has a positive value:
``` c
size_t size;
/* Initialize size, possibly by user-controlled input */
if (size == 0) {
  /* Handle error */
}
int *list = (int *)malloc(size);
if (list == NULL) {
  /* Handle allocation error */
}
/* Continue processing list */
```
## Noncompliant Code Example (`realloc()`)
The `realloc()` function deallocates the old object and returns a pointer to a new object of a specified size. If memory for the new object cannot be allocated, the `realloc()` function does not deallocate the old object, and its value is unchanged. If the `realloc()` function returns `NULL`, failing to free the original memory will result in a memory leak. As a result, the following idiom is often recommended for reallocating memory:
``` c
size_t nsize = /* Some value, possibly user supplied */;
char *p2;
char *p = (char *)malloc(100);
if (p == NULL) {
  /* Handle error */
}
/* ... */
if ((p2 = (char *)realloc(p, nsize)) == NULL) {
  free(p);
  p = NULL;
  return NULL;
}
p = p2;
```
However, this commonly recommended idiom has problems with zero-length allocations. If the value of `nsize` in this example is 0, the standard allows the option of either returning a null pointer or returning a pointer to an invalid (for example, zero-length) object. In cases where the `realloc()` function frees the memory but returns a null pointer, execution of the code results in a double-free vulnerability. If the `realloc()` function returns a non-null value, but the size was 0, the returned memory will be of size 0, and a heap overflow will occur if nonempty data is copied there.
### Implementation Details
If this noncompliant code is compiled with GCC 3.4.6 and linked with libc 2.3.4, invoking `realloc(p, 0)` returns a non-null pointer to a zero-sized object (the same as `malloc(0)`). However, if the same code is compiled with either Microsoft Visual Studio or GCC 4.1.0 , `realloc(p, 0)` returns a null pointer, resulting in a double-free vulnerability.
## Compliant Solution (`realloc()`)
This compliant solution does not pass a size argument of zero to the `realloc()` function:
``` c
size_t nsize;
/* Initialize nsize */
char *p2;
char *p = (char *)malloc(100);
if (p == NULL) {
  /* Handle error */
}
/* ... */
p2 = NULL;
if (nsize != 0) {
  p2 = (char *)realloc(p, nsize);
}
if (p2 == NULL) {
  free(p);
  p = NULL;
  return NULL;
}
p = p2;
```
## Risk Assessment
Allocating 0 bytes can lead to [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM04-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | (customization) | Users can add a custom check for allocator calls with size argument 0 (this includes literal 0, underconstrained tainted values, and computed values).; |
| Compass/ROSE |  |  | Can detect some violations of this rule. In particular, it warns when the argument to malloc() is a variable that has not been compared against;0 or that is known at compile time to be 0 |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM04-a | The validity of values passed to library functions shall be checked |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM04-C | Checks for:Variable length array with nonpositive sizeTainted sign change conversionTainted size of variable length arrayRec. fully covered. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM04-CPP. Do not perform zero-length allocations |
| MITRE CWE | CWE-687, Function call with incorrectly specified argument value |

##  Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.22.3, "Memory Management Functions" |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |
| [Vanegue 2010] | "Automated Vulnerability Analysis of Zero-Sized Heap Allocations" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152468) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152078)
## Comments:

|  |
| ----|
| In the first CS, the test for less than or equal to zero should just be equal to zero since the size will be an unsigned integer if the other rules have been followed - indeed, it should be a size_t.
In the implementation details section, 'realloc(0)' is an invalid call to realloc; presumably, that should be 'realloc(p, 0)'.
Isn't the primary advice here really "do not attempt to allocate zero length memory segments", with the sub-text "and do not use realloc() to free data - that's what free() is for".
                                        Posted by jonathan.leffler@gmail.com at Mar 17, 2008 00:19
                                     |
| Of course you can use the pointer from allocating 0 bytes.;  If you need a unique poiner (so it compares differently from all other pointers), a non-NULL result from malloc will do fine.  What you canÂ´t do is _follow_ the pointer.  ThatÂ´s just a special case of, after allocating N bytes you must not access data beyond those N bytes.  With N = 0, there is nothing you can access.
That said, malloc/realloc(0 bytes) is indeed a bad idea.  If you want to malloc a pointer in the first place, likely the possible NULL return will not be useful so itÂ´s better to allocate 1 byte (which you do not intend to access). And as said, realloc of 0 bytes is ambiguous.
Nitpick: ItÂ´s not quite right that the standard allows realloc(non-NULL, 0) to either free or not free.  The C standard*s* together do:  The C89 standard says it frees and returns NULL, while the C99 standard does not allow it to free (except after allocating a new memory area to return). So the result is the same: If realloc(ptr, 0) returns NULL, you donÂ´t know if the pointer was freed or not unless you know which C version the runtime library has.  (Which, given compilers like gcc that use the systemÂ´s library, is not necessarily the same as the compile-time mode, so a preprocessor #ifdef does not disambiguate.)
                                        Posted by hbf at Apr 17, 2008 12:53
                                     |
| The 'realloc(0)' is an invalid call to realloc; presumably, that should be 'realloc(p, 0)' problem got fixed before I could get to it.
I liked your other idea, and changed the title to "Do not perform zero length allocations".  Sometimes you need to read these things to figure out what you were saying.  ;^)
I'm not sure anyone would consciously consider using realloc() to free data, and if these people exist, they are beyond our reach anyway.
                                        Posted by rcs at Apr 18, 2008 03:14
                                     |
| realloc(non-null, 0) was a valid way to free data in C89, so there was no reason not to use it when convenient.  One reason to use it was that malloc and free could both be implemented as wrappers around realloc. Similarly, if you were writing a wrapper around those functions, you only needed to implement the realloc wrapper - the others could be wrappers (maybe macros) around your realloc variant.
                                        Posted by hbf at Apr 21, 2008 12:50
                                     |
| The realloc() non-compliant code example has 2 problems, the double free problem that may occur when realloc() is given a size of 0 and returns NULL (which the descriptive text mentions), and the problem that realloc() could return an invalid-to-dereference non-NULL pointer when given a size of 0 (i.e., the same problem as malloc(0)). Maybe the second problem should be explicitly stated in the realloc() descriptive text.
                                        Posted by sayre@cert.org at Jul 14, 2008 15:32
                                     |
| done
                                        Posted by svoboda at Jul 14, 2008 16:10
                                     |
| Jeff, Martin,
Please consider my presentation on vulnerabilities due to zero allocations:
http://hackitoergosum.org/wp-content/uploads/2010/04/HES10-jvanegue_zero-allocations.pdf
Thanks,
Julien
                                        Posted by jvanegue at Jun 06, 2010 03:25
                                     |
| Yes, this page has been here since Jun 23, 2006.  I've added a reference to your presentation, because it contains some interesting information about exploitation and automated detection.
                                        Posted by rcs_mgr at Jun 06, 2010 12:30
                                     |
| Robert,
Thanks for adding the reference to the presentation.
Julien
                                        Posted by jvanegue at Jun 06, 2010 23:01
                                     |
| Got a 404 on that. A Google search later, it can still be found here:http://repo.meh.or.id/expl0it/HES10-jvanegue_zero-allocations.pdf
                                        Posted by asolano at Apr 08, 2013 14:57
                                     |

