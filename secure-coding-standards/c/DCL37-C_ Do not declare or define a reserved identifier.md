According to the C Standard, 6.4.2.1 paragraph 7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> Some identifiers are reserved.
>
>     —  All identifiers that begin with a double underscore (\_\_) or begin with an underscore (\_) followed by an uppercase letter are reserved for any use, except those identifiers which are lexically identical to keywords.
>
>     —  All identifiers that begin with an underscore are reserved for use as identifiers with file scope in both the ordinary and tag name spaces.
>
> Other identifiers may be reserved, see 7.1.3.

C Standard, 7.1.3 paragraph 1 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> Each header declares or defines all identifiers listed in its associated subclause, and optionally declares or defines identifiers listed in its associated future library directions subclause and identifiers which are always reserved either for any use or for use as file scope identifiers.
>
>     — All potentially reserved identifiers (including ones listed in the future library directions) that are provided by an implementation with an external definition are reserved for any use. An implementation shall not provide an external definition of a potentially reserved identifier unless that identifier is reserved for a use where it would have external linkage. All other potentially reserved identifiers that are provided by an implementation (including in the form of a macro) are reserved for any use when the associated header is included. No other potentially reserved identifiers are reserved.
>
>     — Each macro name in any of the following subclauses (including the future library directions) is reserved for use as specified if any of its associated headers is included; unless explicitly stated otherwise (see 7.1.4).
>
>     — All identifiers with external linkage in any of the following subclauses (including the future library directions) and errno are always reserved for use as identifiers with external linkage.
>
>     — Each identifier with file scope listed in any of the following subclauses (including the future library directions) is reserved for use as a macro name and as an identifier with file scope in the same name space if any of its associated headers is included.

Additionally, subclause 7.33 defines many other reserved identifiers for future library directions.
No other identifiers are reserved. (The POSIX standard extends the set of identifiers reserved by the C Standard to include an open-ended set of its own. See *Portable Operating System Interface \[POSIX<sup>®</sup>\], Base Specifications, Issue 7*, [Section 2.2](http://www.opengroup.org/onlinepubs/9699919799/functions/V2_chap02.html#tag_15_02), "The Compilation Environment" \[[IEEE Std 1003.1-2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\].) The behavior of a program that declares or defines an identifier in a context in which it is reserved or that defines a reserved identifier as a macro name is undefined. (See [undefined behavior 105](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_105).)
## Noncompliant Code Example (Include Guard)
A common, but noncompliant, practice is to choose a reserved name for a macro used in a preprocessor conditional guarding against multiple inclusions of a header file. (See also [PRE06-C. Enclose header files in an include guard](PRE06-C_%20Enclose%20header%20files%20in%20an%20include%20guard).) The name may clash with reserved names defined by the implementation of the C standard library in its headers or with reserved names implicitly predefined by the compiler even when no C standard library header is included.
``` c
#ifndef _MY_HEADER_H_
#define _MY_HEADER_H_
/* Contents of <my_header.h> */
#endif /* _MY_HEADER_H_ */
```
## Compliant Solution (Include Guard)
This compliant solution avoids using leading underscores in the macro name of the include guard:
``` c
#ifndef MY_HEADER_H
#define MY_HEADER_H
/* Contents of <my_header.h> */
#endif /* MY_HEADER_H */
```
## Noncompliant Code Example (File Scope Objects)
In this noncompliant code example, the names of the file scope objects `_max_limit` and `_limit` both begin with an underscore. Because `_max_limit` is static, this declaration might seem to be impervious to clashes with names defined by the implementation. However, because the header `<stddef.h>` is included to define `size_t`, a potential for a name clash exists. (Note, however, that a [conforming](BB.-Definitions_87152273.html#BB.Definitions-conformingprogram) compiler may implicitly declare reserved names regardless of whether any C standard library header is explicitly included.)
In addition, because `_limit` has external linkage, it may clash with a symbol of the same name defined in the language runtime library even if such a symbol is not declared in any header. Consequently, it is not safe to start the name of any file scope identifier with an underscore even if its linkage limits its visibility to a single translation unit.
``` c
#include <stddef.h>
static const size_t _max_limit = 1024;
size_t _limit = 100;
unsigned int getValue(unsigned int count) {
  return count < _limit ? count : _limit;
}
```
## Compliant Solution (File Scope Objects)
In this compliant solution, names of file scope objects do not begin with an underscore:
``` c
#include <stddef.h>
static const size_t max_limit = 1024;
size_t limit = 100;
unsigned int getValue(unsigned int count) {
  return count < limit ? count : limit;
}
```
## Noncompliant Code Example (Reserved Macros)
In this noncompliant code example, because the C standard library header `<inttypes.h>` is specified to include `<stdint.h>`, the name `SIZE_MAX` conflicts with a standard macro of the same name, which is used to denote the upper limit of `size_t`. In addition, although the name `INTFAST16_LIMIT_MAX` is not defined by the C standard library, it is a reserved identifier because it begins with the `INT` prefix and ends with the `_MAX` suffix. (See the C Standard, 7.33.14.)
``` c
#include <inttypes.h>
#include <stdio.h>
static const int_fast16_t INTFAST16_LIMIT_MAX = 12000;
void print_fast16(int_fast16_t val) {
  enum { SIZE_MAX = 80 };
  char buf[SIZE_MAX];
  if (INTFAST16_LIMIT_MAX < val) {
    sprintf(buf, "The value is too large");
  } else {
    snprintf(buf, SIZE_MAX, "The value is %" PRIdFAST16, val);
  }
}
```
## Compliant Solution (Reserved Macros)
This compliant solution avoids redefining reserved names or using reserved prefixes and suffixes:
``` c
#include <inttypes.h>
#include <stdio.h>
static const int_fast16_t MY_INTFAST16_UPPER_LIMIT = 12000;
void print_fast16(int_fast16_t val) {
  enum { BUFSIZE = 80 };
  char buf[BUFSIZE];
  if (MY_INTFAST16_UPPER_LIMIT < val) {
    sprintf(buf, "The value is too large");
  } else {
    snprintf(buf, BUFSIZE, "The value is %" PRIdFAST16, val);
  }
}
```
## Noncompliant Code Example (Identifiers with External Linkage)
This noncompliant example provides definitions for the C standard library functions `malloc()` and `free()`. Although this practice is permitted by many traditional implementations of UNIX (for example, the [Dmalloc](http://dmalloc.com/) library), it is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) according to the C Standard. Even on systems that allow replacing `malloc()`, doing so without also replacing `aligned_alloc()`, `calloc()`, and `realloc()` is likely to cause problems.
``` c
#include <stddef.h>
void *malloc(size_t nbytes) {
  void *ptr;
  /* Allocate storage from own pool and set ptr */
  return ptr;
}
void free(void *ptr) {
  /* Return storage to own pool */
}
```
## Compliant Solution (Identifiers with External Linkage)
The compliant, portable solution avoids redefining any C standard library identifiers with external linkage. In addition, it provides definitions for all memory allocation functions:
``` c
#include <stddef.h>
void *my_malloc(size_t nbytes) {
  void *ptr;
  /* Allocate storage from own pool and set ptr */
  return ptr;
}
void *my_aligned_alloc(size_t alignment, size_t size) {
  void *ptr;
  /* Allocate storage from own pool, align properly, set ptr */
  return ptr;
}
void *my_calloc(size_t nelems, size_t elsize) {
  void *ptr;
  /* Allocate storage from own pool, zero memory, and set ptr */
  return ptr;
}
void *my_realloc(void *ptr, size_t nbytes) {
  /* Reallocate storage from own pool and set ptr */
  return ptr;
}
void my_free(void *ptr) {
  /* Return storage to own pool */
}
```
## Noncompliant Code Example (`errno`)
In addition to symbols defined as functions in each C standard library header, identifiers with external linkage include `errno` and `math_errhandling`.  According to the C Standard, 7.5, paragraph 2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], the behavior of a program is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when
> A macro definition of `errno` is suppressed in order to access an actual object, or the program defines an identifier with the name `errno`. 

See [undefined behavior 111](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_111).
The `errno` identifier expands to a modifiable [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) that has type `int` but is not necessarily the identifier of an object. It might expand to a modifiable lvalue resulting from a function call, such as `*errno()`. It is unspecified whether `errno` is a macro or an identifier declared with external linkage. If a macro definition is suppressed to access an actual object, or if a program defines an identifier with the name `errno`, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
Legacy code is apt to include an incorrect declaration, such as the following:
``` c
extern int errno;
```
## Compliant Solution (`errno`)
The correct way to declare `errno` is to include the header `<errno.h>`:
``` c
#include <errno.h>
```
[Implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) [conforming](BB.-Definitions_87152273.html#BB.Definitions-conformingprogram) to C are required to declare `errno` in `<errno.h>`, although some historic implementations failed to do so.
## Exceptions
**DCL37-C-EX1:** Provided that a library function can be declared without reference to any type defined in a header, it is permissible to declare that function without including its header provided that declaration is compatible with the standard declaration.
``` c
/* Not including stdlib.h */
void free(void *);
void func(void *ptr) {
  free(ptr);
}
```
Such code is compliant because the declaration matches what `stdlib.h` would provide and does not redefine the reserved identifier. However, it would not be acceptable to provide a definition for the `free()` function in this example.
**DCL37-C-EX2:** For compatibility with other compiler vendors or language standard modes, it is acceptable to create a macro identifier that is the same as a reserved identifier so long as the behavior is idempotent, as in this example:
``` c
/* Sometimes generated by configuration tools such as autoconf */
#define const const
/* Allowed compilers with semantically equivalent extension behavior */
#define inline __inline
```
**DCL37-C-EX3:** As a compiler vendor or standard library developer, it is acceptable to use identifiers reserved for your implementation. Reserved identifiers may be defined by the compiler, in standard library headers or headers included by a standard library header, as in this example declaration from the glibc standard C library implementation:
``` c
/*
  The following declarations of reserved identifiers exist in the glibc implementation of
  <stdio.h>. The original source code may be found at:
  https://sourceware.org/git/?p=glibc.git;a=blob_plain;f=include/stdio.h;hb=HEAD
*/
#  define __need_size_t
#  include <stddef.h>
/* Generate a unique file name (and possibly open it).  */
extern int __path_search (char *__tmpl, size_t __tmpl_len,
              const char *__dir, const char *__pfx,
              int __try_tempdir);
```
## Risk Assessment
Using reserved identifiers can lead to incorrect program operation.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL37-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | future-library-uselanguage-overridelanguage-override-c99reserved-declarationreserved-declaration-c99reserved-identifier | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL37 | Fully implemented. Reserved identifiers, as in DCL37-C-EX3, are configurable. |
| CodeSonar | 8.3p0 | LANG.STRUCT.DECL.RESERVED | Declaration of reserved name |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISRA C 2004 Rule 20.1MISRA C 2004 Rule 20.2MISRA C 2012 Rule 21.1MISRA C 2012 Rule 21.2 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-dcl37-c |  |
| ECLAIR | 1.2 | CC2.DCL37 | Fully implemented |
| Helix QAC | 2024.4 | C0602, C0603, C4600, C4601, C4602, C4603, C4604, C4605, C4606, C4607, C4608, C4620, C4621, C4622, C4623, C4624, C4640, C4641, C4642, C4643, C4644, C4645 | Fully implemented |
| Klocwork | 2024.4 | MISRA.DEFINE.WRONGNAME.UNDERSCOREMISRA.STDLIB.WRONGNAME.UNDERSCORE
MISRA.STDLIB.WRONGNAME | Fully implemented |
| LDRA tool suite | 9.7.1 | 86 S, 218 S, 219 S, 580 S, 626 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL37-bCERT_C-DCL37-c
CERT_C-DCL37-d
CERT_C-DCL37-e
CERT_C-DCL37-f
CERT_C-DCL37-g
 | Identifiers that begin with an underscore and either an uppercase letter or another underscore should not be declaredAvoid declaring file-scoped objects whose names begin with an underscore
The names of standard library macros should not be reused (C11 code)
The names of standard library identifiers with file scope should not be reused (C11 code)
The standard library identifiers with external linkage should not be reused (C11 code)
Macros that begin with an underscore and either an uppercase letter or another underscore should not be defined |
| PC-lint Plus | 1.4 | 978, 9071, 9093 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule DCL37-C | Checks for:Defining and undefining reserved identifiers or macrosDeclaring a reserved identifier or macro nameRule partially covered |
| PVS-Studio | 7.35 | V677 |  |
| SonarQube C/C++ Plugin | 3.11 | S978 |  |
| RuleChecker | 24.04 | future-library-uselanguage-overridelanguage-override-c99reserved-declarationreserved-declaration-c99reserved-identifier | Partially checked |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | PRE00-C. Prefer inline or static functions to function-like macros | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | PRE06-C. Enclose header files in an include guard | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | PRE31-C. Avoid side effects in arguments to unsafe macros | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | DCL51-CPP. Do not declare or define a reserved identifier | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Using identifiers that are reserved for the implementation [resident] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 21.1 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 21.2 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1-2013] | Section 2.2, "The Compilation Environment" |
| [ISO/IEC 9899:2024] | 7.1.3, "Reserved Identifiers"7.33.14, "Integer Types <stdint.h>" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152132) [](../c/Rule%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152410)
## Comments:

|  |
| ----|
| A few of the code examples were ill-formed (missing return statement) so I corrected them and also simplified them in the process. In doing so, I noticed a few other possible improvements to this page but before making them I want to check to make sure there isn't a deeper reason for the status quo that eludes me.
    It seems that the first example could be merged with the one dealing with global variables. Doing so would reduce duplicity and let us add other, more interesting examples.
    The last non-compliant example and solution seems excessively involved for something as simple as redefining errno. Reducing their complexity would avoid distracting the reader with irrelevant details and allow them to focus on the real problem.
    A class of problems not yet covered by any of the examples is redefining names reserved for library functions (as opposed to macros). In this area, an interesting topic to cover is replacing functions such as malloc() and free(), which while not permitted by the C standard, is commonly allowed on some UNIX systems (notably those that support the ELF object model).
    Another class of problems not yet discussed here is using names that aren't necessarily defined by the standard or even used by existing implementations but that encroach on the namespace reserved for future use. For example, a pervasive non-compliant practice is defining names that end in the _t suffix (such as mystruct_t). This is particluarly onerous for POSIX applications given the size of the reserved namespace(s) – see section 2.2.2 The Name Space  in the Single UNIX Specification online.
                                        Posted by martinsebor at Jan 16, 2010 17:30
                                     |
| All your changes sound fine.  I think the reason this guideline is like it is is because it is relatively new and hasn't been massaged as much as other rules.
                                        Posted by rcs at Jan 16, 2010 19:15
                                     |
| Agreed. I'll note the existence of the rule ERR31-C. Don't redefine errno which probably should be folded into this rule.
                                        Posted by svoboda at Jan 18, 2010 09:37
                                     |
| DCL37-C-EX3:;As a compiler vendor or standard library developer, it is acceptable to use identifiers reserved for your implementation. Reserved identifiers may be defined by the compiler, in standard library headers, or headers included by a standard library headerIt's not only acceptable but necessary to use reserved names in implementations of the language. Doing otherwise might conflict with the same names used by programs. So implementations don't just need to be exempted from this rule: they need to follow the converse of it.But I'm not sure that adding individual exceptions for implementations makes sense. Implementations unavoidably must make use of non-portable constructs and even rely on undefined behavior and thus violate the guidelines. A survey of how many others might need to be exempted would be interesting (or how many are violated in common implementations).
                                        Posted by martinsebor at Dec 18, 2014 11:29
                                     |
| Agreed that it's basically required to use reserved identifiers as an implementer. I put "acceptable" in the wording to normatively allow for it, but am happy to consider other wordings.As for not adding exceptions for implementations, I'm on the fence. I raised this question earlier today and;Robert Seacord suggested I was being too clever. If you agree, I can remove it. My rationale for adding it was that implementers may want to conform to our secure coding rules, and this would be one rule they absolutely could not avoid failing.
                                        Posted by aballman at Dec 18, 2014 11:34
                                     |
| "Header Guard" and "Inclusion Guard".dcl37-c uses "header guards".; pre06-c uses "inclusion guards".  I think the same wording should be used in both guidelines."inclusion guards" sounds a little better than "header guards" for me.  Any comment? Quick searching the web shows:"include guard" (https://en.wikipedia.org/wiki/Include_guard)"header guards" (http://faculty.cs.niu.edu/~mcmahon/CS241/c241man/node90.html)"guard macro" (https://gcc.gnu.org/onlinedocs/cppinternals/Guard-Macros.html)"include guard" (https://llvm.org/docs/CodingStandards.html)"header guard" (https://clang.llvm.org/extra/doxygen/HeaderGuardCheck_8h_source.html)
                                        Posted by yozo at Dec 15, 2017 06:25
                                     |
| I agree that "Inclusion Guard" is better. This is the true meaning (protect against multiple inclusion).
                                        Posted by jerome.guy at Dec 15, 2017 07:35
                                     |
| Thanks for the feedback. We've decided to use the term "include guard";  In addition to the above reasons, it yields more Google hits than 'header guard' or 'include guard'.
                                        Posted by svoboda at Dec 15, 2017 13:58
                                     |
| I moved the paragraph "In addition to symbols defined as functions in each C standard library header, identifiers with external linkage include;errnoand math_errhandling, among others, regardless of whether any of them are masked by a macro of the same name."This paragraph lives since revision 16, I suppose it should be deleted at that time. But now we have NCCE(errno), to have this paragraph.Please fix it if I misunderstand something...
                                        Posted by yozo at Dec 19, 2017 00:29
                                     |
| No, this looks good to me. Thanks!
                                        Posted by svoboda at Dec 19, 2017 10:25
                                     |
| We should add an exception for feature test macros, e.g., #define _GNU_SOURCE.
                                        Posted by jcsible at Jul 01, 2020 12:53
                                     |
| Feature test macros, including _GNU_SOURCE, are a GNU extension, and are not currentluy addressed by any of this rule's exceptions. One could argue that they are out of scope (see Scope), because they are a platform extension, which are outside the scope of this standard.However, the popularity of gcc and clang (both use glibc and GNU features) does suggest that such an exception might have enough of an audience to be worthwhile.
                                        Posted by svoboda at Jul 02, 2020 14:36
                                     |
| It's necessary in order to use Annex K, for instance, because you need to be able to define __STDC_WANT_LIB_EXT1__. The tricky part will be in specifying what constitutes a feature test macro.
                                        Posted by aballman at Jul 02, 2020 14:44
                                     |

