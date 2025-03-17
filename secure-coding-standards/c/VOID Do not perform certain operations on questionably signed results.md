> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=534) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+return+from+SIGFPE+from+inside+a+signal+handler?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Another tricky point that should deserve a mention are comparisons of operands differing in signedness.  The following program prints out 0, meaning that a negative int is not considered smaller than a positive unsigned int.
int main(void)
{
        int x = -1;
        unsigned y = 1;
        printf("%d\n", x < y);
        return 0;
}

![](images/icons/contenttypes/comment_16.png) Posted by zvrba at Mar 31, 2008 12:28
\| \|
The introduction (and maybe even the C Rationale) is confusing at best, perhaps wrong.; In general, signed integer overflow produces undefined behavior.  The cited rules seem to pertain only to conversions.
I suggest dropping this rule.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 17:00
\| \|
I've mirrored your comment under INT02-A...it is also appropriate there.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 21, 2008 15:25
\| \|
We should keep this rule; it does address a unique condition (which is, admittedly, a specific problem wrt conversion). INT02-A handles conversion in general, but that's a recommendation, not a rule, so it is weaker than the condition that necessitates this rule.
I do agree that the intro & rationale are confusing and require elucidation. Not sure how to improve the example given, but one good idea: add Zeljko's bad code example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 21, 2008 15:44
\| \|
Your code sample is now in INT02-A.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2008 15:18
\| \|
You seem to be misunderstanding the Rationale. The ambiguity is between "unsigned preserving" rules and "value preserving" rules. That was a problem when choosing which of these rule sets to standardize, because both were in use for K&R C. ANSI (and thus ISO) C picked one them, so this code is not ambiguous in ISO C.; Not in the sense the Rationale means here, anyway.
Note also that this rule starts talking about expressions which signed integer overflow, which yields undefined behavior anyway.
It's true that the sign of an integer expression can depend on the implementation's integer type sizes, and this is a problem, but you seem to cover that under INT02-A.
This rule needs to be dropped or totally rewritten.
Note also that it's often impractical to obey rules that require programs to cater to any valid integer type and representation.  For example, unsuffixed hex constants larger than 0x7fff can be either signed or unsigned depending on integer sizes.  But there is so much code out there which assumes two's complement int at least  32 bits wide that the reasonable fix for much of it can be to refuse to compile on a host with other ints.  Fixing it can be too much work for a possibly non-existent gain.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 23, 2008 09:42
\| \|
OK, after studying the rationale and the C99 standard for most of the morning, I think the following (which I believe concurs with your statements).
What this rule is covering is ultimately covered in INT02-A, since the error involves narrowing unsigned ints to signed ints. If an unsigned integer's value cannot fit in the corresponding signed type, the result is undefined, hence best avoided.
However, INT02-A is a recommendation, not a rule, and so its 'enforceability' is weaker than this rule. So a rule that cites a specific subset of integer conversion problems is still a worthwhile goal.
But this rule currently does not meet that goal, simply because it is complex and confusing (mostly because the standard and rationale are also complex).
The ambiguity between 'unsigned preserving' rules vs 'value preserving' rules was resolved by the standard, which we are basing these rules on. But even though the standard resolves the ambiguity, the point of this rule is: it is still best to avoid the ambiguity, if only to appease those hapless programmers who have not read the standard.
In conclusion, if the preserving ambiguity can be expressed more concisely as a rule, we should do so. But I suspect it can't, and so we may be better off letting INT02-A's general warning of understanding the nuances of integer conversion suffice for this issue.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 23, 2008 13:51
\| \|
The value-preserving rules were chosen for being safer for novices, as the Rationale points out. The relevant "hapless programmers who have not read the standard" would be K&R C programmers who are almost 2 decades out of touch, and who didn't write portable programs back then either (since there was an ambiguity back then). I'm getting the impression that someone has scavenged the Standard and Rationale for apparent security problems, without having experience with or understanding of whether they really are security problems.
Signed vs unsigned, and in particular "signed meets unsigned", *is* a bad enough problem that it may warrant a separate recommendation or rule, but this obsolete ambiguity is not. As I said above I think it'd be impractical for many programs to obey such a rule though, because they make assumptions about integer types.
Actually much code which had a problem with this ambiguity can have a problem due to different integer sizes too. E.g. "EOF \< (unsigned char)ch" can be false - if sizeof(int) == 1, which is allowed at least on freestanding implementations. Do you want a rule which forbids comparing an unsigned char with int-variables? A *lot* of programs just ignore such problems. Google one of Chris Torek's rants about value preserving vs unsigned preserving rules on comp.lang.c.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Apr 23, 2008 17:22
\|
