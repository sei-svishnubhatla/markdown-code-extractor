The incorrect use of arrays has traditionally been a source of exploitable [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability). Elements referenced within an array using the subscript operator `[]` are not checked unless the programmer provides adequate bounds checking. As a result, the expression `array [pos] = value` can be used by an attacker to transfer control to arbitrary code.
An attacker who can control the values of both `pos` and `value` in the expression `array [pos] = value` can perform an arbitrary write (which is when the attacker overwrites other storage locations with different content). The consequences range from changing a variable used to determine what permissions the program grants to executing arbitrary code with the permissions of the vulnerable process. Arrays are also a common source of buffer overflows when iterators exceed the bounds of the array.
An array is a series of objects, all of which are the same size and type. Each object in an array is called an *array element*. The entire array is stored contiguously in memory (that is, there are no gaps between elements). Arrays are commonly used to represent a sequence of elements where random access is important but there is little or no need to insert new elements into the sequence (which can be an expensive operation with arrays).
Arrays containing a constant number of elements can be declared as follows:
``` java
enum { ARRAY_SIZE = 12 };
int array[ARRAY_SIZE];
```
These statements allocate storage for an array of 12 integers referenced by `array`. Arrays are indexed from `0..n-1` (where `n` represents an array bound). Arrays can also be declared as follows:
``` java
int array[];
```
This array is called an *incomplete type* because the size is unknown. If an array of unknown size is initialized, its size is determined by the largest indexed element with an explicit initializer. At the end of its initializer list, the array no longer has incomplete type.
``` java
int array[] = { 1, 2 };
```
Although these declarations work fine when the size of the array is known at compile time, it is not possible to declare an array in this fashion when the size can be determined only at runtime. The C Standard adds support for variable length arrays or arrays whose size is determined at runtime. Before the introduction of variable length arrays in C99, however, these "arrays" were typically implemented as pointers to their respective element types allocated using `malloc()`, as shown in this example:
``` java
int *dis = (int *)malloc(ARRAY_SIZE * sizeof(int));
```
Always check that `malloc()` returns a non-null pointer, as per [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors).
It is important to retain any pointer value returned by `malloc()` so that the referenced memory may eventually be deallocated. One possible way to preserve such a value is to use a constant pointer:
``` java
int * const dat = (int * const)malloc(
  ARRAY_SIZE * sizeof(int)
);
/* ... */
free(dat);
```
Below we consider some techniques for array initialization.  Both `dis` and `dat` arrays can be initialized as follows:
``` java
for (i = 0; i < ARRAY_SIZE; i++) {
   dis[i] = 42; /* Assigns 42 to each element of dis */ 
   dat[i] = 42; /* Assigns 42 to each element of dat */
}
```
The `dis` array can also be initialized as follows:
``` java
for (i = 0; i < ARRAY_SIZE; i++) {
   *dis = 42;
   dis++;
}
dis -= ARRAY_SIZE;
```
This technique, however, will not work for `dat`.  The `dat` identifier cannot be incremented (produces a fatal compilation error), as it was declared with type `int * const`.  This problem can be circumvented by copying `dat` into a separate pointer:
``` java
int *p = dat;
for (i = 0; i < ARRAY_SIZE; i++)  {
  *p = 42; /* Assigns 42 to each element */
  p++;
}
```
The variable `p` is declared as a pointer to an integer, initialized with the value stored in `dat`, and then incremented in the loop. This technique can be used to initialize both arrays, and is a better style of programming than incrementing the original pointer to the array (e.g., `dis++`, in the above example), as it avoids having to reset the pointer back to the start of the array after the loop completes. 
Obviously, there is a relationship between array subscripts `[]` and pointers. The expression `dis[i]` is equivalent to `*(dis+i)` for all integral values of `i`. In other words, if `dis` is an array object (equivalently, a pointer to the initial element of an array object) and `i` is an integer, `dis[i]` designates the `i`<sup>th</sup> element of `dis`. In fact, because `*(dis+i)` can be expressed as `*(i+dis)`, the expression `dis[i]` can be represented as `i[dis]`, although doing so is not encouraged. Because array indices are zero-based, the first element is designated as `dis[0]`, or equivalently as `*(dis+0)` or simply `*dis`.
## Risk Assessment
Arrays are a common source of vulnerabilities in C language programs because they are frequently used but not always fully understood.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ARR00-C | High | Probable | High | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | LANG.CAST.ARRAY.TEMP | Array to Pointer Conversion on Temporary Object |
| Klocwork | 2024.4 | ABV.ANY_SIZE_ARRAYABV.GENERAL
ABV.GENERAL.MULTIDIMENSION
ABV.ITERATOR
ABV.MEMBER
ABV.STACK
ABV.TAINTED
ABV.UNICODE.BOUND_MAP
ABV.UNICODE.FAILED_MAP
ABV.UNICODE.NNTS_MAP
ABV.UNICODE.SELF_MAP
ABV.UNKNOWN_SIZE
NNTS.MIGHT
NNTS.MUST
NNTS.TAINTED
SV.STRBO.BOUND_COPY.OVERFLOW
SV.STRBO.BOUND_COPY.UNTERM
SV.STRBO.BOUND_SPRINTF
SV.STRBO.UNBOUND_COPY
SV.STRBO.UNBOUND_SPRINTF
SV.TAINTED.ALLOC_SIZE
SV.TAINTED.CALL.INDEX_ACCESS
SV.TAINTED.CALL.LOOP_BOUND
SV.TAINTED.INDEX_ACCESS
SV.TAINTED.LOOP_BOUND
SV.UNBOUND_STRING_INPUT.CIN
SV.UNBOUND_STRING_INPUT.FUNC |  |
| LDRA tool suite | 9.7.1 | 45 D, 47 S, 489 S, 567 S, 64 X, 66 X, 68 X, 69 X, 70 X, 71 X | Partially implemented |
| PC-lint Plus | 1.4 | 409, 413, 429, 613 | Partially supported: conceptually includes all other ARR items which are mapped to their respective guidelines; explicit mappings for ARR00 are present when a situation mentioned in the guideline itself is encountered |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR00-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C | CTR00-CPP. Understand when to prefer vectors over arrays | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | Prior to 2018-01-12: CERT: |
| CWE 2.11 | CWE-123, Write-what-where Condition | Prior to 2018-01-12: CERT: |
| CWE 2.11 | CWE-125, Out-of-bounds Read | Prior to 2018-01-12: CERT: |
| CWE 2.11 | CWE-129, Unchecked array indexing | Prior to 2018-01-12: CERT: |

------------------------------------------------------------------------
[](../c/Rec_%2006_%20Arrays%20_ARR_) [](../c/Rec_%2006_%20Arrays%20_ARR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152137)
## Comments:

|  |
| ----|
| I think there may be a few issues with some examples on this page:
    Storing the result of the malloc in a constant pointer makes clearing the pointer to NULL impossible.
Does MEM01-C then imply that constants should not be used to hold pointers from malloc() because they will remain dangling (exception is if the free is the last thing before the auto constant goes out of scope)?
Perhaps suggest storing the pointer elsewhere for deallocation would be better.
    Should the ones using malloc should at least note MEM32-C?
    The constant version of dat cannot be initialized by the loop using dat++; The name used in the constant example should be different.
                                        Posted by abrowne at Sep 22, 2010 20:56
                                     |
| 
Storing the result of the malloc in a constant pointer makes clearing the pointer to NULL impossible.
Fixed
Does MEM01-C then imply that constants should not be used to hold pointers from malloc() because they will remain dangling (exception is if the free is the last thing before the auto constant goes out of scope)?
Obviously it can't. Technically, we could add an exception to MEM01-C, but it strikes me as so obvious as to not be worth mentioning 
Perhaps suggest storing the pointer elsewhere for deallocation would be better.
Should the ones using malloc should at least note MEM32-C?
Yes, I've added a note.
The constant version of dat cannot be initialized by the loop using dat++; The name used in the constant example should be different.
Yes it can. dat is a const pointer to a (non-const) array. You can change the integers it points to; you just can't change dat to point elsewhere.
                                        Posted by svoboda at Sep 23, 2010 16:57
                                     |
| In the second last example dat is being changed to point elsewhere by dat++;
I was saying if you use the loop in the second last example to initialize the second example defining dat, then your changing the constant pointer.
It would have been written to go with the first example defining dat, where it is not a constant pointer.
The second example defining dat should use a different name, datc or something, so it can't be confused with that initialization.
                                        Posted by abrowne at Sep 23, 2010 19:26
                                     |
| Whoops, you're right. The concepts are sound, but the varnames used were confusing. Overhauled the varnames; dis is non-const, and dat is const.
                                        Posted by svoboda at Sep 24, 2010 09:35
                                     |
| the last sentence looks broken.
The dat identifier points to the start of the array, so adding zero is inconsequential because *(dat+i) is equivalent to *(dat+0), which is equivalent to *(dat). 
should it be the following?
    The dat identifier points to the start of the array, so adding zero is inconsequential; *(dat+0) is equivalent to *(dat).
                                        Posted by yozo at Aug 12, 2011 07:49
                                     |
| The whole sentence seems redundant because the preceding paragraph already says:
...if dis is an array object [...] and i is an integer [then] dis[i] designates the ith element of dis (counting from zero).
Let me tweak it.
                                        Posted by martinsebor at Aug 14, 2011 14:54
                                     |

