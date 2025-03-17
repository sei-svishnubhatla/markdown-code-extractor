Do not make any assumptions about the size of environment variables because an adversary might have full control over the environment. If the environment variable needs to be stored, the length of the associated string should be calculated and the storage dynamically allocated (see [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator)).
## Noncompliant Code Example
This noncompliant code example copies the string returned by `getenv()` into a fixed-size buffer:
``` c
void f() {
  char path[PATH_MAX]; /* Requires PATH_MAX to be defined */
  strcpy(path, getenv("PATH"));
  /* Use path */
}
```
Even if your platform assumes that `$PATH` is defined, defines `PATH_MAX`, and enforces that paths not have more than `PATH_MAX` characters, the `$PATH` environment variable still is not required to have less than `PATH_MAX` chars. And if it has more than `PATH_MAX` chars, a buffer overflow will result. Also, if `$PATH` is not defined, then `strcpy()` will attempt to dereference a null pointer.
## Compliant Solution
In this compliant solution, the `strlen()` function is used to calculate the size of the string, and the required space is dynamically allocated:
``` c
void f() {
  char *path = NULL;
  /* Avoid assuming $PATH is defined or has limited length */
  const char *temp = getenv("PATH");
  if (temp != NULL) {
    path = (char*) malloc(strlen(temp) + 1);
    if (path == NULL) {
      /* Handle error condition */
    } else {
      strcpy(path, temp);
    }
    /* Use path */
    free(path);
  }
}
```
## Compliant Solution (POSIX or C2x)
In this compliant solution, the `strdup()` function is used to dynamically allocate a duplicate of the string:
``` c
void f() {
  char *path = NULL;
  /* Avoid assuming $PATH is defined or has limited length */
  const char *temp = getenv("PATH");
  if (temp != NULL) {
    path = strdup(temp);
    if (path == NULL) {
      /* Handle error condition */
    }
    /* Use path */
    free(path);
  }
}
```
## Risk Assessment
Making assumptions about the size of an environmental variable can result in a buffer overflow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV01-C | High | Likely | Medium |  P18  |  L1  |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.MEM.BO LANG.MEM.TO
 (general) | Buffer overrunType overrun
CodeSonar's taint analysis includes handling for taint introduced through the environment |
| Compass/ROSE |  |  | Can detect violations of the rule by using the same method as STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| Klocwork | 2024.4 | ABV.ANY_SIZE_ARRAYABV.GENERAL
ABV.GENERAL.MULTIDIMENSION
ABV.ITERATOR
ABV.MEMBER
ABV.STACK
ABV.TAINTED
ABV.UNKNOWN_SIZE
ABV.UNICODE.BOUND_MAP
ABV.UNICODE.FAILED_MAP
ABV.UNICODE.NNTS_MAP
ABV.UNICODE.SELF_MAP |  |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV01-a CERT_C-ENV01-b 
CERT_C-ENV01-c | Don't use unsafe C functions that do write to range-unchecked buffersAvoid using unsafe string functions which may cause buffer overflows
Avoid overflow when writing to a buffer |
| PC-lint Plus | 1.4 | 669 | Fully supported |
| Polyspace Bug Finder |  R2024a  | CERT C: Rec. ENV01-C | Checks for tainted NULL or non-null-terminated string (rec. partially covered) |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV01-C).
## Related Guidelines

|  |  |
| ----|----|
| MITRE CWE | CWE-119, Improper Restriction of Operations within the Bounds of a Memory BufferCWE-123, Write-what-where Condition
CWE-125, Out-of-bounds Read |

## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | Chapter 8, "Environment Variables" |
| [Viega 2003] | Section 3.6, "Using Environment Variables Securely" |

------------------------------------------------------------------------
[](../c/Rec_%2010_%20Environment%20_ENV_) [](../c/Rec_%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152358)
## Comments:

|  |
| ----|
| This rule looks totally subsumed by STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator.
                                        Posted by svoboda at May 11, 2009 14:23
                                     |
| True, although I think it's still valuable if only as a reminder. I'm pretty sure I've seen code like this:
void f() {
    /* allocate enough room for PATH */
    char path [PATH_MAX];
    /* PATH must be defined */
    strcpy(path, getenv("PATH"));
    /* use path */
}

Might this be a better example?
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 10, 2010 22:48
\| \|
Yes. Reworked the NCCE/CS to use your sample.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 11, 2010 11:21
\| \|
Oops...accompanying text need to be updated too.
It does seem that several platforms, including Linux and OSX allow paths to be constructed that are longer than PATH_MAX. While this is an issue, we shouldn't deal with it here (maybe set aside for the POSIX section.) So we focus on that fact that an attacker can set $PATH to anything they wish, incl. a string longer than PATH_MAX.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 11, 2010 13:19
\| \|
Not only that, an implementation that doesn't impose a restriction on the length of a pathname need not define `PATH_MAX` at all. (When it is defined, it gives the maximum length of a pathname that a system call is able to process at a time. Pathnames that are longer than that are valid, they just cannot be processed in a single call but may require intermediate steps.)
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 11, 2010 18:48
\| \|
True, PATH_MAX need not be defined. If it isn't, then the NCCE won't compile. Added the assumption that PATH_MAX is at least defined ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 12, 2010 08:53
\| \|
In my experience, assuming that `PATH_MAX` and other similar resource limit constants (or optional types) are necessarily defined, expand to values suitable for use in array declarations, or represent parameters that cannot change at runtime is a sufficiently common mistake to warrant a guideline warning users against such assumptions.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 12, 2010 14:07
\| \|
The *Compliant Solution* as of JUN-14-2010 is a mess:
``` java
void f() {
  char *copy = NULL;
  /* avoid assuming $PATH is defined or has limited length */
  const char *temp = getenv("PATH");
  if (temp != NULL) {
    path = (char*) malloc(strlen(temp) + 1);
    if (copy == NULL) {
      /* Handle error condition */
    } else {
      strcpy(path, temp);
    }
    /* use path */
  }
}
```
It uses `copy` and `path` when it should use only one of them in addition to `temp`. `path` is undeclared and the test for `if (copy == NULL)` is always true. I find it rather embarrasing that bugs like this slip in such a carefully crafted coding guideline. Has it never been considered to at least test compile the *Compliant Solutions* (at least with `-c`; no `main()` required, but correct headers, please)? I don't dare asking for test linting... :-)
![](images/icons/contenttypes/comment_16.png) Posted by jens schweikhardt at Jun 14, 2010 05:20
\| \|
I've fixed the compliant solution (and even compiled it ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 15, 2010 15:27
\| \|
This recommendation and example appears to be entirely redundant with the getenv() example in STR31-C.; We should probably eliminate this, because recommendation instead of the example, because this code example violates STR31-C.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 30, 2013 08:14
\| \|
A much simpler compliant solution is possible with POSIX, by using `strdup`.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 13:38
\|
