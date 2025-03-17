> [!info]  
>
> This page has been labeled [void](https://confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This page has not been erased yet in case it contains information that might still be useful.


| Preprocessor Guideline | LDRA | Klockwork | Coverity Prevent | Fortify SCA | Compass ROSE |
| ----|----|----|----|----|----|
| PRE00-C. Prefer inline or static functions to function-like macros | ; | ; | ; | ; | ; |
| PRE01-C. Use parentheses within macros around parameter names | ; | ; | ; | ; | ; |
| PRE02-C. Macro replacement lists should be parenthesized | ; | ; | ; | ; | ; |
| VOID PRE03-C. Prefer typedefs to defines for encoding non-pointer types | ; | ; | ; | ; | ; |
| PRE04-C. Do not reuse a standard header file name | ; | ; | ; | ; | ; |
| PRE05-C. Understand macro replacement when concatenating tokens or performing stringification | ; | ; | ; | ; | ; |
| PRE06-C. Enclose header files in an include guard | ; | ; | ; | ; | ; |
| PRE07-C. Avoid using repeated question marks | ; | ; | ; | ; | ; |
| PRE08-C. Guarantee that header file names are unique | ; | ; | ; | ; | ; |
| PRE09-C. Do not replace secure functions with deprecated or obsolescent functions | ; | ; | ; | ; | ; |
| PRE10-C. Wrap multistatement macros in a do-while loop | ; | ; | ; | ; | ; |
| PRE11-C. Do not conclude macro definitions with a semicolon | ; | ; | ; | ; | ; |
| VOID Define numeric constants in a portable way | ; | ; | ; | ; | ; |


| Declarations and Initialization Guideline | LDRA | Klockwork | Coverity Prevent | Fortify SCA | Compass ROSE |
| ----|----|----|----|----|----|
| DCL00-C. Const-qualify immutable objects? | ; | ; | ; | ; | ; |
| DCL01-C. Do not reuse variable names in subscopes? | ; | ; | ; | ; | ; |
| DCL02-C. Use visually distinct identifiers? | ; | ; | ; | ; | ; |
| DCL03-C. Use a static assertion to test the value of a constant expression? | ; | ; | ; | ; | ; |
| DCL04-C. Do not declare more than one variable per declaration? | ; | ; | ; | ; | ; |
| DCL05-C. Use typedefs of non-pointer types only? | ; | ; | ; | ; | ; |
| DCL06-C. Use meaningful symbolic constants to represent literal values? | ; | ; | ; | ; | ; |
| DCL07-C. Include the appropriate type information in function declarators? | ; | ; | ; | ; | ; |
| DCL08-C. Properly encode relationships in constant definitions? | ; | ; | ; | ; | ; |
| DCL09-C. Declare functions that return errno with a return type of errno_t? | ; | ; | ; | ; | ; |
| DCL10-C. Maintain the contract between the writer and caller of variadic functions? | ; | ; | ; | ; | ; |
| DCL11-C. Understand the type issues associated with variadic functions? | ; | ; | ; | ; | ; |
| DCL12-C. Implement abstract data types using opaque types? | ; | ; | ; | ; | ; |
| DCL13-C. Declare function parameters that are pointers to values not changed by the function as const? | ; | ; | ; | ; | ; |
| DCL15-C. Declare file-scope objects or functions that do not need external linkage as static? | ; | ; | ; | ; | ; |
| DCL16-C. Use 'L', not 'l', to indicate a long value? | ; | ; | ; | ; | ; |

This information has been collected for:
-   Compass ROSE v 0.93a
-   Coverity Prevent
-   Fortify SCA Version 5.0 with the CERT C Rule Pack v 1.1
-   Gimpel Software PC-lint v 9.00
-   Klocwork Version 8.0.4.16
-   LDRA tool suite V 7.6.0
-   Splint Version 3.1.1
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=43319401) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Avoid+reopening+a+file+stream?showChildren=false&showComments=false)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>A 'legally binding' certification is tricky. Consider the case of a checker to prohibit use of the <code>gets()</code> function. This checker must do the following:</p>
<ol>
<li>tokenizing the program + grep yields no references to <code>gets()</code></li>
<li>No pointer arithmetic on function pointers (fp) <a href="ARR37-C_%20Do%20not%20add%20or%20subtract%20an%20integer%20to%20a%20pointer%20to%20a%20non-array%20object">ARR37-C. Do not add or subtract an integer to a pointer to a non-array object</a> and <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=ARR38-C.+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element">ARR38-C. Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element</a></li>
<li>No execution of a fp, unless that fp's value set is limited to a subset of valid fn's.</li>
<li>No undefined behavior (similar to <a href="MSC15-C_%20Do%20not%20depend%20on%20undefined%20behavior">MSC15-C. Do not depend on undefined behavior</a></li>
<li>No code-execution vuls; a vul could cause shellcode to run <code>gets()</code></li>
</ol>
<p>The first item is possible, the second is also possible, but seems unrelated, as it deals with a separate rule. The last several are impossible, or at least severely difficult.</p>
<p>It is probably worthwhile to enforce just point 1 above, and ignore the others (dealing with some other other points in other checkers). CERT could certify a Compass/ROSE checker that enforced the first item, while ingoring the others.</p>
<p>A second complication is the tool checkers themselves. CERT should never certify a Fortify/SCA rule, as we do not have access to the Fortify source code. Legal responsibility for certification of Fortify checkers should rest with Fortify, not with CERT. Likewise, LDRA should certify their own checkers, and so on.</p>
<p>Finally, forbidding <code>gets()</code> is not a rule by itself, but is part of a bigger rule: <a href="/confluence/pages/createpage.action?spaceKey=c&amp;title=STR35-C.+Do+not+copy+data+from+an+unbounded+source+to+a+fixed-length+array">STR35-C. Do not copy data from an unbounded source to a fixed-length array</a>. Ensuring code does not call <code>gets()</code> is insufficient for enforcing this rule.</p>
<p>When considering the effectiveness of a checker when applying it to sourcecode, we should ask ourselves two questions:</p>
<ul>
<li>Does the checker catch all violations of the rule? If not, the checker permits 'false negatives'; that is code that violates the rule, but escapes detection.</li>
<li>Does the checker flag as violation code that in fact does not violate t he rule. If so, the checker permits 'false positives', that is, code that abides by the rule, but appears flawed.</li>
</ul>
<p>The answers to these questions yields four states:</p>
<div class="table-wrap">
<pre class="table"><code>|  |  |  |
| ----|----|----|
|  False Negative  |  No  |  Yes  |
|  False Positive  | ; | ; |
|  No  |  perfect  |  incomplete  |
|  Yes  |  inconsistent  |  inconsistent &amp; incomplete  |</code></pre>
</div>
<p>So to restate our above items:</p>
<p>A checker that prohibits any execution of the gets() function would be<br />
incomplete; as a sufficiently skilled programmer could use gets() via<br />
pointer arithmetic or other sufficiently advanced techniques to foil<br />
our checker. A checker that prohibits references to gets() in the<br />
tokenized program would be perfect; as it could catch all such<br />
references while not flagging any false positives. And finally, a<br />
checker that enforces [STR35-C. Do not copy data from an unbounded<br />
source to a fixed-length array] would probably be incomplete, as only<br />
the <code>gets()</code> usage is easy to catch.</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by svoboda at Dec 17, 2008 16:29
</div></td>
</tr>
</tbody>
</table>
