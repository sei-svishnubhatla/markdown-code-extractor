The POSIX function `putenv()` is used to set environment variable values. The `putenv()` function does not create a copy of the string supplied to it as an argument; rather, it inserts a pointer to the string into the environment array. If a pointer to a buffer of automatic storage duration is supplied as an argument to `putenv()`, the memory allocated for that buffer may be overwritten when the containing function returns and stack memory is recycled. This behavior is noted in the Open Group Base Specifications, Issue 6 \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\]:
> A potential error is to call `putenv()` with an automatic variable as the argument, then return from the calling function while `string` is still part of the environment.

The actual problem occurs when passing a *pointer* to an automatic variable to `putenv()`. An automatic pointer to a static buffer would work as intended.
## Noncompliant Code Example
In this noncompliant code example, a pointer to a buffer of automatic storage duration is used as an argument to `putenv()` \[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\]. The `TEST` environment variable may take on an unintended value if it is accessed after `func()` has returned and the stack frame containing `env` has been recycled.
Note that this example also violates [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations).
``` c
int func(const char *var) {
  char env[1024];
  int retval = snprintf(env, sizeof(env),"TEST=%s", var);
  if (retval < 0 || (size_t)retval >= sizeof(env)) {
    /* Handle error */
  }
  return putenv(env);
}
```
## Compliant Solution (`static`)
This compliant solution uses a static array for the argument to `putenv()`.
``` c
int func(const char *var) {
  static char env[1024];
  int retval = snprintf(env, sizeof(env),"TEST=%s", var);
  if (retval < 0 || (size_t)retval >= sizeof(env)) {
    /* Handle error */
  }
  return putenv(env);
}
```
According to the \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] entry for `putenv()`:
> ...the string pointed to by *string* shall become part of the environment, so altering the string shall change the environment.

This means that the call to `putenv()` is only necessary the first time `func()` is called, since subsequent changes to the string update the environment. If `func()` were called more than once, an additional variable could be added to avoid calling it unnecessarily.
## Compliant Solution (Heap Memory)
This compliant solution dynamically allocates memory for the argument to `putenv()`:
``` c
int func(const char *var) {
  const char *env_format = "TEST=%s";
  const size_t len = strlen(var) + strlen(env_format);
  char *env = (char *) malloc(len);
  if (env == NULL) {
    return -1;
  }
  int retval = snprintf(env, len, env_format, var);
  if (retval < 0 || (size_t)retval >= len) {
    /* Handle error */
  }
  if (putenv(env) != 0) {
    free(env);
    return -1;
  }
  return 0;
}
```
The POSIX `setenv()` function is preferred over this function \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\]. In particular, using `putenv()` will necessarily leak memory if called multiple times for the same environment variable, due to restrictions on when you can safely free the old value. According to the \[[Open Group 2004](AA.-Bibliography_87152170.html#AA.Bibliography-OpenGroup04)\] entry for `putenv()`:
> Although the space used by *string* is no longer used once a new string which defines *name* is passed to *putenv*(), if any thread in the application has used [getenv()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/getenv.html) to retrieve a pointer to this variable, it should not be freed by calling [free()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/free.html). If the changed environment variable is one known by the system (such as the locale environment variables) the application should never free the buffer used by earlier calls to *putenv*() for the same variable.

## Compliant Solution (`setenv()`)
The `setenv()` function allocates heap memory for environment variables, which eliminates the possibility of accessing volatile stack memory:
``` c
int func(const char *var) {
  return setenv("TEST", var, 1);
}
```
Using `setenv()` is easier and consequently less error prone than using `putenv()`.
## Risk Assessment
Providing a pointer to a buffer of automatic storage duration as an argument to `putenv()` may cause that buffer to take on an unintended value. Depending on how and when the buffer is used, it can cause unexpected program behavior or possibly allow an attacker to run arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS34-C | high | unlikely | medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Can be checked with appropriate analysis stubs. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS34 |  |
| CodeSonar | 8.3p0 | (customization)BADFUNC.PUTENV
 | Users can add a custom check for all uses of putenv().Use of putenv |
| Compass/ROSE |  |  |  |
| Helix QAC | 2024.4 | C5024 |  |
| Klocwork | 2024.4 | CERT.PUTENV.AUTO_VARIABLE |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS34-aCERT_C-POS34-b | Usage of system properties (environment variables) should be restrictedDo not call putenv() with a pointer to an automatic variable as the argument |
| PC-lint Plus | 1.4 | 2601 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS34-C | Checks for use of automatic variable as putenv-family function argument (rule fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+POS34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-252/CWE-253/CWE-391 and ERR33-C/POS34-C
Independent( ERR33-C, POS54-C, FLP32-C, ERR34-C)
Intersection( CWE-252, CWE-253) = Ø
CWE-391 = Union( CWE-252, CWE-253)
CWE-391 = Union( ERR33-C, POS34-C, list) where list =
-   Ignoring return values of functions outside the C or POSIX standard libraries
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 10, "UNIX Processes" |
| [ISO/IEC 9899:2024] | Section 6.2.4, "Storage Durations of Objects"Section 7.24.3, "Memory Management Functions" |
| [Open Group 2004] | putenv()setenv() |

------------------------------------------------------------------------
[](POS30-C_%20Use%20the%20readlink__%20function%20properly) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152082)
## Comments:

|  |
| ----|
| Here's a question. Is this an example of secure code that uses putenv? (Specifically, it gives putenv a dynamically-allocated pointer.)
int POS34_c(char *var) {
  char env[1024];
  if (snprintf(env, sizeof(env),"TEST=%s", var) < 0) {
    /* Handle Error */
  }
  size_t len = strlen( env);
  char* env2 = NULL;
  env2 = (char*) calloc( len, sizeof( char));
  strncpy( env2, env, len);
  return putenv(env2);
}
                                        Posted by svoboda at Dec 06, 2007 17:00
                                     |
| Yes, this is a valid solution.;  However, it causes a memory leak if TEST is ever redefined, since the string pointed to by env2 will never be freed.   The putenv() function only frees memory that putenv() itself allocated.
I have changed the language in the rule to clarify the difference between an automatic variable and a pointer to an automatic variable in the context of putenv().  The POSIX standard was slightly inaccurate on this point.
                                        Posted by dmk at Dec 06, 2007 17:31
                                     |
| No - the space allocated is one byte short of what is needed.
If you fix the off-by-one bug, then yes, it is fine.; Note, however, that if you subsequently set the value again, you are leaking memory.  Actually, it is quite hard to avoid leaking memory with putenv().  One of the advantages of setenv() is that it does avoid such leakages.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 03:54
                                     |
| I don't see the point of the implementation details, and think they should be removed.
A compliant solution using putenv is
int func(char *var) {
  char env[1024];
  static char *p;
  if (snprintf(env, sizeof(env),"TEST=%s", var) < 0) {
    /* Handle Error */
  }
  if (p != NULL)
    free(p); // avoid memory leak
  if ((p = strdup(env)) == NULL) {
    /* Handle Error */
  }
  return putenv(p);
} 
                                        Posted by dagwyn at Apr 18, 2008 15:40
                                     |
| Implementation Details
The putenv() function is not required to be thread-safe, and the one in libc4, libc5 and glibc2.0 is not, but the glibc2.1 version is.
Description for libc4, libc5, glibc: If the argument string is of the form name, and does not contain an `=' character, then the variable name is removed from the environment. If putenv() has to allocate a new array environ, and the previous array was also allocated by putenv(), then it will be freed. In no case will the old storage associated to the environment variable itself be freed.
The libc4 and libc5 and glibc 2.1.2 versions conform to SUSv2: the pointer argument given to putenv() is used. In particular, this string becomes part of the environment; changing it later will change the environment. (Thus, it is an error to call putenv() with a pointer to a buffer of automatic storage duration as the argument, then return from the calling function while the string is still part of the environment.) However, glibc 2.0-2.1.1 differs: a copy of the string is used. On the one hand this causes a memory leak, and on the other hand it violates SUSv2. This has been fixed in glibc2.1.2.
The BSD4.4 version, like glibc 2.0, uses a copy.
SUSv2 removes the `const' from the prototype, and so does glibc 2.1.3.
The FreeBSD implementation of putenv() copies the value of the provided string, and the old values remain accessible indefinitely. As a result, a second call to putenv() assigning a differently sized value to the same name results in a memory leak.
                                        Posted by rcs at Apr 20, 2008 06:50
                                     |
| I'm quite confused by this.  
POSIX Draft 5 says:
"The standard developers noted that putenv( ) is the only function available to add to the
environment without permitting memory leaks."
Although I have seen older documents which claim both can leak.
                                        Posted by rcs_mgr at Apr 20, 2008 07:40
                                     |
| The code should not free the old buffer until after the putenv(). Otherwise when putenv() searches environ to see if the TEST variable already exists, it will try to access the freed memory.
Is there some reason for doing the snprintf() to a local buffer and then copying it to a buffer on the heap, rather than just using malloc() to obtain a buffer of the necessary length and doing the snprintf() straight to that buffer?
Also, the snprintf() return value check does not detect truncation.
                                        Posted by geoffclare at Apr 21, 2008 06:12
                                     |
| I can't think of a reason why this needs to be done on the stack.  
Please feel free to take another crack at the putenv() example.
                                        Posted by rcs at Apr 21, 2008 06:16
                                     |
| In the putenv() CS, is there any algorithmic way for ROSE to know that oldenv is allocated dynamically?
                                        Posted by avolkovi at Jul 28, 2008 11:17
                                     |
| In the CS, it obviously is allocated dynamically, as it is the result of a call to malloc(). In general, one usually can't tell, as it may be a paramter, or may be assigned from another variable...one would need runtime dataflow analysis to know for sure.
                                        Posted by svoboda at Jul 28, 2008 12:35
                                     |
| It is not obvious that it is allocated dynamically.  There aren't any writes to oldenv before the call to free().  oldenv gets the value of env which is allocated dynamically, but only after the line with free. That is not obvious to a static checker.
Currently, I am having ROSE bail on global and static vars.
                                        Posted by avolkovi at Jul 28, 2008 13:42
                                     |
| The compilent sample is wrong, because memory for env was freed.
Here is a "compilent" sampe, if you use only one environment variable.
The only difference is the "static" definition.
int func(const char *var) {
Â; static char env[1024];
Â  if (snprintf(env, sizeof(env),"TEST=%s", var) < 0) {
Â Â Â  /* Handle error */
Â  }
Â  return putenv(env);
}

If you have to set more than one environmet variable, you can define env as an array of strings.  
Always: Keep your solution small and simple!
![](images/icons/contenttypes/comment_16.png) Posted by stefan at Mar 18, 2011 05:54
\| \|
Not sure what problem you're citing. I did find a problem in that the `oldenv` var was freed, while never being initialized, so I took it out. There might be a memory leak now, if the old environment variable was also allocated on the heap, but that is less harmful than freeing memory twice or freeing memory not on the heap.
I also added your code sample as another compliant solution...thanks!
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2011 10:35
\| \|
The oldenv var was statically initialized. I can't see any problem with that old code.
There are some oddities concerning snprintf(). The heap memory compliant solution has a check on whether the snprintf() return was larger than the buffer. This can't happen because the buffer was sized to be large enough (although the check doesn't do any harm and should probably stay.) However, the two earlier examples do not have this check but do need it.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 18, 2011 11:13
\| \|
What value was `oldenv` statically initialized to?
The C99 {\[snprintf()}} method prevents buffer overflows, and right now it is present in all examples (except the setenv one). You're right, it could be replaced with old sprintf() for the heap example. But the first two examples need it to prevent buffer overflow.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2011 11:57
\| \|
> What value was oldenv statically initialized to?

A null pointer, of course.
> The C99 {\[snprintf()}} method prevents buffer overflows, and right now it is present in all examples (except the setenv one). You're right, it could be replaced with old sprintf() for the heap example. But the first two examples need it to prevent buffer overflow.

I wasn't suggesting using `sprintf()`. My point was that if the fixed-size buffer in those examples is not large enough, `snprintf()` will return a value larger than the buffer size but the code will not detect that this happened.
![](images/icons/contenttypes/comment_16.png) Posted by geoffclare at Mar 18, 2011 12:36
\| \|
I see. I keep forgetting that static vars are never uninitialized. Brought back oldenv, and added the snprintf checks you suggest.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2011 13:25
\| \|
I don't like the `static` or heap memory compliant solutions. In the `static` one, the call to `putenv` is redundant (and I'm not sure if it's even safe) on all calls to that function except the first, since POSIX says "altering the string shall change the environment". In the heap memory one, we `free()` the old value even though POSIX says this:
> Although the space used by *string* is no longer used once a new string which defines *name* is passed to *putenv*(), if any thread in the application has used [getenv()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/getenv.html) to retrieve a pointer to this variable, it should not be freed by calling [free()](https://pubs.opengroup.org/onlinepubs/9699919799/functions/free.html). If the changed environment variable is one known by the system (such as the locale environment variables) the application should never free the buffer used by earlier calls to *putenv*() for the same variable.

I think we should add `static _Bool called_putenv` to the `static` one so that `putenv` is only called once, and we should remove the logic to free the old value from the heap memory one.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 07, 2020 11:48
\| \|
Joe:Now that you have editing superpowers, why don't you try fixing these two CS's? Here are my suggestions:
\* I agree with you that in the static CS the call to 'putenv()' is redundant after the first call to func(). However, don't change the code as it is more readable with putenv() than with it wrapped in an if statement. Instead add some text (after the CS explaining this issue wrt putenv().
\* For the dynamic CS you can replace the call to free() with a comment saying something like "don't free...see below", and provide some text explaining the issue. Include the POSIX quote you cited. Be sure to explain why the CS doesn't violate MEM31-C.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 07, 2020 19:32
\| \|
"Be sure to explain why the CS doesn't violate MEM31-C." It *does* violate MEM31-C. That's why I commented over there that we need an exception for this.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 00:34
\| \|
We do need an exception, but not in the way you suggest:
In particular, putenv() is a pathological system call, and has no similarly pathological function in ISO C which is why we don't address it in MEM31-C. Since putenv() imposes a pathological constraint on the lifetime of its argument, I would argue that putenv() itself is culpable in violating MEM31-C, rather than any code that calls putenv(). That's why the CS should not free the pointer. That's also one reason that people should prefer setenv() or putenv().
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 12:47
\| \|
"I would argue that putenv() itself is culpable in violating MEM31-C, rather than any code that calls putenv()." Fair enough. I updated this accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 13:05
\| \|
It might be worthwhile to add a recommendation (and possibly a rule) that says "if your function imposes constraints on the lifetime of its pointer arguments, you must abide by them", and cite putenv() as an example.; I wouldn't add that to MSC31-C, although it could reference the new guideline.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 13:35
\| \|
[Joseph C. Sible](https://wiki.sei.cmu.edu/confluence/display/~jcsible);:  why did you add this line? What is wrong with calling putenv() multiple times on the same pointer?
> Note that func should only be called once in this example, since otherwise `putenv()` will be called multiple times with the same pointer.

Your other changes look good to me.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2020 13:39
\| \|
I thought I could make it break somehow with it, but everywhere I've looked/tried it, it does just seem to be redundant. I adjusted it accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 08, 2020 14:03
\|
