> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This page has been merged into guideline [MSC09-C. Character encoding: Use subset of ASCII for safety](MSC09-C_%20Character%20encoding_%20Use%20subset%20of%20ASCII%20for%20safety). This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Define+numeric+constants+in+a+portable+way?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Is this a case where "white listing" would be preferred? Rather than saying what characters are bad, should we say what characters are good?
Also don't forget that we're rapidly moving into the era of Unicode and that many Unicode characters can cause user confusion if not outright security problems. Though I know of no file system whose default is to assume Unicode file names, but we're on the verge of that becoming the norm.
                                        Posted by wlf@cert.org at May 14, 2007 11:30
                                     |
| This seems like a specific case of:
MSC09-A. Character Encoding - Use Subset of ASCII for Safety
Do we really need this article?
And in any case, I agree, white-listing is a much better approach for this.
                                        Posted by jpincar at May 29, 2007 13:38
                                     |

