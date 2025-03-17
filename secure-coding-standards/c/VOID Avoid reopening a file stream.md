> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Automated+Detection+Tools?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Be+careful+using+errno+with+multiple+threads?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Why is this an issue? If the attacker can open the file for writing, he has full permissions to it anyway, and has the right to do whatever he pleases with it.; Why should we waste kernel memory and keep around extra file descriptors when it goes against everything we have said about releasing locks as soon as possible?  The idea here is to stress the importance of verification during the fopen to make sure we don't clobber something accidentally, but the problem being described is a race condition, with the compliant solution being "never release locks, ever".  Besides, fopen/fclose is not a really good locking mechanism anyway, especially with mounted file systems (imho).
As a counterexample, imagine a log rotating cron job that runs during this process, it will be unable to do it's job because we keep the file open for writing indefinitely.
                                        Posted by avolkovi at Mar 06, 2008 10:13
                                     |
| I sympathize with and largely share that concern.
Comment: an attacker does not have to have access permissions on the file to be able to interfere with it - they merely need permission to modify the directory containing the file.; In a POSIX system, with that permission, the attacker can rename (or remove) the file and place a symlink to somewhere else in its place - and especially for programs with raised privileges (those run by root, or setuid or setgid programs), that can lead to damage in unexpected places.
Long-running processes that have logs that get rotated need to close the old file periodically, because the program can continue writing to a removed log file even though no-one else can access it -- thereby chewing up disk space that the admin thought had been released.  For some processes, the cost of opening and closing a file is negligible and it can be done on demand.  For other processes, the cost of opening and closing a file is not negligible and the overhead would be intolerable.  Nevertheless, it is probably a good practice to have some limit on the log file size, and once that limit is reached, it would be sensible to start a new log file.  Depending on the application, that might be some kilobytes or a few megabytes in size.  That size should, in a POSIX environment, be determined by fstat().  And for logs in general, the O_APPEND flag should be specified to open().  And you probably want to create new log files with the O_CREAT and O_EXCL flags.
Other ways of switching logs include sending a signal to the long-running process to indicate that it should switch. 
                                        Posted by jonathan.leffler@gmail.com at Mar 19, 2008 02:17
                                     |
| I'm also not sure why this particular behavior is a vulnerability.; Even if the file is only opened once, a user who is able to substitute a symbolic link at some point along the file path can cause that one open to overwrite an arbitrary file.
I would think a better rule would be to avoid opening files with a path that can be compromised through a user symbolic link in a program that runs with elevated privileges.  Or if such behavior must take place, temporarily drop privileges before the call to open.
                                        Posted by adahmad at Apr 14, 2008 09:15
                                     |
| Again, apps should almost never allow users to specify file names other than sanitized entries in protected directories maintained by the app, in which case the only issue is coordinating access between multiple instances of the app (which append mode should handle, or if not, use file/record locking).
                                        Posted by dagwyn at Apr 17, 2008 19:05
                                     |
| I was also having a hard time seeing where the vulnerability was. I made significant changes to this recommendation to try to  identify a circumstance in which this recommendation was applicable.  Please review and let me know if this works or not.  If not, we may need to just get rid of this recommendation.
                                        Posted by rcs_mgr at Jun 08, 2008 10:00
                                     |

