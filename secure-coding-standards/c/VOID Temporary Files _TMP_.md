> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Take+granularity+into+account+when+comparing+floating+point+values?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Temporary+files+must+be+opened+with+exclusive+access?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| UNIX/Linux users may well have an extra weapon in this arsenal if this temporary file is needed only by the current program.
After they create and open some suitable temp file, they can *unlink the file* so it is completely invisible in the filesystem while they use it. As long as they have a handle (the file descriptor, or indirectly via a FILE* pointer), they can read, write, and seek that file as much as they like with *no chance* of it being seen or interrupted by any outside program.
Furthermore, when the program using the temp file exists, it's automatically deleted because the last link to the file is removed, and it requires no intentional cleanup operation by the program - the OS handles this.
The file descriptor can be passed to child processes (if desired), and the same rules apply.
It's a huge win for a temporary file on *ix.
Win32 (and probably other operating systems) won't allow a file to be deleted while open, so all the usual precautions about sharing and cleanup-on-exit must be observed.;
                                        Posted by steve at Mar 14, 2008 01:48
                                     |
| This is shown in FIO43-C. Do not create temporary files in shared directories.
                                        Posted by dmk at Mar 14, 2008 16:14
                                     |
| (1) It should be mentioned that the POSIX function tempnam() lets the user specify at run time the directory in which the temp file will be created.
(2)  This is one more case in which the app should create temp files in a protected directory rather than in a public one.
                                        Posted by dagwyn at Apr 17, 2008 19:15
                                     |
| (1) What about the TOCTOU and clean up problems associated with tempnam (same as tmpnam)
                                        Posted by avolkovi at Apr 29, 2008 10:53
                                     |

