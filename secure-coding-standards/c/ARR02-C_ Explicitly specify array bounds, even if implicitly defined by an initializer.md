The C Standard allows an array variable to be declared both with a bound and with an initialization literal. The initialization literal also implies an array bound in the number of elements specified.
The size implied by an initialization literal is usually specified by the number of elements,
``` java
int array[] = {1, 2, 3}; /* 3-element array */
```
but it is also possible to use designators to initialize array elements in a noncontiguous fashion. Subclause 6.7.9, Example 12, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] states:
> Space can be "allocated" from both ends of an array by using a single designator:
>
> ``` java
> int a[MAX] = {
>   1, 3, 5, 7, 9, [MAX-5] = 8, 6, 4, 2, 0
> };
> ```
>
> In the above, if `MAX` is greater than ten, there will be some zero-valued elements in the middle; if it is less than ten, some of the values provided by the first five initializers will be overridden by the second five.

The C Standard also dictates how array initialization is handled when the number of initialization elements does not equal the explicit array bound. Subclause 6.7.9, paragraphs 21 and 22, state:
> If there are fewer initializers in a brace-enclosed list than there are elements or members of an aggregate, or fewer characters in a string literal used to initialize an array of known size than there are elements in the array, the remainder of the aggregate shall be initialized implicitly the same as objects that have static storage duration.  
> If an array of unknown size is initialized, its size is determined by the largest indexed element with an explicit initializer. The array type is completed at the end of its initializer list.

Although compilers can compute the size of an array on the basis of its initialization list, explicitly specifying the size of the array provides a redundancy check, ensuring that the array's size is correct. It also enables compilers to emit warnings if the array's size is less than the size implied by the initialization.
Note that this recommendation does not apply (in all cases) to character arrays initialized with string literals. See [STR11-C. Do not specify the bound of a character array initialized with a string literal](STR11-C_%20Do%20not%20specify%20the%20bound%20of%20a%20character%20array%20initialized%20with%20a%20string%20literal) for more information.
## Noncompliant Code Example (Incorrect Size)
This noncompliant code example initializes an array of integers using an initialization with too many elements for the array:
``` c
int a[3] = {1, 2, 3, 4};
```
The size of the array `a` is 3, although the size of the initialization is 4. The last element of the initialization (`4`) is ignored. Most compilers will diagnose this error.
### Implementation Details
This noncompliant code example generates a warning in GCC. Microsoft Visual Studio generates a fatal diagnostic: `error C2078: too many initializers`.
## Noncompliant Code Example (Implicit Size)
In this example, the compiler allocates an array of four integer elements and, because an array bound is not explicitly specified by the programmer, sets the array bound to `4`. However, if the initializer changes, the array bound may also change, causing unexpected results.
``` c
int a[] = {1, 2, 3, 4};
```
## Compliant Solution
This compliant solution explicitly specifies the array bound:
``` c
int a[4] = {1, 2, 3, 4};
```
Explicitly specifying the array bound, although it is implicitly defined by an initializer, allows a compiler or other static analysis tool to issue a diagnostic if these values do not agree.
## Exceptions
**ARR02-C-EX1:** [STR11-C. Do not specify the bound of a character array initialized with a string literal](STR11-C_%20Do%20not%20specify%20the%20bound%20of%20a%20character%20array%20initialized%20with%20a%20string%20literal) is a specific exception to this recommendation; it requires that the bound of a character array initialized with a string literal is unspecified.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR02-C | Medium | Unlikely | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | array-size-global | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ARR02 | Fully implemented |
| Compass/ROSE |  |  |  |
| ECLAIR | 1.2 | CC2.ARR02 | Fully implemented |
| Helix QAC | 2024.4 | C0678, C0688, C3674, C3684 |  |
| LDRA tool suite | 9.7.1 | 127 S397 S
404 S | Fully; implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ARR02-a | Explicitly specify array bounds in array declarations with initializers |
| PC-lint Plus | 1.4 | 576 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. ARR02-C | Checks for improper array initialization (rec, partially covered). |
| PVS-Studio | 7.35 | V798 |  |
| RuleChecker | 24.04 | array-size-global | Partially checked |
| SonarQube C/C++ Plugin | 3.11 | S834 |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR02-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | CTR02-CPP. Explicitly specify array bounds, even if implicitly defined by an initializer | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-665, Incorrect or incomplete initialization | Prior to 2018-01-12: CERT: |
| MISRA C:2012 | Rule 8.11 (advisory) | Prior to 2018-01-12: CERT: Unspecified Relationship |
| MISRA C:2012 | Rule 9.5 (required) | Prior to 2018-01-12: CERT: Unspecified Relationship |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.7.9, "Initialization" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152137) [](../c/Rec_%2006_%20Arrays%20_ARR_) [](../c/Rec_%2014_%20Concurrency%20_CON_)
## Comments:

|  |
| ----|
| 
sometype_t varname[] = { .... };
int const varname_ct = sizeof(varname)/sizeof(varname[0]);
// I have trouble seeing why this style would be discouraged, as it seems to be.

![](images/icons/contenttypes/comment_16.png) Posted by bkorb at Aug 01, 2008 17:46
\| \|
This recommendation came out of the safety community. The general notion is that by specifying the bound and the initialization, the compiler can issue a warning if the two sizes disagree, decreasing the changes of an error occurring.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Aug 01, 2008 18:19
\| \|
I also have trouble envisioning the type of an error this recommendation intends to prevent given that C99 doesn't allow initializing an array with more initializers than there are elements. In fact, in my experience, it's the redundancy that this guideline recommends that can lead to problems. For example:
``` java
#define NSTRINGS 5
const char* const a[NSTRINGS] = { "foo", "bar", "baz", "foobar" };
for (size_t i = 0; i != NSTRINGS; ++i)
    puts(a[i]);   /* whoops! undefined behavior when (i == 4) */
```
This type of an error would be avoided if Bruce's approach had been used:
``` java
const char* const a[] = { "foo", "bar", "baz", "foobar" };
const size_t NSTRINGS = sizeof a / sizeof *a;
for (size_t i = 0; i != NSTRINGS; ++i)
    puts(a[i]);
```
In light of this common programming mistake I tend to rather strongly disagree with this recommendation and suggest one to the contrary: i.e., **Avoid explicitly specifying array size in array declarations with initializers.**
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 09, 2010 16:16
\| \|
This rule conflicts with flexible array members.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Jul 08, 2010 19:03
\|
