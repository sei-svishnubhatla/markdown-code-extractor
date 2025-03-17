-   Page:
    [MSC00-C. Compile cleanly at high warning levels](/confluence/display/c/MSC00-C.+Compile+cleanly+at+high+warning+levels)
-   Page:
    [MSC01-C. Strive for logical completeness](/confluence/display/c/MSC01-C.+Strive+for+logical+completeness)
-   Page:
    [MSC04-C. Use comments consistently and in a readable fashion](/confluence/display/c/MSC04-C.+Use+comments+consistently+and+in+a+readable+fashion)
-   Page:
    [MSC05-C. Do not manipulate time_t typed values directly](/confluence/display/c/MSC05-C.+Do+not+manipulate+time_t+typed+values+directly)
-   Page:
    [MSC06-C. Beware of compiler optimizations](/confluence/display/c/MSC06-C.+Beware+of+compiler+optimizations)
-   Page:
    [MSC07-C. Detect and remove dead code](/confluence/display/c/MSC07-C.+Detect+and+remove+dead+code)
-   Page:
    [MSC09-C. Character encoding: Use subset of ASCII for safety](/confluence/display/c/MSC09-C.+Character+encoding%3A+Use+subset+of+ASCII+for+safety)
-   Page:
    [MSC10-C. Character encoding: UTF8-related issues](/confluence/display/c/MSC10-C.+Character+encoding%3A+UTF8-related+issues)
-   Page:
    [MSC11-C. Incorporate diagnostic tests using assertions](/confluence/display/c/MSC11-C.+Incorporate+diagnostic+tests+using+assertions)
-   Page:
    [MSC12-C. Detect and remove code that has no effect or is never executed](/confluence/display/c/MSC12-C.+Detect+and+remove+code+that+has+no+effect+or+is+never+executed)
-   Page:
    [MSC13-C. Detect and remove unused values](/confluence/display/c/MSC13-C.+Detect+and+remove+unused+values)
-   Page:
    [MSC14-C. Do not introduce unnecessary platform dependencies](/confluence/display/c/MSC14-C.+Do+not+introduce+unnecessary+platform+dependencies)
-   Page:
    [MSC15-C. Do not depend on undefined behavior](/confluence/display/c/MSC15-C.+Do+not+depend+on+undefined+behavior)
-   Page:
    [MSC17-C. Finish every set of statements associated with a case label with a break statement](/confluence/display/c/MSC17-C.+Finish+every+set+of+statements+associated+with+a+case+label+with+a+break+statement)
-   Page:
    [MSC18-C. Be careful while handling sensitive data, such as passwords, in program code](/confluence/display/c/MSC18-C.+Be+careful+while+handling+sensitive+data%2C+such+as+passwords%2C+in+program+code)
-   Page:
    [MSC19-C. For functions that return an array, prefer returning an empty array over a null value](/confluence/display/c/MSC19-C.+For+functions+that+return+an+array%2C+prefer+returning+an+empty+array+over+a+null+value)
-   Page:
    [MSC20-C. Do not use a switch statement to transfer control into a complex block](/confluence/display/c/MSC20-C.+Do+not+use+a+switch+statement+to+transfer+control+into+a+complex+block)
-   Page:
    [MSC21-C. Use robust loop termination conditions](/confluence/display/c/MSC21-C.+Use+robust+loop+termination+conditions)
-   Page:
    [MSC22-C. Use the setjmp(), longjmp() facility securely](/confluence/display/c/MSC22-C.+Use+the+setjmp%28%29%2C+longjmp%28%29+facility+securely)
-   Page:
    [MSC23-C. Beware of vendor-specific library and language differences](/confluence/display/c/MSC23-C.+Beware+of+vendor-specific+library+and+language+differences)
-   Page:
    [MSC24-C. Do not use deprecated or obsolescent functions](/confluence/display/c/MSC24-C.+Do+not+use+deprecated+or+obsolescent+functions)
-   Page:
    [MSC25-C. Do not use insecure or weak cryptographic algorithms](/confluence/display/c/MSC25-C.+Do+not+use+insecure+or+weak+cryptographic+algorithms)
> [!info]  
>
> **Information for Editors**  
> To have a new guideline automatically listed above be sure to label it [msc](https://confluence/label/seccode/msc) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC00-C | Medium | Probable | Medium | P8 | L2 |
| MSC01-C | Medium | Probable | Medium | P8 | L2 |
| MSC04-C | Medium | Unlikely | Medium |  P4  |  L3  |
| MSC05-C | Low | Unlikely | Medium | P2 | L3 |
| MSC06-C | Medium | Probable | Medium | P8 | L2 |
| MSC07-C | Low | Unlikely | Medium | P2 | L3 |
| MSC09-C | Medium | Unlikely | Medium | P4 | L3 |
| MSC10-C | Medium | Unlikely | High | P2 | L3 |
| MSC11-C | Low | Unlikely | High | P1 | L3 |
| MSC12-C | Low | Unlikely | Medium | P2 | L3 |
| MSC13-C | Low | Unlikely | Medium | P2 | L3 |
| MSC14-C | Low | Unlikely | Medium | P2 | L3 |
| MSC15-C | High | Likely | Medium | P18 | L1 |
| MSC17-C | Medium | Likely | Low | P18 | L1 |
| MSC18-C | Medium | Probable | Medium | P8 | L2 |
| MSC19-C | Low | Unlikely | High | P1 | L3 |
| MSC20-C | Medium | Probable | Medium | P8 | L2 |
| MSC21-C | Low | Unlikely | Low | P3 | L3 |
| MSC22-C | Low | Probable | Medium | P4 | L3 |
| MSC23-C | High | Probable | Medium | P12 | L1 |
| MSC24-C | High | Probable | Medium | P12 | L1 |
| MSC25-C | Medium | Probable | High | P4 | L3 |

------------------------------------------------------------------------
[](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152104)
## Comments:

|  |
| ----|
| Just noticed that MSC23-C is not rated. Can this be rated?
                                        Posted by morano at Jul 12, 2018 11:05
                                     |
| I presume you mean to ask why MSC23-C lacks a Risk Assessment section?While many recommendations do have Risk Assessments, we only require Risk Assessments in our rules, not our recommendations.IMO a risk assessment would not be useful for MSC23-C, as its scope includes any incompatibilities or extensions that a compiler may wish to add to the C language.
                                        Posted by svoboda at Jul 16, 2018 12:57
                                     |
| Only for completeness: Please add MSC23-C also in table "Risk Assessment Summary" since recommendation is rated.;
                                        Posted by volker.erben at Nov 29, 2018 09:05
                                     |

