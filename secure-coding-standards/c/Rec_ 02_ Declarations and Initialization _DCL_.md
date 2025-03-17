-   Page:
    [DCL00-C. Const-qualify immutable objects](/confluence/display/c/DCL00-C.+Const-qualify+immutable+objects)
-   Page:
    [DCL01-C. Do not reuse variable names in subscopes](/confluence/display/c/DCL01-C.+Do+not+reuse+variable+names+in+subscopes)
-   Page:
    [DCL02-C. Use visually distinct identifiers](/confluence/display/c/DCL02-C.+Use+visually+distinct+identifiers)
-   Page:
    [DCL03-C. Use a static assertion to test the value of a constant expression](/confluence/display/c/DCL03-C.+Use+a+static+assertion+to+test+the+value+of+a+constant+expression)
-   Page:
    [DCL04-C. Do not declare more than one variable per declaration](/confluence/display/c/DCL04-C.+Do+not+declare+more+than+one+variable+per+declaration)
-   Page:
    [DCL05-C. Use typedefs of non-pointer types only](/confluence/display/c/DCL05-C.+Use+typedefs+of+non-pointer+types+only)
-   Page:
    [DCL06-C. Use meaningful symbolic constants to represent literal values](/confluence/display/c/DCL06-C.+Use+meaningful+symbolic+constants+to+represent+literal+values)
-   Page:
    [DCL07-C. Include the appropriate type information in function declarators](/confluence/display/c/DCL07-C.+Include+the+appropriate+type+information+in+function+declarators)
-   Page:
    [DCL08-C. Properly encode relationships in constant definitions](/confluence/display/c/DCL08-C.+Properly+encode+relationships+in+constant+definitions)
-   Page:
    [DCL09-C. Declare functions that return errno with a return type of errno_t](/confluence/display/c/DCL09-C.+Declare+functions+that+return+errno+with+a+return+type+of+errno_t)
-   Page:
    [DCL10-C. Maintain the contract between the writer and caller of variadic functions](/confluence/display/c/DCL10-C.+Maintain+the+contract+between+the+writer+and+caller+of+variadic+functions)
-   Page:
    [DCL11-C. Understand the type issues associated with variadic functions](/confluence/display/c/DCL11-C.+Understand+the+type+issues+associated+with+variadic+functions)
-   Page:
    [DCL12-C. Implement abstract data types using opaque types](/confluence/display/c/DCL12-C.+Implement+abstract+data+types+using+opaque+types)
-   Page:
    [DCL13-C. Declare function parameters that are pointers to values not changed by the function as const](/confluence/display/c/DCL13-C.+Declare+function+parameters+that+are+pointers+to+values+not+changed+by+the+function+as+const)
-   Page:
    [DCL15-C. Declare file-scope objects or functions that do not need external linkage as static](/confluence/display/c/DCL15-C.+Declare+file-scope+objects+or+functions+that+do+not+need+external+linkage+as+static)
-   Page:
    [DCL16-C. Use "L," not "l," to indicate a long value](/confluence/pages/viewpage.action?pageId=87152241)
-   Page:
    [DCL17-C. Beware of miscompiled volatile-qualified variables](/confluence/display/c/DCL17-C.+Beware+of+miscompiled+volatile-qualified+variables)
-   Page:
    [DCL18-C. Do not begin integer constants with 0 when specifying a decimal value](/confluence/display/c/DCL18-C.+Do+not+begin+integer+constants+with+0+when+specifying+a+decimal+value)
-   Page:
    [DCL19-C. Minimize the scope of variables and functions](/confluence/display/c/DCL19-C.+Minimize+the+scope+of+variables+and+functions)
-   Page:
    [DCL20-C. Explicitly specify void when a function accepts no arguments](/confluence/display/c/DCL20-C.+Explicitly+specify+void+when+a+function+accepts+no+arguments)
-   Page:
    [DCL21-C. Understand the storage of compound literals](/confluence/display/c/DCL21-C.+Understand+the+storage+of+compound+literals)
-   Page:
    [DCL22-C. Use volatile for data that cannot be cached](/confluence/display/c/DCL22-C.+Use+volatile+for+data+that+cannot+be+cached)
-   Page:
    [DCL23-C. Guarantee that mutually visible identifiers are unique](/confluence/display/c/DCL23-C.+Guarantee+that+mutually+visible+identifiers+are+unique)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [dcl](https://confluence/label/seccode/dcl) and [recommendation](https://confluence/label/seccode/recommendation).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL00-C | Low | Unlikely | High | P1 | L3 |
| DCL01-C | Low | Unlikely | Medium | P2 | L3 |
| DCL02-C | Low | Unlikely | Medium | P2 | L3 |
| DCL03-C | Low | Unlikely | High | P1 | L3 |
| DCL04-C | Low | Unlikely | Low | P3 | L3 |
| DCL05-C | Low | Unlikely | Medium | P2 | L3 |
| DCL06-C | Low | Unlikely | Medium | P2 | L3 |
| DCL07-C | Low | Unlikely | Low | P3 | L3 |
| DCL08-C | Low | Unlikely | High | P1 | L3 |
| DCL09-C | Low | Unlikely | Low | P3 | L3 |
| DCL10-C | High | Probable | High | P6 | L2 |
| DCL11-C | High | Probable | High | P6 | L2 |
| DCL12-C | Low | Unlikely | High | P1 | L3 |
| DCL13-C | Low | Unlikely | Low | P3 | L3 |
| DCL15-C | Low | Unlikely | Low | P3 | L3 |
| DCL16-C | Low | Unlikely | Low | P3 | L3 |
| DCL17-C | Medium | Probable | High | P4 | L3 |
| DCL18-C | Low | Unlikely | Low | P3 | L3 |
| DCL19-C | Low | Unlikely | Medium | P2 | L3 |
| DCL20-C | Medium | Probable | Low | P12 | L1 |
| DCL21-C | Low | Unlikely | Medium | P2 | L3 |
| DCL22-C | Low | Probable | High | P2 | L3 |
| DCL23-C | Medium | Unlikely | Low | P6 | L2 |

------------------------------------------------------------------------
[](../c/Rec_%2014_%20Concurrency%20_CON_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151929) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152463)
