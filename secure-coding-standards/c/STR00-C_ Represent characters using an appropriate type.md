Strings are a fundamental concept in software engineering, but they are not a built-in type in C. Null-terminated byte strings (NTBS) consist of a contiguous sequence of characters terminated by and including the first null character and are supported in C as the format used for string literals. The C programming language supports single-byte character strings, multibyte character strings, and wide-character strings. Single-byte and multibyte character strings are both described as null-terminated byte strings, which are also called *narrow* character strings.
A pointer to a null-terminated byte string points to its initial character. The length of the string is the number of bytes preceding the null character, and the value of the string is the sequence of the values of the contained characters, in order.
A wide string is a contiguous sequence of wide characters (of type `wchar_t`) terminated by and including the first null wide character. A pointer to a wide string points to its initial (lowest addressed) wide character. The length of a wide string is the number of wide characters preceding the null wide character, and the value of a wide string is the sequence of code values of the contained wide characters, in order.
Null-terminated byte strings are implemented as arrays of characters and are susceptible to the same problems as arrays. As a result, rules and recommendations for [arrays](Rule%2006_%20Arrays%20_ARR_) should also be applied to null-terminated byte strings.
The C Standard uses the following philosophy for choosing character types, though it is not explicitly stated in one place:
#### `signed char` and `unsigned char`
-   Suitable for small integer values
#### "Plain" `char`
-   The type of each element of a string literal
-   Used for character data from a limited character set (where signedness has little meaning) as opposed to integer data
#### `int`
-   Used for data that can be either `EOF` (a negative value) or character data interpreted as `unsigned char` and then converted to `int`. As a result, it is returned by `fgetc()`, `getc()`, `getchar()`, and `ungetc()`. Also, accepted by the character-handling functions from `<ctype.h>` because they might be passed the result of `fgetc()`, and so on
-   The type of a character constant; its value is that of a plain `char` converted to `int`
Note that the two different ways a character is used as an `int` (as an `unsigned char` + `EOF` or as a plain `char` converted to `int`) can lead to confusion. For example, `isspace('\200')` results in undefined behavior when `char` is signed.
#### `unsigned char`
-   Used internally for string comparison functions even though these functions operate on character data; consequently, the result of a string comparison does not depend on whether plain `char` is signed
-   Used when the object being manipulated might be of any type, and it is necessary to access all bits of that object, as with `fwrite()`
Unlike other integer types, `unsigned char` has the unique property that
> values stored in . . . objects of type `unsigned char` shall be represented using a pure binary notation (C Standard, subclause 6.2.6.1 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\])

where *a pure binary notation* is defined as the following:
> A positional representation for integers that uses the binary digits 0 and 1, in which the values represented by successive bits are additive, begin with 1, and are multiplied by successive integral powers of 2, except perhaps the bit with the highest position. A byte contains `CHAR_BIT` bits, and the values of type `unsigned char` range from 0 to 2 <sup>`CHAR_BIT`</sup> − 1. (subclause 6.2.6, footnote 49)

That is, objects of type `unsigned char` may have no *padding bits* and consequently no *trap representation*. As a result, non-bit-field objects of any type may be copied into an array of `unsigned char` (for example, via `memcpy()`) and have their representation examined one byte at a time.
#### `wchar_t`
-   Wide characters are used for natural-language character data
## Risk Assessment
Understanding how to represent characters and character strings can eliminate many common programming errors that lead to software [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR00-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2004 rule 6.1 and MISRA C:2012 rule 10.1. |
| CodeSonar | 8.3p0 | MISC.NEGCHAR | Negative Character Value |
| LDRA tool suite | 9.7.1 | 329 S, 432 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR00-a | The plain char type shall be used only for the storage and use of character values |
| RuleChecker | 24.04 |  | Supported indirectly via MISRA C:2004 rule 6.1 and MISRA C:2012 rule 10.1. |
| SonarQube C/C++ Plugin | 3.11 | S810 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR00-CPP. Represent characters using an appropriate type |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.2.6, "Representations of Types" |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152414)
## Comments:

|  |
| ----|
| Is there any way to check for compliance with this rec? Coding samples would be illustrative.
                                        Posted by svoboda at May 27, 2008 13:11
                                     |
| the only thing I can thing of is type safety... which we don't really have in C... we could probably check to make sure plain char are not getting typecast to signed/unsigned chars or signed/unsigned ints since that implies wanting to treat a character as an integer, which is usually wrong
                                        Posted by avolkovi at Jun 03, 2008 09:59
                                     |
| We have a number of rules and recommendations that deal with specific compliance issues.  This is really a place holder for the intro material that used to be on the TOC page. I think it is still useful/informative to capture the philosophy behind character types in one location, however.
                                        Posted by rcs at Jun 03, 2008 11:07
                                     |
| The recommendation says plain char is:
"Used for character data from a limited character set (where signedness has little meaning) as opposed to integer data."
How can you say that signedness has little meaning in a limited character set? This sentence doesn't make sense to me.
                                        Posted by masaki at Nov 19, 2009 21:48
                                     |
| I think 'limited character set' means 8-bit chars, as opposed to Unicode. Don't let the phrase "limited character set" distract you. The point is that plain char is for when you don't care about sign, such as if you're just working with strings. Use signed or unsigned char if you care about the integer value, use plain char otherwise.
                                        Posted by svoboda at Nov 20, 2009 15:34
                                     |
| Thanks David, I got it (I'll try to make it more obvious in the translation). 
                                        Posted by masaki at Nov 23, 2009 22:08
                                     |
| Unlike other integer types, unsigned char also has the unique property that (quoting from 6.2.6.1 of C99):
Values stored in [...] objects of type unsigned char shall be represented using a pure binary notation.
where a pure binary notation is defined as
A positional representation for integers that uses the binary digits 0 and 1, in which the values represented by successive bits are additive, begin with 1, and are multiplied by successive integral powers of 2, except perhaps the bit with the highest position. A byte contains CHAR_BIT bits, and the values of type unsigned char range from 0 to 2 CHAR_BIT - 1 .
That is, objects of type unsigned char may have no padding bits and thus no trap representation. Thus, non-bit field objects of any type may be copied into an array of unsigned char (e.g., via memcpy()) and have their representation examined one byte at a time.
                                        Posted by martinsebor at Jan 02, 2010 13:42
                                     |
| This is all true, but is it extraneous information here, where we are trying to recommend what types should be used to represent characters?
                                        Posted by rcs_mgr at Aug 04, 2011 09:24
                                     |
| A pointer to a wide string points to its initial (lowest addressed) wide character.Is it independent of endianness?
                                        Posted by iamanubhavsaini at May 14, 2014 01:37
                                     |
| sure, it is going to point to the lowest addressed wide character regardless of endianness.; endianness is never going to result in the characters being reordered in memory.
                                        Posted by rcs_mgr at May 14, 2014 10:12
                                     |

