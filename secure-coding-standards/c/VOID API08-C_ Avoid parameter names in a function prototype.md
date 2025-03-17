Naming the parameters in a prototype declaration should never be necessary, and is often unwise, because these names can be affected by macro definitions.
Although the scope of an identifier in a function prototype begins at its declaration and ends at the end of that function's declarator, this scope is ignored by the preprocessor. Consequently, an identifier in a prototype having the same name as that of an existing macro is treated as an invocation of that macro.
Safeguarding parameter names is particularly critical in standard and system headers where the user expects to be able to include the header and have only the function names visible.
## Noncompliant Code Example
This noncompliant code example,
``` c
#define status 23
void update_status(int status);
```
generates an error, because the prototype, after preprocessing, becomes
``` c
void update_status(int 23);
```
Perhaps more surprising is what happens if status is defined:
``` c
#define status []
```
Then the resulting prototype is
``` c
void update_status(int []);
```
which is syntactically correct but semantically quite different from the intent.
## Compliant Solution
To protect an API's header prototypes from such misinterpretation, the developer must write them to avoid these surprises. Possible solutions include not using identifiers in prototypes, as in this example:
``` c
void update_status(int);
```
Another solution is to comment them out, as in this example:
``` c
void update_status(int /* status */);
```
Comments are converted to a single whitespace character in translation phase two.
## Risk Assessment
Failure to protect header prototypes from misinterpretation can result in type errors in the program.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API08-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | named-declaration-parameter | Fully checked |
| ECLAIR | 1.2 | CC2.API08 | Fully implemented |
| RuleChecker | 24.04 | named-declaration-parameter | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+API08-C).
## Bibliography

|  |
| ----|
| [C99 Rationale 2003] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152337) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152226)
## Comments:

|  |
| ----|
| Doesn't this conflict with API05-C ("Use conformant array parameters")?
                                        Posted by nemequ at Mar 06, 2014 03:17
                                     |
| With regards to C++, isn't the violation in the "Noncompliant code" examples the defining of a macro, in violation of;PRE00-CPP. "Avoid defining macros"? This seems to be the general consensus of the C++ ISO (e.g. Preprocessor is evil)Bjarne Stroustrup's 2014 "A Tour of C++" contains many examples with parameter names in a function prototype, as do many other ISO and non-ISO examples (e.g. Section 2.4 of the ISO's Tour, or see "Declaring Functions" in this Function tutuorial).Would it be preferable to limit this advise to C by tagging this recommendation as "not-for-cpp"? 
                                        Posted by brian.szuter at Oct 31, 2014 10:02
                                     |
| Technically, this also violates;PRE00-C. Prefer inline or static functions to function-like macros as well.I don't believe this recommendation makes sense given the number of places identifiers are used where they cannot be elided, such as struct names, local variables, types, etc. I think this puts the burden on the wrong place – the recommendation should be to not write macros that will conflict with other identifiers, especially since macros are idem non grata. For instance, by recommending all macro names be in all caps, and other identifiers not be in all caps.C++ adds to the list of places where identifiers are required, such as template parameter lists, class base specifier lists, exception handler parameter lists, lambda parameter lists, etc, so this recommendation can't really apply in C++ without some work, which is why I am adding the not-for-cpp label.
                                        Posted by aballman at Oct 31, 2014 11:42
                                     |
| Technically API05-C. Use conformant array parameters;violates this recommendation. That's OK, because they are both recommendations and not hard-and-fast rules.
                                        Posted by svoboda at Oct 31, 2014 16:02
                                     |
| I think the NCCE meant to say something like "Suppose status is a macro with the following value, and you can't change it (though it violates several CERT rules and lots of convention). Then the following code does not mean what you think it means".I agree with Aaron...this rule should not exist; the fault lies with the macro, not with the function.AFAICT this is the same in both C++ and C, even if the C++ community is more against macros than C.
                                        Posted by svoboda at Oct 31, 2014 16:07
                                     |
| This recommendation has high cost and low benefit. This reduces the readability of all function prototypes, thus increasing the chance of errors by API consumers. This only has benefit when macros are misused (and thus has zero benefit in good quality code). This rule;is more likely to reduce security (due to API usage errors) than to increase it. I concur with others who believe this recommendation should be removed.
                                        Posted by chris.newman at Jun 04, 2015 12:36
                                     |
| The recommendation is useful for avoiding situations where an incorrect program can be compiled:jheadland@LT-02296 ~/C
$ cat define.c
void f(char *status);
void g(void)
{
; char *x[] = {
    "hello",
    "world"
  };
  f(x); /* this should fail, argument type is wrong */
}
jheadland@LT-02296 ~/C
$ gcc -c define.c
define.c: In function ‘g’:
define.c:9:5: warning: passing argument 1 of ‘f’ from incompatible pointer type [-Wincompatible-pointer-types]
    9 |   f(x);
      |     ^
      |     |
      |     char **
define.c:1:14: note: expected ‘char *’ but argument is of type ‘char **’
    1 | void f(char *status);
      |        ~~~~~~^~~~~~
jheadland@LT-02296 ~/C
$ gcc -Dstatus=[] -c define.c
jheadland@LT-02296 ~/C

![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 17, 2020 06:29
\| \|
What does this have to do with not using the parameter name in a function prototype?
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 17, 2020 07:04
\| \|
In the first line of;`define.c`, a function prototype employing a parameter name, namely `status`, is used.
Because this unnecessary lexeme is used, the program is vulnerable to the misfortune demonstrated, where the precompiler's replacement of the name `status` with a pair of squared brackets causes an incorrect program to compile, leading to undefined behaviour when its object code gets linked together with the code implementing function `f()`.
Many of the previous comments on this recommendation are critical of it, and I was thereby motivated to seek an example of why this recommendation was made.  I suppose that's an implicit criticism of the sparseness of the examples in the recommendation's body.
I should probably have explained that better, rather than just posting the use case.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 17, 2020 07:22
\| \|
Oh! Thank you for the explanation –;I didn't notice the -Dstatus on the command line in the last part of your example, now the code makes more sense. 
That said, I still think this recommendation causes more active harm than it does good and I think the recommendation should be scrapped entirely. For instance, static analysis tools make use of the parameter identifiers for performing analysis that points out real flaws in programs (consider a tool checking for swapped arguments at call sites where the parameter names give critical semantic information to the analysis as an example). Most importantly: parameter names are part of the interface's documentation and convey important information to the user (and that information may be displayed by tools such as code editors showing autocomplete choices, etc).
It's not that the issues the recommendation tries to address aren't possible, it's that they often result in obvious compilation issues unless the circumstances are carefully crafted. It's just not a common enough problem to throw the baby out with the bathwater over in terms of API usability.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 17, 2020 07:38
\| \|
Since the way you fix VLAs is much less obvious than other parameters, we should mention them in particular. We should add `void f(int rows, int cols, int data[rows][cols]);` as a non-compliant example, and `void f(int, int, int [*][*]);` as the corresponding compliant example.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 13:18
\| \|
I still contend that this recommendation is an anti-pattern and the entire rec should be scrapped because the advice given produces far more problems than the recommendation is capable of solving.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 30, 2020 13:29
\| \|
Sigh. I last studied this recommendation in 2014 and noted its problems. Since it was still evolving, I assumed it would "grow up" to become a valuable recommendation. That hasn't happened yet, so I'm removing it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 06, 2020 11:14
\|
