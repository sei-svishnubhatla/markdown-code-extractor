The size of a structure is not always equal to the sum of the sizes of its members. Subclause 6.7.2.1 of the C Standard states, "There may be unnamed padding within a structure object, but not at its beginning" \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\].
This unnamed padding is often called *structure padding*. Structure members are arranged in memory as they are declared in the program text. Padding may be added to the structure to ensure the structure is properly aligned in memory. Structure padding allows for faster member access on many architectures.
Rearranging the fields in a `struct` can change the size of the `struct`. It is possible to minimize padding anomalies if the fields are arranged in such a way that fields of the same size are grouped together.
Padding is also called *`struct` member alignment*. Many compilers provide a flag that controls how the members of a structure are packed into memory. Modifying this flag may cause the size of the structures to vary. Most compilers also include a keyword that removes all padding; the resulting structures are called *packed structures*. Overriding the default behavior is often unwise because it leads to interface compatibility problems (the nominally same `struct` has its layout interpreted differently in different modules).
## Noncompliant Code Example
This noncompliant code example assumes that the size of `struct buffer` is equal to the sum of the size of its individual components, which may not be the case \[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\]. The size of `struct buffer` may actually be larger because of structure padding.
``` c
enum { buffer_size = 50 };
struct buffer {
  size_t size;
  char bufferC[buffer_size];
};
/* ... */
void func(const struct buffer *buf) {
  /*
   * Incorrectly assumes sizeof(struct buffer) =
   * sizeof(size_t) + sizeof(bufferC)
   */
  struct buffer *buf_cpy = (struct buffer *)malloc(
    sizeof(size_t) + (buffer_size * sizeof(char) /* 1 */)
  );
  if (buf_cpy == NULL) {
    /* Handle malloc() error */
  }
  /* 
   * With padding, sizeof(struct buffer) may be greater than
   * sizeof(size_t) + sizeof(buff.bufferC), causing some data  
   * to be written outside the bounds of the memory allocated.
   */
  memcpy(buf_cpy, buf, sizeof(struct buffer));
  /* ... */
  free(buf_cpy);
}
```
## Compliant Solution
Accounting for structure padding prevents these types of errors:
``` c
enum { buffer_size = 50 };
struct buffer {
  size_t size;
  char bufferC[buffer_size];
};
/* ... */
void func(const struct buffer *buf) {
  struct buffer *buf_cpy = 
    (struct buffer *)malloc(sizeof(struct buffer));
  if (buf_cpy == NULL) {
    /* Handle malloc() error */
  }
  /* ... */
  memcpy(buf_cpy, buf, sizeof(struct buffer));
  /* ... */
  free(buf_cpy);
}
```
## Risk Assessment
Failure to correctly determine the size of a structure can lead to subtle logic errors and incorrect calculations, the effects of which can lead to abnormal program termination, memory corruption, or execution of arbitrary code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP03-C | High | Unlikely | High | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports accesses outside the bounds of allocated memory. |
| Helix QAC | 2024.4 | C0697 |  |
| LDRA tool suite | 9.7.1 | 578 S | Enhanced enforcement |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP03-CPP. Do not assume the size of a class or struct is the sum of the sizes of its members |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Structure Padding," pp.;284–287) |
| [ISO/IEC 9899:2011] | Subclause 6.7.2.1, "Structure and Union Specifiers" |
| [Sloss 2004] | Section 5.7, "Structure Arrangement" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152061) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152191)
## Comments:

|  |
| ----|
| The compliant solution must be improved upon - it does not compile, it has memory leak and the name of the struct is buffer and the field in it is also named buffer .;
here is the compliant code
struct buffer {
    size_t size;
    char bufferC[50];
};
/* ... */
void func(struct buffer *buf) {
  struct buffer *buf_cpy = malloc(sizeof(struct buffer));
  if (buf_cpy == NULL) {
    /* Handle malloc() error */
  }
  /* ... */
  memcpy(buf_cpy, buf, sizeof(struct buffer));Â   /* ... */Â  free(buf_cpy);Â }

Perhaps other aspects of Padding must also be discussed. Padding is also refered to as "Struct Member Alignment" - it is compiler flag. By changing this option - the size can vary. Most compilers include a keyword that removes all padding, such structures are referred to as Packed structures.
It is also important to emphasize that rearranging the fields in a struct can change the size of the struct. It is possible to minimize padding anomalies if the fields are arranged  in such a way that fields of the same size are \*grouped\* together.
 Reference
\[ARM system Developer's Guide\] Chapter 5, Efficient C Programming, Section 5.7 Structure Arrangement 
![](images/icons/contenttypes/comment_16.png) Posted by abhi at Mar 06, 2008 07:30
\| \|
I've incorporated all your suggestions (to the best of my ability) above.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 06, 2008 09:54
\| \|
It should be explained that structure padding allows for faster member access, on many architectures, and that overriding this default is unwise since it leads to interface compatibility problems (the nominally same struct has its layout interpreted differently in different modules).
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 14:24
\| \|
OK, I've added words to this effect.
Do we need another recommendation that says something like "avoid unaligned references on packed structures?" Anyone want to write it? ;^)
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Apr 16, 2008 08:54
\| \|
It's impossible for a static analysis tool to infer the intentions of a programmer, so ROSE can't tell that the programmer summed up the size of a struct's elements and substituted that for the size of a struct. Besides, such an error would cause a programmer to issue magic numbers (54) to a malloc function, or some function that expected a sizeof() operator. We have rules to catch magic numbers and a rule to catch malloc without a sizeof().
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 16, 2008 16:00
\| \|
I'm leaning towards this being analyzable. I rewrote the noncompliant code example to not use magic numbers (and still be wrong). I think it is analyzable however because a tool could keep track of the size of buf_cpy and determine that the subsequent memcpy() is copying more memory then has been allocated.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 09, 2009 10:17
\| \|
Changed to 'rose-partial'. The NCCE is now analyzeable. But I still think that many, many instances of code will not be amenable to static analysis.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 09, 2009 11:21
\| \|
If violating this rule can lead to arbitrary code execution, its severity should be High. I've made this change.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 09, 2015 10:02
\| \|
Good catch, thank you!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Nov 09, 2015 10:07
\| \|
> memcpy(buf_cpy, buf, sizeof(struct buffer));

Correct me if I'm wrong, but shouldn't it be 'buff' and not 'buf' in memcpy?
This would apply to the non compliant example as well as the compliant example.
![](images/icons/contenttypes/comment_16.png) Posted by christian.bock at May 13, 2022 04:35
\| \|
There's a global called `buff` and a function parameter called `buf`. I think they're each being used correctly right now.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at May 13, 2022 10:02
\| \|
Agreed, the code is correct. For the sake of clarity, I took out the 'buff' type since it is not used anywhere.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 13, 2022 16:52
\| \|
Uh, that is used: `sizeof(buff.bufferC)`;
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at May 13, 2022 17:05
\| \|
sizeof(buf→bufferC) or buffer_size.
I suppose buffer_size is better here (-:
![](images/icons/contenttypes/comment_16.png) Posted by yozo at May 14, 2022 02:39
\| \|
Thanks I was so concentrated on the buf and buff I completely missed the function parameter.
![](images/icons/contenttypes/comment_16.png) Posted by christian.bock at May 16, 2022 07:18
\| \|
Agreed, I made this change.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 16, 2022 07:29
\| \|
When allocating memory, it is better to use sizeof(\*pointer) than sizeof(struct_name). Moreover, casting the return value which is a void pointer is redundant.; So, in the Compliant Solution it is better to write
``` java
struct buffer *buf_cpy = malloc(sizeof(*buf_cpy));
```
than
``` java
struct buffer *buf_cpy = (struct buffer *)malloc(sizeof(struct buffer));
```
It improves readability and protects from a bug when someone needs to change the type of the variable but forgets to change the argument of sizeof.
It is also recommended to do so by Linux kernel coding style <https://www.kernel.org/doc/html/v4.10/process/coding-style.html#allocating-memory>
![](images/icons/contenttypes/comment_16.png) Posted by marcin.gebus at May 25, 2023 03:13
\| \|
Marcin:You might be interested in related recommendations [MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](MEM02-C_%20Immediately%20cast%20the%20result%20of%20a%20memory%20allocation%20function%20call%20into%20a%20pointer%20to%20the%20allocated%20type) and [ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array](ARR01-C_%20Do%20not%20apply%20the%20sizeof%20operator%20to%20a%20pointer%20when%20taking%20the%20size%20of%20an%20array).  I suggest that future discussion go in the comment section of one of those recommendations.  While MEM02-C recommends explicitly casting the output of malloc(), it says nothing about what whether malloc() should get a type or an expression (from which it infers the type). ARR01-C is the closest we come to specifying what goes in malloc, and that is specific to arrays (where getting the type wrong can cause obvious security problems)..
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 06, 2023 10:50
\|
