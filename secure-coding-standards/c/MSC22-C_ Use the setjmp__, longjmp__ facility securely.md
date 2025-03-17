The `setjmp()` macro should be invoked from only one of the contexts listed in subclause 7.13.2.1 of the C Standard \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]. Invoking `setjmp()` outside of one of these contexts results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 125](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_125).)
After invoking `longjmp()`, non-volatile-qualified local objects should not be accessed if their values could have changed since the invocation of `setjmp()`. Their value in this case is considered [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue), and accessing them is undefined behavior. (See undefined behaviors [127](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_127) and [10](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_10).)
The `longjmp()` function should never be used to return control to a function that has terminated execution. (See [undefined behavior 126](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_126).)
Signal masks, floating-point status flags, and the state of open files are *not* saved by the `setjmp()` function. If signal masks need to be saved, the POSIX `sigsetjmp()` function should be used.
This recommendation is related to [SIG30-C. Call only asynchronous-safe functions within signal handlers](SIG30-C_%20Call%20only%20asynchronous-safe%20functions%20within%20signal%20handlers) and [ENV32-C. All exit handlers must return normally](ENV32-C_%20All%20exit%20handlers%20must%20return%20normally).
## Noncompliant Code Example
This noncompliant code example calls `setjmp()` in an assignment statement, resulting in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
jmp_buf buf;
void f(void) {
  int i = setjmp(buf);
  if (i == 0) {
    g();
  } else {
    /* longjmp was invoked */
  }
}
void g(void) {
  /* ... */
  longjmp(buf, 1);
}
```
## Compliant Solution
Placing the call to `setjmp()` in the `if` statement and, optionally, comparing it with a constant integer removes the undefined behavior, as shown in this compliant solution:
``` c
jmp_buf buf;
void f(void) {
  if (setjmp(buf) == 0) {
    g();
  } else {
    /* longjmp was invoked */
  }
}
void g(void) {
  /* ... */
  longjmp(buf, 1);
}
```
## Noncompliant Code Example
Any attempt to invoke the `longjmp()` function to transfer control to a function that has completed execution results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
static jmp_buf buf;
static void bad(void);
static void g(void) {
  if (setjmp(buf) == 0) {
    printf("setjmp() invoked\n");
  } else {
    printf("longjmp() invoked\n");
  }
}
static void f(void) {
  g();
}
static void setup(void) {
  f();
}
void do_stuff(void) {
  void (*b)(void) = bad;
  /* ... */
  longjmp(buf, 1);
}
static void bad(void) {
  printf("Should not be called!\n");
  exit(1);
}
int main(void) {
  setup();
  do_stuff();
}
```
## Implementation Details
Compiled at -O0 using GCC 7.5 or Clang 8.0 on Ubuntu 18.04 (Linux for x86-64), the preceding example outputs the following when run:
``` java
setjmp() invoked
longjmp() invoked
Should not be called!
```
Because `g()` has finished executing at the time `longjmp()` is called, it is no longer on the stack. When `do_stuff()` is invoked, its stack frame occupies the same memory as the old stack frame of `g()`. In this case, `a` was located in the same location as the return address of function `g()`. The assignment of `b` overwrites the return address, so when `longjmp()` sends control back to function `g()`, the function returns to the wrong address (in this case, to function `bad()`).
If the array `b` were user specified, the user would be able to set the return address of function `g()` to any location.
## Compliant Solution
The `longjmp()` function should be used only when the function containing the corresponding `setjmp()` is guaranteed not to have completed execution, as in the following example:
``` c
#include <setjmp.h>
#include <stdio.h>
#include <stdlib.h>
static jmp_buf buf;
static void bad(void);
void do_stuff(void) {
  void (*b)(void) = bad;
  /* ... */
  longjmp(buf, 1);
}
static void bad(void) {
  printf("Should not be called!\n");
  exit(1);
}
int main(void) {
  if (setjmp(buf) == 0) {
    printf("setjmp() invoked\n");
  } else {
    printf("longjmp() invoked\n");
  }
  do_stuff();
} 
```
There is no risk of overwriting a return address because the stack frame of `main()` (the function that invoked `setjmp()`) is still on the stack; so when `do_stuff()` is invoked, the two stack frames will not overlap.
## Noncompliant Code Example
In this noncompliant example, non-volatile-qualified objects local to the function that invoked the corresponding `setjmp()` have [indeterminate values](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) after `longjmp()` is executed if their value has been changed since the invocation of `setjmp()`:
``` c
jmp_buf buf;
void f(void) {
  int i = 0;
  if (setjmp(buf) != 0) {
    printf("%i\n", i);
    /* ... */
  }
  i = 2;
  g();
}
void g(void) {
  /* ... */
  longjmp(buf, 1);
}
```
## Implementation Details
Calling `f()` will print `2` if you compile with `-O0`, but will print `0` if you compile with `-O2`.  This involves using GCC 7.5 or Clang 8.0 on Ubuntu 18.04 (Linux x86-64).
## Compliant Solution
If an object local to the function that invoked `setjmp()` needs to be accessed after `longjmp()` returns control to the function, the object should be volatile-qualified:
``` c
jmp_buf buf;
void f(void) {
  volatile int i = 0;
  if (setjmp(buf) != 0) {
    printf("%i\n", i);
    /* ... */
  }
  i = 2;
  g();
}
void g(void) {
  /* ... */
  longjmp(buf, 1);
}
```
This will now correctly print `2` regardless of optimization level.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC22-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.LONGJMPBADFUNC.SETJMP | Use of longjmpUse of setjmp |
| LDRA tool suite | 9.7.1 | 43 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC22-a | The facilities provided by <setjmp.h> should not be used |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC22-C | Checks for use of setjmp/longjmp (rec. fully covered) |
| SonarQube C/C++ Plugin | 3.11 | S982 |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152327) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152033)
## Comments:

|  |
| ----|
| Good rule so far. Comments:
    I disagree with the Remediation Cost
    The two references can be merged since they come from the same document
Any attempt to longjmp to a function that has terminated execution results in possibly exploitable undefined behavior.
    How is it exploitable? Please provide details or remove that phrase. Perhaps an 'Implementation Details' section describing what actually happens when you run the NCCE on some platform would be helpful.
    By our style guidelines, you should say longjmp() rather than just longjmp.
                                        Posted by svoboda at Mar 03, 2010 11:42
                                     |
| I agree that Remediation Cost was off; I've changed it to medium. Two of the three rules should be automatically detectable (using setjmp() in the wrong place, and accessing non-volatile local objects), though I'm not sure if you can automatically detect a longjmp() to a terminated functions. If you can't, then should the remediation cost be set to high, or is medium good?
I've taken out the 'possibly exploitable' phrase for now. If I can confirm that is exploitable, I'll add in an example.
                                        Posted by rmcelrat at Mar 03, 2010 17:38
                                     |
| I'm willing to bet that (unless you are doing weird things with function pointers), you can always tell if a longjmp() call might occur at some point in the program where a setjmp() might not be in the call stack. That's a 99% guarantee, which IMHO is good enough to justify a medium remediation cost.
Good rule so far, but I'm really hungry for implementation details on various platforms.
                                        Posted by svoboda at Mar 03, 2010 18:02
                                     |
| In the second compliant solution, the behavior of the program is undefined when h() is invoked the second time, after the if statement in f() terminates (in other words, the if statement must return from f() in order for the solution to be compliant).
jmp_buf buf;
void f() {
  if (setjmp(buf) != 0) {
    /* longjmp was invoked */
  }
  h();   // called twice, once when setjmp(buf) == 0 holds and again when it doesn't
  return;
}
void h() {
  /* ... */
  longjmp(buf, 1);
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 03, 2010 22:17
\| \|
Is this actually undefined behavior? I can't find anything in the C99 standard saying multiple `longjmp()` invocations to the same `setjmp()` is undefined behavior.
Regardless, `h()` wasn't supposed to be called twice. It's fixed. Thanks for pointing it out
![](images/icons/contenttypes/comment_16.png) Posted by rmcelrat at Mar 03, 2010 22:54
\| \|
You're right, it's perfectly fine. There's even an example in the spec that looks similar to your original. I must have been thinking of `va_list`.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 04, 2010 21:14
\| \|
-   I like the behavior of the 2nd NCCE, changing a variable from 10 to 0. You could even fine-tune it to behave like the NCCE from [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations), which changes a char\* from a 'good' string literal to an 'evil' one.
<!-- -->
-   The 'Implementation Details' after the 2nd CS is unnecessary, as no undefined behavior occurs. If you like, the text there can just appear after the CS code itself.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 05, 2010 10:00
\| \|
The implementation details concerning the glibc v2.11.1 definition of the jmp_buf type seems like a distraction. Does this add anything to this guideline, or can it be removed?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 18, 2010 10:02
\| \|
Now that I think of it, shouldn't this be a rule? These calls are easy to misuse, and doing so is always UB. It may not be easy for a tool to detect misuse, but given that they are rare (used at most once in any program that uses them at all), not much onus on an auditor.
;
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 05, 2013 11:36
\|
