Few programmers consider the issues around formatted I/O and type definitions. A programmer-defined integer type might be any type supported by the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation), even a type larger than `unsigned long long`. For example, given an implementation that supports 128-bit unsigned integers and provides a `uint_fast128_t` type, a programmer may define the following type:
``` java
typedef uint_fast128_t mytypedef_t;
```
Furthermore, the definition of programmer-defined types may change, which creates a problem when these types are used with formatted output functions, such as `printf()`, and formatted input functions, such as `scanf()`. (See [FIO47-C. Use valid format strings](FIO47-C_%20Use%20valid%20format%20strings).)
The C `intmax_t` and `uintmax_t` types can represent any value representable by any other integer types of the same signedness. (See [INT00-C. Understand the data model used by your implementation(s)](INT00-C_%20Understand%20the%20data%20model%20used%20by%20your%20implementation_s_).) This capability allows conversion between programmer-defined integer types (of the same signedness) and `intmax_t` and `uintmax_t`:
``` cpp
mytypedef_t x;
uintmax_t temp;
temp = x; /* Always secure if mytypedef_t is unsigned*/
/* ... Change the value of temp ... */
if (temp <= MYTYPEDEF_MAX) {
  x = temp;
}
```
Formatted I/O functions can be used to input and output greatest-width integer typed values. The `j` length modifier in a format string indicates that the following `d`, `i`, `o`, `u`, `x`, `X`, or `n` conversion specifier will apply to an argument with type `intmax_t` or `uintmax_t`. C also specifies the `z` length modifier for use with arguments of type `size_t` and the `t` length modifier for arguments of type `ptrdiff_t`.
In addition to programmer-defined types, there is no requirement that an implementation provide format-length modifiers for [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-defined) integer types. For example, a machine with an implementation-defined 48-bit integer type may not provide format-length modifiers for the type. Such a machine still must have a 64-bit `long long`, with `intmax_t` being at least that large.
## Noncompliant Code Example (`printf()`)
This noncompliant code example prints the value of `x` as an `unsigned long long` value even though the value is of a programmer-defined integer type:
``` c
#include <stdio.h>
mytypedef_t x;
/* ... */
printf("%llu", (unsigned long long) x); 
```
There is no guarantee that this code prints the correct value of `x`, as `x` may be too large to represent as an `unsigned long long`.
## Compliant Solution (`printf()`)
The C `intmax_t` and `uintmax_t` can be safely used to perform formatted I/O with programmer-defined integer types by converting signed programmer-defined integer types to `intmax_t` and unsigned programmer-defined integer types to `uintmax_t`, then outputting these values using the `j` length modifier. Similarly, programmer-defined integer types can be input to variables of `intmax_t` or `uintmax_t` (whichever matches the signedness of the programmer-defined integer type) and then converted to programmer-defined integer types using appropriate range checks.
This compliant solution guarantees that the correct value of `x` is printed, regardless of its length, provided that `mytypedef_t` is an unsigned type:
``` c
#include <stdio.h>
#include <inttypes.h>
mytypedef_t x;
/* ... */
printf("%ju", (uintmax_t) x);
```
## Compliant Solution (Microsoft `printf()`)
Visual Studio 2012 and earlier versions do not support the standard `j` length modifier and do not have a nonstandard analog. Consequently, the programmer must hard code the knowledge that `intmax_t` is `int64_t` and `uintmax_t` is ` ``uint64_t` for Microsoft Visual Studio versions.
``` c
#include <stdio.h>
#include <inttypes.h>
mytypedef_t x;
/* ... */
#ifdef _MSC_VER
  printf("%llu", (uintmax_t) x);
#else
  printf("%ju", (uintmax_t) x);
#endif  
```
A feature request has been submitted to Microsoft to add support for the `j` length modifier to a future release of Microsoft Visual Studio.
## Noncompliant Code Example (`scanf()`)
This noncompliant code example reads an `unsigned long long` value from standard input and stores the result in `x`, which is of a programmer-defined integer type:
``` c
#include <stdio.h>
mytypedef_t x;
/* ... */
if (scanf("%llu", &x) != 1) {
  /* Handle error */
}
```
This noncompliant code example can result in a buffer overflow if the size of `mytypedef_t` is smaller than `unsigned long long`, or it might result in an incorrect value if the size of `mytypedef_t` is larger than `unsigned long long`.  Moreover, `scanf()` lacks the error checking capabilities of alternative conversion routines, such as `strtol()`. For more information, see [INT06-C. Use strtol() or a related function to convert a string token to an integer](https://www.securecoding.cert.org/confluence/display/seccode/INT06-C.+Use+strtol%28%29+or+a+related+function+to+convert+a+string+token+to+an+integer).
## Compliant Solution (`strtoumax()`)
This compliant solution guarantees that a correct value in the range of `mytypedef_t` is read, or an error condition is detected, assuming the value of `MYTYPEDEF_MAX` is correct as the largest value representable by `mytypedef_t`:  The `strtoumax()` function is used instead of `scanf()` as it provides enhanced error checking functionality.  The `fgets()` function is used to read input from `stdin`.
``` c
#include <stdio.h>
#include <inttypes.h>
#include <errno.h> 
mytypedef_t x;
uintmax_t temp;
/* ... */
if (fgets(buff, sizeof(buff), stdin) == NULL) {
  if (puts("EOF or read error\n") == EOF) {
    /* Handle error */
  }
} else {
  /* Check for errors in the conversion */
  errno = 0;
  temp = strtoumax(buff, &end_ptr, 10);
  if (ERANGE == errno) {
    if (puts("number out of range\n") == EOF) {
      /* Handle error */
    } 
  } else if (end_ptr == buff) {
    if (puts("not valid numeric input\n") == EOF) {
      /* Handle error */
    }
  } else if ('\n' != *end_ptr && '\0' != *end_ptr) {
    if (puts("extra characters on input line\n") == EOF) {
      /* Handle error */
    }
  }
  /* No conversion errors, attempt to store the converted value into x */
  if (temp > MYTYPEDEF_MAX) {
    /* Handle error */
  } else {
    x = temp;
  }
}
```
## Risk Assessment
Failure to use an appropriate conversion specifier when inputting or outputting programmer-defined integer types can result in buffer overflow and lost or misinterpreted data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT15-C | High | Unlikely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT15 |  |
| Compass/ROSE |  |  | Can catch violations of this rule by scanning the printf() and scanf() family of functions. For each such function, any variable that corresponds to a %d qualifier (or any qualifier besides %j) and that is not one of the built-in types (char, short, int, long, long long) indicates a violation of this rule. To catch violations, ROSE would also have to recognize derived types in expressions, such as size_t |
| LDRA tool suite | 9.7.1 | 586 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-INT15-a | Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT15-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT15-CPP. Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types |
| MITRE CWE | CWE-681, Incorrect conversion between numeric types |

## Bibliography

|  |  |
| ----|----|
| [Saks 2007c] | Standard C's Pointer Difference Type |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152075) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152334)
## Comments:

|  |
| ----|
| I don't like the phrase 'user-defined'. I believe you are referring to nonstandard integer types supported by hardware (eg your hypothetical 48-bit integer). Suggest using 'implementation-defined' instead.
                                        Posted by svoboda at Jun 06, 2008 11:44
                                     |
| No, I think it means type(def)s defined by the program, and that the first typedef has gotten reversed and should be
typedef uint_fast128_t mytypedef_t;
                                        Posted by hbf at Jun 07, 2008 12:36
                                     |
| The typedef was wrong, that's for sure.  The rule is definitely about user or programmer-defined types (maybe programmer is a better, more specific term than user?)  But perhaps this should also applied to implementation-defined types for which no length modifier is defined by the implementation.  Of course, even if a length modifier is defined it will not be portable, so perhaps this idiom of casting to max integer types should be preferred even in this case.
                                        Posted by rcs_mgr at Jun 07, 2008 14:57
                                     |
| Several touch-ups to the rule, added "#include <inttypes.h>", and s/user-defined/programmer-defined/g;
                                        Posted by svoboda at Jun 09, 2008 10:03
                                     |
| what is the first greyed out example trying to accomplish? i see temp=x and x=temp...which is a nop
                                        Posted by avolkovi at Jun 09, 2008 11:39
                                     |
| it was trying to illustrate how to convert x to temp (automatic) and temp to x (range check required). I made the code example more clear (hopefully)
                                        Posted by svoboda at Jun 09, 2008 11:53
                                     |
| The j length modifier is not supported in Visual C++, so we probably need an alternate solution for Windows.; I'm not sure how these values are printed on this platform, however.
                                        Posted by rcs_mgr at Sep 11, 2012 12:49
                                     |
| I think I fixed this, although the solution is not very elegant.; Please check if you have the chance.
                                        Posted by rcs at Sep 12, 2012 09:33
                                     |
| It might be nice to note that for standard numeric types there are defines in inttypes.h such as PRId8 that define strings for outputting them. Also, the provider of a type can provide their own defines as well.;
                                        Posted by sstewartgallus at Feb 22, 2014 00:29
                                     |
| This seems to contradict with another recommendation INT5-C . Should this suggest using;strtoimax or strtoumax instead of scanf?  
                                        Posted by gbuella at Apr 15, 2014 07:32
                                     |
| This rule and INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs;cover different, though similar, territory. This rule specifically addreses user-defined integer types, not standard types like long. INT05-C covers more issues with inputting standard integer types (or intmax_t t ypes). The only overlap is in using *scanf() to input a user-defined integer type, in which case both recommendations should be followed.
                                        Posted by svoboda at Apr 15, 2014 10:20
                                     |

