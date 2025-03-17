Immutable objects should be `const`-qualified. Enforcing object immutability using `const` qualification helps ensure the correctness and security of applications. ISO/IEC TR 24772, for example, recommends labeling parameters as constant to avoid the unintentional modification of function arguments \[[ISO/IEC TR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24772-2010)\]. [STR05-C. Use pointers to const when referring to string literals](STR05-C_%20Use%20pointers%20to%20const%20when%20referring%20to%20string%20literals) describes a specialized case of this recommendation.
Adding `const` qualification may propagate through a program; as you add `const`, qualifiers become still more necessary. This phenomenon is sometimes called *`const` poisoning*, which can frequently lead to violations of [EXP05-C. Do not cast away a const qualification](EXP05-C_%20Do%20not%20cast%20away%20a%20const%20qualification). Although `const` qualification is a good idea, the costs may outweigh the value in the remediation of existing code.
A macro or an enumeration constant may also be used instead of a `const`-qualified object. [DCL06-C. Use meaningful symbolic constants to represent literal values](DCL06-C_%20Use%20meaningful%20symbolic%20constants%20to%20represent%20literal%20values) describes the relative merits of using `const`-qualified objects, enumeration constants, and object-like macros. However, adding a `const` qualifier to an existing variable is a better first step than replacing the variable with an enumeration constant or macro because the compiler will issue warnings on any code that changes your `const`-qualified variable. Once you have verified that a `const`-qualified variable is not changed by any code, you may consider changing it to an enumeration constant or macro, as best fits your design.
## Noncompliant Code Example
In this noncompliant code, `pi` is declared as a `float`. Although pi is a mathematical constant, its value is not protected from accidental modification.
``` c
float pi = 3.14159f;
float degrees;
float radians;
/* ... */
radians = degrees * pi / 180;
```
## Compliant Solution
In this compliant solution, `pi` is declared as a `const`-qualified object:
``` c
const float pi = 3.14159f;
float degrees;
float radians;
/* ... */
radians = degrees * pi / 180;
```
## Risk Assessment
Failing to `const`-qualify immutable objects can result in a constant being modified at runtime.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL00-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | parameter-missing-const | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL00 |  |
| CodeSonar | 8.3p0 | LANG.CAST.PC.CRCQLANG.TYPE.VCBCLANG.STRUCT.RPNTC | Cast removes const qualifierVariable Could Be constReturned Pointer Not Treated as const |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.DCL00 | Partially implemented |
| Helix QAC | 2024.4 | C3204, C3227, C3232, C3673, C3677 |  |
| LDRA tool suite | 9.7.1 | 78 D93 D
200 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL00-aCERT_C-DCL00-b
 | Declare local variable as const whenever possibleDeclare parameters as const whenever possible |
| PC-lint Plus | 1.4 | 953 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: DCL00-C | Checks for unmodified variable not const-qualified (rule fully covered). |
| RuleChecker | 24.04 | parameter-missing-const | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL00-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL00-CPP. Const-qualify immutable objects |

##  Bibliography

|  |  |
| ----|----|
| [Dewhurst 2002] | Gotcha #25, "#define Literals" |
| [Saks 2000] |  |

------------------------------------------------------------------------
[](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152192)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>What exactly makes it a feature to prevent the programmer from taking the address of a const integer?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by josh@freedesktop.org at Mar 16, 2008 05:42
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The most significant case I could think of would be where you have an API function that takes an integer pointer as an argument and then changes that argument. For example:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb1" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="dt">int</span> <span class="fu">wait_for_event</span><span class="op">(</span>event_t event<span class="op">,</span> <span class="dt">int</span> <span class="op">*</span> msec_to_wait<span class="op">);</span></span></code></pre></div>
</div>
</div>
<p>If the programmer passes a constant integer to our hypothetical function here, not realizing that the function actually modifies msec_to_wait to indicate how many msec's actually elapsed or remain (roughly analogous to the way that select(2) can do for a struct timeval), unexpected behavior will occur. Such a mistake would not be possible with an enum constant or a #define constant - it would force putting the constant in a variable first, and then calling wait_for_event().</p>
<p>Of course, the programmer should use const which will elicit a compiler warning when passed to this function, and I believe there is another recommendation on this site regarding functions that take pointers to values like this, but nevertheless with secure coding it is usual to follow the "belt and suspenders" principle and nip something in the bud at various levels.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by gbeeley at Mar 17, 2008 16:51
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I basically disagree with this guideline.  The only real value I see in this practice is that a debugger will show the identifier rather than the numeric value.  That has nothing to do with code safety.  Using #define avoids most of the problems listed for the other techniques.  I think this guideline originates in a C++ bias against the preprocessor.<br />
</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dagwyn at Apr 15, 2008 11:38
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>A strage rule, and a somewhat confused one. The intro<br />
does not seem to say the same as the meat of the rule either.</p>
<p>Objects of any type and complexity can be immutable.<br />
The intro says to constify everything we can, of any type.<br />
This leads to serious "const poisoning" - it requires<br />
functions and variables who will receive pointers to these<br />
objects to be constified too, and then functions/variables<br />
using these functions, and so on. Sooner or later you'll<br />
likely have to cast away a lost of consts somewhere.</p>
<p>Spurious consts are less painful in C++, where you have<br />
'const_cast', 'mutable' and much more ability to play<br />
with types.</p>
<p>Anyway, the meat of the suggestion seems to be something<br />
else: "use enum/const rather than #define". That can<br />
have its benefits at times, other times it would be<br />
limiting or costly. Personally I like enums for small<br />
const ints (for debuggers like you mention), but<br />
their limited both in range and what type I can make them.<br />
No such thing as "unsigned enum {}" for example.</p>
<p>expressions of integer constants and enums can also be<br />
expected to evaluated at compile time, but one can<br />
not expect the same of a const variable. That can<br />
make a noticeable difference at times. Sometimes it<br />
also allows for complex constant expressions which would<br />
be truly ridiculous pessimizations if the compiler<br />
did not optimize them.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by hbf at Apr 17, 2008 18:43
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>In general it is always easier to use 'const' in new programs, than to try to retrofit it into old programs. Both C and C++ allow you to override constness, with C++ being a bit more mature in this regard (having acquired the const keyword first).</p>
<p>The rule can be summed up as:</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |  |  |  |
| ----|----|----|----|----|
|  Method  |  Evaluated at  |  Memory Allocated  |  Viewable by Debuggers  |  Types  |
|  Enumerations  |  compile time  |  no  |  yes  |  only int  |
|  const variables  |  compile time  |  yes  |  yes  |  any type  |
|  Macros  |  preprocessor  |  no  |  no  |  typeless  |</code></pre>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Apr 18, 2008 09:22
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>No. In C, "const" variables need <em>not</em> be evaluated at compile time. In the abstract machine they are not, but the compiler can optimize that. And optimization or no, C programs may not use "const" variables as constant expressions (e.g. for array indexes). So:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb3" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a><span class="dt">const</span> <span class="dt">int</span> a <span class="op">=</span> <span class="dv">12345</span><span class="op">;</span></span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a><span class="dt">int</span> <span class="fu">foo</span><span class="op">(</span><span class="dt">void</span><span class="op">)</span> <span class="op">{</span> <span class="cf">return</span> a<span class="op">;</span> <span class="op">}</span></span>
<span id="cb3-3"><a href="#cb3-3" aria-hidden="true" tabindex="-1"></a><span class="dt">char</span> x<span class="op">[</span>a<span class="op">];</span></span></code></pre></div>
</div>
</div>
<p>gcc-3.4.6 i386/linux evaluates 'a' in foo() at runtime without -O and at compile time with -O.</p>
<p>The array declaration is valid in C++, but en error in C (with or without optimization).</p>
<p>Memory is allocated at startup in the abstract machine, but can be optimized away. BTW, I suggest avoiding the word "allocated" in this sense so it won't be confused with malloc &amp; co.</p>
<p>And be careful with the type of "enumerations" - do you mean the type of the declared "enum" (which is compatible with _some_ integer type) or the enumeration constants (which have type int)?</p>
<p>It is indeed easier to use const in a new program than insert it in an old one, but how easy or how good idea it is still depends on the program's structure, its data structures, what external APIs it'll use, etc.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by hbf at Apr 21, 2008 11:52
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Few compilers in the embedded world have a build option to specify that the smallest type possible be used for Enum. If this option is turned on then 1 byte can be used to store the enums, if this flag is not set then int is used.</p>
<p>These compilers also let the programmer specify the "signedness" for the enum type - usualy by default it is unsigned.</p>
<p>Also there are variants on how to specify the type - for example there is "<em>#pragma enumsalwaysint</em>" and then there <em>-fshort-enums</em></p>
<p>A programmer has to be aware of these quirks especially when porting code. So the size of the enum type shoudl be best classifed as compiler implementation defined, and the optimization flags.</p>
<p>C99 specifies that the underlying type for enum  is int; C++ specifies it as implementation defined.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by abhi at May 08, 2008 14:52
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I think the text is ok.  It's only a recommendation.  But Doug's comment suggests adding a further clarification, such as:</p>
<p>In a C project, constant values are often provided by #define in preference to const object data; indeed, this is the only way to provide a named compile-time constant in C.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by tplum@plumhall.com at May 27, 2008 16:49
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I added a paragraph discussing macros, as well as enumeration constants, as alternatives to const variabbles, along with a link to DCL06, which discusses the three strategies in detail.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at May 27, 2008 17:03
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I'm not sure I buy this:</p>
<blockquote>
<p>However, adding a const qualifier to an existing variable is a better first step than replacing the variable with an enumeration constant or macro, because the compiler will issue warnings on any code that changes your const-qualified variable. Once you have verified that a const-qualified variable is not changed by any code, you may consider changing it to an enumeration constant or macro, as best fits your design.</p>
</blockquote>
<p>Won't the compiler generate diagnostics if the program tries to change an rvalue or literal as well? Suggest we deleted these two sentences.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at May 29, 2008 12:26
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Does this part of both NCE/CS violate <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=FLP03-C.+Detect+and+handle+floating+point+errors">FLP03-C. Detect and handle floating point errors</a>:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb4" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb4-1"><a href="#cb4-1" aria-hidden="true" tabindex="-1"></a>degrees <span class="op">*</span> pi</span></code></pre></div>
</div>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jul 23, 2008 10:41
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Yes.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Aug 13, 2008 16:21
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>What do you mean by "correctness of applications"? The definition of correctness seems to be not so obvious.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by masaki at Apr 12, 2009 23:20
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Here we are referring to 'software correctness', IOW software that is bug-free; runs as designed. Our rules are about security, not correctness. But the good news is that security and correctness often go hand-in-hand. Violating this rule has more dire consequences for correctness than for security, but security is affected enough to warrant its presence in this standard.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Apr 13, 2009 17:37
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>&gt;&gt; The value <code>1 &lt;&lt; 16</code> could be an <code>int</code> or a <code>long</code> depending on the platform.</p>
<p>The type of the expression (<code>1 &lt;&lt; 16</code>) is determined by its integer-promoted left operand, which has type of int.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by whyglinux at Jun 14, 2009 08:57
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Took out the offending NCCE/CCE. It's not legit C anyway, as you can't define two <code>f</code> functions that take different argument types. The example lives on, however, in <a href="https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+DCL00-CPP.+Const-qualify+immutable+objects">VOID DCL00-CPP. Const-qualify immutable objects</a>.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Jun 15, 2009 09:36
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>What is the point of the exception (allowing inclusion guard macros)? It is meaningless to refer to const-qualifying a macro value.</p>
<p>Hmm... that suggests a new preprocessor recommendation: don't use #undef followed by #define to alter the value of a macro unless it is done at the top of the source file before the macro has been invoked.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by donbock at Feb 21, 2012 08:52
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Better noncompliant example here would be, ignoring const in below crc_table definition</p>
<pre><code>/* CRC table for the CRC-16. The poly is 0x8005 (x^16 + x^15 + x^2 + 1) */
UINT16 crc16_table[CRC_TABLE_SIZE] = 
 {
        0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
        0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
        0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
        0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
        0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
        0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
        0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
        0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
        0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
        0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
        0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
        0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
        0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
        0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
        0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
        0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
        0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
        0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
        0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
        0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
        0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
        0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
        0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
        0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
        0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
        0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
        0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
        0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
        0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
        0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
        0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
        0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040
 };</code></pre>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by mohandhan at Dec 30, 2012 23:10
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Looks like that was left over from an earlier version of the recommendation; I'm removing it.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Jan 02, 2013 15:29
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Nice page, thanks.</p>
<p>BTW, could you please shed some light on const * &lt;variable type&gt; and &lt;variable type&gt; * const?</p>
<p>Thanks</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dev at Sep 05, 2013 09:42
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p> Some example code to help:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb6" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb6-1"><a href="#cb6-1" aria-hidden="true" tabindex="-1"></a><span class="dt">const</span> foo <span class="op">*</span>var1<span class="op">;</span></span>
<span id="cb6-2"><a href="#cb6-2" aria-hidden="true" tabindex="-1"></a>foo <span class="dt">const</span> <span class="op">*</span> var2<span class="op">;</span></span>
<span id="cb6-3"><a href="#cb6-3" aria-hidden="true" tabindex="-1"></a>foo <span class="op">*</span> <span class="dt">const</span> var3<span class="op">;</span></span>
<span id="cb6-4"><a href="#cb6-4" aria-hidden="true" tabindex="-1"></a><span class="dt">const</span> foo <span class="op">*</span> <span class="dt">const</span> var4<span class="op">;</span></span></code></pre></div>
</div>
</div>
<p>var1 is a mutable pointer to a constant foo.<br />
var2 is a mutable pointer to a constant foo.<br />
var3 is a constant pointer to a mutable foo.<br />
var4 is a constant pointer to a constant foo.</p>
<p>If the pointer is const, then it means the pointer cannot be manipulated (think ++ or --).  If the object is const, then the object being pointed to cannot be manipulated.  Does that clear things up?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by aballman at Sep 05, 2013 17:35
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>If you're going to use <strong>const</strong> to declare a fixed constant then you should go all the way and use <strong>static const</strong>:</p>
<p>static const float pi = 3.14159f;</p>
<p>Advantages include:</p>
<ul>
<li>Variable is only initialized once at start-up, even if it is declared inside a function (save a tiny bit of run-time overhead).</li>
<li>Some (many) compilers will allocate the variable in read-only memory; thus, you get a run-time error via the MMU if you try to change the variable after casting away const-ness.</li>
</ul>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by donbock at Mar 31, 2015 05:20
</div></td>
</tr>
</tbody>
</table>
