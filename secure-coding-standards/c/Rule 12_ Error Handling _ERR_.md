-   Page:
    [ERR30-C. Take care when reading errno](/confluence/display/c/ERR30-C.+Take+care+when+reading+errno)
-   Page:
    [ERR32-C. Do not rely on indeterminate values of errno](/confluence/display/c/ERR32-C.+Do+not+rely+on+indeterminate+values+of+errno)
-   Page:
    [ERR33-C. Detect and handle standard library errors](/confluence/display/c/ERR33-C.+Detect+and+handle+standard+library+errors)
-   Page:
    [ERR34-C. Detect errors when converting a string to a number](/confluence/display/c/ERR34-C.+Detect+errors+when+converting+a+string+to+a+number)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [err](https://confluence/label/seccode/err) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR30-C | Medium | Probable | Medium | P8 | L2 |
| ERR32-C | Low | Unlikely | Low | P3 | L3 |
| ERR33-C | High | Likely | Medium | P18 | L1 |
| ERR34-C | Medium | Unlikely | Medium | P4 | L3 |

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
[](../c/Rule%2011_%20Signals%20_SIG_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152351)
