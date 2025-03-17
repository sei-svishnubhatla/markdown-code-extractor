> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 24.04

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| alignas-extended | 
     MSC40-C. Do not violate constraints
     |
| alignof-side-effect | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| alloc-without-cast | 
     MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type
     |
| alloc-without-sizeof | 
     EXP09-C. Use sizeof to determine the size of a type or variable
     |
| array-index-range | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| array-index-range-constant | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| array-size-global | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| array_out_of_bounds | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| array_out_of_bounds | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| array_out_of_bounds | 
     API01-C. Avoid laying out strings in memory directly before sensitive data
     |
| assignment-conditional | 
     EXP45-C. Do not perform assignments in selection statements
     |
| assignment-to-non-modifiable-lvalue | 
     EXP40-C. Do not modify constant objects
     |
| assignment-to-non-modifiable-lvalue | 
     MSC40-C. Do not violate constraints
     |
| bad-function | 
     ENV32-C. All exit handlers must return normally
     |
| bad-function | 
     API04-C. Provide a consistent and usable error-checking mechanism
     |
| bad-function | 
     ERR06-C. Understand the termination behavior of assert() and abort()
     |
| bad-function | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| bad-function | 
     WIN01-C. Do not forcibly terminate execution
     |
| bad-function-use | 
     ENV32-C. All exit handlers must return normally
     |
| bad-function-use | 
     API04-C. Provide a consistent and usable error-checking mechanism
     |
| bad-macro-expansion | 
     POS47-C. Do not use threads that can be canceled asynchronously
     |
| bad-macro-use | 
     POS47-C. Do not use threads that can be canceled asynchronously
     |
| bad-macro-use | 
     ERR06-C. Understand the termination behavior of assert() and abort()
     |
| bitfield-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| bitfield-type | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| bitop-type | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| bitop-type | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| cast-pointer-void-arithmetic-implicit | 
     MSC40-C. Do not violate constraints
     |
| chained-comparison | 
     EXP13-C. Treat relational and equality operators as if they were nonassociative
     |
| chained-errno-function-calls | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| char-sign-conversion | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| character-constant | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| compound-ifelse | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| compound-loop | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| conversion_overflow | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| ctype-limits | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| dangling_pointer_use | 
     MEM30-C. Do not access freed memory
     |
| dead-assignemnt | 
     MSC07-C. Detect and remove dead code
     |
| dead-assignment | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| dead-initializer | 
     MSC07-C. Detect and remove dead code
     |
| dead-initializer | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| deadlock | 
     CON35-C. Avoid deadlock by locking in a predefined order
     |
| distinct-extern | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| element-type-incomplete | 
     MSC40-C. Do not violate constraints
     |
| empty-body | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| empty-parameter-list | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| encoding-mismatch | 
     STR10-C. Do not concatenate different type of string literals
     |
| enum-implicit-value | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| enum-tag-spelling | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| enumeration-constant-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| errno-reset | 
     ERR30-C. Take care when reading errno
     |
| errno-test-after-wrong-call | 
     ERR32-C. Do not rely on indeterminate values of errno
     |
| error-information-unused | 
     ERR33-C. Detect and handle standard library errors
     |
| error-information-unused | 
     POS54-C. Detect and handle POSIX library errors
     |
| error-information-unused | 
     API04-C. Provide a consistent and usable error-checking mechanism
     |
| error-information-unused | 
     EXP12-C. Do not ignore values returned by functions
     |
| error-information-unused-computed | 
     ERR33-C. Detect and handle standard library errors
     |
| error-information-unused-computed | 
     POS54-C. Detect and handle POSIX library errors
     |
| error-information-unused-computed | 
     API04-C. Provide a consistent and usable error-checking mechanism
     |
| error-information-unused-computed | 
     EXP12-C. Do not ignore values returned by functions
     |
| essential-type-assign | 
     FIO34-C. Distinguish between characters read from a file and EOF or WEOF
     |
| evaluation-order | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| evaluation-order | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| expanded-side-effect-multiplied | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| expanded-side-effect-not-evaluated | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| expression-result-unused | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| field_overflow_upon_dereference | 
     API01-C. Avoid laying out strings in memory directly before sensitive data
     |
| file-dereference | 
     FIO38-C. Do not copy a FILE object
     |
| flexible-array-member-assignment | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| flexible-array-member-declaration | 
     MEM33-C.  Allocate and copy structures containing a flexible array member dynamically
     |
| float-comparison | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| float-division-by-zero | 
     FLP03-C. Detect and handle floating-point errors
     |
| for-loop-float | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| function-argument-with-padding | 
     DCL39-C. Avoid information leakage when passing a structure across a trust boundary
     |
| function-like-macro-expansion | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| function-like-macro-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| function-name-constant-comparison | 
     EXP16-C. Do not compare function pointers to constant values
     |
| function-pointer-integer-cast | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| function-pointer-integer-cast-implicit | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| function-pointer-integer-cast-implicit | 
     MSC40-C. Do not violate constraints
     |
| function-prototype | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| function-return-type | 
     DCL31-C. Declare identifiers before using them
     |
| function-return-type | 
     MSC40-C. Do not violate constraints
     |
| future-library-use | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| generic-selection-side-effect | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| global-function-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| global-object-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| global-object-name-const | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| global-object-scope | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| global-object-scope | 
     DCL19-C. Minimize the scope of variables and functions
     |
| header-filename | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| implementation-filename | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| implicit-function-declaration | 
     DCL31-C. Declare identifiers before using them
     |
| implicit-function-declaration | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| inappropriate-bool | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| inappropriate-pointer-cast-implicit | 
     MSC40-C. Do not violate constraints
     |
| include-guard-missing | 
     PRE06-C. Enclose header files in an include guard
     |
| include-guard-pragma-once | 
     PRE06-C. Enclose header files in an include guard
     |
| incompatible-argument-type | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| incompatible-function-pointer-conversion | 
     MSC40-C. Do not violate constraints
     |
| incompatible-object-pointer-conversion | 
     MSC40-C. Do not violate constraints
     |
| initializer-excess | 
     MSC40-C. Do not violate constraints
     |
| int-division-by-zero | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| int-modulo-by-zero | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| integer-overflow | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| integer-overflow | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| integer-overflow | 
     INT08-C. Verify that all integer values are in range
     |
| invalid-array-size | 
     MSC40-C. Do not violate constraints
     |
| invalid-free | 
     MEM34-C. Only free memory allocated dynamically
     |
| language-override | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| language-override-c99 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| literal-assignment | 
     STR05-C. Use pointers to const when referring to string literals
     |
| local-object-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| local-object-name-const | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| local-object-scope | 
     DCL19-C. Minimize the scope of variables and functions
     |
| local-static-object-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| local-static-object-name-const | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| logop-side-effect | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| long-suffix | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| macro-argument-hash | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| macro-final-semicolon | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| macro-function-like | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| macro-parameter-multiplied | 
     PRE12-C. Do not define unsafe macros
     |
| macro-parameter-parentheses | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| macro-parameter-unused | 
     PRE12-C. Do not define unsafe macros
     |
| malloc-size-insufficient | 
     MEM35-C. Allocate sufficient memory for an object
     |
| memcmp-with-float | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| memcpy-with-padding | 
     EXP42-C. Do not compare padding data
     |
| missing-else | 
     MSC01-C. Strive for logical completeness
     |
| mmline-comment | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| multiple-atomic-accesses | 
     CON40-C. Do not refer to an atomic variable twice in an expression
     |
| multiple-volatile-accesses | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| multiple-volatile-accesses | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| non-constant-static-assert | 
     MSC40-C. Do not violate constraints
     |
| null-dereferencing | 
     EXP34-C. Do not dereference null pointers
     |
| null-dereferencing | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| object-like-macro-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| octal-constant | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| parameter-match | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| parameter-match-computed | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| parameter-match-type | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| parameter-match-type | 
     MSC40-C. Do not violate constraints
     |
| parameter-missing-const | 
     DCL00-C. Const-qualify immutable objects
     |
| parameter-missing-const | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| pointer-cast-alignment | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| pointer-integral-cast | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| pointer-integral-cast-implicit | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| pointer-integral-cast-implicit | 
     MSC40-C. Do not violate constraints
     |
| pointer-qualifier-cast-const | 
     EXP40-C. Do not modify constant objects
     |
| pointer-qualifier-cast-const | 
     EXP05-C. Do not cast away a const qualification
     |
| pointer-qualifier-cast-const-implicit | 
     EXP40-C. Do not modify constant objects
     |
| pointer-qualifier-cast-const-implicit | 
     MSC40-C. Do not violate constraints
     |
| pointer-qualifier-cast-const-implicit | 
     EXP05-C. Do not cast away a const qualification
     |
| pointer-qualifier-cast-volatile | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| pointer-qualifier-cast-volatile-implicit | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| pointer-qualifier-cast-volatile-implicit | 
     MSC40-C. Do not violate constraints
     |
| pointer-subtraction | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| pointer-typedef | 
     DCL05-C. Use typedefs of non-pointer types only
     |
| pointered-deallocation | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| pointered-deallocation | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| precision-shift-width | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| precision-shift-width-constant | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| read_data_race | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| read_data_race | 
     CON43-C. Do not allow data races in multithreaded code
     |
| redeclaration | 
     MSC40-C. Do not violate constraints
     |
| redundant-operation | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| reserved-declaration | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| reserved-declaration-c99 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| reserved-identifier | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| restrict | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| return-empty | 
     MSC40-C. Do not violate constraints
     |
| return-implicit | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| return-non-empty | 
     MSC40-C. Do not violate constraints
     |
| return-reference-local | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| return-reference-local | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| scaled-pointer-arithmetic | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| side-effect-not-expanded | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| signal-handler-shared-access | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| signal-handler-signal-call | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| signal-handler-unsafe-call | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| sizeof | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| sizeof-array-parameter | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| sline-comment | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| sline-splicing | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| smline-comment | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| statement-sideeffect | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| static-assert | 
     MSC40-C. Do not violate constraints
     |
| static-function-declaration | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| static-function-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| static-object-declaration | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| static-object-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| static-object-name-const | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| stdlib-const-pointer-assign | 
     ENV30-C. Do not modify the object referenced by the return value of certain functions
     |
| stdlib-limits | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| stdlib-macro-ato | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| stdlib-macro-atoll | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| stdlib-use-ato | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| stdlib-use-atoll | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| stdlib-use-rand | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| stdlib-use-signal | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| stdlib-use-system | 
     ENV33-C. Do not call system()
     |
| stream-argument-with-side-effects | 
     FIO41-C. Do not call getc(), putc(), getwc(), or putwc() with a stream argument that has side effects
     |
| string-literal | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| string-literal-modfication | 
     STR30-C. Do not attempt to modify string literals
     |
| struct-member-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| struct-tag-spelling | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| Supported | 
     FIO46-C. Do not access a closed file
     |
| Supported | 
     ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it
     |
| Supported | 
     MSC41-C. Never hard code sensitive information
     |
| Supported | 
     API00-C. Functions should validate their parameters
     |
| Supported | 
     EXP14-C. Beware of integer promotion when performing bitwise operations on integer types smaller than int
     |
| Supported | 
     INT02-C. Understand integer conversion rules
     |
| Supported | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| Supported by stubbing/taint analysis | 
     STR02-C. Sanitize data passed to complex subsystems
     |
| Supported by taint analysis | 
     INT04-C. Enforce limits on integer values originating from tainted sources
     |
| Supported indirectly via MISRA C:2004 rule 6.1. | 
     STR04-C. Use plain char for characters in the basic character set
     |
| Supported indirectly via MISRA C:2004 rule 6.1 and MISRA C:2012 rule 10.1. | 
     STR00-C. Represent characters using an appropriate type
     |
| Supported indirectly via MISRA C:2004 Rule 13.2. | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| Supported indirectly via MISRA C:2004 Rule 17.4. | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| Supported indirectly via MISRA C:2012 Rule 5.3. | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| Supported indirectly via MISRA C:2012 rule 10.1. | 
     STR09-C. Don't assume numeric values for expressions with type plain character
     |
| Supported indirectly via MISRA C:2012 Rules 5.1, 5.2, 5.3, 5.4 and 5.5. | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| Supported indirectly via MISRA C:2012 rules 10.1, 10.3 and 10.4. | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| Supported via MISRA C:2012 Rules 10.1, 10.3, 10.4, 10.6 and 10.7 | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| Supported via stubbing/taint analysis | 
     FIO30-C. Exclude user input from format strings
     |
| Supported, but no explicit checker | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| Supported, but no explicit checker | 
     MEM36-C. Do not modify the alignment of objects by calling realloc()
     |
| Supported, but no explicit checker | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| Supported, but no explicit checker | 
     FIO42-C. Close files when they are no longer needed
     |
| Supported, but no explicit checker | 
     CON30-C. Clean up thread-specific storage
     |
| Supported, but no explicit checker | 
     CON31-C. Do not destroy a mutex while it is locked
     |
| Supported, but no explicit checker | 
     CON33-C. Avoid race conditions when using library functions
     |
| Supported, but no explicit checker | 
     CON39-C. Do not join or detach a thread that was previously joined or detached
     |
| Supported, but no explicit checker | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| Supported, but no explicit checker | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| Supported, but no explicit checker | 
     MSC38-C. Do not treat a predefined identifier as an object if it might only be implemented as a macro
     |
| Supported, but no explicit checker | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| Supported, but no explicit checker | 
     CON06-C. Ensure that every mutex outlives the data it protects
     |
| Supported, but no explicit checker | 
     DCL10-C. Maintain the contract between the writer and caller of variadic functions
     |
| Supported, but no explicit checker | 
     INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
     |
| Supported, but no explicit checker | 
     MEM04-C. Beware of zero-length allocations
     |
| Supported, but no explicit checker | 
     MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap
     |
| Supported, but no explicit checker | 
     MSC13-C. Detect and remove unused values
     |
| Supported, but no explicit checker | 
     PRE09-C. Do not replace secure functions with deprecated or obsolescent functions
     |
| Supported, resulting undefined behavior is reported by the runtime error analysis | 
     CON34-C. Declare objects shared between threads with appropriate storage durations
     |
| Supported: Astrée can detect subsequent code defects that this rule aims to prevent. | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| Supported: Astrée keeps track of all floating point rounding errors and loss of precision and reports code defects resulting from those. | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| Supported: Astrée reports accesses outside the bounds of allocated memory. | 
     EXP03-C. Do not assume the size of a structure is the sum of the sizes of its members
     |
| Supported: Astrée reports all potential deadlocks. | 
     POS51-C. Avoid deadlock with POSIX threads by locking in predefined order
     |
| Supported: Astrée reports defects due to returned (empty) strings. | 
     FIO37-C. Do not assume that fgets() or fgetws() returns a nonempty string when successful
     |
| Supported: Astrée reports non-standard language elements. | 
     MSC23-C. Beware of vendor-specific library and language differences
     |
| Supported: Astrée reports overflows due to insufficient precision. | 
     INT35-C. Use correct integer precisions
     |
| Supported: Astrée reports potential infinite loops. | 
     MSC21-C. Use robust loop termination conditions
     |
| Supported: Astrée reports potential runtime error resulting from missing checks for exceptional values. | 
     FLP04-C. Check floating-point inputs for exceptional values
     |
| Supported: Astrée reports potential runtime errors resulting from invalid pointer arithmetics. | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| Supported: Astrée reports runtime errors resulting from invalid assumptions. | 
     EXP11-C. Do not make assumptions regarding the layout of structures with bit-fields
     |
| Supported: Astrée reports undefined behavior. | 
     MSC15-C. Do not depend on undefined behavior
     |
| Supported: Astrée reports usage of invalid pointers. | 
     MEM01-C. Store a new value in pointers immediately after free()
     |
| Supported: Can be checked with appropriate analysis stubs. | 
     POS30-C. Use the readlink() function properly
     |
| Supported: Can be checked with appropriate analysis stubs. | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| Supported: Can be checked with appropriate analysis stubs. | 
     WIN30-C. Properly pair allocation and deallocation functions
     |
| Supported: This rule aims to prevent truncations and overflows. All possible overflows are reported by Astrée. | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| SupportedAstrée reports all buffer overflows resulting from copying data to a buffer that is not large enough to hold that data. | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| SupportedAstrée reports all potential overflows resulting from floating-point conversions. | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| SupportedAstrée supports the implementation of library stubs to fully verify this guideline. | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| switch-clause-break | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| switch-clause-break-continue | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| switch-clause-break-return | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| switch-default | 
     MSC01-C. Strive for logical completeness
     |
| switch-label | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| switch-skipped-code | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| taint_sink | 
     POS39-C. Use the correct byte ordering when transferring data between systems
     |
| temporary-object-modification | 
     EXP35-C. Do not modify objects with temporary lifetime
     |
| trigraph | 
     PRE07-C. Avoid using repeated question marks
     |
| type-compatibility | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| type-compatibility | 
     MSC40-C. Do not violate constraints
     |
| type-compatibility-link | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| type-compatibility-link | 
     MSC40-C. Do not violate constraints
     |
| type-specifier | 
     DCL31-C. Declare identifiers before using them
     |
| type-specifier | 
     MSC40-C. Do not violate constraints
     |
| typedef-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| undeclared-parameter | 
     DCL31-C. Declare identifiers before using them
     |
| undeclared-parameter | 
     MSC40-C. Do not violate constraints
     |
| uninitialized-local-read | 
     EXP33-C. Do not read uninitialized memory
     |
| uninitialized-variable-use | 
     EXP33-C. Do not read uninitialized memory
     |
| union-member-name | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| union-tag-spelling | 
     MSC09-C. Character encoding: Use subset of ASCII for safety
     |
| universal-character-name-concatenation | 
     PRE30-C. Do not create a universal character name through concatenation
     |
| unnamed-parameter | 
     MSC40-C. Do not violate constraints
     |
| unreachable-code | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| unreachable-code-after-jump | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| unused-function | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| user_defined | 
     ENV32-C. All exit handlers must return normally
     |
| user_defined | 
     POS35-C. Avoid race conditions while checking for the existence of a symbolic link
     |
| user_defined | 
     POS36-C. Observe correct revocation order while relinquishing privileges
     |
| user_defined | 
     POS37-C. Ensure that privilege relinquishment is successful
     |
| wide-narrow-string-cast | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| wide-narrow-string-cast-implicit | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| write-to-constant-memory | 
     EXP40-C. Do not modify constant objects
     |
| write-to-string-literal | 
     STR30-C. Do not attempt to modify string literals
     |
| write_data_race | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| write_data_race | 
     CON43-C. Do not allow data races in multithreaded code
     |

