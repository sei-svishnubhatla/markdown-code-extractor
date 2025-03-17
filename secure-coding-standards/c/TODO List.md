# Tags (Labels)

| Tag | Meaning |
| ----|----|
| section  | Pages that form the main sections of this standard and that are listed in the Section Index on the SEI CERT C Coding Standard page. |
| links-to-void  | Guidelines with links to a rule in 6 The Void. The link should be removed. |
| update-checker  | Guidelines that have been significantly changed since the checker was coded. The checker needs updating. |
| incomplete  | Pages that need work. |
| deleteme  | Pages that need to be deleted. See also void  below. |
| citations-incomplete  | Pages that have problems with the citations at the bottom. |
| sidebar  | Pages with comments that might make good sidebars. |
| exportable-c  | Guidelines in other CERT secure coding standards (residing in other Wiki spaces) that might make good C guidelines. Port to C those rules that are truly applicable. |
| exportable-java  | Guidelines that might be candidates for adoption in the SEI CERT Oracle Coding Standard for Java. |
| void  | Pages tagged for elimination from the standard and that are listed in 6 The Void. |

## ROSE-Specific Tags (Labels)
Pages now have tags (also known as
[Labels](http://confluence.atlassian.com///display/DOC/Working%20with%20Labels%20Overview)
) to indicate the status of their corresponding checker in Compass Rose:

| Tag | Meaning |
| ----|----|
| rose-complete | ROSE catches all violations |
| rose-partial | ROSE catches some violations |
| rose-possible | ROSE could catch some or all violations, but doesn't yet. |
| rose-gcc | ROSE doesn't catch violations, but will soon, GCC catches violations |
| unenforceable | These rules can't be checked automatically. |
| rose-nonapplicable | These rules could be checked automatically in theory, but not by ROSE. |
| rose-na-macros | ROSE could check these rules if it recognized macro usage. |
| rose-na-multiple-files | ROSE could check these rules if it operated on multiple files at once. |
| rose-false-positive | ROSE could enforce this rule, but could not avoid catching some false positives. |

At this point, all rules should have one of these tags. That is, they should be completely or partially checked by ROSE, or they should be marked 'rose-possible', in that we will try to check them with ROSE, or they should have one of the nonapplicable tags indicating we don't think they can be checked with ROSE.
------------------------------------------------------------------------
It might also be worth giving [these](https://www.securecoding.cert.org/confluence/display/seccode/Undefined+and+implementation-defined+behaviors+not+deemed+ruleworthy) another look.
------------------------------------------------------------------------
## Comments:

|  |
| ----|
| There are no pages tagged citations-incomplete , only one page tagged by each of links-to-void , delete-me , and rose-na-exptypes , and just two tagged update-checker . Are any of these labels still being used or potentially useful, or should they be eliminated?
                                        Posted by martinsebor at Feb 03, 2010 15:07
                                     |
| I think all these tags are now eliminated, except for update-checker. Which is useful, and described in this page.
                                        Posted by svoboda at Feb 03, 2010 16:32
                                     |
| ;seI'm going to start using these again as we prepare for the second edition.
                                        Posted by rcs at Sep 15, 2013 05:55
                                     |

