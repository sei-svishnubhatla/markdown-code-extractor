Although programmers often use integers and pointers interchangeably in C, pointer-to-integer and integer-to-pointer conversions are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior). 
Conversions between integers and pointers can have undesired consequences depending on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation).
According to the C Standard, subclause 6.3.2.3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> An integer may be converted to any pointer type. Except as previously specified, the result is implementation-defined, might not be correctly aligned, might not point to an entity of the referenced type, and might be a trap representation.
> Any pointer type may be converted to an integer type. Except as previously specified, the result is implementation-defined. If the result cannot be represented in the integer type, the behavior is undefined. The result need not be in the range of values of any integer type.

Do not convert an integer type to a pointer type if the resulting pointer is incorrectly aligned, does not point to an entity of the referenced type, or is a [trap representation](BB.-Definitions_87152273.html#BB.Definitions-traprepresentation).
Do not convert a pointer type to an integer type if the result cannot be represented in the integer type. (See [undefined behavior 23](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_23).)
The mapping between pointers and integers must be consistent with the addressing structure of the execution environment. Issues may arise, for example, on architectures that have a segmented memory model.
## Noncompliant Code Example
The size of a pointer can be greater than the size of an integer, such as in an implementation where pointers are 64 bits and unsigned integers are 32 bits. This code example is noncompliant on such implementations because the result of converting the 64-bit `ptr` cannot be represented in the 32-bit integer type:
``` c
void f(void) {
  char *ptr;
  /* ... */
  unsigned int number = (unsigned int)ptr;
  /* ... */
}
```
## Compliant Solution
Any valid pointer to `void` can be converted to `intptr_t` or `uintptr_t` and back with no change in value. (See **INT36-EX2**.) The C Standard guarantees that a pointer to `void` may be converted to or from a pointer to any object type and back again and that the result must compare equal to the original pointer. Consequently, converting directly from a `char *` pointer to a `uintptr_t`, as in this compliant solution, is allowed on implementations that support the `uintptr_t` type.
``` c
#include <stdint.h>
void f(void) {
  char *ptr;
  /* ... */
  uintptr_t number = (uintptr_t)ptr;  
  /* ... */
}
```
## Noncompliant Code Example
In this noncompliant code example, the pointer `ptr` is converted to an integer value. The high-order 9 bits of the number are used to hold a flag value, and the result is converted back into a pointer. This example is noncompliant on an implementation where pointers are 64 bits and unsigned integers are 32 bits because the result of converting the 64-bit `ptr` cannot be represented in the 32-bit integer type.
``` c
void func(unsigned int flag) {
  char *ptr;
  /* ... */
  unsigned int number = (unsigned int)ptr;
  number = (number & 0x7fffff) | (flag << 23);
  ptr = (char *)number;
}
```
A similar scheme was used in early versions of Emacs, limiting its portability and preventing the ability to edit files larger than 8MB.
## Compliant Solution
This compliant solution uses a `struct` to provide storage for both the pointer and the flag value. This solution is portable to machines of different word sizes, both smaller and larger than 32 bits, working even when pointers cannot be represented in any integer type. 
``` c
struct ptrflag {
  char *pointer;
  unsigned int flag : 9;
} ptrflag;
void func(unsigned int flag) {
  char *ptr;
  /* ... */
  ptrflag.pointer = ptr;
  ptrflag.flag = flag;
}
```
## Noncompliant Code Example
It is sometimes necessary to access memory at a specific location, requiring a literal integer to pointer conversion. In this noncompliant code, a pointer is set directly to an integer constant, where it is unknown whether the result will be as intended:
``` c
unsigned int *g(void) {
  unsigned int *ptr = 0xdeadbeef;
  /* ... */
  return ptr;
} 
```
The result of this assignment is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior), might not be correctly aligned, might not point to an entity of the referenced type, and might be a [trap representation](BB.-Definitions_87152273.html#BB.Definitions-traprepresentation).
## Compliant Solution
Unfortunately this code cannot be made safe while strictly conforming to ISO C.
A particular platform (that is, hardware, operating system, compiler, and Standard C library) might guarantee that a memory address is correctly aligned for the pointer type, and actually contains a value for that type. A common practice is to use addresses that are known to point to hardware that provides valid values.
## Exceptions
**INT36-C-EX1:** The integer value 0 can be converted to a pointer; it becomes the null pointer.
**INT36-C-EX2:** Any valid pointer to `void` can be converted to `intptr_t` or `uintptr_t` or their underlying types and back again with no change in value. Use of underlying types instead of `intptr_t` or `uintptr_t` is discouraged, however, because it limits portability.
``` c
#include <assert.h>
#include <stdint.h>
void h(void) {
  intptr_t i = (intptr_t)(void *)&i;
  uintptr_t j = (uintptr_t)(void *)&j;
  void *ip = (void *)i;
  void *jp = (void *)j;
  assert(ip == &i);
  assert(jp == &j);
}
```
## Risk Assessment
Converting from pointer to integer or vice versa results in code that is not portable and may create unexpected pointers to invalid memory locations.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT36-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-integral-castpointer-integral-cast-implicitfunction-pointer-integer-cast function-pointer-integer-cast-implicit | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT36 | Fully implemented |
| Clang | 3.9 | -Wint-to-pointer-cast, -Wint-conversion | Can detect some instances of this rule, but does not detect all |
| CodeSonar | 8.3p0 | LANG.CAST.PC.CONST2PTRLANG.CAST.PC.INT | Conversion: integer constant to pointerConversion: pointer/integer |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | PW.POINTER_CONVERSION_LOSES_BITS | Fully implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-int36-c |  |
| Helix QAC | 2024.4 | C0303, C0305, C0306, C0309, C0324, C0326, C0360, C0361, C0362C++3040, C++3041, C++3042, C++3043, C++3044, C++3045, C++3046, C++3047, C++3048 |  |
| Klocwork | 2024.4 | MISRA.CAST.OBJ_PTR_TO_INT.2012 |  |
| LDRA tool suite | 9.7.1 | 439 S, 440 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT36-b | A conversion should not be performed between a pointer to object type and an integer type other than 'uintptr_t' or 'intptr_t' |
| PC-lint Plus | 1.4 | 4287 | Partially supported: reports casts from pointer types to smaller integer types which lose information |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT36-C | Checks for unsafe conversion between pointer and integer (rule partially covered) |
| PVS-Studio | 7.35 | V527, V528,;V542, V566, V601, V647, V1091 |  |
| RuleChecker | 24.04 | pointer-integral-castpointer-integral-cast-implicitfunction-pointer-integer-cast function-pointer-integer-cast-implicit | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S1767 | Partially implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT36-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT11-CPP. Take care when converting from pointer to integer or integer to pointer | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Converting a pointer to integer or integer to pointer [intptrconv] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-587, Assignment of a Fixed Address to a Pointer | 2017-07-07: CERT: Partial overlap |
| CWE 2.11 | CWE-704 | 2017-06-14: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-758 | 2017-07-07: CERT: Rule subset of CWE |
| CWE 3.1 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2018-10-19:CERT:None |
| CWE 3.1 | CWE-466, Return of Pointer Value Outside of Expected Range | 2018-10-19:CERT:None |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-758 and INT36-C
Independent( INT34-C, INT36-C, MEM30-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( INT36-C, list) where list =
-   Undefined behavior that results from anything other than integer \<-\> pointer conversion
### CWE-704 and INT36-C
CWE-704 = Union( INT36-C, list) where list =
-   Incorrect (?) typecast that is not between integers and pointers
### CWE-587 and INT36-C
Intersection( CWE-587, INT36-C) =
-   Setting a pointer to an integer value that is ill-defined (trap representation, improperly aligned, mis-typed, etc)
CWE-587 – INT36-C =
-   Setting a pointer to a valid integer value (eg points to an object of the correct t ype)
INT36-C – CWE-587 =
-   Illegal pointer-to-integer conversion
Intersection(INT36-C,CWE-466) =  ∅  
Intersection(INT36-C,CWE-466) =  ∅
An example explaining the above two equations follows:
`static char x[3];`
`char* foo() {`
`  int x_int = (int) x; // x_int = 999 eg`
`  return x_int + 5; // returns 1004 , violates CWE 466`
`}`
`...`
`int y_int = foo(); // violates CWE-466`
`char* y = (char*) y_int; //  // well-defined but y may be invalid, violates INT36-C`
`char c = *y; // indeterminate value, out-of-bounds read, violates CWE-119`
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 6.3.2.3, "Pointers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151939) [](../c/Rule%2004_%20Integers%20_INT_) [](../c/Rule%2005_%20Floating%20Point%20_FLP_)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>uh, you should maybe rethink your identifiers and literals to be a little less colorful</p>
<p>i think this could probably be broken into two recommendations. part 1: NULL and 0 overlaps with:</p>
<p>EXP36-C. A pointer shall not be compared to NULL or assigned NULL, use plain 0 instead</p>
<p>but I think this rule has been abandoned and your content is better. I would take what you have and move it to that rule.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Apr 25, 2007 08:32
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I would add to that rule but honestly I think it is wrong. There are many schools of thought on the NULL/0 usage but to be honest, it doesn't actually matter. NULL is effectively the same as 0. If I had to make a suggestion, NULL should be used in the pointer context to keep your code straight, but with the awareness that they aren't any different ... </p>
<p>I'll get on to fixing the names. It was kind of a joke.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by sditmore at Apr 25, 2007 15:20
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Isn't this really a pointer rule, not an integer rule?</p>
<p>Wouldn't it be effectively the same rule if we said don't convert pointers to/from any other type?</p>
<p>Seems strange to call it an integer rule.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by wlf@cert.org at Apr 26, 2007 09:27
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>It's called an integer rule because of the old history of pointers being the same as integers. People are most likely to know they shouldn't go arbitrarly converting pointers to whatever, but they may not know that pointers are now different from integers.</p>
<p> With that said it's not the best rationale in the world, the big issue is there's no actual plain pointer section... show me where to put it/feel free to move it.</p>
<p> also I have not the best idea as to the vulnerability index so someone else might want to poke at that and see if it looks off.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by sditmore at Apr 26, 2007 17:30
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>This rule should have a prerequisite that sizeof(unsigned int*) is equal to sizeof(unsigned int). Right? How does the intpoint union work on platform with different size of int and pointer, such as LP64?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by zhenyuwu@gmail.com at Oct 23, 2007 09:40
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The recommendation has now been edited to take this into account.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dmk at Jan 17, 2008 09:08
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The second compliant solution is non-portable, because you are performing arithmetic on values of type intptr_t/uintptr_t.  All the C standard guarantees (7.18.1.4) is that you can convert void* values to intptr_t (or uintptr_t) and back again and end up with an equal value for the pointer.  Mathematical operations (including ==) are non-portable.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by stewartb at Mar 13, 2008 20:47
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>There is nothing wrong with performing arithmetic on an <code>intptr_t</code>.  The problem lies in where the values came from.  Since they came from pointers, the two values may not have any particular relation to each other.  This example has been deleted.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dmk at Mar 14, 2008 00:28
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The bit about conversion okay for 0 should be omitted, and it isn't pertinent and is stated too strongly.  Consider</p>
<p>intptr_t x = 0;<br />
double *p = (double *)x;  // result is not necessarily a null pointer!</p>
<p>This example should have a cast:</p>
<p>unsigned int *ptr = (unsigned int *)0xcfcfcfcf;</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dagwyn at Apr 15, 2008 16:55
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>This compliant solution</p>
<p><strong>Compliant Solution</strong></p>
<p>Adding an explicit cast may help the compiler convert the integer value into a valid pointer.</p>
<div class="table-wrap">
<pre class="table"><code>|  |
| ----|
| unsigned int *ptr = (unsigned int *) 0xcfcfcfcf; |</code></pre>
</div>
<p> </p>
<p>Is almost identical to this noncompliant solution from  TS 17961: </p>
<h2 id="INT36C.Convertingapointertointegerorintegertopointer-Convertingapointertointegerorintegertopointer[intptrconv]">Converting a pointer to integer or integer to pointer       [intptrconv]</h2>
<p> </p>
<p>EXAMPLE 2 In this noncompliant example, a diagnostic is required because the conversion of the integer literal 0xdeadbeef to a pointer that is not known to point to an entity of the referenced type.</p>
<pre><code>unsigned int *g(void) {</code></pre>
<pre><code>  unsigned int *ptr = (unsigned int *)0xdeadbeef;  // diagnostic required</code></pre>
<pre><code>  /* ... */</code></pre>
<pre><code>  return ptr;</code></pre>
<pre><code>}</code></pre>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jan 22, 2013 09:30
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I feel that, with a little more work, this recommendation can be promoted to a rule.  The remaining issue for me would be changing the emphasis from portability to security.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jan 22, 2013 09:30
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p><br />
</p>
<blockquote>
<h2 id="INT36C.Convertingapointertointegerorintegertopointer-NoncompliantCodeExample">Noncompliant Code Example</h2>
<p>It is sometimes necessary to access memory at a specific location, requiring a literal integer to pointer conversion. In this noncompliant code, a pointer is set directly to an integer constant, where it is unknown whether the result will be as intended:</p>
<div class="table-wrap">
<pre class="table"><code>|  |
| ----|
| unsigned;int *g(void) {
  unsigned int *ptr = 0xdeadbeef;
  /* ... */
  return ptr;
}  |</code></pre>
</div>
<p>The result of this assignment is <a href="https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-implementation-definedbehavior">implementation-defined</a>, might not be correctly aligned, might not point to an entity of the referenced type, and might be a <a href="https://wiki.sei.cmu.edu/confluence/display/c/BB.+Definitions#BB.Definitions-traprepresentation">trap representation</a>.</p>
<h2 id="INT36C.Convertingapointertointegerorintegertopointer-CompliantSolution">Compliant Solution</h2>
<p>Adding an explicit cast may help the compiler convert the integer value into a valid pointer. A common technique is to assign the integer to a volatile-qualified object of type <code>intptr_t</code> or <code>uintptr_t</code> and then assign the integer value to the pointer:</p>
<div class="table-wrap">
<pre class="table"><code>|  |
| ----|
| unsigned;int *g(void) {
  volatile uintptr_t iptr = 0xdeadbeef;
  unsigned int *ptr = (unsigned int *)iptr;
  /* ... */
  return ptr;
} |</code></pre>
</div>
<p><br />
</p>
</blockquote>
<p>This example confuses me a lot. As far as I know explicit cast does not do anything to help with alignment or any other mentioned issues, which means the implementation-defined behaviour would remain in the "complaint solution".</p>
<p>I would also like to ask what difference does <code>volatile</code> make here. Eliminating the auto variable <code>iptr</code> does not seem to break anything.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by idingdong at Mar 27, 2020 23:32
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I've just confirmed..."volatile" makes no difference here.  In fact, the compliant solution was really no better than the noncompliant code example it sought to improve on. So I replaced it with a disclaimer saying that such code leads to undefined behavior in C...though it may be well-defined on some platforms.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Apr 01, 2020 16:09
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Exception  <strong>INT36-C-EX1</strong> says:</p>
<blockquote>
<p>A null pointer can be converted to an integer; it takes on the value 0.</p>
</blockquote>
<p>It is not guaranteed. A null pointer produces implementation-defined value when converted to integer. It is true that integer constant expressions with the value 0 can be converted to null pointers, but not necessarily vice versa.</p>
<blockquote>
<p>Likewise, the integer value 0 can be converted to a pointer; it becomes the null pointer.</p>
</blockquote>
<p>Only integer constant expressions are well defined for that. Integer variables, or even non-constant const integers with value 0 will not be guaranteed to be converted to null pointers.</p>
<p>See also:</p>
<p><a href="https://stackoverflow.com/questions/2759845/why-is-address-zero-used-for-the-null-pointer">https://stackoverflow.com/questions/2759845/why-is-address-zero-used-for-the-null-pointer</a></p>
<p><a href="https://stackoverflow.com/questions/47528069/casting-null-pointers">https://stackoverflow.com/questions/47528069/casting-null-pointers</a></p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by idingdong at Apr 13, 2020 23:34
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Agreed. C17 6.3.2.3p6 specifies the problematic part of not being able to convert the null pointer to zero.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by aballman at Apr 14, 2020 07:20
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I removed that sentence. The exception now only permits casting 0 to a pointer, which becomes the null pointer, as is guaranteed by s6.2.3.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Apr 14, 2020 10:37
</div></td>
</tr>
</tbody>
</table>
