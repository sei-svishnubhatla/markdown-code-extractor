Upon return, functions should guarantee that any object returned by the function, or any modified value referenced by a pointer argument, is a valid object of function return type or argument type. Otherwise, type errors can occur in the program.
A good example is the null-terminated byte string type in C. If a string lacks the terminating null character, the program may be tricked into accessing storage after the string as legitimate data. A program may, as a result, process a string it should not process, which might be a [security flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) in itself. It may also cause the program to abort, which might be a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack).
The emphasis of this recommendation is to avoid producing unterminated strings; it does not address processing of already existing unterminated strings. However, by preventing the creation of unterminated strings, the need to process them is greatly lessened.
## Noncompliant Code Example
The standard `strncpy()` function does not guarantee that the resulting string is null-terminated. If there is no null character in the first `n` characters of the `source` array, the result may not be null-terminated.
``` c
char *source;
char a[NTBS_SIZE];
/* ... */
if (source) {
  char* b = strncpy(a, source, 5); // b == a
}
else {
  /* Handle null string condition */
}
```
## Compliant Solution (`strncpy_s()`, C11 Annex K)
The C11 Annex K `strncpy_s()` function copies up to `n` characters from the source array to a destination array. If no null character was copied from the source array, the `n`th position in the destination array is set to a null character, guaranteeing that the resulting string is null-terminated.
``` c
char *source;
char a[NTBS_SIZE];
/* ... */
if (source) {
  errno_t err = strncpy_s(a, sizeof(a), source, 5);
  if (err != 0) {
    /* Handle error */
  }
}
else {
  /* Handle null string condition */
}
```
## Risk Assessment
Failure to enforce type safety can result in type errors in the program.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API07-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.CAST.VALUELANG.CAST.COERCE 
ALLOC.TM | Cast alters valueCoercion alters value
Type mismatch |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+API07-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | String Termination [CJM] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MITRE CWE | CWE-192 | Prior to 2018-01-12: |
| MITRE CWE | CWE-227 | Prior to 2018-01-12: |
| MITRE CWE | CWE-590 | Prior to 2018-01-12: |
| MITRE CWE | CWE-686 | Prior to 2018-01-12: |
| MITRE CWE | CWE-704 | Prior to 2018-01-12: |
| MITRE CWE | CWE-761 | Prior to 2018-01-12: |
| MITRE CWE | CWE-762 | Prior to 2018-01-12: |
| MITRE CWE | CWE-843 | Prior to 2018-01-12: |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152031) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [API09-C. Compatible values should have the same type](/confluence/pages/createpage.action?spaceKey=android&title=API09-C.+Compatible+values+should+have+the+same+type)
## Comments:

|  |
| ----|
| Add a second example that doesn't involve NTBS?
                                        Posted by rcs at Dec 10, 2008 09:44
                                     |
| The concept of a NUL-terminated byte string is not represented by a type in C so the uses of strncpy() or strncpy_s() are unrelated to type safety. The noncompliant example on this page actually demonstrates a violation of STR32-C. Null-terminate byte strings as required. Unless there are examples of true type safety bugs that aren't already addressed by other existing rules (such as EXP39-C. Do not access a variable through a pointer of an incompatible type) I suggest this rule be removed.
                                        Posted by martinsebor at Jan 18, 2010 20:40
                                     |
| Furthermore, it is not always feasible to validate that a string is null-termiated. What if a function returns a string it allocated on the heap, and expects the caller to free? The caller does not know the string length, and if the string is not null-terminated, the caller cannot verify this w/o overflowing the heap. The GNU getline() function is a good example of this.
                                        Posted by svoboda at Jan 19, 2010 09:58
                                     |
| Just for the record, strncpy() does not return "errno_t" but "char *".
                                        Posted by xuinkrbin. at Dec 12, 2012 11:18
                                     |
| Fixed, thanks. (OTOH strncpy_s() does return errno_t)
                                        Posted by svoboda at Dec 14, 2012 11:27
                                     |

