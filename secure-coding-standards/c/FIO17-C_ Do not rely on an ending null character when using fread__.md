The `fread()` function, as defined in the C Standard, subclause 7.21.8.1 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], does not explicitly null-terminate the read character sequence.
> Synopsis  
> `size_t fread(void * restrict ptr, size_t size, size_t nmemb, FILE * restrict stream)`
>
> Description  
> The `fread` function reads, into the array pointed to by `ptr`, up to `nmemb` elements  
> whose size is specified by `size`, from the stream pointed to by `stream`.

Although the content of a file has a properly null-terminated character sequence, if `nmemb` is less than the total length of the characters, the `fread()` function will not read after `nmemb` characters. `fread()` will not append a null character to the end of the string being read to.
## Noncompliant Code Example
Suppose we have a null-terminated character sequence in a file, and we need to extract a null-terminated byte string:
``` c
#include <stdio.h>
#include <stdlib.h>
int main (void) {
    FILE *fp;
    size_t size;
    long length;
    char *buffer;
    fp = fopen("file.txt", "rb");
    if (fp == NULL) {
      /* Handle file open error */
    }
    /* Obtain file size */
    if (fseek(fp, 0, SEEK_END) != 0) {
      /* Handle repositioning error */
    }
    length = ftell(fp);
    if (fseek(fp, 0L, SEEK_SET) != 0) {
      /* Handle repositioning error */
    }
    /* Allocate memory to contain whole file */
    buffer = (char*) malloc(length);
    if (buffer == NULL) {
      /* Handle memory allocation error */
    }
    /* size assigned here in some other code */
    if (fread(buffer, 1, size, fp) < size) {
      /* Handle file read error */
    }
    fclose(fp);
    return 0;
}
```
When `size` is less than the total length of the file (`file.txt`), `buffer` is not properly null-terminated.
## Compliant Solution
To correct this example, the size of `buffer` must be compared with the total length of the file to identify the erroneous case where `size` differs from `length`. At this point, it is up to the programmer to handle this case.
``` c
#include <stdio.h>
#include <stdlib.h>
int main (void) {
    FILE *fp;
    size_t size;
    long length;
    char *buffer;
    fp = fopen("file.txt", "rb");
    if (fp == NULL) {
      /* Handle file open error */
    }
    /* Obtain file size */
    if (fseek(fp, 0, SEEK_END) != 0) {
      /* Handle repositioning error */
    }
    length = ftell(fp);
    if (fseek(fp, 0L, SEEK_SET) != 0) {
      /* Handle repositioning error */
    }
    /* Allocate memory to contain whole file */
    buffer = (char*) malloc(length);
    if (buffer == NULL) {
      /* Handle memory allocation error */
    }
    /* ... Assign size here ... */
    if (length != size) {
      /* Handle case when size isn't the length of file */
    }
    /* ... Other code ... */
    if (fread(buffer, 1, size, fp) < size) {
      /* Handle file read error */
    }
    fclose(fp);
    return 0;
}
```
## Risk Assessment
When reading an input stream, the read character sequence is not explicitly null-terminated by the `fread()` function. Operations on the read-to buffer could result in overruns, causing [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO17-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this guideline on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO17-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO20-CPP. Do not rely on an ending null character when using read() |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.21.8.1, "The fread Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152134) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO18-C_%20Never%20expect%20fwrite__%20to%20terminate%20the%20writing%20process%20at%20a%20null%20character)
## Comments:

|  |
| ----|
| Hi, Glenn. This looks like a legit rule. I presume you mean to rewrite the C++ rule to work with the C language, so I'll reserve comments until you finish it.
I'll add one comment that in C 'read()' is a non-standard function (it is defined by POSIX but not C99), so you'll probably want to focus on the 'fread()' function which C99. (We have a separate section for POSIX-related rules.)
                                        Posted by svoboda at Mar 29, 2009 10:56
                                     |
| The rule is valid; here are my comments:
    Take out the 'work in progress' if you want feedback...otherwise I'll assume you are still working on the rule & feedback is premature.
    Why is the severity 'medium'? Can this cause info disclosure?
    Good quote from the C standard...but it could be trimmed down, since we only need to emphasize that it doesn't null-terminate its output.
                                        Posted by svoboda at Mar 30, 2009 15:46
                                     |
| Your risk analysis statement just restates the behavior of the function, it doesn't describe a risk.
Don't say c-string.  Say "null terminated byte string".
Wrong format for references.  Just lose the [1] and use [ISO/IEC 9899:1999]
Try to emulate the style of writing in the other, completed rules.  For example, get rid of the "suppose" and "here we" stuff.
Your initial statement is weaker than your title.  Go with as strong as a statement as you can correctly make.
                                        Posted by rcs at Mar 31, 2009 17:38
                                     |
| In the compliant solution, shouldn't the (length != size) check be done before the fread() rather than after it?
                                        Posted by geoffclare at Apr 07, 2009 10:29
                                     |
| I suppose so; as that's more efficient (if length != size). Since size is computed separately by the program, I'm not sure that it makes a lot of difference when the comparison takes place, however. What do you think, Glenn?
                                        Posted by svoboda at Apr 07, 2009 10:44
                                     |
| My thinking was that with the current code, the part that assigns size would need to include a check that (size <= length) to ensure fread() will not overflow the buffer.  It doesn't make sense to do that check before the fread() and then a separate check for (length != size) after the fread(), rather than just a single (length != size) check before the fread().
                                        Posted by geoffclare at Apr 07, 2009 12:05
                                     |
| I made the change. I agree; the size check should be made ASAP, as a good design principle.
                                        Posted by svoboda at Apr 07, 2009 12:22
                                     |
| I believe my original thought was that the buffer allocated would be the length of the entire file. Thus there'd be no possibility of overflowing the buffer and you wouldn't need to check if size <= length.
                                        Posted by gstroz at Apr 07, 2009 13:52
                                     |
| The buffer size is the length that the file had at the time of the fseek(fp, 0, SEEK_END).  The file could grow larger by the time the fread() call is made.
                                        Posted by geoffclare at Apr 08, 2009 04:17
                                     |
| Perhaps I missed it; where is the assignment to the "size" variable in either example?
                                        Posted by xuinkrbin. at Jan 09, 2013 15:41
                                     |
| In both code samples size is supposed to be initialized in the comments just above the fread() call.There is a bigger problem in that both code samples violate FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file. This technique is only guaranteed to work as expected for POSIX...both code samples will have surprising effects on Windows or other non-POSIX platforms.There can also be overflow issues if this code runs on a platform where sizeof(size_t) != sizeof(long).
                                        Posted by svoboda at Jan 09, 2013 16:25
                                     |

