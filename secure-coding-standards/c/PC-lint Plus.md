> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 1.4

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| 1 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 18 | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 111 | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| 175 | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| 401 | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 409 | 
     ARR00-C. Understand how arrays work
     |
| 413 | 
     EXP34-C. Do not dereference null pointers
     |
| 413 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 413 | 
     POS54-C. Detect and handle POSIX library errors
     |
| 413 | 
     API00-C. Functions should validate their parameters
     |
| 413 | 
     ARR00-C. Understand how arrays work
     |
| 413 | 
     MEM11-C. Do not assume infinite heap space
     |
| 413 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 415 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 416 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 416 | 
     EXP08-C. Ensure pointer arithmetic is used correctly
     |
| 418 | 
     EXP34-C. Do not dereference null pointers
     |
| 418 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 419 | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 419 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 420 | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| 420 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 421 | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 424 | 
     MEM34-C. Only free memory allocated dynamically
     |
| 427 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 429 | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| 429 | 
     FIO42-C. Close files when they are no longer needed
     |
| 429 | 
     ARR00-C. Understand how arrays work
     |
| 429 | 
     MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources
     |
| 433 | 
     MEM35-C. Allocate sufficient memory for an object
     |
| 436 | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| 438 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 438 | 
     MSC13-C. Detect and remove unused values
     |
| 440 | 
     MSC21-C. Use robust loop termination conditions
     |
| 442 | 
     MSC21-C. Use robust loop termination conditions
     |
| 443 | 
     MSC21-C. Use robust loop termination conditions
     |
| 444 | 
     EXP34-C. Do not dereference null pointers
     |
| 444 | 
     MSC21-C. Use robust loop termination conditions
     |
| 445 | 
     MSC21-C. Use robust loop termination conditions
     |
| 449 | 
     MEM30-C. Do not access freed memory
     |
| 449 | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| 454 | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| 455 | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| 456 | 
     CON01-C. Acquire and release synchronization primitives in the same module, at the same level of abstraction
     |
| 457 | 
     CON32-C. Prevent data races when accessing bit-fields from multiple threads
     |
| 457 | 
     CON43-C. Do not allow data races in multithreaded code
     |
| 457 | 
     POS49-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
     |
| 473 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 474 | 
     MSC01-C. Strive for logical completeness
     |
| 474 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 488 | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| 489 | 
     STR30-C. Do not attempt to modify string literals
     |
| 492 | 
     FIO47-C. Use valid format strings
     |
| 493 | 
     FIO47-C. Use valid format strings
     |
| 494 | 
     FIO47-C. Use valid format strings
     |
| 498 | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| 499 | 
     FIO47-C. Use valid format strings
     |
| 501 | 
     INT02-C. Understand integer conversion rules
     |
| 502 | 
     INT02-C. Understand integer conversion rules
     |
| 502 | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| 503 | 
     EXP13-C. Treat relational and equality operators as if they were nonassociative
     |
| 505 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 505 | 
     MSC13-C. Detect and remove unused values
     |
| 514 | 
     EXP46-C. Do not use a bitwise operator with a Boolean-like operand
     |
| 522 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 523 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 527 | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| 527 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 528 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 529 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 529 | 
     MSC13-C. Detect and remove unused values
     |
| 530 | 
     EXP33-C. Do not read uninitialized memory
     |
| 533 | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| 534 | 
     ERR33-C. Detect and handle standard library errors
     |
| 534 | 
     POS54-C. Detect and handle POSIX library errors
     |
| 534 | 
     EXP12-C. Do not ignore values returned by functions
     |
| 557 | 
     FIO47-C. Use valid format strings
     |
| 558 | 
     FIO47-C. Use valid format strings
     |
| 558 | 
     DCL10-C. Maintain the contract between the writer and caller of variadic functions
     |
| 559 | 
     FIO47-C. Use valid format strings
     |
| 559 | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| 559 | 
     INT00-C. Understand the data model used by your implementation(s)
     |
| 563 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 564 | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| 564 | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 566 | 
     FIO47-C. Use valid format strings
     |
| 569 | 
     INT02-C. Understand integer conversion rules
     |
| 570 | 
     INT02-C. Understand integer conversion rules
     |
| 571 | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| 573 | 
     INT02-C. Understand integer conversion rules
     |
| 574 | 
     INT02-C. Understand integer conversion rules
     |
| 576 | 
     ARR02-C. Explicitly specify array bounds, even if implicitly defined by an initializer
     |
| 578 | 
     DCL01-C. Do not reuse variable names in subscopes
     |
| 584 | 
     PRE07-C. Avoid using repeated question marks
     |
| 586 | 
     EXP43-C. Avoid undefined behavior when using restrict-qualified pointers
     |
| 586 | 
     ENV33-C. Do not call system()
     |
| 586 | 
     ERR34-C. Detect errors when converting a string to a number
     |
| 586 | 
     CON33-C. Avoid race conditions when using library functions
     |
| 586 | 
     CON37-C. Do not call signal() in a multithreaded program
     |
| 586 | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| 586 | 
     MSC33-C. Do not pass invalid data to the asctime() function
     |
| 586 | 
     POS44-C. Do not use signals to terminate threads
     |
| 586 | 
     POS47-C. Do not use threads that can be canceled asynchronously
     |
| 586 | 
     ERR04-C. Choose an appropriate termination strategy
     |
| 586 | 
     ERR06-C. Understand the termination behavior of assert() and abort()
     |
| 586 | 
     ERR07-C. Prefer functions that support error checking over equivalent functions that don't
     |
| 586 | 
     INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs
     |
| 586 | 
     MSC06-C. Beware of compiler optimizations
     |
| 586 | 
     MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| 586 | 
     MSC24-C. Do not use deprecated or obsolescent functions
     |
| 586 | 
     POS04-C. Avoid using PTHREAD_MUTEX_NORMAL type mutex locks
     |
| 586 | 
     SIG00-C. Mask signals handled by noninterruptible signal handlers
     |
| 586 | 
     SIG01-C. Understand implementation-specific details regarding signal handler persistence
     |
| 586 | 
     SIG02-C. Avoid using signals to implement normal functionality
     |
| 586 | 
     STR07-C. Use the bounds-checking interfaces for string manipulation
     |
| 586 | 
     WIN00-C. Be specific when dynamically loading libraries
     |
| 586 | 
     WIN01-C. Do not forcibly terminate execution
     |
| 586 | 
     WIN02-C. Restrict privileges when spawning child processes
     |
| 592 | 
     FIO30-C. Exclude user input from format strings
     |
| 601 | 
     DCL31-C. Declare identifiers before using them
     |
| 602 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 603 | 
     EXP33-C. Do not read uninitialized memory
     |
| 604 | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 612 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 613 | 
     EXP34-C. Do not dereference null pointers
     |
| 613 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 613 | 
     POS54-C. Detect and handle POSIX library errors
     |
| 613 | 
     API00-C. Functions should validate their parameters
     |
| 613 | 
     ARR00-C. Understand how arrays work
     |
| 613 | 
     MEM11-C. Do not assume infinite heap space
     |
| 613 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 616 | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| 620 | 
     DCL16-C. Use "L," not "l," to indicate a long value
     |
| 621 | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 621 | 
     DCL23-C. Guarantee that mutually visible identifiers are unique
     |
| 644 | 
     EXP33-C. Do not read uninitialized memory
     |
| 646 | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| 648 | 
     INT08-C. Verify that all integer values are in range
     |
| 650 | 
     INT08-C. Verify that all integer values are in range
     |
| 653 | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| 661 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 661 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 662 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 662 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 666 | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 668 | 
     EXP34-C. Do not dereference null pointers
     |
| 668 | 
     API00-C. Functions should validate their parameters
     |
| 668 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 669 | 
     ENV01-C. Do not make assumptions about the size of an environment variable
     |
| 669 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 670 | 
     MSC19-C. For functions that return an array, prefer returning an empty array over a null value
     |
| 673 | 
     MEM34-C. Only free memory allocated dynamically
     |
| 674 | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 676 | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| 679 | 
     INT08-C. Verify that all integer values are in range
     |
| 680 | 
     INT08-C. Verify that all integer values are in range
     |
| 682 | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| 689 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 697 | 
     EXP20-C. Perform explicit tests to determine success, true and false, and equality
     |
| 701 | 
     INT02-C. Understand integer conversion rules
     |
| 702 | 
     INT02-C. Understand integer conversion rules
     |
| 705 | 
     FIO47-C. Use valid format strings
     |
| 705 | 
     INT00-C. Understand the data model used by your implementation(s)
     |
| 706 | 
     FIO47-C. Use valid format strings
     |
| 706 | 
     INT00-C. Understand the data model used by your implementation(s)
     |
| 707 | 
     STR10-C. Do not concatenate different type of string literals
     |
| 714 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 715 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 715 | 
     MSC13-C. Detect and remove unused values
     |
| 718 | 
     DCL31-C. Declare identifiers before using them
     |
| 718 | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 719 | 
     FIO47-C. Use valid format strings
     |
| 719 | 
     DCL10-C. Maintain the contract between the writer and caller of variadic functions
     |
| 719 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 720 | 
     EXP45-C. Do not perform assignments in selection statements
     |
| 721 | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 722 | 
     EXP15-C. Do not place a semicolon on the same line as an if, for, or while statement
     |
| 731 | 
     EXP13-C. Treat relational and equality operators as if they were nonassociative
     |
| 732 | 
     INT02-C. Understand integer conversion rules
     |
| 733 | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 734 | 
     INT02-C. Understand integer conversion rules
     |
| 735 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 736 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 736 | 
     FLP03-C. Detect and handle floating-point errors
     |
| 737 | 
     API09-C. Compatible values should have the same type
     |
| 737 | 
     INT02-C. Understand integer conversion rules
     |
| 744 | 
     MSC01-C. Strive for logical completeness
     |
| 746 | 
     DCL31-C. Declare identifiers before using them
     |
| 746 | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 749 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 750 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 751 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 752 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 753 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 754 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 755 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 756 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 757 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 758 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 765 | 
     DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
     |
| 765 | 
     DCL19-C. Minimize the scope of variables and functions
     |
| 768 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 769 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 773 | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| 774 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 776 | 
     INT08-C. Verify that all integer values are in range
     |
| 777 | 
     FLP00-C. Understand the limitations of floating-point numbers
     |
| 777 | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| 784 | 
     STR11-C. Do not specify the bound of a character array initialized with a string literal
     |
| 787 | 
     MSC01-C. Strive for logical completeness
     |
| 789 | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| 790 | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| 793 | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 808 | 
     DCL31-C. Declare identifiers before using them
     |
| 816 | 
     FIO47-C. Use valid format strings
     |
| 818 | 
     DCL13-C. Declare function parameters that are pointers to values not changed by the function as const
     |
| 823 | 
     PRE11-C. Do not conclude macro definitions with a semicolon
     |
| 825 | 
     MSC17-C. Finish every set of statements associated with a case label with a break statement
     |
| 826 | 
     MEM35-C. Allocate sufficient memory for an object
     |
| 827 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 838 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 838 | 
     MSC13-C. Detect and remove unused values
     |
| 839 | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 846 | 
     INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression
     |
| 853 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 854 | 
     PRE07-C. Avoid using repeated question marks
     |
| 855 | 
     FIO47-C. Use valid format strings
     |
| 882 | 
     ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array
     |
| 901 | 
     EXP33-C. Do not read uninitialized memory
     |
| 908 | 
     MEM02-C. Immediately cast the result of a memory allocation function call into a pointer to the allocated type
     |
| 915 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 915 | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| 917 | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| 922 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 922 | 
     FLP36-C. Preserve precision when converting integral values to floating-point type
     |
| 931 | 
     EXP10-C. Do not depend on the order of evaluation of subexpressions or the order in which side effects take place
     |
| 936 | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 937 | 
     DCL20-C. Explicitly specify void when a function accepts no arguments
     |
| 942 | 
     FLP06-C. Convert integers to floating point for floating-point operations
     |
| 952 | 
     INT08-C. Verify that all integer values are in range
     |
| 953 | 
     DCL00-C. Const-qualify immutable objects
     |
| 958 | 
     EXP42-C. Do not compare padding data
     |
| 959 | 
     EXP42-C. Do not compare padding data
     |
| 967 | 
     PRE06-C. Enclose header files in an include guard
     |
| 973 | 
     PRE02-C. Macro replacement lists should be parenthesized
     |
| 978 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 1051 | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| 1776 | 
     STR30-C. Do not attempt to modify string literals
     |
| 1776 | 
     STR05-C. Use pointers to const when referring to string literals
     |
| 1972 | 
     MSC12-C. Detect and remove code that has no effect or is never executed
     |
| 2401 | 
     FIO47-C. Use valid format strings
     |
| 2402 | 
     FIO47-C. Use valid format strings
     |
| 2403 | 
     FIO47-C. Use valid format strings
     |
| 2403 | 
     INT00-C. Understand the data model used by your implementation(s)
     |
| 2404 | 
     FIO47-C. Use valid format strings
     |
| 2405 | 
     FIO47-C. Use valid format strings
     |
| 2406 | 
     FIO47-C. Use valid format strings
     |
| 2407 | 
     FIO47-C. Use valid format strings
     |
| 2408 | 
     DCL11-C. Understand the type issues associated with variadic functions
     |
| 2423 | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| 2434 | 
     MEM30-C. Do not access freed memory
     |
| 2434 | 
     MEM00-C. Allocate and free memory in the same module, at the same level of abstraction
     |
| 2440 | 
     EXP16-C. Do not compare function pointers to constant values
     |
| 2441 | 
     EXP16-C. Do not compare function pointers to constant values
     |
| 2445 | 
     EXP36-C. Do not cast pointers into more strictly aligned pointer types
     |
| 2454 | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| 2460 | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| 2460 | 
     MSC41-C. Never hard code sensitive information
     |
| 2461 | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| 2462 | 
     CON35-C. Avoid deadlock by locking in a predefined order
     |
| 2470 | 
     FIO13-C. Never push back anything other than one read character
     |
| 2471 | 
     FIO46-C. Do not access a closed file
     |
| 2472 | 
     FIO11-C. Take care when specifying the mode parameter of fopen()
     |
| 2473 | 
     FIO11-C. Take care when specifying the mode parameter of fopen()
     |
| 2478 | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| 2479 | 
     FIO39-C. Do not alternately input and output from a stream without an intervening flush or positioning call
     |
| 2480 | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| 2481 | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| 2498 | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| 2499 | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| 2601 | 
     POS34-C. Do not call putenv() with a pointer to an automatic variable as the argument
     |
| 2650 | 
     MSC21-C. Use robust loop termination conditions
     |
| 2662 | 
     ARR37-C. Do not add or subtract an integer to a pointer to a non-array object
     |
| 2666 | 
     PRE31-C. Avoid side effects in arguments to unsafe macros
     |
| 2670 | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| 2671 | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| 2704 | 
     INT08-C. Verify that all integer values are in range
     |
| 2704 | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| 2760 | 
     MSC32-C. Properly seed pseudorandom number generators
     |
| 2761 | 
     SIG30-C. Call only asynchronous-safe functions within signal handlers
     |
| 2762 | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| 2763 | 
     SIG34-C. Do not call signal() from within interruptible signal handlers
     |
| 2764 | 
     SIG35-C. Do not return from a computational exception signal handler
     |
| 2765 | 
     SIG31-C. Do not access shared objects in signal handlers
     |
| 4287 | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| 4376 | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| 9001 | 
     DCL18-C. Do not begin integer constants with 0 when specifying a decimal value
     |
| 9003 | 
     DCL19-C. Minimize the scope of variables and functions
     |
| 9005 | 
     EXP05-C. Do not cast away a const qualification
     |
| 9006 | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| 9007 | 
     EXP02-C. Be aware of the short-circuit behavior of the logical AND and OR operators
     |
| 9009 | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| 9012 | 
     EXP19-C. Use braces for the body of an if, for, or while statement
     |
| 9013 | 
     MSC01-C. Strive for logical completeness
     |
| 9022 | 
     PRE01-C. Use parentheses within macros around parameter names
     |
| 9024 | 
     PRE05-C. Understand macro replacement when concatenating tokens or performing stringification
     |
| 9026 | 
     PRE00-C. Prefer inline or static functions to function-like macros
     |
| 9035 | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| 9035 | 
     MEM05-C. Avoid large stack allocations
     |
| 9040 | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| 9046 | 
     DCL02-C. Use visually distinct identifiers
     |
| 9047 | 
     FIO38-C. Do not copy a FILE object
     |
| 9050 | 
     EXP00-C. Use parentheses for precedence of operation
     |
| 9055 | 
     MSC20-C. Do not use a switch statement to transfer control into a complex block
     |
| 9059 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 9060 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 9060 | 
     PRE07-C. Avoid using repeated question marks
     |
| 9066 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 9070 | 
     MEM05-C. Avoid large stack allocations
     |
| 9071 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 9074 | 
     DCL07-C. Include the appropriate type information in function declarators
     |
| 9088 | 
     INT16-C. Do not make assumptions about representation of signed integers
     |
| 9093 | 
     DCL37-C. Do not declare or define a reserved identifier
     |
| 9112 | 
     INT07-C. Use only explicitly signed or unsigned char type for numeric values
     |
| 9118 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 9120 | 
     FLP03-C. Detect and handle floating-point errors
     |
| 9146 | 
     DCL04-C. Do not declare more than one variable per declaration
     |
| 9148 | 
     INT09-C. Ensure enumeration constants map to unique values
     |
| 9209 | 
     STR09-C. Don't assume numeric values for expressions with type plain character
     |
| 9227 | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| 9227 | 
     FLP03-C. Detect and handle floating-point errors
     |
| 9233 | 
     INT13-C. Use bitwise operators only on unsigned operands
     |
| 9252 | 
     FLP00-C. Understand the limitations of floating-point numbers
     |
| 9252 | 
     FLP02-C. Avoid using floating-point numbers when precise computation is needed
     |
| 9259 | 
     MSC04-C. Use comments consistently and in a readable fashion
     |
| 9501 | 
     PRE32-C. Do not use preprocessor directives in invocations of function-like macros
     |
| 9502 | 
     PRE10-C. Wrap multistatement macros in a do-while loop
     |

