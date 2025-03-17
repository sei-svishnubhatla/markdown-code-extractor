Do not use a semicolon on the same line as an `if`, `for`, or `while` statement because it typically indicates programmer error and can result in unexpected behavior.
## Noncompliant Code Example
In this noncompliant code example, a semicolon is used on the same line as an `if` statement:
``` c
if (a == b); {
  /* ... */
}
```
## Compliant Solution
It is likely, in this example, that the semicolon was accidentally inserted:
``` c
if (a == b) {
  /* ... */
}
```
## Risk Assessment
Errors of omission can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP15-C | High | Likely | Low | P27 | L1 |

###  Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | empty-body | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP15 | Fully implemented |
| CodeSonar | 8.3p0 | LANG.STRUCT.EBS | Empty branch statement |
| Helix QAC | 2024.4 | C3109 |  |
| Klocwork | 2024.4 | SEMICOL |  |
| LDRA tool suite | 9.7.1 | 11 S, 12 S, 428 S | Fully Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP15-a | Suspicious use of semicolon |
| PC-lint Plus | 1.4 | 721, 722 | Partially supported: reports missing body from if, for, or while with semi-colon immediately following predicate |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP15-C | Checks for semicolon on same line as for, if or while statement (rule fully covered) |
| PVS-Studio | 7.35 | V529, V715 |  |
| SonarQube C/C++ Plugin | 3.11 | S1116 |  |
| RuleChecker | 24.04 | empty-body | Fully checked |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT Oracle Coding Standard for Java | MSC51-J. Do not place a semicolon immediately following an if, for, or while condition |
| ISO/IEC TR 24772:2013 | Likely Incorrect Expression [KOA] |
| MITRE CWE | CWE-480, Use of incorrect operator |

## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.7.2, "Errors of Omission and Addition" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152251) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152223)
## Comments:

|  |
| ----|
| This guideline seems way too strict.  For example, I see nothing wrong with the following example:
if ( x ) y++;

Notice this example is nonconforming because a semicolon appears on the same line as the if.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 25, 2010 12:14
\| \|
I think this guideline should be eliminated and the example integrated with [MSC12-C. Detect and remove code that has no effect](/confluence/pages/createpage.action?spaceKey=c&title=MSC12-C.+Detect+and+remove+code+that+has+no+effect)
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 25, 2010 12:18
\| \|
I agree that this is draconian. I suspect the intent is to prevent problems such as:
``` java
char* strchr(const char *str, int c) {
  for (; *str; ++str);   /* <<< forgot to remove semicolon */
    if ((unsigned char)*str == c)
      return str;
  return NULL;
}
```
that are sometimes introduced by copying and pasting, for instance from code such as:
``` java
size_t strlen(const char *str) {
  const char *s = str;
  for (; *str; ++str);
  return (size_t)(str - s);
}
```
(Note the `strchr()` implementation above is buggy in another way that's unrelated to the semicolon.)
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Nov 28, 2010 13:57
\| \|
There is no; risk assesment for this recommendation
![](images/icons/contenttypes/comment_16.png) Posted by oliver.holzkamp at Aug 01, 2014 04:47
\|
