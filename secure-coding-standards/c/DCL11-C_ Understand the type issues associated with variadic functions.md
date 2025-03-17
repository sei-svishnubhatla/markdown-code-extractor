The variable parameters of a variadic function—that is, those that correspond with the position of the ellipsis—are interpreted by the `va_arg()` macro. The `va_arg()` macro is used to extract the next argument from an initialized argument list within the body of a variadic function implementation. The size of each parameter is determined by the specified type. If the type is inconsistent with the corresponding argument, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and may result in misinterpreted data or an alignment error (see [EXP36-C. Do not cast pointers into more strictly aligned pointer types](EXP36-C_%20Do%20not%20cast%20pointers%20into%20more%20strictly%20aligned%20pointer%20types)).
The variable arguments to a variadic function are not checked for type by the compiler. As a result, the programmer is responsible for ensuring that they are compatible with the corresponding parameter after the default argument promotions:
-   Integer arguments of types ranked lower than `int` are promoted to `int` if `int` can hold all the values of that type; otherwise, they are promoted to `unsigned int` (the *integer promotions*).
-   Arguments of type `float` are promoted to `double`.
## Noncompliant Code Example (Type Interpretation Error)
The C `printf()` function is implemented as a variadic function. This noncompliant code example swaps its null-terminated byte string and integer parameters with respect to how they are specified in the format string. Consequently, the integer is interpreted as a pointer to a null-terminated byte string and dereferenced, which will likely cause the program to [abnormally terminate](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination). Note that the `error_message` pointer is likewise interpreted as an integer.
``` c
const char *error_msg = "Error occurred";
/* ... */
printf("%s:%d", 15, error_msg);
```
## Compliant Solution (Type Interpretation Error)
This compliant solution modifies the format string so that the conversion specifiers correspond to the arguments:
``` c
const char *error_msg = "Error occurred";
/* ... */
printf("%d:%s", 15, error_msg);
```
As shown, care must be taken to ensure that the arguments passed to a format string function match up with the supplied format string.
## Noncompliant Code Example (Type Alignment Error)
In this noncompliant code example, a type `long long` integer is incorrectly parsed by the `printf()` function with a `%d` specifier. This code may result in data truncation or misrepresentation when the value is extracted from the argument list.
``` c
long long a = 1;
const char msg[] = "Default message";
/* ... */
printf("%d %s", a, msg);
```
Because a `long long` was not interpreted, if the `long long` uses more bytes for storage, the subsequent format specifier `%s` is unexpectedly offset, causing unknown data to be used instead of the pointer to the message.
## Compliant Solution (Type Alignment Error)
This compliant solution adds the length modifier `ll` to the `%d` format specifier so that the variadic function parser for `printf()` extracts the correct number of bytes from the variable argument list for the `long long` argument:
``` c
long long a = 1;
const char msg[] = "Default message";
/* ... */
printf("%lld %s", a, msg);
```
## Noncompliant Code Example (`NULL`)
The C Standard allows NULL to be either an integer constant or a pointer constant. While passing NULL as an argument to a function with a fixed number of arguments will cause NULL to be cast to the appropriate pointer type, when it is passed as a variadic argument, this will not happen if `sizeof(NULL) != sizeof(void *). `This is possible for several reasons:
-   Pointers and ints may have different sizes on a platform where NULL is an integer constant
-   The platform may have different pointer types with different sizes on a platform. In that case, if NULL is a void pointer, it is the same size as a pointer to char (C11 section 6.2.5, paragraph 28), which might be sized differently than the required pointer type.
On either such platform, the following code will have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
char* string = NULL;
printf("%s %d\n", string, 1);
```
On a system with 32-bit `int` and 64-bit pointers, `printf()` may interpret the `NULL` as high-order bits of the pointer and the third argument `1` as the low-order bits of the pointer. In this case, `printf()` will print a pointer with the value `0x00000001` and then attempt to read an additional argument for the `%d` conversion specifier, which was not provided.
## Compliant Solution (`NULL`)
This compliant solution avoids sending `NULL` to `printf()`:
``` c
char* string = NULL;
printf("%s %d\n", (string ? string : "null"), 1);
```
## Risk Assessment
Inconsistent typing in variadic functions can result in [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) or unintended information disclosure.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL11-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL11 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.ELLIPSIS | Ellipsis |
| Compass/ROSE |  |  | Does not currently detect violations of this recommendation. Although the recommendation in general cannot be automated, because of the difficulty in enforcing contracts between a variadic function and its invokers, it would be fairly easy to enforce type correctness on arguments to the printf() family of functions |
| ECLAIR | 1.2 | CC2.DCL11 | Partially implemented |
| GCC | 4.3.5 |  | Warns about inconsistently typed arguments to formatted output functions when the -Wall is used |
| Helix QAC | 2024.4 | C0179, C0184, C0185, C0186, C0190, C0191, C0192, C0193, C0194, C0195, C0196, C0197, C0198, C0199, C0200, C0201, C0206, C0207, C0208 |  |
| Klocwork | 2024.4 | MISRA.FUNC.VARARGSV.FMT_STR.PRINT_FORMAT_MISMATCH.BAD
SV.FMT_STR.PRINT_FORMAT_MISMATCH.UNDESIRED
SV.FMT_STR.SCAN_FORMAT_MISMATCH.BAD
SV.FMT_STR.SCAN_FORMAT_MISMATCH.UNDESIRED
SV.FMT_STR.PRINT_IMPROP_LENGTH
SV.FMT_STR.PRINT_PARAMS_WRONGNUM.FEW
SV.FMT_STR.PRINT_PARAMS_WRONGNUM.MANY
SV.FMT_STR.UNKWN_FORMAT.SCAN |  |
| LDRA tool suite | 9.7.1 | 41 S, 589 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL11-aCERT_C-DCL11-b
CERT_C-DCL11-c
CERT_C-DCL11-d
CERT_C-DCL11-e
CERT_C-DCL11-f | There should be no mismatch between the '%s' and '%c' format specifiers in the format string and their corresponding arguments in the invocation of a string formatting function
There should be no mismatch between the '%f' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
There should be no mismatch between the '%i' and '%d' format specifiers in the string and their corresponding arguments in the invocation of a string formatting function
There should be no mismatch between the '%u' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
There should be no mismatch between the '%p' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
The number of format specifiers in the format string and the number of corresponding arguments in the invocation of a string formatting function should be equal |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 175, 559, 2408 | Assistance provided: reports issues involving format strings |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL11-C | Checks for format string specifiers and arguments mismatch (rec. partially covered) |
| PVS-Studio | 7.35 | V576 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this recommendation on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL11-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Type System [IHN]Subprogram Signature Mismatch [OTR] |
| MISRA C:2012 | Rule 17.1 (required) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152093) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152098)
## Comments:

|  |
| ----|
| The example here seems rather contrived. A mismatch between printf format specifications and arguments passed is a widely known problem and really does not have anything to do with the point of this rule.
It seems to me that a better example would be one that intermixes arguments of clearly different widths (int with long long, float with double) so that a correcting ordered, but with incorrect type indicators, format string would result in extremely unexpected results.
Lastly, it is unclear to me that alignment errors are possible. A variadic function call results in the "..." arguments being put through default promotions, regardless of their original widths (char and short -> int). In the end, the only two possible alignments are word or double-word (as the examples I gave above). On no architecture will a word boundary cause an alignment error. And only on rare architectures must double-word values be aligned on a double-word boundary (usually word boundaries are sufficient).
All these details aside, my observation is that this example does not demonstrate your rule's title.;
                                        Posted by wlf@cert.org at Jul 11, 2007 08:47
                                     |
| While the example seems contrived, on my copy of Visual C++ 2005 it compiles without warning on the highest warning level (and of course promptly crashes when ran due to the attempt to dereference the value 15 converted to an address). I think writing something off because it is a widely known problem is not the way to go about things.
I agree that the previous NCCE/CS did not fully encompass what the recommendation was hoping to accomplish, but I'm not sure I understand how it does not demonstrate the rule's title--it displays a failure to understand the type issues of printf which leads to an integer being converted to a pointer which is dereferenced. I think your idea of displaying a width issue was a good idea and it has been added.
As for the possibility of an alignment error, I've removed some references specifically mentioning this. However, since the scope of this wiki is the C standard, which does not define a specific concept of "words" or "double-words" and makes no guarantees about the effective dereference of something misaligned, I do not see anything wrong with mentioning this as a possibility, especially since, as you mention, it is a problem on some architectures.
                                        Posted by shaunh at Jul 11, 2007 14:01
                                     |
| 100% of C programmers use printf(), but far less use variadic functions of their own creation, and I believe that making a separate printf-type page would make these rules a lot more approachable.
The rules are essentially the same, of course, but removing the va_arg() business to a separate rule means that one can focus on conveying the alignment and promotion rules in a much more familiar context.
                                        Posted by steve at Mar 13, 2008 20:33
                                     |
| long long a = 1L;
char msg[] = "Default message";
/* ... */
printf("%lld %s", a, msg);
Â 
sizeof(msg) will be 17 but not 128   Â 
long long a = 1L - Software Optimization Guide for AMD64 Processors
                                        Posted by pavlinux at Mar 15, 2008 19:20
                                     |
| I don't think I get it - naming an array size overrides the size implied by the initializer.
char msg[] = "Foo";Â;Â Â     // sizeof(msg) = 4
char msg[128] = "Foo"; // sizeof(msg) = 128

![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 15, 2008 20:02
\| \|
I recall that Fortify SCA can also detect violations of this rule. Can someone double check and add to auto-detection section if appropriate?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jul 06, 2008 13:11
\| \|
This is perhaps an issue specific to the macro `NULL` rather than to variadic functions but I haven't been able to find a rule that deals with the former.
Another cause of undefined behavior is using the `NULL` macro as an argument to a variadic functions such as `printf()` or `execl()` where a pointer value is expected. For example, the following function calls will have undefined behavior when `sizeof(NULL) != sizeof(void*)` as may be the case in LP64 when `NULL` defined to be of type `int`:
``` java
printf("%p %d\n", NULL, 1);
execl("ls", "*.text", NULL);
```
To ensure that the calls behave correctly the code must be written like so:
``` java
printf("%p %d\n", (void*)0, 1);
execl("ls", "*.text", (char*)0);
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Nov 30, 2009 23:48
\| \|
The issue is specific to both NULL and variadic functions because
-   NULL may be defined as an int or a pointer
-   variadic functions do not convert between ints and pointers. (I think non-variadic functions will take NULL as an int or pointer as indicated by the function's appropriate argument type.)
Anyway, I've added your issue to the rule as another NCCE/CS pair. Thanks!
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 01, 2009 16:36
\| \|
``` java
printf("%s\n", (char *)NULL);
```
C99 does not define what happens if you pass NULL to a `%s` format; it expects the argument to be a valid char array, so I don't think this code can be a compliant code example, as it is undefined behavior (although it does alleviate the problem stated in DCL11-C).
On a side note, most modern implementations handle this gracefully by printing "null" or some such, but we can't promote this while remaining compliant with C99.
(BTW %p is C99, but C99 leaves as implementation-defined what actually gets printed.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 02, 2009 09:51
\| \|
I agree: neither `NULL` or `(char*)0` is a valid argument for `%s` or any other conversion specification that expects a pointer to an object in memory (e.g., `%n`).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 05, 2009 17:29
\| \|
Currently both lines of the last CCE pass NULL to a %s format.
This may be a better example:
``` java
unsigned int m = UINT_MAX-10;
printf("%lld\n", m);  //NCCE
printf("%lld\n", (long long int)m); //CCE
```
![](images/icons/contenttypes/comment_16.png) Posted by abrowne at Sep 27, 2010 03:31
\| \|
I modified the compliant example to not pass NULL.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 27, 2010 12:34
\| \|
`NULL` is perfectly fine for `%p`.
![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Nov 13, 2013 14:53
\| \|
`%p` does not expect a pointer to an object in memory, it expects a pointer to void, which is subtly different.; In the case of `%s` and `%n`, they expect a pointer to something specific that is then interpreted.  `%p` simply cares about the value of the pointer itself, not what the pointer is pointing to.
To be clear, you are correct that `NULL` is perfectly fine for `%p`, just that `%p` is not covered by what Martin was referring to.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 13, 2013 15:09
\| \|
I'm sorry, but I don't understand this `NULL` example. I know it's undefined (null pointer is not a string, and printing nothing could do anything), but the explanation just doesn't make sense. Yes, null pointer is not guaranteed to be `((void *) 0)`, but in this case it doesn't matter. Let's assume that we use a crazy platform where `NULL` is `((_Bool) 0)` (by the way, C specification guarantes that any constant zero is null pointer), and the code is ran on it. After this strange boolean null is assigned to `char *`, the value is a pointer (pointer that would magically change sizes depending on whether it stores null pointer or not wouldn't make sense, would it?).
I made a small code sample in order to show null pointer being boolean false. If you run it in compiler that understands null pointer is any constant zero (like Clang), you will notice that `var` has the same size as `void *`. The `NULL` is called `NULLISH`, because some compilers disallow redefining `NULL`.
``` cpp
#include <stdio.h>
#define NULLISH ((_Bool) 0)
int main(void) {
    char *var = NULLISH;
    printf("%d %d %d\n", (int) sizeof NULLISH, (int) sizeof var, (int) sizeof(void *));
    return 0;
}
```
On my computer, this code returns `1 8 8`, which makes sense. I believe the guideline should mention something else instead. I think that something like GTK+ variadic argument lists (real code) is a good idea for an example - in GTK, some functions expect list of strings that ends with null pointer. If the platform has null declared as integer, and size of pointers is different to size of integers, things break. For example, I propose following code sample as example, containing a big trap (if `NULL` is not declared as pointer, things are broken).
``` cpp
#include <stdio.h>
#include <stdarg.h>
void put_multiple(const char *argument, ...) {
    va_list args;
    va_start(args, argument);
    while (argument) {
        puts(argument);
        argument = va_arg(args, const char *);
    }
    va_end(args);
}
int main(void) {
    put_multiple("Line 1", "Line 2", "Line 3", NULL);
    return 0;
}
```
Imagine that `NULL` is declared as boolean false (completely valid, even if it's silly). You would get random explosions that would be hard to debug just because `_Bool` is not `const char *`.
![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Nov 13, 2013 15:28
\| \|
The NULL example in its current form is broken.; `string`, as passed to `printf()` has a type of `char *` and so it will be passed using the appropriate size that `printf()` expects.  At some point, we should rewrite that example to be a bit more clear as to what the problem is, and the example you point out would be a reasonable demonstration of the problem.
One other thing to note about using `((_Bool)0)` are integer promotions that happen when passing an argument as part of a variable argument list.  You don't need anything nearly so contrived to demonstrate the problem.  On any system where `sizeof(void *) != sizeof(int)`, you will run into this problem if NULL is an integer constant zero instead of a pointer constant zero.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 13, 2013 16:30
\| \|
I'm considering on how to fix this currently-wrong NCCE(NULL).
how about this idea?
-   change NCCE code to one line:; `printf("%s %d\n", NULL, 1);`
-   add a little more comment on passing NULL to "%s" specifier, which is undefined behavior
-   adding this NCCE to MSC15-C. Do not depend on undefined behavior
BTW, I just learned that C++ defines NULL as integer, not pointer.
(stll implementation-defined as 0 or 0L, but anyway, not a pointer!)
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Jan 23, 2015 06:45
\| \|
The first two bullets sound great to me.;I would also change the NCCE wording to mention that you cannot send a `char *` that is `NULL` either (as the current code does) because it would violate the `%s` constraint: "If no `l` length modifier is present, the argument shall be a pointer to the initial element of an array of character type." Either situation is undefined behavior, but the code you are proposing 1) fits the explanatory text already written, and 2) is more compelling.
I would not bother with adding the NCCE to MSC15-C (a great many of our guidelines are due to undefined behavior).
As for C++, the current recommended usage is to use `nullptr` instead of `NULL` because the former will be strongly typed to something sensible, while the latter is not type safe. You are correct that the macro `NULL` is an integral constant and not a pointer value in C++. ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 23, 2015 08:59
\| \|
C11 7.19p3 says:
> The macros are  NULL  
> which expands to an implementation-defined null pointer constant;

This text is unchanged since C99. (does C90 say something different?)
Since the standard says nothing about NULL being an integer constant, I wonder if the NULL NCCE is truly noncompliant?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 11, 2019 09:11
\| \|
See C17 6.3.2.3p3:;
> An integer constant expression with the value 0, or such an expression cast to type void \*, is called a *null pointer constant*. 

So a null pointer constant must be an integer constant expression with the value 0.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 11, 2019 10:05
\| \|
Aaron, are you suggesting the same holds for C?
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jan 14, 2019 20:53
\| \|
That quote is from the latest C standard (C17), so yes, this holds in C.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 15, 2019 08:08
\| \|
Aaron,
I just looked it up myself and found it.; The statement is in C11.  Your reference to "C17" threw me.  So, I agree, it holds in C, as your reference is to the C standard.  It looks like the exact same text (and section) is in C99 as well.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jan 15, 2019 08:50
\| \|
C17 is the final version of C11, including all resolved defect reports and is the version of the standard you should be referencing.
![](images/icons/contenttypes/comment_16.png) Posted by rcseacord at Jan 15, 2019 10:06
\| \|
Aaron thanks for the info.
I've decided that the NCCE is truly noncompliant, but the intro text was a bit muddy, so I clarified it. No change to the code or the corresponding CS.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 15, 2019 16:32
\|
