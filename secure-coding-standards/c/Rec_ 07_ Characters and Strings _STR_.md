-   Page:
    [STR00-C. Represent characters using an appropriate type](/confluence/display/c/STR00-C.+Represent+characters+using+an+appropriate+type)
-   Page:
    [STR01-C. Adopt and implement a consistent plan for managing strings](/confluence/display/c/STR01-C.+Adopt+and+implement+a+consistent+plan+for+managing+strings)
-   Page:
    [STR02-C. Sanitize data passed to complex subsystems](/confluence/display/c/STR02-C.+Sanitize+data+passed+to+complex+subsystems)
-   Page:
    [STR03-C. Do not inadvertently truncate a string](/confluence/display/c/STR03-C.+Do+not+inadvertently+truncate+a+string)
-   Page:
    [STR04-C. Use plain char for characters in the basic character set](/confluence/display/c/STR04-C.+Use+plain+char+for+characters+in+the+basic+character+set)
-   Page:
    [STR05-C. Use pointers to const when referring to string literals](/confluence/display/c/STR05-C.+Use+pointers+to+const+when+referring+to+string+literals)
-   Page:
    [STR06-C. Do not assume that strtok() leaves the parse string unchanged](/confluence/display/c/STR06-C.+Do+not+assume+that+strtok%28%29+leaves+the+parse+string+unchanged)
-   Page:
    [STR07-C. Use the bounds-checking interfaces for string manipulation](/confluence/display/c/STR07-C.+Use+the+bounds-checking+interfaces+for+string+manipulation)
-   Page:
    [STR08-C. Use managed strings for development of new string manipulation code](/confluence/display/c/STR08-C.+Use+managed+strings+for+development+of+new+string+manipulation+code)
-   Page:
    [STR09-C. Don't assume numeric values for expressions with type plain character](/confluence/display/c/STR09-C.+Don%27t+assume+numeric+values+for+expressions+with+type+plain+character)
-   Page:
    [STR10-C. Do not concatenate different type of string literals](/confluence/display/c/STR10-C.+Do+not+concatenate+different+type+of+string+literals)
-   Page:
    [STR11-C. Do not specify the bound of a character array initialized with a string literal](/confluence/display/c/STR11-C.+Do+not+specify+the+bound+of+a+character+array+initialized+with+a+string+literal)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [str](https://confluence/label/seccode/str) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR00-C | Medium | Probable | Low | P12 | L1 |
| STR01-C | Low | Unlikely | High | P1 | L3 |
| STR02-C | High | Likely | Medium | P18 | L1 |
| STR03-C | Medium | Probable | Medium | P8 | L2 |
| STR04-C | Low | Unlikely | Low | P3 | L3 |
| STR05-C | Low | Unlikely | Low | P3 | L3 |
| STR06-C | Medium | Likely | Medium | P12 | L1 |
| STR07-C | High | Probable | Medium | P12 | L1 |
| STR08-C | High | Probable | High | P6 | L2 |
| STR09-C | Low | Unlikely | Low | P3 | L3 |
| STR10-C | Low | Probable | Medium | P4 | L3 |
| STR11-C | Low | Probable | Low | P6 | L2 |

## Related Rules and Recommendations

|  |
| ----|
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO20-C. Avoid unintentional truncation when using fgets() or fgetws() |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO30-C. Exclude user input from format strings |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO47-C. Use valid format strings |
| FIO47-C. Use valid format strings |
| FIO47-C. Use valid format strings |
| INT07-C. Use only explicitly signed or unsigned char type for numeric values |
| INT07-C. Use only explicitly signed or unsigned char type for numeric values |
| INT07-C. Use only explicitly signed or unsigned char type for numeric values |
| POS30-C. Use the readlink() function properly |
| POS30-C. Use the readlink() function properly |
| POS30-C. Use the readlink() function properly |
| STR37-C. Arguments to character-handling functions must be representable as an unsigned char |
| STR37-C. Arguments to character-handling functions must be representable as an unsigned char |
| STR37-C. Arguments to character-handling functions must be representable as an unsigned char |

------------------------------------------------------------------------
[](../c/Rec_%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152151)
