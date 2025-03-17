Sensitive data stored in reusable resources may be inadvertently leaked to a less privileged user or attacker if not properly cleared. Examples of reusable resources include
-   Dynamically allocated memory
-   Statically allocated memory
-   Automatically allocated (stack) memory
-   Memory caches
-   Disk
-   Disk caches
The manner in which sensitive information can be properly cleared varies depending on the resource type and platform.
## Noncompliant Code Example (`free()`)
Dynamic memory managers are not required to clear freed memory and generally do not because of the additional runtime overhead. Furthermore, dynamic memory managers are free to reallocate this same memory. As a result, it is possible to accidentally leak sensitive information if it is not cleared before calling a function that frees dynamic memory. Programmers also cannot rely on memory being cleared during allocation.
To prevent information leakage, sensitive information must be cleared from dynamically allocated buffers before they are freed. Calling `free()` on a block of dynamic memory causes the space to be deallocated; that is, the memory block is made available for future allocation. However, the data stored in the block of memory to be recycled may be preserved. If this memory block contains sensitive information, that information may be unintentionally exposed.
In this noncompliant example, sensitive information stored in the dynamically allocated memory referenced by `secret` is copied to the dynamically allocated buffer, `new_secret`, which is processed and eventually deallocated by a call to `free()`. Because the memory is not cleared, it may be reallocated to another section of the program where the information stored in `new_secret` may be unintentionally leaked.
``` c
char *secret;
/* Initialize secret to a null-terminated byte string, 
   of less than SIZE_MAX chars */
size_t size = strlen(secret);
char *new_secret;
new_secret = (char *)malloc(size+1);
if (!new_secret) {
  /* Handle error */
}
strcpy(new_secret, secret);
/* Process new_secret... */
free(new_secret);
new_secret = NULL;
```
## Compliant Solution
To prevent information leakage, dynamic memory containing sensitive information should be [sanitized](BB.-Definitions_87152273.html#BB.Definitions-sanitize) before being freed. Sanitization is commonly accomplished by clearing the allocated space (that is, filling the space with `'\0'` characters).
``` c
char *secret;
/* Initialize secret to a null-terminated byte string, 
   of less than SIZE_MAX chars */
size_t size = strlen(secret);
char *new_secret;
/* Use calloc() to zero-out allocated space */
new_secret = (char *)calloc(size+1, sizeof(char));
if (!new_secret) {
  /* Handle error */
}
strcpy(new_secret, secret);
/* Process new_secret... */
/* Sanitize memory */
memset_s(new_secret, '\0', size);
free(new_secret);
new_secret = NULL;
```
The `calloc()` function ensures that the newly allocated memory has also been cleared. Because `sizeof(char)` is guaranteed to be 1, this solution does not need to check for a numeric overflow as a result of using `calloc()`. (See [MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap](MEM07-C_%20Ensure%20that%20the%20arguments%20to%20calloc__,%20when%20multiplied,%20do%20not%20wrap).)
See [MSC06-C. Beware of compiler optimizations](MSC06-C_%20Beware%20of%20compiler%20optimizations) for a definition and discussion of using the `memset_s()` function.
## Noncompliant Code Example (`realloc()`)
Reallocating memory using `realloc()` can have the same problem as freeing memory. The `realloc()` function deallocates the old object and returns a pointer to a new object. Using `realloc()` to resize dynamic memory may inadvertently expose sensitive information, or it may allow heap inspection, as described in *Fortify Taxonomy: Software Security Errors* \[[Fortify 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Fortify06)\] and NIST's *Source Code Analysis Tool Functional Specification* \[[Black 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Black07)\].
In this example, when `realloc()` is called, it may allocate a new, larger object, copy the contents of `secret` to this new object, `free()` the original object, and assign the newly allocated object to `secret`. However, the contents of the original object may remain in memory.
``` c
char *secret;
/* Initialize secret */
size_t secret_size = strlen(secret);
/* ... */
if (secret_size > SIZE_MAX/2) {
   /* Handle error condition */
}
else {
secret = (char *)realloc(secret, secret_size * 2);
}
```
The `secret_size` is tested to ensure that the integer multiplication (`secret_size * 2`) does not result in an integer overflow. (See [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).)
## Compliant Solution
A compliant program cannot rely on `realloc()` because it is not possible to clear the memory before the call. Instead, a custom function must be used that operates similarly to `realloc()` but sanitizes sensitive information as heap-based buffers are resized. Again, sanitization is done by overwriting the space to be deallocated with `'\0'` characters.
``` c
char *secret;
/* Initialize secret */
size_t secret_size = strlen(secret);
char *temp_buff;
/* ... */
if (secret_size > SIZE_MAX/2) {
   /* Handle error condition */
}
/* calloc() initializes memory to zero */
temp_buff = (char *)calloc(secret_size * 2, sizeof(char));
if (temp_buff == NULL) {
 /* Handle error */
}
memcpy(temp_buff, secret, secret_size);
/* Sanitize the buffer */
memset((volatile char *)secret, '\0', secret_size);
free(secret);
secret = temp_buff; /* Install the resized buffer */
temp_buff = NULL;
```
The `calloc()` function ensures that the newly allocated memory is also cleared. Because `sizeof(char)` is guaranteed to be 1, this solution does not need to check for a numeric overflow as a result of using `calloc()`. (See [MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap](MEM07-C_%20Ensure%20that%20the%20arguments%20to%20calloc__,%20when%20multiplied,%20do%20not%20wrap).)
## Risk Assessment
In practice, this type of [security flaw](BB.-Definitions_87152273.html#BB.Definitions-securityflaw) can expose sensitive information to unintended parties. The Sun tarball [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) discussed in *Secure Coding Principles & Practices: Designing and Implementing Secure Applications* \[[Graf 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Graf03)\] and Sun Security Bulletin #00122 \[[Sun 1993](AA.-Bibliography_87152170.html#AA.Bibliography-Sun93)\] shows a violation of this recommendation, leading to sensitive data being leaked. Attackers may also be able to leverage this defect to retrieve sensitive information using techniques such as *heap inspection*.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM03-C | Medium | Unlikely | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users can add a custom check for use of realloc(). |
| Compass/ROSE |  |  | Could detect possible violations of this rule by first flagging any usage of realloc(). Also, it could flag any usage of free that is not;preceded by code to clear out the preceding memory, using memset. This heuristic is imperfect because it flags all possible data leaks, not just leaks of "sensitive" data, because ROSE cannot tell which data is sensitive |
| Helix QAC | 2024.4 | C5010 |  |
| LDRA tool suite | 9.7.1 | 44 S | Enhanced Enforcement |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM03-a | Sensitive data should be cleared before being deallocated |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM03-C | Checks for:Sensitive heap memory not cleared before releaseUncleared sensitive data in stackRec. partially covered. |
| PVS-Studio | 7.35 | V1072 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM03-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Sensitive Information Uncleared Before Use [XZK] |
| MITRE CWE | CWE-226, Sensitive information uncleared before releaseCWE-244, Failure to clear heap memory before release ("heap inspection") |

## Bibliography

|  |
| ----|
| [Black 2007] |
| [Fortify 2006] |
| [Graff 2003] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152375) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152091)
## Comments:

|  |
| ----|
| Need to add some discussion about declaring variables as volatile to prevent compilers from optimizing away memory wipes
                                        Posted by rcs at Feb 04, 2007 16:50
                                     |
| David Wheeler discusses this issue here: http://www.dwheeler.com/secure-programs/Secure-Programs-HOWTO/protect-secrets.html
                                        Posted by btucker at Apr 26, 2007 14:59
                                     |
| This could be an issue on the stack too.; More general principle: clear sensitive info out of all reusable resources (heap, stack, disk sectors, whiteboards, whatever) before returning it to reuse.
                                        Posted by davearonson at Jan 11, 2008 11:43
                                     |
| My initial reaction is to expand to include "memory" including heap, stack, data segment, etc.
I don't think we should discuss clearing disk memory, as I think this topic is very complex.  For example, I found this quote on the subject:  "There is only one real way to really ensure that data can not be accessed. This is to destroy the hard drive in a very hot fire and melt it."
I think whiteboards are outside of our scope.  Once we start talking about mechanisms not defined by the language, the list becomes infinite.
There are a couple of topics referenced in the Wheeler article above that we may want to consider:
1. keeping memory form being paged to disk
2. disabling core dumps.
The problem with this rule (MEM03-A) is that it is a gateway to a bunch of other rules that talk about various security mechanisms which we have considered out of scope for this project.  For example, we don't talk about encryption at all yet.
                                        Posted by rcs at Jan 12, 2008 12:34
                                     |
| I didn't mean that we need to delve into the details of the other media.; The main thing I meant was to acknowledge that it's a problem with all media.  Maybe a list ("including but not limited to") of the most common types (such as those mentioned above, plus temp files) would help.  No need to mention whiteboards.  Post-It notes are Right Out.     It could possibly be mentioned that encryption make the data meaningless to other programs, and leave the entire field of encryption as an exercise for the reader.  
                                        Posted by davearonson at Jan 13, 2008 11:00
                                     |
| This rule may need to be consolidated with MSC06-C. Be aware of compiler optimization when dealing with sensitive data
                                        Posted by rcs at Mar 16, 2008 10:40
                                     |
| I tried consolidating these and didn't like the result.; It is worthwhile to go into detail on each subject separately rather than merge them into one very long recommendation.
                                        Posted by dmk at Mar 31, 2008 21:11
                                     |
| One way to deal with agressive optimization is to use volatile qualification, which a conforming implementation must honor:
memset((volatile char *)new_secret, '\0', size);
                                        Posted by dagwyn at Apr 16, 2008 22:09
                                     |
| I'm not completely sure the meaning of "regenerative case" inReallocating memory using the realloc() function is a regenerative case of freeing memory.Can we rewrite this to the following?When reallocating memory using the realloc() function we have the same problem as in freeing memory.
                                        Posted by yozo at Aug 14, 2013 05:54
                                     |
| I'm not sure what "regenerative case" means either. ;Rewritten.
                                        Posted by svoboda at Aug 14, 2013 10:00
                                     |
| thanks!; very understandable for me now (-:and I separated paragraphs.
                                        Posted by yozo at Aug 14, 2013 23:38
                                     |
| At the first Compliant solution the wrong check is not fixed:Current version:if;(size == SIZE_MAX) {  /* Handle error */}Must be:if (size >= SIZE_MAX) {  /* Handle error */}
                                        Posted by andrey.neyvanov at Sep 11, 2015 02:54
                                     |
| SIZE_MAX is the largest value a;size_t can hold. Since size is declared as a size_t, there are no values larger than SIZE_MAX that can be stored within the variable, and so == is a correct implementation. Using >= would also be correct, but misleading (and less efficient), since the value could never satisfy the >.
                                        Posted by aballman at Sep 11, 2015 08:03
                                     |
| If SIZE_MAX;is the largest value a size_t can hold then it will be hard (impossible) to allocate this chunk of memory. 
                                        Posted by andrey.neyvanov at Sep 14, 2015 04:49
                                     |
| size_t may be 16-bit.; You can imagine a segmented architecture where no object may be larger than 65535 bytes, and thus defining SIZE_MAX to 65535 is correct.  This would be permitted by the C11 standard.  However, I still don't think the example is correct; strlen is not guaranteed to return SIZE_MAX on an object which does not contain a zero byte, and in any case, there's nothing wrong with having a 65535-byte long secret.  What the author is trying to guard against is integer overflow in the next line where they do size + 1, which would overflow to 0; they would call malloc(0) and then write to ... well, it's not specified by C11 what malloc returns if you ask it to allocate 0 bytes.  So it might allocate a full 64k segment, but more likely it would return NULL or it might return a non-NULL-value-which-isn't-valid, or it might return a pointer to the minimum-size-object that malloc supports (typically 1-8 bytes).  All of the last three would lead to bad behaviour, either crashes or heap corruption.I would avoid this problem altogether in the example and define a SECRET_MAX.  I would also use strnlen, which I know isn't in C11, but is defined by POSIX-2008 and implemented by all good vendors (one can define one's own strnlen() in terms of memchr() if one is afflicted by having a poor vendor).
                                        Posted by willy6545 at Mar 24, 2018 08:13
                                     |
| Matthew's analysis is correct. However, the whole discussion of string lengths and malloc(0) is tangential to this recommendation. See;MEM04-C. Beware of zero-length allocations and INT30-C. Ensure that unsigned integer operations do not wrap for more relavent details. So I recoded both the code examples to use a SECRET_MAX limit, as Matthew suggested.
                                        Posted by svoboda at Mar 26, 2018 12:05
                                     |

