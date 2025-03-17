According to the C Standard, 3.8 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\], a constraint is a "restriction, either syntactic or semantic, by which the exposition of language elements is to be interpreted."  Despite the similarity of the terms, a runtime constraint is not a kind of constraint.
Violating any *shall* statement within a constraint clause in the C Standard requires an [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) to issue a diagnostic message, the C Standard, 5.1.1.3 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\] states
> A conforming implementation shall produce at least one diagnostic message (identified in an implementation-defined manner) if a preprocessing translation unit or translation unit contains a violation of any syntax rule or constraint, even if the behavior is also explicitly specified as undefined or implementation-defined. Diagnostic messages need not be produced in other circumstances.

The C Standard further explains in a footnote
> The intent is that an implementation should identify the nature of, and where possible localize, each violation. Of course, an implementation is free to produce any number of diagnostics as long as a valid program is still correctly translated. It may also successfully translate an invalid program.

Any constraint violation is a violation of this rule because it can result in an invalid program.
## Noncompliant Code Example (Inline, Internal Linkage)
The C Standard, 6.7.4, paragraph 3 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\], states
> An inline definition of a function with external linkage shall not contain a definition of a modifiable object with static or thread storage duration, and shall not contain a reference to an identifier with internal linkage.

The motivation behind this constraint lies in the semantics of inline definitions. Paragraph 7 of subclause 6.7.4 reads, in part:
> An inline definition provides an alternative to an external definition, which a translator may use to implement any call to the function in the same translation unit. It is unspecified whether a call to the function uses the inline definition or the external definition.

That is, if a function has an external and inline definition, implementations are free to choose which definition to invoke (two distinct invocations of the function may call different definitions, one the external definition, the other the inline definition). Therefore, issues can arise when these definitions reference internally linked objects or mutable objects with static or thread storage duration.
This noncompliant code example refers to a static variable with file scope and internal linkage from within an external inline function:
``` c
static int I = 12;
extern inline void func(int a) {
  int b = a * I;
  /* ... */
}
```
## Compliant Solution (Inline, Internal Linkage)
This compliant solution omits the `static` qualifier;  consequently,  the variable `I` has external linkage by default:
``` c
int I = 12;
extern inline void func(int a) {
  int b = a * I;
  /* ... */
}
```
## Noncompliant Code Example (inline, Modifiable Static)
This noncompliant code example defines a modifiable `static` variable within an `extern inline` function.
``` c
extern inline void func(void) {
  static int I = 12;
  /* Perform calculations which may modify I */
}
```
## Compliant Solution (Inline, Modifiable Static)
This compliant solution removes the `static` keyword from the local variable definition. If the modifications to `I` must be retained between invocations of `func()`, it must be declared at file scope so that it will be defined with external linkage.
``` c
extern inline void func(void) {
  int I = 12;
  /* Perform calculations which may modify I */
}
```
## Noncompliant Code Example (Inline, Modifiable `static`)
This noncompliant code example includes two translation units: `file1.c` and `file2.c`. The first file, `file1.c`, defines a pseudorandom number generation function:
``` c
/* file1.c */
/* Externally linked definition of the function get_random() */
extern unsigned int get_random(void) {
  /* Initialize the seeds */
  static unsigned int m_z = 0xdeadbeef;
  static unsigned int m_w = 0xbaddecaf;
  /* Compute the next pseudorandom value and update the seeds */
  m_z = 36969 * (m_z & 65535) + (m_z >> 16);
  m_w = 18000 * (m_w & 65535) + (m_w >> 16);
  return (m_z << 16) + m_w;
}
```
The left-shift operation in the last line may wrap, but this is permitted by exception INT30-C-EX3 to rule [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap).
The second file, `file2.c`, defines an `inline` version of this function that references mutable `static` objects—namely, objects that maintain the state of the pseudorandom number generator. Separate invocations of the `get_random()` function can call different definitions, each operating on separate static objects, resulting in a faulty pseudorandom number generator.
``` c
/* file2.c */
/* Inline definition of get_random function */
inline unsigned int get_random(void) {
  /* 
   * Initialize the seeds 
   * Constraint violation: static duration storage referenced
   * in non-static inline definition
   */
  static unsigned int m_z = 0xdeadbeef;
  static unsigned int m_w = 0xbaddecaf;
  /* Compute the next pseudorandom value and update the seeds */
  m_z = 36969 * (m_z & 65535) + (m_z >> 16);
  m_w = 18000 * (m_w & 65535) + (m_w >> 16);
  return (m_z << 16) + m_w;
}
int main(void) {
  unsigned int rand_no;
  for (int ii = 0; ii < 100; ii++) {
    /* 
     * Get a pseudorandom number. Implementation defined whether the
     * inline definition in this file or the external definition  
     * in file2.c is called. 
     */
    rand_no = get_random();
    /* Use rand_no... */
  }
  /* ... */
  /* 
   * Get another pseudorandom number. Behavior is
   * implementation defined.
   */
  rand_no = get_random();
  /* Use rand_no... */
  return 0;
}
```
## Compliant Solution (Inline, Modifiable `static`)
This compliant solution adds the `static` modifier to the `inline` function definition in `file2.c`, giving it internal linkage. All references to `get_random()` in `file.2.c` will now reference the internally linked definition. The first file, which was not changed, is not shown here.
``` c
/* file2.c */
/* Static inline definition of get_random function */
static inline unsigned int get_random(void) {
  /* 
   * Initialize the seeds. 
   * No more constraint violation; the inline function is now 
   * internally linked. 
   */
  static unsigned int m_z = 0xdeadbeef;
  static unsigned int m_w = 0xbaddecaf;
  /* Compute the next pseudorandom value and update the seeds  */
  m_z = 36969 * (m_z & 65535) + (m_z >> 16);
  m_w = 18000 * (m_w & 65535) + (m_w >> 16);
  return (m_z << 16) + m_w;
}
int main(void) {
  /* Generate pseudorandom numbers using get_random()... */
  return 0;
}
```
## Risk Assessment
Constraint violations are a broad category of error that can result in unexpected control flow and corrupted data.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC40-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| ;Astrée | ;24.04 | alignas-extendedassignment-to-non-modifiable-lvalue
cast-pointer-void-arithmetic-implicit
element-type-incomplete
function-pointer-integer-cast-implicit
function-return-type
inappropriate-pointer-cast-implicit
incompatible-function-pointer-conversion
incompatible-object-pointer-conversion
initializer-excess
invalid-array-size
non-constant-static-assert
parameter-match-type
pointer-integral-cast-implicit
pointer-qualifier-cast-const-implicit
pointer-qualifier-cast-volatile-implicit
redeclaration
return-empty
return-non-empty
static-assert
type-compatibility
type-compatibility-link
type-specifier
undeclared-parameter
unnamed-parameter | Partially checked |
| Cppcheck Premium | 24.11.0 | premium-cert-msc40-c |  |
| Helix QAC | 2024.4 | C0232, C0233, C0244, C0268, C0321, C0322, C0338, C0422, C0423, C0426, C0427, C0429, C0430, C0431, C0432, C0435, C0436, C0437, C0446, C0447, C0448, C0449, C0451, C0452, C0453, C0454, C0456, C0457, C0458, C0460, C0461, C0462, C0463, C0466, C0467, C0468, C0469, C0476, C0477, C0478, C0481, C0482, C0483, C0484, C0485, C0486, C0487, C0493, C0494, C0495, C0496, C0497, C0513, C0514, C0515, C0536, C0537, C0540, C0541, C0542, C0546, C0547, C0550, C0554, C0555, C0556, C0557, C0558, C0559, C0560, C0561, C0562, C0563, C0564, C0565, C0580, C0588, C0589, C0590, C0591, C0605, C0616, C0619, C0620, C0621, C0622, C0627, C0628, C0629, C0631, C0638, C0640, C0641, C0642, C0643, C0644, C0645, C0646, C0649, C0650, C0651, C0653, C0655, C0656, C0657, C0659, C0664, C0665, C0669, C0671, C0673, C0674, C0675, C0677, C0682, C0683, C0684, C0685, C0690, C0698, C0699, C0708, C0709, C0736, C0737, C0738, C0746, C0747, C0755, C0756, C0757, C0758, C0766, C0767, C0768, C0774, C0775, C0801, C0802, C0803, C0804, C0811, C0821, C0834, C0835, C0844, C0845, C0851, C0852, C0866, C0873, C0877, C0940, C0941, C0943, C0944, C1023, C1024, C1025, C1033, C1047, C1048, C1050, C1061, C1062, C3236, C3237, C3238, C3244C++4122 |  |
| Klocwork | 2024.4 | MISRA.FUNC.STATIC.REDECL |  |
| ;LDRA tool suite | ;9.7.1 | ;21 S, 145 S, 323 S, 345 S, 387 S, 404 S, 481 S, 580 S, 612 S, 615 S, 646 S |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC40-a | An inline definition of a function with external linkage shall not contain definitions and uses of static objects |
| ;Polyspace Bug Finder | ;R2024a | CERT C: Rule MSC40-C | Checks for inline constraint not respected (rule partially covered) |
| RuleChecker | 24.04 | alignas-extendedassignment-to-non-modifiable-lvalue
cast-pointer-void-arithmetic-implicit
element-type-incomplete
function-pointer-integer-cast-implicit
function-return-type
inappropriate-pointer-cast-implicit
incompatible-function-pointer-conversion
incompatible-object-pointer-conversion
initializer-excess
invalid-array-size
non-constant-static-assert
parameter-match-type
pointer-integral-cast-implicit
pointer-qualifier-cast-const-implicit
pointer-qualifier-cast-volatile-implicit
redeclaration
return-empty
return-non-empty
static-assert
type-compatibility
type-compatibility-link
type-specifier
undeclared-parameter
unnamed-parameter | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC40-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | 4, "Conformance"5.1.1.3, "Diagnostics" 
6.7.4, "Function Specifiers" |

------------------------------------------------------------------------
[](../c/MSC39-C_%20Do%20not%20call%20va_arg__%20on%20a%20va_list%20that%20has%20an%20indeterminate%20value) [](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=108396967)
