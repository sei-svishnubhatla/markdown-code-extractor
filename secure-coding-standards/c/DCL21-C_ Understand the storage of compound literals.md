Subclause 6.5.2.5 of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] defines a compound literal as
> A postfix expression that consists of a parenthesized type name followed by a brace-enclosed list of initializers. . . . The value of the compound literal is that of an unnamed object initiated by the initializer list.

The storage for this object is either static (if the compound literal occurs at file scope) or automatic (if the compound literal occurs at block scope), and the storage duration is associated with its immediate enclosing block. For example, in the function
``` java
void func(void) {
  int *ip = (int[4]){1,2,3,4};
  /* ... */
}
```
following initialization, the `int` pointer `ip` contains the address of an unnamed object of type `int[4]`, allocated on the stack. Once `func` returns, any attempts to access this object will produce [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
Note that only one object is created per compound literal—even if the compound literal appears in a loop and has dynamic initializers.
This recommendation is a specific instance of [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations).
## Noncompliant Code Example
In this noncompliant code example, the programmer mistakenly assumes that the elements of the `ints` array of the pointer to `int_struct` are assigned the addresses of distinct `int_struct` objects, one for each integer in the range `[0, MAX_INTS - 1]`:
``` c
#include <stdio.h>
typedef struct int_struct {
  int x;
} int_struct;
#define MAX_INTS 10
int main(void){
  size_t i;
  int_struct *ints[MAX_INTS];
  for (i = 0; i < MAX_INTS; i++) {
    ints[i] = &(int_struct){i};
  }
  for (i = 0; i < MAX_INTS; i++) {
    printf("%d\n", ints[i]->x);
  }
  return 0;
}
```
However, only one `int_struct` object is created. At each iteration of the first loop, the `x` member of this object is set equal to the current value of the loop counter `i`. Therefore, just before the first loop terminates, the value of the `x` member is `MAX_INTS - 1`.
Because the storage duration of the compound literal is associated with the `for` loop that contains it, dereferencing `ints` in the second loop results in [undefined behavior 9](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_9) (Annex J of the C Standard).
Even if the region of memory that contained the compound literal is not written to between loops, the print loop will display the value `MAX_INTS - 1` for `MAX_INTS` lines. This is contrary to the intuitive expected result, which is that the integers `0` through `MAX_INTS - 1` would be printed in order.
## Compliant Solution
This compliant solution uses an array of structures rather than an array of pointers. That way, an actual copy of each `int_struct` (rather than a pointer to the object) is stored.
``` c
#include <stdio.h>
typedef struct int_struct {
  int x;
} int_struct;
#define MAX_INTS 10
int main(void){
  size_t i;
  int_struct ints[MAX_INTS];
  for (i = 0; i < MAX_INTS; i++) {
    ints[i] = (int_struct){i};
  }
  for (i = 0; i < MAX_INTS; i++) {
    printf("%d\n", ints[i].x);
  }
  return 0;
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL21-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Axivion Bauhaus Suite | 7.2.0 | CertC-DCL21 |  |
| Helix QAC | 2024.4 | C1054, C3217 |  |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.5.2.5, "Compound Literals" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152311) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152049)
## Comments:

|  |
| ----|
| 
    Please use our numbering conventions for the rule ID. 90 is a bit high 
    I'm not sure what this rule is trying to forbid. The NCCE & CS seem to be saying "if you declare a pointer, don't assume the system allocates space for the pointed-to type". Generally, you shouldn't have rules titled "Understand..." if you're demonstrating a particular coding error.
    The code samples need to be colored red for the NCCE and blue for the CS.
    I disagree with the Risk Assessment metrics...please provide some argument for the values, or change them.
                                        Posted by svoboda at Mar 03, 2010 12:17
                                     |
| Suppose I changed the compliant solution as shown below. What would be the behavior of the program?
typedef struct INT_STRUCT {
  int x;
} INT_STRUCT;
#define MAX_INTS 10
int main() {
  int i;
  INT_STRUCT* ints[MAX_INTS];
  for (i = 0; i < MAX_INTS; i++)
      ints[i] = (INT_STRUCT[2]){ { i }, { i + 1} };
  for (i = 0; i < MAX_INTS; i++)
      printf("%d, %d\n", ints[i][0].x, ints[i][1].x);
}

Btw., I would suggest to avoid using all caps for type names (all caps are typically reserved for the names of macros).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 10, 2010 11:15
\| \|
That would print "9 10" for 10 lines.
It seems to me that your example and the NCCE have exactly the same problem - only one object is ever initialized and subsequent "initializations" in the first loop are in fact just accesses to that single object.
![](images/icons/contenttypes/comment_16.png) Posted by aleontie at Mar 10, 2010 15:21
\| \|
I don&#39;t think the two examples suffer from the same problem. The NCCE has surprising but well-defined semantics. The example I gave has undefined behavior because the lifetime of the compound literal object in the first `for` loop ends after the first loop terminates, and the second loop dereferences is after its lifetime has ended. My intent was to show that there is a more serious potential problem with compound literals than just surprising behavior.
Oh, wait, I had completely missed that the NCCE also declares `ints` to be an array of pointers, just like the example I gave. I should have my eyes checked! In that case, both the NCCE and my example do suffer from the same problem: they both exhibit undefined behavior, namely UB [8](CC.-Undefined-Behavior_87152280.html#CC.UndefinedBehavior-ub_8).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Mar 10, 2010 16:27
\| \|
Ah, I completely overlooked that in the spec - it indeed states that a CL declared in a loop or other block scope has duration of the block. I'll add this information.
Thanks for the pointers.
![](images/icons/contenttypes/comment_16.png) Posted by aleontie at Mar 10, 2010 19:44
\| \|
For the example in the guideline description:
``` java
int *ip = (int[4]){1,2,3,4};
```
you should state what happens to the storage when the function returns.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Mar 12, 2010 09:48
\| \|
This rule is correct, but I am not completely comfortable with it. Mainly because I have never made this mistake so to me it seems implausible. Also we tend to frown on rules whose titles begin with "Understand". A stronger title might be: "Don't use compound literals except to initialize a struct or array". What do others think?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 20, 2010 14:54
\| \|
I wonder (suspect) if the trap might be to assume that a compound literal has the same lifetime as, for example, a string literal:
``` java
const char* f() { return "foo"; }
const char* g() { return (char[]){'f', 'o', 'o', '\0'}; }
void h() {
    puts(f());   // okay
    puts(g());   // undefined
}
```
I assume you meant "to initialize or assign" but even constraining the use of compound literals to the initialization or assignment of structs and arrays would severely limit their usefulness (e.g., when assigning or initializing pointers). For example, this is a valid and useful/common use case:
``` java
void f() {
    puts(asctime(&(struct tm){ .tm_hour = 1, .tm_min = 2, .tm_sec = 3 }));
}
```
That being said, this guideline is just one of the several cases belonging under [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations) and might as well be rolled into it.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 20, 2010 20:41
\|
