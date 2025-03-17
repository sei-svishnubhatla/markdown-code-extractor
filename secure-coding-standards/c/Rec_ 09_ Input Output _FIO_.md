-   Page:
    [FIO01-C. Be careful using functions that use file names for identification](/confluence/display/c/FIO01-C.+Be+careful+using+functions+that+use+file+names+for+identification)
-   Page:
    [FIO02-C. Canonicalize path names originating from tainted sources](/confluence/display/c/FIO02-C.+Canonicalize+path+names+originating+from+tainted+sources)
-   Page:
    [FIO03-C. Do not make assumptions about fopen() and file creation](/confluence/display/c/FIO03-C.+Do+not+make+assumptions+about+fopen%28%29+and+file+creation)
-   Page:
    [FIO05-C. Identify files using multiple file attributes](/confluence/display/c/FIO05-C.+Identify+files+using+multiple+file+attributes)
-   Page:
    [FIO06-C. Create files with appropriate access permissions](/confluence/display/c/FIO06-C.+Create+files+with+appropriate+access+permissions)
-   Page:
    [FIO08-C. Take care when calling remove() on an open file](/confluence/display/c/FIO08-C.+Take+care+when+calling+remove%28%29+on+an+open+file)
-   Page:
    [FIO09-C. Be careful with binary data when transferring data across systems](/confluence/display/c/FIO09-C.+Be+careful+with+binary+data+when+transferring+data+across+systems)
-   Page:
    [FIO10-C. Take care when using the rename() function](/confluence/display/c/FIO10-C.+Take+care+when+using+the+rename%28%29+function)
-   Page:
    [FIO11-C. Take care when specifying the mode parameter of fopen()](../c/FIO11-C_%20Take%20care%20when%20specifying%20the%20mode%20parameter%20of%20fopen__)
-   Page:
    [FIO13-C. Never push back anything other than one read character](/confluence/display/c/FIO13-C.+Never+push+back+anything+other+than+one+read+character)
-   Page:
    [FIO14-C. Understand the difference between text mode and binary mode with file streams](/confluence/display/c/FIO14-C.+Understand+the+difference+between+text+mode+and+binary+mode+with+file+streams)
-   Page:
    [FIO15-C. Ensure that file operations are performed in a secure directory](/confluence/display/c/FIO15-C.+Ensure+that+file+operations+are+performed+in+a+secure+directory)
-   Page:
    [FIO17-C. Do not rely on an ending null character when using fread()](../c/FIO17-C_%20Do%20not%20rely%20on%20an%20ending%20null%20character%20when%20using%20fread__)
-   Page:
    [FIO18-C. Never expect fwrite() to terminate the writing process at a null character](/confluence/display/c/FIO18-C.+Never+expect+fwrite%28%29+to+terminate+the+writing+process+at+a+null+character)
-   Page:
    [FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file](/confluence/display/c/FIO19-C.+Do+not+use+fseek%28%29+and+ftell%28%29+to+compute+the+size+of+a+regular+file)
-   Page:
    [FIO20-C. Avoid unintentional truncation when using fgets() or fgetws()](../c/FIO20-C_%20Avoid%20unintentional%20truncation%20when%20using%20fgets__%20or%20fgetws__)
-   Page:
    [FIO21-C. Do not create temporary files in shared directories](/confluence/display/c/FIO21-C.+Do+not+create+temporary+files+in+shared+directories)
-   Page:
    [FIO22-C. Close files before spawning processes](/confluence/display/c/FIO22-C.+Close+files+before+spawning+processes)
-   Page:
    [FIO23-C. Do not exit with unflushed data in stdout or stderr](/confluence/display/c/FIO23-C.+Do+not+exit+with+unflushed+data+in+stdout+or+stderr)
-   Page:
    [FIO24-C. Do not open a file that is already open](/confluence/display/c/FIO24-C.+Do+not+open+a+file+that+is+already+open)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [fio](https://confluence/label/seccode/fio) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO01-C | Medium | Likely | Medium | P12 | L1 |
| FIO02-C | Medium | Probable | Medium | P8 | L2 |
| FIO03-C | Medium | Probable | High | P4 | L3 |
| FIO05-C | Medium | Probable | Medium | P8 | L2 |
| FIO06-C | Medium | Probable | High | P4 | L3 |
| FIO08-C | Medium | Probable | High | P4 | L3 |
| FIO09-C | Medium | Probable | High | P4 | L3 |
| FIO10-C | Medium | Probable | Medium | P8 | L2 |
| FIO11-C | Medium | Probable | Medium | P8 | L2 |
| FIO13-C | Medium | Probable | High | P4 | L3 |
| FIO14-C | Low | Probable | High | P2 | L3 |
| FIO15-C | Medium | Probable | High | P4 | L3 |
| FIO17-C | Low | Likely | Medium | P6 | L2 |
| FIO18-C | Medium | Probable | Medium | P8 | L2 |
| FIO19-C | Low | Unlikely | Medium | P2 | L3 |
| FIO20-C | Medium | Likely | Medium | P12 | L1 |
| FIO21-C | Medium | Probable | Medium | P8 | L2 |
| FIO22-C | Medium | Unlikely | Medium | P4 | L3 |
| FIO23-C | Medium | Unlikely | Medium | P4 | L3 |
| FIO31-C | Medium | Probable | High | P4 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| Avoid having unreachable code |
| Copy of Rule Template |
| DRD00. Do not store sensitive information on external storage (SD card) unless encrypted first |
| DRD04-J. Do not log sensitive information |
| DRD11. Ensure that sensitive data is kept secure |
| DRD12.  Do not trust data that is world writable |
| DRD22. Do not cache sensitive information |
| DRD23. Do not use world readable or writeable to share files between apps |
| DRD25. Use constant-time encryption |
| DRD27-J. For OAuth, use an explicit intent method to deliver access tokens |
| FIO00-J. Do not operate on files in shared directories |
| FIO00-PL. Do not use bareword file handles |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO01-C. Be careful using functions that use file names for identification |
| FIO01-J. Create files with appropriate access permissions |
| FIO01-PL. Do not operate on files that can be modified by untrusted users |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO02-C. Canonicalize path names originating from tainted sources |
| FIO02-J. Detect and handle file-related errors |
| FIO03-C. Do not make assumptions about fopen() and file creation |
| FIO03-C. Do not make assumptions about fopen() and file creation |
| FIO03-C. Do not make assumptions about fopen() and file creation |
| FIO03-J. Remove temporary files before termination |
| FIO04-J. Release resources when they are no longer needed |
| FIO05-C. Identify files using multiple file attributes |
| FIO05-C. Identify files using multiple file attributes |
| FIO05-C. Identify files using multiple file attributes |
| FIO05-J. Do not expose buffers or their backing arrays methods to untrusted code |
| FIO06-C. Create files with appropriate access permissions |
| FIO06-C. Create files with appropriate access permissions |
| FIO06-C. Create files with appropriate access permissions |
| FIO06-J. Do not create multiple buffered wrappers on a single byte or character stream |
| FIO07-J. Do not let external processes block on IO buffers |
| FIO08-C. Take care when calling remove() on an open file |
| FIO08-C. Take care when calling remove() on an open file |
| FIO08-C. Take care when calling remove() on an open file |
| FIO08-J. Distinguish between characters or bytes read from a stream and -1 |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-J. Do not rely on the write() method to output integers outside the range 0 to 255 |
| FIO10-C. Take care when using the rename() function |
| FIO10-C. Take care when using the rename() function |
| FIO10-C. Take care when using the rename() function |
| FIO10-J. Ensure the array is filled when using read() to fill an array |
| FIO11-C. Take care when specifying the mode parameter of fopen() |
| FIO11-C. Take care when specifying the mode parameter of fopen() |
| FIO11-C. Take care when specifying the mode parameter of fopen() |
| FIO11-J. Do not convert between strings and bytes without specifying a valid character encoding |
| FIO12-J. Provide methods to read and write little-endian data |
| FIO13-C. Never push back anything other than one read character |
| FIO13-C. Never push back anything other than one read character |
| FIO13-C. Never push back anything other than one read character |
| FIO13-J. Do not log sensitive information outside a trust boundary |
| FIO14-C. Understand the difference between text mode and binary mode with file streams |
| FIO14-C. Understand the difference between text mode and binary mode with file streams |
| FIO14-C. Understand the difference between text mode and binary mode with file streams |
| FIO14-J. Perform proper cleanup at program termination |
| FIO15-C. Ensure that file operations are performed in a secure directory |
| FIO15-C. Ensure that file operations are performed in a secure directory |
| FIO15-C. Ensure that file operations are performed in a secure directory |
| FIO15-J. Do not reset a servlet's output stream after committing it |
| FIO16-J. Canonicalize path names before validating them |
| FIO17-C. Do not rely on an ending null character when using fread() |
| FIO17-C. Do not rely on an ending null character when using fread() |
| FIO17-C. Do not rely on an ending null character when using fread() |
| FIO18-C. Never expect fwrite() to terminate the writing process at a null character |
| FIO18-C. Never expect fwrite() to terminate the writing process at a null character |
| FIO18-C. Never expect fwrite() to terminate the writing process at a null character |
| FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file |
| FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file |
| FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file |
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO21-C. Do not create temporary files in shared directories |
| FIO21-C. Do not create temporary files in shared directories |
| FIO21-C. Do not create temporary files in shared directories |
| FIO22-C. Close files before spawning processes |
| FIO22-C. Close files before spawning processes |
| FIO22-C. Close files before spawning processes |
| FIO23-C. Do not exit with unflushed data in stdout or stderr |
| FIO23-C. Do not exit with unflushed data in stdout or stderr |
| FIO23-C. Do not exit with unflushed data in stdout or stderr |
| FIO24-C. Do not open a file that is already open |
| FIO24-C. Do not open a file that is already open |
| FIO24-C. Do not open a file that is already open |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO30-PL. Use compatible character encodings when performing network or file I/O |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| FIO32-C. Do not perform operations on devices that are only appropriate for files |
| FIO34-C. Distinguish between characters read from a file and EOF or WEOF |
| FIO34-C. Distinguish between characters read from a file and EOF or WEOF |
| FIO34-C. Distinguish between characters read from a file and EOF or WEOF |
| FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful |
| FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful |
| FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful |
| FIO38-C. Do not copy a FILE object |
| FIO38-C. Do not copy a FILE object |
| FIO38-C. Do not copy a FILE object |
| FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call |
| FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call |
| FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects |
| FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects |
| FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects |
| FIO42-C. Close files when they are no longer needed |
| FIO42-C. Close files when they are no longer needed |
| FIO42-C. Close files when they are no longer needed |
| FIO44-C. Only use values for fsetpos() that are returned from fgetpos() |
| FIO44-C. Only use values for fsetpos() that are returned from fgetpos() |
| FIO44-C. Only use values for fsetpos() that are returned from fgetpos() |
| FIO45-C. Avoid TOCTOU race conditions while accessing files |
| FIO45-C. Avoid TOCTOU race conditions while accessing files |
| FIO45-C. Avoid TOCTOU race conditions while accessing files |
| FIO46-C. Do not access a closed file |
| FIO46-C. Do not access a closed file |
| FIO46-C. Do not access a closed file |
| FIO47-C. Use valid format strings |
| FIO47-C. Use valid format strings |
| FIO47-C. Use valid format strings |
| FIO50-CPP. Do not alternately input and output from a file stream without an intervening positioning call |
| FIO50-J. Do not make assumptions about file creation |
| FIO51-CPP. Close files when they are no longer needed |
| FIO51-J. Identify files using multiple file attributes |
| FIO52-J. Do not store unencrypted sensitive information on the client side |
| FIO53-J. Use the serialization methods writeUnshared() and readUnshared() with care |
| Rec. 01. File I/O and Logging (FIO) |
| Rec. 07. File Input and Output (FIO) |
| Rec. 09. Input Output (FIO) |
| Rec. 09. Input Output (FIO) |
| Rec. 09. Input Output (FIO) |
| Rec. 13. Input Output (FIO) |
| Rule 07. File Input and Output (FIO) |
| Rule 07. Input Output (FIO) |
| Rule 09. Input Output (FIO) |
| Rule 09. Input Output (FIO) |
| Rule 09. Input Output (FIO) |
| Rule 13. Input Output (FIO) |
| Rule Template |
| VOID Do not make assumptions about open() and file creation |
| VOID FIO00-CPP. Take care when creating format strings |
| VOID FIO01-CPP. Be careful using functions that use file names for identification |
| VOID FIO02-CPP. Canonicalize path names originating from untrusted sources |
| VOID FIO03-CPP. Do not make assumptions about fopen() and file creation |
| VOID FIO04-CPP. Detect and handle input and output errors |
| VOID FIO05-CPP. Identify files using multiple file attributes |
| VOID FIO06-CPP. Create files with appropriate access permissions |
| VOID FIO07-CPP. Prefer fseek() to rewind() |
| VOID FIO08-CPP. Take care when calling remove() on an open file |
| VOID FIO09-CPP. Be careful with binary data when transferring data across systems |
| VOID FIO10-CPP. Take care when using the rename() function |
| VOID FIO11-CPP. Take care when specifying the mode parameter of fopen() |
| VOID FIO12-CPP. Prefer setvbuf() to setbuf() |
| VOID FIO13-CPP. Never push back anything other than one read character |
| VOID FIO14-CPP. Understand the difference between text mode and binary mode with file streams |
| VOID FIO15-CPP. Ensure that file operations are performed in a secure directory |
| VOID FIO17-CPP. Prefer streams to C-style input and output |
| VOID FIO18-CPP. Never expect write() to terminate the writing process at a null character |
| VOID FIO19-CPP. Do not create temporary files in shared directories |
| VOID FIO20-CPP. Do not rely on an ending null character when using read() |
| VOID FIO21-CPP. Do not simultaneously open the same file multiple times |
| VOID Intro-FIO51-JG. Be careful using methods that use file names for identification |
| VOID Rec. 07. Input Output (FIO) |

------------------------------------------------------------------------
[](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152403)
