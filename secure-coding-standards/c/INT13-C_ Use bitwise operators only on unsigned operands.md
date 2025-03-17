Bitwise operators include the complement operator `~`, bitwise shift operators `>>` and `<<`, bitwise AND operator `&`, bitwise exclusive OR operator `^`, bitwise inclusive OR operator `|` and compound assignment operators \>\>=, \<\<=, &=, ^= and \|=. Bitwise operators should be used only with unsigned integer operands, as the results of bitwise operations on signed integers are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior).
The C11 standard, section 6.5, paragraph 4 \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/c/AA.+Bibliography#AA.Bibliography-ISO-IEC9899-2011)\], states:
> Some operators (the unary operator ~ , and the binary operators \<\<, \>\>, &, ^, and \|, collectively described as bitwise operators) shall have operands that have integral type. These operators return values that depend on the internal representations of integers, and thus have implementation-defined and undefined aspects for signed types.

Furthermore, the bitwise shift operators \<\< and `>>` are undefined under many circumstances, and are implementation-defined for signed integers for more circumstances; see rule [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](INT34-C_%20Do%20not%20shift%20an%20expression%20by%20a%20negative%20number%20of%20bits%20or%20by%20greater%20than%20or%20equal%20to%20the%20number%20of%20bits%20that%20exist%20in%20the%20operand) for more information.
### Implementation details
The Microsoft C compiler documentation says that:
> Bitwise operations on signed integers work the same as bitwise operations on unsigned integers.

On-line GCC documentation about the implementation of bitwise operations on signed integers says:
> Bitwise operators act on the representation of the value including both the sign and value bits, where the sign bit is considered immediately above the highest-value value bit.

## Noncompliant Code Example (Right Shift)
The right-shift operation may be implemented as either an arithmetic (signed) shift or a logical (unsigned) shift. If `E1` in the expression `E1 >> E2` has a signed type and a negative value, the resulting value is implementation-defined. Also, a bitwise shift can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](INT34-C_%20Do%20not%20shift%20an%20expression%20by%20a%20negative%20number%20of%20bits%20or%20by%20greater%20than%20or%20equal%20to%20the%20number%20of%20bits%20that%20exist%20in%20the%20operand).)
This noncompliant code example can result in an error condition on [implementations](BB.-Definitions_87152273.html#BB.Definitions-implementation) in which an arithmetic shift is performed, and the sign bit is propagated as the number is shifted \[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\]:
``` c
int rc = 0;
int stringify = 0x80000000;
char buf[sizeof("256")];
rc = snprintf(buf, sizeof(buf), "%u", stringify >> 24);
if (rc == -1 || rc >= sizeof(buf)) {
  /* Handle error */
}
```
In this example, `stringify >> 24` evaluates to `0xFFFFFF80`, or 4,294,967,168. When converted to a string, the resulting value `"4294967168"` is too large to store in `buf` and is truncated by `snprintf()`.
If this code had been implemented using `sprintf()` instead of `snprintf()`, this noncompliant code example would have resulted in a buffer overflow.
## Compliant Solution (Right Shift)
In this compliant solution, `stringify` is declared as an `unsigned` integer. The value of the result of the right-shift operation is the integral part of the quotient of `stringify` `/ 2 ^ 24`:
``` c
int rc = 0;
unsigned int stringify = 0x80000000;
char buf[sizeof("256")];
rc = snprintf(buf, sizeof(buf), "%u", stringify >> 24);
if (rc == -1 || rc >= sizeof(buf)) {
  /* Handle error */
}
```
Also, consider using the `sprintf_s()` function, defined in ISO/IEC TR 24731-1, instead of `snprintf()` to provide some additional checks. (See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).)
## Exceptions
**INT13-C-EX1:** When used as bit flags, it is acceptable to use preprocessor macros or enumeration constants as arguments to the `&` and `|` operators even if the value is not explicitly declared as unsigned.
``` c
fd = open(file_name, UO_WRONLY | UO_CREAT | UO_EXCL | UO_TRUNC, 0600);
```
**INT13-C-EX2:** If the right-side operand to a shift operator is known at compile time, it is acceptable for the value to be represented with a signed type provided it is positive.
``` c
#define SHIFT 24
foo = 15u >> SHIFT;
```
## Risk Assessment
Performing bitwise operations on signed numbers can lead to buffer overflows and the execution of arbitrary code by an attacker in some cases, unexpected or implementation-defined behavior in others.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT13-C | High | Unlikely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | bitop-type | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT13 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.IOT | Inappropriate operand type |
| Compass/ROSE |  |  | Can detect violations of this rule. In particular, it flags bitwise operations that involved variables not declared with unsigned type |
| ECLAIR | 1.2 | CC2.INT13 | Fully implemented |
| Helix QAC | 2024.4 | C4532, C4533, C4534, C4543, C4544 |  |
| Klocwork | 2024.4 | MISRA.BITS.NOT_UNSIGNEDMISRA.BITS.NOT_UNSIGNED.PREP |  |
| LDRA tool suite | 9.7.1 | 50 S120 S
331 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT13-aCERT_C-INT13-b
 | Operands of bitwise and complement operators shall have an unsigned typeOperands of shift operators shall have an unsigned type |
| PC-lint Plus | 1.4 | 9233 | Partially supported: reports use of a bitwise operator on an expression with a signed MISRA C 2004 underlying type |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT13-C | Checks for bitwise operation on negative value (rec. fully covered) |
| RuleChecker | 24.04 | bitop-type | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S874 |  |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT13-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT13-CPP. Use bitwise operators only on unsigned operands |
| ISO/IEC TR 24772:2013 | Bit Representations [STR]Arithmetic Wrap-around Error [FIF]
Sign Extension Error [XZI] |
| MITRE CWE | CWE-682, Incorrect calculation |

## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [C99 Rationale 2003] | Subclause 6.5.7, "Bitwise Shift Operators" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152212) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152075)
## Comments:

|  |
| ----|
| The code used in the example:
char buf[sizeof("256")];

is asking to confuse readers - this has nothing to do with 256 - a common buffer limit - but instead represents the space required to store three characters plus a trailing NUL. I guarantee this will create a double-take.
Wouldn't it illustrate the point better as:
``` java
char buf[sizeof("XXX")];
```
;or (better), just
``` java
char buf[3+1]; // 3 chars plus trailing NUL
```
?  
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 13, 2008 23:37
\| \|
To me this looks clearer as is.; It makes explicit the fact that the maximum number to be converted is 256.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 14, 2008 00:11
\| \|
Sure there are. If a variable is signed (maybe due to some API or data structure you are using) and you need it shifted, you might as well do x \<\<= 2 or whatever and be done with it. \[Edit: If you check properly that you dont' shift in or out of the sign anyway.; If you don't check, unsigned shifting behaves better.\]
You can copy it to unsigned and shift, but then you need to assign it back to signed, which means you must test that it's in range for that anyway. It might be less work to test that the signed value is in range for shifting instead.
Also one little trap: Shifting "signed items" happens when you shift an unsigned variable narrower than int. The variable is promoted to (signed) int, and that's what you shift.
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 14, 2008 09:18
\| \|
The real issue is that left shifting a signed value leads to implementation-defined behavior. This is never a good thing to have...
;The easiest way to guard against this (and make it tool detectable) is to prohibit shifting of signed objects.
![](images/icons/contenttypes/comment_16.png) Posted by keylevel at May 29, 2008 11:03
\| \|
Because this is a recommendation, I think it is reasonable to recommend that "bitwise operators be used with unsigned operands". I think perhaps we can preserve the current example, including the discussion of logical vs. arithmetic shift, and add a left shift example discussing the implementaiton defined behavior.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at May 29, 2008 12:01
\| \|
Hm. The title is definitely too strong. For unsigned ints it is perfectly safe to assume logical & arithmetic shift. I believe the same is true for unsigned short or char (as long as you don't potentially lose data casting the result back to a short/char)
The problem is strictly with signed integers (of all sizes), and then you're still OK as long as your domain number is nonnegative, and your output number doesn't exceed the size limit of your signed type, potentially twiddling the sign bit.
Hallvard's instances of using shifts on signed integers don't convince me...they are operationally identicial to converting to unsigned, shifting, and converting back (including range checks)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 29, 2008 12:39
\| \|
I've changed the title and scope of this rule and it is now ready for review. I did not add a second example, because I thought the rule was fairly self-explanatory although it is still a little vague in places, for example, "the results of some bitwise operations on signed integers is implementation-defined".
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at May 30, 2008 09:27
\| \|
> "Hallvard's instances of using shifts on signed integers don't convince me...they are operationally identicial to converting to unsigned, shifting, and converting back (including range checks)"

Yes, that was my point. Likely applying this rule to int x; ... x \>\>= 10; will simply mean replacing it with something like x = (int) ((unsigned) x \>\> 10);. This is less readable and doesn't gain anything that I can see: Instead of an "unsafe" shift you have an "unsafe" conversion to int - and the test to ensure a correct and safe result will likely be exactly the same.
;\[edit\] Which doesn't mean I think this is a bad recommendation, just that you asked for counterexamples and I can think of some.  But then, even the ruleagainst using uninitialized data has useful counterexamples - as in the recent debacle where OpenSSL uses uninitialized data as one source of randomness and Debian "fixed" that code.
About operating on narrower unsigneds than int, I'm just pointing out that when you do that, you do in fact operate on a signed value. Is this rule intended to apply to the operands before or after the integer promotions / usual arithmetic conversions? A shift example where it matters is possible but silly: Given a 16-bit short and 32-bit int, and unsigned short x; you can do x \<\< 20 which shifts it as an int - but that can then shift into the sign bit. More relevant in this case is ~x which actually does ~(int)x.
BTW, I had only skimmed this page before -- I note the example's "int stringify = 0x80000000;" has implementation-defined/undefined behavior, regardless of any shifting done afterwards. (Assuming 32-bit int, which the example does.)
![](images/icons/contenttypes/comment_16.png) Posted by hbf at May 31, 2008 01:07
\| \|
The exceptions to this rule arise because most predefined bitflags are not explicitly defined as unsigned int (such as the bitflags to `fopen()` illustrated in INT13A-EX1). These exceptions do allow one to create insecure code; their presence provides 'backwards compatibility' with the standard C headers defining these bitflags. New bitflag constants should be explicitly defined as `unsigned int`.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 27, 2008 13:01
\| \|
One could even mask the extended bits before use. The original value will be shifted as required but it will still protect the buffer overflow because of the masking. Interestingly, in Java a CS can be to use the logical shift operator "\>\>\>" as opposed to "\>\>" but in C there is only one kind of operator, the "\>\>". EDIT: On closer inspection this seems to fall under INT13-EX2.
![](images/icons/contenttypes/comment_16.png) Posted by dmohindr at Oct 10, 2009 21:27
\| \|
compliant solution (Right Shift) has no color. how can we edit the bgcolor?
(I cannot find any clue to change bgcolor on editing code block macro window...)
;
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Feb 12, 2015 06:47
\| \|
I've fixed it;– the color was set properly by the editor, but it wasn't being honored by the renderer. This happens sometimes, and the only way I've found to fix it is to delete the code block entirely and copy/paste in a working one. Thank you for pointing it out, though!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Feb 12, 2015 09:07
\| \|
Thanks, Aaron!;I didn't think of copy-and-pasting the working block...
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Feb 15, 2015 00:59
\| \|
i have some question about this rule. From the bitwise operation's result, only right shift will cause undefined behavior , for others bitwise like complement operator, left shift, AND operator,exclusive OR and;inclusive OR operator will not cause undefined behavior. So shall we just think about the right shift? May we get some example for the bitwise operation except right shift?
![](images/icons/contenttypes/comment_16.png) Posted by shendong70 at Apr 20, 2018 23:50
\| \|
Don't conflate undefined behavior with implementation-defined behavior. The code examples in this recommendation illustrate implementation-defined behavior. Undefined behavior is illustrated in depth in rule;[INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand](INT34-C_%20Do%20not%20shift%20an%20expression%20by%20a%20negative%20number%20of%20bits%20or%20by%20greater%20than%20or%20equal%20to%20the%20number%20of%20bits%20that%20exist%20in%20the%20operand).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 23, 2018 09:40
\| \|
Isn't this completely redundant to [INT16-C. Do not make assumptions about representation of signed integers](INT16-C_%20Do%20not%20make%20assumptions%20about%20representation%20of%20signed%20integers)?
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Jul 09, 2020 16:49
\| \|
Not quite. There is overlap, and you could argue that INT16-C includes the contents of this rec. But this rec is of a more specific problem and goes into more detail.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 10, 2020 09:25
\|
