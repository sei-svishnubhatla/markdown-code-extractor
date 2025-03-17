> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID.+Do+not+create+temporary+files+in+shared+directories?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I took a quick look at IntegerLib and have to recommend against using it.; There are numerous problems, but for example in add.c:
int addsi(int lhs, int rhs){
 errno = 0;
 if( (((lhs+rhs)^lhs)&((lhs+rhs)^rhs)) >> (sizeof(int)*CHAR_BIT-1) ) {
  error_handler("OVERFLOW ERROR", NULL, EOVERFLOW);
  errno = EINVAL;
 }
return lhs+rhs;
}
Right off the bat, it adds lhs and rhs, which can overflow immediately, producing undefined behavior which could include trapping.  There are also problems using bitwise operations that involve the sign bit.  I'm sure that there are ways to correctly implement such a library, but this isn't one of them.
                                        Posted by dagwyn at Apr 15, 2008 15:59
                                     |
| It occurs to me that this could theoretically be enforced by an automated checker.
The checker could catch all instances of arithmetic expressions and demand they be replaced by functions in IntegerLib.  Not sure this is worth it. At any rate, if this rule is to be considered 'enforceable', we should add a NCCE/CCE pair to it.
                                        Posted by svoboda at Jun 18, 2008 14:01
                                     |
| We should extend this recommendation to provide for the possibility of using AIR integers instead of a library.
                                        Posted by rcs_mgr at Aug 01, 2009 21:09
                                     |
| I found a Google library (Safe Integer Operations - http://code.google.com/p/safe-iop/). ; The CERT IntegerLib.zip URL is 404/AWOL.  I've seen INT03-CPP (the C++ equivalent of this recommendation) has been voided.
    What is the state of play here?
    What happened?
(I'm also mildly curious: what are AIR integers?)
                                        Posted by jonathan.leffler@gmail.com at Apr 17, 2012 19:23
                                     |
| yes, this rule needs a major overhaul or be voided.  you can read about AIR integers here:  http://www.sei.cmu.edu/library/abstracts/reports/10tn008.cfm
                                        Posted by rcs_mgr at Apr 18, 2012 01:42
                                     |

