Traditionally, C arrays are declared with an index that is either a fixed constant or empty. An array with a fixed constant index indicates to the compiler how much space to reserve for the array. An array declaration with an empty index is an incomplete type and indicates that the variable references a pointer to an array of indeterminate size.
The term *conformant array parameter* comes from Pascal; it refers to a function argument that is an array whose size is specified in the function declaration. Since C99, C has supported conformant array parameters by permitting array parameter declarations to use extended syntax. Subclause 6.7.6.2, paragraph 1, of C11 \[ISO/IEC 9899:2011\] summarizes the array index syntax extensions:
> The \[ and \] may delimit an expression or \*. If they delimit an expression (which specifies the size of an array), the  expression shall have an integer type. If the expression is a constant expression, it shall  have a value greater than zero.

Consequently, an array declaration that serves as a function argument may have an index that is a variable or an expression. The array argument is demoted to a pointer and is consequently not a variable length array (VLA). Conformant array parameters can be used by developers to indicate the expected bounds of the array. This information may be used by compilers, or it may be ignored. However, such declarations are useful to developers because they serve to document relationships between array sizes and pointers. This information can also be used by [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis) tools to diagnose potential defects.
``` java
int f(size_t n, int a[n]);  /* Documents a relationship between n and a */
```
## Standard Examples
Subclause 6.7.6.3 of the C Standard \[ISO/IEC 9899:2011\] has several examples of conformant array parameters. Example 4 (paragraph 20) illustrates a variably modified parameter:
``` java
void addscalar(int n, int m, double a[n][n*m+300], double x);
int main(void)
{
  double b[4][308];
  addscalar(4, 2, b, 2.17);
  return 0;
}
void addscalar(int n, int m, double a[n][n*m+300], double x)
{
  for (int i = 0; i < n; i++)
  for (int j = 0, k = n*m+300; j < k; j++)
    /* a is a pointer to a VLA with n*m+300 elements */
    a[i][j] += x;
}
```
Example 4 illustrates a set of compatible function prototype declarators
``` java
double maximum(int n, int m, double a[n][m]);
double maximum(int n, int m, double a[*][*]);
double maximum(int n, int m, double a[ ][*]);
double maximum(int n, int m, double a[ ][m]);
```
## Noncompliant Code Example
This code example provides a function that wraps a call to the standard `memset()` function and has a similar set of arguments. However, although this function clearly intends that `p` point to an array of at least `n` chars, this invariant is not explicitly documented.
``` c
void my_memset(char* p, size_t n, char v)
{
  memset( p, v, n);
}
```
## Noncompliant Code Example
This noncompliant code example attempts to document the relationship between the pointer and the size using conformant array parameters. However, the variable `n` is used as the index of the array declaration before `n` is itself declared. Consequently, this code example is not standards-compliant and will usually fail to compile.
``` c
void my_memset(char p[n], size_t n, char v)
{
  memset( p, v, n);
}
```
## Compliant Solution (GCC)
This compliant solution uses a GNU extension to forward declare the `size_t` variable `n` before using it in the subsequent array declaration. Consequently, this code allows the existing parameter order to be retained and successfully documents the relationship between the array parameter and the size parameter.
``` c
void my_memset(size_t n; char p[n], size_t n, char v)
{
  memset(p, v, n);
}
```
## Compliant Solution (API change)
This compliant solution changes the function's API by moving the `size_t` variable `n` to before the subsequent array declaration. Consequently, this code complies with the C99 standard and successfully documents the relationship between the array parameter and the size parameter, but requires all callers to be updated.
``` c
void my_memset(size_t n, char p[n], char v)
{
  memset(p, v, n);
}
```
## Exceptions
**API05-C-EX0:** The extended array syntax is not supported by C++, or platforms that do not support C99, such as MSVC. Consequently, C programs that must support such platforms, including Windows, need not use conformant array parameters. One option for portable code that must support such platforms is to use macros:
``` c
#include <stddef.h>
#if !defined(__STDC_VERSION__) || __STDC_VERSION__ < 199901L || defined(__STDC_NO_VLA__)
#define N(x)
#else
#define N(x)  (x)
#endif
int f(size_t n, int a[N(n)]);
```
## Risk Assessment
Failing to specify conformant array dimensions increases the likelihood that another developer will invoke the function with out-of-range integers, which could cause an out-of-bounds memory read or write.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API05-C | High | Probable | Medium | P12 | L1 |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.7.6.2, "Array Declarators"Subclause 6.7.6.3, "Function Declarators (Including Prototypes)" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152244) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152337)
## Comments:

|  |
| ----|
| The term "conformant array parameters" does not appear in the C standard.; It may be useful to offer some short explanation of where the term originated, and probably to offer a definition. 
                                        Posted by rcs_mgr at Aug 25, 2013 09:05
                                     |
| Google does not provide a definition, but does cite origins from Pascal, so I've added some text to mention this.
                                        Posted by svoboda at Sep 05, 2013 16:04
                                     |
| I now question if this is a good recommendation to have.The problem is that if an array size is a function argument that is not known at compile time, then providing an array with the size as dimension converts the argument from a pointer to a variable length array (VLA). VLAs have many problems (see ARR32-C. Ensure size arguments for variable length arrays are in a valid range for some). Fortunately most of these problems don't occur when a VLA is merely used as a function argument (as opposed to being declared on the stack). But some problems remain:VLA's have inconsistent compiler support.Conformant array parameters require that the size parameter be declared before the array parameter. (You can sidestep this problem by using K&R-style declarations, or by using non-portable extensions such as GCC's.) But many functions, like memcpy(), have established placing the array before its size.GCC's -Wvla warning will fire if you have a VLA as a function parameter, just as much as if you declare a VLA on the stack.VLA's are not supported by ISO C++. So a C function with conformant array parameters cannot be invoked by C++ code.VLA's are not supported by MSVC (which only supports C90.)We could fix this recommendation by restricting it to arrays whose size is known at compile time...but that will be tricky to get right...consider this story: https://lwn.net/Articles/749064/.;Or we could kill this recommendation completely.Comments?
                                        Posted by svoboda at Dec 07, 2020 10:29
                                     |
| IMO, it's pointless to put an array size somewhere that it's just going to decay to a pointer, since doing so is basically just a glorified comment, unless you do something like int arr[static 10].
                                        Posted by jcsible at Dec 07, 2020 10:41
                                     |
| From the introduction:This information may be used by compilers, or it may be ignored. However, such declarations are useful to developers because they serve to document relationships between array sizes and pointers. This information can also be used by static analysis tools to diagnose potential defects.Don't discount the value of conveying extra info to developers, or SA tools.
                                        Posted by svoboda at Dec 07, 2020 10:45
                                     |
| This information may be used by compilers, or it may be ignored.Is that true? I thought compilers had to ignore it unless you used static like I did above. And as for conveying extra info to developers, why not just use an actual comment for that, so it doesn't break compatibility with MSVC and C++?
                                        Posted by jcsible at Dec 07, 2020 10:46
                                     |
| IIUC a conforming compiler must still demote an array parameter to a pointer, whether or not it has a dimension. So the compiler is free to ignore the dimension. GCC's -Wvla is a good example of not ignoring such a dimension.And while specifying the bounds in a comment is a useful way of informing developers, specifying the bounds as the array dimension is a more formal and precise convention (at least for C99-conforming compilers)
                                        Posted by svoboda at Dec 07, 2020 10:55
                                     |
| Here's what the standard says:A declaration of a parameter as “array of type” shall be adjusted to “qualified pointer to type”, where the type qualifiers (if any) are those specified within the [ and ] of the array type derivation. If the keyword static also appears within the [ and ] of the array type derivation, then for each call to the function, the value of the corresponding actual argument shall provide access to the first element of an array with at least as many elements as specified by the size expression.Note "shall be adjusted". I think GCC's -Wvla is a good example of a compiler not strictly complying with the standard.
                                        Posted by jcsible at Dec 07, 2020 11:39
                                     |
| One nit: emitting a warning does not constitute noncompliance with the standard. The -Wvla makes GCC produce a warning, but it also still produces working code, so it does strictly comply with ISO C.Of course, ISO C says nothing about how -Wvla should behave. But I would argue that (regardless of how it behaves now), -Wvla would be far more useful if it only fired on VLA declarations on the stack or data segment, and not on VLA declarations in a function argument list.
                                        Posted by svoboda at Dec 07, 2020 11:47
                                     |
| Another option is to pass a pointer to a VLA. Here no array-to-pointer adjustment happens:void;my_memset(size_t n, char(*p)[n], char v)
{
  memset(*p, v, n);
}Also realize that a pointer to a VLA is a bounded pointer type and GCC/clang compilers support checking the bound at runtime with -fsanitize=undefined. VLAs should be actively promoted as a tool for safer programming.  Under some conditions, VLAs on the stack might be also a better and safer alternative to fixed size arrays on the stack.
                                        Posted by uecker at Dec 09, 2020 13:22
                                     |

