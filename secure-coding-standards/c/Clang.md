> [!warning]  
>
> This page was automatically generated and should not be edited.
> [!warning]  
>
> The information on this page was provided by outside contributors and has not been verified by SEI CERT.
> [!info]  
>
> The table below can be re-ordered, by clicking column headers.

**Tool Version:** 3.9

| 
    Checker
    | 
    Guideline
    |
| ----|----|
| -Wimplicit-int | 
     DCL31-C. Declare identifiers before using them
     |
| -Wincompatible-pointer-types | 
     STR38-C. Do not confuse narrow and wide character strings and functions
     |
| -Wincompatible-pointer-types-discards-qualifiers | 
     EXP32-C. Do not access a volatile object through a nonvolatile reference
     |
| -Wint-conversion | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| -Wint-to-pointer-cast | 
     INT36-C. Converting a pointer to integer or integer to pointer
     |
| -Wparentheses | 
     EXP45-C. Do not perform assignments in selection statements
     |
| -Wsometimes-uninitialized | 
     DCL41-C. Do not declare variables inside a switch statement before the first case label
     |
| -Wunevaluated-expression | 
     EXP44-C. Do not rely on side effects in operands to sizeof, _Alignof, or _Generic
     |
| -Wunsequenced | 
     EXP30-C. Do not depend on the order of evaluation for side effects
     |
| -Wvarargs | 
     EXP47-C. Do not call va_arg with an argument of the incorrect type
     |
| -Ww | 
     STR05-C. Use pointers to const when referring to string literals
     |
| cert-env33-c | 
     ENV33-C. Do not call system()
     |
| cert-err34-c | 
     ERR34-C. Detect errors when converting a string to a number
     |
| cert-flp30-c | 
     FLP30-C. Do not use floating-point variables as loop counters
     |
| cert-msc30-c | 
     MSC30-C. Do not use the rand() function for generating pseudorandom numbers
     |
| clang-analyzer-unix.Malloc | 
     MEM34-C. Only free memory allocated dynamically
     |
| misc-non-copyable-objects | 
     FIO38-C. Do not copy a FILE object
     |
| misc-static-assert | 
     DCL03-C. Use a static assertion to test the value of a constant expression
     |
| rite-strings | 
     STR05-C. Use pointers to const when referring to string literals
     |

## Comments:

|  |
| ----|
| When listing Clang as an analyzer that can catch a rule violation, should we distinguish between things that it catches as regular compile warnings, vs. things that it only catches if you use clang --analyze?
                                        Posted by jcsible at May 23, 2022 14:49
                                     |

