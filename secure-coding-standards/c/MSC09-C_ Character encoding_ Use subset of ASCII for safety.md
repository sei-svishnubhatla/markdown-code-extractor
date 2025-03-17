According to subclause 5.2.1 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> Two sets of characters and their associated collating sequences shall be defined: the set in which source files are written (the *source character set*), and the set interpreted in the execution environment (the *execution character set*). Each set is further divided into a *basic character set*, whose contents are given by this subclause, and a set of zero or more [locale-specific](BB.-Definitions_87152273.html#BB.Definitions-locale-specificbehavior) members (which are not members of the basic character set) called *extended characters*. The combined set is also called the *extended character set*. The values of the members of the execution character set are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior).

There are several national variants of ASCII. As a result, the original ASCII is often called US-ASCII. ISO/IEC 646-1991 defines a character set, similar to US-ASCII, but with code positions corresponding to US-ASCII characters `@[]{|`} as *national use positions* \[[ISO/IEC 646-1991](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC646-1991)\]. It also gives some liberties with particular characters (e.g., `` #$^`~ ``).  In ISO/IEC 646-1991, several national variants of ASCII are defined, assigning different letters and symbols to the national use positions. Consequently, the characters that appear in those positions, including those in US-ASCII, are less portable in international data transfer. Because of the national variants, some characters are less portable than others: they might be transferred or interpreted incorrectly.
In addition to the letters of the English alphabet (A through Z and a through z), the digits (0 through 9), and the space, only the following characters are portable:
> [!note]  
>
>     % & + , - . : = _

When naming files, variables, and other objects, only these characters should be considered for use. This recommendation is related to [STR02-C. Sanitize data passed to complex subsystems](STR02-C_%20Sanitize%20data%20passed%20to%20complex%20subsystems).
### File Names
File names containing particular characters can be troublesome and can cause [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) leading to potential [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). If a program allows the user to specify a file name in the creation or renaming of a file, certain checks should be made to disallow the following characters and patterns:
-   Leading dashes—Leading dashes can cause problems when programs are called with the file name as a parameter because the first character or characters of the file name might be interpreted as an option switch.
-   Control characters, such as newlines, carriage returns, and escape—Control characters in a file name can cause unexpected results from shell scripts and in logging.
-   Spaces—Spaces can cause problems with scripts and when double quotes are not used to surround the file name.
-   Invalid character encodings—Character encodings can be a huge issue. (See [MSC10-C. Character encoding: UTF8-related issues](MSC10-C_%20Character%20encoding_%20UTF8-related%20issues).)
-   Any characters other than letters, numbers, and punctuation designated here as portable—Other special characters are included in this recommendation because they are commonly used as separators, and having them in a file name can cause unexpected and potentially insecure behavior.
Also, many of the punctuation characters are not unconditionally safe for file names even of they are portably available.
Most of these characters or patterns are primarily a problem to scripts or automated parsing, but because they are not commonly used, it is best to disallow their use to reduce potential problems. Interoperability concerns also exist because different operating systems handle file names of this sort in different ways.
As a result of the influence of MS-DOS, file names of the form `xxxxxxxx.xxx`, where `x` denotes an alphanumeric character, are generally supported by modern systems. On some platforms, file names are case sensitive, and on other platforms, they are case insensitive. VU#439395 is an example of a vulnerability resulting from a failure to deal appropriately with case-sensitivity issues \[[VU#439395](AA.-Bibliography_87152170.html#AA.Bibliography-VU439395)\].
## Noncompliant Code Example (File Name 1)
In this noncompliant code example, unsafe characters are used as part of a file name:
``` c
#include <fcntl.h>
#include <sys/stat.h>
int main(void) {
   char *file_name = "\xe5ngstr\xf6m";
   mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
   int fd = open(file_name, O_CREAT | O_EXCL | O_WRONLY, mode);
   if (fd == -1) {
      /* Handle error */
   }
}
```
An [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) is free to define its own mapping of the "nonsafe" characters. For example, when run on Red Hat Enterprise Linux 7.5, this noncompliant code example resulted in the following file name being revealed by the `ls` command:
``` java
?ngstr?m
```
## Compliant Solution (File Name 1)
Use a descriptive file name containing only the subset of ASCII previously described:
``` c
#include <fcntl.h>
#include <sys/stat.h>
int main(void) {
   char *file_name = "name.ext";
   mode_t mode = S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH;
   int fd = open(file_name, O_CREAT | O_EXCL | O_WRONLY, mode);
   if (fd == -1) {
      /* Handle error */
   }
}
```
## Noncompliant Code Example (File Name 2)
This noncompliant code example is derived from [FIO30-C. Exclude user input from format strings](FIO30-C_%20Exclude%20user%20input%20from%20format%20strings), except that a newline is removed on the assumption that `fgets()` will include it:
``` c
char myFilename[1000];
const char elimNewLn[] = "\n";
fgets(myFilename, sizeof(myFilename)-1, stdin);
myFilename[sizeof(myFilename)-1] = '\0';
myFilename[strcspn(myFilename, elimNewLn)] = '\0';
```
No checks are performed on the file name to prevent troublesome characters. If an attacker knew this code was in a program used to create or rename files that would later be used in a script or automated process of some sort, he or she could choose particular characters in the output file name to confuse the later process for malicious purposes.
## Compliant Solution (File Name 2)
In this compliant solution, the program rejects file names that violate the guidelines for selecting safe characters:
``` c
char myFilename[1000];
const char elimNewln[] = "\n";
const char badChars[] = "-\n\r ,;'\\<\"";
do {
  fgets(myFilename, sizeof(myFilename)-1, stdin);
  myFilename[sizeof(myFilename)-1] ='\0';
  myFilename[strcspn(myFilename, elimNewln)]='\0';
} while ( (strcspn(myFilename, badChars))
           < (strlen(myFilename)));
```
Similarly, you must validate all file names originating from untrusted sources to ensure they contain only safe characters.
## Risk Assessment
Failing to use only the subset of ASCII that is guaranteed to work can result in misinterpreted data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC09-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bitfield-namecharacter-constantenum-tag-spelling
enumeration-constant-name
function-like-macro-name
global-function-name
global-object-name
global-object-name-const
header-filename
implementation-filename
local-object-name
local-object-name-const
local-static-object-name
local-static-object-name-const
object-like-macro-name
static-function-name
static-object-name
static-object-name-const
string-literal
struct-member-name
struct-tag-spelling
typedef-name
union-member-name
union-tag-spelling | Partially checked |
| Helix QAC | 2024.4 | C0285, C0286, C0287, C0288, C0289, C0299 |  |
| LDRA tool suite | 9.7.1 | 113 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC09-a | Only use characters defined in the ISO C standard |
| RuleChecker | 24.04 | bitfield-namecharacter-constantenum-tag-spelling
enumeration-constant-name
function-like-macro-name
global-function-name
global-object-name
global-object-name-const
header-filename
implementation-filename
local-object-name
local-object-name-const
local-static-object-name
local-static-object-name-const
object-like-macro-name
static-function-name
static-object-name
static-object-name-const
string-literal
struct-member-name
struct-tag-spelling
typedef-name
union-member-name
union-tag-spelling | Partially checked |
| SonarQube C/C++ Plugin | 3.11 | S1578 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC09-CPP. Character encoding: Use subset of ASCII for safety |
| CERT Oracle Secure Coding Standard for Java | IDS50-J. Use conservative file naming conventions |
| MISRA C:2012 | Directive 1.1 (required)Rule 4.1 (required) |
| MITRE CWE | CWE-116, Improper encoding or escaping of output |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 646-1991] | "ISO 7-Bit Coded Character Set for Information Interchange" |
| [ISO/IEC 9899:2011] | Subclause 5.2.1, "Character Sets" |
| [Kuhn 2006] | "UTF-8 and Unicode FAQ for UNIX/Linux" |
| [VU#439395] |  |
| [Wheeler 2003 | Section 5.4, "File Names" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152362) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/MSC10-C_%20Character%20encoding_%20UTF8-related%20issues)
## Comments:

|  |
| ----|
| Many instances of "safe" should be changed to "portable".
Many of the punctuation characters aren't unconditionally safe for filenames even of they are portably available.
Due to MS-DOS influence, xxxxxxxx.xxx where x denotes alphanumeric is generally supported by modern systems.; Sometimes upper-case is not distinct from lower-case, although that is rare nowadays.
                                        Posted by dagwyn at Apr 18, 2008 14:25
                                     |
| Marked 'unenforceable' because the problem of identifying if a program recognizes bad chars in a filename string is unenforceable.
It would be easy to catch the first NCCE: that is, a string literal with bad chars passed to fopen(). But I'm not sure it's worth it.
                                        Posted by svoboda at Jul 29, 2008 16:51
                                     |
| I changed the link to VU#881872 in the bibliography section to the link to VU#439395.
(VU#439395 is mentioned right before the first NCCE.)
as far as I understand, VU#881872 is a kind of vulnerability instance missing user input sanitization, so, VU#881872 has nothing to do with this guideline.
anyone please revise it if I misunderstand something.
                                        Posted by yozo at Jun 14, 2011 04:02
                                     |
| The first noncompliant example seems to have been broken by the wiki formatter. It looks like the control characters got changed to their HTML escapes, which C obviously doesn't treat specially.
                                        Posted by jcsible at Jun 30, 2020 11:46
                                     |
| I feel uneasy about this rule in general. On Linux, file names can contain any byte except for 0x00 (NUL) and 0x2F (/). I don't like the idea of rejecting valid names just because something else might mishandle them. It feels like trying to stop SQL injection by doing https://thedailywtf.com/articles/Injection_Rejection instead of using parameterized queries.
                                        Posted by jcsible at Jun 30, 2020 11:49
                                     |
| FWIW the first noncompliant code example has been butchered a looooonnnnggg time; here is an old version of the rule which has the original "invalid" characters:https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87155867
However, this noncompliant code works fine on RHEL7.5 as well as CentOS7.
                                        Posted by svoboda at Jun 30, 2020 13:52
                                     |
| I have removed the 1st NCCE/CS, as the NCCE (in its original form) is not currently reproducible.However, this recommendation is still valid. While Linux (and POSIX in general) is very permissive in filename characters as you note, ISO C must also be supported on other, less permissive filesystems. Thus we must base this guideline on what the standard guarantees.Even when permitted by the filesystem, weird characters in filenames can lead to other problems, as is explained in;IDS31-PL. Do not use the two-argument form of open().
                                        Posted by svoboda at Jun 30, 2020 13:58
                                     |
| The problem that the first example was trying to demonstrate is still reproducible with a non-UTF-8 name. Do char *file_name = "\xe5ngstr\xf6m"; and weirdness will happen again. (Though note that the weirdness is a consequence of the ls command and/or your terminal; Linux itself can handle it fine.)
                                        Posted by jcsible at Jun 30, 2020 14:14
                                     |
| I restored the example, as it does behave as you cite on RHEL 7.5.; Again, the filesystem can handle the characters but other code (eg ls) can't.
                                        Posted by svoboda at Jun 30, 2020 16:31
                                     |

