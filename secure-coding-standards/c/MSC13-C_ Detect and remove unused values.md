The presence of unused values may indicate significant logic errors. To prevent such errors, unused values should be identified and removed from code.
This recommendation is a specific case of [MSC12-C. Detect and remove code that has no effect or is never executed](MSC12-C_%20Detect%20and%20remove%20code%20that%20has%20no%20effect%20or%20is%20never%20executed).
## Noncompliant Code Example
In this example, `p2` is assigned the value returned by `bar()`, but that value is never used. Note this example assumes that `foo()` and `bar()` return valid pointers (see [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations)).
``` c
int *p1;
int *p2;
p1 = foo();
p2 = bar();
if (baz()) {
  return p1;
}
else {
  p2 = p1;
}
return p2;
```
## Compliant Solution
This example can be corrected in many different ways, depending on the intent of the programmer. In this compliant solution, `p2` is found to be extraneous. The calls to `bar()` and `baz()` can be removed if they do not produce any side effects.
``` c
int *p1 = foo();
/* Removable if bar() does not produce any side effects */
(void)bar();
/* Removable if baz() does not produce any side effects */
(void)baz();
return p1;
```
## Exceptions
**MSC13-EX1:** Initializing a variable with a default value, such as 0, which gets subsequently overwritten may be inefficient, but is less of a problem than reading an uninitialized value, as per [EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory).
## Risk Assessment
Unused values may indicate significant logic errors.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC13-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | LANG.STRUCT.UUVAL | Unused value |
| Coverity | 2017.07 | UNUSED_VALUE | Finds variables that are assigned pointer values returned from a function call but never used |
| Helix QAC | 2024.4 | C1500, C1502, C3203, C3205, C3206, C3207, C3229DF2980, DF2981, DF2982, DF2983, DF2984, DF2985, DF2986 |  |
| Klocwork | 2024.4 | LV_UNUSED.GENVA_UNUSED.GEN
VA_UNUSED.INIT |  |
| LDRA tool suite | 9.7.1 | 1 D, 8 D, 105 D, 94 D, 15 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC13-a | Avoid unnecessary local variables |
| PC-lint Plus | 1.4 | 438, 505, 529, 715, 838 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC13-C | Checks for:Unused parameterWrite without a further readRec. partially covered. |
| PVS-Studio | 7.35 | V519, V596, V603, V714, V744, V751, V763, V1001, V5003 |  |
| SonarQube C/C++ Plugin | 3.11 | S1854 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC13-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC13-CPP. Detect and remove unused values |
| ISO/IEC TR 24772 | Likely Incorrect Expressions [KOA]Dead and Deactivated Code [XYQ]
Unused Variable [XYR] |

## Bibliography

|  |
| ----|
| [Coverity 2007] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152101) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152340)
## Comments:

|  |
| ----|
| I'm uncomfortable with the examples, as the replacement is only possible if bar() has no side-effects.  A few options:
    Add a comment that you can only remove bar() if it has no side-effects
    Add a bar() call on its own line, with a comment saying it's removable if there's no side-effects
    Replace the call to bar() with inline code, such as p2 = &p1[3];, where its clear there are no side-effects.
                                        Posted by hburch at Jun 14, 2007 08:34
                                     |
| Agreed and fixed.
                                        Posted by jsg at Jun 15, 2007 06:49
                                     |
| Most compliers will issue warnings when variables are unused, and the compiler should always be asked to issue these warnings.
They are not always easy to make go away when in #ifdef hell, but the approach I've taken in the past is to either delete the variable (if it's really unused), or to create some macros that tag the variable with the proper intent.
/* common header file */
#define UNUSED_PARAMETER(p)     (void)(p)       /* shut up compiler warnings */
#define UNUSED_VARIABLE(p)     (void)(p)       /* shut up compiler warnings */

Now one can do:  
``` java
void on_SIGALRM(int signo) {
   UNUSED_PARAMETER(signo);
   /* do something on the signal handler but we darn well know it's SIGALRM */
}
```
and not only shut up the compiler warnings, but tell the user "We really know this parameter is not used"
Other examples could be - a contrived one:  
``` java
void myfunction(int i) {
#ifdef _WIN32
  /* do stuff using i */
#else
 /* do stuff with UNIX, that doesn't use i */
 UNUSED_PARAMETER(i);
#endif
}
```
This allows max documentation of **programmer intent**, which conveys a valuable security message.
The only reason for `UNUSED_PARAMETER()` and `UNUSED_VARIABLE()` is documentation; they do the same thing.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 01:23
\| \|
What would be a good algorithm for ROSE to try and detect this? I thought at first that looking for two consecutive writes to a variable without an intervening read should set off a flag, but looking trough our code there seem to be plenty of cases in which that is not a violation...
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 30, 2008 10:44
\| \|
I think that the title and content of this recommendation should be modified to explicitly mention unreferenced formal parameters as well.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 01, 2008 09:49
\|
