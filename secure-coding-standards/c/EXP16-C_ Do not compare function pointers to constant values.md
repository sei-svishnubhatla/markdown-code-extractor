Comparing a function pointer to a value that is not a null function pointer of the same type will be diagnosed because it typically indicates programmer error and can result in [unexpected behavior](http://BB.%20Definitions#unexpected%20behavior). Implicit comparisons will be diagnosed, as well.
## Noncompliant Code Example
In this noncompliant code example, the addresses of the POSIX functions `getuid` and `geteuid` are compared for equality to 0. Because no function address shall be null, the first subexpression will always evaluate to false (0), and the second subexpression always to true (nonzero). Consequently, the entire expression will always evaluate to true, leading to a potential security vulnerability.
``` c
/* First the options that are allowed only for root */
if (getuid == 0 || geteuid != 0) {
  /* ... */
}
```
## Noncompliant Code Example
In this noncompliant code example, the function pointers `getuid` and `geteuid` are compared to 0. This example is from an actual [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) ([VU#837857](http://www.kb.cert.org/vuls/id/837857)) discovered in some versions of the X Window System server. The vulnerability exists because the programmer neglected to provide the open and close parentheses following the `geteuid()` function identifier. As a result, the `geteuid` token returns the address of the function, which is never equal to 0. Consequently, the `or` condition of this `if` statement is always true, and access is provided to the protected block for all users. Many compilers issue a warning noting such pointless expressions. Therefore, this coding error is normally detected by adherence to [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).
``` c
/* First the options that are allowed only for root */
if (getuid() == 0 || geteuid != 0) {
  /* ... */
}
```
## Compliant Solution
The solution is to provide the open and close parentheses following the `geteuid` token so that the function is properly invoked:
``` c
/* First the options that are allowed only for root */
if (getuid() == 0 || geteuid() != 0) {
  /* ... */
}
```
## Compliant Solution
A function pointer can be compared to a null function pointer of the same type:
``` c
/* First the options that are allowed only for root */ 
if (getuid == (uid_t(*)(void))0 || geteuid != (uid_t(*)(void))0) { 
  /* ... */ 
} 
```
This code should not be diagnosed by an analyzer.
## Noncompliant Code Example
In this noncompliant code example, the function pointer `do_xyz` is implicitly compared unequal to 0:
``` c
int do_xyz(void); 
int f(void) {
/* ... */
  if (do_xyz) { 
    return -1; /* Indicate failure */ 
  }
/* ... */
  return 0;
} 
```
## Compliant Solution
In this compliant solution, the function `do_xyz()` is invoked and the return value is compared to 0:
``` c
int do_xyz(void); 
int f(void) {
/* ... */ 
  if (do_xyz()) { 
    return -1; /* Indicate failure */
  }
/* ... */
  return 0;  
} 
```
## Risk Assessment
Errors of omission can result in unintended program flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP16-C | Low | Likely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | function-name-constant-comparison | Partially checked |
| Coverity | 2017.07 | BAD_COMPARE | Can detect the specific instance where the address of a function is compared against 0, such as in the case of geteuid versus getuid() in the implementation-specific details |
| GCC | 4.3.5 |  | Can detect violations of this recommendation when the -Wall flag is used |
| Helix QAC | 2024.4 | C0428, C3004, C3344 |  |
| Klocwork | 2024.4 | CWARN.NULLCHECK.FUNCNAMECWARN.FUNCADDR |  |
| LDRA tool suite | 9.7.1 | 99 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP16-a | Function address should not be compared to zero |
| PC-lint Plus | 1.4 | 2440, 2441 | Partially supported: reports address of function, array, or variable directly or indirectly compared to null |
| PVS-Studio | 7.35 | V516, V1058 |  |
| RuleChecker | 24.04 | function-name-constant-comparison | Partially checked |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP16-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID EXP16-CPP. Avoid conversions using void pointers |
| ISO/IEC TR 24772:2013 | Likely incorrect expressions [KOA] |
| ISO/IEC TS 17961 | Comparing function addresses to zero [funcaddr] |
| MITRE CWE | CWE-480, Use of incorrect operatorCWE-482, Comparing instead of assigning |

## Bibliography

|  |  |
| ----|----|
| [Hatton 1995] | Section 2.7.2, "Errors of Omission and Addition" |

------------------------------------------------------------------------
[](../c/EXP15-C_%20Do%20not%20place%20a%20semicolon%20on%20the%20same%20line%20as%20an%20if,%20for,%20or%20while%20statement) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](../c/EXP19-C_%20Use%20braces%20for%20the%20body%20of%20an%20if,%20for,%20or%20while%20statement)
## Comments:

|  |
| ----|
| Since, as the description mentions, comparing the address of a function against a literal other than NULL is typically due to an accidental programmer mistake (forgetting the parentheses after the name of the function) rather than deliberately, this guideline effectively advises against making accidental mistakes. I see little value in such advice – no one makes mistakes on purpose. They just happen. That's where compiler warnings and static analysis tools come in handy. This rule might be appropriate for a standard aimed at tool vendors but seems less so for one aimed at human users.
                                        Posted by martinsebor at Jan 21, 2010 21:50
                                     |
| This makes sense as we bifurcate this standard into this one, which is targeted towards developers, and the analyzable guidelines targeted towards analyzers.
Alot of these guidelines on avoid accidents of omission and addition probably fall into this category.
These may be worthwhile for this standard if they can provide advice on how to encode certain constructs to eliminate unwanted diagnostics, for example, how to compare a function pointer to a null function pointer of the same type.
                                        Posted by rcs at Jan 22, 2010 05:12
                                     |
| Another one that doesn't map well to CWE.; The examples here don't map to cwe 482 or 480.
                                        Posted by azukich at Feb 18, 2010 10:00
                                     |

