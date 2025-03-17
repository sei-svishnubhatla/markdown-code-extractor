Do not cast away a `const` qualification on an object of pointer type. Casting away the `const` qualification allows a program to modify the object referred to by the pointer, which may result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). See [undefined behavior 61](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_61) in Appendix J of the C Standard.
As an illustration, the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] provides a footnote (subclause 6.7.3, paragraph 4):
> The implementation may place a `const` object that is not volatile in a read-only region of storage. Moreover, the implementation need not allocate storage for such an object if its address is never used.

## Noncompliant Code Example
The `remove_spaces()` function in this noncompliant code example accepts a pointer to a string `str` and a string length `slen` and removes the space character from the string by shifting the remaining characters toward the front of the string. The function `remove_spaces()` is passed a `const` `char` pointer as an argument. The `const` qualification is cast away, and then the contents of the string are modified.
``` c
void remove_spaces(const char *str, size_t slen) {
  char *p = (char *)str;
  size_t i;
  for (i = 0; i < slen && str[i]; i++) {
    if (str[i] != ' ') *p++ = str[i];
  }
  *p = '\0';
}
```
## Compliant Solution
In this compliant solution, the function `remove_spaces()` is passed a non-`const` `char` pointer. The calling function must ensure that the null-terminated byte string passed to the function is not `const` by making a copy of the string or by other means.
``` c
void remove_spaces(char *str, size_t slen) {
  char *p = str;
  size_t i;
  for (i = 0; i < slen && str[i]; i++) {
    if (str[i] != ' ') *p++ = str[i];
  }
  *p = '\0';
}
```
## Noncompliant Code Example
In this noncompliant code example, the contents of the `const` `int` array `vals` are cleared by the call to `memset()`:
``` c
const int vals[3] = {3, 4, 5};
memset(vals, 0, sizeof(vals));
```
Because the `memset()` function takes a (non-`const`) pointer to `void`, the compiler must implicitly cast away `const`.
### Implementation Details
The GCC compiler issues a warning when an implicit cast is performed.
## Compliant Solution
If the intention is to allow the array values to be modified, do not declare the array as `const`:
``` c
int vals[3] = {3, 4, 5};
memset(vals, 0, sizeof(vals));
```
Otherwise, do not attempt to modify the contents of the array.
## Exceptions
**EXP05-C-EX1:** An exception to this recommendation is allowed when it is necessary to cast away `const` when invoking a legacy API that does not accept a `const` argument, provided the function does not attempt to modify the referenced variable. For example, the following code casts away the `const` qualification of `INVFNAME` in the call to the `audit_log()` function.
``` java
/* Legacy function defined elsewhere—cannot be modified */
void audit_log(char *errstr) {
  fprintf(stderr, "Error: %s.\n", errstr);
}
/* ... */
const char INVFNAME[]  = "Invalid file name.";
audit_log((char *)INVFNAME); /* EXP05-EX1 */
/* ... */
```
**EXP05-C-EX2:** A number of C standard library functions are specified to return non-`const` pointers that refer to their `const`-qualified arguments. When the actual arguments to such functions reference `const` objects, attempting to use the returned non-`const` pointers to modify the `const` objects would be a violation of [EXP40-C. Do not modify constant objects](EXP40-C_%20Do%20not%20modify%20constant%20objects) and would lead to [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). These functions are the following:

|  |  |  |  |
| ----|----|----|----|
| memchr | strchr | strpbrk | strrchr |
| strstr | strtod | strtof | strtold |
| strtol | strtoll | strtoul | strtoull |
| wmemchr | wcschr | wcspbrk | wcsrchr |
| wcsstr |  |  |  |

For instance, in following example, the function `strchr` returns an unqualified `char*` that points to the terminating null character of the constant character array `s` (which could be stored in ROM). Even though the pointer is not `const`, attempting to modify the character it points to would lead to undefined behavior.
``` java
  extern const char s[];
  char* where;
  where = strchr(s, '\0');
  /* Modifying *s is undefined */
```
Similarly, in the following example, the function `strtol` sets the unqualified `char*` pointer referenced by `end` to point just past the last successfully parsed character of the constant character array `s` (which could be stored in ROM). Even though the pointer is not `const`, attempting to modify the character it points to would lead to undefined behavior.
``` java
  extern const char s[];
  long x;
  char* end;
  x = strtol(s, &end, 0);
  /* Modifying **end is undefined */
```
**EXP05-C-EX3:** Because *`const`* means "read-only," and not "constant," it is sometimes useful to declare `struct` members as (pointer to) `const` objects to obtain diagnostics when the user tries to change them in some way other than via the functions that are specifically designed to maintain that data type. Within those functions, however, it may be necessary to strip off the `const` qualification to update those members.
## Risk Assessment
If the object is constant, the compiler may allocate storage in ROM or write-protected memory. Attempting to modify such an object may lead to a program crash or [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP05-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | pointer-qualifier-cast-constpointer-qualifier-cast-const-implicit | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP05 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.CAST.PC.CRCQ | Cast removes const qualifier |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.EXP05 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violations of this recommendation when the -Wcast-qual flag is used |
| Helix QAC | 2024.4 | C0311, C0431 |  |
| LDRA tool suite | 9.7.1 | 203 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP05-a | A cast shall not remove any 'const' or 'volatile' qualification from the type of a pointer or reference |
| PC-lint Plus | 1.4 | 9005 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP05-C | Checks for cast to pointer that removes const qualification (rec. fully supported) |
| RuleChecker | 24.04 | pointer-qualifier-cast-constpointer-qualifier-cast-const-implicit | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP05-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | EXP55-CPP. Do not access a cv-qualified object through a cv-unqualified type |
| ISO/IEC TR 24772:2013 | Pointer Casting and Pointer Type Changes [HFC]Type System [IHN] |
| MISRA C:2012 | Rule 11.8 (required) |
| MITRE CWE | CWE-704, Incorrect type conversion or cast |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.7.3, "Type Qualifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152053) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152149)
## Comments:

|  |
| ----|
| This is a far harder problem to remediate than is suggested here: all of us will agree that you should not modify data that is *actually* constant, but it's so common to deal with library code written by others that doesn't properly qualify its parameters (even though they are known not to modify the pointed-to data) that one cannot always fix this without diving into the libraries bigtime *or* casting away the const.
Example: I made a serious pass over the Net::SNMP libraries some years ago to properly const qualify parameters to dozens and dozens of functions, and even though the patches were accepted by the project, portable code can't assume everybody is always and forever using a modern version (though I suppose that *secure* code might demand more modern versions, though not for this reason).
One must be very aggressive about properly const-qualifying one's own code so as not to foist this nastiness on others.
                                        Posted by steve at Mar 13, 2008 21:22
                                     |
| We do assume C99 as described in Scope (complete with rationale).
The only indication we provide of how hard a problem is, is in the remediation cost.  I've modified this from medium to hard based on your comment.  Unfortunately, this reduces the priority of applying the recommendation (because it makes more sense to fix problems that are easier to fix, but which have the same severity and likelihood).
                                        Posted by rcs at Mar 16, 2008 11:13
                                     |
| It's actually a semantic violation (undefined behavior);to attempt to modify an object declared with const qualification.
As to casting away const-ness in other contexts, usually it's a mistake, but not always.  Because "const" just means "read-only", not "constant", it is sometimes useful to declare some struct members as (pointer to) const objects in order to obtain diagnostics when the user tries to change them in some way other than via the functions that are specifically designed to maintain that data type.  Within those functions, however, it will probably be necessary to strip off the const qualification in order to update those members.
                                        Posted by dagwyn at Apr 15, 2008 14:33
                                     |
| (Edit: Part of this comment is nonsense as David points out - I was confusing two of your rules.  Leaving it all behind for reference, and overstriking some.)
The text says "Casting away the const qualification allows violation of rule EXP31-C. Do not modify constant values prohibiting the modification of constant values."
Not true.  Consider:
char buf-10;-
const char *ptr = buf;
strcpy((char *)ptr, "abcd");
It is the buf array which is being modified, and buf is not a constant value.
This is legal in C.  Whether you can modify an object depends on whether that
object is defined as const, not on whether some pointer to it has a const*.
This rule in practice contradicts DCL00-A "Declare immutable values using enum or const".
(Which I think is a bad rule anyway.  I'll go there to go on about that a bit.)
I think the various rules about const need to be consolidated into a more careful
discussion about when to constify.
To const or not to const is a problem even when there is no library API you need to
stay compliant with.
You may e.g. have some data structure which is read-only to most of the program, but
is written by a the few functions that maintain it.  It may make sense to declare parts
of it const, and cast away const in the maintainer funcions.
Also, consider how you would define a function like strchr().  It can take both a
it can take a char* or const char*.  A user passing a const char* value should not
have to cast away const in the argument.  A user passing a char* value should not
have to cast away const in the return value.  Thus your function should do just
what strchr does - take a const * argument, and cast away const in it.
(argh, 2 edits to get the example right [even before David's reply] - I'm getting tired...)
                                        Posted by hbf at Apr 17, 2008 18:08
                                     |
| Your comment from DCL00-A is a precise interpration, const really means 'read-only in this scope'. It does not restrict you from modifying the data from some other scope, or from a non-const pointer.
I'm not sure what your example code is trying to prove, since you are explicitly casting away const. 
You would const static data only if the program never modifies it...if it is modified in one location only, it's not constant, now, is it?
You can const function arguments, but that doesn't mean the arg's data can't change, it only means the function promises not to change the data via that arg. The data is still changeable via another arg, or an aliasesd pointer, and the const-ness goes away once the function's done. So the fact that strchr() takes a const char* doesn't mean you can only pass it const data, it only means strchr() promises not to modify it.
                                        Posted by svoboda at Apr 18, 2008 09:55
                                     |
| Right, that was confused.  You are not getting it right either though.  Const does not mean 'read-only in this scope' either:
A function argument like "const int *arg" is not a promise the function won't change *arg, aliasing or no aliasing.  All it promises is that the compiler will be rude if the function tries to change *arg or *(variable derived from arg) without casting away const at some point.  Well, there are some escapes the compiler need not catch, like *(int **)(void *)&arg or (int *)(intptr_t)arg, or copying the pointer with memcpy.
OTOH if an object is created as const, that means it's immutable - or rather, since the implementation need not enforce that, it means an attempt to modify it yields undefined behavior.
                                        Posted by hbf at Apr 21, 2008 12:37
                                     |
| As Douglas A. Gwyn notes above, casting away a const qualification from a pointer isn't necessarily problematic in and of itself. It's modifying an object declared const after the cast that may lead to undefined behavior. Thus, in addition to this recommendation I suggest that there ought to be a rule prohibiting the modification of const objects, analogous to EXP32-C. Do not access a volatile object through a non-volatile reference:
Do not modify a const object through a non-const reference
Both of the non-compliant examples on this page are actually violations of this (yet to be created) rule.
                                        Posted by martinsebor at Jan 09, 2010 20:35
                                     |
| Sounds OK to me.  I thought what Doug was saying was that there was another valid exception to this guideline (which I added as an exception to this guideline).
Do you want to create the new rule or do you want me to?  Looks like copy/paste this one and then make some modifications.
Don't the NCE/CS pairs here also violate this recommendation, or do you think this should only apply to explicit casts?
You may be able to shorten the title to "Do not modify a const object".  How it is done is irrelevant, right?
You may also be able to cannibalize this rule EXP40-C. Do not modify constant values that ended up in the void.  
                                        Posted by rcs_mgr at Jan 09, 2010 21:06
                                     |
| Yes, the examples here apply to both this guideline and the one I'm proposing to add.
I'd be happy to add a new rule or resuscitate EXP40-C. Do not modify constant values. If I understand correctly, the main objection to that rule was the example(s) which demonstrated a violation of EXP05-C. Do not cast away a const qualification rather than the actual modification of constant objects.
After re-reading the examples in the rule I realize that the non-compliant example does, in fact, modify a const object and the objections were actually based on a particular compiler not diagnosing such modification and generating code that ran without suffering any adverse consequences of the undefined behavior. I don't think such objections are grounds for a dismissal of an otherwise valid rule. Compilers are free to provide well-defined semantics in cases where the standard leaves the behavior undefined. Unless the compiler documents this behavior, it is still undefined and may change as a result of compiler options. In addition, other compilers (on the same or other operating systems or hardware architectures) may generate code that will exhibit undefined behavior.
                                        Posted by martinsebor at Jan 12, 2010 15:56
                                     |
| I actually wrote that rule and never quite understood the objections to it, although alot of folks did seem to find some fault.
The non-compliant code example is right out of C99.  I was surprised when I compiled it with whatever version of MSVS I had on my desktop and it compiled straight away w/o warning and successfully modified the constant.  I reported this as a defect to Microsoft to diagnose the problem so newer versions of MSVS should work fine.  
Long story short, I think perhaps you can revive it.
                                        Posted by rcs_mgr at Jan 12, 2010 18:32
                                     |
| Done: EXP40-C. Do not modify constant values is back.
                                        Posted by martinsebor at Jun 05, 2010 19:44
                                     |

