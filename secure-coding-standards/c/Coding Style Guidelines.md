This document details the coding style guidelines to be used within the CERT C and C++ Coding Standards. It is not meant as a general-purpose style guideline for production code and is not intended to be viewed as a "secure coding style guideline." It is only meant as a mechanism to ensure the coding standards have a uniform coding style. Note that deviation from these rules is always acceptable if the substantive content of the rule requires it. For instance, a rule about K&R-style C functions is not required to have the code examples include function declarations with prototypes, despite that being a style guideline.
## Basics
-   NCCE source code should have the standard "red box" background. CS source code should have the standard "blue box" background, as should code examples that are showing a valid exception to the rule. Informative source code that is neither NCCE nor CS/exception should have no background.
-   All NCCE and CS code examples must compile without requiring user modification unless otherwise noted in the text surrounding the example code. The only exception to this rule is for code samples pulled from snippets of other source (such as when demonstrating a vulnerability from a CVE). In this case, the surrounding text should cite the source of the code (preferably with a link so that the reader can find more context for the source code). Some web hosted C and C++ compilers that you can use for testing include:
    -   <http://coliru.stacked-crooked.com/> (clang and gcc)
    -   <http://melpon.org/wandbox/> (clang and gcc)
    -   <http://webcompiler.cloudapp.net/> (Microsoft Visual Studio)
    -   <http://gcc.godbolt.org/> (clang, gcc, and icc)
    -   <http://ideone.com/> (gcc)
Note that the examples must compile but **are not** required to link. Not every example needs to have a `main` function, or requires function definitions, for instance.
If you have a code example that fixes a problem by being ill-formed, it should use a red box and be a noncompliant code example, followed by a well-formed compliant solution. For example, we have a C++ NCCE that uses auto_ptr. A second NCCE replaces auto_ptr with unique_ptr, rendering the code ill-formed. While this is an NCCE it is obvious because the compiler will complain. There is a subsequent CS using unique_ptr that is compile-able. This is in [VOID MEM00-CPP. Don't use auto_ptr where copy semantics might be expected](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+MEM00-CPP.+Don%27t+use+auto_ptr+where+copy+semantics+might+be+expected).
-   Code should have as few `#include` statements as possible, and only include the functionality required for the code example (from the canonical header for that functionality, not transitively via some other intermediary header). e.g., when the code example requires a variable of type `size_t`, include `stddef.h` or `cstddef` directly, instead of obtaining the type through another header, such as `string.h`. Includes should be listed in alphabetical order when possible.
-   When refering to code entities from the surrounding text (including file header names, function names, variable names, etc), the entities should be written in `monospace font`.
-   All NCCEs should only violate the rule being discussed, and comply with secure coding *recommendations* unless otherwise noted in the surrounding text. All CSs should comply with all secure coding rules and recommendations.
-   Code should not exceed an 80 column limit, including comments.
-   \<thought\>Run clang-format over the code, using a format configuration file that I gin up and expose from this page. This takes care of all spacing, column limits, where-do-line-breaks-go kind of questsions.\</thought\>
## Broad Details
These details apply only to code built to illustrate an example. They do not apply to pre-existing code, such as excerpts from a bug report or open-source software.
Java code should use the standard Java conventions as mandated by Sun, with the single exception that indentation is two spaces rather than four.
The following details apply to C & C++ code
-   All non-builtin type and enumerator names should be in [PascalCase](http://c2.com/cgi/wiki?PascalCase). e.g., `struct S;` `typedef int MyAwesomeInt;` `template <typename T>`, `enum MyEnum { MyFirstValue, MySecondValue };` etc.
-   All function names should be in [snake_case](https://en.wikipedia.org/wiki/Snake_case). e.g., `void func();`, `int my_awesome_int_func(void);`, `struct S { void cool_func(); };` etc.
    -   Excluded from this requirement are: constructors and destructors.
-   All variable names should be in [camelCase](http://c2.com/cgi/wiki?CamelCase). e.g., `int i;` `std::string userPassword;`, `struct S { int i; char smallData; };` etc.
-   All macro definition names should be in UPPERCASE. e.g., `#define FOO(x) (x)`
-   Do not use Hungarian notation.
-   Use `/**/` for multiline comments, use `//` for single-line comments, in both C and C++ code. Comments should be a complete sentence or noun phrase (with proper spelling, grammar, capitalization, and punctuation), except when given an imperative (e.g., Handle error).
-   Use two spaces for indentation. Do not tabs. Indent all code consistently.
Function Details
-   When writing C code (including C++ code marked as `extern "C"`), always provide a function prototype. e.g., `void func(void);` instead of `void func();`
-   When writing C++ code, do not include a parameter type list for a function that accepts no arguments. e.g., `void func();` instead of `void func(void);`
## Control Flow Details
-   All control flow statements should use a compound statement block instead of a single, non-compound statement. e.g., `if (x) { x = y; }` instead of `if (x) x = y;`
-   Do not use `else` after something that interrupts control flow (`return`, `break`, etc). This reduces the amount of indented code and makes the examples more readable. e.g., `if (x) { return; } else { /* Do not do this; remove the else. */ }`
## Microscopic Details
-   Put spaces between an open parenthesis only in control flow statements. e.g., `if (x);` instead of `if(x);` Do not put spaces in function calls or function-like macro invocations. e.g., `foo(1, 2);` instead of `foo (1, 2);` or `foo( 1, 2 );`
-   Prefix and suffix binary operators with spaces. e.g. `1 + 1 * 2` instead of `1+1*2`.
## C++ Details
-   Do not use `auto` unless the type is explicitly spelled out within the remainder of the statement. e.g., `int good = g();` instead of `auto bad = g();`  `auto *good = dynamic_cast<SomeType *>(bar);`
-   Do not use `using namespace XXX;` at file scope (it is permissible at function scope, but should be used very sparingly).
-   Since we now care about C++14 more than C++98, use `>>` rather than `> >` to close out nested template declarations. e.g., `std::vector<Foo<int>>;` instead of `std::vector<Foo<int> >;`
## C Details
-   Since we now care about C11 more than C89, put variable declarations as close to their use as possible instead of in a group at the top of a function definition. Declare the loop induction variable as part of a `for` loop instead of at function scope.
## Comments:

|  |
| ----|
| FWIW, I picked a 40 column limit explicitly over an 80 column limit because of book formatting. 80 columns of monospaced text doesn't look very good in printed format from what I recall, and 40 columns makes it much more likely to not run off the edge of a page. We should have something more concrete than my guesstimate, but my gut feeling is that 80 columns is way too long for our web & print needs.
                                        Posted by aballman at May 20, 2016 10:38
                                     |
| We have an old style guidelines doc: https://www.securecoding.cert.org/confluence/display/sci/Secure+Coding+Standard+Development+Guidelines
I think this eventually morphed into our introduction matieral, but there is some content there we should resurrect.
                                        Posted by svoboda at May 20, 2016 10:44
                                     |
| WRT broad details, do we use snake_case or camelCase for C variables? ;IMO we should adopt whatever standard we have been following so far, which is snake_case.
                                        Posted by svoboda at May 20, 2016 10:44
                                     |
| Ah, interesting and good to know.
                                        Posted by aballman at May 20, 2016 10:46
                                     |
| I think we mostly use single-letter, lowercase variables in C which works as camelCase or snake_case. I picked snake_case for functions because of its usage in the STL. I picked camelCase for variables because it distinguishes between variable and function for descriptive names (which we rarely use anyway). e.g.,
void this_is_a_function();
void g();
;
void f() {
  auto thisIsAVariable = [](){};
  thisIsAVariable(); // You know this is called through a function pointer or lambda object instead of a direct call.
  this_is_a_function(); // You know this is a direct function call.
  g(); // Good luck.
}

![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 20, 2016 10:48
\| \|
[FIO15-C. Ensure that file operations are performed in a secure directory](FIO15-C_%20Ensure%20that%20file%20operations%20are%20performed%20in%20a%20secure%20directory) is a guideline that uses snake_case for variables and functions. Any counterexamples?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2016 10:57
\| \|
I pay no attention to recommendations because no one else pays attention to them.;![](images/icons/emoticons/tongue.svg)
[EXP30-C. Do not depend on the order of evaluation for side effects](EXP30-C_%20Do%20not%20depend%20on%20the%20order%20of%20evaluation%20for%20side%20effects) (snake_case for variables)
[EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory) (snake_case for functions and variables)
[EXP47-C. Do not call va_arg with an argument of the incorrect type](EXP47-C_%20Do%20not%20call%20va_arg%20with%20an%20argument%20of%20the%20incorrect%20type) (camelCase for variables)
[MSC40-C. Do not violate constraints](MSC40-C_%20Do%20not%20violate%20constraints) (PascalCase and snake_case for variables)
I think existing practice is mostly incredibly terse identifiers where it doesn't matter with a smattering of wildly inconsistent identifiers.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 20, 2016 11:10
\| \|
Looking at these rules, I'd say snake_case was the unspoken convention. EXP47-C was a case where the author didn't get that memo (because it was unspoken;![](images/icons/emoticons/smile.svg)  MSC40-C was clearly written by someone who was still thinking about Java ![](images/icons/emoticons/smile.svg), and it is one of the later rules.
So I'd say that its less work to convert our rules to use snake_case than any other convention.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2016 13:19
\| \|
Okay, so types and enumerators are PascalCase, functions and variables are snake_case, macros are UPPERCASE, and nothing is camelCase?
![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 20, 2016 13:25
\| \|
Functions & variables should be snake_case; it's easy to distinguish them b/c of the parens.Macros are UPPERCASE.  
Classes and custom typedefs are PascalCase.
All the structs I have seen are lowercase, but they are preceded by 'struct', so I don't care. If you use typedef to create a struct type (that does not need the struct keyword) you can use PascalCase.
Constants and enumerator values are PascalCase.
This is difficult to mandate b/c we loosely based our standards on K&R and they weren't consistent. Consider that constants, enumeration values, and macros can be used interchangeably but have different conventions. Also consider that the standard permits some functions (eg getc()) to be implemented as macros.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2016 13:39
\| \|
Parens don't distinguish them, which is why I was advocating for different conventions. You cannot tell from parens alone whether something is a function pointer (variable), lambda (variable), or direct call (function). However, I don't see much use to that distinction in a coding style for short snippets of code vs production code, so I don't care what convention we use there so long as we apply it consistently.
You're probably correct about structs in C, but the structs being used in the C++ space are (all?) PascalCase (and do not use the;`struct` keyword to introduce them as a type in a declaration). I would prefer we just consistently say "if it's defining a type, use PascalCase" simply because it is consistent, which is the whole point to this exercise.
I'm not concerned about functions the standard permits to be implemented as macros (which for the C standard library is "all of them"), but macro **definitions** that we define ourselves.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 20, 2016 14:02
\|
