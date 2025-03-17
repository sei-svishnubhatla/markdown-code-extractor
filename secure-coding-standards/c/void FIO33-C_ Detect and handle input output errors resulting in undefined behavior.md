It is essential to always check the status of I/O functions that can fail and leave variables improperly initialized. Failure to detect and properly handle these errors can lead to [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) program behavior.
The following quote from Apple's *Secure Coding Guide* \[[Apple 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Apple06)\] demonstrates the importance of error handling:
> Most of the file-based security vulnerabilities that have been caught by Apple's security team could have been avoided if the developers of the programs had checked result codes. For example, if someone has called the `chflags` utility to set the immutable flag on a file and you call the `chmod` utility to change file modes or access control lists on that file, then your `chmod` call will fail, even if you are running as root. Another example of a call that might fail unexpectedly is the `rm` call to delete a directory. If you think a directory is empty and call `rm` to delete the directory, but someone else has put a file or subdirectory in there, your `rm` call will fail.

The C Standard I/O functions defined in subclause 7.21 and in Annex K provide a clear indication of failure or success. [ERR33-C. Detect and handle standard library errors](https://www.securecoding.cert.org/confluence/display/seccode/ERR33-C.+Detect+and+handle+standard+library+errors) describes how to test for failure of I/O and other standard library functions.
## Noncompliant Code Example (`fgets()`)
The `fgets()` function can fail and return a null pointer. This noncompliant code example fails to test for the error return from `fgets()`.
``` c
#include <stdio.h>
#include <string.h>
void func(void) {
  enum { BUFFERSIZE = 32 };
  char buf[BUFFERSIZE];
  fgets(buf, sizeof(buf), stdin);
  buf[strlen(buf) - 1] = '\0'; /* Overwrite newline */
}
```
The `fgets()` function does not distinguish between end-of-file and error, and callers must use `feof()` and `ferror()` to determine which occurred. If `fgets()` fails, the array contents are either unchanged or indeterminate depending on the reason for the error. According to subclause 7.21.7.2, paragraph 2, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> The `fgets` function returns `s` if successful. If end-of-file is encountered and no characters have been read into the array, the contents of the array remain unchanged and a null pointer is returned. If a read error occurs during the operation, the array contents are indeterminate and a null pointer is returned.

It is possible that `buf[0]` will contains a null character so that `strlen(buf)` will return 0. As a result, the assignment statement meant to overwrite the newline character will result in a write-outside-array-bounds error.
## Compliant Solution (`fgets()`)
This compliant solution checks the return value for `fgets()` before processing the input buffer:
``` c
#include <stdio.h>
#include <string.h>
void func(void) {
  enum { BUFFERSIZE = 32 };
  char buf[BUFFERSIZE];
  char *p;
  if (fgets(buf, sizeof(buf), stdin)) {
    /* fgets succeeds; scan for newline character */
    p = strchr(buf, '\n');
    if (p) {
      *p = '\0';
    } else {
      /* Newline not found; flush stdin to end of line */
      while ((getchar() != '\n')
             && !feof(stdin)
             && !ferror(stdin))
        ;
    }
  } else {
    /* fgets failed; handle error */
  }
}
```
The solution checks for an error condition from `fgets()` and allows for application-specific error handling. If `fgets()` succeeds, the resulting buffer is scanned for a newline character, and if it is found, it is replaced with a null character. If a newline character is not found, `stdin` is flushed to the end of the line to simulate the functionality of `gets()`. See [FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful](FIO37-C_%20Do%20not%20assume%20that%20fgets__%20or%20fgetws__%20returns%20a%20nonempty%20string%20when%20successful) for more information.
The following test for the `while` loop is normally sufficient:
``` java
int c;
while ((c = getchar()) != '\n' && !feof(stdin) && !ferror(stdin))
```
For more information, see [FIO34-C. Distinguish between characters read from a file and EOF or WEOF](FIO34-C_%20Distinguish%20between%20characters%20read%20from%20a%20file%20and%20EOF%20or%20WEOF).
## Noncompliant Code Example (`fopen()`)
In this example, the `fopen()` function is used to open the file referred to by `file_name`. However, if `fopen()` fails, the value of `fptr` will be `NULL`. When `fptr` is then dereferenced in the call to `fclose()`, the program may crash or behave in an unintended manner.
``` c
#include <stdio.h>
int truncate_file(const char *file_name) {
  FILE *fptr = fopen(file_name, "w");
  return fclose(fptr);
}
```
## Compliant Solution (`fopen()`)
The `fopen()` function returns a null pointer to indicate that an error occurred. Testing for errors before processing the file, as shown in this compliant solution, eliminates the undefined behavior resulting from dereferencing a null pointer. Always test the returned value to make sure an error did not occur before operating on the file. If an error did occur, handle it appropriately.
``` c
#include <stdio.h>
int truncate_file(const char *file_name) {
  FILE *fptr = fopen(file_name, "w");
  if (NULL == fptr) {
    return -1;
  }
  return fclose(fptr);
}
```
## Noncompliant Code Example (`snprintf()`)
Check return status from calls to `snprintf()` and related functions. The `snprintf()` function returns −1 on an encoding error or a value greater than or equal to the buffer size if the full result does not fit in the buffer.
In this noncompliant code example, the variable `j`, already at 0, can be decremented further, almost always with unexpected results. Although this particular error is not commonly associated with software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), it can easily lead to [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).
A return value greater than or equal to the buffer size would limit the size passed to the next call to `snprintf()` in this example, but a string truncation would go undetected.
``` c
#include <stdio.h>
int fmt_data(char *buffer, size_t bufsize, char *s, char c,
             int i, float fp) {
  int j;
  j = snprintf(buffer, bufsize, " String:    %s\n", s);
  j += snprintf(buffer + j, bufsize - j, " Character: %c\n",
                (unsigned char)c);
  j += snprintf(buffer + j, bufsize - j, " Integer:   %d\n",
                i);
  j += snprintf(buffer + j, bufsize - j, " Real:      %f\n",
                fp);
  return j;
}
```
Note that when passing an object of type `char` to `snprintf()` or related functions, the caller should cast the object to `unsigned char` to avoid potential sign extension (as described in [STR37-C. Arguments to character-handling functions must be representable as an unsigned char](STR37-C_%20Arguments%20to%20character-handling%20functions%20must%20be%20representable%20as%20an%20unsigned%20char)).
## Compliant Solution (`snprintf()`)
In this compliant solution, the value returned from `snprintf()` stored in `rc` is checked before being added to the count of characters written and stored in `nbytes`. The function's return type is also changed from `int` to `size_t` to avoid the possibility of data truncation. (See [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](INT31-C_%20Ensure%20that%20integer%20conversions%20do%20not%20result%20in%20lost%20or%20misinterpreted%20data).)
``` c
#include <stdio.h>
size_t fmt_data(char *buffer, size_t bufsize, char *s, char c,
                int i, float fp) {
  int rc;
  size_t nbytes = 0;
  rc = snprintf(buffer, bufsize, " String: %s\n", s);
  if (rc < 0) { /* Handle error */ }
  else if (rc >= bufsize) { /* Handle truncated output */ }
  else { nbytes += rc; }
  rc = snprintf(buffer + nbytes, bufsize - nbytes, " Character: %c\n",
                (unsigned char)c);
  if (rc < 0) { /* Handle error */ }
  else if (rc >= bufsize - nbytes) { /* Handle truncated output */ }
  else { nbytes += rc; }
  rc = snprintf(buffer + nbytes, bufsize - nbytes, " Integer: %d\n",
                i);
  if (rc < 0) { /* Handle error */ }
  else if (rc >= bufsize - nbytes) { /* Handle truncated output */ }
  else { nbytes += rc; }
  rc = snprintf(buffer + nbytes, bufsize - nbytes, " Real: %f\n",
                fp);
  if (rc < 0) { /* Handle error */ }
  else if (rc >= bufsize - nbytes) { /* Handle truncated output */ }
  else { nbytes += rc; }
  return nbytes;
}
```
## Noncompliant Code Example (`snprintf()`)
In this noncompliant code example, the `snprintf()` function is called twice: first with a null buffer and 0 size to determine the size of a buffer large enough to fit the formatted string and a second time to perform the actual formatting into the dynamically allocated buffer. If the first call to `snprintf()` fails by returning a negative value (for example, because of insufficient memory, as described in GNU libc bug [441945](http://bugzilla.redhat.com/show_bug.cgi?id=441945) ), using the negative value as an argument to `malloc()` may cause the function to fail to allocate storage and return `NULL`, leading to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in the subsequent call to `snprintf()`. If the first call to `snprintf()` and the call to `malloc()` both succeed, but the second call to `snprintf()` fails, the `fmtint()` function returns a pointer to uninitialized memory to the caller, possibly leading to undefined behavior when the contents of the buffer are accessed.
``` c
#include <stdio.h>
#include <stdlib.h>
char *fmtint(int i, int width, int prec) {
  int n;
  char *buf;
  static const char fmt[] = "%*.*d";
  /* Determine the size of the buffer */
  n = snprintf(NULL, 0, fmt, width, prec, i);
  /* Assume successful return from snprintf() */
  buf = (char *)malloc(n + 1);
  /* Assume successful return from malloc() */
  snprintf(buf, n + 1, fmt, width, prec, i);
  return buf;
}
```
## Compliant Solution (`snprintf()`)
This compliant solution checks the value returned from `snprintf()` after each call to the function and avoids using the value in a way that might lead to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior):
``` c
#include <stdio.h>
#include <stdlib.h>
char *fmtint(int i, int width, int prec) {
  int n;
  char *buf;
  static const char fmt[] = "%*.*d";
  /* Determine the size of the buffer */
  n = snprintf(NULL, 0, fmt, width, prec, i);
  /* Check for snprintf() failure */
  if (n < 0) {
    return NULL;
  }
  /* Check for malloc() failure */
  buf = (char *)malloc(n + 1);
  if (NULL == buf) {
    return NULL;
  }
  /* Check again for snprintf() failure */
  n = snprintf(buf, n + 1, fmt, width, prec, i);
  if (n < 0) {
    free(buf);
    buf = NULL;
  }
  return buf;
}
```
## Risk Assessment
Failure to handle certain input/output errors may result in undefined behavior or possible buffer overflow [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO33-C | High | Probable | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this rule when checking for violations of EXP12-C. Do not ignore values returned by functions |
| Coverity | 2017.07 | CHECKED_RETURN | Finds inconsistencies in how function call return values are handled. Coverity Prevent cannot discover all violations of this rule, so further verification is necessary |
| Fortify SCA | 5.0 | ; | Can detect violations of this rule with CERT C Rule Pack |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO33-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | VOID STR35-C. Do not copy data from an unbounded source to a fixed-length arraySTR37-C. Arguments to character-handling functions must be representable as an unsigned char
INT31-C. Ensure that integer conversions do not result in lost or misinterpreted dataFIO34-C. Distinguish between characters read from a file and EOF or WEOF
FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful |
| SEI CERT C++ Coding Standard | VOID FIO33-CPP. Detect and handle input output errors resulting in undefined behavior |
| MITRE CWE | CWE-391, Unchecked error condition |

## Bibliography

|  |  |
| ----|----|
| [Apple 2006] | "Secure File Operations" |
| [Haddad 2005] | ; |
| [ISO/IEC 9899:2011] | Subclause 7.21.7.2, "The fgets Function" |
| [Kettlewell 2002] | Section 6, "I/O Error Checking" |
| [Seacord 2013] | Chapter 6, "Formatted Output" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FIO32-C.+Do+not+perform+operations+on+devices+that+are+only+appropriate+for+files?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040) [](https://www.securecoding.cert.org/confluence/display/seccode/FIO34-C.+Use+int+to+capture+the+return+value+of+character+IO+functions?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| For practical purposes, I would like to see more info about handling fgets(). Consider the program
at http://zakalwe.fi/tmp/fgets3.c
while (1) {Â 
Â Â Â  Â Â  Â Â Â Â  s = fgets(buf, sizeof buf, stdin);
Â Â Â  Â Â Â  Â Â Â  if (s == NULL && (feof(stdin) || ferror(stdin)))
            break;
} Â 

 As a surprise, this loop terminates because fgets() returns NULL and libc sets an error condition for stdin. Note, stdin still has data to be read. Only checking (s == NULL && feof(stdin)) works. I suspect there are many programs that are affected with this behavior. Should there be more info about IO handling in the secure coding standard?  
![](images/icons/contenttypes/comment_16.png) Posted by heikki.orsila@iki.fi at Mar 16, 2008 16:23
\| \|
One addition: Exit of a child causes the fgets() to exit unobviously. For POSIX read() this would be obvious. A common phenomena in many programs I suspect.
![](images/icons/contenttypes/comment_16.png) Posted by heikki.orsila@iki.fi at Mar 16, 2008 16:26
\| \|
In a correct implementation, fgets should not be affected by any child exiting.;   If it is affected (presumably by a read operation on a slow device being interrupted by SIGCLD before any data is transferred), then most likely so are all other stdio input functions, since they typically share the same \_filbuf() function to invoke read().  This would be a bug in the implementation of \_filbuf(), which should do the usual testing to determine why read returned -1 and iterate when it is a spurious "error" like interruption by a signal (errno==EINTR).  I note that the original Unix System V Release 4 does have this bug.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 17, 2008 17:05
\| \|
The code sample as you entered in in your comment does the expected thing for me (on ubuntu 7.10 / gcc 4.1)...no abnormal termination.
So your problem is signal-related, due to interactions between `fgets()` and signal behavior.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2008 16:31
\| \|
I converted the ints for width and precision to be size_t in conformance with:
INT01-C. Use rsize_t or size_t for all integer values representing the size of an object
I didn't change `n` because this clearly needs to be signed.
This suggests an exception to INT01-C which is "unless the variable is used to store the return value from a function with a return type of int"\>
Yes? No?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 01, 2010 19:39
\| \|
There are a few minor problems with the first **Compliant Solution (`snprintf()`)** that I think should be corrected:
1.  since `snprintf()` returns any negative value on error (not necessarily exactly -1) a compliant solution must check for `rc < 0` rather than for `rc == -1`
2.  since a return value from `snprintf()` in excess of the second argument indicates a successful completion of the function (i.e., not an error), a compliant solution should distinguish the two cases and handle each separately (rather than by common code as suggested in the example)
3.  strictly speaking, a compliant solution should also check for integer overflow when incrementing the index into the buffer (denoted `j` in the example) in order to comply with [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow)
4.  while correct as shown in the example, in general, when passing an object of type `char` to `snprintf()` or friends the caller should cast the object to `unsigned char` in order to avoid potential sign extension (as described in [STR37-C. Arguments to character handling functions must be representable as an unsigned char](/confluence/pages/createpage.action?spaceKey=seccode&title=STR37-C.+Arguments+to+character+handling+functions+must+be+representable+as+an+unsigned+char))
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 01, 2010 19:49
\| \|
The *width* and *precision* arguments to `sprintf()` format directives must be of type `int`. Quoting from the spec:
> A field *width*, or *precision*, or both, may be indicated by an asterisk (`'*'`). In this case an argument of type `int` supplies the field width or precision. ...

Passing them as any other type leads to undefined behavior (which might be a worthwhile example to add to [FIO00-C. Take care when creating format strings](/confluence/pages/createpage.action?spaceKey=c&title=FIO00-C.+Take+care+when+creating+format+strings)).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 01, 2010 20:01
\| \|
Sounds like a good idea. Definitely tripped me up. I went ahead and did this.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 02, 2010 07:07
\| \|
1\. done 2. ok, i made this change. i also converted to a function, so there was a chance the formatted arguments would not fit in the buffer.  
3. I changed `j` to always between 0 and `MAXBUFSIZE` so there is no chance for overflow.  
4. Is this really necessary when the function takes a `char` and not an `int`? There is also a recommendation [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type) that says to use plain char for character data.
I didn't get to compiler the new examples... they may be badly flawed.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 02, 2010 08:31
\| \|
Great, thanks for doing that! FWIW, I started converting the code to a function but ran out of steam. I think it would be quite helpful if all code examples were written in the form of "general-purpose" functions with as few hardcoded values as possible. Would adding such a guideline to the Coding Guidelines section be appropriate?
Regarding (4), since the `char` argument to `%c` is promoted to `int` when passed through the ellipsis it may be subject to sign extension. According to my understanding of the spec, converting the sign-extended `int` into `unsigned char` may result in a different binary pattern than the original `char` argument when `CHAR_MAX` \< `UCHAR_MAX / 2` and when `char` objects consist of one or more *padding bits* and have *trap representations*.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 02, 2010 12:27
\| \|
WRT (4) I see what you mean now and made the change. I was thinking of something else (the char \*) arguments.
I'm on the fence about a guideline for writing general purpose functions. This sounds a little bit like meta guidance for how to develop guidelines. We have a really poorly maintained page <https://www.securecoding.cert.org/confluence/display/sci/Secure+Coding+Standard+Development+Guidelines> that tries to provide such guidance. We could make this suggestion there, if it is only meant to apply to the development of guidelines.
As a general recommendation to programmers, it almost seems too general, like "use meaningful variable names". I also believe it is possible to "over generalize" functions over variables that do not vary in an application. This is sometime done for the sake of evolvability but I really think it can be overdone. Anyway, a recommendation to "appropriately generalize" functions might go in section [13. Application Programming Interfaces (API)](/confluence/pages/createpage.action?spaceKey=c&title=13.+Application+Programming+Interfaces+%28API%29). This is a reasonable place to put some advice on how to decompose a program into functions. I would think this would be low priority, especially since "appropriate" is likely to be subjective.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 02, 2010 14:16
\| \|
Right, I did mean adding it to the Development Guidelines (not as a rule or recommendation for users of the coding standard).
I also think each non-compliant example should actually demonstrate the diagnosable violation of the rule or recommendation in code rather than just doing so in the form of a comment. For instance, the **Noncompliant Code Example (`fopen()`** on this page:
``` java
FILE * fptr = fopen(file_name, "w");
/* process file */
```
isn't really non-compliant at all since `fptr` is never accessed.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 02, 2010 14:25
\| \|
yes, sounds good.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 02, 2010 15:52
\| \|
The name of this rule is misleading. Taken literally, it calls for the empty set of conditions to be handled: no I/O errors result in undefined behavior in and of themselves. Rather, it is the failure to detect such errors and assuming that none occurred that can subsequently lead to undefined behavior.
I think this rule should be renamed to **FIO33-C. Detect and handle input output errors**. Are there any objections to renaming it?
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 17, 2010 12:41
\| \|
Yes. We already have that recommendation: [FIO04-C. Detect and handle input and output errors](/confluence/pages/createpage.action?spaceKey=c&title=FIO04-C.+Detect+and+handle+input+and+output+errors) ![](images/icons/emoticons/smile.svg)
I think this rule is meant to be an enforceable version of that recommendation...it is supposed to apply to functions where ignoring their output can lead to UB. Perhaps a better title would be
FIO33-C. Detect and handle input output errors that, when ignored, can lead to undefined behavior
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 18, 2010 09:28
\| \|
Indeed we have – thanks for pointing it out! Let me add a reference to it.
But in light of FIO04-C, I find this rule superfluous. Failing to handle I/O errors (or any other kind) does not, in and of itself, lead to undefined behavior. As all the noncompliant code examples given here show, all instances of undefined behavior that result from ignoring errors (or any other conditions) are actually due to violations of other guidelines, and it's those violations, not the failure to handle the errors, that are the real causes of the undefined behavior. In addition to violating FIO04-C:
1.  **Noncompliant Code Example (`fgets()`)** violates [EXP34-C. Do not dereference null pointers](EXP34-C_%20Do%20not%20dereference%20null%20pointers)
2.  **Noncompliant Code Example (`fopen()`)** also violates EXP34-C
3.  **Noncompliant Code Example (`snprintf()`)** violates [ARR38-C. Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element](/confluence/pages/createpage.action?spaceKey=c&title=ARR38-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element) and [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap)
4.  **Noncompliant Code Example (`snprintf()`)** #2 violates [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow) and [EXP34-C. Do not dereference null pointers](EXP34-C_%20Do%20not%20dereference%20null%20pointers)
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 18, 2010 16:42
\| \|
Off the top of my head, these cases seem underspecified:
\(1\) Wrapper functions (imagine an "xfopen", which calls fopen to do all the work). ;Lots of programs use this idiom to ensure a single point where they can do logging, set breakpoints, etc.  If we want this to be a simple intraprocedural rule, then all wrappers are either compliant, or all non-compliant without regard for whether the caller of the wrapper does the right thing or not.
\(2\) The rule doesn't say much about whether the check of the return value is "right".  For example, what if the program says "snprintf(...) != -2"?
\(3\) What if there is a "check" function that validates the return value?
if(!check(fopen(...))) /\* handle error \*/
What if they get the check function wrong, or use the wrong check function?
These are just a few of the cases that need much more precise specification for this rule to truly separate compliant and non-compliant code unambiguously.
![](images/icons/contenttypes/comment_16.png) Posted by andy@coverity.com at Feb 18, 2010 00:04
\| \|
The way we have handled problems like these in the past is we see if **any** checking is performed. For instance, is the return value of fopen() ever checked? (that is is it ever compared to NULL?). If so, good. If it is used in another I/O function, bad (could be NULL). It is fairly easy for a developer to 'fool' us into thinking the value is checked when it isn't, such as passing the result of fopen() directly into a check() function. (which may or may not check the value). We decided that trying to prevent devs from fooling us was too hard, and so if a dev did something to check the value (such as passing it to a function), we allowed it.
Without inter-functional SA you can code things to fool any SA tool. With inter-functional SA you can achieve soundness & consistency (just go inside that check() function to see what gets done with your fopen() result).
But my main point was that if it looks like the developer tried to check for errors we did not flag it as a violation (that is we did not validate that the check was correct.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 18, 2010 10:32
\| \|
Following up on my own comment [Re: FIO33-C. Detect and handle input output errors resulting in undefined behavior](https://www.securecoding.cert.org/confluence/display/seccode/FIO33-C.+Detect+and+handle+input+output+errors+resulting+in+undefined+behavior?focusedCommentId=40730762#comment-40730762), I would like to merge this rule with [FIO04-C. Detect and handle input and output errors](/confluence/pages/createpage.action?spaceKey=seccode&title=FIO04-C.+Detect+and+handle+input+and+output+errors). I think the latter deserves to be a rule and it should specify as an exception those (rare) cases where the error handling policy permits certain types of errors to be ignored. Such cases must never lead to undefined or unspecified behavior. Whether such a strategy is appropriate depends on the nature of the program and its safety and security requirements (this is touched on in [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy)).
If there are no objections I will proceed with this change.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at May 02, 2010 18:04
\|
