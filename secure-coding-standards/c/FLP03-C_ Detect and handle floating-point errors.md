Errors during floating-point operations are often neglected by programmers who instead focus on validating operands before an operation. Errors that occur during floating-point operations are admittedly difficult to determine and diagnose, but the benefits of doing so often outweigh the costs. This recommendation suggests ways to capture errors during floating-point operations.
The following code exhibits undefined behavior:
``` java
int j = 0;
int iResult = 1 / j;
```
On most implementations, integer division by zero is a terminal error, commonly printing a diagnostic message and aborting the program:
``` java
double x = 0.0;
double dResult = 1 / x;
```
Floating-point division by zero also results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), although most [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) do not treat it as a terminal error. If additional precautions are not taken, it results in a silent error.
The most portable way to determine if a floating-point exceptional condition has occurred is to use the floating-point exception facilities provided by C in `fenv.h`.
However, the C floating-point exception functions are not without problems. The following caveats exist regarding the interaction between floating-point exceptions and conversions:
-   Conversion from floating-point to integer may cause an "invalid" floating-point exception. If this occurs, the value of that integer is undefined and should not be used.
-   Most implementations fail to raise "invalid" for conversions from any negative or "large" positive floating-point values to unsigned integer types or to `signed char`. (See [tflt2int.c](http://www.tybor.com/tflt2int.c).)
-   When a noninteger floating-point value is converted to an integer, the "inexact" floating-point exception is raised.
For information regarding floating-point number conversions, see [FLP34-C. Ensure that floating-point conversions are within range of the new type](FLP34-C_%20Ensure%20that%20floating-point%20conversions%20are%20within%20range%20of%20the%20new%20type).
The C Standard does not require all implementations to support floating-point exceptions. Each exception macro in `fenv.h` is defined if, and only if, the corresponding exception is supported. Only implementations that use IEC 60559 (formerly IEEE-754) floating-point arithmetic are required to support all five exceptions defined by C (see the C Standard, subclause 7.6.2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]). Nevertheless, these functions are the most portable solution for handling floating-point exceptions.
A less portable but potentially more secure solution is to use the capabilities provided by the underlying implementation. If this approach is taken, the caveats of that system must be well understood. The following table provides a starting point for some common operating systems:

| Operating System | How to Handle Floating-Point Errors |
| ----|----|
| LinuxSolaris 10
AIX 5.3
HP-UX 11.31
Mac OS X 10.5 | Use the C floating-point exception functions |
| Windows | Use either the C floating-point exception functions or structured exception handling through _fpieee_flt [MSDN] |

## Noncompliant Code Example
In this noncompliant code example, floating-point operations are performed without checking for errors. Note that range checking has been intentionally omitted because the intent is to detect errors following the floating-point operation.
``` c
void fpOper_noErrorChecking(void) {
  /* ... */
  double a = 1e-40, b, c = 0.1;
  float x = 0, y;
  /* Inexact and underflows */
  y = a;
  /* Divide-by-zero operation */
  b = y / x;
  /* Inexact (loss of precision) */
  c = sin(30) * a;
  /* ... */
}
```
However, exceptional conditions (as indicated by the comments) occur that may lead to unexpected arithmetic results.
## Compliant Solution (C)
This compliant solution uses C Standard functions to handle floating-point errors:
``` c
#include <fenv.h>
#pragma STDC FENV_ACCESS ON
void fpOper_fenv(void) {
  double a = 1e-40, b, c = 0.1;
  float x = 0, y;
  int fpeRaised;
  /* ... */
  feclearexcept(FE_ALL_EXCEPT);
  /* Store a into y is inexact and underflows: */
  y = a;
  fpeRaised = fetestexcept(FE_ALL_EXCEPT);
  /* fpeRaised has FE_INEXACT and FE_UNDERFLOW */
  feclearexcept(FE_ALL_EXCEPT);
  /* Divide-by-zero operation */
  b = y / x;
  fpeRaised = fetestexcept(FE_ALL_EXCEPT);
  /* fpeRaised has FE_DIVBYZERO */
  feclearexcept(FE_ALL_EXCEPT);
  c = sin(30) * a;
  fpeRaised = fetestexcept(FE_ALL_EXCEPT);
  /* fpeRaised has FE_INEXACT */
  feclearexcept(FE_ALL_EXCEPT);
  /* ... */
}
```
## Compliant Solution (Windows)
Microsoft Visual Studio 2008 and earlier versions do not support C functions to handle floating-point errors. Windows provides an alternative method using `_statusfp()`, `_statusfp2()`, and `_clearfp()`.
``` c
void fpOper_usingStatus(void) {
  /* ... */
  double a = 1e-40, b, c;
  float x = 0, y;
  unsigned int rv = _clearfp();
  /* Store into y is inexact and underflows: */
  y = a;
  rv = _clearfp();  /* rv has _SW_INEXACT and _SW_UNDERFLOW */
  /* Zero-divide */
  b = y / x; rv = _clearfp(); /* rv has _SW_ZERODIVIDE */
  /* Inexact */
  c = sin(30) * a; rv = _clearfp(); /* rv has _SW_INEXACT */
  /* ... */
}
```
## Compliant Solution (Windows SEH)
Microsoft Visual Studio 2008 also uses structured exception handling (SEH) to handle floating-point operations. SEH provides more information about the error and allows the programmer to change the results of the floating-point operation that caused the error condition.
``` c
void fp_usingSEH(void) {
  /* ... */
  double a = 1e-40, b, c = 0.1;
  float x = 0, y;
  unsigned int rv ;
  unmask_fpsr();
  _try {
    /* Store into y is inexact and underflows: */
    y = a;
    /* Divide-by-zero operation */
    b = y / x;
    /* Inexact */
    c = sin(30) * a;
  }
  _except (_fpieee_flt(
             GetExceptionCode(),
             GetExceptionInformation(),
             fpieee_handler)) {
  {
  printf ("fpieee_handler: EXCEPTION_EXECUTE_HANDLER");
  }
  /* ... */
}
void unmask_fpsr(void) {
  unsigned int u;
  unsigned int control_word;
  _controlfp_s(&control_word, 0, 0);
  u = control_word & ~(_EM_INVALID
                     | _EM_DENORMAL
                     | _EM_ZERODIVIDE
                     | _EM_OVERFLOW
                     | _EM_UNDERFLOW
                     | _EM_INEXACT);
  _controlfp_s( &control_word, u, _MCW_EM);
  return ;
}
int fpieee_handler(_FPIEEE_RECORD *ieee) {
  /* ... */
  switch (ieee->RoundingMode) {
    case _FpRoundNearest:
      /* ... */
      break;
      /*
       * Other RMs include _FpRoundMinusInfinity,
       * _FpRoundPlusInfinity, _FpRoundChopped.
       */
      /* ... */
    }
  switch (ieee->Precision) {
    case _FpPrecision24:
      /* ... */
      break;
      /* Other Ps include _FpPrecision53 */
      /* ... */
    }
   switch (ieee->Operation) {
     case _FpCodeAdd:
       /* ... */
       break;
       /* 
        * Other Ops include _FpCodeSubtract, _FpCodeMultiply,
        * _FpCodeDivide, _FpCodeSquareRoot, _FpCodeCompare,
        * _FpCodeConvert, _FpCodeConvertTrunc.
        */
       /* ... */
    }
  /* 
   * Process the bitmap ieee->Cause.
   * Process the bitmap ieee->Enable.
   * Process the bitmap ieee->Status.
   * Process the Operand ieee->Operand1, 
   * evaluate format and Value.
   * Process the Operand ieee->Operand2, 
   * evaluate format and Value.
   * Process the Result ieee->Result, 
   * evaluate format and Value.
   * The result should be set according to the operation 
   * specified in ieee->Cause and the result formatted as 
   * specified in ieee->Result.
   */
  /* ... */
}
```
## Risk Assessment
Undetected floating-point errors may result in lower program efficiency, inaccurate results, or software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Most processors stall for a significant duration when an operation incurs a NaN (not a number) value.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP03-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | float-division-by-zero | Partially checked |
| Compass/ROSE |  |  | Could detect violations of this rule by ensuring that floating-point operations are surrounded by feclearexcept() and fetestexcept(). It would need to look for type conversions to float or double, divisions (by a number not known to be nonzero), and multiplication. It may be wisest to apply this to all floating-point operations in general |
| LDRA tool suite | 9.7.1 | 43 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FLP03-aCERT_C-FLP03-b
CERT_C-FLP03-c
CERT_C-FLP03-d | Avoid division by zeroAvoid implicit conversions from wider to narrower floating type
Avoid implicit conversions from narrower to wider floating type
Avoid implicit conversions of floating point numbers from wider to narrower floating type |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 736, 9120, 9227 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rec. FLP03-C | Checks for:Float conversion overflowFloat overflowFloat division by zeroRec. partially covered. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this recommendation on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FLP03-CPP. Detect and handle floating point errors |
| MITRE CWE | CWE-369, Divide by zero |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XBD, Headers, <fenv.h> |
| [Intel 2001] |  |
| [ISO/IEC 9899:2011] | Subclause 7.6.2, "Floating-Point Exceptions" |
| [Keil 2008] |  |
| [MSDN] | "fpieee_flt (CRT)" |
| [SecurityFocus 2007] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152394) [](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152304)
## Comments:

|  |
| ----|
| Actually 1 / zero might generate a run-time fault.; Generally speaking, only when IEEE/IEC f.p. is used does it silently produce an "infinity" instead.  However, there was one now-defunct platform (Gould/Encore PowerNode) where integer and f.p. exceptions were controlled by a single bit, so for efficient integer generated code the system had to sacrifice trapping on divide-by-zero.
                                        Posted by dagwyn at Apr 16, 2008 19:29
                                     |
| The rule is ambiguous over whether MSVC2008 handles C99 exceptions...that needs to be cleared up.
I'd guess from context that MSVC2008 handles FPE exceptions differently from prev versions of MSVC.
                                        Posted by svoboda at Jun 06, 2008 15:39
                                     |
| Ok... the ROSE code for this is written, but there's no way to ever have a compliant solution since the pragma is broken.
                                        Posted by avolkovi at Jul 23, 2008 10:43
                                     |
| "Most processors stall for a significant duration (sometimes up to a second or even more on 32-bit desktop processors) when an operation incurs a NaN (not a number) value."A second is just too long for a single operation. I think that's impossible (unless it triggers a swap).Maybe there is a typo.;
                                        Posted by ntysdd at Jan 21, 2014 13:21
                                     |
| I'm not sure it is not true (see http://ds9a.nl/fp/ for example) but I removed it anyway because it was not necessary.
                                        Posted by rcs_mgr at Jan 21, 2014 14:46
                                     |
| Maybe he means the whole program instead of a single operation takes 0.5 second.;
                                        Posted by ntysdd at Jan 25, 2014 04:54
                                     |

