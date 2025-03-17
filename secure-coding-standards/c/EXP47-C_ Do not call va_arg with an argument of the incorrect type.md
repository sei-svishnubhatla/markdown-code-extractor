The variable arguments passed to a variadic function are accessed by calling the `va_arg()` macro. This macro accepts the `va_list` representing the variable arguments of the function invocation and the type denoting the expected argument type for the argument being retrieved. The macro is typically invoked within a loop, being called once for each expected argument. However, there are no type safety guarantees that the type passed to `va_arg` matches the type passed by the caller, and there are generally no compile-time checks that prevent the macro from being invoked with no argument available to the function call.
The C Standard, 7.16.1.1, states \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\], in part:
> If type is not compatible with the type of the actual next argument (as promoted according to the default argument promotions), the behavior is undefined, except for the following cases:
>
> —  both types are pointers to qualified or unqualified versions of compatible types;
>
> —  one type is compatible with a signed integer type, the other type is compatible with the corresponding unsigned integer type, and the value is representable in both types;
>
> —  one type is pointer to qualified or unqualified void and the other is a pointer to a qualified or unqualified character type;
>
> —  or, the type of the next argument is nullptr_t and type is a pointer type that has the same representation and alignment requirements as a pointer to a character type.

Ensure that an invocation of the `va_arg()` macro does not attempt to access an argument that was not passed to the variadic function. Further, the type passed to the `va_arg()` macro must match the type passed to the variadic function after default argument promotions have been applied. Either circumstance results in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
This noncompliant code example attempts to read a variadic argument of type `unsigned char` with `va_arg()`. However, when a value of type `unsigned char` is passed to a variadic function, the value undergoes default argument promotions, resulting in a value of type `int` being passed.
``` c
#include <stdarg.h>
#include <stddef.h>
void func(size_t num_vargs, ...) {
  va_list ap;  
  va_start(ap, num_vargs);
  if (num_vargs > 0) {
    unsigned char c = va_arg(ap, unsigned char);
    // ...
  }
  va_end(ap);
}
void f(void) {
  unsigned char c = 0x12;
  func(1, c);
}
```
## Compliant Solution
The compliant solution accesses the variadic argument with type `int`, and then casts the resulting value to type `unsigned char`:
``` c
#include <stdarg.h>
#include <stddef.h>
void func(size_t num_vargs, ...) {
  va_list ap;  
  va_start(ap, num_vargs);
  if (num_vargs > 0) {
    unsigned char c = (unsigned char) va_arg(ap, int);
    // ...
  }
  va_end(ap);
}
void f(void) {
  unsigned char c = 0x12;
  func(1, c);
}
```
## Noncompliant Code Example
This noncompliant code example assumes that at least one variadic argument is passed to the function, and attempts to read it using the `va_arg()` macro. This pattern arises frequently when a variadic function uses a sentinel value to denote the end of the variable argument list. However, the caller passes no variadic arguments to the function, which results in undefined behavior.
``` c
#include <stdarg.h>
void func(const char *cp, ...) {
  va_list ap;  
  va_start(ap, cp);
  int val = va_arg(ap, int);
  // ...
  va_end(ap);
}
void f(void) {
  func("The only argument");
}
```
## Compliant Solution
Standard C provides no mechanism to enable a variadic function to determine how many variadic arguments are actually provided to the function call. That information must be passed in an out-of-band manner. Oftentimes this results in the information being encoded in the initial parameter, as in this compliant solution:
``` c
#include <stdarg.h>
#include <stddef.h>
void func(size_t num_vargs, const char *cp, ...) {
  va_list ap;  
  va_start(ap, cp);
  if (num_vargs > 0) {
    int val = va_arg(ap, int);
    // ...
  }
  va_end(ap);
}
void f(void) {
  func(0, "The only argument");
}
```
## Risk Assessment
Incorrect use of `va_arg()` results in undefined behavior that can include accessing stack memory.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP47-C | Medium | Likely | High | P6 | L2 |

### Automated Detection
<table class="wrapped relative-table confluenceTable" style="width: 71.7808%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 22%" />
<col style="width: 23%" />
<col style="width: 40%" />
<col />
<col />
<col />
</colgroup>
<thead>
<tr>
<th class="confluenceTh"><p>Tool</p></th>
<th class="confluenceTh"><p>Version</p></th>
<th class="confluenceTh"><p>Checker</p></th>
<th class="confluenceTh"><p>Description</p></th>
<th></th>
<th></th>
<th></th>
</tr>
</thead>
<tbody>
<tr>
<td class="confluenceTd"><a href="Axivion%20Bauhaus%20Suite">Axivion Bauhaus Suite</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>7.2.0</p>
</div></td>
<td class="confluenceTd"><strong>CertC-EXP47</strong></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="https://wiki.sei.cmu.edu/confluence/display/cplusplus/Clang">Clang</a></td>
<td class="confluenceTd"><div class="content-wrapper">
3.9
</div></td>
<td class="confluenceTd"><code>-Wvarargs</code></td>
<td class="confluenceTd">Can detect some instances of this rule, such as promotable types.<br />
Cannot detect mismatched types or incorrect number of variadic arguments.</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="CodeSonar">CodeSonar</a></td>
<td class="confluenceTd"><div class="content-wrapper">
8.3p0
</div></td>
<td class="confluenceTd"><strong>BADMACRO.STDARG_H</strong></td>
<td class="confluenceTd">Use of &lt;stdarg.h&gt; feature</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="Helix%20QAC">Helix QAC</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>2024.4</p>
</div></td>
<td class="confluenceTd"><p><strong>DF4901, DF4902, DF4903, DF4904</strong></p></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="https://wiki.sei.cmu.edu/confluence/display/c/Klocwork">Klocwork</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>2024.4</p>
</div></td>
<td class="confluenceTd"><div class="content-wrapper">
<p><strong>CERT.VA_ARG.TYPE</strong></p>
</div></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><div class="content-wrapper">
<p><br />
</p>
</div></td>
<td class="confluenceTd"><div class="content-wrapper">
<br />
&#10;</div></td>
<td class="confluenceTd"><div class="content-wrapper">
<p><br />
</p>
</div></td>
</tr>
<tr>
<td class="confluenceTd"><a href="https://wiki.sei.cmu.edu/confluence/display/cplusplus/LDRA">LDRA tool suite</a></td>
<td class="confluenceTd"><div class="content-wrapper">
9.7.1
</div></td>
<td class="confluenceTd"><p><strong>44 S<br />
</strong></p></td>
<td class="confluenceTd"><p>Enhanced Enforcement</p></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="Parasoft">Parasoft C/C++test</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>2024.2</p>
</div></td>
<td class="confluenceTd"><strong>CERT_C-EXP47-a</strong></td>
<td class="confluenceTd">Do not call va_arg with an argument of the incorrect type</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="PC-lint%20Plus">PC-lint Plus</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>1.4</p>
</div></td>
<td class="confluenceTd"><p><strong>917</strong></p></td>
<td class="confluenceTd"><p>Assistance provided: reports argument promotion to match prototype</p></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><p><a href="https://wiki.sei.cmu.edu/confluence/display/c/Polyspace+Bug+Finder">Polyspace Bug Finder</a></p></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>R2024a</p>
</div></td>
<td class="confluenceTd"><p><a href="https://www.mathworks.com/help/bugfinder/ref/certcruleexp47c.html">CERT C: Rule EXP47-C</a></p>
<p><br />
</p></td>
<td class="confluenceTd"><p>Checks for:</p>
<ul>
<li>Incorrect data type passed to va_arg</li>
<li>Too many va_arg calls for current argument list</li>
</ul>
<p>Rule fully covered</p></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
<tr>
<td class="confluenceTd"><a href="TrustInSoft%20Analyzer">TrustInSoft Analyzer</a></td>
<td class="confluenceTd"><div class="content-wrapper">
<p>1.38</p>
</div></td>
<td class="confluenceTd"><strong>unclassified (variadic)</strong></td>
<td class="confluenceTd"><p>Exhaustively verified (see <a href="https://taas.trust-in-soft.com/tsnippet/t/7c83c498">one compliant and one non-compliant example</a>).</p></td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
<td class="confluenceTd"><br />
</td>
</tr>
</tbody>
</table>
### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+EXP47-C).
## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2024] | Subclause;7.16, "Variable Arguments <stdarg.h>" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152216) [](../c/Rule%2003_%20Expressions%20_EXP_) [](../c/Rule%2004_%20Integers%20_INT_)
## Comments:

|  |
| ----|
| In the last compliant solution function is called with invalid arguments order:func("The only argument", 0);but should be:func(0, "The only argument");
                                        Posted by oleg.omelyusik at Dec 20, 2017 10:08
                                     |
| Fixed, thanks.
                                        Posted by svoboda at Dec 21, 2017 08:55
                                     |

