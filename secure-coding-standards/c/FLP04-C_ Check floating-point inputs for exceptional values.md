Floating-point numbers can take on two classes of exceptional values; infinity and NaN (not-a-number). These values are returned as the result of exceptional or otherwise unresolvable floating-point operations. (See also [FLP32-C. Prevent or detect domain and range errors in math functions](FLP32-C_%20Prevent%20or%20detect%20domain%20and%20range%20errors%20in%20math%20functions).) Additionally, they can be directly input by a user by `scanf` or similar functions. Failure to detect and handle such values can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).
NaN values are particularly problematic because the expression NaN == NaN (for every possible value of NaN) returns false. Any comparisons made with NaN as one of the arguments returns false, and all arithmetic functions on NaNs simply propagate them through the code. Hence, a NaN entered in one location in the code and not properly handled could potentially cause problems in other, more distant sections.
Formatted-input functions such as `scanf` will accept the values `INF`, `INFINITY`, or `NAN` (case insensitive) as valid inputs for the `%f` format specification, allowing malicious users to feed them directly to a program. Programs should therefore check to ensure that all input floating-point values (especially those controlled by the user) have neither of these values if doing so would be inappropriate. The `<math.h>` library provides two macros for this purpose: `isinf` and `isnan`.
## `isinf` and `isnan`
The `isinf` macro tests an input floating-point value for infinity. `isinf(val)` is nonzero if `val` is an infinity (positive or negative), and 0 otherwise.
`isnan` tests if an input is NaN. `isnan(val)` is nonzero if `val` is a NaN, and 0 otherwise.
If infinity or NaN values are not acceptable inputs in a program, these macros should be used to ensure they are not passed to vulnerable functions.
## Noncompliant Code Example
This noncompliant code example accepts user data without first validating it:
``` c
float currentBalance; /* User's cash balance */
void doDeposit() {
  float val;
  scanf("%f", &val);
  if(val >= MAX_VALUE - currentBalance) {
    /* Handle range error */
  }
  currentBalance += val;
}
```
This can be a problem if an invalid value is entered for `val` and subsequently used for calculations or as control values. The user could, for example, input the strings `"INF"`, `"INFINITY"`, or `"NAN"` (case insensitive) on the command line, which would be parsed by `scanf` into the floating-point representations of infinity and NaN. All subsequent calculations using these values would be invalid, possibly crashing the program and enabling a [denial-of-service attack](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack).
Here, for example, entering `"nan"` for `val` would force `currentBalance` to also equal `"nan"`, corrupting its value. If this value is used elsewhere for calculations, every resulting value would also be a NaN, possibly destroying important data.
### Implementation Details
The following code was run on 32-bit GNU Linux using the GCC 3.4.6 compiler. On this platform, `FLT_MAX` has the value 340282346638528859811704183484516925440.000000.
``` java
#include <stdio.h>
int main(int argc, char *argv[]) {
  float val, currentBalance=0;
  scanf("%f", &val);
  currentBalance+=val;
  printf("%f\n", currentBalance);
  return 0;
}
```
The following table shows the value of `currentBalance` returned for various arguments:

| Input | currentBalance |
| ----|----|
| 25 | 25.00000 |
| infinity | inf |
| inf | inf |
| -infinity | -inf |
| NaN | nan |
| nan | nan |
| 1e9999 | inf |
| -1e9999 | -inf |

As this example demonstrates, the user can enter the exceptional values `infinity` and `NaN`, as well as force a float's value to be infinite, by entering out-of-range floats. These entries subsequently corrupt the value of `currentBalance`. So by entering exceptional floats, an attacker can corrupt the program data, possibly leading to a crash.
## Compliant Solution
This compliant solution first validates the input float before using it. The value is tested to ensure that it is neither an infinity nor a NaN.
``` c
float currentBalance; /* User's cash balance */
void doDeposit() {
  float val;
  scanf("%f", &val);
  if (isinf(val)) {
    /* Handle infinity error */
  }
  if (isnan(val)) {
    /* Handle NaN error */
  }
  if (val >= MAX_VALUE - currentBalance) {
    /* Handle range error */
  }
  currentBalance += val;
}
```
## Exceptions
Occasionally, NaN or infinity may be acceptable or expected inputs to a program. If this is the case, then explicit checks may not be necessary. Such programs must, however, be prepared to handle these inputs gracefully and not blindly use them in mathematical expressions where they are not appropriate.
## Risk Assessment
Inappropriate floating-point inputs can result in invalid calculations and unexpected results, possibly leading to crashing and providing a [denial-of-service](BB.-Definitions_87152273.html#BB.Definitions-denial-of-serviceattack) opportunity.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FLP04-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Astrée reports potential runtime error resulting from missing checks for exceptional values. |

###  Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this recommendation on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FLP03-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | FLP04-CPP. Check floating-point inputs for exceptional values |
| CERT Oracle Secure Coding Standard for Java | FLP06-J. Check floating-point inputs for exceptional values |

## Bibliography

|  |
| ----|
| [IEEE 754] |
| [IEEE Std 1003.1:2013] |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152060) [](../c/Rec_%2005_%20Floating%20Point%20_FLP_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152252)
## Comments:

|  |
| ----|
| Michael, how is this rule distinct from FLP32-C. Prevent or detect domain and range errors in math functions?  That rule explains how to detect and handle range errors from fp operations. Extra info on how to handle range errors should go there, not in a separate rule.
                                        Posted by svoboda at Mar 19, 2009 10:32
                                     |
| I was thinking more down the lines of a malicious user deliberately feeding invalid floating point values to a program, rather than a program generating them via out-of-range inputs. I.E., the attacker himself supplies NaN or infinity as an input to a program to manipulate it, rather than relying on an unchecked floating point function to generate them.
I guess checking for this does count as detecting a range error, since NaN and infinity are "out of range" for all functions. I'll try a different rule.
                                        Posted by mrosenma at Mar 21, 2009 15:25
                                     |
| Well, FLP32 deals with range errors when doing math functions. It sounds like you are saying that scanf("%f") can produce Infinity or NaN.  I don't think this is possible, but I could be wrong, and if so, this would be a valid secure coding rule (check for bad fp values input from the user).  We do have rules to make sure you check that scanf did 'succeed' in getting valid input, but not that the input isn't NaN or some other such value.
                                        Posted by svoboda at Mar 22, 2009 10:40
                                     |
| According to http://www.opengroup.org/onlinepubs/009695399/functions/scanf.html:
"[format specifier] a,;e, f, g Matches an optionally signed floating-point number, infinity, or NaN, whose format is the same as expected for the subject sequence ofstrtod(). In the absence of a size modifier, the application shall ensure that the corresponding argument is a pointer tofloat. "Following the strtod() link:
"
The expected form of the subject sequence is an optional plus or minus sign, then one of the following:
    A non-empty sequence of decimal digits optionally containing a radix character, then an optional exponent part
    A 0x or 0X, then a non-empty sequence of hexadecimal digits optionally containing a radix character, then an optional binary exponent part
    One of INF or INFINITY, ignoring case
    One of NAN or NAN(n-char-sequenceopt), ignoring case in the NAN part, where:"
So it looks like it is possible (if that site is correct, anyway). 
                                        Posted by mrosenma at Mar 23, 2009 22:53
                                     |
| Sounds like a valid research topic then. If you can provide a reasonable NCCE that is vulnerable to a user inputting a 'weird' float, such as NAN or 1.0e999, then this will be a valid rule.
                                        Posted by svoboda at Mar 24, 2009 11:27
                                     |
| 
    The code is complete, but I'm still not convinced this is a legit rule. It needs an 'implementation details' section to demonstrate how the NCCE could be exploited. What values can the user enter to cause the NCCE to produce Infinity or NaN? And on what platform/compiler?
    The background colors of the code needs to match our styling conventions
    Neeeds a 'Risk Assessment' section
    Needs added to the Floating Point section
    Needs a 'References' section. You can include the Austin Group's findings here.
                                        Posted by svoboda at Mar 25, 2009 11:35
                                     |
| Two more points:
    Doesn't C provide an isNaN() method to check for NaN? That strikes me as a better test then x!=x. Also is there an isInfinity() function?
    Assuming a user can enter 'invalid' values, I'm guessing some apps will be perfectly happy accepting Infinity or NaN. So this is less a rule about preventing those values; it is more of a rec: The user may enter those values, you may want to check for them; here's how.
                                        Posted by svoboda at Mar 25, 2009 16:31
                                     |
| 
    The code is complete, but I'm still not convinced this is a legit rule. It needs an 'implementation details' section to demonstrate how the NCCE could be exploited. What values can the user enter to cause the NCCE to produce Infinity or NaN? And on what platform/compiler?
    The compliant code needs to be updated to check for both Infinity and NaN
    The References section should include the Austin Group's findings from your comment. Does C99 discuss Infinity & NaN?
                                        Posted by svoboda at Mar 26, 2009 10:57
                                     |
| I'm not sure what you mean "demonstrate how the NCCE could be exploited". If the user enters the strings "nan", "inf", or "infinity" on the command line during a call to scanf, the returned floating point variable will be NaN (in the first case) or infinity (in the other two). So the user can directly enter these values in the NCCE. This appears to be inherent in the definition of scanf and the like, so I think it's platform-independent.
C99 does discuss Infinity and NaN. 
                                        Posted by mrosenma at Mar 26, 2009 15:25
                                     |
| I guess I want to see a working program that takes a float from the user. The user enters infinity or NaN, or simply a large number (eg 1e1000000), confounding the program. Before you wrote this rule, I thought scanf wouldn't accept 'infinity' as legit fp input, I'm sure others will be equally skeptical.
WRT C99, some authoritative documentation saying "yes scanf() can accept 'infinity' as a fp input" would be helpful to convince the skeptics. Citing the Austin Group (from your earlier comment) would be good, citing C99 would be even better.
                                        Posted by svoboda at Mar 26, 2009 15:33
                                     |
| One last note (in addition to the others). If your code has "current += balance', you probably want to range-check balance, to make sure the user didn't enter something like FLOAT_MAX to screw up the balance.
                                        Posted by svoboda at Mar 27, 2009 09:58
                                     |
| The rule adequately illustrates the danger of a user entering Infinity or NaN, but should also illustrate what happens if the user enters a large number, such as 1e1000000. You'll need an 'implementation details' section here since the maximum value a user can enter is implementation-defined.
                                        Posted by svoboda at Mar 28, 2009 08:44
                                     |
| Michael, the 'Implementation Details' section needs to not be theoretical. You need to write a small program that exposes the vul, compile it on a C99-compliant compiler (GCC or MSVC works), and run it. The Imp.Details section should come after your code and say "On platform X with compiler Y this program produces: Z."  Including that platform's value of FLOAT_MAX will probably be necessary.  Finally the Imp.Details section should follow a NonCompliantCodeExample section which has your small program, and the theory of why it is bad. So the ImpDetails section is useful in informing the reader "This is a real vul, not just theory".
Your current non-compliant code example can serve as the core for this small program, if you wish.
                                        Posted by svoboda at Mar 28, 2009 20:03
                                     |
| Michael, thanks for the implementation details. One last question, which version of Linux & GCC did you use? (and 32-bit or 64-bit platform)?
That said, you'll get full credit for this assignment.
                                        Posted by svoboda at Mar 29, 2009 11:03
                                     |

