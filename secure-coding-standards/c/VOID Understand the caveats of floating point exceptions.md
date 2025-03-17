> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Temporary+files+must+be+removed+before+the+program+exits?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Use+expression+containing+sizeof+operator+to+calculate+the+length+of+an+array?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Are examples needed?
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 17:48
                                     |
| Do we need a risk assessment here?
                                        Posted by avolkovi at Apr 15, 2008 11:12
                                     |
| Should also mention that IEEE/IEC f.p., which is widespread, generally represents "exceptional" values as infinities or NaNs ("in band" and meant to propagate throughout a computation, to be tested only at the end).
                                        Posted by dagwyn at Apr 16, 2008 19:24
                                     |
| We should also mention that non-floating point operations will sometimes throw FPEs because of the way modulus and division are implemented ... ie: INT_MIN%-1 or foo%0
                                        Posted by avolkovi at Apr 17, 2008 09:24
                                     |

