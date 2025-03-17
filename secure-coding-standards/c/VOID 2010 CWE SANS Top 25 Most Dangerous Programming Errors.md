The [2010 CWE/SANS Top 25 Most Dangerous Programming Errors](http://cwe.mitre.org/top25/archive/2010/2010_cwe_sans_top25.html) is a list of the most significant programming errors that can lead to serious software vulnerabilities compiled by the SANS Institute, MITRE, and top software security experts in the US and Europe.
Existing CERT C guidelines reference relevant [Common Weakness Enumeration](http://cwe.mitre.org/) (CWE) IDs via
[labels](http://confluence.atlassian.com//display/DOC/Working+with%20Labels%20Overview)
. The tables on this page identify the appropriate secure coding guidelines for the C language that must be enforced to mitigate against each CWE in the Top 25 Most Dangerous Programming Errors. There are some cases where there are no corresponding guidelines, either because these CWEs address web development which is not in scope for any of the existing secure coding standards or address other elements of secure programming that cannot be adequately addressed by a secure coding standard.
### Insecure Interaction Between Components
These weaknesses are related to insecure ways in which data is sent and received between separate components, modules, programs, processes, threads, or systems.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-79: Failure to Preserve Web Page Structure ('Cross-site Scripting') | n/a |
| CWE-89: Failure to Preserve SQL Query Structure (aka 'SQL Injection') | n/a |
| CWE-352: Cross-Site Request Forgery (CSRF) | n/a |
| CWE-434: Unrestricted Upload of File with Dangerous Type | n/a |
| CWE-78: Failure to Preserve OS Command Structure (aka 'OS Command Injection') | 
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
                Page:        
                        ENV33-C. Do not call system()
                Page:        
                        STR02-C. Sanitize data passed to complex subsystems
     |
| CWE-209: Error Message Information Leak | 
                Page:        
                        MEM03-C. Clear sensitive information stored in reusable resources
     |
| CWE-601: URL Redirection to Untrusted Site ('Open Redirect') | n/a |
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

### Risky Resource Management
The weaknesses in this category are related to ways in which software does not properly manage the creation, usage, transfer, or destruction of important system resources.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | 
                Page:        
                        STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
                Page:        
                        VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array
     |
| CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 
                Page:        
                        FIO02-C. Canonicalize path names originating from tainted sources
     |
| CWE-98: Improper Control of Filename for Include/Require Statement in PHP Program ('PHP File Inclusion') | n/a |
| CWE-805: Buffer Access with Incorrect Length Value | 
                Page:        
                        ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
                Page:        
                        EXP09-C. Use sizeof to determine the size of a type or variable
                Page:        
                        void STR33-C. Size wide character strings correctly
     |
| CWE-754: Improper Check for Unusual or Exceptional Conditions | 
                Page:        
                        API04-C. Provide a consistent and usable error-checking mechanism
                Page:        
                        ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy
                Page:        
                        ERR07-C. Prefer functions that support error checking over equivalent functions that don't
                Page:        
                        EXP12-C. Do not ignore values returned by functions
                Page:        
                        void MEM32-C. Detect and handle memory allocation errors
     |
| CWE-129: Improper Validation of Array Index | 
                Page:        
                        ARR00-C. Understand how arrays work
                Page:        
                        ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
                Page:        
                        INT32-C. Ensure that operations on signed integers do not result in overflow
                Page:        
                        VOID Guarantee that array indices are within the valid range
     |
| CWE-190: Integer Overflow or Wraparound | 
                Page:        
                        INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
                Page:        
                        INT30-C. Ensure that unsigned integer operations do not wrap
                Page:        
                        INT32-C. Ensure that operations on signed integers do not result in overflow
                Page:        
                        MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap
                Page:        
                        MEM35-C. Allocate sufficient memory for an object
                Page:        
                        VOID. INT03-C. Use a secure integer library
     |
| CWE-131: Incorrect Calculation of Buffer Size | 
                Page:        
                        MEM35-C. Allocate sufficient memory for an object
     |
| CWE-494: Download of Code Without Integrity Check | n/a |
| CWE-770: Allocation of Resources Without Limits or Throttling | 
                Page:        
                        FIO22-C. Close files before spawning processes
     |

### Porous Defenses
The weaknesses in this category are related to defensive techniques that are often misused, abused, or just plain ignored.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-285: Improper Access Control (Authorization) | 
        Content by label
        There is no content with the specified labels
     |
| CWE-807: Reliance on Untrusted Inputs in a Security Decision | 
                Page:        
                        ENV01-C. Do not make assumptions about the size of an environment variable
                Page:        
                        ENV02-C. Beware of multiple environment variables with the same effective name
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
     |
| CWE-311: Missing Encryption of Sensitive Data | 
                Page:        
                        MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
                Page:        
                        WIN04-C. Consider encrypting function pointers
     |
| CWE-798: Use of Hard-coded Credentials | 
                Page:        
                        MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| CWE-306: Missing Authentication for Critical Function | n/a |
| CWE-732: Insecure Permission Assignment for Critical Resource | 
                Page:        
                        FIO06-C. Create files with appropriate access permissions
     |
| CWE-327: Use of a Broken or Risky Cryptographic Algorithm | 
                Page:        
                        MSC30-C. Do not use the rand() function for generating pseudorandom numbers
                Page:        
                        MSC32-C. Properly seed pseudorandom number generators
     |

## Other Languages
A mapping between the CERT C++ Secure Coding Standard and [VOID 2010 CWE SANS Top 25 Most Dangerous Programming Errors](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+2010+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors) is available.
A mapping between the CERT Sun Microsystems Secure Coding Standard for Java and [VOID Rule: 2010 CWE SANS Top 25 Most Dangerous Programming Errors](https://wiki.sei.cmu.edu/confluence/display/java/VOID+Rule%3A+2010+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors) is available.
## References
[2010 CWE/SANS Top 25 Most Dangerous Programming Errors](http://cwe.mitre.org/top25/archive/2010/2010_cwe_sans_top25.html)  
[Common Weakness Enumeration](http://cwe.mitre.org/)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>It is surprising to see these 3 notes:</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |  |  |
| ----|----|----|----|
|  CWE-129: Improper Validation of Array Index  | ; |  No content found for label(s) cwe-129.  | ; |
|  CWE-190: Integer Overflow or Wraparound  | ; |  No content found for label(s) cwe-190.  | ; |
|  CWE-131: Incorrect Calculation of Buffer Size  | ; |  No content found for label(s) cwe-131.  | ; |</code></pre>
</div>
<p>We need to determine which of the CSCG guidelines should apply to these CWG items.<br />
</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by tplum@plumhall.com at Feb 20, 2010 00:48
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Is it worthwhile to keep <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=FIO02-C.+Canonicalize+path+names+originating+from+untrusted+sources">FIO02-C. Canonicalize path names originating from untrusted sources</a>?</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dmohindr at Feb 20, 2010 14:39
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Yes. Creating a canonical name is the first step in determining if a file is in a secure directory.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Feb 20, 2010 14:49
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I've fixed these tags as well as some others. There is still some more work to be done.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Feb 20, 2010 14:51
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>CWE-807 could be mapped to every guideline that contains the phrase "untrusted sources" or perhaps a more narrow reading of CWE-807 would only encompass "environment variables".</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Feb 20, 2010 15:01
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I should have mentioned that I haven't gone through all the CWEs on this list to try to match them up to CERT guidelines. I did a few of them but it's slow going. In some cases a guideline doesn't seem to map cleanly to any one CWE, or its name and description map to one CWE but certain NCCE demonstrate another. For example:</p>
<p><a href="STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator">STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator</a> maps to fairly cleanly to <a href="http://cwe.mitre.org/data/definitions/119.html">CWE-119: Failure to Constrain Operations within the Bounds of a Memory Buffer</a> but the majority of the NCCEs in the guideline actually demonstrate the (closely related) <a href="http://cwe.mitre.org/data/definitions/120.html">CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')</a>.</p>
<p>There definitely is more work to be done.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Feb 20, 2010 16:35
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>I don't think this mapping will ever be perfect. For now, I've found applicable C guidelines for all the CWEs in the Top-25 or labeled them as n/a.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by rcs_mgr at Feb 20, 2010 19:41
</div></td>
</tr>
</tbody>
</table>
