> [!warning]  
>
> This guideline has been deprecated.  It has been superseded by:
>
> -   [STR07-C. Use the bounds-checking interfaces for remediation of existing string manipulation code](https://www.securecoding.cert.org/confluence/display/seccode/STR07-C.+Use+the+bounds-checking+interfaces+for+remediation+of+existing+string+manipulation+code)
>
> 11/05/2014 -- Version 2.0

When a guideline has been deprecated, it will remain available until the next major release at which point it will be moved to
The managed string library described in *Specifications for Managed Strings* \[[Burch 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Burch06)\] was developed in response to the need for a string library that could improve the quality and security of newly developed C language code while eliminating obstacles to widespread adoption and possible standardization.
The managed string library is based on a dynamic approach in which memory is allocated and reallocated as required. This approach eliminates the possibility of unbounded copies, null-termination errors, and truncation by ensuring adequate space is always available for the resulting string (including the terminating null character).
A runtime-constraint violation occurs when memory cannot be allocated. In this way, the managed string library accomplishes success or failure in a pronounced manner.
The managed string library also provides a mechanism for dealing with data [sanitization](BB.-Definitions_87152273.html#BB.Definitions-sanitize) by (optionally) checking that all characters in a string belong to a predefined set of *safe* characters.
The following code shows how the managed string library can be used to create a managed string and retrieve a null-terminated byte string from the managed string:
``` java
errno_t retValue;
char *cstr;  /* Pointer to null-terminated byte string */
string_mx *str1 = NULL;
retValue = strcreate_m(&str1, "hello, world", 0, NULL);
if (retValue != 0) {
  fprintf(stderr, "Error %d from strcreate_m.\n", retValue);
}
else { /* Retrieve null-terminated byte string and print */
  retValue = getstr_m(&cstr, str1);
  if (retValue != 0) {
    fprintf(stderr, "error %d from getstr_m.\n", retValue);
  }
  printf("(%s)\n", cstr);
  free(cstr); /* Free null-terminated byte string */
  cstr = NULL;
}
```
Note that the calls to `fprintf()` and `printf()` are C Standard functions and not managed string functions.
The technical report ISO/IEC TR 24731-2 \[[ISO/IEC TR 24731-2:2010](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTR24731-2-2010)\] also provides an API that dynamically allocates the results of string functions as needed.
## Risk Assessment
String-handling functions defined in the C Standard, subclause 7.24, and elsewhere are susceptible to common programming errors that can lead to serious, exploitable [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Managed strings, when used properly, can eliminate many of these errors, particularly in new development.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR08-C | High | Probable | High | P6 | L2 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR08-C).
## Bibliography

|  |  |
| ----|----|
| [Burch 2006] | ; |
| [CERT 2006c] | ; |
| [Seacord 2013] | Chapter 2, "Strings" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152413) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](../c/STR09-C_%20Don't%20assume%20numeric%20values%20for%20expressions%20with%20type%20plain%20character)
## Comments:

|  |
| ----|
| Shouldn't this recommendation be labeled "not-for-cpp"?;I would think that std::string would be preferred in C++ code.
                                        Posted by brian.szuter at Oct 31, 2014 07:55
                                     |
| Agreed;– I've added the label; thanks!
                                        Posted by aballman at Oct 31, 2014 10:27
                                     |
| I suppose a C++ analog of this rec would be "dont use C null-terminated byte strings, use std::string instead". If we have this rec, we should hav ethat C++ rec, too.
                                        Posted by svoboda at Oct 31, 2014 16:08
                                     |
| We have;VOID STR01-CPP. Adopt and implement a consistent plan for managing strings, which basically covers that.
                                        Posted by aballman at Oct 31, 2014 16:13
                                     |
| we've really stopped recommending this managed string library in favor of C11 Annex K.; I'm going to deprecate this recommendation.
                                        Posted by rcs_mgr at Nov 05, 2014 09:24
                                     |

