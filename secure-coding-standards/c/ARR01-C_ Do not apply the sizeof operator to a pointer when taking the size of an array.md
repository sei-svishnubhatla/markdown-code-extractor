The `sizeof` operator yields the size (in bytes) of its operand, which can be an expression or the parenthesized name of a type. However, using the `sizeof` operator to determine the size of arrays is error prone.
The `sizeof` operator is often used in determining how much memory to allocate via `malloc()`. However using an incorrect size is a violation of [MEM35-C. Allocate sufficient memory for an object](MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object).
## Noncompliant Code Example
In this noncompliant code example, the function `clear()` zeros the elements in an array. The function has one parameter declared as `int array[]` and is passed a static array consisting of 12 `int` as the argument. The function `clear()` uses the idiom `sizeof(array) / sizeof(array[0])` to determine the number of elements in the array. However, `array` has a pointer type because it is a parameter. As a result, `sizeof(array)` is equal to the `sizeof(int *)`. For example, on an architecture (such as IA-32) where the `sizeof(int) == 4` and the `sizeof(int *) == 4`, the expression `sizeof(array) / sizeof(array[0])` evaluates to 1, regardless of the length of the array passed, leaving the rest of the array unaffected.
``` c
void clear(int array[]) {
  for (size_t i = 0; i < sizeof(array) / sizeof(array[0]); ++i) {
     array[i] = 0;
   }
}
void dowork(void) {
  int dis[12];
  clear(dis);
  /* ... */
}
```
Footnote 103 in subclause 6.5.3.4 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] applies to all array parameters:
> When applied to a parameter declared to have array or function type, the `sizeof` operator yields the size of the adjusted (pointer) type.

## Compliant Solution
In this compliant solution, the size of the array is determined inside the block in which it is declared and passed as an argument to the function:
``` c
void clear(int array[], size_t len) {
  for (size_t i = 0; i < len; i++) {
    array[i] = 0;
  }
}
void dowork(void) {
  int dis[12];
  clear(dis, sizeof(dis) / sizeof(dis[0]));
  /* ... */
}
```
This `sizeof(array) / sizeof(array[0])` idiom will succeed provided the original definition of `array` is visible.
## Noncompliant Code Example
In this noncompliant code example, `sizeof(a)` does not equal `100 * sizeof(int)`, because the `sizeof` operator, when applied to a parameter declared to have array type, yields the size of the adjusted (pointer) type even if the parameter declaration specifies a length:
``` c
enum {ARR_LEN = 100};
void clear(int a[ARR_LEN]) {
  memset(a, 0, sizeof(a)); /* Error */
}
int main(void) {
  int b[ARR_LEN];
  clear(b);
  assert(b[ARR_LEN / 2]==0); /* May fail */
  return 0;
}
```
## Compliant Solution
In this compliant solution, the size is specified using the expression `len * sizeof(int)`:
``` c
enum {ARR_LEN = 100};
void clear(int a[], size_t len) {
  memset(a, 0, len * sizeof(int));
}
int main(void) {
  int b[ARR_LEN];
  clear(b, ARR_LEN);
  assert(b[ARR_LEN / 2]==0); /* Cannot fail */
  return 0;
}
```
## Risk Assessment
Incorrectly using the `sizeof` operator to determine the size of an array can result in a buffer overflow, allowing the execution of arbitrary code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR01-C | High | Probable | Low | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | sizeof-array-parameter | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR01 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.TYPE.SAP | sizeof Array Parameter |
| Compass/ROSE |  |  | Can detect violations of the recommendation but cannot distinguish between incomplete array declarations and pointer declarations |
| Klocwork | 2024.4 | CWARN.MEMSET.SIZEOF.PTR | Fully implemented |
| LDRA tool suite | 9.7.1 | 401 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR01-a | Do not call 'sizeof' on a pointer type |
| PC-lint Plus | 1.4 | 682, 882 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. ARR01-C | Checks for:Wrong type used in sizeofPossible misuse of sizeofRec, fully covered. |
| Splint | 3.1.1 |  |  |
| PVS-Studio | 7.35 | V511, V512, V514, V568, V579, V604, V697, V1086 |  |
| RuleChecker | 24.04 | sizeof-array-parameter | Fully checked |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR01-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | CTR01-CPP. Do not apply the sizeof operator to a pointer when taking the size of an array | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-467, Use of sizeof() on a pointer type | Prior to 2018-01-12: CERT: |
| ISO/IEC TS 17961 | Taking the size of a pointer to determine the size of the pointed-to type [sizeofptr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MITRE CWE | CWE-569 | Prior to 2018-01-12: |
| MITRE CWE | CWE-783 | Prior to 2018-01-12: |

## Bibliography

|  |  |
| ----|----|
| [Drepper 2006] | Section 2.1.1, "Respecting Memory Bounds" |
| [ISO/IEC 9899:2011] | Subclause 6.5.3.4, "The sizeof and _Alignof Operators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152117) [](../c/Rec_%2006_%20Arrays%20_ARR_) [](../c/ARR02-C_%20Explicitly%20specify%20array%20bounds,%20even%20if%20implicitly%20defined%20by%20an%20initializer)
## Comments:

|  |
| ----|
| We may want to show another NCCE, where sizeof(array) / sizeof(array[0]) is used in other dangerous ways.  If not, we may want to just make these example to be part of the test suite.
                                        Posted by rcs at May 25, 2008 09:13
                                     |
| Per the discussion between me, David, and Robert:
We first thought that this title should be "Do not apply the sizeof operator to array parameters" to make it more concrete and to help with static tool analysis.; However, we thought of an example that would fit the current title:
char arg[SIZE] = /* ... */
char *ptr = arg;
printf("%d\n", sizeof(ptr));

Thoughts on changing the title, including this NCCE, splitting this into two recommendations, or (my favorite) making a recommendation that says "Do not use sizeof on pointers"?
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Apr 29, 2009 11:55
\| \|
I thought of a more likely scenario:
``` java
char *str = "Hello, world";
/* I can never remember if it's strlen(str) + 1 or -1. */
char *str2 = (char *)malloc(sizeof(str));  /* Woops, got 4 instead of strlen(str) + 1. */
```
![](images/icons/contenttypes/comment_16.png) Posted by akeeton at Apr 29, 2009 12:15
\| \|
Should this rule also detect this kind of error?
``` java
        unsigned char   string[SIZE];
        memset(&string, 0, sizeof(string));
```
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 09, 2010 10:17
\| \|
What makes you think the code is in error? The address of an array is the address of its first element so the snippet simply zeroes out the array.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 11, 2010 18:36
\| \|
Why is this not a rule but a recommendation? Clearly applying the "sizeof operator to a pointer" does not work when one is "taking the size of an array", i.e. the title is a bit of a contradiction in terms in my non-native ears. In any case this easily leads to miscalculated sizes of objects and thus potential OOB accesses, so why not make it a rule?
![](images/icons/contenttypes/comment_16.png) Posted by stefanct at Aug 24, 2018 11:36
\| \|
Because violations of this recommendation also violate [MEM35-C. Allocate sufficient memory for an object](MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 10, 2018 14:01
\| \|
The coderwall explains in Some detail the theory of how best to get the size of an array in C++ https://coderwall.com/p/nb9ngq/better-getting-array-size-in-c
![](images/icons/contenttypes/comment_16.png) Posted by ryshevv at Oct 14, 2020 16:24
\| \|
Interesting. I would guess that, like the sizeof trick, the template only applies to arrays whose sizes are known at compile time. Trying to pass a pointer to that template would yield a compiler error. Which is admittedly better than having the computer return the "wrong" value for the szieof ratio.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 15, 2020 07:40
\| \|
An even better approach is to use;`std::size()` <https://en.cppreference.com/w/cpp/iterator/size> since it's defined for you (in C++17 and later).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 15, 2020 08:24
\| \|
Note that there's also the much less common pointer-to-array type you **could** use here, as it preserve the array size.
`#include <stddef.h>``#include <stdio.h>`
`void clear(int (*parray)[12]) {`  
`    printf("sizeof parray: %d\n", sizeof(parray));`  
`    printf("sizeof *parray: %d\n", sizeof(*parray));`  
`    printf("sizeof parray[0]: %d\n", sizeof(parray[0]));`  
`    printf("sizeof *parray[0]: %d\n", sizeof(*parray[0]));`  
`    printf("element count: %d\n", sizeof(*parray) / sizeof(*parray[0]));`  
`    for (size_t i = 0; i < sizeof(*parray) / sizeof(*parray[0]); ++i) {`  
`        *parray[i] = 0;`  
`    }`  
`}`  
` `  
`void main(void) {`  
`  int dis[12];`  
`  clear(&dis);`  
`}`
I wouldn't recommend it though, as the element counter is easy to mess up, especially when compared to the normal idiom.
![](images/icons/contenttypes/comment_16.png) Posted by poddster at Jan 06, 2022 12:07
\| \|
Agreed. I suspect the compiler is inferring some of those sizes at compile timel If you change the parray type; to \*\*int, you get completely different sizes.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 07, 2022 15:11
\| \|
Remember, though, that `int **` and `int (*)[12]` are incompatible types, and changing one to the other would break things even if they don't use `sizeof`.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jan 10, 2022 09:54
\|
