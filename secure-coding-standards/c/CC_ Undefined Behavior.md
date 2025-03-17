According to the C Standard, Annex J, J.2 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], the behavior of a program is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) in the circumstances outlined in the following table. The "Guideline" column in the table identifies the coding practices that address the specific case of undefined behavior (UB). The descriptions of undefined behaviors in the "Description" column are direct quotes from the standard. The parenthesized numbers refer to the subclause of the C Standard (C23) that identifies the undefined behavior. 

| UB | Class | Description | Guideline |
| ----|----|----|----|
| 1  |  | A "shall" or "shall not" requirement that appears outside of a constraint is violated (clause 4). | MSC15-C  |
| 2  |  | A nonempty source file does not end in a new-line character which is not immediately preceded by a backslash character or ends in a partial preprocessing token or comment (5.1.1.2). |  |
| 3  |  | Token concatenation produces a character sequence matching the syntax of a universal character name (5.1.1.2). | PRE30-C  |
| 4  |  | A program in a hosted environment does not define a function named main using one of the specified forms (5.1.2.3.2). |  |
| 5 |  | The execution of a program contains a data race (5.1.2.5). |  |
| 6; |  | A character not in the basic source character set is encountered in a source file, except in an identifier, a character constant, a string literal, a header name, a comment, or a preprocessing token that is never converted to a token (5.2.1). |  |
| 7; |  | An identifier, comment, string literal, character constant, or header name contains an invalid multibyte character or does not begin and end in the initial shift state (5.2.2). |  |
| 8 |  | The same identifier has both internal and external linkage in the same translation unit (6.2.2). | DCL36-C  |
| 9; |  | An object is referred to outside of its lifetime (6.2.4). | DCL21-C, DCL30-C  |
| 10;  |  | The value of a pointer to an object whose lifetime has ended is used (6.2.4). | DCL30-C, EXP33-C |
| 11 |  | The value of an object with automatic storage duration is used while the object has an indeterminate representation;(6.2.4, 6.7.11, 6.8). | EXP33-C, MSC22-C |
| 12 |  | A non-value representation is read by an lvalue expression that does not have character type (6.2.6.1). | EXP33-C  |
| 13 |  | A non-value representation is produced by a side effect that modifies any part of the object;using an lvalue expression that does not have character type (6.2.6.1). |  |
| 14 |  | Two declarations of the same object or function specify types that are not compatible (6.2.7). | DCL23-C, 
DCL40-C |
| 15 |  | A program requires the formation of a composite type from a variable length array type whose size is specified by an expression that is not evaluated (6.2.7). |  |
| 16 |  | Conversion to or from an integer type produces a value outside the range that can be represented (6.3.1.4). | FLP34-C  |
| 17 |  | Demotion of one real floating type to another produces a value outside the range that can be represented (6.3.1.5). | FLP34-C  |
| 18  |  | An lvalue does not designate an object when evaluated (6.3.2.1). |  |
| 19  |  | A non-array lvalue with an incomplete type is used in a context that requires the value of the designated object (6.3.2.1). |  |
| 20; |  | An lvalue designation an object of automatic storage duration that could have been declared with the register storage class is used in a context that requires the value of the designated object, but the object is uninitialized (6.3.2.1). |  |
| 21 |  | An lvalue having array type is converted to a pointer to the initial element of the array, and the array object has register storage class (6.3.2.1). |  |
| 22; |  | An attempt is made to use the value of a void expression, or an implicit or explicit conversion (except to void) is applied to a void expression (6.3.2.2). |  |
| 23; |  | Conversion of a pointer to an integer type produces a value outside the range that can be represented (6.3.2.3). | INT36-C  |
| 24; |  | Conversion between two pointer types produces a result that is incorrectly aligned (6.3.2.3). | EXP36-C  |
| 25 |  | A pointer is used to call a function whose type is not compatible with the referenced type;(6.3.2.3). | EXP37-C |
| 26; |  | An unmatched ' or " character is encountered on a logical source line during tokenization (6.4). |  |
| 27; |  | A reserved keyword token is used in translation phase 7 or 8 (5.1.1.2);for some purpose other than as a keyword (6.4.1). |  |
| 28; |  | A universal character name in an identifier does not designate a character whose encoding falls into one of the specified ranges (6.4.2.1). |  |
| 29; |  | The initial character of an identifier is a universal character name designating a digit (6.4.2.1). |  |
| 30; |  | Two identifiers differ only in nonsignificant characters (6.4.2.1). | DCL23-C,DCL31-C |
| 31; |  | The identifier __func__;is explicitly declared (6.4.2.2). |  |
| 32; |  | The program attempts to modify a string literal (6.4.5). | STR30-C  |
| 33; |  | The characters ', back-slash, ", /, or /* occur in the sequence between the < and > delimiters, or the characters ', back-slash, //, or /* occur in the sequence between the " delimiters, in a header name preprocessing token (6.4.7). | EXP39-C |
| 34; |  | A side effect on a scalar object is unsequenced relative to either a different side effect on the same scalar object or a value computation using the value of the same scalar object (6.5.1). | EXP30-C  |
| 35; |  | An exceptional condition occurs during the evaluation of an expression (6.5.1). | INT32-C |
| 36; |  | An object has its stored value accessed other than by an lvalue of an allowable type (6.5.1). | DCL40-C,EXP39-C  |
| 37; |  | A function is defined with a type that is not compatible with the type (of the expression);pointed to by the expression that denotes the called function (6.5.3.3). | DCL40-C,EXP37-C |
| 38  |  | A member of an atomic structure or union is accessed (6.5.3.4). |  |
| 39; |  | The operand of the unary * operator has an invalid value (6.5.4.2). | EXP34-C |
| 40; |  | A pointer is converted to other than an integer or pointer type (6.5.5). |  |
| 41; |  | The value of the second operand of the / or % operator is zero (6.5.6). | INT33-C  |
| 42 |  | If the quotient a/b is not representable, the behavior of both a/b and a%b (6.5.6). |  |
| 43 |  | Addition or subtraction of a pointer into, or just beyond, an array object and an integer type produces a result that does not point into, or just beyond, the same array object (6.5.7). | ARR30-C |
| 44 |  | Addition or subtraction of a pointer into, or just beyond, an array object and an integer type produces a result that points just beyond the array object and is used as the operand of a unary * operator that is evaluated (6.5.7). | ARR30-C |
| 45; |  | Pointers that do not point into, or just beyond, the same array object are subtracted (6.5.7). | ARR36-C  |
| 46; |  | An array subscript is out of range, even if an object is apparently accessible with the given subscript (as in the lvalue expression a[1][7] given the declaration int a[4][5]) (6.5.7). | ARR30-C |
| 47; |  | The result of subtracting two pointers is not representable in an object of type ptrdiff_t (6.5.7). |  |
| 48  |  | An expression is shifted by a negative number or by an amount greater than or equal to the width of the promoted expression (6.5.8). | INT34-C  |
| 49; |  | An expression having signed promoted type is left-shifted and either the value of the expression is negative or the result of shifting would not be representable in the promoted type (6.5.8). |  |
| 50; |  | Pointers that do not point to the same aggregate or union (nor just beyond the same array object) are compared using relational operators (6.5.9). | ARR36-C  |
| 51 |  | An object is assigned to an inexactly overlapping object or to an exactly overlapping object with incompatible type (6.5.17.2). |  |
| 52; |  | An expression that is required to be an integer constant expression does not have an integer;type; has operands that are not integer constants, named constants, compound literal constants, enumeration constants, character constants, predefined constants, sizeof expressions whose results are integer constants, alignof expressions, or immediately-cast floating constants; or contains casts (outside operands to sizeof and alignof operators) other than conversions of arithmetic types to integer types (6.6). |  |
| 53 |  | A constant expression in an initializer is not, or does not evaluate to, one of the following: a;named constant, a compound literal constant, an arithmetic constant expression, a null pointer constant, an address constant, or an address constant for a complete object type plus or minus an integer constant expression (6.6). |  |
| 54 |  | An arithmetic constant expression does not have arithmetic type; has operands that are not;integer constants, floating constants, named and compound literal constants of arithmetic type, character constants, predefined constants, sizeof expressions whose results are integer constants, or alignof expressions; or contains casts (outside operands to sizeof or alignof operators) other than conversions of arithmetic types to arithmetic types (6.6). |  |
| 55 |  | The value of an object is accessed by an array-subscript [], member-access . or ->, address &, or indirection * operator or a pointer cast in creating an address constant (6.6). |  |
| 56; |  | An identifier for an object is declared with no linkage and the type of the object is incomplete after its declarator, or after its init-declarator if it has an initializer (6.7). |  |
| 57; |  | A function is declared at block scope with an explicit storage-class specifier other than extern (6.7.2). |  |
| 58 |  | A structure or union is defined as containing no named members;(including those specified indirectly via anonymous structures and unions) (6.7.3.2). |  |
| 59; |  | An attempt is made to access, or generate a pointer to just past, a flexible array member of a structure when the referenced object provides no elements for that array (6.7.3.2). | ARR30-C |
| 60 |  | When the complete type is needed, an incomplete structure or union type is not completed in the same scope by another declaration of the tag that defines the content (6.7.3.4). |  |
| 61; |  | An attempt is made to modify an object defined with a const-qualified type through use of an lvalue with non-const-qualified type (6.7.4). | EXP05-C, EXP40-C  |
| 62; |  | An attempt is made to refer to an object defined with a volatile-qualified type through use of an lvalue with non-volatile-qualified type (6.7.4). | EXP32-C  |
| 63 |  | The specification of a function type includes any type qualifiers (6.7.4). |  |
| 64; |  | Two qualified types that are required to be compatible do not have the identically qualified version of a compatible type (6.7.4). |  |
| 65; |  | An object which has been modified is accessed through a restrict-qualified pointer to a const-qualified type, or through a restrict-qualified pointer and another pointer that are not both based on the same object (6.7.4.2). | EXP43-C |
| 66 |  | A restrict-qualified pointer is assigned a value based on another restricted pointer whose associated block neither began execution before the block associated with this pointer, nor ended before the assignment (6.7.4.2). |  |
| 67 |  | A function with external linkage is declared with an inline function specifier, but is not also defined in the same translation unit (6.7.5). |  |
| 68 |  | A function declared with a _Noreturn function specifier returns to its caller (6.7.5). |  |
| 69 |  | The definition of an object has an alignment specifier and another declaration of that object has a different alignment specifier (6.7.6). |  |
| 70 |  | Declarations of an object in different translation units have different alignment specifiers (6.7.6). |  |
| 71 |  | Two pointer types that are required to be compatible are not identically qualified, or are not pointers to compatible types (6.7.7.2). |  |
| 72 |  | The size expression in an array declaration is not a constant expression and evaluates at program execution time to a nonpositive value (6.7.7.3). | ARR32-C |
| 73 |  | In a context requiring two array types to be compatible, they do not have compatible element types, or their size specifiers evaluate to unequal values (6.7.7.23). | EXP39-C |
| 74 |  | A declaration of an array parameter includes the keyword static within the [ and ] and the corresponding argument does not provide access to the first element of an array with at least the specified number of elements (6.7.7.4). |  |
| 75; |  | A storage-class specifier or type qualifier modifies the keyword void as a function parameter type list (6.7.7.4). |  |
| 76; |  | In a context requiring two function types to be compatible, they do not have compatible return types, or their parameters disagree in use of the ellipsis terminator or the number and type of parameters (after default argument promotion, when there is no parameter type list) (6.7.7.4). |  |
| 77 |  | A declaration for which a type is inferred contains a pointer, array, or function declarators;(6.7.10). |  |
| 78 |  | A declaration for which a type is inferred contains no or more than one declarators (6.7.10). |  |
| 79 |  | The value of an unnamed member of a structure or union is used (6.7.11). |  |
| 80 |  | The initializer for a scalar is neither a single expression nor a single expression enclosed in braces (6.7.11). |  |
| 81; |  | The initializer for a structure or union object is neither an initializer list nor a single expression;that has compatible structure or union type (6.7.11). |  |
| 82 |  |  |  |
| 83 |  | A function definition that does not have the asserted property is called by a function declaration or a function pointer with a type that has the unsequenced or reproducible attribute (6.7.13.8). |  |
| 84 |  | An identifier with external linkage is used, but in the program there does not exist exactly one external definition for the identifier, or the identifier is not used and there exist multiple external definitions for the identifier (6.9). |  |
| 85  |  | A function that accepts a variable number of arguments is defined without a parameter type list that ends with the ellipsis notation (6.9.2). |  |
| 86; |  | The } that terminates a function is reached, and the value of the function call is used by the caller (6.9.2). | MSC37-C |
| 87; |  | An identifier for an object with internal linkage and an incomplete type is declared with a tentative definition (6.9.3). |  |
| 88 |  | A non-directive preprocessing directive is executed (6.10). |  |
| 89 |  | The token defined is generated during the expansion of a #if or #elif preprocessing directive, or the use of the defined unary operator does not match one of the two specified forms prior to macro replacement (6.10.2). |  |
| 90 |  | The #include preprocessing directive that results after expansion does not match one of the two header name forms (6.10.3). | EXP43-C |
| 91 |  | The character sequence in an #include preprocessing directive does not start with a letter (6.10.3). |  |
| 92 |  | There are sequences of preprocessing tokens within the list of macro arguments that would otherwise act as preprocessing directives (6.10.5). | PRE32-C  |
| 93; |  | The result of the preprocessing operator # is not a valid character string literal (6.10.5.2). |  |
| 94; |  | The result of the preprocessing operator ## is not a valid preprocessing token (6.10.5.3). |  |
| 95; |  | The #line preprocessing directive that results after expansion does not match one of the two well-defined forms, or its digit sequence specifies zero or a number greater than 2147483647 (6.10.6). |  |
| 96; |  | A non-STDC #pragma preprocessing directive that is documented as causing translation failure or some other form of undefined behavior is encountered (6.10.8). |  |
| 97 |  | A #pragma STDC preprocessing directive does not match one of the well-defined forms (6.10.8). |  |
| 98; |  | The name of a predefined macro, or the identifier defined, is the subject of a #define or #undef preprocessing directive (6.10.10). |  |
| 99 |  | An attempt is made to copy an object to an overlapping object by use of a library function, other than as explicitly allowed (e.g., memmove) (clause 7). |  |
| 100; |  | A file with the same name as one of the standard headers, not provided as part of the implementation, is placed in any of the standard places that are searched for included source files (7.1.2). |  |
| 101 |  | A header is included within an external declaration or definition (7.1.2). |  |
| 102 |  | A function, object, type, or macro that is specified as being declared or defined by some standard header is used before any header that declares or defines it is included (7.1.2). |  |
| 103 |  | A standard header is included while a macro is defined with the same name as a keyword (7.1.2). |  |
| 104 |  | The program attempts to declare a library function itself, rather than via a standard header, but the declaration does not have external linkage (7.1.2). |  |
| 105 |  | The program declares or defines a reserved identifier, other than as allowed by 7.1.4 (7.1.3). | DCL37-C  |
| 106 |  | The program removes the definition of a macro whose name begins with an underscore and either an uppercase letter or another underscore (7.1.3). |  |
| 107 |  | An argument to a library function has an invalid value or a type not expected by a function with a variable number of arguments (7.1.4). |  |
| 108 |  | The pointer passed to a library function array parameter does not have a value such that all address computations and object accesses are valid (7.1.4). | ARR30-C, ARR38-C |
| 109 |  | The macro definition of assert is suppressed in order to access an actual function (7.2). | MSC38-C |
| 110 |  | The argument to the assert macro does not have a scalar type (7.2). |  |
| 111; |  | The CX_LIMITED_RANGE, FENV_ACCESS, or FP_CONTRACT pragma is used in any context other than outside all external declarations or preceding all explicit declarations and statements inside a compound statement (7.3.4, 7.6.1, 7.12.2). |  |
| 112 |  | The value of an argument to a character handling function is neither equal to the value of EOF nor representable as an unsigned char (7.4). | STR37-C  |
| 113 |  | A macro definition of errno is suppressed in order to access an actual object, or the program defines an identifier with the name errno (7.5). | DCL37-C, MSC38-C |
| 114 |  | Part of the program tests floating-point status flags, sets floating-point control modes, or runs under non-default mode settings, but was translated with the state for the FENV_ACCESS pragma "off" (7.6.1). |  |
| 115 |  | The exception-mask argument for one of the functions that provide access to the floating-point status flags has a nonzero value not obtained by bitwise OR of the floating-point exception macros (7.6.2). |  |
| 116 |  | The fesetexceptflag function is used to set floating-point status flags that were not specified in the call to the fegetexceptflag function that provided the value of the corresponding fexcept_t object (7.6.4.5). |  |
| 117 |  | The argument to fesetenv or feupdateenv is neither an object set by a call to fegetenv or feholdexcept, nor is it an environment macro (7.6.6.3, 7.6.6.4). |  |
| 118 |  | The value of the result of an integer arithmetic or conversion function cannot be represented (7.8.2.1, 7.8.2.2, 7.8.2.3, 7.8.2.4, 7.24.6.1, 7.24.6.2, 7.24.1). | ERR07-C  |
| 119; |  | The program modifies the string pointed to by the value returned by the setlocale function (7.11.1.1). | ENV30-C  |
| 120 |  | A pointer returned by the setlocale function is used after a subsequent call to the function, or after the calling thread has exited (7.11.1.1). |  |
| 121; |  | The program modifies the structure pointed to by the value returned by the localeconv function (7.11.2.1). | ENV30-C  |
| 122 |  | The initializer for an aggregate or union, other than an array initialized by a string literal, is not a brace-enclosed list of initializers for its elements or members (6.7.11).A macro definition of math_errhandling is suppressed or the program defines an identifier with the name math_errhandling (7.12). | MSC38-C |
| 123 |  | An argument to a floating-point classification or comparison macro is not of real floating type (7.12.3, 7.12.17). |  |
| 124 |  | A macro definition of setjmp;is suppressed to access an actual function, or the program defines an external identifier with the name setjmp (7.13). | MSC38-C |
| 125 |  | An invocation of the setjmp macro occurs other than in an allowed context (7.13.2.1). | MSC22-C |
| 126; |  | The longjmp function is invoked to restore a nonexistent environment (7.13.2.1). | MSC22-C |
| 127 |  | After a longjmp, there is an attempt to access the value of an object of automatic storage class with non-volatile-qualified type, local to the function containing the invocation of the corresponding setjmp macro, that was changed between the setjmp invocation and longjmp call (7.13.2.1). | MSC22-C |
| 128; |  | The program specifies an invalid pointer to a signal handler function (7.14.1.1). |  |
| 129; |  | A signal handler returns when the signal corresponded to a computational exception (7.14.1.1). | SIG31-C  |
| 130 |  | A signal handler called in response to SIGFPE, SIGILL, SIGSEGV, or any other implementation-defined value corresponding to a computational exception returns (7.14.1.1). | SIG35-C |
| 131 |  | A signal occurs as the result of calling the abort or raise function, and the signal handler calls the raise function (7.14.1.1). | SIG30-C,SIG31-C  |
| 132 |  | A signal occurs other than as the result of calling the abort or raise function, and the signal;handler refers to an object with static or thread storage duration that is not a lock-free atomic object other than by assigning a value to an object declared as volatile sig_atomic_t, or calls any function in the standard library other than the abort function, the_Exit function, the quick_exit function, the functions in  (except where explicitly stated otherwise) when the atomic arguments are lock-free, the atomic_is_lock_free function with any atomic argument, or the signal function (for the same signal number) (7.14.1.1). | SIG31-C  |
| 133; |  | The value of errno is referred to after a signal occurred other than as the result of calling the abort or raise function and the corresponding signal handler obtained a SIG_ERR return from a call to the signal function (7.14.1.1). | ERR32-C  |
| 134 |  | A signal is generated by an asynchronous signal handler (7.14.1.1). |  |
| 135 |  | The signal function is used in a multi-threaded program (7.14.1.1). | CON37-C |
| 136; |  | A function with a variable number of arguments attempts to access its varying arguments other than through a properly declared and initialized va_list object, or before the va_start macro is invoked (7.16, 7.16.1.1, 7.16.1.4). |  |
| 137 |  | The macro va_arg is invoked using the parameter ap that was passed to a function that invoked the macro va_arg with the same parameter (7.16). |  |
| 138 |  | A macro definition of va_start, va_arg, va_copy, or va_end is suppressed in order to access an actual function, or the program defines an external identifier with the name va_copy or va_end (7.16.1). | MSC38-C |
| 139 |  | The va_start or va_copy macro is invoked without a corresponding invocation of the va_end macro in the same function, or vice versa (7.16.1, 7.16.1.2, 7.16.1.3, 7.16.1.4). |  |
| 140 |  | The va_arg macro is invoked when there is no actual next argument, or with a specified type that is not compatible with the promoted type of the actual next argument, with certain exceptions (7.16.1.1). |  |
| 141 |  | The type parameter to the va_arg macro is not such that a pointer to an object of that type can be obtained simply by postfixing a * (7.16.1.1). |  |
| 142 |  | Using a null pointer constant in form of an integer expression as an argument to a . . . function;and then interpreting it as a void* or char* (7.16.1.1). |  |
| 143; |  | The va_copy or va_start macro is called to initialize a va_list that was previously initialized by either macro without an intervening invocation of the va_end macro for the same va_list (7.16.1.2, 7.16.1.4). |  |
| 144 |  | The va_start macro is invoked with additional arguments that include unbalanced parentheses, or unrecognized preprocessing tokens (7.16.1.4). |  |
| 145; |  | The macro definition of a generic function is suppressed to access an actual function (7.17.1, 7.18). |  |
| 146 |  | The type parameter of an offsetof macro defines a new type (7.21). |  |
| 147 |  | When program execution reaches an unreachable() macro invocation (7.21.1). |  |
| 148 |  | Arbitrarily copying or changing the bytes of or copying from a non-null pointer into a nullptr_t object and then reading that object (7.21.2). |  |
| 149 |  | The member designator parameter of an offsetof macro is an invalid right operand of the . operator for the type parameter, or designates a bit-field (7.21). |  |
| 150 |  | The argument in an instance of one of the integer-constant macros is not a decimal, octal, or hexadecimal constant, or it has a value that exceeds the limits for the corresponding type (7.22.4). |  |
| 151 |  | A byte input/output function is applied to a wide-oriented stream, or a wide character input/output function is applied to a byte-oriented stream (7.23.2). |  |
| 152 |  | Use is made of any portion of a file beyond the most recent wide character written to a wide-oriented stream (7.23.2). |  |
| 153 |  | The value of a pointer to a FILE object is used after the associated file is closed (7.23.3). | FIO46-C |
| 154 |  | The stream for the fflush function points to an input stream or to an update stream in which the most recent operation was input (7.23.5.2). |  |
| 155 |  | The string pointed to by the mode argument in a call to the fopen function does not exactly match one of the specified character sequences (7.23.5.3). |  |
| 156 |  | An output operation on an update stream is followed by an input operation without an intervening call to the fflush function or a file positioning function, or an input operation on an update stream is followed by an output operation with an intervening call to a file positioning function (7.23.5.3). | FIO39-C  |
| 157 |  | An attempt is made to use the contents of the array that was supplied in a call to the setvbuf function (7.23.5.6). |  |
| 158; |  | There are insufficient arguments for the format in a call to one of the formatted input/output functions, or an argument does not have an appropriate type (7.23.6.1, 7.23.6.2, 7.31.2.1, 7.31.2.2). | FIO47-C  |
| 159 |  | The format in a call to one of the formatted input/output functions or to the strftime or wcsftime function is not a valid multibyte character sequence that begins and ends in its initial shift state;(7.23.6.1, 7.23.6.2, 7.29.3.5, 7.31.2.1, 7.31.2.2, 7.31.5.1). |  |
| 160 |  | In a call to one of the formatted output functions, a precision appears with a conversion specifier other than those described (7.23.6.1, 7.31.2.1). | FIO47-C; |
| 161 |  | A conversion specification for a formatted output function uses an asterisk to denote an argument-supplied field width or precision, but the corresponding argument is not provided (7.23.6.1, 7.31.2.1). |  |
| 162 |  | A conversion specification for a formatted output function uses a # or 0 flag with a conversion specifier other than those described (7.23.6.1, 7.31.2.1). | FIO47-C; |
| 163 |  | A conversion specification for one of the formatted input/output functions uses a length modifier with a conversion specifier other than those described (7.23.6.1, 7.23.6.2, 7.31.2.1,7.31.2.2). | FIO47-C; |
| 164 |  | An s conversion specifier is encountered by one of the formatted output functions, and the argument is missing the null terminator (unless a precision is specified that does not require null termination) (7.23.6.1, 7.31.2.1). |  |
| 165 |  | An n conversion specification for one of the formatted input/output functions includes any flags, an assignment-suppressing character, a field width, or a precision (7.23.6.1, 7.23.6.2,;7.31.2.1, 7.31.2.2). |  |
| 166 |  | A % conversion specifier is encountered by one of the formatted input/output functions, but the complete conversion specification is not exactly %% (7.23.6.1, 7.23.6.2, 7.31.2.1, 7.31.2.2). | FIO47-C; |
| 167 |  | An invalid conversion specification is found in the format for one of the formatted input/output functions, or the strftime or wcsftime function (7.23.6.1, 7.23.6.2, 7.29.3.5, 7.31.2.1,;7.31.2.2, 7.31.5.1). | FIO47-C |
| 168 |  | The number of characters or wide characters transmitted by a formatted output function (or written to an array, or that would have been written to an array) is greater than INT_MAX (7.23.6.1, 7.31.2.1). |  |
| 169 |  | The number of input items assigned by a formatted input function is greater than INT_MAX (7.23.6.2, 7.31.2.2). |  |
| 170 |  | The result of a conversion by one of the formatted input functions cannot be represented in the corresponding object, or the receiving object does not have an appropriate type (7.23.6.2, 7.31.2.2). |  |
| 171 |  | A c, s, or [ conversion specifier is encountered by one of the formatted input functions, and the array pointed to by the corresponding argument is not large enough to accept the input sequence (and a null terminator if the conversion specifier is s or [) (7.23.6.2, 7.31.2.2). |  |
| 172 |  | A c, s, or [ conversion specifier with an l qualifier is encountered by one of the formatted input functions, but the input is not a valid multibyte character sequence that begins in the initial shift state (7.23.6.2, 7.31.2.2). |  |
| 173 |  | The input item for a %p conversion by one of the formatted input functions is not a value converted earlier during the same program execution (7.23.6.2, 7.31.2.2). |  |
| 174 |  | The vfprintf, vfscanf, vprintf, vscanf, vsnprintf, vsprintf, vsscanf, vfwprintf, vfwscanf, vswprintf, vswscanf, vwprintf, or vwscanf function is called with an improperly initialized va_list argument, or the argument is used (other than in an invocation of va_end) after the function returns (7.23.6.8, 7.23.6.9, 7.23.6.10, 7.23.6.11, 7.23.6.12, 7.23.6.13, 7.23.6.14,;7.31.2.5, 7.31.2.6, 7.31.2.7, 7.31.2.8, 7.31.2.9, 7.31.2.10). |  |
| 175 |  | The contents of the array supplied in a call to the fgets, gets, or fgetws function are used after a read error occurred (7.23.7.2, 7.31.3.2). | FIO40-C  |
| 176 |  | The n parameter is negative or zero for a call to fgets or fgetws. (7.23.7.2, 7.31.3.2). |  |
| 177; |  | The file position indicator for a binary stream is used after a call to the ungetc function where its value was zero before the call (7.23.7.11). |  |
| 178 |  | The file position indicator for a stream is used after an error occurred during a call to the fread or fwrite function (7.23.8.1, 7.23.8.2). |  |
| 179 |  | A partial element read by a call to the fread function is used (7.23.8.1). |  |
| 180 |  | The fseek function is called for a text stream with a nonzero offset and either the offset was not returned by a previous successful call to the ftell function on a stream associated with the same file or whence is not SEEK_SET (7.23.9.2). |  |
| 181 |  | The fsetpos function is called to set a position that was not returned by a previous successful call to the fgetpos function on a stream associated with the same file (7.23.9.3). |  |
| 182 |  | A non-null pointer returned by a call to the calloc, malloc, realloc, or aligned_alloc function with a zero requested size is used to access an object (7.24.3). | MEM04-C |
| 183 |  | The value of a pointer that refers to space deallocated by a call to the free or realloc function is used (7.24.3). | MEM30-C  |
| 184 |  | The pointer argument to the free or realloc function is unequal to a null pointer and does;not match a pointer earlier returned by a memory management function, or the space has been deallocated by a call to free or realloc (7.24.3.3, 7.24.3.7). | MEM34-C  |
| 185 |  | The value of the object allocated by the malloc function is used (7.24.3.4). |  |
| 186 |  | The values of any bytes in a new object allocated by the realloc function beyond the size of the old object are used (7.24.3.7). | EXP33-C |
| 187; |  | The program calls the exit or quick_exit function more than once, or calls both functions (7.24.4.4, 7.24.4.7). | ENV32-C,ERR04-C |
| 188 |  | During the call to a function registered with the atexit or at_quick_exit function, a call is made to the longjmp function that would terminate the call to the registered function (7.24.4.4, 7.24.4.7). | ENV32-C |
| 189 |  | The string set up by the getenv or strerror function is modified by the program (7.24.4.6, 7.26.6.3). | ENV30-C  |
| 190 |  | A signal is raised while the quick_exit function is executing (7.24.4.7). |  |
| 191 |  | A command is executed through the system function in a way that is documented as causing termination or some other form of undefined behavior (7.24.4.8). |  |
| 192 |  | A searching or sorting utility function is called with an invalid pointer argument, even if the number of elements is zero (7.24.5). |  |
| 193 |  | The comparison function called by a searching or sorting utility function alters the contents of the array being searched or sorted, or returns ordering values inconsistently (7.24.5). |  |
| 194 |  | The array being searched by the bsearch function does not have its elements in proper order (7.24.5.1). |  |
| 195 |  | The current conversion state is used by a multibyte/wide character conversion function after changing the LC_CTYPE category (7.24.7). |  |
| 196 |  | A string or wide string utility function is instructed to access an array beyond the end of an object (7.26.1, 7.31.4). |  |
| 197 |  | A string or wide string utility function is called with an invalid pointer argument, even if the length is zero (7.26.1, 7.31.4). |  |
| 198 |  | The contents of the destination array are used after a call to the strxfrm, strftime, wcsxfrm, or wcsftime function in which the specified length was too small to hold the entire null-terminated result;(7.26.4.5, 7.29.3.5, 7.31.4.4.4, 7.31.5.1). |  |
| 199 |  | A sequence of calls of the strtok function is made from different threads (7.26.5.9). |  |
| 200 |  | The first argument in the very first call to the strtok or wcstok is a null pointer (7.26.5.9,;7.31.4.5.8). |  |
| 201 |  | A pointer returned by the strerror function is used after a subsequent call to the function, or;after the calling thread has exited (7.26.6.3). |  |
| 202 |  | The type of an argument to a type-generic macro is not compatible with the type of the corresponding parameter of the selected function (7.27). |  |
| 203 |  | Arguments for generic parameters of a type-generic macro are such that some argument has a;corresponding real type that is of standard floating type and another argument is of decimal floating type (7.27). |  |
| 204 |  | Arguments for generic parameters of a type-generic macro are such that neither  and  define a function whose generic parameters have the determined corresponding real type (7.27). |  |
| 205 |  | A complex argument is supplied for a generic parameter of a type-generic macro that has no corresponding complex function (7.27). |  |
| 206 |  | A decimal floating argument is supplied for a generic parameter of a type-generic macro that;expects a complex argument (7.27). |  |
| 207 |  | A standard floating or complex argument is supplied for a generic parameter of a type-generic;macro that expects a decimal floating type argument (7.27). |  |
| 208 |  | A non-recursive mutex passed to mtx_lock is locked by the calling thread (7.28.4.3). |  |
| 209 |  | The mutex passed to mtx_timedlock does not support timeout (7.28.4.4). |  |
| 210 |  | The mutex passed to mtx_unlock is not locked by the calling thread (7.28.4.6). |  |
| 211 |  | The thread passed to thrd_detach or thrd_join was previously detached or joined with;another thread (7.28.5.3, 7.28.5.6). |  |
| 212 |  | The tss_create function is called from within a destructor (7.28.6.1). |  |
| 213 |  | The key passed to tss_delete, tss_get, or tss_set was not returned by a call to tss_create before the thread commenced executing destructors (7.28.6.2, 7.28.6.3, 7.28.6.4). |  |
| 214 |  | An attempt is made to access the pointer returned by the time conversion functions after the thread that originally called the function to obtain it has exited (7.29.3). |  |
| 215 |  | At least one member of the broken-down time passed to asctime contains a value outside its normal range, or the calculated year exceeds four digits or is less than the year 1000 (7.29.3.1). |  |
| 216 |  | The argument corresponding to an s specifier without an l qualifier in a call to the fwprintf function does not point to a valid multibyte character sequence that begins in the initial shift state (7.31.2.11). |  |
| 217 |  | In a call to the wcstok function, the object pointed to by ptr does not have the value stored by the previous call for the same wide string (7.31.4.5.8). |  |
| 218 |  | An mbstate_t object is used inappropriately (7.31.6). | EXP33-C |
| 219 |  | The value of an argument of type wint_t to a wide character classification or case mapping function is neither equal to the value of WEOF nor representable as a wchar_t (7.32.1). |  |
| 220 |  | The iswctype function is called using a different LC_CTYPE category from the one in effect for the call to the wctype function that returned the description (7.32.2.2.1). |  |
| 221 |  | The towctrans function is called using a different LC_CTYPE category from the one in effect for the call to the wctrans function that returned the description (7.32.3.2.1). |  |

Graphical symbols used in the preceding table:

| Symbol |
| ----|
| Critical Undefined Behavior |
| Bounded Undefined Behavior |
| Undefined Behavior (information/confirmation needed) |
| Possible Conforming Language Extension |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/BB.+Definitions?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/CERT+C+Coding+Standard) [](https://www.securecoding.cert.org/confluence/display/seccode/DD.+Unspecified+Behavior?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| hi, i'm beginner in CERT C Coding Standard, and I have two questions.;First, there are 58 unspecified behaviors and 203 undefined behavior in C11.and according to this page, it seems that only 8 of 58 unspecified behaviors and 75 of 203 undefined behaviors can be avoided by complying with CERT C Coding Standard, is it right?I wonder whether it is true or not. Second, if it is true, it might be too weak to apply CERT C to some safety-critical systems which i'm going to develop considering CERT C Coding Standard is a necessary not sufficient set of rules for developing safe, reliable and secure systems.in order to be applied to develop safety-critical systems, i think there should be huge updates or great changes and i seriously wonder the plan. is there anybody who can help me?I will appreciate your advices and help.
                                        Posted by bycho at Oct 25, 2016 08:52
                                     |
| I am not certain that this page has been kept up to date with the list of secure coding rules, but the possibility still exists that we do not have rules covering all instances of undefined behavior in the C Standard.You are correct that the CERT secure coding rules are not intended to be used for safety-critical systems (we call this out in the Front Matter section in a few places, such as;System Qualities), except as a companion piece. We do not currently intend to support the safety-critical space with this coding standard, but there are other standards which give guidance in that space (such as MISRA C).
                                        Posted by aballman at Oct 25, 2016 10:41
                                     |
| yes... i read Front Matter section and i know that CERT C Coding Standard was not for safe system at the beginning. However since 2004, second edition, the keywords 'safe', and 'reliable' has inserted into title.when it compared to MISRA C, the gap is shocking. MISRA C covers 43 unspecified behaviors among 50 in C99 and 183 undefined behaviors among 191 in C99so now i'm little bit confused and i want to know how to read these tables.(in MISRA C,there are lots of blanks too but the blanks doesn't mean 'not cover'.Does blank mean 'not cover' in these tables of CERT C? Is there anybody who know how to interpret these tables?
                                        Posted by bycho at Oct 25, 2016 11:48
                                     |
| In the table above, a blank in the last column means that we have not mapped the information in the row on to a specific CERT C Coding Standard guideline. That doesn't mean we don't cover the UB, but it does mean that we've not formalized the mapping. For instance, I notice that UB 19 is covered by;EXP33-C. Do not read uninitialized memory, despite it being a blank in the table.
                                        Posted by aballman at Oct 26, 2016 08:32
                                     |
| oh is it true? then why has these tables not been update?hmm.. I really want to know full tables...Is there any way I can know that?
                                        Posted by bycho at Oct 26, 2016 09:21
                                     |
| I suspect the table got out of sync due to bit rot as we added information to the coding standard, and we do not currently have funding to work on the CERT C Coding Standard aside from basic maintenance. No one has taken a comprehensive pass over the rules recently to perform the updates to the table, but;we would welcome contributions from anyone willing to put in the effort. 
                                        Posted by aballman at Oct 26, 2016 09:36
                                     |
| The guideline for UB 137 is currently specified as CON37-C. Is this a typo?; Should instead UB 135 have the guideline CON37-C (and UB 137 guideline left blank)?
                                        Posted by morano at Jun 20, 2018 18:35
                                     |
| Yes, I fixed it, thanks.
                                        Posted by svoboda at Jun 21, 2018 19:25
                                     |
| UB 151: "output operation with an intervening call" should be changed to "output operation without an intervening call"
                                        Posted by rootkea at Apr 18, 2022 13:44
                                     |
| Avinash Sonawane;I have good news and bad news:First, this is directly quoting from ISO C Annex J, and our quotation is correct...that is Annex J says "with an intervening call", not "without".Second, my studying of ISO C has convinced me that you are correct, and it should be "without" not "with". I'll file a DefectReport with the ISO C committee.I'll let you decide which is the good news :)
                                        Posted by svoboda at Apr 18, 2022 16:40
                                     |
| I think it's a bad news that ISO C Annex J contradicts section 7.21.5.3 of the same standard.
> I'll file a DefectReport with the ISO C committee.

Cool! This is a good news.
                                        Posted by rootkea at Apr 18, 2022 21:14
                                     |
| #32 The identifier;func{} is explicitly declared (6.4.2.2).=>#32 The identifier _ _func_ _ is explicitly declared (6.4.2.2).
                                        Posted by danix800 at May 29, 2023 03:21
                                     |
| Fixed, thanks.
                                        Posted by svoboda at Jun 06, 2023 12:45
                                     |

