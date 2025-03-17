> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [EXP39-C. Do not access a variable through a pointer of an incompatible type](EXP39-C_%20Do%20not%20access%20a%20variable%20through%20a%20pointer%20of%20an%20incompatible%20type)

According to the C standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\], Section 7.22.3.5, calling `realloc(ptr, size)`
> deallocates the old object pointed to by `ptr` and returns a pointer to a new object that has the size specified by `size`. The contents of the new object shall be the same as that of the old object prior to deallocation, up to the lesser of the new and old sizes. Any bytes in the new object beyond the size of the old object have indeterminate values.

## Noncompliant Code Example
This noncompliant code example uses `realloc()` to allocate storage for an object of one type but initializes it as if it were an object of a different type:
``` c
#include <stdlib.h>
typedef struct gadget gadget;
struct gadget {
  int i;
  double d;
  char *p;
};
typedef struct widget widget;
struct widget {
  char *q;
  int j;
  double e;
};
gadget *gp;
widget *wp;
/* ... */
wp = (widget *)realloc(gp, sizeof(widget));
```
Here, the `realloc()` call allocates storage for a `widget`, but it initializes that `widget` as if it were a `gadget`. At best, this would effectively produce silent conversions from `char *` to `int` or from `int` to `char *`. Even worse, it could initialize a `double` with bits copied from a pointer.
## Compliant Solution
A program should use `realloc()` only to resize dynamically allocated arrays. It could reallocate an array as another array with elements of the same type but with a greater or lesser dimension, as in this compliant solution:
``` c
#include <stdlib.h>
typedef struct widget widget;
struct widget {
  char *q;
  int j;
  double e;
};
widget *wp;
widget *wq;
/* ... */
wp = (widget *)malloc(10 * sizeof(widget));
/* ... */
wq = (widget *)realloc(wp, 20 * sizeof(widget));
/* ... */
wp = (widget *)realloc(wq, 15 * sizeof(widget));
```
The program calls `malloc()` to allocate storage for an array of 10 widgets. Later, it calls `realloc()` to resize that array as an array of 20 widgets. Even later, it calls `realloc()` again, this time to shrink the array to only 15 widgets.
## Risk Assessment
Resizing storage for objects other than dynamically allocated arrays may result in silently converting data to an incompatible type.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM08-C | high | likely | medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this recommendation by ensuring that the type of the pointer argument to realloc() matches the type in the cast |
| ECLAIR | 1.2 | CC2.MEM08 | Can detect violations of this recommendation by ensuring that the type of the pointer argument to realloc() matches the type in the cast |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM08-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Type-breaking Reinterpretation of Data [AMV] |
| MITRE CWE | CWE-628, Function call with incorrectly specified arguments |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.22.3.5, "The realloc Function" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/MEM07-C.+Ensure+that+the+arguments+to+calloc()%2C+when+multiplied%2C+do+not+wrap?showChildren=false&showComments=false)[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=437)[](https://www.securecoding.cert.org/confluence/display/seccode/MEM09-C.+Do+not+assume+memory+allocation+functions+initialize+memory?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| The conversion from gadget ptr to widget ptr is fine (assuming one is done with the gadget) and does not have the conversion problems described, since the copy is done as uninterpreted bytes.; Presumably each member of the widget would be assigned to before being used for anything.
                                        Posted by dagwyn at Apr 16, 2008 22:20
                                     |
| the header is abit wrong - you can also use realloc to allocate the memory in the first place (with arg 1 = NULL).; Often more convenient than a first malloc, in a "allocate or grow allocated memory" setting.
                                        Posted by hbf at Apr 18, 2008 06:16
                                     |
| The idiom below (or variants on it - the key point is that the initial pointer passed to realloc() is NULL) is simpler than one which interleaves malloc() on the first use and realloc() thereafter.
typedef struct x { ... } x;
static x *x_base = 0;
static size_t x_size = 0;
static size_t x_used = 0; 
... 
if (x_used >= x_size) {
    size_t new_size = (x_size + 2) * 2;
    x *x_new = (x *)realloc(x_base, new_size * sizeof(x));
    if (x_new == 0)
    {
        /* Handle error */
    }
    x_size = new_size;
    x_base = x_new;
} 

And you're welcome to substitute a struct widget or struct gadget for `'x'` ![](images/icons/emoticons/smile.svg) (I have found that using `(n + 2) * 2` works quite nicely for testing - it uses size 4, 12, 28, ... so it triggers reallocations sufficiently quickly for half-way decent testing to shake out incorrect assumptions in the code. But I usually use named constants (like `RNA_EXTRA_ADD` and `RNA_EXTRA_MUL`) to permit configuration with larger - or smaller - values.)
![](images/icons/contenttypes/comment_16.png) Posted by jonathan.leffler@gmail.com at Apr 20, 2008 00:45
\|
