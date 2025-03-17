> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+use+volatile+as+a+synchronization+primitive?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=43319861)
## Comments:

|  |
| ----|
| This looks like a pretty good start.
Some comments:
> except it is a specific and possibly more common case of incorrect pointer arithmetic.

this seems contradictory.  If it is a specific instances of a more general problem there is no way it can be more common (by definition it is a subset).
> Assume malloc failure check exists but is truncated from code. 

No, let's not assume that and add the check.  Perhaps you could encapsulate these examples in a function?
"int i" should be declared as "size_t"
                                        Posted by rcs_mgr at Mar 16, 2010 07:54
                                     |
| Did you consider using offsetof() in a compliant solution?
In reading this:
C99 guarantees that it is permissible to use the address of fieldbuffer + (i * 8) as written in Section 6.5.6.9.
it is not clear to me what exactly C99 guarantees and why this guarantee is violated.  Can you elaborate further, and possibly quote the relevant section of the standard?
> This compliant solution uses the sizeof operator to eliminate the problem.

replace "eliminate the problem" with a more precise description of the solution.
                                        Posted by rcs_mgr at Mar 16, 2010 08:02
                                     |
| All the code examples here merely demonstrate the importance of EXP09-C. Use sizeof to determine the size of a type or variable.  Also the pointer arithmetic is wrong, in that since fieldBuffer is a dynamicField* you can only add numbers between 0 and BUFFERSIZE...you don't want to multiply by anything.  (You could mitigate this problem by making fieldBuffer a char*.)   Can you provide a NCCE that complies with EXP09-C?
    In 1st NCCE, good to remember that malloc failure check is necessary, but better to include it explicitly in the code.
                                        Posted by svoboda at Mar 16, 2010 16:37
                                     |
| Added some of these fixes. Now I need to fix logic in compliant code examples
                                        Posted by kaichong at Mar 17, 2010 15:24
                                     |
| 
    In the CCE, sizeof(char) == 1 as mandated by C99, so you don't need to divide by sizeof(char).
    In both NCCE & CCE, the final assignment statement has a type problem...you are assigning a dynamicField to a char. I would be shocked if GCC didn't at least produce a warning about this.
There may be a valid rule here but I can't see it behind the technical problems in both code samples.
                                        Posted by svoboda at Mar 22, 2010 15:38
                                     |

