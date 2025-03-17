> [!info]  
>
> This guideline has been labeled void and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
When writing a library, each exposed function should perform a validity check on its parameters. Validity checks allow the library to survive at least some forms of improper usage, enabling an application using the library to likewise survive, and often simplifies the task of determining the condition that caused the invalid parameter.
## Noncompliant Code Example
In this noncompliant code example, setState() and {{useState()}}do not validate their parameters. It is possible that an invalid file pointer may be used by the library, corrupting the library's internal state and exposing a \[vulnerability\|../display/seccode/BB.+Definitions#BB.Definitions-vulnerability\].private Object \*myState;
/\* sets some internal state in the library \*/  
void setfile(Object state) {  
myFile = file;  
}
/\* performs some action using the file passed earlier \*/  
void usefile() {  
/\* perform some action here \*/  
}
The vulnerability may be more severe if the internal state references sensitive or system-critical data.
## Compliant Solution
Validating the function parameters and verifying the internal state leads to consistency of program execution and may eliminate potential vulnerabilities./\* sets some internal state in the library \*/  
extern int setfile(FILE \*file);
/\* performs some action using the file passed earlier \*/  
extern int usefile();
static FILE \*myFile;
/\* sets some internal state in the library \*/  
errno_t setfile(FILE \*file) {  
if (file && !ferror(file) && !feof(file))
Unknown macro: { myFile = file; return 0; }
myFile = NULL;  
return INVALID_ARG;  
}
errno_t usefile(void) {  
if (!myFile) return -1;
/\* perform other checks if needed, return
-   error condition \*/
/\* perform some action here \*/  
return 0;  
}
## Risk Assessment
Failing to validate the parameters in library functions may result in an access violation or a data integrity violation. Such a scenario is indicative of a flaw in the manner in which the library is used by the calling code. However, it may still be the library itself that is the vector by which the calling code's vulnerability is exploited.

|  Recommendation  |  Severity  |  Likelihood  |  Remediation Cost  |  Priority  |  Level  |
| ----|----|----|----|----|----|
|  MSC08-C  |  medium  |  unlikely  |  high  |  P2  |  L3  |

### Automated Detection
TODO
### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the CERT website.
## Related Guidelines
This rule appears in the C Secure Coding Standard as APP00-C. Functions should validate their parameters.
[cplusplus:CERT C++ Secure Coding Standard](/confluence/pages/createpage.action?spaceKey=cplusplus&title=CERT+C%2B%2B+Secure+Coding+Standard): \[MSC08-CPP. Library functions should validate their parameters\|../display/cplusplus/MSC08-CPP.+Library+functions+should+validate+their+parameters\]
MITRE CWE: CWE-20, "Insufficient Input Validation"
## References
\[\[Apple 2006\|../display/seccode/AA.+C+References#AA.CReferences-Apple06\]\] Application Interfaces That Enhance Security, May 2006.
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Ensure+that+source+and+destination+pointers+in+function+arguments+do+not+point+to+overlapping+objects?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Guarantee+that+array+indices+are+within+the+valid+range?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| This page is a mistake and needs to be deleted.; However, I can't find how to do that.
                                        Posted by eschwelm at Mar 31, 2009 03:49
                                     |

