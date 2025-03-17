-   Page:
    [ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy](/confluence/display/c/ERR00-C.+Adopt+and+implement+a+consistent+and+comprehensive+error-handling+policy)
-   Page:
    [ERR01-C. Use ferror() rather than errno to check for FILE stream errors](/confluence/display/c/ERR01-C.+Use+ferror%28%29+rather+than+errno+to+check+for+FILE+stream+errors)
-   Page:
    [ERR02-C. Avoid in-band error indicators](/confluence/display/c/ERR02-C.+Avoid+in-band+error+indicators)
-   Page:
    [ERR03-C. Use runtime-constraint handlers when calling the bounds-checking interfaces](/confluence/display/c/ERR03-C.+Use+runtime-constraint+handlers+when+calling+the+bounds-checking+interfaces)
-   Page:
    [ERR04-C. Choose an appropriate termination strategy](/confluence/display/c/ERR04-C.+Choose+an+appropriate+termination+strategy)
-   Page:
    [ERR05-C. Application-independent code should provide error detection without dictating error handling](/confluence/display/c/ERR05-C.+Application-independent+code+should+provide+error+detection+without+dictating+error+handling)
-   Page:
    [ERR06-C. Understand the termination behavior of assert() and abort()](../c/ERR06-C_%20Understand%20the%20termination%20behavior%20of%20assert__%20and%20abort__)
-   Page:
    [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](/confluence/display/c/ERR07-C.+Prefer+functions+that+support+error+checking+over+equivalent+functions+that+don%27t)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [err](https://confluence/label/seccode/err) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR00-C | Medium | Probable | High | P4 | L3 |
| ERR01-C | Low | Probable | Low | P6 | L2 |
| ERR02-C | Low | Unlikely | High | P1 | L3 |
| ERR03-C | Low | Unlikely | Medium | P2 | L3 |
| ERR04-C | Medium | Probable | High | P4 | L3 |
| ERR05-C | Medium | Probable | High | P4 | L3 |
| ERR06-C | Medium | Unlikely | Medium | P4 | L3 |
| ERR07-C | Medium | Probable | Medium | P8 | L2 |

## Related Rules and Recommendations

|  |
| ----|
| DCL09-C. Declare functions that return errno with a return type of errno_t |
| DCL09-C. Declare functions that return errno with a return type of errno_t |
| DCL09-C. Declare functions that return errno with a return type of errno_t |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FIO40-C. Reset strings on fgets()  or fgetws() failure |
| FLP03-C. Detect and handle floating-point errors |
| FLP03-C. Detect and handle floating-point errors |
| FLP03-C. Detect and handle floating-point errors |
| FLP32-C. Prevent or detect domain and range errors in math functions |
| FLP32-C. Prevent or detect domain and range errors in math functions |
| FLP32-C. Prevent or detect domain and range errors in math functions |
| MSC11-C. Incorporate diagnostic tests using assertions |
| MSC11-C. Incorporate diagnostic tests using assertions |
| MSC11-C. Incorporate diagnostic tests using assertions |
| VOID Always check for errors when using threads |
| VOID Always check for errors when using threads |
| VOID Always check for errors when using threads |
| VOID FIO04-C. Detect and handle input and output errors |
| VOID FIO04-C. Detect and handle input and output errors |
| VOID FIO04-C. Detect and handle input and output errors |
| void FIO33-C. Detect and handle input output errors resulting in undefined behavior |
| void FIO33-C. Detect and handle input output errors resulting in undefined behavior |
| void FIO33-C. Detect and handle input output errors resulting in undefined behavior |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void MEM32-C. Detect and handle memory allocation errors |
| void MEM32-C. Detect and handle memory allocation errors |
| void MEM32-C. Detect and handle memory allocation errors |

------------------------------------------------------------------------
[](../c/Rec_%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152349)
## Comments:

|  |
| ----|
| The link for ERR08-C is not available in this overview sheet.
                                        Posted by volker.erben at Nov 29, 2018 08:44
                                     |
| Volker,That's because it is currently a stub.; When it's complete, it will be added through the correct tag.
                                        Posted by rschiela at Mar 20, 2019 10:29
                                     |

