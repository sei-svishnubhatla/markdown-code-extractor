> [!info]  
>
> Don't try to use anything here as it needs a great deal of work and is most likely incorrect at the moment.

`ptrdiff_t` is the signed integer type of the result of subtracting two pointers (C99 7.17 p2).
## Noncompliant Code Example
``` java
/* test if we can fit elem_count chars in the space between p_current and p_max.
int test_ptr(size_t elem_count, char *p_max, char *p_current) {
  int subscript_diff = p_max - p_current;
  if ( (p_max > p_current) && (subscript_diff > elem_count) ) {
    return 0;
  }
  return -1;
}
```
Consider what happens when this function is called in the following manner on a 64-bit platform:
``` java
size_t char_count = INT_MAX + 10;
char *huge_string = malloc(char_count); //we have lots of RAM ;)
test_ptr(3, huge_string + char_count - 1, huge_string);
```
test_ptr() will return -1 when it should return 0.
The result of p_max - p_current is a ptrdiff_t with a value of INT_MAX + 10. However, on a 64-bit platform, ints are still most-likely only 32-bits which means that when p_max - p_current is stored into an int, the result will be a negative value of INT_MIN + 9. Now subscript_diff is less than elem_count and the comparison will fail.
NOTE: Changing subscript_diff from int to ptrdiff_t would solve this problem on a 64-bit platform, but it would not fix it on a 32-bit platform (because on a 32-bit platform, sizeof(ptrdiff_t) == 4 and so ptrdiff_t is equivalent to int), and thus we would be introducing platform-defined behavior.
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT20-C | high | probable | low | P18 | L1 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT18-C).
## Related Guidelines
[SEI CERT C++ Coding Standard](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=88046682): [VOID INT17-CPP. Define integer constants in an implementation-independent manner](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+INT17-CPP.+Define+integer+constants+in+an+implementation-independent+manner)
[ISO/IEC 9899-1999](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-1999) Section 6.4.4.1, "Integer constants"
## Bibliography
Dan Saks. Standard C's pointer difference type.  
10/18/2007
<http://www.eetimes.com/design/signal-processing-dsp/4007211/Standard-C-s-pointer-difference-type><http://embedded-systems.com/columns/technicalinsights/202404371>
Ptrdiff_t is evil  
david_leblanc  
2 Sep 2008 <http://blogs.msdn.com/b/david_leblanc/archive/2008/09/02/ptrdiff-t-is-evil.aspx>
------------------------------------------------------------------------
[INT17-C. Do not make assumptions about representation of signed integers](/confluence/pages/createpage.action?spaceKey=seccode&title=INT17-C.+Do+not+make+assumptions+about+representation+of+signed+integers)      [](Rule%2004_%20Integers%20_INT_)      [](INT30-C_%20Ensure%20that%20unsigned%20integer%20operations%20do%20not%20wrap)
