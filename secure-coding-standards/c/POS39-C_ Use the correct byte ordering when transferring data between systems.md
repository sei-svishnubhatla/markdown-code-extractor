Different system architectures use different byte ordering, either little endian (least significant byte first) or big endian (most significant byte first). IA-32 is an example of an architecture that implements little endian byte ordering. In contrast, PowerPC and most Network Protocols (including TCP and IP) use big endian.
When transferring data between systems of different endianness, the programmer must take care to reverse the byte ordering before interpreting the data.
The functions `htonl()`, `htons()`, `ntohl()`, and `ntohs()` can be used to transfer between network byte ordering (big endian) and the host's byte ordering. On big endian systems, these functions do nothing. They may also be implemented as macros rather than functions.
## Noncompliant Code Example
In this noncompliant code example, the programmer tries to read an unsigned 32-bit integer off a previously connected network socket.
It is important to know the sizes of your data types lest they be different on architectures that are accessible over the network. Hence, we transfer a `uint32_t` rather than an `int`. For more information, see [FIO09-C. Be careful with binary data when transferring data across systems](FIO09-C_%20Be%20careful%20with%20binary%20data%20when%20transferring%20data%20across%20systems).
``` c
/* sock is a connected TCP socket */
uint32_t num;
if (recv(sock, (void *)&num, sizeof(uint32_t), 0) < (int)sizeof(uint32_t)) {
  /* Handle error */
}
printf("We received %u from the network!\n", (unsigned int)num);
```
This program prints out the number received from the socket using an incorrect byte ordering. For example, if the value 4 is sent from a big endian machine, and the receiving system is little endian, the value 536,870,912 is read. This problem can be corrected by sending and receiving using network byte ordering.
## Compliant Solution
In this compliant solution, the programmer uses the `ntohl()` function to convert the integer from network byte order to host byte ordering:
``` c
/* sock is a connected TCP socket */
uint32_t num;
if (recv(sock, (void *)&num, sizeof(uint32_t), 0) < (int)sizeof(uint32_t)) {
  /* Handle error */
}
num = ntohl(num);
printf("We recieved %u from the network!\n", (unsigned int)num);
```
The `ntohl()` function (network to host long) translates a `uint32_t` value into the host byte ordering from the network byte ordering. This function is always appropriate to use because its implementation depends on the specific system's byte ordering. Consequently, on a big endian architecture, `ntohl()` does nothing.
The reciprocal function `htonl()` (host to network long) should be used before sending any data to another system over network protocols.
#### Portability Details
-   `ntohs()`, `ntohl()`, `htons()`, and `htonl()` are not part of the C Standard and are consequently not guaranteed to be portable to non-POSIX systems.
-   The POSIX implementations of `ntohs()`, `ntohl()`, `htons()`, and `htonl()` take arguments of types `uint16_t` and `uint32_t` and can be found in the header file `<arpa/inet.h>`.
-   The Windows implementations use `unsigned short` and `unsigned long` and can be found in the header file `<winsock2.h>`.
-   Other variants of `ntoht()` and `htont()`, such as `ntohi()`/`htoni()` or `ntohll()`/`htonll()`, may exist on some systems.
## Risk Assessment
If the programmer is careless, this bug is likely. However, it will immediately break the program by printing the incorrect result and therefore should be caught by the programmer during the early stages of debugging and testing. Recognizing a value as in reversed byte ordering, however, can be difficult depending on the type and magnitude of the data.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS39-C | Medium | Likely | Low | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | taint_sink | Soundly supported |
| Axivion Bauhaus Suite | 7.2.0 | CertC-POS39 |  |
| Helix QAC | 2024.4 | DF4906, DF4907, DF4908 |  |
| Klocwork | 2024.4 | BYTEORDER.NTOH.RECVBYTEORDER.NTOH.READ
BYTEORDER.HTON.SEND
BYTEORDER.HTON.WRITE |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS39-a | Use the correct byte ordering when transferring data between systems |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS39-C | Checks for missing byte reordering when transferring data (rule fully covered) |

## Bibliography

|  |  |
| ----|----|
| [MSDN] | "Winsock Functions" |
| [Open Group 2004] | htonl, htons, ntohl, ntohs—Convert Values between Host and Network Byte Order |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152299) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152034)
## Comments:

|  |
| ----|
| This is the beginnings of a good rule. Suggestions:
    It should be in the POSIX section, since networking functions & sockets are not defined by the C standard.
    I thought that mtobl() and other related functions were fully portable; in that they abstract away the fact that host byte order may differ from network byte order.
    The manpage reference needs more qualification; which platform? Prob best to use the POSIX standard definition as a reference instead.
    Complete the rule (eg risk assessment)
                                        Posted by svoboda at Apr 01, 2009 13:04
                                     |
| What do you mean by adding qualification to the manpage? That link is to the POSIX definition of the function.  
                                        Posted by hpitelka at Apr 01, 2009 17:04
                                     |
| Then cite the POSIX definition as the source, as POSIX is an authoritative standard.
The other rules in the POSIX section show how to reference POSIX.
                                        Posted by svoboda at Apr 01, 2009 20:30
                                     |
| The best place to reference POSIX functions is at the The Open Group Base Specifications Issue 7
IEEE Std 1003.1-2008.  For example, you can reference ntohl to this page:
http://www.opengroup.org/onlinepubs/9699919799/functions/htonl.html
We also need a new entry in the bibliography because we haven't linked to IEEE Std 1003.1-2008 before because this is a new standard.
Other problems with this guideline... neither Little Endian or Big Endian should be capitalized.
If you mention specific processors outside of an "Implementation Details" section, make sure you say they are "examples". 
I would not say that "Currently x86 is the most common platform to use Little Endian." because this information is clearly dated and also reads a bit like marketing material.  Just say something like "IA-32 is an example of a little endian architecture."
Now, a bigger problem.  I actually don't see any real reason why this rule should be in the POSIX section.  Byte ordering is a problem on any system.  Could you just rewrite the compliant solution to only use C99 functions?  I'm OK with a POSIX specific solution (marked POSIX) but you should also be able to provide a portable solution.
Noncompliant is spelled without a hyphen (at least in our guideline).
Instead of saying "(assuming an x86 system)" just specify the actual assumptions necessary for your example to hold true "assuming a little endian architecture and 32 bit signed integers" or whatever.
                                        Posted by rcs at Apr 01, 2009 20:59
                                     |
| 
    The references section is for external references, the link to FIO09-C belongs in the discussion.
    Not sure the severity is high, how can you execute shellcode thru this vul? Also the probability strikes me as very likely, assuming you're on a little-endian system, no?
    Probably should define ntohl in the intro, since on little-endiansystems it reverses the bits while on big-endian systems it does nothing, and explain its rationale.
Those plus Rob's suggestions should complete this rule.
                                        Posted by svoboda at Apr 01, 2009 23:05
                                     |
| Hunter, please double check my edits, particularly the "Notes".   I changed the severity to medium because I view this primarily as a data integrity issue and not a run arbitrary code type of issue.  I also changed the likelihood to high based on David's comment.
                                        Posted by rcs at Apr 02, 2009 10:05
                                     |
| I agree with your comments. However, on the BSD libc these {h,n}to{h,n}{l,s} functions are included by default and are in a different header file, should I add that to the notes section? And what else would you recommend I change about this rule? 
                                        Posted by hpitelka at Apr 03, 2009 16:04
                                     |
| Hunter, please see my last comment for suggestions on improving the rule. To answer your question, I don't think details like which header file the byte-ordering functions live in is that significant. So you can include the BSD info if you like, but its not necessary.
                                        Posted by svoboda at Apr 03, 2009 21:51
                                     |
| 
    It's good to define ntohl() & co in the intro but the text could be clearer. Assume the reader is new to network programming and doesn't know about these functions.
    As I said earlier, the link to FIO09-C belongs in the discussion. The 'related vuls' is the Wrong Place for it.
                                        Posted by svoboda at Apr 04, 2009 08:42
                                     |
| The code examples assume that sizeof(int) is the same between architectures.  This is just as bad an assumption as the byte ordering one that is the subject of the rule.
I suggest changing the rule name to something like "Allow for data types having different representations when transferring data between systems" and covering both issues.
                                        Posted by geoffclare at Apr 06, 2009 04:50
                                     |
| Good catch. I weaseled around the problem by using uint32_t instead of int.
The issue of differing data type representations is mostly covered by FIO09-C, which is referenced in the rule.
                                        Posted by svoboda at Apr 06, 2009 11:39
                                     |
| 
Good catch. I weaseled around the problem by using uint32_t instead of int.
Now that num isn't an int, the printf format is wrong.  You should either use the PRIu32 macro from <inttypes.h>, or use %u and cast the argument to unsigned int.
The issue of differing data type representations is mostly covered by FIO09-C, which is referenced in the rule.
Oops.  I hadn't noticed the reference.  I agree that FIO09 covers the other issue.
                                        Posted by geoffclare at Apr 06, 2009 12:10
                                     |
| 
Now that num isn't an int, the printf format is wrong. You should either use the PRIu32 macro from <inttypes.h>, or use %u and cast the argument to unsigned int.
Fixed, thanks.
                                        Posted by svoboda at Apr 07, 2009 08:59
                                     |
| I believe I have addressed all the remaining issues in this rule.
                                        Posted by svoboda at Apr 14, 2009 17:16
                                     |

