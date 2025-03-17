Declaring function parameters `const` indicates that the function promises not to change these values.
In C, function arguments are passed by value rather than by reference. Although a function may change the values passed in, these changed values are discarded once the function returns. For this reason, many programmers assume a function will not change its arguments and that declaring the function's parameters as `const` is unnecessary.
``` java
void foo(int x) {
  x = 3; /* Visible only in the function */
  /* ... */
}
```
Pointers behave in a similar fashion. A function may change a pointer to reference a different object, or `NULL`, yet that change is discarded once the function exits. Consequently, declaring a pointer as `const` is unnecessary.
``` java
void foo(int *x) {
  x = NULL; /* Visible only in the function */
  /* ... */
}
```
## Noncompliant Code Example
Unlike passed-by-value arguments and pointers, pointed-to values are a concern. A function may modify a value referenced by a pointer argument, leading to a [side effect](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) that persists even after the function exits. Modification of the pointed-to value is not diagnosed by the compiler, which assumes this behavior was intended.
``` c
void foo(int *x) {
  if (x != NULL) {
    *x = 3; /* Visible outside function */
  }
  /* ... */
}
```
If the function parameter is `const`-qualified, any attempt to modify the pointed-to value should cause the compiler to issue a diagnostic message.
``` c
void foo(const int *x) {
  if (x != NULL) {
    *x = 3; /* Compiler should generate diagnostic message */
  }
  /* ... */
}
```
As a result, the `const` violation must be resolved before the code can be compiled without a diagnostic message being issued.
## Compliant Solution
This compliant solution addresses the `const` violation by not modifying the constant argument:
``` c
void foo(const int * x) {
  if (x != NULL) {
    printf("Value is %d\n", *x);
  }
  /* ... */
}
```
## Noncompliant Code Example
This noncompliant code example defines a fictional version of the standard `strcat()` function called `strcat_nc()`. This function differs from `strcat()` in that the second argument is not `const`-qualified.
``` c
char *strcat_nc(char *s1, char *s2);
char *c_str1 = "c_str1";
const char *c_str2 = "c_str2";
char c_str3[9] = "c_str3";
const char c_str4[9] = "c_str4";
strcat_nc(c_str3, c_str2);  /* Compiler warns that c_str2 is const */
strcat_nc(c_str1, c_str3);  /* Attempts to overwrite string literal! */
strcat_nc(c_str4, c_str3);  /* Compiler warns that c_str4 is const */
```
The function behaves the same as `strcat()`, but the compiler generates warnings in incorrect locations and fails to generate them in correct locations.
In the first `strcat_nc()` call, the compiler generates a warning about attempting to cast away `const` on `c_str2` because `strcat_nc()` does not modify its second argument yet fails to declare it `const`.
In the second `strcat_nc()` call, the compiler compiles the code with no warnings, but the resulting code will attempt to modify the `"c_str1"` literal. This violates [STR05-C. Use pointers to const when referring to string literals](STR05-C_%20Use%20pointers%20to%20const%20when%20referring%20to%20string%20literals) and [STR30-C. Do not attempt to modify string literals](STR30-C_%20Do%20not%20attempt%20to%20modify%20string%20literals).
In the final `strcat_nc()` call, the compiler generates a warning about attempting to cast away `const` on `c_str4`, which is a valid warning.
## Compliant Solution
This compliant solution uses the prototype for the `strcat()` from C90. Although the `restrict` type qualifier did not exist in C90, `const` did. In general, function parameters should be declared in a manner consistent with the semantics of the function. In the case of `strcat()`, the initial argument can be changed by the function, but the second argument cannot.
``` c
char *strcat(char *s1, const char *s2); 
char *c_str1 = "c_str1";
const char *c_str2 = "c_str2";
char c_str3[9] = "c_str3";
const char c_str4[9] = "c_str4";
strcat(c_str3, c_str2); 
/* Args reversed to prevent overwriting string literal */ 
strcat(c_str3, c_str1);  
strcat(c_str4, c_str3);  /* Compiler warns that c_str4 is const */
```
The `const`-qualification of the second argument, `s2`, eliminates the spurious warning in the initial invocation but maintains the valid warning on the final invocation in which a `const`-qualified object is passed as the first argument (which can change). Finally, the middle `strcat()` invocation is now valid because `c_str3` is a valid destination string and may be safely modified.
## Risk Assessment
Failing to declare an unchanging value `const` prohibits the function from working with values already cast as `const`. This problem can be sidestepped by type casting away the `const`, but doing so violates [EXP05-C. Do not cast away a const qualification](EXP05-C_%20Do%20not%20cast%20away%20a%20const%20qualification).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL13-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | parameter-missing-const | Fully checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL13 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.CBCONST
 | Pointed-to Type Could Be const |
| Compass/ROSE |  |  | Can detect violations of this recommendation while checking for violations of recommendation DCL00-C. Const-qualify immutable objects |
| ECLAIR | 1.2 | CC2.DCL13 | Fully implemented |
| Helix QAC | 2024.4 | C0431, C3673, C3677 |  |
| Klocwork | 2024.4 | MISRA.PPARAM.NEEDS.CONST |  |
| LDRA tool suite | 9.7.1 | 120 D | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-DCL13-a | A pointer parameter in a function prototype should be declared as pointer to const if the pointer is not used to modify the addressed object |
| PC-lint Plus | 1.4 | 111, 818 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. DCL13-C | Checks for pointer to non-const qualified function parameter (rec. fully covered) |
| RuleChecker | 24.04 | parameter-missing-const | Fully checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL13-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID DCL13-CPP. Declare function parameters that are pointers to values not changed by the function as const |
| ISO/IEC TR 24772:2013 | Passing Parameters and Return Values [CSJ] |
| MISRA C:2012 | Rule 8.13 (advisory) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152098) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152278)
## Comments:

|  |
| ----|
| The 2nd noncompliant code example seems to be redundant since it is almost identical to the first one but changed the argument declaration in a compliant-way. The intent of the programmer may be clarified.
                                        Posted by masaki at Apr 19, 2009 19:30
                                     |
| I've reworded the example. It's confusing because the 2nd code example abides by the rule but fails to compile. In this case failure to compile is a Good Thing.
Assuming this is more clear, we'll need to make the same change to DCL13-CPP.
                                        Posted by svoboda at Apr 20, 2009 11:06
                                     |
| The problem with strcat_nc(str1, str3);  /* Attempts to overwrite string literal! */ example is that the const-ness of the string literal was lost earlier, when a string literal was assigned to a char*. The illustrated problem is unrelated to const-correct function parameters, as the same problem would occur even if the standard strcat were used. It seems this example and the assignment of string literal to char* should be elsewhere, as they more illustrate the basic meaning of const, rather than const as relating to function arguments.
It also seems that missing is an example that shows how the properly-declared standard strcat can be used to do things like strcat(str,".txt") without any compiler diagnostic, while strcat_nc(str,".txt") will give one, since the second parameter is declared as a non-const char*. It does pass a const char*, but not in a clear way like this.
                                        Posted by sgreen at Aug 20, 2009 17:23
                                     |
| I'll grant your point, that that specific line of code fails because the string literal is assigned to a non-const string pointer. It's still useful for completeness. 
We have a separate rule STR05-C. Use pointers to const when referring to string literals which covers the issue you describe.
                                        Posted by svoboda at Aug 21, 2009 08:58
                                     |

