An object that has volatile-qualified type may be modified in ways unknown to the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) or have other unknown side effects. Asynchronous signal handling, for example, may cause objects to be modified in a manner unknown to the compiler. Without this type qualifier, unintended optimizations may occur. These optimizations may cause race conditions because a programmer may write code that prevents a race condition, yet the compiler is not aware of the programmer's data model and may modify the code during compilation to permit race conditions.
The `volatile` keyword eliminates this confusion by imposing restrictions on access and caching. According to the C99 Rationale \[[C99 Rationale 2003](AA.-Bibliography_87152170.html#AA.Bibliography-C992003)\],
> No caching through this [lvalue](BB.-Definitions_87152273.html#BB.Definitions-lvalue): each operation in the abstract semantics must be performed (that is, no caching assumptions may be made, because the location is not guaranteed to contain any previous value). In the absence of this qualifier, the contents of the designated location may be assumed to be unchanged except for possible aliasing.

Type qualifying objects as volatile does not guarantee synchronization between multiple threads, protect against simultaneous memory accesses, or, unless used to declare objects of type `sig_atomic_t`, guarantee atomicity of accesses to the object. For restrictions specific to signal handlers, see [SIG31-C. Do not access shared objects in signal handlers](SIG31-C_%20Do%20not%20access%20shared%20objects%20in%20signal%20handlers). However, type qualifying objects as volatile does ensure that a conforming compiler will not elide or reorder access to the object.
## Noncompliant Code Example
In this noncompliant code example, the programmer is targeting a custom piece of hardware that controls an LED by writing values into a register bank. The register bank is memory mapped into the process such that writing to a specific memory location will actually place a value into a hardware register to be read by the LED controller. The programmer intends to turn the LED on by placing value 1 into the first register, and then turn the LED off later by placing the value 0 into the first register.
``` c
#include <stddef.h>
#include <stdint.h>
extern void get_register_bank(int32_t **bank,
                              size_t *num_registers);
extern void external_wait(void);
void func(void) {
  int32_t bank[3];
  size_t num_regs = 3;
  get_register_bank((int32_t **)&bank, &num_regs);
  if (num_regs < 3) {
    /* Handle error */
   }
  bank[0] = 1;
  external_wait();
  bank[0] = 0;
}
```
The compiler is free to optimize what it perceives as being a dead store to `bank[0]` by removing the first assignment to the variable. This would cause the LED to never be turned on in an optimized build. 
## Compliant Solution
In this compliant solution, the register bank's memory is qualified with the `volatile` keyword, ensuring the compiler does not optimize access to the memory.
``` c
#include <stddef.h>
#include <stdint.h>
extern void get_register_bank(volatile int32_t **bank,
                              size_t *num_registers);
extern void external_wait(void);
void func(void) {
  volatile int32_t bank[3];
  size_t num_regs = 3;
  get_register_bank((volatile int32_t **)&bank, &num_regs);
  if (num_regs < 3) {
    /* Handle error */
   }
  bank[0] = 1;
  external_wait();
  bank[0] = 0;
}
```
## Risk Assessment
Failure to declare variables containing data that cannot be cached as volatile can result in unexpected runtime behavior resulting from compiler optimizations.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL22-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | ;9.7.1 | 8 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL22-a | Avoid unused values |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL22-C | Checks for write without a further read (rule partially covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL22-C).
## Related Guidelines

|  |  |
| ----|----|
| CERT C Secure Coding Standard | SIG31-C. Do not access shared objects in signal handlers |
| SEI CERT C++ Coding Standard | VOID DCL20-CPP. Use volatile for data that cannot be cached |
| MISRA C:2012 | Rule 2.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [C99 Rationale 2003] | ;Subclause 6.7.3, "Type Qualifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152320) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152406)
## Comments:

|  |
| ----|
| The ISO C standard says:
An object that has volatile-qualified type may be modified in ways unknown to the implementation or have other unknown side effects.
As I read that, a signal handler modifying a global variable would not appear as 'unknown to the implementation' or 'have other unknown side effects'.
Do you have a compiled version of the non-compliant solution that runs forever?
                                        Posted by hburch at May 24, 2007 10:29
                                     |
| No, I dont. 
I found a description of this somewhere. I'm trying to find it again.
Also, here are non-signal examples. I didn't notice this page before.
https://www.securecoding.cert.org/confluence/display/seccode/Use+volatile+type+qualifer+for+objects+of+automatic+storage+duration+that+are+modified+between+setjmp%28%29+and+longjmp%28%29
                                        Posted by jpincar at May 24, 2007 10:42
                                     |
| Found it.
http://docs.sun.com/source/819-3688/tguide.html#pgfId-997898
search for "while (flag)"
                                        Posted by jpincar at May 24, 2007 10:53
                                     |
| Marking a variable volatile will only have the desired effect IF the variable can be loaded/stored atomically (more complex than a natural integer). If, for example, the variable is a struct, marking it volatile will only prevent the compiler from caching pieces of its content in registers; it won't help synchronize interleaved modifications. A real concurrency control structure is required to do this.
                                        Posted by wlf@cert.org at May 25, 2007 12:32
                                     |
| The specific example of signal handling is covered by SIG31-C.
The volatile keyword essentially tells the compiler "this variable is special in ways you can't detect". So it is inherently undebatable...if it was easy to determine if a varaible should be volatile or not, the compiler could detect it, rendering the volatile keyword unnecessary. I would therefore assert this rule is not automatically enforceable and should therefore be a recommendation.
                                        Posted by svoboda at Mar 07, 2008 11:40
                                     |
| Failing to use volatile can also cause an aggressive optimizer to remove whole bits of code if it thinks that it knows in advance that it will or won't be used: this can be a big surprise also, especially when Heisenbugs enter the picture (bugs that go away when you turn on the debugger and/or compile w/ debugging).
                                        Posted by steve at Mar 13, 2008 20:46
                                     |
| Please consider noting that volatile only affects reordering and optimization done by the compiler; it does not cause the compiler to emit any necessary memory barriers for multiprocessor synchronization.  Many programmers assume that using volatile precludes the need for memory barriers.
                                        Posted by josh@freedesktop.org at Mar 16, 2008 06:36
                                     |
| The requirements for threads haven't yet been worked out.
Another compliant solution involves using while (*(volatile sig_atomic_t *)&i) and is worth showing since too many programmers think that using volatile qualification means that all accesses are going to be uncached (and thus slow).
                                        Posted by dagwyn at Apr 15, 2008 14:07
                                     |
| compiling on gcc with -O causes the program to ignore SIGINT
(note... if you try this at home, you can kill it with a SIGHUP or some other similar signal)
                                        Posted by avolkovi at May 16, 2008 16:06
                                     |
| done
                                        Posted by avolkovi at May 16, 2008 16:24
                                     |
| i believe this has been addressed by the emphasis on unexpected optimization
                                        Posted by avolkovi at May 16, 2008 16:32
                                     |
| i believe this has been addressed
                                        Posted by avolkovi at May 16, 2008 16:32
                                     |
| 1) added references to SIG31 and from there to here
2) i disagree, this rule is automatically enforceable by marking all variables as volatile.. sure that disables many optimizations, but the standard doesn't say that code must execute super fast
                                        Posted by avolkovi at May 16, 2008 16:40
                                     |
| i believe this has been addressed by the warning about synchronization
                                        Posted by avolkovi at May 16, 2008 16:41
                                     |
| After discussion with Alex, I agree this is still a valid rule. We could enforce it by enumerating the cases where 'volatile' is warranted, and checking those cases.
                                        Posted by svoboda at May 16, 2008 17:12
                                     |
| Marked 'unenforceable' because the 'volatile' term defies static analysis...it is the programmer instructing the compiler that its static analysis that a variable can be optimized away is wrong.
                                        Posted by svoboda at Jul 16, 2008 12:37
                                     |
| I think the noncompliant code examples in this rule can be easily diagnosed, as well as others. I don't think we should list this as unenforceable, particularly since this is is a rule and therefore must be enforceable by definition.
                                        Posted by rcs_mgr at Jun 06, 2009 00:05
                                     |
| This rule may be correct as far as it goes, but the NCCE/CS code is all about signal handlers, and is more suited for  SIG31-C. Do not access or modify shared objects in signal handlers. I wish we had a non-signal-based code samples for this rule.
                                        Posted by svoboda at Jan 15, 2010 10:27
                                     |
| The nice thing about using signals is that the examples can be strictly conforming C programs. Let me see if I can cook up one that doesn't involve signals.
                                        Posted by martinsebor at Jan 15, 2010 11:57
                                     |
| Actually signal(2) is fraught with security problems, mainly because it tries to introduce concurrency into C, at a time when C had no way of handling concurrency issues.  POSIX has long recommended sigaction(2), which is much stronger.  But WG14 refuses to admit sigaction(2) into their standard, mainly because it brings too much baggage into C. I think WG14 is hoping no one actually notices that signal(2) is in C99  
The CS here is one of the few strictly-conforming programs that works using signal()...if you study the Signals section, you'll see most of the CS's use sigaction().
                                        Posted by svoboda at Jan 15, 2010 14:30
                                     |
| The only examples that come to mind that do not involve signals are those that either rely on threads or some hardware register(s). The former will require making use of some threads API (e.g., Pthreads), while the latter would probably be a little hand-wavy. Unless someone has an objection or another preference I'll work on replacing the second non-compliant example (Cast to volatile) with one involving Pthreads.
                                        Posted by martinsebor at Jan 16, 2010 19:02
                                     |
| Originally the scope of this document was C99.  Consequently, we tried to ensure that all noncompliant code examples represented errors you can make in C99 conforming programs, although we allowed for the compliant solutions to lie outside C99.
Because the CSCG SG is looking at C99 and C1X, I've sort of decided we should expand the scope of these guidelines to include C1X as well.  If you agree with this, it might make more sense for the noncompliant code example to be based on the threading API that has been added to C1X.
A POSIX based noncompliant code example could go into the posix section. Another good Windows example might be structured exceptions.
                                        Posted by rcs at Jan 16, 2010 20:29
                                     |
| I agree in principle. Regarding the threads API proposed for C1x, however, I actually have some rather strong reservations about it: I believe it's a mistake to adopt a proprietary interface when a standard one is widely established and well specified. The proposed interface is neither.
                                        Posted by martinsebor at Jan 17, 2010 10:00
                                     |
| I am trespassing here but I encountered some posts on the Java Concurrency Mailing list which say (general) race conditions != data races. It appears from the posts that this paper was used to write the Java Memory Model. 
From  chapter 2.2.1 of "Java Concurrency In Practice" from Brian Goetz, Tim Peierls, Joshua Bloch, Joseph Bowbeer, David Holmes, Doug Lea:
The term race condition is often confused with the related term data race, which arises when synchronization is not used to coordinate all access to a shared nonfinal field. You risk a data race whenever a thread writes a variable that might next be read by another thread or reads a variable that might have last been written by another thread if both threads do not use synchronization; code with data races has no useful defined semantics under the Java Memory Model. Not all race conditions are data races, and not all data races are race conditions, but they both can cause concurrent programs to fail in unpredictable ways.
So for example this text from the guideline:
Note, however, that declaring an object volatile is not sufficient to prevent race conditions when the object is simultaneously accessed from within two or more threads of execution.  
could perhaps use data races instead of race conditions.
                                        Posted by dmohindr at Jan 17, 2010 13:44
                                     |
| The Getz book does not provide a definition for data races that does not involve the Java Memory Model, so I don't think the distinction between data race/race condition exists outside Java.
                                        Posted by svoboda at Jan 18, 2010 09:17
                                     |
| Thanks for your feedback! I'm not sure what the status of the C memory model is but the C++ 1x memory model (see N2664 ) does indeed define the term data race and doesn't speak of race conditions. Quoting from the [intro.multithread] section of the current C++ 1x Draft Working Paper (N3000 ):
The execution of a program contains a data race if it contains two conflicting actions in different threads, at least one of which is not atomic, and neither happens before the other. Any such data race results in undefined behavior.
Therefore, I will correct the wording as you suggest.
I considered replacing all references to race condition with data race on this page but rejected the idea because with just one exception, none of them actually fit the definition  of the term I added to the BB. Definitions section.
                                        Posted by martinsebor at Jan 18, 2010 17:03
                                     |
| I'm getting a feeling that the Noncompliant Code Example (Cast to volatile) doesn't belong in this section.;  Right now, the big problem is that there is no CS to go with this example.  The example shows an invalid way to synchronize between threads, so it should probably be moved to a rule that deals with thread synchronization.
                                        Posted by rcs at Nov 05, 2012 08:28
                                     |
| On behalf of MISRA Working group:; I have added a reference to MISRA C:2012 rule 2.2 "There shall be no dead code", even though it is not a precise match to this guideline.  Examples such as the ones given here, would be caught a "dead code" rule since the value of the first assignment to bank[0] is never used.
                                        Posted by liz.whiting@ldra.com at Sep 30, 2014 03:41
                                     |
| Risk AssessmentBlah blah blahHmm. Looks like some description is missing.
                                        Posted by sami.merila at Oct 16, 2014 07:06
                                     |
| fixed.; I should do a search for "blah blah blah" but I'm afraid.  
                                        Posted by rcs_mgr at Oct 16, 2014 09:18
                                     |
| Interesting.; I'm assuming the compliant solution would not be flagged under this rule?
                                        Posted by rcs_mgr at Oct 16, 2014 09:20
                                     |
| I just did a search, and it now only appears in comments.;
                                        Posted by aballman at Oct 16, 2014 13:46
                                     |

