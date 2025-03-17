> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 8.3p0

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| (customization) | 
     FIO44-C. Only use values for fsetpos() that are returned from fgetpos()
     |
| (customization) | 
     ERR34-C. Detect errors when converting a string to a number
     |
| (customization) | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| (customization) | 
     DCL03-C. Use a static assertion to test the value of a constant expression
     |
| (customization) | 
     FIO06-C. Create files with appropriate access permissions
     |
| (customization) | 
     FIO08-C. Take care when calling remove() on an open file
     |
| (customization) | 
     FIO10-C. Take care when using the rename() function
     |
| (customization) | 
     FIO13-C. Never push back anything other than one read character
     |
| (customization) | 
     FIO24-C. Do not open a file that is already open
     |
| (customization) | 
     MEM03-C. Clear sensitive information stored in reusable resources
     |
| (customization) | 
     MEM04-C. Beware of zero-length allocations
     |
| (customization) | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| (customization) | 
     STR06-C. Do not assume that strtok() leaves the parse string unchanged
     |
| (customization) | 
     WIN01-C. Do not forcibly terminate execution
     |
| (general) | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| (general) | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| (general) | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| (general) | 
     MEM11-C. Do not assume infinite heap space
     |
| ALLOC.DF | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| ALLOC.DF | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| ALLOC.LEAK | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| ALLOC.LEAK | 
     FIO42-C. Close files when they are no longer needed
     |
| ALLOC.LEAK | 
     CON30-C. Clean up thread-specific storage
     |
| ALLOC.LEAK | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| ALLOC.LEAK | 
     MEM11-C. Do not assume infinite heap space
     |
| ALLOC.SIZE.ADDOFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| ALLOC.SIZE.ADDOFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| ALLOC.SIZE.ADDOFLOW | 
     MEM35-C. Allocate sufficient memory for an object
     |
| ALLOC.SIZE.ADDOFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| ALLOC.SIZE.ADDOFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| ALLOC.SIZE.IOFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| ALLOC.SIZE.IOFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| ALLOC.SIZE.IOFLOW | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| ALLOC.SIZE.IOFLOW | 
     MEM35-C. Allocate sufficient memory for an object
     |
| ALLOC.SIZE.IOFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| ALLOC.SIZE.IOFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| ALLOC.SIZE.MULOFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| ALLOC.SIZE.MULOFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| ALLOC.SIZE.MULOFLOW | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| ALLOC.SIZE.MULOFLOW | 
     MEM35-C. Allocate sufficient memory for an object
     |
| ALLOC.SIZE.MULOFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| ALLOC.SIZE.MULOFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| ALLOC.SIZE.MULOFLOW | 
     MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap
     |
| ALLOC.SIZE.SUBUFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| ALLOC.SIZE.SUBUFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| ALLOC.SIZE.SUBUFLOW | 
     MEM35-C. Allocate sufficient memory for an object
     |
| ALLOC.SIZE.SUBUFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| ALLOC.SIZE.SUBUFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| ALLOC.SIZE.TRUNC | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| ALLOC.SIZE.TRUNC | 
     MEM35-C. Allocate sufficient memory for an object
     |
| ALLOC.SIZE.TRUNC | 
     INT02-C. Understand integer conversion rules
     |
| ALLOC.SIZE.TRUNC | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| ALLOC.TM | 
     MEM34-C. Only free memory allocated dynamically
     |
| ALLOC.TM | 
     WIN30-C. Properly pair allocation and deallocation functions
     |
| ALLOC.TM | 
     API07-C. Enforce type safety
     |
| ALLOC.UAF | 
     MEM30-C. Do not access freed memory
     |
| ALLOC.UAF | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| BADFUNC.* | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| BADFUNC.* | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| BADFUNC.ABORT | 
     ENV32-C. All exit handlers must return normally
     |
| BADFUNC.ATOF | 
     ERR34-C. Detect errors when converting a string to a number
     |
| BADFUNC.ATOI | 
     ERR34-C. Detect errors when converting a string to a number
     |
| BADFUNC.ATOL | 
     ERR34-C. Detect errors when converting a string to a number
     |
| BADFUNC.ATOLL | 
     ERR34-C. Detect errors when converting a string to a number
     |
| BADFUNC.BO.* | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| BADFUNC.BO.* | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| BADFUNC.BO.* | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| BADFUNC.BO.* | 
     API02-C. Functions that read or write to or from an array should take an argument to specify the source or target size
     |
| BADFUNC.BO.* | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| BADFUNC.CHROOT | 
     POS05-C. Limit access to files by creating a jail
     |
| BADFUNC.CREATEFILE | 
     FIO06-C. Create files with appropriate access permissions
     |
| BADFUNC.CREATEPROCESS | 
     WIN02-C. Restrict privileges when spawning child processes
     |
| BADFUNC.CREATETHREAD | 
     WIN02-C. Restrict privileges when spawning child processes
     |
| BADFUNC.EXIT | 
     ENV32-C. All exit handlers must return normally
     |
| BADFUNC.FORK | 
     POS38-C. Beware of race conditions when using fork and file descriptors
     |
| BADFUNC.GETENV | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| BADFUNC.LONGJMP | 
     ENV32-C. All exit handlers must return normally
     |
| BADFUNC.LONGJMP | 
     MSC22-C. Use the setjmp(), longjmp() facility securely
     |
| BADFUNC.MEMCMP | 
     EXP42-C. Do not compare padding data
     |
| BADFUNC.MEMSET | 
     MSC06-C. Beware of compiler optimizations
     |
| BADFUNC.PATH.* | 
     FIO02-C. Canonicalize path names originating from tainted sources
     |
| BADFUNC.PATH.AFXLOADLIBRARY | 
     WIN00-C. Be specific when dynamically loading libraries
     |
| BADFUNC.PATH.COLOADLIBRARY | 
     WIN00-C. Be specific when dynamically loading libraries
     |
| BADFUNC.PATH.LOADLIBRARY | 
     WIN00-C. Be specific when dynamically loading libraries
     |
| BADFUNC.PATH.SYSTEM | 
     ENV33-C. Do not call system()
     |
| BADFUNC.PUTENV | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| BADFUNC.RANDOM.RAND | 
     CON33-C. Avoid race conditions when using library functions
     |
| BADFUNC.RANDOM.RAND | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| BADFUNC.REALLOC | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| BADFUNC.SETJMP | 
     MSC22-C. Use the setjmp(), longjmp() facility securely
     |
| BADFUNC.SIGNAL | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| BADFUNC.SIGNAL | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| BADFUNC.SIGNAL | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| BADFUNC.SIGNAL | 
     SIG00-C. Mask signals handled by noninterruptible signal handlers
     |
| BADFUNC.SIGNAL | 
     SIG01-C. Understand implementation-specific details regarding signal handler persistence
     |
| BADFUNC.SIGNAL | 
     SIG02-C. Avoid using signals to implement normal functionality
     |
| BADFUNC.TEMP.* | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| BADFUNC.TEMP.* | 
     FIO21-C. Do not create temporary files in shared directories
     |
| BADFUNC.TEMP.TMPNAM | 
     CON33-C. Avoid race conditions when using library functions
     |
| BADFUNC.TIME_H | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| BADFUNC.TMPFILE_S | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| BADFUNC.TMPFILE_S | 
     FIO21-C. Do not create temporary files in shared directories
     |
| BADFUNC.TMPNAM_S | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| BADFUNC.TMPNAM_S | 
     FIO21-C. Do not create temporary files in shared directories
     |
| BADFUNC.TTYNAME | 
     CON33-C. Avoid race conditions when using library functions
     |
| BADFUNC.WEAKCRYPTO | 
     MSC25-C. Do not use insecure or weak cryptographic algorithms
     |
| BADMACRO.STDARG_H | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| BADMACRO.STDARG_H | 
     MSC38-C. Do not treat a predefined identifier as an object if it might only be implemented as a macro
     |
| BADMACRO.STDARG_H | 
     MSC39-C. Do not call va_arg() on a va_list that has an indeterminate value
     |
| BADMACRO.WEAK_CRYPTO | 
     MSC25-C. Do not use insecure or weak cryptographic algorithms
     |
| BUILD.WALL | 
     MSC00-C. Compile cleanly at high warning levels
     |
| BUILD.WERROR | 
     MSC00-C. Compile cleanly at high warning levels
     |
| CONCURRENCY.BADFUNC.CNDSIGNAL | 
     CON38-C. Preserve thread safety and liveness when using condition variables
     |
| CONCURRENCY.BADFUNC.CNDWAIT | 
     CON36-C. Wrap functions that can spuriously wake up in a loop
     |
| CONCURRENCY.BADFUNC.PTHREAD_KILL | 
     POS44-C. Do not use signals to terminate threads
     |
| CONCURRENCY.C_ATOMIC | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| CONCURRENCY.C_THREAD.ISD | 
     CON34-C. Declare objects shared between threads with appropriate storage durations
     |
| CONCURRENCY.DATARACE | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| CONCURRENCY.DATARACE | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| CONCURRENCY.DATARACE | 
     CON43-C. Do not allow data races in multithreaded code
     |
| CONCURRENCY.DATARACE | 
     POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
     |
| CONCURRENCY.DATARACE | 
     CON07-C. Ensure that compound operations on shared variables are atomic
     |
| CONCURRENCY.DU | 
     POS48-C. Do not unlock or destroy another POSIX thread's mutex
     |
| CONCURRENCY.LOCALARG | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| CONCURRENCY.LOCALARG | 
     CON34-C. Declare objects shared between threads with appropriate storage durations
     |
| CONCURRENCY.LOCK.NOLOCK | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| CONCURRENCY.LOCK.NOUNLOCK | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| CONCURRENCY.LOCK.ORDER | 
     CON35-C. Avoid deadlock by locking in a predefined order
     |
| CONCURRENCY.LOCK.ORDER | 
     POS51-C. Avoid deadlock with POSIX threads by locking in predefined order
     |
| CONCURRENCY.MAA | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| CONCURRENCY.MAA | 
     CON40-C. Do not refer to an atomic variable twice in an expression
     |
| CONCURRENCY.MAA | 
     CON43-C. Do not allow data races in multithreaded code
     |
| CONCURRENCY.MAA | 
     POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
     |
| CONCURRENCY.STARVE.BLOCKING | 
     POS52-C. Do not perform operations that can block while holding a POSIX lock
     |
| CONCURRENCY.STARVE.BLOCKING | 
     CON05-C. Do not perform operations that can block while holding a lock
     |
| CONCURRENCY.THREADLOCAL | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| CONCURRENCY.TNJ | 
     CON39-C. Do not join or detach a thread that was previously joined or detached
     |
| DIAG.UNEX.* | 
     MSC07-C. Detect and remove dead code
     |
| DIAG.UNEX.* | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| HARDCODED.AUTH | 
     MSC41-C. Never hard code sensitive information
     |
| HARDCODED.AUTH | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| HARDCODED.DNS | 
     MSC41-C. Never hard code sensitive information
     |
| HARDCODED.KEY | 
     MSC41-C. Never hard code sensitive information
     |
| HARDCODED.KEY | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| HARDCODED.SALT | 
     MSC41-C. Never hard code sensitive information
     |
| HARDCODED.SALT | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| HARDCODED.SEED | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| HARDCODED.SEED | 
     MSC41-C. Never hard code sensitive information
     |
| IO.BRAW | 
     FIO24-C. Do not open a file that is already open
     |
| IO.INJ.COMMAND | 
     ENV33-C. Do not call system()
     |
| IO.INJ.COMMAND | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.INJ.FMT | 
     FIO30-C. Exclude user input from format strings
     |
| IO.INJ.FMT | 
     FIO47-C. Use valid format strings
     |
| IO.INJ.FMT | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.INJ.LDAP | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.INJ.LIB | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.INJ.SQL | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.IOWOP | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| IO.OIWOP | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| IO.RACE | 
     FIO45-C. Avoid TOCTOU race conditions while accessing files
     |
| IO.RACE | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| IO.RACE | 
     FIO24-C. Do not open a file that is already open
     |
| IO.TAINT.ADDR | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| IO.TAINT.FNAME | 
     FIO01-C. Be careful using functions that use file names for identification
     |
| IO.TAINT.FNAME | 
     FIO02-C. Canonicalize path names originating from tainted sources
     |
| IO.TAINT.SIZE | 
     MEM35-C. Allocate sufficient memory for an object
     |
| IO.TAINT.SIZE | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| IO.TAINT.SIZE | 
     MEM05-C. Avoid large stack allocations
     |
| IO.TAINT.SIZE | 
     MEM11-C. Do not assume infinite heap space
     |
| IO.UAC | 
     FIO46-C. Do not access a closed file
     |
| IO.UT.HOST | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| IO.UT.LIB | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| IO.UT.PORT | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| IO.UT.PROC | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| LANG.ARITH.BIGSHIFT | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| LANG.ARITH.BIGSHIFT | 
     INT35-C. Use correct integer precisions
     |
| LANG.ARITH.DIVZERO | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| LANG.ARITH.FDIVZERO | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| LANG.ARITH.FMULOFLOW | 
     FLP00-C. Understand the limitations of floating-point numbers
     |
| LANG.ARITH.NEGSHIFT | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| LANG.CAST.ARRAY.TEMP | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| LANG.CAST.ARRAY.TEMP | 
     ARR00-C. Understand how arrays work
     |
| LANG.CAST.COERCE | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.CAST.COERCE | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| LANG.CAST.COERCE | 
     API07-C. Enforce type safety
     |
| LANG.CAST.COERCE | 
     INT02-C. Understand integer conversion rules
     |
| LANG.CAST.COERCE | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| LANG.CAST.PC.AV | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.CAST.PC.CONST2PTR | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.CAST.PC.CONST2PTR | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| LANG.CAST.PC.CRCQ | 
     DCL00-C. Const-qualify immutable objects
     |
| LANG.CAST.PC.CRCQ | 
     EXP05-C. Do not cast away a const qualification
     |
| LANG.CAST.PC.INT | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.CAST.PC.INT | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| LANG.CAST.PC.OBJ | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| LANG.CAST.PC.VBASE | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| LANG.CAST.RIP | 
     EXP14-C. Beware of integer promotion when performing bitwise operations on integer types smaller than int
     |
| LANG.CAST.VALUE | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.CAST.VALUE | 
     API07-C. Enforce type safety
     |
| LANG.CAST.VALUE | 
     INT02-C. Understand integer conversion rules
     |
| LANG.CAST.VALUE | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| LANG.ERRCODE.NOTEST | 
     ERR33-C. Detect and handle standard library errors
     |
| LANG.ERRCODE.NOTEST | 
     POS54-C. Detect and handle POSIX library errors
     |
| LANG.ERRCODE.NZ | 
     ERR33-C. Detect and handle standard library errors
     |
| LANG.ERRCODE.NZ | 
     POS54-C. Detect and handle POSIX library errors
     |
| LANG.FUNCS.APM | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| LANG.FUNCS.ASSERTS | 
     MSC11-C. Incorporate diagnostic tests using assertions
     |
| LANG.FUNCS.IRV | 
     ERR33-C. Detect and handle standard library errors
     |
| LANG.FUNCS.IRV | 
     POS54-C. Detect and handle POSIX library errors
     |
| LANG.FUNCS.IRV | 
     EXP12-C. Do not ignore values returned by functions
     |
| LANG.FUNCS.NORETURN | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.FUNCS.PROT | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| LANG.FUNCS.PROT | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| LANG.ID.AMBIG | 
     DCL02-C. Use visually distinct identifiers
     |
| LANG.ID.ND.EXT | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.ND.MM | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.ND.MO | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.ND.NEST | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| LANG.ID.ND.NEST | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.ND.SS | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.NU.EXT | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.NU.INT | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.NU.LIBFN | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.NU.TAG | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.ID.NU.TYPE | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.MEM.BO | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.MEM.BO | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.MEM.BO | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| LANG.MEM.BO | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.MEM.BO | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| LANG.MEM.BO | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| LANG.MEM.BO | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.MEM.BO | 
     POS30-C. Use the readlink() function properly
     |
| LANG.MEM.BO | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| LANG.MEM.BO | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.MEM.BU | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.MEM.BU | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.MEM.BU | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| LANG.MEM.BU | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.MEM.BU | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.MEM.BU | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.MEM.NPD | 
     EXP34-C. Do not dereference null pointers
     |
| LANG.MEM.TBA | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| LANG.MEM.TBA | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.MEM.TBA | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.MEM.TBA | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.MEM.TBA | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| LANG.MEM.TBA | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.MEM.TBA | 
     POS30-C. Use the readlink() function properly
     |
| LANG.MEM.TBA | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.MEM.TBA | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| LANG.MEM.TO | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.MEM.TO | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.MEM.TO | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.MEM.TO | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| LANG.MEM.TO | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.MEM.TO | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| LANG.MEM.TO | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.MEM.TU | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.MEM.TU | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.MEM.TU | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.MEM.TU | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.MEM.TU | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.MEM.UVAR | 
     EXP33-C. Do not read uninitialized memory
     |
| LANG.MEM.UVAR | 
     FIO40-C. Reset strings on fgets()  or fgetws() failure
     |
| LANG.PREPROC.FUNCMACRO | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| LANG.PREPROC.FUNCMACRO | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| LANG.PREPROC.HASH | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| LANG.PREPROC.INCL.TGMATH_H | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.PREPROC.MACROARG | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| LANG.PREPROC.MACROEND | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| LANG.PREPROC.MACROEND | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| LANG.PREPROC.MACROSTART | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| LANG.PREPROC.MARGME | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| LANG.PREPROC.PASTE | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| LANG.PREPROC.PASTE | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| LANG.PREPROC.PASTEHASH | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| LANG.STRUCT.ALIGNAS | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.ALIGNAS.EZA | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.ALIGNAS.EZA | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.ALIGNAS.IAS | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.ALIGNAS.TMAS | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.ALIGNOF | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.CONDASSIG | 
     EXP45-C. Do not perform assignments in selection statements
     |
| LANG.STRUCT.CUP | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| LANG.STRUCT.CUP | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.STRUCT.DECL.FAM | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| LANG.STRUCT.DECL.IF | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| LANG.STRUCT.DECL.IMPFN | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.DECL.IMPT | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| LANG.STRUCT.DECL.IO | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| LANG.STRUCT.DECL.MGT | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| LANG.STRUCT.DECL.ML | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| LANG.STRUCT.DECL.NOEXT | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| LANG.STRUCT.DECL.RESERVED | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| LANG.STRUCT.DECL.VLA | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.EBS | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| LANG.STRUCT.EBS | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.ELLIPSIS | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| LANG.STRUCT.ICOL | 
     CON36-C. Wrap functions that can spuriously wake up in a loop
     |
| LANG.STRUCT.ICOL | 
     CON41-C. Wrap functions that can fail spuriously in a loop
     |
| LANG.STRUCT.INIT.ENUM | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| LANG.STRUCT.INIT.UADI | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| LANG.STRUCT.LOOP.FPC | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| LANG.STRUCT.LOOP.HR | 
     MSC21-C. Use robust loop termination conditions
     |
| LANG.STRUCT.LOOP.UB | 
     MSC21-C. Use robust loop termination conditions
     |
| LANG.STRUCT.MRS | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| LANG.STRUCT.NTAD | 
     EXP34-C. Do not dereference null pointers
     |
| LANG.STRUCT.PARENS | 
     EXP00-C. Use parentheses for precedence of operation
     |
| LANG.STRUCT.PARITH | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.STRUCT.PARITH | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.STRUCT.PARITH | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.STRUCT.PARITH | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.STRUCT.PARITH | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.STRUCT.PBB | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.STRUCT.PBB | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.STRUCT.PBB | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.STRUCT.PBB | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.STRUCT.PBB | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.STRUCT.PIT | 
     DCL05-C. Use typedefs of non-pointer types only
     |
| LANG.STRUCT.PPE | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| LANG.STRUCT.PPE | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| LANG.STRUCT.PPE | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| LANG.STRUCT.PPE | 
     MEM35-C. Allocate sufficient memory for an object
     |
| LANG.STRUCT.PPE | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.STRUCT.RC | 
     ERR30-C. Take care when reading errno
     |
| LANG.STRUCT.RC | 
     MSC07-C. Detect and remove dead code
     |
| LANG.STRUCT.RC | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.RFCESH | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| LANG.STRUCT.RPL | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| LANG.STRUCT.RPNTC | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| LANG.STRUCT.RPNTC | 
     DCL00-C. Const-qualify immutable objects
     |
| LANG.STRUCT.SCOPE.FILE | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| LANG.STRUCT.SCOPE.FILE | 
     DCL19-C. Minimize the scope of variables and functions
     |
| LANG.STRUCT.SCOPE.LOCAL | 
     DCL19-C. Minimize the scope of variables and functions
     |
| LANG.STRUCT.SE.CGEN | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| LANG.STRUCT.SE.COND | 
     EXP45-C. Do not perform assignments in selection statements
     |
| LANG.STRUCT.SE.DEC | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| LANG.STRUCT.SE.DEC | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| LANG.STRUCT.SE.INC | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| LANG.STRUCT.SE.INC | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| LANG.STRUCT.SE.INIT | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| LANG.STRUCT.SE.IOE | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| LANG.STRUCT.SE.SIZEOF | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| LANG.STRUCT.SUP | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| LANG.STRUCT.SUP | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| LANG.STRUCT.SW.BAD | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| LANG.STRUCT.SW.MB | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| LANG.STRUCT.SW.MPC | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| LANG.STRUCT.SW.SWNEE | 
     DCL06-C. Use meaningful symbolic constants to represent literal values
     |
| LANG.STRUCT.UA | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UC | 
     MSC07-C. Detect and remove dead code
     |
| LANG.STRUCT.UC | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UPD | 
     EXP34-C. Do not dereference null pointers
     |
| LANG.STRUCT.UPD | 
     API00-C. Functions should validate their parameters
     |
| LANG.STRUCT.USEASSIGN | 
     EXP45-C. Do not perform assignments in selection statements
     |
| LANG.STRUCT.UULABEL | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UUMACRO | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UUPARAM | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UUTAG | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UUTYPE | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.STRUCT.UUVAL | 
     MSC13-C. Detect and remove unused values
     |
| LANG.STRUCT.UUVAR | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| LANG.TYPE.AWID | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| LANG.TYPE.BASIC | 
     INT01-C. Use rsize_t or size_t for all integer values representing the size of an object
     |
| LANG.TYPE.BFSIGN | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| LANG.TYPE.CBCONST | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| LANG.TYPE.CSUF | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| LANG.TYPE.IAT | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| LANG.TYPE.IAT | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| LANG.TYPE.IAT | 
     STR04-C. Use plain char for characters in the basic character set
     |
| LANG.TYPE.ICA | 
     STR04-C. Use plain char for characters in the basic character set
     |
| LANG.TYPE.IOT | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| LANG.TYPE.IOT | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| LANG.TYPE.IOT | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| LANG.TYPE.IOT | 
     STR04-C. Use plain char for characters in the basic character set
     |
| LANG.TYPE.MOT | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| LANG.TYPE.MOT | 
     STR04-C. Use plain char for characters in the basic character set
     |
| LANG.TYPE.NCS | 
     STR05-C. Use pointers to const when referring to string literals
     |
| LANG.TYPE.OC | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| LANG.TYPE.OWID | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| LANG.TYPE.RESTRICT | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| LANG.TYPE.SAP | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| LANG.TYPE.VCBC | 
     DCL00-C. Const-qualify immutable objects
     |
| LANG.TYPE.VMAT | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| MATH.DOMAIN | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.ATAN | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.FE_INVALID | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.LOG | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.POW | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.SQRT | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.TOOHIGH | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.DOMAIN.TOOLOW | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.RANGE | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.RANGE.COSH.TOOHIGH | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.RANGE.COSH.TOOLOW | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.RANGE.GAMMA | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MATH.RANGE.GAMMA | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| MATH.RANGE.LOG | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| MISC.CHROOT.NOCHDIR | 
     POS05-C. Limit access to files by creating a jail
     |
| MISC.CRYPTO.TIMESEED | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| MISC.FMT | 
     FIO30-C. Exclude user input from format strings
     |
| MISC.FMT | 
     FIO47-C. Use valid format strings
     |
| MISC.FMTTYPE | 
     FIO47-C. Use valid format strings
     |
| MISC.MEM.NTERM | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| MISC.MEM.NTERM | 
     STR03-C. Do not inadvertently truncate a string
     |
| MISC.MEM.NTERM.CSTRING | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| MISC.MEM.NTERM.CSTRING | 
     POS30-C. Use the readlink() function properly
     |
| MISC.MEM.SIZE.ADDOFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| MISC.MEM.SIZE.ADDOFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| MISC.MEM.SIZE.ADDOFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| MISC.MEM.SIZE.ADDOFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| MISC.MEM.SIZE.BAD | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| MISC.MEM.SIZE.BAD | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| MISC.MEM.SIZE.BAD | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| MISC.MEM.SIZE.BAD | 
     MEM35-C. Allocate sufficient memory for an object
     |
| MISC.MEM.SIZE.BAD | 
     INT08-C. Verify that all integer values are in range
     |
| MISC.MEM.SIZE.BAD | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| MISC.MEM.SIZE.BAD | 
     MEM05-C. Avoid large stack allocations
     |
| MISC.MEM.SIZE.BAD | 
     MEM11-C. Do not assume infinite heap space
     |
| MISC.MEM.SIZE.MULOFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| MISC.MEM.SIZE.MULOFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| MISC.MEM.SIZE.MULOFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| MISC.MEM.SIZE.MULOFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| MISC.MEM.SIZE.SUBUFLOW | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| MISC.MEM.SIZE.SUBUFLOW | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| MISC.MEM.SIZE.SUBUFLOW | 
     INT08-C. Verify that all integer values are in range
     |
| MISC.MEM.SIZE.SUBUFLOW | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| MISC.MEM.SIZE.TRUNC | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| MISC.MEM.SIZE.TRUNC | 
     INT02-C. Understand integer conversion rules
     |
| MISC.MEM.SIZE.TRUNC | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| MISC.NEGCHAR | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| MISC.NEGCHAR | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| MISC.NEGCHAR | 
     INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs
     |
| MISC.NEGCHAR | 
     STR00-C. Represent characters using an appropriate type
     |
| MISC.NOEFFECT | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| MISC.PADDING.POTB | 
     DCL39-C. Avoid information leakage when passing a structure across a trust boundary
     |
| MISC.PWD.PLAIN | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| MISC.PWD.PLAINTRAN | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |

