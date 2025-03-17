> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Temporary+files+must+be+opened+with+exclusive+access?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Understand+the+caveats+of+floating+point+exceptions?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| The text in the Risk Assessment section is identical to that of TMP32-C and does not correspond to the rule being discussed.
                                        Posted by adahmad at Apr 14, 2008 09:52
                                     |
| All the TMP pages seem to be about the same, and my comments on the othe rpages apply here also, including that tmpfile() is fine on POSIX.
The mkstemp solution is not useful for non-POSIX systems, or for older POSIX implementations.; If for soime reason one doesn't use tmpfile(), then the tmpnam/fopen approach may be the only alternative, in which case the program should use atexit to register a clean-up function, which will remove the tmp file.  Indeed, there should be some rule to "use atexit to ensure that clean-up actions are done before termination".  Of course if the program ABENDs (illegal instruction, etc) then the clean-up function won't be called, but that indicates a severe bug and nothing can fix that other than correcting the bug.
                                        Posted by dagwyn at Apr 17, 2008 19:55
                                     |
| 
Of course if the program ABENDs (illegal instruction, etc) then the clean-up function won't be called, but that indicates a severe bug
If the program is forcibly terminated (e.g. by somebody sending it a SIGKILL, on a POSIX system), the clean-up function will also not be called, and that is not a bug.
                                        Posted by geoffclare at Apr 21, 2008 10:51
                                     |
| The way mktemp() and mkstemp() are treated on this page is inconsistent. It says of mktemp()+open() "Neither of these functions provides any guarantees about removing the temporary file", but this is equally true of mkstemp().; The compliant solution using mkstemp() gets round this by unlinking the file immediately after the mkstemp() call.
Either the text after the mktemp()+open() code should explain that the code could meet this rule by unlinking the file immediately after the open(), but that it would still be non-compliant for reasons explained in other rules, or the mktemp()+open() example should just be removed.
                                        Posted by geoffclare at Apr 21, 2008 11:16
                                     |
| We should probably merge this with FIO43-C. Do not create temporary files in shared directories as half the rule is recycled from there anyway
                                        Posted by avolkovi at Apr 29, 2008 10:10
                                     |
| on second thought, this should either be deleted or made into a recommendation, since even our CS does not guarantee compliance under abnormal termination (ie- just before the unlink)
                                        Posted by avolkovi at Apr 29, 2008 10:12
                                     |
| resolved by someone who is not me
                                        Posted by avolkovi at Apr 29, 2008 10:13
                                     |
| mktemp+open is also vulnerable to a TOCTOU problem, I think this might have been mentioned in another comment... both are vulnerable to the closing issue
                                        Posted by avolkovi at Apr 29, 2008 11:01
                                     |

