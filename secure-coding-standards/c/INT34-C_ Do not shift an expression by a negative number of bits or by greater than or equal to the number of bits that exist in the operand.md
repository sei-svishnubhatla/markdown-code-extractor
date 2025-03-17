Bitwise shifts include left-shift operations of the form *shift-expression* `<<` *additive-expression* and right-shift operations of the form *shift-expression* `>>` *additive-expression*. The standard integer promotions are first performed on the operands, each of which has an integer type. The type of the result is that of the promoted left operand. If the value of the right operand is negative or is greater than or equal to the width of the promoted left operand, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See [undefined behavior 48](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_48).)
Do not shift an expression by a negative number of bits or by a number greater than or equal to the *precision* of the promoted left operand. The precision of an integer type is the number of bits it uses to represent values, excluding any sign and padding bits. For unsigned integer types, the width and the precision are the same; whereas for signed integer types, the width is one greater than the precision. This rule uses precision instead of width because, in almost every case, an attempt to shift by a number of bits greater than or equal to the precision of the operand indicates a bug (logic error). A logic error is different from overflow, in which there is simply a representational deficiency.  In general, shifts should be performed only on unsigned operands. (See [INT13-C. Use bitwise operators only on unsigned operands](INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands).)
## Noncompliant Code Example (Left Shift, Unsigned Type)
The result of `E1 << E2` is `E1` left-shifted `E2` bit positions; vacated bits are filled with zeros. The following diagram illustrates the left-shift operation.
![](attachments/87152418/88038562.jpg)
According to the C Standard, if `E1` has an unsigned type, the value of the result is `E1` \* `2`<sup>`E2`</sup>, reduced modulo 1 more than the maximum value representable in the result type. 
This noncompliant code example fails to ensure that the right operand is less than the precision of the promoted left operand:
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int uresult = ui_a << ui_b;
  /* ... */
}
```
## Compliant Solution (Left Shift, Unsigned Type)
This compliant solution eliminates the possibility of shifting by greater than or equal to the number of bits that exist in the precision of the left operand:
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(x) popcount(x)
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int uresult = 0;
  if (ui_b >= PRECISION(UINT_MAX)) {
    /* Handle error */
  } else {
    uresult = ui_a << ui_b;
  }
  /* ... */
}
```
The `PRECISION()` macro and `popcount()` function provide the correct precision for any integer type. (See [INT35-C. Use correct integer precisions](INT35-C_%20Use%20correct%20integer%20precisions).)
Modulo behavior resulting from left-shifting an unsigned integer type is permitted by exception INT30-EX3 to [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).
## Noncompliant Code Example (Left Shift, Signed Type)
The result of `E1 << E2` is `E1` left-shifted `E2` bit positions; vacated bits are filled with zeros. If `E1` has a signed type and nonnegative value, and `E1` \* `2`<sup>`E2`</sup> is representable in the result type, then that is the resulting value; otherwise, the behavior is undefined.
This noncompliant code example fails to ensure that left and right operands have nonnegative values and that the right operand is less than the precision of the promoted left operand. This example does check for signed integer overflow in compliance with [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow).
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
void func(signed long si_a, signed long si_b) {
  signed long result;
  if (si_a > (LONG_MAX >> si_b)) {
    /* Handle error */
  } else {
    result = si_a << si_b;
  }
  /* ... */
}
```
Shift operators and other bitwise operators should be used only with unsigned integer operands in accordance with [INT13-C. Use bitwise operators only on unsigned operands](INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands).
## Compliant Solution (Left Shift, Signed Type)
In addition to the check for overflow, this compliant solution ensures that both the left and right operands have nonnegative values and that the right operand is less than the precision of the promoted left operand:
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(x) popcount(x)
void func(signed long si_a, signed long si_b) {
  signed long result;
  if ((si_a < 0) || (si_b < 0) ||
      (si_b >= PRECISION(ULONG_MAX)) ||
      (si_a > (LONG_MAX >> si_b))) {
    /* Handle error */
  } else {
    result = si_a << si_b;
  }
  /* ... */
}
```
Noncompliant Code Example (Right Shift)
The result of `E1 >> E2` is `E1` right-shifted `E2` bit positions. If `E1` has an unsigned type or if `E1` has a signed type and a nonnegative value, the value of the result is the integral part of the quotient of `E1` / `2`<sup>`E2`</sup>. If `E1` has a signed type and a negative value, the resulting value is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior) and can be either an arithmetic (signed) shift
![](attachments/87152418/88038557.jpg)
or a logical (unsigned) shift
![](attachments/87152418/88018503.jpg)
This noncompliant code example fails to test whether the right operand is greater than or equal to the precision of the promoted left operand, allowing undefined behavior:
``` c
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int uresult = ui_a >> ui_b;
  /* ... */
}
```
When working with signed operands, making assumptions about whether a right shift is implemented as an arithmetic (signed) shift or a logical (unsigned) shift can also lead to [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). (See [INT13-C. Use bitwise operators only on unsigned operands](INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands).)
## Compliant Solution (Right Shift)
This compliant solution eliminates the possibility of shifting by greater than or equal to the number of bits that exist in the precision of the left operand:
``` c
#include <limits.h>
#include <stddef.h>
#include <inttypes.h>
extern size_t popcount(uintmax_t);
#define PRECISION(x) popcount(x)
void func(unsigned int ui_a, unsigned int ui_b) {
  unsigned int uresult = 0;
  if (ui_b >= PRECISION(UINT_MAX)) {
    /* Handle error */
  } else {
    uresult = ui_a >> ui_b;
  }
  /* ... */
}
```
### Implementation Details
GCC has no options to handle shifts by negative amounts or by amounts outside the width of the type predictably or to trap on them; they are always treated as undefined. Processors may reduce the shift amount modulo the width of the type. For example, 32-bit right shifts are implemented using the following instruction on x86-32:
``` java
sarl   %cl, %eax
```
The `sarl` instruction takes a bit mask of the least significant 5 bits from `%cl` to produce a value in the range \[0, 31\] and then shift `%eax` that many bits:
``` java
// 64-bit right shifts on IA-32 platforms become
shrdl  %edx, %eax
sarl   %cl, %edx
```
where `%eax` stores the least significant bits in the doubleword to be shifted, and `%edx` stores the most significant bits.
## Risk Assessment
Although shifting a negative number of bits or shifting a number of bits greater than or equal to the width of the promoted left operand is undefined behavior in C, the risk is generally low because processors frequently reduce the shift amount modulo the width of the type.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT34-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | precision-shift-widthprecision-shift-width-constant | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT34 | Can detect shifts by a negative or an excessive number of bits and right shifts on negative values. |
| CodeSonar | 8.3p0 | LANG.ARITH.BIGSHIFTLANG.ARITH.NEGSHIFT | Shift amount exceeds bit widthNegative shift amount |
| Compass/ROSE |  |  | Can detect violations of this rule. Unsigned operands are detected when checking for INT13-C. Use bitwise operators only on unsigned operands |
| Coverity | 2017.07 | BAD_SHIFT | Implemented |
| Cppcheck | ;2.15 | shiftNegative, shiftTooManyBits |  |
| Cppcheck Premium | 24.11.0 | shiftNegative, shiftTooManyBitspremium-cert-int34-c |  |
| ECLAIR | 1.2 | CC2.INT34 | Partially implemented |
| Helix QAC | 2024.4 | C0499, C2790,;C++2790,  C++3003DF2791, DF2792, DF2793 |  |
| Klocwork | 2024.4 | MISRA.SHIFT.RANGE.2012 |  |
| LDRA tool suite | 9.7.1 | 51 S, 403 S, 479 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-INT34-a | Avoid incorrect shift operations |
| Polyspace Bug Finder | R2024a | CERT C: Rule INT34-C | Checks for:Shift of a negative valueShift operation overflowRule partially covered. |
| PVS-Studio | 7.35 | V610 |  |
| RuleChecker | 24.04 | precision-shift-width-constant | Partially checked |
| TrustInSoft Analyzer | 1.38 | shift | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT34-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | INT13-C. Use bitwise operators only on unsigned operands | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT35-C. Use correct integer precisions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | INT32-C. Ensure that operations on signed integers do not result in overflow | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Arithmetic Wrap-Around Error [FIF] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-682 | 2017-07-07: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-758 | 2017-07-07: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-758 and INT34-C
Independent( INT34-C, INT36-C, MEM30-C, MSC37-C, FLP32-C, EXP33-C, EXP30-C, ERR34-C, ARR32-C)
CWE-758 = Union( INT34-C, list) where list =
-   Undefined behavior that results from anything other than incorrect bit shifting
### CWE-682 and INT34-C
Independent( INT34-C, FLP32-C, INT33-C) CWE-682 = Union( INT34-C, list) where list =
-   Incorrect calculations that do not involve out-of-range bit shifts
## Bibliography

|  |  |
| ----|----|
| [C99 Rationale 2003] | 6.5.7, "Bitwise Shift Operators" |
| [Dowd 2006] | Chapter 6, "C Language Issues" |
| [Seacord 2013b] | Chapter 5, "Integer Security" |
| [Viega 2005] | Section 5.2.7, "Integer Overflow" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152254) [](../c/Rule%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151939)
## Attachments:
![](images/icons/bullet_blue.gif) [ShiftRight.JPG](attachments/87152418/88038557.jpg) (image/jpeg)  
![](images/icons/bullet_blue.gif) [ShiftLeft.JPG](attachments/87152418/88038562.jpg) (image/jpeg)  
![](images/icons/bullet_blue.gif) [leftshift.cpp](attachments/87152418/88038559.cpp) (text/plain)  
![](images/icons/bullet_blue.gif) [LogicalShiftRight.JPG](attachments/87152418/88018503.jpg) (image/jpeg)  
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>What's up with the test program in the references?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jun 11, 2008 14:57
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>In the code for the compliant solution (left shift, unsigned type) it appears that mod2 and mod1 are never assigned a value. Is there something in the solution that sets mod1 and mod2 that I am missing?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by sayre@cert.org at Jul 10, 2008 16:31
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Yeah, that's true. Also, this code snippets are non-compliant with <a href="DCL04-C_%20Do%20not%20declare%20more%20than%20one%20variable%20per%20declaration">DCL04-C. Do not declare more than one variable per declaration</a></p>
<p>Also, the last compliant solution didn't even compile because the variables had different names (<code>result</code> vs <code>uresult</code>.</p>
<p>I've fixed up some of these examples. I'll finish the rest later, unless someone beats me to it.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jul 10, 2008 19:29
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I'm also confused as to why the Non-Compliant Code Example (Right Shift) has signed and unsigned examples, but the compliant solution only uses unsigned.</p>
<p>I think we have a recommendation somewhere that <a href="INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands">INT13-C. Use bitwise operators only on unsigned operands</a>. This should probably be referenced above.</p>
<p>It may still be OK to show compliant solutions for signed types, so that if someone tries to do this we have an example of how to do it. However, they should reference <a href="INT13-C_%20Use%20bitwise%20operators%20only%20on%20unsigned%20operands">INT13-C. Use bitwise operators only on unsigned operands</a> to indicate that this practice is not recommended.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jul 10, 2008 19:34
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>This problem still (urgently) needs to be addressed.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jul 21, 2008 18:56
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I think I addressed this problem by removing the signed types from the non-compliant solution. I also think we should not introduce a compliant solution that would violate one of our own recommendations.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 22, 2008 09:39
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>In the first NCCE, the diagram shows a '1' in the leftmost box, which disappears when the byte is shifted. Doesn't this represent an int that is 'too large' to be shifted properly? (either it's unsigned and &gt; UINT_MAX/2 or it's signed &amp; &lt;0.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jul 22, 2008 10:36
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Yes that is true, but perhaps OK in this context. The example is only meant to show how this works, and it is in the NCE section so is actually an example of the problem.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jul 22, 2008 13:48
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>uhhh... doesn't this line in the first CCE violate the rule?</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb1" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="cf">if</span> <span class="op">(</span> <span class="op">(</span>ui2 <span class="op">&gt;=</span> <span class="fu">sizeof</span><span class="op">(</span>unsigned <span class="dt">int</span><span class="op">)*</span>CHAR_BIT<span class="op">)</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>  <span class="op">||</span> <span class="op">(</span>ui1 <span class="op">&gt;</span> <span class="op">(</span>UINT_MAX  <span class="op">&gt;&gt;</span> ui2<span class="op">)))</span> ) <span class="op">{</span></span></code></pre></div>
</div>
</div>
<p>Note how UINT_MAX is being shifted by more bits than exist in the operand...</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 24, 2008 15:07
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>robert sez:</p>
<blockquote>
<p>I'm thinking that because of short circuiting rules, the second operand to || is not executed if the first one is true</p>
</blockquote>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 24, 2008 16:38
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>In that case I guess this is a false positive that we can't really avoid without dynamic analysis</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 24, 2008 16:38
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Why? By the logic of his if statement, if the 2nd part of the if expression executes then {{ui2} &lt; sizeof(CHAR_BIT). And since we know it is unsigned, we can therefore validate the shift operation at compile time (or with ROSE).</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jul 24, 2008 17:05
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>And how do you propose we match the condition <code>ui2 &lt; sizeof(CHAR_BIT)</code> using ROSE? Especially knowing that there are at least 100 different ways to structure that conditional statement?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 25, 2008 09:27
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Right, there are 100 different ways to structure the cond. For now just worry about the two that are demonstrated by the code examples here.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jul 25, 2008 10:07
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Sorry to come on such an old article.</p>
<p>First of all : thank you very much because I was becoming creasy.</p>
<p>Secondly : using a negative parameter should not be a bug. In terms of algorithmic, it is usefull. At least for me and my algorithm. To escape from undefined, I have to write two lines instead of one with an <em>if.</em> </p>
<p>I understand that in assembly language, the result is undefined. But in my opinion, C++ standard should accept it and manage it because writting code with a parameter that can be negative is natural, while shaking one's mind to anticipate what the processor will do is not. Or suppress simply every languages except assembly ! <em>natural</em> here  means that I do expect it to work and I don't ask myself the question.</p>
<p>Moreover, the compiler does not issue any warning, even with all the warnings enabled. That's another argument to make it work.</p>
<p>One may argue against me that if the compiler adds a test in the assembly translation of &lt;&lt; or &gt;&gt;, it will be less efficient. My answer is C and C++ are (also) high level languages and the first priority is robustness. And one can include assembly code easily. Or we may have variants : &gt;&gt;&gt; and &lt;&lt;&lt;.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by lalebarde at Feb 16, 2012 09:30
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Shifting by a negative number is explicitly mentioned as undefined behavior by the C and C++ standards. This gives different platform vendors the latitude to have the system do whatever they want (usually whatever is fastest) when they encounter it. I believe i86 ignores all but the least significant 5 bits of the right operand to a shift operation, so if you know your code only runs on those platforms you <strong>could</strong> rely on that behavior. But we don't recommend it, as your code is inherently non-portable.</p>
<p>Given that other vendors most likely do something different when the right operand is negative, I doubt the standards committees are inclined to change this behavior.</p>
<p>The compiler is not officiially required to issue a warning, although some try to. Perhaps your compiler simply cannot determine that shifting by a negative number is occurring. Alas, that means it is your responsibility to make sure your right operand is positive (and not more than the number of bits in your left operand.)</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Feb 16, 2012 19:02
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>So the C and C++ standards are bad ! Just my opinion.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by lalebarde at Feb 17, 2012 05:23
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Only if you think that this feature (shifting a negative number of bits) outweighs the portability and speed that platforms gain by leaving this behavior undefined. Clearly the C committee believed otherwise (and still does).</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Feb 17, 2012 10:16
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><blockquote>
<div class="code panel pdl" style="border-width: 1.0px;">
<div class="codeContent panelContent pdl">
<div>
<div class="syntaxhighlighter nogutter java">
<div class="table-wrap">
<pre class="table"><code>|  |
| ----|
| // 64-bit shifts on IA-32 platforms becomesh[rl]dl; %eax, %edxsa[rl]l   %cl, %eax |</code></pre>
</div>
<p> </p>
</div>
</div>
</div>
</div>
<p>where <code>%eax</code> stores the least significant bits in the doubleword to be shifted, and <code>%edx</code> stores the most significant bits.</p>
</blockquote>
<p>about implementation details.</p>
<div class="line number3 index2 alt2">
<div class="line number1 index0 alt2">
I think 64bit data shifting cannot be written in a single pattern.
</div>
</div>
<div class="line number1 index0 alt2">
LEFT shifing 64bit data should be
</div>
<div class="line number3 index2 alt2" style="margin-left: 30.0px;">
  shldl %cl, %eax, %edx
</div>
<div class="line number3 index2 alt2" style="margin-left: 30.0px;">
  s[ah]ll  %cl, %eax
</div>
<div class="line number3 index2 alt2">
and RIGHT shifing 64bit data should be
</div>
<div class="line number3 index2 alt2" style="margin-left: 30.0px;">
  shrdl  %cl, %edx, %eax
</div>
<div class="line number3 index2 alt2" style="margin-left: 30.0px;">
  s[ah]rl %cl, %edx
</div>
<div class="line number3 index2 alt2">
anyone please confirm this?
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by yozo at Aug 20, 2014 08:02
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>GCC 4.9.0 produces (using AT&amp;T syntax):</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb3" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="dt">int</span> <span class="fu">main</span><span class="op">(</span><span class="dt">void</span><span class="op">)</span> <span class="op">{</span></span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">long</span> <span class="dt">long</span> op1 <span class="op">=</span> <span class="dv">12</span><span class="op">;</span> <span class="co">// Expository</span></span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a>  <span class="dt">long</span> <span class="dt">long</span> op2 <span class="op">=</span> <span class="dv">36</span><span class="op">;</span> <span class="co">// Expository</span></span>
<span id="cb3-4"><a href="#cb3-4" aria-hidden="true" tabindex="-1"></a>  <span class="dt">long</span> <span class="dt">long</span> l <span class="op">=</span> op1 <span class="op">&lt;&lt;</span> op2<span class="op">;</span> <span class="co">// Change the op to change the generated disassembly</span></span>
<span id="cb3-5"><a href="#cb3-5" aria-hidden="true" tabindex="-1"></a><span class="op">}</span></span>
<span id="cb3-6"><a href="#cb3-6" aria-hidden="true" tabindex="-1"></a> </span>
<span id="cb3-7"><a href="#cb3-7" aria-hidden="true" tabindex="-1"></a><span class="co">// &lt;&lt;</span></span>
<span id="cb3-8"><a href="#cb3-8" aria-hidden="true" tabindex="-1"></a>shldl   <span class="op">%</span>eax<span class="op">,</span> <span class="op">%</span>edx</span>
<span id="cb3-9"><a href="#cb3-9" aria-hidden="true" tabindex="-1"></a>sall    <span class="op">%</span>cl<span class="op">,</span> <span class="op">%</span>eax</span>
<span id="cb3-10"><a href="#cb3-10" aria-hidden="true" tabindex="-1"></a> </span>
<span id="cb3-11"><a href="#cb3-11" aria-hidden="true" tabindex="-1"></a><span class="co">// &gt;&gt;</span></span>
<span id="cb3-12"><a href="#cb3-12" aria-hidden="true" tabindex="-1"></a>shrdl   <span class="op">%</span>edx<span class="op">,</span> <span class="op">%</span>eax</span>
<span id="cb3-13"><a href="#cb3-13" aria-hidden="true" tabindex="-1"></a>sarl    <span class="op">%</span>cl<span class="op">,</span> <span class="op">%</span>edx</span></code></pre></div>
</div>
</div>
<p>So you are correct, two different patterns are needed. I have rectified this now, thank you for pointing it out!</p>
<p>You can play with this yourself using <a href="http://gcc.godbolt.org">http://gcc.godbolt.org</a> if you don't have a GCC implementation handy.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by aballman at Aug 20, 2014 08:46
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>thanks, Aaron.</p>
<p>I fixed the register operands for correct right shifting (-:</p>
<p>and thanks too for the information on gcc.godbolt.org!</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by yozo at Aug 23, 2014 11:58
</div></td>
</tr>
</tbody>
</table>
