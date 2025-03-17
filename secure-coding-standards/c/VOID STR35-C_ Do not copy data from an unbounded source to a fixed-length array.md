Functions that perform unbounded copies often rely on external input to be a reasonable size. Such assumptions may prove to be false, causing a buffer overflow to occur. For this reason, care must be taken when using functions that may perform unbounded copies.
## Noncompliant Code Example (`strcat()`)
Using the `strcat()` or `strcpy()` function to copy a string of an unknown length into a buffer of limited size is a frequent cause of buffer overflows and one of the leading sources of security [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). This noncompliant code example assumes that the length of command-line arguments of the program does not exceed 4096 bytes and concatenates all arguments into the fixed-size buffer without checking for the possibility of overflow. When the call to `strcat()` or any other string utility function attempts to write past the end of the buffer, the behavior of the program is undefined (see [undefined behavior 181](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_181).)
``` c
#include <string.h>
int main(int argc, char *argv[]) {
  char cmdline [4096];
  cmdline[0] = '\0';
  for (int i = 1; i < argc; ++i) {
    strcat(cmdline, argv[i]);
    strcat(cmdline, " ");
  }
  return 0;
}
```
## Compliant Solution (`memcpy()`)
This compliant solution avoids making assumptions about the maximum length of the command-line arguments and instead dynamically allocates sufficient space for all arguments regardless of their length and safely copies each into the provided space. The solution is not only safer but also more robust in that it does not needlessly impose artificial limits on users of the program.
``` c
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]) {
  size_t bufsize = 0;
  size_t buflen = 0;
  char *cmdline = NULL;
  for (int i = 1; i < argc; ++i) {
    const size_t len = strlen(argv[i]);
    if (bufsize - buflen <= len) {
      char *newCmdLine;
      bufsize = (bufsize + len + 1) * 2;
      newCmdLine = realloc(cmdline, bufsize);
      if (NULL == newCmdLine) {
        free(cmdline);
        return EXIT_FAILURE;
      }
      cmdline = newCmdLine;
    }
    memcpy(cmdline + buflen, argv[i], len);
    buflen += len;
    cmdline[buflen++] = ' ';
  }
  if (cmdline) {
    cmdline[buflen] = '\0';
  }
  free(cmdline);
  return EXIT_SUCCESS;
}
```
## Noncompliant Code Example (`gets()`)
The `gets()` function, which was deprecated in the C99 Technical Corrigendum 3 and removed from C11, is inherently unsafe and should never be used because it provides no way to control how much data is read into a buffer from `stdin`. This noncompliant code example assumes that `gets()` will not read more than `BUFSIZ - 1` characters from `stdin`. This is an invalid assumption, and the resulting operation can cause a buffer overflow. Note further that `BUFSIZ` is a macro integer constant, defined in `stdio.h`, representing a suggested argument to `setvbuf()` and not the maximum size of such an input buffer.
The `gets()` function reads characters from the `stdin` into a destination array until end-of-file is encountered or a newline character is read. Any newline character is discarded, and a null character is written immediately after the last character read into the array.
``` c
#include <stdio.h>
void func(void) {
  char buf[BUFSIZ];
  if (gets(buf) == NULL) {
    /* Handle error */
  }
}
```
See also [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions).
## Compliant Solution (`fgets()`)
The `fgets()` function reads, at most, one less than a specified number of characters from a stream into an array. This solution is compliant because the number of bytes copied from `stdin` to `buf` cannot exceed the allocated memory:
``` c
#include <stdio.h>
#include <string.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  int ch;
  if (fgets(buf, sizeof(buf), stdin)) {
    /* fgets succeeds; scan for newline character */
    char *p = strchr(buf, '\n');
    if (p) {
      *p = '\0';
    } else {
      /* Newline not found; flush stdin to end of line */
      while (((ch = getchar()) != '\n')
            && !feof(stdin)
            && !ferror(stdin))
        ;
    }
  } else {
    /* fgets failed; handle error */
  }
}
```
The `fgets()` function, however, is not a strict replacement for the `gets()` function because `fgets()` retains the newline character (if read) but may also return a partial line. It is possible to use `fgets()` to safely process input lines too long to store in the destination array, but this is not recommended for performance reasons. Consider using one of the following compliant solutions when replacing `gets()`.
## Compliant Solution (`gets_s()`, Annex K)
The `gets_s()` function reads, at most, one less than the number of characters specified from the stream pointed to by `stdin` into an array.
Annex K, subclause K.3.5.4.1, of the C Standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] states:
> No additional characters are read after a new-line character (which is discarded) or after end-of-file. The discarded new-line character does not count towards number of characters read. A null character is written immediately after the last character read into the array.

If end-of-file is encountered and no characters have been read into the destination array, or if a read error occurs during the operation, then the first character in the destination array is set to the null character and the other elements of the array take unspecified values:
``` c
#define __STDC_WANT_LIB_EXT1__
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  if (gets_s(buf, sizeof(buf)) == NULL) {
    /* Handle error */
  }
}
```
## Compliant Solution (`getline()`, POSIX)
The `getline()` function behaves similarly to `fgets()` but offers several extra features. First, if the input line is too long, it resizes the buffer, using `realloc()`, rather than truncating the input. Second, if successful, it returns the number of characters read, which is useful in determining whether the input has any null characters before the newline.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void func(void) {
  int ch;
  size_t buffer_size = 32;
  char *buffer = malloc(buffer_size);
  if (!buffer) {
    /* Handle error */
    return;
  }
  if ((ssize_t size = getline(&buffer, &buffer_size, stdin))
        == -1) {
    /* Handle error */
  } else {
    char *p = strchr(buffer, '\n');
    if (p) {
      *p = '\0';
    } else {
      /* Newline not found; flush stdin to end of line */
      while (((ch = getchar()) != '\n')
         && !feof(stdin)
         && !ferror(stdin))
        ;
    }
  }
  free (buffer);
}
```
`getline()` works only with buffers allocated with `malloc()`. If passed a `NULL` pointer, `getline()` allocates a buffer of sufficient size to hold the input. As such, the user must explicitly `free()` the buffer later. Do not pass `NULL` to `getline()` because this is a violation of [MEM00-C. Allocate and free memory in the same module, at the same level of abstraction](MEM00-C_%20Allocate%20and%20free%20memory%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction).
## Noncompliant Code Example (`getchar()`)
This noncompliant cod example uses the `getchar()` function to read one character at a time from `stdin` instead of reading the entire line at once. The `stdin` stream is read until end-of-file is encountered or a newline character is read. Any newline character is discarded, and a null character is written immediately after the last character read into the array. Similar to the previous example, there are no guarantees that this code will not result in a buffer overflow.
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  char *p;
  int ch;
  p = buf;
  while (((ch = getchar()) != '\n')
         && !feof(stdin)
         && !ferror(stdin)) {
    *p++ = ch;
  }
  *p++ = 0;
}
```
## Compliant Solution (`getchar()`)
In this compliant solution, characters are no longer copied to `buf` once `index == BUFFERSIZE - 1`, leaving room to null-terminate the string. The loop continues to read characters until the end of the line, the end of the file, or an error is encountered.
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  unsigned char buf[BUFFERSIZE];
  int ch;
  int index = 0;
  int chars_read = 0;
  while (((ch = getchar()) != '\n')
          && !feof(stdin)
          && !ferror(stderr)) {
    if (index < sizeof(buf) - 1) {
      buf[index++] = (unsigned char)ch;
    }
    chars_read++;
  }
  buf[index] = '\0';  /* Terminate NTBS */
  if (feof(stdin)) {
    /* Handle EOF */
  }
  if (ferror(stdin)) {
    /* Handle error */
  }
  if (chars_read > index) {
    /* Handle truncation */
  }
}
```
After the loop ends, if `feof(stdin) != 0`, the loop has read through to the end of the file without encountering a newline character. Similarly, if `ferror(stdin) != 0`, a read error occurred before the loop encountered a newline character, and if `chars_read > index`, the input string has been truncated. [void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file](void%20FIO34-C_%20Use%20int%20to%20capture%20the%20return%20value%20of%20character%20IO%20functions%20that%20might%20be%20used%20to%20check%20for%20end%20of%20file) is also applied in this solution.
Reading one character at a time provides more flexibility in controlling behavior without additional performance overhead.
The following test for the `while` loop is normally sufficient:
``` java
while (((ch = getchar()) != '\n') && ch != EOF)
```
See [void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_) for the case where `feof()` and `ferror()` must be used instead.
## Noncompliant Code Example (`scanf()`)
The `scanf()` function is used to read and format input from `stdin`. Improper use of `scanf()` can result in an unbounded copy. In this noncompliant code example, the call to `scanf()` does not limit the amount of data read into `buf`. If more than nine characters are read, a buffer overflow occurs.
``` c
#include <stdio.h>
enum { CHARS_TO_READ = 9 };
void func(void) {
  char buf[CHARS_TO_READ + 1];
  scanf("%s", buf);
}
```
## Compliant Solution (`scanf()`)
The number of characters read by `scanf()` can be bounded by using the format specifier supplied to `scanf()`:
``` c
#include <stdio.h>
enum { CHARS_TO_READ = 9 };
void func(void) {
  char buf[CHARS_TO_READ + 1];
  scanf("%9s", buf);
}
```
## Risk Assessment
Copying data from an unbounded source to a buffer of fixed size may result in a buffer overflow.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR35-C | High | Likely | Medium |  P18  |  L1  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  | Can detect some violations of this rule |
| Coverity | 2017.07 | SECURE_CODING  | Fully Implemented |
| LDRA tool suite | 9.7.1 |  |  |
| PRQA QA-C | Unable to render {include} The included page could not be found. | warncall for 'gets' | Partially implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR35-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | MSC24-C. Do not use deprecated or obsolescent functions  MEM00-C. Allocate and free memory in the same module, at the same level of abstraction 
 void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file 
 void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| SEI CERT C++ Coding Standard | STR50-CPP. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| ISO/IEC TS 17961 | Tainted strings are passed to a string copying function [taintstrcpy] |
| MITRE CWE | CWE-120, Unbounded transfer ("classic buffer overflow") |

##  Bibliography

|  |  |
| ----|----|
| [Drepper 2006] | Section 2.1.1, "Respecting Memory Bounds" |
| [ISO/IEC 9899:2011] | Subclause K.3.5.4.1, "The gets_s function" |
| [Lai 2006] |  |
| [NIST 2006] | SAMATE Reference Dataset Test Case ID 000-000-088 |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=271) [](https://www.securecoding.cert.org/confluence/display/seccode/STR36-C.+Do+not+specify+the+bound+of+a+character+array+initialized+with+a+string+literal?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| What do fgets and getchar do when newlines are CR-LF (Microsoft Windows) or CR (MacOS through v9)?  I can imagine fgets converting the character, but would not expect getchar to (and would argue that it would be incorrect behavior if it did).  
Another concern is whether fgets converts the CRLF to a single newline under Microsoft Windows either.  MSDN implies that it does, but I haven't set-up MSVC to test it.
                                        Posted by hburch at Jun 05, 2007 09:30
                                     |
| the BSD version of fgets does no conversions, it is simply copies memory in the dumbest way possible
looks like GNU and Microsoft versions are written more or less the same and do no conversions of any type (of course this depends on how trustworthy the internet is at giving me source code...)
                                        Posted by avolkovi at Mar 06, 2008 10:46
                                     |
| By reputation (rather than empirical experiment, in other words), the behaviour of fgets() on Windows will depend on whether the file is opened as a text file or a binary file -- whereas on Unix there is no difference between those two.; If the file is opened as a text file, then fgets() will strip the CR and leave the LF.  If the file is opened as a binary file, then fgets() will not strip the CR (so the string will normally end CRLF when the input operation completes).  Similar comments apply to all the other functions.  Kernighan & Pike's "The Practice of Programming" illustrates a variant of fgets() that handles three separate line termination conventions - Unix with LF, MacOS (pre-X) with CR, and Windows with CRLF (Chapter 4, on reading CSV data; function endofline()).
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 22:50
                                     |
| The gets_s() example should probably use sizeof rather than BUFSIZ in the call.
Kernighan and Pike's "The Practice of Programming" (also referenced in my response to Hal's comment) mentions the problem with scanf() and string formats, and suggests using sprintf() to format the scanf() format string - see the function 'build()' in the C implementation of the Markov program in chapter 3.; One more trouble with the example is that the 9 in the string is 'sizeof(buf)-1' - so changing the size of buf requires (at least) two changes in the program.  TPOP avoids that - at some cost in runtime performance, but greater reliability and security.  There's an item somewhere about making related constants properly related, and unrelated constants properly unrelated.  This is a case of related constants not looking identical.  (And TPOP has an explicit example of 'related constants' in chapter 1 - with a remarkable piece of code that includes explicit values 20, 21, 22, 23 and 27 -- but the only two numbers of relevance are 24 (lines on the screen) and 26 (letters in the alphabet), neither of which actually appears in the code.) 
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 23:21
                                     |
| Both are now taken care of.
                                        Posted by dmk at Mar 30, 2008 22:55
                                     |
| The C standard requires that all streams opened in text mode (including the three standard streams) properly handle the mapping between the internal newline character and whatever is used externally to represent it, be it CR,LF or a record size maintained in an associated index file.
                                        Posted by dagwyn at Apr 16, 2008 21:47
                                     |
| Ale Contenti @ Microsoft sez:
I heartily agree with everything here. gets() was the main reason why we entered in the Safer CRT function (TR 24731) business. I do have a couple of suggestions.
(1) In the example about get_s():
char buf[BUFSIZ];
if (gets_s(buf, sizeof(buf)) == NULL) {
  /* handle error */
}

I would not use sizeof(buf), but \_countof(buf). Since \_countof is not part of the Std (yet? Can we ask to add it?) at least I would use sizeof(buf)/sizeof(buf[0](/confluence/pages/createpage.action?spaceKey=c&title=0)) or something similar.
\(2\) in the getchar() complaint solution, I would point out how hard is to write a compliant solution. Using the \_s functions is more natural and leads to far more readable and maintainable code.
\(3\) scanf_s would be a compliant solution for scanf, right? Any reason why is not listed?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2008 12:30
\| \|
I just discovered that BUFSIZ is defined in C99, as part of \<stdio.h\>. Section 7.19.1:
> which expands to an integer constant expression that is the size of the buffer used by the setbuf function;

Since we are not using this definition of BUFSIZ perpahs, we should change the code to use a different variable name.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 18, 2009 11:32
\| \|
Yes, I knew that. 8^)
When I first used `BUFSIZ` in the noncompliant code example, the intent was to illustrate a possible misconception that `BUFSIZ` represented the maximum buffer size that could be read by `gets()`. Perhaps the usage has devolved from here.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 18, 2009 14:28
\| \|
A rule that applies to strings calls for an example with string functions (in addition to all the I/O) – I added one.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 28, 2010 23:33
\| \|
I think it would be worthwhile to add cwe 242 reference as well.
![](images/icons/contenttypes/comment_16.png) Posted by azukich at Feb 22, 2010 12:32
\| \|
I have feeling that a good number of NCCEs might actually exhibit weaknesses that aren't directly intended to be addressed by the guidelines they go with. [CWE-242: Use of Inherently Dangerous Function](http://cwe.mitre.org/data/definitions/242.html) is a good example – `gets()` is an inherently unsafe function that should be avoided. But there is a rule that specifically addresses `gets()` (among others): [MSC34-C. Do not use deprecated or obsolescent functions](/confluence/pages/createpage.action?spaceKey=c&title=MSC34-C.+Do+not+use+deprecated+or+obsolescent+functions). That rule should definitely reference CWE-242.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 22, 2010 15:53
\|
