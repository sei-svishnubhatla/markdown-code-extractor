The C11 Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] introduced a new term: *temporary lifetime*. This term still remains in the C23 Standard. Modifying an object with temporary lifetime is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). According to subclause 6.2.4, paragraph 8 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]
> A non-lvalue expression with structure or union type, where the structure or union contains a member with array type (including, recursively, members of all contained structures and unions) refers to an object with automatic storage duration and temporary lifetime. Its lifetime begins when the expression is evaluated and its initial value is the value of the expression. Its lifetime ends when the evaluation of the containing full expression ends. Any attempt to modify an object with temporary lifetime results in undefined behavior.

This definition differs from the C99 Standard (which defines modifying the result of a function call or accessing it after the next sequence point as undefined behavior) because a temporary object's lifetime ends when the evaluation containing the full expression or full declarator ends, so the result of a function call can be accessed. This extension to the lifetime of a temporary also removes a quiet change to C90 and improves compatibility with C++. 
C functions may not return arrays; however, functions can return a pointer to an array or a  `struct` or union that contains arrays. Consequently, in any version of C, if a function call returns by value a `struct` or `union` containing an array, do not modify those arrays within the expression containing the function call. In C99 and older, do not access an array returned by a function after the next sequence point or after the evaluation of the containing full expression or full declarator ends.
## Noncompliant Code Example
This noncompliant code example [conforms](BB.-Definitions_87152273.html#BB.Definitions-conformingprogram) to the C11 Standard; however, it fails to conform to C99. If compiled with a C99-conforming implementation, this code has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because the sequence point preceding the call to `printf()` comes between the call and the access by `printf()` of the string in the returned object.
``` c
#include <stdio.h>
struct X { char a[8]; };
struct X salutation(void) {
  struct X result = { "Hello" };
  return result;
}
struct X addressee(void) {
  struct X result = { "world" };
  return result;
}
int main(void) {
  printf("%s, %s!\n", salutation().a, addressee().a);
  return 0;
}
```
## Compliant Solution (C11 and newer)
This compliant solution checks `__STDC_VERSION__` to ensure that a pre-C11 compiler will fail to compile the code, rather than invoking undefined behavior.
``` c
#include <stdio.h>
#if __STDC_VERSION__ < 201112L
#error This code requires a compiler supporting the C11 standard or newer
#endif
struct X { char a[8]; };
struct X salutation(void) {
  struct X result = { "Hello" };
  return result;
}
struct X addressee(void) {
  struct X result = { "world" };
  return result;
}
int main(void) {
  printf("%s, %s!\n", salutation().a, addressee().a);
  return 0;
}
```
## Compliant Solution
This compliant solution stores the structures returned by the call to `addressee()` before calling the `printf()` function. Consequently, this program conforms to both C99 and C11.
``` c
#include <stdio.h>
struct X { char a[8]; };
struct X salutation(void) {
  struct X result = { "Hello" };
  return result;
}
struct X addressee(void) {
  struct X result = { "world" };
  return result;
}
int main(void) {
  struct X my_salutation = salutation();
  struct X my_addressee = addressee();
  printf("%s, %s!\n", my_salutation.a, my_addressee.a);
  return 0;
}
```
## Noncompliant Code Example
This noncompliant code example attempts to retrieve an array and increment the array's first value. The array is part of a `struct` that is returned by a function call. Consequently, the array has temporary lifetime, and modifying the array is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in both C99 and C11.
``` c
#include <stdio.h>
struct X { int a[6]; };
struct X addressee(void) {
  struct X result = { { 1, 2, 3, 4, 5, 6 } };
  return result;
}
int main(void) {
  printf("%x", ++(addressee().a[0]));
  return 0;
}
```
## Compliant Solution
This compliant solution stores the structure returned by the call to `addressee()` as `my_x` before calling the `printf()` function. When the array is modified, its lifetime is no longer temporary but matches the lifetime of the block in `main()`.
``` c
#include <stdio.h>
struct X { int a[6]; };
struct X addressee(void) {
  struct X result = { { 1, 2, 3, 4, 5, 6 } };
  return result;
}
int main(void) {
  struct X my_x = addressee();
  printf("%x", ++(my_x.a[0]));
  return 0;
}
```
## Noncompliant Code Example
This noncompliant code example attempts to save a pointer to an array that is part of a `struct` that is returned by a function call. Consequently, the array has temporary lifetime, and using the pointer to it outside of the full expression is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in both C99 and C11.
``` c
#include <stdio.h>
struct X { int a[6]; };
struct X addressee(void) {
  struct X result = { { 1, 2, 3, 4, 5, 6 } };
  return result;
}
int main(void) {
  int *my_a = addressee().a;
  printf("%x", my_a[0]);
  return 0;
}
```
## Compliant Solution
This compliant solution stores the structure returned by the call to `addressee()` as `my_x` before saving a pointer to its array member. When the pointer is used, its lifetime is no longer temporary but matches the lifetime of the block in `main()`.
``` c
#include <stdio.h>
struct X { int a[6]; };
struct X addressee(void) {
  struct X result = { { 1, 2, 3, 4, 5, 6 } };
  return result;
}
int main(void) {
  struct X my_x = addressee();
  int *my_a = my_x.a;
  printf("%x", my_a[0]);
  return 0;
}
```
## Risk Assessment
Attempting to modify an array or access it after its lifetime expires may result in erroneous program behavior.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP35-C | Low | Probable | Medium |  P4  |  L3  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | temporary-object-modification | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP35 |  |
| CodeSonar | 8.3p0 | LANG.CAST.ARRAY.TEMP | Array to Pointer Conversion on Temporary Object |
| Cppcheck Premium | 24.11.0 | premium-cert-exp35-c |  |
| Helix QAC | 2024.4 | C0450, C0455, C0459, C0464, C0465C++3807, C++3808 | Fully implemented |
| LDRA tool suite | 9.7.1 | 642 S, 42 D, 77 D | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP35-a | Do not modify objects with temporary lifetime |
| Polyspace Bug Finder | R2024a | CERT-C: Rule EXP35-C | Checks for accesses on objects with temporary lifetime (rule fully covered) |
| Splint | 3.1.1 |  |  |
| RuleChecker | 24.04 | temporary-object-modification | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP35-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | Dangling References to Stack Frames [DCM] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Side-effects and Order of Evaluation [SAM] | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.2.4, "Storage Durations of Objects" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152449) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152059)
## Comments:

|  |
| ----|
| I at least agree with Hal. These examples in juxtaposition do nothing to help me understand the problem being solved.
I think the issue is made unnecessarily complex through the use of the compiler internal terminology "sequence point." Programmers do not know what they are, much less where they occur. If we are attempting to teach them something about them, then annotating the examples with some sort of sequence point clues would help. If not, the use of the term obscures the point being made. I'd stick with pure programmer-aware terminologies.
                                        Posted by wlf@cert.org at May 25, 2007 12:15
                                     |
| The statement "This program has undefined behavior because there is a sequence point before printf() is called, and printf() accesses the result of the call to addressee()." is not an adequate explanation of the failure here. If you replace "address().a" with "address()", the explanation would be the same, but the code would be correct. It's the ".a" that's wrong and the explanation should reflect that. There must be a sequence point between address() and address().a that's the issue.
                                        Posted by wlf@cert.org at Jul 10, 2007 11:31
                                     |
| The term "sequence point" is not "compiler internal terminology." It is the terminology used by the C standard. AFAIK, there isn't any other correct terminology. Sequence points are basically the places where order of execution is specified. As a programmer, you do need to know about them, although not necessarily what  they they are called. Eg, if you say f( x );g( y );, even as a programmer, you generally want to know that f will be called before g is called.
Anyways, if you were reading the rules in order (or even the titles), you would have come across [EXP30-C. Do not depend on order of evaluation between sequence points] first, which does explain what a sequence point is. If you know of better terminology, would you mind suggesting it?
                                        Posted by aij at Aug 31, 2007 12:26
                                     |
| It's not  the ".a" that is wrong. It's the fact that the printf() function will be trying to access the value returned by address() in the previous sequence point.
Perhaps you are confused because they are using a function call as a sequence point. Would it be more clear if they instead used semicolon?
char *s = addressee().a;
/* the next line accesses the return value from the previous sequence point */
char c = s[3]; 

I think this is a worse example, because it also violates \[[DCL30-C. Do not refer to an object outside of its lifetime](/confluence/pages/createpage.action?spaceKey=c&title=DCL30-C.+Do+not+refer+to+an+object+outside+of+its+lifetime)\]
![](images/icons/contenttypes/comment_16.png) Posted by aij at Aug 31, 2007 12:42
\| \|
When I compile this code with GCC version4.1 and the -Wall switch, I do not get a warning about this bug.; I only get a warning that the format string expects type 'char \*' but the argument has type 'char\[6\]'
![](images/icons/contenttypes/comment_16.png) Posted by adahmad at Apr 12, 2008 13:10
\| \|
I think this rule needs to be rewritten / expanded. See <http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1285.htm>
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 14, 2008 09:52
\| \|
printf does not accesses the return value from addressee(). main() does that, and passes its member 'a' to printf().
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 17, 2008 18:59
\| \|
I can reproduce this on gcc3.4.4
then again... this could just be a case of a less than informative warning, perhaps we should explain a bit more exactly what is going on?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 16, 2008 16:48
\| \|
The code examples don't support the rule. Not sure why the NCCE segfaults, but I suspect it is due to the array, not to anything regarding sequence points.
First off, the examples are evidence of **something**. And I also get the silly compiler warning from gcc that Arbob and Alex report on the NCCE:
``` java
foo.c:11: warning: format '%s' expects type 'char *', but argument 2 has type 'char[6]'
```
This is, of course, specific to `printf()` and its ilk. In fact gcc, is very sticky about passing the 'temporary array' `addressee().a` to functions...usually it returns an error and rejects typecasting events.
At first I thought the problem is that arrays are glorified pointers and the NCCE violates [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations). But as a counterexample, the following code compiles w/o warning and works properly:
``` java
#include <stdio.h>
struct X { char a[6]; };
struct X addressee() {
  struct X result = { "world" };
  return result;
}
int main(void) {
  printf("Hello, %s!\n", &(addressee().a[0]));
  return 0;
}
```
Also, if `struct X` uses something besides arrays, the code also compiles cleanly and works.
``` java
#include <stdio.h>
struct X { char a; };
struct X addressee() {
  struct X result = { '!' };
  return result;
}
int main(void) {
  printf("Hello, World%c\n", addressee().a);
  return 0;
}
```
So I think the NCCE illustrates something bad about arrays, but don't know what. No rule in the Arrays section seems to apply.
On a side note, the NCCE may be bad C, but it seems to be valid C+. It compiles cleanly under G+ and runs correctly. I suspect C++ treats temporary values differently than C. For instance, in C++ a function can return a reference to a variable, the result being that you can use a function call as an lvalue. So I suspect C++ is more thorough in its treatment of temporary values (or of arrays, whichever this is about.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 23, 2008 12:12
\| \|
C++ has different semantics. In C++ temporaries (like return values) are preserved until the end of evaluation of the containing full expression or full declarator.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 12, 2008 09:15
\| \|
OK, having looked at this example more, I am convinced that the problem is better formulated in terms of arrays. C99 section 6.9.1, paragraph 3 explicitly states that functions may not return arrays. The NCCE violates the spirit of this, but not the letter, as its function returns an array wrapped inside a struct.
The NCCE behaves the same even if the array being returned lives on the heap, not the stack (eg created with malloc()). Also, I can't recreate the problem without arrays; eg a struct containing a struct works perfectly.
The webpage "Extending the Lifetime of Temporary Objects" provides the reference for this rule, claiming a sequence point after the addressee() function and printf() is responisible for the behavior.
But the NCCE is not bad because of sequence points, and I think the C99 standard is being misinterpreted here. Obviously a function's return value must be leglitimate across at least one sequence point, otherwise you couldn't do `foo( bar())`, since there is a sequence point between the bar() call and the foo() call. There is no sequence point in referring to the array within the struct; the only sequence points (by definition) are the call to addressee() and the call to printf().
I haven't found a definitive reference forbidding the NCCE.
As for gcc, it does not seem to properly convert the array to a pointer in the NCCE, which is why the NCCE crashes, but works if we wrap the array in a &array\[0\] expression, as in my previous comment.
One telling clue about this is that gcc won't compile the program if you replace 'printf' with some other function taking a char\* or char array. I get the impression they were trying to prevent some array casts at the compiler level, and doing other array casts right, and the NCCE was just a loophole they never changed (prob because its claimed to violate sequence points.) As noted in the rule, this is not a problem with MSVC.
So this may just be a gcc bug. If it merits a rule, it would be "Don't pass as a function argument an array that is a member of a struct returned by another function.
I guess my big question is: Can anyone cite a reference (that isn't about sequence points) saying why the NCCE is bad?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 12, 2008 15:33
\| \|
Clark Nelson sez:
\>\> Perhaps I am cofused over the meaning of this paragraph, from \>\> C99 Section 6.5.2.2 says [1999](#):  
\>\>  
\>\> If an attempt is made to modify the result of a function call or  
\>\> to access it after the next sequence point, the behavior is  
\>\> undefined.  
\>\>  
\>\> It would seem to me that this paragraph renders a simple cascading  
\>\> function call like foo( bar()) illegal, because there is a sequence  
\>\> point before the call to foo() and after the call to bar(), and that  
\>\> sequence point 'kills' the return value of bar().  
\>  
\> You have to remember that in C, all arguments are passed by value, so what foo receives is not the object returned by bar, but a copy thereof. So it's not the same object, so there's no undefined behavior.  
\>  
\>\> So why is foo( bar()) legal, but foo( bar().a) illegal? (assuming  
\>\> bar() returns a struct with an array member 'a')?  
\>  
\> Because (bar().a) implicitly takes the address of an object returned by bar, so if foo dereferences that pointer, it is accessing the actual object returned by bar after a sequence point.  
\>  
\>\> Rob pointed me to your proposal to amend this paragraph in the C  
\>\> standard:  
\>\>  
\>\> <http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1285.htm>  
\>\>  
\>\> AFAICT this would kill our rule, as the non-compliant code example  
\>\> would become perfectly legal C (it is already legal C++). But, as you  
\>\> know, your proposal is not part of the C standard yet, so how do we  
\>\> cope in the meantime?  
\>  
\> That's a judgment call. Theoretically, even after a new C standard comes out, there will still be compilers around that won't yet conform to it. So from some perspective, it will still be reasonable to suggest to programmers that they avoid references to rvalue arrays. On the other hand, no one has yet found a C compiler that actually generates code that doesn't satisfy the C++ rule, which suggests that references to rvalue arrays are practically pretty safe.  
\>  
\> Actually, I take it back: in pre-C99 mode, GCC does something entirely unexpected with rvalue arrays. At least on IA-32, if an rvalue array expression is used as an argument to a function, the whole array is passed by value, i.e. copied into the argument block of the called function. No matter what the standard says, it might be reasonable to warn people away from that behavior.  
\>  
\> Clark
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 15, 2008 10:05
\| \|
After studying Clark's responses above to my questions, I tested the NCCE again. The code still coredumps on gcc version 4.2.3 (on an AMD64-bit Ubuntu box), but it works perfectly if I add a `--std=c99` flag to the compile command, which instructs GCC to adhere to C99 as much as possible.
Clark's last two paragraphs sum up the situation pretty effectively. I'll just add:
-   As mentioned above, the problem is with array rvalues, so the rule should focus on arrays.
-   Most compilers already 'do the right thing' and compile the NCCE so that it runs correctly. So does GCC4.2, but only with --std=c99.
-   It's our call if we wish to maintain this rule or drop it. It will be obsolete someday, but isn't yet.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 15, 2008 10:34
\| \|
At some point, we need to look into the Automated Detection section; the NCCEs all compile cleanly with gcc 4.8.1 in -Wall -Weverything -pedantic mode.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 23, 2013 16:31
\| \|
Clang also does not catch instances of this rule. I've removed the GCC row from the table; I don't believe it catches this rule currently (5.2.0).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 27, 2015 11:39
\| \|
I don't like rules that basically say "Don't do this because it's not safe in an older standard, even though it is in a newer one". What's the point of adopting newer standards if you're still going to bind yourself to the old one?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 14:21
\| \|
The first edition of the SEI C Coding Standard was published in 2008, and it supported the C99 standard, with a lot of support for C90 as well. While it is good to encourage people to use the latest C standard, that is often not a choice they can make. It is foolish for us to throw away details that address an old edition of the standard, as long as people still write code that must conform to it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 31, 2020 12:48
\| \|
I'm not saying we should throw it away completely. My concern is that right now, it reads "you must not do this, even if you are targeting C11 or newer where it works as intended".
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 31, 2020 12:52
\| \|
Most of our rules forbid undefined behavior. As you note, this rule goes farther, forbidding not only UB, but behavior that is well-defined in C11, but not C99. It would make sense to permit C11-compliant code if it was written with the programmer aware of these details for C11 and C99. However, we believe that most programmers are not aware of this distinction. So forbidding the well-defined-in-C11 behavior serves as a safety measure, without causing much harm to those few programmers who wish to make use of the C11-specific behavior.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 31, 2020 14:24
\| \|
Let me play devil's advocate then: In that case, why does [MSC37-C-EX1](MSC37-C_%20Ensure%20that%20control%20never%20reaches%20the%20end%20of%20a%20non-void%20function) exist, since in C90, falling off the end of `main` was Undefined Behavior? And why don't we ban the `"x"` modes to `fopen`, since they didn't exist in C99, and using modes that don't exist is Undefined Behavior?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 31, 2020 14:41
\| \|
The point of these rules is not to limit C to a least-common-denominator, but to balance security & safety with the set of permissible features.
OK consider these three features: fopen("x"), MSC37-C:EX1 (which permits main() to lack a return statement), and EXP35-C's forbidden feature (of accessing an object with temporary lifetime.
Consider these questions:
Q: How likely are people to use the feature to write safe code without being aware of the feature?fopen(x): Never  
MSC37-C:EX1: Likely  
EXP35-C: Likely
Q: If we forbid the feature, how likely are people to complain?  
fopen(x): Likely  
MSC37-C:EX1: Likely  
EXP35-C: Unlikely (no one else has complained about this)
So I still want to keep the status quo, because unlike this rule, people will holler if we forbid fopen(x) or MSC37-C:EX1.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 31, 2020 16:02
\| \|
Can we at least add an exception for code that will always be compiled with a C11 or newer compiler? Perhaps we could even require the use of a `static_assert` or something so the code itself enforces it.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 31, 2020 16:19
\| \|
That would be useful if we just wanted to prevent people from running C11-specific code on a merely-C99 platform. We don't want people to use this C11-specific feature, not because of portability, but because the increase in safety justifies the limitation of power.
We employ the same principle in [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap);(where we forbid letting signed integers wrap, which is perfectly well-defined behavior).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 31, 2020 17:10
\| \|
It has INT30-C-EX1 though, and that's exactly the kind of thing I'm asking for here.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 31, 2020 17:35
\| \|
I think there should be an exception to this rule for C11 mode where the code is not problematic. The whole reason the specification changed is to bless the kind of code in the first NCCE because it's not unreasonable code and the alternative has strictly worse performance due to needing an extra copy (unless you have a kind optimizer).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 01, 2020 13:51
\| \|
[Joseph C. Sible](https://wiki.sei.cmu.edu/confluence/display/~jcsible):
You just added a new noncompliant code example and compliant solution, that involves incrementing the first element of an array with temporary lifetime.; Why?  
Assuming we keep your new code examples, should we modify or remove the other code examples to minimize redundancy?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 20, 2021 09:57
\| \|
The increment example was already there. My new example is the last one, the one that saves a pointer. I don't see any redundancy between any of these three examples. Here's how I'd summarize each:
1.  If you're on C99 still, don't use things with temporary lifetime past the sequence point where you got them.
2.  Don't modify things with temporary lifetime.
3.  Don't use things with temporary lifetime past the full expression where you got them.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 20, 2021 15:48
\|
