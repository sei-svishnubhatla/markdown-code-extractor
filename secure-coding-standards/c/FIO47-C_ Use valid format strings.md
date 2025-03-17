The formatted output functions (`fprintf()` and related functions) convert, format, and print their arguments under control of a *format* string. The C Standard, 7.23.6.1, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\], specifies
> The format shall be a multibyte character sequence, beginning and ending in its initial shift state. The format is composed of zero or more directives: ordinary multibyte characters (not **%**), which are copied unchanged to the output stream; and conversion specifications, each of which results in fetching zero or more subsequent arguments, converting them, if applicable, according to the corresponding conversion specifier, and then writing the result to the output stream.

Each *conversion specification* is introduced by the `%` character followed (in order) by
-   Zero or more *flags* (in any order), which modify the meaning of the conversion specification
-   An optional minimum field *width*
-   An optional *precision* that gives the minimum number of digits, the maximum number of digits, or the maximum number of bytes, etc. depending on the conversion specifier
-   An optional *length modifier* that specifies the size of the argument
-   A *conversion specifier character* that indicates the type of conversion to be applied
Common mistakes in creating format strings include
-   Providing an incorrect number of arguments for the format string
-   Using invalid conversion specifiers
-   Using a flag character that is incompatible with the conversion specifier
-   Using a length modifier that is incompatible with the conversion specifier
-   Mismatching the argument type and conversion specifier
-   Using an argument of type other than `int` for *width* or *precision*
The following table summarizes the compliance of various conversion specifications. The first column contains one or more conversion specifier characters. The next four columns consider the combination of the specifier characters with the various flags (the apostrophe \[`'`\], `-`, `+`, the space character, `#`, and `0`). The next eight columns consider the combination of the specifier characters with the various length modifiers (`h`, `hh`, `l`, `ll`, `j`, `z`, `t`, and `L`).
Valid combinations are marked with a type name; arguments matched with the conversion specification are interpreted as that type. For example, an argument matched with the specifier `%hd` is interpreted as a `short`, so `short` appears in the cell where `d` and `h` intersect. The last column denotes the expected types of arguments matched with the original specifier characters.
Valid and meaningful combinations are marked by the ![](images/icons/emoticons/check.svg) symbol (save for the length modifier columns, as described previously). Valid combinations that have no effect are labeled *N/E*. Using a combination marked by the ![](images/icons/emoticons/error.svg) symbol, using a specification not represented in the table, or using an argument of an unexpected type is [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). (See undefined behaviors [158](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_158), [160](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_1560), [162](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_162), [163](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_163), [166](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_166), and [167](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_167).) 

| Conversion
Specifier 
Character | ' XSI | - 
+ 
SPACE | 
 # | 
0 | 
h | 
hh | 
l | 
ll | 
j | 
z | 
t | 
L | Argument 
Type |
| ----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| d, i |  |  |  |  | short | signed char | long | long long | intmax_t | size_t | ptrdiff_t |  | Signed integer |
| o |  |  |  |  | unsigned short | unsigned char | unsigned long | unsigned long long | uintmax_t | size_t | ptrdiff_t |  | Unsigned integer |
| u |  |  |  |  | unsigned short | unsigned; char | unsigned long | unsigned long long | uintmax_t | size_t | ptrdiff_t |  | Unsigned integer |
| x, X |  |  |  |  | unsigned short | unsigned char | unsigned long | unsigned long long | uintmax_t | size_t | ptrdiff_t |  | Unsigned integer |
| f, F |  |  |  |  |  |  | N/E | N/E |  |  |  | long double | double or long double |
| e, E |  |  |  |  |  |  | N/E | N/E |  |  |  | long double | double or long double |
| g, G |  |  |  |  |  |  | N/E | N/E |  |  |  | long double | double or long double |
| a, A |  |  |  |  |  |  | N/E | N/E |  |  |  | long double | double or long double |
| c |  |  |  |  |  |  | wint_t |  |  |  |  |  | int or wint_t |
| s |  |  |  |  |  |  | NTWS |  |  |  |  |  | NTBS or NTWS |
| p |  |  |  |  |  |  |  |  |  |  |  |  | void* |
| n |  |  |  |  | short* | char* | long* | long long* | intmax_t* | size_t* | ptrdiff_t* |  | Pointer to integer |
| C XSI |  |  |  |  |  |  |  |  |  |  |  |  | wint_t |
| S XSI |  |  |  |  |  |  |  |  |  |  |  |  | NTWS |
| % |  |  |  |  |  |  |  |  |  |  |  |  | None |

     SPACE: The space (`" "`) character  
*     N/E*: No effect  
     NTBS: `char*` argument pointing to a null-terminated character string  
     NTWS: `wchar_t*` argument pointing to a null-terminated wide character string  
     XSI: [ISO/IEC 9945-2003](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9945-2003) XSI extension
The formatted input functions (`fscanf()` and related functions) use similarly specified format strings and impose similar restrictions on their format strings and arguments.
Do not supply an unknown or invalid conversion specification or an invalid combination of flag character, precision, length modifier, or conversion specifier to a formatted IO function. Likewise, do not provide a number or type of argument that does not match the argument type of the conversion specifier used in the format string.
Format strings are usually string literals specified at the call site, but they need not be. However, they should not contain [tainted values](BB.-Definitions_87152273.html#BB.Definitions-taintedvalue). (See [FIO30-C. Exclude user input from format strings](FIO30-C_%20Exclude%20user%20input%20from%20format%20strings) for more information.)
## Noncompliant Code Example
Mismatches between arguments and conversion specifications may result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). Compilers may diagnose type mismatches in formatted output function invocations. In this noncompliant code example, the `error_type` argument to `printf()` is incorrectly matched with the `s` specifier rather than with the `d` specifier. Likewise, the `error_msg` argument is incorrectly matched with the `d` specifier instead of the `s` specifier. These usages result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). One possible result of this invocation is that `printf()` will interpret the `error_type` argument as a pointer and try to read a string from the address that `error_type` contains, possibly resulting in an access violation.
``` c
#include <stdio.h>
void func(void) {
  const char *error_msg = "Resource not available to user.";
  int error_type = 3;
  /* ... */
  printf("Error (type %s): %d\n", error_type, error_msg);
  /* ... */
}
```
## Compliant Solution
This compliant solution ensures that the arguments to the `printf()` function match their respective conversion specifications:
``` c
#include <stdio.h>
void func(void) {
  const char *error_msg = "Resource not available to user.";
  int error_type = 3;
  /* ... */
  printf("Error (type %d): %s\n", error_type, error_msg);
  /* ... */
}
```
## Risk Assessment
Incorrectly specified format strings can result in memory corruption or [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO47-C | High | Unlikely | Medium | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-FIO47 | Fully implemented |
| CodeSonar | 8.3p0 | IO.INJ.FMTMISC.FMT
MISC.FMTTYPE
 | Format string injectionFormat string
Format string type error |
| Coverity | 2017.07 | PW | Reports when the number of arguments differs from the number of required arguments according to the format string |
| Cppcheck | ; 2.15 | invalidscanfwrongPrintfScanfArgNum
invalidLengthModifierError
invalidScanfFormatWidth
wrongPrintfScanfParameterPositionError |  |
| Cppcheck Premium | 24.11.0 | invalidscanfwrongPrintfScanfArgNum
invalidLengthModifierError
invalidScanfFormatWidth
wrongPrintfScanfParameterPositionError |  |
| GCC | 4.3.5 |  | Can detect violations of this recommendation when the -Wformat flag is used |
| Helix QAC | 2024.4 | C0161, C0162, C0163, C0164, C0165, C0166, C0167, C0168, C0169, C0170, C0171, C0172, C0173, C0174, C0175, C0176, C0177, C0178, C0179, C0180, C0184, C0185, C0190, C0191, C0192, C0193, C0194, C0195, C0196, C0197, C0198, C0199, C0200, C0201, C0202, C0204, C0206, C0209C++3150, C++3151, C++3152, C++3153, C++3154, C++3155, C++3156, C++3157, C++3158, C++3159 |  |
| Klocwork | 2024.4 | SV.FMT_STR.PRINT_FORMAT_MISMATCH.BADSV.FMT_STR.PRINT_FORMAT_MISMATCH.UNDESIRED
SV.FMT_STR.PRINT_IMPROP_LENGTH
SV.FMT_STR.PRINT_PARAMS_WRONGNUM.FEW
SV.FMT_STR.PRINT_PARAMS_WRONGNUM.MANY
SV.FMT_STR.SCAN_FORMAT_MISMATCH.BAD
SV.FMT_STR.SCAN_FORMAT_MISMATCH.UNDESIRED
SV.FMT_STR.SCAN_IMPROP_LENGTH
SV.FMT_STR.SCAN_PARAMS_WRONGNUM.FEW
SV.FMT_STR.SCAN_PARAMS_WRONGNUM.MANY
SV.FMT_STR.UNKWN_FORMAT
 |  |
| LDRA tool suite | 9.7.1 | 486 S589 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-FIO47-aCERT_C-FIO47-b
CERT_C-FIO47-c
CERT_C-FIO47-d
CERT_C-FIO47-e
CERT_C-FIO47-f | There should be no mismatch between the '%s' and '%c' format specifiers in the format string and their corresponding arguments in the invocation of a string formatting functionThere should be no mismatch between the '%f' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
There should be no mismatch between the '%i' and '%d' format specifiers in the string and their corresponding arguments in the invocation of a string formatting function
There should be no mismatch between the '%u' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
There should be no mismatch between the '%p' format specifier in the format string and its corresponding argument in the invocation of a string formatting function
The number of format specifiers in the format string and the number of corresponding arguments in the invocation of a string formatting function should be equal |
| PC-lint Plus | 1.4 | 492, 493, 494, 499, 557,558, 559, 566, 705, 706,
719, 816, 855, 2401, 2402,
2403, 2404, 2405, 2406, 2407 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule FIO47-C | Check for format string specifiers and arguments mismatch (rule fully covered) |
| PVS-Studio | 7.35 | V510, V576 |  |
| TrustInSoft Analyzer | 1.38 | match format and arguments | Exhaustively verified (see;the compliant and the non-compliant example). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO47-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | FIO00-CPP. Take care when creating format strings | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Using invalid format strings [invfmtstr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-686, Function Call with Incorrect Argument Type | 2017-06-29: CERT: Partial overlap |
| CWE 2.11 | CWE-685 | 2017-06-29: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-686 and FIO47-C
Intersection( EXP37-C, FIO47-C) =
-   Invalid argument types passed to format I/O function
EXP37-C – FIO47-C =
-   Invalid argument types passed to non-format I/O function
FIO47-C – EXP37-C =
-   Invalid format string, but correctly matches arguments in number and type
Intersection( CWE-686, FIO47-C) =
-   Use of format strings that do not match the type of arguments
CWE-686 – FIO47-C =
-   Incorrect argument type in functions outside of the printf() family.
FIO47-C – CWE-686 =
-   Invalid format strings that still match their arguments in type
### CWE-685 and FIO47-C
Intersection( CWE-685, FIO47-C) =
-   Use of format strings that do not match the number of arguments
CWE-685 – FIO47-C =
-   Incorrect argument number in functions outside of the printf() family.
FIO47-C – CWE-685 =
-   Invalid format strings that still match their arguments in number
### CWE-134 and FIO47-C
Intersection( FIO30-C, FIO47-C) =
-   Use of untrusted and ill-specified format string
FIO30-C – FIO47-C =
-   Use of untrusted, but well-defined format string
FIO47-C – FIO30-C =
-   Use of Ill-defined, but trusted format string
FIO47-C = Union(CWE-134, list) where list =
-   Using a trusted but invalid format string
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause 7.23.6.1, "The fprintf Function" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151937) [](../c/Rule%2009_%20Input%20Output%20_FIO_) [](../c/Rule%2010_%20Environment%20_ENV_)
## Comments:

|  |
| ----|
| My recommendation: Convert all printf statements according to the following pattern:
printf("Error (type %s): %d\n", CHECK_s(error_type), CHECK_d(error_msg));

where CHECK_s is a macro that returns error_type if error_type is a valid argument for the %s formatting code, otherwise cause the compiler to emit a warning message.; Verified and tested under Microsoft Visual C 15.
The visual correspondence between the formatting code and the verification macro is so evident that it makes easy to spot the discrepancy between the formal parameter and the verifying macro used by superficial inspection.  The only requirement is that the formatting string must be inline, otherwise this evidence is lost and it must be reinvented on the place where the format string is defined.
![](images/icons/contenttypes/comment_16.png) Posted by yecril at Oct 06, 2007 10:34
\| \|
Question: how do you internationalize the error message template?
Observation: in the circles in which I've moved, it would be more plausible that the error type would be an integer and the message a string than vice versa.; I'm not clear if that's what you're trying to show.  Isn't it better to include the (relatively) short number at the beginning of the message and the variable length string at the end rather than vice versa?
Separate question - not related to comment above:
-   Should this recommendation be recast in the NCCE/CS format? 
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Mar 17, 2008 23:00
\| \|
Since the majority of misuses of the format string result in undefined behavior (both of the non-compliant examples shown here do) and since compilers have been diagnosing such misues for some time now, it seems to me that this recommendation is ready to be made a rule (although perhaps under a different name).
> [!warning]
>
> Unless someone objects in the next day or so I will go ahead and make this guideline a **rule** (choosing a more suitable name for it in the process).

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 03, 2010 15:49
\| \|
I agree this looks more like a rule rather than a rec. Violations are (usually) vuls, this rec is easily enforceable, and there are no exceptions. Does anyone remember why this was made a rec in the first place?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 05, 2010 13:23
\| \|
Well, the title sounds like a recommendation. "Take care" is statically unenforceable. 8^)
Perhaps the title should be:
FIO00-C. Avoid common mistakes in creating format strings
Then the guideline does a good job of defining in detail what these common mistakes are.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 06, 2010 03:53
\| \|
Also, if we move this, we should try to play nice and update the tables for the various static analysis tools.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Feb 06, 2010 04:00
\| \|
I'll take care of it.
Btw., with labels, changing a guideline from [recommendation](https://wiki.sei.cmu.edu//confluence/label/seccode/recommendation) to [rule](https://wiki.sei.cmu.edu//confluence/label/seccode/rule) is now a trivial matter of deleting one label and the other.
What are your thoughts on my proposal in my comment [Re: Rules Versus Recommendations](https://www.securecoding.cert.org/confluence/display/seccode/Rules+Versus+Recommendations?focusedCommentId=41386402#comment-41386402)?
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 06, 2010 15:16
\| \|
the meaning of *precision* depends on the conversion specifier.
so, how about revising this line
-   An optional;*precision* that gives the minimum number of digits to appear for certain conversion specifiers
to the following?
-   An optional *precision* that gives the minimum number of digits, the maximum number of digits, or the maximum number of bytes, etc. depending on the conversion specifiers
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Sep 06, 2021 16:08
\| \|
Agreed, I adopted your suggestion.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 07, 2021 09:12
\| \|
The table shows that the flags +-SPACE are compatible with the % specifier. However, the standard says that in the case of % the full conversion specification must be %% so %-% should be undefined behavior...  
Is that a typo in the table or am I missing something?
![](images/icons/contenttypes/comment_16.png) Posted by mbaluda at Aug 10, 2022 10:36
\| \|
No, having studied the standard, I think you are correct. So I changed the check to an X. I also marked X for the flags to the `%n`; conversion specifier, which also forbids flags.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 10, 2022 11:27
\|
