> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [EXP42-C. Do not compare padding data](EXP42-C_%20Do%20not%20compare%20padding%20data)

Structures may be padded with data to ensure that they are properly aligned in memory. The contents of the padding and the amount of padding added is [unspecified](BB.-Definitions_87152273.html#BB.Definitions-unspecifiedbehavior). (See [unspecified behavior 10](DD.-Unspecified-Behavior_87152246.html#DD.UnspecifiedBehavior-usb_10) in Annex J, Section J.1, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\].) This can lead to incorrect results when attempting a byte-by-byte comparison between structures \[[Summit 1995](AA.-Bibliography_87152170.html#AA.Bibliography-Summit95)\].
## Noncompliant Code Example
This noncompliant code example uses `memcmp()` to compare two structures:
``` c
struct my_buf {
  char buff_type;
  size_t size;
  char buffer[50];
};
bool buf_equal(const struct my_buf *s1, 
               const struct my_buf *s2) 
{
  return 0 == memcmp(s1, s2, sizeof *s1);
}
void f (void) {
  my_buf a = { 0, 0, "" };
  my_buf b;
  memset(&b, 0, sizeof b);
  assert(true == buf_equal(&a, &b));   /* need not hold */
  /* ... */
}
```
Many machines access values in memory most efficiently when the values are appropriately aligned. For example, on a byte-addressed machine, 2-byte `short` integers might best be placed at even addresses, while 4-byte `long` integers might best be placed at addresses that are a multiple of 4. Some machines cannot perform unaligned accesses at all and require that all data be appropriately aligned.
For structures like the one in this example, the compiler will usually leave an unnamed, unused hole between the `char` and `size_t` fields to ensure that the `size_t` field is properly aligned. This incremental alignment of subsequent fields based on the initial field assumes the structure itself is always properly aligned, with the most conservative alignment requirement. The compiler guarantees this alignment for structures it allocates, as does `malloc()`.
Regardless of how these structures are initialized, structure padding may cause `memcmp()` to evaluate the structures to be unequal irrespective of the values of their fields. This is because this padding memory may not have been initialized and may contain arbitrary contents. In this particular example, unused memory allocated to the character array `buffer` may also cause the objects `a` and `b` to compare unequal, despite having zeroed out their members at initialization and by calling `memset()`. Neither technique is guaranteed to affect the value of the padding bits.
## Compliant Solution
In this compliant solution, the `buf_compare()` function has been rewritten to perform a field-by-field comparison:
``` c
struct my_buf {
  char buff_type;
  size_t size;
  char buffer[50];
};
bool buf_equal(const struct my_buf *s1, 
               const struct my_buf *s2) 
{
  if (   s1->buff_type != s2->buff_type
      || s1->size != s2->size)
    return false;
  return 0 == strcmp(s1->buffer, s2->buffer);
}
```
## Risk Assessment
Failure to correctly compare structure can lead to unexpected program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP04-C | medium | unlikely | high | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP04-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP04-CPP. Do not perform byte-by-byte comparisons between classes or structs |
| ISO/IEC TS 17961 | Comparison of padding data [padcomp] |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" ("Structure Padding," pp.;284–287) |
| [Kerrighan 1988] | Chapter 6, "Structures" ("Structures and Functions," p. 129) |
| [Summit 1995] | Question 2.8, Question 2.12 |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/EXP03-C.+Do+not+assume+the+size+of+a+structure+is+the+sum+of+the+sizes+of+its+members?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=358) [](https://www.securecoding.cert.org/confluence/display/seccode/EXP05-C.+Do+not+cast+away+a+const+qualification?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| s1 and s2 in the solution will have same padding - same rules apply to them - so why is this a "Risk" in doing memcmp? Two variables of the same data type - what can go wrong in comparing them? If S1 came from lib that was say 4byte Aligned and s2 came from lib that was 1byte aligned - it is considered plain wrong to mix lib that have different alignment settings. If the writer want to point the perils of mixing libraries then this should perhaps have a different title.
To me it looks like this is very tightly coupled with the my_buf - looks like the writer wants the size to be checked first before compared the other element of my_buf.;  . 
Also I guess in the Non-compliant code example the writer meant "sizeof(struct my_buf)" and not "sizeof(struct my_struct)" and the in the Compliant solution it must be struct my_buf and not struct buffer. 
                                        Posted by abhi at Mar 07, 2008 05:13
                                     |
| The issue, I believe, is that when these structures are created the memory is not necessarily wiped, and there can be random bits of data throughout the structures.
Even if equal values are assigned to size and buffer, the structures may not compare equal using memcmp because the padding values are "uninitialized" to different values.
This is especially true of buffer, which contains a null-terminated byte string.  This means that not all the memory allocated for buffer contains meaningful data--only the date up to the first null byte.
This example may be improved by adding a char c; to the start of the structure.  This would tend to cause padding to be added by the compiler for alignment (see http://c-faq.com/struct/padding.html).
The compliant solution could reorganize the structure based on the recommendation to "minimize the effects of padding by ordering the members of a structure based on their base types, from largest to smallest."  However, I'm not sure this advice is that great in this case because 50 is not a multiple of four.
We may also want to point out the issues with padding and IO http://c-faq.com/struct/io.html
                                        Posted by rcs at Mar 08, 2008 08:23
                                     |
| Thank you! that makes sense
                                        Posted by abhi at Mar 10, 2008 03:36
                                     |
| It may be worthwhile to mention that, if the programmer chooses (for whatever reason) to directly memcmp() structures, the program should guarantee that the structures are memset() to 0 when created.
It may also be worthwhile to mention that doing an ordered compare, such as the native return value of memcmp(), won't be reliable across platforms due to differences in byte ordering of integers, and is dependent on signed/unsigned issues (memcmp treats the data as unsigned char for purposes of comparison, so doing a memcmp on signed integers would produce inconsistent results).
                                        Posted by gbeeley at Mar 13, 2008 17:55
                                     |
| Forget whether the individual fields have the same value - the whole point is that the padding is that you cannot read it at all (undefined behaviour, because the values are indeterminate).; Robert's point that the character array may only be equal up to the first NUL is a different point  - specifically because the values of the two arrays are not equal unless each element of one array is equal to the correspondingly-positioned element in the other in the first place.
To Greg: no, you cannot guarantee the value of the padding (value is indeterminate), even if you memset it, or allocate the memory with calloc.  There may be padding bits in integers too - unsigned char is your only hope here.
                                        Posted by stewartb at Mar 13, 2008 20:22
                                     |
| Re. padding values being indeterminate - actually memcmp() on structures in the general case makes many more assumptions than just that the holes are all zero.; In reverse of my previous comment, I'd say that list of assumptions is just too long to suggest that there are solutions to permitting memcmp on structures in the general case.  Thanks.
                                        Posted by gbeeley at Mar 13, 2008 23:09
                                     |
| Should we provide an exception in cases where the structure is initialized to all zeros, for example using memset()?
                                        Posted by rcs_mgr at Jul 23, 2008 10:11
                                     |
| I don't understand. The rule is about doing byte-by-byte comparison, presumably using memcmp(). Two structs that have been zeroed out might match according to memcmp(), but then one can easily fool memcmp() by sneaking a nonzero value inside a padding region. So I don't see that a zeroed-out struct constitutes a valid exception.
                                        Posted by svoboda at Jul 23, 2008 10:41
                                     |
| What if one argument to memcmp() is a pointer to a structure and the other is a pointer to, say, char? ;I would think the padding issue would exist also in this situation.
                                        Posted by xuinkrbin. at Feb 13, 2009 13:43
                                     |
| Agreed. You'd also have other issues that derive from the assumptions about how your struct is laid out in memory such that it should match your char array.
                                        Posted by svoboda at Feb 16, 2009 13:26
                                     |
| In that case, should the guideline be changed to something similar to 'Do not perform a byte-by-byte comparison involving a structure'? ;[The difference in wording may seem trivial to Some.  However, I did find Myself, at first, thinking the guideline required a comparison between two actual structure objects.]
                                        Posted by xuinkrbin. at Feb 16, 2009 13:32
                                     |
| Agreed, I've changed the title.
                                        Posted by svoboda at Feb 16, 2009 13:48
                                     |
| This seems important enough to be a Rule rather than just a Recommendation. It certainly meets all the criteria to be a Rule.
Unless there are objections to making it a Rule I'll plan on moving/renaming it sometime soon.
                                        Posted by martinsebor at Jun 12, 2011 18:22
                                     |
| no objection
                                        Posted by rcs_mgr at Jun 13, 2011 09:37
                                     |
| Am I correct in presuming this rule also applies in the case of a pointer to struct which has been cast to void *, like so?memcmp((void *) &struct1, ... );

![](images/icons/contenttypes/comment_16.png) Posted by jimg at Apr 29, 2013 14:05
\| \|
I'm guessing yes. (it depends on how much of the struct you wish to compare...the danger being that internal padding bits may wreck the accuracy of your comparison.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 29, 2013 14:45
\|
