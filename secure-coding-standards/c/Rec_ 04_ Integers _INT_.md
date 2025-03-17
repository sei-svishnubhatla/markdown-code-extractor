-   Page:
    [INT00-C. Understand the data model used by your implementation(s)](../c/INT00-C_%20Understand%20the%20data%20model%20used%20by%20your%20implementation_s_)
-   Page:
    [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](/confluence/display/c/INT01-C.+Use+rsize_t+or+size_t+for+all+integer+values+representing+the+size+of+an+object)
-   Page:
    [INT02-C. Understand integer conversion rules](/confluence/display/c/INT02-C.+Understand+integer+conversion+rules)
-   Page:
    [INT04-C. Enforce limits on integer values originating from tainted sources](/confluence/display/c/INT04-C.+Enforce+limits+on+integer+values+originating+from+tainted+sources)
-   Page:
    [INT05-C. Do not use input functions to convert character data if they cannot handle all possible inputs](/confluence/display/c/INT05-C.+Do+not+use+input+functions+to+convert+character+data+if+they+cannot+handle+all+possible+inputs)
-   Page:
    [INT07-C. Use only explicitly signed or unsigned char type for numeric values](/confluence/display/c/INT07-C.+Use+only+explicitly+signed+or+unsigned+char+type+for+numeric+values)
-   Page:
    [INT08-C. Verify that all integer values are in range](/confluence/display/c/INT08-C.+Verify+that+all+integer+values+are+in+range)
-   Page:
    [INT09-C. Ensure enumeration constants map to unique values](/confluence/display/c/INT09-C.+Ensure+enumeration+constants+map+to+unique+values)
-   Page:
    [INT10-C. Do not assume a positive remainder when using the % operator](../c/INT10-C_%20Do%20not%20assume%20a%20positive%20remainder%20when%20using%20the%20%%20operator)
-   Page:
    [INT12-C. Do not make assumptions about the type of a plain int bit-field when used in an expression](/confluence/display/c/INT12-C.+Do+not+make+assumptions+about+the+type+of+a+plain+int+bit-field+when+used+in+an+expression)
-   Page:
    [INT13-C. Use bitwise operators only on unsigned operands](/confluence/display/c/INT13-C.+Use+bitwise+operators+only+on+unsigned+operands)
-   Page:
    [INT14-C. Avoid performing bitwise and arithmetic operations on the same data](/confluence/display/c/INT14-C.+Avoid+performing+bitwise+and+arithmetic+operations+on+the+same+data)
-   Page:
    [INT15-C. Use intmax_t or uintmax_t for formatted IO on programmer-defined integer types](/confluence/display/c/INT15-C.+Use+intmax_t+or+uintmax_t+for+formatted+IO+on+programmer-defined+integer+types)
-   Page:
    [INT16-C. Do not make assumptions about representation of signed integers](/confluence/display/c/INT16-C.+Do+not+make+assumptions+about+representation+of+signed+integers)
-   Page:
    [INT17-C. Define integer constants in an implementation-independent manner](/confluence/display/c/INT17-C.+Define+integer+constants+in+an+implementation-independent+manner)
-   Page:
    [INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size](/confluence/display/c/INT18-C.+Evaluate+integer+expressions+in+a+larger+size+before+comparing+or+assigning+to+that+size)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [int](https://confluence/label/seccode/int) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT00-C | High | Unlikely | High | P3 | L3 |
| INT01-C | Medium | Probable | Medium | P8 | L2 |
| INT02-C | Medium | Probable | Medium |  P8  |  L2  |
| INT04-C | High | Probable | High | P6 | L2 |
| INT05-C | Medium | Probable | High | P4 | L3 |
| INT07-C | Medium | Probable | Medium | P8 | L2 |
| INT08-C | Medium | Probable | High | P4 | L3 |
| INT09-C | Low | Probable | Medium | P4 | L3 |
| INT10-C | High | Unlikely | High | P3 | L3 |
| INT12-C | Low | Unlikely | Medium | P2 | L3 |
| INT13-C | High | Unlikely | Medium | P6 | L2 |
| INT14-C | Medium | Unlikely | Medium | P4 | L3 |
| INT15-C | High | Unlikely | Medium | P6 | L2 |
| INT16-C | Medium | Unlikely | High |  P2  |  L3  |
| INT17-C | High | Probable | Low | P18 | L1 |
| INT18-C | High | Likely | Medium | P18 | L1 |

## Related Rules and Recommendations

|  |
| ----|
| DCL31-C. Declare identifiers before using them |
| DCL31-C. Declare identifiers before using them |
| DCL31-C. Declare identifiers before using them |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| FIO09-C. Be careful with binary data when transferring data across systems |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |
| void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char) |

------------------------------------------------------------------------
[](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](../c/INT00-C_%20Understand%20the%20data%20model%20used%20by%20your%20implementation_s_)
