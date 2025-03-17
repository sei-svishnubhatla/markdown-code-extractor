The C Standard, subclause 7.21.8.2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], defines the `fwrite()` function as follows:
> Synopsis 
>
> `size_t fwrite(const void *restrict ptr, size_t size, size_t nmemb, FILE *restrict stream);`
>
> Description
>
> The `fwrite()` function writes, from the array pointed to by `ptr`, up to `nmemb` elements whose size is specified by `size`, to the stream pointed to by `stream`. For each object, `size` calls are made to the `fputc()` function, taking the values (in order) from an array of `unsigned char` exactly overlaying the object. The file position indicator for the stream (if defined) is advanced by the number of bytes successfully written. If an error occurs, the resulting value of the file position indicator for the stream is indeterminate.

The definition does not state that the `fwrite()` function will stop copying characters into the file if a null character is encountered. Therefore, when writing a null-terminated byte string to a file using the `fwrite()` function, always use the length of the string plus 1 (to account for the null character) as the `nmemb` parameter.
## Noncompliant Code Example
In this noncompliant code example, the size of the buffer is stored in `size1`, but `size2` number of characters are written to the file. If `size2` is greater than `size1`, `write()` will not stop copying characters at the null character.
``` c
#include <stdio.h>
#include <stdlib.h>
char *buffer = NULL;
size_t size1;
size_t size2;
FILE *filedes;
/* Assume size1 and size2 are appropriately initialized */
filedes = fopen("out.txt", "w+");
if (filedes == NULL) {
  /* Handle error */
}
buffer = (char *)calloc( 1, size1);
if (buffer == NULL) {
  /* Handle error */
}
fwrite(buffer, 1, size2, filedes);
free(buffer);
buffer = NULL;
fclose(filedes);
```
## Compliant Solution
This compliant solution ensures that the correct number of characters are written to the file:
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char *buffer = NULL;
size_t size1;
size_t size2;
FILE *filedes;
/* Assume size1 is appropriately initialized */
filedes = fopen("out.txt", "w+");
if (filedes == NULL){
  /* Handle error */
}
buffer = (char *)calloc( 1, size1);
if (buffer == NULL) {
  /* Handle error */
}
/*
 * Accept characters in to the buffer.
 * Check for buffer overflow.
 */
size2 = strlen(buffer) + 1;
fwrite(buffer, 1, size2, filedes);
free(buffer);
buffer = NULL;
fclose(filedes);
```
## Risk Assessment
Failure to follow the recommendation could result in a non-null-terminated string being written to a file, which will create problems when the program tries to read it back as a null-terminated byte string.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO18-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 44 S | Enhanced enforcement |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO18-CPP. Never expect write() to terminate the writing process at a null character |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.21.8.2, "The fwrite Function" |
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, fwrite |

------------------------------------------------------------------------
[](../c/FIO17-C_%20Do%20not%20rely%20on%20an%20ending%20null%20character%20when%20using%20fread__) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO19-C_%20Do%20not%20use%20fseek__%20and%20ftell__%20to%20compute%20the%20size%20of%20a%20regular%20file)
## Comments:

|  |
| ----|
| Janice, I presume this is a C version of FIO18-CPP. Never expect write() to terminate the writing process at a null character. That's perfectly valid, but you probably want this to be a recommendation, not a rule, since it is a rec in C++. 
                                        Posted by svoboda at Mar 26, 2009 11:32
                                     |
| If this is only about the write() function, and this function is only defined by POSIX, this recommendation needs to be in the POSIX section.
                                        Posted by rcs at Mar 27, 2009 01:11
                                     |
| True. Additionally, the reference is not POSIX, but rather the GNU C library reference doc. Which itself is a valid reference, it just isn't POSIX.
Would this rule apply equally well to the fwrite() function, which is defined in C99?
                                        Posted by svoboda at Mar 27, 2009 15:15
                                     |
| David, I'm not sure I fully understood what you meant. So should I move it to the POSIX section?
                                        Posted by jdsa at Mar 30, 2009 23:10
                                     |
| Janice,  you have two choices:
    Make the rule about the fwrite() function, which is defined in the C standard
    Make the rule about the write() function, which is not in the C standard, but is in the POSIX standard. If you do this, the rule should be moved to the POSIX section.
I recommend doing the former choice.
FYI the C++ standard does define a write() method for output streams, which is why the C++ rule is about write(), but the C rule shouldn't be.
                                        Posted by svoboda at Mar 31, 2009 14:40
                                     |
| I agree this would be better for the fwrite() function from the C standard.  Make sure you write a test case and confirm that this problem exists on at least one conforming implementation.  The quote obviously needs to be changed.
Also, instead of:
Therefore, when writing a C string in to a file using the write() function, always use the size of the buffer string as the size parameter." 
shouldn't this say:
Therefore, when writing a C string to a file using the fwrite() function, always use the length of the string plus one byte for the null termination character as the size parameter." 
Also, try to write this rule so it is enforceable.  I think the problem you are really trying to solve here is "not writing uninitialized or incorrectly initialized data using fwrite()".
Anyway, think about it some more.
                                        Posted by rcs at Mar 31, 2009 17:06
                                     |
| The rule is nearly complete. Needs the following:
    Please follow my style guidelines (add a link from FIO page, need risk assessment section)
    The open group reference is good, but you will also want the C99 reference for fwrite(), since the C99 standard is what we are working on here.
                                        Posted by svoboda at Apr 01, 2009 14:52
                                     |
| I'm not sure what link to provide as a reference to the C99 standard.
                                        Posted by jdsa at Apr 01, 2009 16:40
                                     |
| If you study some other rules you'll see how they reference C99. I'm guessing youll want to reference the definition of the fwrite() function.
                                        Posted by svoboda at Apr 01, 2009 20:25
                                     |
| I can't find any online access to the standard
                                        Posted by jdsa at Apr 03, 2009 21:36
                                     |
| I'd say this rule is now complete.
                                        Posted by svoboda at Apr 03, 2009 22:16
                                     |
| The calloc() and fwrite() calls are inconsistent, in that one uses sizeof(char) where the other uses 1.  Either they should both use sizeof(char) or they should both use 1 (preferably the latter).
                                        Posted by geoffclare at Apr 06, 2009 04:21
                                     |
| Thanks, I've made this change.
                                        Posted by svoboda at Apr 06, 2009 11:30
                                     |

