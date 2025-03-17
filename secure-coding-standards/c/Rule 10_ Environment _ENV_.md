-   Page:
    [ENV30-C. Do not modify the object referenced by the return value of certain functions](/confluence/display/c/ENV30-C.+Do+not+modify+the+object+referenced+by+the+return+value+of+certain+functions)
-   Page:
    [ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it](/confluence/display/c/ENV31-C.+Do+not+rely+on+an+environment+pointer+following+an+operation+that+may+invalidate+it)
-   Page:
    [ENV32-C. All exit handlers must return normally](/confluence/display/c/ENV32-C.+All+exit+handlers+must+return+normally)
-   Page:
    [ENV33-C. Do not call system()](../c/ENV33-C_%20Do%20not%20call%20system__)
-   Page:
    [ENV34-C. Do not store pointers returned by certain functions](/confluence/display/c/ENV34-C.+Do+not+store+pointers+returned+by+certain+functions)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [env](https://confluence/label/seccode/env) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV30-C | Low | Probable | Medium | P4 | L3 |
| ENV31-C | Low | Probable | Medium | P4 | L3 |
| ENV32-C | Medium | Likely | Medium | P12 | L1 |
| ENV33-C | High | Probable | Medium | P12 | L1 |
| ENV34-C | Low | Probable | Medium | P4 | L3 |

## Related Rules and Recommendations

|  |
| ----|
| ENV00-J. Do not sign code that performs only unprivileged operations |
| ENV01-C. Do not make assumptions about the size of an environment variable |
| ENV01-C. Do not make assumptions about the size of an environment variable |
| ENV01-C. Do not make assumptions about the size of an environment variable |
| ENV01-J. Place all security-sensitive code in a single JAR and sign and seal it |
| ENV02-C. Beware of multiple environment variables with the same effective name |
| ENV02-C. Beware of multiple environment variables with the same effective name |
| ENV02-C. Beware of multiple environment variables with the same effective name |
| ENV02-J. Do not trust the values of environment variables |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV03-C. Sanitize the environment when invoking external programs |
| ENV03-J. Do not grant dangerous combinations of permissions |
| ENV04-J. Do not disable bytecode verification |
| ENV05-J. Do not deploy an application that can be remotely monitored |
| ENV06-J. Production code must not contain debugging entry points |
| ENV30-C. Do not modify the object referenced by the return value of certain functions |
| ENV30-C. Do not modify the object referenced by the return value of certain functions |
| ENV30-C. Do not modify the object referenced by the return value of certain functions |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV31-C. Do not rely on an environment pointer following an operation that may invalidate it |
| ENV32-C. All exit handlers must return normally |
| ENV32-C. All exit handlers must return normally |
| ENV32-C. All exit handlers must return normally |
| ENV33-C. Do not call system() |
| ENV33-C. Do not call system() |
| ENV33-C. Do not call system() |
| ENV34-C. Do not store pointers returned by certain functions |
| ENV34-C. Do not store pointers returned by certain functions |
| ENV34-C. Do not store pointers returned by certain functions |
| Rec. 10. Environment (ENV) |
| Rec. 10. Environment (ENV) |
| Rec. 10. Environment (ENV) |
| Rule 10. Environment (ENV) |
| Rule 10. Environment (ENV) |
| Rule 10. Environment (ENV) |
| Rule 16. Runtime Environment (ENV) |
| VOID Do not call the longjmp function to terminate a call to a function registered by atexit() |
| VOID Do not call the longjmp function to terminate a call to a function registered by atexit() |
| VOID Do not call the longjmp function to terminate a call to a function registered by atexit() |
| VOID ENV00-CPP. Beware of multiple environment variables with the same effective name |
| VOID ENV01-CPP. Sanitize the environment when invoking external programs |
| VOID ENV02-CPP. Do not call system() if you do not need a command processor |
| VOID Environment (ENV) |
| VOID Rec. 12. Environment (ENV) |

------------------------------------------------------------------------
[](../c/Rule%2009_%20Input%20Output%20_FIO_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152111)
## Comments:

|  |
| ----|
| Do NOT modify the TZ enviornment as part of a hack to convert date/time from one time zone to another.I spent several days tracking down a bug in a production environment with a multi-threaded application in which conversion between time zones was done by setting the TZ environment variable to one time zone, getting local time, then changing to another time zone to get an ascii string to store the information in a database. Other portions of the code accessed the time functions to find the current time (assumed) local time. Depending on race conditions, this occasionally resulted in incorrect times. This is a published hack that should NOT be used. Use Boost or similar library instead.
                                        Posted by klimasauskas at Jul 13, 2015 12:16
                                     |

