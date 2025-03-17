Prefer type definitions (`typedef`) to macro definitions (`#define`) when encoding types. Type definitions obey scope rules; macro definitions do not. textual substitution is inferior to using the type system. While type definitions for non-pointer types have similar advantages \[[Summit 2005](AA.-Bibliography_87152170.html#AA.Bibliography-Summit05)\], can make it more difficult to write `const`-correct code (see [DCL05-C. Use typedefs of non-pointer types only](https://www.securecoding.cert.org/confluence/display/c/DCL05-C.+Use+typedefs+of+non-pointer+types+only)).
## Noncompliant Code Example
In this noncompliant code example, `s1` is declared as `char *`, but `s2` is declared as a `char`, which is probably not what the programmer intended:
``` java
#define cstring char *
cstring s1, s2;
```
This noncompliant code example also violates  [DCL04-C. Do not declare more than one variable per declaration](https://wiki.sei.cmu.edu/confluence/display/c/DCL04-C.+Do+not+declare+more+than+one+variable+per+declaration).
## Compliant Solution
In this compliant solution, both  `s1`  and  `s2`  are declared as  `char *`:
``` java
typedef char * cstring;
cstring s1;
cstring s2;
```
The compliant solution violates [DCL05-C. Use typedefs of non-pointer types only](https://wiki.sei.cmu.edu/confluence/display/c/DCL05-C.+Use+typedefs+of+non-pointer+types+only), but effectively demonstrates the difference between type definitions and macro replacements.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE03-C | Low | Unlikely | Medium |  P2  |  L3  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-PRE03 |  |
| ECLAIR | 1.2 | CC2.PRE03 | Fully implemented |
| Helix QAC | 2024.4 | C3413 |  |
| LDRA tool suite | 9.7.1 | 79 S | Enhanced Enforcement |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID PRE03-CPP. Prefer typedefs to defines for encoding types |
| ISO/IEC TR 24772:2013 | Pre-processor Directives [NMP] |

## Bibliography

|  |  |
| ----|----|
| [Saks 1999] |  |
| [Summit 2005] | Question 1.13 Question 11.11 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152384) [](../c/Rec_%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152186)
## Comments:

|  |
| ----|
| This might be enforceable by a static analyzer that could parse macro definitions and see that they refer to a valid typedef. ROSE can't currently do this, so we don't know how effective or difficult this would be.
                                        Posted by svoboda at Jul 07, 2008 15:35
                                     |
| in
typedef char *NTCS;
const NTCS p = &data;
Isn't p a "pointer to a const char" not "a constant pointer to char"?
                                        Posted by masaki at Apr 07, 2009 03:21
                                     |
| No, p is a const pointer to char. If the code had used a macro instead of a typedef:
#define NTCS char*
const NTCS p = &data;

Then p would be a pointer to a const char. The upshot is that typedefs are treated differently than macros (which is the focus of this rule.)
These code snippets should prob be examples in the rule as well, although I'm not sure that one is 'noncompliant' while the other is 'compliant'.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 07, 2009 10:34
\| \|
While I agree with this rule in principle, in my opinion using a `typedef` for `char*` or any other pointer type is ill-advised because:
-   applying the `const` or `volatile` qualifiers to the `typedef` has an unexpected effect (as mentioned in second paragraph of the recommendation and evidenced by the comment by [Masaki Kubo](https://wiki.sei.cmu.edu/confluence/display/~masaki) above)
-   doing so makes it difficult to see, at a glance, that the name refers to a pointer rather than an ordinary type
Both of these issues can lead to subtle and difficult to diagnose bugs. For example:
``` java
typedef char *cstring;
void f(cstring s) { s[0] = '\0'; }
void g(const char *s) {
    f(s);   // diagnostic: call discards const qualifier
}
// programmer misunderstood rules, thinks const cstring
// is the same as const char*
void h(const cstring s) {
    f(s);   // whoops! s modified, no diagnostic issued
}
```
Perhaps instead of using examples involving pointers it might be better to use structs instead. I.e., instead of the following non-compliant solution:
``` java
struct some_struct_tag { /* ... */ };
#define some_struct struct some_struct_tag
```
use the following compliant solution:
``` java
struct some_struct_tag { /* ... */ };
typedef struct some_struct_tag some_struct;
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 06, 2009 23:38
\| \|
The problem with using typedefs on pointers is more the confusion between
``` java
const char* s;
```
and
``` java
char* const s;
```
Perhaps we need a rule about that, but it should be distinct from this rule.
If you read it in English, cstring is a pointer to char, and so const cstring is a const pointer to char. Then the compiler's behavior on your code samples becomes obvious. (The tricky one is 'const char\*' which is 'a pointer to const char'.
Furthermore, your suggestion of using structs for the NCCE/CCE fail, because macros and typedefs behave the same (both are accepted by the compiler:
``` java
struct some_struct_tag { /* ... */ };
#define some_struct1 struct some_struct_tag
typedef struct some_struct_tag some_struct2;
some_struct1 ss11, ss12;
some_struct2 ss21, ss22;
```
OTOH I'm not enamored of this rule, as the NCCE violates DCL04. Unless we can find a NCCE that does not violate another rule, I'm not sure this rule should live on in its current form. Perhaps it should die, or be replaced by the "const char\* vs char\* const" rule suggested above. What do you think?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 07, 2009 10:58
\| \|
I think the rule is sound and worthwhile as is. My objection is only to the the code examples. Incidentally, as I just noted in a comment [Re: API03-C. Create consistent interfaces and capabilities across related functions](https://www.securecoding.cert.org/confluence/display/seccode/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions?focusedCommentId=40075401#comment-40075401), the problem with using typedefs for pointers is exemplified in the interfaces of The Managed String Library \[[Burch 06](AA.-Bibliography_87152170.html#AA.Bibliography-Burch06)\].
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 06, 2010 16:40
\| \|
After thinking about this as well as first hand experiencing the same design flaw as the one that affects The Managed String Library discussed above, I'd like to change this guideline to:
-   use something like `unsigned char` or `long double` as an example where `typedef` may be called for, e.g., instead of
    ``` java
    #define UCHAR unsigned char
    ```
    use:
    ``` java
    typedef unsigned char UChar;
    ```
    with a rationale analogous to that given in [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros), namely that textual substitution is inferior to using the type system, and
-   either as an exception to this guideline, or in a guideline of its own, recommend against using `typedef` for pointers and give the interface of the Managed String Library as a Noncompliant Code Example.
If no one objects I'll go ahead and make these changes.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 19, 2010 23:27
\| \|
no objections from me. I'm thinking the pointers should be given as an exception to this rule, because otherwise the two rules would contradict each other. You could also build it right into the title,e.g.:
PRE03-C. Prefer typedefs to defines for encoding types other than pointers
In this case, rather than exception you could provide a NCE using the managed string library and then showed the preferred solution. After that, I should probably go back and fix the library. 8^(
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 20, 2010 13:13
\| \|
I would like to remove the DCL05-C issue with the CCE, but am struggling to come up with a compelling code example.; It would be trivial to use:
``` java
#define foo unsigned long
foo f;
```
But the existing code example is better at showing the dangers of using the macro over the typedef.  Ideas welcome!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 25, 2013 14:07
\| \|
Well, to comply with DCL05-C, you prob should limit this rule to not apply to pointers. You could make a NCCE involving structs or unionts or arrays. And it could involve pointers (just not a toplevel pointer such as it has now)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 25, 2013 15:12
\| \|
This is not confusing at all. An personally I prefer putting **const** storage class specifier on the right of type.What typedef does, unlike #define that only expands the text, is to make a type alias.
So consider that :
**const NTCS p;**
is equivalent to
**NTSC const p;;**
The latter one is much more consistent ans easy to understand and will never cause confusion as read as "const pointer to char".
![](images/icons/contenttypes/comment_16.png) Posted by jeffreybian at Jul 03, 2013 15:50
\| \|
If NTCS is not a pointer type, then it doesn't matter where you put the const. If it is a pointer type, then it does matter. Putting the const after it renders the pointer const, but not the pointed-to data. Likewise, putting the const before NTCS renders the pointed-to-data const (it can't be changed by the pointer) but the pointer itself could be changed to point somewhere else.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 03, 2013 16:13
\| \|
Yup. I was referring to the specific case above (typedef char \* NTSC).
I mean by always having const storage class on right to the type, it will help enhance the readability and reduce the confusion, especially in production quality code. It also makes an obviously tip that : const storage class decorates the closest type left to it.
;
![](images/icons/contenttypes/comment_16.png) Posted by jeffreybian at Jul 03, 2013 16:39
\| \|
Is it necessary to split the CS into:
``` cpp
cstring s1;
cstring s2;
```
Testing under gcc 4.6.3, I got the correct result with just:
``` cpp
cstring s1, s2;
```
While this violates DCL04-C, I think that this better demonstrates the differences between typedef and #define behavior since it more closely mirrors the NCCS. As it is, the correct behavior of the CS could be incorrectly attributed to the declarations being on separate lines.
![](images/icons/contenttypes/comment_16.png) Posted by jloo at Jan 15, 2014 12:41
\| \|
It is not strictly necessary to split the CS into multiple lines.
We try to ensure all of our coding examples (especically CSes) comply with our rules and recommendations. Since it would violate;[DCL04-C. Do not declare more than one variable per declaration](DCL04-C_%20Do%20not%20declare%20more%20than%20one%20variable%20per%20declaration), it was likely written that way.
However, you do bring up a good point that the problem in the NCCE could also be solved in exactly the same way (splitting up the declarations). I'm on the fence as to whether the problem here is with the NCCE's formatting (esp since it violates more than one guideline) or the CS, or the example as a whole.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jan 15, 2014 13:00
\| \|
There are 2 non-compliant code examples.
;\* The first code example does not even compile.
 \* The description of the second code example is "I don't actually know what is wrong with this"
In my humble opinion those problems should be fixed.
A better description in the second code example would imho be "The macro below can be replaced with a typedef".
![](images/icons/contenttypes/comment_16.png) Posted by dmarjamäk at Dec 15, 2024 10:09
\| \|
Thanks for the catch. I trawled through the history to see if this recommendation ever had good code examples. And I found it, from back in 2014. So I replaced the current code examples with the good ones.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 17, 2024 10:44
\| \|
that is a really good example however the rule text explicitly says "non-pointer types".
but I like the example it's a real oopsie. :-)
![](images/icons/contenttypes/comment_16.png) Posted by dmarjamäk at Dec 18, 2024 03:48
\| \|
Since the code example is technically out-of-scope for this recommendation, and since we haven't been able to come up with other noncompliant code examples for this recommendation, we have decided to delete it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 19, 2024 08:40
\|
