> [!warning]  
>
> This guideline has been deprecated.  It has been superseded by:
>
> -   [FIO34-C. Distinguish between characters read from a file and EOF or WEOF](FIO34-C_%20Distinguish%20between%20characters%20read%20from%20a%20file%20and%20EOF%20or%20WEOF)

Character I/O functions such as `fgetc()`, `getc()`, and `getchar()` return a value that may or may not mean `EOF` when `char` is 16 bits or larger and `int` is the same size as `char`. The C Standard does not guarantee that `EOF` is distinguishable from a character in this case. As a result, it is necessary to use the `feof()` and `ferror()` functions to test the end-of-file and error indicators for a stream on such systems \[[Kettlewell 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Kettle02)\].
This problem can occur on a word-addressed machine that uses a large character set.
Note that in the UTF-16 character set, `0xFFFF` is guaranteed not to be a character, which leaves room for `EOF` to be chosen as the value −1. In 16-bit EUC (Extended UNIX Code), the high byte can never be `0xFF`, so a conflict cannot occur at all. Similarly, all UTF-32 characters are positive when viewed as a signed 32-bit integer. Consequently, it would require a custom character set designed without consideration of the C programming language for this problem to occur.
This rule also applies to wide characters. In particular, do not compare a wide character with `WEOF` to detect end-of-file on platforms where `sizeof(wint_t) == sizeof(wchar_t)`. On both 64-bit machines running Ubuntu Linux or Mac OSX, both types are 32 bits.
## Noncompliant Code Example
This noncompliant code example tests to see if the character `c` is not equal to `EOF` as a loop-termination condition:
``` c
#include <stdio.h>
void func(void) {
  int c;
  do {
    c = getchar();
  } while (c != EOF);
}
```
Although `EOF` is guaranteed to be negative and distinct from the value of any `unsigned char`, it is not guaranteed to be different from any such value when converted to an `int`. Consequently, when `int` is the same size as `char`, this loop may terminate early. (See [void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file](void%20FIO34-C_%20Use%20int%20to%20capture%20the%20return%20value%20of%20character%20IO%20functions%20that%20might%20be%20used%20to%20check%20for%20end%20of%20file).)
## Compliant Solution (Portable to Rare Systems)
This compliant solution uses `feof()` to test for end-of-file and `ferror()` to test for errors:
``` c
#include <stdio.h>
void func(void) {
  int c;
  do {
    c = getchar();
  } while (!feof(stdin) && !ferror(stdin));
}
```
## Compliant Solution (Explicitly Nonportable)
This compliant solution uses an assertion to ensure that the code is executed only on architectures where it is guaranteed to work. See [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions) for the definition of the `PRECISION()` macro.
``` c
#include <assert.h>
#include <stdio.h>
void func(void) {
  int c;
  assert(PRECISION(UCHAR_MAX) < PRECISION(INT_MAX));
  do {
    c = getchar();
  } while (c != EOF);
}
```
## Exceptions
**FIO35-EX1:** A number of C functions do not return characters but can return `EOF` as a status code. These functions include `fclose()`, `fflush()`, `fputs()`, `fscanf()`, `puts()`, `scanf()`, `sscanf()`, `vfscanf()`, and `vscanf()`. It is perfectly correct to test these return values to `EOF`.
**FIO35-EX2:** Comparing characters with `EOF` is acceptable if there is an explicit guarantee that `int` can represent more values than `char` on all supported platforms. This guarantee is usually easy to make because [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) on which these types are the same size are rare.
## Risk Assessment
The C Standard requires only that an `int` type be able to represent a maximum value of +32767 and that a `char` type be no larger than an `int`. Although uncommon, this situation can result in the integer constant expression `EOF` being indistinguishable from a normal character; that is, `(int)(unsigned char)65535 == -1`. Consequently, failing to use `feof()` and `ferror()` to detect end-of-file and file errors can result in incorrectly identifying the `EOF` character on rare implementations where `sizeof(int)` equals the `sizeof(char)`.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO35-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Fortify SCA | 5.0 | ; | Can detect violations of this rule with CERT C Rule Pack |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO35-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of fileDCL03-C. Use a static assertion to test the value of a constant expression |
| SEI CERT C++ Coding Standard | VOID FIO35-CPP. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |

## Bibliography

|  |  |
| ----|----|
| [Kettlewell 2002] | Section 1.2, "<stdio.h> and Character Types" |
| [Summit 2005] | Question 12.2 |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FIO34-C.+Use+int+to+capture+the+return+value+of+character+IO+functions?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040) [](https://www.securecoding.cert.org/confluence/display/seccode/FIO37-C.+Do+not+assume+that+fgets%28%29+returns+a+nonempty+string+when+successful)
## Comments:

|  |
| ----|
| Wietse Venema sez:
You need to revisit FIO35-C. This claims that getchar() can't
distinguish between EOF and non-EOF character values. This results
in collateral damage elsewhere in the guideline where tests for EOF
have been replaced with tests of feof() and ferror().
The "problem" hinted at in FIO35-C can happen only on non-existent
systems where sizeof(char)==sizeof(int). And since int is at least
16 bits, this means the "problem" happens on non-existent systems
where char is at least a 16-bit type.
                                        Posted by svoboda at Apr 16, 2008 10:15
                                     |
| As seen from the comments in FIO34-C, there are a few (rare) platforms where sizeof(char)==sizeof(int).
                                        Posted by svoboda at Apr 23, 2008 14:18
                                     |
| Added a comment to FIO34-C regarding it and this rule.
                                        Posted by svoboda at Apr 23, 2008 14:22
                                     |
| #posting comments in place of Yozo Toda.
I wonder what is "16-bit EUC"?
Here in Japan, we have EUC-JP, which is a variable-width encoding;
    ascii character set is encoded in 8 bit width
    Japanese character set is encoded in 16 bit width with each byte having higher bit set ("1")
the description in FIO35 differs from EUC-JP.
I found that the japanese Wikipedia page of EUC says there are two formats for EUC, "EUC Packed Format" and "EUC Fixed Width Format".
 Extended Unix Code
 http://en.wikipedia.org/wiki/Extended_Unix_Code
 Extended Unix Code
 http://ja.wikipedia.org/wiki/Extended_Unix_Code
Do you mean "16-bit EUC" as "EUC Fixed Width Format"?
I searched around the web but cannot find the specification of "EUC Fixed Width Format."
                                        Posted by masaki at Aug 26, 2009 22:24
                                     |
| EUC-JP looks like it could not be problematic on a platform where char is two bytes.The lower half of JIS-X-0201 is one byte, but 0xFF is not allowed.; The upper half of JIS-X-0201 is two bytes with the lead byte being 0x8E, which means it cannot be -1.  JIS-X-0208 (code set 1) is two bytes, but 0xFF is not allowed in either.  JIS-X-0212 (code set 3) is three bytes, but again, 0xFF cannot be any of the three.  So in all cases, there's no way to form -1. In fact, as far as I can tell, none of the EUC code pages have the high byte set to 0xFF, so none of them can be -1.  The confusion seems to come from "high bit" being used incorrectly.
                                        Posted by aballman at Oct 07, 2013 13:58
                                     |

