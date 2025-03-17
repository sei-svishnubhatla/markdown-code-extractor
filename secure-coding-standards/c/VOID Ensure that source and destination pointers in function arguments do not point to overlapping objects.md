> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=43319861) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Functions+should+validate+their+parameters?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I was thinking we needed this rule.  ;^)
Please fix up the formatting a bit (use courier fonts on function, variable names within the text.
Also please reference ISO/IEC 9899-1999 and use the same reference style as the other rules.
How did you arrive at your assessment of severity, likelihood, and remediation costs?  Off the top of my head I'm not sure I agree with these but we should discuss.
                                        Posted by rcs at Apr 03, 2007 04:16
                                     |
| You should generalize this rule to include all functions that cannot accept arguments that overlap.
                                        Posted by rcs at Apr 03, 2007 04:46
                                     |
| I think the examples above violate STR30-C. Do not attempt to modify string literals
                                        Posted by jsg at Apr 06, 2007 13:29
                                     |
| I think this example is OK.  As an array initializer, a string literal specifies the initial values of characters in an array (as well as the size of the array). This code creates a copy of the string literal in the space allocated to the character array a. The string stored in a can be safely modified.
                                        Posted by rcs at Apr 07, 2007 09:54
                                     |
| Other functions that are affected by this rule include snprintf, sscanf, mbstowcs, wcstombs, strcpy, etc.  You should do more to identify other functions that are affected.  You may want to add a second pair of compliant / non-compliant code perhaps showing some subtle problem with sscanf() or other formatted output function. 
                                        Posted by rcs at Apr 07, 2007 10:57
                                     |
| I don't really like the example for the second compliant solution because it is a very manufactured example which makes no sense in an actual program.  You may want to come up with a non-compliant / compliant pair to illustrate your point (safeguard calls to memcpy()).
Also, I don't believe the expression (ptr2 > ptr1 + 6 || ptr2 < ptr1 - 6) can always be used to determine overlap, for example, on architectures with segmented memory addressing.
                                        Posted by rcs at Apr 07, 2007 11:04
                                     |
| Dear Prof. Seacord,
I think i can add another rule to strings section which includes all the string manipulation functions such as strcpy, sscanf, etc that are affected by the rule.
                                        Posted by aarya at Apr 07, 2007 14:46
                                     |
| Keep this as one rule.  We will decide where it fits best after you are done.
                                        Posted by rcs at Apr 13, 2007 13:25
                                     |
| This rule has been re-added elsewhere and needs deletion.
                                        Posted by jpincar at Jun 01, 2007 10:24
                                     |

