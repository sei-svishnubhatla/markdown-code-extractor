The `restrict` qualification requires that the pointers do not reference overlapping objects. If the objects referenced by arguments to functions overlap (meaning the objects share some common memory addresses), the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). See also [undefined behavior 68](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_68) in Appendix J of the C Standard.
Several C functions define parameters that use the `restrict` qualification. The following is a list of the most common:
``` java
void *memcpy(
  void * restrict s1,
  const void * restrict s2,
  size_t n
);
int printf(
  const char * restrict format,
  /* ... */
);
int scanf(
  const char * restrict format,
  /* ... */
);
int sprintf(
  char * restrict s,
  const char * restrict format,
  /* ... */
);
int snprintf(
  char * restrict s,
  size_t n,
  const char * restrict format,
  /* ... */
);
char *strcpy(
  char * restrict s1,
  const char * restrict s2
);
char *strncpy(
  char * restrict s1,
  const char * restrict s2,
  size_t n
);
```
If any of the preceding functions are passed pointers to overlapping objects, the result of the functions is unknown and data may be corrupted. As a result, these functions must never be passed pointers to overlapping objects. If data must be copied between objects that share common memory addresses, a copy function guaranteed to work on overlapping memory, such as `memmove()`, should be used.
## Noncompliant Code Example
In this noncompliant code example, the values of objects referenced by `ptr1` and `ptr2` become unpredictable after the call to `memcpy()` because their memory areas overlap:
``` c
#include <string.h>
void func(void) {
  char c_str[]= "test string";
  char *ptr1 = c_str;
  char *ptr2;
  ptr2 = ptr1 + 3;
  memcpy(ptr2, ptr1, 6);
  /* ... */
}
```
## Compliant Solution
In this compliant solution, the call to `memcpy()` is replaced with a call to `memmove()`. The `memmove()` function performs the same operation as `memcpy()`, but copying takes place as if the *n* characters from the object pointed to by the source (`ptr1`) are first copied into a temporary array of *n* characters that does not overlap the objects pointed to by the destination (`ptr2`) or the source. The *n* characters from the temporary array are then copied into the object pointed to by the destination.
``` c
#include <string.h>
void func(void) {char c_str[]= "test string";
  char *ptr1 = c_str;
  char *ptr2;
  ptr2 = ptr1 + 3;
  memmove(ptr2, ptr1, 6);  /* Replace call to memcpy() */
  /* ... */
}
```
Similar solutions using `memmove()` can replace the string functions as long as care is taken regarding the byte size of the characters and proper null-termination of the copied string.
## Risk Assessment
Using functions such as `memcpy()`, `strcpy()`, `strncpy()`, `sscanf()`, `sprintf()`, `snprintf()`, `mbstowcs()`, and `wcstombs()` to copy overlapping objects results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) that can be exploited to cause data integrity violations.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL33-C | Medium | Probable | High | P4 | L3 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL33-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 480 S489 S | Partially implemented |

## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Passing Parameters and Return Values [CSJ] |
| ISO/IEC TS 17961 | Passing pointers into the same object as arguments to different restrict-qualified parameters [restrict] |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/DCL32-C.+Guarantee+that+mutually+visible+identifiers+are+unique?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=331) [](https://www.securecoding.cert.org/confluence/display/seccode/DCL34-C.+Use+volatile+for+data+that+cannot+be+cached?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| The non-overlap restriction applies to not just the regions that are nominally involved, but to the whole objects based on the pointers.; The reason for that is that more than just the nominal subobjects may need to be modified; for example, on a word-addressed machine accessing a byte requires that a whole word be involved, including nearby bytes that might not lie within the nominal regions.
                                        Posted by dagwyn at Apr 15, 2008 14:00
                                     |
| ;This is an odd rule, because the title is more precise than the description.  I'm wondering if the stricter or narrower rule is the right one.  TS 17961 gives the stricter rule.  I also think we should include Douglas Gwyn's observation in the description as it is an interesting and informative point.
                                        Posted by rcs at Sep 27, 2013 15:24
                                     |
| ;We did not include this example from TS 17961:EXAMPLE 2 In this noncompliant example, the src operand is used twice to refer to unmodified memory, which is allowed by the C Standard; the aliasing restrictions apply only when the object is modified. A diagnostic is required nontheless because the pointer src is twice a restrict-qualified pointer parameter to dual_memcpy, referencing overlapping objects.void *dual_memcpy(

      void *restrict  s1, const void *restrict  s2, size_t n1,
      void *restrict  s3, const void *restrict  s4, size_t n2
    ) {
      memcpy(s1, s2, n1);
      memcpy(s3, s4, n2);
      return s1;
    }
    void f(void) {
      char dest1[10];
      char dest2[10];
      char src[] = "hello";
      dual_memcpy(dest1, src, sizeof(src),
                  dest2, src, sizeof(src));  // diagnostic required
      puts(dest1);
      puts(dest2);
    }
I wonder if we should?  If I remember correctly, this code is valid as far as the C standard is concerned, but violates the TS 17961 rule because of the fidelity of the analysis.  Consequently, you might want to include this as a noncompliant example here as well to prevent false positives and improve the analyzability of your code, or alternatively we could use the narrower rule which would allow us to treat these diagnostics as a false positive. 
In general, this coding standard is stricter than TS 17961, so it would be interesting if we were to allow this code and in cases like this make this standard narrower than TS 17961.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 27, 2013 15:45
\|
