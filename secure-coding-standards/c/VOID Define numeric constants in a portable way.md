> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Create+temporary+files+securely?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2687100)
## Comments:

|  |
| ----|
| Nice rule. Just one comment:
    You computed the priority / levels in the 'Risk Assessment' section correctly. But I would argue that the severity is high, not medium. This would be because your security flaw can lead to a buffer overflow, and buffer overflows allow arbitrary code execution as we've shown in class.
                                        Posted by svoboda at Nov 04, 2008 10:59
                                     |
| Thanks for adjusting the severity. Don't forget that changing the severity also changes the priority & level.
                                        Posted by svoboda at Nov 05, 2008 08:52
                                     |
| I think an even more portable way to turn all bits on is:
unsigned int max = ~0;
I think this guideline needs a thorough review.  My confidence is not high.
                                        Posted by rcs at Apr 01, 2009 07:32
                                     |
| I think this belongs in the INT section... all of the NCCEs would still be broken if we replaced macros by longs.  Is this why INT17-C. Define integer constants in an implementation-independent manner exists?
We also need to be careful that our CCE uses unsigned longs as per INT13-C. Use bitwise operators only on unsigned operands... as it stands, our CCE violates INT13-C, but changing it to unsigned would violate INT30-C. Ensure that unsigned integer operations do not wrap
Should this example be an exception to INT13-C?
                                        Posted by avolkovi at Jul 23, 2009 10:12
                                     |

