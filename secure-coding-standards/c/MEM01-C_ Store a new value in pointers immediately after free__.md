Dangling pointers can lead to exploitable double-free and access-freed-memory [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). A simple yet effective way to eliminate dangling pointers and avoid many memory-related vulnerabilities is to set pointers to `NULL` after they are freed or to set them to another valid object.
## Noncompliant Code Example
In this noncompliant code example, the type of a message is used to determine how to process the message itself. It is assumed that `message_type` is an integer and `message` is a pointer to an array of characters that were allocated dynamically. If `message_type` equals `value_1`, the message is processed accordingly. A similar operation occurs when `message_type` equals `value_2`. However, if `message_type == value_1` evaluates to true and `message_type == value_2` also evaluates to true, then `message` is freed twice, resulting in a double-free vulnerability.
``` c
char *message;
int message_type;
/* Initialize message and message_type */
if (message_type == value_1) {
  /* Process message type 1 */
  free(message);
}
/* ...*/
if (message_type == value_2) {
   /* Process message type 2 */
  free(message);
}
```
## Compliant Solution
Calling `free()` on a null pointer results in no action being taken by `free()`. Setting `message` to `NULL` after it is freed eliminates the possibility that the `message` pointer can be used to free the same memory more than once.
``` c
char *message;
int message_type;
/* Initialize message and message_type */
if (message_type == value_1) {
  /* Process message type 1 */
  free(message);
  message = NULL;
}
/* ... */
if (message_type == value_2) {
  /* Process message type 2 */
  free(message);
  message = NULL;
}
```
## Exceptions
**MEM01-C-EX1:** If a nonstatic variable goes out of scope immediately following the `free()`, it is not necessary to clear its value because it is no longer accessible.
``` c
void foo(void) {
  char *str;
  /* ... */
  free(str);
  return;
}
```
## Risk Assessment
Setting pointers to `NULL` or to another valid value after memory is freed is a simple and easily implemented solution for reducing dangling pointers. Dangling pointers can result in freeing memory multiple times or in writing to memory that has already been freed. Both of these problems can lead to an attacker executing arbitrary code with the permissions of the vulnerable process.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM01-C | High | Unlikely | Low | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports usage of invalid pointers. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-MEM01 | Fully implemented |
| CodeSonar | 8.3p0 | ALLOC.DFALLOC.UAF | Double freeUse after free |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | USE_AFTER_FREE | Can detect the specific instances where memory is deallocated more than once or read/written to the target of a freed pointer |
| LDRA tool suite | 9.7.1 | 484 S, 112 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM01-aCERT_C-MEM01-b
CERT_C-MEM01-c
CERT_C-MEM01-d | Do not use resources that have been freedAlways assign a new value to an expression that points to deallocated memory
Always assign a new value to global or member variable that points to deallocated memory
Always assign a new value to parameter or local variable that points to deallocated memory |
| Parasoft Insure++ |  |  | Detects dangling pointers at runtime |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM01-C | Checks for missing reset of a freed pointer (rec. fully covered) |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM01-CPP. Store a valid value in pointers immediately after deallocation |
| ISO/IEC TR 24772:2013 | Dangling References to Stack Frames [DCM]Dangling Reference to Heap [XYK]
Off-by-one Error [XZH] |
| MITRE CWE | CWE-415, Double freeCWE-416, Use after free |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |
| [Plakosh 2005] |  |

------------------------------------------------------------------------
[](../c/MEM00-C_%20Allocate%20and%20free%20memory%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152375)
## Comments:

|  |
| ----|
| I dislike this suggestion because it fixes a symptom and not the problem. In almost every instance where I've run across a multiple free() bug, it's been the result of an unexpected code path, which is either the problem itself or the result of another assumption in the code base. This in itself is the biggest flaw, but setting the pointer to NULL you may/may not catch a dereference at some point in the code base (depending on ptr use of course), but you don't catch the fact that you accidentally free()'d memory twice, which means your code ships with an unexpected code path that nicely hidden. Furthermore, I think if most companies did the cost analysis on which costs them more in terms of both time and money, I think they'd find that having the original author spend the time to track down the code path and figure out what occurred is cheaper than having to issue an advisory/patch/et cetera later.
                                        Posted by jf at Aug 20, 2007 09:11
                                     |
| While implementing this recommendation does not correct the underlying error, the impact of that error is effectively mitigated. Its a form of defensive programming. Besides, assume the pointer is not set to null - there is no guarantee that the program will crash or the bug will otherwise become visible.
Yes the underlying error should be sought out and fixed, but the causes of that error depend on the program itself and cannot be addressed in this standard. This recommendation provides good advice to mitigate the impact of this error, which (given the double free/accessing freed memory issues on file) does occur.
                                        Posted by jsg at Aug 21, 2007 11:40
                                     |
| IMHO, maybe changing the title to "Set pointers to dynamically allocated memory to NULL after they are released, or set it to a valid pointer". Sometimes we need reuse that pointer variable immediately.
/* ... */
free(p);
p = malloc(16);
/* ... */
                                        Posted by zhenyuwu@gmail.com at Oct 30, 2007 10:59
                                     |
| I very much support this practice: it certainly doesn't fix the underlying problem - as Justin has correctly suggested - but it reinforces the notion of *ownership* of a handle to a resource (pointer, file descriptor, etc.)
And when combined with the fantatic, nutbar-like use of assert(), it can help shake out bugs far earlier in the process than otherwise - NULL pointers are the best kind of invalid pointers.
                                        Posted by steve at Mar 14, 2008 00:19
                                     |

