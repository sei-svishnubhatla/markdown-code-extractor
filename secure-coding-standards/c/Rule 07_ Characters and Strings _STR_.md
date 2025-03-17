-   Page:
    [STR30-C. Do not attempt to modify string literals](/confluence/display/c/STR30-C.+Do+not+attempt+to+modify+string+literals)
-   Page:
    [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](/confluence/display/c/STR31-C.+Guarantee+that+storage+for+strings+has+sufficient+space+for+character+data+and+the+null+terminator)
-   Page:
    [STR32-C. Do not pass a non-null-terminated character sequence to a library function that expects a string](/confluence/display/c/STR32-C.+Do+not+pass+a+non-null-terminated+character+sequence+to+a+library+function+that+expects+a+string)
-   Page:
    [STR34-C. Cast characters to unsigned char before converting to larger integer sizes](/confluence/display/c/STR34-C.+Cast+characters+to+unsigned+char+before+converting+to+larger+integer+sizes)
-   Page:
    [STR37-C. Arguments to character-handling functions must be representable as an unsigned char](/confluence/display/c/STR37-C.+Arguments+to+character-handling+functions+must+be+representable+as+an+unsigned+char)
-   Page:
    [STR38-C. Do not confuse narrow and wide character strings and functions](/confluence/display/c/STR38-C.+Do+not+confuse+narrow+and+wide+character+strings+and+functions)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [str](https://confluence/label/seccode/str) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR30-C | Low | Likely | Low | P9 | L2 |
| STR31-C | High | Likely | Medium | P18 | L1 |
| STR32-C | High | Probable | Medium | P12 | L1 |
| STR34-C | Medium | Probable | Medium | P8 | L2 |
| STR37-C | Low | Unlikely | Low | P3 | L3 |
| STR38-C | High | Likely | Low | P27 | L1 |

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
[](Rule%2006_%20Arrays%20_ARR_) [](2%20Rules) [](STR30-C_%20Do%20not%20attempt%20to%20modify%20string%20literals)
## Comments:

|  |
| ----|
| This document uses the terminology of the C standard, which is that "null" is an English adjective and "NULL" is a C noun.; The term "NUL" is from ASCII and does not appear in the C standard.  For that, this document says "null character."
                                        Posted by dmk at Mar 14, 2008 00:16
                                     |

