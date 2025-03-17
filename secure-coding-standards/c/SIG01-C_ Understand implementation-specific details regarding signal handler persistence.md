The `signal()` function has [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) behavior and behaves differently on Windows, for example, than it does on many UNIX systems.
The following code example shows this behavior:
``` java
#include <stdio.h>
#include <signal.h>
volatile sig_atomic_t e_flag = 0;
void handler(int signum) {
  e_flag = 1;
}
int main(void) {
  if (signal(SIGINT, handler) == SIG_ERR) {
    /* Handle error */
  }
  while (!e_flag) {}
  puts("Escaped from first while ()");
  e_flag = 0;
  while (!e_flag) {}
  puts("Escaped from second while ()");
  return 0;
}
```
Many UNIX (and UNIX-like) systems automatically reinstall signal handlers upon handler execution, meaning that the signal handler defined by the user is left in place until it is explicitly removed. For example, when this code is compiled with GCC 3.4.4 and executed under Red Hat Linux, `SIGINT` is captured both times by `handler`:
``` java
% ./test
^C
Escaped from first while ()
^C
Escaped from second while ()
%
```
When a signal handler is installed with the `signal()` function in Windows and some UNIX systems, the default action is restored for that signal after the signal is triggered. This means that signal handlers are not automatically reinstalled. For example, when this code is compiled with Microsoft Visual Studio 2005, version 8.0, only the first `SIGINT` is captured by `handler`:
``` java
> test.exe

^C
Escaped from first while ()
^C
>

```
The second `SIGINT` executes the default action, which is to terminate program execution.
Different actions must be taken depending on whether or not the application requires signal handlers to be persistent.
# Persistent Handlers
Asynchronous signals may originate from malicious actors external to the process. Consequently, [vulnerabilities](http://BB.%20Definitions#vulnerability) may exist if the signal-handler-persistence behavior is inconsistent with the developer's expectations, such as when the developer expects the signal handler to persist but it does not.
## Noncompliant Code Example
This noncompliant code example fails to persist the signal handler on Windows platforms and on those UNIX systems where handlers are not persistent by default:
``` c
void handler(int signum) {
  /* Handle signal */
}
```
## Noncompliant Code Example
A common approach to create persistent signal handlers is to call `signal()` from within the handler itself, consequently *unresetting* the reset signal:
``` c
void handler(int signum) {
  if (signal(signum, handler) == SIG_ERR) {
    /* Handle error */
  }
  /* Handle signal */
}
```
Unfortunately, this solution still contains a race window, starting when the host environment resets the signal and ending when the handler calls `signal()`. During that time, a second signal sent to the program will trigger the default signal behavior, defeating the persistent behavior. (See [SIG34-C. Do not call signal() from within interruptible signal handlers](SIG34-C_%20Do%20not%20call%20signal__%20from%20within%20interruptible%20signal%20handlers).)
A secure solution must prevent the environment from resetting the signal in the first place, guaranteeing persistence. Unfortunately, Windows does not provide a secure solution to this problem.
## Compliant Solution (POSIX)
The POSIX `sigaction()` function assigns handlers to signals in a manner similar to the C `signal()` function but also allows signal-handler persistence to be controlled via the `SA_RESETHAND` flag. (Leaving the flag clear makes the handler persistent.)
``` c
/* 
 * Equivalent to signal(SIGUSR1, handler) but makes
 * signal persistent. 
 */
struct sigaction act;
act.sa_handler = handler;
act.sa_flags = 0;
if (sigemptyset(&act.sa_mask) != 0) {
  /* Handle error */
}
if (sigaction(SIGUSR1, &act, NULL) != 0) {
  /* Handle error */
}
```
POSIX recommends `sigaction()` and deprecates `signal()`. Unfortunately, `sigaction()` is not defined in the C Standard and is consequently not as portable a solution.
# Nonpersistent Handlers
Errors may also occur when the developer expects the default action to be restored for a signal but the signal handler persists instead.
## Noncompliant Code Example (UNIX)
This noncompliant code example fails to reset the signal handler to its default behavior on systems where handlers are persistent by default:
``` c
void handler(int signum) {
  /* Handle signal */
}
```
## Compliant Solution (UNIX and Windows)
A C-compliant solution to reset the handler on a UNIX system is to rebind the signal to the default handler in the first line of the handler itself. Windows, however, automatically resets handlers to their default behavior.
``` c
void handler(int signum) {
#ifndef WINDOWS
  if (signal(signum, SIG_DFL) == SIG_ERR) {
    /* Handler error */
  }
#endif
  /* Handle signal */
}
```
With the compliant solution for UNIX, no race condition occurs that can be [exploited](BB.-Definitions_87152273.html#BB.Definitions-exploit) by an attacker sending a second signal. This is because a second signal sent to the handler, before the latter calls `signal(signum, SIG_DFL)`, will only cause the handler to restart and call `signal()` anyway.
This solution is an exception to [SIG34-C. Do not call signal() from within interruptible signal handlers](SIG34-C_%20Do%20not%20call%20signal__%20from%20within%20interruptible%20signal%20handlers).
## Compliant Solution (POSIX)
The POSIX `sigaction()` function assigns handlers to signals in a manner similar to the C `signal()` function but also allows signal-handler persistence to be controlled via the `SA_RESETHAND` flag. (Setting the flag makes the handler nonpersistent.)
``` c
/* 
 * Equivalent to signal(SIGUSR1, handler) but makes
 * signal nonpersistent.
 */
struct sigaction act;
act.sa_handler = handler;
act.sa_flags = SA_RESETHAND;
if (sigemptyset(&act.sa_mask) != 0) {
  /* Handle error */
}
if (sigaction(SIGUSR1, &act, NULL) != 0) {
  /* Handle error */
}
```
## Risk Assessment
Failure to understand implementation-specific details regarding signal-handler persistence can lead to [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| SIG01-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.SIGNAL | Use of signal |
| Compass/ROSE |  |  | Could detect possible violations by flagging any signal handler that calls signal() to (re)assert itself as the handler for its signal |
| Helix QAC | 2024.4 | C5020 |  |
| LDRA tool suite | 9.7.1 | 97 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-SIG01-a | The signal handling facilities of <signal.h> shall not be used |
| PC-lint Plus | 1.4 | 586 | Assistance provided: reports use of the signal function |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+SIG01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID SIG01-CPP. Understand implementation-specific details regarding signal handler persistence |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152179) [](../c/Rec_%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152106)
## Comments:

|  |
| ----|
| POSIX specifies this as implementation defined:
When a signal occurs, and func points to a function, it is implementation defined whether the equivalent of a:
signal(sig, SIG_DFL));

is executed or the implementation prevents some implementation-defined set of signals (at least include *sig*) from ocurring until the current signal handler has completed.
I suspect there are other platforms from Microsoft Windows that deregister the signal handler.
Does it make sense to add an example where deregistering is the expected/desired behavior? I'm having problem with coming up with a reasonable example, but suspect they exist.
![](images/icons/contenttypes/comment_16.png) Posted by hburch at Jun 07, 2007 14:00
\| \|
Amongst other things, the POSIX standard says that the `signal()` interface is deprecated (use `sigaction()` instead), and its behaviour is undefined in a process that uses threads.; Many (older) Unix implementations reset the signal handler; you only have to look at Kernighan & Pike "The UNIX Programming Environment" or  Kernighan & Ritchie "The C Programming Language" to see that.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 20, 2008 01:30
\| \|
On systems that reset the signal to SIG_DFL on entry to the signal handler (and don't mask it during execution of the handler), calling signal() at the beginning of the handler to reinstate the handler does **not** make the handler safe.; There is still a timing window between entry to the signal handler and the call to signal() during which delivery of the signal would terminate the process.
I suggest that there should be a rule (yes a rule, not just a recommendation) that signal() should never be used to set up signal handling functions, only to set signals to SIG_DFL or SIG_IGN. (Although I suppose there could be an exception for the rare cases where resetting to SIG_DFL after receipt of one signal is actually desired, as per the "Non-Persistent Handlers" section on this page.)
All of the other pages that deal with signal() should be reworked to have separate compliant solutions for POSIX and Windows.  The POSIX code would use sigaction().  Presumably Windows also has something safer than signal().
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 08, 2008 10:17
\| \|
The one problem with sigaction(2) is that it is not C99-compliant, and is not supported by Windows. So I added POSIX solutions using sigaction(2), but we need to leave in the original code samples utilizing signal(), and note the race condition you cite. Even for cases like Windows, where the non-persistent race condition seems unavoidable.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 10, 2008 13:57
\| \|
Are you sure the Windows API doesn't have an alternative way of setting up signal handlers that doesn't reset the signal to default when the handler is called?; If it were true, then how does Windows SFU implement the sigaction() function?  I suppose it could be using an undocumented kernel interface.  Or maybe "signals" in SFU are not the same thing as the "signals" in the Windows API.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Apr 11, 2008 05:05
\| \|
Dunno if this has been obsolesced, but MS doesn't support `sigaction()` functionality using signals:
<http://msdn2.microsoft.com/en-us/library/ms811896.aspx#ucmgch09_topic3>
They recommend you use Windows Objects or Windows Messenging to achieve the functionality of `sigaction()`.
I suppose the Right Thing to do here is to add the above link to SIG01 saying "Windows uses do this instead", but I don't fee confident doing this given how little we know wrt the security of Windows Objects or Windows Messenging...those are out of scope of these rules (not complying with C99 or POSIX).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 14, 2008 10:05
\| \|
Why is this rule so redundant? The second half is just a rehash of the first half with the same examples... Can we trim this down at all?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 15, 2008 09:45
\| \|
You can give it a shot.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 15, 2008 10:04
\| \|
Under Non-Persistent Handlers, I merged the Compliant solution for Windows with that for Unix. The CS for Unix was already using a preprocessor define to;detect the OS - so I combined them.
![](images/icons/contenttypes/comment_16.png) Posted by abhi at Apr 17, 2008 05:15
\| \|
Ale Contenti @ Microsoft sez:
Interesting. ![](images/icons/emoticons/smile.svg) I didn't know about the difference. I guess the C Std leaves this unspecified, right? The main issue I see here is about code portability, at least with the Windows CRT. I mean, executing the default signal handler is pretty safe (but maybe something you don't want). On \*nix, if you're used to the Windows CRT, you get a possibly unsafe behavior, IMO.
I think it would be interesting to ask the C Std if it's possible to be explicit about the behavior with a flag set (or maybe just read) at runtime, so that different programs can act accordingly. Anyway, even without this flag, the portable option is to assume that the handler will be reset after each call. The MSDN docs about signal describe this in detail, I think.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 17, 2008 12:28
\| \|
The #ifndef WINDOWS is unnecessary.; Even though the reset is redundant, it is harmless.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 18, 2008 11:36
\| \|
while technically true, [MSC12-C. Detect and remove code that has no effect](/confluence/pages/createpage.action?spaceKey=c&title=MSC12-C.+Detect+and+remove+code+that+has+no+effect) tells us we shouldn't compile the reset in on Unix systems
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 19, 2008 16:47
\| \|
We should cross-reference all NCCE that violate SIG34-C, if we are going to keep that rule.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at May 20, 2008 08:45
\| \|
Doesn't our Windows compliant solution violate SIG34-C as well because of the race window? Or are windows signal handlers non-interruptible?
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 20, 2008 10:08
\| \|
Huh? The Windows code doesn't call signal() in the handler.
The Unix code in the same CS does, but the call is allowed by exception SIG34-EX1.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at May 20, 2008 11:50
\| \|
nvm, I saw `ifndef` as `ifdef`... so there is no way to provide a Windows solution in the Persistent section because of SIG34? perhaps we should cite that
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 20, 2008 11:58
\| \|
Just checked. No NCCEs in the Signals section violate SIG34-C, except for those in this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2008 12:46
\|
