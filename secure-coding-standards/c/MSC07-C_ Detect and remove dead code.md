> [!warning]  
>
> This rule has been deprecated.  It has been merged with:
>
> -   [MSC12-C. Detect and remove code that has no effect or is never executed](https://www.securecoding.cert.org/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed)
>
> 10/07/2014 -- Version 2.0
>
>   

Code that is never executed is known as *dead code*. Typically, the presence of dead code indicates that a logic error has occurred as a result of changes to a program or the program's environment. Dead code is usually optimized out of a program during compilation. However, to improve readability and ensure that logic errors are resolved, dead code should be identified, understood, and eliminated.
This recommendation is related to [MSC12-C. Detect and remove code that has no effect or is never executed](MSC12-C_%20Detect%20and%20remove%20code%20that%20has%20no%20effect%20or%20is%20never%20executed).
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
    /* ... */
    if (s) {
        /* This code is never reached */
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
    /* ... */
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
        /* ... */
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
        /* ... */
      if (s[i+1] == '\0') {
        /* This code is now reached */
      }
    }
    return 0;
}
```
## Exceptions
**MSC07-C-EX1:** In some situations, seemingly dead code may make software resilient. An example is the `default` label in a `switch` statement whose controlling expression has an enumerated type and that specifies labels for all enumerations of the type. (See [MSC01-C. Strive for logical completeness](MSC01-C_%20Strive%20for%20logical%20completeness).) Because valid values of an enumerated type include all those of its underlying integer type, unless enumeration constants are provided for all those values, the `default` label is appropriate and necessary.
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
**MSC07-EX2:** It is also permissible to temporarily remove code that may be needed later. (See [MSC04-C. Use comments consistently and in a readable fashion](MSC04-C_%20Use%20comments%20consistently%20and%20in%20a%20readable%20fashion) for an illustration.)
## Risk Assessment
The presence of dead code may indicate logic errors that can lead to unintended program behavior. The ways in which dead code can be introduced into a program and the effort required to remove it can be complex. As a result, resolving dead code can be an in-depth process requiring significant analysis.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC07-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | dead-assignemntdead-initializer | Partially checked and soundly supported. |
| CodeSonar | 8.3p0 | DIAG.UNEX.*LANG.STRUCT.RC
LANG.STRUCT.UC | Code not exercised by analysisRedundant condition
Unreachable {Call, Computation, Conditional, Control Flow, Data Flow} |
| Coverity | 2017.07 | DEADCODE
UNREACHABLE
 | Can detect the specific instance where code can never be reached because of a logical contradiction or a dead "default" in switch statementCan detect the instances where code block is unreachable because of the syntactic structure of the code |
| GCC | 4.3.5 |  | Can detect violations of this recommendation when the -Wunreachable-code flag is used |
| Helix QAC | 2024.4 | C1501, C1503, C2008, C2877, C2880, C2881, C2882, C2883,C3202, C3203, C3205, C3206, C3207, C3210, C3219, C3229, C3404, C3422, C3423, C3425, C3470DF2877, DF2880, DF2881, DF2882, DF2883, DF2980, DF2981, DF2982, DF2983, DF2984, DF2985, DF2986 |  |
| Klocwork | 2024.4 | LA_UNUSEDUNREACH.GEN
UNREACH.RETURN
UNREACH.SIZEOFUNREACH.ENUM
INVARIANT_CONDITION.UNREACH |  |
| LDRA tool suite | 9.7.1 | 1 J139 S
140 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC07-aCERT_C-MSC07-b
CERT_C-MSC07-c
CERT_C-MSC07-d
CERT_C-MSC07-e
CERT_C-MSC07-f
CERT_C-MSC07-g
CERT_C-MSC07-h
CERT_C-MSC07-i
 | There shall be no unreachable code in "else" blockThere shall be no unreachable code after 'return', 'break', 'continue', 'goto', 'throw' statements, and after calls to functions with the 'noreturn' attribute
There shall be no unreachable code in "if/else/while/for" block
There shall be no unreachable code in switch statement
There shall be no unreachable code in 'for' loop
There shall be no unreachable code after 'if' or 'switch' statement
There shall be no unreachable code after "if" or "switch" statement inside while/for/do...while loop
Avoid switch with unreachable branches
Avoid unreachable methods |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC07-C | Checks for:Code does not executeDefault case is missing and may be reachedCode following control-flow statements |
| RuleChecker | 24.04 | dead-assignemntdead-initializer | Partially checked |
| SonarQube C/C++ Plugin | ;3.11 | S1763, S1751 |  |
| Splint | 3.1.1 |  | Can detect violations of this recommendation when the -Wunreachable-code flag is used |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC07-C).
[CVE-2014-1266](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2014-1266) results from a violation of this rule. There is a spurious `goto fail` statement on line 631 of [sslKeyExchange.c](http://opensource.apple.com/source/Security/Security-55471/libsecurity_ssl/lib/sslKeyExchange.c?txt). This `goto` statement gets executed unconditionally, even though it is indented as if it were part of the preceding `if` statement. As a result, the call to `sslRawVerify()` (which would perform the actual signature verification) becomes dead code.  \[[ImperialViolet 2014](https://www.imperialviolet.org/2014/02/22/applebug.html)\]
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC07-CPP. Detect and remove dead code |
| ISO/IEC TR 24772 | Unspecified functionality [BVQ]Dead and deactivated code [XYQ] |
| MISRA C:2012 | Rule 2.1 (required) |
| MITRE CWE | CWE-561, Dead code |

## Bibliography

|  |  |
| ----|----|
| [Fortify 2006] | Code Quality, "Dead Code" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152190) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/MSC09-C_%20Character%20encoding_%20Use%20subset%20of%20ASCII%20for%20safety)
## Comments:

|  |
| ----|
| I don't believe the second non-compliant example is dead code.  All the code is executed.  It's may be an error of omission.
Perhaps you meant to have a (stri+1 == NULL) conditional in there?
                                        Posted by hburch at Jun 01, 2007 11:14
                                     |
| While compliant solution 1 might be the correct solution, it is more likely (IMNSHO) that the correct course of action was to remove the second 'if (s)' and its associated block.; At the very least, this should be mentioned as a plausible alternative course of action.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 02:46
                                     |
| As currently written, there is dead code in the second non-compliant example:
[!note]
Â int string_loop(char *str) {
    size_t i;
    for (i=0; i < strlen(str); i++) {
        /* ... */
    if (str[i] == '\0')
        /* This code is never reached */
    }
    return 0;
}

Assuming that nothing adds zeroes into the middle of the string, then i is constrained to range over values for which str\[i\] is non-zero by virtue of the definition of what strlen() does.
However, there is also an as yet unremarked upon performance bug in the code - calling strlen() on each iteration of the loop is wasteful unless you are busy adding or removing zeroes ('\0') from the data in str.  At one time (about 2 decades ago), Sun had a bug in their implementation of strstr() which evaluated strlen() on each iteration in strstr().  That didn't matter much of the time - but was disastrous when working with 20 KB long strings and chasing substrings that appeared every few hundred characters.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 20, 2008 02:57
\| \|
I think it's okay as is.; Of course we don't know what the actual intent was, but presumably the programmer thought the code would be of some use or he wouldn't have bothered to write it.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 14:04
\| \|
In MISRA C:2012 parlance, this appears to be called "unreachable code".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 14, 2014 11:19
\| \|
I'm thinking we should deprecate this guideline and combine with [MSC12-C. Detect and remove code that has no effect](https://www.securecoding.cert.org/confluence/display/seccode/MSC12-C.+Detect+and+remove+code+that+has+no+effect).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Oct 07, 2014 10:54
\| \|
The -Wunreachable-code has been removed, because it was unstable: it relied on the optimizer, and so different versions of gcc would warn about different code.; The compiler still accepts and ignores the command line option so that existing Makefiles are not broken.  In some future release the option will be removed entirely.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Oct 07, 2014 14:32
\|
