This page discusses the contents we make available on the [SEI CERT C Coding Standard](SEI%20CERT%20C%20Coding%20Standard). Once we decide a section of this page is ready for publication, it moves to the public [Wiki Contents](Wiki%20Contents) page.
-   [Labels](#WikiContents(Internal)-Labels)
    -   [Structural labels](#WikiContents(Internal)-Structurallabels)
    -   [Chapters](#WikiContents(Internal)-Chapters)
    -   [Internal Use Labels](#WikiContents(Internal)-InternalUseLabels)
    -   [Unknown](#WikiContents(Internal)-Unknown)
        -   [Scripting](#WikiContents(Internal)-Scripting)
        -   [CWE](#WikiContents(Internal)-CWE)
        -   [Review](#WikiContents(Internal)-Review)
        -   [Android](#WikiContents(Internal)-Android)
        -   [Static Analysis Tools](#WikiContents(Internal)-StaticAnalysisTools)
        -   [Exportablity](#WikiContents(Internal)-Exportablity)
        -   [Unknown](#WikiContents(Internal)-Unknown.1)
    -   [Deprecated](#WikiContents(Internal)-Deprecated)
        -   [Rose Labels](#WikiContents(Internal)-RoseLabels)
-   [Guidelines for AD Tool Vendors](#WikiContents(Internal)-GuidelinesforADToolVendors)
    -   [Format for AD Table section](#WikiContents(Internal)-FormatforADTablesection)
-   [How to Deprecate (and Void) Guidelines](#WikiContents(Internal)-HowtoDeprecate(andVoid)Guidelines)
-   [Making a New Guideline](#WikiContents(Internal)-MakingaNewGuideline)
## Labels
These are the labels currently used in the C wiki. The complete list is in [Labels for this Space](Labels%20for%20this%20Space).
### Structural labels
These labels are used to identify front matter, chapters, rules, and guidelines in this space:

| Label | Description | Examples |
| ----|----|----|
| rule | A rule page | ; |
| recommendation | A recommendation page | ; |
| rule-list | A page that lists rules | Rule 01. Preprocessor (PRE) |
| recommendation-list | A page that lists recommendations | Rec. 01. Preprocessor (PRE) |
| section-list | A page that lists sections | 2 Rules |
| wikimain | The main page of a wiki space | ; |
| front-matter | A page in the front matter | ; |
| bm | A page in the back matter | ; |
| not-for-cpp | Used within the coding standards to signify that a guideline does not apply in C++, for instance because the Compliant Solution would not be compliant or will not compile with a conforming C++ compiler. Controls the list of what appears in the C++ coding standard section lists under "rules that also apply in C++". | Rule 10. Concurrency (CON) |

### Chapters
These labels are used to identify the chapters in the wiki space:
-   [api](https://securecoding.cert.org/confluence/label/c/api)
-   [arr](https://securecoding.cert.org/confluence/label/c/arr)
-   [con](https://securecoding.cert.org/confluence/label/c/con)
-   dcl
-   [env](https://securecoding.cert.org/confluence/label/c/env)
-   [err](https://securecoding.cert.org/confluence/label/c/err)
-   [exp](https://securecoding.cert.org/confluence/label/c/exp)
-   [fio](https://securecoding.cert.org/confluence/label/c/fio)
-   [flp](https://securecoding.cert.org/confluence/label/c/flp)
-   [int](https://securecoding.cert.org/confluence/label/c/int)
-   [mem](https://securecoding.cert.org/confluence/label/c/mem)
-   [msc](https://securecoding.cert.org/confluence/label/c/msc)
-   [pos](https://securecoding.cert.org/confluence/label/c/pos)
-   [pre](https://securecoding.cert.org/confluence/label/c/pre)
-   [sig](https://securecoding.cert.org/confluence/label/c/sig)
-   [str](https://securecoding.cert.org/confluence/label/c/str)
-   [win](https://securecoding.cert.org/confluence/label/c/win)
### Internal Use Labels

| Label | Description |
| ----|----|
| ptc | In use by Aaron Ballman. Stands for "Practical to Check" and will be used to label rules with expert opinion on whether the rule should be practical to automatically detect (for some definition of practical). |
| nptc | In use by Aaron Ballman. Stands for "Not Practical to Check" and will be used to label rules with expert opinion on whether the rule is impractical to automatically detect (for instance, relies on programmer intent, etc). |
| nptc-aliasing | In use by Aaron Ballman. Used when a rule is not practical to check because of alias analysis. |
| nptc-thread | In use by Aaron Ballman. Used when a rule is not practical to check because it requires nontrivial threading analysis or dynamic analysis at runtime. |
| nptc-complexity | In use by Aaron Ballman. Used when a rule is not practical to check because the checker would be too complex, reduce compiler performance too much, would require dynamic runtime analysis, etc. |
| nptc-wpa | In use by Aaron Ballman. Used when a rule is not practical to check because it would require Whole Program Analysis, which is not generally plausible for production compilers. |
| nptc-intent | In use by Aaron Ballman. Used when a rule is not practical to check because it relies on programmer intent. |
| review-dms | In use by David Svoboda. Indicates that he has reviewed and approved the page for subsequent publication. |
| review-ajb | In use by Aaron Ballman. Indicates that he has reviewed and approved the page for subsequent publication. |
| review | In use by the Secure Coding team to signify that a guideline is requesting additional review. |
| unedited | In use by the Secure Coding team to signify that a guideline has not had any editing and likely requires some. |
| notes | In use by the Secure Coding team to signify that a guideline has hidden notes associated with it. The notes are in a "Page Properties" macro with the Hidden field set to true (so that the text is not displayed to the user), and this label helps to identify rules that contain such a macro. |

### Unknown
These are labels that we do not understand their usage. Can we deprecate any of these?
#### Scripting
These labels are used in our scraping scripts

| Label | Description |
| ----|----|
| intro | Not sure about this one (Some pages in the front matter seem to have this label?) |
| incomplete | Not sure about this one |
| definition | Not sure about this one |
| void | A voided page |

#### CWE
These labels seem to identify CWEs:
-   [cwe-116](https://securecoding.cert.org/confluence/label/c/cwe-116)
-   [cwe-119](https://securecoding.cert.org/confluence/label/c/cwe-119)
-   [cwe-120](https://securecoding.cert.org/confluence/label/c/cwe-120)
-   [cwe-121](https://securecoding.cert.org/confluence/label/c/cwe-121)
-   [cwe-122](https://securecoding.cert.org/confluence/label/c/cwe-122)
-   [cwe-128](https://securecoding.cert.org/confluence/label/c/cwe-128)
-   [cwe-129](https://securecoding.cert.org/confluence/label/c/cwe-129)
-   [cwe-131](https://securecoding.cert.org/confluence/label/c/cwe-131)
-   [cwe-134](https://securecoding.cert.org/confluence/label/c/cwe-134)
-   [cwe-135](https://securecoding.cert.org/confluence/label/c/cwe-135)
-   [cwe-170](https://securecoding.cert.org/confluence/label/c/cwe-170)
-   [cwe-190](https://securecoding.cert.org/confluence/label/c/cwe-190)
-   [cwe-192](https://securecoding.cert.org/confluence/label/c/cwe-192)
-   [cwe-193](https://securecoding.cert.org/confluence/label/c/cwe-193)
-   [cwe-197](https://securecoding.cert.org/confluence/label/c/cwe-197)
-   [cwe-20](https://securecoding.cert.org/confluence/label/c/cwe-20)
-   [cwe-209](https://securecoding.cert.org/confluence/label/c/cwe-209)
-   [cwe-22](https://securecoding.cert.org/confluence/label/c/cwe-22)
-   [cwe-242](https://securecoding.cert.org/confluence/label/c/cwe-242)
-   [cwe-250](https://securecoding.cert.org/confluence/label/c/cwe-250)
-   [cwe-252](https://securecoding.cert.org/confluence/label/c/cwe-252)
-   [cwe-253](https://securecoding.cert.org/confluence/label/c/cwe-253)
-   [cwe-276](https://securecoding.cert.org/confluence/label/c/cwe-276)
-   [cwe-279](https://securecoding.cert.org/confluence/label/c/cwe-279)
-   [cwe-311](https://securecoding.cert.org/confluence/label/c/cwe-311)
-   [cwe-326](https://securecoding.cert.org/confluence/label/c/cwe-326)
-   [cwe-327](https://securecoding.cert.org/confluence/label/c/cwe-327)
-   [cwe-330](https://securecoding.cert.org/confluence/label/c/cwe-330)
-   [cwe-362](https://securecoding.cert.org/confluence/label/c/cwe-362)
-   [cwe-366](https://securecoding.cert.org/confluence/label/c/cwe-366)
-   [cwe-367](https://securecoding.cert.org/confluence/label/c/cwe-367)
-   [cwe-369](https://securecoding.cert.org/confluence/label/c/cwe-369)
-   [cwe-379](https://securecoding.cert.org/confluence/label/c/cwe-379)
-   [cwe-390](https://securecoding.cert.org/confluence/label/c/cwe-390)
-   [cwe-391](https://securecoding.cert.org/confluence/label/c/cwe-391)
-   [cwe-401](https://securecoding.cert.org/confluence/label/c/cwe-401)
-   [cwe-403](https://securecoding.cert.org/confluence/label/c/cwe-403)
-   [cwe-404](https://securecoding.cert.org/confluence/label/c/cwe-404)
-   [cwe-413](https://securecoding.cert.org/confluence/label/c/cwe-413)
-   [cwe-416](https://securecoding.cert.org/confluence/label/c/cwe-416)
-   [cwe-426](https://securecoding.cert.org/confluence/label/c/cwe-426)
-   [cwe-456](https://securecoding.cert.org/confluence/label/c/cwe-456)
-   [cwe-462](https://securecoding.cert.org/confluence/label/c/cwe-462)
-   [cwe-464](https://securecoding.cert.org/confluence/label/c/cwe-464)
-   [cwe-466](https://securecoding.cert.org/confluence/label/c/cwe-466)
-   [cwe-468](https://securecoding.cert.org/confluence/label/c/cwe-468)
-   [cwe-469](https://securecoding.cert.org/confluence/label/c/cwe-469)
-   [cwe-476](https://securecoding.cert.org/confluence/label/c/cwe-476)
-   [cwe-479](https://securecoding.cert.org/confluence/label/c/cwe-479)
-   [cwe-480](https://securecoding.cert.org/confluence/label/c/cwe-480)
-   [cwe-567](https://securecoding.cert.org/confluence/label/c/cwe-567)
-   [cwe-587](https://securecoding.cert.org/confluence/label/c/cwe-587)
-   [cwe-59](https://securecoding.cert.org/confluence/label/c/cwe-59)
-   [cwe-606](https://securecoding.cert.org/confluence/label/c/cwe-606)
-   [cwe-628](https://securecoding.cert.org/confluence/label/c/cwe-628)
-   [cwe-665](https://securecoding.cert.org/confluence/label/c/cwe-665)
-   [cwe-667](https://securecoding.cert.org/confluence/label/c/cwe-667)
-   [cwe-675](https://securecoding.cert.org/confluence/label/c/cwe-675)
-   [cwe-676](https://securecoding.cert.org/confluence/label/c/cwe-676)
-   [cwe-681](https://securecoding.cert.org/confluence/label/c/cwe-681)
-   [cwe-682](https://securecoding.cert.org/confluence/label/c/cwe-682)
-   [cwe-686](https://securecoding.cert.org/confluence/label/c/cwe-686)
-   [cwe-697](https://securecoding.cert.org/confluence/label/c/cwe-697)
-   [cwe-704](https://securecoding.cert.org/confluence/label/c/cwe-704)
-   [cwe-705](https://securecoding.cert.org/confluence/label/c/cwe-705)
-   [cwe-707](https://securecoding.cert.org/confluence/label/c/cwe-707)
-   [cwe-73](https://securecoding.cert.org/confluence/label/c/cwe-73)
-   [cwe-732](https://securecoding.cert.org/confluence/label/c/cwe-732)
-   [cwe-754](https://securecoding.cert.org/confluence/label/c/cwe-754)
-   [cwe-764](https://securecoding.cert.org/confluence/label/c/cwe-764)
-   [cwe-768](https://securecoding.cert.org/confluence/label/c/cwe-768)
-   [cwe-770](https://securecoding.cert.org/confluence/label/c/cwe-770)
-   [cwe-78](https://securecoding.cert.org/confluence/label/c/cwe-78)
-   [cwe-788](https://securecoding.cert.org/confluence/label/c/cwe-788)
-   [cwe-798](https://securecoding.cert.org/confluence/label/c/cwe-798)
-   [cwe-805](https://securecoding.cert.org/confluence/label/c/cwe-805)
-   [cwe-807](https://securecoding.cert.org/confluence/label/c/cwe-807)
-   [cwe-88](https://securecoding.cert.org/confluence/label/c/cwe-88)
#### Review
These labels were used to review rules in the past:
-   [review-jb](https://securecoding.cert.org/confluence/label/c/review-jb)
-   [review-rcs](https://securecoding.cert.org/confluence/label/c/review-rcs)
#### Android
These labels apply to Android:
-   [android-applicable](https://securecoding.cert.org/confluence/label/c/android-applicable)
-   [android-inapplicable](https://securecoding.cert.org/confluence/label/c/android-inapplicable)
-   [android-unknown](https://securecoding.cert.org/confluence/label/c/android-unknown)
#### Static Analysis Tools
These labels are associated with static analysis tools (besides Rosecheckers)
-   [compass/rose](https://securecoding.cert.org/confluence/labels/viewlabel.action?ids=48726022&key=c)
-   [coverity](https://securecoding.cert.org/confluence/label/c/coverity)
-   [edg](https://securecoding.cert.org/confluence/label/c/edg)
-   [fortify](https://securecoding.cert.org/confluence/label/c/fortify)
-   [gcc](https://securecoding.cert.org/confluence/label/c/gcc)
-   [klocwork](https://securecoding.cert.org/confluence/label/c/klocwork)
-   [ldra](https://securecoding.cert.org/confluence/label/c/ldra)
-   [splint](https://securecoding.cert.org/confluence/label/c/splint)
#### Exportablity
These labels indicate rules that may or may not be applicable to other languages:
-   [exportable-c++](https://securecoding.cert.org/confluence/labels/viewlabel.action?ids=19922949&key=c)
-   [exportable-java](https://securecoding.cert.org/confluence/label/c/exportable-java)
-   [update-c++](https://securecoding.cert.org/confluence/labels/viewlabel.action?ids=23592961&key=c)
-   [update-checker](https://securecoding.cert.org/confluence/label/c/update-checker)
#### Unknown
The purpose for these labels is currently unknown:
1.  A-B
    -   [admin](https://securecoding.cert.org/confluence/label/c/admin)
    -   [analyzer](https://securecoding.cert.org/confluence/label/c/analyzer)
    -   [arithmetic](https://securecoding.cert.org/confluence/label/c/arithmetic)
    -   [array](https://securecoding.cert.org/confluence/label/c/array)
    -   [asynchronous](https://securecoding.cert.org/confluence/label/c/asynchronous)
2.  C
    -   [c11](https://securecoding.cert.org/confluence/label/c/c11)
    -   [char-strings](https://securecoding.cert.org/confluence/label/c/char-strings)
    -   [character](https://securecoding.cert.org/confluence/label/c/character)
    -   [code-defect](https://securecoding.cert.org/confluence/label/c/code-defect)
    -   [comparison](https://securecoding.cert.org/confluence/label/c/comparison)
    -   [compliance](https://securecoding.cert.org/confluence/label/c/compliance)
    -   [concurrency](https://securecoding.cert.org/confluence/label/c/concurrency)
    -   [constant](https://securecoding.cert.org/confluence/label/c/constant)
    -   [conversion](https://securecoding.cert.org/confluence/label/c/conversion)
    -   [cost](https://securecoding.cert.org/confluence/label/c/cost)
    -   [crypto](https://securecoding.cert.org/confluence/label/c/crypto)
3.  D-E
    -   [declar-init](https://securecoding.cert.org/confluence/label/c/declar-init)
    -   [deprecated](https://securecoding.cert.org/confluence/label/c/deprecated)
    -   [ear](https://securecoding.cert.org/confluence/label/c/ear)
    -   [enum](https://securecoding.cert.org/confluence/label/c/enum)
    -   [error-handling](https://securecoding.cert.org/confluence/label/c/error-handling)
    -   [exceptions](https://securecoding.cert.org/confluence/label/c/exceptions)
    -   [expressions](https://securecoding.cert.org/confluence/label/c/expressions)
4.  F-H
    -   [file](https://securecoding.cert.org/confluence/label/c/file)
    -   [filename](https://securecoding.cert.org/confluence/label/c/filename)
    -   [first_metadata_test](https://securecoding.cert.org/confluence/label/c/first_metadata_test)
    -   [floating-point](https://securecoding.cert.org/confluence/label/c/floating-point)
    -   [front-matter-section](https://securecoding.cert.org/confluence/label/c/front-matter-section)
    -   [general](https://securecoding.cert.org/confluence/label/c/general)
    -   [hand-coded](https://securecoding.cert.org/confluence/label/c/hand-coded)
5.  I-N
    -   [input](https://securecoding.cert.org/confluence/label/c/input)
    -   [integer](https://securecoding.cert.org/confluence/label/c/integer)
    -   [intro](https://securecoding.cert.org/confluence/label/c/intro)
    -   [library](https://securecoding.cert.org/confluence/label/c/library)
    -   [likelihood](https://securecoding.cert.org/confluence/label/c/likelihood)
    -   [memory-management](https://securecoding.cert.org/confluence/label/c/memory-management)
    -   [my_first_metadata_test](https://securecoding.cert.org/confluence/label/c/my_first_metadata_test)
    -   [no-autodetect](https://securecoding.cert.org/confluence/label/c/no-autodetect)
    -   [not-in-book](https://securecoding.cert.org/confluence/label/c/not-in-book)
6.  O-Q
    -   [opening-files](https://securecoding.cert.org/confluence/label/c/opening-files)
    -   [order-of-op](https://securecoding.cert.org/confluence/label/c/order-of-op)
    -   [os-specific](https://securecoding.cert.org/confluence/label/c/os-specific)
    -   [overflow](https://securecoding.cert.org/confluence/label/c/overflow)
    -   [padding](https://securecoding.cert.org/confluence/label/c/padding)
    -   [permissions](https://securecoding.cert.org/confluence/label/c/permissions)
    -   [portability](https://securecoding.cert.org/confluence/label/c/portability)
    -   [posix](https://securecoding.cert.org/confluence/label/c/posix)
    -   [pre-risk](https://securecoding.cert.org/confluence/label/c/pre-risk)
    -   [preprocessor](https://securecoding.cert.org/confluence/label/c/preprocessor)
    -   [priority](https://securecoding.cert.org/confluence/label/c/priority)
    -   [privileges](https://securecoding.cert.org/confluence/label/c/privileges)
7.  R
    -   [race-condition](https://securecoding.cert.org/confluence/label/c/race-condition)
    -   [remediation](https://securecoding.cert.org/confluence/label/c/remediation)
8.  S-T
    -   [s](https://securecoding.cert.org/confluence/label/c/s)
    -   [sample](https://securecoding.cert.org/confluence/label/c/sample)
    -   [section](https://securecoding.cert.org/confluence/label/c/section)
    -   [severity](https://securecoding.cert.org/confluence/label/c/severity)
    -   [sidebar](https://securecoding.cert.org/confluence/label/c/sidebar)
    -   [signal](https://securecoding.cert.org/confluence/label/c/signal)
    -   [style](https://securecoding.cert.org/confluence/label/c/style)
    -   [tempfile](https://securecoding.cert.org/confluence/label/c/tempfile)
    -   [tr24731](https://securecoding.cert.org/confluence/label/c/tr24731)
9.  U-Z
    -   [unlikely](https://securecoding.cert.org/confluence/label/c/unlikely)
    -   [usage](https://securecoding.cert.org/confluence/label/c/usage)
    -   [windows](https://securecoding.cert.org/confluence/label/c/windows)
### Deprecated
These labels can be eliminated:
#### Rose Labels
These labels indicate the capability for Rosecheckers to enforce the rule:
-   [rose](https://securecoding.cert.org/confluence/label/c/rose)
-   [rose-complete](https://securecoding.cert.org/confluence/label/c/rose-complete)
-   [rose-false-positive](https://securecoding.cert.org/confluence/label/c/rose-false-positive)
-   [rose-gcc](https://securecoding.cert.org/confluence/label/c/rose-gcc)
-   [rose-na-macros](https://securecoding.cert.org/confluence/label/c/rose-na-macros)
-   [rose-na-multiple-files](https://securecoding.cert.org/confluence/label/c/rose-na-multiple-files)
-   [rose-nonapplicable](https://securecoding.cert.org/confluence/label/c/rose-nonapplicable)
-   [rose-partial](https://securecoding.cert.org/confluence/label/c/rose-partial)
-   [rose-possible](https://securecoding.cert.org/confluence/label/c/rose-possible)
-   [unenforceable](https://securecoding.cert.org/confluence/label/c/unenforceable)
## Guidelines for AD Tool Vendors
...
### Format for AD Table section
...
## How to Deprecate (and Void) Guidelines
In the event a guideline becomes obsolete, it is clearly marked as deprecated at the top of the guideline, and the label "deprecated" is added to the page. If the guideline has been superseded, the superseding guidelines are listed in the deprecation message. Additionally, the date of deprecation and current publication cycle are displayed in the deprecation message. The deprecation message should use the format in the following example (if it has not been superseded by another guideline, some text will look different):
> [!warning]  
>
> This guideline has been deprecated. It has been superseded by:
>
> -   [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules)
>
> 07/01/2013 -- Version 1.0

When a guideline is deprecated, it remains available until the next major release, at which point it is moved to the VOID section. This allows the community and tool vendors time to react to the changing guidelines in the Wiki.
When moving a guideline to the VOID section,
-   Add the void label
-   Prefix the title with "VOID", but keep the SEI CERT guideline ID and the rest of the original title. (E.g., new title becomes "VOID INT02-C. Understand integer conversion rules")
-   If a guideline ID (e.g., "INT02-C" in the example above) has previously already been voided, add the number of the latest voiding after the word "VOID" in the title. (E.g., for the third voiding, new title becomes "VOID #3 INT02-C. Understand integer conversion rules")
Use the Move command, which is available at the top right of the page in the Page View mode. Revise the 'Deprecated' note so it instead says 'Void', and add the date the rule became void. For example:
> [!warning]  
>
> This guideline has been voided. It has been superseded by:
>
> -   [INT02-C. Understand integer conversion rules](INT02-C_%20Understand%20integer%20conversion%20rules)
>
> Date deprecated: 07/01/2013 -- Version 1.0
>
> Date voided: 05/01/2014

 Deprecated or voided guideline IDs should not be re-used for a different guideline. 
## Making a New Guideline
 Deprecated or voided guideline IDs should not be re-used for a different guideline.
