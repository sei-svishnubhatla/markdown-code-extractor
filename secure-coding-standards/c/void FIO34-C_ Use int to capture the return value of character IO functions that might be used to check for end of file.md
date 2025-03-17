The character I/O functions `fgetc()`, `getc()`, and `getchar()` all read a character from a stream and return it as an `int`. If the stream is at end-of-file, the end-of-file indicator for the stream is set and the function returns `EOF`. If a read error occurs, the error indicator for the stream is set and the function returns `EOF`. The character I/O functions `fputc()`, `putc()`, `putchar()`, and `ungetc()` also return a character or `EOF`.
Do not convert the value returned by a character I/O function to `char` if that value will be compared to `EOF`. Once the return value of these functions has been converted to a `char` type, character values may be indistinguishable from `EOF`. Also, if `sizeof(int) == sizeof(char)`, then the `int` used to capture the return value may be indistinguishable from `EOF`. See [void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_) for more details about when `int` and `char` have the same number of precision bits. See [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type) for more information on the proper use of character types.
This rule applies to the use of all character I/O functions, including wide character I/O functions.
## Noncompliant Code Example (`char`)
This code example is noncompliant because the variable `c` is declared as a `char` and not an `int`:
``` c
#include <stdio.h>
void func(void) {
  enum { BUFFER_SIZE = 32 };
  char buf[BUFFER_SIZE];
  char c;
  int i = 0;
  while ((c = getchar()) != '\n' && c != EOF) {
    if (i < (BUFFER_SIZE- 1)) {
      buf[i++] = c;
    }
  }
  buf[i] = '\0';
}
```
Assuming that a `char` is a signed 8-bit value and an `int` is a 32-bit value, if `getchar()` returns the character encoded as `0xFF` (decimal 255), it will be interpreted as `EOF` because this value is sign-extended to `0xFFFFFFFF` (the value of `EOF`) to perform the comparison. (See [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](INT31-C_%20Ensure%20that%20integer%20conversions%20do%20not%20result%20in%20lost%20or%20misinterpreted%20data).)
## Compliant Solution (`int`)
This compliant solution declares `c` to be an `int`. It is valid on architectures where `char` is smaller than `int`.
``` c
#include <stdio.h>
#include <assert.h>
void func(void) {
  enum { BUFFER_SIZE = 32 };
  assert(PRECISION(UCHAR_MAX) < PRECISION(INT_MAX));
  unsigned char buf[BUFFER_SIZE];
  int c;
  int i = 0;
  while (((c = getchar()) != '\n') && c != EOF) {
    if (i < (BUFFER_SIZE - 1)) {
      buf[i++] = c;
    }
  }
  buf[i] = '\0';
}
```
But in some cases, `feof()` and `ferror()` must be used instead.
See [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions) for more information about the `PRECISION` macro.
## Noncompliant Code Example (`wchar_t`)
In this noncompliant example, the result of the call to the C standard library function `getwc()` is stored into a variable of type` wchar_t, wc`, and `wc` is compared to `WEOF`:
``` c
#include <stddef.h>
#include <stdio.h>
#include <wchar.h>
void g(void) {
  enum { BUFFER_SIZE = 32 };
  wchar_t buf[BUFFER_SIZE];
  wchar_t wc;
  size_t i = 0;
  while ((wc = getwc(stdin)) != L'\n' && wc != WEOF) {
    if (i < (BUFFER_SIZE - 1)) {
      buf[i++] = wc;
    }
  }
  buf[i] = L'\0';
}
```
## Compliant Solution (wint_t)
This compliant solution declares `c` to be a `wint_t`, the type of integer returned by `fgetwc()`. It is valid on architectures where `wchar_t` is smaller than `wint_t`.
``` c
#include <stddef.h>
#include <stdio.h>
#include <wchar.h>
void g(void) {
  enum { BUFFER_SIZE = 32 };
  assert(PRECISION(WCHAR_MAX) < PRECISION(WINT_MAX));
  wchar_t buf[BUFFER_SIZE];
  wint_t wc;
  size_t i = 0;
  while (((wc = getwc(stdin)) != L'\n' && wc != WEOF) { 
    if (i < BUFSIZ - 1) {
      buf[i++] = wc;
    }
  }
  buf[i] = L'\0';
}
```
Exceptions
**FIO34-EX1:** If the value returned by a character I/O function is not compared to the `EOF` integer constant expression, there is no need to preserve the value as an `int`, and it may be immediately converted to a `char` type. In general, it is preferable *not* to compare a character with `EOF` because this comparison is not guaranteed to succeed in certain circumstances. (See [void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_).)  
The following code example uses `char` to capture a value from `getchar()` but does not compare it with `EOF`. Converting the `int` output of `getchar()` to a `char` falls under exception `INT31-EX2` of [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](INT31-C_%20Ensure%20that%20integer%20conversions%20do%20not%20result%20in%20lost%20or%20misinterpreted%20data).
Instead,, `feof()` is used to test for end-of-file, and `ferror()` is used to test for errors.
``` c
#include <stdio.h>
void func(void) {
  enum { BUFFER_SIZE = 32 };
  unsigned char buf[BUFFER_SIZE];
  char c;
  int i = 0;
  while (((c = getchar()) != '\n')
          && !feof(stdin)
          && !ferror(stdin)) {
    if (i < (BUFFER_SIZE - 1)) {
      buf[i++] = c;
    }
  }
  buf[i] = '\0';
}
```
## Risk Assessment
Historically, using a `char` type to capture the return value of character I/O functions has resulted in significant [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), including command injection attacks. (See the [CA-1996-22 advisory](http://www.cert.org/advisories/CA-1996-22.html).) As a result, the severity of this error is high.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO34-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| Coverity | 2017.07 | CHAR_IO | Identifies defects when the return value of fgetc(), getc(), or getchar() is incorrectly assigned to a char instead of an int. Coverity Prevent cannot discover all violations of this rule, so further verification is necessary |
| ECLAIR | 1.2 | CC2.FIO34 | Partially implemented |
| Fortify SCA | 5.0 | ; | Can detect violations of this rule with CERT C Rule Pack |
| Splint | 3.1.1 | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO34-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)STR00-C. Represent characters using an appropriate type
INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data |
| SEI CERT C++ Coding Standard | VOID FIO34-CPP. Use int to capture the return value of character IO functions |
| CERT Oracle Secure Coding Standard for Java | FIO08-J. Distinguish between characters or bytes read from a stream and -1 |
| ISO/IEC TS 17961 | Using character values that are indistinguishable from EOF [chreof] |

## Bibliography

|  |  |
| ----|----|
| [NIST 2006] | SAMATE Reference Dataset Test Case ID 000-000-088 |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FIO33-C.+Detect+and+handle+input+output+errors+resulting+in+undefined+behavior?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2952)
## Comments:

|  |
| ----|
| The comment:
It is also non-compliant because EOF is not guaranteed by the C99 standard to be distinct from the value of any unsigned char when converted to an int
;is plain weird.  EOF is a negative integer - and I fail to see how that cannot be distinct from every unsigned char when converted to int.  Did you have 'signed char' (or plain char if CHAR_MIN < 0) in mind?  I'm not excusing the code - it is wrong.  But I don't think this is anything different from the basic "don't use char" reason.
I'm also not on board with this use of feof() and ferror() in loops.  The idiom that I learned still seems sound to me:
[!note]
Â int c;
while ((c = getchar()) != EOF && c != '\n')
{
    /* Consume valid non-newline character - should the code worry about ASCII NUL '\0' in the data? */
}
/* Null terminate accumulated string.  Consider whether EOF means error or just EOF */Â 

This doesn't miss anything that adding the (relatively wasteful) feof() and ferror() calls would catch - assuming a compliant getchar(), of course.  Even if feof() and ferror() are macros, there are two tests instead of just one.
I note that if you want to exclude '\0' from the data, you can modify the loop condition to `while ((c = getchar()) > 0 && c != '\n')` since the standard guarantees that EOF is negative.  (The relevant fragment of the standard says "...the fgetc function obtains that character as an unsigned char converted to an int...".  So, with CHAR_BIT == 8, fgetc() returns a negative value on error or EOF, or a non-negative value 0..255 on success.
Or am I missing something?  If so, what? 
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 18, 2008 03:11
\| \|
The problem occurs when int and (unsigned) char have the same size, which is not unheard of (e.g. for some embedded processors).
Testing for \> 0 is even worse since it malfunctions for all values that convert to negative as an int.
The advice to back up the ==EOF test by feof() and ferror() tests is correct.; Note that they will not be performed unless c==EOF, which for 16-bit char/int occurs by accident 1/65536 of the time for random input (and not at all for valid ASCII or 16-bit Unicode characters), which is not enough overhead to worry about.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 17, 2008 17:53
\| \|
FIO34-C and FIO35-C seem to be two distinct approaches to solving the same problem. We should keep both rules only if there are scenarios where FIO34-C is appropriate but not FIO35-C, and there are also scenarios where FIO35-C is appropriate but not FIO34-C.
Judging from the comments, I'd suggest FIO35-C is the better rule to keep, as the notion of using an `int` to store characters rather than a `char` defeats the notions of int's and char's. (Yes, I've done it often, too; it still hurts!)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 23, 2008 14:23
\| \|
Quick reaction, I think having both rules is OK. Notice the CS in this rule applies both rules.
Note that the functions reference by this rule such as:
``` java
#include <stdio.h>
int fgetc(FILE *stream);
```
Return an `int`, so this rule could really be a specialization of a rule that says "don't mix types" (if we had such a rule).
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 26, 2008 12:39
\|
