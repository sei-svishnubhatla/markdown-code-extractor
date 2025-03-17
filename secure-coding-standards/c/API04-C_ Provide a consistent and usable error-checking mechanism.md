Functions should provide consistent and usable error-checking mechanisms. Complex interfaces are sometimes ignored by programmers, resulting in code that is not error checked. Inconsistent interfaces are frequently misused and difficult to use, resulting in lower-quality code and higher development costs.
## Noncompliant Code Example (`strlcpy()`)
The `strlcpy()` function copies a null-terminated source string to a destination array. It is designed to be a safer, more consistent, and less error-prone replacement for `strcpy()`.
The `strlcpy()` function returns the total length of the string it tried to create (the length of the source string).
To detect truncation, perhaps while building a path name, code such as the following might be used:
``` c
char *dir, *file, pname[MAXPATHLEN];
/* ... */
if (strlcpy(pname, dir, sizeof(pname)) >= sizeof(pname)) {
  /* Handle source-string-too long error */
}
```
## Compliant Solution (`strcpy_m()`)
The managed string library \[[Burch 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Burch06)\] handles errors by consistently returning the status code in the function return value. This approach encourages status checking because the user can insert the function call as the expression in an `if` statement and take appropriate action on failure.
The `strcpy_m()` function is an example of a managed string function that copies a source-managed string into a destination-managed string:
``` c
errno_t retValue; 
string_m dest, source;  
/* ... */
if (retValue = strcpy_m(dest, source)) { 
  fprintf(stderr, "Error %d from strcpy_m.\n", retValue);
} 
```
The greatest disadvantage of this approach is that it prevents functions from returning any other value. Consequently, all values (other than the status) returned by a function must be returned as a pass-by-reference parameter, preventing a programmer from nesting function calls. This trade-off is necessary because nesting function calls can conflict with a programmer's willingness to check status codes.
## Risk Assessment
Failure to provide a consistent and usable error-checking mechanism can result in type errors in the program.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API04-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | error-information-unusederror-information-unused-computedbad-functionbad-function-use | Supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. API04-C | Checks for situations where returned value of a sensitive function is not checked (rule partially covered) |
| RuleChecker | 24.04 | error-information-unusedbad-functionbad-function-use | Supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+API04-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC 9945:2003 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC 23360-1:2006 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24731-1 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24731-2 |  | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 21.3 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Directive 4.12 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-754, Improper check for unusual or exceptional conditions | Prior to 2018-01-12: CERT: |

## Bibliography

|  |  |
| ----|----|
| [Burch 2006] |  |
| [CERT 2006c] |  |
| [Miller 1999] |  |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152287) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152031)
## Comments:

|  |
| ----|
| Not sure this rule should stand by itself. The NCCE doesn't explain why strlcpy() is bad, or worse than strcpy_m(). I trust its bad because it violates ERR02-C. Avoid in-band error indicators, right?  
Also the CCE code violates MSC02-C. Avoid errors of omission. Suggest it be rewritten as:
if ((retValue = strcpy_m(dest, source)) != 0)

Finally, we ought to have a CCE using strcpy_s from TR24731-1.
I suspect for this to be a legit rule, we need another NCCE/CCE pair that doesn't violate ERR02-C.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 07, 2009 11:13
\| \|
The function called is `strcpy_m()`, but the error message refers to `strcreate_m()`.
![](images/icons/contenttypes/comment_16.png) Posted by marcel.waldvogel at Apr 15, 2017 05:21
\| \|
Fixed
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2017 17:46
\| \|
Readability would be improved by:
> retValue = strcpy_m(dest, source);
>
> if (retValue != 0) …

![](images/icons/contenttypes/comment_16.png) Posted by marcel.waldvogel at Jan 13, 2018 06:47
\| \|
How this recommendation relates to the MISRA C:2012 Rule 21.3 and Dir 4.12? They both refer to use of dynamic memory allocation.
![](images/icons/contenttypes/comment_16.png) Posted by rozenau at Jul 18, 2018 09:41
\| \|
Yes. The specific relation is unclear, except in so far as they are about defining good APIs...this guideline specifically covers error handling.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 18, 2018 15:03
\| \|
When using the return error code method for functions in an API, and several functions in the API return the same type of error such as out of memory, is it better for each function to have it's own individual error codes such as an enum of error codes for each function, or would it be better to have a specific error code for each type of error that can occur in the API?
If each function has it's own set of error codes and if you are exporting them to allow a dynamic linked user of the api to discover the codes at run time, then you end up having a lot more exported symbols... and the exported names of the error codes will probably end up looking like this:
myapi_function1_outofmemoryerrorcase1
myapi_function1_outofmemoryerrorcase2
myapi_function1_success
myapi_function2_outofmemory
myapi_function2_success
myapi_function3_outofmemory
myapi_function3_success
Then when you start nesting function calls, the number of exported symbols increases even more. I'm assuming the programmer would change the error code before passing it up to a higher level routine so that the consumer of the API could figure out exactly what happened. This would look like:
myapi_higherfunction_lowerfunction_outofmemoryerrorcase1
And what do you do if an error changes in a low level function? The higher up functions error codes would also change...
(I'm going somewhere with this ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by thaine at Oct 26, 2018 12:13
\|
