This section lists a snapshot of the CERT C Coding Standard guidelines in 2014 that are automatically checked by version 9.5.1 of the LDRA tool suite.

| Guidelines Definition | Total |
| ----|----|
| Implemented by LDRA | 75 |
| Enhanced Enforcement of rule by LDRA | 47 |
| Partially implemented by LDRA | 78 |
| Not yet implemented by LDRA | 22 |
| Deemed to be not statically analyzable by a tool | 42 |
| Total | 264 |


| CERT C PRE Guideline | Description |
| ----|----|
| PRE00-C | Prefer inline or static functions to function-like macros |
| PRE01-C | Use parentheses within macros around parameter names |
| PRE02-C | Macro replacement lists should be parenthesized |
| PRE03-C | Prefer typedefs to defines for encoding types |
| PRE04-C | Do not reuse a standard header file name |
| PRE05-C | Understand macro replacement when concatenating tokens or performing stringification |
| PRE06-C | Enclose header file in an inclusion guard |
| PRE07-C | Avoid using repeated question marks |
| PRE08-C | Guarantee that header filenames are unique |
| PRE09-C | Do not replace secure functions with less secure functions |
| PRE10-C | Wrap multistatement macros in a do-while loop |
| PRE11-C | Do not conclude macro definitions with a semicolon |
| PRE12-C | Do not define unsafe macros |
| PRE13-C | Use the Standard predefined macros to test for versions and features. |
| PRE30-C | Do not create a universal character name through concatenation |
| PRE31-C | Avoid side effects in arguments to unsafe macros |
| PRE32-C | Do not use preprocessor directives in invocations of function-like macros |


| CERT C DCL Guideline | Description |
| ----|----|
| DCL00-C | Const-qualify immutable objects |
| DCL01-C | Do not reuse variable names in subscopes |
| DCL02-C | Use visually distinct identifiers |
| DCL03-C | Use a static assertion to test the value of a constant expression |
| DCL04-C | Do not declare more than one variable per declaration |
| DCL05-C | Use typedefs of non-pointer types only |
| DCL06-C | Use meaningful symbolic constants to represent literal values in program logic |
| DCL07-C | Include the appropriate type information in function declarators |
| DCL08-C | Properly encode relationships in constant definitions |
| DCL09-C | Declare functions that return an errno with a return type of errno_t |
| DCL10-C | Maintain the contract between the writer and caller of variadic functions |
| DCL11-C | Understand the type issues associated with variadic functions |
| DCL12-C | Implement abstract data types using opaque types |
| DCL13-C | Declare function parameters that are pointers to values not changed by the function as const |
| DCL15-C | Declare objects that do not need external linkage with storage-class specifier static |
| DCL16-C | Use "L," not "l," to indicate a long value |
| DCL17-C | Beware of miscompiled volatile-qualified variables |
| DCL18-C | Do not begin integer constants with 0 when specifying a decimal value |
| DCL19C | Minimize the scope of variables and functions |
| DCL20-C | Explicitly specify void when a function accepts no arguments |
| DCL21-C | Understand the storage of compound literals |
| DLC22-C | Use volatile for data that cannot be cached |
| DCL23-C | Guarantee that mutually visible identifiers are unique |
| DCL30-C | Declare objects with appropriate storage durations |
| DCL31-C | Declare identifiers before using them |
| DCL36-C | Do not declare an identifier with conflicting linkage classifications |
| DCL37-C | Do not declare or define a reserved identifier |
| DCL38-C | Use the correct syntax when declaring flexible array members |
| DCL39-C | Avoid information leak in structure padding |
| DCL40-C | Do not create incompatible declarations of the same function or object |
| DCL41-C | Do not declare variables inside a switch statement before the first case label |


| CERT C EXP Guideline | Description |
| ----|----|
| EXP00-C | Use parentheses for precedence of operation |
| EXP02-C | Be aware of the short-circuit behavior of the logical AND and OR operators |
| EXP03-C | Do not assume the size of a structure is the sum of the of the sizes of its members |
| EXP05-C | Do not cast away a const qualification |
| EXP07-C | Do not diminish the benefits of constants by assuming their values in expressions |
| EXP08-C | Ensure pointer arithmetic is used correctly |
| EXP09-C | Use sizeof to determine the size of a type or variable |
| EXP10-C | Do not depend on the order of evaluation of subexpressions or the order in which side effects take place |
| EXP11-C | Do not make assumptions regarding the layout of structures with bit-fields |
| EXP12-C | Do not ignore values returned by functions |
| EXP13-C | Treat relational and equality operators as if they were nonassociative |
| EXP15-C | Do not place a semicolon on the same line as an if, for, or while statement |
| EXP16-C | Do not compare function pointers to constant values |
| EXP19-C | Use braces for the body of an if, for, or while statement |
| EXP20-C | Perform explicit tests to determine success, true and false, and equality |
| EXP30-C | Do not depend on order of evaluation between sequence points |
| EXP32-C | Do not access a volatile object through a nonvolatile reference |
| EXP33-C | Do not read uninitialized memory |
| EXP34-C | Do not dereference null pointers |
| EXP35-C | Do not modify objects with temporary lifetime |
| EXP36-C | Do not cast pointers into more strictly aligned pointer types |
| EXP37-C | Call functions with the correct number and type of arguments |
| EXP39-C | Do not access a variable through a pointer of an incompatible type |
| EXP40-C | Do not modify constant objects |
| EXP42-C | Do not compare padding data |
| EXP43-C | Avoid undefined behaviors when using restrict-qualified pointers |
| EXP44-C | Do not rely on side effects in operands to sizeof, _Alignof, or _Generic |
| EXP45-C | Do not perform assignments in selection statements |
| EXP46-C | Do not use a bitwise operator with a Boolean-like operand |


| CERT C INT Guideline | Description |
| ----|----|
| INT00-C | Understand the data model used by your implementation(s) |
| INT01-C | Use rsize_t or size_t for all integer values representing the size of an object |
| INT02-C | Understand integer conversion rules |
| INT04-C | Enforce limits on integer values originating from untrusted sources |
| INT05-C | Do not use input functions to convert character data if they cannot handle all possible inputs |
| INT06-C | Use strtol() or a related function to convert a string token to an integer |
| INT07-C | Use only explicitly signed or unsigned char type for numeric values |
| INT08-C | Verify that all integer values are in range |
| INT09-C | Ensure enumeration constants map to unique values |
| INT10-C | Do not assume a positive remainder when using the % operator |
| INT12-C | Do not make assumptions about the type of a plain int bit-field when used in an expression |
| INT13-C | Use bitwise operators only on unsigned operands |
| INT14-C | Avoid performing bitwise and arithmetic operations on the same data |
| INT15-C | Use intmax_t or uintmax_t for formatted I/O on programmer-defined integer types |
| INT16-C | Do not make assumptions about representation of signed integers |
| INT17-C | Define integer constants in an implementation-independent manner |
| INT18-C | Evaluate integer expressions in a larger size before comparing or assigning to that size |
| INT30-C | Ensure that unsigned integer operations do not wrap |
| INT31-C | Ensure that integer conversions do not result in lost or misinterpreted data |
| INT32-C | Ensure that integer operations on signed integers do not result in an overflow |
| INT33-C | Ensure that division and modulo operations do not result in divide-by-zero errors |
| INT34-C | Do not shift a negative number of bits or more bits than exist in the operand |
| INT35-C | Use correct integer precisions |
| INT36-C | Converting a pointer to integer or integer to pointer |


| CERT C FLP Guideline | Description |
| ----|----|
| FLP00-C | Understand the limitations of floating-point numbers |
| FLP01-C | Take care in rearranging floating point expressions |
| FLP02-C | Avoid using floating-point numbers when precise computation is needed |
| FLP03-C | Detect and handle floating-point errors |
| FLP04-C | Check floating-point inputs for exceptional values |
| FLP05C | Don't use denormalized numbers |
| FLP06-C | Convert integers to floating point for floating-point operations |
| FLP07-C | Cast the return value of a function that returns a floating-point type |
| FLP30-C | Do not use floating-point variables as loop counters |
| FLP32-C | Prevent or detect domain and range errors in math functions |
| FLP34-C | Ensure that floating-point conversions are within range of the new type |
| FLP36-C | Preserve precision when converting integral values to floating-point type |
| FLP37-C | Do not use object representations to compare floating-point values |


| CERT C ARR Guideline | Description |
| ----|----|
| ARR00-C | Understand how arrays work |
| ARR01-C | Do not apply the size of operator to a pointer when taking the size of an array |
| ARR02-C | Explicitly specify array bounds, even if implicitly defined by an initializer |
| ARR30-C | Do not form or use out-of-bounds pointers or array subscripts |
| ARR31-C | Use consistent array notation across all source files |
| ARR32-C | Ensure size arguments for variable length arrays are in a valid range |
| ARR36-C | Do not subtract or compare two pointers that do not refer to the same array |
| ARR37-C | Do not add or subtract an integer to a pointer to a non-array object |
| ARR38-C | Guarantee that library functions do not form invalid pointers |
| ARR39-C | Do not add or subtract a scaled integer to a pointer |


| CERT C STR Guideline | Description |
| ----|----|
| STR00-C | Represent characters using an appropriate type |
| STR01-C | Adopt and implement a consistent plan for managing strings |
| STR02-C | Sanitize data passed to complex subsystems |
| STR03-C | Do not inadvertently truncate a null-terminated byte string |
| STR04-C | Use plain char for characters in the basic character set |
| STR05-C | Use pointers to const when referring to string literals |
| STR06-C | Do not assume that strtok() leaves the parse string unchanged |
| STR07-C | Use the bounds-checking interfaces for string manipulation |
| STR09-C | Don't assume numeric values for expressions with type plain character |
| STR10-C | Do not concatenate different type of string literals |
| STR11-C | Do not specify the bound of a character array initialized with a string literal |
| STR30-C | Do not attempt to modify string literals |
| STR31-C | Guarantee that storage for strings has sufficient space for character data and the null terminator |
| STR32-C | Do not pass a non-null-terminated character sequence to a library function that expects a string |
| STR34-C | Cast characters to unsigned types before converting to larger integer sizes |
| STR37-C | Arguments to character-handling functions must be representable as an unsigned char |
| STR38-C | Do not confuse narrow and wide character strings and functions |


| CERT C MEM Guideline | Description |
| ----|----|
| MEM00-C | Allocate and free memory in the same module at the same level of abstraction |
| MEM01-C | Store a new value in pointers immediately after free() |
| MEM02-C | Immediately cast the result of a memory allocation function call into a pointer to the allocated type |
| MEM03-C | Clear sensitive information stored in reusable resources returned for reuse |
| MEM04-C | Do not perform zero-length allocations |
| MEM05-C | Avoid large stack allocations |
| MEM06-C | Ensure that sensitive data is not written out to disk |
| MEM07-C | Ensure that the arguments to calloc(), when multiplied, do not wrap |
| MEM10-C | Define and use a pointer validation function |
| MEM11-C | Do not assume infinite heap space |
| MEM12-C | Consider using a goto chain when leaving a function on error when using and releasing resources |
| MEM30-C | Do not access freed memory |
| MEM31-C | Free dynamically allocated memory exactly once |
| MEM33-C | Allocate and copy structures containing a flexible array member dynamically |
| MEM34-C | Only free memory allocated dynamically |
| MEM35-C | Allocate sufficient memory for an object |
| MEM36-C | Do not modify the alignment of objects by calling realloc() |


| CERT C FIO Guideline | Description |
| ----|----|
| FIO01-C | Be careful using functions that use file names for identification |
| FIO02-C | Canonicalize path names originating from untrusted sources |
| FIO03-C | Do not make assumptions about fopen() and file creation |
| FIO05-C | Identify files using multiple file attributes |
| FIO06-C | Create files with appropriate access permissions |
| FIO08-C | Take care when calling remove() on an open file |
| FIO09-C | Be careful with binary data when transferring data across systems |
| FIO10-C | Take care when using the rename() function |
| FIO11-C | Take care when specifying the mode parameter of fopen() |
| FIO13-C | Never push back anything other than one read character |
| FIO14-C | Understand the difference between text mode and binary mode with file streams |
| FIO15-C | Ensure that file operations are performed in a secure directory |
| FIO17-C | Do not rely on an ending null character when using fread() |
| FIO18-C | Never expect fwrite() to terminate the writing process at a null character |
| FIO19-C | Do not use fseek() and ftell() to compute the size of a regular file |
| FIO20-C | Avoid unintentional truncation when using fgets() or fgetws() |
| FIO21-C | Do not create temporary files in shared directories |
| FIO22-C | Close files before spawning processes |
| FIO23-C | Do not exit with unflushed data in stdout or stderr |
| FIO30-C | Exclude user input from format strings |
| FIO31-C | Do not open a file that is already open |
| FIO32-C | Do not perform operations on devices that are only appropriate for files |
| FIO37-C | Do not assume that fgets() or fgetws() returns a nonempty string when successful |
| FIO38-C | Do not copy a FILE object |
| FIO39-C | Do not alternately input and output from a stream without an intervening flush or positioning call |
| FIO40-C | Reset strings on fgets() or fgetws() failure |
| FIO41-C | Do not call getc(), putc(), getwc(), or putwc() with stream arguments that have side effects |
| FIO42-C | Close files when they are no longer needed |
| FIO44-C | Only use values for fsetpos() that are returned from fgetpos() |
| FIO45-C | Avoid TOCTOU race conditions while accessing files |
| FIO46-C | Do not access a closed file |
| FIO47-C | Use valid format strings |


| CERT C ENV Guideline |  Description |
| ----|----|
| ENV01-C | Do not make assumptions about the size of an environment variable |
| ENV02-C | Beware of multiple environment variables with the same effective name |
| ENV03-C | Sanitize the environment before external programs |
| ENV30-C | Do not modify the object referenced by the return value of certain functions |
| ENV31-C | Do not rely on an environment pointer following an operation that may invalidate it |
| ENV32-C | All exit handlers must return normally |
| ENV33-C | Do not call system() |
| ENV34-C | Do not store pointers returned by certain functions |


| CERT C SIG Guideline | Description |
| ----|----|
| SIG00-C | Mask signals handled by noninterruptable signal handlers |
| SIG01-C | Understand implementation-specific details regarding signal handler persistence |
| SIG02-C | Avoid using signals to implement normal functionality |
| SIG30-C | Call only asynchronous-safe functions within signal handlers |
| SIG31-C | Do not access shared objects in signal handlers |
| SIG34-C | Do not call signal() from within interruptable signal handlers |
| SIG35-C | Do not return from a computational exception signal handler |


|  |  |
| ----|----|
| CERT C ERR Guideline | Description |
| ERR00-C | Adopt and implement a consistent and comprehensive error handling policy |
| ERR01-C | Use ferror() rather than errno to check for FILE stream errors |
| ERR02-C | Avoid in-band error indicators |
| ERR03-C | Use runtime-constraint handlers when calling functions defined by TR31-1 |
| ERR04-C | Choose an appropriate termination strategy |
| ERR05-C | Application-independent code should provide error detection without dictating error handling |
| ERR06-C | Understand the termination behavior of assert() and abort() |
| ERR07-C | Prefer functions that support error checking over equivalent functions that don't |
| ERR30-C | Set errno to zero before calling a library function known to set errno, and check errno only after the function returns a value indicating failure |
| ERR32-C | Do not rely on indeterminate values of errno |
| ERR33-C | Detect and handle standard library errors |


| CERT C MSC Guideline | Description |
| ----|----|
| MSC00-C | Compile cleanly at high warning levels |
| MSC01-C | Strive for logical completeness |
| MSC04-C | Use comments consistently and in a readable fashion |
| MSC05-C | Do not manipulate time_t typed values directly |
| MSC06-C | Beware of compiler optimizations |
| MSC09-C | Character Encoding - Use Subset of ASCII for Safety |
| MSC10-C | Character Encoding - UTF8 Related Issues |
| MSC11-C | Incorporate diagnostic tests using assertions |
| MSC12-C | Detect and remove code that has no effect or is never executed |
| MSC13-C | Detect and remove unused values |
| MSC14-C | Do not introduce unnecessary platform dependencies |
| MSC15-C | Do not depend on undefined behavior |
| MSC17-C | Finish every set of statements associated with a case label with a break statement |
| MSC18-C | Be careful while handling sensitive data, such as passwords, in program code |
| MSC19-C | For functions that return an array, prefer returning an empty array over a null value |
| MSC20-C | Do not use a switch statement to transfer control into a complex block |
| MSC21-C | Use robust loop termination conditions |
| MSC22-C | Use the setjmp(), longjmp() facility securely |
| MSC23-C | Beware of vendor-specific library and language differences |
| MSC24-C | Do not use deprecated or obsolescent functions |
| MSC30-C | Do not use the rand function;for generating pseudorandom numbers |
| MSC32-C | Properly seed pseudorandom number generators |
| MSC33-C | Do not pass invalid data to the asctime() function |
| MSC37-C | Ensure that control never reaches the end of a non-void function |
| MSC38-C | Do not treat a predefined identifier as an object if it might only be implemented as a macro |
| MSC39-C | Do not call va_arg() on a va_list that has an indeterminate value |
| MSC40-C | Do not violate constraints |


| CERT C POS Guideline | Description |
| ----|----|
| POS01-C | Check for the existence of links when dealing with files |
| POS02-C | Follow the principle of least privilege |
| POS04-C | Avoid using PTHREAD_MUTEX_NORMAL type mutex locks |
| POS05-C | Limit access to files by creating a jail |
| POS30-C | Use the readlink() function properly |
| POS33-C | Do not use vfork() |
| POS34-C | Do not call putenv() with a pointer to an automatic variable as the argument |
| POS35-C | Avoid race conditions while checking for the existence of a symbolic link |
| POS36-C | Observe correct revocation order while relinquishing privileges |
| POS37-C | Ensure that privilege relinquishment is successful |
| POS38-C | Beware of race conditions when using fork and file descriptors |
| POS39-C | Use the correct byte ordering when transferring data between systems |
| POS44-C | Do not use signals to terminate threads |
| POS47-C | Do not use threads that can be canceled asynchronously |
| POS48-C | Do not unlock or destroy another POSIX thread's mutex |
| POS49-C | When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed |
| POS50-C | Declare objects shared between POSIX threads with appropriate storage durations |
| POS51-C | Avoid deadlock with POSIX threads by locking in predefined order |
| POS52-C | Do not perform operations that can block while holding a POSIX lock |
| POS53-C | Do not use more than one mutex for concurrent waiting operations on a condition variable |
| POS54-C | Detect and handle POSIX library errors |

Disclaimer: The information on this page was provided directly by the vendor and has not been validated by CERT.  
## Comments:

|  |
| ----|
| In two weeks, this page will be moved to 6 The Void, as it has been obsolesced by the;LDRA page.
                                        Posted by svoboda at Jul 31, 2019 16:37
                                     |

