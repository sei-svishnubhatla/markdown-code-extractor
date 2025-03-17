The process of parsing an integer or floating-point number from a string can produce many errors. The string might not contain a number. It might contain a number of the correct type that is out of range (such as an integer that is larger than `INT_MAX`). The string may also contain extra information after the number, which may or may not be useful after the conversion. These error conditions must be detected and addressed when a string-to-number conversion is performed using a C Standard Library function.
The `strtol()`, `strtoll()`,  strtoimax(), `strtoul(), strtoull(), ``strtoumax()``, strtof(),` `strtod()`, and `strtold()` functions convert the initial portion of a null-terminated byte string to a `long int`, `long long int`, intmax_t, `unsigned long int`, `unsigned long long int, uintmax_t, float, double`, and `long double` representation, respectively.
Use one of the C Standard Library `strto*()` functions to parse an integer or floating-point number from a string. These functions provide more robust error handling than alternative solutions. Also, use the `strtol()` function to convert to a smaller signed integer type such as `signed int`, `signed short`, and `signed char`, testing the result against the range limits for that type. Likewise, use the `strtoul()` function to convert to a smaller unsigned integer type such as `unsigned int`, `unsigned short`, and `unsigned char`, and test the result against the range limits for that type. These range tests do nothing if the smaller type happens to have the same size and representation for a particular implementation.
## Noncompliant Code Example (`atoi()`)
This noncompliant code example converts the string token stored in the `buff` to a signed integer value using the `atoi()` function:
``` c
#include <stdlib.h>
void func(const char *buff) {
  int si;
  if (buff) {
    si = atoi(buff);
  } else {
    /* Handle error */
  }
}
```
The `atoi()`, `atol()`, `atoll()`, and `atof()` functions convert the initial portion of a string token to `int`, `long int, long long int`, and `double` representation, respectively. Except for the behavior on error (\[[ISO/IEC 9899:2024](https://www.securecoding.cert.org/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2024)\], s7.24.1.2), they are equivalent to
``` java
atoi: (int)strtol(nptr, (char **)NULL, 10)
atol: strtol(nptr, (char **)NULL, 10)
atoll: strtoll(nptr, (char **)NULL, 10)
atof: strtod(nptr, (char **)NULL)
```
Unfortunately, `atoi()` and related functions lack a mechanism for reporting errors for invalid values. Specifically, these functions:
-   do not need to set `errno` on an error;
-   have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) if the value of the result cannot be represented;
-   return 0 (or 0.0) if the string does not represent an integer (or decimal), which is indistinguishable from a correctly formatted, zero-denoting input string.
## Noncompliant Example (`sscanf()`)
This noncompliant example uses the `sscanf()` function to convert a string token to an integer. The `sscanf()` function has the same limitations as `atoi()`:
``` c
#include <stdio.h>
void func(const char *buff) {
  int matches;
  int si;
  if (buff) {
    matches = sscanf(buff, "%d", &si);
    if (matches != 1) {
      /* Handle error */
    }
  } else {
    /* Handle error */
  }
}
```
The `sscanf()` function returns the number of input items successfully matched and assigned, which can be fewer than provided for, or even 0 in the event of an early matching failure. However, `sscanf()` fails to report the other errors reported by `strtol()`, such as numeric overflow.
## Compliant Solution (`strtol()`)
The `strtol()`, `strtoll()`, `strtoimax())`, `strtoul(), strtoull(), strtoumax(), strtof(),` `strtod()`, and `strtold()` functions convert a null-terminated byte string to `long int`, `long long int`, `intmax_t`, `unsigned long int`, `unsigned long long int, uintmax_t, float, double`, and `long double` representation, respectively.
This compliant solution uses `strtol()` to convert a string token to an integer and ensures that the value is in the range of `int`:
``` c
#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <stdio.h>
void func(const char *buff) {
  char *end;
  int si;
  errno = 0;
  const long sl = strtol(buff, &end, 10);
  if (end == buff) {
    (void) fprintf(stderr, "%s: not a decimal number\n", buff);
  } else if ('\0' != *end) {
    (void) fprintf(stderr, "%s: extra characters at end of input: %s\n", buff, end);
  } else if ((LONG_MIN == sl || LONG_MAX == sl) && ERANGE == errno) {
    (void) fprintf(stderr, "%s out of range of type long\n", buff);
  } else if (sl > INT_MAX) {
    (void) fprintf(stderr, "%ld greater than INT_MAX\n", sl);
  } else if (sl < INT_MIN) {
    (void) fprintf(stderr, "%ld less than INT_MIN\n", sl);
  } else {
    si = (int)sl;
    /* Process si */
  }
}
```
## Risk Assessment
It is rare for a violation of this rule to result in a security [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) unless it occurs in security-sensitive code. However, violations of this rule can easily result in lost or misinterpreted data. 

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR34-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-ERR34 |  |
| Clang | 3.9 | cert-err34-c | Checked by clang-tidy |
| CodeSonar | 8.3p0 | BADFUNC.ATOFBADFUNC.ATOI
BADFUNC.ATOL
BADFUNC.ATOLL
(customization) | Use of atofUse of atoi
Use of atol
Use of atollUsers can add custom checks for uses of other undesirable conversion functions. |
| Compass/ROSE |  |  | Can detect violations of this recommendation by flagging invocations of the following functions:atoi()scanf(), fscanf(), sscanf()Others? |
| Helix QAC | 2024.4 | C5030C++5016 |  |
| Klocwork | 2024.4 | CERT.ERR.CONV.STR_TO_NUMMISRA.STDLIB.ATOI
SV.BANNED.RECOMMENDED.SCANF |  |
| LDRA tool suite | 9.7.1 | 44 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR34-a | The 'atof', 'atoi', 'atol' and 'atoll' functions from the 'stdlib.h' or 'cstdlib' library should not be used |
| PC-lint Plus | 1.4 | 586 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rule ERR34-C | Checks for unsafe conversion from string to numeric value (rule fully covered) |
| SonarQube C/C++ Plugin | 3.11 | S989 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT06-CPP. Use strtol() or a related function to convert a string token to an integer | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-676, Use of potentially dangerous function | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-758 | 2017-06-29: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-20 and ERR34-C
Intersection( ERR34-C, CWE-20) = Ø
CERT C does not define the concept of ‘input validation’. String-to-integer conversion (ERR34-C) may qualify as input validation, but this is outside the scope of the CERT rule.
### CWE-391 and ERR34-C
CWE-391 = Union( ERR34-C, list) where list =
-   Failure to errors outside of string-to-number conversion functions
### CWE-676 and ERR34-C
-   Independent( ENV33-C, CON33-C, STR31-C, EXP33-C, MSC30-C, ERR34-C)
-   ERR34-C implies that string-parsing functions (eg atoi() and scanf()) are dangerous.
-   CWE-676 = Union( ERR34-C, list) where list =
-   Invocation of dangerous functions besides the following:
-   atoi(), atol(), atoll(), atof(), The scanf()family
### CWE-758 and ERR34-C
Independent( INT34-C, INT36-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
Intersection( CWE-758, ERR34-C) =
-   Undefined behavior arising from a non-representable numeric value being parsed by an ato\*() or scanf() function
CWE-758 – ERR34-C =
-   Undefined behavior arising from using a function outside of the ato\*() or scanf() family
ERR34-C – CWE-758 =
-   The ato\*() or scanf() family receives input that is not a number when trying to parse one
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.24.1, "Numeric conversion functions" |
| [Klein 2002] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152272) [](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](../c/Rule%2013_%20Application%20Programming%20Interfaces%20_API_)
## Comments:

|  |
| ----|
| According to the man page...
The behaviour is the same as
strtol(nptr, (char **)NULL, 10);

except that `atoi()` does not detect errors.
So we should advocate strto\* functions, moreover, regarding returning 0:
> If there were no digits at all, `strtol()` stores the original value of `nptr` in `*endptr` (and returns 0).

So we should be checking for that scenario to find out if the 0 is invalid or not.
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 06, 2008 09:36
\| \|
What do you mean by "initial portion of a null-terminated byte string" in the first paragraph?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at May 04, 2009 22:41
\| \|
That language comes from C99. The implication is that the string (which is null-terminated like all C strings) must begin with the number to be parsed, but the string may also contain other non-numeric data (eg "12 drummers drumming"). The strtol() function ignores the non-numeric data and just extracts the number.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 06, 2009 09:22
\| \|
I'm a bit concerned that we are too heavy handed on using scanf to parse integers from strings. The rule says:
> Unfortunately, atoi() and related functions lack a mechanism for reporting errors for invalid values. Specifically, the atoi(), atol(), and atoll() functions
>
> -   do not need to set errno on an error
> -   have undefined behavior if the value of the result cannot be represented
> -   return 0 if the string does not represent an integer, which is indistinguishable from a correctly formatted, zero-denoting input string.
> The sscanf() function does return the number of input items successfully matched and assigned, which can be fewer than provided for, or even zero in the event of an early matching failure. However, sscanf() fails to report the other errors reported by strtol(), such as overflow.

Judging from this, it seems that scanf("%d") & co. do not set errno, but who cares? they do indicate success via their return value. C99 doesn't really address how scanf handles out-of-range integers...is that why it is considered undefined behavior, and rendered as a NCCE?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 08, 2009 15:17
\| \|
To answer my own question, checking the return value of scanf() is just as easy as checking errno. The vulnerability of scanf() is that it does not report overflows. On my 64-bit Ubuntu box, if I feed the number 1234567890123456789 to
``` java
  long num;
  int result = scanf("%ld", &num);
```
Then result gets 1 while num gets 9223372036854775807. IOW scanf() reports no errors but happily mangles my input.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 23, 2010 16:09
\| \|
I noticed the Compliant Solution in Version [71](https://www.securecoding.cert.org/confluence/x/AobaAw) is testing for `errno != 0`:
``` java
  if ((sl == LONG_MIN || sl == LONG_MAX) && errno != 0) {
```
That's not entirely accurate. The special meaning of `strtol` return value being equal to `LONG_MIN` or `LONG_MAX` only applies when `(errno == ERANGE)`. I.e., this is a more accurate way of writing the test:
``` java
(sl == LONG_MIN || sl == LONG_MAX) && errno == ERANGE)
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at May 07, 2011 17:38
\| \|
There are a bug in the code.The end pointer is an input and output.
The end pointer content would be filled only if the end pointer is not NULL.
In the code the end pointer is not initialized, assumming that it is not NULL, but the address are composed by garbage. Are few possibilities, but is posible that because that pointer is not unitialized the garbage data would be 0 and the end should be considered NULL, and in that case the \*end expression cause a problem trying access to the content of the address 0 (maybe a crash).
A possible solution is assign the end pointer to the input, after check that input is not NULL:
`const` `char``* ``const` `c_str = argv[1];`
if (NULL == c_str) {
/\* bad \*/
return;
}
/\* ensure initialize end pointer to not NULL \*/
`char end = (char*)``c_str;`` `
![](images/icons/contenttypes/comment_16.png) Posted by cmontiers at Mar 03, 2014 06:34
\| \|
`strtol()` is defined to store a pointer to the final string into the object pointed to by;`endptr` if `endptr` is not a null pointer. So the code is correct – `&end` will never result in a null pointer. The object pointed to by `&end` (so `end` itself), is overwritten, so the contents of `end` are immaterial on input.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Mar 04, 2014 15:37
\| \|
If you compile this with all warning:
gcc -Wall -O0 test.c -o test.exe
//test.c
#include \<stdio.h\>
void checkNull(void \* ptr) {return;}
int main() {
void \* p;
checkNull(p);
return 0;
}
;
you get:
test.c: In function 'main':
**test.c:9:10: warning: 'p' is used uninitialized in this function \[-Wuninitialized\]**
 checkNull(p);
          ^
because this, you not are ensuring  that end pointer will never result in a null pointer, because in one of many possibilities, the address that hold the pointer (not the address of the pointer) can be 0, because it are not initialized, then the address that hold can be any number, in the case that it be 0, the endptr will be considered NULL in the function strtol and the result will be NULL.
![](images/icons/contenttypes/comment_16.png) Posted by cmontiers at Mar 09, 2014 20:29
\| \|
Edit: I verified that the code in the page is correct, because the address of the pointer will never be 0 using: &ptr as parameter of strtol:
char \*end;
const long sl = strtol(c_str, &end, 10);
is ok, sorry for my mistake.
The problem that I mentions would be in the case the code would be:
char \*\*end;
const long sl = strtol(c_str, end, 10);
;
that is not the case in code of the page.
![](images/icons/contenttypes/comment_16.png) Posted by cmontiers at Mar 09, 2014 20:56
\| \|
I am aware that this comment may be overly fastidious so feel free to disregard.
According to my reading of the rules, the CCE (strtol) violates [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors) since it does not attempt to check for an error on the calls to `fprintf.;`
Admittedly, I feel applying that rule here would require going through each rule and verifying no function call listed in ERR33 table is ever used in a CCE without error checking which seems excessive and not in the spirit of these rules. 
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at Jun 19, 2023 09:04
\| \|
Samuel:
I will refer you to the exception in that rule (ERR33-C-EX1), which permits ignoring the value of many functions that are traditionally used to indicate that an error has occurred. ;After all, if an error occurs when you are trying to report a pre-existing error, how do you handle the new error?  (This is a longstanding unanswered question in standard C).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 20, 2023 08:58
\| \|
I had overlooked that thank you. It certainly highlights the intent.
Purely for the purposes of academic discussion I note two things. `fprintf` is not listed in the table of functions mentioned in the exception you quoted. Additionally, the exception explicitly mentions that "The function's results should be explicitly cast to;`void` to signify programmer intent." Would it then be ideal to put (void) preceding essentially every write where the intent is to report an error?
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at Jun 20, 2023 13:56
\| \|
Samuel:I have tweaked the text in ERR33-C-EX1 to address your comment. It now describes fprintf(), and that you can ignore the output of fprintf() when sending data to stdout or stderr (but not otherwise). And, to be precise, casting the return value of printf() to void is a good recommendation, but not a strict requirement for now...we are now more explicit about that.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 20, 2023 16:22
\| \|
I have prepended (void) to all the print statements in this rule, as is recommended by the exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 21, 2023 11:18
\| \|
revision.147: removing unnecessary "and" and adding a closing paren.
should we add C.23 to the bibliography?
(oh, it's not published yet...; I check the contents with N3096.)
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 18, 2023 21:25
\| \|
Hello, Yozo-san!
The latest draft of C23 is n3149, and it should be published this year. And still it will be called 'C23' :)
Fortunately, C11 also indicates that the ato\*() functions depend on the strto\*() functions, so I changed the reference from C23 to C11.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 19, 2023 08:16
\| \|
Hi, David!
Looking at the table of contents of [C11 preview](https://www.iso.org/obp/ui/#iso:std:iso-iec:9899:ed-3:v1:en), it should be "s7.2**2**.1.2" instead of "s7.2**3**.1.2"?
BTW, I found n3149 is password-protected, and the reason is on n3150 (Editor's Report)![](plugins/servlet/twitterEmojiRedirector) 
The latest draft IN PUBLIC seems n3096![](plugins/servlet/twitterEmojiRedirector) 
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 19, 2023 22:47
\| \|
Yozo-san:Thanks. I updated the reference for C11.  
Sigh. The password is a new requirement imposed by ISO.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 20, 2023 08:53
\|
