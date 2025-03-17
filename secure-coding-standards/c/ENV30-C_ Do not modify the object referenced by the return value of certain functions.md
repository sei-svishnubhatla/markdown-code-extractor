Some functions return a pointer to an object that cannot be modified without causing [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). These functions include `getenv()`, `setlocale()`, `localeconv()`, `asctime()`, and `strerror()`. In such cases, the function call results must be treated as being `const`-qualified.
The C Standard, 7.24.4.6, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines `getenv()` as follows:
> The `getenv` function returns a pointer to a string associated with the matched list member. The string pointed to shall not be modified by the program, but may be overwritten by a subsequent call to the `getenv` function. If the specified name cannot be found, a null pointer is returned.

If the string returned by `getenv()` must be altered, a local copy should be created. Altering the string returned by `getenv()` is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 189](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_189).)
Similarly, subclause 7.11.1.1, paragraph 8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines `setlocale()` as follows:
> The pointer to string returned by the `setlocale` function is such that a subsequent call with that string value and its associated category will restore that part of the program'€™s locale. The string pointed to shall not be modified by the program, but may be overwritten by a subsequent call to the `setlocale` function.

 And subclause 7.11.2.1, paragraph 8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], defines `localeconv()` as follows:
> The `localeconv` function returns a pointer to the filled-in object. The structure pointed to by the return value shall not be modified by the program, but may be overwritten by a subsequent call to the `localeconv` function. In addition, calls to the `setlocale` function with categories `LC_ALL`, `LC_MONETARY`, or `LC_NUMERIC` may overwrite the contents of the structure.
>
>   

Altering the string returned by `setlocale()` or the structure returned by `localeconv()` are [undefined behaviors](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behaviors 119](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_119) and [121](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_121).) Furthermore, the C Standard imposes no requirements on the contents of the string by `setlocale()`. Consequently, no assumptions can be made as to the string's internal contents or structure.
Finally, subclause 7.26.6.3, paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> The strerror function returns a pointer to the string, the contents of which are locale-specific. The array pointed to shall not be modified by the program. The behavior is undefined if the returned value is used after a subsequent call to the strerror function, or after the thread which called the function to obtain the returned value has exited.

Altering the string returned by `strerror()` is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 189](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_189).)
## Noncompliant Code Example (`getenv()`)
This noncompliant code example modifies the string returned by `getenv()` by replacing all double quotation marks (`"`) with underscores (`_`):
``` c
#include <stdlib.h>
void trstr(char *c_str, char orig, char rep) {
  while (*c_str != '\0') {
    if (*c_str == orig) {
      *c_str = rep;
    }
    ++c_str;
  }
}
void func(void) {
  char *env = getenv("TEST_ENV");
  if (env == NULL) {
    /* Handle error */
  }
  trstr(env,'"', '_');
}
```
## Compliant Solution (`getenv()`) (Environment Not Modified)
If the programmer does not intend to modify the environment, this compliant solution demonstrates how to modify a copy of the return value:
``` c
#include <stdlib.h>
#include <string.h>
void trstr(char *c_str, char orig, char rep) {
  while (*c_str != '\0') {
    if (*c_str == orig) {
      *c_str = rep;
    }
    ++c_str;
  }
}
void func(void) {
  const char *env;
  char *copy_of_env;
  env = getenv("TEST_ENV");
  if (env == NULL) {
    /* Handle error */
  }
  copy_of_env = (char *)malloc(strlen(env) + 1);
  if (copy_of_env == NULL) {
    /* Handle error */
  }
  strcpy(copy_of_env, env);
  trstr(copy_of_env,'"', '_');
  /* ... */
  free(copy_of_env);
}
```
## Compliant Solution (`getenv()`) (Modifying the Environment in POSIX)
If the programmer's intent is to modify the environment, this compliant solution, which saves the altered string back into the environment by using the POSIX `setenv()` and `strdup()` functions, can be used:
``` c
#include <stdlib.h>
#include <string.h>
void trstr(char *c_str, char orig, char rep) {
  while (*c_str != '\0') {
    if (*c_str == orig) {
      *c_str = rep;
    }
    ++c_str;
  }
}
void func(void) {
  const char *env;
  char *copy_of_env;
  env = getenv("TEST_ENV");
  if (env == NULL) {
    /* Handle error */
  }
  copy_of_env = strdup(env);
  if (copy_of_env == NULL) {
    /* Handle error */
  }
  trstr(copy_of_env,'"', '_');
  if (setenv("TEST_ENV", copy_of_env, 1) != 0) {
    /* Handle error */
  }
  /* ... */
  free(copy_of_env);
}
```
## Noncompliant Code Example (`localeconv()`)
In this noncompliant example, the object returned by `localeconv()` is directly modified:
``` c
#include <locale.h>
void f2(void) {
  struct lconv *conv = localeconv();
  if ('\0' == conv->decimal_point[0]) {
    conv->decimal_point = ".";
  }
}
```
## Compliant Solution (`localeconv()`) (Copy)
This compliant solution modifies a copy of the object returned by `localeconv()`:
``` c
#include <locale.h>
#include <stdlib.h>
#include <string.h>
void f2(void) {
  const struct lconv *conv = localeconv();
  if (conv == NULL) {
     /* Handle error */
  }
  struct lconv *copy_of_conv = (struct lconv *)malloc(
    sizeof(struct lconv));
  if (copy_of_conv == NULL) {
    /* Handle error */
  }
  memcpy(copy_of_conv, conv, sizeof(struct lconv));
  if ('\0' == copy_of_conv->decimal_point[0]) {
    copy_of_conv->decimal_point = ".";  
  }
  /* ... */
  free(copy_of_conv);
}
```
## Risk Assessment
Modifying the object pointed to by the return value of `getenv()`, `setlocale()`, `localeconv()`, `asctime()`, or `strerror()` is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Even if the modification succeeds, the modified object can be overwritten by a subsequent call to the same function.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV30-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | stdlib-const-pointer-assign | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ENV30 |  |
| CodeSonar | 8.3p0 | BADFUNC.GETENVLANG.STRUCT.RPNTC
 | Use of getenvReturned Pointer Not Treated as const |
| Compass/ROSE |  |  | Can detect violations of this rule. In particular, it ensures that the result of getenv() is stored in a const variable |
| Cppcheck Premium | 24.11.0 | premium-cert-env30-c |  |
| Helix QAC | 2024.4 | C1492, C1493, C1494DF4751, DF4752, DF4753 |  |
| Klocwork | 2024.4 | MISRA.STDLIB.CTYPE.RANGE.2012_AMD1MISRA.STDLIB.ILLEGAL_REUSE.2012_AMD1
MISRA.STDLIB.ILLEGAL_WRITE.2012_AMD1 |  |
| LDRA tool suite | 9.7.1 | 107 D | Partially Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV30-a | The pointers returned by the Standard Library functions 'localeconv', 'getenv', 'setlocale' or, 'strerror' shall only be used as if they have pointer to const-qualified type |
| Polyspace Bug Finder | R2024a | CERT C: Rule ENV30-C | Checks for modification of internal buffer returned from nonreentrant standard function (rule fully covered) |
| PVS-Studio | 7.35 | V675 |  |
| RuleChecker | 24.04 | stdlib-const-pointer-assign | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV30-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961:2013 | Modifying the string returned by getenv, localeconv, setlocale, and strerror [libmod] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, getenvXSH, System Interfaces, setlocale
XSH, System Interfaces, localeconv |
| [ISO/IEC 9899:2024] | 7.11.1.1, "The setlocale Function"7.11.2.1, "The localeconv Function"
7.24.4.6, "The getenv Function"
7.26.6.3, "The strerror Function" |

------------------------------------------------------------------------
[](../c/Rule%2010_%20Environment%20_ENV_) [](../c/Rule%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152100)
## Comments:

|  |
| ----|
| In most Unix-ish implementations, modifying the return from getenv() will modify the actual environment.; If that's the required effect, we need to illustrate using putenv() with caveats about where it is supported.
                                        Posted by jonathan.leffler@gmail.com at Mar 19, 2008 15:45
                                     |
| In the compliant examples, env[0]==0 should be treated as an error condition, since storing 'a' there could leave the string unterminated.
Generally, modifying the environment should be discouraged (except for sanitizing before spawning a child process).; For one thing, on some systems it affects parent processes and on others it doesn't.
                                        Posted by dagwyn at Apr 17, 2008 20:44
                                     |
| Theoretically shouldn't getenv() return a const char*? Perhaps this rule should be rephrased that only a const char* should hold the result of getenv()?
                                        Posted by svoboda at Jul 25, 2008 11:20
                                     |
| I like the const char * idea a lot, it would also make validation MUCH easier, should I go ahead and try to merge this into the article?
                                        Posted by avolkovi at Jul 25, 2008 13:55
                                     |
| If the additions to this page relating to setlocale() and localeconv() are going to stay, then the page needs more changes.  For example:
    The page title should not refer to "functions that give environmental settings".
    The first paragraph should not imply that setlocale() and localeconv() return "a pointer to a[n] object containing current environmental settings".
    The risk assessment should not say "modifying the object pointed to by the return value of these functions may or may not modify the environment".  (It should probably just say "modifying the object pointed to by the return value of these functions causes undefined behavior".)
Also the setlocale() compliant solution may follow the secure coding rules, but it is not portable.  The content of the string returned by setlocale() is unspecified; applications cannot assume it contains a locale name.
                                        Posted by geoffclare at Nov 13, 2009 11:33
                                     |
| I addressed most of your comments.  I also added the strerror() function which has similar characteristics.  Still need to look at portability of the setlocale() compliant solution. A further problem is where this rule now belongs because the environment section is probably not the right place anymore.  I'm sort of thinking the expressions section, because that is a pretty good catch all section.  This might be best suited for a "Library" section, if we had one.
                                        Posted by rcs_mgr at Nov 15, 2009 21:32
                                     |
| Yes, you fixed the major problems (except the setlocale() portability one).  I made a few more small fixes, including changing strtr to trstr since strtr is in the namespace reserved by the C Standard.
                                        Posted by geoffclare at Nov 16, 2009 05:22
                                     |
| C99, section 7.11.1 (setlocale()) says:
If a pointer to a string is given for locale and the selection can be honored, the setlocale function returns a pointe
r to the string associated with the specified category for the new locale. If the selection cannot be honored, the setlocale function returns a null pointer and the programâ€™s locale is not changed.
Furthermore, both the setlocale() NCCE & CS make no assumptions about the string returned; they should work no matter what its contents. So I stipulate that both the NCCE & CS are fully C99-compliant & portable.
                                        Posted by svoboda at Nov 23, 2009 13:34
                                     |
| The C99 text you quote doesn't mean that setlocale() returns the string you passed to it.  If it did, then calling setlocale(category, "") would return an empty string.
C99 says (para 8):
The pointer to string returned by the setlocale function is such that a subsequent call
with that string value and its associated category will restore that part of the program's locale.
This, to me, is a clear warning that the only thing applications can legitimately do with the string is pass it to a subsequent setlocale() call; they shouldn't try to interpret the contents of the string.  Also, if the call to setlocale(LC_ALL, "") sets two or more categories to different locales then those multiple locale names need to be encoded in the returned string somehow.  The way this is done is implementation-specific.
Moving on:
Furthermore, both the setlocale() NCCE & CS make no assumptions about the string returned
They assume something about what a "." character in the string means.  This may be reasonably safe, but they also assume there will be at most one "." character.  If the call to setlocale(LC_ALL, "") sets two or more categories to different locales then there could be more than one "." in the string.
                                        Posted by geoffclare at Nov 24, 2009 05:43
                                     |
| 
They assume something about what a "." character in the string means. This may be reasonably safe, but they also assume there will be at most one "." character. If the call to setlocale(LC_ALL, "") sets two or more categories to different locales then there could be more than one "." in the string.
Granted.
This, to me, is a clear warning that the only thing applications can legitimately do with the string is pass it to a subsequent setlocale() call; they shouldn't try to interpret the contents of the string.
Hmm. Clearly you can't make a NCCE w/o making some assumptions about the string's contents. I don't know much about localization, but I presume that other platforms or standards provide some details about the contents of the string returned by setlocale(). This means you could make a compliant solution that copies the string and modifies it; it would just be non-portable.
The simplest solution is to leave the code as is, but add your caveat about multiple .'s.  Alternately we could make a different (nonportable) modification...suggestions?
                                        Posted by svoboda at Nov 24, 2009 11:17
                                     |
| 
Clearly you can't make a NCCE w/o making some assumptions about the string's contents.
Indeed.
Usually a NCCE tries to achieve something sensible, only it goes about it in an insecure way.  The problem with the setlocale() NCCE is that there is nothing sensible that can be achieved by modifying the string returned by setlocale().
My suggestion would be just to remove the setlocale() examples, or perhaps replace them with ones based on one of the other functions (if you can think of something sensible that can be achieved for one of them).
                                        Posted by geoffclare at Nov 24, 2009 12:02
                                     |
| I've removed the setlocale() examples. We should add a NCCE/CS pair based on strerror() later.
                                        Posted by svoboda at Nov 24, 2009 13:36
                                     |

