All the rules can use review. Sections of particular interest include Signals and File I/0
Specific rules/recommendations that can use review in priority order:
------------------------------------------------------------------------
[SIG01-C. Understand implementation-specific details regarding signal handler persistence](SIG01-C_%20Understand%20implementation-specific%20details%20regarding%20signal%20handler%20persistence)
Comment:
Are you sure the Windows API doesn't have an alternative way of setting up signal handlers that doesn't reset the signal to default when the handler is called? If it were true, then how does Windows SFU implement the sigaction() function? I suppose it could be using an undocumented kernel interface. Or maybe "signals" in SFU are not the same thing as the "signals" in the Windows API.
------------------------------------------------------------------------
[FLP03-C. Detect and handle floating-point errors](FLP03-C_%20Detect%20and%20handle%20floating-point%20errors)
Comment:
Windows OS nor the libraries with MS Visual studio support C99 functions, instead Structured Exception Handling is used to handle for FP operation.
------------------------------------------------------------------------
[FIO32-C. Do not perform operations on devices that are only appropriate for files](FIO32-C_%20Do%20not%20perform%20operations%20on%20devices%20that%20are%20only%20appropriate%20for%20files)
Comment:
Updated the compliant solution and eliminated a race condition a la POS01-A
Not sure what to do about the Windows solution as I don't really understand it
Comment from Aaron Ballman: the Windows solution does not have the same race condition issues because the file is already opened at the point of determining whether it is a disk file or not.  I don't believe there are any further concerns with the example.
------------------------------------------------------------------------
[VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array](VOID%20STR35-C_%20Do%20not%20copy%20data%20from%20an%20unbounded%20source%20to%20a%20fixed-length%20array)
Comment:
What do fgets and getchar do when newlines are CR-LF (Microsoft Windows) or CR (MacOS through v9)? I can imagine fgets converting the character, but would not expect getchar to (and would argue that it would be incorrect behavior if it did).
Another concern is whether fgets converts the CRLF to a single newline under Microsoft Windows either. MSDN implies that it does, but I haven't set-up MSVC to test it.
By reputation (rather than empirical experiment, in other words), the behaviour of fgets() on Windows will depend on whether the file is opened as a text file or a binary file – whereas on Unix there is no difference between those two. If the file is opened as a text file, then fgets() will strip the CR and leave the LF. If the file is opened as a binary file, then fgets() will not strip the CR (so the string will normally end CRLF when the input operation completes). Similar comments apply to all the other functions. Kernighan & Pike's "The Practice of Programming" illustrates a variant of fgets() that handles three separate line termination conventions - Unix with LF, MacOS (pre-X) with CR, and Windows with CRLF (Chapter 4, on reading CSV data; function endofline()).
------------------------------------------------------------------------
[FIO06-C. Create files with appropriate access permissions](FIO06-C_%20Create%20files%20with%20appropriate%20access%20permissions)
Also, are there any Unix-like systems where fopen() permissions are not affected by umask()? I can't imagine that there are. What about the alternative - Windows?
------------------------------------------------------------------------
