Many applications need to handle sensitive data either in memory or on disk. If this sensitive data is not protected properly, it might lead to loss of secrecy or integrity of the data. It is very difficult (or expensive) to completely secure all the sensitive data. Users tend to use the same passwords everywhere. So even if your program is a simple game that stores the user's profile information and requires the user to enter a password, the user might choose the same password he or she uses for an online bank account for your game program. Now the user's bank account is only as secure as your program enables it to be.
There are simple steps you can take to secure sensitive data in your programs.
##### Prefer the system's authentication dialog (or any other mechanism provided by the OS) for authentication to privileged services.
If you are accessing some privileged service already installed on the system, most likely that service will have some mechanism to take a password from the user. Before asking the user for a user name and password from your application, check if the service itself authenticates the user in some way. If so, let the service handle the authentication because doing so would at least not increase the footprint of the sensitive data.
##### Do not hard code sensitive data in programs.
See [MSC41-C. Never hard code sensitive information](MSC41-C_%20Never%20hard%20code%20sensitive%20information) for details.
##### Disable memory dumps.
Memory dumps are automatically created when your program crashes. They can contain information stored in any part of program memory. Therefore, memory dumps should be disabled before an application is shipped to users. See [MEM06-C. Ensure that sensitive data is not written out to disk](MEM06-C_%20Ensure%20that%20sensitive%20data%20is%20not%20written%20out%20to%20disk) for details.
##### Do not store sensitive data beyond its time of use in a program.
Sensitive data that is stored in memory can get written to disk when a page is swapped out of the physical memory. (See next point for details about keeping sensitive data on disk.) You may be able to "lock" your data to keep it from swapping out. Your program will generally need administrative privileges to do so successfully, but it never hurts to try. See [MEM06-C. Ensure that sensitive data is not written out to disk](MEM06-C_%20Ensure%20that%20sensitive%20data%20is%20not%20written%20out%20to%20disk) for details.
##### Do not store sensitive data in plaintext (either on disk or in memory).
See [MEM06-C. Ensure that sensitive data is not written out to disk](MEM06-C_%20Ensure%20that%20sensitive%20data%20is%20not%20written%20out%20to%20disk).
While using a password, consider storing its hash instead of plaintext. Use the hash for comparisons and other purposes. The following code \[[Viega 2001](AA.-Bibliography_87152170.html#AA.Bibliography-Viega01)\] illustrates:
``` c
int validate(char *username) {
  char *password;
  char *checksum;
  password = read_password();
  checksum = compute_checksum(password);
  erase(password);  /* Securely erase password */
  return !strcmp(checksum, get_stored_checksum(username));
}
```
##### If you must store sensitive data, encrypt it first.
1.  If encrypting or hashing sensitive data, do not implement your own encryption functions (or library). Use proven secure crypto libraries, which have been extensively tested for security.
2.  If using standard crypto libraries, be aware that they have certain requirements (documented with the library) for the key sizes and other properties. Choose keys that satisfy these conditions.
3.  Do not store the encryption keys (you can derive the key from the hash of the user's password or any other cryptographic mechanism, provided the above condition holds). If the key is to be stored, store it securely.
##### Securely erase sensitive data from disk and memory.
1.  Be aware of compiler optimization when erasing memory. (See [MSC06-C. Beware of compiler optimizations](MSC06-C_%20Beware%20of%20compiler%20optimizations).)
2.  Use secure erase methods specified in U.S. Department of Defense Standard 5220 \[[DOD 5220](AA.-Bibliography_87152170.html#AA.Bibliography-DOD5220)\] or Peter Gutmann's paper \[[Gutmann 1996](AA.-Bibliography_87152170.html#AA.Bibliography-Gutmann96)\].
## Risk Assessment
If sensitive data is not handled correctly in a program, an attacker can gain access to it.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC18-C | Medium | Probable | Medium | P8 | L2 |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC18-C).
## Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | HARDCODED.AUTHHARDCODED.KEYHARDCODED.SALTMISC.PWD.PLAINMISC.PWD.PLAINTRAN | Hardcoded AuthenticationHardcoded Crypto KeyHardcoded Crypto SaltPlaintext Storage of PasswordPlaintext Transmission of Password |
| PC-lint Plus | 1.4 | 586 | Partially supported: reports functions that read passwords from the user or that take a password as an argument instead of prompting the user as well as insecure password erasure |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC18-C | Checks for:Constant or predictable block cipher initialization vectorConstant or predictable cipher keySensitive heap memory not cleared before releaseUncleared sensitive data in stackUnsafe standard encryption functionRec. partially covered. |

## Related Guidelines

|  |  |
| ----|----|
| CERT Oracle Secure Coding Standard for Java | MSC03-J. Never hard code sensitive information |
| CERT C Secure Coding Standard | MSC41-C. Never hard code sensitive information |
| MITRE CWE | CWE-259, Use of Hard-coded PasswordCWE-261, Weak Cryptography for Passwords
CWE-311, Missing encryption of sensitive data
CWE-319, Cleartext Transmission of Sensitive Information
CWE-321, Use of Hard-coded Cryptographic Key
CWE-326, Inadequate encryption strength
CWE-798, Use of hard-coded credentials |

## Bibliography

|  |  |
| ----|----|
| [DOD 5220] | Standard 5220 |
| [Gutmann 1996] | "Secure Deletion of Data from Magnetic and Solid-State Memory" |
| [Lewis 2006] | "Security Considerations when Handling Sensitive Data" |
| [Viega 2001] | "Protecting Sensitive Data in Memory" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152277) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/MSC19-C_%20For%20functions%20that%20return%20an%20array,%20prefer%20returning%20an%20empty%20array%20over%20a%20null%20value)
## Comments:

|  |
| ----|
| This recommendation needs to be reconciled with MSC06-C. Be aware of compiler optimization when dealing with sensitive data and MEM03-C. Clear sensitive information stored in reusable resources.
                                        Posted by rcs at Jan 20, 2009 09:52
                                     |
| For this part:;
If you must store sensitive data, encrypt it first.
I suggest adding reference to CWE 326 as well.
                                        Posted by azukich at Feb 21, 2010 14:44
                                     |
| ok, done.
                                        Posted by rcs_mgr at Feb 21, 2010 22:32
                                     |
| Hi,There is a rule for Java which is  MSC03-J. Never hard code sensitive information
As i know and saw, it is possible to find information since an exe or dll. It is likely more difficult.
Don't you think we should have the same rule for C ?
Jérôme
                                        Posted by jerome.guy at Mar 26, 2018 01:53
                                     |
| You're right. I've added a C rule:;MSC41-C. Never hard code sensitive information, based on the Java rule. Comments welcome.
                                        Posted by svoboda at Mar 26, 2018 11:42
                                     |
| "If the key is to be stored, store it securely." This seems silly. If you have a way you can "securely" store the key, you could skip the encryption and just store the original data that way.
                                        Posted by jcsible at Jun 30, 2020 12:06
                                     |
| As I also commented on MEM06-C. Ensure that sensitive data is not written out to disk, completely disabling memory dumps is overly broad. (In fact, I can see an argument that it may reduce security in the long run: crash bugs often end up being exploitable, and not having dumps will make it take longer to debug and fix them, lengthening the window of vulnerability.)
                                        Posted by jcsible at Jun 30, 2020 12:09
                                     |
| I agree that wording sounds silly on the surface. But there are multiple degrees of sensitive information and multiple layers of security. Obviously encrypting some plainext with a key that must also be encrypted is also silly. But you can take security measures to protect the key that are less secure (or complex) than encryption. ;Storing it in a secure directory (see FIO15-C. Ensure that file operations are performed in a secure directory) is one such possibility.
                                        Posted by svoboda at Aug 13, 2020 14:56
                                     |
| If you have a secure directory, why not just store the password there instead?
                                        Posted by jcsible at Aug 13, 2020 15:11
                                     |
| Do you store your passwords in plain text on your home directory? :)There are different levels of security, just as there are different types of attackers with different motives. A password should not be stored unencrypted on your filesystem, because the machine doesn't even need to know them...it only needs their hashed values. (If you use some sort of password manager I hope for your sake it at least encrypts your passwords :) But a key needs less security than a password (in general), and you need the actual key (rather than a hash).
                                        Posted by svoboda at Aug 13, 2020 15:29
                                     |
| Hashing passwords only applies for the program that's verifying the hash. For example, to set up an application to connect to a database, the password can be hashed on the database's end, but can't be hashed in the application's config file.
                                        Posted by jcsible at Aug 13, 2020 15:32
                                     |

