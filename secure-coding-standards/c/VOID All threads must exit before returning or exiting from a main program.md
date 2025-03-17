> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Allocate+sufficient+memory+for+an+object?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| First, this should be in the C++ space, under memory management.  
The title should be "Ensure all threads exit before exiting main"
You need to give the rule an identifier.
main should be spelled main().  Put dual curly braces around your code that appears in text so that it is formatted properly.
Don't say "The following noncompliant code example..." just say "This noncompliant code example"
Just declare your main as int main(void) when you are not doing using the arguments.
Fix up the format of your reference.
Non-compliant should be spelled "Noncompliant" and the noncompliant code example should be pink, not blue.  Try to match the formatting of the other guidelines.
You need a description in the risk assessment session that reads "Failure to exit all threads before exiting main may result in (something scary happening)" 
                                        Posted by rcs at Nov 06, 2009 18:56
                                     |
| In addition to Rob's suggestions, you should also do the following:
    Sigh. We have a few pthreads in the POSIX C section, but nothing in C++. Eventually we will make Concurrency sections for both C & C++, but they will likely use the threading APIs in both standards. For now, just put this rule in the Misc section of the C++ wiki.
    Why is the severity and remediation cost medium? Add some text to the Risk Assessment section describing the consequences of violating this rule.
    Minor item: add appropriate background colors to the code samples (see the raw text of a finished rule to see how to do this.)
                                        Posted by svoboda at Nov 06, 2009 19:59
                                     |
| 
    Does pthread_join() really "destroy" threads? What does the documentation say?
    IIRC, abort() and exit() are also pretty sinister.
    In java world we typically use a finally block to ensure that any cleanup code is executed. However, in case of abnormal program termination such as a ctrl + c this does not work unless you use shutdown hooks as described in the Java guideline ERR09-J. Do not allow untrusted code to terminate the JVM. There might be something similar for C++. I hope this helps.
                                        Posted by dmohindr at Nov 06, 2009 20:22
                                     |

