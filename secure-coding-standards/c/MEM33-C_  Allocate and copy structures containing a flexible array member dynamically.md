The C Standard, 6.7.3.2, paragraph 20 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], says
> As a special case, the last element of a structure with more than one named member may have an incomplete array type; this is called a *flexible array member*. In most situations, the ﬂexible array member is ignored. In particular, the size of the structure is as if the flexible array member were omitted except that it may have more trailing padding than the omission would imply.

The following is an example of a structure that contains a flexible array member:
``` java
struct flex_array_struct {
  int num;
  int data[];
};
```
This definition means that when computing the size of such a structure, only the first member, `num`, is considered. Unless the appropriate size of the flexible array member has been explicitly added when allocating storage for an object of the `struct`, the result of accessing the member `data` of a variable of nonpointer type `struct flex_array_struct` is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). [DCL38-C. Use the correct syntax when declaring a flexible array member](DCL38-C_%20Use%20the%20correct%20syntax%20when%20declaring%20a%20flexible%20array%20member) describes the correct way to declare a `struct` with a flexible array member.
To avoid the potential for undefined behavior, structures that contain a flexible array member should always be allocated dynamically. Flexible array structures must
-   Have dynamic storage duration (be allocated via `malloc()` or another dynamic allocation function)
-   Be dynamically copied using `memcpy()` or a similar function and not by assignment
-   When used as an argument to a function, be passed by pointer and not copied by value
## Noncompliant Code Example (Storage Duration)
This noncompliant code example uses automatic storage for a structure containing a flexible array member:
``` c
#include <stddef.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void func(void) {
  struct flex_array_struct flex_struct;
  size_t array_size = 4;
  /* Initialize structure */
  flex_struct.num = array_size;
  for (size_t i = 0; i < array_size; ++i) {
    flex_struct.data[i] = 0;
  }
}
```
Because the memory for `flex_struct` is reserved on the stack, no space is reserved for the `data` member. Accessing the `data` member is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Compliant Solution (Storage Duration)
This compliant solution dynamically allocates storage for `flex_array_struct`:
``` c
#include <stdlib.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void func(void) {
  struct flex_array_struct *flex_struct;
  size_t array_size = 4;
  /* Dynamically allocate memory for the struct */
  flex_struct = (struct flex_array_struct *)malloc(
    sizeof(struct flex_array_struct)
    + sizeof(int) * array_size);
  if (flex_struct == NULL) {
    /* Handle error */
  }
  /* Initialize structure */
  flex_struct->num = array_size;
  for (size_t i = 0; i < array_size; ++i) {
    flex_struct->data[i] = 0;
  }
}
```
## Noncompliant Code Example (Copying)
This noncompliant code example attempts to copy an instance of a structure containing a flexible array member (`struct ``flex_array_struct`) by assignment:
``` c
#include <stddef.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void func(struct flex_array_struct *struct_a,
          struct flex_array_struct *struct_b) {
  *struct_b = *struct_a;
}
```
When the structure is copied, the size of the flexible array member is not considered, and only the first member of the structure, `num`, is copied, leaving the array contents untouched.
## Compliant Solution (Copying)
This compliant solution uses `memcpy()` to properly copy the content of `struct_a` into `struct_b`:
``` c
#include <string.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void func(struct flex_array_struct *struct_a,
          struct flex_array_struct *struct_b) {
  if (struct_a->num > struct_b->num) {
    /* Insufficient space; handle error */
    return;
  }
  memcpy(struct_b, struct_a,
         sizeof(struct flex_array_struct) + (sizeof(int)
           * struct_a->num));
}
```
## Noncompliant Code Example (Function Arguments)
In this noncompliant code example, the flexible array structure is passed by value to a function that prints the array elements:
``` c
#include <stdio.h>
#include <stdlib.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void print_array(struct flex_array_struct struct_p) {
  puts("Array is: ");
  for (size_t i = 0; i < struct_p.num; ++i) {
    printf("%d ", struct_p.data[i]);
  }
  putchar('\n');
}
void func(void) {
  struct flex_array_struct *struct_p;
  size_t array_size = 4;
  /* Space is allocated for the struct */
  struct_p = (struct flex_array_struct *)malloc(
    sizeof(struct flex_array_struct)
    + sizeof(int) * array_size);
  if (struct_p == NULL) {
    /* Handle error */
  }
  struct_p->num = array_size;
  for (size_t i = 0; i < array_size; ++i) {
    struct_p->data[i] = i;
  }
  print_array(*struct_p);
}
```
Because the argument is passed by value, the size of the flexible array member is not considered when the structure is copied, and only the first member of the structure, `num`, is copied.
## Compliant Solution (Function Arguments)
In this compliant solution, the structure is passed by reference and not by value:
``` c
#include <stdio.h>
#include <stdlib.h>
struct flex_array_struct {
  size_t num;
  int data[];
};
void print_array(struct flex_array_struct *struct_p) {
  puts("Array is: ");
  for (size_t i = 0; i < struct_p->num; ++i) {
    printf("%d ", struct_p->data[i]);
  }
  putchar('\n');
}
void func(void) {
  struct flex_array_struct *struct_p;
  size_t array_size = 4;
  /* Space is allocated for the struct and initialized... */
  print_array(struct_p);
}
```
## Risk Assessment
Failure to use structures with flexible array members correctly can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). 

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM33-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | flexible-array-member-assignmentflexible-array-member-declaration | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM33 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.DECL.FAM | Declaration of Flexible Array Member |
| Compass/ROSE |  |  | Can detect all of these |
| Cppcheck Premium | 24.11.0 | premium-cert-mem33-c |  |
| Helix QAC | 2024.4 | C1061, C1062, C1063, C1064 |  |
| Klocwork | 2024.4 | MISRA.INCOMPLETE.STRUCTMISRA.MEMB.FLEX_ARRAY.2012 |  |
| LDRA tool suite | 9.7.1 | 649 S, 650 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM33-aCERT_C-MEM33-b | Allocate structures containing a flexible array member dynamicallyDo not copy instances of structures containing a flexible array member |
| Polyspace Bug Finder | R2024a | CERT C: Rule MEM33-C | Checks for misuse of structure with flexible array member (rule fully covered) |
| RuleChecker | 24.04 | flexible-array-member-assignmentflexible-array-member-declaration | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | DCL38-C. Use the correct syntax when declaring a flexible array member | Prior to 2018-01-12: CERT: Unspecified Relationship |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-401 and MEM33-CPP
There is no longer a C++ rule for MEM33-CPP. (In fact, all C++ rules from 30-50 are gone, because we changed the numbering system to be 50-99 for C++ rules.)
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 6.7.3.2, "Structure and Union Specifiers" |
| [JTC1/SC22/WG14 N791] | Solving the Struct Hack Problem |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152152) [](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152156)
## Comments:

|  |
| ----|
| Unfortunately this advice doesn't really work in practice.  If you try this on many compilers you'll get warnings about the use of a zero-sized array.  Since the level of compiler complaints you get about 'data[]' is vastly higher than 'data[1]', I can't see people rushing to adopt this.
                                        Posted by pgut001@cs.auckland.ac.nz at Jan 18, 2008 06:44
                                     |
| This only happens on old compilers that are not up to date with C99.
                                        Posted by dmk at Jan 18, 2008 11:04
                                     |
| I've just run a quick test on a handful of accessible machines and the set "old compilers that are not up to date with C99" seems to be tending towards "everything but gcc".; Admittedly some of them aren't the latest (e.g. for the Windows representative I have Visual Studio 2005 with 2007 updates and not the 2008 version which has only just been released), but it indicates that you're going to run into problems with this if you assume it's supported.  Windows in particular is problematic because the Win32 API could well be the heaviest user of flexible arrays around.
                                        Posted by pgut001@cs.auckland.ac.nz at Jan 20, 2008 05:56
                                     |
| The Scope of this document is C99 and later.
                                        Posted by dmk at Mar 30, 2008 14:50
                                     |
| Berin Babcock-McConnell says:
If we look at the (original) code examples we will see that the
noncompliant examples revolve around the use of,
struct flexArrayStruct {
  int num;
  int data[1];
};

whereas the compliant examples "fix" the problem with,
``` java
struct flexArrayStruct{
  int num;
  int data[];
};
```
My understanding is that flexible array members entered the language  
in C99. So, regardless of language version, my understanding is that  
the first example is merely a structure whose second member is a one  
element array. Consequently, "fixing" the first example with the  
second example is a bit of an apples to oranges comparison.
As a bit of an aside, under the "Noncompliant Code Example  
(Declaration)" is the statement, "The problem with this code is that  
the only member that is guaranteed to be valid, by strict C99  
definition, is structP-\>data[0](/confluence/pages/createpage.action?spaceKey=c&title=0)." But I have a doubt as to whether  
that is true and in what sense. Perhaps this explanation should be  
extended to make this clear. I would think that a tendency toward  
explaining problems in detail so as to be understood even by those not  
familiar with the intricacies of the language would be a good thing.
The second set of examples (the Reference examples) strikes me as  
being more problematic than the first in that not only does it compare  
apples to oranges but it switches modes (i.e. it switches from passing  
a structure to passing a pointer to a structure) and confuses issues.  
Of course the "flexible array member" in the noncompliant example  
isn't going to be considered - all it is a one element array.
The guideline not well written and I think it should be redone or, at  
least, heavily modified. It should introduce flexible arrays as a new  
feature of C99 and maybe explain why you would want to use them. It  
might cover how a similar thing could have been hacked prior to C99  
and discuss the problems with this approach. It should describe the  
various situations in which you can shoot yourself in the foot using  
flexible arrays (by declaring them directly, copying them, using them  
as parameters (same problem as copying really but no problem in making  
it explicit), whatever else). It should then show proper usage with  
pointers, bringing the guideline to its conclusion. The title should  
also probably be changed to something more reflective of the content  
of the guideline.
Berin
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 06, 2009 14:23
\| \|
I think I have a difference of opinion with this comment, that needs to be sorted out.
I believe that the data[1](/confluence/pages/createpage.action?spaceKey=c&title=1) syntax predated C99 for flexible array members. Perhaps this was part of ISO C89 as the previous version of this guideline suggests; I need to check.
Anyway, I think there is too much text in the beginning. I'm not really happy with the innovation here of having compliant and noncompliant text in the intro section; usually anything that appears here is just neautral/informative.
This is why I sort of think the original CS/NCE pair showing how to declare flexible array members should be restored, but it may be prudent to discuss this first.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Nov 16, 2009 16:20
\| \|
Why would Compass/ROSE complain if the last element of a `struct` is an array with an index of 0, as this the correct syntax for structs with flexible array members?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 21, 2009 19:58
\| \|
That automated detection is more fit for DCL38 than for this rule now. I've updated the 'Automated Detection' section. We'll have to write a new ROSE checker for this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 23, 2009 11:12
\| \|
Typo in;Compliant Solution (Storage Duration):
`if` `(flex_sruct == NULL) {`
must be
`if` `(flex_struct == NULL) {`
![](images/icons/contenttypes/comment_16.png) Posted by karbyshev at Feb 14, 2018 10:00
\| \|
fixed, thanks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 15, 2018 09:27
\| \|
Why is the Rem Cost low here? ;I think the theory is that no flexible array member should be allocated on the stack, because the member should be flexible. So it should use the heap. Also don't pass f.a.m's in as function parameters, pass pointers to f.a.m.'s around instead. And don't use =, use memcpy() instead.  But none of this strikes me as easily automatically repairable. An automatic repair may be possible in theory, but tricky to get right.
It is automatically detectible, so the Rem Cost should prob be Medium.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 22, 2023 16:15
\|
