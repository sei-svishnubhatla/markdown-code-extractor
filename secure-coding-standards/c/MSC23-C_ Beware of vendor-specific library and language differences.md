When compiling with a specific vendor's [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) of the C language, and related libraries, be aware that, unfortunately, standards conformance can differ from vendor to vendor. Be certain to read your vendor's documentation to reduce the likelihood of accidentally relying on implementation-specific behavior or deviations.
## Implementation-Specific Deviations
Implementation-specific deviations are listed below. The Version column lists the latest version of the compiler or library that exhibits the behavior.
### Microsoft Visual Studio

| API | Description | Version  |
| ----|----|----|
| Variable-length arrays | Absent; | 2012; |
| static;and type qualifiers in
parameter array declarators | Absent; | 2012; |
| _Static_assert | Absent; can use;static_assert, as in C++11 | 2012 |
| _Noreturn | Absent;;can use __declspec(noreturn) | 2012 |
| inline | Absent; can use;__inline | 2012; |
| Hexadecimal floating-point constants | Absent; | 2012; |
| Compound literals | Absent; | 2012; |
| Designated initializers | Absent; | 2012; |
| Implicit function declarations | Support was removed in C11, but it is still supported in MSVC (with diagnostic); | 2012; |
| Mixed declarations and code | Absent; | 2012; |
| _Pragma

\| Absent; can use [`__pragma`](http://msdn.microsoft.com/en-us/library/d9x1s805.aspx) \| 2012; \| \| `_Bool` \| Absent \| 2012; \| \| `_Complex` \| Absent; \| 2012; \| \| `__func__` \| Absent; can use;[`__FUNCTION__`](http://msdn.microsoft.com/en-us/library/b0084kay(v=vs.110).aspx) \| 2012 \| \|
idempotent type qualifiers
\| Diagnosed, but;functional \| 2012 \| \| `_Thread_local` \| Absent; can use;[`__declspec(thread)`](http://msdn.microsoft.com/en-us/library/9w1sdazb.aspx) \| \| \| \<complex.h\> \| Absent; `__STDC_NO_COMPLEX__` is not;defined \| 2012; \| \| `isblank()` \| Absent \| 2012; \| \| \<fenv.h\> \| Absent \| 2012; \| \| \<inttypes.h\> \| Absent \| 2012; \| \|
`float_t`, `double_t`, `HUGE_VALF,HUGE_VALL, INFINITY, NAN`
\| Absent; \| 2012; \| \| #pragma `FP_CONTRACT` \| Spelled;[`fp_contract`](http://msdn.microsoft.com/en-us/library/4f994tzs(v=vs.110).aspx) instead of `FP_CONTRACT` \| 2012; \| \| `fpclassify()` \| Absent, use;[`_fpclass()`](http://msdn.microsoft.com/en-us/library/39s1cck2.aspx) instead \| 2012; \| \| `isfinite()`, `isinf()` \| Absent, use;[`_finite()`](http://msdn.microsoft.com/en-us/library/sb8es7a8.aspx) or `_finitef()`instead \| 2012; \| \| `isnan()` \| Absent, use;[`_isnan()`](http://msdn.microsoft.com/en-us/library/tzthab44.aspx) or `_isnanf()` instead \| 2012 \| \| `isnormal()` \| Absent, use;[`_fpclass()`](http://msdn.microsoft.com/en-us/library/39s1cck2.aspx) instead  \| 2012 \| \| `signbit()` \| Absent; \| 2012; \| \| `acosh()`, `asinh()`, `atanh()` \| Absent \| 2012; \| \| `exp2()`, `expm1()`, `ilogb()`, `log1p()`,`log2()` \| Absent \| 2012; \| \| `scalbn()` \| Absent; use;[`_scalb()`](http://msdn.microsoft.com/en-us/library/esw6b4yx.aspx) (or `_scalbf()` on x64 targets only) instead  \| 2012; \| \| `cbrt()` \| Absent; \| 2012; \| \| `erf()`, `erfc()`, `lgamma()`, `tgamma()` \| Absent \| 2012 \| \| `nearbyint()`, `rint()`, `lrint()`,`round()`, `lround()`, `trunk()` \| Absent; \| 2012 \| \| `remainder()`, `remquo()` \| Absent \| 2012; \| \| `copysign()` \| Absent; use;[`_copysign()`](http://msdn.microsoft.com/en-us/library/0yafk1hc.aspx) instead  \| 2012; \| \| `nan()`, `nexttoward()` \| Absent; \| 2012; \| \| `nextafter()` \| Absent; use;[`_nextafter()`](http://msdn.microsoft.com/en-us/library/h0dff77w.aspx) or `_nextafterf()` instead  \| 2012; \| \| `fdim()`,;`fmax(),` `fmin()` \| Absent; \| 2012; \| \| `fma()` \| Absent; \| 2012 \| \| `isgreater()`, `isgreaterequal()`,`isless()`, `islessequal()`,  
`isunordered()` \| Absent; \| 2012; \| \| `<stdalign.h>` \| Absent; \| \| \| `va_copy()` \| Absent; \| 2012; \| \| `<stdatomic.h>` \| Absent;;`__STDC_NO_ATOMICS__` is not defined \| 2012; \| \| `<stdbool.h>` \| Absent;;`_Bool` is not supported in `/TC` mode, but [`bool`](http://msdn.microsoft.com/en-us/library/tf4dy80a.aspx) is supported in `/TP` mode \| 2012; \| \| `max_align_t` \| Absent; \| 2012; \| \| Printing;format specifier [type field](http://msdn.microsoft.com/en-us/library/hf4y5e3w.aspx) \| `S`;is MSVC-specific; `c`, `s`, and `z` are not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `F` is unsupported \| 2012 \| \| Printing;format specifier [size field](http://msdn.microsoft.com/en-us/library/tcxf1dw6.aspx) \| `I`,;`I32` and `I64` are MSVC-specific; `h`, `w` and `l` are not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `hh`, `j`, `z`  
and `t` unsupported \| 2012 \| \| Scanning;format specifier [type field](http://msdn.microsoft.com/en-us/library/6ttkkkhh.aspx) \| `S`;is MSVC-specific; `c` and `s` are not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `p` is unsupported \| 2012; \| \| Scanning;format specifier [size field](http://msdn.microsoft.com/en-us/library/xdb9w69d.aspx) \| `I64`;is MSVC-specific; `h`, `l`, and `L` prefixes are not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `hh`, `j`, `z`, and  
`t` are unsupported \| 2012; \| \| `snprintf()` \| Absent; beware that [`_snprintf()`](http://msdn.microsoft.com/en-us/library/2ts7cx93.aspx)'s semantics are sufficiently different that it is not advisable as a replacement \| 2012 \| \| `vfscanf()`, `vscanf()`, `vsscanf()` \| Absent; \| 2012; \| \| [fopen(), freopen()](http://msdn.microsoft.com/en-us/library/yeby3zcb(v=vs.110).aspx) \| Mode parameter not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `t`, `c`, `n`, `N`, `S`, `R`, `T`,;`D` and `css` are MSVC  
extensions; `x` is unsupported; see remarks \| 2012; \| \| `atoll()` \| Absent; use;[`_atoi64()`](http://msdn.microsoft.com/en-us/library/czcad93k.aspx) instead  \| 2012; \| \| `strtof()`, `strtold()` \| Absent; \| 2012 \| \| `strtoll()` \| Absent; use;`_strtoi64()` instead  \| 2012; \| \| `strtoull()` \| Absent; use;[`_strtoui64()`](http://msdn.microsoft.com/en-us/library/h80404d3.aspx) instead  \| 2012; \| \| `aligned_alloc()` \| Absent; use;[`_aligned_malloc()`](http://msdn.microsoft.com/en-us/library/8z34s9c6.aspx) instead (beware, the parameter order is reversed) \| 2012; \| \| `at_quick_exit()`, `quick_exit()` \| Absent; \| 2012; \| \| `_Exit()` \| Absent; use;[`_exit()`](http://msdn.microsoft.com/en-us/library/6wdz5232.aspx) instead \| 2012 \| \| \<stdnoreturn.h\> \| Absent; use;[`__declspec(noreturn)`](http://msdn.microsoft.com/en-us/library/k6ktzx3s(v=vs.110).aspx) instead  \| 2012; \| \| `<tgmath.h>` \| Absent; \| 2012; \| \| `<threads.h>` \| Absent;;`__STDC_NO_THREADS__` is not defined \| 2012; \| \| `TIME_UTC,` `struct timespec,``timespec_get()` \| Absent \| 2012; \| \| [`strftime(), wcsftime()`](http://msdn.microsoft.com/en-us/library/fe06s4ak.aspx) \| `z`;is not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; `C`, `D`, `e`, `F`, `g`, `G`, `h`, `n`, `r`, `R`, `t`, `T`, `u`, `V` unsupported \| 2012 \| \| `<uchar.h>` \| Absent; \| 2012; \| \| `vfwscanf()`, `vswscanf()`, `vwscanf()` \| Absent \| 2012; \| \| `fwide()` \| [Unsupported](http://msdn.microsoft.com/en-us/library/aa985619.aspx) \| 2012; \| \| `wcstof()`, `wcstold()` \| Absent; \| 2012; \| \| `wcstoll()` \| Absent; use;[`_wcstoi64()`](http://msdn.microsoft.com/en-us/library/h80404d3.aspx) instead  \| 2012; \| \| `wcstoull()` \| Absent; use;[`_wcstoui64()`](http://msdn.microsoft.com/en-us/library/85zk715d.aspx) instead \| 2012; \| \| `iswblank()` \| Absent; \| 2012; \| \| `FLT_EVAL_METHOD`, `*_HAS_SUBNORM`,`*_DECIMAL_DIG`, `*_TRUE_MIN` \| Absent; \| 2012; \| \|
    __STDC_LIB_EXT1__,__STDC_WANT_LIB_EXT1__
\| Not defined; instead, MSVC uses;`__STDC_SECURE_LIB__` and `__STDC_WANT_SECURE_LIB__` \| 2012; \| \| [`fopen_s(), freopen_s()`](http://msdn.microsoft.com/en-us/library/z5hh6ee9.aspx) \| Uses the same mode strings as `fopen()`;;`u` prefix is unsupported; see remarks \| 2012; \| \| `vfscanf_s()`, `vscanf_s()`,`vsscanf_s()` \| Absent; \| 2012; \| \| `constraint_handler_t`,`set_constraint_handler_s(),`  
`abort_handler_s(),`  
`ignore_handler_s()` \| Absent; use;`_invalid_parameter_handler` and [`_set_invalid_parameter_handler()`](http://msdn.microsoft.com/en-us/library/a9yf33zb.aspx)  
instead.  Beware that the `_invalid_parameter_handler` signature is considerably different than  
that of `constraint_handler_t`.  No replacement for `abort_handler_s()` or  
`ignore_handler_s()` \| 2012; \| \| [`bsearch_s()`](http://msdn.microsoft.com/en-us/library/2w9185b8.aspx) \| Not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; beware that the comparison function pointer's signature is different from the standard; namely that the context parameter comes first in MSVC but last in ISO C \| 2012; \| \| [`qsort_s()`](http://msdn.microsoft.com/en-us/library/4xc60xas.aspx) \| Not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; beware that the comparison function's pointer signature is different from the standard; namely that the context parameter comes first in MSVC but last in ISO C \| 2012 \| \| [`strtok_s()`](http://msdn.microsoft.com/en-us/library/ftsafwz3.aspx) \| Not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; the function signature is missing the;`rsize_t *` parameter \| 2012; \| \| `memset_s(), strerrorlen_s()`; \| Absent; \| 2012 \| \| [`gmtime_s()`](http://msdn.microsoft.com/en-us/library/3stkd9be.aspx)`, `[`localtime_s()`](http://msdn.microsoft.com/en-us/library/a442x3ye.aspx) \| Not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; the function signature has the parameters reversed and returns`errno_t` instead of `struct tm *` \| 2012 \| \| `snwprintf_s()` \| Absent; use;[`_snwprintf_s()`](http://msdn.microsoft.com/en-us/library/f30dzcf6.aspx) instead.  Note that the parameters differ from the ISO C signature \| 2012 \| \| `vfwscanf_s()`, `vswscanf_s()`,`vwscanf_s()` \| Absent \| 2012 \| \|
`vsnwprintf_s()`
\| Absent, use;[`_vsnwprintf_s()`](http://msdn.microsoft.com/en-us/library/d3xd30zz.aspx) instead.  Note that the parameters differ from the ISO C signature \| 2012; \| \| [`wcstok_s()`](http://msdn.microsoft.com/en-us/library/ftsafwz3.aspx) \| Not conforming \[[ISO/IEC 9899-2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-ISO/IEC9899-2011)\]; the function signature is missing the;`rsize_t *` parameter \| 2012; \|
#### `fopen()` & `freopen()`
The C standard does not specify what happens with Windows newline characters (CRLF), and so care should be taken when working with text files.  For instance:
``` java
#include <stdio.h>
void func( void ) {
  FILE *fp = fopen("text_file.txt", "r");
  if (fp) {
    int counter = 0;
    while (!feof(fp) && !ferror(fp)) {
      ++counter;
      (void)fgetc(fp);
    }
    fclose(fp);
    printf("Number of characters read: %d\n", counter);
  }
}
// Contents of text_file.txt
This has
CRLF newlines
in it.
```
If you save the contents of text_file.txt with Windows line endings (CRLF) and run the program on Windows, it will print 30. However, if you compile the application on a platform which does not use CRLF as its line endings, it will print 32. This is because MSVC's text translation mode will translate the CRLF characters into a single LF character on input, and translate a single LF character to CRLF on output. To ensure consistent behavior between platforms, consider opening the file in binary translation mode explicitly.
``` c
#include <stdio.h>
void func( void ) {
  FILE *fp = fopen("text_file.txt", "rb");
  if (fp) {
    int counter = 0;
    while (!feof(fp) && !ferror(fp)) {
      ++counter;
      (void)fgetc(fp);
    }
    fclose(fp);
    printf("Number of characters read: %d\n", counter);
  }
}
```
 This program will print 32 with the given text, regardless of platform.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC23-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports non-standard language elements. |
| CodeSonar | 8.3p0 | BADFUNC.*CONCURRENCY.C_ATOMIC
CONCURRENCY.THREADLOCAL
LANG.FUNCS.NORETURN
LANG.PREPROC.INCL.TGMATH_H
LANG.STRUCT.ALIGNAS
LANG.STRUCT.ALIGNAS.EZA
LANG.STRUCT.ALIGNAS.IAS
LANG.STRUCT.ALIGNAS.TMAS
LANG.STRUCT.ALIGNOF
LANG.STRUCT.DECL.IMPFN
LANG.STRUCT.DECL.VLA
LANG.STRUCT.INIT.UADI
LANG.TYPE.VMAT
MATH.RANGE.GAMMA | Many checks for uses of functions that have vendor-specific differencesUse of C Atomic
Use of Thread Local
Use of Noreturn
Use of <tgmath.h>
Use of Alignas
Explicit Zero Alignment
Inconsistent Alignment Specifications
Too Many Alignment Specifiers
Use of Alignof
Implicit Function Declaration
Declaration of Variable Length Array
Unspecified Array Size with Designator Initialization
Pointer to Variably-modified Array Type
Gamma on Zero |

[](../c/MSC22-C_%20Use%20the%20setjmp__,%20longjmp__%20facility%20securely) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152260)
## Comments:

|  |
| ----|
| Instead of having a separate column for link, why not just link the appropriate term?I don't think you want to compare to "ANSI" or "ISO C".; Probably should reference a specific ISO/IEC version of the standard.
                                        Posted by rcs_mgr at Jul 06, 2013 22:35
                                     |
| Both good suggestions, I'll modify in the next round of updates.; Thanks!
                                        Posted by aballman at Jul 07, 2013 13:00
                                     |

