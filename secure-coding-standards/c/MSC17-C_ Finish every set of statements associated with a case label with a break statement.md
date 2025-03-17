A `switch` statement consists of several case labels, plus a default label. The default label is optional but recommended. (See [MSC01-C. Strive for logical completeness](MSC01-C_%20Strive%20for%20logical%20completeness).) A series of statements following a case label conventionally ends with a `break` statement; if omitted, control flow falls through to the next case in the `switch` statement block. Because the `break` statement is not required, omitting it does not produce compiler diagnostics. If the omission was unintentional, it can result in an unexpected control flow.
## Noncompliant Code Example
In this noncompliant code example, the case where `widget_type` is `WE_W` lacks a `break` statement. Consequently, statements that should be executed only when `widget_type` is `WE_X` are executed even when `widget_type` is `WE_W`.
``` c
enum WidgetEnum { WE_W, WE_X, WE_Y, WE_Z } widget_type;
widget_type = WE_X;
switch (widget_type) {
  case WE_W:
    /* ... */
  case WE_X:
    /* ... */
    break;
  case WE_Y: 
  case WE_Z:
    /* ... */
    break;
  default: /* Can't happen */
     /* Handle error condition */
}
```
## Compliant Solution
In this compliant solution, each sequence of statements following a case label ends with a `break` statement:
``` c
enum WidgetEnum { WE_W, WE_X, WE_Y, WE_Z } widget_type;
widget_type = WE_X;
switch (widget_type) {
  case WE_W:
    /* ... */
    break;
  case WE_X:
    /* ... */
    break;
  case WE_Y: 
  case WE_Z:
    /* ... */
    break;
  default: /* Can't happen */
     /* Handle error condition */
}
```
A `break` statement is not required following the case where `widget_type` is `WE_Y` because there are no statements before the next case label, indicating that both `WE_Y` and `WE_Z` should be handled in the same fashion.
A `break` statement is not required following the default case because it would not affect the control flow.
## Exceptions
**MSC17-C-EX1:** The last label in a `switch` statement requires no final `break`. It will conventionally be the `default` label.
**MSC17-C-EX2:** When control flow is intended to cross statement labels, it is permissible to omit the `break` statement. In these instances, the unusual control flow must be made clear, such as by adding the `[[fallthrough]]` C2x attribute, the `__attribute__((__fallthrough__))` GNU extension, or a simple comment.
``` c
enum WidgetEnum { WE_W, WE_X, WE_Y, WE_Z } widget_type;
widget_type = WE_X;
switch (widget_type) {
  case WE_W:
    /* ... */
    /* No break; fall through to the WE_X case */
  case WE_X:
    /* ... */
    break;
  case WE_Y: case WE_Z:
    /* ... */
    break;
  default: /* Can't happen */
     /* Handle error condition */
}
```
## Risk Assessment
Failure to include `break` statements leads to unexpected control flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC17-C | Medium | Likely | Low | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | switch-clause-breakswitch-clause-break-continue
switch-clause-break-return | Fully checked |
| CodeSonar | 8.3p0 | LANG.STRUCT.SW.MB | Missing break |
| Compass/ROSE |  |  |  |
| Coverity | 2017.07 | MISSING_BREAK | Can find instances of missing break statement between cases in switch statement |
| ECLAIR | 1.2 | CC2.MSC17 | Fully implemented |
| Helix QAC | 2024.4 | C2003 |  |
| Klocwork | 2024.4 | MISRA.SWITCH.WELL_FORMED.BREAK.2012 |  |
| LDRA tool suite | 9.7.1 | 62 S | Fully implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MSC17-a | Missing break statement between cases in a switch statement |
| PC-lint Plus | 1.4 | 616, 825 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MSC17-C | Checks for missing break of switch case (rec. fully covered) |
| PVS-Studio | 7.35 | V796 |  |
| RuleChecker | 24.04 | switch-clause-breakswitch-clause-break-continue
switch-clause-break-return | Fully checked |
| SonarQube C/C++ Plugin | 3.11 | NonEmptyCaseWithoutBreak |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC17-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MSC18-CPP. Finish every set of statements associated with a case label with a break statement |
| CERT Oracle Secure Coding Standard for Java | MSC52-J. Finish every set of statements associated with a case label with a break statement |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152050) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](../c/MSC18-C_%20Be%20careful%20while%20handling%20sensitive%20data,%20such%20as%20passwords,%20in%20program%20code)
## Comments:

|  |
| ----|
| I disagree with MSC17-EX1 for two reasons: 1) I don't think we should speak to conventions in this case. I've seen coding standards that require the default statement to be the first statement in the switch, for instance.; We don't know what "most programmers" do, basically.  2) Leaving off the break on the last case (be it case or default) makes the code more error prone when refactoring because adding a subsequent case would then possibly run afoul of the same recommendation.
                                        Posted by aballman at Sep 17, 2013 10:26
                                     |
| Instead of just saying "In these instances, the unusual control flow must be explicitly documented" and using arbitrary freeform comments, we should say to use the comment /* FALLTHROUGH */ for intentional fallthroughs so that GCC's -Wimplicit-fallthrough warning can be used to catch accidental fallthroughs.
                                        Posted by jcsible at Jun 30, 2020 11:59
                                     |
| Please keep in mind that fallthrough comments are not portable (GCC supports them, Clang has recently refused to), are somewhat arbitrary (some different capitalizations and whitespaces are supported), and are lost when you do operations like preprocess to a file and then compile that output. Also, there are other approaches to consider recommending, like;[[fallthrough]] in C2x or __attribute__((fallthrough)), etc.
                                        Posted by aballman at Jun 30, 2020 12:10
                                     |
| [[fallthrough]] would definitely be my preferred choice once C2x becomes official. For current code that's meant to be portable to Windows, I prefer a comment over __attribute__ since MSVC will choke on the latter unless you #define it away (in violation of DCL37-C. Do not declare or define a reserved identifier), but compilers that don't recognize the fallthrough comment will still be fine, since it's still just a comment.I think it would make sense to mention all of the approaches, though, and briefly mention the pros and cons of each.
                                        Posted by jcsible at Jun 30, 2020 12:27
                                     |
| I agree that listing several options and discussing the pros and cons of each would be reasonable.
                                        Posted by aballman at Jun 30, 2020 12:33
                                     |
| I would also encourage a discussion about nonportable alternatives. I'll add that MSC17-C-EX2 is the reason that this is a recommendation, not a rule. We don't expect analysis tools to parse comments and so we believe that they cannot currently distinguish intentional vs unintentional fallthrough.If the [[fallthrough]] attribute gets accepted into C1x, then we can not only promote it, but we could promote this recommendation to a rule, and add "if you use an old compiler then you can't comply with this rule, good luck".BTW MSVC has supported the [[fallthrough]] attribute since v15.3https://docs.microsoft.com/en-us/cpp/cpp/attributes?view=vs-2019
                                        Posted by svoboda at Jul 06, 2020 10:47
                                     |
| I also wanted to thank Aaron Ballmanfor promoting attributes (including [[fallthrough]]) in C. As he knows, I tried promoting them in 2010 and failed, but Aaron's effort is more likely to succeed:http://www.open-std.org/jtc1/sc22/wg14/www/docs/n2269.pdf
                                        Posted by svoboda at Jul 06, 2020 10:52
                                     |
| FWIW, the attribute syntax and the;[[fallthrough]] attribute were both adopted for C2x (and is available in both Clang and GCC). While it's possible they get pulled out of the standard before we publish, I'd be surprised as they were adopted with strong consensus and we'd need stronger consensus to remove.
                                        Posted by aballman at Jul 06, 2020 12:24
                                     |

