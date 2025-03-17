Software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) can result when a programmer fails to consider all possible data states.
## Noncompliant Code Example (`if` Chain)
This noncompliant code example fails to test for conditions where `a` is neither `b` nor `c`. This behavior may be correct in this case, but failure to account for all the values of `a` can result in logic errors if `a` unexpectedly assumes a different value.
``` c
if (a == b) {
  /* ... */
}
else if (a == c) {
  /* ... */
}
```
## Compliant Solution (`if` Chain)
This compliant solution explicitly checks for the unexpected condition and handles it appropriately:
``` c
if (a == b) {
  /* ... */
}
else if (a == c) {
  /* ... */
}
else {
  /* Handle error condition */
}
```
## Noncompliant Code Example (`switch`)
This noncompliant code example fails to consider all possible cases. Failure to account for all valid values of type `Color` will result in a logic error. Because valid values of an enumerated type include all those of its underlying integer type, unless enumeration constants have been provided for all those values, the `default` label is appropriate and necessary.
``` c
typedef enum { Red, Green, Blue } Color;
const char* f(Color c) {
  switch (c) {
    case Red: return "Red";
    case Green: return "Green";
    case Blue: return "Blue";
  }
}
void g() {
  Color unknown = (Color)123;
  puts(f(unknown));
}
```
### Implementation Details
Microsoft Visual C++ .NET with `/W4` does not warn when assigning an integer value to an `enum` type or when the `switch` statement does not contain all possible values of the enumeration.
## Compliant Solution (`switch`)
This compliant solution takes care to provide the `default` label to handle all valid values of type `Color`:
``` c
typedef enum { Red, Green, Blue } Color;
const char* f(Color c) {
  switch (c) {
    case Red: return "Red";
    case Green: return "Green";
    case Blue: return "Blue";
    default: return "Unknown color";   /* Necessary */
  }
}
```
Note that adding a default case to a `switch` statement, even when all possible `switch` labels are specified, is an exception ([MSC07-C-EX1](MSC07-C.-Detect-and-remove-dead-code_87152362.html#MSC07C.Detectandremovedeadcode-MSC07-EX1)) to [MSC07-C. Detect and remove dead code](MSC07-C_%20Detect%20and%20remove%20dead%20code).
An alternative compliant solution to the noncompliant code example is to provide a `return` statement after the `switch` statement. Note, however, that this solution may not be appropriate in all situations.
``` c
typedef enum { Red, Green, Blue } Color;
const char* f(Color c) {
  switch (c) {
    case Red: return "Red";
    case Green: return "Green";
    case Blue: return "Blue";
  }
  return "Unknown color";   /* Necessary */
}
```
### Historical Discussion
This practice has been a subject of debate for some time, but a clear direction has emerged.
Originally, the consensus among those writing best practices was simply that each `switch` statement should have a `default` label. Eventually, emerging compilers and [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis) tools could verify that a `switch` on an `enum` type contained a `case` label for each enumeration value, but only if no `default` label existed. This led to a shift toward purposely leaving out the `default` label to allow static analysis. However, the resulting code was then vulnerable to `enum` variables being assigned `int` values outside the set of `enum` values.
These two practices have now been merged. A `switch` on an `enum` type should now contain a `case` label for each `enum` value but should also contain a `default` label for safety. This practice does not add difficulty to [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis).
Existing implementations are in transition, with some not yet analyzing `switch` statements with `default` labels. Developers must take extra care to check their own `switch` statements until the new practice becomes universal.
## Noncompliant Code Example (Zune 30)
This noncompliant code example shows incomplete logic when converting dates. The code appeared in the Zune 30 media player, causing many players to lock up on December 30, 2008, at midnight PST. This noncompliant code example comes from the `ConvertDays` function in the real-time clock (RTC) routines for the MC13783 PMIC RTC. It takes the number of days since January 1, 1980, and computes the correct year and number of days since January 1 of the correct year.
The flaw in the code occurs when `days` has the value 366 because the loop never terminates. This bug manifested itself on the 366th day of 2008, which was the first leap year in which this code was active.
``` c
#define ORIGINYEAR 1980
UINT32 days = /* Number of days since January 1, 1980 */
int year = ORIGINYEAR;
/* ... */
while (days > 365) {
  if (IsLeapYear(year)) {
    if (days > 366) {
      days -= 366;
      year += 1;
    }
  }
  else {
    days -= 365;
    year += 1;
  }
}
```
## Compliant Solution (Zune 30)
The following proposed rewrite is provided at [http://winjade.net/2009/01/lesson-on-infinite-loops](http://winjade.net/2009/01/lesson-on-infinite-loops/). The loop is guaranteed to exit, because `days` decreases for each iteration of the loop, unless the `while` condition fails and the loop terminates.
``` c
#define ORIGINYEAR 1980
UINT32 days = /* Input parameter */
int year = ORIGINYEAR;
/* ... */
int daysThisYear = (IsLeapYear(year) ? 366 : 365);
while (days > daysThisYear) {
  days -= daysThisYear;
  year += 1;
  daysThisYear = (IsLeapYear(year) ? 366 : 365);
}
```
This compliant solution is for illustrative purposes and is not necessarily the solution implemented by Microsoft.
## Risk Assessment
Failing to account for all possibilities within a logic statement can lead to a corrupted running state, potentially resulting in unintentional information disclosure or [abnormal termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC01-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | missing-elseswitch-default | Partially checked |
| Compass/ROSE |  |  | Can detect some violations of this recommendation. In particular, it flags switch statements that do not have a default clause. ROSE should detect "fake switches" as well (that is, a chain of if statements each checking the value of the same variable). These if statements should always end in an else clause, or they should mathematically cover every possibility. For instance, consider the following:  if (x > 0) {
      /* ... */
  } else if (x < 0) {
    /* ... */
  } else if (x == 0) {
    /* ... */
  }

\| \| [GCC](GCC) \|
4.3.5
\| \|
Can detect some violations of this recommendation when the `-Wswitch` and `-Wswitch-default` flags are used
\| \| [Helix QAC](Helix%20QAC) \|
2024.4
\| **C2000, C2002, C2004** \| \| \| [Klocwork](Klocwork) \|
;2024.4
\|
**CWARN.EMPTY.LABEL;**  
**LA_UNUSED**  
**MISRA.IF.NO_ELSE**  
**MISRA.SWITCH.WELL_FORMED.DEFAULT.2012**  
**INFINITE_LOOP.GLOBAL**  
**INFINITE_LOOP.LOCAL**  
**INFINITE_LOOP.MACRO**
\| \| \| [LDRA tool suite](LDRA) \|
9.7.1
\| **48 S, 59 S** \| Fully implemented \| \| [Parasoft C/C++test](Parasoft) \|
2024.2
\|
**CERT_C-MSC01-aCERT_C-MSC01-b**
\| All 'if...else-if' constructs shall be terminated with an 'else' clause
The final clause of a switch statement shall be the default clause
\| \| [PC-lint Plus](PC-lint%20Plus) \|
1.4
\|
**474, 744, 787, 9013**
\|
Partially supported
\| \| [Polyspace Bug Finder](Polyspace%20Bug%20Finder) \|
R2024a
\|
[CERT C: Rec. MSC01-C](https://www.mathworks.com/help/bugfinder/ref/certcrec.msc01c.html)
\|
Checks for missing case for switch condition (rule partially covered)
\| \| [PVS-Studio](https://wiki.sei.cmu.edu/confluence/display/c/PVS-Studio) \|
7.35
\|
**[V517](https://pvs-studio.com/en/docs/warnings/v517/),** **[V533](https://pvs-studio.com/en/docs/warnings/v533/),** **[V534](https://pvs-studio.com/en/docs/warnings/v534/),** **[V535](https://pvs-studio.com/en/docs/warnings/v535/),;[V556](https://pvs-studio.com/en/docs/warnings/v556/),** **[V577](https://pvs-studio.com/en/docs/warnings/v577/),** **[V590](https://pvs-studio.com/en/docs/warnings/v590/),** **[V612](https://pvs-studio.com/en/docs/warnings/v612/),** **[V695](https://pvs-studio.com/en/docs/warnings/v695/),** **[V696](https://pvs-studio.com/en/docs/warnings/v696/),** **[V719](https://pvs-studio.com/en/docs/warnings/v719/),** **[V722](https://pvs-studio.com/en/docs/warnings/v722/),** **[V747](https://pvs-studio.com/en/docs/warnings/v747/),** **[V785](https://pvs-studio.com/en/docs/warnings/v785/),** **[V786](https://pvs-studio.com/en/docs/warnings/v786/)**
\|
\| \| [RuleChecker](RuleChecker) \|
24.04
\|
**missing-else**
**switch-default**
\| Partially checked \| \| [SonarQube C/C++ Plugin](SonarQube%20C_C++%20Plugin) \|
3.11
\|
**ElseIfWithoutElse,** **SwitchWithoutDefault**
\| \|
### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC01-CPP. Strive for logical completeness |
| CERT Oracle Secure Coding Standard for Java | MSC57-J. Strive for logical completeness |
| ISO/IEC TS 17961 | Use of an implied default in a switch statement [swtchdflt] |
| ISO/IEC TR 24772 | Switch Statements and Static Analysis [CLL] |

## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.7.2, "Errors of Omission and Addition" |
| [Viega 2005] | Section 5.2.17, "Failure to Account for Default Case in Switch" |
| [Zadegan 2009] | "A Lesson on Infinite Loops" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152104) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152275)
## Comments:

|  |
| ----|
| "may result in logic errors if widget_type unexpectedly assumes a different value" should have appended "or if its valid range is expanded during code maintenance and the programmer overlooks the need to add a case to the switch".
Is adding a default case really an instance of "remove dead code"?; It seems like more of an exception, where unreachable code is added as a precautionary measure.
I think a useful common practice should be shown by using
  default:  /* "can't happen" */
which shows that it handles an internal logic error.
                                        Posted by dagwyn at Apr 18, 2008 13:35
                                     |
| OK, all done.  The "remove dead code" was indicating this was an exception, but I tried to make this clearer.
                                        Posted by rcs_mgr at Apr 19, 2008 19:46
                                     |
| The "x == 0" expression in the Automated Detection example could be flagged by some code checkers as "expression is always true."
                                        Posted by christey at Jul 26, 2008 16:52
                                     |
| I agree, perhaps we should change the code to simply have an else at the end.
However, I question how well we can recognize "fake switches", who's to say that code that checks for thresholds is wrong?
if (x > t1) {
} else if (x > t2) {
}
// don't care for the other case because the value is too low

![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 28, 2008 10:12
\| \|
The idea is to ensure that switch statements and chains of if statements cover all possible cases. An else clause (without a subsequent if statement) does this, much like a switch statement's default clause. The code sample in question is intended to illustrate a case of logical completeness but without a terminating else clause.
I suppose it's a matter of style if you want to end that code with the tautological 'if (x == 0)...' or just the 'else'. Personally, I prefer else clauses that have a comment saying under what conditions the else clause handles (unless it is clearly an 'error' clause).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 28, 2008 12:33
\| \|
Well, what about if statements that just check for a single condition? Almost all of our code on the wiki is of the form
``` java
if (/* error check */) {
  /* Handle Error */
}
```
Are you saying that's wrong because there is no `else`?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 28, 2008 15:26
\| \|
Actually it technically is, because presumably the "Handle Error" clause would be unable to recover gracefully and should prevent the subsequent code from being executed. But those are illustrations and its pretty obvious that they are simple if statements and not long if-elseif-elseif-... chains.
Offhand, I'd suggest that the only violations that we should report (based on nested if statements) would be the NCCE above, which tests an int for being \> 0 and \< 0, neglecting the == 0 case.
I suspect any other chain of if statements that lacks a final else clause will be too complex for static analysis.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 28, 2008 15:40
\| \|
Why do you say an if branch could not gracefully recover? Almost all of our rose code is structured like
``` java
if (/* blah */) {
  return false;
}
```
Also, if the error handling branches terminate the function, the `else` is extraneous and only serves to add an extra layer of needless indentation.
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 28, 2008 16:17
\| \|
This rule may talk about 'goto' too ?
-   No backward GOTO
-   Limit forward GOTO
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jan 23, 2018 09:20
\| \|
This may be surprising, but we don't get many vulnerability reports that stem from bad uses of GOTO :) I'd guess that is because everyone knows the dangers of GOTO. So writing about it is not a high priority.
We do have;[MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources](MEM12-C_%20Consider%20using%20a%20goto%20chain%20when%20leaving%20a%20function%20on%20error%20when%20using%20and%20releasing%20resources).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 23, 2018 11:16
\| \|
I agree with you about this knowledge.
However, everyone knows this danger until the day we forgot it ![](images/icons/emoticons/wink.svg)
This is why we need a rule, at least a recommendation,; about GOTO, i think so.
The use of GOTO may certainly introduce vulnerabilities in some case.
![](images/icons/contenttypes/comment_16.png) Posted by jerome.guy at Jan 24, 2018 01:39
\| \|
What about simple if clauses without any "else if"? MISRA 15.7 clearly states that only after else if an (most of the time empty) else clause is needed. Here the example shows such a more complex case, but no exception is given. Static checks on this guideline show both interpretations: Parasoft and Polyspace use the MISRA interpretation, QAC also warns on simple if clauses.
![](images/icons/contenttypes/comment_16.png) Posted by olstyle at Jan 25, 2021 10:21
\| \|
Good question.Personally, I would not impose this recommendation on any if condition that lacked an else-if clause. However, other standards (eg MISRA) disagree, as you note.
Remember this guideline is a recommendation not a rule. So we believe that whatever hard condition we impose could be countered with code that violates the condition but would be regarded as reasonable by experienced programmers.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 25, 2021 11:44
\|
