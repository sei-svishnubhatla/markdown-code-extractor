When accessing a bit-field, a thread may inadvertently access a separate bit-field in adjacent memory. This is because compilers are required to store multiple adjacent bit-fields in one storage unit whenever they fit. Consequently, data races may exist not just on a bit-field accessed by multiple threads but also on other bit-fields sharing the same byte or word.  A similar problem is discussed in [CON43-C. Do not allow data races in multithreaded code](CON43-C_%20Do%20not%20allow%20data%20races%20in%20multithreaded%20code), but the issue described by this rule can be harder to diagnose because it may not be obvious that the same memory location is being modified by multiple threads.
One approach for preventing data races in concurrent programming is to use a mutex. When properly observed by all threads, a mutex can provide safe and secure access to a shared object. However, mutexes provide no guarantees with regard to other objects that might be accessed when the mutex is not controlled by the accessing thread. Unfortunately, there is no portable way to determine which adjacent bit-fields may be stored along with the desired bit-field.
Another approach is to insert a non-bit-field member between any two bit-fields to ensure that each bit-field is the only one accessed within its storage unit. This technique effectively guarantees that no two bit-fields are accessed simultaneously.
## Noncompliant Code Example (Bit-field)
Adjacent bit-fields may be stored in a single memory location. Consequently, modifying adjacent bit-fields in different threads is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), as shown in this noncompliant code example:
``` c
struct multi_threaded_flags {
  unsigned int flag1 : 2;
  unsigned int flag2 : 2;
};
struct multi_threaded_flags flags;
int thread1(void *arg) {
  flags.flag1 = 1;
  return 0;
}
int thread2(void *arg) {
  flags.flag2 = 2;
  return 0;
}
```
The C Standard, 3.17, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], states
> Note 2 to entry: A bit-field and an adjacent non-bit-field member are in separate memory locations. The same applies to two bit-fields, if one is declared inside a nested structure declaration and the other is not, or if the two are separated by a zero-length bit-field declaration, or if they are separated by a non-bit-field member declaration. It is not safe to concurrently update two non-atomic bit-fields in the same structure if all members declared between them are also (nonzero-length) bit-fields, no matter what the sizes of those intervening bit-fields happen to be.

For example, the following instruction sequence is possible:
``` java
Thread 1: register 0 = flags
Thread 1: register 0 &= ~mask(flag1)
Thread 2: register 0 = flags
Thread 2: register 0 &= ~mask(flag2)
Thread 1: register 0 |= 1 << shift(flag1)
Thread 1: flags = register 0
Thread 2: register 0 |= 2 << shift(flag2)
Thread 2: flags = register 0
```
## Compliant Solution (Bit-field, C11, Mutex)
This compliant solution protects all accesses of the flags with a mutex, thereby preventing any data races:
``` c
#include <threads.h>
struct multi_threaded_flags {
  unsigned int flag1 : 2;
  unsigned int flag2 : 2;
};
struct mtf_mutex {
  struct multi_threaded_flags s;
  mtx_t mutex;
};
struct mtf_mutex flags;
int thread1(void *arg) {
  if (thrd_success != mtx_lock(&flags.mutex)) {
    /* Handle error */
  }
  flags.s.flag1 = 1;
  if (thrd_success != mtx_unlock(&flags.mutex)) {
    /* Handle error */
  }
  return 0;
}
int thread2(void *arg) {
  if (thrd_success != mtx_lock(&flags.mutex)) {
    /* Handle error */
  }
  flags.s.flag2 = 2;
  if (thrd_success != mtx_unlock(&flags.mutex)) {
    /* Handle error */
  }
  return 0;
}
```
## Compliant Solution (C11)
In this compliant solution, two threads simultaneously modify two distinct non-bit-field members of a structure. Because the members occupy different bytes in memory, no concurrency protection is required.
``` c
struct multi_threaded_flags {
  unsigned char flag1;
  unsigned char flag2;
};
struct multi_threaded_flags flags;
int thread1(void *arg) {
  flags.flag1 = 1;
  return 0;
}
int thread2(void *arg) {
  flags.flag2 = 2;
  return 0;
}
```
Unlike C99, C11 and C23 explicitly define a memory location and provides the following note in subclause 3.17 paragraph 2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\]:
> Note 1 to entry: Two threads of execution can update and access separate memory locations without interfering with each other.

It is almost certain that `flag1` and `flag2` are stored in the same word. Using a compiler that conforms to C99 or earlier, if both assignments occur on a thread-scheduling interleaving that ends with both stores occurring after one another, it is possible that only one of the flags will be set as intended. The other flag will contain its previous value because both members are represented by the same word, which is the smallest unit the processor can work on. Before the changes were made to the C Standard for C11, there were no guarantees that these flags could be modified concurrently.
## Risk Assessment
Although the race window is narrow, an assignment or an expression can evaluate improperly because of misinterpreted data resulting in a corrupted running state or unintended information disclosure.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| CON32-C | Medium | Probable | Medium | P8 | L2 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | read_data_racewrite_data_race | Supported by sound analysis (data race alarm) |
| Axivion Bauhaus Suite | 7.2.0 | CertC-CON32 |  |
| CodeSonar | 8.3p0 | CONCURRENCY.DATARACECONCURRENCY.MAA
 | Data raceMultiple Accesses of Atomic |
| Coverity | 2017.07 | MISSING_LOCK | Partially implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-con32-c |  |
| Helix QAC | 2024.4 | C1774, C1775 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-CON32-a | Use locks to prevent race conditions when modifying bit fields |
| PC-lint Plus | 1.4 | 457 | Partially supported: access is detected at the object level (not at the field level) |
| Polyspace Bug Finder | R2024a | CERT C: Rule CON32-C | Checks for data race (rule fully covered) |

### Related Vulnerabilities
Search for [vulnerabilities](http://BB.%20Definitions#vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+CON32-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | 3.17, "Memory Location" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152173) [](../c/Rule%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152247)
## Comments:

|  |
| ----|
| The issue is stated incorrectly; it is not specific to bit fields, but applies to nearby variables in general, since to access one may involve loading a wider set of bits, especially likely when using a word-addressed machine.; Also, the implementation is required to modify only the specified bits (when there is only a single thread), which is contrary to what seems to be stated.  It is true that a mutex is needed (anyway) and that it needs to protect any adjacent variables that might be spanned by the load/store.  Unfortunately there is no portable way to determine just what that span is.  Most likely, if non-floating types are used, unioning with a long (that is not used except for alignment) provides a safe span (pushing other nearby variables outside the load/store width).
                                        Posted by dagwyn at Apr 18, 2008 15:20
                                     |
| Rewrote rule to address this concern (I hope 
                                        Posted by svoboda at Jun 19, 2008 14:11
                                     |
| We need to an exception to handle non-blocking algorithms & compare-and-swap.
                                        Posted by svoboda at Oct 22, 2010 09:57
                                     |
| ;This rule needs another good look.  The first noncompliant example is really compliant in our scope.  Huh?
                                        Posted by rcs at Oct 29, 2013 10:27
                                     |
| I think the point was to show valid information; the code in C11 is fine, but on a C99 compiler or earlier it is not fine.; It's kind of like what we did for EXP35-C. Do not modify objects with temporary lifetime, only far more clear.
                                        Posted by aballman at Oct 29, 2013 10:34
                                     |
| Robert is correct, the first noncompliant example is compliant for C11, we are focusing on C11. ;Maybe a better approach is to make this first noncompliant example a C11 compliant example, with a note that points out that in earlier C compliant compilers there is no guarantees that the two flags can be modified concurrently.
                                        Posted by bluepilot at Oct 29, 2013 10:58
                                     |
| So long as we keep the information that notes the code is not fine in earlier versions of the language, I'm okay with that.
                                        Posted by aballman at Oct 29, 2013 11:04
                                     |
| I think that is what I was suggesting.
                                        Posted by bluepilot at Oct 29, 2013 11:12
                                     |
| How about listing atomic bit-fields as an implementation-defined compliant solution?
                                        Posted by rcseacord at Oct 12, 2018 23:18
                                     |
| Do you know of any implementations that provide atomic access to bit-fields? Both Clang and GCC err on trying to declare such a thing, and MSVC doesn't support;_Atomic at all.
                                        Posted by aballman at Oct 13, 2018 11:54
                                     |
| No, I don't.; Maybe we can find out next week.  I also have a related question about what the heck a "maximal sequence of adjacent bit-fields all having nonzero width" is.
                                        Posted by rcseacord at Oct 13, 2018 12:17
                                     |

