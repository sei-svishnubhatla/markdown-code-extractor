> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 1.38

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| alloca_bounds | 
     ARR32-C. Ensure size arguments for variable length arrays are in a valid range
     |
| Body of function falls-through | 
     MSC37-C. Ensure that control never reaches the end of a non-void function
     |
| comparable_char_blocks | 
     EXP42-C. Do not compare padding data
     |
| dangling_pointer | 
     DCL30-C. Declare objects with appropriate storage durations
     |
| dangling_pointer | 
     MEM30-C. Do not access freed memory
     |
| differing_blocks | 
     ARR36-C. Do not subtract or compare two pointers that do not refer to the same array
     |
| division_by_zero | 
     INT33-C. Ensure that division and remainder operations do not result in divide-by-zero errors
     |
| Exhaustively verified. | 
     FLP37-C. Do not use object representations to compare floating-point values
     |
| float_to_int | 
     FLP34-C. Ensure that floating-point conversions are within range of the new type
     |
| incompatible declaration | 
     DCL40-C. Do not create incompatible declarations of the same function or object
     |
| index_bound | 
     DCL38-C. Use the correct syntax when declaring a flexible array member
     |
| index_in_address | 
     ARR30-C. Do not form or use out-of-bounds pointers or array subscripts
     |
| index_in_address | 
     ARR39-C. Do not add or subtract a scaled integer to a pointer
     |
| initialisation | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| initialisation | 
     EXP33-C. Do not read uninitialized memory
     |
| malloc | 
     MEM31-C. Free dynamically allocated memory when no longer needed
     |
| match format and arguments | 
     STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string
     |
| match format and arguments | 
     FIO47-C. Use valid format strings
     |
| mem_access | 
     EXP34-C. Do not dereference null pointers
     |
| mem_access | 
     EXP40-C. Do not modify constant objects
     |
| mem_access | 
     STR30-C. Do not attempt to modify string literals
     |
| mem_access | 
     STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
     |
| mem_access | 
     MEM35-C. Allocate sufficient memory for an object
     |
| non-static declaration follows static declaration | 
     DCL36-C. Do not declare an identifier with conflicting linkage classifications
     |
| non-terminating | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| out of bounds read | 
     ARR38-C. Guarantee that library functions do not form invalid pointers
     |
| out of bounds read | 
     STR34-C. Cast characters to unsigned char before converting to larger integer sizes
     |
| out-of-range argument | 
     FLP32-C. Prevent or detect domain and range errors in math functions
     |
| pointer arithmetic | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| pointer arithmetic | 
     ERR33-C. Detect and handle standard library errors
     |
| separated | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| shift | 
     INT34-C. Do not shift an expression by a negative number of bits or by greater than or equal to the number of bits that exist in the operand
     |
| signed_downcast | 
     INT31-C. Ensure that integer conversions do not result in lost or misinterpreted data
     |
| signed_overflow | 
     INT32-C. Ensure that operations on signed integers do not result in overflow
     |
| type specifier missing | 
     DCL31-C. Declare identifiers before using them
     |
| unclassified ("free expects a free-able address") | 
     MEM34-C. Only free memory allocated dynamically
     |
| unclassified ("function type matches") | 
     EXP37-C. Call functions with the correct number and type of arguments
     |
| unclassified (variadic) | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| unsigned overflow | 
     INT30-C. Ensure that unsigned integer operations do not wrap
     |
| valid_char | 
     STR37-C. Arguments to character-handling functions must be representable as an unsigned char
     |
| variadic | 
     MSC39-C. Do not call va_arg() on a va_list that has an indeterminate value
     |

