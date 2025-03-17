The internal representations of bit-field structures have several properties (such as internal padding) that are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-defined). Additionally, bit-field structures have several implementation-defined constraints:
-   The alignment of bit-fields in the storage unit (for example, the bit-fields may be allocated from the high end or the low end of the storage unit)
-   Whether or not bit-fields can overlap a storage unit boundary
Consequently, it is impossible to write portable safe code that makes assumptions regarding the layout of bit-field structure members.
## Noncompliant Code Example (Bit-Field Alignment)
Bit-fields can be used to allow flags or other integer values with small ranges to be packed together to save storage space. Bit-fields can improve the storage efficiency of structures. Compilers typically allocate consecutive bit-field structure members into the same `int`-sized storage, as long as they fit completely into that storage unit. However, the order of allocation within a storage unit is implementation-defined. Some [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) are *right-to-left*: the first member occupies the low-order position of the storage unit. Others are *left-to-right*: the first member occupies the high-order position of the storage unit. Calculations that depend on the order of bits within a storage unit may produce different results on different implementations.
Consider the following structure made up of four 8-bit bit-field members:
``` java
struct bf {
  unsigned int m1 : 8;
  unsigned int m2 : 8;
  unsigned int m3 : 8;
  unsigned int m4 : 8;
};  /* 32 bits total */
```
Right-to-left implementations will allocate `struct bf` as one storage unit with this format:
``` java
m4   m3   m2   m1
```
Conversely, left-to-right implementations will allocate `struct bf` as one storage unit with this format:
``` java
m1   m2   m3   m4
```
The following code behaves differently depending on whether the implementation is left-to-right or right-to-left:
``` c
struct bf {
  unsigned int m1 : 8;
  unsigned int m2 : 8;
  unsigned int m3 : 8;
  unsigned int m4 : 8;
}; /* 32 bits total */
void function() {
  struct bf data;
  unsigned char *ptr;
  data.m1 = 0;
  data.m2 = 0;
  data.m3 = 0;
  data.m4 = 0;
  ptr = (unsigned char *)&data;
  (*ptr)++; /* Can increment data.m1 or data.m4 */
}
```
## Compliant Solution (Bit-Field Alignment)
This compliant solution is explicit in which fields it modifies:
``` c
struct bf {
  unsigned int m1 : 8;
  unsigned int m2 : 8;
  unsigned int m3 : 8;
  unsigned int m4 : 8;
}; /* 32 bits total */
void function() {
  struct bf data;
  data.m1 = 0;
  data.m2 = 0;
  data.m3 = 0;
  data.m4 = 0;
  data.m1++;
}
```
## Noncompliant Code Example (Bit-Field Overlap)
In this noncompliant code example, assuming 8 bits to a byte, if bit-fields of 6 and 4 bits are declared, is each bit-field contained within a byte, or are the bit-fields split across multiple bytes?
``` c
struct bf {
  unsigned int m1 : 6;
  unsigned int m2 : 4;
};
void function() {
  unsigned char *ptr;
  struct bf data;
  data.m1 = 0;
  data.m2 = 0;
  ptr = (unsigned char *)&data;
  ptr++;
  *ptr += 1; /* What does this increment? */
}
```
If each bit-field lives within its own byte, then `m2` (or `m1`, depending on alignment) is incremented by 1. If the bit-fields are indeed packed across 8-bit bytes, then `m2` might be incremented by 4.
## Compliant Solution (Bit-Field Overlap)
This compliant solution is explicit in which fields it modifies:
``` c
struct bf {
  unsigned int m1 : 6;
  unsigned int m2 : 4;
};
void function() {
  struct bf data;
  data.m1 = 0;
  data.m2 = 0;
  data.m2 += 1;
}
```
## Risk Assessment
Making invalid assumptions about the type of type-cast data, especially bit-fields, can result in unexpected data values.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP11-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports runtime errors resulting from invalid assumptions. |
| Compass/ROSE |  |  | Can detect violations of this recommendation. Specifically, it reports violations ifA pointer to one object is type cast to the pointer of a different objectThe pointed-to object of the (type cast) pointer is then modified arithmetically |
| Helix QAC | 2024.4 | C0310, C0751 |  |
| LDRA tool suite | 9.7.1 | 554 S | Fully implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this recommendation on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP11-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP11-CPP. Do not apply operators expecting one type to data of an incompatible type |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |
| MISRA C:2012 | Directive 1.1 (required) |

## Bibliography

|  |  |
| ----|----|
| [Plum 1985] | Rule 6-5: In portable code, do not depend upon the allocation order of bit-fields within a word |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152207) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152282)
## Comments:

|  |
| ----|
| Chris Tapp sez:
> These examples really show that the use of pointers needs restricting. Would a pointer-related rule not be more concrete (and therefore tool-enforceable)?

Given this and Doug Gwynn's comment, it sounds like these are good examples, its just that this rule is not about integers, and belongs somewhere else. And should probably be focused on pointers into bitfield structs.
                                        Posted by svoboda at May 01, 2008 17:00
                                     |
| If you need an example: I haven't seen code which updates bitfields via pointers like your non-compliant examples, but I've seen code which sends structs with bitfields over the network or stores such structs in files.; Sometimes wrapped in #ifdef <config macro which says if bitfields have big-endian bitfield order> to make it portable:
struct foo {
#ifdef BIG_ENDIAN_BITFIELDS
    unsigned x:5;
    unsigned y:3;
#else
    unsigned y:3;
    unsigned x:5;
#endif
};

This solution and your non-conformant examples also have the problem that the compiler may insert more padding than you expected, e.g. because char is 12-bit so your data doesn't exactly fit in a whole number of bytes or whole number of words.  Though the code could use an assert to catch it.
(BTW, this time underscores showed up as spaces when I first typed the code section, but the came back when I switched to Wiki Markup, and stayed when I switched back to Rich Text.  Weird.)
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 19, 2008 06:25
\| \|
This example about sending over networks is addressed by [FIO09-C. Be careful with binary data when transferring data across systems](FIO09-C_%20Be%20careful%20with%20binary%20data%20when%20transferring%20data%20across%20systems)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 19, 2008 11:00
\| \|
;Well, it's a special case of that rule.You could do the same in-memory, given a spec of an image format or something which describes some data bit by bit.  Sometimes bitfields can then simplify the program code since you avoid shift and bitmask operations, but you lock yourself to a particular compiler's bitfield layout unless you use tricks like the #ifdef above to get around that.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 19, 2008 13:47
\| \|
I can't imagine any good/portable way to use bitfields for that purpose... if you're taking data and casting it into a bitfield structure, there is no way for you to know which bits are which because of compiler+padding, just knowing the endianess isn't enough
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at May 19, 2008 13:55
\| \|
Right, as I said you'd need an assert or something to stop it from running on an implementation where it breaks.; Not all code cares about portability, or about portability to hosts the author thinks is weird (like 9-bit chars or "unexpected" padding).  Or the code is inherently unportable, like a device driver for an OS which makes such assumptions anyway.
Anyway, that is the one reason I remember seeing for getting into trouble with how the compiler arranges bitfields.
I suppose a simpler reason would be if you just want to write a struct which contains bitfields do disk, or hash it, or something.  But both are just special cases of "don't assume a struct value has the same binary representation or even size on all hosts".  
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 20, 2008 08:34
\| \|
We should probably change the name of this rule back to the original "Do not make assumptions about the layout of bit-field structures" since all of the pointer arithmetic stuff is covered by ARR37, and we should also mention that [EXP03-C. Do not assume the size of a structure is the sum of the sizes of its members](EXP03-C_%20Do%20not%20assume%20the%20size%20of%20a%20structure%20is%20the%20sum%20of%20the%20sizes%20of%20its%20members) is a special case of this rec
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 03, 2008 09:25
\| \|
The problems illustrated by the rule are not unique to bit-field structures. Added a NCCE/CCE pair illustrating the same problems between ints and floats, and changed the rule title accordingly.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 04, 2008 14:07
\| \|
The current ROSE code works well, but has several exceptions:
-   MEM02-A explicitly requires pointer casts to the result of malloc()
-   NULL is usually defined as an (int\*) 0, which is OK
-   Strings are not pointers, but can be assigned to them.
This rule should probably mention these exceptions as well.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2008 16:38
\| \|
These are all exceptions due to the behavior of ROSE, and they have nothing to do with the C standard
-   MEM02 casts from `void *` to `foo *`, which is explicitly allowed by C99
-   NULL should be a `void *`, declaring it `int *` is implementation specific behavior
-   Strings should be treated as pointers, there's nothing special about treating them as `char *`, especially given that there is no `string` type in C99 (but there is in ROSE)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 10, 2008 10:46
\| \|
We should probably add an exception for when C handles socket addresses. This code snippet violates the rule, but shouldn't:
``` java
struct ifreq ifr;
struct sockaddr_in *sin = (struct sockaddr_in *)&ifr.ifr_addr;
```
It is trying to assign a `sockaddr*` to a `sockaddr_in*`. Not only are the two data types the same size (16), but `sockaddr_in`'s last field is a char-array designed to make it the same size. IOW the types were designed for assignment to be safe.
This is a common mechanism in C++; assigning a `Derived*` to a variable of type `Base*` is OK if `Derived` inherits from `Base`. But TCP and socket addresses predate C++ :S
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 13, 2008 16:55
\| \|
The title of this practice doesn't correspond to the coding examples most of which demonstrate undefined behavior due to accessing objects by lvalues of incompatible types (i.e., [34](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_34)) rather than "applying operators to operands of incompatible types."
In addition, I believe the essence of this practice is a duplicate of [EXP39-C. Do not access a variable through a pointer of an incompatible type](EXP39-C_%20Do%20not%20access%20a%20variable%20through%20a%20pointer%20of%20an%20incompatible%20type). I propose to merge it into the latter.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 19, 2011 11:41
\| \|
We did combine these in \[ptrcomp\] in TS 17961.; I can see eliminating the first NCE/CS pair as a result.
The remaining examples involving bit-field rules.  These are being accessed through a pointer to unsigned char, which is actual an exclusion of [EXP39-C. Do not access a variable through a pointer of an incompatible type](https://www.securecoding.cert.org/confluence/display/seccode/EXP39-C.+Do+not+access+a+variable+through+a+pointer+of+an+incompatible+type).  Maybe we should replace this rule with something specific to bit-fields?  E.g., "Do not makes assumptions regarding the layout of bit-field structure members"?
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jan 07, 2013 11:18
\| \|
I second the idea of changing the name, even if not to the name proposed by Alex, if for no other reason than the fact the current version is grammatically incorrect.
![](images/icons/contenttypes/comment_16.png) Posted by xuinkrbin. at Jan 09, 2013 13:30
\| \|
Sigh, I just noticed that;![](images/icons/emoticons/sad.svg) Fixed.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 09, 2013 14:21
\|
