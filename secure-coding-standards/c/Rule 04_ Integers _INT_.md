-   Page:
    [INT30-C. Ensure that unsigned integer operations do not wrap](/confluence/display/c/INT30-C.+Ensure+that+unsigned+integer+operations+do+not+wrap)
-   Page:
    [INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data](/confluence/display/c/INT31-C.+Ensure+that+integer+conversions+do+not+result+in+lost+or+misinterpreted+data)
-   Page:
    [INT32-C. Ensure that operations on signed integers do not result in overflow](/confluence/display/c/INT32-C.+Ensure+that+operations+on+signed+integers+do+not+result+in+overflow)
-   Page:
    [INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors](/confluence/display/c/INT33-C.+Ensure+that+division+and+remainder+operations+do+not+result+in+divide-by-zero+errors)
-   Page:
    [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](/confluence/display/c/INT34-C.+Do+not+shift+an+expression+by+a+negative+number+of+bits+or+by+greater+than+or+equal+to+the+number+of+bits+that+exist+in+the+operand)
-   Page:
    [INT35-C. Use correct integer precisions](/confluence/display/c/INT35-C.+Use+correct+integer+precisions)
-   Page:
    [INT36-C. Converting a pointer to integer or integer to pointer](/confluence/display/c/INT36-C.+Converting+a+pointer+to+integer+or+integer+to+pointer)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [int](https://confluence/label/seccode/int) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT30-C | High | Likely | High | P9 | L2 |
| INT31-C | High | Probable | High | P6 | L2 |
| INT32-C | High | Likely | High | P9 | L2 |
| INT33-C | Low | Likely | Medium | P6 | L2 |
| INT34-C | Low | Unlikely | Medium | P2 | L3 |
| INT35-C | Low | Unlikely | Medium |  P2  |  L3  |
| INT36-C | Low | Probable | High | P2 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| DCL31-C. Declare identifiers before using them |
| DCL31-C. Declare identifiers before using them |
| DCL31-C. Declare identifiers before using them |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |

------------------------------------------------------------------------
[](../c/Rule%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152236)
## Comments:

|  |
| ----|
| Not sure where this should go, but you might want to mention arithmetic right shift as it can surprise people. We talk about it on page 273 of TAOSSA. Basically if the left operand of a right shift is signed, an arithmetic shift is performed, and the sign bit can be propagated as the number is shifted. So, you could have something like this:
int print_high_byte(int number){    char buf[sizeof("256")];    sprintf(buf, "%u", number >> 24);        ...

;If number was 0x80000000, **number \>\> 24** would be 0xFFFFFF80, thus overflowing **buf**.
For bit extraction, one remediation is to use the idiom **((number \>\> 24) & 0xff)**. However, you really probably want to make sure that you're not right-shifting signed integers unless you expect arithmetic shift.
![](images/icons/contenttypes/comment_16.png) Posted by jm at Dec 25, 2006 15:37
\| \|
I've added this as:
INT13-A. Do not assume that a right shift operation is implemented as a logical or an arithmetic shift
Thanks!
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 28, 2007 13:25
\| \|
A common vulnerability that I haven't seen explicitly called out in any of the rules in this section is calling the [Character classification functions](http://www.opengroup.org/onlinepubs/009695399/basedefs/ctype.h.html) with an argument of type `char` in environments where `char` is a signed type. For example, the following program may exhibit undefined behavior when the value of the character argument passed to `toupper()` is negative:
``` java
int strcasecmp(const char *s1, const char *s2) {
    int result;
    for (; (0 == (result = (toupper(*s1) - toupper(*s2)))) && *s1; ++s1, ++s2);
    return result;
}
```
The safe way to write the same function is like so:
``` java
int strcasecmp(const char *s1, const char *s2) {
    int result;
    for (; (0 == (result = (toupper((unsigned char)*s1) - toupper((unsigned char)*s2)))) && *s1; ++s1, ++s2);
    return result;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 02, 2009 19:17
\| \|
I should have searched the site. This problem is already covered in [STR37-C](https://www.securecoding.cert.org/confluence/display/seccode/STR37-C.+Arguments+to+character+handling+functions+must+be+representable+as+an+unsigned+char).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 02, 2009 19:30
\|
