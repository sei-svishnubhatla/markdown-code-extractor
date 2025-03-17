> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 7.2.0

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| CertC-ARR01 | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| CertC-ARR02 | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| CertC-ARR30 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| CertC-ARR36 | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| CertC-ARR37 | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| CertC-ARR39 | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| CertC-CON32 | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| CertC-CON40 | 
     CON40-C. Do not refer to an atomic variable twice in an expression
     |
| CertC-DCL00 | 
     DCL00-C. Const-qualify immutable objects
     |
| CertC-DCL01 | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| CertC-DCL02 | 
     DCL02-C. Use visually distinct identifiers
     |
| CertC-DCL03 | 
     DCL03-C. Use a static assertion to test the value of a constant expression
     |
| CertC-DCL04 | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| CertC-DCL05 | 
     DCL05-C. Use typedefs of non-pointer types only
     |
| CertC-DCL06 | 
     DCL06-C. Use meaningful symbolic constants to represent literal values
     |
| CertC-DCL07 | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| CertC-DCL09 | 
     DCL09-C. Declare functions that return errno with a return type of errno_t
     |
| CertC-DCL11 | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CertC-DCL12 | 
     DCL12-C. Implement abstract data types using opaque types
     |
| CertC-DCL13 | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| CertC-DCL15 | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| CertC-DCL16 | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| CertC-DCL18 | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| CertC-DCL19 | 
     DCL19-C. Minimize the scope of variables and functions
     |
| CertC-DCL20 | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| CertC-DCL21 | 
     DCL21-C. Understand the storage of compound literals
     |
| CertC-DCL23 | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| CertC-DCL30 | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| CertC-DCL31 | 
     DCL31-C. Declare identifiers before using them
     |
| CertC-DCL36 | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| CertC-DCL37 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CertC-DCL38 | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| CertC-DCL39 | 
     DCL39-C. Avoid information leakage when passing a structure across a trust boundary
     |
| CertC-DCL40 | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| CertC-DCL41 | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| CertC-ENV30 | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| CertC-ENV32 | 
     ENV32-C. All exit handlers must return normally
     |
| CertC-ENV33 | 
     ENV33-C. Do not call system()
     |
| CertC-ERR07 | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| CertC-ERR30 | 
     ERR30-C. Take care when reading errno
     |
| CertC-ERR32 | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| CertC-ERR33 | 
     ERR33-C. Detect and handle standard library errors
     |
| CertC-ERR34 | 
     ERR34-C. Detect errors when converting a string to a number
     |
| CertC-EXP00 | 
     EXP00-C. Use parentheses for precedence of operation
     |
| CertC-EXP02 | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| CertC-EXP05 | 
     EXP05-C. Do not cast away a const qualification
     |
| CertC-EXP07 | 
     EXP07-C. Do not diminish the benefits of constants by assuming their values in expressions
     |
| CertC-EXP10 | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| CertC-EXP12 | 
     EXP12-C. Do not ignore values returned by functions
     |
| CertC-EXP14 | 
     EXP14-C. Beware of integer promotion when performing bitwise operations on integer types smaller than int
     |
| CertC-EXP15 | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| CertC-EXP19 | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| CertC-EXP20 | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| CertC-EXP30 | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| CertC-EXP32 | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| CertC-EXP33 | 
     EXP33-C. Do not read uninitialized memory
     |
| CertC-EXP34 | 
     EXP34-C. Do not dereference null pointers
     |
| CertC-EXP35 | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| CertC-EXP36 | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| CertC-EXP37 | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| CertC-EXP40 | 
     EXP40-C. Do not modify constant objects
     |
| CertC-EXP42 | 
     EXP42-C. Do not compare padding data
     |
| CertC-EXP44 | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| CertC-EXP45 | 
     EXP45-C. Do not perform assignments in selection statements
     |
| CertC-EXP46 | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| CertC-EXP47 | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| CertC-FIO30 | 
     FIO30-C. Exclude user input from format strings
     |
| CertC-FIO34 | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| CertC-FIO37 | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| CertC-FIO38 | 
     FIO38-C. Do not copy a FILE object
     |
| CertC-FIO39 | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| CertC-FIO41 | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| CertC-FIO47 | 
     FIO47-C. Use valid format strings
     |
| CertC-FLP02 | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| CertC-FLP06 | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| CertC-FLP07 | 
     FLP07-C. Cast the return value of a function that returns a floating-point type
     |
| CertC-FLP30 | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| CertC-FLP32 | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| CertC-FLP37 | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| CertC-INT00 | 
     INT00-C. Understand the data model used by your implementation(s)
     |
| CertC-INT01 | 
     INT01-C. Use rsize_t or size_t for all integer values representing the size of an object
     |
| CertC-INT05 | 
     INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs
     |
| CertC-INT07 | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| CertC-INT08 | 
     INT08-C. Verify that all integer values are in range
     |
| CertC-INT09 | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| CertC-INT12 | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| CertC-INT13 | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| CertC-INT15 | 
     INT15-C. Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types
     |
| CertC-INT17 | 
     INT17-C. Define integer constants in an implementation-independent manner
     |
| CertC-INT30 | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| CertC-INT33 | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| CertC-INT34 | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| CertC-INT36 | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| CertC-MEM01 | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| CertC-MEM02 | 
     MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type
     |
| CertC-MEM30 | 
     MEM30-C. Do not access freed memory
     |
| CertC-MEM31 | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| CertC-MEM33 | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| CertC-MEM34 | 
     MEM34-C. Only free memory allocated dynamically
     |
| CertC-MEM35 | 
     MEM35-C. Allocate sufficient memory for an object
     |
| CertC-MEM36 | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| CertC-MSC24 | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| CertC-MSC30 | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| CertC-MSC32 | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| CertC-MSC33 | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| CertC-MSC37 | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| CertC-POS30 | 
     POS30-C. Use the readlink() function properly
     |
| CertC-POS34 | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| CertC-POS35 | 
     POS35-C. Avoid race conditions while checking for the existence of a symbolic link
     |
| CertC-POS36 | 
     POS36-C. Observe correct revocation order while relinquishing privileges
     |
| CertC-POS37 | 
     POS37-C. Ensure that privilege relinquishment is successful
     |
| CertC-POS39 | 
     POS39-C. Use the correct byte ordering when transferring data between systems
     |
| CertC-POS47 | 
     POS47-C. Do not use threads that can be canceled asynchronously
     |
| CertC-POS49 | 
     POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
     |
| CertC-POS54 | 
     POS54-C. Detect and handle POSIX library errors
     |
| CertC-PRE00 | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| CertC-PRE01 | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| CertC-PRE02 | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| CertC-PRE04 | 
     PRE04-C. Do not reuse a standard header file name
     |
| CertC-PRE05 | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| CertC-PRE06 | 
     PRE06-C. Enclose header files in an include guard
     |
| CertC-PRE07 | 
     PRE07-C. Avoid using repeated question marks
     |
| CertC-PRE08 | 
     PRE08-C. Guarantee that header file names are unique
     |
| CertC-PRE09 | 
     PRE09-C. Do not replace secure functions with deprecated or obsolescent functions
     |
| CertC-PRE10 | 
     PRE10-C. Wrap multistatement macros in a do-while loop
     |
| CertC-PRE11 | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| CertC-PRE12 | 
     PRE12-C. Do not define unsafe macros
     |
| CertC-PRE13 | 
     PRE13-C. Use the Standard predefined macros to test for versions and features.
     |
| CertC-PRE30 | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| CertC-PRE31 | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| CertC-PRE32 | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| CertC-SIG30 | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| CertC-SIG31 | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| CertC-SIG34 | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| CertC-SIG35 | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| CertC-STR04 | 
     STR04-C. Use plain char for characters in the basic character set
     |
| CertC-STR05 | 
     STR05-C. Use pointers to const when referring to string literals
     |
| CertC-STR07 | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| CertC-STR09 | 
     STR09-C. Don't assume numeric values for expressions with type plain character
     |
| CertC-STR10 | 
     STR10-C. Do not concatenate different type of string literals
     |
| CertC-STR11 | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| CertC-STR30 | 
     STR30-C. Do not attempt to modify string literals
     |
| CertC-STR31 | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CertC-STR32 | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| CertC-STR34 | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| CertC-STR37 | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| CertC-STR38 | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |

