> [!warning]  
>
> This guideline has been deprecated by
>
> -   EXP37-C. Call functions with the arguments intended by the API

Do not call a function with the wrong number or type of arguments. C identifies four distinct situations in which undefined behavior may arise as a result of invoking a function using a declaration that is incompatible with its definition or with incorrect types or numbers of arguments:

|  |  |
| ----|----|
| 26 | A pointer is used to call a function whose type is not compatible with the pointed-to type (6.3.2.3).  |
| 38 | For a call to a function without a function prototype in scope, the number of arguments does not equal the number of parameters (6.5.2.2).  |
| 39 | For call to a function without a function prototype in scope where the function is defined with a function prototype, either the prototype ends with an ellipsis or the types of the arguments after promotion are not compatible with the types of the parameters (6.5.2.2).  |
| 41 | A function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function (6.5.2.2).  |

------------------------------------------------------------------------
A function type is determined by its returned type and the types and number of its parameters. Do not call a function with a wrong function type.
Setting a function pointer to refer to a function of an incompatible type generates a compiler warning. These warnings should be resolved. (See [MSC00-C. Compile cleanly at high warning levels](MSC00-C_%20Compile%20cleanly%20at%20high%20warning%20levels).) Otherwise, a call through that function pointer will result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
## Noncompliant Code Example
In this noncompliant example, the C Standard Library function `strchr()` is called through the function pointer `fp` with incorrectly typed arguments. According to the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\],
> A pointer to a function of one type may be converted to a pointer to a function of another type and back again; the result shall compare equal to the original pointer. If a converted pointer is used to call a function whose type is not compatible with the pointed-to type, the behavior is undefined.

(See also [undefined behavior 26](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_26) in Annex J.)
``` c
char *(*fp)();
void f(void) {
  char *c;
  fp = strchr;
  c = fp(12, 2);  /* violation */
} 
```
## Compliant Solution
In this compliant solution, the function pointer `fp` points to a function returning `char *`, with the correct number and type of arguments. 
``` c
char *(*fp)(const char *, int);
void f(void) {
  char *c;
  char str[] = "This is a sample string";
  fp = strchr;
  c = fp(str,'s');  /* address of the first occurrence of the character s in str */
}
```
## Noncompliant Code Example
In this noncompliant example, the function copy is defined to take two arguments but is called with three arguments.
``` c
/* in another source file */
void copy(char *dst, const char *src) {
  if (!strcpy(dst, src)) {
    /* report error */
  }
}
/* in this source file -- no copy prototype in scope */
void copy();
void g(const char *s) {
  char buf[20];
  copy(buf, s, sizeof buf);  /* violation */
  /* ... */
}
```
## Compliant Solution
In this compliant solution, the function copy is defined to take two arguments and is called with two arguments. The program behaves as expected.
``` c
/* in another source file */
void copy(char *dst, const char *src) {
  if (!strcpy(dst, src)) {
    /* report error */
  }
}
/* in this source file -- no copy prototype in scope */
void copy(char *, const char *);
void g(const char *s) {
  char buf[20];
  copy(buf, s);  /* copies the characters in s to buf */
  /* ... */
}
```
## Risk Assessment
Calling through function pointers that have been converted from one type to another causes undefined behavior. However, it is unlikely that an attacker can exploit this behavior to run arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL35-C | low | probable | medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| EDG | ; | ; | ; |
| Fortify SCA | V. 5.0 | ; | ; |
| GCC | 4.3.5 | ; | ; |
| LDRA tool suite | 9.7.1 | 576 S | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 0674 (C) | Fully implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+DCL35-C).
## Related Guidelines

|  |  |
| ----|----|
| ISO/IEC TR 24772:2013 | Type System;[IHN]
Subprogram Signature Mismatch [OTR] |
| ISO/IEC TS 17961 | Calling functions with incorrect arguments [argcomp] |
| MITRE CWE | CWE-686, Function call with incorrect argument type |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 6.3.2.3, "Pointers" |

[](https://www.securecoding.cert.org/confluence/display/seccode/DCL34-C.+Use+volatile+for+data+that+cannot+be+cached?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=331) [](https://www.securecoding.cert.org/confluence/display/seccode/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications?showChildren=false&showComments=false)
## Comments:
<table data-border="0" width="100%">
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td><p>This is a fun area - especially when you get involved with dynamic libraries and loading. Different platforms have different interfaces (three of relevance to me - Windows <code>LoadLibrary()</code> et al., HP-UX <code>shl_load()</code> et al., and pretty much everything else <code>dlopen()</code> et al.). The lookup functions all return the symbol via a <code>void *</code> - which is painful for functions. The HP system does provide specific lookups for functions versus data, but still uses the same function. I don't know if there are relevant standard practices here to get the code to compile without warnings. The best I've come up with is a union:</p>
<div class="code panel pdl" style="border-width: 1px;">
<div class="codeContent panelContent pdl">
<div class="sourceCode" id="cb1" data-syntaxhighlighter-params="brush: java; gutter: false; theme: Confluence" data-theme="Confluence" style="brush: java; gutter: false; theme: Confluence"><pre class="sourceCode java"><code class="sourceCode java"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a>union data_func_ptr <span class="op">{</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a>  <span class="dt">void</span>  <span class="op">*</span>data<span class="op">;</span></span>
<span id="cb1-3"><a href="#cb1-3" aria-hidden="true" tabindex="-1"></a>  <span class="dt">void</span> <span class="op">(*</span>func<span class="op">)(</span><span class="dt">void</span><span class="op">);</span></span>
<span id="cb1-4"><a href="#cb1-4" aria-hidden="true" tabindex="-1"></a><span class="op">};</span></span></code></pre></div>
</div>
</div>
<p>Using this, you can circumvent compiler warnings - at the moment - by assigning the return value of the lookup functions (or the lookup argument for <code>shl_findsym</code>) to the <code>.data</code> member, and then coercing the <code>.func</code> member to the correct function type.</p>
<p>The key point in your example is that although you can cast function pointers to a common type - such as the <code>(void ( * )(void))</code> type in <code>union data_func_ptr</code> - and back to the original type, it is not safe to invoke the function via anything other than its correct (original, real) function type. Even with the basic lookup sanitized, you are still forced to write fairly brutal casts in the code to make the coercions between function pointers work. However, if you stick with pointers to functions, you can stop GCC complaining -- if you play with data pointers, it still objects (an objection sanctioned by the C standard since there is no defined conversion between data pointers and function pointers).</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by jonathan.leffler@gmail.com at Mar 15, 2008 21:29
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>Yes, the rule is overstated since there are occasions where a "generic" function pointer has legitimate uses.  The problem is not in converting a function pointer but in using a type that does not match the function definition (as happens when one fails to convert back to the original type).</p>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by dagwyn at Apr 15, 2008 14:10
</div></td>
</tr>
<tr>
<td style="border-top: 1px dashed #666666"><p>There are a number of interesting cases of undefined behavior (UB) that look like they could fall under this guideline. Which one do we want to cover here?</p>
<div class="table-wrap">
<pre class="table"><code>|  UB  |  Annex J, Section 2 Description  |
| ----|----|
|  14  |  Two declarations of the same object or function specify types that are not compatible (6.2.7).  |
|  23  |  A pointer is used to call a function whose type is not compatible with the pointed-to type (6.3.2.3).  |
|  36  |  For a call to a function without a function prototype in scope, the number of arguments does not equal the number of parameters (6.5.2.2).  |
|  37  |  For call to a function without a function prototype in scope where the function is defined with a function prototype, either the prototype ends with an ellipsis or the types of the arguments after promotion are not compatible with the types of the parameters (6.5.2.2).  |
|  38  |  For a call to a function without a function prototype in scope where the function is not defined with a function prototype, the types of the arguments after promotion are not compatible with those of the parameters after promotion (with certain exceptions) (6.5.2.2).  |
|  39  |  A function is defined with a type that is not compatible with the type (of the expression) pointed to by the expression that denotes the called function (6.5.2.2).  |
|  73  |  In a context requiring two function types to be compatible, they do not have compatible return types, or their parameters disagree in use of the ellipsis terminator or the number and type of parameters (after default argument promotion, when there is no parameter type list or when one type is specified by a function definition with an identifier list) (6.7.5.3).  |
|  97  |  A function, object, type, or macro that is specified as being declared or defined by some standard header is used before any header that declares or defines it is included (7.1.2).  |</code></pre>
</div>
<div class="smallfont" data-align="left" style="color: #666666; width: 98%; margin-bottom: 10px;">
<img src="images/icons/contenttypes/comment_16.png" /> Posted by martinsebor at Jan 29, 2010 23:21
</div></td>
</tr>
</tbody>
</table>
