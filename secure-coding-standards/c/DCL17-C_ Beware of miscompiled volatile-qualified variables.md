As described in depth in rule [DCL22-C. Use volatile for data that cannot be cached](DCL22-C_%20Use%20volatile%20for%20data%20that%20cannot%20be%20cached), a `volatile`-qualified variable "shall be evaluated strictly according to the rules of the abstract machine" \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]. In other words, the `volatile` qualifier is used to instruct the compiler to not make caching optimizations about a variable.
However, as demonstrated in "Volatiles Are Miscompiled, and What to Do about It" \[[Eide and Regehr](AA.-Bibliography_87152170.html#AA.Bibliography-EideandRegehr)\], all tested compilers generated some percentage of incorrect compiled code with regard to `volatile` accesses. Therefore, it is necessary to know how your compiler behaves when the standard `volatile` behavior is required. The authors also provide a workaround that eliminates some or all of these errors.
## Noncompliant Code Example
As demonstrated in Eide and Regehr's work, the following code example compiles incorrectly using GCC 4.3.0 for IA32 and the `-Os` optimization flag:
``` c
const volatile int x;
volatile int y;
void foo(void) {
  for(y = 0; y < 10; y++) {
    int z = x;
  }
}
```
Because the variable `x` is `volatile`-qualified, it should be accessed 10 times in this program. However, as shown in the compiled object code, it is accessed only once due to a loop-hoisting optimization \[[Eide and Regehr](AA.-Bibliography_87152170.html#AA.Bibliography-EideandRegehr)\]:
``` c
foo:
  movl $0, y
  movl x, %eax
  jmp .L2
.L3:
  movl y, %eax
  incl %eax
  movl %eax, y
.L2:
  movl y, %eax
  cmpl $10, %eax
  jg .L3
  ret
```
Should `x` represent a hardware register or some other memory-mapped device that has [side effects](BB.-Definitions_87152273.html#BB.Definitions-sideeffect) when accessed, the previous miscompiled code example may produce [unexpected behavior](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior).
## Compliant Solution
Eide and Regehr tested a workaround by wrapping `volatile` accesses with function calls. They describe it with the intuition that "we can replace an action that compilers empirically get wrong by a different action—a function call—that compilers can get right" \[[Eide and Regehr](AA.-Bibliography_87152170.html#AA.Bibliography-EideandRegehr)\]. For example, the workaround for the noncompliant code example would be
``` c
int vol_read_int(volatile int *vp) {
  return *vp;
}
volatile int *vol_id_int(volatile int *vp) {
  return vp;
}
const volatile int x;
volatile int y;
void foo(void) {
  for(*vol_id_int(&y) = 0; vol_read_int(&y) < 10; *vol_id_int(&y) = vol_read_int(&y) + 1) {
    int z = vol_read_int(&x);
  }
}
```
The workarounds proposed by Eide and Regehr fix many of the `volatile`-access bugs in the tested compilers. However, compilers are always changing, so critical sections of code should be compiled as if for deployment, and the compiled object code should be inspected for the correct behavior.
## Risk Assessment
The `volatile` qualifier should be used with caution in mission-critical situations. Always make sure code that assumes certain behavior when using the `volatile` qualifier is inspected at the object code level for compiler bugs.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL17-C | Medium | Probable | High | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| LDRA tool suite | ;9.7.1 | 134 S | Partially implemented |

## Bibliography

|  |  |
| ----|----|
| [Eide and Regehr] | "Volatiles Are Miscompiled, and What to Do about It" |
| [ISO/IEC 9899:2011] | Subclause 6.7.3, "Type Qualifiers" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152241) [](../c/Rec_%2002_%20Declarations%20and%20Initialization%20_DCL_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152234)
## Comments:

|  |
| ----|
| Very good rule, Andrew. Main issues are formatting-related:
    Add link to this rule from Declarations page
    The coding sections should prob still be 'Non Compliant Code Example' and 'Compliant Solution'. (I know the fault lies with the compiler, not the code, but for consistency...) And the C code is the part that should be colored, since that is what the developer can control. Finally, the compliant solution example typically 'fixes' the problem set by the NCCE.
    The Eide and Regehr links should point to an Eide & Regehr bibliographic entry on the referneces page, but we don't have one yet. So go ahead & add it to the References page, and link to it from this page.
                                        Posted by svoboda at Mar 24, 2009 11:23
                                     |
| Rose can catch violations of this rule, but I'm not sure it should...AFAICT this rule prohibits use of volatile variables, except via function calls (akin to get/set methods in Java).
Anyway this rule is less about programming practice than about compiler bugs.
                                        Posted by svoboda at Apr 08, 2009 14:20
                                     |
| If you use gcc --std=c99 things work correctly.
                                        Posted by jpincar at Apr 23, 2009 14:28
                                     |
| The cited paper is now 12 years old. Is this guideline still relevant? I'd expect the bugs to be fixed by now.
                                        Posted by jcsible at Jun 30, 2020 15:40
                                     |

