Pointer arithmetic must be performed only on pointers that reference elements of array objects.
The C Standard, 6.5.7 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states the following about pointer arithmetic:
> When an expression that has integer type is added to or subtracted from a pointer, the result has the type of the pointer operand. If the pointer operand points to an element of an array object, and the array is large enough, the result points to an element offset from the original element such that the difference of the subscripts of the resulting and original array elements equals the integer expression.

## Noncompliant Code Example
This noncompliant code example attempts to access structure members using pointer arithmetic. This practice is dangerous because structure members are not guaranteed to be contiguous.
``` c
struct numbers {
  short num_a, num_b, num_c;
};
int sum_numbers(const struct numbers *numb){
  int total = 0;
  const short *numb_ptr;
  for (numb_ptr = &numb->num_a;
       numb_ptr <= &numb->num_c;
       numb_ptr++) {
    total += *(numb_ptr);
  }
  return total;
}
int main(void) {
  struct numbers my_numbers = { 1, 2, 3 };
  sum_numbers(&my_numbers);
  return 0;
}
```
## Compliant Solution
It is possible to use the `->` operator to dereference each structure member:
``` c
total = numb->num_a + numb->num_b + numb->num_c;
```
However, this solution results in code that is hard to write and hard to maintain (especially if there are many more structure members), which is exactly what the author of the noncompliant code example was likely trying to avoid.
## Compliant Solution
A better solution is to define the structure to contain an array member to store the numbers in an array rather than a structure, as in this compliant solution:
``` c
#include <stddef.h>
struct numbers {
  short a[3];
};
int sum_numbers(const short *numb, size_t dim) {
  int total = 0;
  for (size_t i = 0; i < dim; ++i) {
    total += numb[i];
  }
  return total;
}
int main(void) {
  struct numbers my_numbers = { .a[0]= 1, .a[1]= 2, .a[2]= 3};
  sum_numbers(
    my_numbers.a,
    sizeof(my_numbers.a)/sizeof(my_numbers.a[0])
  );
  return 0;
}
```
Array elements are guaranteed to be contiguous in memory, so this solution is completely portable.
## Exceptions
**ARR37-C-EX1:** Any non-array object in memory can be considered an array consisting of one element. Adding one to a pointer for such an object yields a pointer one element past the array, and subtracting one from that pointer yields the original pointer. This allows for code such as the following:
``` c
#include <stdlib.h>
#include <string.h>
struct s {
  char *c_str;
  /* Other members */
};
struct s *create_s(const char *c_str) {
  struct s *ret;
  size_t len = strlen(c_str) + 1;
  ret = (struct s *)malloc(sizeof(struct s) + len);
  if (ret != NULL) {
    ret->c_str = (char *)(ret + 1);
    memcpy(ret + 1, c_str, len);
  }
  return ret;
}
```
A more general and safer solution to this problem is to use a flexible array member that guarantees the array that follows the structure is properly aligned by inserting padding, if necessary, between it and the member that immediately precedes it.
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR37-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2004 Rule 17.4. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR37 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.BU
LANG.STRUCT.PARITH
LANG.STRUCT.PBB
LANG.STRUCT.PPE
LANG.MEM.TBA
LANG.MEM.TO
LANG.MEM.TU | Buffer OverrunBuffer Underrun
Pointer Arithmetic
Pointer Before Beginning of Object
Pointer Past End of Object
Tainted Buffer Access
Type Overrun
Type Underrun |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | ARRAY_VS_SINGLETON | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-arr37-c |  |
| Helix QAC | 2024.4 | DF2930, DF2931, DF2932, DF2933C++3705, C++3706, C++3707 |  |
| Klocwork | 2024.4 | MISRA.PTR.ARITH.2012 |  |
| LDRA tool suite | ;9.7.1 | 567 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR37-a | Pointer arithmetic shall not be applied to pointers that address variables of non-array type |
| PC-lint Plus | 1.4 | 2662 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule ARR37-C | Checks for invalid assumptions about memory organization (rule partially covered) |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2004 Rule 17.4. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR37-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|

## Bibliography

|  |  |
| ----|----|
| [Banahan 2003] | Section 5.3, "Pointers"Section 5.7, "Expressions Involving Pointers" |
| [ISO/IEC 9899:2024] | 6.5.7, "Additive Operators" |
| [VU#162289] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152341) [](../c/Rule%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151963)
## Comments:

|  |
| ----|
| I believe it is technically valid for a pointer that points to an object to be incremented, eg:
int x;
int *ptr = &x;
ptr++; /* valid, but can't dereference ptr */
ptr--; /* valid, ptr is &x again */

However, one can argue that if one wishes to do arithmetic on a pointer, that pointer should point to an array (or be cast to point to an array). The above code example could have been rewritten:
``` java
int x[1];
int *ptr = &x;
ptr++; /* valid, but can't dereference ptr */
ptr--; /* valid, ptr is &x again */
```
As for ROSE checkability, one can merely highlight arithmetic to pointers that have not been initialized (or assigned) to point to an array.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 24, 2008 16:23
\| \|
Really? What about...
``` java
char arr[] = "foo";
char * a = arr;
char * b = a;
*(b+2) = 'c';
```
`b` was never initialized or assigned to point to an array, and yet the arithmetic is OK. What I'm trying to say is this involves tainting variables and flow control, which we know as being super tough under ROSE.
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 10, 2008 10:55
\| \|
I'm not sure I would call flow control analysis 'super tough'...it is merely a harder level of problem than we have currently tried to solve. But I do think others have done flow control analysis using ROSE...
Your point is valid although the example is not (it tries to modify a string literal; we have a rule against that ![](images/icons/emoticons/smile.svg) It's pretty easy to validate a, and consequently validate b. A better example might replace your second line with:
``` java
  char * a = get_string();
```
where we don't know that get_string() returns a valid array; it might return NULL, after all. In that case, for now, we should probably 'give up', and either ignore the code sample, or issue a warning that 'this var might not point to a sufficient array'. This might be a good argument for adding a 'sensitivity' parameter to ROSE, that indicates how willing we are to tolerate false positives...we print the warning if the sensitivity parameter is sufficiently high.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 11, 2008 11:32
\| \|
My example is not invalid... `arr[]` is an initialized array, not a string literal, so writing to it is OK
As for checking whether a variable points to an array, I could imagine backtracking up a chain of assignments until we see an Sg\*AssignOp with an SgArrayType on the rhs? My biggest issue is, how do we differentiate cases where the backtrace fails due to complicated code/function calls/etc, and when it fails because the var actually does not point to an array.
To flag this, we need to identify cases where a variable does not point to an array, and doing so with any reasonable certainty seems impossible.
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 11, 2008 12:33
\| \|
After discussion with Alex, we decided that this rule is still implementable in ROSE (tho it may not be terribly useful). The method we use is:
-   Search for any pointer arithmetic on a pointer
-   Search for any assignment to that pointer
-   If the pointer is being assigned to point to an expression that can be determined (at compile time) to NOT be an array index (as in the NCCE), report a violation. If the pointer is being assigned the value of another pointer, do nothing.
We need to see some more code samples to determine just how feasible this is. It may not actually catch more than the NCCE.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 11, 2008 13:16
\| \|
yozo found this.
in the non-compliant example, the for loop should be corrected as follows:
for (numb_ptr = &numb-\>num1; numb_ptr \<= &numb-\>num9;  
numb_ptr++)
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Oct 16, 2008 02:28
\| \|
Thanks, I've made this change.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Oct 16, 2008 11:13
\| \|
Should the title be "Do not add or subtract an integer to a pointer to *an element of* a non-array object?"; But then does it make sense to say that a non-array object has "elements?"  Maybe the title should be "Only perform pointer arithmetic on a pointer to an array element."
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Apr 30, 2009 14:39
\| \|
I think the best title depends on whether you prefer technical accuracy or simplicity in your titles. In this case I vote for simplicity: "Only perform pointer arithmetic on pointers that point into arrays".
Pointer arithmetic is explained in full technical detail in C99 Section 6.5.6, paragraphs 7, 8, 9, and it really can't be expressed simply w/o sacrificing technical accuracy. The body of the rule should provide the accuracy and the title should provide the simplicity IMO.
My suggested title is technically good, but overly restrictive. The exceptions (which should prob go into the rule) are:
-   you can add or subtract 0 from any valid pointer, since it's a nop.
-   A pointer to a valid (non-array) object can be incremented, in which case it points to 'past the object'. Dereferencing it is undefined. But it can be decremented, in which case it points back to the object. That last item also applies to the last item in an array. But the rule already explains that.
Comments?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 30, 2009 16:18
\| \|
I'm having trouble with this rule. According to the definition of [valid pointer](BB.-Definitions_87152273.html#BB.Definitions-validpointer) (quoted below), this standard doesn't distinguish between a standalone object and an element of an array of size 1.
> ...a pointer to an object that is not an element of an array behaves the same as a pointer to the first element of an array of length one with the type of the object as its element type.

Thus, this rule (and indeed the only non-compliant code example provided in it) is just a special case of [ARR38-C. Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element](/confluence/pages/createpage.action?spaceKey=c&title=ARR38-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element) combined with [ARR30-C. Guarantee that array indices are within the valid range](/confluence/pages/createpage.action?spaceKey=c&title=ARR30-C.+Guarantee+that+array+indices+are+within+the+valid+range).
In addition, not only is it perfectly valid to add or subtract 0 from any valid pointer (as it is valid to add or subtract 0 from the null pointer), but it is also valid to add 1 to a pointer to any object (with the result still being a valid pointer).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 17, 2010 14:11
\| \|
Well, I'm on the fence, put I'll argue for keeping this just to ensure we've considered this decision.
C99 states:
> For the purposes of these operators, a pointer to an object that is not an element of an array behaves the same as a pointer to the first element of an array of length one with the type of the object as its element type.

This looks like the same thing you quoted, but I believe this says that "For purposes of these operators" a scalar is the same as an array of one value. It doesn't say that these two things can't be differentiated for some purpose.
The intent of this guideline is to further restrict (or subset) the standard. We certainly want to be very careful in doing something like this, but I can't think of use case where it makes sense to perform arithmetic with a pointer to anything other than an array (I'm pretty sure the effective type of the object referenced by char \*c = malloc(100) is array of char)
You could make an argument that this guideline is covered by the other guidelines you referenced, particularly ARR38-C, but this guideline I think makes it clear that arithmetic on non-array pointers is disallowed. The other solution would be to add this as a NCE/CS pair to ARR38-C but it might get lost a little because that guideline seems to be more about creating a pointer that lies outside the bounds of an array.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 17, 2010 14:49
\| \|
Seconded, I think this rule is worthwhile. We do reserve the 'right' to prohibit things that are valid C99, if we think they still indicate security flaws. So disallowing pointer arithmetic on non-arrays seems a reasonable restriction, esp. if no one can cite a legitimate reason for **not** doing so.
I can think of two borderline cases. I don't think either invalidates this rule, but they should both be considered:
-   Performing pointer arithmetic on a struct. I forget where, but C99 specifically allows a struct to be cast to an array of char of the same size.
<!-- -->
-   Serialization / deserialization. This often involves taking some memory owned by data, treating it as an array of chars and writing it to a file or socket. Deserialization often reads in data with implicit types and then casts to those types. I guess since it is usually treated as a char array, it's also not breaking this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 18, 2010 09:01
\| \|
Here's a common use case of treating a non-array object as an array of one element which is effectively prohibited by this rule even though it is safe and doesn't violate either [VOID Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element](VOID%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20if%20the%20resulting%20value%20does%20not%20refer%20to%20a%20valid%20array%20element) or [ARR30-C. Do not form or use out of bounds pointers or array subscripts](/confluence/pages/createpage.action?spaceKey=c&title=ARR30-C.+Do+not+form+or+use+out+of+bounds+pointers+or+array+subscripts).
``` java
struct int_pair { int first; int last; };
/* read n elements of struct int_pair into the ip array */
size_t read_int_pairs(FILE *stream, struct int_pair *ip, size_t n) {
  size_t nread, i;
  for (i = 0, nread = 0; i != n; ++i, ++nread) {
    if (1 != fread(ip + i, sizeof *ip, 1, stream))
      break;
  }
  return nread;  
}
int main() {
  struct int_pair p;
  /* read just one object */
  read_int_pairs(stream, &ip, 1);
  return 0;
```
You're right that C99 allows every non-bit field object to be treated as an array of bytes (`unsigned char`). This is discussed in [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 18, 2010 17:42
\| \|
If the decision is to retain this rule I believe that, at minimum, an exception should be added to make it possible to treat an object as an array of `unsigned char`, otherwise there's would be no way to implement user-defined variants of `memset()` or `memcpy()` without violating this standard.
But I do still think this rule is overly restrictive and the decision to prohibit treating non-array objects of any type equivalently to arrays of a single element should be reconsidered. To avoid violating the rule, programmers whose code is subject to this standard would have to define all objects that might be potentially treated as arrays as arrays of size 1. That's an infeasible requirement in systems consisting of libraries or modules whose public APIs expose individual objects.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 10, 2011 20:09
\| \|
One common use case for pointer arithmetic is for allocation locality:
``` java
#include <stdlib.h>
#include <string.h>
;
struct s {
  char *str;
  /* Other fields */
};
struct s *create_s(const char *str) {
  struct s *ret;
  size_t len = strlen(str) + 1;
  ret = (struct s *)malloc(sizeof(struct s) + len);
  ret->str = (char *)(ret + 1);
  memcpy(ret + 1, str, len);
  return ret;
}
```
I think the rule is overly restrictive as it disallows this sort of usage because `struct s` is not being used as an array.  Also, as Martin points out further down, usage of `unsigned char *` should probably be specifically allowed, otherwise `memset()` becomes impossible to write.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 09, 2013 14:44
\| \|
This rule needs an exception that every object in memory that is not part of an array can be considered an array of 1 element. So adding 1 to such a pointer puts it one past the array, and subtracting it puts it back at the object again. All valid by C11.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 14, 2013 16:39
\| \|
This rule needs a reference to offsetof(), which is a valid way to do pointer arithmetic inside a structure.
Given:
``` cpp
struct foo {
    ...
    sometype elem;
    ...
};
size_t off = offsetof(struct foo, elem);
struct foo *p = get_a_foo();
```
it is valid to do
``` cpp
sometype st = *(sometype *)((char *)p + off);
```
This tends to be most interesting when the reference is done by code that isn't familiar with the insides of struct foo, or when it's desirable to do some kind of table-driven walk of the elements of the structure.
![](images/icons/contenttypes/comment_16.png) Posted by jordanbrown at Jan 02, 2014 13:41
\| \|
`The offsetof` macro is used in the related rule [ARR39-C. Do not add or subtract a scaled integer to a pointer](https://www.securecoding.cert.org/confluence/display/seccode/ARR39-C.+Do+not+add+or+subtract+a+scaled+integer+to+a+pointer).; I think your main concern of how to use pointer arithmetic within a struct is covered in **ARR37-EX1**.  This example could have used the `offsetof` macro, but it is not necessary that it does.  I think the other rule does a good job of showing the issues surrounding the use of this macro.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 03, 2014 03:53
\| \|
This rule seems to say that there's no valid way to do pointer arithmetic to walk around inside a structure.; My point is that offsetof() supplies such a way, and so should be listed as an exception.  It must be used with care, as ARR39-C shows, but it's a valid and portable mechanism if used correctly.  (Well, unless one decides that almost all pointer arithmetic and casting is too dangerous and error-prone, but personally I think that's too high a cost.)
![](images/icons/contenttypes/comment_16.png) Posted by jordanbrown at Jan 03, 2014 14:34
\| \|
The exception ARR37-EX1 provides a way to perform pointer arithmetic within a structure by observing that "All non-array objects in memory can be considered an array of one element."; The example then shows addition to a struct pointer.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 13, 2014 10:07
\| \|
As best I can tell, you and Jordan are both approaching the same concept from different angles. So this is me taking a stab at interpreting...
I think Jordan is discussing the fact that the title says "Do not add or subtract an integer to a pointer to a non-array object", and yet you can clearly use;`offsetof()` to gain the offset of an element within a structure object.
I think Robert is discussing the fact that once you have that offset within the structure, the only safe way to use it for pointer arithmetic is to treat the object as an array of `unsigned char` so that you do not get pointer scaling when performing the arithmetic.
So you're both right, but I agree with Robert's assessment that a discussion of `offsetof()` doesn't really belong in this rule except perhaps as an NCCE.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 13, 2014 14:00
\|
