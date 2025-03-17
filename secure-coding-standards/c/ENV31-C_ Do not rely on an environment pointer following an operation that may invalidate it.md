Some implementations provide a nonportable environment pointer that is valid when `main()` is called but may be invalidated by operations that modify the environment.
The C Standard, J.5.2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\], states
> In a hosted environment, the main function receives a third argument, char \*envp\[\], that points to a null-terminated array of pointers to char, each of which points to a string that provides information about the environment for this execution of the program (5.1.2.3.2).

Consequently, under a [hosted environment](BB_%20Definitions) supporting this common extension, it is possible to access the environment through a modified form of `main()`:
``` java
main(int argc, char *argv[], char *envp[]){ /* ... */ }
```
However, modifying the environment by any means may cause the environment memory to be reallocated, with the result that `envp` now references an incorrect location. For example, when compiled with GCC 4.8.1 and run on a 32-bit Intel GNU/Linux machine, the following code,
``` java
#include <stdio.h>
#include <stdlib.h>
extern char **environ;
int main(int argc, const char *argv[], const char *envp[]) {
  printf("environ:  %p\n", environ);
  printf("envp:     %p\n", envp);
  setenv("MY_NEW_VAR", "new_value", 1);
  puts("--Added MY_NEW_VAR--");
  printf("environ:  %p\n", environ);
  printf("envp:     %p\n", envp);
  return 0;
}
```
yields
``` java
% ./envp-environ
environ: 0xbf8656ec
envp:    0xbf8656ec
--Added MY_NEW_VAR--
environ: 0x804a008
envp:    0xbf8656ec
```
It is evident from these results that the environment has been relocated as a result of the call to `setenv()`. The external variable `environ` is updated to refer to the current environment; the `envp` parameter is not.
An environment pointer may also become invalidated by subsequent calls to `getenv().` (See [ENV34-C. Do not store pointers returned by certain functions](ENV34-C_%20Do%20not%20store%20pointers%20returned%20by%20certain%20functions) for more information.)
## Noncompliant Code Example (POSIX)
After a call to the POSIX `setenv()` function or to another function that modifies the environment, the `envp` pointer may no longer reference the current environment. The *Portable Operating System Interface (POSIX<sup>®</sup>), Base Specifications, Issue 7* \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\], states
> Unanticipated results may occur if `setenv()` changes the external variable `environ`. In particular, if the optional `envp` argument to `main()` is present, it is not changed, and thus may point to an obsolete copy of the environment (as may any other copy of `environ`).

This noncompliant code example accesses the `envp` pointer after calling `setenv()`:
``` c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, const char *argv[], const char *envp[]) {
  if (setenv("MY_NEW_VAR", "new_value", 1) != 0) {
    /* Handle error */
  }
  if (envp != NULL) {
    for (size_t i = 0; envp[i] != NULL; ++i) {
      puts(envp[i]);
    }
  }
  return 0;
}
```
Because `envp` may no longer point to the current environment, this program has unanticipated behavior.
## Compliant Solution (POSIX)
Use `environ` in place of `envp` when defined:
``` c
#include <stdio.h>
#include <stdlib.h>
extern char **environ;
int main(void) {
  if (setenv("MY_NEW_VAR", "new_value", 1) != 0) {
    /* Handle error */
  }
  if (environ != NULL) {
    for (size_t i = 0; environ[i] != NULL; ++i) {
      puts(environ[i]);
    }
  }
  return 0;
}
```
## Noncompliant Code Example (Windows)
After a call to the Windows [\_putenv_s()](http://msdn.microsoft.com/en-us/library/eyw7eyfw.aspx) function or to another function that modifies the environment, the `envp` pointer may no longer reference the environment.
According to the Visual C++ reference \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\]
> The environment block passed to `main` and `wmain` is a "frozen" copy of the current environment. If you subsequently change the environment via a call to `_putenv` or `_wputenv`, the current environment (as returned by `getenv` / `_wgetenv` and the `_environ` / `_wenviron` variable) will change, but the block pointed to by `envp` will not change.

This noncompliant code example accesses the `envp` pointer after calling `_putenv_s()`:
``` c
#include <stdio.h>
#include <stdlib.h>
int main(int argc, const char *argv[], const char *envp[]) {
  if (_putenv_s("MY_NEW_VAR", "new_value") != 0) {
    /* Handle error */
  }
  if (envp != NULL) {
    for (size_t i = 0; envp[i] != NULL; ++i) {
      puts(envp[i]);
    }
  }
  return 0;
}
```
Because `envp` no longer points to the current environment, this program has unanticipated behavior.
## Compliant Solution (Windows)
This compliant solution uses the [\_environ](http://msdn.microsoft.com/en-us/library/stxk41x1.aspx) variable in place of `envp`:
``` c
#include <stdio.h>
#include <stdlib.h>
_CRTIMP extern char **_environ;
int main(int argc, const char *argv[]) {
  if (_putenv_s("MY_NEW_VAR", "new_value") != 0) {
    /* Handle error */
  }
  if (_environ != NULL) {
    for (size_t i = 0; _environ[i] != NULL; ++i) {
      puts(_environ[i]);
    }
  }
return 0;
}
```
## Compliant Solution
This compliant solution can reduce remediation time when a large amount of noncompliant `envp` code exists. It replaces
``` java
int main(int argc, char *argv[], char *envp[]) {
  /* ... */
}
```
with
``` c
#if defined (_POSIX_) || defined (__USE_POSIX)
  extern char **environ;
  #define envp environ
#elif defined(_WIN32)
  _CRTIMP extern char **_environ;
  #define envp _environ
#endif
int main(int argc, char *argv[]) {
  /* ... */
}
```
This compliant solution may need to be extended to support other implementations that support forms of the external variable `environ`.
## Risk Assessment
Using the `envp` environment pointer after the environment has been modified can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV31-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | ; | Supported |
| Compass/ROSE |  |  |  |
| Cppcheck Premium | 24.9.0 | premium-cert-env31-c |  |
| Helix QAC | 2024.4 | DF4991, DF4992, DF4993 |  |
| LDRA tool suite | 9.7.1 | 118 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV31-a | Do not rely on an environment pointer following an operation that may invalidate it |
| Polyspace Bug Finder | R2024a | CERT C: Rule ENV31-C | Checks for environment pointer invalidated by previous operation (rule fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM00-CPP).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | VOID ENV31-CPP. Do not rely on an environment pointer following an operation that may invalidate it | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, setenv |
| [ISO/IEC 9899:2024] | J.5.2, "Environment Arguments" |
| [MSDN] | _environ, _wenviron,getenv, _wgetenv,
_putenv_s, _wputenv_s |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152111) [](../c/Rule%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152169)
## Comments:

|  |
| ----|
| In a multi-threaded environment, could the string become invalidated by a different thread calling setenv()?  In that case, is a compliant solution even possible?  Or do we not care since we can assume that a user will use mutexes around environment operations?
                                        Posted by avolkovi at Jul 25, 2008 13:58
                                     |
| This rule seems to violate our requirement that the noncompliant code example can be expressed using standard C.; That being said, I think it is a valid exception to the requirement.
                                        Posted by rcs_mgr at Nov 22, 2013 16:20
                                     |
| I think we're misusing the term "undefined behavior" here. The quote from MSDN makes it clear that looking at envp will show you the old environment, which, though unexpected, would seem to be well-defined. POSIX is slightly less clear that that's all that will happen, but I think even calling it undefined behavior would be a stretch.
                                        Posted by jcsible at Jul 07, 2020 10:14
                                     |
| Agreed, I changed both cases to 'unanticipated behavior'.
                                        Posted by svoboda at Jul 07, 2020 11:09
                                     |
| Is the following the complete set of functions that invalidate envp?POSIX: setenv, unsetenv, putenv
Windows: _putenv_s, _wputenv_s
                                        Posted by mbaluda at Aug 12, 2022 10:53
                                     |
| I have not seen a complete list of functions that invalidate envp. Such a list of POSIX functions would be huge, ditto for Windows.
                                        Posted by svoboda at Aug 12, 2022 14:13
                                     |

