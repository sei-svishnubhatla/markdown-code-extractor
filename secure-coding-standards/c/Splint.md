> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 3.1.1

| 
    Checker
    | 
    Guideline
    |
| ----|----|
|  | 
     DCL30-C. Declare objects with appropriate storage durations
     |
|  | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
|  | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
|  | 
     EXP33-C. Do not read uninitialized memory
     |
|  | 
     EXP34-C. Do not dereference null pointers
     |
|  | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
|  | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
|  | 
     STR30-C. Do not attempt to modify string literals
     |
|  | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
|  | 
     MEM30-C. Do not access freed memory
     |
|  | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
|  | 
     MEM35-C. Allocate sufficient memory for an object
     |
|  | 
     FIO30-C. Exclude user input from format strings
     |
|  | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
|  | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
|  | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
|  | 
     DCL01-C. Do not reuse variable names in subscopes
     |
|  | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
|  | 
     EXP12-C. Do not ignore values returned by functions
     |
|  | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
|  | 
     INT01-C. Use rsize_t or size_t for all integer values representing the size of an object
     |
|  | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
|  | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
|  | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| -standard | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| Can detect violations of this recommendation when the -Wunreachable-code flag is used | 
     MSC07-C. Detect and remove dead code
     |

