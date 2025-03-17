# C Rules Implemented in Fortify SCA
The [CERT C Rule Pack](/confluence/download/attachments/87152344/CSCS-C.xml?version=1&modificationDate=1206464223000&api=v2) for Fortify SCA is available for general use. The CERT C Rule Pack has been tested with Fortify SCA version 4.5 and version 5.0
## Current progress:
NO - 57
PARTIAL - 14
DONE - 27
FORTIFY - 16
Complete : 113 of 180
<table class="confluenceTable">
<colgroup>
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
<col style="width: 20%" />
</colgroup>
<tbody>
<tr>
<th class="confluenceTh"><p>Rule</p></th>
<th class="confluenceTh"><p>Severity</p></th>
<th class="confluenceTh"><p>Progress</p></th>
<th class="confluenceTh"><p>Description</p></th>
<th class="confluenceTh"><p>Notes</p></th>
</tr>
&#10;<tr>
<td class="confluenceTd"><p><strong>01. PRE</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prefer inline functions to macros</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE01-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parentheses within macros around variable names</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE02-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Macro expansion should always be parenthesized for function-like macros</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE03-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid invoking a macro when trying to invoke a function</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE04-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not reuse a standard header file name</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parenthesis around any macro definition containing operators</p></td>
<td class="confluenceTd"><p>Fortify can not detect this, code is analyzed after preprocessing. -Taschner 10/12</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE06-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Enclose header file in an inclusion sandwich</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not create a universal character name through concatenation</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Never invoke an unsafe macro with arguments containing assignment, increment, decrement, or function call</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>02. DCL</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Declare immutable values using const or enum</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL01-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not reuse variable names in sub-scopes</p></td>
<td class="confluenceTd"><p>Fortify can not compair contents of two different scopes. -Taschner 10/12</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL02-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use visually distinct identifiers</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL03-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Place const as the rightmost declaration specifier</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL04-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Take care when declaring more than one variable per declaration</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use typedefs to improve code readability</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL06-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use meaningful symbolic constants to represent literal values in program logic</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Include type information in function declarators</p></td>
<td class="confluenceTd"><p>I can't get any of these code examples to compile - these recommendations look like they're already taken care of by compiler?? -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL08-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare function pointers using compatible types</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL09-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare functions that return an errno with a return type of errno_t</p></td>
<td class="confluenceTd"><p>Fortify can not detect the return value of a function. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL10-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Take care when using variadic functions</p></td>
<td class="confluenceTd"><p>Having trouble writing structural rule, requested help. -Taschner 10/16<br />
It's not possible as "insert (loc+, ..)" is translated to two sequence points "loc_0 = loc+; insert(loc_0, ...)". -Ning 10/22</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL11-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand the type issues associated with variadic functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL12-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Create and use abstract data types</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY PARTIAL</p></td>
<td class="confluenceTd"><p>Declare objects with appropriate storage durations</p></td>
<td class="confluenceTd"><p>Fortify catches the case of declaring an array and then returning a pointer to that array within a function. Can't do any more with Fortify. -Taschner 9/17</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL31-C</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Guarantee identifiers are unique</p></td>
<td class="confluenceTd"><p>Fortify does not have a mechanism to deal with this issue properly. -Taschner 11/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL33-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that source and destination pointers in function arguments do not point to overlapping objects if they are restrict qualified</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use volatile for data that cannot be cached</p></td>
<td class="confluenceTd"><p>Not sure how to check for this - I don't think Fortify can do this. Asked Chad for help. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL35-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Do not convert a function pointer to a function of an incompatible type</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL36-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use identifiers with different linked classifications</p></td>
<td class="confluenceTd"><p>You wont be able to find this kind of thing with the structural analyzer. Currently, our frontend tries to resolve multiple definitions as well as it can and then presents a consistent view to the analyzers, so a structural rule doesn't even see the multiple definitions. -Kannan Goundan</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>03. EXP</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parentheses for precedence of operation</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP01-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not take the sizeof a pointer to determine the size of a type</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-proccessed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP02-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>The second operands of the logical AND and OR operators should not contain side effects</p></td>
<td class="confluenceTd"><p>Can not flag on "&amp;&amp;" - need to request help from Fortify. -Taschner 10/18<br />
Because our front-end translate the<br />
if ( a &amp;&amp; b) ... to if (a)<br />
</p>
<div class="error">
Unknown macro: { if (b) ... }
</div>
<p><br />
and '(i++) == max' is translated to 'tmp = i; i = i + 1; tmp == max'<br />
In order to handle this case, we need to reverse the translation which we cannot now. -Ning 10/24</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP03-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not assume the size of a structure is the sum of the of the sizes of its members</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-proccessed out before Fortify can analyze the code. -Taschner 10/24</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP04-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not perform byte-by-byte comparisons between structures</p></td>
<td class="confluenceTd"><p>Can create a semantic rule to flag on memcmp, but can't flag structs being passed that fn. -Taschner 10/25</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not cast away a const qualification</p></td>
<td class="confluenceTd"><p>Can not flag on "const". -Taschner 10/25</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP06-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Operands to the sizeof operator should not contain side effects</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use caution with NULL and 0, especially concerning pointers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP08-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure pointer arithmetic is used correctly</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/25</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP09-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use sizeof to determine the size of a type or variable</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP10-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not diminish the benefits of constants by assuming their values in expressions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP30-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not depend on order of evaluation between sequence points</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not modify constant values</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not access a volatile object through a non-volatile reference</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY<br />
PARTIAL</p></td>
<td class="confluenceTd"><p>Do not reference uninitialized variables</p></td>
<td class="confluenceTd"><p>This catches the example code, but doesn't always recognize initialization. If initialization done in another function it is not recognized. Weirdness occurs when pointers used as well. Lots of false positives. Fortify catches as "low : Uninitialized Variable : controlflow" -Taschner 10/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Ensure a pointer is valid before dereferencing it</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP35-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not access or modify the result of a function call after a subsequent sequence point</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP36-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not cast between pointers to objects or types with differing alignments</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Call functions with the correct arguments</p></td>
<td class="confluenceTd"><p>Structural Rule language does not support the predicate required to detect the function call violation because it requires the universal quantifier "forall" which we don't support at this moment. -Ning Wang (Fortify)</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>04. INT</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand the data model used by your implementation(s)</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT01-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Use size_t for all integer values representing the size of an object</p></td>
<td class="confluenceTd"><p>This is partially covered by the rule for INT32-C - but Fortify can't flag on type size_t, Fortify sees size_t as unsigned long. -Taschner 10/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT02-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand integer conversion rules</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT03-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use a secure integer library</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT04-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Enforce limits on integer values originating from untrusted sources</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT05-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use functions that input character data and convert the data if these functions cannot handle all possible inputs</p></td>
<td class="confluenceTd"><p>This is covered by FIO33-C. -Taschner 10/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT06-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use strtol() to convert a string token to an integer</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag atoi, atol, and atoll when they're passed strings. -Taschner 10/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT07-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Explicitly specify signed or unsigned for character types</p></td>
<td class="confluenceTd"><p>Created structural rule to check if int is assigned a char (not unsigned or signed char) or if an operation is done with a char. -Taschner 10/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT08-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Verify that all integer values are in range</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT09-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure enumeration constants map to unique values</p></td>
<td class="confluenceTd"><p>Can't flag on enum. -Taschner 10/29</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT10-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the sign of the resulting value from the remainder % operator</p></td>
<td class="confluenceTd"><p>Created a structural rule that flags on %. -Taschner 10/29</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT11-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not depend upon the allocation order of bit-fields within a word</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT12-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the type of a bit-field when used in an expression</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT13-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not assume that a right shift operation is implemented as a logical or an arithmetic shift</p></td>
<td class="confluenceTd"><p>Able to create a structural rule to flag when a right shift operation is performed. -Taschner 10/30</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT14-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Distinguish bitmaps from numeric types</p></td>
<td class="confluenceTd"><p>Able to create a structural rule to match when an arithmetic operation is preformed in the same line as a bit manipulation operation. Not able to distiguish between operations on positive numbers and operations on negative numbers. -Taschner 10/30</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT15-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when converting from pointer to integer or integer to pointer</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not perform certain operations on questionably signed results</p></td>
<td class="confluenceTd"><p>There is a lot involved in finding these types of issues, but I believe your specific question involved determining the size of a type. Currently, there's no way to do that, but in SCA 5.0 the structural analyzer's "Type" objects will have a "storageSize" property that gives you the number of bytes the type occupies. One deficiency is that, if you have the Type object for "MyStruct*" you'll be able to determine the size of "MyStruct*", but you can't just "remove the pointer" and then get the size of "MyStruct". To do that, we'd have to enhance our "Type" object to be a tree structure -Kannan Goundan</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that integer conversions do not result in lost or misinterpreted data</p></td>
<td class="confluenceTd"><p>Able to create a structural rule that looks for type conversion without checking the variable on the left hand side of the assignment. -Taschner 10/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that integer operations do not result in an overflow</p></td>
<td class="confluenceTd"><p>Able to create a structural rule that tests to see if the affected operations are being preformed and there is no "if" statement. -Taschner 10/10<br />
 Further testing revealed tons of false positives, most of which related to for loops.  Added a check to flag only if it's not part of a for loop statement.  Not sure that this is entirely the right thing to do.  -Taschner 12/13<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that division and modulo operations do not result in divide-by-zero errors</p></td>
<td class="confluenceTd"><p>Created rule similar to INT32-C. -Taschner 10/10</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT34-C</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Upcast integers before comparing or assigning to a larger integer size</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT36-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not shift a negative number of bits or more bits than exist in the operand</p></td>
<td class="confluenceTd"><p>Covered by rule for INT32-C. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Arguments to character handling functions must be representable as an unsigned char</p></td>
<td class="confluenceTd"><p>Wrote a structural rule to flag when a char handling fn from ctype.h is passed anything but an unsigned char. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>05. FLP</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Consider avoiding floating point numbers when precise computation is needed</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP01-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care in rearranging floating point expressions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Take granularity into account when comparing floating point values</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when an if statement consists of two floats being compaired in the form "f == g". -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not call functions expecting real values with complex values</p></td>
<td class="confluenceTd"><p>2 Structural rules written, one to catch floats being passed to the list of functions detailed in this rule and one to catch any time a function is passed a variable with a type different than what the function expects. -Taschner 9/18<br />
<br />
Take a look at C99 Section 7.22 Type-generic math tgmath.h I think the issue is that the math.h and complex.h functions define type-generic macros. Use of the macro invokes a function whose corresponding real type and type domain are determined by the arguments for the generic parameters. If the type of the argument is not compatible with the type of the parameter for the selected function, the behavior is undefined. I think you are going to need to delve into this deeper, as there are a bunch of rules about what gets called. -RCS 9/18<br />
<br />
Upon closer inspection, Fortify won't flag on any of these functions - possibly they're processed out before Fortify sees them<img src="images/icons/emoticons/help_16.png" /><br />
. There is still no example code with the rule, and that should be remedied. -Taschner 11/9</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP32-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Prevent domain errors in math functions</p></td>
<td class="confluenceTd"><p>Created a control flow rule to handle this. -Taschner 10/11</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Convert integers to floating point for floating point operations</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when an assignment statement for a variable of type double or float that contains an operation that does not result in either a double or a float. Fortify incorrectly flags the first compliant code solution with the rule written. I think this is a bug in fortify, but may be a problem with my code, requested help from Ning. -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP34-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that demoted floating point values are within range</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when a double or long double is demoted to float or when a long double is demoted to float and there is not if block to check to make sure the larger variable doesn't contain a value that the smaller can't contain. -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>06. ARR</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Be careful using the sizeof operator to determine the size of an array</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Guarantee that array indices are within the valid range</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use consistent array notation across all source files</p></td>
<td class="confluenceTd"><p>Can't do this for the same reason we can't do DCL36-C. -Kannan Goundan</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure size arguments for variable length arrays are in a valid range</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when an array is dynamically allocated and the value is not properly checked. This will flag on the example compliant code as Fortify can't see outside of a single function's scope. -Taschner 11/8<br />
This rule generates too many false positives - Fortify can't explicitly detect arrays (verses references to other types of pointers), and this rule ends up flagging on tons of things that don't fall into the rule. -Taschner 12/12</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Guarantee that copies are made into storage of sufficient size</p></td>
<td class="confluenceTd"><p>At least catches the code in the NCCE. -crd 2007-09-24</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that array types in expressions are compatible</p></td>
<td class="confluenceTd"><p>I can't get Fortify to flag on the array access/assignments nor identify the differences in the types in the example code. -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>07. STR</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use TR 24731 for remediation of existing string manipulation code</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR01-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use managed strings for development of new string manipulation code</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR02-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Sanitize data passed to complex subsystems</p></td>
<td class="confluenceTd"><p>Fortify flags the example code as - "[1E605754626A177B9721905D023B495E : medium : Command Injection : semantic ]". -Taschner 10/31</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR03-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not inadvertently truncate a null-terminated byte string</p></td>
<td class="confluenceTd"><p>Created a control flow rule to flag when strncpy, strncat, fgets, or snprintf are called and the result is used without a test. -Taschner 10/31</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prefer making string literals const-qualified</p></td>
<td class="confluenceTd"><p>Fortify can not distinguish between "char" and "char const". -Taschner 11/1</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR06-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Don't assume that strtok() leaves its string argument unchanged</p></td>
<td class="confluenceTd"><p>Fortify catches this with [CDFD0C4C211178014C47940B7C19EA30 : medium : Missing Check against Null : controlflow ] and [2F6C99890155DBEB91367CA22A5D7E74 : low : Obsolete : semantic ]. -Taschner 10/30</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Use plain char for character data</p></td>
<td class="confluenceTd"><p>Attempted to write a structural rule to flag when a signed char contains something other than something with double qoutes - got errors from Fortify. Requested help. -Taschner 11/1<br />
Ning suggested I try using StringLiteral - this worked - Created a structural rule to flag when an unsigned char is assigned a StringLiteral. Only a partial fix - as Fortify can't tell the difference between char and signed char. -Taschner 11/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not attempt to modify string literals</p></td>
<td class="confluenceTd"><p>Not currently possible in Fortify.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Guarantee that storage for strings has sufficient space for character data and the null terminator</p></td>
<td class="confluenceTd"><p>Fortify flags the strcpy and the getenv example code with " high : Buffer Overflow : dataflow ", the first bit of example code Fortify can't deal with since it uses sizeof. -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Guarantee that all byte strings are null-terminated</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Size wide character strings correctly</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>STR34-C. Cast characters to unsigned types before converting to larger integer sizes</p></td>
<td class="confluenceTd"><p>Created a structrual rule to flag when an int or long is assigned a char. -Taschner 11/6</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>08. MEM</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Allocate and free memory in the same module, at the same level of abstraction</p></td>
<td class="confluenceTd"><p>Created a control flow rule to catch fns that have just malloc or just free. -Taschner 11/1</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM01-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Set pointers to dynamically allocated memory to NULL after they are released</p></td>
<td class="confluenceTd"><p>Attempted to write a control flow rule to flag if a pointer isn't freed by the end of the fn - haven't sorted out the logic and not sure if Fortify can do this. Will get back to it later. -Taschner 11/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM02-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not cast the return value from malloc()</p></td>
<td class="confluenceTd"><p>Created structural rule to flag a variable assignment when the return value of malloc's type doesn't match the type being assigned. -Taschner 11/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM03-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Clear sensitive information stored in dynamic memory prior to deallocation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM04-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the result of allocating 0 bytes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid large stack allocations</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM06-A</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM07-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Ensure that size arguments to calloc() do not result in an integer overflow</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Do not access freed memory</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Free dynamically allocated memory exactly once</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Detect and handle critical memory allocation errors</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use flexible array members for dynamically sized structures</p></td>
<td class="confluenceTd"><p>Fortify can't flag on array declarations inside a struct. -Taschner 11/9</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM34-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Only free memory allocated dynamically</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MEM35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Allocate sufficient memory for an object</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when malloc, calloc, or realloc are called and multsize_t is not or when memcpy is called with a length value other than size_t. Fortify can't flag on sizeof, so won't catch the third non-compliant example. -Taschner 11/9</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>09. FIO</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when creating format strings</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO01-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer functions that do not rely on file names for identification</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO02-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Canonicalize file names originating from untrusted sources</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO03-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not make assumptions about fopen() and file creation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO04-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Detect and handle input and output errors</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO05-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Identify files using multiple file attributes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO06-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Create files with appropriate access permissions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer fseek() to rewind()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO08-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when calling remove() on an open file</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO09-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>fflush() should be called after writing to an output stream if data integrity is important</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO10-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when using the rename() function</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO11-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when specifying the mode parameter of fopen()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO12-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer setvbuf() to setbuf()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO13-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Take care when using ungetc()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO14-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand the difference between text mode and binary mode with file streams</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Exclude user input from format strings</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO31-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not simultaneously open the same file multiple times</p></td>
<td class="confluenceTd"><p>Fortify can not detect this. -Taschner 11/7</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO32-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Detect and handle file operation errors</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Detect and handle input output errors resulting in undefined behavior</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use int to capture the return value of character IO functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use feof() and ferror() to detect end-of-file and file errors</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO36-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not assume a newline character is read when using fgets()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO37-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Don't assume character data has been read</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO38-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not use a copy of a FILE object for input and output</p></td>
<td class="confluenceTd"><p>Pointer weirdness leads to false negatives. Requested more help. -Taschner 9/17</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO39-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not read in from a stream directly following output to that stream</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO40-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Reset strings on fgets() failure</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO41-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not call getc() or putc() with parameters that have side effects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO42-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure files are properly closed when they are no longer needed</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO43-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY *PARTIAL*</p></td>
<td class="confluenceTd"><p>Do not copy data from an unbounded source to a fixed-length array</p></td>
<td class="confluenceTd"><p>Fortify catches the gets() and scanf(), but not the getchar() example. Not sure how to do the getchar() example at this time. -Taschner (9/14)</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO44-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Only use values for fsetpos() that are returned from fgetpos()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO45-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not reopen a file stream</p></td>
<td class="confluenceTd"><p>Attempted a control flow rule, but this can't be done because it requires a larger scope than Fortify can deal with. -Taschner</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>10. TMP</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>TMP00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not create temporary files in shared directories</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>TMP30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Temporary files must created with unique and unpredictable file names</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>TMP31-C</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>TMP32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Temporary files must be opened with exclusive access</p></td>
<td class="confluenceTd"><p>Fortify catches this with "Insecure Temporary File", a semantic rule of low severity. However, it also catches our advised compliant solution (mkstemp) with "Insecure Temporary File".</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>TMP33-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Temporary files must be removed before the program exits</p></td>
<td class="confluenceTd"><p>Created a control flow rule to flag when tmpfile, fopen, mktemp, etc are called rather than tmpfile_s or mkstemp. -Taschner 11/7</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>11. ENV</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV00-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not store the pointer to the string returned by getenv()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV01-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the size of an environment variable</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV02-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Beware of multiple environment variables with the same name</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV03-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Sanitize the environment before invoking external programs</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV04-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not call system() if you do not need a command interpreter</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not modify the string returned by getenv()</p></td>
<td class="confluenceTd"><p>Check for completion. -crd 2007-09-25 </p>
<blockquote>
&#10;</blockquote>
I talked to one of the analyzer guys and it is not possible to match what you are looking for in the current version of SCA. However, we hope to add the functionality to the next version (5.1).  Currently "env[0]" is translated to be "(* env) [0]" and we will update the analyzer to ignore the array indices. -Joy Forsythe (Fortify) 2008-02-29<br />
<br />
</td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not rely on an environment pointer following an operation that may invalidate it</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not call the exit() function more than once</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ENV33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not call the longjmp function to terminate a call to a function registered by atexit()</p></td>
<td class="confluenceTd"><p>Fortify can't flag this - it's a scope issue (Fortify can't compair the contents of two different scopes. -Taschner</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>12. SIG</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid using the same handler for multiple signals</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG01-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand implementation-specific details regarding signal handler persistence</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Only call asynchronous-safe functions within signal handlers</p></td>
<td class="confluenceTd"><p>Can't detect signal handlers in Fortify</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not access or modify shared objects in signal handlers</p></td>
<td class="confluenceTd"><p>Can't detect signal handlers in Fortify</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not call longjmp() from inside a signal handler</p></td>
<td class="confluenceTd"><p>Can't detect signal handlers in Fortify</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>SIG33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not recursively invoke the raise() function</p></td>
<td class="confluenceTd"><p>Can't detect signal handlers in Fortify</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>13. MSC</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC00-A</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Compile cleanly at high warning levels</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC01-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Strive for logical completeness</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC02-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid errors of omission</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC03-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid errors of addition</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC04-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use comments consistently and in a readable fashion</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC05-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not manipulate time_t typed values directly</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC06-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Be aware of insecure compiler optimization when dealing with sensitive data</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Detect and remove dead code</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC08-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Library functions should validate their parameters</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC09-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Character Encoding - Use Subset of ASCII for Safety</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC10-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Character Encoding - UTF8 Related Issues</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC11-A</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p>RESERVED</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC12-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Detect and remove code that has no effect</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC13-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Detect and remove unused values</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use the rand function</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that return values are compared against the proper type</p></td>
<td class="confluenceTd"><p>Fortify can't distiguish between time_t and long or size_t and unsigned long. -Taschner 11/8</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p><strong>50. POS</strong></p></td>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS00-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid race conditions with multiple threads</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS01-A</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Check for the existence of links</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use the readlink() function properly</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-proccessed out before Fortify can analyze the code. -Taschner 11/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS31-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not unlock or destroy another thread's mutex</p></td>
<td class="confluenceTd"><p>Created a control flow rule to flag when a function destroys a lock before acquiring that lock. -Taschner 11/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS32-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Include a mutex when using bit-fields in a multi-threaded environment</p></td>
<td class="confluenceTd"><p>Fortify can't flag on this - there's a scope issue and a preprocessing issue here. -Taschner 11/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Do not use vfork()</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>POS34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not call putenv() with an automatic variable as the argument</p></td>
<td class="confluenceTd"><p>Created a Fortify structural rule to flag when putenv is called with a variable that is not static. -Taschner 11/8</p></td>
</tr>
</tbody>
</table>
## Attachments:
![](images/icons/bullet_blue.gif) [CSCS-C.xml](attachments/87152344/88040194.xml) (text/xml)  
