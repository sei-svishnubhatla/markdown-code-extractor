> [!info]  
>
> This practice has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard: It has been superseded by rule [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts). This guideline has not been erased in case it contains information that might be useful in the future.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Functions+should+validate+their+parameters?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Initialize+local+variables+immediately+after+declaration?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| How is this rose-possible?
                                        Posted by avolkovi at Jul 21, 2008 11:16
                                     |
| The general problem of array bounds-checking is not solveable by static analysis.
I'm not sure how LDRA and Kocwork handle this rule, but there is a simple check to catch the NCCE: A violation is code that:
    uses a variable to index an array
    performs a bounds check on the var (eg if (var < ...))
    the variable is signed
    no bounds check that the var >= 0.
                                        Posted by svoboda at Jul 21, 2008 12:22
                                     |
| Would it make sense to ask for all array indexes to be unsigned?
                                        Posted by avolkovi at Jul 29, 2008 13:40
                                     |
| Strictly speaking, yes. But that would invalidate the use of (signed) ints as array indices, which is a fairly common coding convention. It also doesn't eliminate the need for explicit range checking of your array indices, it just ensures they can't be < 0.
                                        Posted by svoboda at Jul 29, 2008 14:34
                                     |
| But the rose algorithm you proposed assumes that range checking is already occurring.  It's also not correct to use signed values for indices, that definitely violates a CWE rule, and I believe one of our's as well.
                                        Posted by avolkovi at Jul 29, 2008 14:56
                                     |
| This recommendation should be modified to be clearer that negative array indices are not in themselves a problem provided that the pointer + integer does not reference outside the array or the toofar.
                                        Posted by rcs at Oct 29, 2009 14:56
                                     |

