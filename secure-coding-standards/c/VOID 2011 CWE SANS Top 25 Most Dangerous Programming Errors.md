The [2011 CWE/SANS Top 25 Most Dangerous Programming Errors](https://cwe.mitre.org/top25/) is a list of the most significant programming errors that can lead to serious software vulnerabilities compiled by the SANS Institute, MITRE, and top software security experts in the US and Europe.
Existing CERT C guidelines reference relevant [Common Weakness Enumeration](http://cwe.mitre.org/) (CWE) IDs via [labels](http://confluence.atlassian.com/display/DOC/Working+with+Labels). The tables on this page identify the appropriate secure coding guidelines for the C language that must be enforced to mitigate against each CWE in the Top 25 Most Dangerous Programming Errors. There are some cases where there are no corresponding guidelines, either because these CWEs address web development which is not in scope for any of the existing secure coding standards or address other elements of secure programming that cannot be adequately addressed by a secure coding standard.
### Insecure Interaction Between Components
These weaknesses are related to insecure ways in which data is sent and received between separate components, modules, programs, processes, threads, or systems.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | n/a |
| CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | 
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
                Page:        
                        ENV33-C. Do not call system()
                Page:        
                        STR02-C. Sanitize data passed to complex subsystems
     |
| CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | n/a |
| CWE-434: Unrestricted Upload of File with Dangerous Type | n/a |
| CWE-352: Cross-Site Request Forgery (CSRF) | n/a |
| CWE-601: URL Redirection to Untrusted Site ('Open Redirect') | n/a |

### Risky Resource Management
The weaknesses in this category are related to ways in which software does not properly manage the creation, usage, transfer, or destruction of important system resources.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | 
                Page:        
                        STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator
                Page:        
                        VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array
     |
| CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | 
                Page:        
                        FIO02-C. Canonicalize path names originating from tainted sources
     |
| CWE-494: Download of Code Without Integrity Check | n/a |
| CWE-829: Inclusion of Functionality from Untrusted Control Sphere | n/a |
| CWE-676: Use of Potentially Dangerous Function | 
                Page:        
                        ERR07-C. Prefer functions that support error checking over equivalent functions that don't
                Page:        
                        ERR34-C. Detect errors when converting a string to a number
                Page:        
                        FIO01-C. Be careful using functions that use file names for identification
                Page:        
                        MSC24-C. Do not use deprecated or obsolescent functions
     |
| CWE-131: Incorrect Calculation of Buffer Size | 
                Page:        
                        MEM35-C. Allocate sufficient memory for an object
     |
| CWE-134: Uncontrolled Format String | 
                Page:        
                        FIO30-C. Exclude user input from format strings
     |
| CWE-190: Integer Overflow or Wraparound | 
                Page:        
                        INT18-C. Evaluate integer expressions in a larger size before comparing or assigning to that size
                Page:        
                        INT30-C. Ensure that unsigned integer operations do not wrap
                Page:        
                        INT32-C. Ensure that operations on signed integers do not result in overflow
                Page:        
                        MEM07-C. Ensure that the arguments to calloc(), when multiplied, do not wrap
                Page:        
                        MEM35-C. Allocate sufficient memory for an object
                Page:        
                        VOID. INT03-C. Use a secure integer library
     |

### Porous Defenses
The weaknesses in this category are related to defensive techniques that are often misused, abused, or just plain ignored.

| CWE | CERT C Guidelines |
| ----|----|
| CWE-306: Missing Authentication for Critical Function | n/a |
| CWE-862: Missing Authorization | n/a |
| CWE-798: Use of Hard-coded Credentials | 
                Page:        
                        MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
     |
| CWE-311: Missing Encryption of Sensitive Data | 
                Page:        
                        MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
                Page:        
                        WIN04-C. Consider encrypting function pointers
     |
| CWE-807: Reliance on Untrusted Inputs in a Security Decision | 
                Page:        
                        ENV01-C. Do not make assumptions about the size of an environment variable
                Page:        
                        ENV02-C. Beware of multiple environment variables with the same effective name
                Page:        
                        ENV03-C. Sanitize the environment when invoking external programs
     |
| CWE-250: Execution with Unnecessary Privileges | 
                Page:        
                        POS02-C. Follow the principle of least privilege
                Page:        
                        POS36-C. Observe correct revocation order while relinquishing privileges
                Page:        
                        POS37-C. Ensure that privilege relinquishment is successful
     |
| CWE-863: Incorrect Authorization | n/a |
| CWE-732: Incorrect Permission Assignment for Critical Resource | 
                Page:        
                        FIO06-C. Create files with appropriate access permissions
     |
| CWE-327: Use of a Broken or Risky Cryptographic Algorithm | 
                Page:        
                        MSC30-C. Do not use the rand() function for generating pseudorandom numbers
                Page:        
                        MSC32-C. Properly seed pseudorandom number generators
     |
| CWE-307: Improper Restriction of Excessive Authentication Attempts | n/a |
| CWE-759: Use of a One-Way Hash without a Salt | n/a |

## Other Languages
A mapping between the CERT C++ Secure Coding Standard and [VOID 2011 CWE SANS Top 25 Most Dangerous Programming Errors](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+2011+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors) is available.
A mapping between the CERT Oracle Secure Coding Standard for Java and [VOID Rule: 2011 CWE SANS Top 25 Most Dangerous Programming Errors](https://wiki.sei.cmu.edu/confluence/display/java/VOID+Rule%3A+2011+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors) is available.
## References
[2011 CWE/SANS Top 25 Most Dangerous Programming Errors](https://cwe.mitre.org/top25/)  
[Common Weakness Enumeration](http://cwe.mitre.org/)
