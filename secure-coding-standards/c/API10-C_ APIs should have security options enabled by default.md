APIS should have security options enabled by default– for example, having best practice cipher suites enabled by default (something that changes over time) while disabling out-of-favor cipher suites by default. When interface stability is also a design requirement, an interface can meet both goals by providing off-by-default options that produce stable behavior, such as `TLS_ENABLE_Y2015_BEST_PRACTICE_CIPHERS_ONLY`.
## Noncompliant Code Example
If the caller of this API in this noncompliant example doesn't understand what the options mean, they will pass 0 or `TLS_DEFAULT_OPTIONS` and get a connection vulnerable to man-in-the-middle attacks and using old versions of TLS.
``` c
int tls_connect_by_name(const char *host, int port, int option_bitmask);
#define TLS_DEFAULT_OPTIONS 0
#define TLS_VALIDATE_HOST 0x0001
#define TLS_DISABLE_V1_0 0x0002
#define TLS_DISABLE_V1_1 0x0004
```
## Compliant Solution
If the caller of this API doesn't understand the options and passes 0 or `TLS_DEFAULT_OPTIONS` they will get certificate validation with only the current version of TLS enabled.
``` c
int tls_connect_by_name(const char *host, int port, int option_bitmask);
#define TLS_DEFAULT_OPTIONS 0
#define TLS_DISABLE_HOST_VALIDATION 0x0001  // use rarely, subject to man-in-the-middle attack
#define TLS_ENABLE_V1_0 0x0002
#define TLS_ENABLE_V1_1 0x0004
```
## Risk Assessment

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API10-C | Medium | Likely | High | P12 | L1 |

##  Related Guidelines

|  |  |
| ----|----|
|  |  |

## Bibliography

|  |  |
| ----|----|
|  |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152226) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](../c/Rec_%2006_%20Arrays%20_ARR_)
## Comments:

|  |
| ----|
| Reference for bibliography:;http://www.cs.utexas.edu/~shmat/shmat_ccs12.pdf(related news article: http://www.infoq.com/news/2012/10/ssl-vulnerabilities}
                                        Posted by chris.newman at Jun 08, 2015 03:07
                                     |

