> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 24.11.0

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| arrayIndexOutOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| arrayIndexOutOfBoundsCond | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| arrayIndexThenCheck | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| autoVariables | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| autovarInvalidDeallocation | 
     MEM34-C. Only free memory allocated dynamically
     |
| bitwiseOnBoolean | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| comparePointers | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| danglingLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| deallocret | 
     MEM30-C. Do not access freed memory
     |
| deallocuse | 
     MEM30-C. Do not access freed memory
     |
| doubleFree | 
     MEM30-C. Do not access freed memory
     |
| floatConversionOverflow | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| invalidLengthModifierError | 
     FIO47-C. Use valid format strings
     |
| invalidLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| invalidscanf | 
     FIO47-C. Use valid format strings
     |
| invalidScanfFormatWidth | 
     FIO47-C. Use valid format strings
     |
| IOWithoutPositioning | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| leakReturnValNotUsed | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| leakUnsafeArgAlloc | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memleak | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memleakOnRealloc | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| memsetValueOutOfRange | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| mismatchAllocDealloc | 
     MEM34-C. Only free memory allocated dynamically
     |
| missingReturn | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| negativeArraySize | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| negativeIndex | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| nullPointer | 
     EXP34-C. Do not dereference null pointers
     |
| nullPointerDefaultArg | 
     EXP34-C. Do not dereference null pointers
     |
| nullPointerRedundantCheck | 
     EXP34-C. Do not dereference null pointers
     |
| outOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| possibleBufferAccessOutOfBounds | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| premium-cert-arr30-c | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| premium-cert-arr32-c | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| premium-cert-arr37-c | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| premium-cert-arr38-c | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| premium-cert-arr39-c | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| premium-cert-con30-c | 
     CON30-C. Clean up thread-specific storage
     |
| premium-cert-con31-c | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| premium-cert-con32-c | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| premium-cert-con33-c | 
     CON33-C. Avoid race conditions when using library functions
     |
| premium-cert-con34-c | 
     CON34-C. Declare objects shared between threads with appropriate storage durations
     |
| premium-cert-con35-c | 
     CON35-C. Avoid deadlock by locking in a predefined order
     |
| premium-cert-con36-c | 
     CON36-C. Wrap functions that can spuriously wake up in a loop
     |
| premium-cert-con37-c | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| premium-cert-con38-c | 
     CON38-C. Preserve thread safety and liveness when using condition variables
     |
| premium-cert-con39-c | 
     CON39-C. Do not join or detach a thread that was previously joined or detached
     |
| premium-cert-con40-c | 
     CON40-C. Do not refer to an atomic variable twice in an expression
     |
| premium-cert-con41-c | 
     CON41-C. Wrap functions that can fail spuriously in a loop
     |
| premium-cert-dcl31-c | 
     DCL31-C. Declare identifiers before using them
     |
| premium-cert-dcl36-c | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| premium-cert-dcl37-c | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| premium-cert-dcl38-c | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| premium-cert-dcl39-c | 
     DCL39-C. Avoid information leakage when passing a structure across a trust boundary
     |
| premium-cert-dcl40-c | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| premium-cert-dcl41-c | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| premium-cert-env30-c | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| premium-cert-env31-c | 
     ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it
     |
| premium-cert-env32-c | 
     ENV32-C. All exit handlers must return normally
     |
| premium-cert-env33-c | 
     ENV33-C. Do not call system()
     |
| premium-cert-env34-c | 
     ENV34-C. Do not store pointers returned by certain functions
     |
| premium-cert-err30-c | 
     ERR30-C. Take care when reading errno
     |
| premium-cert-err32-c | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| premium-cert-err33-c | 
     ERR33-C. Detect and handle standard library errors
     |
| premium-cert-exp32-c | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| premium-cert-exp35-c | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| premium-cert-exp36-c | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| premium-cert-exp37-c | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| premium-cert-exp39-c | 
     EXP39-C. Do not access a variable through a pointer of an incompatible type
     |
| premium-cert-exp40-c | 
     EXP40-C. Do not modify constant objects
     |
| premium-cert-exp42-c | 
     EXP42-C. Do not compare padding data
     |
| premium-cert-exp43-c | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| premium-cert-exp45-c | 
     EXP45-C. Do not perform assignments in selection statements
     |
| premium-cert-fio30-c | 
     FIO30-C. Exclude user input from format strings
     |
| premium-cert-fio32-c | 
     FIO32-C. Do not perform operations on devices that are only appropriate for files
     |
| premium-cert-fio34-c | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| premium-cert-fio37-c | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| premium-cert-fio38-c | 
     FIO38-C. Do not copy a FILE object
     |
| premium-cert-fio40-c | 
     FIO40-C. Reset strings on fgets()  or fgetws() failure
     |
| premium-cert-fio41-c | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| premium-cert-fio44-c | 
     FIO44-C. Only use values for fsetpos() that are returned from fgetpos()
     |
| premium-cert-fio45-c | 
     FIO45-C. Avoid TOCTOU race conditions while accessing files
     |
| premium-cert-flp30-c | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| premium-cert-flp36-c | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| premium-cert-flp37-c | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| premium-cert-int30-c | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| premium-cert-int31-c | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| premium-cert-int32-c | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| premium-cert-int33-c | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| premium-cert-int34-c | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| premium-cert-int35-c | 
     INT35-C. Use correct integer precisions
     |
| premium-cert-int36-c | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| premium-cert-mem33-c | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| premium-cert-mem35-c | 
     MEM35-C. Allocate sufficient memory for an object
     |
| premium-cert-mem36-c | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| premium-cert-msc30-c | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| premium-cert-msc32-c | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| premium-cert-msc33-c | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| premium-cert-msc38-c | 
     MSC38-C. Do not treat a predefined identifier as an object if it might only be implemented as a macro
     |
| premium-cert-msc39-c | 
     MSC39-C. Do not call va_arg() on a va_list that has an indeterminate value
     |
| premium-cert-msc40-c | 
     MSC40-C. Do not violate constraints
     |
| premium-cert-pre00-c | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| premium-cert-pre01-c | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| premium-cert-pre04-c | 
     PRE04-C. Do not reuse a standard header file name
     |
| premium-cert-pre09-c | 
     PRE09-C. Do not replace secure functions with deprecated or obsolescent functions
     |
| premium-cert-pre11-c | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| premium-cert-pre31-c | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| premium-cert-sig30-c | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| premium-cert-sig31-c | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| premium-cert-sig34-c | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| premium-cert-sig35-c | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| premium-cert-str32-c | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| premium-cert-str34-c | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| premium-cert-str38-c | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| preprocessorErrorDirective | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| resourceLeak | 
     FIO42-C. Close files when they are no longer needed
     |
| returnDanglingLifetime | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| shiftNegative | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| shiftTooManyBits | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| suspiciousFloatingPointCast | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| uninitdata | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitMemberVar | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitstring | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitStructMember | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitvar | 
     EXP33-C. Do not read uninitialized memory
     |
| unknownEvaluationOrder | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| wrongPrintfScanfArgNum | 
     FIO47-C. Use valid format strings
     |
| wrongPrintfScanfParameterPositionError | 
     FIO47-C. Use valid format strings
     |
| zerodiv | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| zerodivcond | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |

