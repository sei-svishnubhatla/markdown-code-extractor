> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 2024.2

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| CERT_C-API00-a | 
     API00-C. Functions should validate their parameters
     |
| CERT_C-API01-a | 
     API01-C. Avoid laying out strings in memory directly before sensitive data
     |
| CERT_C-API01-b | 
     API01-C. Avoid laying out strings in memory directly before sensitive data
     |
| CERT_C-API02-a | 
     API02-C. Functions that read or write to or from an array should take an argument to specify the source or target size
     |
| CERT_C-API02-b | 
     API02-C. Functions that read or write to or from an array should take an argument to specify the source or target size
     |
| CERT_C-ARR01-a | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| CERT_C-ARR02-a | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| CERT_C-ARR30-a | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| CERT_C-ARR32-a | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| CERT_C-ARR36-a | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| CERT_C-ARR36-b | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| CERT_C-ARR37-a | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| CERT_C-ARR38-a | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| CERT_C-ARR38-b | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| CERT_C-ARR38-c | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| CERT_C-ARR38-d | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| CERT_C-ARR39-a | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| CERT_C-ARR39-b | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| CERT_C-ARR39-c | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| CERT_C-CON01-a | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| CERT_C-CON02-a | 
     CON02-C. Do not use volatile as a synchronization primitive
     |
| CERT_C-CON05-a | 
     CON05-C. Do not perform operations that can block while holding a lock
     |
| CERT_C-CON30-a | 
     CON30-C. Clean up thread-specific storage
     |
| CERT_C-CON31-a | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| CERT_C-CON31-b | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| CERT_C-CON31-c | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| CERT_C-CON32-a | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| CERT_C-CON33-a | 
     CON33-C. Avoid race conditions when using library functions
     |
| CERT_C-CON34-a | 
     CON34-C. Declare objects shared between threads with appropriate storage durations
     |
| CERT_C-CON35-a | 
     CON35-C. Avoid deadlock by locking in a predefined order
     |
| CERT_C-CON36-a | 
     CON36-C. Wrap functions that can spuriously wake up in a loop
     |
| CERT_C-CON37-a | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| CERT_C-CON38-a | 
     CON38-C. Preserve thread safety and liveness when using condition variables
     |
| CERT_C-CON39-a | 
     CON39-C. Do not join or detach a thread that was previously joined or detached
     |
| CERT_C-CON40-a | 
     CON40-C. Do not refer to an atomic variable twice in an expression
     |
| CERT_C-CON41-a | 
     CON41-C. Wrap functions that can fail spuriously in a loop
     |
| CERT_C-CON43-a | 
     CON43-C. Do not allow data races in multithreaded code
     |
| CERT_C-DCL00-a | 
     DCL00-C. Const-qualify immutable objects
     |
| CERT_C-DCL00-b | 
     DCL00-C. Const-qualify immutable objects
     |
| CERT_C-DCL01-a | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| CERT_C-DCL01-b | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| CERT_C-DCL02-a | 
     DCL02-C. Use visually distinct identifiers
     |
| CERT_C-DCL04-a | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| CERT_C-DCL05-a | 
     DCL05-C. Use typedefs of non-pointer types only
     |
| CERT_C-DCL06-a | 
     DCL06-C. Use meaningful symbolic constants to represent literal values
     |
| CERT_C-DCL10-a | 
     DCL10-C. Maintain the contract between the writer and caller of variadic functions
     |
| CERT_C-DCL11-a | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL11-b | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL11-c | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL11-d | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL11-e | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL11-f | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| CERT_C-DCL12-a | 
     DCL12-C. Implement abstract data types using opaque types
     |
| CERT_C-DCL13-a | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| CERT_C-DCL15-a | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| CERT_C-DCL16-a | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| CERT_C-DCL18-a | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| CERT_C-DCL18-b | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| CERT_C-DCL19-a | 
     DCL19-C. Minimize the scope of variables and functions
     |
| CERT_C-DCL20-a | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| CERT_C-DCL22-a | 
     DCL22-C. Use volatile for data that cannot be cached
     |
| CERT_C-DCL30-a | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| CERT_C-DCL30-b | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| CERT_C-DCL31-a | 
     DCL31-C. Declare identifiers before using them
     |
| CERT_C-DCL36-a | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| CERT_C-DCL37-b | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL37-c | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL37-d | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL37-e | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL37-f | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL37-g | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| CERT_C-DCL38-a | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| CERT_C-DCL39-a | 
     DCL39-C. Avoid information leakage when passing a structure across a trust boundary
     |
| CERT_C-DCL40-a | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| CERT_C-DCL40-b | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| CERT_C-DCL41-a | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| CERT_C-ENV01-a | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| CERT_C-ENV01-b | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| CERT_C-ENV01-c | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| CERT_C-ENV02-a | 
     ENV02-C. Beware of multiple environment variables with the same effective name
     |
| CERT_C-ENV30-a | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| CERT_C-ENV31-a | 
     ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it
     |
| CERT_C-ENV32-a | 
     ENV32-C. All exit handlers must return normally
     |
| CERT_C-ENV33-a | 
     ENV33-C. Do not call system()
     |
| CERT_C-ENV34-a | 
     ENV34-C. Do not store pointers returned by certain functions
     |
| CERT_C-ERR01-a | 
     ERR01-C. Use ferror() rather than errno to check for FILE stream errors
     |
| CERT_C-ERR02-a | 
     ERR02-C. Avoid in-band error indicators
     |
| CERT_C-ERR04-a | 
     ERR04-C. Choose an appropriate termination strategy
     |
| CERT_C-ERR04-b | 
     ERR04-C. Choose an appropriate termination strategy
     |
| CERT_C-ERR04-c | 
     ERR04-C. Choose an appropriate termination strategy
     |
| CERT_C-ERR05-a | 
     ERR05-C. Application-independent code should provide error detection without dictating error handling
     |
| CERT_C-ERR05-b | 
     ERR05-C. Application-independent code should provide error detection without dictating error handling
     |
| CERT_C-ERR05-c | 
     ERR05-C. Application-independent code should provide error detection without dictating error handling
     |
| CERT_C-ERR06-a | 
     ERR06-C. Understand the termination behavior of assert() and abort()
     |
| CERT_C-ERR07-a | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| CERT_C-ERR07-b | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| CERT_C-ERR30-a | 
     ERR30-C. Take care when reading errno
     |
| CERT_C-ERR32-b | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| CERT_C-ERR33-a | 
     ERR33-C. Detect and handle standard library errors
     |
| CERT_C-ERR33-d | 
     ERR33-C. Detect and handle standard library errors
     |
| CERT_C-ERR33-e | 
     ERR33-C. Detect and handle standard library errors
     |
| CERT_C-ERR34-a | 
     ERR34-C. Detect errors when converting a string to a number
     |
| CERT_C-EXP00-a | 
     EXP00-C. Use parentheses for precedence of operation
     |
| CERT_C-EXP02-a | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| CERT_C-EXP05-a | 
     EXP05-C. Do not cast away a const qualification
     |
| CERT_C-EXP08-a | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| CERT_C-EXP08-b | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| CERT_C-EXP10-a | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| CERT_C-EXP10-b | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| CERT_C-EXP10-c | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| CERT_C-EXP10-d | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| CERT_C-EXP12-a | 
     EXP12-C. Do not ignore values returned by functions
     |
| CERT_C-EXP12-b | 
     EXP12-C. Do not ignore values returned by functions
     |
| CERT_C-EXP14-a | 
     EXP14-C. Beware of integer promotion when performing bitwise operations on integer types smaller than int
     |
| CERT_C-EXP15-a | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| CERT_C-EXP16-a | 
     EXP16-C. Do not compare function pointers to constant values
     |
| CERT_C-EXP19-a | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| CERT_C-EXP20-a | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| CERT_C-EXP20-b | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| CERT_C-EXP30-a | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| CERT_C-EXP30-b | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| CERT_C-EXP30-c | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| CERT_C-EXP30-d | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| CERT_C-EXP32-a | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| CERT_C-EXP33-a | 
     EXP33-C. Do not read uninitialized memory
     |
| CERT_C-EXP34-a | 
     EXP34-C. Do not dereference null pointers
     |
| CERT_C-EXP35-a | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| CERT_C-EXP36-a | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| CERT_C-EXP37-a | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| CERT_C-EXP37-b | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| CERT_C-EXP37-d | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| CERT_C-EXP39-a | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP39-b | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP39-c | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP39-d | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP39-e | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP39-f | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| CERT_C-EXP40-a | 
     EXP40-C. Do not modify constant objects
     |
| CERT_C-EXP42-a | 
     EXP42-C. Do not compare padding data
     |
| CERT_C-EXP43-a | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| CERT_C-EXP44-a | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| CERT_C-EXP44-b | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| CERT_C-EXP45-b | 
     EXP45-C. Do not perform assignments in selection statements
     |
| CERT_C-EXP45-d | 
     EXP45-C. Do not perform assignments in selection statements
     |
| CERT_C-EXP46-b | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| CERT_C-EXP47-a | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| CERT_C-FIO01-a | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| CERT_C-FIO01-c | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| CERT_C-FIO21-b | 
     FIO21-C. Do not create temporary files in shared directories
     |
| CERT_C-FIO22-a | 
     FIO22-C. Close files before spawning processes
     |
| CERT_C-FIO24-a | 
     FIO24-C. Do not open a file that is already open
     |
| CERT_C-FIO30-a | 
     FIO30-C. Exclude user input from format strings
     |
| CERT_C-FIO30-b | 
     FIO30-C. Exclude user input from format strings
     |
| CERT_C-FIO30-c | 
     FIO30-C. Exclude user input from format strings
     |
| CERT_C-FIO32-a | 
     FIO32-C. Do not perform operations on devices that are only appropriate for files
     |
| CERT_C-FIO34-a | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| CERT_C-FIO37-a | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| CERT_C-FIO38-a | 
     FIO38-C. Do not copy a FILE object
     |
| CERT_C-FIO39-a | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| CERT_C-FIO40-a | 
     FIO40-C. Reset strings on fgets()  or fgetws() failure
     |
| CERT_C-FIO41-a | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| CERT_C-FIO41-b | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| CERT_C-FIO42-a | 
     FIO42-C. Close files when they are no longer needed
     |
| CERT_C-FIO44-a | 
     FIO44-C. Only use values for fsetpos() that are returned from fgetpos()
     |
| CERT_C-FIO45-a | 
     FIO45-C. Avoid TOCTOU race conditions while accessing files
     |
| CERT_C-FIO46-a | 
     FIO46-C. Do not access a closed file
     |
| CERT_C-FIO47-a | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FIO47-b | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FIO47-c | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FIO47-d | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FIO47-e | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FIO47-f | 
     FIO47-C. Use valid format strings
     |
| CERT_C-FLP00-a | 
     FLP00-C. Understand the limitations of floating-point numbers
     |
| CERT_C-FLP02-a | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| CERT_C-FLP03-a | 
     FLP03-C. Detect and handle floating-point errors
     |
| CERT_C-FLP03-b | 
     FLP03-C. Detect and handle floating-point errors
     |
| CERT_C-FLP03-c | 
     FLP03-C. Detect and handle floating-point errors
     |
| CERT_C-FLP03-d | 
     FLP03-C. Detect and handle floating-point errors
     |
| CERT_C-FLP06-a | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| CERT_C-FLP06-b | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| CERT_C-FLP30-a | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| CERT_C-FLP32-a | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| CERT_C-FLP34-a | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| CERT_C-FLP34-b | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| CERT_C-FLP36-a | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| CERT_C-FLP36-b | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| CERT_C-FLP37-c | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| CERT_C-INT02-a | 
     INT02-C. Understand integer conversion rules
     |
| CERT_C-INT02-b | 
     INT02-C. Understand integer conversion rules
     |
| CERT_C-INT04-a | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| CERT_C-INT04-b | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| CERT_C-INT04-c | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| CERT_C-INT05-a | 
     INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs
     |
| CERT_C-INT07-a | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| CERT_C-INT07-b | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| CERT_C-INT08-a | 
     INT08-C. Verify that all integer values are in range
     |
| CERT_C-INT08-b | 
     INT08-C. Verify that all integer values are in range
     |
| CERT_C-INT08-c | 
     INT08-C. Verify that all integer values are in range
     |
| CERT_C-INT08-d | 
     INT08-C. Verify that all integer values are in range
     |
| CERT_C-INT09-a | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| CERT_C-INT10-a | 
     INT10-C. Do not assume a positive remainder when using the % operator
     |
| CERT_C-INT12-a | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| CERT_C-INT13-a | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| CERT_C-INT13-b | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| CERT_C-INT15-a | 
     INT15-C. Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types
     |
| CERT_C-INT16-a | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| CERT_C-INT16-b | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| CERT_C-INT18-a | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| CERT_C-INT18-b | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| CERT_C-INT18-c | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| CERT_C-INT30-a | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| CERT_C-INT30-b | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| CERT_C-INT30-c | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| CERT_C-INT31-a | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-b | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-c | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-d | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-e | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-f | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-g | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-h | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-i | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-j | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-k | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-l | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-m | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-n | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-o | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT31-p | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| CERT_C-INT32-a | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| CERT_C-INT32-b | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| CERT_C-INT32-c | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| CERT_C-INT33-a | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| CERT_C-INT34-a | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| CERT_C-INT35-a | 
     INT35-C. Use correct integer precisions
     |
| CERT_C-INT36-b | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| CERT_C-MEM00-a | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| CERT_C-MEM00-b | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| CERT_C-MEM00-c | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| CERT_C-MEM00-d | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| CERT_C-MEM00-e | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| CERT_C-MEM01-a | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| CERT_C-MEM01-b | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| CERT_C-MEM01-c | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| CERT_C-MEM01-d | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| CERT_C-MEM02-a | 
     MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type
     |
| CERT_C-MEM02-b | 
     MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type
     |
| CERT_C-MEM03-a | 
     MEM03-C. Clear sensitive information stored in reusable resources
     |
| CERT_C-MEM04-a | 
     MEM04-C. Beware of zero-length allocations
     |
| CERT_C-MEM05-a | 
     MEM05-C. Avoid large stack allocations
     |
| CERT_C-MEM05-b | 
     MEM05-C. Avoid large stack allocations
     |
| CERT_C-MEM07-a | 
     MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap
     |
| CERT_C-MEM12-a | 
     MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources
     |
| CERT_C-MEM30-a | 
     MEM30-C. Do not access freed memory
     |
| CERT_C-MEM31-a | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| CERT_C-MEM33-a | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| CERT_C-MEM33-b | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| CERT_C-MEM34-a | 
     MEM34-C. Only free memory allocated dynamically
     |
| CERT_C-MEM35-a | 
     MEM35-C. Allocate sufficient memory for an object
     |
| CERT_C-MEM36-a | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| CERT_C-MSC01-a | 
     MSC01-C. Strive for logical completeness
     |
| CERT_C-MSC01-b | 
     MSC01-C. Strive for logical completeness
     |
| CERT_C-MSC04-a | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| CERT_C-MSC04-b | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| CERT_C-MSC04-c | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| CERT_C-MSC04-d | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| CERT_C-MSC06-a | 
     MSC06-C. Beware of compiler optimizations
     |
| CERT_C-MSC07-a | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-b | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-c | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-d | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-e | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-f | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-g | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-h | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC07-i | 
     MSC07-C. Detect and remove dead code
     |
| CERT_C-MSC09-a | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| CERT_C-MSC11-a | 
     MSC11-C. Incorporate diagnostic tests using assertions
     |
| CERT_C-MSC12-a | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-b | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-c | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-d | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-e | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-f | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-g | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-h | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-i | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-j | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC12-k | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| CERT_C-MSC13-a | 
     MSC13-C. Detect and remove unused values
     |
| CERT_C-MSC14-a | 
     MSC14-C. Do not introduce unnecessary platform dependencies
     |
| CERT_C-MSC14-b | 
     MSC14-C. Do not introduce unnecessary platform dependencies
     |
| CERT_C-MSC15-a | 
     MSC15-C. Do not depend on undefined behavior
     |
| CERT_C-MSC15-b | 
     MSC15-C. Do not depend on undefined behavior
     |
| CERT_C-MSC17-a | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| CERT_C-MSC19-a | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| CERT_C-MSC19-b | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| CERT_C-MSC22-a | 
     MSC22-C. Use the setjmp(), longjmp() facility securely
     |
| CERT_C-MSC24-a | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| CERT_C-MSC24-b | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| CERT_C-MSC24-c | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| CERT_C-MSC24-d | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| CERT_C-MSC30-a | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| CERT_C-MSC32-d | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| CERT_C-MSC33-a | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| CERT_C-MSC37-a | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| CERT_C-MSC38-a | 
     MSC38-C. Do not treat a predefined identifier as an object if it might only be implemented as a macro
     |
| CERT_C-MSC39-a | 
     MSC39-C. Do not call va_arg() on a va_list that has an indeterminate value
     |
| CERT_C-MSC40-a | 
     MSC40-C. Do not violate constraints
     |
| CERT_C-MSC41-a | 
     MSC41-C. Never hard code sensitive information
     |
| CERT_C-POS30-a | 
     POS30-C. Use the readlink() function properly
     |
| CERT_C-POS30-b | 
     POS30-C. Use the readlink() function properly
     |
| CERT_C-POS30-c | 
     POS30-C. Use the readlink() function properly
     |
| CERT_C-POS34-a | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| CERT_C-POS34-b | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| CERT_C-POS35-b | 
     POS35-C. Avoid race conditions while checking for the existence of a symbolic link
     |
| CERT_C-POS36-a | 
     POS36-C. Observe correct revocation order while relinquishing privileges
     |
| CERT_C-POS37-a | 
     POS37-C. Ensure that privilege relinquishment is successful
     |
| CERT_C-POS38-a | 
     POS38-C. Beware of race conditions when using fork and file descriptors
     |
| CERT_C-POS39-a | 
     POS39-C. Use the correct byte ordering when transferring data between systems
     |
| CERT_C-POS44-a | 
     POS44-C. Do not use signals to terminate threads
     |
| CERT_C-POS47-a | 
     POS47-C. Do not use threads that can be canceled asynchronously
     |
| CERT_C-POS48-a | 
     POS48-C. Do not unlock or destroy another POSIX thread's mutex
     |
| CERT_C-POS48-b | 
     POS48-C. Do not unlock or destroy another POSIX thread's mutex
     |
| CERT_C-POS49-a | 
     POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
     |
| CERT_C-POS50-a | 
     POS50-C. Declare objects shared between POSIX threads with appropriate storage durations
     |
| CERT_C-POS51-a | 
     POS51-C. Avoid deadlock with POSIX threads by locking in predefined order
     |
| CERT_C-POS52-a | 
     POS52-C. Do not perform operations that can block while holding a POSIX lock
     |
| CERT_C-POS53-a | 
     POS53-C. Do not use more than one mutex for concurrent waiting operations on a condition variable
     |
| CERT_C-POS54-a | 
     POS54-C. Detect and handle POSIX library errors
     |
| CERT_C-PRE00-a | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| CERT_C-PRE01-a | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| CERT_C-PRE02-a | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| CERT_C-PRE06-a | 
     PRE06-C. Enclose header files in an include guard
     |
| CERT_C-PRE07-a | 
     PRE07-C. Avoid using repeated question marks
     |
| CERT_C-PRE30-a | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| CERT_C-PRE31-b | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| CERT_C-PRE31-c | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| CERT_C-PRE31-d | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| CERT_C-PRE32-a | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| CERT_C-SIG00-a | 
     SIG00-C. Mask signals handled by noninterruptible signal handlers
     |
| CERT_C-SIG01-a | 
     SIG01-C. Understand implementation-specific details regarding signal handler persistence
     |
| CERT_C-SIG02-a | 
     SIG02-C. Avoid using signals to implement normal functionality
     |
| CERT_C-SIG30-a | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| CERT_C-SIG31-a | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| CERT_C-SIG34-a | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| CERT_C-SIG35-a | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| CERT_C-STR00-a | 
     STR00-C. Represent characters using an appropriate type
     |
| CERT_C-STR02-a | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| CERT_C-STR02-b | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| CERT_C-STR02-c | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| CERT_C-STR03-a | 
     STR03-C. Do not inadvertently truncate a string
     |
| CERT_C-STR04-a | 
     STR04-C. Use plain char for characters in the basic character set
     |
| CERT_C-STR05-a | 
     STR05-C. Use pointers to const when referring to string literals
     |
| CERT_C-STR07-a | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| CERT_C-STR09-a | 
     STR09-C. Don't assume numeric values for expressions with type plain character
     |
| CERT_C-STR10-a | 
     STR10-C. Do not concatenate different type of string literals
     |
| CERT_C-STR11-a | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| CERT_C-STR30-a | 
     STR30-C. Do not attempt to modify string literals
     |
| CERT_C-STR30-b | 
     STR30-C. Do not attempt to modify string literals
     |
| CERT_C-STR31-a | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CERT_C-STR31-b | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CERT_C-STR31-c | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CERT_C-STR31-d | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CERT_C-STR31-e | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| CERT_C-STR32-a | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| CERT_C-STR34-b | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| CERT_C-STR34-c | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| CERT_C-STR34-d | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| CERT_C-STR37-a | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| CERT_C-STR38-a | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| CERT_C-WIN00-a | 
     WIN00-C. Be specific when dynamically loading libraries
     |
| CERT_C-WIN30-a | 
     WIN30-C. Properly pair allocation and deallocation functions
     |
| Detects dangling pointers at runtime | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| Runtime analysis | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| Runtime analysis | 
     EXP33-C. Do not read uninitialized memory
     |
| Runtime analysis | 
     EXP34-C. Do not dereference null pointers
     |
| Runtime analysis | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| Runtime analysis | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| Runtime analysis | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| Runtime analysis | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| Runtime analysis | 
     MEM30-C. Do not access freed memory
     |
| Runtime analysis | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| Runtime analysis | 
     MEM34-C. Only free memory allocated dynamically
     |
| Runtime analysis | 
     ERR33-C. Detect and handle standard library errors
     |
| Runtime analysis | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| Runtime analysis | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| Runtime analysis | 
     FLP03-C. Detect and handle floating-point errors
     |
| Runtime analysis | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| Runtime analysis | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |

