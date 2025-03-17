A *data model* defines the sizes assigned to standard data types. It is important to understand the data models used by your [implementation](http://BB.%20Definitions#implementation). However, if your code depends on any assumptions not guaranteed by the standard, you should provide static assertions to ensure that your assumptions are valid. (See [DCL03-C. Use a static assertion to test the value of a constant expression](DCL03-C_%20Use%20a%20static%20assertion%20to%20test%20the%20value%20of%20a%20constant%20expression).) Assumptions concerning integer sizes may become invalid, for example, when porting from a 32-bit architecture to a 64-bit architecture.
### Common Data Models

| Data Type | iAPX86 | IA-32 | IA-64 | SPARC-64 | ARM-32 | Alpha | 64-bit Linux, FreeBSD, 
NetBSD, and OpenBSD |
| ----|----|----|----|----|----|----|----|
| char | 8 | 8 | 8 | 8 | 8 | 8 | 8 |
| short | 16 | 16 | 16 | 16 | 16 | 16 | 16 |
| int | 16 | 32 | 32 | 32 | 32 | 32 | 32 |
| long | 32 | 32 | 32 | 64 | 32 | 64 | 64 |
| long long | N/A | 64 | 64 | 64 | 64 | 64 | 64 |
| Pointer | 16/32 | 32 | 64 | 64 | 32 | 64 | 64 |

Code frequently embeds assumptions about data models. For example, some code bases require pointer and `long` to have the same size, whereas other large code bases require `int` and `long` to be the same size \[[van de Voort 2007](AA.-Bibliography_87152170.html#AA.Bibliography-vandeVoort07)\]. These types of assumptions, while common, make the code difficult to port and make the ports error prone. One solution is to avoid any [implementation-defined behavior](http://BB.%20Definitions#implementation-defined%20behavior). However, this practice can result in inefficient code. Another solution is to include either static or runtime assertions near any platform-specific assumptions, so they can be easily detected and corrected during porting.
### `<limits.h>`
Possibly more important than knowing the number of bits for a given type is knowing that `limits.h` defines macros that can be used to determine the integral ranges of the standard integer types for any conforming implementation. For example, `UINT_MAX` is the largest possible value of an `unsigned int`, and `LONG_MIN` is the smallest possible value of a `long int`.
### `<stdint.h>`
The `stdint.h` header introduces types with specific size restrictions that can be used to avoid dependence on a particular data model. For example, `int_least32_t` is the smallest signed integer type supported by the implementation that contains at least 32 bits. The type `uint_fast16_t` is the fastest unsigned integer type supported by the implementation that contains at least 16 bits. The type `intmax_t` is the largest signed integer, and `uintmax_t` is the largest unsigned type, supported by the implementation. The following types are required to be available on all implementations:

| Smallest Types | Signed | Unsigned |
| ----|----|----|
| 8 bits | int_least8_t | uint_least8_t |
| 16 bits | int_least16_t | uint_least16_t |
| 32 bits | int_least32_t | uint_least32_t |
| 64 bits | int_least64_t | uint_least64_t |
| 8 bits | int_fast8_t | uint_fast8_t |
| 16 bits | int_fast16_t | uint_fast16_t |
| 32 bits | int_fast32_t | uint_fast32_t |
| 64 bits | int_fast64_t | uint_fast64_t |
| Maximum | intmax_t | uintmax_t |

Additional types may be supported by an implementation, such as `int8_t`, a type of exactly 8 bits, and `uintptr_t`, a type large enough to hold a converted `void *` if such an integer exists in the implementation.
### `<inttypes.h>`
The `inttypes.h` header declares functions for manipulating greatest-width integers and converting numeric character strings to greatest-width integers.
## Noncompliant Code Example
This noncompliant example attempts to read a `long` into an `int`. This code works for models in which `sizeof(int) == sizeof(long)`. For others, it causes an unexpected memory write similar to a buffer overflow.
``` c
int f(void) {
  FILE *fp;
  int x;
/* ... */
  if (fscanf(fp, "%ld", &x) < 1) {
    return -1; /* Indicate failure */
  }
/* ... */
  return 0;
}
```
Some compilers can generate warnings if a constant format string does not match the argument types.
## Compliant Solution
This compliant solution uses the correct format for the type being used:
``` c
int f(void) {
  FILE *fp;
  int x;
/* Initialize fp */
  if (fscanf(fp, "%d", &x) < 1) {
    return -1; /* Indicate failure */
  }
/* ... */
  return 0;
}
```
## Noncompliant Code Example
This noncompliant code attempts to guarantee that all bits of a multiplication of two `unsigned int` values are retained by performing arithmetic in the type `unsigned long`. This practice works for some platforms, such as 64-bit Linux, but fails for others, such as 64-bit Microsoft Windows.
``` c
unsigned int a, b;
unsigned long c;
/* Initialize a and b */
c = (unsigned long)a * b; /* Not guaranteed to fit */
```
## Compliant Solution
This compliant solution uses the largest unsigned integer type available if it is guaranteed to hold the result. If it is not, another solution must be found, as discussed in [INT32-C. Ensure that operations on signed integers do not result in overflow](INT32-C_%20Ensure%20that%20operations%20on%20signed%20integers%20do%20not%20result%20in%20overflow).
``` c
#if UINT_MAX > UINTMAX_MAX/UINT_MAX
#error No safe type is available.
#endif
/* ... */
unsigned int a, b;
uintmax_t c;
/* Initialize a and b */
c = (uintmax_t)a * b; /* Guaranteed to fit, verified above */
```
## Risk Assessment
Understanding the data model used by your [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation) is necessary to avoid making errors about the sizes of integer types and the range of values they can represent. Making assumptions about the sizes of data types may lead to buffer-overflow-style attacks.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT00-C | High | Unlikely | High | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT00 |  |
| PC-lint Plus | 1.4 | 559, 705, 706, 2403 | Assistance provided: Reports data type inconsistencies in format strings |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT00-C | Checks for:Use of basic numerical types instead of typedef-sInteger overflow or integer constant overflowFormat string specifiers and arguments mismatchRec. partially covered. |
| PVS-Studio | 7.35 | V629, V5004 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT00-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT00-CPP. Understand the data model used by your implementation(s) |
| ISO/IEC TR 24772:2013 | Bit Representations [STR] |

## Bibliography

|  |
| ----|
| [Open Group 1997a] |
| [van de Voort 2007] |

------------------------------------------------------------------------
[](../c/Rec_%2004_%20Integers%20_INT_) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152208)
## Comments:

|  |
| ----|
| I agree with the title of this page, but you make too much of the ILP terminology.; I think that you should acknowledge more clearly the existence of CPUs which do not have int, long and/or pointer that are either 32-bit or 64-bit: this is even more likely in the embedded arena than the desktop areas...  I've had to work with a CPU with 32-bit int, 40-bit long and 32-bit pointers.  These are CPUs that are used today in embedded systems.  Of course, there are a great number of 8-bit and 16-bit embedded systems still, too.
Is the severity really low?  A failure caused by this sort of problem would be very hard to detect, and I agree, very hard to remedy.
                                        Posted by stewartb at Mar 13, 2008 20:32
                                     |
| The ILP terminology should not even be mentioned!; There are minimum width requirements imposed by the C standard, which all implementations must meet, and for specific widths the types in <stdint.h> (and <inttypes.h>, which should at least be mentioned) ought to be used.
                                        Posted by dagwyn at Apr 15, 2008 15:44
                                     |
| rCs and I have modified the rule, and removed ILP terminology. We changed the table to reflect data models on common platforms today.
I can't find any refs on the Web regarding the size of a long long on IA 16-bit systems. I suspect this is because Intel moved to 32-bit machines before long long was ever considered. I do know long long was conceived to be at least 64-bits, and its raison d'etre was to ease the 32-to-64-bit transition devs are undergoing now. 
I also removed the column with 64-bit ints, longs, and pointers. According to http://www.unix.org/version2/whatsnew/lp64_wp.html
this data model (henceforth known as ILP64) proved to be difficult in porting programs (mainly because of the lack of a true 32-bit integer), and so is not widely popular.
                                        Posted by svoboda at May 23, 2008 15:45
                                     |
| should we enumerate the extra types defined in <stdint.h> by POSIX? we mention uintptr_t, but maybe we should just list all of them?
                                        Posted by avolkovi at Jun 06, 2008 10:35
                                     |
| Probably not. Certainly not by POSIX.  I think we are just listing some types that C99 says are optional.
The only thing that has been bothering me is that we mention intmax_t but not uintmax_t.  I'll go ahead and fix this.
Any other specific types you think we should call out?
                                        Posted by rcs_mgr at Jun 06, 2008 11:42
                                     |
| I have upped the severity to "high" because of this comment and the mention of buffer overflow type attacks in the code samples
                                        Posted by avolkovi at Jun 09, 2008 10:49
                                     |
| Not sure if "pointer" should be set in monospace (as "long" is) in the following: "For example, there are code bases that require pointer and long to have the same size, while other large code bases require int and long to be the same size van de Voort 07."
                                        Posted by erd at Jun 10, 2008 11:49
                                     |
| Should we merge SPARC-64 and ALPHA into the 64-bit Linux column and ARM-32 into IA-32?
                                        Posted by avolkovi at Jun 17, 2008 16:22
                                     |
| The 'rose-na-macros' is meant to emphasize that macro awareness is required to catch the last NCCE (regarding macros). I am scared that a checker for this would flag all multiplication, which is not necessarily the right thing to do.
                                        Posted by svoboda at Jul 17, 2008 09:19
                                     |
| INT05-C pretty much forbids using scanf() to parse ints, so the NCCE/CS pair using fscanf should probably be scrapped.
                                        Posted by svoboda at Oct 03, 2008 15:13
                                     |
| your non-compliant examples only show poor programming technique, and not a shortcoming in the language.
i am not a gun-nut, nor supporter of the nra, etc; but their mantra: "...guns don't kill people (c language), people kill people (poor implementation) really applies with respect to the examples you have provided.
before jumping off a cliff, maybe you should provide some examples that are far more "unavoidable" than the ones you have provided here.
it would really provide some justification for all the effort this project is making (in terms of financial resources, members time, etc).
                                        Posted by etkinsd@battelle.org at Jun 18, 2009 09:22
                                     |
| We are not trying to show shortcomings in the language.  We are trying to identify programming errors that are not necessarily diagnosed by a compiler that can result in software vulnerabilities.  
All errors are avoidable, that is the whole point of this document.
                                        Posted by rcs_mgr at Jun 19, 2009 09:31
                                     |
| As to "Common Data Models" chart,
    'IA-32' or 'IA-64' is the name of an architecture of microprocessors and "64-bit Linux, FreeBSD, NetBSD, and OpenBSD" are the names of operating systems.
    FreeBSD is, for example, supported on IA-32, IA-64, UltraSPARC, and HP/Compaq Alpha systems.
I'm not sure how the very right column of the chart should be interpreted. Maybe the easiest solution is to drop the column?
                                        Posted by masaki at May 10, 2011 04:42
                                     |
| I noticed that as well.
The whole table isn't very useful or interesting (or even correct). For example, IA-64 (which, incidentally, Intel uses to refer the Itanium architecture) can run ILP32 software. Similarly SPARC v9 (there's no such thing as SPARC-64). The sizes of data types are as much a function of the hardware as they are of the operating system and the language and its runtime. So for example, while 64-bit Windows running on IA64 uses the LLP64 data model as indicated in the table, HP-UX or Linux running on the same hardware uses LP64 (making the IA64 column incorrect).
                                        Posted by martinsebor at May 11, 2011 17:20
                                     |
| What do you think about replacing this table with with some interesting examples such as:
    IA-32 bit MSVC
    IA-64 bit MSVC
    IA-32 bit gcc
    IA-64 bit gcc
                                        Posted by rcs_mgr at May 12, 2011 02:57
                                     |
| IA;doesn't make as much sense on Windows as you might think, since that's what they call the Itanium Architecture.  The standard terminology on Windows is Win32 (for 32-bit), x64 (for 64-bit), Itanium, and ARM.  Not exactly the most consistent thing ever.Perhaps we could go with what Wikipedia goes with: http://en.wikipedia.org/wiki/64-bit_computingBut I do agree with Martin that the current models are dangerously wrong for MSVC. 
                                        Posted by aballman at Jun 06, 2013 14:51
                                     |

