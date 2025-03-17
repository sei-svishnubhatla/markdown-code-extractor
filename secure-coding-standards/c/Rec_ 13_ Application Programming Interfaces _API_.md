> [!info]  
>
> This section is under construction.

-   Page:
    [API00-C. Functions should validate their parameters](/confluence/display/c/API00-C.+Functions+should+validate+their+parameters)
-   Page:
    [API01-C. Avoid laying out strings in memory directly before sensitive data](/confluence/display/c/API01-C.+Avoid+laying+out+strings+in+memory+directly+before+sensitive+data)
-   Page:
    [API02-C. Functions that read or write to or from an array should take an argument to specify the source or target size](/confluence/display/c/API02-C.+Functions+that+read+or+write+to+or+from+an+array+should+take+an+argument+to+specify+the+source+or+target+size)
-   Page:
    [API03-C. Create consistent interfaces and capabilities across related functions](/confluence/display/c/API03-C.+Create+consistent+interfaces+and+capabilities+across+related+functions)
-   Page:
    [API04-C. Provide a consistent and usable error-checking mechanism](/confluence/display/c/API04-C.+Provide+a+consistent+and+usable+error-checking+mechanism)
-   Page:
    [API05-C. Use conformant array parameters](/confluence/display/c/API05-C.+Use+conformant+array+parameters)
-   Page:
    [API07-C. Enforce type safety](/confluence/display/c/API07-C.+Enforce+type+safety)
-   Page:
    [API09-C. Compatible values should have the same type](/confluence/display/c/API09-C.+Compatible+values+should+have+the+same+type)
-   Page:
    [API10-C. APIs should have security options enabled by default](/confluence/display/c/API10-C.+APIs+should+have+security+options+enabled+by+default)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [api](https://confluence/label/seccode/api) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API00-C | Medium | Unlikely | High | P2 | L3 |
| API01-C | High | Likely | High | P9 | L2 |
| API02-C | High | Likely | High | P9 | L2 |
| API03-C | Medium | Unlikely | Medium | P4 | L3 |
| API04-C | Medium | Unlikely | Medium | P4 | L3 |
| API05-C | High | Probable | Medium | P12 | L1 |
| API07-C | Medium | Unlikely | Medium | P4 | L3 |
| API09-C | Low | Unlikely | High | P1 | L3 |
| API10-C | Medium | Likely | High | P12 | L1 |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152074)
## Comments:

|  |
| ----|
| How does one suggest a new rule? I'd like to suggest API10-C. APIs should have security options enabled by defaultNon-compliant example:Non-compliant
int tls_connect_by_name(const char *host, int port, int option_bitmask);
#define TLS_DEFAULT_OPTIONS 0
#define TLS_VALIDATE_HOST 0x0001
#define TLS_DISABLE_V1_0 0x0002
#define TLS_DISABLE_V1_1 0x0004

If the caller of this API doesn't understand what the options mean, they will pass 0 or TLS_DEFAULT_OPTIONS and get a connection vulnerable to man-in-the-middle attacks and using old versions of TLS.
Compliant example:
**Compliant Example**
``` cpp
int tls_connect_by_name(const char *host, int port, int option_bitmask);
#define TLS_DEFAULT_OPTIONS 0
#define TLS_DISABLE_HOST_VALIDATION 0x0001  // use rarely, subject to man-in-the-middle attack
#define TLS_ENABLE_V1_0 0x0002
#define TLS_ENABLE_V1_1 0x0004
```
If the caller of this API doesn't understand the options and passes 0 or TLS_DEFAULT_OPTIONS they will get certificate validation with only the current version of TLS enabled.
This API design principle can be extended to cover other security properties;– for example, having best practice cipher suites enabled by default (something that changes over time) while disabling out-of-favor cipher suites by default. When interface stability is also a design requirement, an interface can meet both goals by providing off-by-default options that produce stable behavior, such as TLS_ENABLE_Y2015_BEST_PRACTICE_CIPHERS_ONLY.
![](images/icons/contenttypes/comment_16.png) Posted by chris.newman at Jun 04, 2015 13:23
\| \|
seems like a reasonable recommendation; possibly difficult to enforce.; i'll try to add something.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 06, 2015 01:08
\| \|
OK, stubbed out as API02-C. APIs should have security options enabled by default
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Jun 06, 2015 01:23
\| \|
only for completeness: In table "Risk Assessment Summary" the items API02-C, API05-C and API10-C are missing. Please correct.
![](images/icons/contenttypes/comment_16.png) Posted by volker.erben at Nov 29, 2018 08:51
\|
