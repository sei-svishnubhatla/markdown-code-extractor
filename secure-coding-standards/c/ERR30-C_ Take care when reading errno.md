The value of `errno` is initialized to zero at program startup, but it is never subsequently set to zero by any C standard library function. The value of `errno` may be set to nonzero by a C standard library function call whether or not there is an error, provided the use of `errno` is not documented in the description of the function. It is meaningful for a program to inspect the contents of `errno` only after an error might have occurred. More precisely, `errno` is meaningful only after a library function that sets `errno` on error has returned an error code.
According to Question 20.4 of C-FAQ \[[Summit 2005](AA.-Bibliography_87152170.html#AA.Bibliography-Summit05)\],
> In general, you should detect errors by checking return values, and use `errno` only to distinguish among the various causes of an error, such as "File not found" or "Permission denied." (Typically, you use `perror` or `strerror` to print these discriminating error messages.) It's only necessary to detect errors with `errno` when a function does not have a unique, unambiguous, out-of-band error return (that is, because all of its possible return values are valid; one example is `atoi [`*`sic`*`]`). In these cases (and in these cases only; check the documentation to be sure whether a function allows this), you can detect errors by setting `errno` to 0, calling the function, and then testing `errno`. (Setting `errno` to 0 first is important, as no library function ever does that for you.)

Note that `atoi()` is not required to set the value of `errno`.
Library functions fall into the following categories:
-   Those that set `errno` and return an [out-of-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-out-of-banderrorindicator)
-   Those that set `errno` and return an [in-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-in-banderrorindicator)
-   Those that do not promise to set `errno`
-   Those with differing standards documentation
## Library Functions that Set `errno` and Return an Out-of-Band Error Indicator
The C Standard specifies that the functions listed in the following table set `errno` and return an [out-of-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-out-of-banderrorindicator). That is, their return value on error can never be returned by a successful call.
A program may check `errno` after invoking these library functions but is not required to do so. The program should not check the value of `errno` without first verifying that the function returned an error indicator. For example, `errno` should not be checked after calling `signal()` without first ensuring that `signal()` actually returned `SIG_ERR`.
**Functions That Set `errno` and Return an Out-of-Band Error Indicator**

| Function Name | Return Value | errno Value |
| ----|----|----|
| ftell() | -1L; | Positive; |
| fgetpos(), fsetpos() | Nonzero | Positive |
| mbrtowc(),;mbsrtowcs() | (size_t)(-1) | EILSEQ |
| signal() | SIG_ERR | Positive |
| wcrtomb(),;wcsrtombs() | (size_t)(-1) | EILSEQ |
| mbrtoc16(), mbrtoc32() | (size_t)(-1); | EILSEQ |
| c16rtomb(), c32rtomb() | (size_t)(-1); | EILSEQ; |

## Library Functions that Set `errno` and Return an In-Band Error Indicator
The C Standard specifies that the functions listed in the following table set `errno` and return an [in-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-in-banderrorindicator). That is, the return value when an error occurs is also a valid return value for successful calls. For example, the `strtoul()` function returns `ULONG_MAX` and sets `errno` to `ERANGE` if an error occurs. Because `ULONG_MAX` is a valid return value, the only way to confirm that an error occurred when LONG_MAX is returned is to check `errno`.
The `fgetwc()` and `fputwc()` functions return `WEOF` in multiple cases, only one of which results in setting `errno`. The string conversion functions will return the maximum or minimum representable value and set `errno` to `ERANGE` if the converted value cannot be represented by the data type. However, if the conversion cannot happen because the input is invalid, the function will return `0`, and the output pointer parameter will be assigned the value of the input pointer parameter, provided the output parameter is non-null.
A program that uses `errno` for error checking  a function that returns an in-band error indicator must set `errno` to `0` before calling one of these library functions and then inspect `errno` before a subsequent library function call.
**Functions that Set `errno` and Return an In-Band Error Indicator**

| Function Name | Return Value | errno Value |
| ----|----|----|
| fgetwc(), fputwc() | WEOF | EILSEQ |
| strtol(), wcstol() | LONG_MIN or LONG_MAX | ERANGE |
| strtoll(), wcstoll() | LLONG_MIN or LLONG_MAX | ERANGE |
| strtoul(), wcstoul() | ULONG_MAX | ERANGE |
| strtoull(), wcstoull() | ULLONG_MAX | ERANGE |
| strtoumax(),;wcstoumax() | UINTMAX_MAX | ERANGE |
| strtod(), wcstod() | 0;or ±HUGE_VAL | ERANGE |
| strtof(), wcstof() | 0;or ±HUGE_VALF | ERANGE |
| strtold(), wcstold() | 0;or ±HUGE_VALL | ERANGE |
| strtoimax(),;wcstoimax() | INTMAX_MIN, INTMAX_MAX | ERANGE |

## Library Functions that Do Not Promise to Set `errno`
The C Standard fails to document the behavior of `errno` for some functions. For example, the `setlocale()` function normally returns a null pointer in the event of an error, but no guarantees are made about setting `errno`.
After calling one of these functions, a program should not rely solely on the value of `errno` to determine if an error occurred. The function might have altered `errno`, but this does not ensure that `errno` will properly indicate an error condition. If the program does check `errno` after calling one of these functions, it should set `errno` to 0 before the function call.
## Library Functions with Differing Standards Documentation
Some functions behave differently regarding `errno` in various standards. The `fopen()` function is one such example. When `fopen()` encounters an error, it returns a null pointer. The C Standard makes no mention of `errno` when describing `fopen()`. However, POSIX.1 declares that when `fopen()` encounters an error, it returns a null pointer and sets `errno` to a value indicating the error \[[IEEE Std 1003.1-2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. The implication is that a program conforming to C but not to POSIX (such as a Windows program) should not check `errno` after calling `fopen()`, but a POSIX program may check `errno` if `fopen()` returns a null pointer.
## Library Functions and `errno`
The following uses of `errno` are documented in the C Standard:
-   Functions defined in `<complex.h>` may set `errno` but are not required to.
-   For numeric conversion functions in the `strtod`, `strtol`, `wcstod`, and `wcstol` families, if the correct result is outside the range of representable values, an appropriate minimum or maximum value is returned and the value `ERANGE` is stored in `errno`. For floating-point conversion functions in the `strtod` and `wcstod` families, if an underflow occurs, whether `errno` acquires the value `ERANGE` is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). If the conversion fails, `0` is returned and `errno` is not set.
-   The numeric conversion function `atof()` and those in the `atoi` family "need not affect the value of" `errno`.
-   For mathematical functions in `<math.h>`, if the integer expression `math_errhandling & MATH_ERRNO` is nonzero, on a domain error, `errno` acquires the value `EDOM`; on an overflow with default rounding or if the mathematical result is an exact infinity from finite arguments, `errno` acquires the value `ERANGE`; and on an underflow, whether `errno` acquires the value `ERANGE` is implementation-defined.
-   If a request made by calling `signal()` cannot be honored, a value of `SIG_ERR` is returned and a positive value is stored in `errno`.
-   The byte I/O functions, wide-character I/O functions, and multibyte conversion functions store the value of the macro `EILSEQ` in `errno` if and only if an encoding error occurs.
-   On failure, `fgetpos()` and `fsetpos()` return nonzero and store an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) positive value in `errno`.
-   On failure, `ftell()` returns `-1L` and stores an [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) positive value in `errno`.
-   The `perror()` function maps the error number in `errno` to a message and writes it to `stderr`.
The POSIX.1 standard defines the use of `errno` by many more functions (including the C standard library function). POSIX also has a small set of functions that are exceptions to the rule. These functions have no return value reserved to indicate an error, but they still set `errno` on error. To detect an error, an application must set `errno` to `0` before calling the function and check whether it is nonzero after the call. Affected functions include `strcoll()`, `strxfrm()`, `strerror()`, `wcscoll()`, `wcsxfrm()`, and `fwide()`. The C Standard allows these functions to set `errno` to a nonzero value on success. Consequently, this type of error checking should be performed only on POSIX systems.
## Noncompliant Code Example (`strtoul()`)
This noncompliant code example fails to set `errno` to `0` before invoking `strtoul()`. If an error occurs, `strtoul()` returns a valid value (`ULONG_MAX`), so `errno` is the only means of determining if `strtoul()` ran successfully.
``` c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
void func(const char *c_str) {
  unsigned long number;
  char *endptr;
  number = strtoul(c_str, &endptr, 0);
  if (endptr == c_str || (number == ULONG_MAX 
                         && errno == ERANGE)) {
    /* Handle error */
  } else {
    /* Computation succeeded */
  }
}
```
Any error detected in this manner may have occurred earlier in the program or may not represent an actual error.
## Compliant Solution (`strtoul()`)
This compliant solution sets `errno` to `0` before the call to `strtoul()` and inspects `errno` after the call:
``` c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
void func(const char *c_str) {
  unsigned long number;
  char *endptr;
  errno = 0;
  number = strtoul(c_str, &endptr, 0);
  if (endptr == c_str || (number == ULONG_MAX 
                         && errno == ERANGE)) {
    /* Handle error */
  } else {
    /* Computation succeeded */
  }
}
```
## Noncompliant Code Example (`ftell()`)
This noncompliant code example, after calling `ftell()`, examines `errno` without first checking whether the out-of-band indicator returned by `ftell() `indicates an error.
``` c
#include <errno.h>
#include <stdio.h>
void func(FILE* fp) { 
  errno=0;
  ftell(fp);
  if (errno) {
    perror("ftell");
  }
}
```
## Compliant Solution (`ftell()`)
This compliant solution first detects that `ftell() `failed using its out-of-band error indicator. Once an error has been confirmed, reading `errno` (implicitly by using the `perror()` function) is permitted.
``` c
#include <errno.h>
#include <stdio.h>
void func(FILE* fp) { 
  if (ftell(fp) == -1) {
    perror("ftell");
  }
}
```
## Noncompliant Code Example (`fopen()`)
This noncompliant code example may fail to diagnose errors because `fopen()` might not set `errno` even if an error occurs:
``` c
#include <errno.h>
#include <stdio.h>
void func(const char *filename) {
  FILE *fileptr;
  errno = 0;
  fileptr = fopen(filename, "rb");
  if (errno != 0) {
    /* Handle error */
  }
}
```
## Compliant Solution (`fopen()`, C)
The C Standard makes no mention of `errno` when describing `fopen()`. In this compliant solution, the results of the call to `fopen()` are used to determine failure and `errno` is not checked:
``` c
#include <stdio.h>
void func(const char *filename) {
  FILE *fileptr = fopen(filename, "rb");
  if (fileptr == NULL)  {
    /* An error occurred in fopen() */
  }
}
```
## Compliant Solution (`fopen()`, POSIX)
In this compliant solution, `errno` is checked only after an error has already been detected by another means:
``` c
#include <errno.h>
#include <stdio.h>
void func(const char *filename) {
  FILE *fileptr;
  errno = 0;
  fileptr = fopen(filename, "rb");
  if (fileptr == NULL)  {
    /*
     * An error occurred in fopen(); now it's valid 
     * to examine errno.
     */
    perror(filename);
  }
}
```
## Risk Assessment
The improper use of `errno` may result in failing to detect an error condition or in incorrectly identifying an error condition when none exists.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR30-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | errno-reset | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ERR30 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.RC | Redundant Condition |
| Compass/ROSE |  |  | Could detect violations of this rule by ensuring that each library function is accompanied by the proper treatment of errno |
| Coverity | 2017.07 | MISRA C 2012 Rule 22.8MISRA C 2012 Rule 22.9MISRA C 2012 Rule 22.10 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-err30-c |  |
| Helix QAC | 2024.4 | C2500, C2501, C2502, C2503;C++3172, C++3173, C++3174, C++3175, C++3176, C++3177, C++3178, C++3179, C++3183, C++3184 |  |
| Klocwork | 2024.4 | CXX.ERRNO.NOT_SETCXX.ERRNO.NOT_CHECKED
CXX.ERRNO.INCORRECTLY_CHECKED |  |
| LDRA tool suite | 9.7.1 | 111 D, 121 D, 122 D, 132; D, 134 D
 | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR30-a | Properly use errno value |
| Polyspace Bug Finder | R2024a | CERT C: Rule ERR30-C | Checks for:Misuse of errnoErrno not resetRule fully covered. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | EXP12-C. Do not ignore values returned by functions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Incorrectly setting and using errno [inverrno] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-456, Missing Initialization of a Variable | 2017-07-05: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-456 and ERR30-C
CWE-456 = EXP33-C
CWE-456 = Union( ERR30-C, list) where list =
-   Reading potentially uninitialized variables besides errno
### CWE-248 and ERR30-C
Intersection( CWE-248, ERR30-C) = Ø
CWE-248 is only for languages that support exceptions.  It lists C++ and Java, but not C.
## Bibliography

|  |  |
| ----|----|
| [Brainbell.com] | Macros and Miscellaneous Pitfalls |
| [Horton 1990] | Section 11, p. 168Section 14, p. 254 |
| [IEEE Std 1003.1-2013] | XSH, System Interfaces, fopen |
| [Koenig 1989] | Section 5.4, p. 73 |
| [Summit 2005] |  |

------------------------------------------------------------------------
[](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152125)
## Attachments:
![](images/icons/bullet_blue.gif) [Bold.url](attachments/87152351/335675458.url) (application/octet-stream)  
## Comments:

|  |
| ----|
| This would be a good place to state that applications should not try to use errno to report their own error codes.
                                        Posted by dagwyn at Apr 18, 2008 13:17
                                     |
| I agree with the sentiment, which is sort of captured by this recommendation:
DCL09-C. Declare functions that return errno with a return type of errno_t
I'm having trouble figuring out how to incorporate it into this recommendation, because no interface is defined.  
                                        Posted by rcs_mgr at Apr 19, 2008 15:03
                                     |
| The text describing the 2nd NCCE pair doesn't match the code. It warns that a C library function may set errno even if no error occurs...is this in the standard? And it doesn't illustrate what the NCCE & CCE seem to be illustrating, that you shouldn't rely on errno if the library function (fopen() in this case) provides an in-band error indicator (a NULL pointer).
                                        Posted by svoboda at Jul 25, 2008 16:53
                                     |
| Fixed.
What it said about functions setting errno even if no error occurs was just a less accurate repeat of what the second sentence at the top of the page says (which closely matches what C99 says).
                                        Posted by geoffclare at Jul 26, 2008 05:20
                                     |
| The new text describing a ROSE algorithm made me realise that part of this rule is too strict.  It says
A program that uses errno for error checking should set it to zero before a library function call and then inspect it before a subsequent library function call.
However, it is only necessary to set errno to zero before the call if the value returned by the call as an error indication is also a valid return value, as in the strtoul() example with return value ULONG_MAX.
Also the final statement in the ROSE algorithm is problematic:
Furthermore, one can check that errno isn't set or tested near a function that doesn't set it, like fopen().
because there are C99 functions for which C99 doesn't require errno to be set but POSIX does.  ROSE would need to know whether the code is targeted at a pure C99 implementation or a POSIX implementation.
                                        Posted by geoffclare at Jul 26, 2008 05:32
                                     |
| The sentence starting with "It might be more reasonable" under Automated Detection reads funny, and I'm not sure what it's trying to say, since it seems so similar to the previous sentence.
                                        Posted by christey at Jul 26, 2008 15:14
                                     |
| Rewrote the ROSE section...since we are considering three types of functions (see the ROSE section for details). Perhaps these three types of functions should be described in the rule itself (and not just wrt ROSE).
                                        Posted by svoboda at Jul 28, 2008 09:06
                                     |
| Yes, I think the rule should cover those three types of functions.  (I tweaked their descriptions in the ROSE section).
Also the rule name needs to change to something more general, e.g. "Handle errno appropriately for the error reporting characteristics of each function".
                                        Posted by geoffclare at Jul 28, 2008 12:23
                                     |
| Right, unless we have a table/list of these, it's going to be hard to write the actual code...
                                        Posted by avolkovi at Jul 28, 2008 16:40
                                     |
| ok this rule now discusses differing behavior of these functions
especially fopen(), which sets errno in POSIX but doesn't in pure C99.
                                        Posted by svoboda at Jul 29, 2008 14:28
                                     |
| I removed that part about functions that only indicate errors via errno from the main three function types, as I believe there are no such functions in C99, only POSIX.  They are covered in the section about POSIX, where it says they are an exception to the rule.
The choice of printf() as an example in "Library Functions that don't promise to set errno" is unfortunate, since it is one of the byte input/output functions and C99 requires those to set errno to EILSEQ when an encoding error occurs.  (It is one of the bullet points under "Library Functions and errno".)
The new rule name is better, but still doesn't match the details within the rule.  E.g. it doesn't cover the part of the rule about not checking errno for "Library Functions that don't promise to set errno".  I still think it should be changed to something more general like "Handle errno appropriately for the error reporting characteristics of each function".
                                        Posted by geoffclare at Jul 31, 2008 06:53
                                     |
| 
I removed that part about functions that only indicate errors via errno from the main three function types, as I believe there are no such functions in C99, only POSIX. They are covered in the section about POSIX, where it says they are an exception to the rule.
Your changes are good, but it doesn't look to me like you removed any significant parts.
The choice of printf() as an example in "Library Functions that don't promise to set errno" is unfortunate, since it is one of the byte input/output functions and C99 requires those to set errno to EILSEQ when an encoding error occurs. (It is one of the bullet points under "Library Functions and errno".)
I see it in the bullet point, but I don't see anything in C99 about EILSEQ and printf/fprintf. Perhaps the standard links errno & printf elsewhere, but not in the printf section (7.19.6.1). Besides, while printf might set errno if an encoding error occurs, would it set errno if anything else happens (eg what if the stdout is closed?).
I thought the atoi() family of functions was considered 'deprecated', in lieu of the strtoul() family...that's why I didn't want to use atoi() as an example function that doesn't set errno. I take it from your comment that there isn't a function (in C99) that doesn't use errno to indicate errors...is there a good POSIX function we can use in our NCCE/CCE pair instead of printf()?A
The new rule name is better, but still doesn't match the details within the rule. E.g. it doesn't cover the part of the rule about not checking errno for "Library Functions that don't promise to set errno". I still think it should be changed to something more general like "Handle errno appropriately for the error reporting characteristics of each function".
Title is shorter, and hopefully, more accurate.
                                        Posted by svoboda at Jul 31, 2008 10:41
                                     |
| about the sentence after the first NCCE(strtoul()),Any error detected in this manner may have occurred earlier in the program or may not represent an actual error.how about omitting the latter part ("or may not represent an actual error"), or changing the sentence to"Any error detected in this manner may have occurred earlier in the program and not represent an actual error."I want to confirm if I understand correctly the intention of this sentence...I guess there are only three situations possible here, as detected as error.nothing's been converted, hence endptr == stringthe string (or a part of the string) indicates too big value to represent in unsigned longthe string (or a part of the string) is converted successfully to ULONG_MAX, but errno was previously set to ERANGE;
                                        Posted by yozo at Nov 28, 2012 07:20
                                     |
| See ERR34-C. Detect errors when converting a string to a number for a more comprehensive code example about the proper use of strtoul(). In particular, it is also possible for strtoul() to make a successful conversion but still leave garbage characters in the input string...this may or may not be an error depending on your circumstances.It is possible that errno is set by some older routine and so it indicates an error, but not one in strtoul(). It is also possible (though unlikely) that the routine set errno erroneously and so it does not actually indicate an error. So I still believe the sentence is most correct as it is currently written.
                                        Posted by svoboda at Nov 28, 2012 10:33
                                     |
| ;Affected functions include strcoll(), strxfrm(), strerror(), wcscoll(), wcsxfrm(), and fwide(). The C Standard allows these functions to set errno to a nonzero value on success.I have checked C90 and C11 standards and I could not find anything describing behavior of functions strcoll(), strxfrm(), wcscoll(), wcsxfrm() with respect to errno. What have I missed?
                                        Posted by karbyshev at Feb 01, 2018 11:07
                                     |
| The POSIX standard specifies some of the behavior of these functions with errno.
                                        Posted by svoboda at Feb 02, 2018 17:25
                                     |
| Could you please clarify, if it is required by the rule that every call to a function that returns an in-band error indicator is followed by an errno-check.
                                        Posted by karbyshev at Feb 08, 2018 07:47
                                     |
| These two sentences in the intro clarify things:It is meaningful for a program to inspect the contents of errno only after an error might have occurred. More precisely, errno is meaningful only after a library function that sets errno on error has returned an error code.In particular, if your function returns an in-band error indicator, then setting & checking errno is not required. It is only required that you check the return value for errors, because that indicates *if* an error occurs. Typically this function does not precisely indicate *which* error occurred, and if you want that information, then you set errno before the call and check it afterwards.
                                        Posted by svoboda at Feb 08, 2018 09:53
                                     |
| Let me summarize my current understanding of the rule's requirements:For both classes of functions that return in-/out-of-band error indicators, if;the value of errno is checked after the function call then the rule requires thaterrno is set to 0 before the callthe returned value is checked against a corresponding error indicator value before the errno checkThe rule does not require that a possible error is detected (as this is the subject of ERR33-C).Is my understanding correct?
                                        Posted by karbyshev at Feb 08, 2018 13:32
                                     |
| Yes! This correctly describes how to handle in-band and out-of-band functions.
                                        Posted by svoboda at Feb 08, 2018 14:11
                                     |
| Thanks!;
                                        Posted by karbyshev at Feb 08, 2018 18:29
                                     |
| In table;Functions That Set errno and Return an Out-of-Band Error Indicator, the function name should be c32rtomb, not cr32rtomb
                                        Posted by karbyshev at Mar 22, 2018 10:35
                                     |
| Fixed, thanks
                                        Posted by svoboda at Mar 22, 2018 12:06
                                     |
| In the two bullet items:Those that set errno and return and;out-of-band error indicatorThose that set errno and return and in-band error indicatorshould the words here 'and' actually be 'an'?
                                        Posted by morano at Jun 12, 2018 18:38
                                     |
| Agreed, fixed.
                                        Posted by svoboda at Jun 13, 2018 09:14
                                     |
| Could you, please, explain the reasoning behind the following part of the description (in the "Library Functions that Set errno and Return an Out-of-Band Error Indicator" section):The program should not check the value of;errno without first verifying that the function returned an error indicator. For example, errno should not be checked after calling signal() without first ensuring that signal() actually returned SIG_ERR.Standard seems to clearly state for these kind of functions that - in case of an error - they return given value and set non-zero value of errno. As I understand, that implies that the value of errno remains unchanged when the call is successful.The following code is IMHO correct (correctly checks erroneous situation):    long test(FILE* file)
    {
        long pos;
        errno = 0;
        pos = ftell(file);
        if (0 != errno) {
            // Handle error...
        }
        return pos;
    }

Is the intention to treat this as non-compliant with this rule?
![](images/icons/contenttypes/comment_16.png) Posted by rozenau at Feb 01, 2019 15:08
\| \|
Michal: Yes, this code violates this rule. The text associated with;`ftell()` says:
> A program may set and check `errno` for these library functions but is not required to do so. The program should not check the value of `errno` without first verifying that the function returned an error indicator. For example, `errno` should not be checked after calling `signal()` without first ensuring that `signal()` actually returned `SIG_ERR`.

The caveat is that a platform is free to have ftell() set errno to a nonzero value even if it succeeds. In that case your program will "handle error" even though ftell() succeeded. So you should first check that pos is -1 (as a signed long), before reading errno.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 01, 2019 18:47
\| \|
When I look at C11 standard, in 7.5 #3 there is:
> The value of errno in the initial thread is zero at program startup (the initial value oferrno in other threads is an indeterminate value), but is never set to zero by any library  
> function. The value of errno may be set to nonzero by a library function call  
> whether or not there is an error, provided the use of errno is not documented in the  
> description of the function in this International Standard.

and then, e.g. for ftell in 7.21.9.4, #3:
> If successful, the ftell function returns the current value of the file position indicator  
> for the stream. On failure, the ftell function returns −1L and stores an  
> implementation-defined positive value in errno.

As I understand, it implies that the ftell function cannot change the value of errno if there is no error.
Could you, please, provide some reference to the standard that allows such platform-specific behavior? Or maybe there are some known non-compliant implementations we should guard against?
![](images/icons/contenttypes/comment_16.png) Posted by rozenau at Feb 03, 2019 14:50
\| \|
Michal: It sounds like you have already cited the most relevant parts of the standard.
Offhand, your interpretation (that 7.21.9.4 precludes ftell from setting errno when it succeeds) seems reasonable.;  But I could see a platform writer arguing that that section is loose enough to allow their ftell() to set errno and yet return a successful value.
Next to the standard, there is the C FAQ \[[Summit 2005](https://wiki.sei.cmu.edu/confluence/display/c/AA.+Bibliography#AA.Bibliography-Summit05)\], whose most relevant errno information is already quoted in this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 05, 2019 14:51
\| \|
Can we have a list of functions (like `atoi`) from the standard library which return an in-band error indicator **and** do not set `errno `(or any other error indicator) recommending users not to use them?  
Such a list can even list the corresponding recommended alternatives.
![](images/icons/contenttypes/comment_16.png) Posted by rootkea at Mar 31, 2022 00:45
\| \|
> Can we have a list of functions

No, in the sense that we do not provide such a list in the CERT C rules.
Yes, in that the ISO draft standards are freely available and so you (or anyone else) can build such a list yourself :)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 31, 2022 08:04
\| \|
Well, one can build a list of functions which return an in-band error indicator and set the `errno` from ISO draft standards too. But still we provided such a list in this very article.  
A list of functions returning an in-band error indicator and **not** setting the `errno` (or any other error indicator) is more interesting from secure coding perspective IMHO. Because there's no way to detect if such a function failed or not. E.g. `atoi.`
![](images/icons/contenttypes/comment_16.png) Posted by rootkea at Mar 31, 2022 08:32
\| \|
See;[ERR34-C. Detect errors when converting a string to a number](ERR34-C_%20Detect%20errors%20when%20converting%20a%20string%20to%20a%20number) for details on atoi() and why we recommend against it.
I suspect this list is small for the reasons  you cite.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 31, 2022 09:08
\| \|
> I suspect this list is small for the reasons you cite.

May be.
But do you think such a list is indeed interesting and should be compiled? We can even put that list in this very article under the section "Library Functions that Do Not Promise to Set errno" with a note like "additionally, these functions;\[the functions from that list\] return an in-band error indicator and so offer no way to detect failures. Therefore should be avoided".
![](images/icons/contenttypes/comment_16.png) Posted by rootkea at Mar 31, 2022 09:43
\| \|
Such a list will be mildly interesting, and will include many common functions, like fgetc() and atoi(). We do warn about usage of many such functions...if you know of one that isn't addressed somewhere in the CERT standards, I'd like to hear it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 31, 2022 10:37
\| \|
Avinash,
The scope of this rule is functions that set `errno`, and how to use these functions securely.; Functions that do not set `errno` are outside of the scope of this rule, as is recommending to not use some functions that are outside of the scope of this rule.  Such a guideline or recommendation would need to be considered with the other existing rules and recommendations, as well as a consideration of the specific security benefit.  As Dave is referring to, that is currently done on a case-by-case basis for specific functions. If you compiled the list, and added it here as a comment, it would effectively be available as your contribution to something that might be useful to some readers.
Thanks.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Apr 05, 2022 12:28
\| \|
Incidentally, we already have such a recommendation and the list! Guess I should've searched first before starting this discussion thread.[https://wiki.sei.cmu.edu/confluence/display/c/ERR07-C.+Prefer+functions+that+support+error+checking+over+equivalent+functions+that+don't](https://wiki.sei.cmu.edu/confluence/display/c/ERR07-C.+Prefer+functions+that+support+error+checking+over+equivalent+functions+that+don)
![](images/icons/contenttypes/comment_16.png) Posted by rootkea at Apr 17, 2022 23:45
\| \|
Avinash,
I'm not convinced this list is exactly what you asked for in your original post about functions that provide an;[in-band error indicator](https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-in-banderrorindicator). See the definition at that link. Technically, since atoi() returns 0 for some errors, which is indistinguishable from an inputted 0, it is not a function that provides a reliable in-band error indicator.
But, I'm glad the list in ERR07-C supports some of your needs (or perhaps all of what you intended).
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Apr 18, 2022 11:21
\| \|
It is far from clear to me why it is recommended to set errno to 0 before making a call that returns an in-band errror indicator.; For example, what could go wrong with the following?
if (ftell(fp) == -1)
   perror("ftell");
As far as I can tell, this is non-compliant according to this rule because it doesn't set errno=0 before calling ftell(), and yet it goes on to call perror() if the call fails. Is this rule really saying that errno=0 is necessary here?  If so, I think there is a whole lot of non-compliant code out there. In my experience, setting errno to zero is almost never done.
I've read over this rule many times and if the reason for setting errno to zero  is given, it's sailing right over my head.  I do understand why it is necessary in those cases where the called function returns an in-band error indicator, but to my mind, those are the **only**  cases where it should be required.
![](images/icons/contenttypes/comment_16.png) Posted by edougra at Jun 24, 2022 11:45
\| \|
I assume you meant "out-of-band" in your first sentence. Given that, I agree that it seems unnecessary.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 24, 2022 15:41
\| \|
When calling a function, you must follow this rule (eg set errno to 0 before the call and check the value of errno ;afterwards) specifically for functions whose only way of determining if an error occurred is with errno. This could either be because their documentation explicitly says so, or because they return an in-band error indicator (eg the return value could indicate failure or success).
You must not check errno for functions that do not guarantee that they set errno (such as ISO C's definition of fopen().
You need not check errno for functions that give an out-of-band error indicator. If you do, you should set errno to 0 before calling the function, to make sure that only the function could have set errno to a nonzero value.
UPDATE: I'll agree that this rule's current normative text is confusing...if we agree that what I wrote is more clear, I'll update the rule accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 24, 2022 16:00
\| \|
Oops.; Joseph is corrrect. I did mean out-of-band in my first sentence.
I still do not understand the reasoning in your second last sentence. Specifically this part: "If you do, you should set errno to 0 before calling the function, to make sure that only the function could have set errno to a nonzero value".  A function like ftell() is documented to return -1 and set errno on failure.  I understand that I should not examine errno unless ftell has returned -1 indicating failure, but if it has  returned -1, then what does setting errno to 0 before the call acomplish?  If ftell() sets errno, then it doesn't matter what I set it to before the failure; the value of errno when I call perror() will be whatever ftell() set it to. If ftell() does not set errno on failure, then it is not behaving as documented.  Setting errno to 0 might change perror's output from "Function not implemented" (if errno happened to contain ENOSYS) to "Success", but if functions like ftell() don't do what they are documented to do, then all bets are off anyway.
I bring this up because I recently found a bug in mq_timedreceive() in glibc 2.33 where if it is called with errno set to ENOSYS, it will misbehave (it will make one syscall with a 64 bit timestamp and then another with a 32 bit timestamp).  Somebody was arguing that it wasn't really a bug in mq_timedreceive() because if I had been following this rule, then I never would have called mq_timedreceive() with errno set to anything other than zero anyway.  That isn't necessarily true because you don't require errno to be set to 0 unless it will be examined after the call, but this still got me wondering when it would ever make sense to set errno to 0 before a call that returns an out-of-band error indication (like mq_timedreceive).
![](images/icons/contenttypes/comment_16.png) Posted by edougra at Jun 24, 2022 16:49
\| \|
Given that ftell() is \*required\* to set errno if it returns -1, setting errno to 0 beforehand is technically unnecessary.
However, setting errno to 0 before calling ftell() is still good defense-in-depth programming. The argument is that setting errno to 0 before calling a function prevents a nasty scenario where you call the function, check errno, see that it is nonzero, and assume the function must have failed, when errno could have been nonzero before the call. ;As the rule notes, many functions leave unspecified whether they do or do not set errno.  This is why we de-prioritize checking errno (don't check it if the function has a better way of indicating errors).
That said, I would revise my final paragraph to say:
You need not check errno for functions that give an out-of-band error indicator. If you do, we do recommend that you set errno to 0 before calling the function, to make sure that only the function could have set errno to a nonzero value. (Setting errno to 0 is not strictly necessary; it is merely a good defense-in-depth strategy).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 24, 2022 20:31
\| \|
C23 s7.5p3 says:
;   The value of errno may be set to nonzero by a library function  
    call whether or not there is an error, provided the use of errno is  
    not documented in the description of the function in this  
    document.
The above paragraph does suggest that C standard functions are free to take liberties reading and writing errno beyond what is explicitly documented...eg a C function could alter unspecified behavior based on the current value of errno (as long as it still performs the behavior explicitly documented.)
Which brings us to mq_timedreceive(). Since mq_timedreceive() is not a C standard function, I have no idea what requirements it enforces wrt errno.  It would stand to reason that if its behavior changes when errno is nonzero, this property should be documented.  Rule ERR30-C recommends zeroing errno to prevent stale values of errno from being misinterpreted, not to prevent unexpected behavior of functions based on a nonzero errno value.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 24, 2022 20:31
\| \|
Well....Ok I guess.; So you're suggesting that it's a good idea to set errno to 0 first in case you forget to check the out-of-band error indicator after the call and go ahead and examine errno anyway?  If that's what you mean, then I think this set errno to zero business should be moved to a footnote and should not be mentioned in the rule's title. Mentioning it in the title takes the focus away from what the rule is really trying to say. I think your proposed rewording is a good step forward, but I don't think it goes far enough.
Perhaps you could also provide an example like my original ftell() example and state clearly whether that example is compliant with this rule or not.  It would obviously be noncompliant if ftell's return value was not checked before errno was examined, but that would be true whether errno were set to 0 first or not. eg:
ftell(fp); if (errno) perror("ftell");                   /\* noncompliant. Examines errno without checking out-of-band indicator first \*/
errno=0; ftell(fp); if (errno) perror("ftell");    /\* noncompliant. Examines errno without checking out-of-band indicator first \*/
if (ftell(fp) == -1) perror("ftell");                   /\* noncompliant?   Does not set errno to zero before the call \*/
errno = 0; if (ftell(fp) == -1) perror("ftell");  /\* compliant at last. \*/
Is it really your intent to declare the third of these examples noncompliant?  In my experience, that's what 99% of real world code actually does.  Although I do admit that I'm mostly talking about POSIX calls like mq_timedreceive(), which, just like ftell(), are documented to return -1 on failure, with errno set appropriately.
Please note that I am talking only about functions that return out-of-band error indicators and that promise to set errno on error.  Most or all POSIX system calls fall into this category. I am not talking about functions that alter errno in undocumented ways.  I know that this document is about standard C and not POSIX, but people still draw lessons from this about how to program with POSIX, and rightfully so I think. I can't think of any reason the rules should be any different for POSIX programming than they are for standard C.
![](images/icons/contenttypes/comment_16.png) Posted by edougra at Jun 24, 2022 23:27
\| \|
OK, I have changed the rule title. Unfortunately the normative text is too complicated to fit in the title, so I made it purposefully vague :) ;I have also verified that the four categories of functions listed each has a normative paragraph saying how errno should be handled.  Finally, I also added a noncompliant code example & compliant solution involving ftell() based on your code examples.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 26, 2022 15:05
\| \|
Thanks! Looks good to me now.
![](images/icons/contenttypes/comment_16.png) Posted by edougra at Jun 27, 2022 10:44
\| \|
For functions with out-of bound error indicators, it does not seem required to set errno to 0 before the call.After the check of the return value in fact the error surely happened and errno cannot have a spurious value  
That's what I see in **Compliant Solution (`ftell()`)**
![](images/icons/contenttypes/comment_16.png) Posted by mbaluda at Oct 20, 2022 19:09
\| \|
It would be nice to have compliant and noncompliant examples for the setlocale() case.My interpretation is that if we decide to check `errno` after the call then we need to both:  
a) check the return value against null  
b) set errno to zero before the call
![](images/icons/contenttypes/comment_16.png) Posted by mbaluda at Oct 20, 2022 19:21
\| \|
According to ISO C, the setlocale() function makes no promise of setting errno, so it would not be good to showcase in this rule. Instead, see rule [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) for some examples of how to use setlocale().
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 21, 2022 08:12
\| \|
Yes, a lot more is explained about this in the two comment threads below started by Doug Graham from June 2022.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Dec 28, 2022 17:34
\|
