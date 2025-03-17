Macros are frequently used to make source code more readable. Macro definitions, regardless of whether they expand to a single or multiple statements, should not conclude with a semicolon. (See [PRE10-C. Wrap multistatement macros in a do-while loop](PRE10-C_%20Wrap%20multistatement%20macros%20in%20a%20do-while%20loop).) If required, the semicolon should be included following the macro expansion. Inadvertently inserting a semicolon at the end of the macro definition can unexpectedly change the control flow of the program.
Another way to avoid this problem is to prefer inline or static functions over function-like macros. (See also [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros).)
In general, the programmer should ensure that there is no semicolon at the end of a macro definition. The responsibility for having a semicolon where needed during the use of such a macro should be delegated to the person invoking the macro.
## Noncompliant Code Example
This noncompliant code example creates a macro definition for a `for` loop in the program. A `for` loop should require braces, even if it contains only a single body statement. (See [EXP19-C. Use braces for the body of an if, for, or while statement](EXP19-C_%20Use%20braces%20for%20the%20body%20of%20an%20if,%20for,%20or%20while%20statement).) This macro takes an integer argument, which is the number of times the loop should run. The programmer has inserted a semicolon at the end of the macro definition by mistake.
``` c
#define FOR_LOOP(n)  for(i=0; i<(n); i++);
int i;
FOR_LOOP(3)
{
  puts("Inside for loop\n");
}
```
The programmer expects to get the following output from the code:
``` java
Inside for loop
Inside for loop
Inside for loop
```
But because of the semicolon at the end of the macro definition, the `for` loop in the program has a null statement, so the statement "Inside for loop" gets printed just once. Essentially, the semicolon at the end of the macro definition changes the program control flow.
Although this example might not actually be used in code, it shows the effect a semicolon in a macro definition can have.
## Compliant Solution
The compliant solution is to write the macro definition without the semicolon at the end, leaving the decision whether or not to have a semicolon up to the person who is using the macro:
``` c
#define FOR_LOOP(n)  for(i=0; i<(n); i++)
int i;
FOR_LOOP(3)
{
  puts("Inside for loop\n");
}
```
## Noncompliant Code Example
In this noncompliant code example, the programmer defines a macro that increments the value of the first argument, `x`, by 1 and modulates it with the value of the second argument, `max`:
``` c
#define INCREMOD(x, max) ((x) = ((x) + 1) % (max));
int index = 0;
int value;
value = INCREMOD(index, 10) + 2;
/* ... */
```
In this case, the programmer intends to increment `index` and then use that as a value by adding 2 to it. Unfortunately, the value is equal to the incremented value of `index` because of the semicolon present at the end of the macro. The `+ 2;` is treated as a separate statement by the compiler. The user will not get any compilation errors. If the user has not enabled warnings while compiling, the effect of the semicolon in the macro cannot be detected at an early stage.
## Compliant Solution
The compliant solution is to write the macro definition without the semicolon at the end, leaving the decision whether or not to have a semicolon up to the person who is using the macro:
``` c
#define INCREMOD(x, max) ((x) = ((x) + 1) % (max))
```
## Compliant Solution
This compliant solution uses an inline function as recommended by [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros).
``` c
inline int incremod(int *x, int max) {*x = (*x + 1) % max;}
```
## Risk Assessment
Using a semicolon at the end of a macro definition can result in the change of program control flow and thus unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE11-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | macro-final-semicolon | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE11 |  |
| CodeSonar | 8.3p0 | LANG.PREPROC.MACROEND | Macro Does Not End With ) or } |
| Cppcheck Premium | 24.11.0 | premium-cert-pre11-c |  |
| Helix QAC | 2024.4 | C3412 |  |
| LDRA tool suite | 9.7.1 | 79 S | Enhanced Enforcement |
| PC-lint Plus | 1.4 | 823 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE11-C | Checks for macros terminated with semicolons (rule fully covered) |
| RuleChecker | 24.04 | macro-final-semicolon  | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE11-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE11-CPP. Do not conclude macro definitions with a semicolon |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152293) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152230)
## Comments:

|  |
| ----|
| Ruchi, just two comments:
    This rule is specifically about macros that contain single statements (not expressions or multi-statement blocks). It should say so, both in the title and discussion.
    The rule should acknowledge other rules (eg PRE00-C & PRE10-C) that discuss similar issues.
                                        Posted by svoboda at Nov 03, 2008 12:31
                                     |
| I think "Mitigation Strategies" section is redundant and can be removed.
                                        Posted by masaki at Apr 09, 2009 01:27
                                     |
| The info is useful, but it technically is not a 'mitigation' (eg a workaround for insecure code), it is rather a design constraint (how to write code correctly). So I moved the paragraph to the intro and wordsmithed it a bit.
                                        Posted by svoboda at Apr 09, 2009 10:26
                                     |
| This recommendation applies to multi-statement macros for the same reason it does to single-statement ones. Is there any reason not to extend it to include all macros? If not, what is the process for changing the title of a recommendation or rule?
                                        Posted by martinsebor at Dec 07, 2009 14:23
                                     |
| Thanks for changing the title, Martin.
                                        Posted by svoboda at Dec 08, 2009 08:55
                                     |
| The first NCCE/CS pair seems superfluous to me; the code is simply incorrect, regardless of the presence of the macro.; It's also covered by EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement  Any complaints if I remove the pair?
                                        Posted by aballman at Sep 17, 2013 09:45
                                     |
| #define FOR_LOOP(n); for(i=0; i<(n); i++) int i;FOR_LOOP(3){  puts("Inside for loop\n");}IMHO this is a bad coding practice example. And giving this example, though it achieves right result, is defeating the purpose of secure coding practice. Loop in macros should be allowed when they do definite task e.g.#define CALL_func_n_TIMES(n, func) while(--n){ func(); }or#define PRINT_this_n_TIMES(n, this) while(--n){ printf("%s\n", this); }Though, PRINT_this_n_TIMES is itself bad, since it's going to print only strings, macros should be generic. Also, in for example, I think you will need to supply 'i' too like FOR_LOOP(n, i), and call macro appropriately. Because, macro can be in entirely different header file, and in that case if you don't mention 'i' explicitly, you will be creating side-effects that you might not understand until your program crashes or does something wrong.Take case:a lot of declarations in some functionint i = 0; // I am going to use this i for counting something. very important.
             // but I am not going to mention this in comments, because I know 
             // what I am doing.... // a lot of things you do and count.now, unfortunately you callFOR_LOOP(3) ...// and BOOM, you just changed the number of things I counted. now, i == 3.... // keep on going doing things and counting and incrementing i.return i // perhaps. Make decision based on returned value.// KA-BOOM wrong output, though you did all the right things. So if you use i in FOR_LOOP(n, i) it makes more sense, as things will be explicit. 
                                        Posted by iamanubhavsaini at May 14, 2014 12:20
                                     |
| #define INCREMENT(x, max) ((x) = ((x) + 1) % (max))Shouldn't it be an inline function? Plus, this is not actual "increment".
                                        Posted by iamanubhavsaini at May 14, 2014 12:23
                                     |
| Yes, as the description of this guideline suggests:Another way to avoid this problem is to prefer inline or static functions over function-like macros.
                                        Posted by martinsebor at May 14, 2014 14:16
                                     |
| The FOR_LOOP example isn't a very good one. It exists only to demonstrate the point about the terminating semicolon. Most (but not all) uses of macros can be replaced by better alternatives, and the FOR_LOOP macro is a case in point -- the for statement is perfectly adequate and would be far more appropriate.That said, making the loop control variable an argument to the macro would solve the problem you point out. An even better solution would be to declare the variable directly in the for statement, like so:
#define FOR_LOOP(i, n)  for (int i=0; i<(n); i++)The advantage of this approach is that it limits the scope of the variable to the for statement alone.
                                        Posted by martinsebor at May 14, 2014 14:33
                                     |
| I've addressed these issues. It is ;possible to violate the recommendations (like PRE00-C) and still have secure code, so I did not change that compliant solution. But I did add one that uses an inline function, as Martin suggests.
                                        Posted by svoboda at May 15, 2014 17:06
                                     |

