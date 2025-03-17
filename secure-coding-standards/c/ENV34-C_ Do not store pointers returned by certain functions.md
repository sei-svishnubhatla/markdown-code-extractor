The C Standard, 7.24.4.6, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> The `getenv` function returns a pointer to a string associated with the matched list member. The string pointed to shall not be modified by the program but may be overwritten by a subsequent call to the `getenv` function. If the specified name cannot be found, a null pointer is returned.

This paragraph gives an implementation the latitude, for example, to return a pointer to a statically allocated buffer. Consequently, do not store this pointer because the string data it points to may be overwritten by a subsequent call to the `getenv()` function or invalidated by modifications to the environment. This string should be referenced immediately and discarded. If later use is anticipated, the string should be copied so the copy can be safely referenced as needed.
The `getenv()` function is not thread-safe. Make sure to address any possible race conditions resulting from the use of this function.
The `asctime()`, `localeconv()`, `setlocale()`, and `strerror()` functions have similar restrictions. Do not access the objects returned by any of these functions after a subsequent call.
## Noncompliant Code Example
This noncompliant code example attempts to compare the value of the `TMP` and `TEMP` environment variables to determine if they are the same:
``` c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void func(void) {
  char *tmpvar;
  char *tempvar;
  tmpvar = getenv("TMP");
  if (!tmpvar) {
    /* Handle error */
  }
  tempvar = getenv("TEMP");
  if (!tempvar) {
    /* Handle error */
  }
  if (strcmp(tmpvar, tempvar) == 0) {
    printf("TMP and TEMP are the same.\n");
  } else {
    printf("TMP and TEMP are NOT the same.\n");
  }
}
```
This code example is noncompliant because the string referenced by `tmpvar` may be overwritten as a result of the second call to the `getenv()` function. As a result, it is possible that both `tmpvar` and `tempvar` will compare equal even if the two environment variables have different values.
## Compliant Solution
This compliant solution uses the `malloc()` and `strcpy()` functions to copy the string returned by `getenv()` into a dynamically allocated buffer:
``` c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void func(void) {
  char *tmpvar;
  char *tempvar;
  const char *temp = getenv("TMP");
  if (temp != NULL) {
    tmpvar = (char *)malloc(strlen(temp)+1);
    if (tmpvar != NULL) {
      strcpy(tmpvar, temp);
    } else {
      /* Handle error */
    }
  } else {
    /* Handle error */
  }
  temp = getenv("TEMP");
  if (temp != NULL) {
    tempvar = (char *)malloc(strlen(temp)+1);
    if (tempvar != NULL) {
      strcpy(tempvar, temp);
    } else {
      /* Handle error */
    }
  } else {
    /* Handle error */
  }
  if (strcmp(tmpvar, tempvar) == 0) {
    printf("TMP and TEMP are the same.\n");
  } else {
    printf("TMP and TEMP are NOT the same.\n");
  }
  free(tmpvar);
  free(tempvar);
}
```
## Compliant Solution (Annex K)
The C Standard, Annex K, provides the `getenv_s()` function for getting a value from the current environment. However, `getenv_s()` can still have data races with other threads of execution that modify the environment list.
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void func(void) {
  char *tmpvar;
  char *tempvar;
  size_t requiredSize;
  errno_t err;
  err = getenv_s(&requiredSize, NULL, 0, "TMP");
  if (err) {
    /* Handle error */
  }
  tmpvar = (char *)malloc(requiredSize);
  if (!tmpvar) {
    /* Handle error */
  }
  err = getenv_s(&requiredSize, tmpvar, requiredSize, "TMP" );
  if (err) {
    /* Handle error */
  }
  err = getenv_s(&requiredSize, NULL, 0, "TEMP");
  if (err) {
    /* Handle error */
  }
  tempvar = (char *)malloc(requiredSize);
  if (!tempvar) {
    /* Handle error */
  }
  err = getenv_s(&requiredSize, tempvar, requiredSize, "TEMP" );
  if (err) {
    /* Handle error */
  }
  if (strcmp(tmpvar, tempvar) == 0) {
    printf("TMP and TEMP are the same.\n");
  } else {
    printf("TMP and TEMP are NOT the same.\n");
  }
  free(tmpvar);
  tmpvar = NULL;
  free(tempvar);
  tempvar = NULL;
}
```
## Compliant Solution (Windows)
Microsoft Windows provides the [`_dupenv_s()`](http://msdn.microsoft.com/en-us/library/ms175774.aspx) and [wdupenv_s()](http://msdn.microsoft.com/en-us/library/ms175774.aspx) functions for getting a value from the current environment \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\]. The `_dupenv_s()` function searches the list of environment variables for a specified name. If the name is found, a buffer is allocated; the variable's value is copied into the buffer, and the buffer's address and number of elements are returned. The `_dupenv_s()` and `_wdupenv_s()` functions provide more convenient alternatives to `getenv_s()` and `_wgetenv_s()` because each function handles buffer allocation directly.
The caller is responsible for freeing any allocated buffers returned by these functions by calling `free()`.
``` c
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <stdio.h>
void func(void) {
  char *tmpvar;
  char *tempvar;
  size_t len;
  errno_t err = _dupenv_s(&tmpvar, &len, "TMP");
  if (err) {
    /* Handle error */
  }
  err = _dupenv_s(&tempvar, &len, "TEMP");
  if (err) {
    /* Handle error */
  }
  if (strcmp(tmpvar, tempvar) == 0) {
    printf("TMP and TEMP are the same.\n");
  } else {
    printf("TMP and TEMP are NOT the same.\n");
  }
  free(tmpvar);
  tmpvar = NULL;
  free(tempvar);
  tempvar = NULL;
}
```
## Compliant Solution (POSIX or C2x)
POSIX provides the `strdup()` function, which can make a copy of the environment variable string \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. The `strdup()` function is also included in *Extensions to the C Library—Part II* \[[ISO/IEC TR 24731-2:2010](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24731-2-2010)\]. Further, it is expected to be present in the C2x standard.
``` c
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
void func(void) {
  char *tmpvar;
  char *tempvar;
  const char *temp = getenv("TMP");
  if (temp != NULL) {
    tmpvar = strdup(temp);
    if (tmpvar == NULL) {
      /* Handle error */
    }
  } else {
    /* Handle error */
  }
  temp = getenv("TEMP");
  if (temp != NULL) {
    tempvar = strdup(temp);
    if (tempvar == NULL) {
      /* Handle error */
    }
  } else {
    /* Handle error */
  }
  if (strcmp(tmpvar, tempvar) == 0) {
    printf("TMP and TEMP are the same.\n");
  } else {
    printf("TMP and TEMP are NOT the same.\n");
  }
  free(tmpvar);
  tmpvar = NULL;
  free(tempvar);
  tempvar = NULL;
}
```
## Risk Assessment
Storing the pointer to the string returned by `getenv()`, `localeconv()`, `setlocale()`, or `strerror()` can result in overwritten data.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV34-C | Low | Probable | Medium | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV34-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  |  |
| Cppcheck Premium | 24.9.0 | premium-cert-env34-c |  |
| Helix QAC | 2024.4 | DF2681, DF2682, DF2683 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.ILLEGAL_REUSE.2012_AMD1
 |  |
| LDRA tool suite | 9.7.1 | 133 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV34-a | Pointers returned by certain Standard Library functions should not be used following a subsequent call to the same or related function |
| Polyspace Bug Finder | R2024a | CERT C: Rule ENV34-C | Checks for misuse of return value from nonreentrant standard function (rule fully covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| C Secure Coding Standard | ENV00-C. Do not store objects that can be overwritten by multiple calls to getenv() and similar functions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24731-2 | 5.3.1.1, "The strdup Function" | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Using an object overwritten by getenv, localeconv, setlocale, and strerror [libuse] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | Chapter 8, "Environment Variables"XSH, System Interfaces, strdup |
| [ISO/IEC 9899:2024] | Subclause 7.24.4, "Communication with the Environment"Subclause 7.24.4.6, "The getenv Function"
Subclause K.3.6.2.1, "The getenv_s Function" |
| [MSDN] | _dupenv_s(), _wdupenv_s() |
| [Viega 2003] | Section 3.6, "Using Environment Variables Securely" |

------------------------------------------------------------------------
[](../c/ENV33-C_%20Do%20not%20call%20system__) [](../c/Rule%2010_%20Environment%20_ENV_) [](../c/Rule%2011_%20Signals%20_SIG_)
## Comments:

|  |
| ----|
| Question: on which actual system does getenv() create copies of the environment variable?
                                        Posted by jonathan.leffler@gmail.com at Apr 21, 2008 23:10
                                     |
| None that I know of.
                                        Posted by jpincar at Jun 18, 2008 09:44
                                     |
| reading over this again, it seems like there is an inherent TOCTOU in getenv() between it returning a pointer, and a user reading it... why aren't we more worried about this?
                                        Posted by avolkovi at Jul 25, 2008 13:50
                                     |
| I think this whole rule is about the TOCTOU condition you cite, without ever mentioning it.
I think the reason the race condition is not highlighted more is that we have  agood handle on how the contents of the getenv return pointer can change...through another getenv call, (maybe through putenv/setenv too?)
Unless you are talking about a multithreaded env...the rule does state that getenv() is not thread-safe.
                                        Posted by svoboda at Jul 25, 2008 15:05
                                     |
| Would it be worthwhile to address the potential TOCTOU within the compliant code examples themselves, maybe in the form of a comment?   I know the examples are already long enough but it might increase the chances of someone recognizing the implications if they're prone to cut-and-paste of these examples.
                                        Posted by christey at Jul 28, 2008 18:33
                                     |
| Regarding the ROSE algorithm, do we also need to check for calls to putenv()/setenv() between a store from getenv() and an access?
                                        Posted by avolkovi at Jul 29, 2008 15:19
                                     |
| Good question, and one that applies to the rule as a whole, not just to ROSE. The POSIX standard says nothing about putenv() or setenv() invalidating pointers returned by getenv().
I would guess that putenv() and setenv() do invalidate getenv() pointers, as they do modify the environment array, which is how env vars are usually stored these days. We have another rule that declares that they invalidate envp, so invalidating getenv() is likely.
                                        Posted by svoboda at Jul 29, 2008 17:21
                                     |
| I think that the POSIX and C compliant solutions are hiding buffer overflow bugs.; There's no assurance that the string returned by getenv() or getenv_s() will be null terminated.  So, for instance, putenv() or its moral equivalent were called with an unterminated string, the call to getenv() would return an unterminated string that would be passed to strdup() or strlen()/ strcpy().
                                        Posted by aballman at Aug 01, 2013 13:08
                                     |
| I would like to extend this to "similar functions" meaning any function anyone writes that returns a pointer to a reusable buffer.; I know we considered this for TS 17961 but I don't recall why it didn't make it into the document.
                                        Posted by rcs_mgr at Nov 27, 2013 07:06
                                     |
| The C standard says this:The string pointed to shall not be modified by the program, but may be overwritten by a subsequent call to the getenv function.And POSIX says this:[]  The returned string pointer might be invalidated or  ;the string content might be overwritten by a subsequent call to getenv(), []  setenv(), unsetenv(), 
 []   or (if supported) putenv()   but they shall not be affected by a call to any other function in this volume of POSIX.1-2017.So why do we need to copy the result of the second call to getenv(), given that we know for sure that we're done with it before anything that might overwrite it could happen? Couldn't we just copy the result of the first call?
                                        Posted by jcsible at Jul 10, 2020 09:56
                                     |
| putenv() or its moral equivalent were called with an unterminated stringI'd consider that an unambiguous bug in the caller of putenv(). In particular, it'd no longer be safe to exec anything with that environment. POSIX says this:The argument envp is an array of character pointers to null-terminated strings. These strings shall constitute the environment for the new process image. The envp array is terminated by a null pointer.For those forms not containing an envp pointer (execl(), execv(), execlp(), and execvp()), the environment for the new process image shall be taken from the external variable environ in the calling process.And the Linux kernel will absolutely keep reading the environment strings until it finds a null character or it E2BIG or EFAULTs.
                                        Posted by jcsible at Jul 13, 2020 15:40
                                     |
| It's been a few years since I made this comment, but I think I was thinking of a malicious attacker calling;putenv() with invalid data to force a crash they can control.
                                        Posted by aballman at Jul 13, 2020 15:54
                                     |
| If your attacker can call putenv with an unterminated byte string, she must be able to run custom C code, which means you've got much bigger problems than putenv();
                                        Posted by svoboda at Jul 27, 2020 16:17
                                     |
| Joseph C. Sible:I see that you edited this rule to suggest that C2x will support strdup(). This is news to me...can you add a citation to a public document that suggests so? Perhaps the latest C2x draft?
                                        Posted by svoboda at Jul 27, 2020 16:29
                                     |
| You're right...we could have dispensed with the second malloc/strcpy/free. We were just being consistent with the first call to getenv().
                                        Posted by svoboda at Jul 27, 2020 16:31
                                     |
| Yep, it's in N2478. I don't see any existing links to draft standards in the bibliography; do you know the right format for them?
                                        Posted by jcsible at Jul 27, 2020 16:38
                                     |

