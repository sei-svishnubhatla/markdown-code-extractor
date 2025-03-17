Assertions are a valuable diagnostic tool for finding and eliminating software defects that may result in [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) (see [MSC11-C. Incorporate diagnostic tests using assertions](MSC11-C_%20Incorporate%20diagnostic%20tests%20using%20assertions)). The runtime `assert()` macro has some limitations, however, in that it incurs a runtime overhead and because it calls `abort()`. Consequently, the runtime `assert()` macro is useful only for identifying incorrect assumptions and not for runtime error checking. As a result, runtime assertions are generally unsuitable for server programs or embedded systems.
Static assertion is a new facility in the C Standard. It takes the form
``` java
static_assert(constant-expression, string-literal);
```
Subclause 6.7.10 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] states:
> The constant expression shall be an integer constant expression. If the value of the constant expression compares unequal to 0, the declaration has no effect. Otherwise, the constraint is violated and the implementation shall produce a diagnostic message that includes the text of the string literal, except that characters not in the basic source character set are not required to appear in the message.

It means that if `constant-expression` is true, nothing will happen. However, if `constant-expression` is false, an error message containing `string-literal` will be output at compile time.
``` java
/* Passes */
static_assert(
  sizeof(int) <= sizeof(void*), 
  "sizeof(int) <= sizeof(void*)"
); 
/* Fails */
static_assert(
  sizeof(double) <= sizeof(int), 
  "sizeof(double) <= sizeof(int)"
);
```
Static assertion is not available in C99.
## Noncompliant Code Example
This noncompliant code uses the `assert()` macro to assert a property concerning a memory-mapped structure that is essential for the code to behave correctly:
``` c
#include <assert.h>
struct timer {
  unsigned char MODE;
  unsigned int DATA;
  unsigned int COUNT;
};
int func(void) {
  assert(sizeof(struct timer) == sizeof(unsigned char) + sizeof(unsigned int) + sizeof(unsigned int));
}
```
Although the use of the runtime assertion is better than nothing, it needs to be placed in a function and executed. This means that it is usually far away from the definition of the actual structure to which it refers. The diagnostic occurs only at runtime and only if the code path containing the assertion is executed.
## Compliant Solution
For assertions involving only constant expressions, a preprocessor conditional statement may be used, as in this compliant solution:
``` c
struct timer {
  unsigned char MODE;
  unsigned int DATA;
  unsigned int COUNT;
};
#if (sizeof(struct timer) != (sizeof(unsigned char) + sizeof(unsigned int) + sizeof(unsigned int)))
  #error "Structure must not have any padding"
#endif
```
Using `#error` directives allows for clear diagnostic messages. Because this approach evaluates assertions at compile time, there is no runtime penalty.
## Compliant Solution
This portable compliant solution uses `static_assert`:
``` c
#include <assert.h>
struct timer {
  unsigned char MODE;
  unsigned int DATA;
  unsigned int COUNT;
};
static_assert(sizeof(struct timer) == sizeof(unsigned char) + sizeof(unsigned int) + sizeof(unsigned int),
              "Structure must not have any padding");
```
Static assertions allow incorrect assumptions to be diagnosed at compile time instead of resulting in a silent malfunction or runtime error. Because the assertion is performed at compile time, no runtime cost in space or time is incurred. An assertion can be used at file or block scope, and failure results in a meaningful and informative diagnostic error message.
Other uses of static assertion are shown in [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation) and [FIO34-C. Distinguish between characters read from a file and EOF or WEOF](FIO34-C_%20Distinguish%20between%20characters%20read%20from%20a%20file%20and%20EOF%20or%20WEOF).
## Risk Assessment
Static assertion is a valuable diagnostic tool for finding and eliminating software defects that may result in [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) at compile time. The absence of static assertions, however, does not mean that code is incorrect.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL03-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL03 |  |
| Clang | 3.9 | misc-static-assert | Checked by clang-tidy |
| CodeSonar | 8.3p0 | (customization) | Users can implement a custom check that reports uses of the assert() macro |
| Compass/ROSE |  |  | Could detect violations of this rule merely by looking for calls to assert(), and if it can evaluate the assertion (due to all values being known at compile time), then the code should use static-assert instead; this assumes ROSE can recognize macro invocation |
| ECLAIR | 1.2 | CC2.DCL03 | Fully implemented |
| LDRA tool suite | 9.7.1 | 44 S | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL03-C).
## Related Guidelines

|  |  |
| ----|----|
| C++ Secure Coding Standard | VOID DCL03-CPP. Use a static assertion to test the value of a constant expression |

##  Bibliography

|  |  |
| ----|----|
| [Becker 2008] |  |
| [Eckel 2007] |  |
| [ISO/IEC 9899:2011] | Subclause 6.7.10, "Static Assertions" |
| [Jones 2010] |  |
| [Klarer 2004] |  |
| [Saks 2005] |  |
| [Saks 2008] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152407) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152402)
## Comments:

|  |
| ----|
| _LINE_ should be __LINE__.  (Arg, the wiki ate my double '_' too, that's why.  Needed to use wiki markup.  You'll probably read to proofreed this other places too.) (...and switching between rich text and wiki markup ate my limits.h, and then my recently quoted double _.)
Compilers do not always catch constraint violations, due to either sloppy error checking or extensions.  Thus my variant violates two constraints, hopefully the compiler will catch at least one:
#define static_assert(e) typedef \
    struct { int STATIC_ASSERT_NAME_(__LINE__): ((e) ? 1 : -1); } \
    STATIC_ASSERT_NAME_(__LINE__)[(e) ? 1 : -1]
#define STATIC_ASSERT_NAME_(line)   STATIC_ASSERT_NAME2_(line)
#define STATIC_ASSERT_NAME2_(line)  assertion_failed_at_##line

Static assertions are also useful to protect code which makes non-standard assumptions. E.g. code which manipulates the representation of longs and does not bother to implement the case where long or unsigned long can have trap representations:
``` java
#include <limits.h>
/* LONG_MIN == -LONG_MAX-1, and unsigned/signed long have the same width */
static_assert(ULONG_MAX/2 == (unsigned long) (-1 - LONG_MIN));
/* No unsigned long padding bits (well, if sizeof(long) <= UCHAR_MAX anyway) */
static_assert(ULONG_MAX % UCHAR_MAX == 0 &&
          ULONG_MAX / UCHAR_MAX % UCHAR_MAX == sizeof(long));
```
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 07, 2008 04:06
\| \|
The definition of static_assert here only has the one argument, while the uses elsewhere assume two arguments. We need to make a decision and make get this consistent.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at May 10, 2008 21:07
\| \|
"typically removed from the actual structure to which it refers." didn't make sense to me. Could you paraphrase the sentence?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Apr 13, 2009 22:14
\| \|
the intent of using the word 'dimension' seems a bit confusing in this context since it is normally used for such as "1-dimensional array" and "multidimensional array."
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Apr 13, 2009 22:31
\| \|
I've modified the text to address these comments.
We had a discussion about a year ago about the use of 'dimension' to refer to the initial size of the array...don't remember details. An array's 'dimension' should only refer to how many indices it has...a[3](/confluence/pages/createpage.action?spaceKey=c&title=3)[4](/confluence/pages/createpage.action?spaceKey=c&title=4) is a 2-dimensional array. The code here only works with one-dimensional arrays, and the only thing varying is the array's initial size: 1 vs. -1.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 14, 2009 10:09
\| \|
Thanks David. Makes much clearer sense now.
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Apr 16, 2009 19:49
\| \|
I think the call needs to be to `struct timer` (instead of just `timer`) in the passes to `offset_of(timer, DATA)` (the final compliant solution does, but the others do not, including the compliant macro. Thoughts?
![](images/icons/contenttypes/comment_16.png) Posted by agoyal at Jul 10, 2009 14:53
\| \|
You are probably right... just make sure it compiles without warning (at high warning levels).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jul 15, 2009 10:32
\| \|
If static_assert is going to be in the next C++, and possibly in the next C, naming one's macro the same virtually guarantees incompatibility with these upcoming standards. Better to name it something different, like STATIC_ASSERT.
![](images/icons/contenttypes/comment_16.png) Posted by sgreen at Aug 20, 2009 17:03
\| \|
I suggest the first **Compliant Solution** be either removed or changed to a **Noncompliant Code Example**. It's misleading to suggest that the `offsetof()` macro may be used in preprocessor conditionals, even there is an implementation that happens to allow it. (Incidentally, is there really, and if so, is it a documented feature of the implementation or just an accidental side-effect of some optimization?)
In addition, since the fixed width types used in the compliant solutions on this page are optional and need not be defined by a conforming C99 implementation I think it would be best to replace them with required types (or, better yet, fundamental types). Using the fixed width types doesn't contribute to the value of the examples in any way.
If there are no objections I'll go ahead and make these changes.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 19, 2010 20:25
\| \|
I also agree with you.First compliant solution can be replaced with something like one shown at <http://www.pixelbeat.org/programming/gcc/static_assert.html>.
;
![](images/icons/contenttypes/comment_16.png) Posted by mohandhan at Jan 01, 2013 04:20
\| \|
I've changed the code samples to rely on sizeof, rather than offsetof. That renders the 1st CS conformant with the standard, actually.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 03, 2013 13:06
\| \|
Hello,
;
The first « Compliant Solution » is incorrect. Conforming to §6.10.1 p4 (doc. N1570), all identifiers in the controlling constant expression of a conditional inclusion are replaced by the token 0. So, the first example became :
    struct timer {
            unsigned char MODE;
            unsigned int DATA;
            unsigned int COUNT;
    };
    #if (0(0 0) != (0(0 0) + 0(0 0) + 0(0 0)))
    #error "Structure must not have any padding"
    #endif
which is syntactically incorrect. The object of \_Static_assert is precisely to permit evaluation of integer constants expressions at compile time which is only partially possible with a conditional inclusion.
![](images/icons/contenttypes/comment_16.png) Posted by taurre at Nov 24, 2013 06:35
\|
