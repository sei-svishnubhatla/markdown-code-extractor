Abstract data types are not restricted to object-oriented languages such as C++ and Java. They should be created and used in C language programs as well. Abstract data types are most effective when used with private (opaque) data types and information hiding.
## Noncompliant Code Example
This noncompliant code example is based on the managed string library developed by CERT \[[Burch 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Burch06)\]. In this example, the managed string type and the functions that operate on this type are defined in the `string_m.h` header file as follows:
``` c
struct string_mx {
  size_t size;
  size_t maxsize;
  unsigned char strtype;
  char *cstr;
};
typedef struct string_mx string_mx;
/* Function declarations */
extern errno_t strcpy_m(string_mx *s1, const string_mx *s2);
extern errno_t strcat_m(string_mx *s1, const string_mx *s2);
/* ... */
```
The implementation of the `string_mx` type is fully visible to the user of the data type after including the `string_m.h` file. Programmers are consequently more likely to directly manipulate the fields within the structure, violating the software engineering principles of information hiding and data encapsulation and increasing the probability of developing incorrect or nonportable code.
## Compliant Solution
This compliant solution reimplements the `string_mx` type as a private type, hiding the implementation of the data type from the user of the managed string library. To accomplish this, the developer of the private data type creates two header files: an external `string_m.h` header file that is included by the user of the data type and an internal file that is included only in files that implement the managed string abstract data type.
In the external `string_m.h` file, the `string_mx` type is defined to be an instance of `struct string_mx`, which in turn is declared as an [incomplete type](BB.-Definitions_87152273.html#BB.Definitions-incompletetype):
``` c
struct string_mx;
typedef struct string_mx string_mx;
/* Function declarations */
extern errno_t strcpy_m(string_mx *s1, const string_mx *s2);
extern errno_t strcat_m(string_mx *s1, const string_mx *s2);
/* ... */
```
In the internal header file, `struct string_mx` is fully defined but not visible to a user of the data abstraction:
``` c
struct string_mx {
  size_t size;
  size_t maxsize;
  unsigned char strtype;
  char *cstr;
};
```
Modules that implement the abstract data type include both the external and internal definitions, whereas users of the data abstraction include only the external `string_m.h` file. This allows the implementation of the `string_mx` data type to remain private.
## Risk Assessment
The use of opaque abstract data types, though not essential to secure programming, can significantly reduce the number of defects and [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) introduced in code, particularly during ongoing maintenance.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL12-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL12 |  |
| LDRA tool suite | 9.7.1 | 104 D | Partially implemented |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL12-C | Checks for structure or union object implementation visible in file where pointer to this object is not dereferenced (rule partially covered) |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL12-a | If a pointer to a structure or union is never dereferenced within a translation unit, then the implementation of the object should be hidden |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL12-C).
## Related Guidelines

|  |  |
| ----|----|
| MISRA C:2012 | Directive 4.8 (advisory) |

## Bibliography

|  |
| ----|
| [Burch 2006] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152357) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152301)
## Comments:

|  |
| ----|
| 
The NASA Goddard Space Flight Centre (oh, darn - when are the American's going to learn to spell!) Center (http://software.gsfc.nasa.gov/) has good coding standards for a number of languages including C.; They actually ban the use of variadic functions outright - something that might be worth noting in those sections.  There is also a good requirement that headers for modules (and hence ADTs - some marginal relevance to this item) should be the first header included in the implementation module in order to ensure that the header is 'free-standing'.  That is, consumers of the services provided by the module (header) do not need to do more than include the header; it ensures that any other headers it needs itself are included.  Of course, the extra headers should be the minimal set required.  I find that a valuable discipline.  I also find myself using <stddef.h> more than I used to because it is the smallest header that defines size_t.
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 16:10
                                     |
| Compass/ROSE could study a .h file and detect structs that are defined, and report them as violations. However, this would catch many false positives (eg the st struct filled by fstat()). Before ROSE should report violations of this rule, we need a more rigorous definition of what constitutes a legit ADT...not just any publicly-defined struct is a violation.
                                        Posted by svoboda at Jul 16, 2008 12:15
                                     |
| Using typedef to define a pointer type makes const correctness more difficult to achieve, less obvious, or inconsistent. In the compliant example above, const is used incorrectly, illustrating the point. Taking a const string_m is wrong as shown, as this merely takes a constant pointer to a non-constant string_mx. To do it right one either needs to take a const struct string_mx*, or add a typedef const struct string_mx* const_string_m and use that. Neither is attractive. The first results in arguments of type string_m and const struct string_mx*, which visually look like two quite different types, even though they actually differ only in const-ness. The second gives more consistency, but still tries to replace C-style declaration with a typedef. Unless the indirection is useful, why not just take string_mx* and const string_mx*?
                                        Posted by sgreen at Aug 20, 2009 17:15
                                     |
| This is illustrated by C99 6.7.5.1 &quot;pointer declarators&quot;, which says:
The declaration of the constant pointer constant_ptr may be clarified by including a definition for the type â€˜â€˜pointer to intâ€™â€™.
         typedef int *int_ptr;
         const int_ptr constant_ptr;

declares constant_ptr as an object that has type â€˜â€˜const-qualified pointer to intâ€™â€™.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 06, 2010 13:38
\| \|
You are right. "const string_m" will give us a constant pointer, not a constant string. A new datatype for const string "const_string_m" is defined by typecasting the pointer to the constant structure string_mx. This solution seems more appropriate as it will keep the original structure hidden from the user. Indirection is useful here to prevent users to know about the actual implementation of the datatype.
![](images/icons/contenttypes/comment_16.png) Posted by rrungta at Apr 07, 2010 16:03
\| \|
I suggest removing the `typedef` for pointers from the compliant solution. In fact, I have been meaning to propose a guideline recommending against using typedefs to define pointers to avoid exactly this problem (see the discussion [Re: PRE03-C. Prefer typedefs to defines for encoding types](https://www.securecoding.cert.org/confluence/display/seccode/PRE03-C.+Prefer+typedefs+to+defines+for+encoding+types?focusedCommentId=38371341#comment-38371341) – although I am yet to make the changes discussed there).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 07, 2010 22:28
\| \|
Unless someone objects in the next day or so I will go ahead and make the change.
------------------------------------------------------------------------
I has missed this was already been done by [Raunak Rungta](https://wiki.sei.cmu.edu/confluence/display/~rrungta). Excellent!
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 23, 2010 18:56
\| \|
Unless I'm missing something, I think that there is an error in the compliant solution. I think that the following declarations:/\* Function declarations \*/ extern errno_t strcpy_m(string_mx \*s1, const string_mx \*s2);  
extern errno_t strcat_m(string_mx \*s1, const string_mx \*s2) ;  
/\* etc. \*/
should be be in the external header file, not in the internal header file, as these functions are part of the  
interface exported by this abstract data type.
![](images/icons/contenttypes/comment_16.png) Posted by gerivera at Dec 17, 2010 15:13
\| \|
yes, that sounds right.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Dec 19, 2010 20:52
\| \|
Consider the following file, temp.c which needs to use the ADT:
**temp.c**
``` cpp
#include "string_m.h"
string_mx x;
struct a {Â;Â Â Â 
 string_mx *z;
 string_mx y;
};
```
I then compile the code and get the following error:  
temp.c:6: error: field 'y' has incomplete type
I imagine this means that the compiler does not like not knowing the size of string_mx type to allocate for y.  
It knows how big a pointer is so it doesn't complain about z.
But why is it not complaining about x?  
Does it mean that the consumer code should always use the ADTs as pointers?
Thanks!
![](images/icons/contenttypes/comment_16.png) Posted by ilya at Nov 02, 2011 21:35
\| \|
You are correct that the compiler will complain because it does not know sizeof( string_mx). I don't know what compiler you are using, but when I build the code sample using GCC 4.4, I also get a complaint about y, but none about x. If I fix the code around y, the compiler then complains about x. So the answer to your question is not based on standard C, but rather on the details of your compiler.
I would guess that the declaration of y affects the sizeof( struct a), which must be known at compile time, and so the compiler senses an error immediately. The declaration of x has no effect on compilation of the rest of the code, so its problem is only discovered by the linker, rather than the compiler.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 03, 2011 12:34
\|
