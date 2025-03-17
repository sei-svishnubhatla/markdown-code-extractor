The C Standard, Annex K (normative), defines alternative versions of standard string-handling functions designed to be safer replacements for existing functions. For example, it defines the `strcpy_s()`, `strcat_s()`, `strncpy_s()`, and `strncat_s()` functions as replacements for `strcpy()`, `strcat()`, `strncpy()`, and `strncat()`, respectively.
The Annex K functions were created by Microsoft to help retrofit its existing legacy code base in response to numerous, well-publicized security incidents over the past decade. These functions were subsequently proposed to the international standardization working group for the programming language C (ISO/IEC JTC1/SC22/WG14) for standardization.
The `strcpy_s()` function, for example, has this signature:
``` java
errno_t strcpy_s(
  char * restrict s1,
  rsize_t s1max,
  const char * restrict s2
);
```
The signature is similar to `strcpy()` but takes an extra argument of type `rsize_t` that specifies the maximum length of the destination buffer. Functions that accept parameters of type `rsize_t` diagnose a constraint violation if the values of those parameters are greater than `RSIZE_MAX`. Extremely large object sizes are frequently a sign that an object's size was calculated incorrectly. For example, negative numbers appear as very large positive numbers when converted to an unsigned type like `size_t`. For those reasons, it is sometimes beneficial to restrict the range of object sizes to detect errors. For machines with large address spaces, the C Standard, Annex K, recommends that `RSIZE_MAX` be defined as the smaller of the size of the largest object supported or `(SIZE_MAX >> 1)`, even if this limit is smaller than the size of some legitimate, but very large, objects (see also [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](INT01-C_%20Use%20rsize_t%20or%20size_t%20for%20all%20integer%20values%20representing%20the%20size%20of%20an%20object)).
The semantics of `strcpy_s()` are similar to the semantics of `strcpy()`. When there are no input validation errors, the `strcpy_s()` function copies characters from a source string to a destination character array up to and including the terminating null character. The function returns 0 on success.
The `strcpy_s()` function succeeds only when the source string can be fully copied to the destination without overflowing the destination buffer. Specifically, the following checks are made:
-   The source and destination pointers are checked to see if they are `NULL`.
-   The maximum length of the destination buffer is checked to see if it is equal to 0, greater than `RSIZE_MAX`, or less than or equal to the length of the source string.
-   Copying is not allowed between objects that overlap.
When a runtime-constraint violation is detected, the destination string is set to the null string (as long as it is not a null pointer, and the maximum length of the destination buffer is greater than 0 and not greater than `RSIZE_MAX`), and the function returns a nonzero value. In the following example, the `strcpy_s()` function is used to copy `src1` to `dst1`:
``` java
char src1[100] = "hello";
char src2[8] =  {'g','o','o','d','b','y','e','\0'};
char dst1[6];
char dst2[5];
int r1;
int r2;
r1 = strcpy_s(dst1, sizeof(dst1), src1);
r2 = strcpy_s(dst2, sizeof(dst2), src2);
```
However, the call to copy `src2` to `dst2` fails because insufficient space is available to copy the entire string, which consists of eight characters, to the destination buffer. As a result, `r2` is assigned a nonzero value and `dst2[0]` is set to the null character.
Users of the C Standard Annex K functions are less likely to introduce a [security flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) because the size of the destination buffer and the maximum number of characters to append must be specified. ISO/IEC TR 24731 Part II \[[ISO/IEC TR 24731-2:2010](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\] offers another approach, supplying functions that allocate enough memory for their results. ISO/IEC TR 24731 Part II functions also ensure null termination of the destination string.
The C Standard Annex K functions are still capable of overflowing a buffer if the maximum length of the destination buffer and number of characters to copy are incorrectly specified. ISO/IEC TR 24731 Part II functions can make it more difficult to keep track of memory that must be freed, leading to memory leaks. As a result, the C Standard Annex K and the ISO/IEC TR 24731 Part II functions are not particularly secure but may be useful in preventive maintenance to reduce the likelihood of vulnerabilities in an existing legacy code base.
## Noncompliant Code Example
This noncompliant code overflows its buffer if `msg` is too long, and it has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if `msg` is a null pointer:
``` c
void complain(const char *msg) {
  static const char prefix[] = "Error: ";
  static const char suffix[] = "\n";
  char buf[BUFSIZ];
  strcpy(buf, prefix);
  strcat(buf, msg);
  strcat(buf, suffix);
  fputs(buf, stderr);
}
```
## Compliant Solution (Runtime)
This compliant solution will not overflow its buffer:
``` c
void complain(const char *msg) {
  errno_t err;
  static const char prefix[] = "Error: ";
  static const char suffix[] = "\n";
  char buf[BUFSIZ];
  err = strcpy_s(buf, sizeof(buf), prefix);
  if (err != 0) {
    /* Handle error */
  }
  err = strcat_s(buf, sizeof(buf), msg);
  if (err != 0) {
    /* Handle error */
  }
  err = strcat_s(buf, sizeof(buf), suffix);
  if (err != 0) {
    /* Handle error */
  }
  fputs(buf, stderr);
}
```
## Compliant Solution (Partial Compile Time)
This compliant solution performs some of the checking at compile time using a static assertion (see [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression)).
``` c
void complain(const char *msg) {
  errno_t err;
  static const char prefix[] = "Error: ";
  static const char suffix[] = "\n";
  char buf[BUFSIZ];
  /* 
   * Ensure that more than one character
   * is available for msg
   */
  static_assert(sizeof(buf) > sizeof(prefix) + sizeof(suffix),
                "Buffer for complain() is too small");
  strcpy(buf, prefix);
  err = strcat_s(buf, sizeof(buf), msg);
  if (err != 0) {
    /* Handle error */
  }
  err = strcat_s(buf, sizeof(buf), suffix);
  if (err != 0) {
    /* Handle error */
  }
  fputs(buf, stderr);
}
```
## Risk Assessment
String-handling functions defined in the C Standard, subclause 7.24, and elsewhere are susceptible to common programming errors that can lead to serious, [exploitable](BB.-Definitions_87152273.html#BB.Definitions-exploit) [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Proper use of the C11 Annex K functions can eliminate most of these issues.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR07-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR07 |  |
| CodeSonar | 8.3p0 | BADFUNC.BO.* | Many checks for uses of library functions that do not perform bounds checking. |
| Helix QAC | 2024.4 | C5008 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-STR07-a | Avoid using unsafe string functions that do not check bounds |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. STR07-C | Checks for:Use of dangerous standard functionDestination buffer overflow in string manipulationInsufficient destination buffer sizeRec. partially covered. |
| SonarQube C/C++ Plugin | 3.11 | S1081 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR07-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24731-2:2010 |  |
| ISO/IEC TR 24772:2013 | Use of Libraries [TRJ] |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2005b] | "Managed String Library for C, C/C++" |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](../c/STR06-C_%20Do%20not%20assume%20that%20strtok__%20leaves%20the%20parse%20string%20unchanged) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152118)
## Comments:

|  |
| ----|
| Is there a recommendation for how to use these functions on machines where the standard compilers do not support them?
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 18:28
                                     |
| > Is there a recommendation for how to use these functions on machines where the standard compilers do not support them?
A TR 24731-1 implementation is available as part of the Dinkumware Compleat Libraries.
                                        Posted by rcs at Mar 16, 2008 18:53
                                     |
| Hi Jonathan,
> Is there a recommendation for how to use these functions on machines where the
> standard compilers do not support them

The functions are usually either (1) available, or (2) not available in a library. Microsoft makes the functions available in its standard runtimes, Linux, Unix, and BSD do not.
If you're on a Unix-like platform, try the following as 'safer' replacements to the less-secure C string functions until the fate of TR 24731 is determined (ISO/IEC TR 24731 is a Technical Report of type 2. ... without an immediate possibility of an agreement on an International Standard 1). Taken from Apple's Secure Coding Guide, p 36 2):
strcat -> strlcat
strcpy -> strlcpy
strncat -> strlcat
strncpy -> strlcpy
sprintf -> snprintf
vsprintf -> vsnprintf
gets -> fgets
Jeff
1 http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1172.pdf
2 http://developer.apple.com/documentation/Security/Conceptual/SecureCodingGuide/SecureCodingGuide.pdf
                                        Posted by noloader@gmail.com at Sep 22, 2010 01:31
                                     |
| Actually, WG14 recognizes two TRs: TR24731-1 is the 24731 of which you speak, currently supported by Microsoft but not GCC.
TR24731-2 is the 'other' TR, and provides similar functionality to TR24731-1, but lists functions commonly used on POSIX systems, including the strl* functions you cite.
BTW TR24731-1 is now a normative part of the C1x draft (N1494), as Annex K. So I expect that the *_s functions will eventually become supported by GCC if it wants to claim C1x compliance.
                                        Posted by svoboda at Sep 23, 2010 16:47
                                     |
| Hi David,
I just checked the ISO/IEC's C - Project status and milestones at http://www.open-std.org/Jtc1/sc22/wg14/www/projects.
Bounds checking interfaces are now part of the C1X draft dated 2010-10-04 (no longer tacked on as an annex). Grab the N1516 PDF at the above link.
Ulrich Drepper's reign of terror on the safer string functions will be ending shortly. He has made a mess of strl* and friend, and str*_s and friends for far too long.
> TR24731-2 ... lists functions commonly used on POSIX systems, including  the strl* functions you cite

Sadly, I only saw strndup in TR24731-2. Perhaps I missed a detail somewhere?
Jeff
                                        Posted by noloader@gmail.com at Nov 16, 2010 22:41
                                     |
| Jeff,
I just checked this working draft of C1X and the _s functions are still defined in Annex K (normative) Bounds-checking interfaces.
However, I believe you are correct concerning TR24731-2.
rCs
                                        Posted by rcs_mgr at Nov 17, 2010 07:06
                                     |
| This should explictly mention the strl... variants as well as the ..._s variants.; Both are useful depending on the context.  The strl... variants truncate the result.  They can be added quickly in most cases by adding "l" to the name and adding sizeof(...) as the last argument.  In all the other cases I have encountered, it was just a matter of adding a size parameter to the subroutine that used strcpy or strcat.  It may not be perfect, but it does ensure there is no buffer overflow.  This is especially helpful when you are downstream of an open source project and it's impractical to make massive source changes (because you need to merge every time), but you still want to ensure there are no buffer overflows.  They are also useful in a context where there may not really be buffer overflows, but you want to outlaw all uses of strcpy and strcat just on principle.The ..._s variants report string overflow as an error, which is going to be more convenient if you have the luxury and resources to re-engineer the algorithm.
                                        Posted by herbierobinson at Jul 14, 2022 18:49
                                     |
| The strl...functions are not part of Annex K, whose functions are the scope of this recommendation, hence strl... functions are out of scope.
                                        Posted by svoboda at Jul 15, 2022 07:13
                                     |

