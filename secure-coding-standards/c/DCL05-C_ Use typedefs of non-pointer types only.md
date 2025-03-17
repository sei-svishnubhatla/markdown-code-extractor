Using type definitions (`typedef`) can often improve code readability. However, type definitions to pointer types can make it more difficult to write `const`-correct code because the `const` qualifier will be applied to the pointer type, not to the underlying declared type.
## Noncompliant Code Example
The following type definition improves readability at the expense of introducing a `const`-correctness issue. In this example, the `const` qualifier applies to the `typedef` instead of to the underlying object type. Consequently, `func` does not take a pointer to a `const struct obj` but instead takes a `const` pointer to a `struct obj`.
``` c
struct obj {
  int i;
  float f;
};
typedef struct obj *ObjectPtr;
void func(const ObjectPtr o) {
  /* Can actually modify o's contents, against expectations */
}
```
## Compliant Solution
This compliant solution makes use of type definitions but does not declare a pointer type and so cannot be used in a `const`-incorrect manner:
``` c
struct obj {
  int i;
  float f;
};
typedef struct obj Object;
void func(const Object *o) {
  /* Cannot modify o's contents */
}
```
## Noncompliant Code Example (Windows)
The Win32 SDK headers make use of type definitions for most of the types involved in Win32 APIs, but this noncompliant code example demonstrates a `const`-correctness bug:
``` c
#include <Windows.h>
/* typedef char *LPSTR; */
void func(const LPSTR str) {
  /* Can mutate str's contents, against expectations */
}
```
## Compliant Solution (Windows)
This compliant solution demonstrates a common naming convention found in the Win32 APIs, using the proper `const` type:
``` c
#include <Windows.h>
/* typedef const char *LPCSTR; */
void func(LPCSTR str) {
  /* Cannot modify str's contents */
}
```
## Noncompliant Code Example (Windows) 
Note that many structures in the Win32 API are declared with pointer type definitions but not pointer-to-`const` type definitions (`LPPOINT`, `LPSIZE`, and others). In these cases, it is suggested that you create your own type definition from the base structure type.
``` c
#include <Windows.h>
/*
  typedef struct tagPOINT {
    long x, y;
  } POINT, *LPPOINT;
*/
void func(const LPPOINT pt) {
  /* Can modify pt's contents, against expectations */
}
```
## Compliant Solution (Windows)
``` c
#include <Windows.h>
/*
  typedef struct tagPOINT {
    long x, y;
  } POINT, *LPPOINT;
*/
typedef const POINT *LPCPOINT;
void func(LPCPOINT pt) {
  /* Cannot modify pt's contents */
}
```
## Noncompliant Code Example
In this noncompliant code example, the declaration of the `signal()` function is difficult to read and comprehend:
``` c
void (*signal(int, void (*)(int)))(int);
```
## Compliant Solution
This compliant solution makes use of type definitions to specify the same type as in the noncompliant code example:
``` c
typedef void SighandlerType(int signum);
extern SighandlerType *signal(
  int signum,
  SighandlerType *handler
);
```
## Exceptions
Function pointer types are an exception to this recommendation. 
## Risk Assessment
Code readability is important for discovering and eliminating [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL05-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-typedef | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL05 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.PIT | Pointer type inside typedef |
| Compass/ROSE |  |  |  |
| Helix QAC | 2024.4 | C5004 |  |
| LDRA tool suite | 9.7.1 | 299 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL05-a | Declare a type of parameter as typedef to pointer to const if the pointer is not used to modify the addressed object |
| RuleChecker | 24.04 | pointer-typedef | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL05-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | DCL12-C. Implement abstract data types using opaque types |
| SEI CERT C++ Coding Standard | VOID DCL05-CPP. Use typedefs to improve code readability |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152402) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152130)
## Comments:

|  |
| ----|
| There should be a rule against using identifiers for parameters in prototypes, typecasts, etc.; The problem is that they may be macro-replaced or may match typedef names, resulting in unintended consequences, not all of them producing diagnostics.  I've found that commented identifiers work pretty well:
extern bool ZeroBuffer( byte * /*buffer*/, size_t /*length*/ );

![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 12:07
\| \|
This sounds more like a style guideline rather than a secure coding rule. Can you give an example of code where identifiers in prototypes produces unexpected behavior? AFAIK no compiler does any checking of prototype identifiers.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 15, 2008 13:08
\| \|
Just a thought, would a better check for a "too complicated" type be one with a certain number of parentheses?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 21, 2008 16:08
\| \|
if you define 'parentheses' to include 'array brackets', then yes, I would agree.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 21, 2008 16:30
\| \|
This declaration from [EXP37-C. Call functions with the arguments intended by the API](/confluence/pages/createpage.action?spaceKey=c&title=EXP37-C.+Call+functions+with+the+arguments+intended+by+the+API) has been deemed simple enough to not warrant a typedef:
``` java
char *(*fp) ();
```
On the other tentacle, the signal typedef in the NCCE & CCE do need a typedef. So what algo do we use to flag the signal typedef, but leave the EXP37 typedef?
Alex and I have come up with a suitable algo, which is now described in the ROSE paragraph to handle these.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 23, 2008 11:11
\| \|
now in code, and works well
Incidentally, it's interesting to note that `signal` in the above examples is treated as a SgFunctionDeclaration not a SgInitialiazedName like all other variables :/
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 23, 2008 13:50
\| \|
Minor point wrt the risk assessment - the description doesn't point out the potential consequences of not addressing this particular vulnerability (for example, hard to maintain error-prone code).
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Mar 08, 2010 00:29
\| \|
For the compliant solution, I wonder if a slightly more readable (and elegant IMHO) way of using the typdef would be:
typedef void SighandlerType(int signum); \<-- typedef just for the function signature
extern SighandlerType signal( int signum,  
SighandlerType \*handler \<-- made explicit the fact that 'handler' is a pointer  
);
Also, this is consistent with a change made to the compliant solution section of DCL-12-C, motivated  
by a comment against using typedefs for pointers.
![](images/icons/contenttypes/comment_16.png) Posted by gerivera at Dec 17, 2010 15:25
\| \|
On a different issue, I think that the use of typedefs for pointers and for structs should be explicitly discouraged, as it does not really
improve readability, and instead may have some practical disadvantages.
Saying "char \*p" is not less readable than "char_ptr_t p" and saying "struct foo \*foo_p" is not less readable than "foo_t \* foo_p".
A disadvantage of using typedefs for pointers was mentioned by Shay Green in the comments section of DCL-12-C:
"Using typedef to define a pointer type makes const correctness more difficult to achieve, less obvious, or inconsistent."
A disadvantage of using typdefs for structs is that finding the full declaration of a struct with tools such as cscope or
ctags requires two queries instead of one, which can get annoying after while. Another disadvantage, specifically
for opaque types implemented with incomplete struct declarations (as described in DCL-12-C), is that it causes
unnecessary nested includes. For example, the header file that contains the typedef declaration for an incomplete
struct (opaque type) needs to be included in all header files that reference the opaque type, even if they
just need it to declare pointers to the opaque type. This type of nested includes is unnecessary, as the header file
referencing the opaque type can just have an incomplete struct declaration, instead of having to do a nested include.
In large code bases, avoiding unnecessary nested includes, in frequently included header files, can help reduce build
times. Also, porting or reusing header files can be easier, if unnecessary header file dependencies are avoided.
I think that, in practice, typedefs are useful mostly for numeric data types and function pointers.
![](images/icons/contenttypes/comment_16.png) Posted by gerivera at Dec 17, 2010 18:03
\| \|
overall, this is much improved.; some minor points.  at least after the first noncompliant example, i would be more explicit about what the const correctness issue is.
would it make sense to show how the windows typedefs are defined?
i would include comments in all the function bodies explaining what the function is doing, or minimally /\* . . . \*/
I used to think the word "utilize" should never be use, but Fred Long and I discovered it means something slightly different than "use".  It basically means to use for a purpose for which it was not intended.  In this case, I think you should just say "use".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 13, 2013 17:01
\| \|
Thanks!; I believe I've addressed most of these issues.  I left out the part about showing how the Windows typedefs are defined.  Still thinking about how best to do that (Windows tends to string multiple typedefs together, and I'm not certain how many lines of code we want to show to demonstrate that).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 13, 2013 18:05
\| \|
maybe you can reduce it to a single line using the standard types.; i think we're going for pedagogy here over realism.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 17, 2013 09:49
\| \|
I added the definitions as part of a comment after the #include, so we should be set.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 17, 2013 10:39
\| \|
The declaration `func(``const` `ObjectPtr o)` is by definition equivalent to the declaration `func``(``ObjectPtr o)`.; If the developer knows that, your concern is void, otherwise she is an impostor and this material does not apply to her.  Therefore this entry is useless and harmful (as it gratuitously limits the developer’s toolbox ) and should be removed.
![](images/icons/contenttypes/comment_16.png) Posted by yecril at Aug 08, 2013 14:28
\| \|
I think I agree...at the very least the 1st NCCE needs to include this info. Using ObjectPtr or (struct obj\* const) is useless as a function argument, since the function can't change the pointer in the calling context anyway.
The NCCE is otherwise good. A 'const struct obj\* const' type is worthwhile passing as a function argument; having the function promise not to change the pointed-to data is worthwhile. The NCCE does look like it promises that, but actually doesn't.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 09, 2013 14:21
\|
