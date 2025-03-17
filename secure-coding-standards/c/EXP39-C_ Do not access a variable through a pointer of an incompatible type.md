Modifying a variable through a pointer of an incompatible type (other than `unsigned char`) can lead to unpredictable results. Subclause 6.2.7 of the C Standard states that two types may be distinct yet compatible and addresses precisely  when two distinct types are compatible.
This problem is often caused by a violation of aliasing rules. The C Standard, 6.5, paragraph 7 \[ [ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024) \], specifies those circumstances in which an object may or may not be aliased.
> An object shall have its stored value accessed only by an lvalue expression that has one of the following types:
>
> -   a type compatible with the effective type of the object,
> -   a qualified version of a type compatible with the effective type of the object, 
> -   the signed or unsigned type compatible with the underlying type of the effective type of the object,
> -   the signed or unsigned type compatible with a qualified version of the underlying type of the effective type of the object, 
> -   an aggregate or union type that includes one of the aforementioned types among its members (including, recursively, a member of a subaggregate or contained union), or 
> -   a character type. 

Accessing an object by means of any other [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue) expression (other than `unsigned char`) is [undefined behavior 36](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_36).
## Noncompliant Code Example
In this noncompliant example, an object of type `float` is incremented through an `int *`. The programmer can use the unit in the last place to get the next representable value for a floating-point type.  However, accessing an object through a pointer of an incompatible type is undefined behavior.
``` c
#include <stdio.h>
void f(void) {
  if (sizeof(int) == sizeof(float)) {
    float f = 0.0f;
    int *ip = (int *)&f;
    (*ip)++;
    printf("float is %f\n", f);
  }
}
```
## Compliant Solution
In this compliant solution, the standard C function `nextafterf()` is used to round toward the highest representable floating-point value:
``` c
#include <float.h>
#include <math.h>
#include <stdio.h>
void f(void) {
  float f = 0.0f;
  f = nextafterf(f, FLT_MAX);
  printf("float is %f\n", f);
}
```
## Noncompliant Code Example
In this noncompliant code example, an array of two values of type `short` is treated as an integer and assigned an integer value. The resulting values are indeterminate.
``` c
#include <stdio.h>
void func(void) {
  short a[2];
  a[0]=0x1111;
  a[1]=0x1111;
  *(int *)a = 0x22222222;
  printf("%x %x\n", a[0], a[1]);
}
```
When translating this code, an implementation can assume that no access through an integer pointer can change the array `a`, consisting of shorts. Consequently, `printf()` may be called with the original values of `a[0]` and `a[1]`.
### Implementation Details
Recent versions of GCC turn on the option `-fstrict-aliasing,` which allows alias-based optimizations, by default with `-O2`. Some architectures then print "1111 1111" as a result. Without optimization, the executable generates the *expected* output "2222 2222."
To disable optimizations based on alias analysis for faulty legacy code, the option `-fno-strict-aliasing` can be used as a workaround. The option `-Wstrict-aliasing,` which is included in `-Wall,` warns about some, but not all, violations of aliasing rules when `-fstrict-aliasing` is active.
When GCC 3.4.6 compiles this code with optimization, the assignment through the aliased pointer is effectively eliminated.
## Compliant Solution
This compliant solution uses a `union` type that includes a type compatible with the effective type of the object:
``` c
#include <stdio.h>
void func(void) {
  union {
    short a[2];
    int i;
  } u;
  u.a[0]=0x1111;
  u.a[1]=0x1111;
  u.i = 0x22222222;
  printf("%x %x\n", u.a[0], u.a[1]);
  /* ... */
}
```
The C standard states:
> If the member used to read the contents of a union object is not the same as the member last used to store a value in the object, the appropriate part of the object representation of the value is reinterpreted as an object representation in the new type as described in 6.2.6 (a process sometimes called “type punning”). This might be a trap representation

The call to `printf()` typically outputs "2222 2222". However, there is no guarantee that this will be true; the object representations of `a` and `i` are unspecified and need not be compatible in this way, despite this operation being commonly accepted as an implementation extension. (See [unspecified behavior 11](DD.-Unspecified-Behavior_87152246.html#DD.UnspecifiedBehavior-unspecifiedbehavior11).)
## Noncompliant Code Example
In this noncompliant code example, a `gadget` object is allocated, then `realloc()` is called to create a `widget` object using the memory from the `gadget` object. Although reusing memory to change types is acceptable, accessing the memory copied from the original object is undefined behavior.
``` c
#include <stdlib.h>
struct gadget {
  int i;
  double d;
  char *p;
};
struct widget {
  char *q;
  int j;
  double e;
};
void func(void) {
  struct gadget *gp;
  struct widget *wp;
  gp = (struct gadget *)malloc(sizeof(struct gadget));
  if (!gp) {
    /* Handle error */
  }
  /* ... Initialize gadget ... */
  wp = (struct widget *)realloc(gp, sizeof(struct widget));
  if (!wp) {
    free(gp);
    /* Handle error */
  }
  if (wp->j == 12) {
    /* ... */
  }
  /* ... */
  free(wp);
}
```
## Compliant Solution
This compliant solution reuses the memory from the `gadget` object but reinitializes the memory to a consistent state before reading from it:
``` c
#include <stdlib.h>
#include <string.h>
struct gadget {
  int i;
  double d;
  char *p;
};
struct widget {
  char *q;
  int j;
  double e;
};
void func(void) {
  struct gadget *gp;
  struct widget *wp;
  gp = (struct gadget *)malloc(sizeof (struct gadget));
  if (!gp) {
    /* Handle error */
  }
  /* ... */
  wp = (struct widget *)realloc(gp, sizeof(struct widget));
  if (!wp) {
    free(gp);
    /* Handle error */
  }
  memset(wp, 0, sizeof(struct widget));
  /* ... Initialize widget ... */
  if (wp->j == 12) {
    /* ... */
  }
  /* ... */
  free(wp);
}
```
## Noncompliant Code Example
According to the C Standard, 6.7.7.3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], using two or more incompatible arrays in an expression is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See also [undefined behavior 73](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_73).)
For two array types to be compatible, both should have compatible underlying element types, and both size specifiers should have the same constant value. If either of these properties is violated, the resulting behavior is undefined.
In this noncompliant code example, the two arrays `a` and `b` fail to satisfy the equal size specifier criterion for array compatibility. Because `a` and `b` are not equal, writing to what is believed to be a valid member of `a` might exceed its defined memory boundary, resulting in an arbitrary memory overwrite.
``` c
enum { ROWS = 10, COLS = 15 };
void func(void) {
  int a[ROWS][COLS];
  int (*b)[ROWS] = a;
}
```
Most compilers will produce a warning diagnostic if the two array types used in an expression are incompatible.
## Compliant Solution
In this compliant solution, `b` is declared to point to an array with the same number of elements as `a`, satisfying the size specifier criterion for array compatibility:
``` c
enum { ROWS = 10, COLS = 15 };
void func(void) {
  int a[ROWS][COLS];
  int (*b)[COLS] = a;
}
```
## Risk Assessment
Optimizing for performance can lead to aliasing errors that can be quite difficult to detect. Furthermore, as in the preceding example, unexpected results can lead to buffer overflow attacks, bypassing security checks, or unexpected execution.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP39-C | Medium | Unlikely | High |  P2  |   L3  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Cppcheck Premium | 24.11.0 | premium-cert-exp39-c |  |
| Helix QAC | 2024.4 | C0310, C0751, C3305C++3017, C++3030, C++3033 |  |
| Klocwork | 2024.4 | MISRA.CAST.FUNC_PTR.2012MISRA.CAST.INCOMPLETE_PTR_TO_ANY.2012
MISRA.CAST.OBJ_PTR_TO_NON_INT.2012
MISRA.CAST.OBJ_PTR_TO_OBJ_PTR.2012 |  |
| LDRA tool suite | 9.7.1 | 94 S, 554 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP39-a CERT_C-EXP39-b 
CERT_C-EXP39-c 
CERT_C-EXP39-d 
CERT_C-EXP39-e 
CERT_C-EXP39-f | There shall be no implicit conversions from integral to floating typeA cast should not be performed between a pointer to object type and a different pointer to object type
Avoid accessing arrays and pointers out of bounds
Avoid buffer overflow from tainted data due to defining incorrect format limits
Avoid buffer read overflow from tainted data
Avoid buffer write overflow from tainted data |
| Polyspace Bug Finder | R2024a | CERT C: Rule EXP39-C | Checks for cast to pointer pointing to object of different type (rule partially covered) |
| PVS-Studio | 7.35 |  V580  |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP39-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TS 17961 | Accessing an object through a pointer to an incompatible type [ptrcomp] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-125, Out-of-bounds Read | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-704 | 2017-06-14: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-119 and EXP39-C
Independent( ARR30-C, ARR38-C, ARR32-C, INT30-C, INT31-C, EXP39-C, EXP33-C, FIO37-C) STR31-C = Subset( Union( ARR30-C, ARR38-C)) STR32-C = Subset( ARR38-C)
Intersection( EXP39-C, CWE-119) =
-   Reading memory assigned to one type, but being accessed through a pointer to a larger type.
EXP39-C – CWE-119 =
-   Writing to memory assigned to one type, but accessed through a pointer to a larger type
-   Reading memory assigned to one type, but being accessed through a pointer to a smaller (or equal-sized) type
CWE-119 – EXP39-C =
-   Reading beyond a buffer using a means other than accessing a variable through an incompatible pointer.
### CWE-123 and EXP39-C
Intersection( CWE-123, EXP39-C) = Ø
EXP39-C allows overflowing a (small) buffer, but not arbitrary memory writes. (Possibly an arbitrary-memory write exploit could be devised using a “perfect storm” of incompatible types, but this would be uncommon in practice.)
### CWE-125 and EXP39-C
Independent( ARR30-C, ARR38-C, EXP39-C, INT30-C) STR31-C = Subset( Union( ARR30-C, ARR38-C)) STR32-C = Subset( ARR38-C)
Intersection( EXP39-C, CWE-125) =
-   Reading memory assigned to one type, but being accessed through a pointer to a larger type.
ESP39-C – CWE-125 =
-   Reading memory assigned to one type, but being accessed through a pointer to a smaller (or equal-sized) type
CWE-125 – EXP39-C =
-   Reading beyond a buffer using a means other than accessing a variable through an incompatible pointer.
### CWE-188 and EXP39-C
Intersection( CWE-188, EXP39-C) = Ø
CWE-188 appears to be about making assumptions about the layout of memory between distinct variables (that are not part of a larger struct or array). Such assumptions typically involve pointer arithmetic (which violates ARR30-C). EXP39-C involves only one object in memory being (incorrectly) interpreted as if it were another object. EG a float being treated as an int (usually via pointers and typecasting)
### CWE-704 and EXP39-C
CWE-704 = Union( EXP39-C, list) where list =
-   Incorrect (?) typecast that is not incompatible
## Bibliography

|  |  |
| ----|----|
| [Acton 2006] | "Understanding Strict Aliasing" |
| GCC Known Bugs | "C Bugs, Aliasing Issues while Casting to Incompatible Types" |
| [ISO/IEC 9899:2024] | 6.5, "Expressions"6.7.7.3, "Array Declarators" |
| [Walfridsson 2003] | Aliasing, Pointer Casts and GCC 3.3 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152099) [](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152401)
## Comments:

|  |
| ----|
| Submitted by email from John Engelhart:
Specifically, the example at the end of the page designated as the "Compliant Solution" (reproduced here)
Compliant Solution
This compliant solution uses a union type that includes a type compatible with the effective type of the object.
union {
  short a[2];
  int i;
} u;
u.a[0]=0x1111;
u.a[1]=0x1111;
u.i = 0x22222222;
printf("%x %x\n", u.a[0], u.a[1]);

This code example now reliably outputs "2222 2222". ------------------
In fact, this is an example of "undefined behavior" and should be removed.  
From "The New C Standard" ( <http://www.knosof.co.uk/cbook/cbook.html> ) page ~960 (covering C99 Section 6.5 clause 7 "An object shall have its stored value accessed only by an lvalue expression that has one of the following types:" (the same rules quoted at the top of EXP39-C):
Commentary
This list is sometimes known as the aliasing rules for C. Any access to the
stored value of an object using a type that is not one of those listed next
results in undefined behavior. To access the same object using one of the different types listed requires the use of a pointer type. Reading from a different member of a union type than the one last stored into is unspecified behavior.  
------------------
Note the last sentence. Reading from a different member of a union other than the last one used to store a value is unspecified behavior. Clearly the example given as "Compliant" in EXP39-C is reading from different members (u.a[0](/confluence/pages/createpage.action?spaceKey=c&title=0) and u.a[1](/confluence/pages/createpage.action?spaceKey=c&title=1)) than the one last stored (u.i = ...). This example /WILL NOT/ reliably output "2222 2222".
Type punning like this is very difficult to do "correctly". IMHO, any form of type punning should be strongly discouraged, and no examples of how to do it "correctly" should be given.:
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jul 19, 2010 11:35
\| \|
I agree with the sentiment...type punning is not something we want to encourage. OTOH we can't exactly show a compliant solution without it.
Still, the 1st CS doesn't define what the "expected value" is. On my platform f() returns 0...is that the expected value??? The 2nd CS also has an implicit assumption that sizeof(int) == 2 \* sizeof(short).
I suspect a good CS can be made involving any type T and an array of: char\[ sizeof(T)\]. By 'good', I don't mean 'recommended', I only mean 'well-defined'. I think its a mistake to even refer to 'expected values' when doing type-punning.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 19, 2010 15:54
\| \|
In the 2nd CS, what is the 'expected value'? And what is type-punning? (that is, if the rule is going to use 'type-punning' in a legit context, it needs to cite a definition.On my Ubuntu box, this CS (and the corresponding NCCEs) print 0...is that the expected value? Or is it 3?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 04, 2013 15:15
\| \|
The expected value is unspecified because the underlying representation of a double is unspecified.; So whatever random bits happen to be there appears to be what's "expected."
Also, I agree we should have a formal definition for type punning.  But I would prefer we simply didn't use the terminology or the example in our rules as it's an evil concept, even if valid in C.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 04, 2013 16:20
\| \|
It sounds like you agree with me that the compliant solution isn't really compliant.
I'm nuking the NCCE & CS pair on Monday unless someone steps in to save it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 08, 2013 13:36
\| \|
I neither agree nor disagree.; ![](images/icons/emoticons/wink.svg)  The code, as it stands, is useless without further explanation of programmer intent.  However, the code could be valid depending on that intent as there is no UB.
Don't consider this to be "stepping in to save" the examples though, just clarifying why I didn't chop them when I reviewed.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 11, 2013 09:04
\| \|
Nuked those code samples, approved the rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 11, 2013 10:55
\| \|
the gadget example is not encapsulated in a function of any kind; this probably needs to be fixed.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 24, 2013 09:01
\| \|
Newbie here... first comment on the site.; So bear with me.  How did P18/L1 MEM08-C become depracated by this rule (EXP39-C) which is P2/L3?
John Whited, CISSP, CSSLP
Principal Security Engineer
Raytheon IIS Garland TX
![](images/icons/contenttypes/comment_16.png) Posted by john.whited at Aug 12, 2014 11:30
\| \|
The rationale for the deprecation was that MEM08-C's underlying problem (realloc'ing something other than an array) is the same problem as EXP39-C's: don't access a pointer through an incompatible type, because the realloc needs to copy data from the original object. So if the original objects are not compatible, you get UB.
I think MEM08-C's priority was a bit on the high side (I think I would have ranked it about a P4-P6), and perhaps EXP39-C's priority may be a bit low with this addition.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 12, 2014 12:48
\| \|
Agreed. ;One note though...the priorities are directly derived from the Severity, Liklihood, and Remediation Cost metrics. See [How this Coding Standard is Organized](How%20this%20Coding%20Standard%20is%20Organized) for more info.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 12, 2014 14:44
\| \|
If there's a better place for this discussion let me know.; But has there been any discussion about harmonizing SEI CERT Priority / Level with MITRE's CWRAF / CWSS and/or OWASP prioritization techniques?  There are pluses and minuses to each I'm sure. But the Priority / Level approach lacks the ability to factor in software operational factors such as business / mission impact, technology in use (OS, language, etc.) and operational environment (web app vs. embedded systems etc.).
![](images/icons/contenttypes/comment_16.png) Posted by john.whited at Aug 12, 2014 16:30
\| \|
maybe email?; we haven't looked at any of these.  I think we've had our system for about 10 years now;  I'm not sure when these other systems came about.  I'm pretty happy about not factoring in business / mission impact, etc.  The assignments we have made for criticality, likelihood, and remediation cost are meant to be independent of all of this, but may serve as input into such metrics. 
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 14, 2014 20:51
\| \|
Gadget/Widget example is error prone. gp and wp in most cases point at the same location. In worst case gp will be point at freed area (when re-allocation doesn't append memory, but allocates it in a different area).; 
![](images/icons/contenttypes/comment_16.png) Posted by vlad at Apr 13, 2018 13:09
\| \|
It is important to not touch;`gp` after the `realloc()` call, because its memory has either been freed, or it points to the same chunk as `wp`.  I added code to free `wp` when it is no longer in use.
Freeing `gp` if `realloc()` returns NULL is perfectly fine in this case, and necessary when doing normal cleanup.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 19, 2018 13:16
\| \|
Strict aliasing is such a problem that a lot of compilers let you turn it off. Can we add an exception for compiling with `gcc -fno-strict-aliasing`, etc.?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 14:40
\| \|
The "right" solution to this in a lot of cases is `memcpy`. We should have a compliant solution that uses it.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 01, 2020 14:40
\| \|
Hmm, in C, type punning is well-defined when using unions and the only danger from it is that the punned value could be a trap representation in the new type. I don't think we make this very clear with the prose, but see C17 6.2.6, 6.5p7, and footnote 97.
Using;`memcpy()` as done in the new compliant solution is not valid; that only works if the memory has no declared type (e.g., it's a void \* you got from `malloc()`). See C17 6.5p6 and p7
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 14, 2020 11:06
\| \|
> Hmm, in C, type punning is well-defined when using unions and the only danger from it is that the punned value could be a trap representation in the new type. I don't think we make this very clear with the prose, but see C17 6.2.6, 6.5p7, and footnote 97.

Fair enough. That's definitely not what we're saying now though; I'll try to reword it.
> Using;`memcpy()` as done in the new compliant solution is not valid; that only works if the memory has no declared type (e.g., it's a void \* you got from `malloc()`). See C17 6.5p6 and p7

Are you sure? My reading is exactly the opposite (that it only works if it *does* have a declared type). <https://blog.regehr.org/archives/959> and <https://stackoverflow.com/a/38610554/7509065> seem to take that view as well.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 14, 2020 11:25
\| \|
Okay, I think I fixed the issue with `union`s. Let me know if you still think the `memcpy` is unsafe; if so, I'll remove it.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 14, 2020 11:55
\| \|
> Are you sure?

Reasonably sure, but this is complex stuff that experts don't always agree on because we sometimes are talking about different situations. The new `memcpy()`;example is definitely UB because `_Alignof(short) != _Alignof(int)`, but I think also because it's working with declared types.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 14, 2020 12:23
\| \|
I removed the example for now to avoid possibly giving bad information until we're sure.
I'm not sure how alignment is relevant in that example. The memcpy just copies bytes around, which doesn't have an alignment requirement, and everything else that accesses memory is accessing it from a location that is properly aligned for the type.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 14, 2020 12:42
\| \|
I was thinking of C17 6.3.2.3p7 where the pointer object is not correctly aligned for the type, but then stupidly was testing the non-pointer alignments. Sorry for the confusion with that!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 14, 2020 12:58
\| \|
Do the examples here stand for the C++ context ? I know that there is; the same thing on the C11 Stndard section *6.5 Expressions paragraph 7.*
![](images/icons/contenttypes/comment_16.png) Posted by aymen.chehaider at May 02, 2021 20:25
\| \|
Yes, this rule also applies in C++. The top-level "rule" page in the C++ coding standard lists all of the C rules that also apply in C++. e.g.,;[Rule 02. Expressions (EXP)](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046335) (the second set of links on the page).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 03, 2021 07:06
\| \|
I wonder if this rule is not appropriate for some cases in C++?
I have a base class and a derived class implemented as bellow:
*class base {*
*; base() {}*
*};*
*class derive : public base {*
*  derive() : base() {} //calling base constructor*
*};*
And I received this warning (CERT-EXP39-C) like this in the constructor of derived class:
"Calling function base::base() which access an object through a pointer **this** whose type base\* is incompatible with the type of the object"
![](images/icons/contenttypes/comment_16.png) Posted by mathchuong89 at Jun 24, 2021 06:04
\| \|
That sounds to me like a bug in whatever was performing the check and not a bug in the CERT rule.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 24, 2021 07:28
\| \|
The relevant part of the C++20 standard is section 7.2.1 \[basic.lval\], paragraph 11. It refers to 3.1;\[defns.access\] for the definition of "access" and also says "C++ has no accesses of class type." Under 3.1 \[defns.access\], it says "Only objects of scalar type can be accessed. Attempts to read or modify an object of class type typically invoke a constructor (11.4.4) or assignment operator (11.4.5); such invocations do not themselves constitute accesses, although they may involve accesses of scalar subobjects." As such, the tool that gave you the warning is wrong, as that constructor invocation is not actually accessing anything.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 24, 2021 12:01
\|
