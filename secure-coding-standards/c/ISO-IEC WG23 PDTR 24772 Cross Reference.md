
| Rule Number | WG23 | JSF | MISRA | CERT C |
| ----|----|----|----|----|
| 6.1 | BRS Leveraging Human Experience | 84, 86, 88, 97 | 10.2, 13.1, 20.6–20.12, 12.10, 3.2, 17.5 | ; |
| 6.2
 6.3
 6.4 | BQF Unspecified Behavior 
EWF Undefined Behavior 
FAB Implementation-defined behavior | 17–25 (cited from MISRA), 97.1 | 1.3 , 1.5, 3.1 3.3, 3.4, 17.3, 1.2, 5.1, 18.2, 19.2, 19.14 | MSC15-C. Do not depend on undefined behavior |
| 6.5 | MEM Deprecated Language Features | 8, 152 | 1.1, 4.2, 20.10 | ; |
| 6.6 | BVQ Unspecified Functionality | 127 | 14.1, 2.2, 2.3 2.4 | ; |
| 6.7 | NMP Pre-processor Directives | 26, 27, 28, 29, 30, 31, and 32 | 19. 6, 19.7, 19.8, and 19.9 | PRE01-C. Use parentheses within macros around parameter names
PRE02-C. Macro replacement lists should be parenthesized
PRE10-C. Wrap multistatement macros in a do-while loop
PRE31-C. Avoid side effects in arguments to unsafe macros |
| 6.8 | NAI Choice of Clear Names | 48-56 | 1.4 | DCL02-C. Use visually distinct identifiers |
| 6.9 | AJN Choice of Filenames and other External Identifiers | 48-56 | 5.1 | MSC09-C. Character encoding: Use subset of ASCII for safety
MSC10-C. Character encoding: UTF8-related issues |
| 6.10 | XYR Unused Variable | ; | ; | MSC13-C. Detect and remove unused values |
| 6.11 | YOW Identifier name reuse | 120, 159 (C++) | 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 20.1, 20.2, 16.9 | DCL01-C. Do not reuse variable names in subscopes
DCL23-C. Guarantee that mutually visible identifiers are unique |
| 6.12 | IHN Type system | 148, 183 | 6.1, 6.2, 6.3, 10.1-10.5 | DCL07-C. Include the appropriate type information in function declarators
DCL11-C. Understand the type issues associated with variadic functions
EXP05-C. Do not cast away a const qualification
EXP32-C. Do not access a volatile object through a nonvolatile referenceEXP37-C. Call functions with the correct number and type of arguments |
| 6.13 | STR Bit Representations | ; | 3.5, 6.4, 6.5, 12.7 | INT00-C. Understand the data model used by your implementation(s)
INT07-C. Use only explicitly signed or unsigned char type for numeric values
INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
INT13-C. Use bitwise operators only on unsigned operands
INT14-C. Avoid performing bitwise and arithmetic operations on the same data |
| 6.14 | PLF Floating Point Arithmetic | 146, 147, 184, 197, 202 | 13.3, 13.4, 1.5, 12.12 | FLP00-C. Understand the limitations of floating-point numbers
FLP01-C. Take care in rearranging floating-point expressions
FLP02-C. Avoid using floating-point numbers when precise computation is needed
FLP30-C. Do not use floating-point variables as loop counters |
| 6.15 | CCB Enumerator issues | ; | 9.1 - 9.3 | INT09-C. Ensure enumeration constants map to unique values |
| 6.16 | FLC Numeric Conversion Errors | ; | 12.9, 10.1-10.6, 11.3-11.5 | FLP34-C. Ensure that floating-point conversions are within range of the new type
INT02-C. Understand integer conversion rules
INT08-C. Verify that all integer values are in range
INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size |
| 6.17 | CJM String Termination | ; | ; | STR03-C. Do not inadvertently truncate a string
STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
STR11-C. Do not specify the bound of a character array initialized with a string literal |
| 6.18 | XYX Boundary Beginning Violation | ; | ; | ARR30-C. Do not form or use out-of-bounds pointers or array subscriptsARR32-C. Ensure size arguments for variable length arrays are in a valid range |
| 6.19 | XYZ Unchecked Array Indexing | ; | ; | ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
ARR32-C. Ensure size arguments for variable length arrays are in a valid range |
| 6.20 | XYW Buffer Overflow in Stack | ; | ; | STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator |
| 6.21 | XZB Buffer Overflow in Heap | ; | ; | STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
MEM35-C. Allocate sufficient memory for an object |
| 6.22 | HFC Pointer casting and pointer type changes | ; | 11.1, 11.2, 11.3, 11.4, 11.5 | INT36-C. Converting a pointer to integer or integer to pointer
EXP36-C. Do not cast pointers into more strictly aligned pointer types |
| 6.23 | RVG Pointer Arithmetic | 215 | 17.1, 17.2, 17.3, and 17.4 | EXP08-C. Ensure pointer arithmetic is used correctly |
| 6.24 | XYH Null Pointer Dereference | ; | ; | EXP34-C. Do not dereference null pointers |
| 6.25 | XYK Dangling Reference to Heap | ; | 17.6, 17.1, 17.2, 17.3, 17.4, 17.5 | MEM01-C. Store a new value in pointers immediately after free()
MEM30-C. Do not access freed memory
MEM31-C. Free dynamically allocated memory when no longer needed |
| 6.26 | SYM Templates and generics | 100, 101, 102, 103, 104, 105 | (C++) 14-7-2 14-8-1 14-8-2 | ; |
| 6.27 | LAV Initialization of variables | ; | ; | EXP33-C. Do not read uninitialized memory |
| 6.28 | XYY Wrap-around Error | ; | 10.1–10.6, 12.8, 12.11 | INT30-C. Ensure that unsigned integer operations do not wrap
INT32-C. Ensure that operations on signed integers do not result in overflow
INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand |
| 6.29 | XZI Sign Extension Error | ; | ; | INT13-C. Use bitwise operators only on unsigned operands |
| 6.30 | JCW Operator precedence | 204, 213 | 12.1, 12.2, 12.5, 12.6, 13.2, 19.10, 19.12, 19.13 | EXP00-C. Use parentheses for precedence of operation |
| 6.31 | SAM Side-effects and order of evaluation | ; | ; | EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
EXP30-C. Do not depend on the order of evaluation for side effects |
| 6.32 | KOA Likely Incorrect Expressions | 160, 166 | 12.3, 12.4, 12.13, 13.1, 14.2, 13.7 | ;EXP15-C. Do not place a semicolon on the same line as an if, for, or while statementEXP16-C. Do not compare function pointers to constant valuesEXP45-C. Do not perform assignments in selection statementsEXP46-C. Do not use a bitwise operator with a Boolean-like operand
MSC12-C. Detect and remove code that has no effect or is never executed |
| 6.33 | XYQ Dead and Deactivated Code | ; | 14.1, 14.2, 2.4 | MSC07-C. Detect and remove dead code
MSC12-C. Detect and remove code that has no effect or is never executed |
| 6.34 | CLL Switch Statements and Static Analysis | ; | 15.2, 15.3, 15.5 | MSC01-C. Strive for logical completeness |
| 6.35 | EOJ Demarcation of control flow | ; | 14.9, 14.8, 14.10, 19.5 | ; |
| 6.36 | TEX Loop Control Variables | ; | ; | ; |
| 6.37 | XZH Off-by-one Error | ; | ; | ; |
| 6.38 | EWD Structured Programming | ; | 14.4, 14.5, 20.7 | SIG30-C. Call only asynchronous-safe functions within signal handlers |
| 6.39 | CSJ Passing parameters and return values | ; | 16.7, 16.9, 16.1–16.6 | EXP12-C. Do not ignore values returned by functions |
| 6.40 | DCM Dangling references to stack frames | ; | 17.6, 21.1 | EXP35-C. Do not modify objects with temporary lifetime
DCL30-C. Declare objects with appropriate storage durations |
| 6.41 | OTR Subprogram Signature Mismatch | 108, 110 | 8.1, 8.2, 8.3, 8.4 16.1, 16.3, 16.4, 16.5, 16.6 | DCL31-C. Declare identifiers before using them
EXP37-C. Call functions with the correct number and type of arguments |
| 6.42 | GDL Recursion | ; | 16.2 | MEM05-C. Avoid large stack allocations |
| 6.43 | NZN Returning error status | 208 | 20.5 | DCL09-C. Declare functions that return errno with a return type of errno_t
ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy
ERR02-C. Avoid in-band error indicators |
| 6.44 | REU Termination strategy | ; | 20.11 | ERR04-C. Choose an appropriate termination strategy
ERR06-C. Understand the termination behavior of assert() and abort()
ENV32-C. All exit handlers must return normally |
| 6.45 | AMV Type-breaking reinterpretation of data | ; | ; | EXP39-C. Do not access a variable through a pointer of an incompatible type |
| 6.46 | XYL Memory Leak | ; | ; | MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
MEM31-C. Free dynamically allocated memory when no longer needed |
| 6.47 | TRJ Use of Libraries | 16, 18, 19, 20, 21, 22, 23, 24, and 25 | 20.2, 20.3, 20.4, 20.6, 20.7, 20.8, 20.9, 20.10, 20.11, and 20.12 | STR07-C. Use the bounds-checking interfaces for string manipulation |
| 6.48 | NYY Dynamically-linked code and self-modifying code | 2 | ; | ; |
| 7.1 | XYN Privilege Management | ; | ; | POS02-C. Follow the principle of least privilege |
| 7.2 | XYO Privilege Sandbox Issues | ; | ; | POS36-C. Observe correct revocation order while relinquishing privileges 
POS37-C. Ensure that privilege relinquishment is successful |
| 7.3 | XYS Executing or Loading Untrusted Code | ; | ; | PRE09-C. Do not replace secure functions with deprecated or obsolescent functions
ENV02-C. Beware of multiple environment variables with the same effective name
ENV03-C. Sanitize the environment when invoking external programs |
| 7.4 | XZX Memory Locking | ; | ; | MEM06-C. Ensure that sensitive data is not written out to disk |
| 7.5 | XZY Resource Exhaustion | ; | ; | ; |
| 7.6 | RST Injection | ; | ; | FIO30-C. Exclude user input from format strings |
| 7.7 | XYT Cross-site Scripting | ; | ; | ; |
| 7.8 | XZQ Unquoted Search Path or Element | ; | ; | ENV33-C. Do not call system() |
| 7.9 | XZR Improperly Verified Signature | ; | ; | ; |
| 7.10 | XZL Discrepancy Information Leak | ; | ; | ; |
| 7.11 | XZK Sensitive Information Uncleared Before Use | ; | ; | MEM03-C. Clear sensitive information stored in reusable resources |
| 7.12 | EWR Path Traversal | ; | ; | FIO02-C. Canonicalize path names originating from tainted sources |
| 7.13 | XZS Missing Required Cryptographic Step | ; | ; | ; |
| 7.14 | XYM Insufficiently Protected Credentials | ; | ; | ; |
| 7.15 | XZN Missing or Inconsistent Access Control | ; | ; | FIO06-C. Create files with appropriate access permissions |
| 7.16 | XZO Authentication Logic Error | ; | ; | ; |
| 7.17 | XYP Hard-coded Password | ; | ; | ; |

