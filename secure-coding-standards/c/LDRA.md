> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 9.7.1

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| 1 D | 
     MSC13-C. Detect and remove unused values
     |
| 1 J | 
     MSC07-C. Detect and remove dead code
     |
| 1 Q | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 1 Q | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 1 Q | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| 1 Q | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 1 Q | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 1 Q | 
     PRE12-C. Do not define unsafe macros
     |
| 1 U | 
     MEM11-C. Do not assume infinite heap space
     |
| 1 X | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 2 D | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| 2 X | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 3 J | 
     MSC06-C. Beware of compiler optimizations
     |
| 5 C | 
     MEM11-C. Do not assume infinite heap space
     |
| 5 Q | 
     MSC15-C. Do not depend on undefined behavior
     |
| 6 D | 
     MEM11-C. Do not assume infinite heap space
     |
| 7 S | 
     ENV32-C. All exit handlers must return normally
     |
| 8 D | 
     DCL22-C. Use volatile for data that cannot be cached
     |
| 8 D | 
     MSC06-C. Beware of compiler optimizations
     |
| 8 D | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 8 D | 
     MSC13-C. Detect and remove unused values
     |
| 9 S | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 9 S | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 9 S | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| 11 S | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 11 S | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| 12 S | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 12 S | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| 15 D | 
     MSC13-C. Detect and remove unused values
     |
| 17 D | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 17 D | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| 17 D | 
     MSC14-C. Do not introduce unnecessary platform dependencies
     |
| 20 S | 
     DCL31-C. Declare identifiers before using them
     |
| 21 S | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 21 S | 
     MSC40-C. Do not violate constraints
     |
| 21 S | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 24 D | 
     DCL31-C. Declare identifiers before using them
     |
| 25 D | 
     DCL19-C. Minimize the scope of variables and functions
     |
| 26 S | 
     MEM11-C. Do not assume infinite heap space
     |
| 27 D | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| 28 D | 
     MEM11-C. Do not assume infinite heap space
     |
| 30 S | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 30 S | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| 35 D | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 35 D | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 35 D | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| 35 D | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 35 D | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 35 D | 
     PRE12-C. Do not define unsafe macros
     |
| 35 S | 
     MSC06-C. Beware of compiler optimizations
     |
| 36 S | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| 39 S | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| 40 S | 
     DCL19-C. Minimize the scope of variables and functions
     |
| 41 D | 
     DCL31-C. Declare identifiers before using them
     |
| 41 D | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 41 S | 
     DCL10-C. Maintain the contract between the writer and caller of variadic functions
     |
| 41 S | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| 42 D | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 42 D | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| 42 S | 
     MSC14-C. Do not introduce unnecessary platform dependencies
     |
| 43 D | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 43 D | 
     FLP03-C. Detect and handle floating-point errors
     |
| 43 S | 
     MSC22-C. Use the setjmp(), longjmp() facility securely
     |
| 44 S | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| 44 S | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| 44 S | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| 44 S | 
     FIO40-C. Reset strings on fgets()  or fgetws() failure
     |
| 44 S | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| 44 S | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| 44 S | 
     ERR34-C. Detect errors when converting a string to a number
     |
| 44 S | 
     CON33-C. Avoid race conditions when using library functions
     |
| 44 S | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| 44 S | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| 44 S | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| 44 S | 
     DCL03-C. Use a static assertion to test the value of a constant expression
     |
| 44 S | 
     ERR01-C. Use ferror() rather than errno to check for FILE stream errors
     |
| 44 S | 
     ERR06-C. Understand the termination behavior of assert() and abort()
     |
| 44 S | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| 44 S | 
     FIO03-C. Do not make assumptions about fopen() and file creation
     |
| 44 S | 
     FIO05-C. Identify files using multiple file attributes
     |
| 44 S | 
     FIO06-C. Create files with appropriate access permissions
     |
| 44 S | 
     FIO09-C. Be careful with binary data when transferring data across systems
     |
| 44 S | 
     FIO17-C. Do not rely on an ending null character when using fread()
     |
| 44 S | 
     FIO18-C. Never expect fwrite() to terminate the writing process at a null character
     |
| 44 S | 
     FIO19-C. Do not use fseek() and ftell() to compute the size of a regular file
     |
| 44 S | 
     FIO20-C. Avoid unintentional truncation when using fgets() or fgetws()
     |
| 44 S | 
     FIO21-C. Do not create temporary files in shared directories
     |
| 44 S | 
     INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs
     |
| 44 S | 
     MEM03-C. Clear sensitive information stored in reusable resources
     |
| 44 S | 
     MEM05-C. Avoid large stack allocations
     |
| 44 S | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| 44 S | 
     SIG00-C. Mask signals handled by noninterruptible signal handlers
     |
| 44 S | 
     SIG02-C. Avoid using signals to implement normal functionality
     |
| 44 S | 
     STR03-C. Do not inadvertently truncate a string
     |
| 44 S | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| 45 D | 
     EXP34-C. Do not dereference null pointers
     |
| 45 D | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 45 D | 
     ARR00-C. Understand how arrays work
     |
| 45 D | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 47 S | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 47 S | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 47 S | 
     ARR00-C. Understand how arrays work
     |
| 48 D | 
     FIO46-C. Do not access a closed file
     |
| 48 D | 
     MSC15-C. Do not depend on undefined behavior
     |
| 48 S | 
     MSC01-C. Strive for logical completeness
     |
| 49 D | 
     FIO42-C. Close files when they are no longer needed
     |
| 49 D | 
     FIO22-C. Close files before spawning processes
     |
| 49 S | 
     EXP00-C. Use parentheses for precedence of operation
     |
| 50 D | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| 50 D | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| 50 D | 
     MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources
     |
| 50 S | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| 50 S | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| 51 D | 
     MEM30-C. Do not access freed memory
     |
| 51 S | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| 52 S | 
     INT02-C. Understand integer conversion rules
     |
| 53 D | 
     EXP33-C. Do not read uninitialized memory
     |
| 53 D | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 54 D | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 54 S | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| 56 S | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| 57 S | 
     MSC06-C. Beware of compiler optimizations
     |
| 57 S | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 59 S | 
     MSC01-C. Strive for logical completeness
     |
| 61 D | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| 61 D | 
     DCL19-C. Minimize the scope of variables and functions
     |
| 61 X | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| 62 S | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| 62 X | 
     MSC15-C. Do not depend on undefined behavior
     |
| 63 D | 
     MSC15-C. Do not depend on undefined behavior
     |
| 63 S | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| 63 X | 
     MSC15-C. Do not depend on undefined behavior
     |
| 64 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 64 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 64 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 64 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 64 X | 
     ARR00-C. Understand how arrays work
     |
| 65 D | 
     MSC06-C. Beware of compiler optimizations
     |
| 65 D | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 65 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 66 S | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| 66 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 66 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 66 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 66 X | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 66 X | 
     ARR00-C. Understand how arrays work
     |
| 67 X | 
     DCL02-C. Use visually distinct identifiers
     |
| 68 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 68 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 68 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 68 X | 
     ARR00-C. Understand how arrays work
     |
| 69 D | 
     EXP33-C. Do not read uninitialized memory
     |
| 69 S | 
     MSC14-C. Do not introduce unnecessary platform dependencies
     |
| 69 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 69 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 69 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 69 X | 
     ARR00-C. Understand how arrays work
     |
| 70 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 70 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 70 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 70 X | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 70 X | 
     ARR00-C. Understand how arrays work
     |
| 71 S | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 71 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 71 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 71 X | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 71 X | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 71 X | 
     ARR00-C. Understand how arrays work
     |
| 72 D | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 73 S | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| 75 D | 
     FIO45-C. Avoid TOCTOU race conditions while accessing files
     |
| 75 D | 
     FIO24-C. Do not open a file that is already open
     |
| 76 D | 
     MSC06-C. Beware of compiler optimizations
     |
| 76 S | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| 77 D | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 77 D | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| 77 S | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| 78 D | 
     DCL00-C. Const-qualify immutable objects
     |
| 78 S | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| 79 S | 
     PRE10-C. Wrap multistatement macros in a do-while loop
     |
| 79 S | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| 79 X | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 79 X | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 80 D | 
     ERR33-C. Detect and handle standard library errors
     |
| 80 D | 
     POS54-C. Detect and handle POSIX library errors
     |
| 80 X | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 81 D | 
     FIO08-C. Take care when calling remove() on an open file
     |
| 81 S | 
     PRE07-C. Avoid using repeated question marks
     |
| 82 D | 
     FIO44-C. Only use values for fsetpos() that are returned from fgetpos()
     |
| 83 D | 
     FIO13-C. Never push back anything other than one read character
     |
| 83 S | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| 84 D | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| 84 D | 
     MSC15-C. Do not depend on undefined behavior
     |
| 85 D | 
     FIO02-C. Canonicalize path names originating from tainted sources
     |
| 85 S | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| 86 D | 
     FIO30-C. Exclude user input from format strings
     |
| 86 S | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 87 D | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| 88 D | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| 89 D | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| 93 D | 
     DCL00-C. Const-qualify immutable objects
     |
| 93 S | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| 93 S | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 93 S | 
     INT02-C. Understand integer conversion rules
     |
| 93 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 93 S | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 94 D | 
     MSC13-C. Detect and remove unused values
     |
| 94 S | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| 94 S | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| 96 S | 
     INT02-C. Understand integer conversion rules
     |
| 96 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 96 S | 
     MSC05-C. Do not manipulate time_t typed values directly
     |
| 97 D | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| 97 D | 
     SIG01-C. Understand implementation-specific details regarding signal handler persistence
     |
| 98 S | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 99 S | 
     EXP16-C. Do not compare function pointers to constant values
     |
| 100 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 101 S | 
     INT02-C. Understand integer conversion rules
     |
| 101 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 101 S | 
     MSC05-C. Do not manipulate time_t typed values directly
     |
| 101 S | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 104 D | 
     DCL12-C. Implement abstract data types using opaque types
     |
| 105 D | 
     MSC06-C. Beware of compiler optimizations
     |
| 105 D | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 105 D | 
     MSC13-C. Detect and remove unused values
     |
| 107 D | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| 107 S | 
     INT02-C. Understand integer conversion rules
     |
| 107 S | 
     MSC05-C. Do not manipulate time_t typed values directly
     |
| 108 D | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| 109 D | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 109 D | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| 109 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 111 D | 
     ERR30-C. Take care when reading errno
     |
| 112 D | 
     MEM30-C. Do not access freed memory
     |
| 112 D | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| 113 D | 
     MSC15-C. Do not depend on undefined behavior
     |
| 113 S | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| 114 S | 
     EXP45-C. Do not perform assignments in selection statements
     |
| 114 S | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| 115 D | 
     MEM35-C. Allocate sufficient memory for an object
     |
| 115 S | 
     STR03-C. Do not inadvertently truncate a string
     |
| 118 S | 
     ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it
     |
| 119 S | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 120 D | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| 120 S | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| 120 S | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| 121 D | 
     ERR30-C. Take care when reading errno
     |
| 122 D | 
     ERR30-C. Take care when reading errno
     |
| 122 S | 
     ENV32-C. All exit handlers must return normally
     |
| 123 D | 
     EXP34-C. Do not dereference null pointers
     |
| 125 D | 
     MEM34-C. Only free memory allocated dynamically
     |
| 125 S | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| 127 D | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 127 S | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| 128 D | 
     EXP34-C. Do not dereference null pointers
     |
| 129 D | 
     EXP34-C. Do not dereference null pointers
     |
| 130 D | 
     EXP34-C. Do not dereference null pointers
     |
| 131 D | 
     EXP34-C. Do not dereference null pointers
     |
| 131 S | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| 132  D | 
     ERR30-C. Take care when reading errno
     |
| 132 S | 
     EXP45-C. Do not perform assignments in selection statements
     |
| 133 D | 
     ENV34-C. Do not store pointers returned by certain functions
     |
| 133 S | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 134 D | 
     ERR30-C. Take care when reading errno
     |
| 134 S | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 134 S | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| 134 S | 
     DCL17-C. Beware of miscompiled volatile-qualified variables
     |
| 134 S | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 135 S | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 136 S | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| 139 S | 
     MSC07-C. Detect and remove dead code
     |
| 139 S | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 140 S | 
     MEM11-C. Do not assume infinite heap space
     |
| 140 S | 
     MSC07-C. Detect and remove dead code
     |
| 140 S | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 145 S | 
     MSC40-C. Do not violate constraints
     |
| 156 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 157 S | 
     STR30-C. Do not attempt to modify string literals
     |
| 159 S | 
     MEM10-C. Define and use a pointer validation function
     |
| 170 S | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 170 S | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 176 S | 
     MSC10-C. Character encoding: UTF8-related issues
     |
| 200 S | 
     DCL00-C. Const-qualify immutable objects
     |
| 201 S | 
     DCL06-C. Use meaningful symbolic constants to represent literal values
     |
| 201 S | 
     EXP07-C. Do not diminish the benefits of constants by assuming their values in expressions
     |
| 201 S | 
     EXP09-C. Use sizeof to determine the size of a type or variable
     |
| 203 S | 
     EXP05-C. Do not cast away a const qualification
     |
| 218 S | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 219 S | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 243 S | 
     PRE06-C. Enclose header files in an include guard
     |
| 245 S | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| 248 S | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 252 S | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| 296 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 299 S | 
     DCL05-C. Use typedefs of non-pointer types only
     |
| 302 S | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 323 S | 
     MSC40-C. Do not violate constraints
     |
| 324 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 326 S | 
     DCL31-C. Declare identifiers before using them
     |
| 329 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 329 S | 
     STR00-C. Represent characters using an appropriate type
     |
| 329 S | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 329 S | 
     STR09-C. Don't assume numeric values for expressions with type plain character
     |
| 331 S | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| 332 S | 
     INT02-C. Understand integer conversion rules
     |
| 334 S | 
     INT02-C. Understand integer conversion rules
     |
| 335 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 336 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 339 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 340 S | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| 341 S | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| 344 S | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| 345 S | 
     MSC40-C. Do not violate constraints
     |
| 355 S | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| 361 S | 
     EXP00-C. Use parentheses for precedence of operation
     |
| 376 S | 
     MSC10-C. Character encoding: UTF8-related issues
     |
| 382 S | 
     EXP12-C. Do not ignore values returned by functions
     |
| 385 S | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| 387 S | 
     MSC40-C. Do not violate constraints
     |
| 397 S | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| 400 S | 
     MEM35-C. Allocate sufficient memory for an object
     |
| 401 S | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| 403 S | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| 404 S | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| 404 S | 
     MSC40-C. Do not violate constraints
     |
| 404 S | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| 404 S | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| 406 S | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 407 S | 
     MEM34-C. Only free memory allocated dynamically
     |
| 408 S | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 412 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 427 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 428 S | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 428 S | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| 432 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 432 S | 
     STR00-C. Represent characters using an appropriate type
     |
| 432 S | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 433 S | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| 433 S | 
     EXP13-C. Treat relational and equality operators as if they were nonassociative
     |
| 433 S | 
     INT02-C. Understand integer conversion rules
     |
| 433 S | 
     MSC05-C. Do not manipulate time_t typed values directly
     |
| 434 S | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| 434 S | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| 434 S | 
     INT02-C. Understand integer conversion rules
     |
| 435 S | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 435 S | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| 435 S | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| 437 S | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| 438 S | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| 438 S | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 439 S | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| 440 S | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| 446 S | 
     INT02-C. Understand integer conversion rules
     |
| 450 S | 
     STR10-C. Do not concatenate different type of string literals
     |
| 452 S | 
     INT02-C. Understand integer conversion rules
     |
| 452 S | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| 457 S | 
     INT02-C. Understand integer conversion rules
     |
| 458 S | 
     INT02-C. Understand integer conversion rules
     |
| 458 S | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 458 S | 
     MSC05-C. Do not manipulate time_t typed values directly
     |
| 458 S | 
     STR04-C. Use plain char for characters in the basic character set
     |
| 461 S | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 465 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 476 S | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 479 S | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| 480 S | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 481 S | 
     MSC40-C. Do not violate constraints
     |
| 482 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 483 S | 
     MEM34-C. Only free memory allocated dynamically
     |
| 484 S | 
     MEM30-C. Do not access freed memory
     |
| 484 S | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| 486 S | 
     FIO47-C. Use valid format strings
     |
| 487 S | 
     MEM35-C. Allocate sufficient memory for an object
     |
| 488 S | 
     INT08-C. Verify that all integer values are in range
     |
| 489 S | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 489 S | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 489 S | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 489 S | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 489 S | 
     ARR00-C. Understand how arrays work
     |
| 493 S | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| 493 S | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| 493 S | 
     INT08-C. Verify that all integer values are in range
     |
| 493 S | 
     INT08-C. Verify that all integer values are in range
     |
| 494 S | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| 494 S | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| 496 S | 
     DCL31-C. Declare identifiers before using them
     |
| 496 S | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 497 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 510 S | 
     MSC21-C. Use robust loop termination conditions
     |
| 545 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 553 S | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| 554 S | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| 554 S | 
     EXP11-C. Do not make assumptions regarding the layout of structures with bit-fields
     |
| 562 S | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 562 S | 
     PRE12-C. Do not define unsafe macros
     |
| 565 S | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 567 S | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| 567 S | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| 567 S | 
     ARR00-C. Understand how arrays work
     |
| 568 S | 
     PRE04-C. Do not reuse a standard header file name
     |
| 572 S | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 572 S | 
     PRE12-C. Do not define unsafe macros
     |
| 573 S | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| 575 S | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 576 S | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| 576 S | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 578 S | 
     EXP03-C. Do not assume the size of a structure is the sum of the sizes of its members
     |
| 579 S | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| 580 S | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 580 S | 
     MSC40-C. Do not violate constraints
     |
| 582 S | 
     EXP40-C. Do not modify constant objects
     |
| 584 S | 
     INT10-C. Do not assume a positive remainder when using the % operator
     |
| 585 S | 
     INT14-C. Avoid performing bitwise and arithmetic operations on the same data
     |
| 586 S | 
     INT15-C. Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types
     |
| 587 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 588 S | 
     ENV33-C. Do not call system()
     |
| 588 S | 
     ENV03-C. Sanitize the environment when invoking external programs
     |
| 589 S | 
     FIO47-C. Use valid format strings
     |
| 589 S | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| 590 S | 
     FIO11-C. Take care when specifying the mode parameter of fopen()
     |
| 591 S | 
     FIO38-C. Do not copy a FILE object
     |
| 592 S | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| 592 S | 
     FIO10-C. Take care when using the rename() function
     |
| 593 S | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| 594 S | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| 600 S | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| 602 S | 
     STR06-C. Do not assume that strtok() leaves the parse string unchanged
     |
| 606 S | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| 608 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 611 S | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 612 S | 
     MSC40-C. Do not violate constraints
     |
| 613 S | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 615 S | 
     MSC40-C. Do not violate constraints
     |
| 618 S | 
     EXP42-C. Do not compare padding data
     |
| 618 S | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| 621 S | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| 623 S | 
     STR05-C. Use pointers to const when referring to string literals
     |
| 626 S | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 629 S | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| 630 S | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| 631 S | 
     EXP33-C. Do not read uninitialized memory
     |
| 634 S | 
     DCL09-C. Declare functions that return errno with a return type of errno_t
     |
| 637 S | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| 642 S | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| 642 S | 
     MSC15-C. Do not depend on undefined behavior
     |
| 644 S | 
     MEM34-C. Only free memory allocated dynamically
     |
| 645 S | 
     MEM34-C. Only free memory allocated dynamically
     |
| 646 S | 
     MSC40-C. Do not violate constraints
     |
| 648 S | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| 649 S | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| 650 S | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| 652 S | 
     EXP33-C. Do not read uninitialized memory
     |
| 652 S | 
     EXP34-C. Do not dereference null pointers
     |
| 653 S | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| 662 S | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| 663 S | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| I J | 
     MSC06-C. Beware of compiler optimizations
     |
| I J | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| Partially implemented | 
     PRE13-C. Use the Standard predefined macros to test for versions and features.
     |

