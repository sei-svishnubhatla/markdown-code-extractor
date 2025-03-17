Avoid excessive stack allocations, particularly in situations where the growth of the stack can be controlled or influenced by an attacker. See [INT04-C. Enforce limits on integer values originating from tainted sources](INT04-C_%20Enforce%20limits%20on%20integer%20values%20originating%20from%20tainted%20sources) for more information on preventing attacker-controlled integers from exhausting memory.
## Noncompliant Code Example
The C Standard includes support for variable length arrays (VLAs). If the array length is derived from an [untrusted data](BB.-Definitions_87152273.html#BB.Definitions-untrusteddata) source, an attacker can cause the process to perform an excessive allocation on the stack.
This noncompliant code example temporarily stores data read from a source file into a buffer. The buffer is allocated on the stack as a VLA of size `bufsize`. If `bufsize` can be controlled by a malicious user, this code can be [exploited](BB.-Definitions_87152273.html#BB.Definitions-exploit) to cause a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack):
``` c
int copy_file(FILE *src, FILE *dst, size_t bufsize) {
  char buf[bufsize];
  while (fgets(buf, bufsize, src)) {
    if (fputs(buf, dst) == EOF) {
      /* Handle error */
    }
  }
  return 0;
}
```
The BSD extension function `alloca()` behaves in a similar fashion to VLAs; its use is not recommended \[[Loosemore 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Loosemore07)\].
## Compliant Solution
This compliant solution replaces the VLA with a call to `malloc()`. If `malloc()` fails, the return value can be checked to prevent the program from terminating abnormally.
``` c
int copy_file(FILE *src, FILE *dst, size_t bufsize) {
  if (bufsize == 0) {
    /* Handle error */
  }
  char *buf = (char *)malloc(bufsize);
  if (!buf) {
    /* Handle error */
  }
  while (fgets(buf, bufsize, src)) {
    if (fputs(buf, dst) == EOF) {
      /* Handle error */
    }
  }
  /* ... */
  free(buf);
  return 0;
}
```
## Noncompliant Code Example
Recursion can also lead to large stack allocations. Recursive functions must ensure that they do not exhaust the stack as a result of excessive recursions.
This noncompliant implementation of the Fibonacci function uses recursion:
``` c
unsigned long fib1(unsigned int n) {
  if (n == 0) {
    return 0;
  }
  else if (n == 1 || n == 2) {
    return 1;
  }
  else {
    return fib1(n-1) + fib1(n-2);
  }
}
```
The amount of stack space needed grows linearly with respect to the parameter `n`. Large values of `n` have been shown to cause [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).
## Compliant Solution
This implementation of the Fibonacci functions eliminates the use of recursion:
``` c
unsigned long fib2(unsigned int n) {
  if (n == 0) {
    return 0;
  }
  else if (n == 1 || n == 2) {
    return 1;
  }
  unsigned long prev = 1;
  unsigned long cur = 1;
  unsigned int i;
  for (i = 3; i <= n; i++) {
    unsigned long tmp = cur;
    cur = cur + prev;
    prev = tmp;
  }
  return cur;
}
```
Because there is no recursion, the amount of stack space needed does not depend on the parameter `n`, greatly reducing the risk of stack overflow.
## Risk Assessment
Program stacks are frequently used for convenient temporary storage because allocated memory is automatically freed when the function returns. Generally, the operating system grows the stack as needed. However, growing the stack can fail because of a lack of memory or a collision with other allocated areas of the address space (depending on the architecture). When the stack is exhausted, the operating system can terminate the program abnormally. This behavior can be exploited, and an attacker can cause a denial-of-service attack if he or she can control or influence the amount of stack memory allocated.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM05-C | Medium | Likely | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | IO.TAINT.SIZEMISC.MEM.SIZE.BAD | Tainted Allocation SizeUnreasonable Size Argument |
| Coverity | 2017.07 | STACK_USE | Can help detect single stack allocations that are dangerously large, although it will not detect excessive stack use resulting from recursion |
| Helix QAC | 2024.4 | C1051, C1520, C3670 |  |
| Klocwork | 2024.4 | MISRA.FUNC.RECUR |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM05-aCERT_C-MEM05-b | Do not use recursionEnsure the size of the variable length array is in valid range |
| PC-lint Plus | 1.4 | 9035, 9070 | Partially supported: reports use of variable length arrays and recursion |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM05-C | Checks for:Direct or indirect function call to itselfVariable length array with nonpositive sizeTainted size of variable length arrayRec. partially covered. |
| PVS-Studio | 7.35 | V505 |  |

### Related Vulnerabilities
Stack overflow has been implicated in Toyota unintended acceleration cases, where Camry and other Toyota vehicles accelerated unexpectedly.  Michael Barr testified at the trial that a stack overflow could corrupt the critical variables of the operating system, because they were located in memory adjacent to the top of the stack \[Samek 2014\].
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM05-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM05-CPP. Avoid large stack allocations |
| ISO/IEC TR 24772:2013 | Recursion [GDL] |
| MISRA C:2012 | Rule 17.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [Loosemore 2007] | Section 3.2.5, "Automatic Storage with Variable Size" |
| [Samek 2014] | Are We Shooting Ourselves in the Foot with Stack Overflow?Monday, February 17th, 2014 by Miro Samek |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152091) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152115)
## Comments:

|  |
| ----|
| Reading the comments, I'm not sure if this was once in here or not, but it should be pointed out that the same holds true for using alloca(), most implementations I've seen do no sanity checking whatsoever and simply decrement/increment the stack pointer by that much yielding a potentially bogus/dangerous stack pointer.;       
                                        Posted by jf at Aug 20, 2007 09:21
                                     |
| I agree that alloca() warrants concern, but (as pointed out in the comments above) alloca() is not included because it is not a C99 function. 
                                        Posted by jsg at Aug 21, 2007 09:23
                                     |
| Even a couple of BUFSIZed buffers can be too much to allocate as autos.; Some platforms require specification of a fixed stack at link time; this was true for Gould/Encore PowerNode and is also generally true for embedded systems.
                                        Posted by dagwyn at Apr 16, 2008 22:12
                                     |
| If we're going to use C99 in the non-recursive solution, shouldn't the loop start:
for (unsigned int i = 3; i < n; i++)

;That scopes the variable i to the loop.  
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Apr 20, 2008 00:20
\| \|
OK, I've made this change.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 20, 2008 06:44
\| \|
Is there any portable way to know just how much space is available on the stack? How big a VLA can my function have? Could a CCE that uses VLAs even exist?
For that matter could a CCE that employs recursion (where the user can control the level of recursion) exist?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 25, 2008 10:18
\| \|
What qualifies as "large"?
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Jan 09, 2013 19:04
\| \|
Good question, with no good answer. Typically 'too large' here means that something bad happens. Many systems have a fixed page of memory for the stack and the stack overruns that page, the program coredumps. But this is not enforced by the standard...C99 doesn't even define a 'stack', so you could have implementations which don't use a stack (don't ask me what they do instead ![](images/icons/emoticons/smile.svg)
The closest usable statistic that C99 mandates is that your platform must support functions with up to 127 args (S5.2.4.2).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 10, 2013 09:42
\| \|
I think it's important here that the combination of attacker-controlled recursion and large allocations can lead to arbitrary code execution vulnerabilities. For example, if you do threading with pthreads on linux, there is a 4096-byte guard page below the area reserved for the thread stack, and directly below that is memory that was e.g. allocated using malloc() or so. Accesses to the guard page cause an abnormal termination, but if an attacker can cause an application to first use up nearly all the available stack space, then allocate \>=4096 unused bytes on the stack and then call another function, its saved instruction pointer is in a malloc()ed memory area or so where an unprivileged user in another thread might be able to overwrite it.
Is that really low severity?
Edit: But it seems that there are compiler options to mitigate that (-fstack-check for gcc).
![](images/icons/contenttypes/comment_16.png) Posted by thejh at Mar 23, 2014 18:38
\| \|
The Fibonacci example will take;exponential time, but will not consume exponential stack space, will only consume linear stack space.
You can just try it, your application will not crash when n is small number like 500 or 1000,
but will only crash when n reaches 100000 or so. I bet you don't have a stack as large as 2^1000 (or 1.618 ^ 1000) .
In fact you can reason that, since the recursion depth is bounded by parameter n, you will not use more than linear space.
![](images/icons/contenttypes/comment_16.png) Posted by ntysdd at Mar 25, 2014 10:26
\| \|
I've changed the severity to medium. Clearly, excessive stack allocations can corrupt non-stack memory, in light of the Toyota allegations (see the Related Vuls section for details). I'm less confident that an attacker can use large stack allocations to execute arbitrary code, though it should be theoretically possible.
I also suspect that this should be a rule, or we should create a rule saying something like "don't let an attacker make arbitarry stack allocations, using VLAs or recusion". Such a rule would have high severity, as fine control of the stack size would be necessary for an attacker to run arbitrary code.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 11:14
\| \|
Agreed, I changed the text.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 11:16
\| \|
The first example suggests using malloc instead of allocating memory at the stack. Apart from being a relatively complex example (the whole loop and file access has nothing to do with the rule) the mitigation of simply relying on malloc's error handling is a bit disappointing. Allowing an external entity to control the amount of allocated memory is in itself a problem as it might lead to a DoS attack even when heap memory is used.
Also, since the definition of "\[too\] large" is not possibly in a portable manner, wouldn't it make more sense to formulate the rule more similar to the tainted rules of ISO 17961 or [INT04-C](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87148966)? I.e. "validate values that specify the amount of memory to allocate". I suppose one could even argue that [INT04-C](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87148966) could replace this very rule - not because they are equal but due to the lack of a good definition of "\[too\] large". Not even the implementing compiler or static analyzers can determine what "\[too\] large" is in many cases... so this rule is simply a warning sign with no actionable consequences for programmers or tool writers. I presume the standard committees have put way more thought into the issue (of not even introducing stack in their wording) than me... a reference to documentation on these discussions might be useful if it exists.
The "\[[van Sprundel 2006](http://ilja.netric.org/files/Unusual%20bugs.pdf)\]" reference is dead. Maybe referring to the video instead is viable? <https://media.ccc.de/v/23C3-1456-en-unusual_bugs>
![](images/icons/contenttypes/comment_16.png) Posted by stefanct at Aug 22, 2018 13:48
\| \|
Stefan, thanks for your suggestions.
I changed the 1st compliant solution to not return -1 if malloc() fails, mainly for consistency with the rest of the code.
I added a reference to INT04-C as you suggest. INT04-C does not subsume this rec as it does not address memory exhaustion; both are worthwhile recommendations.
You are correct that the C11 standard offers very little help wrt stack exhaustion. It does (barely) acknowledge that every platform actually \*has\* a stack, which can be exhausted, but if exhausted the result is Undefined Behavior. So you are on your own for preventing or detecting stack exhaustion.
I agree that not having any check that the allocation is too large can be problematic, but there is no clear solution how to rectify that. At least malloc() will return null, which is more than you'd get if you used something like alloca() :)
Finally, I killed the "van Sprundel" link. I decided not to add the video because, while interesting, it was not an original source used to build this rule. I'm also uncertain if your video is the some one that the dead link referenced.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 07, 2018 14:13
\|
