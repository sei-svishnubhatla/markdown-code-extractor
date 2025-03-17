If an integer expression involving an operation is compared to or assigned to a larger integer size, that integer expression should be evaluated in that larger size by explicitly casting one of the operands.
## Noncompliant Code Example
This code example is noncompliant on systems where `size_t` is an unsigned 32-bit value and `long long` is a 64-bit value. In this example, the programmer tests for wrapping by comparing `SIZE_MAX` to `length + BLOCK_HEADER_SIZE`. Because `length` is declared as `size_t`, the addition is performed as a 32-bit operation and can result in wrapping. The comparison with `SIZE_MAX` will always test false. If any wrapping occurs, `malloc()` will allocate insufficient space for `mBlock`, which can lead to a subsequent buffer overflow.
``` c
#include <stdlib.h>
#include <stdint.h>  /* For SIZE_MAX */
enum { BLOCK_HEADER_SIZE = 16 };
void *AllocateBlock(size_t length) {
  struct memBlock *mBlock;
  if (length + BLOCK_HEADER_SIZE > (unsigned long long)SIZE_MAX)
    return NULL;
  mBlock = (struct memBlock *)malloc(
    length + BLOCK_HEADER_SIZE
  );
  if (!mBlock) { return NULL; }
  /* Fill in block header and return data portion */
  return mBlock;
}
```
Some compilers will diagnose this condition.
## Compliant Solution (Upcast)
In this compliant solution, the `length` operand is upcast to `unsigned long long`, ensuring that the addition takes place in this size:
``` c
#include <stdlib.h>
#include <stdint.h>
enum { BLOCK_HEADER_SIZE = 16 };
void *AllocateBlock(size_t length) {
  struct memBlock *mBlock;
  if ((unsigned long long)length + BLOCK_HEADER_SIZE > SIZE_MAX) {
    return NULL;
  }
  mBlock = (struct memBlock *)malloc(
    length + BLOCK_HEADER_SIZE
  );
  if (!mBlock) { return NULL; }
  /* Fill in block header and return data portion */
  return mBlock;
}
```
This test for wrapping is effective only when the `sizeof(unsigned long long) > sizeof(size_t)`. If both `size_t` and `unsigned long long` types are represented as 64-bit unsigned values, the result of the addition operation may not be representable as an `unsigned long long` value.
## Compliant Solution (Rearrange Expression)
In this compliant solution, `length` is subtracted from `SIZE_MAX`, ensuring that wrapping cannot occur. See [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).
``` c
#include <stdlib.h>
#include <stdint.h>
enum { BLOCK_HEADER_SIZE = 16 };
void *AllocateBlock(size_t length) {
  struct memBlock *mBlock;
  if (SIZE_MAX - length < BLOCK_HEADER_SIZE) return NULL;
  mBlock = (struct memBlock *)malloc(
    length + BLOCK_HEADER_SIZE
  );
  if (!mBlock) { return NULL; }
  /* Fill in block header and return data portion */
  return mBlock;
}
```
## Noncompliant Code Example
In this noncompliant code example, the programmer attempts to prevent wrapping by allocating an `unsigned long long` integer called `alloc` and assigning it the result from `cBlocks * 16`:
``` c
#include <stdlib.h>
#include <limits.h>
void *AllocBlocks(size_t cBlocks) {
  if (cBlocks == 0) { return NULL; }
  unsigned long long alloc = cBlocks * 16;
  return (alloc < UINT_MAX) ? malloc(cBlocks * 16) : NULL;
}
```
Two problems occur in this noncompliant code example. The first problem is that this code assumes an [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) where `unsigned long long` has at least 4 more bits than `size_t`. The second problem, assuming an implementation where `size_t` is a 32-bit value and `unsigned long long` is represented by a 64-bit value, is that to be compliant with C, multiplying two 32-bit numbers in this context must yield a 32-bit result. Any wrapping resulting from this multiplication will remain undetected by this code, and the expression `alloc < UINT_MAX` will always be true.
## Compliant Solution
In this compliant solution, the `cBlocks` operand is upcast to `unsigned long long`, ensuring that the multiplication takes place in this size:
``` c
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
static_assert(
  CHAR_BIT * sizeof(unsigned long long) >= 
  CHAR_BIT * sizeof(size_t) + 4, 
  "Unable to detect wrapping after multiplication"
);
void *AllocBlocks(size_t cBlocks) {
  if (cBlocks == 0) return NULL;
  unsigned long long alloc = (unsigned long long)cBlocks * 16;
  return (alloc < UINT_MAX) ? malloc(cBlocks * 16) : NULL;
}
```
Note that this code does not prevent wrapping unless the `unsigned long long` type is at least 4 bits larger than `size_t`.
## Noncompliant Code Example (`size_t`)
The `mbstowcs()` function converts a multibyte string to a wide character string, returning the number of characters converted. If an invalid multibyte character is encountered, `mbstowcs()` returns `(size_t)(-1)`. Depending on how `size_t` is implemented, comparing the return value of `mbstowcs()` to signed integer literal `-1` may not evaluate as expected.
``` c
#include <stdlib.h>
void func(wchar_t *pwcs, const char *restrict s, size_t n) {
  size_t count_modified = mbstowcs(pwcs, s, n);
  if (count_modified == -1) {
    /* Handle error */
  }
}
```
## Compliant Solution (`size_t`)
To ensure the comparison is properly performed, the return value of `mbstowcs()` should be compared against `-1` cast to type `size_t`:
``` c
#include <stdlib.h>
void func(wchar_t *pwcs, const char *restrict s, size_t n) {
  size_t count_modified = mbstowcs(pwcs, s, n);
  if (count_modified == (size_t)-1) {
    /* Handle error */
  }
}
```
## Risk Assessment
Failure to cast integers before comparing or assigning them to a larger integer size can result in software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) that can allow the execution of arbitrary code by an attacker with the permissions of the vulnerable process.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT18-C | high | likely | medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | LANG.TYPE.AWIDLANG.TYPE.OWID
LANG.CAST.VALUE
LANG.CAST.COERCE
ALLOC.SIZE.ADDOFLOW
ALLOC.SIZE.IOFLOW
ALLOC.SIZE.MULOFLOW
ALLOC.SIZE.SUBUFLOW
ALLOC.SIZE.TRUNC
MISC.MEM.SIZE.ADDOFLOW
MISC.MEM.SIZE.BAD
MISC.MEM.SIZE.MULOFLOW
MISC.MEM.SIZE.SUBUFLOW
MISC.MEM.SIZE.TRUNC | Expression value widened by assignmentExpression value widened by other operand
Cast alters value
Coercion alters value
Addition overflow of allocation size
Integer overflow of allocation size
Multiplication overflow of allocation size
Subtraction underflow of allocation size
Truncation of allocation size
Addition overflow of size
Unreasonable size argument
Multiplication overflow of size
Subtraction underflow of size
Truncation of size |
| Compass/ROSE |  |  | Can detect violations of this rule. It should look for patterns of (a op1 b) op2 c wherec has a bigger type than a or bNeither a nor b is typecast to c's typeop2 is assignment or comparison |
| Coverity | 6.5 | OVERFLOW_BEFORE_WIDEN | Fully implemented |
| Helix QAC | 2024.4 | C1890, C1891, C1892, C1893, C1894, C1895, C4490, C4491, C4492 |  |
| Klocwork | 2024.4 | PORTING.CAST.SIZE |  |
| LDRA tool suite | 9.7.1 | 452 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT18-aCERT_C-INT18-b
CERT_C-INT18-c | Avoid possible integer overflow in expressions in which the result is assigned to a variable of a wider integer typeAvoid possible integer overflow in expressions in which the result is compared to an expression of a wider integer type
Avoid possible integer overflow in expressions in which the result is cast to a wider integer type |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT18-C | Checks for integer overflow and unsigned integer overflow (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT35-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | INT35-CPP. Evaluate integer expressions in a larger size before comparing or assigning to that size |
| ISO/IEC TR 24772:2013 | Numeric Conversion Errors [FLC] |
| MITRE CWE | CWE-681, Incorrect conversion between numeric typesCWE-190, Integer overflow (wrap or wraparound) |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [Seacord 2013] | Chapter 5, "Integer Security" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152319) [](../c/Rec_%2004_%20Integers%20_INT_) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_)
## Comments:

|  |
| ----|
| For same-width unsigned addition/subtraction, there is a simple and fast test for overflow (wraparound):
if (a + b < a) /* then handle wraparound */
                                        Posted by dagwyn at Apr 15, 2008 20:57
                                     |
| Since this is a more portable solution (it doesn't require that sizeof(long long) > sizeof(size_t), we need to work this into a compliant solution. Also, we probably should replace
a + b < MAX
with
MAX - b > a
as another compliant solution, as that is also portable.
                                        Posted by svoboda at Jun 17, 2008 12:30
                                     |
| added another compliant solution and cleaned up the code/wording elsewhere
                                        Posted by avolkovi at Jun 17, 2008 16:36
                                     |
| is the malloc() example here an exception to EXP09-C. Use sizeof to determine the size of a type or variable?
                                        Posted by avolkovi at Jun 27, 2008 13:37
                                     |
| Hm, not really. These examples are functions that take the size to allocate as a parameter. One can argue that the size_t parameter to pass to these functions should be the result of a sizeof operator (or a char-based operator like strlen()).
But we should definitely mention EXP09-A and how one needs to pass a sizeof value in to these functions.
                                        Posted by svoboda at Jun 27, 2008 14:28
                                     |
| Should we perhaps make it more clear that we don't expect every single operation to be evaluated in a larger size?  I feel like only a few real-life additions/multiplications could overflow/can take user input, and only those actually need the bounds check.
We should also mention that this is not always possible, ie- when working with long longs....
                                        Posted by avolkovi at Jul 24, 2008 14:24
                                     |
| I believe this rule is not meant to apply to expressions representing a single constant or variable; eg:func(int i, long long ll) { ...
 if (i == ll) ...
 }would not be violating this rule, right?
                                        Posted by svoboda at May 15, 2013 13:23
                                     |
| Svoboda and I have been discussing off line about making this a recommendation and not a rule.; Any real problem with this rule would be detected by one of the following rules:INT30-C. Ensure that unsigned integer operations do not wrapINT31-C. Ensure that integer conversions do not result in lost or misinterpreted dataINT32-C. Ensure that operations on signed integers do not result in overflowThere is potentially alot of code that violates this rule although it is clearly safe and doesn't violate any other rule:uint64_t num = 1 << 3;I think this is clearly more of an informative recommendation that identifies a problem and suggests an appropriate solution but for which conformance is not required. 
                                        Posted by rcs at Sep 29, 2013 11:13
                                     |
| I can live with that.
                                        Posted by bluepilot at Sep 29, 2013 11:40
                                     |
| I think there's a subtle problem with your example.; Consider:
#include <stdint.h>
#include <stdio.h>
int main(void) {
  uint64_t i = 1 << 31;
  printf("0x%llx", i);
  return 0;
}

 This code will compile without warning by default (at least on gcc 4.8.1 and MSVC 11), but print 0xffffffff80000000.  What the programmer intended to write was `1ULL << 31` instead.   This might possibly fit under [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](INT31-C_%20Ensure%20that%20integer%20conversions%20do%20not%20result%20in%20lost%20or%20misinterpreted%20data) since there's an integer conversion there, but it's a subtle one.
Despite that, I am fine with this being a rec instead of a rule.  ![](images/icons/emoticons/wink.svg)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Sep 29, 2013 12:03
\| \|
I think this would be diagnosed by the signed integer overflow rule INT32-C because a positive signed integer is wrapped around to a negative value.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 29, 2013 15:46
\|
