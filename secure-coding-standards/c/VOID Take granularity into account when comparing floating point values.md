> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=28737771) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=3473523)
## Comments:

|  |
| ----|
| 
P.J. Plauger objected to this rule during the WG14 review of the guidelines, and the committee agreed with his argument.; He stated that those who know what they are doing in floating point don't do equality comparisons except against a known exact value, such as 0.0 or 1.0.  Performing a fuzzy comparison would break their code.  He said that if a fuzzy comparison would be necessary, then it is because someone has chosen the wrong algorithm and they need to go back and rethink it.
                                        Posted by dmk at Nov 05, 2007 19:47
                                     |
| This practice is also discredited in [Goldberg 91] which is referenced by [FLP02-C. Avoid using floating point numbers when precise computation is needed].; See the quote from Goldberg at the bottom of this comment.
There is definitely some wiggle room in C's definition of floating point.  For example, if an integer is converted to a floating point type that cannot represent all the bits of its value, the result can be either the nearest higher or nearest lower floating point value, not simply the nearest value (see [ISO/IEC 9899:1999] section 6.3.1.4, "Real floating and integer").  Also, "The accuracy of the floating-point operations . . . is implementation-defined," (see [ISO/IEC 9899:1999] section 5.2.4.2.2, "Characteristics of floating types <float.h>").  I am trying to think of a way to incorporate all of this into a recommendation or rule, but this is not it.
 Incidentally, some people think that the solution to such anomalies is never to compare floating-point numbers for equality, but instead to consider them equal if they are within some error bound E. This is hardly a cure-all because it raises as many questions as it answers. What should the value of E be? If x < 0 and y > 0 are within E, should they really be considered to be equal, even though they have different signs? Furthermore, the relation defined by this rule, a ~ b  |a - b| < E, is not an equivalence relation because a ~ b and b ~ c does not imply that a ~ c.
                                        Posted by dmk at Dec 04, 2007 18:23
                                     |
| This rule is alive (with a better mechanism of determining when two values are 'close enough'), as: FLP35-C. Take granularity into account when comparing floating point values
Further discussion should go there.
                                        Posted by svoboda at Feb 12, 2009 11:12
                                     |

