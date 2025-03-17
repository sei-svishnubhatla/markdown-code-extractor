Before the lifetime of the last pointer that stores the return value of a call to a standard memory allocation function has ended, it must be matched by a call to `free()` with that pointer value.
## Noncompliant Code Example
In this noncompliant example, the object allocated by the call to `malloc()` is not freed before the end of the lifetime of the last pointer `text_buffer` referring to the object:
``` c
#include <stdlib.h>
enum { BUFFER_SIZE = 32 };
int f(void) {
  char *text_buffer = (char *)malloc(BUFFER_SIZE); 
  if (text_buffer == NULL) {
    return -1;
  }
  return 0;
}
```
## Compliant Solution
In this compliant solution, the pointer is deallocated with a call to `free()`:
``` c
#include <stdlib.h>
enum { BUFFER_SIZE = 32 };
int f(void) {
  char *text_buffer = (char *)malloc(BUFFER_SIZE); 
  if (text_buffer == NULL) {
    return -1;
  }
  free(text_buffer);
  return 0;
}
```
## Exceptions
**MEM31-C-EX1**: Allocated memory does not need to be freed if it is assigned to a pointer whose lifetime includes program termination. The following code example illustrates a pointer that stores the return value from `malloc()` in a `static` variable:
``` c
#include <stdlib.h>
enum { BUFFER_SIZE = 32 };
int f(void) {
  static char *text_buffer = NULL;
  if (text_buffer == NULL) {
    text_buffer = (char *)malloc(BUFFER_SIZE); 
    if (text_buffer == NULL) {
      return -1;
    }
  }
  return 0;
}
```
## Risk Assessment
Failing to free memory can result in the exhaustion of system memory resources, which can lead to a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM31-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported, but no explicit checker |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM31 | Can detect dynamically allocated resources that are not freed |
| CodeSonar | 8.3p0 | ALLOC.LEAK | Leak |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | RESOURCE_LEAKALLOC_FREE_MISMATCH | Finds resource leaks from variables that go out of scope while owning a resource |
| Cppcheck | ; 2.15 | memleakleakReturnValNotUsed
leakUnsafeArgAlloc
memleakOnRealloc |  |
| Cppcheck Premium | 24.11.0 | memleakleakReturnValNotUsed
leakUnsafeArgAlloc
memleakOnRealloc |  |
| Helix QAC | 2024.4 | DF2706, DF2707, DF2708C++3337, C++3338 |  |
| Klocwork | 2024.4 | CL.FFM.ASSIGNCL.FFM.COPY
CL.SHALLOW.ASSIGN
CL.SHALLOW.COPY
FMM.MIGHT
FMM.MUST |  |
| LDRA tool suite | 9.7.1 | 50 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM31-a | Ensure resources are freed |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 429 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule MEM31-C | Checks for memory leak (rule fully covered) |
| PVS-Studio | 7.35 | V773 |  |
| SonarQube C/C++ Plugin | 3.11 | S3584 |  |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | malloc | Exhaustively verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM31-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| ISO/IEC TR 24772:2013 | Memory Leak [XYL] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961 | Failing to close files or free dynamic memory when they are no longer needed [fileclose] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-401, Improper Release of Memory Before Removing Last Reference ("Memory Leak") | 2017-07-05: CERT: Exact |
| CWE 2.11 | CWE-404 | 2017-07-06: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-459 | 2017-07-06: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-771 | 2017-07-06: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-772 | 2017-07-06: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-404/CWE-459/CWE-771/CWE-772 and FIO42-C/MEM31-C
Intersection( FIO42-C, MEM31-C) = Ø
CWE-404 = CWE-459 = CWE-771 = CWE-772
CWE-404 = Union( FIO42-C, MEM31-C list) where list =
-   Failure to free resources besides files or memory chunks, such as mutexes)
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.24.3, "Memory Management Functions" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152153) [](../c/Rule%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152183)
## Comments:

|  |
| ----|
| Maybe there needs to special mention of the UNIX realloc() gotcha here - if the size passed to realloc() is 0, realloc() frees the memory you pass, rather than attempting to reallocating it. This can lead to double-free problems.. 
                                        Posted by mdowd at Jan 06, 2007 03:45
                                     |
| The C standard doesn't say anything about what happens with a size argument of 0, but I checked glibc and openbsd source real quick and they appear to return a valid pointer to a zero-sized object.. e.g. the return of a malloc(0);
I mention this because if there was a system where realloc() free'ed the object and then returned NULL, it would make the secure idiom for realloc() exploitable. Here's that idiom, snagged from an openbsd man page:
if ((p2 = realloc(p, nsize)) == NULL) {
    if (p)
        free(p);
    p = NULL;
    return NULL;
}
p = p2; 

You can see that if nsize was 0, and realloc() free'ed the memory and then returned NULL, it would be a double-free of p. I would guess that no systems actually do this, but it might be worth researching. As it stands, the behavior with an nsize of 0 is pretty interesting and counter-intuitive, and I can see people running into trouble because of it.
![](images/icons/contenttypes/comment_16.png) Posted by jm at Jan 06, 2007 13:53
\| \|
OK, I've updated MEM36-C. to talk about reallocating zero bytes.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 11, 2007 14:02
\| \|
This again points to the benefit of setting pointers to NULL after free(); this doesn't fix the logic error that calls free() twice, but it at least gets rid of the gross security issue of freeing a random pointer.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 00:45
\| \|
Solaris 10 (UltraSPARC) specifically returns NULL when you realloc 0 bytes.
> [!note]
>
>     #include <stdlib.h>
>     #include <stdio.h>
>
>     int main(void)
>     {
>         char *s = malloc(24);
>         char *p = realloc(s, 0);
>         puts((s == 0) ? "s was null" : "s was not null");
>         puts((p == 0) ? "p is  null" : "p is  not null");
>         return(0);
>     }

This code yields "s was not null" and "p is null".
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 17, 2008 09:35
\| \|
I prefer if(x!=NULL)free(x) ; since it doesn't depend on the special case for free(NULL) which some libraries might get wrong.; (Before C89, almost all of them croaked.)
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 16, 2008 22:28
\| \|
The document assumes C99 - even if it only assumed C89, free(0) is defined as safe.; It is only pre-C89 implementations that might have the problem.  Presumably, those who work on such implementations are aware of the problems, and for the large majority who do not work on such archaic systems, there is no issue.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Apr 20, 2008 01:15
\| \|
I recall a discussion about the comments that say "handle error". Perhaps the CS would be better if it exits or returns (with an error code) after freeing the memory on error_condition = 1 rather than removing `free()` altogether from that part of code.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Jun 18, 2010 00:14
\| \|
I think you are referring to code that does the following:
``` java
/* ... */
if (error_condition == 1) {
  /* handle error condition*/
  free(x);
  x = NULL;
  return; /* or transfer control, such as abort() or goto */
}
/* ... */
free(x);
x = NULL;
```
This code clearly frees x just once, and so complies with the rule, but this code has the following drawbacks:
-   Its harder to specify. Just saying 'return' is invalid if the code is inside a non-void function.
-   Its easier to modify the code such that the return is deleted, which turns the code back into the NCCE.
-   The cleanup of `x` is duplicated inside & outside the if statement. The redundancy leads to code bloat and potential for more errors.
I suspect these reasons are why this code sample wasn't included as a 2nd CS.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 18, 2010 15:55
\| \|
I agree that the rule would be more "believable" if the error handling was less handwavy. Maybe like so:
``` java
int f(size_t n) {
  int error_condition = 0;
  if (n > SIZE_MAX / sizeof(int)) {
    errno = EOVERFLOW;
    return -1;
  }
  int *x = (int*)malloc(n * sizeof(int));
  if (x == NULL) {
    /* Report allocation failure to caller. */
    return -1;
  }
  /* Use x and set error_condition on error. */
  if (error_condition != 0) {
    /* Handle error condition. */
  }
  free(x);
  return error_condition;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 20, 2010 12:24
\| \|
The above code by Martin appears to address the return problem/possible memory leak I'd imagined. +1
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Jun 20, 2010 15:41
\| \|
I've updated the code examples.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jun 26, 2010 16:44
\| \|
[MSVC error C6308](http://msdn.microsoft.com/en-us/library/kkedhy7c(VS.90).aspx) addresses an improper use of realloc(). which rule corresponds with this diagnostic? I assume its MEM31-C, but that's not obvious. Whichever rule should handle C6308 needs a NCCE & CS pair to illustrate the problem.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 08, 2010 15:25
\| \|
I wonder if [MEM08-C. Use realloc() only to resize dynamically allocated arrays](/confluence/pages/createpage.action?spaceKey=c&title=MEM08-C.+Use+realloc%28%29+only+to+resize+dynamically+allocated+arrays) could be tweaked to cover the case you mention. As it stands, the problem MEM08-C tries to avoid doesn't seem like one that's specific to `realloc()` but rather one of converting a pointer to one object to a pointer of an unrelated type. That can just as easily happen with `malloc()` or in any other situation involving a cast of a pointer to another.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Dec 11, 2010 18:10
\| \|
We may want to add an exception for dynamically-loaded libraries. Most programs allocate memory to hold dynamically-loaded code (eg the LoadLibrary() function in Windows), and do nothing to free them (expecting that they will persist through the lifetime of the program.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 04, 2011 10:23
\| \|
This rule is going to get trashed and replaced by something that looks like the memory portions of this TS 17961 rule:
5.18 Failing to close files or free dynamic memory when they are no longer needed \[fileclose\]
;
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Nov 07, 2013 10:48
\| \|
Even when replaced, the Risk Assessment needs attention.
Severity on this page is "Medium".; But summary on the "Memory Management" page shows Severity for this rule to be "High".  The two should align.
![](images/icons/contenttypes/comment_16.png) Posted by john.whited at Sep 23, 2014 16:20
\| \|
In the example code above, there's a line which reads:
**`char`;`*text_buffer = (``char` `*)``malloc``(BUFFER_SIZE);`**
I don't think that cast to `char *` should be there.  It's redundant, since C implicitly converts a pointer-to-void to any pointer type, and the cast could hide a bug if the call to `malloc()` were to be replaced by a call to a function which didn't return `void *`.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 15, 2020 06:22
\| \|
While not strictly needed, it's commonly viewed as a best practice to do the cast. See;[MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](MEM02-C_%20Immediately%20cast%20the%20result%20of%20a%20memory%20allocation%20function%20call%20into%20a%20pointer%20to%20the%20allocated%20type) for more information.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 15, 2020 06:51
\| \|
Agreed.; Thanks.
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jun 16, 2020 04:20
\| \|
To quote [Raymond Chen](https://devblogs.microsoft.com/oldnewthing/20200130-00/?p=103385), "There’s no point sweeping the floors when the building is being demolished."
I think we should have another exception in line with that. Freeing memory immediately before the process exits is just a waste of time. For example, if your strategy to handle a failing `realloc()` is to call `exit()` or `abort()`, then you don't need to worry about keeping the old pointer around.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 06, 2020 16:47
\| \|
I support this and would point out that EX1 is providing basically this exact exception already (it can likely be reworded to make this more clear, however). It may need some weasel words about verifying that the host OS cleans up memory on program termination to cover embedded systems which may not behave the same way as desktop systems.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 07, 2020 06:42
\| \|
It definitely looks like that was the intent of it, and it almost does that, but the restriction that the pointer must have static storage duration really limits its applicability.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 09:55
\| \|
This point deserves more thought. Given the pushback we've gotten on other rules, I'm a little surprised that we haven't addressed this argument earlier. Possibly because while calling abort() or exit() without freeing memory can still produce safe code, it is sloppy practice, and writing a rigorous exception that permits this safely looks tricky.
For that reason, I would rather not modify EX1, but rather add a new exception about precisely when this is permissible.
-   I wouldn't allow this for C++ code because C++ has new/delete as well as destructors, and being sloppy about those functions will cause more than memory leaks.
-   I would permit leaks when calling abort(), on the grounds that abort() should be used in the face of program or memory corruption, and allowing the program to continue is hazardous (eg suppose the program detected that its stack was smashed).
-   I would only allow it for functions that unconditionally end with exit(), \_Exit(), or abort()
There are probably other corner cases I'm missing. Comments?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 10:56
\| \|
-   For C++, destructors already don't run for objects with automatic storage duration when you call `exit()`. Would this exception really cause new problems there?
-   Agreed on `abort()`.
-   We should also allow it when you're about to return from `main()`.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 11:05
\| \|
> Possibly because while calling abort() or exit() without freeing memory can still produce safe code, it is sloppy practice

The situation I'm talking about is where you're about to return from;`main()` and you elect not to free memory. This situation is exactly identical to calling `exit()` (because that's what returning from `main()` is defined to do). FWIW, this is a very common practice on desktop systems – I just used this pattern in yet another project and reduced my runtime by a significant amount simply by letting the OS reclaim memory rather than walking lists and freeing manually before exiting.
> I wouldn't allow this for C++ code because C++ has new/delete as well as destructors, and being sloppy about those functions will cause more than memory leaks.

Not running a nontrivial destructor is a different kind of issue than this one. I would **definitely** allow this exception for C++ as it relates only to allocated memory.
> I would permit leaks when calling abort()
>
> I would only allow it for functions that unconditionally end with exit(), \_Exit(), or abort()

I would not be prescriptive like this. I would modify the exception:
Allocated memory does not need to be freed if it is assigned to a pointer \<del\>with static storage duration\</del\> whose lifetime is the entire execution of a program. The following code example illustrates a pointer that stores the return value from `malloc()` in a `static` variable:
and then add another example where the memory is not in a static variable, such as:
``` java
int main(void) {
  char *str = (char *)malloc(100);
  strcpy(str, "This doesn't need to be freed");
  printf("%s", str);
}
```
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 07, 2020 11:14
\| \|
As I look through other rules, I think we need another exception: strings that have been passed to `putenv`. From POSIX:
> Although the space used by *string* is no longer used once a new string which defines *name* is passed to *putenv*(), if any thread in the application has used [getenv()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/getenv.html) to retrieve a pointer to this variable, it should not be freed by calling [free()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/free.html). If the changed environment variable is one known by the system (such as the locale environment variables) the application should never free the buffer used by earlier calls to *putenv*() for the same variable.

![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 11:53
\| \|
What is this 'putenv'? That be one of them new-fangled POSIX functions? It aint no C standard function, podner.
More seriously, what constraints does putenv() impose on its argument? Does it copy the argument contents, or does it require the argument's lifetime to last the life of the program (or until the env var is overwritten).There is certainly some guideline you could write about safe use of putenv, but it belongs in the POSIX section.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 12:02
\| \|
We already wrote about `putenv` in the POSIX section: [POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument](POS34-C_%20Do%20not%20call%20putenv__%20with%20a%20pointer%20to%20an%20automatic%20variable%20as%20the%20argument)
The problem is that using it safely means that you'll break this rule.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:07
\| \|
First, I'm willing to modify the exception if we decide that what we want is close enough to it. But let's figure that out first before deciding if it should be separate or part of the current exception.
I'll agree that whatever permissions we put on calling exit() or \_exit() can also apply to returning from main().
If you allow memory to be leaked via exit() (or main()), then you have just defanged this rule...when would code ever violate it?;  FTM your code example is very similar to the noncompliant code example.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 12:11
\| \|
-   *We should also allow it when you're about to return from;`main()`*
That's only safe if `main()` isn't called recursively, surely?
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.headland at Jul 07, 2020 12:15
\| \|
The SEI CERT C Coding Standard addresses specific coding flaws that arise from writing standard-compliant C code. This means that your noncompliant code examples must not rely on POSIX or other OS-specific features, like putenv(). It is OK if your compliant code uses such features, but then you must mark the compliant solution as specific to POSIX.
We created the POSIX section for POSIX-specific coding problems. There is a similar section for Windows.
We do expect that each platform will introduce complications and new exceptions to the CERT C rules and recommendations, but such exceptions are out-of-scope to the rules & recs themselves.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 12:16
\| \|
Yes, that's a good point.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:20
\| \|
We use noncompliant POSIX-specific code outside the POSIX section all over the place, e.g.:
-   [EXP37-C. Call functions with the correct number and type of arguments](EXP37-C_%20Call%20functions%20with%20the%20correct%20number%20and%20type%20of%20arguments)
-   [SIG34-C. Do not call signal() from within interruptible signal handlers](SIG34-C_%20Do%20not%20call%20signal__%20from%20within%20interruptible%20signal%20handlers)
-   [MSC32-C. Properly seed pseudorandom number generators](MSC32-C_%20Properly%20seed%20pseudorandom%20number%20generators)
Why is this case not okay if they are?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:27
\| \|
It's definitely kind of a fuzzy boundary. Here's a few ideas that popped into my head:
-   In a program that accepts user input, once the user requests that the program exit (if there's a confirmation before exiting, then after the confirmation)
-   Once the program won't need to dynamically allocate any more memory for the remainder of execution (for two reasons: first, it means it's almost certainly almost done, and second, memory released by `free()` is often only made reusable by a future `malloc()` and not given back to the OS until the program exits anyway)
-   In a program that does some sort of batch processing in a loop, any code from the end of the loop for the rest of the program
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 12:34
\| \|
I don't think this defangs the rule as the rule is already only intended to cover the cases where the memory is no longer needed (after the program terminates, the memory cannot be needed by the program). The issue is that we need to define "no longer needed" sufficiently.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 07, 2020 12:41
\| \|
Sorry, it is a fine point and I didn't make it fine enough. You are correct in that we do have platform-specific NCCEs. But all of those rules have platform-neutral NCCEs, which prove the point that you can violate the rule without relying on nonstandard functions.While you can write unsafe code using POSIX's putenv() function, I'm not sure you can write unsafe code in the same way using strictly ISO-conforming functions.
Finally, insecure code relating to putenv() is already covered by POS34-C.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 14:16
\| \|
"all of those rules have platform-neutral NCCEs" Of my three links, only the first one does.
"Finally, insecure code relating to putenv() is already covered by POS34-C." The issue isn't that this rule lets you write insecure code; it's that it doesn't let you write safe code. It currently requires you to free memory that isn't safe to free.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 14:25
\| \|
Signals are weird. ISO C standardizes signal() and raise(), but no other signal-related stuff. So SIG34-C's NCCE is actually ISO-compliant, but we can't discuss what the program does in general, because the way it behaves (badly) is platform-dependent. Hence the partitioning of examples into POSIX vs Windows sections.
Random numbers are similarly pathalogical. ISO C defines rand() and srand(), but they do not guarantee that rand() delivers sufficiently random numbers. So we forbid its use in MSC30-C. Meanwhile, when we first wrote MSC32-C it was about using srand() properly, as well as POSIX & Windows-specific solutions. So MSC32-C now describes a platform-neutral problem, but we can no longer write a platform-neutral NCCE for it without also violating MSC30-C.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 14:53
\| \|
Precisely. Right now "no longer needed" applies to all dynamic memory, except those covered by EX1. Which is a bit restrictive, but sufficiently precise to justify this being a rule.
One option would be the "valgrind strategy". If dynamic memory is still allocated once it is no longer referenceable, before the program exits, that is a well-defined violation of this rule. Hard to manually enforce, but valgrind does it automatically. And that lets you exit the program with memory still allocated (and not covered by the exception.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 15:03
\| \|
Yeah, I see what you mean about the problem now;– there's no way to tell the difference between an unwanted pointer you've forgotten to free and an unwanted pointer you only want to free at program termination time, so this requires understanding programmer intent. Blech.
My concern with the Valgrind algorithm approach is that this rule is also used in C++ and the story gets more complicated there. Say, for instance, that I have an automatic variable of type `std::vector<void *>` where the pointers are allocated and this automatic goes away within the scope of `main()`; those pointers are leaked per the Valgrind algorithm, but the user has no way to prevent that situation from occurring, either. e.g.,
``` java
#include <cstdlib>
#include <vector>
int main() {
  std::vector<void *> v;
  for (int i = 0; i < 10; ++i) {
    v.push_back(malloc(10));
  }
} // v is destroyed here, before the program exits, rendering the memory no longer referencable
```
While this is obviously a contrived example, this sort of scenario can easily crop up due to destructors (even within functions called within `main()`).
The primary reason this is a security rule is because we want users to not run out of resources while the program is executing. I wonder if we can reword the rule to be less about which pointers are required to be freed and which ones aren't and more about resource exhaustion, somehow. Then again, that may still not be enough to avoid the programmer intent issue.
Regardless, I think this is a real deficiency with the rule that needs addressing somehow. This approach is not an uncommon one (esp in C++, but also in C) and has no negative security implications on modern desktop OSes (that I've been able to find evidence of).
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 08, 2020 07:15
\| \|
Aaron:I don't follow your example. A vector of raw pointers as you demonstrate violates RAII, and you could easily 'fix' this code example by iterating over the vector freeing its pointers before it goes out of scope.
I will also disagree that this is not a modern problem. Are you really saying that exhausting memory has no security implications on modern systems??? Certainly on an otherwise secure system, exhausting memory will do nothing more than slow down the system. But when memory gets close to exhaustion, then malloc() starts returning NULL for all programs on the system, and, sadly, few programs handle this gracefully. So you get lots of seemingly random breakage in unexpected places.  Unfortunately, this is not a theoretical conjecture ![](images/icons/emoticons/sad.svg)
While we can't discern programmer intent, a programmer who wishes to not deallocate a pointer has several techniques for indicating this, the easiest is to make the pointer static (or make it part of a static data structure). Which means EX1 applies to it.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 12:41
\| \|
> I don't follow your example. A vector of raw pointers as you demonstrate violates RAII, and you could easily 'fix' this code example by iterating over the vector freeing its pointers before it goes out of scope.

Your assumption that this code is broken is a bit strange. It's a contrived example, but it comes up in real code and it's not a bug that needs to be fixed. The;whole point to the concern is that iterating over the list to free the pointers before it goes out of scope is wasted time that has measurable performance impacts when the program is about to exit anyway, and failing to free those pointers has no negative security implications.
> I will also disagree that this is not a modern problem. Are you really saying that exhausting memory has no security implications on modern systems???

I said the only security implication with this is with resource exhaustion, so I'm not certain where you got this idea from.
> While we can't discern programmer intent, a programmer who wishes to not deallocate a pointer has several techniques for indicating this, the easiest is to make the pointer static (or make it part of a static data structure). Which means EX1 applies to it.

And I'm saying that EX1 is insufficient because it restricts it to only handling the easy case while ignoring real world coding practices that should not be considered insecure.
FWIW, this comes up for me when I'm using an arena allocator instead of directly using the system allocator. When the program terminates, I can spend hours (literally) walking the list of allocations and freeing them with the system allocator, or I can just say "the arena is going away because the program is going away, skip those deallocations" and the program terminates almost instantaneously. I could not do that and comply with this rule as it is written because the arena-allocated pointers are not static.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 08, 2020 13:13
\| \|
It looks like we agree on what your code example does, I just interpreted it differently than you. We both agree that it has no security problems on modern hardware, and it currently violates the rule. But it would be nice if we can add an exception to cover your code example.
There are several ways to tweak your code to be covered by EX1 without making it slower. Making either the vector static would be the easiest way. You could also make a static pointer variable and assign it to the vector, tho that's more work.
Your code example would also be covered by my 'valgrind strategy' exception, because the allocated chunk is always reference-able.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 13:30
\| \|
> It looks like we agree on what your code example does, I just interpreted it differently than you. We both agree that it has no security problems on modern hardware, and it currently violates the rule. But it would be nice if we can add an exception to cover your code example.

Awesome, we've got agreement!
> There are several ways to tweak your code to be covered by EX1 without making it slower. Making either the vector static would be the easiest way. You could also make a static pointer variable and assign it to the vector, tho that's more work.

Making the vector static would not meet the requirements of EX1 because the pointers themselves do not have static storage duration just because they're stored within a list that has static storage duration. Assigning into a static pointer variable that then gets overwritten doesn't seem to really match the intention of EX1 either. For instance, we don't want to allow:
``` java
for (int i = 0; i < SomeBigNumber; ++i) {
  static int *ip = (int *)malloc(sizeof(int));
  ... use ip but don't free it or escape its value out of the loop ...
}
```
> Your code example would also be covered by my 'valgrind strategy' exception, because the allocated chunk is always reference-able.

I don't think it would. The vector destructor is run;**before** `main()` terminates, so the pointers it used to store are unreachable at the point the program terminates. Also, I think we don't want to split hairs with code like my original vector example above and code like below (where there is no functional difference in the program behavior):
``` java
#include <cstdlib>
#include <vector>
void func() {
  std::vector<void *> v;
  for (int i = 0; i < 10; ++i) {
    v.push_back(malloc(10));
  }
} 
int main() {
  func();
}
```
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 08, 2020 14:18
\| \|
> Making the vector static would not meet the requirements of EX1 because the pointers themselves do not have static storage duration just because they're stored within a list that has static storage duration. Assigning into a static pointer variable that then gets overwritten doesn't seem to really match the intention of EX1 either.

I think that's a bit too narrow of a reading of it. Consider this code:
``` c
#include <stdlib.h>
#include <string.h>
char **strs;
void init_strs(void) {
    strs = (char **)malloc(5 * sizeof(char *));
    strs[0] = (char *)malloc(4);
    strcpy(strs[0], "foo");
    strs[1] = (char *)malloc(4);
    strcpy(strs[1], "bar");
    strs[2] = (char *)malloc(4);
    strcpy(strs[2], "baz");
    strs[3] = (char *)malloc(4);
    strcpy(strs[3], "qux");
    strs[4] = NULL;
}
```
Should EX1 really only apply to the first malloc, and not to any of the inner mallocs? Instead of only applying to things directly stored in static pointers, shouldn't it apply to anything reachable through static pointers?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 14:36
\| \|
Joe, Aaron is right. I too had interpreted EX1 to include pointers that are owned by a static pointer, eg you had a static array of pointers to allocated chunks. Leaving that whole thing un-freed would be OK. Lots of GUIs do this, by making a static tree of GUI widgets & similar data and leaving it alive until termination. But the current reading of EX1 only applies to the top-level pointer.
Aaron is also right that the vector dtor would complete before main completes. For C++ we would have to define 'program termination' in this rule as after the last statement of main but before the first destructor of the scope executes. (For C we would also have to define program termination as preceding atexit() handlers).
I do suspect that burying your destructors in a 'func' function that is the last thing called by main starts us down a slippery slope. So I'm against that idea for now.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 14:49
\| \|
I read EX1 as only applying to the first;`malloc()` today, but agree that isn't a helpful exception. I think we will want to go with something like pointer reachability, but I still don't see why it has to be reachable through a static pointer specifically. In C, consider:
``` java
void main(void) {
  alloc_t arena = setup_arena_allocator();
  do_work(arena);
}
```
If the arena uses `malloc()` internally, and `do_work()` does allocations through the arena, there's no need to free the entire arena in this case, despite it not being a static variable. While the user could always write `static` there, I'm not certain I agree it should be a requirement to do so.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jul 08, 2020 14:49
\| \|
FWIW, this has come up yet again:;<https://twitter.com/shafikyaghmour/status/1458965190020534276>
It would be nice if the exception to this rule could be made more clear, because (as Shafik later pointed out), education in this area is a challenge.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 12, 2021 08:03
\| \|
Coming back to this rule, I realized something about the introduction. As written, the introductory text specifically does not apply to allocated chunks that are still reference-able at program termination. (Technically this means we could dispense with EX1, such the pointers it covers didn't violate the rule anyway.)
This nicely sidesteps our entire conversation about pointers that are reference able upon termination (and precisely what constitutes termination). So most of the example programs we've discussed (including Shafik's example on Twitter).
This does introduce a security hole...a program can easily assign an allocated chunk to a pointer and (unintentionally) keep the pointer alive until termination. Which is in-distinguishible from Shafik's example). That is simply outside the scope of this rule.
While not strictly necessary, I'll add an explicit exception specifically about this shortly. UPDATE: I modified EX-1, which was easier than adding a new exception.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 15, 2021 09:21
\| \|
If a pointer to memory is stored in a variable scoped to the `main` function, does that count as being reachable at program termination? For example, is this okay?
``` c
#include <stdlib.h>
int main(void) {
    void *x = malloc(1);
}
```
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Nov 15, 2021 10:23
\| \|
[Joseph C. Sible](https://wiki.sei.cmu.edu/confluence/display/~jcsible) This code is "ok" in that it does not violate this rule. EX1 makes this more explicit, but the code would still comply with the rule if we took out EX1. The normative text, in the introduction, does not include this code, because the pointer's lifetime matches the lifetime of the program.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 15, 2021 11:45
\| \|
But is the end of main really the end of the lifetime of the program? Consider this GNU C program:
``` cpp
#include <stdio.h>
#include <stdlib.h>
void aftermain(void) __attribute__((__destructor__));
void aftermain(void) {
    puts("The main function returned, so the memory is no longer reachable, but the program is still running!");
}
int main(void) {
    void *x = malloc(1);
}
```
Or if you say that's an extension so it doesn't count, then consider C++, where code can run in static objects' destructors even after main returned. Would those cases still be okay for main to do that?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Nov 15, 2021 12:01
\| \|
There may be details of the \_\_destructor\_\_ attribute that elude me, and are out of scope, since it is not standard C. But I would suggest that your code does not violate this rule, and is in fact perfectly good code if your memory is still accessible once main() goes out of scope.
For now, I've used the phrase: "whose lifetime includes program termination". Suggestions for improved wording are welcome (including "when main() goes out of scope").
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 15, 2021 12:24
\| \|
> Coming back to this rule, I realized something about the introduction. As written, the introductory text specifically does not apply to allocated chunks that are still reference-able at program termination.

Hmm, I guess I view the termination of the program as ending the lifetime of all pointers. (Termination as in "in a hosted environment, after the OS cleans up the no-longer-running-process".)
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 15, 2021 15:51
\| \|
There is clearly some wiggle room as to what constitutes "program termination".;  And there is a point in any C or C++ program then the program has nothing to do but clean up. (eg destructors or similar activities).  And I'm losing interest in the "what is termination" debate for the purpose of this rule.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 15, 2021 16:03
\|
