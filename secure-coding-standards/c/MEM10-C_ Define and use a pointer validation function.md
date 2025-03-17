Many functions accept pointers as arguments. If the function dereferences an [invalid pointer](BB.-Definitions_87152273.html#BB.Definitions-invalidpointer) (as in [EXP34-C. Do not dereference null pointers](EXP34-C_%20Do%20not%20dereference%20null%20pointers)) or reads or writes to a pointer that does not refer to an object, the results are [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefined). Typically, the program will [terminate abnormally](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) when an invalid pointer is dereferenced, but it is possible for an invalid pointer to be dereferenced and its memory changed without abnormal termination \[[Jack 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Jack07)\]. Such programs can be difficult to debug because of the difficulty in determining if a pointer is [valid](BB.-Definitions_87152273.html#BB.Definitions-validpointer).
One way to eliminate invalid pointers is to define a function that accepts a pointer argument and indicates whether or not the pointer is valid for some definition of valid. For example, the following function declares any pointer to be valid except `NULL`:
``` java
int valid(void *ptr) {
  return (ptr != NULL);
}
```
Some platforms have platform-specific pointer validation tools.
The following code relies on the `_etext` address, defined by the loader as the first address following the program text on many platforms, including AIX, Linux, QNX, IRIX, and Solaris. It is not POSIX-compliant, nor is it available on Windows.
``` java
#include <stdio.h>
#include <stdlib.h>
int valid(void *p) {
  extern char _etext;
  return (p != NULL) && ((char*) p > &_etext);
}
int global;
int main(void) {
  int local;
  printf("pointer to local var valid? %d\n", valid(&local));
  printf("pointer to static var valid? %d\n", valid(&global));
  printf("pointer to function valid? %d\n", valid((void *)main));
  int *p = (int *) malloc(sizeof(int));
  printf("pointer to heap valid? %d\n", valid(p));
  printf("pointer to end of allocated heap valid? %d\n", valid(++p));
  free(--p);
  printf("pointer to freed heap valid? %d\n", valid(p));
  printf("null pointer valid? %d\n", valid(NULL));
  return 0;
}
```
On a Linux platform, this program produces the following output:
``` java
pointer to local var valid? 1
pointer to static var valid? 1
pointer to function valid? 0
pointer to heap valid? 1
pointer to end of allocated heap valid? 1
pointer to freed heap valid? 1
null pointer valid? 0
```
The `valid()` function does not guarantee validity; it only identifies null pointers and pointers to functions as invalid. However, it can be used to catch a substantial number of problems that might otherwise go undetected.
## Noncompliant Code Example
In this noncompliant code example, the `incr()` function increments the value referenced by its argument. It also ensures that its argument is not a null pointer. But the pointer could still be invalid, causing the function to corrupt memory or terminate abnormally.
``` c
void incr(int *intptr) {
  if (intptr == NULL) {
    /* Handle error */
  }
  (*intptr)++;
}
```
## Compliant Solution
This `incr()` function can be improved by using the `valid()` function. The resulting implementation is less likely to dereference an invalid pointer or write to memory that is outside the bounds of a valid object.
``` c
void incr(int *intptr) {
  if (!valid(intptr)) {
    /* Handle error */
  }
  (*intptr)++;
}
```
The `valid()` function can be implementation dependent and perform additional, platform-dependent checks when possible. In the worst case, the `valid()` function may only perform the same null-pointer check as the noncompliant code example. However, on platforms where additional pointer validation is possible, the use of a `valid()` function can provide checks.
## Risk Assessment
A pointer validation function can be used to detect and prevent operations from being performed on some invalid pointers.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM10-C | High | Unlikely | High | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 159 S | Enhanced enforcement |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM10-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM10-CPP. Define and use a pointer validation function |
| MITRE CWE | CWE-20, Improper Input ValidationCWE-79, Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
CWE-89, Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
CWE-91, XML Injection (aka Blind XPath Injection)
CWE-94, Improper Control of Generation of Code ('Code Injection')
CWE-114, Process Control
CWE-601, URL Redirection to Untrusted Site ('Open Redirect') |

## Bibliography

|  |
| ----|
| [Jack 2007] |
| [van Sprundel 2006] |

------------------------------------------------------------------------
[](../c/MEM07-C_%20Ensure%20that%20the%20arguments%20to%20calloc__,%20when%20multiplied,%20do%20not%20wrap) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152220)
## Comments:

|  |
| ----|
| The use of _etext is somewhat unreliable across systems.; For example on an x86-64 FreeBSD system from within a shared lib I'm currently getting:
p = 0xB34110, &_etext = 0x7F9B0C495246, &_edata = 0x7F9B0C7183A0, &_end = 0x7F9B0C718EE8.
In this case p is on the stack, not a malloc'd variable.  I've also had reports of it failing on a PPC Linux embedded device.  Presumably this is because the single shared image can be mapped pretty much anywhere into each process' address space, and in addition there can be multiple _etext's for different shared libs.  Perhaps someone who knows more about how different OSes lay things out in memory could comment on this, and under which conditions it's safe to use _etext.
                                        Posted by pgut001@cs.auckland.ac.nz at Oct 29, 2009 05:00
                                     |
| Maybe I'm just tired and grumpy, but the first Compliant Solution (validation) does exactly the same thing as the non-compliant example (in cases where the validate() function only checks for null pointers) and does significantly less in the second Compliant Solution (assertion) as the assert() would presumably be eliminated in a non-debug build. 
                                        Posted by rcs at Oct 30, 2009 05:04
                                     |
| Maybe the text could do with a bit of cleaning up, as you say solution #2 follows rather trivially from #1, I don't think it's necessary to have two examples with one being a runtime check and the other a debug-build-only check.; It's also making a rather fine distinction between what's "compliant" and what isn't, the "Compliant Solution" is only compliant if your 'valid' macro uses the non-portable _etext trick, but non-compliant otherwise.  Perhaps a better layout would be to remove the distinction between "compliant" and "non-compliant" and re-word the text for solution #1 to say that, depending on whether your OS supports _etext or not, you may get more or less checking that you bargained for.  Even if your OS does have _etext, it may not actually work as you want it to, so perhaps phrase it as "a NULL check works everywhere but won't catch many invalid pointers, the _etext check may work but can be erratic" or "may not work with shared libs".
                                        Posted by pgut001@cs.auckland.ac.nz at Nov 14, 2009 07:34
                                     |
| Looks good now, thanks!
                                        Posted by pgut001@cs.auckland.ac.nz at Nov 23, 2009 06:14
                                     |
| I would imagine the compiler/library vendor would have a much better idea on how to write the valid() function.; I would hope that it would be inline.  There are 3 kinds of valid (at least).  There is a valid function pointer, a valid data pointer and a pointer that you could pass to free.   
                                        Posted by jimg at Jul 06, 2010 16:03
                                     |
| The only vendor I know of that's ever done this is Microsoft with their IsBadXXXPtr() checks, which used mem probing and first-chance exceptions to detect invalid pointers.; This worked really well but had some unfortunate side-effects that meant they turned them into no-ops starting with Vista.  So there really isn't any vendor-blessed way of doing this, which is why there's all the suggestions for platform- and situation-specific checking methods here.
For more on the problems with IsBadXXXPtr(), see Raymond Chen's comments on this.  Having used these functions for years though, I know they've caught huge numbers of user errors, particularly when called from a non-C language where the programmer hasn't got the memory-access convention quite right, and I'm not aware of them causing any problems.
Another option for Unix systems, and this is just pseudocode, is something like:
int nullFD = open( "/dev/null", O_WRONLY );
if( write( nullFD, ptr, length ) == -1 && errno = EFAULT )
  ; /* Invalid access */

(assuming the OS doesn't fast-path the checking for special-case FDs, which it shouldn't be doing). If I did use something like the above in a program I think I'd do it under an assumed name though...
![](images/icons/contenttypes/comment_16.png) Posted by pgut001@cs.auckland.ac.nz at Jul 07, 2010 02:40
\| \|
Some more comments on \_etext, I think in general this is too unreliable to use safely in code unless you have complete control over the environment in which it's deployed.; It doesn't work with shared libs, it fails with SELinux (which is something you'd expect to see used in combination with code that's been carefully written to do things like perform pointer checking), and I have no idea what it'll do in combination with different approaches to ASLR but I suspect it'll break with some of those as well.  Perhaps if you could wrap the \_etext check in some sort of libmemcheck that runs a self-test on startup and turns the comparison into a no-op if the \_etext check can't be relied upon it would be safe, but without this it's too risky to enable on any cross-platform or heterogeneous-environment code.  I've (reluctantly) turned it off in my code, I was getting too many error reports... it might be a good idea in the text above to warn about its high level of nonportability, that even on the same system it can break depending on whether something like SELinux is enabled or not.
![](images/icons/contenttypes/comment_16.png) Posted by pgut001@cs.auckland.ac.nz at Sep 08, 2010 01:11
\| \|
for struct/object pointer, we can do little more in valid(), like checking a magic field in a structure, which can be set while allocating the object and can be set to something different while freeing the object. This will provide us whether its a valid object pointer or already freed object pointer or corrupt pointer.;
![](images/icons/contenttypes/comment_16.png) Posted by anand.tiwari at Feb 15, 2013 14:44
\| \|
This is commonly called a 'canary', and is often a good partial solution. Canaries can be spoofed by regular corruption (rarely) or by attackers (more common!).;
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 18, 2013 11:36
\| \|
about revision 58: someone, reading japanese version, pointed out "\*intptr++" means;"\*(intptr++)". I confirmed with the language reference (C17 draft) that "++" operator has higher precedence than "\*", and small test program. Gee...
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Dec 19, 2019 06:36
\|
