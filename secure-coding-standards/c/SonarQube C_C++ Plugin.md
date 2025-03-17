> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 3.11

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| 
     AssignmentInSubExpression
     | 
     EXP45-C. Do not perform assignments in selection statements
     |
| 
     ElseIfWithoutElse
     | 
     MSC01-C. Strive for logical completeness
     |
| 
     IdentifierLongerThan31
     | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| 
     IncAndDecMixedWithOtherOperators
     | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 
     LiteralSuffix
     | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| 
     NarrowAndWideStringConcat
     | 
     STR10-C. Do not concatenate different type of string literals
     |
| 
     NonEmptyCaseWithoutBreak
     | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| 
     OctalConstantAndSequence
     | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| 
     S121
     | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| 
     S810
     | 
     STR00-C. Represent characters using an appropriate type
     |
| 
     S810
     | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 
     S814
     | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| 
     S819
     | 
     DCL31-C. Declare identifiers before using them
     |
| 
     S819
     | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 
     S820
     | 
     DCL31-C. Declare identifiers before using them
     |
| 
     S820
     | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 
     S834
     | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| 
     S864
     | 
     EXP00-C. Use parentheses for precedence of operation
     |
| 
     S874
     | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| 
     S929
     | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| 
     S930
     | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 
     S930
     | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 
     S935
     | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| 
     S960
     | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| 
     S973
     | 
     MSC00-C. Compile cleanly at high warning levels
     |
| 
     S978
     | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 
     S982
     | 
     MSC22-C. Use the setjmp(), longjmp() facility securely
     |
| 
     S989
     | 
     ERR34-C. Detect errors when converting a string to a number
     |
| 
     S990
     | 
     ENV33-C. Do not call system()
     |
| 
     S1036
     | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| 
     S1065
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1081
     | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| 
     S1116
     | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 
     S1116
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1172
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1578
     | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| 
     S1656
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| S1751 | 
     MSC07-C. Detect and remove dead code
     |
| 
     S1751
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1762
     | 
     MSC00-C. Compile cleanly at high warning levels
     |
| S1763 | 
     MSC07-C. Detect and remove dead code
     |
| 
     S1763
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1764
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S1767
     | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| 
     S1836
     | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 
     S1854
     | 
     MSC13-C. Detect and remove unused values
     |
| 
     S1862
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S2095
     | 
     FIO42-C. Close files when they are no longer needed
     |
| 
     S2193
     | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| 
     S2259
     | 
     EXP34-C. Do not dereference null pointers
     |
| 
     S2583
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S2589
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S2754
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     S3518
     | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 
     S3584
     | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| 
     S3588
     | 
     FIO46-C. Do not access a closed file
     |
| 
     SideEffectInRightHandSideOfLogical
     | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 
     SingleDeclarationPerStatement
     | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| 
     SwitchWithoutDefault
     | 
     MSC01-C. Strive for logical completeness
     |
| 
     TrigraphUsage
     | 
     PRE07-C. Avoid using repeated question marks
     |

