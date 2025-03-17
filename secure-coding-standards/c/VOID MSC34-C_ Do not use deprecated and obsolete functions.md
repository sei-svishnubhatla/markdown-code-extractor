Deprecated and obsolete functions should not be used because there exist equivalent functions that are more secure.  Deprecated functions are defined by the C99 standard and Technical Corrigenda; Obsolete functions are defined by this guideline.
> [!info]  
>
> This page has been labeled [void](https://confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This page has not been erased yet in case it contains information that might still be useful.

## Deprecated Functions
The `gets` function was deprecated by Technical Corrigendum 3.`  gets` fills a buffer with an unbounded string from `stdin` (see [VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array](VOID%20STR35-C_%20Do%20not%20copy%20data%20from%20an%20unbounded%20source%20to%20a%20fixed-length%20array)).  For this reason, `gets` is never safe to use.
## Obsolete Functions
The following functions are obsolete:

|  |  |  |  |  |
| ----|----|----|----|----|
| asctime | bsearch | ctime | fopen | fprintf |
| freopen | fscanf | fwprintf | fwscanf | getenv |
| gets | gmtime | localtime | mbsrtowcs | mbstowcs |
| memcpy | memmove | printf | qsort | rewind |
| setbuf | snprintf | sprintf | sscanf | strcat |
| strcpy | strerror | strncat | strncpy | strtok |
| swprintf | swscanf | tmpfile | tmpnam | vfprintf |
| vfscanf | vfwprintf | vfwscanf | vprintf | vscanf |
| vsnprintf | vsprintf | vsscanf | vswprintf | vswscanf |
| vwprintf | vwscanf | wcrtomb | wcscat | wcscpy |
| wcsncat | wcsncpy | wcsrtombs | wcstok | wcstombs |
| wctomb | wmemcpy | wmemmove | wprintf | wscanf |

Many of the above functions are have been obsolesced by functions defined by \[[ISO/IEC TR 24731-1:2007](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24731-1-2007)\] and \[[ISO/IEC PDTR 24731-2](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECPDTR24731-2-2007)\].
For details on the obsolete string functions, see [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).
See [void FIO07-C. Prefer fseek() to rewind()](void%20FIO07-C_%20Prefer%20fseek__%20to%20rewind__) for details on the `rewind()` function.
See [void FIO12-C. Prefer setvbuf() to setbuf()](void%20FIO12-C_%20Prefer%20setvbuf__%20to%20setbuf__) for details on the `setbuf()` function.
## Risk Assessment
Usage of obsolete functions can lead to to serious, exploitable vulnerabilities. Proper use of TR 24731 functions can eliminate the majority of these issues.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC34-C | high | probable | medium | P12 | L1 |

### Automated Detection
The tool Compass/ROSE can detect violations of this rule.
## References
\[[ISO/IEC 9899:1999](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-1999)\] Section 7.19.9.2, "The `fseek` function"; 7.19.9.5 "The `rewind` function"; and 7.21, "String handling `<string.h>`"  
\[[ISO/IEC PDTR 24772](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECPDTR24772)\] "TRJ Use of Libraries"  
\[[ISO/IEC TR 24731-1:2007](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24731-1-2007)\]  
\[[ISO/IEC PDTR 24731-2](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECPDTR24731-2-2007)\]  
\[[Seacord 05a](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord05a)\] Chapter 2, "Strings"
## Comments:

|  |
| ----|
| I wonder if this rule renders STR07-C. Use TR 24731 for remediation of existing string manipulation code unnecessary?
                                        Posted by svoboda at Jun 11, 2009 14:28
                                     |

