Do not take the size of a pointer to a type when you are trying to determine the size of the type. Taking the size of a pointer to a type always returns the size of the pointer and not the size of the type. This can be especially problematic when calculating the size of an array. (See [ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array](ARR01-C_%20Do%20not%20apply%20the%20sizeof%20operator%20to%20a%20pointer%20when%20taking%20the%20size%20of%20an%20array).)
## Noncompliant Code Example
This noncompliant code example incorrectly calls the `sizeof()` operator on the variable `d_array` (which is declared as a pointer to `double`) instead of to `*d_array`, which is of type `double`:
``` c
double *allocate_array(size_t num_elems) {
  double *d_array;
  if (num_elems > SIZE_MAX/sizeof(d_array)) {
    /* Handle error condition */
  }
  d_array = (double *)malloc(sizeof(d_array) * num_elems);
  if (d_array == NULL) {
    /* Handle error condition */
  }
  return d_array;
}
```
The test of `num_elems` ensures that the expression `sizeof(d_array) * num_elems` does not result in an integer overflow. (See [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow).)
For many [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation), the size of a pointer and the size of `double` (or any other type) is likely to be different. On IA-32 implementations, for example, the `sizeof(double *)` is 4, whereas the `sizeof(double)` is 8. In this case, insufficient space is allocated to contain an array of 100 values of type `double`.
## Compliant Solution
Make sure you correctly calculate the size of the element to be contained in the aggregate data structure. The expression `sizeof(*d_array)` returns the size of the data structure referenced by `d_array` and not the size of the pointer. Furthermore, the expression is valid even if the `d_array` pointer is `NULL` or uninitialized because `sizeof` operates on the type of its argument.
``` c
double *allocate_array(size_t num_elems) {
  double *d_array;
  if (num_elems > SIZE_MAX/sizeof(*d_array)) {
    /* Handle error condition */
  }
  d_array = (double *)malloc(sizeof(*d_array) * num_elems);
  if (d_array == NULL) {
    /* Handle error condition */
  }
  return d_array;
}
```
## Risk Assessment
Taking the size of a pointer instead of the actual type can result in insufficient space being allocated, which can lead to buffer overflows and the execution of arbitrary code by an attacker.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP01-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| LDRA tool suite | 9.7.1 | 577 S | Fully implemented |
| Splint | 3.1.1 | ; | ; |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP01-CPP. Do not take the size of a pointer to determine the size of the pointed-to type |
| ISO/IEC TS 17961 | Taking the size of a pointer to determine the size of the pointed-to type [sizeofptr] |
| MITRE CWE | CWE-467, Use of sizeof() on a pointer type |

## Bibliography

|  |  |
| ----|----|
| [Drepper 2006] | Section 2.1.1, "Respecting Memory Bounds" |
| [Viega 2005] | Section 5.6.8, "Use of sizeof() on a Pointer Type" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/EXP00-C.+Use+parentheses+for+precedence+of+operation?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=358) [](https://www.securecoding.cert.org/confluence/display/seccode/EXP02-C.+Be+aware+of+the+short-circuit+behavior+of+the+logical+AND+and+OR+operators?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I had to read the title a couple of times before I got the point, and I think it would be better to change:
"Do not take the size of a pointer to determine the size of a type"
into "Do not take the size of a pointer to determined the size of the pointed-to type"
--
And we must also keep in mind that that sizeof(*d_array) doesn't give the size of the whole array, but the size of just the first element. This often leads to surprises also.
                                        Posted by steve at Mar 13, 2008 20:54
                                     |
| Should the discussion mention that 'arrays' passed to functions, even when declared as 'int somefunc(int arr[10])', are treated as a pointer by sizeof()?; Or is that sufficiently obscure not to warrant mention?  What about discussion of: extern double array1[200]; vs extern double array2[];?  Again, this could be either obscure enough or common sense enough not to warrant mention.
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 21:50
                                     |
| This is covered by the reference to ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
                                        Posted by rcs at Mar 16, 2008 13:00
                                     |
| Am I correct in presuming this guideline presumes the pointer argument may be a pointer to function?
                                        Posted by xuinkrbin. at Feb 12, 2009 15:30
                                     |
| Also, is the following consider acceptable by this guideline:
void f(int **p)
{
sizeof( *p );
}

![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 12, 2009 15:45
\| \|
\> Also, is the following consider acceptable by this guideline:
It depends on what you do with the result of `sizeof(*p)`. Here is a valid usage:
``` java
void f(int **p)
{
  /* Allocate an array to hold **p */
  int** q = (int**) malloc( sizeof( *p ) * ARRAY_SIZE);
}
```
This rule is singling out not a design flaw, but rather a coding flaw. The size of a pointer can often be different than the size of its pointed-to type, and the rule warns you not to confuse the two.
\> Am I correct in presuming this guideline presumes the pointer argument may be a pointer to function?
I don't think so. IIRC a function (as opposed to a pointer to function) is not a 'supported' type in C99, so you can't apply `sizeof` to it. So using a function type, rather than a pointer to function type, is a compiler error; so the compiler will prevent you from violating this recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 13, 2009 09:58
\| \|
Thanks. ;I think I may have misspoken (mistyped?) with respect to My function pointer question.  Does the guideline *permit* the pointer to be a function pointer?  \[I do know the ISO standard prohibits taking the sizeof a function.  However, I was wondering if the prohibition was on taking the sizeof any pointer symbol.  Clearly, however, I now see the guideline does permit taking the sizeof a function pointer.  Thanks.\]
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 13, 2009 10:24
\| \|
This example may seem somewhat contrived, but what about the following:
``` java
void f(int *p)
{
sizeof(*&p);
}
```
would this be considered acceptable?
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 13, 2009 14:33
\| \|
Does this guideline apply to named pointer types such as:
``` java
... sizeof(struct A*);
```
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Feb 13, 2009 14:35
\| \|
This example is unacceptable, but for other reasons. ;^)
This rule "EXP01-C. Do not take the size of a pointer to determine the size of the pointed-to type" is not violated because you are not taking the size of a pointer.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 14, 2009 09:21
\| \|
Yes.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 14, 2009 09:22
\| \|
isn't this;discussion just pure common sense, i.e. something you would find in a first year computer science class?
why include the obvious in a "standard"?
![](images/icons/contenttypes/comment_16.png) Posted by etkinsd@battelle.org at Jun 18, 2009 10:04
\| \|
Many of the guidelines are obvious, but are here to establish requirements for a conforming system or analysis tool.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 19, 2009 09:18
\| \|
The final paragraph in the Noncompliant Code Example says that `sizeof(*double)` is four.; When I try to compile a program containing that expression with GCC, it generates the following error: "expected expression before 'double'".  Should the asterisk be moved to after "double"?
![](images/icons/contenttypes/comment_16.png) Posted by kraai at Jun 11, 2013 13:22
\| \|
Corrected, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 11, 2013 13:55
\|
