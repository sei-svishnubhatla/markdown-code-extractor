> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 4.3.5

| 
    Checker
    | 
    Guideline
    |
| ----|----|
|  | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 
     -Wchar-subscripts
     | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| 
     -Wrestrict
     | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 
     -Wstringop-truncation
     | 
     STR03-C. Do not inadvertently truncate a string
     |
| 
     -Wunused-parameter
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 
     -Wunused-value
     | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| -Ww | 
     STR05-C. Use pointers to const when referring to string literals
     |
| Can detect some violations of this recommendation when the -Wswitch and -Wswitch-default flags are used | 
     MSC01-C. Strive for logical completeness
     |
| Can detect some violations of this rule when the -Wcast-align flag is used | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| Can detect some;violations of this rule when the -Wuninitialized flag is used | 
     EXP33-C. Do not read uninitialized memory
     |
| Can detect violation of this recommendation when the -Wstrict-prototypes flag is used | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| Can detect violation of this recommendation when the -Wtrigraphs flag is used | 
     PRE07-C. Avoid using repeated question marks
     |
| Can detect violation of this rule when the -Wstrict-prototypes flag is used. However, it cannot detect violations involving variadic functions, such as the open() example described earlier | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| Can detect violations of this recommendation when the -Wall flag is used | 
     EXP45-C. Do not perform assignments in selection statements
     |
| Can detect violations of this recommendation when the -Wall flag is used | 
     EXP16-C. Do not compare function pointers to constant values
     |
| Can detect violations of this recommendation when the -Wcast-qual flag is used | 
     EXP05-C. Do not cast away a const qualification
     |
| Can detect violations of this recommendation when the -Wformat flag is used | 
     FIO47-C. Use valid format strings
     |
| Can detect violations of this recommendation when the -Wunreachable-code flag is used | 
     MSC07-C. Detect and remove dead code
     |
| Can detect violations of this rule when the -Wcast-qual flag is used | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| Can detect violations of this rule when the -Wcomment flag is used | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| Can detect violations of this rule when the -Wformat-security flag is used | 
     FIO30-C. Exclude user input from format strings
     |
| Can detect violations of this rule when the -Wimplicit and -Wreturn-type flags are used | 
     DCL31-C. Declare identifiers before using them
     |
| Can detect violations of this rule when the -Wsequence-point flag is used | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| Option -Wparentheses warns if a comparison like x<=y<=z appears; this warning is also enabled by -Wall | 
     EXP13-C. Treat relational and equality operators as if they were nonassociative
     |
| rite-strings | 
     STR05-C. Use pointers to const when referring to string literals
     |
| Warns about inconsistently typed arguments to formatted output functions when the -Wall is used | 
     DCL11-C. Understand the type issues associated with variadic functions
     |

