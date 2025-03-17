> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+All+threads+must+exit+before+returning+or+exiting+from+a+main+program?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Always+check+for+errors+when+using+threads?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| How does this differ from MEM35-C. Ensure that size arguments to memory allocation functions are correct?
The non-compliant solution should also check for overflow.  I prefer that, whenever possible, the non-compliant and compliant solutions differ only in compliance to the rule/recommendation in which they appear.
I also like the idiom:
  long *p = malloc(len * sizeof(*p));

I'm uncertain if that complies with standard C, since the initializer refers to the variable being defined (I could not find anything in the standard that allowed or disallowed it).
Is there a particular reason we aren't advocating the use of variable-length arrays to avoid this problem completely:
``` java
  long p[len];
```
It runs risk of violating [MEM05-A. Avoid large stack allocations](/confluence/pages/createpage.action?spaceKey=c&title=MEM05-A.+Avoid+large+stack+allocations) if `len` is unbounded, of course, but frees the memory automatically when you got outside the block and sizeof(p) is computed "properly" (what most people mean when they do that).
![](images/icons/contenttypes/comment_16.png) Posted by hburch at Jun 14, 2007 08:51
\| \|
These rules don't appear to be significantly different and should be combined.
I think the sizeof(\*p) is OK. As jsg points out, it is used in C99 6.5.3.4#5.
I think we could advocate VLAs with a few caveats. The first of course is the one you mention of violating MEM05-A. Second, I don't believe VLAs are supported by many compilers including MSVS 2005. GCC does support VLAs in v 4.2 but states in their [documentation](http://gcc.gnu.org/onlinedocs/gcc-4.2.0/gcc/Variable-Length.html#Variable-Length) that: "GCC's implementation of variable-length arrays does not yet conform in detail to the ISO C99 standard." They also compare VLAs to using alloca(). 8^)
In this particular example, I don't think the use of VLAs does anything to address your concerns with integer overflow. The same multiplication operation is going to be performed, me thinks.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 19, 2007 16:02
\|
