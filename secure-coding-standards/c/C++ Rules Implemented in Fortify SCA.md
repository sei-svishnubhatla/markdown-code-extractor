# C++ Rules Implemented in Fortify SCA
The [CERT C++ Rule Pack](attachments/87152131/88040193.xml) for Fortify SCA is available for general use. The CERT C++ Rule Pack has been tested with Fortify SCA version 4.5 and version 5.0
## Current progress:
NO - 35
PARTIAL - 5
DONE - 17
FORTIFY - 6
Complete : 63 of 99
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
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use parentheses within macros around variable names</p></td>
<td class="confluenceTd"><p>Fortify analyzes code after preprocessing is done.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>PRE33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Macro expansion must always be parenthesized</p></td>
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
<td class="confluenceTd"><p>DCL00-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
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
<td class="confluenceTd"><p>Fortify is not able to deal with scope issues. -Taschner 10/15</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use visually distinct identifiers</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/19</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Place const as the rightmost declaration specifier</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/19</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL04-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare no more than one variable per declaration</p></td>
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/19</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Ensure derived classes properly conform to an "is-a" relationship with their base classes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use names reserved for the implementation</p></td>
<td class="confluenceTd"><p>Created a structural rule to catch variables named with two underscores or that begin with an underscore followed by a capital letter. -Taschner 9/28</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DCL31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Avoid self initialization</p></td>
<td class="confluenceTd"><p>Fortify flags this as "Poor Style : Redundant Initialization : structural". -Taschner 11/15<br />
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not use C-style casts</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>The second operands of the logical AND and OR operators should not contain side effects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not overload the logical AND and OR operators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not overload the &amp; operator</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not overload the comma operator</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
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
<td class="confluenceTd"><p>This can be done with a simple "grep", Fortify doesn't seem to have anything built in to do this. -Taschner 10/19</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP07-A</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Operands to the sizeof operator should not contain side effects</p></td>
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP08-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>A switch statement should have a default clause unless every enumeration value is tested</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP09-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Treat relational and equality operators as if they were nonassociative</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not cast away const</p></td>
<td class="confluenceTd"><p>Fortify can not distinguish weather a variable is const or not. -Taschner 10/1</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not modify constant values</p></td>
<td class="confluenceTd"><p>Same as C rule</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not access a volatile object through a non-volatile reference</p></td>
<td class="confluenceTd"><p>Same as C rule</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY *PARTIAL*</p></td>
<td class="confluenceTd"><p>Do not reference uninitialized variables</p></td>
<td class="confluenceTd"><p>Same as C rule, This catches the example code, but doesn't always recognize initialization. If initialization done in another function it is not recognized. Weirdness occurs when pointers used as well. Lots of false positives. Fortify catches as "low : Uninitialized Variable : controlflow" -Taschner 10/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not depend on order of evaluation between sequence points</p></td>
<td class="confluenceTd"><p>Same as EXP30-C C rule. According to Jeremy West, "Need to identify sequence point. Probably overly difficult to implement in Fortify." -Taschner 10/2</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that the right hand operand of a shift operation is within range</p></td>
<td class="confluenceTd"><p>Not sure that I can do this in a control flow rule, need help. -Taschner 9/28<br />
This is caught with the structural rule for INT31-C - it looks to me like these rules are related enough to allow one rule to catch them both, so I'm going to leave INT31-C to catch it and mark it "DONE" -Taschner 10/11</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP36-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not cast or delete pointers to incomplete classes</p></td>
<td class="confluenceTd"><p>Wrote a structural rule that detects when a variable of type [UnknownType] is assigned something that is not [UnknownType] - there is no way to detect casts in Fortify. Won't detect inside of a class declaration. This seems to be the best I can do. -Taschner 10/4</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>EXP37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Avoid side effects in assertions</p></td>
<td class="confluenceTd"><p>I was able to create a structural rule that catches "assert( index++ == 0 );" or "assert( index == c.size() );" in a function other than "main", but I'm not able to ensure that "index" or "c" (in these examples) are parameters of the enclosing function. Need to ask for help. -Taschner 10/5</p></td>
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not make assumptions about the type of a bit-field when used in an expression</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Use size_t for all integer values representing the size of an object</p></td>
<td class="confluenceTd"><p>This is partially covered by the rule for INT32-C - but Fortify can't flag on type size_t, Fortify sees size_t as unsigned long. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Understand integer conversion rules</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use a secure integer library</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Enforce limits on integer values originating from untrusted sources</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT05-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not input integer values using formatted input</p></td>
<td class="confluenceTd"><p>This is covered by FIO33-C. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT06-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use strtol() to convert a string token to an integer</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag atoi, atol, and atoll when they're passed strings. -Taschner 11/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that integer conversions do not result in lost or misinterpreted data</p></td>
<td class="confluenceTd"><p>Same as C rule. Able to create a structural rule that looks for type conversion without checking the variable on the left hand side of the assignment. -Taschner 10/8</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that integer operations do not result in an overflow</p></td>
<td class="confluenceTd"><p>Same as C rule. Able to create a structural rule that tests to see if the affected operations are being preformed and there is no "if" statement. -Taschner 10/10</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Ensure that division and modulo operations do not result in divide-by-zero errors</p></td>
<td class="confluenceTd"><p>Same as C rule. Created structural rule similar to INT32-C. -Taschner 10/10</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Ensure integer values are within valid ranges</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>INT35-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not truncate the return value from a character input function</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag on a function that returns an int to a char variable. -Taschner 11/12<br />
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Consider avoiding floating point numbers when precise computation is needed</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP30-C</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Take granularity into account when comparing floating point values</p></td>
<td class="confluenceTd"><p>Same as C rule.  -Taschner 11/12<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use floating point variables as loop counters</p></td>
<td class="confluenceTd"><p>Created a rule that flags conditional loops that test a float that is changed in the loop before breaking out of the loop. -Taschner 10/11</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FLP32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Prevent domain errors in math functions</p></td>
<td class="confluenceTd"><p>Same as C rule. -Taschner 10/11</p></td>
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
<td class="confluenceTd"><p>"sizeof" is pre-processed out before Fortify can analyze the code. -Taschner 10/18</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Guarantee that array indices are within the valid range</p></td>
<td class="confluenceTd"><p>Same as C rule</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ARR31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use consistent array notation across all source files</p></td>
<td class="confluenceTd"><p>Same as C rule</p></td>
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Create a copy constructor and assignment operator for non copyable objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not refer to an object outside of its lifetime</p></td>
<td class="confluenceTd"><p>Fortify can't do scope issues.</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Do not access deleted objects</p></td>
<td class="confluenceTd"><p>Caught by [445B3F3C1AB46D8CC28EA535D6436803 : medium : Use After Free : controlflow ] -Taschner 9/20</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not delete this</p></td>
<td class="confluenceTd"><p>Structural rule to catch function "delete" when called with variable named "this~" -Taschner 9/21</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use invalid iterators</p></td>
<td class="confluenceTd"><p>This is the same as STL30-C. -Taschner 10/5</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>DAN34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not dereference invalid pointers</p></td>
<td class="confluenceTd"><p>Can't get new to flag - requested help. Never heard from Fortify. I can't figure out how to do this after further review -Taschner 10/5</p></td>
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use exception handling rather than error codes</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer special-purpose types for exceptions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>ERR02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
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
<td class="confluenceTd"><p>Could not get Fortify to flag on "throw". -Taschner 9/27</p></td>
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
<td class="confluenceTd"><p>because the front-end will introduce temporary variables and convert the non-compliant one to compliant one (the order is <a href="BB.-Definitions_87152273.html#BB.Definitions-implementation-definedbehavior">implementation-defined</a>). So the structural analyzer cannot match all syntactical patterns in the original code. We have a plan to solve the problems due to introduced temporary variables but it's not the highest priority in the coming release. The more general rule is "not allow more than one side-effect in the call parameters", I believe this require more work to handle it. The principle behind structural analysis and structural rules is: structural rules are supposed to match exact syntactical patterns. So it's not possible to match all semantical equivalent code patterns by one structural rule in most cases. In order to achieve the goal of one rule matching all semantically equivalent code patterns, we need introduce more sophisticated analysis which may cost too much overhead. -Ning (fortify)</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>FORTIFY</p></td>
<td class="confluenceTd"><p>Perform every resource allocation in its own statement that immediately assigns the resource to an owning object</p></td>
<td class="confluenceTd"><p>The front-end will translate<br />
int i = xxxx;<br />
<br />
to<br />
<br />
int i;<br />
i = xxxx;<br />
Actually, the dataflow analyzer will mark all used variables which are not initialized in any execution path. -Ning (fortify) 9/21<br />
Fortify catches the example code with [9C8847DF979C3B2462D6E0C7C30BACB2 : low : Uninitialized Variable : controlflow ]</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use new and delete rather than raw memory allocation and deallocation</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>Fortify</p></td>
<td class="confluenceTd"><p>Object and array delete must be properly paired with the corresponding new</p></td>
<td class="confluenceTd"><p>Caught by [B0B21546D73D736EF3111D2D80AAA168 : medium : Memory Leak : controlflow ]</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES34-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Encapsulate resources that require paired acquire and release in objects</p></td>
<td class="confluenceTd"><p>Not sure how to do this, requested help. Ning seemed to think that this might be possible with a control flow rule, he kicked the question to Geoff Morrison. -Taschner 10/11<br />
 Never heard from Geoff Morrison regarding this issue - set to "NO" unless I hear otherwise. -Taschner 11/12<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES35-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Declare a copy constructor, a copy assignment operator, and a destructor in a class that manages resources</p></td>
<td class="confluenceTd"><p>Fortify can't deal with this. -Taschner 11/12<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES36-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that copy assignment operators do not damage an object that is copied to itself</p></td>
<td class="confluenceTd"><p>Can't get Fortify to flag when a member function is deleting a member variable and then attempting to use the contents of that variable. -Taschner 11/14<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES37-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Release resources that require paired acquire and release in the object's destructor</p></td>
<td class="confluenceTd"><p>Fortify can't flag on the existence (or lack) of an explicit destructor. -Taschner 11/14<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES38-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not leak resources when throwing exceptions</p></td>
<td class="confluenceTd"><p>Can't get Fortify to flag on throw statement.  -Taschner 11/14<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>RES39-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use longjmp</p></td>
<td class="confluenceTd"><p>Created semantic rule to flag all calls to longjmp() -Taschner 9/20</p></td>
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Declare data members private</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Be careful with the definition of conversion operators</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Do not hide inherited non-virtual member functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer not to overload virtual functions</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer not to give virtual functions default argument initializers</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ30-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not use pointer arithmetic polymorphically</p></td>
<td class="confluenceTd"><p>Not sure how to do this one. I don't think it can be done, but maybe it can be done with data flow rule?? Going to ask for help, but call this a "NO" in the mean time. -Taschner 9/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Do not treat arrays polymorphically</p></td>
<td class="confluenceTd"><p>See OBJ30-C. -Taschner 9/26</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure that single-argument constructors are marked "explicit"</p></td>
<td class="confluenceTd"><p>Attempted a structural rule, but could not tell the difference between a constructor and an "explicit" constructor. Asked for help, but not optimistic. -Taschner 9/25<br />
Cannot because we ignore conditional expressions. If it's in assignment statements, for example:<br />
Widget * wt;<br />
w1 = 2;<br />
Then we can write a structural rule to match this case. In order to match conditional expressions, we need to define/implement a new label "ConditionalExpression". -Ning (Fortify)</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ33-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>PARTIAL</p></td>
<td class="confluenceTd"><p>Do not slice polymorphic objects</p></td>
<td class="confluenceTd"><p>Can't seem to flag on a member of class that extends the class that the member it is being set equal to belongs to. Will get more help. -Taschner 9/26<br />
One idea is to check the types of the lhs and rhs of an assigment statement. If the types are not primitive, then the assignment might cause object slicing. But the SCA cannot distinguish the assignments in initializations from others in code, so it flags more assignments than necessary. -Ning (fortify)</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>OBJ34-C</p></td>
<td class="confluenceTd"><p>medium</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Ensure the proper destructor is called for polymorphic objects</p></td>
<td class="confluenceTd"><p>Fortify can't tell the difference between a derived class and a non-derived class. -Taschner 11/14<br />
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer basic_string to the use of null-terminated byte strings</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC30-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Use the c_str() member to retrieve a const pointer to a null-terminated byte string</p></td>
<td class="confluenceTd"><p>Created semantic rule to catch all uses of class "basic_string" member function "data" -Taschner 9/24</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC31-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not modify the null-terminated byte string returned by the c_str() member</p></td>
<td class="confluenceTd"><p>Created control flow rule to flag when the string returned by c_str() is altered with str*cat() or str*cpp() -Taschner 9/24</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC32-C</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>DONE</p></td>
<td class="confluenceTd"><p>Do not use the pointer value returned by c_str() after any subsequent call to a non-const member function</p></td>
<td class="confluenceTd"><p>Created a structural rule to flag when a non-const member function of the basic_string class is called after a pointer value is returned by c_str. -Taschner 11/15<br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC33-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use valid references, pointers, and iterators to reference string objects</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>BSC34-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Range check element access</p></td>
<td class="confluenceTd"><p>Looks like C rule ARR30-C - can't test array access in Fortify. -Taschner 9/24</p></td>
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
<td class="confluenceTd"><p>Same as C rule</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR32-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>Fortify?</p></td>
<td class="confluenceTd"><p>Allocated adequate space when copying bounded strings</p></td>
<td class="confluenceTd"><p>Example code caught by Fortify rule [577ED976ECB85D475F17575778932434 : high : Buffer Overflow : dataflow ] - overall don't like the example code, it doesn't seem too complete - need to revisit this one later -Taschner 9/25</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STR35-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Limit input when reading into a fixed length array</p></td>
<td class="confluenceTd"><p>Attempted to write a control flow rule. Could not flag on "cin" or "operator&gt;&gt;" or "&gt;&gt;" -Taschner 10/5</p></td>
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
<td class="confluenceTd"><p>Fortify doesn't seem to distinguish between different types of unary operators. Asked for varification of this. -Taschner 9/27<br />
<br />
This is still the problem of introducing temperary variables by the front-end. 'd.insert (pos+, data[i]+41)' is converted to 't0 = pos; d.insert(t0, data[i]+41)', We will be able do match on 't0 = pos+' in the next release, but it is still an internal feature. -Ning (Fortify) 10/1</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STL31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use Valid Iterator Ranges</p></td>
<td class="confluenceTd"><p>Iterators seem to be processed out before Foritfy gets to them. -Taschner 9/27</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>STL32-C</p></td>
<td class="confluenceTd"><p>low</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Use a Valid Ordering Rule</p></td>
<td class="confluenceTd"><p>Fortify can't flag on this. -Taschner 11/15<br />
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Prefer streams to C-style input output</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>FIO01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
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
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Compile cleanly at high warning levels</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC01-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Strive for Logical Completeness</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC02-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid errors of omission</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC03-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Avoid errors of addition</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC04-A</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p><br />
</p></td>
<td class="confluenceTd"><p>Use comments consistently and in a readable fashion</p></td>
<td class="confluenceTd"><p><br />
</p></td>
</tr>
<tr>
<td class="confluenceTd"><p>MSC31-C</p></td>
<td class="confluenceTd"><p>high</p></td>
<td class="confluenceTd"><p>NO</p></td>
<td class="confluenceTd"><p>Obey the One Definition Rule</p></td>
<td class="confluenceTd"><p>Fortify can't flag on this issue. -Taschner 11/13<br />
</p></td>
</tr>
</tbody>
</table>
## Attachments:
![](images/icons/bullet_blue.gif) [CSCS-Cplusplus.xml](attachments/87152131/88040193.xml) (text/xml)  
## Comments:

|  |
| ----|
| Description for DCL03-A is incorrect, please check.
                                        Posted by sundar at Dec 19, 2008 07:38
                                     |
| Same for "DCL30-C, DCL31-C".
                                        Posted by sundar at Dec 22, 2008 07:33
                                     |

