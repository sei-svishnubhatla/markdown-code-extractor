Do not hard code the size of a type into an application. Because of alignment, padding, and differences in basic types (e.g., 32-bit versus 64-bit pointers), the size of most types can vary between compilers and even versions of the same compiler. Using the `sizeof` operator to determine sizes improves the clarity of what is meant and ensures that changes between compilers or versions will not affect the code.
Type alignment requirements can also affect the size of structures. For example, the size of the following structure is [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementationdefinedbehavior):
``` java
struct s {
  int i;
  double d;
};
```
Assuming 32-bit integers and 64-bit doubles, for example, the size can range from 12 to 16 bytes, depending on alignment rules.
## Noncompliant Code Example
This noncompliant code example attempts to declare a two-dimensional array of integers with variable length rows. On a platform with 64-bit integers, the loop will access memory outside the allocated memory section.
``` c
int f(void) { /* Assuming 32-bit pointer, 32-bit integer */
  size_t i;
  int **matrix = (int **)calloc(100, 4);
  if (matrix == NULL) {
    return -1; /* Indicate calloc() failure */
  }
  for (i = 0; i < 100; i++) {
    matrix[i] = (int *)calloc(i, 4);
    if (matrix[i] == NULL) {
      return -1; /* Indicate calloc() failure */
    }
  }
 return 0;
}
```
## Compliant Solution
This compliant solution replaces the hard-coded value `4` with `sizeof(int *)`:
``` c
int f(void) {
  size_t i;
  int **matrix = (int **)calloc(100, sizeof(*matrix));
  if (matrix == NULL) {
    return -1; /* Indicate calloc() failure */
  }
  for (i = 0; i < 100; i++) {
    matrix[i] = (int *)calloc(i, sizeof(**matrix));
    if (matrix[i] == NULL) {
      return -1; /* Indicate calloc() failure */
    }
  }
  return 0;
}
```
Also see [MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type](MEM02-C_%20Immediately%20cast%20the%20result%20of%20a%20memory%20allocation%20function%20call%20into%20a%20pointer%20to%20the%20allocated%20type) for a discussion on the use of the `sizeof` operator with memory allocation functions.
### Exceptions
**EXP09-C-EX1:** The C Standard explicitly declares `sizeof(char) == 1`, so any sizes based on characters or character arrays may be evaluated without using `sizeof`. This does not apply to `char*` or any other data types.
## Risk Assessment
Porting code with hard-coded sizes can result in a buffer overflow or related [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP09-C | High | Unlikely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | alloc-without-sizeof | Partially checked |
| Compass/ROSE |  |  | Can detect violations of this recommendation. In particular, it looks for the size argument of malloc(), calloc(), or realloc() and flags when it does not find a sizeof operator in the argument expression. It does not flag if the return value is assigned to a char *; in this case a string is being allocated, and sizeof is unnecessary because sizeof(char) == 1 |
| ECLAIR | 1.2 | CC2.EXP09 | Can detect violations of this recommendation. In particular, it considers when the size of a type is used by malloc(), calloc() or realloc() and flags these functions if either the size argument does not use a sizeof operator, or the size argument uses sizeof, but the type of the returned value is not a pointer to the type of the argument to sizeof. It does not flag if the returned value is assigned to a char * |
| LDRA tool suite | 9.7.1 | 201 S | Partially implemented |
| Polyspace Bug Finder | R2024a | CERT C: Rec. EXP09-C | Checks for hard-coded object size used to manipulate memory (rec. fully covered) |
| RuleChecker | 24.04 | alloc-without-sizeof | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP09-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP09-CPP. Use sizeof to determine the size of a type or variable |
| MITRE CWE | CWE-805, Buffer access with incorrect length value |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152126) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152207)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>I'm a big fan of getting *all* the size information from sizeof:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb1" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="dt">int</span> <span class="op">**</span>triarray <span class="op">=</span> <span class="fu">calloc</span><span class="op">(</span><span class="dv">100</span><span class="op">,</span> <span class="fu">sizeof</span><span class="op">(</span><span class="dt">int</span> <span class="op">*));</span> <span class="co">// ok</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a><span class="dt">int</span> <span class="op">**</span>triarray <span class="op">=</span> <span class="fu">calloc</span><span class="op">(</span><span class="dv">100</span><span class="op">,</span> <span class="fu">sizeof</span><span class="op">(*</span>triarray<span class="op">));</span> <span class="co">// better</span></span></code></pre></div>
</div>
</div>
<p>By extracting the type from the variable itself, it means that if the type is changed someday (say, to long**, then the allocation works automatically.<br />
</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by steve at Mar 13, 2008 22:16
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I use this a lot too, unless of course you get the number of '*'s wrong. <img src="images/icons/emoticons/sad.svg" /> For example in the above example instead of a sizeof *triarray, the common typo is sizeof triarray. In general, if possible, I tend to use the variable array initializers (GCC extension) instead of this to avoid typos.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by k0wsik at Mar 14, 2008 02:03
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>we should either implement this in the solution or add it as a sidebar</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jun 13, 2008 09:25
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>which part? do you want to go ahead and try to modify the rule?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Jun 13, 2008 14:10
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>the part about <code>sizeof(*matrix)</code> vs <code>sizeof(int*)</code>, i moved it into the code</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jun 13, 2008 14:18
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Why is one of the following approaches better than the other?</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb2" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a>matrix<span class="op">[</span>i<span class="op">]</span> <span class="op">=</span> <span class="op">(</span><span class="dt">int</span> <span class="op">*)</span><span class="fu">calloc</span><span class="op">(</span>i<span class="op">,</span> <span class="fu">sizeof</span><span class="op">(*</span>matrix<span class="op">[</span>i<span class="op">]));</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a>matrix<span class="op">[</span>i<span class="op">]</span> <span class="op">=</span> <span class="op">(</span><span class="dt">int</span> <span class="op">*)</span><span class="fu">calloc</span><span class="op">(</span>i<span class="op">,</span> <span class="fu">sizeof</span><span class="op">(**</span>matrix<span class="op">));</span></span></code></pre></div>
</div>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Jun 14, 2008 16:49
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>don't know if either is, but I wanted to remove the reference to <code>i</code> because it felt unnecessary... here's my reasoning: we're dealing with types, and <code>i</code> should have no effect on <code>**matrix</code>, it shouldn't matter which element we're dealing with, the type is inherent in the variable <code>matrix</code></p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by avolkovi at Jun 16, 2008 09:13
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I think we should provide an explicit exception to this recommendation in the case an array of char, signed char, or unsigned char is being allocated and sizeof is unnecessary because sizeof(char) == 1 as guaranteed by the standard.</p>
<p>Also, would rose flag the following code?</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb3" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb3-1"><a href="#cb3-1" aria-hidden="true" tabindex="-1"></a>size_t matrix_size <span class="op">=</span> <span class="fu">sizeof</span><span class="op">(</span><span class="fu">sizeof</span><span class="op">(**</span>matrix<span class="op">));</span></span>
<span id="cb3-2"><a href="#cb3-2" aria-hidden="true" tabindex="-1"></a>matrix<span class="op">[</span>i<span class="op">]</span> <span class="op">=</span> <span class="op">(</span><span class="dt">int</span> <span class="op">*)</span><span class="fu">calloc</span><span class="op">(</span>i<span class="op">,</span> matrix_size<span class="op">);</span></span></code></pre></div>
</div>
</div>
<p>If so, I think this should is a false positive.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs at Feb 09, 2009 11:06
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Rose already has an exception when it detects that space is being allocated for character arrays, but this rule does not discuss <code>sizeof(char) == 1</code>. Added this as an exception.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Feb 09, 2009 11:26
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I would like very much to have a Cert approved method to know at compile time, the sizeof a word, long, and long long, as well as the byte ordering for binary data stored in memory or on a file.   I need this as preprocessor information.</p>
<p>In searching through the GCC include file  &lt;limits.h&gt;, I came across  the #define  __WORDSIZE.  In Linux for Intel/AMD/Atom, this presents 64 or 32, corresponding to compiler.  The depending is if the compiler and library are for 32bits or for 64 bit architectures.</p>
<p>The code that I write is based on the same size variable, be it on a 32bit system or 64 bit system.  Here is a snippet of what I did.</p>
<p>My code has the following</p>
<p><br />
#ifndef  __WORDSIZE<br />
#include &lt;limits.h&gt;<br />
#endif</p>
<p>#if  __WORDSIZE == 64<br />
  typedef unsigned int uint32;<br />
#else<br />
  typedef unsigned long int uint32;<br />
#endif</p>
<p>My stored values are always 4 eight bit bytes in size.   By the way, a long long int in both cases appears to be 8 bytes.  The byte order is quire weird..</p>
<p> </p>
<p>I have not found a Standard define for littleEndian  BigEndian.  Intel for a the number (0x1234) in binary  stores the word as   byte zero  contains 0x12 byte one contains 0x34     <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=1234">1234</a></p>
<p>A long is stored in memory as nibble (half byte) positions as <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=12345678">12345678</a>   while a long long int is stored in successive nibbles as  <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=1234">12349abc 5678defg</a>   </p>
<p>ld like to have a recommandation as to library include file that I may use for both instances.</p>
<p>Leslie Satenstein </p>
<p><a href="mailto:lsatenstein@yahoo.com">lsatenstein@yahoo.com</a></p>
<p> </p>
<p> </p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by lsatenstein at Oct 09, 2012 13:07
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I only have a partial answer.</p>
<p>The CHAR_BIT values defined in &lt;limits.h&gt; defines the number of bits for smallest object that is not a bit-field (byte)</p>
<p>It is also defined by a constant expressions suitable for use in</p>
<p><strong>#if</strong></p>
<p>preprocessing directives.</p>
<p> </p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Oct 10, 2012 10:21
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Would this checker:</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |  |  |
| ----|----|----|----|
| PRQA QA·C | 8.1 | ; | Can detect for apparent null pointer operations. |</code></pre>
</div>
<p>be a better match for this rule:</p>
<p><a href="EXP34-C_%20Do%20not%20dereference%20null%20pointers">EXP34-C. Do not dereference null pointers</a> ?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Nov 08, 2012 09:15
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>sizeof(int *) can cause bugs when the programmer changes the declaration from int * to double * (as an example).  By using sizeof(*variable), the sizeof will always follow the correct type, presuming the programmer has the correct number of dereferences for what they're after.</p>
<p>That being said, sizeof(*some_ptr) can look terrifying because it <strong>looks</strong> like you are dereferencing a null pointer prior to the allocation happening.  So I can understand not wanting to use it.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by aballman at Sep 12, 2013 11:46
</div></td>
</tr>
</tbody>
</table>
