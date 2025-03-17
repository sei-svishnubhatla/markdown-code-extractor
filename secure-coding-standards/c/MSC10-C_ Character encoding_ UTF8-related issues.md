UTF-8 is a variable-width encoding for Unicode. UTF-8 uses 1 to 4 bytes per character, depending on the Unicode symbol. UTF-8 has the following properties:
-   The classical US-ASCII characters (0 to 0x7f) encode as themselves, so files and strings that are encoded with ASCII values have the same encoding under both ASCII and UTF-8.
-   It is easy to convert between UTF-8 and UCS-2 and UCS-4 fixed-width representations of characters.
-   The lexicographic sorting order of UCS-4 strings is preserved.
-   All possible 2^21 UCS codes can be encoded using UTF-8.
Generally, programs should validate UTF-8 data before performing other checks. The following table lists the well-formed UTF-8 byte sequences.
|  |  |  |  |  |  |  |  |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| Bits of code point | First code point | Last code point | Bytes in sequence | Byte 1 | Byte 2 | Byte 3 | Byte 4 |
|   7 | U+0000 | U+007F | 1 | `0xxxxxxx` |  |  |  |
| 11 | U+0080 | U+07FF | 2 | `110xxxxx` | `10xxxxxx` |  |  |
| 16 | U+0800 | U+FFFF | 3 | `1110xxxx` | `10xxxxxx` | `10xxxxxx` |  |
| 21 | U+10000 | U+1FFFFF | 4 | `11110xxx` | `10xxxxxx` | `10xxxxxx` | `10xxxxxx` |
Although UTF-8 originated from the Plan 9 developers \[[Pike 1993](AA.-Bibliography_87152170.html#AA.Bibliography-Pike93)\], Plan 9's own support covers only the low 16-bit range. In general, many "Unicode" systems support only the low 16-bit range, not the full 21-bit ISO 10646 code space \[[ISO/IEC 10646:2012](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC10646-2012)\].
## Security-Related Issues
According to [RFC 2279: UTF-8, a transformation format of ISO 10646](http://www.faqs.org/rfcs/rfc2279.html) \[[Yergeau 1998](AA.-Bibliography_87152170.html#AA.Bibliography-Yergeau98)\],
> Implementors of UTF-8 need to consider the security aspects of how they handle invalid UTF-8 sequences. It is conceivable that, in some circumstances, an attacker would be able to exploit an incautious UTF-8 parser by sending it an octet sequence that is not permitted by the UTF-8 syntax.
>
> A particularly subtle form of this attack can be carried out against a parser that performs security-critical validity checks against the UTF-8 encoded form of its input, but interprets certain invalid octet sequences as characters. For example, a parser might prohibit the null character when encoded as the single-octet sequence `00`, but allow the invalid two-octet sequence `C0 80` and interpret it as a null character. Another example might be a parser which prohibits the octet sequence `2F 2E 2E 2F` (`"/../"`), yet permits the invalid octet sequence `2F C0 AE 2E 2F`.

Following are more specific recommendations.
### Accept Only the Shortest Form
Only the "shortest" form of UTF-8 should be permitted. Naive decoders might accept encodings that are longer than necessary, allowing for potentially dangerous input to have multiple representations. For example,
1.  Process A performs security checks but does not check for nonshortest UTF-8 forms.
2.  Process B accepts the byte sequence from process A and transforms it into UTF-16 while interpreting possible nonshortest forms.
3.  The UTF-16 text may contain characters that should have been filtered out by process A and can potentially be dangerous. These "nonshortest" UTF-8 attacks have been used to bypass security validations in high-profile products, such as Microsoft's IIS Web server.
[Corrigendum #1: UTF-8 Shortest Form](http://www.unicode.org/versions/corrigendum1.html) to the Unicode Standard \[[Unicode 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Unicode06)\] describes modifications made to version 3.0 of the Unicode Standard to forbid the interpretation of the nonshortest forms.
### Handling Invalid Inputs
UTF-8 decoders have no uniformly defined behavior upon encountering an invalid input. Following are several ways a UTF-8 decoder might behave in the event of an invalid byte sequence. Note that implementing these behaviors requires careful security considerations. 
1.  Substitute for the replacement character "U+FFFD" or the wildcard character such as "?" when U+FFFD is not available.
2.  Ignore the bytes (for example, delete the invalid byte before the validation process; see "Unicode Technical Report #36, 3.5 Deletion of Code Points" for more information).
3.  Interpret the bytes according to a different character encoding (often the ISO-8859-1 character map; other encoding, such as Shift_JIS, is known to trigger self-XSS, and so is potentially dangerous).
4.  Fail to notice but decode as if the bytes were some similar bit of UTF-8.
5.  Stop decoding and report an error.
The following function from John Viega's "Protecting Sensitive Data in Memory" \[[Viega 2003](AA.-Bibliography_87152170.html#AA.Bibliography-Viega03)\] detects invalid character sequences in a string but does not reject nonminimal forms. It returns `1` if the string is composed only of legitimate sequences; otherwise, it returns `0`.
``` java
int spc_utf8_isvalid(const unsigned char *input) {
  int nb;
  const unsigned char *c = input;
  for (c = input;  *c;  c += (nb + 1)) {
    if (!(*c & 0x80)) nb = 0;
    else if ((*c & 0xc0) == 0x80) return 0;
    else if ((*c & 0xe0) == 0xc0) nb = 1;
    else if ((*c & 0xf0) == 0xe0) nb = 2;
    else if ((*c & 0xf8) == 0xf0) nb = 3;
    else if ((*c & 0xfc) == 0xf8) nb = 4;
    else if ((*c & 0xfe) == 0xfc) nb = 5;
    while (nb-- > 0)
      if ((*(c + nb) & 0xc0) != 0x80) return 0;
  }
  return 1;
}
```
### Broken Surrogates
Encoding of individual or out-of-order surrogate halves should not be permitted. Broken surrogates are invalid in Unicode and introduce ambiguity when they appear in Unicode data. Broken surrogates are often signs of bad data transmission. They can also indicate internal bugs in an application or intentional efforts to find security vulnerabilities.
## Risk Assessment
Failing to properly handle UTF8-encoded data can result in a data integrity violation or [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC10-C | Medium | Unlikely | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | 9.7.1 | 176 S, 376 S | Partially implemented |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC10-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC10-CPP. Character encoding: UTF8-related issues |
| MITRE CWE | CWE-176, Failure to handle Unicode encodingCWE-116, Improper encoding or escaping of output |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 10646:2012] | ; |
| [Kuhn 2006] | UTF-8 and Unicode FAQ for Unix/Linux |
| [Pike 1993] | "Hello World" |
| [Unicode 2006] | ; |
| [Viega 2003] | Section 3.12, "Detecting Illegal UTF-8 Characters" |
| [Wheeler 2003] | Secure Programmer: Call Components Safely |
| [Yergeau 1998] | RFC 2279 |

------------------------------------------------------------------------
[](../c/MSC09-C_%20Character%20encoding_%20Use%20subset%20of%20ASCII%20for%20safety) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152346)
## Comments:

|  |
| ----|
| You may also want to reference 
UTF-8 and Unicode FAQ for Unix/Linux
by Markus Kuhn 
http://www.cl.cam.ac.uk/~mgk25/unicode.html
The section on handling invalid inputs describes a problem without providing any useful advice.  If you can't provide any useful advice, you should probably just eliminate the material.
Incorporate the description of what the RFC says into the article, and add a reference to the actual document in the reference section.  All your references are incorrectly formatted.
                                        Posted by rcs at May 06, 2007 07:55
                                     |
| The Viega code does not reject non-minimal forms.
                                        Posted by jonathan.leffler@gmail.com at Mar 20, 2008 03:10
                                     |
| In the second property of UTF-8, after "no ASCII byte" add "(including a null byte)", since that property allows use of str* functions.
It should be noted that although UTF-8 originated from the Plan 9 developers, Plan 9's own;support only covers the low 16-bit range.  In general, many "Unicode" systems only support that range, not the full 31-bit ISO 10646 code space.
                                        Posted by dagwyn at Apr 18, 2008 14:32
                                     |
| The table is misleading at the moment - I started to edit it, but I'm not sure what you're trying to show with it.; The '*' notations are not explained, which is part of the trouble.  I suspect you are trying to delineate the minimal ranges, and attempting to exclude the non-minimal ranges.  It might be easier to do that in a second table.  The first table should document the basic UTF-8 notation.  The second should list the ranges of proscribed values.  I think that would be easier to understand.
The sixth and seventh lines appear to be pure duplicates of each other.
The last (eighth) line should probably have 1111 10xx as the first byte.
It might be worth noting that bytes 0xC0 and 0xC1 can never appear in valid UTF-8 data.  You might also note that 0x10FFFFF is the largest Unicode code-point possible.  Whether you want to get into issues with byte-order marks and non-breaking zero-width spaces and the like is debatable.
Unicode 5 (strictly 5.1.0) is current. 
                                        Posted by jonathan.leffler@gmail.com at May 11, 2008 01:16
                                     |
| [Yergeau 1998];or RFC2279 is obsolete and replaced by RFC3629. So the quote should be updated to refer to RFC3629.The table is not only misleading, but technically wrong. "Valid UTF-8 Values (HEX)" are actually not valid on Unicode Standard 6.1 as shown in "Table 3-7. Well-Formed UTF-8 Byte Sequnces" of Unicode Standard 6.1 (which you can find at http://www.unicode.org/versions/Unicode6.1.0/ch03.pdf ). Our table should be replaced by Table 3-7 of the Unicode Standard 6.1I tried to add Roelker 2004 (which I added to the AA. Bibliography section) to the "Sources" section of this rule but couldn't figure out how to do that (due to the update of the confluence, I cannot edit the html source ...)
                                        Posted by masaki at Dec 21, 2012 00:32
                                     |

