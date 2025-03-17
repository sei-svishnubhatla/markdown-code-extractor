An object of type `void *` is a generic data pointer. It can point to any data object. For any incomplete or object type `T`, C permits implicit conversion from `T *` to `void *` or from `void *` to `T *`.  C Standard memory allocation functions `aligned_alloc()`, `malloc()`, `calloc()`, and `realloc() `use `void *` to declare parameters and return types of functions designed to work for objects of different types.
For example, the C library declares `malloc()` as
``` java
void *malloc(size_t);
```
Calling `malloc(s)` allocates memory for an object whose size is `s` and returns either a null pointer or a pointer to the allocated memory. A program can implicitly convert the pointer that `malloc()` returns into a different pointer type.
Because objects returned by the C Standard memory allocation functions are implicitly converted into any object type, we recommend casting the results of these functions into a pointer of the allocated type because it increases the chances that the compiler will catch and diagnose a mismatch between the intended type of the object and the actual type of the object.
## Noncompliant Code Example
The argument to `malloc()` can be *any* value of (unsigned) type `size_t`. If the program uses the allocated storage to represent an object (possibly an array) whose size is greater than the requested size, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The implicit pointer conversion lets this slip by without complaint from the compiler.
Consider the following example:
``` c
#include <stdlib.h>
typedef struct gadget gadget;
struct gadget {
  int i;
  double d;
};
typedef struct widget widget;
struct widget {
  char c[10];
  int i;
  double d;
};
widget *p;
/* ... */
p = malloc(sizeof(gadget)); /* Imminent problem */
if (p != NULL) {
  p->i = 0;                 /* Undefined behavior */
  p->d = 0.0;               /* Undefined behavior */
}
```
An [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) may add padding to a gadget or widget so that `sizeof(gadget)` equals `sizeof(widget)`, but this is highly unlikely. More likely, `sizeof(gadget)` is less than `sizeof(widget)`. In that case,
``` c
p = malloc(sizeof(gadget)); /* Imminent problem */
```
quietly assigns `p` to point to storage too small for a widget. The subsequent assignments to `p->i` and `p->d` will most likely produce memory overruns.
Casting the result of `malloc()` to the appropriate pointer type enables the compiler to catch subsequent inadvertent pointer conversions. When allocating individual objects, the "appropriate pointer type" is a pointer to the type argument in the `sizeof` expression passed to `malloc()`.
In this code example, `malloc()` allocates space for a `gadget`, and the cast immediately converts the returned pointer to a `gadget *`:
``` c
widget *p;
/* ... */
p = (gadget *)malloc(sizeof(gadget)); /* Invalid assignment */
```
This lets the compiler detect the invalid assignment because it attempts to convert a `gadget *` into a `widget *`.
## Compliant Solution (Hand Coded)
This compliant solution repeats the same type in the `sizeof` expression and the pointer cast:
``` c
widget *p;
/* ... */
p = (widget *)malloc(sizeof(widget));
```
## Compliant Solution (Macros)
Repeating the same type in the `sizeof` expression and the pointer cast is easy to do but still invites errors. Packaging the repetition in a macro, such as
``` c
#define MALLOC(type) ((type *)malloc(sizeof(type)))
```
further reduces the possibility of error.
``` c
widget *p;
/* ... */
p = MALLOC(widget);   /* OK */
if (p != NULL) {
  p->i = 0;           /* OK */
  p->d = 0.0;         /* OK */
}
```
Here, the entire allocation expression (to the right of the assignment operator) allocates storage for a `widget` and returns a `widget *`. If `p` were not a `widget *`, the compiler would complain about the assignment.
When allocating an array with `N` elements of type `T`, the appropriate type in the cast expression is still `T *`, but the argument to `malloc()` should be of the form `N * sizeof(T)`. Again, packaging this form as a macro, such as
``` c
#define MALLOC_ARRAY(number, type) \
    ((type *)malloc((number) * sizeof(type)))
```
reduces the chance of error in an allocation expression.
``` c
enum { N = 16 };
widget *p;
/* ... */
p = MALLOC_ARRAY(N, widget);    /* OK */
```
A small collection of macros can provide secure implementations for common uses for the standard memory allocation functions. The omission of a `REALLOC()` macro is intentional (see [EXP39-C. Do not access a variable through a pointer of an incompatible type](EXP39-C_%20Do%20not%20access%20a%20variable%20through%20a%20pointer%20of%20an%20incompatible%20type)).
``` c
/* Allocates a single object using malloc() */
#define MALLOC(type) ((type *)malloc(sizeof(type)))
/* Allocates an array of objects using malloc() */
#define MALLOC_ARRAY(number, type) \
    ((type *)malloc((number) * sizeof(type)))
/* 
 * Allocates a single object with a flexible
 * array member using malloc().
 */
#define MALLOC_FLEX(stype, number, etype) \
    ((stype *)malloc(sizeof(stype) \
    + (number) * sizeof(etype)))
/* Allocates an array of objects using calloc() */
#define CALLOC(number, type) \
    ((type *)calloc(number, sizeof(type)))
/* Reallocates an array of objects using realloc() */
#define REALLOC_ARRAY(pointer, number, type) \
    ((type *)realloc(pointer, (number) * sizeof(type)))
/* 
 * Reallocates a single object with a flexible
 * array member using realloc().
 */
#define REALLOC_FLEX(pointer, stype, number, etype) \
    ((stype *)realloc(pointer, sizeof(stype) \
    + (number) * sizeof(etype)))
```
The following is an example:
``` c
enum month { Jan, Feb, /* ... */ };
typedef enum month month;
typedef struct date date;
struct date {
  unsigned char dd;
  month mm;
  unsigned yy;
};
typedef struct string string;
struct string {
  size_t length;
  char text[];
};
date *d, *week, *fortnight;
string *name;
d = MALLOC(date);
week = MALLOC_ARRAY(7, date);
name = MALLOC_FLEX(string, 16, char);
fortnight = CALLOC(14, date);
```
If one or more of the operands to the multiplication operations used in many of these macro definitions can be influenced by untrusted data, these operands should be checked for overflow before the macro is invoked (see [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow)).
The use of type-generic function-like macros is an allowed exception (PRE00-C-EX4) to [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros).
## Exceptions
**MEM02-C-EX1:** Do not immediately cast the results of `malloc()` for code that will be compiled using a C90-conforming compiler because it is possible for the cast to hide a more critical defect (see [DCL31-C. Declare identifiers before using them](DCL31-C_%20Declare%20identifiers%20before%20using%20them) for a code example that uses `malloc()` without first declaring it).
## Risk Assessment
Failing to cast the result of a memory allocation function call into a pointer to the allocated type can result in inadvertent pointer conversions. Code that follows this recommendation will compile and execute equally well in C++.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM02-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | alloc-without-cast | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM02 | Fully implemented |
| Compass/ROSE |  |  | Can detect some violations of this recommendation when checking EXP36-C. Do not cast pointers into more strictly aligned pointer types |
| ECLAIR | 1.2 | CC2.MEM02 | Fully implemented |
| Helix QAC | 2024.4 | C0695 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM02-aCERT_C-MEM02-b | The result of the memory allocation function should be cast immediatelyThe result of the memory allocation function should be cast immediately into a pointer to the allocated type |
| PC-lint Plus | 1.4 | 908 | Assistance provided: reports implicit conversions from void* to another type |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM02-C | Checks for wrong allocated object size for cast (rule fully covered) |
| RuleChecker | 24.04 | alloc-without-cast | Partially checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM02-CPP. Immediately cast the result of a memory allocation function call into a pointer to the allocated type |

## Bibliography

|  |  |
| ----|----|
| [Summit 2005] | Question 7.7 Question 7.7b |

------------------------------------------------------------------------
[](../c/MEM01-C_%20Store%20a%20new%20value%20in%20pointers%20immediately%20after%20free__) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152468)
## Comments:

|  |
| ----|
| First, it seems to me that the correct recommendation should be: don't use implicit declarations for malloc, or any other function.; i.e., don't use malloc without #including stdlib.h.   For one thing, implicit function declarations are unsafe in general (e.g. if void* is not the same size as int), and for another thing they have been removed from the ANSI C99 standard.
Second, it seems to me that the risk assessment is wrong: "Explicitly casting the return value of malloc() eliminates the warning for the implicit declaration of malloc()."  This statement about compiler warnings is compiler-dependent; for example, gcc 4.1.2 gives a warning for uses of implicitly declared malloc() whether or not you explictly cast the return value. The basic point is that, if you use the implicit declaration of malloc(), you are inviting trouble via compiler- and architecture-dependent behavior no matter whether you cast the result or not.
Third, it seems like a bad habit to write C code that is gratuitously incompatible with C++ like this. Particularly since one platform's primary compiler (Microsoft Visual C++ ) is C++ only. 
                                        Posted by stevenj at Mar 14, 2008 15:46
                                     |
| Steven,
We are going to scrap this rule and replace it with something quite different. Stay tuned.  In fact, I'm going to turn this into a stub now so no one even bothers reading it again.
                                        Posted by rcs at Mar 14, 2008 20:34
                                     |
| Instead of using sizeof(type), use sizeof *p, like so:
widget *p;
...
p = malloc(sizeof *p);

Presto -- no type mismatch issues, no need for casting. ; You allocate the right amount of memory every time. 
I really, really, *really* do not like the idea of casting the return value of malloc().  Furthermore, for ADTs I'd recommend creating constructor- and destructor-like functions, and abstract away the calls to malloc() and free():
``` java
struct widget;
typedef struct widget widget_t;
struct gadget;
typedef struct gadget gadget_t;
widget_t *newWidget(void)
{
    widget_t *p = malloc(sizeof *p);
    if (p) 
        /* initialize members of *p as necessary */
    return p;
} 
gadget_t *newGadget(void)
{
    gadget_t *p = malloc(sizeof *p);
    if (p)
        /* initialize members of *p as necessary */
    return p;
}
void deleteWidget(widget_t **p)
{
     /* delete any subelements of *p */
     free(*p);
     *p = NULL;
}
void deleteGadget(gadget_t **p)
{
    /* delete any subelements of *p */
    free(*p);
    *p = NULL;
}
...
widget_t *p = newWidget();
gadget_t *g = newGadget();
if (p)
    /* do stuff with p */
if (g)
    /* do stuff with g */
...
deleteWidget(&p); 
deleteGadget(&g); 
```
I submit that this method is safer than using macros.  The tradeoff is that it's a bit more work, but I think it's worth the effort. 
So, my recommendations would be as follows:
-   Use the size of the *object* being allocated when calling malloc, instead of the size of the type;
-   Abstract away the calls to malloc() and free() by using creator and destroyer functions for ADTs. 
![](images/icons/contenttypes/comment_16.png) Posted by jbode at Mar 28, 2008 10:27
\| \|
It may be useful to note that the multiplication operation used in the MALLOC_ARRAY macro should be checked for overflow if the user can manipulate the number of elements in the array.
![](images/icons/contenttypes/comment_16.png) Posted by adahmad at Apr 13, 2008 10:15
\| \|
Um... reading it again, a month later.; If what I'm seeing is the "quite different" text, I vote for scrapping this one too.  I'm allergic to unnecessary casts, since they short-circuit type checking.
For that matter, I'd say both this and a number of other items fit better as a new category: neither rules nor recommendations, but something like "tricks and tips to avoid bugs and security problems."  As it stands, it's a bit to close to a more general rule "try to catch bugs in your programs".  Certainly it's a good idea to get the compiler to warn about bad mallocs, but just which method is best will vary with the style of the code among other things.  Often a = malloc(sizeof(\*a)) is fine.  Some times where it's not, whether or not a cast would increase or decrease code safety might depend on the distance from the declaration of the variable being assinged.  Etc.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 18, 2008 06:28
\| \|
I'm disturbed by the first 'compliant solution' which generates a compiler error. It's an odd sort compliance.
I sympathize with those who dislike casting return values from malloc et al. However, in my own code, I write in the C-compliant subset of C++, so the majority of my code can be compiled with a C or C++ compiler. To make memory allocation calls compile, I have to cast the return value, so I do, and I annotate it /\*=C++=\*/ to indicate why the cast is there. That doesn't make it foolproof - but does minimize the damage IMO.
I also use a CONST_CAST(type,value) macro with the C implementation ((type)(value)) and the C++ implementation const_cast(value). The C++ compilations validate that all the cast does is cast away const-ness. In C, it documents what is going on, though I could make mistakes.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Apr 19, 2008 23:54
\| \|
I wasn't comfortable with that either, so I moved the compliant solution bar down a bit.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 20, 2008 06:37
\| \|
Quoting myself, I'm allergic to *unnecessary* casts.; Since you want C++-compatible code, your "extra" casts are *necessary*. Typical example of a reasonable self-imposed constraint which in my view reduces the security of your code *considered as C code* a bit - unless you take measures against that, like you are doing.
But a rule based on that reason doesn't belong in this document, since your reason is not secure C code. Unless you feel getting a C++ compiler's help increases code security, but such a  recommendation is far out of scope for this document.  Might make a nice "trick to help make code secure" like I mentioned elsewhere though, if the document grows such a section
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 21, 2008 05:50
\| \|
This recommendation has an interesting history that is sort of apparent from the comments. Originally the recommendation was to not cast, which upset a lot of people. Then the recommendation was to cast, which also upset a lot of people. In practice, however, programmers are going to need to cast, or not cast, so it would be nice to provide some guidance.
The current recommendation was written by Dan Saks, who generally speaking, knows his stuff. When we discussed this change, the most compelling reason I heard was that casting in this situation in C was likely to uncover more errors than not-casting.
It just occurs to me now that "this situation" is for functions that return (void \*) because this will be implicitly converted to any pointer type in C, while casting actually limits the conversions that the compiler will warn on.
Perhaps this was not clear enough in the description, or perhaps this understanding would be aided by writing this other more general recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 21, 2008 06:10
\| \|
So don't recommend either. The point is to get the compiler's help in catching errors, but it can't help with everything and sometimes one must choose between which errors to get its help with. A recommendation either way takes sides in an issue with numerous conflicting interests and opinions. (I'd say the same of some of the other recommendations on this site, in particular related to warnings.)
Here are some issues a recommendation would need to take into account: Coding style, which errors your compiler(s) can help with, and therefore how varied range of platform you develop on, and how wide a user base you have and whether they submit patches and error reports, how hard to suppress warnings so that each new warning won't drown in all the other warnings, and thus on the size of the program. Same with your suggested wrapper macros - they are useful in themselves but could cost more than they gain since each wrapper function/macro is yet another thing to learn in order to understand the program.
Some things I think you can recommend - though I don't see how to claim compliance or non-compliance:
Be wary of casts and judicious in their use: See if the code can be written differently. Each cast you do use should be there for a considered reason. Since their use is in part a matter of coding style.
Expect a reader to want to know why each cast is there, so try to be consistent in their use: E.g. don't sometimes cast malloc and sometimes not. If you do cast malloc, the reader will then quickly notice the pattern and know that all these casts are there for the same reason. Same if you cast wide integer types to narrower ones (which some compilers warn about), though that could use a comment somewhere.; (Notice "try" in front of all this though - could have different styles for handling big and small data structures, or different styles in code originating from different sources, or whatever.)
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 21, 2008 16:17
\| \|
It sounds like you think this rule should be changed to "Understand issues with allocating memory", said issues being:
-   To cast or not to cast...pros and cons of each
-   Prevent overflow in size multiplications, such as args to calloc()
-   Check return value for NULL
-   Malloc wrappers: macros? inline functions? etc.
My first big C program eventually grew MALLOC macros very similar to what are currently proposed, the big advantage is it gave me a single location to decide memory allocation policy and keep it consistent. But my last big C program actually used constructor-like functions a la John Bode's comment. Probably because it followed an object-oriented design.
But I think I'd stick with the current rule. As Robert mentioned, a typecast in front of malloc is actually more restrictive than malloc w/o a typecast, since malloc returns void\* which can be cast to any other pointer type. Typecasts do give me the willies, and they are frowned upon elsewhere in the Secure Coding rules, but I'm fairly comfortable with casts in front of malloc.
To summarize, IMHO typecasting malloc's return value catches more compiler errors than not typecasting outweighs our discomfort with casts.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 21, 2008 16:48
\| \|
No, as I said previously I think the recommendation should be scrapped.; One reason is the accurate enough "IMHO" in your previous message: You know it conflicts with reasoned choices of others.  In particular it sabotages the "a = malloc(sizeof \*a)" trick.  Another is that "my" alternatives you suggest are really far wider in scope than just malloc, though it's true that I'd prefer recommendations of that kind over a number of items on this site.  E.g. not "check allocation return value for NULL" but "check function calls for error returns".
The cast alone doesn't catch bugs, nothing prevents you from writing (foo\*)malloc(sizeof(bar)).  Without the macro, the remaining point of this rule is in part that it's a *visual* cue to find a bug: In (foo\*)malloc(sizeof(foo)), the two foo's should be the same.  Replace one with "bar" and it looks suspicious, at least if the program is otherwise consistent about how it writes this.  "a = malloc(sizeof(\*a))" is a similar visual cue, I said a cast would sabotage it because that puts more distance and clutter between the two "a"s.  Yet another is the initialization "foo \*a = malloc(sizeof(foo))".
If i were to suggest a replacement for this particular rule, it'd be something on the line of "here are some tricks for making malloc(wrong size) bugs stand out".  (With the several variants discussed here.)  Again that's not something one can claim conformance with though, so it belongs more in a "tips and tricks" section.  Plus: Be consistent about it (again, as with several other issues), since that makes divergences stand out more to the reader.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 23, 2008 18:08
\| \|
;
I am rather concerned by the recommendation in this page. It is unsafe, dangerous, and worse it can result in undefined behavior!
This page seems to concern itself too much with logic errors rather than noncompliant code problems.  The main reason for NOT using a cast is it hides errors - worse it hides undefined behavior.
 A lot of a code still compiles under C89 mode. Probably more C89 code is written every day than any other version of the standard. Now, to understand the issue at hand we must understand C89 function declaration.
First, Let's see what the standard has to say about this
> C89; §3.3.2.2 Function calls:
>
> If the expression that precedes the parenthesized argument list in a function call consists solely of an identifier, and if no declaration is visible for this identifier, the identifier is implicitly declared exactly as if, in the innermost block containing the function call, the declaration:
>
> extern int identifier();  
>   
> appeared.

What's it saying? Well, if a function is called and the compiler has not seen an explicit prototype for it, the compiler is to assume it's a function that takes an unspecified number of arguments and returns an int.
So what does all of this have to do with casting malloc()?
Good question; it's rather common to forget to include \<stdlib.h\>. This is actually the root of the problem.
So what happens when we don't have an explicit prototype for malloc()?  
As the standard states, it's assumed to be:
extern int malloc();
And here is where your troubles began. Let's take a look at the standard again: 
> C89; §3.3.4 Cast operators  
>   
> Semantics  
>   
> Conversions that involve pointers (other than as permitted by the constraints of $3.3.16.1) shall be specified by means of an explicit cast; they have implementation-defined aspects: A pointer may be converted to an integral type. The size of integer required and the result are implementation-defined. **If the space provided is not long enough, the behavior is undefined**. An arbitrary integer may be converted to a pointer. The result is implementation-defined./37/ A pointer to an object or incomplete type may be converted to a pointer to a different object type or a different incomplete type. The resulting pointer might not be valid if it is improperly aligned for the type pointed to.

I am sure you can start to see where this is going. Let's consider the following program:
``` cpp
int main(void)
{
    char *foo = (char*)malloc(10);
    free(foo);
    return 0;
}
```
This program may seem right, right? WRONG! since we forgot to include \<stdlib.h\>, our program is seen by the compiler more like this:
``` cpp
extern int malloc();
extern int free();
int main(void)
{
    char *foo = (char*)malloc(10);
    free(foo);
    return 0;
}
```
Now, what's going on in this program. Firstly, the actual malloc() implementation is returning us a **void\***, in our program, the **compiler knows it as an int**. It is now allowed to handle it as an int for all practical purposes. This is a problem. If we are lucky and the space provided is long enough, the result is *implementation-defined*. If we are not so lucky and the space provided is not longer enough, the result **behavior is undefined**. A simple implementation where a void\* is 64-bits and your int is 32-bit **WILL invoke UB**.
Now we are getting to why the cast is \*HORRIBLE\*. The standard says that such conversion can only be done by the means of an explicit cast. **Your recommendation is masking this error by means of making illegal code legal**. If we left the cast out like you should, a conversion from \`int\` to \`char\*\` will generate some diagnostic message telling you there is a problem - since it's illegal in C. Hopefully such diagnostic message should give the programmer a hint that something is wrong.
I also saw a note about compiling the code as C++. How C++ handles things should be not be mixed with how C handles things, this is not a vegetable soup.
The recommendations on this page are very harmful to the unsuspected stranger.
It is my opinion that this recommendation does more harm than good. This recommendation does not solve any issue in any meaningful way.
Most C programmers would probably tell you that a better recommendation is to use sizeof \*ptr rather than sizeof (type) which would easily solve the problem shown in this page - it would not however solve the problem I've explained above which only NOT using a cast will help. 
``` cpp
widget *p;
/* ... */
p = malloc(sizeof *p);
```
No possible for memory issues, type issues, and bonus no need to cast - unhiding the correct problem. *<u>I just really really REALLY hate the fact you guys recommend casting malloc(), it's a total sin.</u>*
I think a middle ground that could be reached is to rename or change this page (I don't know how you guys organize those things) to a set of guidelines with explanations about the various issues involving malloc.
![](images/icons/contenttypes/comment_16.png) Posted by davidschor at Jun 17, 2013 14:28
\| \|
> A lot of a code still compiles under C89 mode. Probably more C89 code is written every day than any other version of the standard. Now, to understand the issue at hand we must understand C89 function declaration.

I'll accept this argument if you are referring to MS Visual C++, whose C compiler promises C89 compatibility, but not C99 or C11. (GCC can compile under C90 if requested, but it supports newer standards, too.)
I took your code sample (invoking malloc without including \<stdlib.h\>) and tried to reproduce your problem (of truncating the return value.)
On Windows, MSVC 2012 by default refuses to compile the program without 'malloc' being declared. But when I explicitly instructed it to use the C compiler, it compiled and ran the program. I couldn't get truncation, because my machine uses ILP32...ints and pointers are both 32 bits.
On my Linux machine (AMD64 running Ubuntu 12.04), GCC emits warnings, but will compile the code (in both C90 mode and the 'default' language setting). Since ints are 32 bits but pointers are 64 bits, truncation is theoretically possible. By default, the heap seems to start off in low memory, so no truncation occurs because the higher 32 bits are all 0. But if I allocate big chunks (0x10000000 bytes in my sample), then malloc returns pointers such as 0x7f22ce480010. Which do not get truncated.
So your warnings don't work on 32-bit Windows or 64-bit Linux (and I'd guess not on 32-bit Linux either ![](images/icons/emoticons/smile.svg) I suppose there may still exist a C compiler that truncates a malloc() return value if malloc() is not properly declared, and it not generate sufficient warnings (or its developers may ignore these warnings). But it's clearly not a problem in the most popular C90 compilers.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 17, 2013 16:29
\| \|
MSVC 11 compiling as 64-bit gives:
> 1\>test.c(3): warning C4013: 'malloc' undefined; assuming extern returning int
>
> 1\>test.c(4): warning C4013: 'free' undefined; assuming extern returning int

;
And it does indeed believe the returned value is 32-bits because it emits a cdqe to extend the double word into a quad word.  That instruction would end up blowing away anything in the high double word of RAX, and with ASLR being on by default for Visual Studio, this could cause problems.  But, at the same time, you are warned about the behavior.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 17, 2013 17:23
\| \|
David, Clearly you are missing the whole point of me quoting the standard. It's not about what some random implementation does, it's about what the C89 standard says should happen. If the sizes are not big enough and your program works, you got lucky, it's not any less undefined. Note that the only C standard MSVC supports is C89, C89 is also the default mode in GCC, freescale, and other compilers. It also worth mentioning that since this is UB, just because it happens to do what you wanted today doesn't mean the behavior for the next release will not change - they are certainly allowed to. Heck, they can change it tomorrow morning with a patch update! it's undefined!
![](images/icons/contenttypes/comment_16.png) Posted by davidschor at Jun 17, 2013 18:31
\| \|
Aaron, the compiler is not required to issue any such warnings - your compiler happens to be nice. On the other hand, if the cast (which is recommended;here!) is NOT used, a conversion from an 'int' to a pointer requires a cast making the code illegal - by virtue forcing the compiler to throw a diagnostic message.
![](images/icons/contenttypes/comment_16.png) Posted by davidschor at Jun 17, 2013 18:35
\| \|
David,
I guess I could have deleted this rule years ago as "controversial" but it sure generates alot of interesting discussion.
We initially developed this coding standard for C99, and then published the book for this version of the standard.; We are now updating this standard for C11.
We will make notes occasionally when our recommendations might be different for an older version of the standard.  I think that is where Svoboda and Aaron were going.  Although MSVC doesn't support C99, it is an important platform so we need to pay attention to it.
The erroneous code you wrote violates:
[DCL31-C. Declare identifiers before using them](https://www.securecoding.cert.org/confluence/display/seccode/DCL31-C.+Declare+identifiers+before+using+them)
This is actually a rule and not a recommendation like this one (MEM02-C).   When we give noncompliant examples, we assume they are free of other problems that are prevented by other rules.
I'm thinking there may be some value in a historical note for this rule, discussing some of the problems with C89/90.  I don't think we should reverse the guidance (again).  The other possibility is to scrap this as controversial and write a paper titled "malloc, the casting controversy".
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 17, 2013 22:24
\| \|
We definitely should NOT scrap this recommendation, as:
-   It does generate interesting discussion (isn't that the definition of 'controversial'?).
-   People look to us for advice on how to malloc, and questions like whether or not to cast.
We can always add an exception for platforms that follow Schor's scenario. I'm not convinced that MSVC does, and we should settle that question first. Nonetheless, it does look like a plausible scenario for C90 compilers, and WG14 is not fixing it for non-C99-compliant platforms (I presume they fixed it in C99).
If platforms that follow Schor's scenario are indeed prominent (and I'm still not convinced), we should change this guideline to an "understand how malloc behaves" guideline, which would say "cast if you're using these platforms, don't cast if you're using these other platforms".
Schor's rationale for not casting is to prevent errors in noncompliant code (eg using malloc w/o declaring it),. But our rational for casting is also to prevent errors in noncompliant code (eg mixing up pointers of differing types), which is just as weak, but IMO more likely.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 18, 2013 09:33
\| \|
Much earlier, John Bode suggested the following compliant solution:
`widget *p;`
`...`
`p = malloc(sizeof *p);`
as well as the use of Abstract Data Types (ADT).; The ADT discussion is probably orthogonal to this guideline, but the approach of taking the sizeof \*p seems to be a reasonable compliant solution that would seem to be noncompliant given the title of this rule.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 20, 2013 10:02
\| \|
That is a good solution, but I would be afraid of people forgetting the '\*', and therefore violating;[ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array](ARR01-C_%20Do%20not%20apply%20the%20sizeof%20operator%20to%20a%20pointer%20when%20taking%20the%20size%20of%20an%20array).
The truth is that we are splitting fine hairs. Our arguments of what to use are based on compilers that don't produce warnings (a quality-of-implementation issue), compilers that don't comply with C99, and the various ways people can write programs.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 20, 2013 15:11
\| \|
Yes, and because we are splitting hairs, we probably don't want to suggest to an analyzer that we consider the above code to be noncompliant and have them flagging lines without casts.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 21, 2013 09:22
\| \|
I have added an exception because the above code does yield an access violation when compiling 64-bit applications on an LP64 or LLP64 platform.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 28, 2013 10:30
\| \|
I see no warning when compiled with GCC on Fedora (compiler, linker or otherwise). Note that I can reproduce such truncation bugs almost always. Over the past month since I originally posted a comment I've seen dozens of errors popping up on stackoverflow, so this is not a rare case. This is true for GCC on Mac OS X it seems - just this morning I knew immediately this is the problem when the following question was posted: [http://stackoverflow.com/questions/18099224/pointer-truncation-with-realloc-on-os-x-in-jni-library](http://stackoverflow.com/questions/18099224/pointer-truncation-with-realloc-on-os-x-in-jni-library?noredirect=1) crash results from pointer truncation due to missing prototype.
![](images/icons/contenttypes/comment_16.png) Posted by davidschor at Aug 07, 2013 17:09
\| \|
David:
The **MEM02-EX1** exception specifically targets platforms that don't adhere to C99 or C11...this includes MSVC.
C99-compliant platforms must, according to the standard:
> ...produce at least one diagnostic message ... if a preprocessing translation unit or translation unit contains a violation of any  
> syntax rule or constraint, ...

C90 permitted implicit function prototypes for functions that were used without being declared...this is what gave you grief (as well as the case you cited from Stack Overflow). C99 removed implicit function prototypes. Therefore a C99-compliant platform must issue at least one warning if your code uses an undeclared function like malloc(). (Beyond that, it may proceed to compile your program, abort, or do anything else it wants.) Finally, you should get this diagnostic whether or not you cast the return value of malloc().
I don't know which version of GCC you are using, or what arguments you are giving it. On my platform (gcc 4.6.3, Ubuntu 12.04) when I give it the code sample in **MEM02-EX1**, I always get a warning about malloc being undeclared, and GCC always proceeds to compile the program (unless I also use `--pedantic-errors` to turn warnings into errors. The program then runs with the bad behavior you cite. If GCC is not giving you **any** warnings, then I would stipulate that you are not using it in a standards-compliant way. I can compile the program without any warnings by supplying `-w` to GCC. Which works, but breaks standards-compliance.
We do have this recommendation: [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels) Also our [Scope](Scope) page discusses what standards we support (C99 and C11). I don't see a rule or rec specifically stating to use a standards-compliant compiler...perhaps we need one?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 09, 2013 16:27
\| \|
I have transferred the code example in this rule's exception to;[DCL31-C. Declare identifiers before using them](DCL31-C_%20Declare%20identifiers%20before%20using%20them), and linked to it from the exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 12, 2013 10:57
\| \|
I'm having a few issues with this recommendation.; The title of this recommendation implies that our recommendation is to cast the result of malloc to a pointer of the allocated type. If this is the case then in the 3rd box of our non-complant code example where
\*widget p;
p = (gadget \*)malloc(sizeof(gadget));
is valid in the context of this recommendation because the result of mallocing space for a gadget is immediately cast into a pointer to a gadget. This can cause UB because it violates [EXP39-C. Do not access a variable through a pointer of an incompatible type](EXP39-C_%20Do%20not%20access%20a%20variable%20through%20a%20pointer%20of%20an%20incompatible%20type) and [MEM35-C. Allocate sufficient memory for an object](MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object).
I view the CS of
widget \*p;
...
p = malloc(size of \*p);
as a good compliant solution so I don't think this recommendation should require that we immediately cast the result of malloc into a pointer of the right type.
![](images/icons/contenttypes/comment_16.png) Posted by eaevans at Dec 06, 2013 15:42
\| \|
You are correct that the code is compliant in the context of this recommendation, and in violation of other rules. However, the recommendation to immediately cast the results is still an accurate one. Just because a recommendation says to perform an action does not mean the action automatically is valid in all guidelines. For instance:
char \*ptr = (char \*)malloc(0);
is still valid for this recommendation, but invalid because of other guidelines.
That being said, the normative text doesn't really go into \*why\* this is a valid recommendation, which would be nice.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Dec 09, 2013 12:40
\| \|
You are correct...the explicit typecast does not change the fact that the NCCE has undefined behavior. But it does help the compiler detect the fault.
This is a very controversial rec, and just recently got demoted from a rule. It's worthwhile to study the comments in this rec to see how it came to be.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 09, 2013 16:54
\| \|
Alternatively, use this macro in order to automatically allocate values of correct type, without having to use `sizeof`.
``` cpp
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#define alloc(lvalue, size) ((lvalue) = malloc(sizeof *(lvalue) * (size)))
int main(void) {
    const int test[] = {1, 2};
    int *copy;
    alloc(copy, 2);
    memcpy(copy, test, sizeof test);
    copy[0] = 3;
    printf("%d %d %d %d\n", test[0], test[1], copy[0], copy[1]);
    free(copy);
    return 0;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by glitchmr at Dec 10, 2013 03:08
\| \|
Do we need an exception for strings? Casting a malloc return value to;`char*` seems useless (as char\* is also convertable to any other type).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 16, 2013 16:32
\|
