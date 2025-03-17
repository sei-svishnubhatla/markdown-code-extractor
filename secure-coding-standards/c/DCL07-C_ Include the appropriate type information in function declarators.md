Function declarators must be declared with the appropriate type information, including a return type and parameter list. If type information is not properly specified in a function declarator, the compiler cannot properly check function type information. When using standard library calls, the easiest (and preferred) way to obtain function declarators with appropriate type information is to include the appropriate header file.
Attempting to compile a program with a function declarator that does not include the appropriate type information typically generates a warning but does not prevent program compilation. These warnings should be resolved. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)
## Noncompliant Code Example (Non-Prototype-Format Declarators)
This noncompliant code example uses the *identifier-list* form for parameter declarations:
``` c
int max(a, b)
int a, b;
{
  return a > b ? a : b;
}
```
Subclause 6.11.7 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] states that "the use of function definitions with separate parameter identifier and declaration lists (not prototype-format parameter type and identifier declarators) is an obsolescent feature."
## Compliant Solution (Non-Prototype-Format Declarators)
In this compliant solution, `int` is the type specifier, `max(int a, int b)` is the function declarator, and the block within the curly braces is the function body:
``` c
int max(int a, int b) {
  return a > b ? a : b;
}
```
## Noncompliant Code Example (Function Prototypes)
Declaring a function without any prototype forces the compiler to assume that the correct number and type of parameters have been supplied to a function. This practice can result in unintended and [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
In this noncompliant code example, the definition of `func()` in `file_a.c` expects three parameters but is supplied only two:
``` c
/* file_a.c source file */
int func(int one, int two, int three){
  printf("%d %d %d", one, two, three);
  return 1;
}
```
However, because there is no prototype for `func()` in `file_b.c`, the compiler assumes that the correct number of arguments has been supplied and uses the next value on the program stack as the missing third argument:
``` c
/* file_b.c source file */
func(1, 2);
```
C99 eliminated implicit function declarations from the C language. However, many compilers still allow the compilation of programs containing implicitly declared functions, although they may issue a warning message. These warnings should be resolved. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).)
## Compliant Solution (Function Prototypes)
This compliant solution correctly includes the function prototype for `func()` in the compilation unit in which it is invoked, and the function invocation has been corrected to pass the right number of arguments:
``` c
/* file_b.c source file */
int func(int, int, int);
func(1, 2, 3);
```
## Noncompliant Code Example (Function Pointers)
If a function pointer refers to an incompatible function, invoking that function via the pointer may corrupt the process stack. As a result, unexpected data may be accessed by the called function.
In this noncompliant code example, the function pointer `fn_ptr` refers to the function `add()`, which accepts three integer arguments. However, `fn_ptr` is specified to accept two integer arguments. Setting `fn_ptr` to refer to `add()` results in unexpected program behavior. This example also violates [EXP37-C. Call functions with the correct number and type of arguments](EXP37-C_%20Call%20functions%20with%20the%20correct%20number%20and%20type%20of%20arguments):
``` c
int add(int x, int y, int z) {
  return x + y + z;
}
int main(int argc, char *argv[]) {
  int (*fn_ptr) (int, int);
  int res;
  fn_ptr = add;
  res = fn_ptr(2, 3);  /* Incorrect */
  /* ... */
  return 0;
}
```
## Compliant Solution (Function Pointers)
To correct this example, the declaration of `fn_ptr` is changed to accept three arguments:
``` c
int add(int x, int y, int z) {
  return x + y + z;
}
int main(int argc, char *argv[]) {
  int (*fn_ptr) (int, int, int) ;
  int res;
  fn_ptr = add;
  res = fn_ptr(2, 3, 4);
  /* ... */
  return 0;
}
```
## Risk Assessment
Failing to include type information for function declarators can result in [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) or unintended program behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL07-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | function-prototypeimplicit-function-declaration | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL07 |  |
| CodeSonar | 8.3p0 | LANG.FUNCS.PROTLANG.STRUCT.DECL.IMPT
 | Incomplete function prototypeImplicit Type |
| ECLAIR | 1.2 | CC2.DCL07 | Fully implemented |
| GCC | 4.3.5 |  | Can detect violation of this recommendation when the -Wstrict-prototypes flag is used |
| Helix QAC | 2024.4 | C1304, C2050, C3331, C3335, C3408, C3450 |  |
| Klocwork | 2024.4 | MISRA.FUNC.PROT_FORM.KR.2012MISRA.FUNC.NOPROT.DEF
MISRA.CAST.FUNC_PTR.2012 |  |
| LDRA tool suite | 9.7.1 | 21 S135 S
170 S | Fully implemented |
| PC-lint Plus | 1.4 | 718, 746, 936, 9074 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL07-C | Checks for:Cast between function pointers with different typesFunction declared implicitly.Rec. fully covered. |
| RuleChecker | 24.04 | function-prototypeimplicit-function-declaration | Partially checked |
| SonarQube C/C++ Plugin | 3.11 | S819, S930 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL07-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Type System [IHN]Subprogram Signature Mismatch [OTR] |
| ISO/IEC TS 17961 | Using a tainted value as an argument to an unprototyped function pointer [taintnoproto] |
| MISRA C:2012 | Rule 8.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.11.7, "Function Definitions" |
| [Spinellis 2006] | Section 2.6.1, "Incorrect Routine or Arguments" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152130) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152145)
## Comments:

|  |
| ----|
| Including the keyword extern in the function definition is decidedly non-idiomatic and is not applied consistently even in this recommendation.; I recommend not recommending that - even by example.
 The basic description of the problem, while accurate standardese, is also guaranteed to put the reader to sleep.
Function declarators must be declared with the appropriate type information, including a return type, parameter list, and function prototype (if the declarator is part of a function definition). If type information is not properly specified in a function declarator, the compiler cannot properly check function type information. When using standard library calls, the easiest (and preferred) way to obtain function declarators with appropriate type information is to include the appropriate header file.
This is at the cross-roads between coding standard and security, but the wording I use runs along the lines of:
    A source file (as distinct from a header) may not declare functions or variables with 'extern'.  Those declarations should be in a header, and the relevant header should be included in the source file.
    A header (as distinct from a source file) may not declare a variable without the keyword extern, and therefore may never include an initializer either.  A header should declare functions explicitly with the keyword extern even though it is technically optional.
    All function declarations must include the return type (C99 compliance - no implicit int) and use the prototype notation and not K&R notation.
    All function definitions must include the return type (C99 compliance) and use the prototype notation.
    By virtue of these prescriptions, all functions taking variable arguments must use <stdarg.h> and not <varargs.h>.
 Feel free to butcher my wording - but I think the concept is expressed more clearly and directly thus.
                                        Posted by jonathan.leffler@gmail.com at Mar 15, 2008 15:12
                                     |
| The second and third non-compliant examples here will both fail to compile.  In the second example, the definition of func tells the compiler the type of func, allowing it to detect that the call to func does not have enough arguments.  In the third example, the compiler will complain about the mismatched function pointer types in the assignment.
(If either of these behaviors do not represent standard C behavior, that seems like a serious bug in the standard.)
                                        Posted by josh@freedesktop.org at Mar 16, 2008 06:11
                                     |
| For the first example, you might consider noting that some compilers have options to warn or error on K&R-style function definitions, and you might consider recommending that programs use those compiler options when building.
                                        Posted by josh@freedesktop.org at Mar 16, 2008 06:18
                                     |
| Broke both non-compliant examples into two files, as that better illustrates the behavior of implicitly-declared functions.
                                        Posted by svoboda at Apr 15, 2008 11:47
                                     |
| This recommendation refers to DCL14-C, which should be moved to void section.
                                        Posted by masaki at Apr 21, 2009 05:16
                                     |
| I guess dangling pointers aren't just a problem in C  Deleted offending paragraph.
                                        Posted by svoboda at Apr 21, 2009 11:05
                                     |

