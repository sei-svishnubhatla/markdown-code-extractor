Hard coding sensitive information, such as passwords or encryption keys can expose the information to attackers. Anyone who has access to the executable or dynamic library files can examine them for strings or other critical data, revealing the sensitive information. Leaking data protected by International Traffic in Arms Regulations (ITAR) or the Health Insurance Portability and Accountability Act (HIPAA) can also have legal consequences. Consequently, programs must not hard code sensitive information.
Hard coding sensitive information also increases the need to manage and accommodate changes to the code. For example, changing a hard-coded password in a deployed program may require distribution of a patch \[[Chess 2007](AA.-Bibliography_87152170.html#AA.Bibliography-Chess07)\].
## Noncompliant Code Example (Hard-Coded Database Password)
This noncompliant code example must authenticate to a remote service with a code, using the `authenticate()` function declared below. It passes the authentication code to this function as a string literal.
``` cpp
/* Returns nonzero if authenticated */
int authenticate(const char* code);
int main() {
  if (!authenticate("correct code")) {
    printf("Authentication error\n");
    return -1;
  }
  printf("Authentication successful\n");
  // ...Work with system...
  return 0;
}
```
The authentication code exists in the program's binary executable and can be easily discovered.
### Implementation Details (Unix)
Many Unix platforms provide a `strings` utility that prints out all of the ASCII strings in a binary file. Here is the output of running `strings` on this program, on an Ubuntu 16.04 platform:
``` bash
% strings a.out
...
AUATL
[]A\A]A^A_
correct code
Authentication error
Authentication successful
...
%
```
## Compliant Solution
This compliant solution requires the user to supply the authentication code, and securely erases it when done, using `memset_s()`, an optional function provided by C11's Annex K.
``` cpp
/* Returns nonzero if authenticated */
int authenticate(const char* code);
int main() {
#define CODE_LEN 50
  char code[CODE_LEN];
  printf("Please enter your authentication code:\n");
  fgets(code, sizeof(code), stdin);
  int flag = authenticate(code);
  memset_s(code, sizeof(code), 0, sizeof(code));
  if (!flag) {
    printf("Access denied\n");
    return -1;
  }
  printf("Access granted\n");
  // ...Work with system...
  return 0;
}
```
Alternatively, the program could read the authentication code from a file, letting file system security protect the file and the code from untrusted users.
## Risk Assessment
Hard coding sensitive information exposes that information to attackers. The severity of this rule can vary depending on the kind of information that is disclosed. Frequently, the information disclosed is password or key information, which can lead to remote exploitation. Consequently, a high severity rating is given but may be adjusted downwards according to the nature of the sensitive data. 

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC41-C | High | Probable | Medium | P12 | L1 |

## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported |
| CodeSonar | 8.3p0 | HARDCODED.AUTHHARDCODED.DNS
HARDCODED.KEY
HARDCODED.SALT
HARDCODED.SEED
 | Hardcoded AuthenticationHardcoded DNS Name
Hardcoded Crypto Key
Hardcoded Crypto SaltHardcoded Seed in PRNG |
| Helix QAC | 2024.4 | C3122C++3842 |  |
| Klocwork | 2024.4 | HCCHCC.PWD
HCC.USER
CXX.SV.PWD.PLAIN
CXX.SV.PWD.PLAIN.LENGTH
CXX.SV.PWD.PLAIN.ZERO |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC41-a | Do not hard code string literals |
| PC-lint Plus | 1.4 | 2460 | Assistance provided: reports when a literal is provided as an argument to a function parameter with the ‘noliteral’ argument Semantic; several Windows API functions are marked as such and the ‘-sem’ option can apply it to other functions as appropriate |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC41-C | Checks for hard coded sensitive data (rule partially covered) |
| RuleChecker | 24.04 |  | Supported |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT Oracle Coding Standard for Java | MSC03-J. Never hard code sensitive information |
| ISO/IEC TR 24772:2010 | Hard-coded Password [XYP] |
| MITRE CWE | CWE-259, Use of Hard-Coded PasswordCWE-798, Use of Hard-Coded Credentials |

## Bibliography

|  |  |
| ----|----|
| [Chess 2007] | Section 11.2, "Outbound Passwords: Keep Passwords out of Source Code" |
| [Fortify 2006] | "Unsafe Mobile Code: Database Access" |

------------------------------------------------------------------------
[MSC40-C. Do not violate constraints](/confluence/pages/createpage.action?spaceKey=java&title=MSC40-C.+Do+not+violate+constraints) [Rule 48. Miscellaneous (MSC)](/confluence/pages/createpage.action?spaceKey=java&title=Rule+48.+Miscellaneous+%28MSC%29) [Rule 50. POSIX (POS)](/confluence/pages/createpage.action?spaceKey=java&title=Rule+50.+POSIX+%28POS%29)
## Attachments:
![](images/icons/bullet_blue.gif) [button_arrow_left.png](attachments/108396967/108396951.png) (image/png)  
![](images/icons/bullet_blue.gif) [button_arrow_up.png](attachments/108396967/108396953.png) (image/png)  
![](images/icons/bullet_blue.gif) [button_arrow_right.png](attachments/108396967/108396954.png) (image/png)  
![](images/icons/bullet_blue.gif) [Edit.url](attachments/108396967/335675490.url) (application/octet-stream)  
## Comments:

|  |
| ----|
| This rule was created in response to this comment:;Re: MSC18-C. Be careful while handling sensitive data, such as passwords, in program code
                                        Posted by svoboda at Mar 26, 2018 15:55
                                     |
| Taking into account that systems running the code (e.g. microcontrollers) may have a "readback protection mechanism" that does not allow reading back the memory where the program code resides, this rule should be considered more as a recommendation.;
                                        Posted by jjrnavarro at Oct 18, 2018 03:03
                                     |
| You are rightBut here you give a solution.As you wrote the systems "may have a "readback protection mechanism""So we must consider it is not the case and then take your recommandation (use "readback protection mechanism") as a possible solution.What do you think about that ?
                                        Posted by jerome.guy at Oct 18, 2018 03:40
                                     |
| "Never hard code sensitive information" can be a solution to the problem "exposing sensitive information".;"Use readback protection mechanisms" is also a solution to the same problem (as you point out too).Since there is more than one solution to the same problem:Should one solution be declared as rule? In my opinion, if solutions are not always applicable, I would not define any of them as rule but recommendations.  
                                        Posted by jjrnavarro at Oct 18, 2018 04:54
                                     |
| You are right again The aim is "Protect sensitive information" or something like this.So the rule could be renamed in this direction.
                                        Posted by jerome.guy at Oct 18, 2018 05:14
                                     |
| "Protect sensitive information" seems to me a better name for this rule. Said rule, as violation may adversely affect security.; 
                                        Posted by jjrnavarro at Oct 18, 2018 05:22
                                     |
| JoséI have a question about the possibility of finding information since a DLL or an EXE.Also if i use readback protection mechanism, i suppose it is nevertheless possible to find sensitive information in that case.Am I wrong ?
                                        Posted by jerome.guy at Oct 18, 2018 08:21
                                     |
| The goal of this rule is to protect sensitive information, but that is also the goal of many other rules, so I don't think it makes a good title.; Furthermore, embedding sensitive information, such as passwords, in program code increases the attack surface in several ways that cannot be mitigated by readback protections. If the attacker manages to obtain your binary file, readback protection won't protect you.  Finally, as Jérôme GUY noted, readback protections is not required by the C standard and cannot be relied on by truly portable code.
                                        Posted by svoboda at Oct 18, 2018 09:30
                                     |
| The above "complaint solution" relies on a user entering a code or a secure file system. According to the definition of rule, "rules shall not rely on assumptions". Readback protection mechanisms are just another way to protect sensitive data if they are available and prove to be secure. Both solutions unfortunately rely on some assumptions.
                                        Posted by jjrnavarro at Oct 23, 2018 05:18
                                     |
| A small mistake in the code of the Compliant; Solution :?is:memset_s(code, 0, sizeof(code));should be:memset_s(code, sizeof(code), 0, sizeof(code));ormemset(code, 0, sizeof(code));
                                        Posted by piotr.legezinski at May 27, 2022 04:01
                                     |
| You are right. I just fixed it.
                                        Posted by jcsible at May 27, 2022 12:45
                                     |
| Additional note: using memset();would not necessarily give us the behavior we are intending, because memset() can be optimized away if that memory space isn't used again. For a one-time use credential, it's likely to not be used again, and therefore likely to be optimized away.  memset_s() should not be optimized away by a C-compliant compiler.  Therefore, it should only be memset_s() to be a Compliant Solution.
                                        Posted by rschiela at May 27, 2022 18:25
                                     |
| Agreed. This is explained in detail in MSC06-C. Beware of compiler optimizations.
                                        Posted by svoboda at Jun 16, 2022 12:30
                                     |
| FWIW WG14 just approved document n2897 (alternative 1) to be adopted into C23. This provides memset_explicit(), with functionality like Annex K's memset_s(), but it will be in the main litrary (not an Annex).
                                        Posted by svoboda at Jun 16, 2022 12:33
                                     |

