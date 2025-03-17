All integer values originating from [tainted sources](BB.-Definitions_87152273.html#BB.Definitions-taintedsource) should be evaluated to determine if they have identifiable upper and lower bounds. If so, these limits should be enforced by the interface. Restricting the input of excessively large or small integers helps prevent overflow, truncation, and other type range errors. Furthermore, it is easier to find and correct input problems than it is to trace internal errors back to faulty inputs.
## Noncompliant Code Example
In this noncompliant code example, `length` is the value of a user-defined (and thus potentially untrusted) environment variable whose value is used to determine the size of a dynamically allocated array, `table`. In compliance with [INT30-C. Ensure that unsigned integer operations do not wrap](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap), the code prevents [unsigned integer wrapping](http://BB.%20Definitions#unsigned%20integer%20wrapping) but does not impose any upper bound on the size of the array, making it possible for the user to cause the program to use an excessive amount of memory.
``` c
char** create_table(void) {
  const char* const lenstr = getenv("TABLE_SIZE");
  const size_t length = lenstr ? strtoul(lenstr, NULL, 10) : 0;
  if (length > SIZE_MAX / sizeof(char *))
    return NULL;   /* Indicate error to caller */
  const size_t table_size = length * sizeof(char *);
  char** const table = (char **)malloc(table_size);
  if (table == NULL)
    return NULL;   /* Indicate error to caller */
  /* Initialize table... */
  return table;
}
```
Because `length` is user controlled, the value can result in a large block of memory being allocated or can cause the call to `malloc()` to fail. Depending on how error handling is implemented, it may result in a [denial-of-service attack](http://BB.%20Definitions#denial-of-service%20attack) or other error.
## Compliant Solution
This compliant solution defines the acceptable range for `length` as `[1, MAX_TABLE_LENGTH]`. The `length` parameter is declared as `size_t`, which is unsigned by definition. Consequently, it is not necessary to check `length` for negative values (see [INT01-C. Use rsize_t or size_t for all integer values representing the size of an object](INT01-C_%20Use%20rsize_t%20or%20size_t%20for%20all%20integer%20values%20representing%20the%20size%20of%20an%20object)).
``` c
enum { MAX_TABLE_LENGTH = 256 };
char** create_table(void) {
  const char* const lenstr = getenv("TABLE_SIZE");
  const size_t length = lenstr ? strtoul(lenstr, NULL, 10) : 0;
  if (length == 0 || length > MAX_TABLE_LENGTH)
    return NULL;   /* Indicate error to caller */
  const size_t table_size = length * sizeof(char *);
  char** const table = (char **)malloc(table_size);
  if (table == NULL)
    return NULL;   /* Indicate error to caller */
  /* Initialize table... */
  return table;
}
```
The test for `length == 0` ensures that a nonzero number of bytes is allocated. (See [MEM04-C. Beware of zero-length allocations](MEM04-C_%20Beware%20of%20zero-length%20allocations).)
## Noncompliant Code Example
In this noncompliant example, the tainted integer `color_index` is used in pointer arithmetic to index into the array table:
``` c
const char *table[] = { "black", "white", "blue", "green" };
const char *set_background_color(void) {
  int color_index;
  GET_TAINTED_INTEGER(int, color_index);
  const char *color = table[color_index];  /* Violation */
  /* ... */
  return color;
} 
```
## Compliant Solution
This compliant solution defines the acceptable range for `color_index` as `[1, MAX_COLOR_INDEX]`:
``` c
enum { MAX_COLOR_INDEX = 3 };
const char *table[] = { "black", "white", "blue", "green" };
const char *set_background_color(void) {
  int color_index;
  GET_TAINTED_INTEGER(int, color_index);
  if (color_index < 0 || colo_index > MAX_COLOR_INDEX)
    return NULL;   /* Indicate error to caller */ 
  const char *color = table[color_index]; 
  /* ... */
  return color;
}
```
## Noncompliant Code Example (Heartbleed)
CERT vulnerability [720951](http://www.kb.cert.org/vuls/id/720951) describes a vulnerability in OpenSSL versions 1.0.1 through 1.0.1f, popularly known as "Heartbleed." This vulnerability allows an attacker to steal information that under normal conditions would be protected by Secure Socket Layer/Transport Layer Security (SSL/TLS) encryption.
Despite the seriousness of the vulnerability, Heartbleed is the result of a common programming error and an apparent lack of awareness of secure coding principles. Following is the vulnerable code:
``` c
int dtls1_process_heartbeat(SSL *s) {          
  unsigned char *p = &s->s3->rrec.data[0], *pl;
  unsigned short hbtype;
  unsigned int payload;
  unsigned int padding = 16; /* Use minimum padding */
  /* Read type and payload length first */
  hbtype = *p++;
  n2s(p, payload);
  pl = p;
  /* ... More code ... */
  if (hbtype == TLS1_HB_REQUEST) {
    unsigned char *buffer, *bp;
    int r;
    /* Allocate memory for the response, size is 1 byte
     * message type, plus 2 bytes payload length, plus
     * payload, plus padding
     */
    buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    bp = buffer;
    /* Enter response type, length and copy payload */
    *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);
    memcpy(bp, pl, payload);
    /* ... More code ... */
  }
  /* ... More code ... */
}
```
This code processes a "heartbeat" packet from a client. As specified in [RFC 6520](https://tools.ietf.org/html/rfc6520), when the program receives a heartbeat packet, it must echo the packet's data back to the client. In addition to the data, the packet contains a length field that conventionally indicates the number of bytes in the packet data, but there is nothing to prevent a malicious packet from lying about its data length.
The `p` pointer, along with `payload` and `p1`, contain data from a packet. The code allocates a `buffer` sufficient to contain `payload` bytes, with some overhead, then copies `payload` bytes starting at `p1` into this buffer and sends it to the client. Notably absent from this code are any checks that the payload integer variable extracted from the heartbeat packet corresponds to the size of the packet data. Because the client can specify an arbitrary value of `payload`, an attacker can cause the server to read and return the contents of memory beyond the end of the packet data, which violates [INT04-C. Enforce limits on integer values originating from tainted sources](https://www.securecoding.cert.org/confluence/display/seccode/INT04-C.+Enforce+limits+on+integer+values+originating+from+tainted+sources). The resulting call to `memcpy()` can then copy the contents of memory past the end of the packet data and the packet itself, potentially exposing sensitive data to the attacker. This call to `memcpy()` violates [ARR38-C. Guarantee that library functions do not form invalid pointers](https://www.securecoding.cert.org/confluence/display/seccode/ARR38-C.+Guarantee+that+library+functions+do+not+form+invalid+pointers). A version of ARR38-C also appears in [ISO/IEC TS 17961:2013](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IECTS17961), "Forming invalid pointers by library functions \[libptr\]." This rule would require a conforming analyzer to diagnose the Heartbleed vulnerability.
## Compliant Solution (Heartbleed)
OpenSSL version 1.0.1g contains the following patch, which guarantees that payload is within a valid range. The range is limited by the size of the input record.
``` c
int dtls1_process_heartbeat(SSL *s) {          
  unsigned char *p = &s->s3->rrec.data[0], *pl;
  unsigned short hbtype;
  unsigned int payload;
  unsigned int padding = 16; /* Use minimum padding */
  /* ... More code ... */
  /* Read type and payload length first */
  if (1 + 2 + 16 > s->s3->rrec.length)
    return 0; /* silently discard */
  hbtype = *p++;
  n2s(p, payload);
  if (1 + 2 + payload + 16 > s->s3->rrec.length)
    return 0; /* silently discard per RFC 6520 */
  pl = p;
  /* ... More code ... */
  if (hbtype == TLS1_HB_REQUEST) {
    unsigned char *buffer, *bp;
    int r;
    /* Allocate memory for the response, size is 1 byte
     * message type, plus 2 bytes payload length, plus
     * payload, plus padding
     */
    buffer = OPENSSL_malloc(1 + 2 + payload + padding);
    bp = buffer;
    /* Enter response type, length and copy payload */
    *bp++ = TLS1_HB_RESPONSE;
    s2n(payload, bp);
    memcpy(bp, pl, payload);
    /* ... More code ... */
  }
  /* ... More code ... */
}
```
## Risk Assessment
Failing to enforce the limits on integer values can result in a denial-of-service attack, unauthorized disclosure of information, or to run arbitrary code.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT04-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported by taint analysis |
| CodeSonar | 8.3p0 | IO.TAINT.SIZELANG.MEM.TBA
IO.TAINT.ADDR
IO.UT.HOST
IO.UT.PORT
(general) | Tainted allocation sizeTainted buffer access
Tainted network address
Untrusted Network Host
Untrusted Network PortCodeSonar will track the tainted value, along with any limits applied to it, and flag any problems caused by underconstraint. Warnings of a wide range of classes may be triggered, including tainted allocation size, buffer overrun, and division by zero |
| Helix QAC | 2024.4 | DF2794, DF2804, DF2854, DF2859, DF2864, DF2894, DF2899, DF2904, DF2909, DF2914, DF2924, DF2944, DF2949, DF2954, DF2956, DF2959 |  |
| Klocwork | 2024.4 | SV.TAINTED.ALLOC_SIZESV.TAINTED.BINOP
SV.TAINTED.CALL.BINOP
SV.TAINTED.CALL.INDEX_ACCESS
SV.TAINTED.CALL.LOOP_BOUND
SV.TAINTED.INDEX_ACCESS
SV.TAINTED.LOOP_BOUND |  |
| Parasoft C/C++test | 2024.2 | CERT_C-INT04-aCERT_C-INT04-b
CERT_C-INT04-c | Avoid potential integer overflow/underflow on tainted dataAvoid buffer read overflow from tainted data
Avoid buffer write overflow from tainted data |
| Polyspace Bug Finder | R2024a | CERT C: Rec. INT04-C | Checks for:Array access with tainted indexLoop bounded with tainted valueMemory allocation with tainted sizeTainted size of variable length arrayRec. partially supported. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT04-C).
Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT04-CPP. Enforce limits on integer values originating from untrusted sources |
| ISO/IEC TS 17961:2013 | Forming invalid pointers by library functions [libptr]Tainted, potentially mutilated, or out-of-domain integer values are used in a restricted sink [taintsink] |

## Bibliography

|  |  |
| ----|----|
| [Seacord 2013] | Chapter 5, "Integer Security" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152206) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152392)
## Comments:

|  |
| ----|
| Just because the original code could divide by zero is not justification from outlawing a 0-length table.; (Note it should be "length", not "size".)  Many lists in the real world are of zero length.  The compliant solution rearranged the test in a way that would avoid dividing by zero anyway.
                                        Posted by dagwyn at Apr 15, 2008 16:04
                                     |
| Compass/ROSE could easily catch violations of this rule by insisting that any function parameter involved in arithmetic, that isn't already bounds-checked, is a violation. This blithely assumes that any function parameter contains user-defined 'potentially unsafe' values, which is not a safe assumption....we need a more enforceable definition of 'potentially unsafe' value, eg. a value that comes from argv[], or from the scanf() family.
                                        Posted by svoboda at Jul 17, 2008 09:25
                                     |
| A more narrow scope of the problem of enforcing this rule would be to examine any untrusted values that are involved with allocating memory, which is what the NCCE/CS illustrate. A function argument that is involved in a call to malloc() (usually by being multiplied by a size value), must be checked:
    to be nonzero
    to be less than a compile-time constant
    The compile-time constant should, practically speaking, be far less than SIZE_MAX.
                                        Posted by svoboda at Aug 06, 2008 15:27
                                     |
| I think this rule is unenforceable:
All integer values originating from untrusted sources should be evaluated to determine if there are identifiable upper and lower bounds. If so, these limits should be enforced by the interface.
There is no good way for an analysis tool to determine if values originating from untrusted sources have identifiable upper and lower bounds.
                                        Posted by rcs at Feb 09, 2009 12:44
                                     |
| True, but it's easy for an analysis tool to check that a program is enforcing upper/lower bounds on an untrusted value. Hence the 'rose-possible' tag + my earlier comments.
                                        Posted by svoboda at Feb 09, 2009 14:04
                                     |
| The non-compliant code seems to have a bug on the line
if (sizeof(char *) > SIZE_MAX/length) {
It seems it should be
if (length > SIZE_MAX/sizeof(char *)) {
                                        Posted by sgreen at Aug 21, 2009 18:29
                                     |
| OK, I made this change
                                        Posted by rcs_mgr at Aug 21, 2009 20:29
                                     |
| If you are going to use the GET_TAINTED_INTEGER() function like macro you should provide the definition.
                                        Posted by rcs at Feb 05, 2013 13:31
                                     |

