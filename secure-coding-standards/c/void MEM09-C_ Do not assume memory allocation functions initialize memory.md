The C Standard defines four functions for memory management. In addition to allocating and deallocating memory, some of the functions may also partially or fully initialize it. Failure to understand the semantics of each memory management function can lead to program defects with potential security implications. The following table summarizes the essential characteristics of each of these functions.

| Function | Allocation | Deallocation | Initialization |
| ----|----|----|----|
| calloc() |  |  |  |
| free() |  |  |  |
| malloc() |  |  |  |
| realloc() |  |  | Partial |

### `calloc()`
The `calloc()` function is declared as follows:
``` java
void *calloc(size_t nmemb, size_t size);
```
The function allocates space for an array of `nmemb` objects, each of whose size is `size`. The space is initialized to all bits zero, which need not be the same as the representation of floating-point zero or a null pointer constant. Consequently, memory allocated by `calloc()` is immediately usable without further reinitialization unless it is intended to store pointer objects or objects of floating types.
### `free()`
The `free()` function deallocates memory previously allocated by one of the three memory allocation functions: `calloc()`, `malloc()`, and `realloc()`. The function may, but is not required to, overwrite or clear the memory before deallocating it, making it possible for the contents of the memory to be returned without change by a subsequent call to `malloc()` or `realloc()`.
### `malloc()`
In the C Standard, subclause 7.22.3.4 \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\], the `malloc()` function is declared as follows:
``` java
void *malloc(size_t size);
```
and its description reads:
> The `malloc` function allocates space for an object whose size is specified by `size` and whose value is indeterminate.

In other words, memory allocated with `malloc()` is not initialized, and its value is indeterminate. The behavior of a program that uses such memory without first initializing it is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). See [undefined behavior 180](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_180) in Annex J of the standard. Furthermore, this memory may contain unexpected values, including data used in another section of the program (and, on some systems, another program entirely).
### `realloc()`
The `realloc()` function  is declared as follows:
``` java
void *realloc(void *ptr, size_t size);
```
The function changes the size of a dynamically allocated memory object. The initial `size` bytes of the returned memory object are unchanged, but any newly added space is uninitialized, and its value is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue). As in the case of `malloc()`, accessing memory beyond the size of the original object results in undefined behavior. See [undefined behavior 181](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_171) in Annex J of the standard.
It is the programmer's responsibility to ensure that any memory allocated with `malloc()` and `realloc()` is properly initialized before it is used. As discussed in [EXP33-C. Do not read uninitialized memory](EXP33-C_%20Do%20not%20read%20uninitialized%20memory), using an object of a type other than `unsigned char` whose value is indeterminate results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Memory allocated with `calloc()` is zero initialized, but because this need not be the same as the representation of floating-point zero or a null pointer constant, portable programs must reinitialize memory returned by `calloc()` before using it as objects of pointer or floating types.
In addition, uninitialized memory may contribute to information leakage [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability), as is noted in [MEM03-C. Clear sensitive information stored in reusable resources](MEM03-C_%20Clear%20sensitive%20information%20stored%20in%20reusable%20resources).
## Noncompliant Code Example
In this noncompliant code example, the `str` string is copied to a dynamically allocated buffer with the `strncpy()` function:
``` c
enum { MAX_BUF_SIZE = 256 };
char *str = /* User-supplied data */;
size_t len = strlen(str);
if (len >= MAX_BUF_SIZE - 1) {
  /* Handle string-too-long error */
}
char *buf = (char *)malloc(MAX_BUF_SIZE);
if (buf == NULL) {
  /* Handle allocation error */
}
strncpy(buf, str, len);
/* Process buf */
free(buf);
buf = NULL;
```
In the case where `len` is less than the total length of `str` including the null terminator, `buf` may not be terminated. Consequently, this example also violates [STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string](STR32-C_%20Do%20not%20pass%20a%20non-null-terminated%20character%20sequence%20to%20a%20library%20function%20that%20expects%20a%20string).
## Compliant Solution
This compliant solution does not assume that allocated memory has been initialized to zero and explicitly null-terminates the string:
``` c
enum { MAX_BUF_SIZE = 256 };
char *str;
/* Initialize string to be copied */
size_t len = strlen(str);
if (len >= MAX_BUF_SIZE - 1)  {
  /* Handle string-too-long error */
}
char *buf = (char *)malloc(MAX_BUF_SIZE);
if (buf == NULL) {
  /* Handle allocation error */
}
strncpy(buf, str, len);
/* Null-terminate string */
buf[len] = '\0'
/* Process buf */
free(buf);
buf = NULL;
```
## Risk Assessment
Failure to clear memory or explicitly terminate strings can result in leaked information. Occasionally, it can also lead to buffer overflows when programmers assume, for example, a null-termination byte is present when it is not.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM09-C | Medium | Unlikely | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM09-CPP. Do not assume memory allocation routines initialize memory |
| ISO/IEC TS 17961 | Referencing uninitialized memory [uninitref] |
| MITRE CWE | CWE-119, Failure to constrain operations within the bounds of an allocated memory bufferCWE-665, Incorrect or incomplete initialization |

## Bibliography

|  |  |
| ----|----|
| [Graff 2003] | ; |
| [ISO/IEC 9899:2011] | Section 7.22.3.4, "The malloc Function"Section 7.22.3.5, "The realloc Function" |
| [Sun] | ; |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MEM08-C.+Use+realloc()+only+to+resize+dynamically+allocated+arrays?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=437) [](https://www.securecoding.cert.org/confluence/display/seccode/MEM10-C.+Define+and+use+a+pointer+validation+function?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I still do not know what to do about alloca()
                                        Posted by jsg at Jul 13, 2006 11:18
                                     |
| I think there should be some sort of recommendation to avoid using alloca() altogether (and related functions), it is pretty problematic. Particularly on current versions of UNIX, which don't seem to try and touch pages that they allocate in alot of cases. 
                                        Posted by mdowd at Jan 06, 2007 03:54
                                     |
| Hrmm.. what about C99 VLAs then? I think they work out to the same thing as alloca, but haven't looked at them in a while..
                                        Posted by jm at Jan 06, 2007 09:53
                                     |
| Last I checked they were the same. I pretty much think that they should be avoided as well. In fact, I think the MS VC++ compiler doesn't even support them.
                                        Posted by mdowd at Jan 06, 2007 21:03
                                     |
| I think the correct thing to do with alloca() is to ignore it as out of scope as it is not a C99 function.
Although we often reference non-C99 functions in our solution space, I think we should draw the line at not building rules and recommendations where these functions are in the non-compliant solution.  The problem is, of course, is that there is an infinite number of poorly written functions out there and we can't include them all.
                                        Posted by rcs at Jan 08, 2007 14:48
                                     |
| 
You are correct that MSVS does not support VLAs.  GCC sort of provides them, but if I recall correctly, not entirely to spec.  
We do already have one rule for VLAs:
ARR32-C. Ensure size arguments for variable length array are in a valid range
I would hate to throw out a new language feature, just because it is fully supported everywhere.  Instead, I would prefer to create some rules / recommendations so that it can be used safely.
                                        Posted by rcs at Jan 08, 2007 14:52
                                     |
| > This issue does not affect memory allocated with calloc() because calloc() initializes the content of allocated memory.
I'd like this to say something like:
"This does not affect memory allocated with calloc() because this function is defined by its contract to initialize the allocated memory to zero"
I like the idea of thinking about *contracts*
                                        Posted by steve at Mar 14, 2008 00:00
                                     |
| Changed.
                                        Posted by svoboda at Mar 31, 2008 18:11
                                     |
| VLAs behave better than alloca.; For one thing they must be implemented fully by the compiler, so it can handle the stack adjustments correctly.  alloca can be a function which the compiler needs to know about but maybe doesn't.  Also alloca'ed memory only goes out of scope when the function returns, which means alloca inside a loop is likely to be a seriously bad idea.  VLAs obey normal scope rules.  Though I'm sure there is a compiler out there which implements them via alloca  The Linux alloca manpage also says many alloca implementations are buggy.
 As for the good and bad of VLAs vs malloc, that seems to be a topic which won't die on comp.std.c.
                                        Posted by hbf at Apr 18, 2008 11:11
                                     |
| The issue does affect calloced memory, sort of.; calloc initializes memory to zero bytes, but for non-integer types a bunch of zero bytes may not be a valid value.  I have no idea if it's much of an issue in real life, but I don't know it isn't either.  I've seen a tale from long ago on comp.lang.c of an OS vendor who switched to NULL pointers != "all bits zero" - they switched back because too many programs broke.  It doesn't help to be formally in the right if your users decide they prefer your competitors.
                                        Posted by hbf at Apr 18, 2008 11:21
                                     |
| It seems to me that the NCCE is fine subject to the general proviso that the string copied into the buffer is shorter than the buffer size, and subject to the specific proviso that the 'process buf' code treats buf as a null terminated string and not as a block of memory.; If the processing does treat it as a block of memory that is all initialized, then the NCCE is indeed NC; if the processing treats it as a string (calling puts() or something), then there is no problem with it - apart from allocating more space than minimally necessary.  Should the NCCE be annotated to process the buffer passing the allocated space to a function - somefunction(buf, MAX_BUF_SIZE) - so that it is clearer that the code is using the whole block and not just the initialized string?
                                        Posted by jonathan.leffler@gmail.com at Apr 20, 2008 00:52
                                     |
| Indeed.; The "non-compliant" example is actually compliant with this recommendation, as well as valid and normal C code.
                                        Posted by hbf at Apr 21, 2008 13:17
                                     |
| Changed examples, so non-compliant example is now a security risk (possibly a segfault)
                                        Posted by svoboda at Apr 21, 2008 16:12
                                     |
| Why can't len be equal to MAX_BUF_SIZE - 1 in the examples?
                                        Posted by dmohindr at Jun 17, 2010 22:57
                                     |
| Because len is the string length (strlen()), and so does not include the terminating null character. The # of bytes of the string is the string length + 1.
                                        Posted by svoboda at Jun 18, 2010 15:46
                                     |
| I suppose it is safe to allocate size = strlen(str) + 1 using malloc(). This is enough to represent str. If size = 256 as in the examples then why can't the string length be 255 (MAX_BUF_SIZE - 1)?
                                        Posted by dmohindr at Jun 18, 2010 22:09
                                     |
| FWIW, I don't find the NCCE to be representative of the problem this rule is about. It looks much more like an example out of STR32-C. Null-terminate byte strings as required. I think a better example might be one involving realloc() where the programmer assumes the memory past the end of the original block is zeroed out.
In addition, strncpy() is on the list of obsolescent functions in MSC34-C. Do not use deprecated or obsolescent functions so the compliant solution is in violation of that rule. That said, however, the use of strncpy() in the solution, or memcpy() which would be more appropriate, is perfectly safe.
Their recommended replacements, strcpy_s() or memcpy_s(), do not provide any additional safety in this case:
    the string str is guaranteed to be non-null so checking it again in the functions is unnecessary
    the length of the string len is already bounded by MAX_BUF_SIZE so testing it against RSIZE_MAX is redundant.
Btw., it's worth noting that [ISO/IEC 9945:2008] (AKA POSIX) provides the function stpncpy() to deal with the missing NUL problem:
If a NUL character is written to the destination, the stpncpy() function shall return the address of the first such NUL character. Otherwise, it shall return &s1[n].
Since POSIX is an ISO standard while the document that defines strcpy_s() is just an ISO technical report, to promote portability I think it would be appropriate to suggest stpncpy() before recommending strncpy_s().
                                        Posted by martinsebor at Jun 20, 2010 12:10
                                     |
| When I first read it I was expecting a strcpy() in the CS because of adequate bounds checking and str being guaranteed to be null terminated, but realized that the CS would then differ from the NCE. Perhaps the CS could use one of the alternate functions after all.
                                        Posted by dmohindr at Jun 20, 2010 15:24
                                     |

