The [2009 CWE/SANS Top 25 Most Dangerous Programming Errors](http://cwe.mitre.org/top25/archive/2009/2009_cwe_sans_top25.html) is a list of the most significant programming errors that can lead to serious software vulnerabilities compiled by the SANS Institute, MITRE, and top software security experts in the US and Europe.
Existing CERT C guidelines reference relevant [Common Weakness Enumeration](http://cwe.mitre.org/) (CWE) IDs via
[labels](http://confluence.atlassian.com//display/DOC/Working+with%20Labels%20Overview)
. The tables on this page identify the appropriate secure coding guidelines for the C language that must be enforced to mitigate against each CWE in the Top 25 Most Dangerous Programming Errors. There are some cases where there are no corresponding guidelines, either because these CWEs address web development which is not in scope for any of the existing secure coding standards or address other elements of secure programming that cannot be adequately addressed by a secure coding standard.
### Insecure Interaction Between Components
These weaknesses are related to insecure ways in which data is sent and received between separate components, modules, programs, processes, threads, or systems.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-20: Improper Input Validation | 
                Page:        
                        API00-C. Functions should validate their parameters
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
                Page:        
                        ERR07-C. Prefer functions that support error checking over equivalent functions that don't
                Page:        
                        ERR34-C. Detect errors when converting a string to a number
                Page:        
                        MEM10-C. Define and use a pointer validation function
                Page:        
                        MSC24-C. Do not use deprecated or obsolescent functions
                Page:        
                        STR02-C. Sanitize data passed to complex subsystems
                Page:        
                        VOID FIO04-C. Detect and handle input and output errors
     |
| CWE-116: Improper Encoding or Escaping of Output | 
                Page:        
                        MSC09-C. Character encoding: Use subset of ASCII for safety
                Page:        
                        MSC10-C. Character encoding: UTF8-related issues
                Page:        
                        STR02-C. Sanitize data passed to complex subsystems
     |
| CWE-89: Failure to Preserve SQL Query Structure (aka 'SQL Injection') | 
        Content by label
        There is no content with the specified labels
     |
| CWE-79: Failure to Preserve Web Page Structure (aka 'Cross-site Scripting') | 
        Content by label
        There is no content with the specified labels
     |
| CWE-78: Failure to Preserve OS Command Structure (aka 'OS Command Injection') | 
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
                Page:        
                        ENV33-C. Do not call system()
                Page:        
                        STR02-C. Sanitize data passed to complex subsystems
     |
| CWE-319: Cleartext Transmission of Sensitive Information | 
        Content by label
        There is no content with the specified labels
     |
| CWE-352: Cross-Site Request Forgery (CSRF) | 
        Content by label
        There is no content with the specified labels
     |
| CWE-362: Race Condition | 
                Page:        
                        CON43-C. Do not allow data races in multithreaded code
                Page:        
                        FIO24-C. Do not open a file that is already open
                Page:        
                        POS01-C. Check for the existence of links when dealing with files
                Page:        
                        POS35-C. Avoid race conditions while checking for the existence of a symbolic link
                Page:        
                        POS38-C. Beware of race conditions when using fork and file descriptors
                Page:        
                        POS48-C. Do not unlock or destroy another POSIX thread's mutex
                Page:        
                        POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
                Page:        
                        VOID POS05-C. Avoid race conditions with multiple POSIX threads
     |
| CWE-209: Error Message Information Leak | 
                Page:        
                        MEM03-C. Clear sensitive information stored in reusable resources
     |

### Risky Resource Management
The weaknesses in this category are related to ways in which software does not properly manage the creation, usage, transfer, or destruction of important system resources.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-119: Failure to Constrain Operations within the Bounds of a Memory Buffer | 
                Page:        
                        ARR00-C. Understand how arrays work
                Page:        
                        ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
                Page:        
                        ENV01-C. Do not make assumptions about the size of an environment variable
                Page:        
                        EXP33-C. Do not read uninitialized memory
                Page:        
                        EXP39-C. Do not access a variable through a pointer of an incompatible type
                Page:        
                        FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
                Page:        
                        MSC24-C. Do not use deprecated or obsolescent functions
                Page:        
                        STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
                Page:        
                        STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
                Page:        
                        void ARR33-C. Guarantee that copies are made into storage of sufficient size
                Page:        
                        VOID ARR34-C. Ensure that array types in expressions are compatible
                Page:        
                        VOID Do not allow loops to iterate beyond the end of an array
                Page:        
                        void MEM09-C. Do not assume memory allocation functions initialize memory
                Page:        
                        void STR33-C. Size wide character strings correctly
     |
| CWE-642: External Control of Critical State Data | 
        Content by label
        There is no content with the specified labels
     |
| CWE-73: External Control of File Name or Path | 
                Page:        
                        FIO01-C. Be careful using functions that use file names for identification
                Page:        
                        FIO02-C. Canonicalize path names originating from tainted sources
                Page:        
                        MSC24-C. Do not use deprecated or obsolescent functions
     |
| CWE-426: Untrusted Search Path | 
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
     |
| CWE-94: Failure to Control Generation of Code (aka 'Code Injection') | 
        Content by label
        There is no content with the specified labels
     |
| CWE-494: Download of Code Without Integrity Check | 
        Content by label
        There is no content with the specified labels
     |
| CWE-404: Improper Resource Shutdown or Release | 
                Page:        
                        FIO22-C. Close files before spawning processes
                Page:        
                        MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
                Page:        
                        MEM11-C. Do not assume infinite heap space
     |
| CWE-665: Improper Initialization | 
                Page:        
                        ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
                Page:        
                        EXP33-C. Do not read uninitialized memory
                Page:        
                        void MEM09-C. Do not assume memory allocation functions initialize memory
     |
| CWE-682: Incorrect Calculation | 
                Page:        
                        FLP06-C. Convert integers to floating point for floating-point operations
                Page:        
                        FLP32-C. Prevent or detect domain and range errors in math functions
                Page:        
                        INT07-C. Use only explicitly signed or unsigned char type for numeric values
                Page:        
                        INT10-C. Do not assume a positive remainder when using the % operator
                Page:        
                        INT13-C. Use bitwise operators only on unsigned operands
     |

### Porous Defenses
The weaknesses in this category are related to defensive techniques that are often misused, abused, or just plain ignored.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-285: Improper Access Control (Authorization) | 
        Content by label
        There is no content with the specified labels
     |
| CWE-327: Use of a Broken or Risky Cryptographic Algorithm | 
                Page:        
                        MSC30-C. Do not use the rand() function for generating pseudorandom numbers
                Page:        
                        MSC32-C. Properly seed pseudorandom number generators
     |
| CWE-259: Hard-Coded Password | 
        Content by label
        There is no content with the specified labels
     |
| CWE-732: Insecure Permission Assignment for Critical Resource | 
                Page:        
                        FIO06-C. Create files with appropriate access permissions
     |
| CWE-330: Use of Insufficiently Random Values | 
                Page:        
                        MSC30-C. Do not use the rand() function for generating pseudorandom numbers
                Page:        
                        MSC32-C. Properly seed pseudorandom number generators
     |
| CWE-250: Execution with Unnecessary Privileges | 
                Page:        
                        POS02-C. Follow the principle of least privilege
                Page:        
                        POS36-C. Observe correct revocation order while relinquishing privileges
                Page:        
                        POS37-C. Ensure that privilege relinquishment is successful
     |
| CWE-602: Client-Side Enforcement of Server-Side Security | 
        Content by label
        There is no content with the specified labels
     |

## Other Languages
This page appears in the C++ Secure Coding Standard as [VOID 2009 CWE SANS Top 25 Most Dangerous Programming Errors](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+2009+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors).
## References
[2009 CWE/SANS Top 25 Most Dangerous Programming Errors](http://cwe.mitre.org/top25/archive/2009/2009_cwe_sans_top25.html)  
[Common Weakness Enumeration](http://cwe.mitre.org/)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>CWE-404: Improper Resource Shutdown or Release is also addressed by:</p>
<ol>
<li><a href="MEM00-C_%20Allocate%20and%20free%20memory%20in%20the%20same%20module,%20at%20the%20same%20level%20of%20abstraction">MEM00-C. Allocate and free memory in the same module, at the same level of abstraction</a></li>
<li><a href="MEM11-C_%20Do%20not%20assume%20infinite%20heap%20space">MEM11-C. Do not assume infinite heap space</a></li>
</ol>
<p>and perhaps also:</p>
<ol>
<li><a href="/confluence/pages/createpage.action?spaceKey=seccode&amp;title=MEM31-C.+Free+dynamically+allocated+memory+exactly+once">MEM31-C. Free dynamically allocated memory exactly once</a></li>
<li><a href="MEM34-C_%20Only%20free%20memory%20allocated%20dynamically">MEM34-C. Only free memory allocated dynamically</a></li>
<li><a href="MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object">MEM35-C. Allocate sufficient memory for an object</a></li>
</ol>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Jan 10, 2010 22:11
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>The 2010 version of the top 25 is currently under development. We may need to make a new page soon.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Jan 10, 2010 22:19
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I added <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=MEM31-C.+Free+dynamically+allocated+memory+exactly+once">MEM31-C. Free dynamically allocated memory exactly once</a> to the list.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Jan 10, 2010 22:24
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>That's pretty cool. The only thing I don't like is the "No content found for label(s) cwe-89." lines that exposes the mechanism into the interface. Is there anyway to default this text to something like "N/A"?</p>
<p>It would also be nice to use something like this for the tool pages such as <a href="https://www.securecoding.cert.org/confluence/display/seccode/CERT+C+Rules+implemented+in+the+LDRA+tool+suite">https://www.securecoding.cert.org/confluence/display/seccode/CERT+C+Rules+implemented+in+the+LDRA+tool+suite</a>, <a href="https://www.securecoding.cert.org/confluence/display/seccode/Klocwork+Cross+Reference">https://www.securecoding.cert.org/confluence/display/seccode/Klocwork+Cross+Reference</a>, and so forth where we would like to maintain the information on the individual pages and the collect them into summary tables. In these cases we would like the tables to have multiple columns of information though including (perhaps) the name of the checker, the degree to which the tool can discover violations of the guide line, and maybe notes. We have not yet come up with a good way of measuring "degree of support". Ideally, this would be a number produced from a conformance test for the analyzable C secure coding guidelines. Another possibility is that when we complete such a guideline, it will no longer be appropriate to provide such information here because these guidelines are targeted towards the developer and not the tools. On the other hand, these are the real set of guidelines that developers are concerned with, so it is useful for them to know where they can get help. OK, I'm done arguing with myself... comments?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Jan 31, 2010 08:26
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I'm also not crazy about the "No content found" but from user comments on the Confluence help page it doesn't look like it's easy to change. An Atlassian employee suggested editing <code>i18n.properties</code> for the key <code>macros.labelledcontent.no.content.found.for</code> and referred readers to a non-existent documentation page titled <strong>Editing Files within JAR Archives</strong>, and a user posted a piece of JavaScript code that apparently worked for them. I wasn't successful in getting it work but that could very well be because I don't know enough about the Wiki.</p>
<p>Thank you for pointing me to the <a href="void%20CERT%20C%20Rules%20implemented%20in%20the%20LDRA%20tool%20suite">void CERT C Rules implemented in the LDRA tool suite</a> and <a href="VOID%20Klocwork%20Cross%20Reference">VOID Klocwork Cross Reference</a> pages! They are another couple of handy references that I didn't know about, and as you suggest, the perfect candidates for using the {<code>contentbylabel</code>} macro. I'll see what can be done about them. Confluence has some other helpful macros that we might be able to use to generate these types of reports.</p>
<p>Another thing I'd like to do, besides using {<code>contentbylabel</code>} to generate the indices for each section (see my comment <a href="https://www.securecoding.cert.org/confluence/display/seccode/CERT+C+Secure+Coding+Standard?focusedCommentId=41059103#comment-41059103">Re: CERT C Secure Coding Standard</a>), is see if the <strong>Risk Assessment Summary</strong> tables for each section could be automatically generated from the synonymous section on the page for each guideline. The</p>
<p><a href="http://confluence.atlassian.com//display/DOC/Metadata%20Summary%20Macro">{metadatasummary}</a></p>
<p>macro looks promising.</p>
<p>For more sophisticated reports, there is the CustomWare <a href="http://www.customware.net/repository/display/AtlassianPlugins/Reporting+Plugin">Reporting Plugin</a>.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Jan 31, 2010 16:48
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>So the {<code>details</code>} and {<code>detailssummary</code>} macros don't appear to work quite the way I want them to. There appears to be no way to use Wiki formatting in the metadata (e.g., make L3 display in green) and the metadata is formatted as a block of text with one label/value pair per line.</p>
<p>E.g., with the following on one page:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb1" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a><span class="op">{</span>details<span class="op">:</span>label<span class="op">=</span>my_first_metadata_test<span class="op">}</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a><span class="bu">Severity</span><span class="op">:</span> low</span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>Likelihood<span class="op">:</span> unlikely</span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a>Remediation Cost<span class="op">:</span> medium</span>
<span id="cb1-5"><a href="#cb1-5" aria-hidden="true" tabindex="-1"></a>Priority<span class="op">:</span> P2</span>
<span id="cb1-6"><a href="#cb1-6" aria-hidden="true" tabindex="-1"></a><span class="bu">Level</span><span class="op">:</span> L3</span>
<span id="cb1-7"><a href="#cb1-7" aria-hidden="true" tabindex="-1"></a><span class="op">{</span>details<span class="op">}</span></span></code></pre></div>
</div>
</div>
<p>and this on another:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb2" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="op">{</span>detailssummary<span class="op">:</span>label<span class="op">=</span>my_first_metadata_test<span class="op">}</span></span></code></pre></div>
</div>
</div>
<p>will render like so on the first page:</p>
<blockquote>
<p>[!note]<br />
</p>
<p><strong>Severity:</strong> low<br />
<strong>Likelihood:</strong> unlikely<br />
<strong>Remediation Cost:</strong> medium<br />
<strong>Priority:</strong> P2<br />
<strong>Level:</strong> L3</p>
</blockquote>
<p>and like this on the other:</p>
<div class="table-wrap">
<pre class="table"><code>|   |  Severity  |  Likelihood  |  Remediation Cost  |  Priority  |  Level  |
| ----|----|----|----|----|----|
|  VOID 2009 CWE SANS Top 25 Most Dangerous Programming Errors  |  low  |  unlikely  |  medium  |  P2  |  L3  |</code></pre>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Jan 31, 2010 23:53
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Now that the 2010 Top 25 list is out all the CWE links above are broken...</p>
<p>I've fixed up the links in the table but the 2009 CWE/SANS Top 25 Most Dangerous Programming Errors link in the description now points at the 2010 list. Does SANS or MITRE maintain previous versions of the lists?</p>
<p>Btw., I think it would be useful to keep this page as is for historical reasons and add a new page for 2010 (rather than replacing it like SANS/MITRE did). Unless someone has a strong preference for the latter, I'll go ahead and add a new one sometime this week.</p>
<hr />
<p>I've added <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=2010+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors">2010 CWE SANS Top 25 Most Dangerous Programming Errors</a>.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Feb 17, 2010 23:34
</div></td>
</tr>
</tbody>
</table>
