[EXP45-C. Do not perform assignments in selection statements](EXP45-C_%20Do%20not%20perform%20assignments%20in%20selection%20statements) recommends against performing assignments in conditional expressions. Because of the similarity between the assignment and equality operators, such assignments often result from programmer error. To avoid accidental assignment operations when an equality comparison is intended, place constants on the left of equality comparisons.
## Noncompliant Code Example
In this noncompliant code example, the constants in each equality expression are placed as right operands to the equality operator:
``` c
while (ch == ' ' && ch == '\t' && ch == '\n') {
  /* ... */
}
```
In attempting to write the preceding code, an all-too-common syntactic error is to write the following:
``` c
while (ch = ' ' && ch == '\t' && ch == '\n') {
  /* ... */
}
```
This code, though it compiles, will cause [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) to an unsuspecting programmer. If the intent was to verify a string such as a password, user name, or group user ID, the code may produce significant [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) and require significant debugging.
Although verification may be the intended purpose, such code is almost always a case of the programmer mistakenly using the assignment operator `=` instead of the equals operator `==`. Consequently, many compilers will warn about this condition. This coding error would typically be eliminated by adherence to [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).
## Compliant Solution
In this compliant solution, the constant is placed on the left-hand side of the comparison, ensuring a compiler diagnostic at any warning level. If the programmer were to inadvertently use an assignment operator, the statement would try to assign a `ch` to a `' '` and become invalid.
``` c
while (' ' == ch && '\t' == ch && '\n' == ch) {
  /* ... */
}
```
As a result, any mistaken use of the assignment operator that could otherwise create a [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) for operations such as string verification will result in a compiler diagnostic regardless of compiler, warning level, or [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation).
Although [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels) and [EXP18-C. Do not perform assignments in conditional expressions](EXP45-C_%20Do%20not%20perform%20assignments%20in%20selection%20statements) are still applicable and promote avoidance of an assignment, the practice of placing constants on the left safeguards against a common accidental and somewhat self-disguising vulnerability.
## Risk Assessment
Errors of omission can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP21-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ECLAIR | 1.2 | CC2.EXP21 | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP21-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Likely Incorrect Expression [KOA] |
| MITRE CWE | CWE 480, Use of incorrect operator |

## Bibliography

|  |  |
| ----|----|
| [Dutta 03] | "Best Practices for Programming in C" |
| [Hatton 95] | Section 2.7.2, "Errors of Omission and Addition" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/EXP20-C.+Perform+explicit+tests+to+determine+success%2C+true+and+false%2C+and+equality?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=358) [](https://www.securecoding.cert.org/confluence/display/seccode/EXP30-C.+Do+not+depend+on+the+order+of+evaluation+for+side+effects)
## Comments:

|  |
| ----|
| Good guideline! I have been following this practice for many years and I am often surprised when others balk at such code, failing to understand the rationale for it. It is similar in spirit (and similarly underused and underappreciated) to declaring const all objects that do not change (including local variables).
On that note, I suggest to (in addition to correcting the logic error in the controlling expression) I suggest to enhance the examples by showing that the symbol on the right hand side of the equality operator is, in fact, a variable and not a constant. For instance like so:
int is_space(int ch) {
  return ch = ' ' || ch == '\t' || ch == '\n';
}

and the compliant solution to correct the logic error (**not** syntactic error as incorrectly stated in the NCCE narrative):
``` java
int is_space(int ch) {
  return ' ' == ch || '\t' == ch || '\n' == ch;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at May 12, 2010 21:35
\| \|
Should this recommendation apply to just '==' or also to other relational operators, such as '\<=', which could also experience the same "character dropping"? Should the recommendation apply to other relational operators simply out of a notion of stylistic consistency?
![](images/icons/contenttypes/comment_16.png) Posted by jimg at Feb 07, 2013 16:55
\| \|
I think this rec is mainly meant just for equality (==), because people regularly mix up == with =. The other operators are not so eaily mixed up with =.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 08, 2013 10:39
\| \|
;
[Martín Knoblauch Revuelta](https://www.securecoding.cert.org/groups?viewMemberFeed=&gid=1627067&memberID=1905163) comment in our LinkedIn forum that:
Rule EXP21-C recommends "Yoda coding", like "if (3 == x)". I understand its motivation, but I always find it weird. I just cant help it. Maybe if I train hard... Anyway, I'm not the only one finding it strange. The rest of the guide does not use it!               
my response was:
That's a reasonable observation.  We have our own requirement that all our guidelines conform with all our rules;  we would certainly like all our guidelines to conform with our recommendations as well.  I'm noodling on the possibility of 1) removing this guideline, 2) making sure all the rules conform with this guideline, 3) just leaving things the way they are.  What do folks think?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 11, 2013 13:44
\| \|
Hi, any progress on this discussion?
I got a comment from a reader of the japanese edition.
; - why other guidelines do not conform to this "Yoda" notation?
  - thinking about gcc, which can detect and raise warning for this kind of code with -Wall, it is suspicious if this hard-to-read coding practice encourages security
grepping the html sources, the guidelines I found containing "Yoda" notation in some sample code are the following,
    ENV30-C, ERR32-C, ERR33-C, FIO09-C, FIO42-C, INT05-C, INT06-C, MEM36-C, SIG31-C
I'm not sure most compilers today can warn assignments in conditional expressions, so, I believe this guideline has some value.
my personal feeling is that this recommendation should be merged to EXP45-C as one of Compliant Solution, when a conditional expression is comparison to literal constants.
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Jul 12, 2014 02:42
\| \|
We did apply this guideline in some limited cases in the rules.; I think this guideline quite definitely qualifies as a "controversial" rule since I can't get members of my own team to agree if it is a good idea or not.  Consequently, we should probably eliminate it because of our rule against avoiding controversial rules.
The next problem is that we still have to write code examples.  If there is no guideline, either Yoda-code or non-Yoda code is equally valid so it is probably OK to have examples of both.  We could use it in EXP45-C, but of course the presence or absence of Yoda code will not be what makes the solution compliant/noncompliant.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jul 13, 2014 09:00
\| \|
I don't think it should be merged into a rule due to it being controversial, but I also don't think it should be eliminated (since recommendations can be slightly more geared towards purely stylistic choices, such as API08-C).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 14, 2014 09:00
\| \|
I like the idea of merging this guideline's contents into FIO45-C. In this case 'merging' means "add a Yoda-code CS to FIO45-C, leaving the rest of FIO45-C unchanged'. ;I think our team agrees this is a good idea, we just can't require it be used everywhere (including our other secure coding rules). There are other solutions to FIO45-C, so merging this rule's contents there doesn't require anyone to adopt it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 14, 2014 13:54
\| \|
If merging means add/updating a CS (and not changing normative text), then I agree that is a good idea.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 14, 2014 15:05
\| \|
I have done this merge, and will now void this recommendation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 22, 2014 10:45
\|
