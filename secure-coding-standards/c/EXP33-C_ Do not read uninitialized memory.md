Local, automatic variables assume unexpected values if they are read before they are initialized. The C Standard, 6.7.11, paragraph 11, specifies \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]
> If an object that has automatic storage duration is not initialized explicitly, its representation is indeterminate.

See [undefined behavior 11](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_11).
When local, automatic variables are stored on the program stack, for example, their values default to whichever values are currently stored in stack memory.
Additionally, some dynamic memory allocation functions do not initialize the contents of the memory they allocate.

| Function | Initialization |
| ----|----|
| aligned_alloc() | Does not perform initialization |
| calloc() | Zero-initializes allocated memory |
| malloc() | Does not perform initialization |
| realloc() | Copies contents from original pointer; may not initialize all memory |

Uninitialized automatic variables or dynamically allocated memory has [indeterminate values](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue), which for objects of some types, can be a [trap representation](BB.-Definitions_87152273.html#BB.Definitions-traprepresentation). Reading such trap representations is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior); it can cause a program to behave in an [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) manner and provide an avenue for attack. (See [undefined behavior 10](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_10) and [undefined behavior 12](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_12).)  In many cases, compilers issue a warning diagnostic message when reading uninitialized variables. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels) for more information.)
## Noncompliant Code Example (Return-by-Reference)
In this noncompliant code example, the `set_flag()` function is intended to set the parameter, `sign_flag`, to the sign of `number`. However, the programmer neglected to account for the case where `number` is equal to `0`. Because the local variable `sign` is uninitialized when calling `set_flag()` and is never written to by `set_flag()`, the comparison operation exhibits [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when reading `sign`.
``` c
void set_flag(int number, int *sign_flag) {
  if (NULL == sign_flag) {
    return;
  }
  if (number > 0) {
    *sign_flag = 1;
  } else if (number < 0) {
    *sign_flag = -1;
  }
}
int is_negative(int number) {
  int sign;
  set_flag(number, &sign);
  return sign < 0;
}
```
Some compilers assume that when the address of an uninitialized variable is passed to a function, the variable is initialized within that function. Because compilers frequently fail to diagnose any resulting failure to initialize the variable, the programmer must apply additional scrutiny to ensure the correctness of the code.
This defect results from a failure to consider all possible data states. (See [MSC01-C. Strive for logical completeness](MSC01-C_%20Strive%20for%20logical%20completeness) for more information.)
## Compliant Solution (Return-by-Reference)
This compliant solution trivially repairs the problem by accounting for the possibility that `number` can be equal to 0.
Although compilers and [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis) tools often detect uses of uninitialized variables when they have access to the source code, diagnosing the problem is difficult or impossible when either the initialization or the use takes place in object code for which the source code is inaccessible. Unless doing so is prohibitive for performance reasons, an additional defense-in-depth practice worth considering is to initialize local variables immediately after declaration.
``` c
void set_flag(int number, int *sign_flag) {
  if (NULL == sign_flag) {
    return;
  }
  /* Account for number being 0 */
  if (number >= 0) { 
    *sign_flag = 1;
  } else {
    *sign_flag = -1;
  }
}
int is_negative(int number) {
  int sign = 0; /* Initialize for defense-in-depth */
  set_flag(number, &sign);
  return sign < 0;
}
```
## Noncompliant Code Example (Uninitialized Local)
In this noncompliant code example, the programmer mistakenly fails to set the local variable `error_log` to the `msg` argument in the `report_error()` function \[[Mercy 2006](AA.-Bibliography_87152170.html#AA.Bibliography-mercy06)\]. Because `error_log` has not been initialized, an [indeterminate value](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) is read. The `sprintf()` call copies data from the arbitrary location pointed to by the indeterminate `error_log` variable until a null byte is reached, which can result in a buffer overflow.
``` c
#include <stdio.h>
/* Get username and password from user, return -1 on error */
extern int do_auth(void);
enum { BUFFERSIZE = 24 }; 
void report_error(const char *msg) {
  const char *error_log;
  char buffer[BUFFERSIZE];
  sprintf(buffer, "Error: %s", error_log);
  printf("%s\n", buffer);
}
int main(void) {
  if (do_auth() == -1) {
    report_error("Unable to login");
  }
  return 0;
}
```
## Noncompliant Code Example (Uninitialized Local)
In this noncompliant code example, the `report_error()` function has been modified so that `error_log` is properly initialized:
``` c
#include <stdio.h>
enum { BUFFERSIZE = 24 }; 
void report_error(const char *msg) {
  const char *error_log = msg;
  char buffer[BUFFERSIZE];
  sprintf(buffer, "Error: %s", error_log);
  printf("%s\n", buffer);
}
```
This example remains problematic because a buffer overflow will occur if the null-terminated byte string referenced by `msg` is greater than 17 characters, including the null terminator. (See [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator) for more information.)
## Compliant Solution (Uninitialized Local)
In this compliant solution, the buffer overflow is eliminated by calling the `snprintf()` function:
``` c
#include <stdio.h>
enum { BUFFERSIZE = 24 };
void report_error(const char *msg) {
  char buffer[BUFFERSIZE];
  if (0 < snprintf(buffer, BUFFERSIZE, "Error: %s", msg))
    printf("%s\n", buffer);
  else
    puts("Unknown error");
}
```
## Compliant Solution (Uninitialized Local)
A less error-prone compliant solution is to simply print the error message directly instead of using an intermediate buffer:
``` c
#include <stdio.h>
void report_error(const char *msg) {
  printf("Error: %s\n", msg);
}
```
## Noncompliant Code Example (`mbstate_t`)
In this noncompliant code example, the function `mbrlen()` is passed the address of an automatic `mbstate_t` object that has not been properly initialized. This is [undefined behavior 200](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_200) because `mbrlen()` dereferences and reads its third argument.
``` c
#include <string.h> 
#include <wchar.h>
void func(const char *mbs) {
  size_t len;
  mbstate_t state;
  len = mbrlen(mbs, strlen(mbs), &state);
}
```
## Compliant Solution (`mbstate_t`)
Before being passed to a multibyte conversion function, an `mbstate_t` object must be either initialized to the initial conversion state or set to a value that corresponds to the most recent shift state by a prior call to a multibyte conversion function. This compliant solution sets the `mbstate_t` object to the initial conversion state by setting it to all zeros:
``` c
#include <string.h> 
#include <wchar.h>
void func(const char *mbs) {
  size_t len;
  mbstate_t state;
  memset(&state, 0, sizeof(state));
  len = mbrlen(mbs, strlen(mbs), &state);
}
```
## Noncompliant Code Example (POSIX, Entropy)
In this noncompliant code example described in "[More Randomness or Less](http://kqueue.org/blog/2012/06/25/more-randomness-or-less/)" \[[Wang 2012](AA.-Bibliography_87152170.html#AA.Bibliography-Wang12)\], the process ID, time of day, and uninitialized memory `junk` is used to seed a random number generator. This behavior is characteristic of some distributions derived from Debian Linux that use uninitialized memory as a source of entropy because the value stored in `junk` is indeterminate. However, because accessing an [indeterminate value](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), compilers may optimize out the uninitialized variable access completely, leaving only the time and process ID and resulting in a loss of desired entropy.
``` c
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/time.h>
void func(void) {
  struct timeval tv;
  unsigned long junk;
  gettimeofday(&tv, NULL);
  srandom((getpid() << 16) ^ tv.tv_sec ^ tv.tv_usec ^ junk);
}
```
In security protocols that rely on unpredictability, such as RSA encryption, a loss in entropy results in a less secure system.
## Compliant Solution (POSIX, Entropy)
This compliant solution seeds the random number generator by using the CPU clock and the real-time clock instead of reading uninitialized memory:
``` c
#include <time.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/time.h>
void func(void) {     
  double cpu_time;
  struct timeval tv;
  cpu_time = ((double) clock()) / CLOCKS_PER_SEC;
  gettimeofday(&tv, NULL);
  srandom((getpid() << 16) ^ tv.tv_sec ^ tv.tv_usec ^ cpu_time);
}
```
## Noncompliant Code Example (`realloc()`)
The `realloc()` function changes the size of a dynamically allocated memory object. The initial `size` bytes of the returned memory object are unchanged, but any newly added space is uninitialized, and its value is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue). As in the case of `malloc()`, accessing memory beyond the size of the original object is [undefined behavior 186](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_186).
It is the programmer's responsibility to ensure that any memory allocated with `malloc()` and `realloc()` is properly initialized before it is used.
In this noncompliant code example, an array is allocated with `malloc()` and properly initialized. At a later point, the array is grown to a larger size but not initialized beyond what the original array contained. Subsequently accessing the uninitialized bytes in the new array is undefined behavior.
``` c
#include <stdlib.h>
#include <stdio.h>
enum { OLD_SIZE = 10, NEW_SIZE = 20 };
int *resize_array(int *array, size_t count) {
  if (0 == count) {
    return 0;
  }
  int *ret = (int *)realloc(array, count * sizeof(int));
  if (!ret) {
    free(array);
    return 0;
  }
  return ret;
}
void func(void) {
  int *array = (int *)malloc(OLD_SIZE * sizeof(int));
  if (0 == array) {
    /* Handle error */
  }
  for (size_t i = 0; i < OLD_SIZE; ++i) {
    array[i] = i;
  }
  array = resize_array(array, NEW_SIZE);
  if (0 == array) {
    /* Handle error */
  }
  for (size_t i = 0; i < NEW_SIZE; ++i) {
    printf("%d ", array[i]);
  }
}
```
## Compliant Solution (`realloc()`)
In this compliant solution, the `resize_array()` helper function takes a second parameter for the old size of the array so that it can initialize any newly allocated elements:
``` c
#include <stdlib.h>
#include <stdio.h> 
#include <string.h>
enum { OLD_SIZE = 10, NEW_SIZE = 20 };
int *resize_array(int *array, size_t old_count, size_t new_count) {
  if (0 == new_count) {
    return 0;
  }
  int *ret = (int *)realloc(array, new_count * sizeof(int));
  if (!ret) {
    free(array);
    return 0;
  }
  if (new_count > old_count) {
    memset(ret + old_count, 0, (new_count - old_count) * sizeof(int));
  }
  return ret;
}
void func(void) {
  int *array = (int *)malloc(OLD_SIZE * sizeof(int));
  if (0 == array) {
    /* Handle error */
  }
  for (size_t i = 0; i < OLD_SIZE; ++i) {
    array[i] = i;
  }
  array = resize_array(array, OLD_SIZE, NEW_SIZE);
  if (0 == array) {
    /* Handle error */
  }
  for (size_t i = 0; i < NEW_SIZE; ++i) {
    printf("%d ", array[i]);
  }
}
```
## Exceptions
**EXP33-C-EX1:** Reading uninitialized memory by an [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) of type `unsigned char` that could not have been declared with the `register` storage class does not trigger [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The `unsigned char` type is defined to not have a trap representation, which allows for moving bytes without knowing if they are initialized. (See the C Standard, 6.2.6.1, paragraph 3.) The requirement that `register` could not have been used (not merely that it was not used) is because on some architectures, such as the Intel Itanium, registers have a bit to indicate whether or not they have been initialized. The C Standard, 6.3.2.1, paragraph 2, allows such [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) to cause a trap for an object that never had its address taken and is stored in a register if such an object is referred to in any way.
## Risk Assessment
Reading uninitialized variables is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and can result in [unexpected program behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior). In some cases, these [security flaws](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) may allow the execution of arbitrary code.
Reading uninitialized variables for creating entropy is problematic because these memory accesses can be removed by compiler optimization. [VU#925211](http://www.kb.cert.org/vuls/id/925211) is an example of a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) caused by this coding error.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP33-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | uninitialized-local-readuninitialized-variable-use | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP33 |  |
| CodeSonar | 8.3p0 | LANG.MEM.UVAR | Uninitialized variable |
| Compass/ROSE |  |  | Automatically detects simple violations of this rule, although it may return some false positives. It may not catch more complex violations, such as initialization within functions taking uninitialized variables as arguments. It does catch the second noncompliant code example, and can be extended to catch the first as well |
| Coverity | 2017.07 | UNINIT | Implemented |
| Cppcheck | ;2.15 | uninitvaruninitdata
uninitstring
uninitMemberVar
uninitStructMember |  |
| Cppcheck Premium | 24.11.0 | uninitvaruninitdata
uninitstring
uninitMemberVar
uninitStructMember |  |
| GCC | 4.3.5 |  | Can detect some;violations of this rule when the -Wuninitialized flag is used |
| Helix QAC | 2024.4 | DF2726, DF2727, DF2728, DF2961, DF2962, DF2963, DF2966, DF2967, DF2968, DF2971, DF2972, DF2973, DF2976, DF2977, DF2978 | Fully implemented |
| Klocwork | 2024.4 | UNINIT.HEAP.MIGHTUNINIT.HEAP.MUST
UNINIT.STACK.ARRAY.MIGHT
UNINIT.STACK.ARRAY.MUST 
UNINIT.STACK.ARRAY.PARTIAL.MUST
UNINIT.STACK.MIGHT
UNINIT.STACK.MUST | Fully implemented |
| LDRA tool suite | 9.7.1 | 53 D, 69 D, 631 S, 652 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP33-a | Avoid use before initialization |
| Parasoft Insure++ | 2024.2 |  | Runtime analysis |
| PC-lint Plus | 1.4 | 530, 603, 644, 901 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP33-C | Checks for:Non-initialized variableNon-initialized pointerRule partially covered |
| PVS-Studio | 7.35 | V573, V614, V670, V679, V1050 |  |
| RuleChecker | 24.04 | uninitialized-local-read | Partially checked |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | initialisation | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
[CVE-2009-1888](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1888) results from a violation of this rule. Some versions of SAMBA (up to 3.3.5) call a function that takes in two potentially uninitialized variables involving access rights. An attacker can [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) these coding errors to bypass the access control list and gain access to protected files \[[xorl 2009](http://xorl.wordpress.com/2009/06/26/cve-2009-1888-samba-acls-uninitialized-memory-read/)\].
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | MSC00-C. Compile cleanly at high warning levels | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | MSC01-C. Strive for logical completeness | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | EXP53-CPP. Do not read uninitialized memory | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Initialization of Variables [LAV] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Referencing uninitialized memory [uninitref] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-456 | 2017-07-05: CERT: Exact |
| CWE 2.11 | CWE-457 | 2017-07-05: CERT: Exact |
| CWE 2.11 | CWE-758 | 2017-07-05: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-908 | 2017-07-05: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-119 and EXP33-C
-   Intersection( CWE-119, EXP33-C) = Ø
-   EXP33-C is about reading uninitialized memory, but this memory is considered part of a valid buffer (on the stack, or returned by a heap function). No buffer overflow is involved.
### CWE-676 and EXP33-C
-   Intersection( CWE-676, EXP33-C) = Ø
-   EXP33-C implies that memory allocation functions (e.g., malloc()) are dangerous because they do not initialize the memory they reserve. However, the danger is not in their invocation, but rather reading their returned memory without initializing it.
### CWE-758 and EXP33-C
Independent( INT34-C, INT36-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( EXP33-C, list) where list =
-   Undefined behavior that results from anything other than reading uninitialized memory
### CWE-665 and EXP33-C
Intersection( CWE-665, EXP33-C) = Ø
CWE-665 is about correctly initializing items (usually objects), not reading them later. EXP33-C is about reading memory later (that has not been initialized).
### CWE-908 and EXP33-C
CWE-908 = Union( EXP33-C, list) where list =
-   Use of uninitialized items besides raw memory (objects, disk space, etc)
New CWE-CERT mappings:
### CWE-123 and EXP33-C
Intersection( CWE-123, EXP33-C) = Ø
EXP33-C is only about reading uninitialized memory, not writing, whereas CWE-123 is about writing.
### CWE-824 and EXP33-C
EXP33-C = Union( CWE-824, list) where list =
-   Read of uninitialized memory that does not represent a pointer
## Bibliography

|  |  |
| ----|----|
| [Flake 2006] |  |
| [ISO/IEC 9899:2024] | Subclause 6.7.11, "Initialization"Subclause 6.2.6.1, "General"
Subclause 6.3.2.1, "Lvalues, Arrays, and Function Designators" |
| [Mercy 2006] |  |
| [VU#925211] |  |
| [Wang 2012] | "More Randomness or Less" |
| [xorl 2009] | "CVE-2009-1888: SAMBA ACLs Uninitialized Memory Read" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152412) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152449)
## Comments:

|  |
| ----|
| If programmers ignore compiler warnings about uninitialized values, that is the insecure coding practice.
Compilers can catch this error quite well.; Adding an irrelevant initialization simply makes that level of compiler analysis unavailable.  I've seen too many cases where a programmer was told to clean up the warning and responded by simply adding an initialization - changing code that used an unpredictable value inappropriately to code that used a predictable value inappropriately.  Or, looking at it another way, this change converts a bug that can easily be found by static analysis to one that cannot be found by any reasonable automatic analysis.
If you're using a C99 compiler, you can usually put off declaring variables until you are in a position to give them an appropriate value.  Most C++ writers recommend a style in which variable declaration is put off until an actual value is available.  Personally, I don't like that style, since it makes it hard to find the declaration of a variable - and thus the most fundamental property of the variable, its type.  (Of course, if you assume you always read your code in an IDE, this may be a non-issue for you.)
The hard cases - which I've found to be the source of many bugs - is a variable that is supposed to be set by, say, each arm of a switch or if/then/else; or by the first iteration of a loop; and is then used after the body of the switch or loop.  Then it turns out that one arm of the switch or if/then/else forgets to set the value, or the loop unexpectedly has a zero trip count.  Not only are these risky; I would contend that they account for a large fraction of actual bugs due to uninitialized variables.  Most compilers these days will catch these.  But requiring that the value be given some arbitrary initial value disables the compiler analysis - at which point you can have a very subtle failure.
                                                                                                                                                                                         -- Jerry
                                        Posted by leichter@lrw.com at Sep 01, 2006 14:08
                                     |
| In my opinion -- and in my experience -- the advice to initialize variables reflexively is bad advice.; Often, it merely replaces an "unpredictable" value with a "wrong" value, which does not improve the program's characteristics.  True, a consistent wrong value may be easier to debug than a Heisenbuggly unpredictable value.  But (as the article itself admits) compilers are pretty good at dataflow analysis, and many if not most will squawk if the code uses a variable that is not provably initialized on all paths leading to the reference.  Blanket initialization completely defeats such analysis, suppressing a compile-time diagnostic in favor of a run-time error and late nights with the debugger.  This is a step in the wrong direction, a denial of one of the major themes of software enginerring ("Bug cost increases with time to removal"), and an initiative that should be resisted steadfastly.
Rescind this rotten rule.
 --
Eric Sosman
esosman AT ieee  org
                                        Posted by  at Sep 01, 2006 21:50
                                     |
| 
I've narrowed this rule down to "do not reference uninitialized variables" which makes more sense to me.  Next, I'll probably have to move it to the Expressions section as it is no longer focused on declarations.
This is a much less drastic fix than you suggested, but I think it does the trick.  Plus, I like the non-compliant example because it shows the security risk.  Let me know if you are happy with this solution.
                                        Posted by rcs at Sep 02, 2006 13:52
                                     |
| This presentation isolates an interesting pattern that could lead to uninitialized variable use without compiler warnings. Halvar says that basically, since the compiler doesn't do interprocedural dataflow analysis, if you have a variable x, and you pass &x to another function, then x is considered to be initialized after the function call. If the function didn't actually touch x, you could be in trouble. This seems like a reasonably plausible idiom, but I haven't thought too hard about how it would manifest itself in real software.
Anyway, I know this doesn't help much with revising this rule, but I thought it was interesting.
 http://www.blackhat.com/presentations/bh-europe-06/bh-eu-06-Flake.pdf
                                        Posted by jm at Dec 25, 2006 10:49
                                     |
| I added an example to capture this idiom. 
                                        Posted by jsg at Mar 05, 2007 13:26
                                     |
| See: http://gcc.gnu.org/bugzilla/show_bug.cgi?id=35534 for an interesting example of inter-procedural data flow analysis in GCC 4.3.0 on the source of GDB 6.7.1.; The hack fix I used to get GDB to compile with -Werror was basically the 'initialize variable' hack that the other correspondents maligned.  The fix chosen by GDB in the 6.8 development code was to set the variable in the called function.  The original code in GDB was safe - the 'unset' variable was not referenced when not initialized because of the return status; but it would be pretty hard for a compiler to determine that.  The fix avoids the issue by ensuring that the variable is initialized even though it was benign.  (Note: GDB compiles with -Werror, which converts warnings into errors.)
This is a valid reason for initializing a variable when it isn't strictly necessary - the compiler complains even though you can see that the compiler's complaint is not actually valid.  I've had this sort of problem more than once.  Granted, there are times when the 'fix' conceals a real problem; there are, in my experience, more occasions when the 'fix' stops an incorrect warning by the compiler. 
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 22:41
                                     |
| There are static analysis techniques that can catch the failure even when an inappropriate initialization is present.
The variable can be in one of the following states:
Undefined;  ( U ) - The value is indeterminate;
Referenced ( R ) - The value is used in some way (e.g. an expression);
Defined      ( D ) - The variable is explicitly initialized (not default initialized) or assigned a value.
Given the above, the following data-flow anomalies can be detected.
UR - Variable is not assigned a value before use;
DU - Variable is assigned a value that is never used;
DD - Variable is assigned a value twice with no intermediate use.
So, if a variable is initialized to hide a warning (UR anomaly) that exists on one path, DD anomaly(s) with then exist in the other path(s).
                                        Posted by keylevel at Mar 26, 2008 12:35
                                     |
| I have just added a reference to the Debian/OpenSSL vul, stating facts without interpretations.
One can argue that unitialized memory can be securely used as a source of entropy, as illustrated by OpenSSL. But I feel that the vul does not constitute a valid exception to this rule. This is far too narrow of a scope to warrant invalidating this rule. One may also argue that the unitialized memory usage was unnecessary, as random keys were already generated by other means. Furthermore, one can argue that since code validators and other programmers treat unitialized memory usage as a bug, doing so is likely to lead to misunderstandings about the code intentions and subsequent vulnerabilities, again as illustreated by OpenSSL.
                                        Posted by svoboda at Jun 04, 2008 11:52
                                     |
| Typo: "OpenSSL code utilized initialized memory" should be "uninitialized".
I've looked a bit closer at that issue now - check this writeup and the Debian bug report it refers to before assigning blame.;  Fine demonstration of how unclean code was "enhanced" by procedural problems and carelessness into a huge bug.  As far as the OpenSSL codebase is concerned it might have been avoided if they had isolated the unclean code, included strong comments, and a valid if(don't be clever) code path instead of a debugging path which wasn't that important since it after all was just for debugging.  In short, deliberate unclean code requires discipline.
As for whether this should be a rule or not: Seems simple enough.  If this can't be a rule then probably quite a lot of other rules can't be either.  (Several of which I disagree with, but that's another matter.  I won't be following this standard anyway.)  Another case I know of is that Berkeley DB for the sake of performance does not initialize uninteresting bytes before writing them to disk.  I haven't checked what kind of data exactly.  Padding bytes in structs, maybe.  But if so it doesn't actually break this rule since the structs themselves would be initialized.
Which reminds me - it's not just uninitialized variables which should not be used.  Uninitialized memory is more correct, like memory from malloc().  But then padding bytes must be an exception.  Not sure if it's worth the wordsmithing to get it quite right. 
                                        Posted by hbf at Jun 05, 2008 10:28
                                     |
| fixed the typo and added a comment about malloc()
                                        Posted by avolkovi at Jun 05, 2008 10:43
                                     |
| However, on some architectures, such as the Intel Itanium, registers have a bit to indicate whether or not they have been initialized. The C Standard, 6.3.2.1, paragraph 2, allows such implementations to cause a trap for an object that never had its address taken and is stored in a register if such an object is referred to in any way.Is it forbidden only on such platforms or is it forbidden on all platforms?According to my reading of the standard, it is always undefined.
                                        Posted by ntysdd at Aug 17, 2014 14:51
                                     |
| Reading uninitialized values through an;unsigned char is allowed, except in the circumstances where that value has never had its address taken and the value is stored in a register, for some architectures. Eg)
register unsigned char c; // Presume the compiler honors the register keyword
if (c) {} // Possible UB
register unsigned char c2; // Similar
(void)&c2;
if (c2) {} // Okay
memcpy(&c, &c2, 1); // Also okay

So I would say this is only narrowly forbidden on some platforms, and only when working with a nonpointer value. Effectively, this exception is what allows you to implement `memcpy()`.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 18, 2014 08:44
\| \|
Yes, I know the intent.
It seems perfect legal in C99 wording, and suddenly becomes UB in C11.
What I want to say is that, the standard doesn't say "it may be put in a register which may contain special trap representation", instead it says something like "read if never initialized is UB". So it seems perfect legal for the compiler to exploit the fact that the read may never happen.
![](images/icons/contenttypes/comment_16.png) Posted by ntysdd at Aug 18, 2014 10:04
\| \|
There are several issues here that need to be addressed.
1.  ;"Is it forbidden only on such platforms or is it forbidden on all platforms?"  
    No, it is never forbidden.  That is not what undefined behavior means.
2.  "According to my reading of the standard, it is always undefined."  
    That is correct.
3.  "It seems perfect legal in C99 wording, and suddenly becomes UB in C11."  
    a.  The standard never addresses legality.  That would affect the sovereignty of countries that adopt the standard.  The standard does address validity.  
    b.  Undefined behavior is not invalid code.  It is valid code for which the standard does not impose requirements.  
    c.  Reading through uninitialized register-capable lvalues was not called out as undefined behavior in C99.  This was an oversight that was corrected in C11.  It has always resulted in something you didn't want; it just happens to be even more dangerous on architectures that trap.
This is one of the reasons undefined behavior exists.  It serves as a warning that different hardware behaves differently, possibly with dangerous results.  It is never useful to read uninitialized register-capable variables, so nothing has been lost.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Aug 19, 2014 14:54
\| \|
If the C standard doesn't impose any reqirements for some code, why should it be called valid code?
> It has always resulted in something you didn't want; it just happens to be even more dangerous on architectures that trap.

The standard doesn't impose any reqirements, so it is equally dangerous everywhere.
Why care the hardware? The standard is some contract between a programmer and an implementation, and the implementation is not hardware alone.
A sufficiently advanced compiler is indistinguishable from an adversary.
![](images/icons/contenttypes/comment_16.png) Posted by ntysdd at Aug 20, 2014 08:40
\| \|
nytsdd,
I'm fairly sympathetic to your comments.; The bottom line for the C Committee is that there is no useful purpose for reading uninitialized registers in the C language, so this was made undefined behavior to allow for optimization opportunities.  This is a logical and consistent decision for WG14 to reach.  My experience has also been that hardware drives the requirements of the C Standard more than anything else. 
In this coding standard, we recommend [MSC15-C. Do not depend on undefined behavior](https://www.securecoding.cert.org/confluence/display/seccode/MSC15-C.+Do+not+depend+on+undefined+behavior), and in this particular rule, we require that code not read uninitialized memory, which eliminates the undefined behavior.  We allow an exception for reading uninitialized memory by an [lvalue](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-lvalue) of type `unsigned char`, and then we have an exception to the exception for an object that never had its address taken and is stored in a register.  If you follow our coding standard, even an advanced compiler cannot defeat you. ;^)
I do like your comment, however.  OK if I quote it in my "Dangerous Optimizations" lecture?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 20, 2014 09:27
\| \|
> A sufficiently advanced compiler is indistinguishable from an adversary.

I don't mind if you quote it, but I myself quote it from <http://blog.regehr.org/archives/970> , and I don't know the original source.
![](images/icons/contenttypes/comment_16.png) Posted by ntysdd at Aug 21, 2014 11:31
\| \|
Note in C90 reading from an indeterminate value was in the definition of undefined behavior, it became more nuanced in C99 and then stricter in C11. We can see the history laid out well in this article: [Reading indeterminate contents might as well be undefined](http://blog.frama-c.com/index.php?post/2013/03/13/indeterminate-undefined)
Also interesting to note that in C++ prior to C++14 the standard used indeterminate value without actually defining the term and then in C++14 made using an indeterminate value undefined behavior except in the case of unsigned narrow types see;[this Stackoverflow question](http://stackoverflow.com/questions/23415661/has-c-standard-changed-with-respect-to-the-use-of-indeterminate-values-and-und)
![](images/icons/contenttypes/comment_16.png) Posted by samsmith at Dec 19, 2016 00:38
\| \|
The realloc() example has a potential memory leak:
`int` `*resize_array(``int` `*array, ``size_t` `old_count, ``size_t` `new_count) {``  ``if` `(0 == new_count) {`  
`    ``return` `0; // --- ``free`` array before returning error`  
`  ``}`  
`...`  
![](images/icons/contenttypes/comment_16.png) Posted by stevecom2 at May 18, 2020 05:04
\| \|
The problem of passing 0 as a new size to realloc() is much worse than potentially causing a memory leak. I will refer you to Defect Report 400:<http://www.open-std.org/jtc1/sc22/wg14/www/docs/dr_400.htm>  
which points out that this is implemented inconsistently on different platforms. The ISO C committee has decided that passing 0 to realloc() is Undefined Behavior.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2020 10:39
\| \|
The exception here seems a bit too broad. Here's what the standard says:
> If the lvalue designates an object of automatic storage duration that could have been declared with the `register` storage class (never had its address taken), and that object is uninitialized (not declared with an initializer and no assignment to it has been performed prior to use), the behavior is undefined.

Our exception makes it sound like it's safe to read an uninitialized `unsigned char` as long as it's not actually in a register on an architecture like Itanium. In fact, it's not safe even if the compiler could have put it in a register but chose not to, and even if you're on an architecture where all register values are valid. It's only safe when it couldn't have been declared `register`. Suggested new wording:
**EXP33-C-EX1:** Reading uninitialized memory by an [lvalue](https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-lvalue) of type;`unsigned char` that could not have been declared with the `register` storage class does not trigger [undefined behavior](https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-undefinedbehavior). The `unsigned char` type is defined to not have a trap representation, which allows for moving bytes without knowing if they are initialized. (See the C Standard, 6.2.6.1, paragraph 3.) The requirement that `register` could not have been used (not merely that it was not used) is because on some architectures, such as the Intel Itanium, registers have a bit to indicate whether or not they have been initialized. The C Standard, 6.3.2.1, paragraph 2, allows [implementations](https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-implementation) to cause a trap for an object that never had its address taken and is stored in a register if such an object is referred to in any way.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 13:29
\| \|
I don't like the "`Initialize for defense-in-depth`" idea. If the thing that's supposed to be properly initializing my variable isn't, I'd rather find out with a warning at compile time than with a wrong value at runtime.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 13:34
\| \|
All of our examples fix the undefined behavior by not reading uninitialized memory at all. I think we should have one that shows how to safely do so with the exception.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 13:37
\| \|
I agree, a compile-time warning is better than a runtime wrong value. But ISO C does not guarantee that a compiler will issue a warning. So we have to accommodate those poor souls that use inferior compilers :)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 13:30
\| \|
The exception does hit at using memcpy() or a similar function to copy a set of bytes, some of which may not have been initialized. Is that insufficient?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 13:32
\| \|
Ultimately you are rewording the exception to be more normative (including the 'could not be a register') in the initial normative text. I made this change.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 02, 2020 13:35
\| \|
None of the examples use memcpy() though.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 02, 2020 14:11
\| \|
Hey, about the following solution:
``` java
enum { BUFFERSIZE = 24 };
void report_error(const char *msg) {
  char buffer[BUFFERSIZE];
  if (0 < snprintf(buffer, BUFFERSIZE, "Error: %s", msg))
    printf("%s\n", buffer);
  else
    puts("Unknown error");
}
```
Note there are two problems:
1.  `buffer`; isn't initialized and memset'ed to 0.  
    This means that for small `msg`  values, it would leak the previous stack frame content. 
2.  The check foran  error of `snprintf`  should actually be `BUFFERSIZE <= snprintf(...), not ``snprintf <= 0. `
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Feb 04, 2023 09:47
\| \|
Itay:
1\. You are correct in that buffer is not explicitly initialized, but this is not a problem. It is initialized by snprintf(), which does not ready buffer's former contents, but instead writes a fully null-terminated byte string (NTBS) containing up to BUFFERSIZE chars to buffer.
2\. If no error occurs, snprintf() returns the number of chars explicitly 'printed' to the buffer string. ;This will be the length of msg, plus the length of the string literal, plus 1 for the null terminator. This may be less than BUFFSIZE, but will be greater than 0.  The snprintf() command only returns a value \<0 if an error occurs. See [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) for more information about snprintf()'s error conditions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 06, 2023 12:48
\| \|
In the first non-compliant example code I wonder if the is_negative function is required to make it non-compliant? I.e. as a tool developer do I have to see a UB path (using whole program analysis).. or should I just assume that all pointers passed as parameter to a function can point at uninitialized data? Should I assume that global pointers can point at uninitialized data?
One possible heuristic using "shallow analysis" that would not effectively forbid lots of legitimate usage of pointer arguments would be that:
;\* if the pointer-data is const (const int \*ptr) then the data is "readonly". This rule will say that it must always point at initialized data. A function is allowed to dereference the ptr and read the data. Function calls are non compliant if the provided ptr may point at uninitialized data (only needs to look at function prototype of the called function not the function definition).
 \* If the pointer-data is non-const (int\* ptr) then it's allowed to point at uninitialized data. If the function reads \*ptr value before it has been written the function is non-compliant. The caller will probably expect that the pointer data is written..
![](images/icons/contenttypes/comment_16.png) Posted by dmarjamäk at Feb 06, 2025 05:08
\|
