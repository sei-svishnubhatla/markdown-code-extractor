Subclause 5.1.2.3 of the C Standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] states:
> In the abstract machine, all expressions are evaluated as specified by the semantics. An actual [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) need not evaluate part of an expression if it can deduce that its value is not used and that no needed side effects are produced (including any caused by calling a function or accessing a volatile object).

This clause gives compilers the leeway to remove code deemed unused or unneeded when building a program. Although this functionality is usually beneficial, sometimes the compiler removes code that it thinks is not needed but has been added for a specific (often security-related) purpose.
## Noncompliant Code Example (`memset()`)
An example of unexpected and unwanted compiler optimizations involves  overwriting the memory of a buffer that is used to store sensitive data. As a result, care must always be taken when dealing with sensitive data to ensure that operations on it always execute as intended. Some compiler optimization modes can remove code sections if the optimizer determines that doing so will not alter the behavior of the program. In this noncompliant code example, optimization may remove the call to `memset()` (which the programmer had hoped would clear sensitive memory) because the variable is not accessed following the write. Check compiler documentation for information about this compiler-specific behavior and which optimization levels can cause this behavior to occur.
``` c
void getPassword(void) {
  char pwd[64];
  if (GetPassword(pwd, sizeof(pwd))) {
    /* Checking of password, secure operations, etc. */
  }
  memset(pwd, 0, sizeof(pwd));
}
```
For all of the compliant solutions provided for this recommendation, it is strongly recommended that the programmer inspect the generated assembly code in the optimized release build to ensure that memory is actually cleared and none of the function calls are optimized out.
## Noncompliant Code Example (`Touching Memory`)
This noncompliant code example accesses the buffer again after the call to `memset()`. This technique prevents some compilers from optimizing out the call to `memset()` but does not work for all [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation). For example, the MIPSpro compiler and versions 3 and later of GCC cleverly nullify only the first byte and leave the rest intact. Check compiler documentation to guarantee this behavior for a specific platform.
``` c
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
    /* Checking of password, secure operations, etc. */
  }
  memset(pwd, 0, sizeof(pwd));
  *(volatile char*)pwd= *(volatile char*)pwd;
}
```
## Noncompliant Code Example (Windows)
This noncompliant code example uses the `ZeroMemory()` function provided by many versions of the Microsoft Visual Studio compiler:
``` c
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
    /* Checking of password, secure operations, etc. */
  }
  ZeroMemory(pwd, sizeof(pwd));
}
```
A call to `ZeroMemory()` may be optimized out in a similar manner to a call to `memset()`.
## Compliant Solution (Windows)
This compliant solution uses a `SecureZeroMemory()` function provided by many versions of the Microsoft Visual Studio compiler. The documentation for the `SecureZeroMemory()` function guarantees that the compiler does not optimize out this call when zeroing memory.
``` c
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
    /* Checking of password, secure operations, etc. */
  }
  SecureZeroMemory(pwd, sizeof(pwd));
}
```
## Compliant Solution (Windows)
The `#pragma` directives in this compliant solution instruct the compiler to avoid optimizing the enclosed code. This `#pragma` directive is supported on some versions of Microsoft Visual Studio and could be supported on other compilers. Check compiler documentation to ensure its availability and its optimization guarantees.
``` c
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
    /* Checking of password, secure operations, etc. */
  }
#pragma optimize("", off)
  memset(pwd, 0, sizeof(pwd));
#pragma optimize("", on)
}
```
## Compliant Solution (C99)
This compliant solution uses the `volatile` type qualifier to inform the compiler that the memory should be overwritten and that the call to the `memset_s()` function should not be optimized out. Unfortunately, this compliant solution may not be as efficient as possible because of the nature of the `volatile` type qualifier preventing the compiler from optimizing the code at all. Typically, some compilers are smart enough to replace calls to `memset()` with equivalent assembly instructions that are much more efficient than the `memset()` implementation. Implementing a `memset_s()` function as shown in the example may prevent the compiler from using the optimal assembly instructions and can result in less efficient code. Check compiler documentation and the assembly output from the compiler.
``` c
/* memset_s.c */
errno_t memset_s(void *v, rsize_t smax, int c, rsize_t n) {
  if (v == NULL) return EINVAL;
  if (smax > RSIZE_MAX) return EINVAL;
  if (n > smax) return EINVAL;
  volatile unsigned char *p = v;
  while (smax-- && n--) {
    *p++ = c;
  }
  return 0;
}
/* getPassword.c */
extern errno_t memset_s(void *v, rsize_t smax, int c, rsize_t n);
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
     /* Checking of password, secure operations, etc. */
  }
  if (memset_s(pwd, sizeof(pwd), 0, sizeof(pwd)) != 0) {
    /* Handle error */
  }
}
```
However, note that both calling functions and accessing `volatile`-qualified objects can still be optimized out (while maintaining strict [conformance](BB.-Definitions_87152273.html#BB.Definitions-conforming) to the standard), so this compliant solution still might *not* work in some cases.  The `memset_s()` function introduced in C11 is the preferred solution (see the following solution for more information).  If `memset_s()` function is not yet available on your implementation, this compliant solution is the best alternative, and can be discarded once supported by your implementation.
## Compliant Solution (C11, Annex K)
As of C11, tAnnex K of the C Standard includes a `memset_s` function. Subclause K.3.7.4.1, paragraph 4 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\], states:
> Unlike `memset`, any call to the `memset_s` function shall be evaluated strictly according to the rules of the abstract machine as described in (5.1.2.3). That is, any call to the `memset_s` function shall assume that the memory indicated by `s` and `n` may be accessible in the future and thus must contain the values indicated by `c`.

Note that Annex K is conditionally normative, so it may not be available on all platforms.
``` c
void getPassword(void) {
  char pwd[64];
  if (retrievePassword(pwd, sizeof(pwd))) {
     /* Checking of password, secure operations, etc. */
  }
  memset_s(pwd, 0, sizeof(pwd));
}
```
## Noncompliant Code Example
In rare cases, use of an empty infinite loop may be unavoidable. For example, an empty loop may be necessary on a platform that does not support `sleep(3)` or an equivalent function. Another example occurs in OS kernels. A task started before normal scheduler functionality is available may not have access to `sleep(3)` or an equivalent function. An empty infinite loop that does nothing within the loop body is a suboptimal solution because it consumes CPU cycles but performs no useful operations. An optimizing compiler can remove such a loop, which can lead to unexpected results. According to the C Standard, subclause 6.8.5, paragraph 6 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\],
> An iteration statement whose controlling expression is not a constant expression, that performs no input/output operations, does not access volatile objects, and performs no synchronization or atomic operations in its body, controlling expression, or (in the case of a for statement) its expression-3, may be assumed by the implementation to terminate.157157) This is intended to allow compiler transformations, such as removal of empty loops, even when termination cannot be proven.

This noncompliant code example implements an idle task that continuously executes a loop without executing any instructions within the loop. An optimizing compiler could remove the `while` loop in the example.
``` c
static int always = 1;
int main(void) {
  while (always) { }
}
```
## Compliant Solution (`while`)
To avoid the loop being optimized away, this compliant solution uses a constant expression `(1)` as the controlling expression in the `while` loop:
``` c
int main(void) {
  while (1) { }
}
```
## Compliant Solution (`for)`
According to the C Standard, subclause 6.8.5.3, paragraph 2, omitting the *expression-2* from a `for` loop will replace that expression with a nonzero constant.
``` c
int main(void) {
  for (;;) { }
}
```
## Risk Assessment
If the compiler optimizes out memory-clearing code, an attacker can gain access to sensitive data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC06-C | Medium | Probable | Medium | P8 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC06-C).
### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.MEMSET | Use of memset |
| LDRA tool suite | 9.7.1 | 35 S, 57 S, 8 D,65 D, 76 D, 105 D,
I J, 3 J | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC06-a | Avoid calls to memory-setting functions that can be optimized out by the compiler |
| PC-lint Plus | 1.4 | 586 | Assistance provided |
| PVS-Studio | 7.35 | V597, V712 |  |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC06-CPP. Be aware of compiler optimization when dealing with sensitive data |
| CERT Oracle Secure Coding Standard for Java | MSC01-J. Do not use an empty infinite loop |
| MITRE CWE | CWE-14, Compiler removal of code to clear buffers |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.8.5, "Iteration Statements"Subclause K.3.7.4.1, "The memset_s Function" |
| [MSDN] | "SecureZeroMemory""Optimize (C/C++)" |
| [PVS-Studio] | "Safe Clearing of Private Data" |
| [US-CERT] | "MEMSET" |
| [Wheeler 2003] | Section 11.4, "Specially Protect Secrets (Passwords and Keys) in User Memory" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152083) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152362)
## Comments:

|  |
| ----|
| A typical way to trick the compiler into not eliminating such code and not having a seriously detrimental impact on a program is to create an extern function that does nothing and, after clearing the contents of the variable in question, call that function passing the variable to that function. For safety's sake, I always put any do nothing functions on a separate file so that the compiler has no possible chance to optimize the calls out.
                                        Posted by wlf@cert.org at Apr 28, 2007 09:53
                                     |
| A couple of comments.  I wouldn't necessary character "compiler optimizations" as insecure.  They are doing what they are supposed to.
I'm not sure the term "dead code" is used correctly here.  Dead code, is code that exists in the source code of a program but can never be executed.  I think here you want to say that "code may be removed by the optimizer if it determines that doing so will not alter the behavior of the program."
Don't reference GCC in the main body of the description, as this is a specific implementation.  You can provide an h3.Implementation Details section if you so desire.
I'm not too crazy about your solutions, either.  Did you evaluate the use of "volatile" to ensure the memset is not optimized out?  If so, you should also list this as a second non-compliant example because there is literature out there which suggests this approach.
                                        Posted by rcs at Apr 28, 2007 12:13
                                     |
| Indeed - I just didn't think that was "nice enough" to include as a potential solution. You never can tell what is acceptable or not - I had assumed that if I included a recommendation to use code which does nothing that I would get very negative feedback.
                                        Posted by jdamato at Apr 28, 2007 13:34
                                     |
| 
I'm not sure the term "dead code" is used correctly here. 
I think the actual definition varies a bit, as I've seen it used in both contexts about equally. Since it is slightly ambiguous, I will change it.
Did you evaluate the use of "volatile" to ensure the memset is not optimized out? If so, you should also list this as a second non-compliant example because there is literature out there which suggests this approach.
I did. It doesn't seem to me that literature suggests volatile will prevent this from occurring. The literature I read about volatile suggests that volatile should be used for memory-mapped devices, globals that can be modified by interrupt service routines, or globals which are modified by multi-threaded applications.
I could include a non-compliant code for this if you'd like, but it doesn't seem to make any sense to me.
                                        Posted by jdamato at Apr 28, 2007 13:46
                                     |
| In general, volatile does not work. This is due to the way certain optimizers work. Some phases of some optimizers work only on the resulting machine code looking to eliminate useless instructions. They are not working at the C level. GCC is the best example because it knows the mem functions and does not call them. It inlines machine code to do what it knows they do. And then the machine code optimizer phase deletes the instructions. It would have done no good to declare the variable a different way because the machine code optimizer will still see it is useless instructions (whether the data in question is in memory or in a register does not matter). That is also why the fake function call does work, because the machine code optimizer cannot tell whether the function call uses or modifies the variable in question. Compilers without machine code optimizers may behave differently. And conceivably a compiler with a static function call analyzer may be able to eliminate the useless function call and reintroduce the problem.
Any workarounds for this problem must necessarily be compiler-specific unless there is a standard mandatory source code pragma that can disable optimization for so-annotated code.;
                                        Posted by wlf@cert.org at Apr 29, 2007 11:33
                                     |
| Take a look at what David Wheeler has to say on the subject at:
http://www.dwheeler.com/secure-programs/Secure-Programs-HOWTO/protect-secrets.html
                                        Posted by rcs at Apr 30, 2007 13:29
                                     |
| Alternatively, instead of using memset(), call an extern function to do the memory setting - it can even use memset() to retain the probable optimization of memset(), reducing the cost to the negligible overhead of a function call.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 02:42
                                     |
| Google LTO - Link Time Optimization.
Putting a function in another file may keep it safe from the compiler,
but not necessarily from optimizing linkers.  I know little about it
myself though, so I donÂ´t know if it applies to this situation.
                                        Posted by hbf at Apr 17, 2008 17:17
                                     |
| Conforming compilers have to implement volatile semantics correctly; thus simple "peephole" optimization is not allowed (some sort of volatility labels must be attached and obeyed).; The cited C99 text is misleading, in that the parenthetical only describes how needed side effects may be produced, not examples of what can be eliminated.
A much simpler compliant solution is
memset((volatile char *)pwd, 0, sizeof(pwd));
                                        Posted by dagwyn at Apr 18, 2008 14:00
                                     |
| Should this code snippet in the third CCE have an explicit cast to char to avoid violating INT07-C. Use only explicitly signed or unsigned char type for numeric values?
volatile char *p = v;
  while (n--)
    *p++ = c;

![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 30, 2008 11:05
\| \|
The relevant recommendation in this case is [STR00-C. Represent characters using an appropriate type](STR00-C_%20Represent%20characters%20using%20an%20appropriate%20type) and it is to use unsigned char for situations where the object being manipulated might be of any type, and it is necessary to access all bits of that object, as with fwrite().
The code above was wrong, so I corrected it. However INT07-A was never violated because this is not a numeric value, it is a situation where the object being manipulated may be of any type.
Perhaps we can automatically detect this because of the cast from void \*?
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jan 21, 2009 01:33
\| \|
I don't think this is unenforceable. A compiler is certainly making the assessment that it can optimize out some code. If the compiler provided a flag allowing it to "diagnose" when it performs dead code removal would detect this violation. For static analysis tools this would be much harder, because they would need to recreate the optimizer, but not impossible.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Feb 17, 2009 10:04
\| \|
I think you're saying that this rule is enforceable because a static analyzer can (theoretically) predict when a compiler may optimize away some critical code, such as `memset()`. I'll agree that a static analyzer can predict such an optimization. However, a static analyzer IMO cannot determine whether such an optimization is undesirable, hence the unenforceable tag.
To make this rule enforceable we would need to establish when a bit of code is critical and should not be optimized away.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 18, 2009 12:58
\| \|
After the 3rd CCE:
> However, note that both calling functions and accessing `volatile`-qualified objects can still be optimized out (while maintaining strict [conformance](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions#BB.Definitions-conforming) to the standard), so without a C-conforming implementation, this compliant solution still might *not* work in some cases.

"so without a C-conforming implementation" should be read as "even with a C-conforming implementation"?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Aug 21, 2014 20:03
\| \|
Yes, but it is not necessary to say so because we always assume a conforming implementation.; The description needed some further updates anyway, so I rewrote it.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 22, 2014 11:23
\| \|
The memset_s C99 solution should use a different name for the secure memset function, so as to not conflate it with the C11 memset_s.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 20, 2015 20:50
\| \|
I think I entirely disagree.; I would definitely name my function memset_s() so that when the code is ported to a library that conforms to C11 Annex K the custom implementation can simply be ifdef'd out and the standard library solution used without any other modification to the code.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jun 01, 2015 13:38
\| \|
"accessing `volatile`-qualified objects can still be optimized out" When exactly? Doesn't that defeat the whole purpose of `volatile`?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 11:34
\| \|
We should make it more clear that memset_s is not a required part of the C standard, but rather part of the optional Annex K, since so many widely-used implementations (e.g., glibc and musl) don't support it.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 11:42
\| \|
e.g., dead code elimination:;<https://godbolt.org/z/qhVUj8>
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 30, 2020 11:44
\| \|
I'd argue that while the code to do the volatile access was optimized out, the volatile access itself was not, since it wouldn't have occurred even without optimization.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 11:52
\| \|
Then as another example: the implementation is free to ignore the volatile access here because the original object was not declared as volatile:;<https://godbolt.org/z/kvhs6R>
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 30, 2020 12:05
\| \|
But that's not accessing a `volatile`-qualified object then. It's just accessing a regular object through a `volatile`-qualified pointer.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 12:12
\| \|
I think you may be missing the forest for the trees with this bit. From the perspective of the person writing the function, the parameter is a pointer to a volatile int and they may reasonably expect that the volatile accesses in their function will not be optimized away and rely on that. From the perspective of a tool that has knowledge about all compilation units in the program (like a link-time code generator), it turns out that the access wasn't volatile on any code path and so the access can be removed. The danger here is for the API author who was relying on the volatile access. You can see this in action by simply adding a call which;**does** pass a pointer to a volatile object, even when that call is otherwise useless, which causes all calls to `func()` to use volatile accesses again: <https://godbolt.org/z/rBLNEn>
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 30, 2020 12:32
\| \|
I suppose at this point I am just nitpicking our wording a little bit.
Side note: [DR 476](http://www.open-std.org/jtc1/sc22/wg14/www/docs/summary.htm#dr_476) argues that it's a defect in the standard that things work like that.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jun 30, 2020 12:59
\| \|
Agreed, I added this clarification.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 30, 2020 14:09
\|
