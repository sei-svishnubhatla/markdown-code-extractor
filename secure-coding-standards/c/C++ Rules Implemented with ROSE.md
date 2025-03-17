# C++ Rules Implemented in ROSE
## Current progress:
NO - 80
PARTIAL - 6
DONE - 15
Total: 101
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
<td class="confluenceTd"><p>PRE31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prefer inline functions to macros</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parentheses within macros around variable names</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Macro expansion must always be parenthesized</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare immutable values using const or enum</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL01-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not reuse variable names in sub-scopes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use visually distinct identifiers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Place const as the rightmost declaration specifier</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL04-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare no more than one variable per declaration</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure derived classes properly conform to an "is-a" relationship with their base classes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not use names reserved for the implementation</p></td>
<td class="confluenceTd"><p>Currently disabled due to difficulty of configuring rule for each platform.  Without configuration, many false positives.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid self initialization</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL32-C</p></td>
<td class="confluenceTd"><p> </p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Avoid runtime static initialization of objects with external linkage</p></td>
<td class="confluenceTd"><p>Currently disabled due to false positives on extern declarations that are not definitions.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not use C-style casts</p></td>
<td class="confluenceTd"><p>Currently disabled due to false positives.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>The second operands of the logical AND and OR operators should not contain side effects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not overload the logical AND and OR operators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not overload the &amp; operator</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not overload the comma operator</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid conversions using void pointers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP06-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parentheses for precedence of operation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Operands to the sizeof operator should not contain side effects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP08-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>A switch statement should have a default clause unless every enumeration value is tested</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP09-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Treat relational and equality operators as if they were nonassociative</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP10-A</p></td>
<td class="confluenceTd"><p> </p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Prefer the prefix forms of ++ and --<br />
</p></td>
<td class="confluenceTd"><p>Disabled, buggy.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not cast away const</p></td>
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
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not reference uninitialized variables</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not depend on order of evaluation between sequence points</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that the right hand operand of a shift operation is within range</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP36-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not cast or delete pointers to incomplete classes</p></td>
<td class="confluenceTd"><p>Disabled, buggy.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid side effects in assertions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP38-C</p></td>
<td class="confluenceTd"><p> </p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Avoid calling your own virtual functions in constructor and destructors<br />
</p></td>
<td class="confluenceTd"><p> </p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP39-C</p></td>
<td class="confluenceTd"><p> </p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Don't bitwise copy class objects<br />
</p></td>
<td class="confluenceTd"><p>Disabled, buggy.<br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the type of a bit-field when used in an expression</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use size_t for all integer values representing the size of an object</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Understand integer conversion rules</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use a secure integer library</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Enforce limits on integer values originating from untrusted sources</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not input integer values using formatted input</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT06-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use strtol() to convert a string token to an integer</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that integer conversions do not result in lost or misinterpreted data</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that integer operations do not result in an overflow</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that division and modulo operations do not result in divide-by-zero errors</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure integer values are within valid ranges</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT35-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not truncate the return value from a character input function</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Consider avoiding floating point numbers when precise computation is needed</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP30-C</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Take granularity into account when comparing floating point values</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use floating point variables as loop counters</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prevent domain errors in math functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid using the sizeof operator to determine the size of an array</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Guarantee that array indices are within the valid range</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use consistent array notation across all source files</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Create a copy constructor and assignment operator for non copyable objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not refer to an object outside of its lifetime</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not access deleted objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not delete this</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use invalid iterators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not dereference invalid pointers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use exception handling rather than error codes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Prefer special-purpose types for exceptions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Throw anonymous temporaries and catch by reference</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR30-C</p></td>
<td class="confluenceTd"><p><strong>RESERVED</strong><br />
</p></td>
<td class="confluenceTd"><p><strong>RESERVED</strong><br />
</p></td>
<td class="confluenceTd"><p><strong>RESERVED</strong></p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Destructors must be exception-safe</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Never allocate more than one resource in a single statement</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Perform every resource allocation in its own statement that immediately assigns the resource to an owning object</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use new and delete rather than raw memory allocation and deallocation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Object and array delete must be properly paired with the corresponding new</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES34-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Encapsulate resources that require paired acquire and release in objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES35-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Declare a copy constructor, a copy assignment operator, and a destructor in a class that manages resources</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES36-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that copy assignment operators do not damage an object that is copied to itself</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Release resources that require paired acquire and release in the object's destructor</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES38-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not leak resources when throwing exceptions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES39-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use longjmp</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Declare data members private</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Be careful with the definition of conversion operators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not hide inherited non-virtual member functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Prefer not to overload virtual functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Prefer not to give virtual functions default argument initializers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use pointer arithmetic polymorphically</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not treat arrays polymorphically</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that single-argument constructors are marked "explicit"</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not slice polymorphic objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure the proper destructor is called for polymorphic objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prefer basic_string to the use of null-terminated byte strings</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use the c_str() member to retrieve a const pointer to a null-terminated byte string</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not modify the null-terminated byte string returned by the c_str() member</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC32-C</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use the pointer value returned by c_str() after any subsequent call to a non-const member function</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use valid references, pointers, and iterators to reference string objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Range check element access</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTd"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not attempt to modify string literals</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Allocated adequate space when copying bounded strings</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Limit input when reading into a fixed length array</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTd"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STL30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use Valid Iterators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STL31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use Valid Iterator Ranges</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STL32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use a Valid Ordering Rule</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Prefer streams to C-style input output</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not make assumptions about open() and file creation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTh"><p>Rule</p></td>
<td class="confluenceTh"><p>Severity</p></td>
<td class="confluenceTh"><p>Progress</p></td>
<td class="confluenceTh"><p>Description</p></td>
<td class="confluenceTh"><p>Notes</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Compile cleanly at high warning levels</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Strive for Logical Completeness</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid errors of omission</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Avoid errors of addition</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use comments consistently and in a readable fashion</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Obey the One Definition Rule</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
</tbody>
</table>
