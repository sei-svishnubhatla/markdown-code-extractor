Understanding the difference between text mode and binary mode is important when using functions that operate on file streams. (See [FIO14-C. Understand the difference between text mode and binary mode with file streams](FIO14-C_%20Understand%20the%20difference%20between%20text%20mode%20and%20binary%20mode%20with%20file%20streams) for more information.)
Subclause 7.21.9.2 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] specifies the following behavior for `fseek()` when opening a binary file in binary mode:
> A binary stream need not meaningfully support fseek calls with a `whence` value of `SEEK_END`.

In addition, footnote 268 of subclause 7.21.3 says:
> Setting the file position indicator to end-of-file, as with `fseek(file, 0, SEEK_END)`, has undefined behavior for a binary stream (because of possible trailing null characters) or for any stream with state-dependent encoding that does not assuredly end in the initial shift state.

Seeking to the end of a binary stream in binary mode with `fseek()` is not meaningfully supported and is not a recommended method for computing the size of a file.
Subclause 7.21.9.4 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] specifies the following behavior for `ftell()` when opening a text file in text mode:
> For a text stream, its file position indicator contains unspecified information, usable by the `fseek` function for returning the file position indicator for the stream to its position at the time of the `ftell` call.

Consequently, the return value of `ftell()` for streams opened in text mode should never be used for offset calculations other than in calls to `fseek()`.
POSIX \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] provides several guarantees that the problems described in the C Standard do not occur on POSIX systems.
First, the `fopen` page says:
> The character '`b`' shall have no effect, but is allowed for ISO C standard conformance.

This guarantees that binary files are treated the same as text files in POSIX.
Second, the `fwrite` page says:
> For each object, *size* calls shall be made to the *fputc()* function, taking the values (in order) from an array of **unsigned char** exactly overlaying the object. The file-position indicator for the stream (if defined) shall be advanced by the number of bytes successfully written.

This means that the file position indicator, and consequently the file size, is directly based on the number of bytes actually written to a file.
## Noncompliant Code Example (Binary File)
This code example attempts to open a binary file in binary mode and use `fseek()` and `ftell()` to obtain the file size. This code is noncompliant on systems that do not provide the same guarantees as POSIX. On these systems, setting the file position indicator to the end of the file using `fseek()` is not guaranteed to work for a binary stream, and consequently, the amount of memory allocated may be incorrect, leading to a potential [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
``` c
FILE *fp;
long file_size;
char *buffer;
fp = fopen("foo.bin", "rb");
if (fp == NULL) {
  /* Handle error */
}
if (fseek(fp, 0 , SEEK_END) != 0) {
  /* Handle error */
}
file_size = ftell(fp);
if (file_size == -1) {
  /* Handle error */
}
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
## Compliant Solution (POSIX `ftello()`)
If the code needs to handle large files, it is preferable to use `fseeko()` and `ftello()` because, for some implementations, they can handle larger file offsets than `fseek()` and `ftell()` can handle. If they are used, the `file_size` variable should have type `off_t` to avoid the possibility of overflow when assigning the return value of `ftello()` to it. This solution works only with regular files.
``` c
FILE* fp;
int fd;
off_t file_size;
char *buffer;
struct stat st;
fd = open("foo.bin", O_RDONLY);
if (fd == -1) {
  /* Handle error */
}
fp = fdopen(fd, "r");
if (fp == NULL) {
  /* Handle error */
}
/* Ensure that the file is a regular file */
if ((fstat(fd, &st) != 0) || (!S_ISREG(st.st_mode))) {
  /* Handle error */
}
if (fseeko(fp, 0 , SEEK_END) != 0) {
  /* Handle error */
}
file_size = ftello(fp);
if (file_size == -1) {
  /* Handle error */
}
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
## Compliant Solution (POSIX `fstat()`)
This compliant solution uses the size provided by the POSIX `fstat()` function, rather than by `fseek()` and `ftell()`, to obtain the size of the binary file. This solution works only with regular files.
``` c
off_t file_size;
char *buffer;
struct stat stbuf;
int fd;
fd = open("foo.bin", O_RDONLY);
if (fd == -1) {
  /* Handle error */
}
if ((fstat(fd, &stbuf) != 0) || (!S_ISREG(stbuf.st_mode))) {
  /* Handle error */
}
file_size = stbuf.st_size;
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
## Compliant Solution (Windows)
This compliant solution uses the Windows `_filelength()` function to determine the size of the file on a 32-bit operating system. For a 64-bit operating system, consider using `_filelengthi64` instead.
``` c
int fd;
long file_size;
char *buffer;
_sopen_s(&fd, "foo.bin", _O_RDONLY, _SH_DENYRW, _S_IREAD);
if (fd == -1) {
  /* Handle error */
}
file_size = _filelength(fd);
if (file_size == -1) {
  /* Handle error */
}
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
## Compliant Solution (Windows)
This compliant solution uses the Windows `GetFileSizeEx()` function to determine the size of the file on a 32- or 64-bit operating system:
``` c
HANDLE file;
LARGE_INTEGER file_size;
char *buffer;
file = CreateFile(TEXT("foo.bin"), GENERIC_READ, 0, NULL, 
                   OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
if (INVALID_FILE_HANDLE == file) {
  /* Handle error */
}
if (!GetFileSizeEx(file, &file_size)) {
  /* Handle error */
}
/* 
 * Note: 32-bit portability issue with LARGE_INTEGER
 * truncating to a size_t.
 */
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
## Noncompliant Code Example (Text File)
This noncompliant code example attempts to open a text file in text mode and use `fseek()` and `ftell()` to obtain the file size:
``` c
FILE *fp;
long file_size;
char *buffer;
fp = fopen("foo.txt", "r");
if (fp == NULL) {
  /* Handle error */
}
if (fseek(fp, 0 , SEEK_END) != 0) {
  /* Handle error */
}
file_size = ftell(fp);
if (file_size == -1) {
  /* Handle error */
}
buffer = (char*)malloc(file_size);
if (buffer == NULL) {
  /* Handle error */
}
/* ... */ 
```
However, the file position indicator returned by `ftell()` with a file opened in text mode is useful only in calls to `fseek()`. As such, the value of `file_size` may not necessarily be a meaningful measure of the number of characters in the file, and consequently, the amount of memory allocated may be incorrect, leading to a potential [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
The Visual Studio documentation for `ftell()` \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\] states:
> The value returned by `ftell` may not reflect the physical byte offset for streams opened in text mode, because text mode causes carriage return-linefeed translation. Use `ftell` with `fseek` to return to file locations correctly.

Again, this indicates that the return value of `ftell()` for streams opened in text mode is useful only in calls to `fseek()` and should not be used for any other purpose.
## Compliant Solution (Windows)
The compliant solution used for binary files on Windows can also be used for text files.
## Compliant Solution (POSIX)
Because binary files are treated the same as text files in POSIX, either compliant solution can be used for determining the size of a binary file under POSIX to determine the size of a text file as well.
## Risk Assessment
Understanding the difference between text mode and binary mode with file streams is critical when working with functions that operate on them. Setting the file position indicator to end-of-file with `fseek()` has [undefined behavior](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-undefinedbehavior) for a binary stream. In addition, the return value of `ftell()` for streams opened in text mode is useful only in calls to `fseek()`, not for determining file sizes or for any other use. As such, `fstat()` or other platform-equivalent functions should be used to determine the size of a file.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO19-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | XSH, System Interfaces, fopenXSH, System Interfaces, fwrite |
| [ISO/IEC 9899:2011] | Section 7.21.3, "Files"Section 7.21.9.2, "The fseek Function"
Section 7.21.9.4, "The ftell Function" |
| [MSDN] | "ftell" |

------------------------------------------------------------------------
[](../c/FIO18-C_%20Never%20expect%20fwrite__%20to%20terminate%20the%20writing%20process%20at%20a%20null%20character) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](../c/FIO20-C_%20Avoid%20unintentional%20truncation%20when%20using%20fgets__%20or%20fgetws__)
## Comments:

|  |
| ----|
| I think it will be impossible to obtain the size of the file that does not "meaningfully support fseek calls with a whence value of SEEK_END" using fstat() too.
                                        Posted by i.i. at Jul 20, 2011 07:20
                                     |
| Perhaps. The POSIX standard mentions nothing about fstat() ever failing to provide a valid file size (although fstat() can return -1 if it has a general failure, such as if it is given an invalid file descriptor).
Not that this guarantees anything...POSIX and C99 aren't always consistent wrt details like this. Do you have any more evidence of fstat() returning an invalid size (while still indicating success)?
                                        Posted by svoboda at Jul 20, 2011 08:16
                                     |
| No. I only thought that the only case where an;fseek call with SEEK_END is not supported, is the case of an infinite file. And for an infinite file fstat() will not work.
                                        Posted by i.i. at Jul 20, 2011 09:12
                                     |
| Well, I'm not sure what systems, if any, support an 'infinite file'. But a file whose size is bigger than can be represented by fstat would also be problematic.  I found this in the POSIX standard, under the fstatat()/lstat()/stat() page:
These functions shall fail if:
...
[EOVERFLOW]
The file size in bytes or the number of blocks allocated to the file or the file serial number cannot be represented correctly in the structure pointed to by buf.
Which suggests to me that if your file size can't be represneted by the int type used for file sizes, these functions will fail. Conceivably so would fstat().
                                        Posted by svoboda at Jul 20, 2011 09:19
                                     |
| I believe ;"Windows XP Professional SP4" is a typo for SP3. Just revised.
                                        Posted by yozo at Oct 22, 2012 02:16
                                     |
| What if I am trying to tell the size of a device? Clearly in this case using stat is of no help. This is doubly important because AFAICT a device file will never be in text mode.
                                        Posted by skibrianski at Jan 01, 2013 19:57
                                     |
| Another problem with the compliant solutions is that the value of;stbuf.st_size can be greater than LONG_MAX, in which case the assignment to file_size will overflow.  This could be fixed for POSIX by changing the variable file_size to have type off_t instead of long, but I don't know if that's appropriate for Windows.
                                        Posted by geoffclare at Jan 03, 2013 05:52
                                     |
| This link discusses this rule, with some background info:http://stackoverflow.com/questions/5957845/using-fseek-and-ftell-to-determine-the-size-of-a-file-has-a-vulnerability;
                                        Posted by svoboda at Jan 03, 2013 09:01
                                     |
| I've modified the rule to sanction using fseek/ftell on POSIX, because the problems outlined in C are mitigated on POSIX.There is anecdotal evidence that fseek/ftell correctly give the size of some device files, but I'm hesitant to sanction that for all device files...I'm not sure that size is even defined for some device files.Both fssek/ftell and fstat will fail to provide the correct size of any file whose size is larger tha LONG_MAX. POSIX provides the fseeko() and ftello() functions which use type off_t instead of long. Also ftell() and ftello() will set errno to EOVERFLOW if the file is too big to be represented by a long or off_t, respectively. In contrast, fstat() provides no such detection for large files.
                                        Posted by svoboda at Jan 03, 2013 10:47
                                     |
| You are mistaken about fstat().; POSIX requires it to fail with EOVERFLOW if the file size in bytes will not fit in the (type off_t) st_size structure member.  Note that off_t can be wider than long, hence my earlier comment about the potential for overflow when the value is assigned to file_size.
                                        Posted by geoffclare at Jan 03, 2013 11:43
                                     |
| One minor grammar nit: ;In many places, we say "...something, and consequently..." Anywhere you see that, replace the comma with a semicolon and also delete the and. It'll read better.  Trust me.Also, in the NCE for Binary Files, Robert wrote:"This code is noncompliant on systems that do not provide the same guarantees as POSIX. On these systems, setting the file position indicator to the end of the file using fseek() is not guaranteed to work for a binary stream, and consequently, the amount of memory allocated may be incorrect, leading to a potential vulnerability."I suggest rewording this as:"This code is noncompliant on systems that fail to provide the same guarantees as POSIX. On these systems, setting the file position indicator to the end of the file using fseek() may produce incorrect results for a binary stream; consequently, the amount of memory allocated may be incorrect, leading to a potential vulnerability."Both issues in this comment because Confluence says that robert is still editing the page. 
                                        Posted by dfsutherland at Jan 03, 2013 12:05
                                     |
| Sigh, you're right. I assumed fstat (& stat & lstat) wouldn't signal an EOVERFLOW error b/c you can use them for many reasons that have nothing to do with the file's size. Silly me.
                                        Posted by svoboda at Jan 03, 2013 14:13
                                     |
| I'm done fooling around with this for now (I think).; I think my solution to all these problems appears to be "don't use streams" and the problem goes away.  I felt like the solutions that were trying to use streams seemed forced.
                                        Posted by rcs at Jan 04, 2013 10:49
                                     |
| It certainly seems like this should be a rule and not a recommendation.
                                        Posted by rcs at Jan 04, 2013 10:52
                                     |
| No, as written this is still a recommendation, because violating it often does not yield a vul. A suitable rule would be "don't rely on a file size to know when to stop filling a buffer", or some such. That's the real problem.We also seem to have abdicated the issue of non-regular files. It seems people use fseek/ftell to determine the size of devices. Which seems to work sometimes (fstat doesn't define the size value for devices).Both POSIX compliant solutions fail on cases where the file (or device) size cannot be represented in an off_t. I don't think POSIX imposes a limit on file sizes.I do wonder if Windows' _filelength() will return a size that can be allocated to a buffer for reading the file data (which, as noted above, may not be the number of bytes stored in the file).
                                        Posted by svoboda at Jan 04, 2013 11:33
                                     |
| It can be a rule without directly causing a vulnerability.; It only has to be a defect or "security flaw".  Incorrectly sizing an object is definitely a security flaw.I think it is OK to scope the rule to regular files, as I believe this is the issue we were really trying to address.  I'm not sure why anyone would size a device file.  I'm guessing they aren't going to read it into memory.Failing in cases of very large files is OK, provided it is reported as an error.I'll test the Windows program to see if it can read in an entire file..... 
                                        Posted by rcs at Jan 04, 2013 11:51
                                     |
| I agree with your points, except this:It can be a rule without directly causing a vulnerability. It only has to be a defect or "security flaw". Incorrectly sizing an object is definitely a security flaw.OK, but what if you are just using fseek/ftell to size the file so you can print out the size? Or you just want to compute how much freek disk space you've got? Perhaps the rule should be "Don't rely on a file's size to allocate memory" (with a big exception for POSIX)
                                        Posted by svoboda at Jan 04, 2013 13:44
                                     |
| If the size is incorrect / unreliable, then this is a software defect, and because this defect can have security implications, it should be viewed as a diagnosable security flaw.A similar example is INT30-C. Ensure that unsigned integer operations do not wrap.If we were to turn this into a rule for TS 17961, we probably wouldn't require this problem to be diagnosed unless the incorrect size value was used in a restricted sink.; For the CERT C Secure Coding Standard, I think it is OK to have a rule against creating incorrect values to try to catch these problems at the source.
                                        Posted by rcs at Jan 07, 2013 10:04
                                     |
| Your "Compliant Solutions" for POSIX will all crash the very moment you read the (large) file into your malloc()'ed buffer if off_t is 64-bit while the CPU is 32-bit...Before the malloc(), you need to add:if(file_size > SIZE_MAX){; /* handle error: file too big for malloc() on this machine */}Of course, that will throw a compiler warning about comparing signed vs. unsigned.(the POSIX guys didn't care to invent an unsigned filesize type for st_size etc. (one of many flaws in the file function designs)So you need to write:if((unsigned off_t)file_size > SIZE_MAX)...but, while that compiles fine with GCC, clang will report an error because it doesn't recognize that off_t eventually resolves to an integer type.So you need to write:if((uint64_t)file_size > SIZE_MAX)...and eventually, the moment they come up with a 128-bit off_t for some kind of "Extra Large File Support", we're all doomed no matter what. 
                                        Posted by bloody at Sep 12, 2015 07:36
                                     |
| The same issue in the 2nd Windows compliant solution is addressed via a comment, "Note: 32-bit portability issue with LARGE_INTEGER truncating to a size_t."; So, for consistency, either the POSIX compliant solutions should have a similar comment added, or Oliver's suggestion of adding a check against SIZE_MAX should be applied to the POSIX and Windows solutions.To avoid the signed/unsigned comparison warning without making any assumption about how big off_t is, the POSIX code can use:if ((uintmax_t)file_size > SIZE_MAX)

![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Sep 14, 2015 05:27
\|
