Variadic functions access their variable arguments by using `va_start()` to initialize an object of type `va_list`, iteratively invoking the `va_arg()` macro, and finally calling `va_end()`. The `va_list` may be passed as an argument to another function, but calling `va_arg()` within that function causes the `va_list` to have an [indeterminate value](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) in the calling function. As a result, attempting to read variable arguments without reinitializing the `va_list` can have [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior). According to the C Standard, 7.16, paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\],
> If access to the varying arguments is desired, the called function shall declare an object (generally referred to as ap in this subclause) having type va_list. The object ap may be passed as an argument to another function; if that function invokes the va_arg macro with parameter ap, the representation of ap in the calling function is indeterminate and shall be passed to the va_end macro prior to any further reference to ap.
>
> 295\) A pointer to a va_list can be created and passed to another function, in which case the original function can make further use of the original list after the other function returns.

## Noncompliant Code Example
This noncompliant code example attempts to check that none of its variable arguments are zero by passing a `va_list` to helper function `contains_zero()`. After the call to `contains_zero()`, the value of `ap` is [indeterminate](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue).
``` c
#include <stdarg.h>
#include <stdio.h>
int contains_zero(size_t count, va_list ap) {
  for (size_t i = 1; i < count; ++i) {
    if (va_arg(ap, double) == 0.0) {
      return 1;
    }
  }
  return 0;
}
int print_reciprocals(size_t count, ...) {
  va_list ap;  
  va_start(ap, count);
  if (contains_zero(count, ap)) {
    va_end(ap);
    return 1;
  }
  for (size_t i = 0; i < count; ++i) {
    printf("%f ", 1.0 / va_arg(ap, double));
  }
  va_end(ap);
  return 0;
}
```
## Compliant Solution
The compliant solution modifies `contains_zero()` to take a pointer to a `va_list`. It then uses the `va_copy` macro to make a copy of the list, traverses the copy, and cleans it up. Consequently, the print_reciprocals() function is free to traverse the original `va_list`.
``` c
#include <stdarg.h>
#include <stdio.h>
int contains_zero(size_t count, va_list *ap) {
  va_list ap1;
  va_copy(ap1, *ap);
  for (size_t i = 1; i < count; ++i) {
    if (va_arg(ap1, double) == 0.0) {
      return 1;
    }
  }
  va_end(ap1);
  return 0;
}
int print_reciprocals(size_t count, ...) {
  int status;
  va_list ap;
  va_start(ap, count);
  if (contains_zero(count, &ap)) {
    printf("0 in arguments!\n");
    status = 1;
  } else {
    for (size_t i = 0; i < count; i++) {
      printf("%f ", 1.0 / va_arg(ap, double));
    }
    printf("\n");
    status = 0;
  }
  va_end(ap);
  return status;
}
```
## Risk Assessment
Reading variable arguments using a `va_list` that has an [indeterminate value](BB.-Definitions_87152273.html#BB.Definitions-indeterminatevalue) can have unexpected results.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC39-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADMACRO.STDARG_H | Use of <stdarg.h> Feature |
| Cppcheck Premium | 24.11.0 | premium-cert-msc39-c |  |
| Helix QAC | 2024.4 | C3497C++3146, C++3147, C++3148, C++3149, C++3167 |  |
| Klocwork | 2024.4 | VA.LIST.INDETERMINATE |  |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC39-a | Use macros for variable arguments correctly |
| Polyspace Bug Finder | R2024a | CERT C: Rule MSC39-C | Checks for:Invalid va_list argumentToo many va_arg calls for current argument listRule partially covered. |
| TrustInSoft Analyzer | 1.38 | variadic | Exhaustively verified. |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC39-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause;7.16, "Variable Arguments <stdarg.h>" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152297) [](../c/Rule%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151950)
## Comments:

|  |
| ----|
| 
    Needs a better title. Should be precise about what exactly is the problem.
    According to C99, calling va_args on ap is not undefined, but rather indeterminate. Should quote the relevant passage in C99.   I think the problem calls when variadic function f() calls g(), g() calls va_arg() at least once, does not call va_end(), and returns to f(), then f() calling va_arg() is indeterminate. It is OK for f() to call va_end(), however (according to my interpretation of the standard.)
    The intro is rather cryptic. For instance what is ap? some variable in the standard?
    I think that calling va_end() twice is also undefined, but is not what this rule warns about. The NCCE does this.
                                        Posted by svoboda at Mar 02, 2010 11:25
                                     |
| I've revised the title and introduction; hopefully they are clearer now.
I also changed the CS so that the copy is made within contains_zeroes, because that makes it clearer how contains_zeroes is meant to be used.
                                        Posted by astromme at Mar 02, 2010 13:19
                                     |
| 
    The title is better, but still unclear, prob s/va_args()/va_arg()/
    Good change on the CS. But it still needs some work as you can still wind up calling va_end() twice.
                                        Posted by svoboda at Mar 02, 2010 13:47
                                     |
| I would recommend to avoid relying on semantics like those implemented in contains_zero() in the compliant solution. Instead, callers should defensively assume that the callee modifies the va_list argument and pass to it a copy before manipulating the original. (I.e., just as when invoking one of the C standard library functions that take a va_list argument, such as vsprintf().)
Incidentally, this guideline covers undefined behavior 129. Besides this problem, UB 131 and UB 134 are common bugs as well. It would be nice to extend the scope of this guideline and discuss them as well.
int print_reciprocals(int count, ...) {
  int status;
  va_list ap1;
  va_list ap2  
  va_start(ap1, count);
  va_copy(ap2, ap1);
  if (contains_zero(count, ap2))
    status = 1;
  else {
    for (int i = 0; i < count; i++)
      printf("%f ", 1.0 / va_arg (ap1, double));
    status = 0;
  }
  va_end(ap2);
  va_end(ap1);
  return status;
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 02, 2010 23:45
\| \|
-   The NCCE's intro text is inaccurate, it needs to s/undefined/indeterminate/. (The standard is very precise about the meaning of these terms.)
<!-- -->
-   I'm curious as to what actually happens in the NCCE...can you provide an Implementation Details section explaining what the program behavior is on Windows or Linux?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 18, 2010 20:27
\| \|
va_copy does not exist in MSVC, so the CCE is not particularly useful there.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 06, 2013 11:40
\| \|
va_copy is in C11 (and prob C99 too). I suppose a Windows-specific CS would be in order here.
Then again, how heavily are varargs used in Windows? I'd guess not muich.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 07, 2013 14:48
\| \|
In C code; I would guess (based off nothing at all), they're used about the same amount as on other platforms.; I've seen it used in a handful of code bases myself.  I'll think about a CS for Windows and see if I can come up with one.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Jun 07, 2013 14:54
\| \|
So this is not portably possible in Visual Studio until Visual Studio 2013 is released.; On some platforms, you can simply assign the va_list, but on others platforms (notably ARM and x64) it may not be safe.  Once 2013 is released, we should revise this rule.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 19, 2013 15:10
\| \|
Hi, I have a question about the NCCE.;  
The type `va_list` is used for argument pointer variables and I noticed that **contains_zero()** pass va_list by value, not referenced. Does contains_zero(count, ap) affect what \`ap\` point to?  
The compliant solution makes a copy to the va_list( can be interpreted as assign), the change to dest va_list won't affect the original va_list,  is there any difference between passing by value and making a copy to the va_list?  
Please help clarify, many thanks!
![](images/icons/contenttypes/comment_16.png) Posted by zhaohui at May 15, 2020 05:51
\| \|
Variable argument lists are a bit of a strange beast because each architecture does them slightly differently. Because C doesn't have the notion of references, you would think passing a non-pointer value means that the passed object cannot be changed by the caller, but that's not true with variable argument lists because they're essentially magic. This is why the standard explicitly calls out this behavior in the text quoted in the intro paragraph.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at May 15, 2020 07:45
\|
