Many programs and libraries, including the shared library loader on both UNIX and Windows systems, depend on environment variable settings. Because environment variables are inherited from the parent process when a program is executed, an attacker can easily sabotage variables, causing a program to behave in an unexpected and insecure manner \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\].
All programs, particularly those running with higher privileges than the caller (such as those with `setuid/setgid` flags), should treat their environment as untrusted user input. Because the environment is inherited by processes spawned by calls to the `fork()`, `system()`, or `exec()` functions, it is important to verify that the environment does not contain any values that can lead to unexpected behavior.
The best practice for such programs is to
-   Drop privileges once they are no longer necessary. (See [POS02-C. Follow the principle of least privilege](POS02-C_%20Follow%20the%20principle%20of%20least%20privilege).)
-   Avoid calling `system()`. (See [ENV33-C. Do not call system()](ENV33-C_%20Do%20not%20call%20system__).)
-   Clear the environment and fill it with trusted or default values.
This recommendation is a more specific instance of [STR02-C. Sanitize data passed to complex subsystems](STR02-C_%20Sanitize%20data%20passed%20to%20complex%20subsystems).
Subclause 7.22.4.6 of the C Standard states that "the set of environment names and the method for altering the environment list are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior)." Consequently, it is important to understand which functions are available for clearing, modifying, and looking up default values for environment variables. Because some programs may behave in unexpected ways when certain environment variables are not set, it is important to understand which variables are necessary on your system and what are safe values for them.
## Noncompliant Code Example (POSIX, `ls`)
This noncompliant code example invokes the C `system()` function to execute the `/bin/ls` program. The `system()` function passes a string to the command processor in the host environment to be executed.
``` c
if (system("/bin/ls dir.`date +%Y%m%d`") == -1) {
  /* Handle error */
}
```
Although `IFS` does not affect the command portion of this string, `/bin/ls`, it does determine how the argument is built after calling `date`. If the default shell does not ignore the incoming value of the `IFS` environment value, and an attacker sets `IFS` to `"."`, the intended directory will not be found.
## Compliant Solution (POSIX, `ls`)
The nonstandard function `clearenv()` may be used to clear out the environment where available: otherwise, the environment can be cleared by obtaining the environment variable names from `environ` and removing each one using `unsetenv()`.
In this compliant solution, the environment is cleared by `clearenv()`, and then the `PATH` and `IFS` variables are set to safe values before `system()` is invoked. [Sanitizing](BB.-Definitions_87152273.html#BB.Definitions-sanitization) shell commands can be difficult, and doing so can adversely affect the power and flexibility associated with them.
``` c
char *pathbuf;
size_t n;
if (clearenv() != 0) {
  /* Handle error */
}
n = confstr(_CS_PATH, NULL, 0);
if (n == 0) {
  /* Handle error */
}
if ((pathbuf = malloc(n)) == NULL) {
  /* Handle error */
}
if (confstr(_CS_PATH, pathbuf, n) == 0) {
  /* Handle error */
}
if (setenv("PATH", pathbuf, 1) == -1) {
  /* Handle error */
}
if (setenv("IFS", " \t\n", 1) == -1) {
  /* Handle error */
}
if (system("ls dir.`date +%Y%m%d`") == -1) {
  /* Handle error */
}
```
POSIX also specifies the `confstr()` function, which can be used to look up default values for environment variables \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\]. The `_CS_V7_ENV` argument to `confstr()` retrieves a list of environment variable settings required for a default [conforming](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-conforming) environment \[[IEEE Std 1003.1:2013](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-IEEEStd1003.1-2013)\]. A space-separated list of `variable=value` pairs is returned, with variable names guaranteed not to contain equal signs (=), and `variable=value` pairs guaranteed not to contain spaces. Used together with the `_CS_PATH` request, this completely describes the minimum environment variable settings required to obtain a clean, conforming environment. On systems conforming to the POSIX.1-2008 standard, this should be used to create a sanitized environment.
On systems that have no `clearenv()` function, the following implementation can be used:
``` c
extern char **environ;
int clearenv(void) {
  static char *namebuf = NULL;
  static size_t lastlen = 0;
  while (environ != NULL && environ[0] != NULL) {
    size_t len = strcspn(environ[0], "=");
    if (len == 0) {
      /* Handle empty variable name (corrupted environ[]) */
    }
    if (len > lastlen) {
      namebuf = realloc(namebuf, len+1);
      if (namebuf == NULL) {
        /* Handle error */
      }
      lastlen = len;
    }
    memcpy(namebuf, environ[0], len);
    namebuf[len] = '\0';
    if (unsetenv(namebuf) == -1) {
      /* Handle error */
    }
  }
  return 0;
}
```
## Compliant Solution (Windows)
There is no portable or guaranteed way to clear out the environment under Windows. Following [ENV33-C. Do not call system()](ENV33-C_%20Do%20not%20call%20system__), care should be taken to use `_execle()`, `_execlpe()`, `_execve()`, or `_execvpe()` instead of `system()`, because they allow the environment to be explicitly specified.
If it is explicitly known which environment variables need to be kept, *Secure Programming Cookbook for C and C++* \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\] defines a function, `spc_sanitize_environment()`, that will remove everything else.
## Risk Assessment
Invoking an external program in an attacker-controlled environment is inherently dangerous.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV03-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Helix QAC | 2024.4 | C5017 |  |
| LDRA tool suite | 9.7.1 | 588 S | Partially implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ENV01-CPP. Sanitize the environment when invoking external programs |
| CERT Oracle Secure Coding Standard for Java | IDS07-J. Sanitize untrusted data passed to the Runtime.exec() method |
| ISO/IEC TR 24772:2013 | Executing or Loading Untrusted Code [XYS] |
| MITRE CWE | CWE-78, Failure to sanitize data into an OS command (aka "OS command injection")CWE-88, Argument injection or modification
CWE-426, Untrusted search path
CWE-471, Modification of Assumed-Immutable Data (MAID)
CWE-807, Reliance on intrusted inputs in a security decision |

## Bibliography

|  |  |
| ----|----|
| [CA-1995-14] | "Telnetd Environment Vulnerability" |
| [Dowd 2006] | Chapter 10, "UNIX II: Processes" |
| [IEEE Std 1003.1:2013] | Chapter 8, "Environment Variables"XSH, System Interfaces, confstr |
| [ISO/IEC 9899:2011] | Subclause 7.22.4, "Communication with the Environment" |
| [Viega 2003] | Section 1.1, "Sanitizing the Environment" |
| [Wheeler 2003] | Section 5.2, "Environment Variables" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152358) [](../c/Rec_%2010_%20Environment%20_ENV_) [](../c/Rec_%2012_%20Error%20Handling%20_ERR_)
## Comments:

|  |
| ----|
| There is some misinformation in the parts that talk about IFS.; The advice to set IFS to its standard value is fine, but the specifics of why this is needed are wrong.  It says IFS "is used by the sh and bash shells to determine which characters separate command line arguments".  Ancient Bourne shells used to do this, but modern shells do not.  Not even the Bourne shell that Solaris still has as /bin/sh does it.  Modern shells only use IFS to do field splitting on the results of parameter expansion, command substitution, and arithmetic expansion (as required by POSIX).
The example given of system("/bin/ls") is not affected by IFS. However, something like
system("ls dir.`date +%Y%m%d`") would be.
                                        Posted by geoffclare at Mar 19, 2008 11:30
                                     |
| _PATH_STDPATH and paths.h are non-standard.; BSD and Linux systems have them, but many other systems do not.  The portable way to obtain a standard PATH value is to use confstr() with _CS_PATH.
                                        Posted by geoffclare at Mar 19, 2008 11:34
                                     |
| There are a couple of issues with the parts that talk about clearing the environment and preserving some variables.
1. POSIX says "If the application modifies environ or the pointers to which it points, the behavior of getenv() is undefined."; The proper way to remove unwanted variables is to use unsetenv().
2. Some systems have an environment variable that is needed to ensure conforming behaviour.  For example AIX needs XPG_SUS_ENV,  HP-UX needs UNIX95, IRIX needs _XPG, UnixWare needs POSIX2, and Linux needs POSIXLY_CORRECT.  Clearing these variables could change the behaviour of some interfaces or utilities in subtle ways that could make the application misbehave, or even have security implications. The new revision of POSIX will provide a standard way to query which variables are needed.  It gives an example of how to use it via getconf when creating a new environment with env -i:
 env -i $(getconf V7_ENV) PATH="$(getconf PATH)" command
but the same information can also be obtained from confstr() using _CS_V7_ENV. 
                                        Posted by geoffclare at Mar 19, 2008 12:13
                                     |
| There is a lot of work required on this entry - as indicated by the comments.; The comments from Geoff about IFS are mostly valid - but the modern shells (including Solaris /bin/sh) reset IFS on startup and only pay attention to changes that you make in the script.  So, the 'may have issues' example would have to include an assignment to IFS.  Of course, if the system() function invokes the command processor specified by $SHELL then there's another bag'o'worms to deal with.
Conflating the value of $HOME with the entry in the password database is a common mistake -- the two need not be the same.  Further, ~ and ~username do not necessarily equate:
[!note]
$ echo ~ ~jleffler
/work1/jleffler /u/jleffler
$

The value of ~ corresponds to $HOME; the value of ~jleffler corresponds to the value in the password database.  I usually set my home directory off the NFS auto-mounted directory specified in the password database onto a local file system.  It means I have an incredibly complex (possibly over-complex) system for configuring my environment.  Almost all programs work correctly - taking $HOME to mean what I said.  I do work with some that have a fixation that my home directory must be the value in the password database - they are a nuisance.
Suffice to say, this recommendation is not yet ready for prime time. 
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 19, 2008 15:34
\| \|
Not all modern shells reset IFS. For example, dash does not, and dash is used as /bin/sh by default on Ubuntu.; (Note that I haven't checked /bin/sh on an Ubuntu system - I checked /bin/dash on Debian etch. It's possible Ubuntu might have changed dash.)
Also, system() and popen() never use the shell specified by $SHELL. If they did, lots of existing uses would break for csh users, e.g. a simple popen("some_command 2\>&1", "r").
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 20, 2008 11:54
\| \|
I believe all the issues are addressed now.
Another compliant solution could be created to illustrate the discussed `_CS_V7_ENV` if there is time, but this is not critical, since there is not yet a system on which such an example could be tested.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 27, 2008 18:03
\| \|
Yes, my comments have all been addressed (except the code still had the #include of paths.h, which I have fixed)
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 28, 2008 11:50
\| \|
In general, programs should be designed to ignore environment variables.; Unfortunately, many (POSIX) systems use them in surprising ways.  The worst example is the use of LD_LIBRARY_PATH to override the link-time and default search path for shared libraries, which allows a user to substitute his own library that does whatever he wants.  The only defense against this seems to be to bind the libraries into the executable image "statically", i.e. ld -Bstatic.  There should be a rule "Don't use shared/dynamically-linked libraries".  Unfortunately on Windows it is hard to avoid them.  
In the system("rm ~/.config") example, the comopliant solution is incomplete. At the ery least it should be followed by /**...use pwd-\>pw_dir to construct the path...**/
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 17, 2008 20:29
\| \|
The security issues with LD_LIBRARY_PATH should be addressed by the O/S.; Modern O/S's treat it specially when executing a set-uid or set-gid program.  For example, Solaris only uses "trusted" directories from it, and Linux ignores it altogether.  There may be older systems that don't have this protection, but secure programs should not be run on them anyway as they will have any number of well known security holes.
Static linking is a security risk.  Whenever a library has a security update, statically-linked programs remain vulnerable unless/until they are rebuilt with the new library.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 18, 2008 04:56
\| \|
\> In the system("rm ~/.config") example, the comopliant solution is incomplete. At the ery least it should be followed by /...use pwd-\>pw_dir to construct the path.../
Fixed.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 18, 2008 10:49
\| \|
With the addition of the code to call system() this example is now rather odd.; The NCCE used system() in order to have the shell expand the tilde (~) in the pathname.  With no tilde in the pathname in the compliant code, there is no need to use the shell and therefore no need to call system().  The code could just call unlink() on the pathname.
So I think either the compliant code should be changed to use unlink(), or some text should be added explaining that for this specific case it could just call unlink(), but the use of system() has been retained in order to show how to use it safely.  If system() is retained then some changes are needed to make the code safe:
-   It should sanitize the environment (or at least have a comment saying "sanitize the environment here ...").
-   It should ensure the shell does not interpret any special characters in pw_dir.  These are rare in home directory pathnames, but the code should still handle them.  One way would be to check that pw_dir does not contain any single quotes, and put single quotes around the %s.
-   It should check that system() returned 0.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 22, 2008 10:38
\| \|
Agreed. Still, a compliant code example that safely uses `system()` is worthwhile, even if it does functionality that could be more easily accomplished without it.
So I applied your suggestions to the system() coding example. I also added a coding example that uses unlink() instead.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2008 12:11
\| \|
This is what I remember as well. But I was surprised when I read CERT Advisory CA-1995-14, "Telnetd Environment Vulnerability" [CA-1995-14](/confluence/pages/createpage.action?spaceKey=c&title=CA-1995-14) that talks about exploiting the LD_PRELOAD environmental variable. I'm thinking this might be a special case. Do you think this issue was/is a real concern?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 22, 2008 17:03
\| \|
I think we got lost in the weeds on this one. The point of this rule is not to show how to delete a file, but the risks of relying on the shell and environmental variables.
The example "rm ~/.config" shows the problem relying on the value of HOME, and provides an easily understood security issue (deleting random files).
The problem with the example is that rm can be easily coded using existing library functions. We could invoke a more complex program, for example, mail, that can't be easily implemented.
The problem is with coming up with an example that doesn't seem too contrived...
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 22, 2008 17:17
\| \|
Can work on this tomorrow. A program that did "touch ~/foo" might be a suitable example.
But the two compliant examples show the difficulty of safely executing "rm ~/foo", and the suitibility of accomplishing the feat without using system()...that is, by using unlink().
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 22, 2008 17:39
\| \|
Yes, it a real concern, but not a special case.;  It is dealt with by following the recommendation on this page (sanitizing the environment before executing another program).
I think there may be two different issues getting mixed up here. My reply to Doug about LD_LIBRARY_PATH was specifically about the initial execution of the application (in relation to the question of whether the app should be built with static libraries to avoid the problem), not about what is in the environment when an application executes another program.  Protection during the initial execution is a matter for the O/S; protection when an application executes another program is a matter for the application author and is what this page is about.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 23, 2008 04:36
\| \|
Replaced `rm` example with a `grep` example, modelled after Emacs's grep command. This can't be done with exec(3) since user controls which grep cmd to use, and may us things like ~ for HOME.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 30, 2008 15:08
\| \|
The new grep example has a couple of major problems:
1.  Since the user can pass a pathname to grep, it allows the content of any file readable by the program to be seen (using "grep '.\*' /any/path").
2.  It does not have enough "bad" chars in the list.; It would need to include '$' to prevent "$(command ...)", '\|' to prevent piping, '&' to prevent "grep ... & other_command ...", and '\>' to prevent overwriting of files the program has write access to. Having '$' and '\|' in the list rather reduces the usefulness of the feature, as they are often used in \[e\]grep patterns.
I'm also not too keen on the way it silently changes the bad chars to spaces, thus executing a different command than the one the user requested.  It would be better if the code reported the presence of bad characters as an error and did not execute any command.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 01, 2008 07:34
\| \|
Added your extra bad chars to the reject list, and changed the code to 'handle bad-char error' rather than silently change the command. Your other points are difficult to change in the code (or maybe I'm just lazy ![](images/icons/emoticons/smile.svg), so I put disclaimers in the text around the example, noting how difficult it is to properly sanitize a shell command ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 01, 2008 11:19
\| \|
Spotted a couple more problems with the grep example:
It calls spc_sanitize_environment() to sanitize the environment, but that function does not alter the current environment, it creates a new one for use with execle() or execve(). One solution might be to do the sanitizing in the shell command. It would mean inserting some shell code in front of the supplied grep command, so it looks like:
``` java
unset IFS; PATH=$(command -p getconf PATH); env -i $(getconf V7_ENV) PATH="$PATH" TZ="$TZ" grep ...
```
The description says it "ensures that nothing is called except grep, fgrep, or egrep", but the code actually allows other commands as well (anything consisting of a single character followed by "grep"). This includes pgrep (probably harmless) and ngrep (maybe not so harmless).
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 09, 2008 04:51
\| \|
Added a paragraph claiming that if your system has 'dangerous' programs like `ngrep` available (mine doesn't), you may wish to check and disallow execution of such commands. I know this isn't particularly satisfying, but if we explicitly restricted the system to grep, fgrep, and egrep, (or some similar subset), we lose more and more justification for using system() instead of exec\*\*().
Good catch wrt spc_sanitize_environment. Actually the function is currently unusable, as it does not provide access to `new_env`. So I replaced the funcall with a comment saying 'get this done'.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 09, 2008 16:15
\| \|
Good point regarding usability of spc_sanitize_environment().; I have changed it to return new_environ.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 12, 2008 07:35
\| \|
is it just me, or does all of this only matter if the program is running with higher privileges than the caller? (setuid/setgid) we should probably make that more clear, as it stands, this rule implies that all programs should rehash their environment before doing anything useless (which kind of defeats the whole purpose of having an environment...)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 03, 2008 09:56
\| \|
this might make a good sidebar
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 13, 2008 10:41
\| \|
alexv sez:
justin/shaun/I just checked this on a eeePC that runs eeeXUbuntu and /bin/sh-\>dash and it does not in fact reset IFS (so this comment is confirmed)
![](images/icons/contenttypes/comment_16.png) Posted by jpincar at Jun 13, 2008 11:19
\| \|
this might make a good sidebar
![](images/icons/contenttypes/comment_16.png) Posted by jpincar at Jun 13, 2008 11:22
\| \|
Having a Rose checker algorithm that relies on `clearenv()` does not seem very useful, since `clearenv()` is non-standard.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jul 14, 2008 12:05
\| \|
My (linux) clearenv manpage sez:
> CONFORMING TO Various Unix variants (DG/UX, HP-UX, QNX, ...). POSIX.9 (bindings for FORTRAN77). POSIX.1-1996  
> did not accept clearenv() and putenv(3), but changed its mind and scheduled these functions for  
> some later issue of this standard (cf. B.4.6.1). However, POSIX.1-2001 only adds putenv(3), and  
> rejected clearenv().

I'll agree a non-standard function is a poor requirement in a ROSE checker...got any better suggestions?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 14, 2008 13:18
\| \|
If I had anything better to suggest, I would have put it in the original comment.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jul 15, 2008 04:57
\| \|
It looks like the provided implementation of clearenv() will never terminate. The loop condition checks to see if env[0](/confluence/pages/createpage.action?spaceKey=c&title=0)!=0, which if true once will always be true since the value of env[0](/confluence/pages/createpage.action?spaceKey=c&title=0) is never modified in the loop.
It looks like clearenv() should be implemented as:
> [!note]
>
>     extern char **environ;
>
>     int clearenv(void) {
>       static char *namebuf = NULL;
>       static size_t lastlen = 0;
>       unsigned int i = 0;
>       
>       while (environ != NULL && environ[i] != NULL) {
>         size_t len = strcspn(environ[i], "=");
>         if (len == 0) {
>           /* Handle empty variable name (corrupted environ[]) */
>         }
>         if (len > lastlen) {
>           namebuf = realloc(namebuf, len+1);
>           if (namebuf == NULL) {
>             /* Handle error */
>           }
>           lastlen = len;
>         }
>         memcpy(namebuf, environ[i], len);
>         namebuf[len] = '\0';
>         if (unsetenv(namebuf) == -1) {
>           /* Handle error */
>         }
>         i++;
>       }
>       return 0;
>     }

![](images/icons/contenttypes/comment_16.png) Posted by sayre at Jan 16, 2009 16:35
\| \|
No, the loop does terminate. The `unsetenv()` call near the end of the loop should (theoretically) delete environ[0](/confluence/pages/createpage.action?spaceKey=seccode&title=0); thus the loop repeats untio `environ` is empty.
I'm a bit concerned that the program assumes `environ` is actually updated by the `unsetenv` function...it is reminiscent of [ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it](ENV31-C_%20Do%20not%20rely%20on%20an%20environment%20pointer%20following%20an%20operation%20that%20may%20invalidate%20it). Does the POSIX standard guarantee that `environ` is updated by `unsetenv` and the other environment-related functions? For that matter, could one mauipulate the enviornment by manipulating `environ` directly?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 16, 2009 18:15
\| \|
> Does the POSIX standard guarantee that `environ` is updated by `unsetenv` and the other environment-related functions?

Yes it does (except for `getenv()` of course, since it only "reads" from `environ`). However, if the application has directly modified `environ` or the pointers to which it points, the behaviour of these functions is undefined.
> For that matter, could one mauipulate the enviornment by manipulating `environ` directly?

Yes, applications can do that, but having done so they can't call `getenv()` (or the other environment-related functions) as its behaviour is undefined for the reason I gave above.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Jan 17, 2009 04:35
\| \|
This guideline is stated to be a more specific instance of [STR02-C. Sanitize data passed to complex subsystems](STR02-C_%20Sanitize%20data%20passed%20to%20complex%20subsystems)
That guideline has the following "Automated Detection" section:
Fortify SCA Version 5.0 can detect violations of this rule.
Klocwork Version 8.0.4.16 can detect violations of this rule with the NNTS.TAINTED and SV.TAINTED.INJECTION checkers.
Do these checkers also identify violations of this guideline?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 16, 2009 11:20
\| \|
I find the **Compliant Solution (POSIX, ls)** rather contrived. It would be error-prone for a process to clear its own environment before invoking `system()`. A safer approach would be to invoke `fork()` followed by a call to `execve()` with the absolute pathname of the program and a sanitized environment.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 13, 2010 18:38
\|
