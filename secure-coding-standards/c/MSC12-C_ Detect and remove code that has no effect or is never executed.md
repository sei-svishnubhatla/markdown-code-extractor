Code that has no effect or is never executed (that is, dead or unreachable code) is typically the result of a coding error and can cause [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior). Such code is usually optimized out of a program during compilation. However, to improve readability and ensure that logic errors are resolved, it should be identified, understood, and eliminated.
Statements or expressions that have no effect should be identified and removed from code. Most modern compilers, in many cases, can warn about code that has no effect or is never executed. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).) 
## Noncompliant Code Example
This noncompliant code example demonstrates how dead code can be introduced into a program \[[Fortify 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Fortify06)\]. The second conditional statement, `if (s)`, will never evaluate true because it requires that `s` not be assigned `NULL`, and the only path where `s` can be assigned a non-null value ends with a `return` statement.
``` c
int func(int condition) {
    char *s = NULL;
    if (condition) {
        s = (char *)malloc(10);
        if (s == NULL) {
           /* Handle Error */
        }
        /* Process s */
        return 0;
    }
    /* Code that doesn't touch s */
    if (s) {
        /* This code is unreachable */
    }
    return 0;
}
```
## Compliant Solution
Remediation of dead code requires the programmer to determine why the code is never executed and then to resolve the situation appropriately. To correct the preceding noncompliant code, the `return` is removed from the body of the first conditional statement.
``` c
int func(int condition) {
    char *s = NULL;
    if (condition) {
        s = (char *)malloc(10);
        if (s == NULL) {
           /* Handle error */
        }
        /* Process s */
    }
    /* Code that doesn't touch s */
    if (s) {
        /* This code is now reachable */
    }
    return 0;
}
```
## Noncompliant Code Example
In this example, the `strlen()` function is used to limit the number of times the function `s_loop()` will iterate. The conditional statement inside the loop evaluates to true when the current character in the string is the null terminator. However, because `strlen()` returns the number of characters that precede the null terminator, the conditional statement never evaluates true.
``` c
int s_loop(char *s) {
    size_t i;
    size_t len = strlen(s);
    for (i=0; i < len; i++) {
        /* Code that doesn't change s, i, or len */
      if (s[i] == '\0') {
        /* This code is never reached */
      }
    }
    return 0;
}
```
## Compliant Solution
Removing the dead code depends on the intent of the programmer. Assuming the intent is to flag and process the last character before the null terminator, the conditional is adjusted to correctly determine if the `i` refers to the index of the last character before the null terminator.
``` c
int s_loop(char *s) {
    size_t i;
    size_t len = strlen(s);
    for (i=0; i < len; i++) {
        /* Code that doesn't change s, i, or len */
      if (s[i+1] == '\0') {
        /* This code is now reached */
      }
    }
    return 0;
}
```
## Noncompliant Code Example (Assignment)
In this noncompliant code example, the comparison of `a` to `b` has no effect:
``` c
int a;
int b;
/* ... */
a == b;
```
This code is likely a case of the programmer mistakenly using the equals operator `==` instead of the assignment operator `=`.
## Compliant Solution (Assignment)
The assignment of `b` to `a` is now properly performed:
``` c
int a;
int b;
/* ... */
a = b;
```
## Noncompliant Code Example (Dereference)
In this example, a pointer increment and then a dereference occur, but the dereference has no effect:
``` c
int *p;
/* ... */
*p++;
```
## Compliant Solution (Dereference)
Correcting this example depends on the intent of the programmer. For example, if dereferencing `p` was a mistake, then `p` should not be dereferenced.
``` c
int *p;
/* ... */
++p;
```
If the intent was to increment the value referred to by `p`, then parentheses can be used to ensure `p` is dereferenced and then incremented. (See [EXP00-C. Use parentheses for precedence of operation](EXP00-C_%20Use%20parentheses%20for%20precedence%20of%20operation).)
``` c
int *p;
/* ... */
(*p)++;
```
Another possibility is that `p` is being used to reference a memory-mapped device. In this case, the variable `p` should be declared as `volatile`.
``` c
volatile int *p;
/* ... */
(void) *(p++);
```
## Noncompliant Code Example (if/else if)
A chain of if/else if statements is evaluated from top to bottom. At most, only one branch of the chain will be executed: the first one with a condition that evaluates to true. Consequently, duplicating a condition in a sequence of if/else if statements automatically leads to dead code.
``` c
if (param == 1)
   openWindow();
 else if (param == 2)
   closeWindow();
 else if (param == 1) /* Duplicated condition */
   moveWindowToTheBackground();
```
Note that duplicating a condition violates this guideline only if the duplicate conditions always behave similarly...see a compliant solution below for a condition that is textually a duplicate but behaves differently.
## Compliant Solution (if/else if)
In this compliant solution, the third conditional expression has been corrected.
``` c
if (param == 1)
   openWindow();
 else if (param == 2)
   closeWindow();
 else if (param == 3)
   moveWindowToTheBackground();
```
## Compliant Solution (Conditional Side-Effects)
This code does not violate this recommendation, because even though the conditions are textually identical, they have different side effects, because the `getc()`  function advances the stream marker.
``` c
if (getc() == ':')
   readMoreInput();
 else if (getc() == ':')
   readMoreInput();
 else if (getc() == ':')
   readMoreInput();
```
## Noncompliant Code Example (logical operators)
Using the same subexpression on either side of a logical operator is almost always a mistake.  In this noncompliant code example, the rightmost subexpression of the controlling expression of each `if` statement has no effect.  
``` c
if (a == b && a == b) { // if the first one is true, the second one is too
  do_x();
}
if (a == c || a == c ) { // if the first one is true, the second one is too
  do_w();
}
```
## Compliant Solution (logical operators)
In this compliant solution, the rightmost subexpression of the controlling expression of each `if` statement has been removed.
``` c
if (a == b) { 
  do_x();
}
if (a == c) { 
  do_w();
}
```
## Noncompliant Code Example (Unconditional Jump)
Unconditional jump statements typically has no effect.  
``` c
#include <stdio.h>
for (int i = 0; i < 10; ++i) {
  printf("i is %d", i);
  continue;  // this is meaningless; the loop would continue anyway
}
```
## Compliant Solution (Unconditional Jump)
The continue statement has been removed from this compliant solution.
``` c
#include <stdio.h>
for (int i = 0; i < 10; ++i) {
   printf("i is %d", i); 
}
```
## Exceptions
**MSC12-EX1:** In some situations, seemingly dead code may make software resilient. An example is the `default` label in a `switch` statement whose controlling expression has an enumerated type and that specifies labels for all enumerations of the type. (See [MSC01-C. Strive for logical completeness](MSC01-C_%20Strive%20for%20logical%20completeness).) Because valid values of an enumerated type include all those of its underlying integer type, unless enumeration constants are provided for all those values, the `default` label is appropriate and necessary.
``` c
typedef enum { Red, Green, Blue } Color;
const char* f(Color c) {
  switch (c) {
    case Red: return "Red";
    case Green: return "Green";
    case Blue: return "Blue";
    default: return "Unknown color";   /* Not dead code */
  }
}
void g() {
  Color unknown = (Color)123;
  puts(f(unknown));
}
```
**MSC12-EX2:** It is permissible to temporarily remove code that may be needed later. (See [MSC04-C. Use comments consistently and in a readable fashion](MSC04-C_%20Use%20comments%20consistently%20and%20in%20a%20readable%20fashion) for an illustration.)
**MSC12-EX3:** Unused functions and variables that are part of an exported library do not violate this guideline.  Likewise, code that is never executed because it is `#ifdef`ed out does not violate this guideline, on the grounds that it could be subsequently used in another application, or built on a different platform.
### Risk Assessment
The presence of code that has no effect or is never executed can indicate logic errors that may result in [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Such code can be introduced into programs in a variety of ways and eliminating it can require significant analysis.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC12-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | dead-assignmentdead-initializer
expression-result-unused
redundant-operation
unreachable-code
unreachable-code-after-jump
unused-function
statement-sideeffect | Supported + partially checked |
| CodeSonar | 8.3p0 | DIAG.UNEX.*LANG.STRUCT.EBS
LANG.STRUCT.RC
MISC.NOEFFECT
LANG.STRUCT.ALIGNAS.EZA
LANG.STRUCT.UA
LANG.STRUCT.UC
LANG.STRUCT.UULABEL
LANG.STRUCT.UUMACRO
LANG.STRUCT.UUPARAM
LANG.STRUCT.UUTAG
LANG.STRUCT.UUTYPE
LANG.STRUCT.UUVAR | Code not exercised by analysisEmpty branch statement checks
Redundant condition
Function call has no effect
Explicit zero alignment
Useless assignment
Unreachable code checks
Unused label
Unused macro
Unused parameter
Unused tag
Unused type
Unused variable |
| Coverity | 2017.07 | NO_EFFECT;DEADCODE  UNREACHABLE  | Finds statements or expressions that do not accomplish anything or statements that perform an unintended action.Can detect the specific instance where code can never be reached because of a logical contradiction or a dead "default" in switch statementCan detect the instances where code block is unreachable because of the syntactic structure of the code |
| ECLAIR | 1.2 | CC2.MSC12 | Partially implemented |
| GCC | 3.0 | -Wunused-value-Wunused-parameter
 | Options detect unused local variables,;nonconstant static variables and unused function parameters, or unreachable code respectively. |
| Helix QAC | 2024.4 | C3110, C3112, C3307, C3404, C3426, C3427 |  |
| Klocwork | 2024.4 | CWARN.NOEFFECT.SELF_ASSIGNCWARN.NOEFFECT.UCMP.GE
CWARN.NOEFFECT.UCMP.GE.MACRO
CWARN.NOEFFECT.UCMP.LT
CWARN.NOEFFECT.UCMP.LT.MACRO
CWARN.NULLCHECK.FUNCNAME
EFFECT
MISRA.STMT.NO_EFFECT
UNREACH.GEN
UNREACH.RETURN
UNREACH.SIZEOF
UNREACH.ENUM
LA_UNUSED
VA_UNUSED.GEN
VA_UNUSED.INIT
INVARIANT_CONDITION.UNREACH |  |
| LDRA tool suite | 9.7.1 | ;8 D, 65 D, 105 D, I J, 139 S, 140 S, 57 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC12-aCERT_C-MSC12-b
CERT_C-MSC12-c
CERT_C-MSC12-d
CERT_C-MSC12-e
CERT_C-MSC12-f
CERT_C-MSC12-g
CERT_C-MSC12-h
CERT_C-MSC12-i
CERT_C-MSC12-j
CERT_C-MSC12-k
 | There shall be no unreachable code in "else" blockThere shall be no unreachable code after 'return', 'break', 'continue', 'goto', 'throw' statements, and after calls to functions with the 'noreturn' attribute
There shall be no unreachable code in "if/else/while/for" block
There shall be no unreachable code in switch statement
There shall be no unreachable code in 'for' loop
There shall be no unreachable code after 'if' or 'switch' statement
There shall be no unreachable code after "if" or "switch" statement inside while/for/do...while loop
Avoid switch with unreachable branches
Avoid unreachable methods
Avoid conditions that always evaluate to the same value
All non-null statements shall either have at least one side-effect however executed or cause control flow to change |
| PC-lint Plus | 1.4 | 438, 474, 505, 522, 523,527, 528, 529, 563, 612,
714, 715, 719, 749, 750,
751, 752, 753, 754, 755,
756, 757, 758, 768, 769,
774, 827, 838, 1972 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC12-C | Checks for:Unreachable codeDead codeRec. partially covered. |
| RuleChecker | 24.04 | dead-assignmentdead-initializer
expression-result-unused
redundant-operation
unreachable-code-after-jump
unused-function
statement-sideeffect | Partially checked |
| SonarQube C/C++ Plugin | ;3.11 | S1764, S2589, S2583, S1116, S1172, S1763, S1862, S1065, S1656, S2754, S1751 |  |
| Splint | 3.1.1 | ;-standard | The default mode checks for unreachable code. |
| PVS-Studio | 7.35 | V551, V606, V649, V779 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC12-C).
[CVE-2014-1266](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-1266) results from a violation of this rule. There is a spurious `goto fail` statement on line 631 of [sslKeyExchange.c](http://opensource.apple.com/source/Security/Security-55471/libsecurity_ssl/lib/sslKeyExchange.c?txt). This `goto` statement gets executed unconditionally, even though it is indented as if it were part of the preceding `if` statement. As a result, the call to `sslRawVerify()` (which would perform the actual signature verification) becomes dead code \[[ImperialViolet 2014](https://www.imperialviolet.org/2014/02/22/applebug.html)\].
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC12-CPP. Detect and remove code that has no effect |
| ISO/IEC TR 24772 | Unspecified Functionality [BVQ]Likely Incorrect Expressions [KOA]
Dead and Deactivated Code [XYQ] |
| MISRA C:2012 | Rule 2.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [Fortify 2006] | Code Quality, "Dead Code" |
| [Coverity 2007] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152346) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152095)
## Comments:

|  |
| ----|
| > *p++;
This is not an example of dead code, or code with no effect, but *wrong code* - there is no chance that the developer has done this on purpose (or s/he would have done)
(void)*p++; // trust me, there's a good reason for this

(and I am hard-pressed to think of an actual good reason).;
So suggesting that this avoids a troublesome technique - which is by nature intentional - misses the fact that it's just wrong in every way.
One can't code secure if one doesn't actually know how C works. 
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 01:16
\| \|
If there is an actual reason, it would involve volatile qualification; I think I've seen some device driver code that did this.; (Reading the data reset the interrupt, and the following code wanted to use the next sequential register address.)  Certainly it is too "tricky" and should be rewritten for clarity, or else fully explained in a comment.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 14:38
\| \|
Is the statement "Most modern compilers can warn about code that has no effect" too wide? How many would detect the following?  
``` java
int has_dead_code ( int para )
{
   int local = 99;
   para  = para + local;
   local = para;         // Has no effect on program output
   if ( 0 == local )     // Has no effect on program output
   {
      ++local;           // Has no effect on program output
   }
   return para;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by keylevel at Jun 11, 2008 09:25
\| \|
I watered down the statement. It is usually not possible to be too wishy washy (in most cases). 8^)
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 11, 2008 09:45
\| \|
In "Noncompliant Code Example (Dereference)", the description and the code do not match.; The way the code is written "\*p++;", p is dereferenced and then incremented.  In order for p to be incremented and then dereferenced, as the description says, the code would need to say "\*++p;".
![](images/icons/contenttypes/comment_16.png) Posted by joe.konczal@nist.gov at Jun 18, 2010 14:27
\| \|
Sigh...if you know what the code does, the description does match it. But if you don't, it's easy to get the wrong impression from the description. This is a case where the code can not be described by simple English. The C binding rules parse **`p+`** **as** `(p+)`, which means the increment occurs before the dereference as stated. There is a trade-off between being accurate and being short...hopefully my rewrite succeeds on both counts.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 18, 2010 15:16
\| \|
Ok.; I see what you mean.  ANSI X3.159-1989 says that the postincrement operator is applied first to \*p++, but the p++ sub-expression's value is the original value of p, so after p is incremented the previous value of p is what is dereferenced. In most cases \*p++ *looks* as if p is dereferenced first, then incremented.
(When I use the Rich Text tab, some of the backslashes before star and plus are deleted, even after I explicitly added them in Wiki Markup, so some of the pluses are interpreted as text formatting.)
![](images/icons/contenttypes/comment_16.png) Posted by joe.konczal@nist.gov at Jun 18, 2010 16:50
\| \|
In [MISRA C:2012](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-MISRA12);parlance this appears to be "dead code".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 14, 2014 11:21
\| \|
The statement "duplicating a condition in a sequence of if/else if statements automatically leads to dead code." isn't always true, since not every condition yields the same result when evaluated multiple times. For example, there's no dead code here:
``` java
if(rand() % 3) {
    puts("In if");
} else if(rand() % 3) {
    puts("In else if");
}
```
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jan 04, 2021 12:50
\| \|
I would argue that if your conditions yield different results (as they do in your example) then your conditions are not duplicates (never mind that their text is identical), and so that statement does not apply to your code.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 04, 2021 13:57
\| \|
I think that's what we would want it to read as, but currently it just says "duplicate" which strongly implies to me "textually identical" conditions.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 04, 2021 14:03
\| \|
Technically, you're both right, the wording does allow for "textually duplicate", and could be interpreted to forbid @sible's code.
Remember that this is a recommendation not a rule, so I'm not sure that striving for the precision mandated by a rule is worthwhile. Precision is a good goal, and if it is attainable then we should go for it, so can we achieve technical precision here?
Offhand, I doubt it. Consider this variant of Joe's example:
    if (getc() == 'a') {  puts("1st char is a");
    } else if (getc() == 'a') {
      puts("2nd char is a");
    }
I'll argue this example is more pragmatic, but also has the same property; which is that getc() like rand() changes internal state.
Does anyone have a good suggestion for when textually-identical conditions do and do not lead to dead code?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 04, 2021 15:54
\| \|
> Does anyone have a good suggestion for when textually-identical conditions do and do not lead to dead code?

Off the top of my head, I'd say it's when the condition involves a side effect or a call to a function that's not "const" (in the GCC attribute sense: <https://gcc.gnu.org/onlinedocs/gcc/Common-Function-Attributes.html>).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 04, 2021 16:07
\| \|
I added a compliant solution based on my getc code example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 05, 2021 08:40
\|
