Some C standard library functions are not guaranteed to be [reentrant](BB.-Definitions_87152273.html#BB.Definitions-reentrant) with respect to threads. Functions such as `strtok()` and `asctime()` return a pointer to the result stored in function-allocated memory on a per-process basis. Other functions such as `rand()` store state information in function-allocated memory on a per-process basis. Multiple threads invoking the same function can cause concurrency problems, which often result in abnormal behavior and can cause more serious [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), such as [abnormal termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination), [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service), and data integrity violations.
According to the C Standard, the library functions listed in the following table may contain data races when invoked by multiple threads.

| Functions | Remediation |
| ----|----|
| rand(), srand() | MSC30-C. Do not use the rand() function for generating pseudorandom numbers |
| getenv(), getenv_s() | ENV34-C. Do not store pointers returned by certain functions |
| strtok() | strtok_s();in C11 Annex K
strtok_r() in POSIX |
| strerror() | strerror_s() in C11 Annex Kstrerror_r() in POSIX |
| asctime(), ctime(),localtime(), gmtime() | asctime_s(), ctime_s(), localtime_s(), gmtime_s() in C11 Annex K |
| setlocale() | Protect multithreaded access to locale-specific functions with a mutex |
| ATOMIC_VAR_INIT, atomic_init() | Do not attempt to initialize an atomic variable from multiple threads |
| tmpnam() | tmpnam_s();in C11 Annex K
tmpnam_r() in POSIX |
| mbrtoc16(), c16rtomb(),mbrtoc32(), c32rtomb() | Do not call with a null;mbstate_t * argument  |

Section 2.9.1 of the *Portable Operating System Interface (POSIX<sup>®</sup>), Base Specifications, Issue 7* \[[IEEE Std 1003.1:2013](AA.-Bibliography_87152170.html#AA.Bibliography-IEEEStd1003.1-2013)\] extends the list of functions that are not required to be thread-safe.
## Noncompliant Code Example
In this noncompliant code example, the function `f()` is called from within a multithreaded application but encounters an error while calling a system function. The `strerror()` function returns a human-readable error string given an error number.
The C Standard, 7.26.6.3 paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], specifically states that `strerror()` is not required to avoid data races.
> The strerror function is not required to avoid data races with other calls to the strerror function.

An [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) could write the error string into a static array and return a pointer to it, and that array might be accessible and modifiable by other threads.
``` c
#include <errno.h>
#include <stdio.h>
#include <string.h>
void f(FILE *fp) {
  fpos_t pos;
  errno = 0;
  if (0 != fgetpos(fp, &pos)) {
    char *errmsg = strerror(errno);
    printf("Could not get the file position: %s\n", errmsg);
  }
}
```
This code first sets `errno` to 0 to comply with [ERR30-C. Take care when reading errno](ERR30-C_%20Take%20care%20when%20reading%20errno). 
## Compliant Solution (Annex K, `strerror_s()`) 
This compliant solution uses the `strerror_s()` function from Annex K of the C Standard, which has the same functionality as `strerror()` but guarantees thread-safety:
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <errno.h>
#include <stdio.h>
#include <string.h>
enum { BUFFERSIZE = 64 };
void f(FILE *fp) {
  fpos_t pos;
  errno = 0;
  if (0 != fgetpos(fp, &pos)) {
    char errmsg[BUFFERSIZE];
    if (strerror_s(errmsg, BUFFERSIZE, errno) != 0) {
      /* Handle error */
    }
    printf("Could not get the file position: %s\n", errmsg);
  }
}
```
Because Annex K is optional, `strerror_s()` may not be available in all implementations. 
## Compliant Solution (POSIX, `strerror_r()`)
This compliant solution uses the POSIX `strerror_r()` function, which has the same functionality as `strerror()` but guarantees thread safety:
``` c
#include <errno.h>
#include <stdio.h>
#include <string.h>
enum { BUFFERSIZE = 64 };
void f(FILE *fp) {
  fpos_t pos;
  errno = 0;
  if (0 != fgetpos(fp, &pos)) {
    char errmsg[BUFFERSIZE];
    if (strerror_r(errno, errmsg, BUFFERSIZE) != 0) {
      /* Handle error */
    }
    printf("Could not get the file position: %s\n", errmsg);
  }
}
```
Linux provides two versions of `strerror_r()`, known as the XSI-compliant version and the GNU-specific version. This compliant solution assumes the XSI-compliant version, which is the default when an application is compiled as required by POSIX (that is, by defining `_POSIX_C_SOURCE` or `_XOPEN_SOURCE` appropriately). The` strerror_r()` manual page lists versions that are available on a particular system.
## Risk Assessment
Race conditions caused by multiple threads invoking the same library function can lead to [abnormal termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) of the application, data integrity violations, or a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON33-C | Medium | Probable | High | P4 | L3 |

### Related Vulnerabilities
Search for [vulnerabilities](http://BB.%20Definitions#vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON33-C).
## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| CodeSonar | 8.3p0 | BADFUNC.RANDOM.RANDBADFUNC.TEMP.TMPNAM
BADFUNC.TTYNAME | Use of rand (includes check for uses of srand())Use of tmpnam (includes check for uses of tmpnam_r())
Use of ttyname |
| Compass/ROSE |  |  | A;module written in Compass/ROSE can detect violations of this rule |
| Cppcheck Premium | 24.11.0 | premium-cert-con33-c |  |
| Helix QAC | 2024.4 | C5037C++5021DF4976, DF4977 |  |
| Klocwork | 2024.4 | CERT.CONC.LIB_FUNC_USE |  |
| LDRA tool suite | ;9.7.1 | 44 S | Partially Implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-CON33-a | Avoid using thread-unsafe functions |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON33-C | Checks for data race through standard library function call (rule fully covered) |

## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | ERR30-C. Set errno to zero before calling a library function known to set errno, and check errno only after the function returns a value indicating failure | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | CON00-CPP. Avoid assuming functions are thread safe unless otherwise specified | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-330 | 2017-06-28: CERT: Partial overlap |
| CWE 2.11 | CWE-377 | 2017-06-28: CERT: Partial overlap |
| CWE 2.11 | CWE-676 | 2017-05-18: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-330 and CON33-C
Independent( MSC30-C, MSC32-C, CON33-C)
Intersection( CWE-330, CON33-C) =
-   Use of rand() or srand() from multiple threads, introducing a race condition.
CWE-330 – CON33-C =
-   Use of rand() or srand() without introducing race conditions
-   Use of other dangerous functions
CON33-C – CWE-330 =
-   Use of other global functions (besides rand() and srand()) introducing race conditions
### CWE-377 and CON33-C
Intersection( CWE-377, CON33-C) =
-   Use of tmpnam() from multiple threads, introducing a race condition.
CWE-377 – CON33-C =
-   Insecure usage of tmpnam() without introducing race conditions
-   Insecure usage of other functions for creating temporary files (see CERT recommendation FIO21-C for details)
CON33-C – CWE-377 =
-   Use of other global functions (besides tmpnam()) introducing race conditions
### CWE-676 and CON33-C
-   Independent( ENV33-C, CON33-C, STR31-C, EXP33-C, MSC30-C, ERR34-C)
-   CON33-C lists standard C library functions that manipulate global data (e.g., locale()), that can be dangerous to use in a multithreaded context.
-   CWE-676 = Union( CON33-C, list) where list =
-   Invocation of the following functions without introducing a race condition:
-   rand(), srand(, getenv(), getenv_s(), strtok(), strerror(), asctime(), ctime(), localtime(), gmtime(), setlocale(), ATOMIC_VAR_INIT, atomic_init(), tmpnam(), mbrtoc16(), c16rtomb(), mbrtoc32(), c32rtomb()
-   Invocation of other dangerous functions
## Bibliography

|  |  |
| ----|----|
| [IEEE Std 1003.1:2013] | Section 2.9.1, "Thread Safety" |
| [ISO/IEC 9899:2024] | Subclause 7.26.6.3, "The strerror Function"; |
| [Open Group 1997b] | Section 10.12, "Thread-Safe POSIX.1 and C-Language Functions" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152069) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152300)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>I think this can be written as a C1X rule, and not as a POSIX rule. I think all that is needed is to replace the pthreads with C1X threads. In fact, we should probably just go ahead and create a new section on concurrency.</p>
<p>I think the first paragraph with this rule should start with the general description of the project. Then, I think the emphasis on <code>rand()</code> including the quote is too much, because this is just one of many functions with exactly the same problem, right?</p>
<p>In the noncompliant example, I would like to see a little better description of why the rand function is not required to avoid data races (presumably because it needs to access a global variable)?</p>
<p>The "it is possible for them to result in more serious vulnerabilities" is sort of vague. Perhaps you can provide a "such as..."</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Nov 06, 2009 04:58
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I have tried to incorporate the suggestions in the rule.<br />
Do I need to change pthreads in the NCCE and CS code and use library functions and macros in threads.h as per Section 7.24 Threads in N1401-C1X ?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by amahendr at Nov 06, 2009 16:30
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>[comment updated - the original version had some muddled thinking about rand_r()]</p>
<p>The code shown in the compliant solution does not solve the problem. Although not likely for rand(), an implementation can have thread safe functions which access the same internal data as a non-thread-safe function, but the thread safe functions protect the data with an internal mutex. This means that not only can an application not call the non-thread-safe function from different threads at the same time, it can't call the non-thread-safe function and <em>any other function</em> at the same time. The proper solution is not to call non-thread-safe functions at all in multithreaded programs (except perhaps in the initial thread before creating any more threads).</p>
<p>I don't know whether C1X has rand_r(). If it doesn't, then perhaps this should remain a POSIX rule and the compliant solution should show the use of rand_r(). Alternatively change the examples to be based on a function for which C1X does have an _r equivalent.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 09, 2009 06:07
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The CS code does solve the problem, but only if no other (thread-unsafe) functions call rand(), or access its global data. Which the CS should state. C99 guarentees that no other library functions act as if they call rand(), so theoretically you can build thread-safe programs using a mutex on rand().</p>
<p>C1x does not have rand_r().</p>
<p>Unfortunately, the problem is deeper, because usage of rand() violates <a href="MSC30-C_%20Do%20not%20use%20the%20rand__%20function%20for%20generating%20pseudorandom%20numbers">MSC30-C. Do not use the rand() function for generating pseudorandom numbers</a>. That rule recommends POSIX random() (and a similar function for Windows). But random() is not thread-safe. GNU provides a random_r() function, but I could not get it to work (in my last 5 minutes at work <img src="images/icons/emoticons/smile.svg" /></p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Nov 09, 2009 17:56
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The fact that C99 guarantees no other library functions act as if they call rand() does not make it safe to call rand() at the same time as thread-safe functions. The following is a contrived example, but hopefully it serves to illustrate the problem.</p>
<p>Suppose an implementation of rand() has a trace mode that can be activated by setting an environment variable, whereby it writes information about each call to stderr. Since rand() is not thread safe it can write to stderr without locking the stream. If one thread calls rand() at the same time as another thread is writing to stderr, rand() will update the stream internals even though they are locked by the other thread.</p>
<p>Does C1X have strerror_r()? That would be a good choice for the examples.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 10, 2009 04:03
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>C1X does not support strerror_r(), but POSIX.1-2001 does. So I've made NCCE/CS using strerror(). I found the following problems with other functions:</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |
| ----|----|
|  rand()      |  violates MSC30-C                                          |
|  getenv()    |  no _r equivalent                                          |
|  strtok()    |  strtok_r(3) discourages use                               |
|  asctime()   |  POSIX.1-2008 marks asctime() and asctime_r() as obsolete  |
|  ctime()     |  Ditto                                                     |
|  strerror()  |  Specified in POSIX.1-2001. Also a GNU extension           |</code></pre>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Nov 20, 2009 13:27
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The thread-safe version of strerror() also has problems of its own. POSIX defines strerror_r() to return an integer (0 = success, -1 = failure + changes to errno), whereas Linux returns the formatted string. Rule ERR30-C partially addresses this (i.e. set errno to 0 prior to calling strerror_r()), but also by this same rule we shouldn't be checking the value of errno unless we first check the response from strerror_r().</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by eric.decker@itt.com at Nov 24, 2009 19:18
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>POSIX strerror_r() returns 0 on success or an error number on failure. It does not set errno.</p>
<p>Linux (glibc) has two versions of strerror_r(), one conforming and one not. You get the conforming one if you compile applications in the way POSIX requires (i.e. by defining _POSIX_C_SOURCE or _XOPEN_SOURCE appropriately).</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 25, 2009 04:38
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The XSI version of strerror_r() does set errno. The GNU version of sterror_r() does not.</p>
<p>I've made both NCCCE &amp; CS compliant with ERR30-C and xrefed it. Also added a note about the XSI vs GNU versions of strerror_r() on Linux.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Nov 25, 2009 10:16
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>This is an interesting table in that I think we need to deal with each function in this table in some way. If we have a guideline that says "don't use it" that effectively deals with it.</p>
<p>as you say, MSC30-C. Do not use the rand() function for generating pseudorandom numbers, prohibits the use of rand() (for any purpose really)</p>
<p>asctime() and ctime() are both listed as obsolescent in "MSC34-C. Do not use deprecated or obsolescent functions"</p>
<p>There is an interesting article on thread safety of {{getenv()} at: <a href="http://blogs.sun.com/pgdh/date/20050614">http://blogs.sun.com/pgdh/date/20050614</a></p>
<p>So we currently have a POSIX only solution for <code>strerror()</code> but I think we should also have one or more C1X solutions for <code>getenv()} and {{strerror()</code> that use the C1X mtx_lock() function defined in Section 7.24.4.3 of the current working draft and possibly other C1X based solutions.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Nov 25, 2009 11:22
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I like this, but I also like Geoff's suggestion of defining <code>_POSIX_C_SOURCE</code> or <code>_XOPEN_SOURCE</code> appropriately.</p>
<p>There is currently a slight disconnect with the following statement:</p>
<p>Check your <code>strerror_r()</code> man page to see which version is available on your system.</p>
<p>One suggests that you can always do this, and one suggest that it is implementation defined.</p>
<p>Which is correct?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Nov 25, 2009 11:31
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><blockquote>
<p>The XSI version of strerror_r() does set errno.</p>
</blockquote>
<p>Please read the standard. Last paragraph under RETURN VALUE:</p>
<blockquote>
<p>Upon successful completion, strerror_r() shall return 0. Otherwise, an error number shall be returned to indicate the error.</p>
</blockquote>
<p>Perhaps what confused you is that strerror_r() has an ERANGE error listed in the ERRORS section, and you assumed that this section always means errno is set to the listed value. You have to read the RETURN VALUE section to see how the errors are indicated. For strerror_r() the error number is in the return value of the function. It is NOT required to set errno.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 25, 2009 12:10
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>My Linux manpage <code>strerror(3)</code> says (in the last paragraph of RETURN VALUE section):</p>
<p>The XSI-compliant strerror_r() function returns 0 on success; on error, -1 is returned and errno is set to indicate the error.<br />
{quote]</p>
<p>So yes I am definitely confused :-S It's also not the first time we've found inconsistent documentation wrt <code>errno</code>.</p>
<p>Howeve, we don't need to rely on <code>errno</code> for this rule, we can just check the return value instead. If a function both sets errno and returns an out-of-band error indicator (such as NULL), we prefer checking the indicator, as it is more reliable and harder to ignore (and better documented). This is all addressed in ERR30-C.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Nov 25, 2009 13:01
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><blockquote>
<p>My Linux manpage strerror(3) says ...</p>
</blockquote>
<p>That's either a mistake in the man page, or a bug in glibc. Clearly the intention is for the "XSI" version of strerror_r() to conform to the standard. If it doesn't, then presumably whoever wrote it misread the standard.</p>
<p>Does your Linux system have an up to date glibc? Maybe it's been fixed since the version you have.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 25, 2009 13:21
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I think the simplest solution would be to change "which version is available" to "which versions are available" or "which version(s) are available".</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 26, 2009 04:02
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>FYI I have submitted a defect report to the Austin Group regarding the thread safety of getenv() in POSIX.</p>
<p><a href="http://austingroupbugs.net/view.php?id=188">http://austingroupbugs.net/view.php?id=188</a></p>
<p>If this change is accepted, then I would hope that C1X will follow suit.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Nov 26, 2009 05:56
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I'm a big fan of easy. 8^) Done.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Nov 26, 2009 11:49
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Let me know if the change is accepted, and of course, Nick Stoughton. I would be happy to bring a proposal to Italy recommending this change.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Nov 26, 2009 11:51
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The Austin Group decided to make a bigger change: disallow copying to an internal buffer. The thinking here is that since POSIX requires the environment variables to be available via environ[], there is no reason why getenv() can't return a pointer to the actual environment instead of a copy.</p>
<p>The thread-safety of getenv() is affected the same way by this change as by the original request (to require per-thread buffers if copying is done), but since the C Standard does not have environ[] I imagine it would be less likely to be accepted by the C1X committee. You (or Nick) might still consider proposing per-thread buffers for C1X.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Dec 11, 2009 06:58
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>There are still a couple of problems with this rule:</p>
<ul>
<li>fopen() is not guaranteed to set errno in C11. (it is guaranteed in POSIX).</li>
</ul>
<ul>
<li>The first CS still possesses a race window on errno. The window starts on the call to fopen() and ends at the beginning of the call to strerror_r(). This is because in C99 (and presumably POSIX), errno is static. So it can be modified by another thread during the race window. In C11 errno is thread-local, so the 2nd CS has no such race window.</li>
</ul>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jan 22, 2013 16:47
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I've addressed these issues.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jan 23, 2013 09:22
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>There is no race window on errno in POSIX.  See XSH 2.3 Error Numbers:</p>
<p>"For each thread of a process, the value of <em>errno</em> shall not be affected by function calls or assignments to <em>errno</em> by other threads."</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by geoffclare at Jan 30, 2013 10:53
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Oops, you're right. So the strerror_r code is compliant, and we don't need the mutex example. Fixed.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jan 31, 2013 11:07
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I think this note:</p>
<p>Section 2.9.1 of the <em>System Interfaces</em> volume of <a href="https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-POSIX.1-2008">POSIX.1-2008</a> has a much longer list of functions that are not required to be thread-safe.</p>
<p>Might be misconstued to mean "list of C Standard " functions.  If not, this should be restated more clearly, e.g.:</p>
<p>Section 2.9.1 of the <em>System Interfaces</em> volume of <a href="https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AA.Bibliography-POSIX.1-2008">POSIX.1-2008</a> constains a list of POSIX functions that are not required to be thread-safe.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Oct 24, 2013 11:19
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Are there no Standard C functions in the POSIX list? Sorry, don't have a copy of POSIX.1. If there are Standard C functions in the POSIX list. Maybe the words should be:</p>
<p>Section 2.9.1 of the Systems Interface volume of POSIX.1-2008 has a list of additional functions that are not required to be thread-safe.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by bluepilot at Oct 24, 2013 12:06
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p> </p>
<p>You can find all this up on the Open Group website: <a href="http://pubs.opengroup.org/onlinepubs/9699919799/toc.htm">http://pubs.opengroup.org/onlinepubs/9699919799/toc.htm</a> </p>
<p>here are the functions</p>
<h4 id="CON33C.Avoidraceconditionswhenusinglibraryfunctions-2.9.1Thread-Safety">2.9.1 Thread-Safety</h4>
<p>All functions defined by this volume of POSIX.1-2008 shall be thread-safe, except that the following functions<a href="#tag_foot_1">1</a> need not be thread-safe.</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |  |  |
| ----|----|----|----|
| asctime() basename() catgets() crypt() ctime() dbm_clearerr() dbm_close() dbm_delete() dbm_error() dbm_fetch() dbm_firstkey() dbm_nextkey() dbm_open() dbm_store() dirname() dlerror() drand48() encrypt() endgrent() endpwent() endutxent() | ftw() getc_unlocked() getchar_unlocked() getdate() getenv() getgrent() getgrgid() getgrnam() gethostent() getlogin() getnetbyaddr() getnetbyname() getnetent() getopt() getprotobyname() getprotobynumber() getprotoent() getpwent() getpwnam() getpwuid() getservbyname() | getservbyport() getservent() getutxent() getutxid() getutxline() gmtime() hcreate() hdestroy() hsearch() inet_ntoa() l64a() lgamma() lgammaf() lgammal() localeconv() localtime() lrand48() mblen() mbtowc() mrand48() nftw() | nl_langinfo() ptsname() putc_unlocked() putchar_unlocked() putenv() pututxline() rand() readdir() setenv() setgrent() setkey() setpwent() setutxent() strerror() strsignal() strtok() system() ttyname() unsetenv() wctomb() |</code></pre>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Oct 24, 2013 16:15
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>OK, so this list augments the C list. I think I remember seeing some words used in one of the rules that mentions that POSIX extends the C Standard list.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by bluepilot at Oct 24, 2013 16:25
</div></td>
</tr>
</tbody>
</table>
