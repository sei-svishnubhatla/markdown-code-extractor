Macros are dangerous because their use resembles that of real functions, but they have different semantics. The inline function-specifier was introduced to the C programming language in the C99 standard. Inline functions should be preferred over macros when they can be used interchangeably. Making a function an inline function suggests that calls to the function be as fast as possible by using, for example, an alternative to the usual function call mechanism, such as *inline substitution*. (See also [PRE31-C. Avoid side effects in arguments to unsafe macros](PRE31-C_%20Avoid%20side%20effects%20in%20arguments%20to%20unsafe%20macros), [PRE01-C. Use parentheses within macros around parameter names](PRE01-C_%20Use%20parentheses%20within%20macros%20around%20parameter%20names), and [PRE02-C. Macro replacement lists should be parenthesized](PRE02-C_%20Macro%20replacement%20lists%20should%20be%20parenthesized).)
Inline substitution is not textual substitution, nor does it create a new function. For example, the expansion of a macro used within the body of the function uses the definition it had at the point the function body appeared, not where the function is called; and identifiers refer to the declarations in scope where the body occurs.
Arguably, a decision to inline a function is a low-level optimization detail that the compiler should make without programmer input. The use of inline functions should be evaluated on the basis of (a) how well they are supported by targeted compilers, (b) what (if any) impact they have on the performance characteristics of your system, and (c) portability concerns. Static functions are often as good as inline functions and are supported in C.
## Noncompliant Code Example
In this noncompliant code example, the macro `CUBE()` has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when passed an expression that contains side effects:
``` c
#define CUBE(X) ((X) * (X) * (X))
void func(void) {
  int i = 2;
  int a = 81 / CUBE(++i);
  /* ... */
}
```
For this example, the initialization for `a` expands to
``` java
int a = 81 / ((++i) * (++i) * (++i));
```
which is undefined (see [EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects)).
## Compliant Solution
When the macro definition is replaced by an inline function, the [side effect](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) is executed only once before the function is called:
``` c
inline int cube(int i) {
  return i * i * i;
}
void func(void) {
  int i = 2;
  int a = 81 / cube(++i);
  /* ... */ 
}
```
## Noncompliant Code Example
In this noncompliant code example, the programmer has written a macro called `EXEC_BUMP()` to call a specified function and increment a global counter \[[Dewhurst 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Dewhurst02)\]. When the expansion of a macro is used within the body of a function, as in this example, identifiers refer to the declarations in scope where the body occurs. As a result, when the macro is called in the `aFunc()` function, it inadvertently increments a local counter with the same name as the global variable. Note that this example also violates [DCL01-C. Do not reuse variable names in subscopes](DCL01-C_%20Do%20not%20reuse%20variable%20names%20in%20subscopes).
``` c
size_t count = 0;
#define EXEC_BUMP(func) (func(), ++count)
void g(void) {
  printf("Called g, count = %zu.\n", count);
}
void aFunc(void) {
  size_t count = 0;
  while (count++ < 10) {
    EXEC_BUMP(g);
  }
}
```
The result is that invoking `aFunc()` (incorrectly) prints out the following line five times:
``` java
Called g, count = 0.
```
## Compliant Solution
In this compliant solution, the `EXEC_BUMP()` macro is replaced by the inline function `exec_bump()`. Invoking `aFunc()` now (correctly) prints the value of `count` ranging from 0 to 9:
``` c
size_t count = 0;
void g(void) {
  printf("Called g, count = %zu.\n", count);
}
typedef void (*exec_func)(void);
inline void exec_bump(exec_func f) {
  f();
  ++count;
}
void aFunc(void) {
  size_t count = 0;
  while (count++ < 10) {
    exec_bump(g);
  }
}
```
The use of the inline function binds the identifier `count` to the global variable when the function body is compiled. The name cannot be re-bound to a different variable (with the same name) when the function is called.
## Noncompliant Code Example
Unlike functions, the execution of macros can interleave. Consequently, two macros that are harmless in isolation can cause [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when combined in the same expression. In this example, `F()` and `G()` both increment the global variable `operations`, which causes problems when the two macros are used together:
``` c
int operations = 0, calls_to_F = 0, calls_to_G = 0;
#define F(x) (++operations, ++calls_to_F, 2 * x)
#define G(x) (++operations, ++calls_to_G, x + 1)
void func(int x) {
  int y = F(x) + G(x);
}
```
The variable `operations` is both read and modified twice in the same expression, so it can receive the wrong value if, for example, the following ordering occurs:
> [!note]  
>
>     read operations into register 0
>     read operations into register 1
>     increment register 0
>     increment register 1
>     store register 0 into operations
>     store register 1 into operations

This noncompliant code example also violates [EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects).
## Compliant Solution
The execution of functions, including inline functions, cannot be interleaved, so problematic orderings are not possible:
``` c
int operations = 0, calls_to_F = 0, calls_to_G = 0;
inline int f(int x) {
  ++operations;
  ++calls_to_F;
  return 2 * x;
}
inline int g(int x) {
  ++operations;
  ++calls_to_G;
  return x + 1;
}
void func(int x) {
  int y = f(x) + g(x);
}
```
### Platform-Specific Details
GNU C (and some other compilers) supported inline functions before they were added to the C Standard and, as a result, have significantly different semantics. Richard Kettlewell provides a good explanation of differences between the C99 and GNU C rules \[[Kettlewell 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Kettle03)\].
## Exceptions
**PRE00-C-EX1:** Macros can be used to implement *local functions* (repetitive blocks of code that have access to automatic variables from the enclosing scope) that cannot be achieved with inline functions.
**PRE00-C-EX2:** Macros can be used for concatenating tokens or performing stringification. For example,
``` java
enum Color { Color_Red, Color_Green, Color_Blue };
static const struct {
  enum Color  color;
  const char *name;
} colors[] = {
#define COLOR(color)   { Color_ ## color, #color }
  COLOR(Red), COLOR(Green), COLOR(Blue)
};
```
calculates only one of the two expressions depending on the selector's value. See [PRE05-C. Understand macro replacement when concatenating tokens or performing stringification](PRE05-C_%20Understand%20macro%20replacement%20when%20concatenating%20tokens%20or%20performing%20stringification) for more information.
**PRE00-C-EX3:** Macros can be used to yield a compile-time constant. This is not always possible using inline functions, as shown by the following example:
``` java
#define ADD_M(a, b) ((a) + (b))
static inline int add_f(int a, int b) {
  return a + b;
}
```
In this example, the `ADD_M(3,4)` macro invocation yields a constant expression, but the `add_f(3,4)` function invocation does not.
**PRE00-C-EX4:** Macros can be used to implement type-generic functions that cannot be implemented in the C language without the aid of a mechanism such as C++ templates.
An example of the use of [function-like macros](BB.-Definitions_87152273.html#BB.Definitions-function-likemacro) to create type-generic functions is shown in [MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](MEM02-C_%20Immediately%20cast%20the%20result%20of%20a%20memory%20allocation%20function%20call%20into%20a%20pointer%20to%20the%20allocated%20type).
Type-generic macros may also be used, for example, to swap two variables of any type, provided they are of the same type.
**PRE00-C-EX5:** Macro parameters exhibit call-by-name semantics, whereas functions are call by value. Macros must be used in cases where call-by-name semantics are required.
## Risk Assessment
Improper use of macros may result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE00-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | macro-function-likefunction-like-macro-expansion | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE00 |  |
| CodeSonar | 8.3p0 | LANG.PREPROC.FUNCMACRO | Function-Like Macro |
| Cppcheck Premium | 24.11.0 | premium-cert-pre00-c |  |
| ECLAIR | 1.2 | CC2.PRE00 | Fully implemented |
| Helix QAC | 2024.4 | C3453 |  |
| Klocwork | 2024.4 | MISRA.DEFINE.FUNC |  |
| LDRA tool suite | 9.7.1 | 340 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-PRE00-a | A function should be used in preference to a function-like macro |
| PC-lint Plus | 1.4 | 9026 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rec. PRE00-C | Checks for use of function-like macro instead of function (rec. fully covered) |
| RuleChecker | 24.04 | macro-function-likefunction-like-macro-expansion
 | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S960 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE00-CPP. Avoid defining macros |
| ISO/IEC TR 24772:2013 | Pre-processor Directives [NMP] |
| MISRA C:2012 | Directive 4.9 (advisory) |

## Bibliography

|  |  |
| ----|----|
| [Dewhurst 2002] | Gotcha #26, "#define Pseudofunctions" |
| [FSF 2005] | Section 5.34, "An Inline Function Is as Fast as a Macro" |
| [Kettlewell 2003] |  |
| [Summit 2005] | Question 10.4 |

------------------------------------------------------------------------
[](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152393)
## Comments:

|  |
| ----|
| C99, section 6.5.15 "The Conditional Operator", says:
The first operand is evaluated; there is a sequence point after its evaluation. The second operand is evaluated only if the first compares unequal to 0; the third operand is evaluated only if the first compares equal to 0; the result is the value of the second or third operand (whichever is evaluated), converted to the type described below.
That seems to suggest that PRE00-EX2 is unnecessary, since you don't need a macro to use 'lazy evaluation' with the conditional operator.
                                        Posted by svoboda at Jun 01, 2009 16:02
                                     |
| I'm also not sure I understand the point of PRE00-EX2. Is there a better example?
In my experience, the two most compelling use cases in favor of macros are:
    token concatenation and/or stringification
enum Color { Color_Red, Color_Green, Color_Blue };
static const struct {
  enum Color  color;
  const char *name;
} colors[] = {
#define COLOR(color)   { Color_ ## color, #color }
  COLOR(Red), COLOR(Green), COLOR(Blue)
};

implicit expansion of `__FILE__`, `__LINE__`, and `__func__`
``` java
#ifndef NDEBUG
#  define TRACE(fmt, ...) \
    trace("%s:%d (%s): " fmt, __FILE__, __LINE__, __func__, __VA_ARGS__)
#else
#  define TRACE(...) (void)0
#endif
void trace(const char *fmt, ...);
void foo(int a, const char *b) {
  TRACE("a = %d, b = %s\n", a, b);
  /* ... */
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 20, 2010 22:46
\| \|
I replaced the existing exception with your token concatenation and/or stringification example.
I hesitated for your second example which uses implicit expansion of \_*FILE, \_\_LINE, and \_\_func*\_ but also defines a function like macro TRACE().
Doesn't this represent yet another exception to this guideline?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 21, 2010 06:44
\| \|
Yes. Specifically the \_*FILE*\_ and \_*LINE*\_ macros (and others?) provide info you can't get properly from embedding them in a function.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 21, 2010 11:22
\| \|
The return type in PRE00-EX3 appears to be missing.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Mar 06, 2010 00:12
\| \|
I missed your and Robert's responses to my comment.
Yes, my goal behind showing the `TRACE()` macro was to illustrate an exception to this guideline. However, I'm not sure I see the relationship between \_\_FILE\_\_, \_\_LINE\_\_ and this guideline since it focuses on function-like macros. That said, I think a guideline advising against defining macros in general, i.e., including object-like macros, would be appropriate, but I cannot find one. If no one objects I'd like to go ahead and add one. Or rather, extend this one to both kinds of macros.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 06, 2010 10:40
\| \|
If you have a good 'avoid writing object-like macros' go ahead & suggest it. This rule is big enough and covers the function-like- macro space; I'd ranter not complicate it further.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 09, 2010 09:52
\| \|
Are there any objections to extending this guideline to recommend against all macros, not just function-like macros, and renaming it to: **Prefer typed constants and functions to macros**?
The rationale should be obvious: object-like macros are subject to type safety problems, cause namespace pollution, and may cause code bloat (due to duplication of string literals, for example).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 27, 2010 14:22
\| \|
We have a number of guidelines which when taken together say this.
-   This one.
-   [PRE03-C. Prefer typedefs to defines for encoding types](/confluence/pages/createpage.action?spaceKey=seccode&title=PRE03-C.+Prefer+typedefs+to+defines+for+encoding+types)
-   [DCL06-C. Use meaningful symbolic constants to represent literal values](DCL06-C_%20Use%20meaningful%20symbolic%20constants%20to%20represent%20literal%20values)
DCL06-C isn't as strong as "don't use object-like macros" and in fact contains a compliant solution using object-like macros.
I'm a little worried that such a guideline might be too strong for C language. Tom frequently comments at WG14 meetings that "we're not C+, we like macros" which I think may represent a slightly different mindset among C programmers than C+ programmers. If someone would to write a checker for such a guideline it would definitely find **alot** of true positives (as would a checker for finding function-like macros). It might be that you could just strengthen DCL06-C to suggest a preference order among the various mechanisms defining symbolic constants and clearly identify the problems with object-like macros. I think there are good arguments for using enum constants over const-qualified Objects for integer constants as well (don't consume memory, you can't take their address).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Mar 27, 2010 15:31
\| \|
I'm actually with Tom on this one. Despite everyone's best efforts, the unfortunate reality is that writing portable programs in C and especially in C++ would be virtually impossible without macros and I suspect a checker would have plenty of macros of both kinds to complain about. (Google Code Search returns about [41,000](http://tinyurl.com/yeja68y) records of object-like macros in C code and [30,000](http://tinyurl.com/ya8aaxk) occurrences of function-like macros).
That being said, it seems to me that a function-like macro that avoids the common pitfalls (i.e., [PRE01-C](PRE01-C_%20Use%20parentheses%20within%20macros%20around%20parameter%20names), [PRE02-C](PRE02-C_%20Macro%20replacement%20lists%20should%20be%20parenthesized), [PRE31-C](/confluence/pages/createpage.action?spaceKey=seccode&title=PRE31-C.+Avoid+side-effects+in+arguments+to+unsafe+macros), etc.) is no more dangerous than an object-like macro. Both run the risk of colliding with names in other scopes, but with care, both can be used safely. Given that, the rationale for having a guideline advising against writing one kind seems just as good for having a guideline against the other.
Furthermore, as evidenced by the number of exceptions to this guideline, there are a good number of use cases involving function-like macros that cannot be adequately handled by other means (inline functions). On the other hand, outside of `#if` directives I cannot think of any use cases involving object-like macros that could not be equivalently handled by using static constants of the appropriate type instead. In my view, this makes the argument against object-like macros even more compelling than the one against function-like ones.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 27, 2010 19:55
\| \|
`inline` is actually wrong. It's the C99 keyword that actually means the definition in header file is provided for inlining (but the compiler doesn't have to inline it, in fact some compilers ignore this keyword entirely). Inline functions are relatively tricky in C99 - the `inline`;keyword should be specified in the header, but the actual code also should have definition of it without the keyword (code duplication, but I doubt anyone cares). Or use `static inline` to actually make function inline (without actually compiling it to object code).
This is not some random issue, forgetting that `inline` used by itself doesn't actually define the function causes problems in non-gcc compilers (like clang).
![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Nov 12, 2013 16:11
\| \|
The usage of;`inline` in this recommendation is acceptable because the examples place the inline on the function definition, not the function prototype.  All of the examples show functions with external linkage due to being at file scope, but also demonstrate usages within the same translation unit.  As such, they are a valid inline definition. I am not certain what problems you are seeing with compilers such as Clang, but my testing of these examples demonstrated correct behavior (so perhaps it's a version-specific bug with the compiler, or perhaps your tests differ from mine).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 13, 2013 16:31
\| \|
<http://clang.llvm.org/compatibility.html#inline>
![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Dec 10, 2013 02:56
\| \|
inline always misused
![](images/icons/contenttypes/comment_16.png) Posted by 13611593077 at Dec 02, 2019 03:00
\| \|
I think it is also worth pointing out some of the extremely subtle mistakes one can make when porting macros to functions.For instance, consider the following (admittedly contrived) noncompliant code example.  
In this example, the macro **INIT_DB** applies the unary address-of operator (**&**) to its argument **con**:
``` cpp
struct connection_t {
    // name, socket, etc.
};
struct database_t {
    struct connection_t *conn;
};
#define INIT_DB(db, con) ((db)->conn = &(con))
void func() {
    struct database_t *db = malloc(sizeof(struct database_t));
    struct connection_t con;
    INIT_DB(db, con);
    free(db);
}
```
An obvious but erroneous way to make this example compliant would be to replace the macro **INIT_DB** with a static inline function:
``` cpp
static inline void init_db(struct database_t *db, struct connection_t con) {
  ((db)->conn = &(con));
}
```
However this would not preserve the behavior of the original macro, because of the difference between function semantics (call-by-value) and macro semantics (call-by-name).  
The macro invocation, once expanded, applies the **&** operator to the local variable **con** declared in the definition of **func**.  
On the other hand, the function definition of **init_db** applies the **&** operator to the function parameter **con** instead.  
So if one were to replace the macro **INIT_DB** with the function **init_db**, they would assign **db**'s **conn** member to a dangling pointer.
The compliant solution would be to replace the macro definition with a slightly different function definition:
``` cpp
static inline void init_db(struct database_t *db, struct connection_t *con) {
  ((db)->conn = con);
}
```
and also change the invocation site to match:
``` cpp
INIT_DB(db, &con);
```
This may even warrant its own recommendation (e.g., "Do not use argument L-values in macro definitions"), though I am not sure.
![](images/icons/contenttypes/comment_16.png) Posted by pappasbrent at Oct 11, 2022 12:08
\| \|
Brent:
In your code example, INIT_DB actually violates DCL30-C, by letting the static db struct contain a pointer to the con struct, which is local to func(). This is OK by itself, but if your code ever tries to dereference db-\>con after exiting func(), you will be in for a surprise. ;Changing INIT_DB to an inline function does nothing to address this problem (although it doesn't hurt things worse).
See CERT rule DCL30-C, and particularly, its first non-compliant code example for details.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 11, 2022 13:45
\| \|
Hi David,
Thanks for catching that violation of DCL30-C.I've edited my original comment to be in compliance with this rule.
This has got me thinking about PRE00-C-EX5.  
If a macro reads the L-value of one of its arguments, does it fall under this exception, and thus should not be converted to an inline function?  
Here are some macros I found in Lua, Linux, and Perl that do this:
\- <https://github.com/lua/lua/blob/26be27459b11feabed52cf40aaa76f86c7edc977/lundump.c#L58>  
- <https://github.com/torvalds/linux/blob/49da070062390094112b423ba443ea193527b2e4/fs/stat.c#L364>  
- <https://github.com/Perl/perl5/blob/f08b7a33d99b9b204260e108bc1789c5392aff36/numeric.c#L1461>
Would these all be examples of PRE00-C-EX5?  
In either case I think that exception may benefit from an example, would you consider adding one?
![](images/icons/contenttypes/comment_16.png) Posted by pappasbrent at Oct 12, 2022 14:04
\| \|
> If a macro reads the L-value of one of its arguments, does it fall under this exception, and thus should not be converted to an inline function?

If it doesn't, then we should make a new exception for it. Consider this macro:
    #define ALL_ONES(x) memset(&(x), '\xff', sizeof(x))
It can't be replaced with an inline function, since then sizeof(x) would end up being the size of a pointer instead of the size of the thing it's supposed to be operating on, so we definitely shouldn't ban it as a macro.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Oct 12, 2022 15:08
\| \|
Brent & Joe:
The Linux code example cited by Brent, and Joe's code example both use macros to achieve type genericity; that' is why they don't translate well to inline functions. They would be captured by PRE00-C:EX4 rather than EX5.
Typically we enumerate exceptions for rules, not recommendations. We ;enumerated the exceptions for this recommendation in the hope of promoting it to a rule; however, I doubt we can promote this to a rule yet. I do suspect there are many more exceptions that we haven't enumerated.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 13, 2022 12:31
\| \|
Hi David,
Good point about PRE00-C-EX4 - I had not considered that these macros would be covered under that exception. What may also be relevant is that macros share their caller's scope, whereas functions create their own scope, causing l-value differences:
``` c
#define M(x) (&(x))
int *f(int x) { return (&(x)); }
```
`M` doesn't return the same L-value as `f`, because `M` has no local scope. I originally thought this was due to call-by-name vs. call-by-value, but similar scoping anomalies happen without parameters too:
``` c
#define X() g
&X();  // gets address of g
```
Do you think such scoping differences warrant a separate exception as Joseph hinted at?
P.S. I'm a PhD student working on automatically transforming macro functions to C functions, so these guidelines are an interesting source for deciding when a macro should or shouldn't be transformed.
![](images/icons/contenttypes/comment_16.png) Posted by pappasbrent at Oct 20, 2022 14:37
\| \|
Brent:
Interesting. I am also working on automated source code transformations. ;It is possible that in the course of your studies you will come to understand EX5 better than us; in which case you can advise us on how to improve that exception :)
I suspect that the answer to Joe's question is no: that EX5 would cover a macro that needs the l-value of its argument.  Unless the inline function took a pointer to the argument.  It's hard to tell...can you come up with a code example that might fall under EX5 but not EX4?  I do think that EX5 needs a code example to support it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 20, 2022 15:33
\| \|
Hi David,
[Here](https://github.com/mirror/ncurses/blob/859f2280a309b121d29160e4d066ecc0fd39e52c/progs/dump_entry.c#L904) is an example of a macro that falls under EX5 and does not fall under EX4 (I think):
    #define SAME_CAP(n,cap) (&tterm->Strings[n] == &cap)
I do not think this macro is generic because `cap` has to have the same type as `&tterm->Strings[n]` for the expression to typecheck without warning.
Here are [two](https://github.com/torvalds/linux/blob/98555239e4c3aab1810d84073166eef6d54eeb3d/arch/arc/kernel/smp.c#L130) [more](https://github.com/lua/lua/blob/02060b7a37d88d4e92cf64a008c0651eae432c12/lgc.c#L159) examples of realworld macros that fall under EX5 and not EX5, as well as [three contrived examples](https://gist.github.com/PappasBrent/d573d1ae739b1dd3ae6f669629de7ddd).
Hopefully this will be useful for the standard, and perhaps we can chat in the future about source-to-source transformations.
![](images/icons/contenttypes/comment_16.png) Posted by pappasbrent at Oct 28, 2022 15:15
\| \|
Brent:
I agree your code examples are not type-generic, so EX4 does not apply to them.But I'm also not convinced they are better off as macros rather than inline functions:
    inline bool same_cap(term_type *tterm, size_t n,  cap_type *cap) {
       return tterm->Strings[n]  == cap;
    }
    if (same_cap( tterm, n, &cap))
      ...
The inline function has the advantage of being more "honest" about the number & types of arguments.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 31, 2022 09:01
\|
