Many functions return useful values whether or not the function has side effects. In most cases, this value is used to signify whether the function successfully completed its task or if some error occurred (see [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators)). Other times, the value is the result of some computation and is an integral part of the function's API.
Subclause 6.8.3 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] states:
> The expression in an expression statement is evaluated as a void expression for its side effects.

All expression statements, such as function calls with an ignored value, are implicitly cast to `void`. Because a return value often contains important information about possible errors, it should always be checked; otherwise, the cast should be made explicit to signify programmer intent. If a function returns no meaningful value, it should be declared with return type `void`.
This recommendation encompasses [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors). Unlike this recommendation, that rule is restricted to functions from the Standard C library.
Compliance with this recommendation is required in order to comply with [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](ERR00-C_%20Adopt%20and%20implement%20a%20consistent%20and%20comprehensive%20error-handling%20policy)
## Noncompliant Code Example
The `asprintf()` function has been provided by the GNU C library. It works like `sprintf()`, but if given a null pointer as the destination string, it will create a buffer sufficient to hold the resulting string. It relies on `malloc()` to allocate the buffer. If `malloc()` fails, then `asprintf()` returns a negative number.
This noncompliant code example calls `asprintf(),` but fails to check whether the string was successfully created.
``` c
void func(char* name) {
  char* s = NULL;
  asprintf(&s,"Hello, %s!\n", name);
  (void) puts(s);
  free(s);
}
```
## Compliant Solution
This compliant solution checks to make sure no error occurred.
``` c
void func(char* name) {
  char* s = NULL;
  if (asprintf(&s,"Hello, %s!\n", name) < 0) {
    /* Handle error */
  }
  (void) puts(s);
  free(s);
} 
```
## Exceptions
**EXP12-C-EX1:** If the return value is inconsequential or if any errors can be safely ignored, such as for functions called because of their side effects, the function should be explicitly cast to `void` to signify programmer intent. For an example of this exception, see "Compliant Solution (Remove Existing Destination File)" under the section "Portable Behavior" in [FIO10-C. Take care when using the rename() function](FIO10-C_%20Take%20care%20when%20using%20the%20rename__%20function), or Exception **ERR33-C-EX1** in [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors).
**EXP12-C-EX2:** If a function cannot fail or if the return value cannot signify an error condition, the return value may be ignored. Such functions should be added to a whitelist when automatic checkers are used.
``` c
strcpy(dst, src);
```
## Risk Assessment
Failure to handle error codes or other values returned by functions can lead to incorrect program flow and violations of data integrity.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP12-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | error-information-unusederror-information-unused-computed | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP12 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.FUNCS.IRV | Ignored return value |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | CHECKED_RETURN | Finds inconsistencies in how function call return values are handled. Coverity Prevent cannot discover all violations of this recommendation, so further verification is necessary |
| Cppcheck | ; 2.15 | leakReturnValNotUsed, ignoredReturnValue | Return value of memory allocation function is not used.Ignored return value from function when configuration says it must be used. See the chapter "Library configuration" in the cppcheck manual |
| ECLAIR | 1.2 | CC2.EXP12 | Fully implemented |
| Helix QAC | 2024.4 | C3200 |  |
| Klocwork | 2024.4 | MISRA.FUNC.UNUSEDRET.2012SV.RVT.RETVAL_NOTTESTED |  |
| LDRA tool suite | 9.7.1 | 382 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP12-aCERT_C-EXP12-b | The value returned by a function having non-void return type shall be usedThe value returned by a function having non-void return type shall be used |
| PC-lint Plus | 1.4 | 534 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP12-C | Checks for situations where returned value of a sensitive function is not checked (rec. fully covered) |
| PVS-Studio | 7.35 | V530, V698, V757, V797 |  |
| RuleChecker | 24.04 | error-information-unused | Partially checked |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP12-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP12-CPP. Do not ignore values returned by functions or methods |
| CERT Oracle Secure Coding Standard for Java | EXP00-J. Do not ignore values returned by methods |
| ISO/IEC TR 24772:2013 | Passing Parameters and Return Values [CSJ] |
| MITRE CWE | CWE-754, Improper check for unusual or exceptional conditions |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.8.3, "Expression and Null Statements" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152352) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152264)
## Comments:

|  |
| ----|
| Yes, OK.  How many of our compliant solutions do you suppose fail to comply with this recommendation?
Also, if you write a checker for this will you get tons of true positives, but these are very low value true positives and will contribute quite alot to an adverse signal to noise ratio.
I wonder if we could replace with this recommendation with more recommendations to check return values from functions?  If something is not on the list (like strcpy() it is not necessary to check the return status or cast to void.
                                        Posted by rcs_mgr at Jun 24, 2008 20:05
                                     |
| splint says:
10 violations in 61 CCEs
7  violations in 77 NCCEs
I'd say this kind of recommendation is not very useful on legacy code because of the signal to noise issue you mention. But if you write your code and remember to cast to void when you are not checking your return value, a violation is almost certainly a bug.
Would it make you happy if we mentioned the possibility of a white/black list for automatic checkers?
                                        Posted by avolkovi at Jun 25, 2008 09:16
                                     |
| Sort of.  We have an example where we cast a call to remove() to void, which makes perfect sense to me, because normally you would want to check the return status.  There are a number of functions, such as string functions that only return a copy of the string so you can nest the function calls, where it is not unusual or bad practice IMHO to ignore the return value.
I guess I would be happier with this rule if we provided our own white list of functions that are excepted.  This would be one class of exception.  Maybe we could use the remove() example for EXP12-EX1 as an eample of a return value that is inconsequential.
                                        Posted by rcs at Jun 25, 2008 09:59
                                     |
| done, added a new exception for white lists
                                        Posted by avolkovi at Jun 25, 2008 10:26
                                     |
| In the first paragraph, what do you mean by "necessary output"?, necessary for what?
                                        Posted by masaki at Apr 24, 2009 02:20
                                     |
| I'd guess the output is necessary in order to fulfill the API. For instance, strlen returns a size_t which is critical to its API. Rewrote the paragraph; hopefully its clearer now.
                                        Posted by svoboda at Apr 24, 2009 08:58
                                     |
| I am getting a coverity error named CHECKED_RETURN although
I have checked the return value, I am not sure why coverity tool
throw this error.
Both of functions are given below.
The false statement used for func1 is defined as
#ifndef true
#define true 1
#endif
#ifndef false
#define false 0
bool func1(int*pointer)
{
   bool r = false;
   r = func2()
   if(r == false)
Unknown macro: {         return r;        r = func3();    return r;
} 
The FALSE & TRUE value has been considered from given enum
typedef enum {
    FALSE = 0,
    TRUE = 1
} bool_t;
bool_t func2()
{
        if(fun4()){
                 return FALSE;
 if(func5())
Unknown macro: {                  return TRUE;
} 
Coverity ERROR:
unchecked_value: Return value of func2() is not checked
can any body suggest why coverity error is observed
                                        Posted by nikki at Jun 18, 2010 02:53
                                     |
| ERR00-C. Adopt and implement a consistent and comprehensive error-handling policyThis page is not found
                                        Posted by lkylei at Nov 30, 2020 08:18
                                     |
| The link looks fine to me...it goes to;https://wiki.sei.cmu.edu/confluence/x/Io4xBQ
                                        Posted by svoboda at Nov 30, 2020 09:22
                                     |
| Maybe I don't have permission to access this link.Page Not FoundWe can't find that page. This could be because:The page doesn't exist.The page exists, but you don't have view permission for that space.
                                        Posted by lkylei at Nov 30, 2020 09:47
                                     |
| FWIW, it's a 404 for me as well (both when logged out and when logged in).
                                        Posted by aballman at Nov 30, 2020 09:58
                                     |
| OK the link should be fixed now.
                                        Posted by svoboda at Dec 01, 2020 12:48
                                     |
| I can confirm the link now works for me.
                                        Posted by aballman at Dec 01, 2020 12:55
                                     |
|  Should the application of a function call like “puts(s)” be also improved for a “compliant solution”?
                                        Posted by markus.elfring at Jun 22, 2023 02:44
                                     |
| Which code will take care for the release of the string which will eventually be connected to the pointer variable “s” for your demonstration approach?Would you like to adhere to the rule “MEM31-C. Free dynamically allocated memory when no longer needed” also for another “compliant solution”?
                                        Posted by markus.elfring at Jun 22, 2023 04:48
                                     |
| Fixed, thanks.
                                        Posted by svoboda at Jun 22, 2023 08:42
                                     |
| Agreed, I've freed the s; string in both code examples.
                                        Posted by svoboda at Jun 22, 2023 08:44
                                     |
| I got an other impression.I would prefer that the shown undesirable return value ignorance will be avoided (also for calls of more file output functions).
                                        Posted by markus.elfring at Jun 22, 2023 09:18
                                     |
| Markus,I interpret that the issue is that you don't agree with our guidance.; But, the change that Dave made is consistent with our guidance.  Either we need to agree to disagree, or we need an explanation and argument that we do agree with to make the change.  But, I think our position is clear at this point, and I feel that we are going in circles.
                                        Posted by rschiela at Jun 22, 2023 09:29
                                     |
| …, or we need an explanation and argument …Does source code like “(void) puts(s);” (for primary file output) indicate conflicting software development expectations?Would other programmers and code reviewers care any more for data processing failures here?
                                        Posted by markus.elfring at Jun 22, 2023 11:46
                                     |

