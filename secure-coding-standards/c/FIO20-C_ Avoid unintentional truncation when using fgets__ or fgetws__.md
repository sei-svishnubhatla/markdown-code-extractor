The `fgets()` and `fgetws()` functions are typically used to read a newline-terminated line of input from a stream. Both functions read at most one less than the number of narrow or wide characters specified by an argument `n` from a stream to a string. Truncation errors can occur if `n - 1` is less than the number of characters appearing in the input string prior to the new-line narrow or wide character (which is retained) or after end-of-file.  This can result in the accidental truncation of user input.
## Noncompliant Code Example
This noncompliant code example copies the input string into a buffer, and assumes it captured all of the user's input.
``` c
#include <stdbool.h>
#include <stdio.h>
bool get_data(char *buffer, int size) {
  if (fgets(buffer, size, stdin)) {
    return true;
  }
  return false;
}
void func(void) {
  char buf[8];
  if (get_data(buf, sizeof(buf))) {
    printf("The user input %s\n", buf);
  } else {
    printf("Error getting data from the user\n");
  }
}
```
However, if the last character in `buf` is not a newline and the stream is not at the end-of-file marker, the buffer was too small to contain all of the data from the user.  For example, because the buffer is only 8 characters in length, if the user input `"Hello World\n"`, the buffer would contain `"Hello W"` terminated by a null character.
## Compliant Solution (Fail on Truncation)
This compliant solution examines the end-of-file marker for the stream and the last character in the buffer to determine whether it is a newline or not.  If it is the end of file, or the last character is a newline, then the buffer contains all of the user's input.  However, if the last character is not at the end-of-file and not a newline then the user's input has been truncated.
``` c
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
bool get_data(char *buffer, int size) {
  if (fgets(buffer, size, stdin)) {
    size_t len = strlen(buffer);
    return feof(stdin) || (len != 0 && buffer[len-1] == '\n');
  }
  return false;
}
void func(void) {
  char buf[8];
  if (get_data(buf, sizeof(buf))) {
    printf("The user input %s\n", buf);
  } else {
    printf("Error getting data from the user\n");
  }
}
```
## Compliant Solution (Expanding Buffer)
This compliant solution solves the problem by expanding the buffer to read the entire contents from `stdin` instead of failing if the caller did not allocate enough space.  If the allocation fails, it will return `NULL`, but otherwise, it returns a buffer of the received data, which the caller must free.
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char *get_filled_buffer(void) {
  char temp[32];
  char *ret = NULL;
  size_t full_length = 0;
  while (fgets(temp, sizeof(temp), stdin)) {
    size_t len = strlen(temp);
    if (SIZE_MAX - len - 1 < full_length) {
      break;
    }
    char *r_temp = realloc(ret, full_length + len + 1);
    if (r_temp == NULL) {
      break;
    }
    ret = r_temp;
    strcpy(ret + full_length, temp); /* concatenate */
    full_length += len;
    if (feof(stdin) || temp[len-1] == '\n') {
      return ret;
    }
  }
  free(ret);
  return NULL;
}
```
## Compliant Solution (POSIX `getline()`)
The `getline()` function was originally a GNU extension, but is now standard in POSIX.1-2008. It also fills a string with characters from an input stream. In this case, the program passes it a NULL pointer for a string, indicating that `getline()` should allocate sufficient space for the string and the caller frees it later.
``` c
#include <stdio.h>
void func(void) {
  char* buf = NULL;
  size_t dummy = 0;
  if (getline(&buf, &dummy, stdin) == -1) {
    /* handle error */
  }
  printf("The user input %s\n", buf);
  free(buf);
}
```
## Risk Assessment
Incorrectly assuming a newline character is read by `fgets()` or `fgetws()` can result in data truncation.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO20-C | Medium | Likely | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO20-C).
## Bibliography

|  |  |
| ----|----|
| [Lai 2006] | ; |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](../c/FIO19-C_%20Do%20not%20use%20fseek__%20and%20ftell__%20to%20compute%20the%20size%20of%20a%20regular%20file) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152425)
## Comments:

|  |
| ----|
| It shpuld be stated that an obvious alternative, to leave room in the buffer for one more character and when there was no newline transferred to tack a newline onto the end (then a terminator) is unsafe, because it quietly accepts an input that is not what was actually intended, with who knows what consequences.
                                        Posted by dagwyn at Apr 17, 2008 17:58
                                     |
| So stated.
                                        Posted by rcs at Apr 18, 2008 03:03
                                     |
| See FIO37-C for Rose enforceability
                                        Posted by svoboda at Jun 21, 2008 09:08
                                     |
| FIO37-C's example can be caught by ROSE, although the general problem is probably unenforceable. This rule itself is unenforceable since ROSE cannot determine the programmer's intent.
                                        Posted by svoboda at Jul 25, 2008 11:04
                                     |
| C99 7.19.7.2 sez:
The fgets function reads at most one less than the number of characters specified by n from the stream pointed to by stream into the array pointed to by s. No additional characters are read after a new-line character (which is retained) or after end-of-file. A null character is written immediately after the last character read into the array.
/emphasis mine/
Doesn't this indicate that if a string in a file ends with newline, the newline will always be read?
I presume the purpose of this rule is to handle cases where a fgets does not read until the newline, either because the file reaches EOF, or the maximum chars are read, or because some other I/O error occurs.
I guess the rule should resolve this question.
                                        Posted by svoboda at Nov 07, 2008 17:24
                                     |
| Since this is flagged as unenforceable, should it be moved to a recommendation instead of a rule?
                                        Posted by aballman at Sep 27, 2013 11:25
                                     |
| ;I don't think the CS will compile on MSVC because of where the following declaration appears:size_t len = strlen(buffer); 
                                        Posted by rcs at Sep 28, 2013 18:44
                                     |
| It does compile in /TC mode in Visual Studio 2012 once you remove the stdbool.h inclusion.; Perhaps not in earlier versions of the compiler though.
                                        Posted by aballman at Sep 29, 2013 10:09
                                     |
| ;That's good news, I guess.  We have avoided valid C99 declarations like this just to make sure this would compile on MSVC.  If this now works, I think it is reasonable to use this style of declaration.
                                        Posted by rcs at Sep 29, 2013 10:29
                                     |
| One note...my Ubuntu box using gcc 4.6.3 neither recognizes 'bool' or 'false'. Even with -std=c99 or -std=c1x.No other problems with this rule...er rec.
                                        Posted by svoboda at Sep 30, 2013 13:00
                                     |
| Can it find stdbool.h?; If so, something smells off – stdbool.h typedefs _Bool to bool, and defines true and false.
                                        Posted by aballman at Sep 30, 2013 13:18
                                     |
| The last "compliant solution" with the expanding buffer is still not safe if the input can contain nullbytes. E.g. like this:description=AAA\0AAAAAAAAAAAAAAsecret_token=1234This would be parsed like "description=AAAsecret_token=1234", I think.
                                        Posted by thejh at Mar 23, 2014 16:11
                                     |
| That's because fgets() leaves the caller with no way of knowing if the input has an internal null byte. Suppose your buffer has the following contents after a successful fgets() call:"ab\0cde\0"It is possible for fgets to have read two charcters "ab", or 6 characters "ab\0cde", and there is no standard way to distinguish between these two scenarios.
                                        Posted by svoboda at Mar 27, 2014 12:20
                                     |
| The expanding buffer example is broken. ;temp[len] can never be '\n', though temp[len-1] can be - providing that len > 0.temp[len] is the terminating \0, as len = strlen(temp).In any case, using the temp buffer and strcat is unnecessarily convoluted.  strlen() and strcat() are expensive, as they both
require finding the end of the string.  And copying the data is unnecessary.The usual portable solution looks like the following 32 lines of code. 

**Correct expandable buffer**
``` cpp
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
char *fgetline( FILE *stream ) {
    size_t bufsize = 0,
           xpnsize = 80,
           idx = 0;
    char *buf = NULL;
    int c;
    while( (c = getc(stream)) != EOF && c != '\n' ) {
        if( idx + 2 > bufsize ) { /* Space for char & terminal \0 */
            char *nbuf;
            bufsize += xpnsize;
            nbuf = (char *) realloc( buf, bufsize ); /* Create or expand */
            if( nbuf == NULL ) {
                perror( "realloc" ); /* free(buf); return NULL; */
                abort();
            }
            buf = nbuf;
        }
        buf[idx++] = c;
    }
    if( c == EOF && idx == 0 ) { /* EOF with no data on last line */
        free( buf );
        return NULL;
    }
    if( bufsize == 0 ) { /* Empty line.  N.B. idx guaranteed to be 0 */
        buf = (char *) malloc( 1 );
        if( buf == NULL ) {
            perror( "malloc" ); /* return NULL; */
            abort();
        }
    }
    buf[idx] = '\0';
    return buf;
}
/* Sample usage.  */
char *line;
while( (line = fgetline( stdin )) != NULL ) {
    printf( "echo: %s\n", line );
    free(line);
}
exit(0);
```
Notes:
-   Returning NULL on malloc() failure is an alternative, though people may well assume that NULL means EOF and lose data.    
    To do this: As shown in the comments, free the partial buffer at line 17 & return NULL.  Also return NULL at line 31.  
-   You might be tempted to return the partial line at line 17 - but that is a bad idea for the same reason that this recomendation exists: unintentional truncation of user input.  Better to report an error or die.
-   If you're worried about embedded NULs, simply if( c == '\0' ) continue; at line 12.
-   You could read into a dynamic buffer with fgets, but it's rarely worthwhile.  You still need to have strlen() look at each character  
    to see if it ends with \n, and getc() is usually cheap.  In fact, fgets() is often implemented in terms of getc(). As shown each character  
    in memory is touched exactly once.   
-   If you have some a-priori knowledge of the typical record length, the initial value of xpnsize on line 3 can be adjusted accordingly.  
    More involved tuning schemes are possible, though application-specific. Beware of thread-unsafe approaches. 
-   This function is simply called with a stream, returns a buffer and requires the caller to free the buffer. 
-   The \n is not returned.  This is intentional as most callers remove it.
-   If the line before EOF doesn't have a \n, it is returned.  In rare cases, this may be undesirable.
-   getline (3) is another solution if your RTL supports it.  POSIX 2008.  Returns the newline.
![](images/icons/contenttypes/comment_16.png) Posted by tlhackque at Mar 02, 2016 16:42
\| \|
Good catch. I tweaked the current fgets() example to use len-1 in the array index. Your code example is more efficient, but twice as many lines.
I also added a code example that uses getline().
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 03, 2016 13:34
\| \|
David,
;
Thanks for addressing my comment.
I don't see why there's a premium on length; I prefer not to publish inefficient code.  Modifying code for "Efficiency" is often a source of **bugs**... I expect many people use the 'compliant' code as their solution, so it ought to be reasonably efficient.  And not encourage optimization....
Your current solution is 17 LOC,  My version is 24 (if you adopt the equivalent 'return NULL' on error alternative.)  Both counting lines with a statement, not blank or closing }.
(1.4x the line count, not 2x if you're picky.)
Are 7 LOC worth the inefficiency of processing the input three times as often as necessary?  (`fgets() + strlen() + strcat()`) 
<u>Speaking of **bugs**:</u>
Your new code can still index `temp` by -1 if `strlen()` returns zero.  One way it can do that if the input contains a \0.
strcat() and the manipulation of `'end'` can an also be affected by \0 in the input.
`fgets()` doesn't deal gracefully with \0 in the input, but your new code exacerbates its issues.
You'll probably add a few LOC to deal with those boundary cases ![](images/icons/emoticons/smile.svg) If you don't switch to `getc(),` I predict that you'll pass over the input at least once more.
It should also be noted that a `NULL` return from` fgets()` or the aternatives doesn't only mean EOF.  It can mean an I/O error.  E.g. a buffer overrun on pasting from a terminal, or a disk or network failure. 
**Failure to check `errno` or` ferror()` on an error return from` fgets()` is also a source of truncation errors**.  I mentioned this in my first NOTE, but it may not have stood out.
Also, using `getline()` or either of the expanding buffer alternatives is **low** effort - why do you classify this as **medium**?  For the caller, it's actually more convenient.
This article says that a tool suite checks for compliance.  I'm not familiar with the tool, and it's not obvious how it can verify compliance, even with fairly extensive code analysis.  A check for missing newline can be a considerable distance from the `fgets()` in real code.  You run into the halting problem. 
In any case, the tool needs to be updated with the result of our discussion.
![](images/icons/contenttypes/comment_16.png) Posted by tlhackque at Mar 03, 2016 14:29
\| \|
I noticed a vulnerability in the expanding buffer solution: the reallocated buffer in the first iteration is uninitialized (**not** guaranteed to be a string of length 0), so running `strcat()` on it is undefined behavior and may cause a buffer overflow.
In addition, the initial calculation of the `full_size` variable involves subtracting two null pointers (`end` and `ret`), which seems to be undefined behavior in C, though defined in C++. I think it would be a better idea to keep `full_size` a persistent variable between loop iterations, since the `end` pointer is only being used to keep track of the buffer size in a rather roundabout way.
One way to fix both of these issues would be to use `strcpy()` rather than `strcat()`, making use of the fact that the previous length of the string is already known (also improving efficiency). One such solution follows (note that `full_size` has been renamed to `full_length` to indicate it is the string length and not the buffer size):
``` cpp
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char *get_filled_buffer(void) {
  char temp[32];
  char *ret = NULL;
; size_t full_length = 0;
  while (fgets(temp, sizeof(temp), stdin)) {
    size_t len = strlen(temp);
    char *r_temp = realloc(ret, full_length + len + 1);
    if (r_temp == NULL) {
      break;
    }
    ret = r_temp;
    strcpy(ret + full_length, temp); /* concatenate */
    full_length += len;
    if (feof(stdin) || temp[len-1] == '\n') {
      return ret;
    }
  }
  free(ret);
  return NULL;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by bfletcher at Nov 07, 2016 14:39
\| \|
Good catches. I adopted your compliant solution (and also added an integer overflow check).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 07, 2016 15:22
\|
