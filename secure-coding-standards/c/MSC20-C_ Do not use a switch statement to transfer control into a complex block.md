A `switch` statement can be mixed with a block of code by starting the block in one case label, then having another case label within the block. The block can be pictured as spanning more than one case statement.
Subclause 6.8.4.2, paragraph 2, of the C Standard \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\] says,
> If a switch statement has an associated case or default label within the scope of an identifier with a variably modified type, the entire switch statement shall be within the scope of that identifier.<sup>154</sup>

Footnote 154 says:
> That is, the declaration either precedes the switch statement, or it follows the last case or default label associated with the switch that is in the block containing the declaration.

Note that the standard does not disallow jumping via `goto` or `switch` into loops that do not involve variably modified type identifiers. Consequently, loops and other blocks can be freely intermixed with `switch` statements. Unfortunately, such intermixing creates code that is, at best, confusing and unclear in what it does, which can cause undesirable behavior.
The examples here fall under the exception **MSC17-C-EX2** in [MSC17-C. Finish every set of statements associated with a case label with a break statement](MSC17-C_%20Finish%20every%20set%20of%20statements%20associated%20with%20a%20case%20label%20with%20a%20break%20statement).
## Noncompliant Code Example
This example shows the use of the `switch` statement to jump into a `for` loop:
``` c
int f(int i) {
  int j=0;
  switch (i) {
    case 1:
      for(j=0;j<10;j++) {
      /* No break; process case 2 as well */
    case 2: /* switch jumps inside the for block */
        j++;
      /* No break; process case 3 as well */
    case 3:
        j++;
      }
      break;
  default:
    /* Default action */
    break;
  }
  return j;
}
```
### Implementation Details
When `i = 1`, the entire `for` loop is executed. When `i = 2`, two increments to `j` are made before the loop starts. When `i = 3`, one increment to `j` is made before the loop starts. The default case is no loop. Consequently, the function has the following behavior:

| i | f(i) |
| ----|----|
| 1 | 12 |
| 2 | 12 |
| 3 | 11 |
| Other values | 0 |

## Compliant Solution
The compliant solution separates the `switch` and `for` blocks:
``` c
int f(int i) {
  int j=0;
  switch (i) {
    case 1:
      /* No break; process case 2 as well */
    case 2:
      j++;
      /* No break; process case 3 as well */
    case 3:
      j++;
      break;
    default:
      /* Default action */
      return j;
  }
  for(j++;j<10;j++) {
    j+=2;
  }
  return j;
}
```
## Noncompliant Code Example (Duff's Device)
[Duff's device](http://www.lysator.liu.se/c/duffs-device.html) is a curious optimization applied to code intended to perform a serial copy. That is, it copies a series of bytes into one memory output in turn. A simple code to do this would be as follows:
``` java
size_t count; /* Must be nonzero */
char *to;     /* Output destination */
char *from;   /* Points to count bytes to copy */
do {
  *to = *from++;     /*
                      * Note that the "to" pointer 
                      * is NOT incremented.
                      */
} while (--count > 0);
```
However, this code might be unacceptably slow because the `while` condition is performed `count` times. The classic code for Duff's device unrolls this loop to minimize the number of comparisons performed:
``` c
int n = (count + 7) / 8;
switch (count % 8) {
  case 0: do { *to = *from++;
  case 7:      *to = *from++;
  case 6:      *to = *from++;
  case 5:      *to = *from++;
  case 4:      *to = *from++;
  case 3:      *to = *from++;
  case 2:      *to = *from++;
  case 1:      *to = *from++;
          } while (--n > 0);
}
```
In this code, the first iteration of the loop is subject to the `switch` statement, so it performs `count % 8` assignments. Each subsequent iteration of the loop performs 8 assignments. (Being outside the loop, the `switch` statement is ignored.) Consequently, this code performs `count` assignments, but only `n` comparisons, so it is usually faster.
The code is widely considered to be valid C and C++ and is supported by all compliant compilers. When describing Duff's device, the creator \[[Duff 1988](http://AA.%20Bibliography#Duff%2088)\] noted,
> Many people . . . have said that the worst feature of C is that switches don't break automatically before each case label. This code forms some sort of argument in that debate, but I'm not sure whether it's for or against.

## Compliant Solution (Duff's Device)
This is an alternative [implementation](http://BB.%20Definitions#implementation) of Duff's device, which separates the `switch` statement and loop:
``` c
int n = (count + 7) / 8;
switch (count % 8) {
  case 0: *to = *from++; /* Fall through */
  case 7: *to = *from++; /* Fall through */
  case 6: *to = *from++; /* Fall through */
  case 5: *to = *from++; /* Fall through */
  case 4: *to = *from++; /* Fall through */
  case 3: *to = *from++; /* Fall through */
  case 2: *to = *from++; /* Fall through */
  case 1: *to = *from++; /* Fall through */
}
while (--n > 0) {
  *to = *from++;
  *to = *from++;
  *to = *from++;
  *to = *from++;
  *to = *from++;
  *to = *from++;
  *to = *from++;
  *to = *from++;
}
```
## Risk Assessment

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC20-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | switch-label | Fully checked |
| CodeSonar | 8.3p0 | LANG.STRUCT.SW.MPC | Misplaced case |
| ECLAIR | 1.2 | CC2.MSC20 | Fully implemented |
| Helix QAC | 2024.4 | C2019 |  |
| LDRA tool suite | 9.7.1 | 245 S | Fully implemented |
| PC-lint Plus | 1.4 | 646, 9055 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC20-C | Checks for situations where switch label is not at the outermost level of switch statement body (rec. fully covered) |
| RuleChecker | 24.04 | switch-label | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | S1036 |  |

## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC20-CPP. Do not use a switch statement to transfer control into a complex block |
| ISO/IEC TR 24731-1:2007 |  |
| MISRA C:2012 | Rule 16.2 (required) |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Subclause 6.8.6.1, "The goto Statement" |
| [Duff 1988] | Tom Duff on Duff's Device |

------------------------------------------------------------------------
[](../c/MSC19-C_%20For%20functions%20that%20return%20an%20array,%20prefer%20returning%20an%20empty%20array%20over%20a%20null%20value) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152327)
## Comments:

|  |
| ----|
| What is the definition of a "complex block"?
                                        Posted by jimg at Feb 04, 2013 13:40
                                     |
| The C11 standard has new text regarding how you can mix blocks and switch statements, so I updated the quotation that describes what is permitted.
                                        Posted by svoboda at Feb 04, 2013 14:05
                                     |

