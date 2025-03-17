Signed character data must be converted to `unsigned char` before being assigned or converted to a larger signed type. This rule applies to both `signed char` and (plain) `char` characters on implementations where `char` is defined to have the same range, representation, and behaviors as `signed char`.
However, this rule is applicable only in cases where the character data may contain values that can be interpreted as negative numbers. For example, if the `char` type is represented by a two's complement 8-bit value, any character value greater than +127 is interpreted as a negative value.
This rule is a generalization of [STR37-C. Arguments to character-handling functions must be representable as an unsigned char](STR37-C_%20Arguments%20to%20character-handling%20functions%20must%20be%20representable%20as%20an%20unsigned%20char).
## Noncompliant Code Example
This noncompliant code example is taken from a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in bash versions 1.14.6 and earlier that led to the release of CERT Advisory [CA-1996-22](http://www.cert.org/advisories/CA-1996-22.html). This vulnerability resulted from the sign extension of character data referenced by the `c_str` pointer in the `yy_string_get()` function in the `parse.y` module of the bash source code:
``` c
static int yy_string_get(void) {
  register char *c_str;
  register int c;
  c_str = bash_input.location.string;
  c = EOF;
  /* If the string doesn't exist or is empty, EOF found */
  if (c_str && *c_str) {
    c = *c_str++;
    bash_input.location.string = c_str;
  }
  return (c);
}
```
The `c_str` variable is used to traverse the character string containing the command line to be parsed. As characters are retrieved from this pointer, they are stored in a variable of type `int`. For implementations in which the `char` type is defined to have the same range, representation, and behavior as `signed char`, this value is sign-extended when assigned to the `int` variable. For character code 255 decimal (−1 in two's complement form), this sign extension results in the value −1 being assigned to the integer, which is indistinguishable from `EOF`.
## Noncompliant Code Example
This problem can be repaired by explicitly declaring the `c_str` variable as `unsigned char`:
``` c
static int yy_string_get(void) {
  register unsigned char *c_str;
  register int c;
  c_str = bash_input.location.string;
  c = EOF;
  /* If the string doesn't exist or is empty, EOF found */
  if (c_str && *c_str) {
    c = *c_str++;
    bash_input.location.string = c_str;
  }
  return (c);
}
```
This example, however, violates [STR04-C. Use plain char for characters in the basic character set](STR04-C_%20Use%20plain%20char%20for%20characters%20in%20the%20basic%20character%20set).
## Compliant Solution
In this compliant solution, the result of the expression `*c_str++` is cast to `unsigned char` before assignment to the `int` variable `c`:
``` c
static int yy_string_get(void) {
  register char *c_str;
  register int c;
  c_str = bash_input.location.string;
  c = EOF;
  /* If the string doesn't exist or is empty, EOF found */
  if (c_str && *c_str) {
    /* Cast to unsigned type */
    c = (unsigned char)*c_str++;
    bash_input.location.string = c_str;
  }
  return (c);
}
```
## Noncompliant Code Example
In this noncompliant code example, the cast of `*s` to `unsigned int` can result in a value in excess of `UCHAR_MAX` because of integer promotions, a violation of [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts):
``` c
#include <limits.h>
#include <stddef.h>
static const char table[UCHAR_MAX + 1] = { 'a' /* ... */ };
ptrdiff_t first_not_in_table(const char *c_str) {
  for (const char *s = c_str; *s; ++s) {
    if (table[(unsigned int)*s] != *s) {
      return s - c_str;
    }
  }
  return -1;
}
```
## Compliant Solution
This compliant solution casts the value of type `char` to `unsigned char` before the implicit promotion to a larger type:
``` c
#include <limits.h>
#include <stddef.h>
static const char table[UCHAR_MAX + 1] = { 'a' /* ... */ };
ptrdiff_t first_not_in_table(const char *c_str) {
  for (const char *s = c_str; *s; ++s) {
    if (table[(unsigned char)*s] != *s) {
      return s - c_str;
    }
  }
  return -1;
}
```
## Risk Assessment
Conversion of character data resulting in a value in excess of `UCHAR_MAX` is an often-missed error that can result in a disturbingly broad range of potentially severe [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR34-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | char-sign-conversion | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR34 | Fully implemented |
| CodeSonar | 8.3p0 | MISC.NEGCHAR | Negative Character Value |
| Compass/ROSE |  |  | Can detect violations of this rule when checking for violations of INT07-C. Use only explicitly signed or unsigned char type for numeric values |
| Coverity | 2017.07 | MISRA C 2012 Rule 10.1MISRA C 2012 Rule 10.2MISRA C 2012 Rule 10.3MISRA C 2012 Rule 10.4 | ImplementedEssential type checkers |
| Cppcheck Premium | 24.11.0 | premium-cert-str34-c |  |
| ECLAIR | 1.2 | CC2.STR34 | Fully implemented |
| GCC | 2.95 and later | -Wchar-subscripts | Detects objects of type char used as array indices |
| Helix QAC | 2024.4 | C2140, C2141, C2143, C2144, C2145, C2147, C2148, C2149, C2151, C2152, C2153, C2155C++3051 |  |
| Klocwork | 2024.4 | CXX.CAST.SIGNED_CHAR_TO_INTEGER |  |
| LDRA tool suite | 9.7.1 | 434 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR34-bCERT_C-STR34-c
CERT_C-STR34-d | Cast characters to unsigned char before assignment to larger integer sizesAn expressions of the 'signed char' type should not be used as an array index
Cast characters to unsigned char before converting to larger integer sizes |
| PC-lint Plus | 1.4 | 571 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR34-C | Checks for misuse of sign-extended character value (rule fully covered) |
| RuleChecker | 24.04 | char-sign-conversion | Fully checked |
| TrustInSoft Analyzer | 1.38 | out of bounds read | Partially verified (exhaustively detects undefined behavior). |

### Related Vulnerabilities
[CVE-2009-0887](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-0887) results from a violation of this rule. In Linux PAM (up to version 1.0.3), the `libpam` implementation of `strtok()` casts a (potentially signed) character to an integer for use as an index to an array. An attacker can exploit this vulnerability by inputting a string with non-ASCII characters, causing the cast to result in a negative index and accessing memory outside of the array \[[xorl 2009](http://xorl.wordpress.com/2009/03/26/cve-2009-0887-linux-pam-singedness-issue/)\].
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR34-C).
### Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | STR37-C. Arguments to character-handling functions must be representable as an unsigned charSTR04-C. Use plain char for characters in the basic character set
ARR30-C. Do not form or use out-of-bounds pointers or array subscripts |
| ISO/IEC TS 17961:2013 | Conversion of signed characters to wider integer types before a check for EOF [signconv] |
| MISRA-C:2012 | Rule 10.1 (required)Rule 10.2 (required)Rule 10.3 (required)Rule 10.4 (required) |
| MITRE CWE | CWE-704, Incorrect Type Conversion or Cast |

## Bibliography

|  |  |
| ----|----|
| [xorl 2009] | CVE-2009-0887: Linux-PAM Signedness Issue |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152047) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152388)
## Comments:

|  |
| ----|
| The way it's phrased this rule would lead one to believe that casting a char value to any unsigned type before converting it to a larger signed type will prevent sign extension. In fact, to prevent sign extension, a char value must be cast to unsigned char.
For example, in the non-compliant example below the result of the cast of *s to unsigned int may result in a value in excess of UCHAR_MAX due to integer promotion, thus causing the function to violate ARR30-C. Guarantee that array indices are within the valid range, leading to undefined behavior.
static const char table[UCHAR_MAX] = { /* ... * };
int first_not_in_table(const char *str) {
  const char *s = str;
  for (; *s; ++s) {
    if (table[(unsigned)*s] != *s)
      return s - str;
  return -1;
}

The compliant solution is to cast the `char` value to unsigned char before allowing it to be implicitly promoted to a larger unsigned type.
``` java
static const char table[UCHAR_MAX] = { /* ... * };
ptrdiff_t first_not_in_table(const char *str) {
  const char *s = str;
  for (; *s; ++s) {
    if (table[(unsigned char)*s] != *s)
      return s - str;
  return -1;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 09, 2010 19:30
\| \|
Martin,
I updated this guideline based on your comment. If you are happy with the changes, I'll go ahead and remove the comment.
rCs
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 21, 2010 13:08
\| \|
Thanks for updating the wording! FWIW, the example was just for illustration and I didn't mean to suggest that it be added – it seems somewhat redundant (although unlike the Bash bug, it does demonstrate undefined behavior).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Aug 22, 2010 16:39
\| \|
I believe the `table` array in this example should be declared with `UCHAR_MAX+1` elements; otherwise, accessing the element at index `UCHAR_MAX` leads to undefined behavior.
![](images/icons/contenttypes/comment_16.png) Posted by bfletcher at Nov 02, 2016 09:55
\| \|
I've corrected the issue, thank you for pointing it out!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 02, 2016 10:16
\| \|
For the compliant soluation:
``` cpp
static const char table[UCHAR_MAX] = { /* ... * };
ptrdiff_t first_not_in_table(const char *str) {
  const char *s = str;
  for (; *s; ++s) {
    if (table[(unsigned char)*s] != *s)
      return s - str;
  return -1;
}
```
The integer promotion should happened in the both operands of expression **table\[(unsigned char)\*s\] != \*s.** The **table\[(unsigned char)\*s\] and **\*s(right)**** should be promoted to int type. So this should be non-compliant, right?
![](images/icons/contenttypes/comment_16.png) Posted by haoche at Jan 08, 2019 03:52
\| \|
The problem is not that the comparison might fail, it is that s might be an invalid array index (if converted from plain char to int). This is especially likely if s is EOF (or some other signed char less than 0).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 09, 2019 16:03
\| \|
Yes, I see. I meant the char array itself;**table\[(unsigned char)\*s\] and \*s** (right of != ) should also be** non-compliant** case. Refer to the** Integer promotions** of c standard(<https://en.cppreference.com/w/c/language/conversion>):
``` java
Integer promotion is the implicit conversion of a value of any integer type with rank less or equal to rank of int or of a bit field of type _Bool, int, signed int, unsigned int, to the value of type int or unsigned int.
```
The char array **table\[(unsigned char)\*s\]** and** **\*s**** would also be cast to int type implicitly. And this really break the rule and wasn't pointed out in this rule. Does this make sense?
![](images/icons/contenttypes/comment_16.png) Posted by haoche at Jan 10, 2019 02:11
\| \|
Thanks, that does make sense.
This rule does not address this issue because it is not a problem. The C standard provides strict guidance to platforms for how to promote a char expression, and the guidance may promote a plain char to an unsigned or signed int, depending on platform-specific details. On 32- and 64-bit Intel platforms (Windows, Mac, or Linux), char is signed and promotes to signed int. See;[INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules) for details about integer promotion.
The reason there is no problem with the comparison is that the expressions on both sides of the comparison both evaluate to plain char, so they will be promoted to the same type, and will preserve the value. Which means the != (comparison) operation will behave as expected.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 16, 2019 08:47
\| \|
"Signed character data must be converted to `unsigned char` before being assigned or converted to a larger **signed** type"
I believe there is typo here. It should be
"Signed character data must be converted to `unsigned char` before being assigned or converted to a larger unsigned type"
Similarly, the rule heading should also be updated to say
"[STR34-C. Cast characters to unsigned char before converting to larger unsigned integer sizes](https://wiki.sei.cmu.edu/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes)"
![](images/icons/contenttypes/comment_16.png) Posted by pprasad at Aug 28, 2019 06:34
\| \|
The first noncompliant code example demonstrates a plain char being incorrectly promoted to a (signed) int. It is incorrect because char point 255 (0xFF) can be conflated with -1.; So this rule applies to larger signed types as well as unsigned types.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 03, 2019 08:53
\| \|
So this rule is to avoid sign extension.
I don't see why we need to avoid it, except for the few instances shown in this page.
There are a lot of situations where sign extension is required.
![](images/icons/contenttypes/comment_16.png) Posted by pprasad at Sep 04, 2019 02:03
\| \|
Sign extension is a perfectly fine thing to use when doing number-to-number conversion...it helps preserve the values of signed integers, and it preserves the bit-pattern if you convert between signed and unsigned.
It is problematic when dealing with characters however, especially because fgetc() and its ilk return a nonnegative number when reading a valid char, and EOF (-1). That is what this rule focuses on.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 04, 2019 08:36
\| \|
Just want to make things be more clear.;![](images/icons/emoticons/smile.svg)
> Thanks, that does make sense.

Do you mean we should report defects for this kind of case for this rule?
and more specific, could you kindly look at the folloing case and help judge if we shall report defects pointed in the comments? thanks a lot~
``` cpp
int main( int argc, char *argv[] )
{
    char a;
    char b;
    if ((a == b) &&   // shall we report defects for `a` and `b` here?
        (a == '\0')) {  // shall we report defect here for `a`?
    }
   return 0;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by zhuochen at Oct 14, 2019 21:36
\| \|
The cases to report is when a non-unsigned char is cast to an int and a negative value could be misinterpreted as a positive value. And that never happens in your code. (Yes, there is implicit integer promotion but a compliant compiler will handle that case correctly.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Oct 15, 2019 08:48
\|
