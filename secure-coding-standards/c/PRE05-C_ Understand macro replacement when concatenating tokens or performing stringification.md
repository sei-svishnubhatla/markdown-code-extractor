It is necessary to understand how macro replacement works in C, particularly in the context of concatenating tokens using the `##` operator and converting macro parameters to strings using the `#` operator.
# Concatenating Tokens
The `##` preprocessing operator is used to merge two tokens into one while expanding macros, which is called *token pasting* or *token concatenation*. When a macro is expanded, the two tokens on either side of each `##` operator are combined into a single token that replaces the `##` and the two original tokens in the macro expansion \[[FSF 2005](AA.-Bibliography_87152170.html#AA.Bibliography-FSF05)\].
Token pasting is most useful when one or both of the tokens come from a macro argument. If either of the tokens next to a `##` is a parameter name, it is replaced by its actual argument before `##` executes. The actual argument is not macro expanded first.
# Stringification
Parameters are not replaced inside string constants, but the `#` preprocessing operator can be used instead. When a macro parameter is used with a leading `#`, the preprocessor replaces it with the literal text of the actual argument converted to a string constant \[[FSF 2005](AA.-Bibliography_87152170.html#AA.Bibliography-FSF05)\].
## Noncompliant Code Example
The following definition for `static_assert()` from [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression) uses the `JOIN()` macro to concatenate the token `assertion_failed_at_line_` with the value of `__LINE__`:
``` java
#define static_assert(e) \
  typedef char JOIN(assertion_failed_at_line_, __LINE__) \
    [(e) ? 1 : -1]
```
`__LINE__` is a predefined macro name that expands to an integer constant representing the presumed line number of the current source line within the current source file. If the intention is to expand the `__LINE__` macro, which is likely the case here, the following definition for `JOIN()` is noncompliant because the `__LINE__` is not expanded, and the character array is subsequently named `assertion_failed_at_line___LINE__`:
``` c
#define JOIN(x, y) x ## y
```
##  Compliant Solution
To get the macro to expand, a second level of indirection is required, as shown by this compliant solution:
``` c
#define JOIN(x, y) JOIN_AGAIN(x, y)
#define JOIN_AGAIN(x, y) x ## y
```
`JOIN(x, y)` calls `JOIN_AGAIN(x, y)` so that if `x` or `y` is a macro, it is expanded before the `##` operator pastes them together.
Note also that macro parameters cannot be individually parenthesized when concatenating tokens using the `##` operator, converting macro parameters to strings using the `#` operator, or concatenating adjacent string literals. This is an exception, **PRE01-C-EX2**, to [PRE01-C. Use parentheses within macros around parameter names](PRE01-C_%20Use%20parentheses%20within%20macros%20around%20parameter%20names).
## Noncompliant Code Example
This example is noncompliant if the programmer's intent is to expand the macro before stringification:
``` c
#define str(s) #s
#define foo 4
str(foo)
```
The macro invocation `str(foo)` expands to `foo`.
## Compliant Solution
To stringify the result of expansion of a macro argument, two levels of macros must be used:
``` c
#define xstr(s) str(s)
#define str(s) #s
#define foo 4
```
The macro invocation `xstr(foo)` expands to `4` because `s` is stringified when it is used in `str()`, so it is not macro expanded first. However, `s` is an ordinary argument to `xstr()`, so it is completely macro expanded before `xstr()` is expanded. Consequently, by the time `str()` gets to its argument, it has already been macro expanded.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE05-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE05 |  |
| CodeSonar | 8.3p0 | LANG.PREPROC.HASHLANG.PREPROC.MARGME
LANG.PREPROC.PASTE | Macro uses # operatorMacro argument is both mixed and expanded
Macro uses ## operator |
| Helix QAC | 2024.4 | C0341, C0342, C0801, C0802, C0803, C0811, C0872, C0880, C0881, C0884 |  |
| Klocwork | 2024.4 | MISRA.DEFINE.SHARP.ORDER.2012 |  |
| LDRA tool suite | 9.7.1 | 76 S, 125 S, 637 S | Enhanced Enforcement |
| PC-lint Plus | 1.4 | 9024 | Assistance provided: reports any use of pasting or stringizing operators in a macro definition |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE05-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE05-CPP. Understand macro replacement when concatenating tokens or performing stringification |

## Bibliography

|  |  |
| ----|----|
| [FSF 2005] | Section 3.4, "Stringification" Section 3.5, "Concatenation" |
| [Saks 2008] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152186) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152155)
## Comments:

|  |
| ----|
| Compliant SolutionTo stringify the result of expansion of a macro argument, you must use two levels of macros:#define xstr(s) str(s)#define str(s) #s#define foo 4Isn't it wrong to use #define foo 4; I think it should be #define foo (4) to comply with standard Use parentheses within macros around parameter names
                                        Posted by punitkandoi at Apr 05, 2013 07:20
                                     |
| Unfortunately, that would wind up printing (4) instead of 4 when using the xstr macro to expand foo.
                                        Posted by aballman at Jun 25, 2013 09:16
                                     |
| Writing:;   #define FOO 22is fine because the pre-processor simply replaces a token with another one and the semantics is the same.  What is bad is if you do:   #define FOO -22In that case you need to use parentheses to avoid problems, as in:  #define FOO (-22)I think Use parentheses within macros around parameter names should be updated to describe this.
                                        Posted by prouleau001 at Dec 05, 2017 22:27
                                     |
| Wouldn't it make sense to use an array size of zero instead of one if the assertion does not fail?
#define static_assert(e) \
  typedef char JOIN(assertion_failed_at_line_, __LINE__) \
    [(e) ? 0 : -1]

Sure, just an example but adding a lot of that static_assert will (if unused variables are not optimized out) consume some stacks size using 1 and shouldn't using 0.
Or is this assumption wrong?
![](images/icons/contenttypes/comment_16.png) Posted by maggu2810 at Jul 28, 2021 04:14
\| \|
Zero-sized arrays are not allowed by ISO C, so that wouldn't work portably. Thankfully, there's not a storage issue here to be solved; typedefs do not define a new variable, only a type alias, so there is no runtime overhead from their use. See the output (even at -O0) here as an example:;<https://godbolt.org/z/Yv3K961xz> and note how there's space reserved for `c`  but not `foo`  or `bar` .
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 28, 2021 07:49
\|
