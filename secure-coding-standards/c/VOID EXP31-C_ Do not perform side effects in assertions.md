The `assert()` macro is a convenient mechanism for incorporating diagnostic tests in code. (See [MSC11-C. Incorporate diagnostic tests using assertions](MSC11-C_%20Incorporate%20diagnostic%20tests%20using%20assertions).) Expressions used with the standard `assert` macro should not have [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect). Typically, the behavior of the `assert` macro depends on the status of the `NDEBUG` preprocessor symbol. If `NDEBUG` is undefined, the `assert` macro is defined to evaluate its expression argument and abort if the result of the expression is convertible to `false`. If `NDEBUG` is defined, `assert` is defined to be a no-op. Consequently, any side effects resulting from evaluation of the expression in the assertion are lost in non-debugging versions of the code.
Because `assert` is a macro, this rule is a special case of [PRE31-C. Avoid side effects in arguments to unsafe macros](PRE31-C_%20Avoid%20side%20effects%20in%20arguments%20to%20unsafe%20macros).
## Noncompliant Code Example
This noncompliant code example includes an `assert` macro containing an expression (`index++`) that has a side effect:
``` c
#include <assert.h>
void process(size_t index) {
  assert(index++ > 0); /* Side effect */
  /* ... */
}
```
## Compliant Solution
This compliant solution avoids the possibility of side effects in assertions by moving the expression containing the side effect outside of the `assert` macro.
``` c
#include <assert.h>
void process(size_t index) {
  assert(index > 0); /* No side effect */
  ++index;
  /* ... */
}
```
## Risk Assessment
Side effects in assertions can lead to [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) and erroneous behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP31-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Coverity | 2017.07 | ASSERT_SIDE_EFFECTS | Can detect the specific instance where assertion contains an operation/function call that may have a side effect |
| ECLAIR | 1.2 | CC2.EXP31 | Fully implemented |
| LDRA tool suite | 9.7.1 | 9 S30 S | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 3440 | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP31-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP31-CPP. Avoid side effects in assertions |
| CERT Oracle Secure Coding Standard for Java | EXP06-J. Expressions used in assertions must not produce side effects |

## Bibliography

|  |  |
| ----|----|
| [Dewhurst 2002] | Gotcha 28: "Side Effects in Assertions" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/EXP30-C.+Do+not+depend+on+order+of+evaluation+for+side+effects) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=358) [](https://www.securecoding.cert.org/confluence/display/seccode/EXP32-C.+Do+not+access+a+volatile+object+through+a+nonvolatile+reference)
## Comments:

|  |
| ----|
| Side effects in assertions lead to Heisenbugs - this is a huge problem where it works for the devs but not for QA.
                                        Posted by steve at Mar 13, 2008 23:08
                                     |
| Does this guideline apply to assertion functions, such as:
extern void my_assert(int);
void f(int i)
{
my_assert(i++);
}

![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 13, 2009 15:56
\| \|
As written, this rule only applies to the standard assert macro.
Because assert is a macro, this rule is a special case of PRE31-C. Never invoke an unsafe macro with arguments containing assignment, increment, decrement, volatile access, or function call.
Because `my_assert()` in your example is a function, there is no problem with this code. There is always a sequence point before a function invocation meaning that the side effects must be completed before the call.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 14, 2009 09:13
\|
