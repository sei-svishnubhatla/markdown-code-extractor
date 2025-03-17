> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Practices: It has been superseded by recommendation [MSC21-C. Use inequality to terminate a for loop](/confluence/pages/createpage.action?spaceKey=seccode&title=MSC21-C.+Use+inequality+to+terminate+a+for+loop). It has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Be+careful+using+errno+with+multiple+threads?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+C+Rules+Implemented+in+Rose?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| David, can you chop to bits kindly remove the smiley face that consumed my semicolon and right paren?; Thanks.
                                        Posted by akeeton at Jun 24, 2009 14:23
                                     |
| Smiley chop^H^H^H^Hremoved. Remember, the backslash is your friend.
But this rule needs more love. I suspect it should be merged with MSC21-C. Use inequality to terminate a for loop. I do like EX1 however; programmers that intend loops to be inifite should use standard conventions to indicate this.
                                        Posted by svoboda at Jun 24, 2009 14:29
                                     |
| Also the Zune bug from MSC01-C. Strive for logical completeness would be more happy here than in its current home.
                                        Posted by svoboda at Jun 24, 2009 14:32
                                     |
| David's right, this should certainly be merged with MSC21-C, and I actually see this merged rule fitting into the expressions EXP section.
Beware of infinite loops is way to vague a title. Maybe "Use inequality to terminate a loop whose counter changes by more than one"
                                        Posted by rcs_mgr at Jun 24, 2009 15:33
                                     |
| This guideline needs to be merged with MSC21C before I can reference it from Java.  
                                        Posted by dmohindr at Aug 14, 2009 15:16
                                     |
| I assume this guideline has been superseded by MSC21-C. Use inequality to terminate a for loop and has been retired. I'm labeling it void.
                                        Posted by martinsebor at May 01, 2010 11:13
                                     |

