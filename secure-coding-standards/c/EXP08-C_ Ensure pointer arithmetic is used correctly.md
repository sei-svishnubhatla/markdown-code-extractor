When performing pointer arithmetic, the size of the value to add to a pointer is automatically scaled to the size of the type of the pointed-to object. For instance, when adding a value to the byte address of a 4-byte integer, the value is scaled by a factor of 4 and then added to the pointer. Failing to understand how pointer arithmetic works can lead to miscalculations that result in serious errors, such as buffer overflows.
## Noncompliant Code Example
In this noncompliant code example, integer values returned by `parseint(getdata())` are stored into an array of `INTBUFSIZE` elements of type `int` called `buf` \[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\]. If data is available for insertion into `buf` (which is indicated by `havedata()`) and `buf_ptr` has not been incremented past `buf + sizeof(buf)`, an integer value is stored at the address referenced by `buf_ptr`. However, the `sizeof` operator returns the total number of bytes in `buf`, which is typically a multiple of the number of elements in `buf`. This value is scaled to the size of an integer and added to `buf`. As a result, the check to make sure integers are not written past the end of `buf` is incorrect, and a buffer overflow is possible.
``` c
int buf[INTBUFSIZE];
int *buf_ptr = buf;
while (havedata() && buf_ptr < (buf + sizeof(buf))) {
  *buf_ptr++ = parseint(getdata());
}
```
## Compliant Solution
In this compliant solution, the size of `buf`, `INTBUFSIZE`, is added directly to `buf` and used as an upper bound. The integer literal `INTBUFSIZE` is scaled to the size of an integer, and the upper bound of `buf` is checked correctly.
``` c
int buf[INTBUFSIZE];
int *buf_ptr = buf;
while (havedata() && buf_ptr < (buf + INTBUFSIZE)) {
  *buf_ptr++ = parseint(getdata());
}
```
An arguably better solution is to use the address of the nonexistent element following the end of the array, as follows:
``` c
int buf[INTBUFSIZE];
int *buf_ptr = buf;
while (havedata() && buf_ptr < &buf[INTBUFSIZE]) {
  *buf_ptr++ = parseint(getdata());
}
```
This solution works because the C Standard guarantees the address of `buf[INTBUFSIZE]` even though no such element exists.
## Noncompliant Code Example
This noncompliant code example is based on a flaw in the OpenBSD operating system. An integer, `skip`, is added as an offset to a pointer of type `struct big`. The adjusted pointer is then used as a destination address in a call to `memset()`. However, when `skip` is added to the `struct big` pointer, it is automatically scaled by the size of `struct big`, which is 32 bytes (assuming 4-byte integers, 8-byte `long long` integers, and no structure padding). This scaling results in the call to `memset()` writing to unintended memory.
``` c
struct big {
  unsigned long long ull_1; /* Typically 8 bytes */
  unsigned long long ull_2; /* Typically 8 bytes */
  unsigned long long ull_3; /* Typically 8 bytes */
  int si_4; /* Typically 4 bytes */
  int si_5; /* Typically 4 bytes */
};
/* ... */
int f(void) {
  size_t skip = offsetof(struct big, ull_2);
  struct big *s = (struct big *)malloc(sizeof(struct big));
  if (!s) {
   return -1; /* Indicate malloc() failure */
  }
  memset(s + skip, 0, sizeof(struct big) - skip);
  /* ... */
  free(s);
  s = NULL;
  return 0;
}
```
A similar situation occurred in OpenBSD's `make` command \[[Murenin 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Murenin07)\].
## Compliant Solution
To correct this example, the `struct big` pointer is cast as a `char *`, which causes `skip` to be scaled by a factor of 1:
``` c
struct big {
  unsigned long long ull_1; /* Typically 8 bytes */
  unsigned long long ull_2; /* Typically 8 bytes */
  unsigned long long ull_3; /* Typically 8 bytes */
  int si_4; /* Typically 4 bytes */
  int si_5; /* Typically 4 bytes */
};
/* ... */
int f(void) {
  size_t skip = offsetof(struct big, ull_2);
  struct big *s = (struct big *)malloc(sizeof(struct big));
  if (!s) {
    return -1; /* Indicate malloc() failure */
  }
  memset((char *)s + skip, 0, sizeof(struct big) - skip);
/* ... */
  free(s);
  s = NULL;
  return 0;
}
```
## Risk Assessment
Failure to understand and properly use pointer arithmetic can allow an attacker to execute arbitrary code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP08-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports potential runtime errors resulting from invalid pointer arithmetics. |
| CodeSonar | 8.3p0 | LANG.STRUCT.PARITHLANG.MEM.BO
LANG.MEM.BU
LANG.STRUCT.PBB
LANG.STRUCT.PPE
LANG.MEM.TBA
LANG.MEM.TO
LANG.MEM.TU
LANG.STRUCT.CUP
LANG.STRUCT.SUP
 | Pointer arithmeticBuffer overrun
Buffer underrun
Pointer before beginning of object
Pointer past end of object
Tainted buffer access
Type overrun
Type underrun
Comparison of Unrelated Pointers
Subtraction of Unrelated Pointers |
| Helix QAC | 2024.4 | C0488, C2930, C2931, C2932, C2933 |  |
| Klocwork | 2024.4 | ABV.ITERATORABV.GENERAL
ABV.GENERAL.MULTIDIMENSION |  |
| LDRA tool suite | 9.7.1 | 45 D53 D
54 D
438 S
576 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP08-aCERT_C-EXP08-b
 | Pointer arithmetic should not be usedAvoid accessing arrays out of bounds |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 416 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP08-C | Checks for:Pointer points outside array after arithmetic on pointer operandSubtraction between pointers to different arraysIncorrect pointer scalingRec. fully supported. |
| PVS-Studio | 7.35 | V503, V520, V574, V600, V613, V619, V620, V643, V650, V687, V769, V1004 |  |

How long is 4 yards plus 3 feet? It is obvious from elementary arithmetic that any answer involving 7 is wrong, as the student did not take the units into account. The right method is to convert both numbers to reflect the same units.
The examples in this rule reflect both a correct and an incorrect way to handle comparisons of numbers representing different things (either single bytes or multibyte data structures). The noncompliant examples just add the numbers without regard to units, whereas the compliant solutions use type casts to convert one number to the appropriate unit of the other number.
ROSE can catch both noncompliant examples by searching for pointer arithmetic expressions involving different units. The "different units" is the tricky part, but you can try to identify an expression's units using some simple heuristics:
-   A pointer to a `foo` object has `foo` as the unit.
-   A pointer to `char *` has byte as the unit.
-   Any `sizeof` or `offsetof` expression also has unit byte as the unit.
-   Any variable used in an index to an array of `foo` objects (e.g., `foo[variable]`) has `foo` as the unit.
In addition to pointer arithmetic expressions, you can also hunt for array index expressions, as `array[index]` is merely shorthand for "`array + index`."
### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP08-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP08-CPP. Ensure pointer arithmetic is used correctly |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC]Pointer Arithmetic [RVG] |
| ISO/IEC TS 17961 | Forming or using out-of-bounds pointers or array subscripts [invptr] |
| MISRA C:2012 | Rule 18.1 (required)Rule 18.2 (required)
Rule 18.3 (required)
Rule 18.4 (advisory) |
| MITRE CWE | CWE-468, Incorrect pointer scaling |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [Murenin 2007] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152149) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152073)
## Comments:

|  |
| ----|
| Shouldn't the second example be using offsetof() instead of trying to count offsets directly?
Or wouldn't the code be a lot easier to understand if it had been rewritten as:
const unsigned long long ulsave = s->ull_1;  /* save first member */
memset(s, 0, sizeof *s);
s->ull_1 = ullsave; /* put first member back */

\*Poof\* - no funky pointer stuff.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 13:43
\| \|
I implemented the `offsetof()` solution because it looks cleaner to me and does not add run-time overhead.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 14, 2008 14:58
\| \|
The offsetof() solution is the right one, though at times I do make minor concessions to runtime performance if I think it will make the code easier to understand by the next guy who has to work on my code. Clarity breeds maintainability.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 15:09
\| \|
The first compliant example could alternatively use `sizeof(buf)/sizeof(buf[0])`, which represents the standard idiom for checking the size of an array.
![](images/icons/contenttypes/comment_16.png) Posted by josh@freedesktop.org at Mar 16, 2008 06:44
\| \|
The first example is better coded:
``` java
int buf[INTBUFSIZE];
int *buf_ptr = buf;
while (havedata() && buf_ptr < &buf[INTBUFSIZE] {
  *buf_ptr++ = parseint(getdata());
}
```
since "the Standard endorses existing practice by guaranteeing that it's permissible to use the address of buf\[INTBUFSIZE\] even though no such element exists." (from The C Book, by Mike Banahan). This is clearer and less  
error-prone than the alternatives
![](images/icons/contenttypes/comment_16.png) Posted by partner55040717@vansoftcorp.com at Apr 10, 2008 14:28
\| \|
OK, it took me a while, but I'll buy this. Added as a "arguably better" compliant solution.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 16, 2008 09:45
\| \|
As i just commented elsewhere, this problem this practice attempts to prevent is the subject of [ARR30-C. Do not form or use out of bounds pointers or array subscripts](/confluence/pages/createpage.action?spaceKey=c&title=ARR30-C.+Do+not+form+or+use+out+of+bounds+pointers+or+array+subscripts). I suggest this recommendation be moved into [99. The Void](/confluence/pages/createpage.action?spaceKey=c&title=99.+The+Void) (perhaps after copying the first NCCE into ARR30-C, if we'd like to preserve it).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 10, 2011 19:49
\| \|
The while condition for this example is missing the closing right parenthesis.
![](images/icons/contenttypes/comment_16.png) Posted by alex at Sep 18, 2018 10:35
\| \|
Fixed, thanx
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 18, 2018 13:47
\|
