The C Standard defines a set of predefined macros (see subclause 6.10.8) to help the user determine if the implementation being used is a conforming implementation, and if so, to which version of the C Standard it conforms. These macros can also help the user to determine which of the standard features are implemented.
The following tables list these macros and indicate in which version of the C Standard they were introduced. The following macros are required:

| Macro Name | C90 | C99 | C11 |
| ----|----|----|----|
| __STDC__ | ✓ | ✓ | ✓ |
| __STDC_HOSTED__ |  | ✓ | ✓ |
| __STDC_VERSION__1 |  | ✓ | ✓ |
| __DATE__ | ✓ | ✓ | ✓ |
| __FILE__ | ✓ | ✓ | ✓ |
| __LINE__ | ✓ | ✓ | ✓ |
| __TIME__ | ✓ | ✓ | ✓ |

######   1) \_\_STDC_VERSION\_\_ was introduced by an Amendment to C90, this version of the C Standard is commonly call C94 
 The following are optional environment macros:

| Macro Name | C90 | C99 | C11 |
| ----|----|----|----|
| __STDC_ISO_10646__ |  | ✓ | ✓ |
| __STDC_MB_MIGHT_NEQ_WC__ |  | ✓ | ✓ |
| __STDC_UTF_16__ |  |  | ✓ |
| __STDC_UTF_32__ |  |  | ✓ |

  The following are optional feature macros:

| Macro Name | C90 | C99 | C11 |
| ----|----|----|----|
| __STDC_ANALYZABLE__ |  |  | ✓ |
| __STDC_IEC_559__ |  | ✓ | ✓ |
| __STDC_IEC_559_COMPLEX__ |  | ✓ | ✓ |
| __STDC_LIB_EXT1__; |  |  | ✓ |
| __STDC_NO_ATOMICS__ |  |  | ✓ |
| __STDC_NO_COMPLEX__ |  |  | ✓ |
| __STDC_NO_THREADS__ |  |  | ✓ |
| __STDC_NO_VLA__; |  |  | ✓ |

 The following is optional and is defined by the user:

| Macro Name | C90 | C99 | C11 |
| ----|----|----|----|
| __STDC_WANT_LIB_EXT1__; |  |  | ;✓ |

## Noncompliant Code Example (Checking Value of Predefined Macro)
C Standard predefined macros should never be tested for a value before the macro is tested for definition, as shown in this noncompliant code example:
``` c
#include <stdio.h>
int main(void) {
  #if (__STDC__ == 1)
    printf("Implementation is ISO-conforming.\n");
  #else
    printf("Implementation is not ISO-conforming.\n");
  #endif
  /* ... */
  return 0;
}
```
## Compliant Solution (Testing for Definition of Macro)
In this compliant solution, the definition of the predefined macro `__STDC__` is tested before the value of the macro is tested:
``` c
#include <stdio.h>
int main(void) {
  #if defined(__STDC__)
    #if (__STDC__ == 1)
      printf("Implementation is ISO-conforming.\n");
    #else
      printf("Implementation is not ISO-conforming.\n");
    #endif
  #else   /* !defined(__STDC__) */
    printf("__STDC__ is not defined.\n");
  #endif
  /* ... */
  return 0;
}
```
## Compliant Solution (Test for Optional Feature)
This compliant solution tests to see if the C11 predefined macro `__STDC_ANALYZABLE__` is defined and what value the implementation has given the macro:
``` c
#include <stdio.h>
int main(void) {
  #if defined (__STDC__)
    #if defined(__STDC_VERSION__) && (__STDC_VERSION__ >= 201112L)  /* C11 */
      #if defined(__STDC_ANALYZABLE__)
        #if (__STDC_ANALYZABLE__ == 1)
          printf("Compiler conforms to Annex L (Analyzability).\n");
        #else
          printf("Compiler does not support Annex L (Analyzability).\n");
        #endif
      #else
        printf("__STDC_ANALYZABLE__ is not defined.\n");
      #endif
    #else
      printf("Compiler not C11.\n");
    #endif
  #else
    printf("Compiler not Standard C.\n");
  #endif
  return 0;
}
```
## Compliant Solution (Optional Language Features)
This compliant solution checks for the C11 optional language features in Annex K. If Annex K is supported by the implementation, the functions defined in Annex K are used; if Annex K is not supported, then the standard library functions are used. (See [DCL09-C. Declare functions that return errno with a return type of errno_t](DCL09-C_%20Declare%20functions%20that%20return%20errno%20with%20a%20return%20type%20of%20errno_t)[.](MSC14-C_%20Do%20not%20introduce%20unnecessary%20platform%20dependencies))
``` c
#if defined(__STDC_LIB_EXT1__)
  #if (__STDC_LIB_EXT1__ >= 201112L)
    #define USE_EXT1 1
    #define __STDC_WANT_LIB_EXT1__ 1 /* Want the ext1 functions */
  #endif
#endif
#include <string.h>
#include <stdlib.h>
int main(void) {
  char source_msg[] = "This is a test.";
  char *msg = malloc(sizeof(source_msg) + 1);
  if (msg != NULL) {
    #if defined(USE_EXT1)
      strcpy_s(msg, sizeof msg, source_msg);
    #else
      strcpy(msg, source_msg);
    #endif
  } 
  else {
    return EXIT_FAILURE;
  }
  return 0;
}
```
## Compliant Solution (Optional Language Features)
The previous compliant solution comes close to violating [PRE09-C. Do not replace secure functions with deprecated or obsolescent functions](https://www.securecoding.cert.org/confluence/display/seccode/PRE09-C.+Do+not+replace+secure+functions+with+deprecated+or+obsolescent+functions), and would if a function-like macro were defined which called either `strcpy_s()` or `strcpy()` depending on if `USE_EXT1` were defined.  This compliant solution solves the problem by including a custom library that implements the optional language feature, which in this case is the Safe C Library available from [SourceForge](http://safeclib.sourceforge.net/).
``` c
#if defined(__STDC_LIB_EXT1__)
  #if (__STDC_LIB_EXT1__ >= 201112L)
    #define USE_EXT1 1
    #define __STDC_WANT_LIB_EXT1__ 1 /* Want the ext1 functions */
  #endif
#endif
#include <string.h>
#include <stdlib.h>
#if !defined(USE_EXT1)
  #include "safe_str_lib.h"
#endif
int main(void) {
  char source_msg[] = "This is a test.";
  char *msg = malloc(sizeof(source_msg) + 1);
  if (msg != NULL) {
    strcpy_s(msg, sizeof msg, source_msg);
  } 
  else {
    return EXIT_FAILURE;
  }
  return 0;
}
```
## Risk Assessment
Not testing for language features or the version of the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) being used can lead to unexpected or [undefined program behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE13-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE13 |  |
| LDRA tool suite | 9.7.1 |  | Partially implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE33-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Pre-processor Directives;[NMP] |
| ISO/IEC 9899:2011 | 6.10.8, "Predefined macro names"K.3.7.1, "Copying functions" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152230) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](../c/Rec_%2011_%20Signals%20_SIG_)
## Comments:

|  |
| ----|
| I'm not sure "a Standard conforming" is clear in this context... the CERT C Secure Coding Standard for the C Standard.; Should probably just say the C Standard. the phrase:"The tables below list these macros and which version of the C Standard they were introduced."doesn't seem to be correct, because the table appears to list all the versions of the standard in which the macros are defined.The (C94) is wierd.  I've never heard of this version of the standard, and don't know why it's in parenthesis.  A footnote might be necessary.In a related note, it is wierd to have empty columns in these tables.  Perhaps we should have the names of the standards in the column headers, and place check marks in the appropriate cells?  again, we might need a footnote for (C94)   
                                        Posted by rcs at Sep 18, 2013 07:42
                                     |
| Should __func__ be in the table?; Also, I agree that the tables could use some headers for clarity.  I kind of like Robert's suggestion of using checkmarks as the column values, and standard versions as the headers.
                                        Posted by aballman at Sep 18, 2013 09:06
                                     |
| No, _func_ is not a predefined macro, _func_ is a predefined identifier.
                                        Posted by bluepilot at Sep 18, 2013 15:03
                                     |
| Ok, I will add headers and check marks - if I can figure out how to   As for C94, C94 is C90 + Amend1.  I think C94 is a common designation but will double check.
                                        Posted by bluepilot at Sep 18, 2013 15:05
                                     |
| it's beauteous.
                                        Posted by rcs at Sep 18, 2013 19:21
                                     |
| The example with strcpy_s and strcpy violates the rule PRE09-C. Do not replace secure functions with deprecated or obsolescent functions. It could possible be changed so that the code defines strcpy_s itself if it's missing (obviously the actual reimplementation wouldn't be shown there'd just be ellipses).
                                        Posted by sstewartgallus at Feb 15, 2014 21:41
                                     |
| If it doesn't violate PRE09-C. Do not replace secure functions with deprecated or obsolescent functions, it comes pretty close.; I'm sure the next step would be to create a strcpy_s() macro to replace:     #if defined(USE_EXT1)      strcpy_s(msg, sizeof msg, source_msg);    #else      strcpy(msg, source_msg);    #endifWhich would definitely be a violation.
                                        Posted by rcs at Feb 17, 2014 10:43
                                     |

