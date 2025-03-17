The C language provides several different kinds of constants: *integer* constants, such as `10` and `0x1C`; *floating* constants, such as `1.0` and `6.022e+23`; and *character* constants, such as `'a'` and `'\x10'`. C also provides string literals, such as `"hello, world"` and `"\n"`. These constants can all be referred to as *literals*.
When used in program logic, literals can reduce the readability of source code. As a result, literals, in general, and integer constants, in particular, are frequently called *magic numbers* because their purpose is often obscured. Magic numbers can be constant values that represent either an arbitrary value (such as a determined appropriate buffer size) or a malleable concept (such as the age at which a person is considered an adult, which can change between geopolitical boundaries). Rather than embed literals in program logic, use appropriately named symbolic constants to clarify the intent of the code. In addition, if a specific value needs to be changed, reassigning a symbolic constant once is more efficient and less error prone than replacing every instance of the value \[[Saks 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Saks02)\].
The C programming language has several mechanisms for creating named, symbolic constants: `const`-qualified objects, enumeration constants, and [object-like macro](BB.-Definitions_87152273.html#BB.Definitions-object-likemacro) definitions. Each of these mechanisms has associated advantages and disadvantages.
## `const`-Qualified Objects
Objects that are `const`-qualified have scope and can be type-checked by the compiler. Because they are named objects (unlike macro definitions), some debugging tools can show the name of the object. The object also consumes memory.
A `const`-qualified object allows you to specify the exact type of the constant. For example,
``` java
const unsigned int buffer_size = 256;
```
defines `buffer_size` as a constant whose type is `unsigned int`.
Unfortunately, `const`-qualified objects cannot be used where compile-time integer constants are required, namely to define the
-   Size of a bit-field member of a structure.
-   Size of an array (except in the case of variable length arrays).
-   Value of an enumeration constant.
-   Value of a `case` constant.
If any of these are required, then an integer constant (which would be an [rvalue](BB.-Definitions_87152273.html#BB.Definitions-rvalue)) must be used.
`const`-qualified objects allow the programmer to take the address of the object:
``` java
const int max = 15;
int a[max]; /* Invalid declaration outside of a function */
const int *p;
/* A const-qualified object can have its address taken */
p = &max;
```
`const`-qualified objects are likely to incur some runtime overhead \[[Saks 2001b](AA.-Bibliography_87152170.html#AA.Bibliography-Saks02)\]. Most C compilers, for example, allocate memory for `const`-qualified objects. `const`-qualified objects declared inside a function body can have automatic storage duration. If so, the compiler will allocate storage for the object, and it will be on the stack. As a result, this storage will need to be allocated and initialized each time the containing function is invoked.
## Enumeration Constants
Enumeration constants can be used to represent an integer constant expression that has a value representable as an `int`. Unlike `const`-qualified objects, enumeration constants do not consume memory. No storage is allocated for the value, so it is not possible to take the address of an enumeration constant.
``` java
enum { max = 15 };
int a[max]; /* OK outside function */
const int *p;
p = &max; /* Error: "&" on enum constant */
```
Enumeration constants do not allow the type of the value to be specified. An enumeration constant whose value can be represented as an `int` is always an `int`.
## Object-like Macros
A preprocessing directive of the form
`#` `define` *identifier replacement-list*
defines an [object-like macro](BB.-Definitions_87152273.html#BB.Definitions-object-likemacro) that causes each subsequent instance of the macro name to be replaced by the replacement list of preprocessing tokens that constitute the remainder of the directive.
C programmers frequently define symbolic constants as object-like macros. For example, the code
``` java
#define buffer_size 256
```
defines `buffer_size` as a macro whose value is 256. The preprocessor substitutes macros before the compiler does any other symbol processing. Later compilation phases never see macro symbols, such as `buffer_size`; they see only the source text after macro substitution. As a result, many compilers do not preserve macro names among the symbols they pass on to their debuggers.
Macro names do not observe the scope rules that apply to other names. Therefore, macros could substitute in unanticipated places with unexpected results.
Object-like macros do not consume memory; consequently, it is not possible to create a pointer to one. Macros do not provide for type checking because they are textually replaced by the preprocessor.
Macros can be passed as compile-time arguments.
## Summary
The following table summarizes some of the differences between `const`-qualified objects, enumeration constants, and [object-like macro](BB.-Definitions_87152273.html#BB.Definitions-object-likemacro) definitions.

| Method | Evaluated At | Consumes Memory | Viewable by Debuggers | Type Checking | Compile-Time Constant Expression |
| ----|----|----|----|----|----|
| Enumerations | Compile time | No | Yes | Yes | Yes |
| const-qualified | Runtime | Yes | Yes | Yes | No |
| Macros | Preprocessor | No | No | No | Yes |

## Noncompliant Code Example
The meaning of the integer literal 18 is not clear in this example:
``` c
/* ... */
if (age >= 18) {
   /* Take action */
}
else {
  /* Take a different action */
}
/* ... */
```
## Compliant Solution
This compliant solution replaces the integer literal 18 with the symbolic constant `ADULT_AGE` to clarify the meaning of the code:
``` c
enum { ADULT_AGE=18 };
/* ... */
if (age >= ADULT_AGE) {
   /* Take action */
}
else {
  /* Take a different action */
}
/* ... */
```
## Noncompliant Code Example
Integer literals are frequently used when referring to array dimensions, as shown in this noncompliant code example:
``` c
char buffer[256];
/* ... */
fgets(buffer, 256, stdin);
```
This use of integer literals can easily result in buffer overflows if, for example, the buffer size is reduced but the integer literal used in the call to `fgets()` is not.
## Compliant Solution (`enum`)
In this compliant solution, the integer literal is replaced with an enumeration constant. (See [DCL00-C. Const-qualify immutable objects](DCL00-C_%20Const-qualify%20immutable%20objects).)
``` c
enum { BUFFER_SIZE=256 };
char buffer[BUFFER_SIZE];
/* ... */
fgets(buffer, BUFFER_SIZE, stdin);
```
Enumeration constants can safely be used anywhere a constant expression is required.
## Compliant Solution (`sizeof`)
Frequently, it is possible to obtain the desired readability by using a symbolic expression composed of existing symbols rather than by defining a new symbol. For example, a `sizeof` expression can work just as well as an enumeration constant. (See [EXP09-C. Use sizeof to determine the size of a type or variable](EXP09-C_%20Use%20sizeof%20to%20determine%20the%20size%20of%20a%20type%20or%20variable).)
``` c
char buffer[256];
/* ... */
fgets(buffer, sizeof(buffer), stdin);
```
Using the `sizeof` expression in this example reduces the total number of names declared in the program, which is generally a good idea \[[Saks 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Saks02)\]. The `sizeof` operator is almost always evaluated at compile time (except in the case of variable-length arrays).
When working with `sizeof()`, keep in mind [ARR01-C. Do not apply the sizeof operator to a pointer when taking the size of an array](ARR01-C_%20Do%20not%20apply%20the%20sizeof%20operator%20to%20a%20pointer%20when%20taking%20the%20size%20of%20an%20array).
## Noncompliant Code Example
In this noncompliant code example, the string literal `"localhost"` and integer constant `1234` are embedded directly in program logic and are consequently difficult to change:
``` c
LDAP *ld = ldap_init("localhost", 1234);
if (ld == NULL) {
  perror("ldap_init");
  return(1);
}
```
## Compliant Solution
In this compliant solution, the host name and port number are both defined as [object-like macros](BB.-Definitions_87152273.html#BB.Definitions-object-likemacro), so they can be passed as compile-time arguments:
``` c
#ifndef PORTNUMBER     /* Might be passed on compile line */
#  define PORTNUMBER 1234
#endif
#ifndef HOSTNAME       /* Might be passed on compile line */
#  define HOSTNAME "localhost"
#endif
/* ... */
LDAP *ld = ldap_init(HOSTNAME, PORTNUMBER);
if (ld == NULL) {
  perror("ldap_init");
  return(1);
}
```
## Exceptions
**DCL06-C-EX1:** Although replacing numeric constants with a symbolic constant is often a good practice, it can be taken too far. Remember that the goal is to improve readability. Exceptions can be made for constants that are themselves the abstraction you want to represent, as in this compliant solution.
``` c
x = (-b + sqrt(b*b - 4*a*c)) / (2*a);
```
Replacing numeric constants with symbolic constants in this example does nothing to improve the readability of the code and can actually make the code more difficult to read.
``` java
enum { TWO = 2 };     /* A scalar */
enum { FOUR = 4 };    /* A scalar */
enum { SQUARE = 2 };  /* An exponent */
x = (-b + sqrt(pow(b, SQUARE) - FOUR*a*c))/ (TWO * a);
```
When implementing recommendations, it is always necessary to use sound judgment.
Note that this example does not check for invalid operations (taking the `sqrt()` of a negative number). See [FLP32-C. Prevent or detect domain and range errors in math functions](FLP32-C_%20Prevent%20or%20detect%20domain%20and%20range%20errors%20in%20math%20functions) for more information on detecting domain and range errors in math functions.
## Risk Assessment
Using numeric literals makes code more difficult to read and understand. Buffer overruns are frequently a consequence of a magic number being changed in one place (such as in an array declaration) but not elsewhere (such as in a loop through an array).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL06-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL06 |  |
| CodeSonar | 8.3p0 | LANG.STRUCT.SW.SWNEE | Switch with non-enum expression |
| Compass/ROSE |  |  | Could detect violations of this recommendation merely by searching for the use of "magic numbers" and magic strings in the code itself. That is, any number (except a few canonical numbers: −1, 0, 1, 2) that appears in the code anywhere;besides where assigned to a variable is a magic number and should instead be assigned to a const integer, enum, or macro. Likewise, any string literal (except "" and individual characters) that appears in the code anywhere besides where assigned to a char* or char[] is a magic string |
| ECLAIR | 1.2 | CC2.DCL06 | Fully implemented |
| Helix QAC | 2024.4 | C3120, C3121, C3122, C3123, C3131, C3132 |  |
| LDRA tool suite | 9.7.1 | 201 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL06-a | Use meaningful symbolic constants to represent literal values |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL06-C | Checks for:Hard-coded buffer sizeHard-coded loop boundaryRec. fully covered. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL06-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL06-CPP. Use meaningful symbolic constants to represent literal values in program logic |
| MITRE CWE | CWE-547, Use of hard-coded, security-relevant constants |

## Bibliography

|  |  |
| ----|----|
| [Henricson 1992] | Chapter 10, "Constants" |
| [Saks 2001a] |  |
| [Saks 2001b] |  |
| [Saks 2002] |  |
| [Summit 2005] | Question 10.5b |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152187) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152364)
## Comments:

|  |
| ----|
| How much readability is necessary for a symbolic constant name to be meaningful?
                                        Posted by xuinkrbin. at Feb 27, 2009 13:47
                                     |
| I think this would be a quality of implementation issue.  My concern would be how to eliminate false positives by not flagging the exceptions from DCL06-EX1?
                                        Posted by rcs_mgr at Feb 27, 2009 15:47
                                     |
| I don't think you can eliminate false positives from DCL06-EX1. It's easy for a static analyzer to spot a magic number or string literal in code. It's impossible for an analyzer to ascertain if that number is better represeted as a constant (variable/macro/enum).  I do think the amount of false-positive magic numbers is far outweighed by the amount of 'true' magic numbers in the code, so it is still worthwhile flagging violators of DCL06-EX1.
The problem of notifying static analyzers that a 'magic' number actually improves readability (DCL06-EX1) is IMHO best left to some external channel for static analyzers. Something like pragmas or attributes.
                                        Posted by svoboda at Mar 02, 2009 16:51
                                     |
| I have an observation/opinion on the claim that a preprocessor macro has no type checking. Take as an example the following:#define; CONST_VALUE  ((size_t)10)

this <u>has a type</u> that a compiler can check, moreover has a type that an `enum` <u>can't have</u> (a column with "Can specify type" would be helpful in the comparison chart). ~~You can't in fact type the following without a (good) warning from the compiler:  
~~
    enum { CONST_VALUE = 10 };
    size_t  count = 0;
    while (count < CONST_VALUE) {  // type mismatch in comparison
      ...
      count++;
    }
![](images/icons/contenttypes/comment_16.png) Posted by lmatteini at Jun 22, 2023 06:26
\| \|
I believe the text you are complaining about is this:
> Macros do not provide for type checking because they are textually replaced by the preprocessor.

Your points are correct, that the expansion of a macro produces C expressions which themselves can be type-checked. However, the statement meant that there is no type inherently associated with a macro, it is only associated with the macro's expansion. (In some pathalogical cases, the type of the macro can vary between different expansions.) ;A good compiler could infer that a type mismatch (or other error) occurs due to a macro expansion, but this is not required.
BTW the while statement in your code produces no warning on my mac, using clang 14.0.3.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 22, 2023 08:41
\| \|
David, I stand corrected. Tried Clang 16.0 with the same result you mention. Interestingly enough, the compiler resolves that the constant value is simply positive, and does the same with a `const int CONST_VALUE = 10;`;  
My memory went indeed to what happens if I **remove** the `const` specifier - there the compiler warns about the sign.  
The example above then is just meaningless.
What makes me uncertain is then the fact I'm potentially comparing an unsigned integer to a possibly *unpredictable* type - as the enum can resolve to a char, an int, or (finally) an unsigned int, as the standard tells it's implementation-defined.
![](images/icons/contenttypes/comment_16.png) Posted by lmatteini at Jun 22, 2023 10:52
\| \|
Right. This is the type-safety problem associated with macros that this recommendation is trying to allude to. An expression of an expanded macro can depend on other macros (perhaps in the macro's definition) or previous conditional compilation directives (ifdefs). The language has rules for converting types, when doing comparison or equality operators, for instance, so it usually tries to do the Right Thing.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 22, 2023 11:24
\|
