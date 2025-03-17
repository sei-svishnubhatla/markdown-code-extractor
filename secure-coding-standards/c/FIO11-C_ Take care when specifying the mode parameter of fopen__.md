The C Standard identifies specific strings to use for the `mode` on calls to `fopen()` and `fopen_s()`. C11 provides a new mode flag, `x`, that provides the mechanism needed to determine if the file that is to be opened exists. To be strictly [conforming](BB.-Definitions_87152273.html#BB.Definitions-conforming) and portable, one of the strings from the following table (adapted from the C Standard, subclause 7.21.5.2 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]) must be used:
**Strings to Use for the Mode on Calls to `fopen()` and `fopen_s()`**

| mode String | Result |
| ----|----|
| r | Open text file for reading |
| w | Truncate to zero length or create text file for writing |
| wx | Create text file for writing |
| a | Append; open or create text file for writing at end-of-file |
| rb | Open binary file for reading |
| wb | Truncate to zero length or create binary file for writing |
| wbx | Create binary file for writing |
| ab | Append; open or create binary file for writing at end-of-file |
| r+ | Open text file for update (reading and writing) |
| w+ | Truncate to zero length or create text file for update |
| w+x | Create text file for update |
| a+ | Append; open or create text file for update, writing at end-of-file |
| r+b or rb+ | Open binary file for update (reading and writing) |
| w+b or wb+ | Truncate to zero length or create binary file for update |
| w+bx or wb+x | Create binary file for update |
| a+b or ab+ | Append; open or create binary file for update, writing at end-of-file |

If the `mode` string begins with one of these sequences, the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) might choose to ignore the remaining characters, or it might use them to select different kinds of files.
When calling `fopen_s()`, any of the mode strings used for writing (`w` or `a`) may be prefixed with the `u` character to give the file system default access permissions.
An implementation may define additional `mode` strings, but only the modes shown in the table are fully portable and C compliant. Beware that Microsoft Visual Studio 2012 and earlier do not support the `x` or `u` mode characters \[[MSDN](http://msdn.microsoft.com/en-us/library/z5hh6ee9(v=vs.110).aspx)\].
## Risk Assessment
Using a `mode` string that is not recognized by an implementation may cause the call to `fopen()` to fail.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO11-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  |  |
| LDRA tool suite | 9.7.1 | 590 S | Partially implemented |
| PC-lint Plus | 1.4 | 2472, 2473 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. FIO11-C | Checks for bad file access mode or status (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO11-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO11-CPP. Take care when specifying the mode parameter of fopen() |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 7.21.5.3, "The;fopen Function" |

------------------------------------------------------------------------
[](../c/FIO10-C_%20Take%20care%20when%20using%20the%20rename__%20function) [](../c/Rec_%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152185)
## Comments:

|  |
| ----|
| Someone mentioned a GNU C Library extension with the letter 'x' for the O_EXCL flag in a comment in a previous item.
Another previous item mentioned the letter 'u' as modifying the permissions on files - possibly in conjunction with fopen_s().
These seem somewhat inconsistent with the advice given here.;
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:46
                                     |
| The point is that using anything beyond this list is nonportable, which might be okay but the programmer needs to consider whether it fits the project goals, and should warn loudly about it in his source code.
                                        Posted by dagwyn at Apr 17, 2008 12:30
                                     |
| Section 7.19.3 of C99 says
A stream is associated with an external file (which may be a physical device) by opening a file, which may involve creating a new file. Creating an existing file causes its former contents to be discarded, if necessary. If a file can support positioning requests (such as a disk file, as opposed to a terminal), then a file position indicator associated with the stream is positioned at the start (character number zero) of the file, unless the file is opened with append mode in which case it is implementation-defined whether the file position indicator is initially positioned at the beginning or the end of the file. The file position indicator is maintained by subsequent reads, writes, and positioning requests, to facilitate an orderly progression through the file.
How does this reconcile with the definition of the flags given above? Is this a problem with the standard?
                                        Posted by avolkovi at Jun 05, 2008 09:22
                                     |
| There is no "problem" in the standard. The idea is that by opening something in append mode, you will only be appending to it. Therefore, the point of having a file position indicator (knowing where you are in a file and being able to move around within a file) is unnecessary and, in fact, possibly dangerous (what validity is there in seeking around on something that is by definition append-only?). 
If you carefully read the definitions of all of the output functions, you can notice that the C standard weaves around these problems by making the file position indicator basically useless on an append stream, e.g.:
7.19.7.3
The fputc function writes the character specified by c (converted to an unsigned char) to the output   stream pointed to by stream, at the position indicated by the associated file position indicator for the stream (if defined), and advances the indicator appropriately. If the file cannot support positioning requests, or if the stream was opened with append mode, the character is appended to the output stream.
                                        Posted by shaunh at Jun 05, 2008 10:18
                                     |
| ok... shaun and I talked about this... looks the file position indicator isn't defined to do anything useful and has no meaning whatsoever in append mode since you can't seek
                                        Posted by avolkovi at Jun 05, 2008 10:18
                                     |
| I recently had this same question.
> 1. append mode
>
> section 7.19.3 Files paragraph 1 states:
>
> If a file can support positioning requests (such as a
> disk file, as opposed to a terminal), then a file position indicator associated with the
> stream is positioned at the start (character number zero) of the file, unless the file is
> opened with append mode in which case it is implementation-defined whether the file
> position indicator is initially positioned at the beginning or the end of the file.
>
> while section 7.19.5.3 The fopen function, paragraph 3 seemingly contradicts this:
>
> a append; open or create text file for writing at end-of-file
>
> i'm guessing section section 7.19.3 is correct and that section 7.19.5.3 is simply a misleading simplification, yes?

I don't see any obvious contradiction.
The first part describes the initial location of the
"file position indicator" when a file is opened with
append, the second says that writes always occur at
the end of the file.
They are separate things. The first, in effect, says
that what you get returned from ftell() just after
opening with append is implementation defined. The
second says how opening with append differs from a
regular opened-for-writing file.
                                        Posted by rcs at Jun 05, 2008 10:21
                                     |
| This recommendation could use a noncompliant code example and compliant solution.
                                        Posted by svoboda at Feb 01, 2019 11:00
                                     |

