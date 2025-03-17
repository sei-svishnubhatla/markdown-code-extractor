> [!info]  
>
> This practice is an incomplete work in progress. It may contain errors and should not be applied until this notice has been removed.

Like most functions, the vast majority of macros do not change the control flow of the invoking code. However, because macros, unlike functions, are textually expanded at the point of their invocation, they can easily affect the flow of control of the invoking code. This could be done by
-   Evaluating `break`, `continue`, or `return` statements.
-   Failing to properly terminate `if` statements.
The effects of invoking such macros can be surprising and lead to subtle flaws. Thus, as discussed in [PRE00-C. Prefer inline or static functions to function-like macros](PRE00-C_%20Prefer%20inline%20or%20static%20functions%20to%20function-like%20macros), functions are preferable to macros. However, in cases where defining a macro is unavoidable, the macro definition should avoid statements that change the control flow of the invoking code; and, ideally, it should be a single expression.
Note that invoking a function in the body of the macro does not change the flow of control of the invoking code, even if the function does not return. Thus, macros that invoke other functions, including `abort()` or `exit()`, are not necessarily in violation of this guideline. For the same reason, the `assert()` macro does not violate this rule.
## Noncompliant Code Example
In the following noncompliant example, the macro `SAFE_MALLOC()` attempts to provide a primitive form of checking and handling of memory allocation failures. (See [void MEM32-C. Detect and handle memory allocation errors](void%20MEM32-C_%20Detect%20and%20handle%20memory%20allocation%20errors).) Since the solution relies on the expansion involves the predefined context-sensitive constants `__FILE__`, `__LINE__`, and `__func__`, it cannot be implemented as a function and provide the same convenience. However, since the `if` statement in the body of the macro is not necessarily obvious to users of the macro, it is possible for it to inadvertently couple with an `else` clause intended to be paired with an enclosing `if` statement, as shown in the function `f()`.
``` c
#define SAFE_MALLOC(T, p, n)                         \
  if (0 == ((p) = (T*)malloc((n)))) {                \
    fprintf(stderr, "%s:%d (%s): out of memory\n",   \
            __FILE__, __LINE__, __func__);           \
    exit(1);                                         \
  }
void f(const int *array, size_t nelems) {
  int *a;
  size_t nbytes = nelems * sizeof(*a);
  int buffer[128];
  if (sizeof( buffer) < nbytes)
    SAFE_MALLOC(int, a, nbytes)
  else
    a = buffer;
  memcpy(a, array, nbytes);
  /* Proceed to use a ... */
  if (a != buffer)
    free(a);
}
```
The result of expanding the invocation of the macro in `f()` is shown below, with indentation inserted to make the pairing of the `else` substatement apparent. With the macro expanded, the problem is obvious: `a` is set to `buffer` even when the size of memory, `nbytes`, exceeds that of the size of `buffer` and the `malloc()` call succeeds, causing an immediate memory leak and leading to a buffer overflow later in the function.
``` java
  if (sizeof( buffer) < nbytes)
    if (0 == ((a) = (int*)malloc((nbytes)))) {
      fprintf(stderr, "%s:%d (%s): out of memory\n",
              __FILE__, __LINE__, __func__);
      exit(1);
    }
    else
      a = buffer;
```
Note that this code also violates [EXP19-C. Use braces for the body of an if, for, or while statement](EXP19-C_%20Use%20braces%20for%20the%20body%20of%20an%20if,%20for,%20or%20while%20statement).
## Compliant Solution
The following compliant solution combines the definition of a helper function with that of a safe macro that avoids introducing an `if` statement or any other form of change of the flow of control in the caller by expanding into a single expression.
Note that [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions) discourages the use of functions, such as `memcpy()`, in favor of safer alternatives specified in *Extensions to the C Library, Part I: Bounds-checking interfaces* \[[ISO/IEC TR 24731-1](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IECTR24731-1-2007)\].
``` c
#define SAFE_MALLOC(n) \
  safe_malloc(n, __FILE__, __LINE__, __func__)
void* safe_malloc(size_t n,
                  const char *file,
                  int line,
                  const char *func) {
  void *p = malloc(n);
  if (0 == p) {
    fprintf(stderr, "%s:%d (%s): out of memory\n",
            file, line, func);
    exit(1);
  }
  return p;
}
void f(const int *array, size_t nelems) {
  int *a;
  size_t nbytes = nelems * sizeof(*a);
  int buffer[128];
  if (sizeof( buffer) < nbytes) {
    a = (int*)SAFE_MALLOC(nbytes);
  } else {
    a = buffer;
  }
  memcpy(a, array, nbytes);
  /* Proceed to use a ... */
  if (a != buffer) {
    free(a);
  }
}
```
## Compliant Solution
The following compliant solution uses a macro that uses the `?:` conditional operator rather than an if statement. The resulting macro may be safely used anywhere an expression is expected, including as a full statement.
``` c
#define SAFE_MALLOC(T, p, n)                         \
  ((0 == ((p) = (T*)malloc((n)))) ? (                \
    fprintf(stderr, "%s:%d (%s): out of memory\n",   \
            __FILE__, __LINE__, __func__),           \
    exit(1)) : p)
void f(const int *array, size_t nelems) {
  int *a;
  size_t nbytes = nelems * sizeof(*a);
  int buffer[128];
  if (sizeof( buffer) < nbytes) {
    SAFE_MALLOC(int, a, nbytes);
  } else {
    a = buffer;
  }
  memcpy(a, array, nbytes);
  /* Proceed to use a ... */
  if (a != buffer) {
    free(a);
  }
}
```
## Risk Assessment
A macro definition that changes the control flow of the invoking code can lead to subtle flaws whose consequences span the whole gamut of security vulnerabilities from abnormal termination to code injection.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| PRE13-C | medium | unlikely | low | P6 | L2 |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+PRE14-C).
## Bibliography
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/PRE12-C.+Do+not+define+unsafe+macros?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1064) [](https://www.securecoding.cert.org/confluence/display/seccode/PRE30-C.+Do+not+create+a+universal+character+name+through+concatenation?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| What about a macro that should change control flow? For instance, I've used a THROW() macro as a wrapper around C++'s throw keyword. I've also used & seen FOREACH macros.
The NCCE could be remedied by wrapping the macro in a do  ...  while(0) statement, as is recommended by PRE10-C. Wrap multi-statement macros in a do-while loop.
So far, I'm not convinced. I'll only agree that a macro's behavior should not surprise the user. (which is much the same advice given for operator overloading in C++.)
                                        Posted by svoboda at Jun 21, 2010 17:34
                                     |
| I am agree with you. For the example above in segment, ;I think use "do ... while (0) " to wrapper the macro to avoid unexpected behavior.
In some cases, we need the macro change control flow to avoid duplicated codes indeed.
                                        Posted by gfree.wind@gmail.com at May 15, 2011 23:51
                                     |
| Should the standard assert macro be listed as an exception? Or is part of the intent of this recommendation to deprecate use of assert?
                                        Posted by donbock at Feb 21, 2012 08:46
                                     |
| Noncompliant code will not compile. Semicolon at the end of SAFE_MALLOC call results into parser error.
                                        Posted by mohandhan at Dec 30, 2012 09:02
                                     |
| My earlier reference to the standard assert macro was because it invokes the exit() function; and I thought that function would constitute a change in control flow all by itself. A closer look at the examples leads me to wonder if this rule is intended to be restricted to more local control flow issues. Does this rule view exit() differently than return?
                                        Posted by donbock at Dec 30, 2012 19:12
                                     |
| "Note that invoking a function in the body of the macro does not change the flow of control of the invoking code, even if the function does not return." This is not true for longjmp(). On the other hand, there is a point of diminishing returns where reducing ambiguity also decreases readability.Add goto to the list of statements that cause a macro to change the flow of control.Add unbalanced braces to the bullet list of ways a macro could alter control flow. Does this subsume improper termination of if statement?Consider allowing some kind of escape hatch for well-documented macros whose semantics make the possible change in control flow readily apparent and unsurprising; such as the THROW and FOREACH examples given by David Svoboda in the first comment. Allowing exceptions is inconsistent with the desire for a static analysis tool to detect violations of the rule.
                                        Posted by donbock at Jan 04, 2013 18:25
                                     |
| You're right that longjmp is an exception, though I don't think the rule should extend to it as well. longjmp can change the control flow between distinct functions, and so its effects are no more surprising when it's invoked from within a macro than when invoked from within another function.I tend to agree that goto should be included in the list of prohibited statements, though I can imagine macros designed to work safely with such statements (when the label to jump to is an argument to the macro).I also agree that unbalanced braces are a similar problem to the if statement. As David noted, there is some overlap here with PRE10-C. Wrap multi-statement macros in a do-while loop.The THROW macro doesn't apply to C so we don't need an exception for it here. I'd have to see an example of the FOREACH macro to understand how it might violate this rule and to see if creating an exception for it would be worthwhile.
                                        Posted by martinsebor at Jan 06, 2013 12:52
                                     |

