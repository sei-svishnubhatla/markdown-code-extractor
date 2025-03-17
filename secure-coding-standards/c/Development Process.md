The development of a coding standard for any programming language is a difficult undertaking that requires significant community involvement. The following development process has been used to create this standard:
1.  Rules and recommendations for a coding standard are solicited from the communities involved in the development and application of each programming language, including the formal or de facto standards bodies responsible for the documented standard.
2.  These rules and recommendations are edited by members of the CERT technical staff for content and style and placed on this wiki for comment and review.
3.  The user community may then comment on the publicly posted content using threaded discussions and other communication tools. Once a consensus develops that the rule or recommendation is appropriate and correct, the final rule is incorporated into an officially released version of the secure coding standard.
Early drafts of the CERT C Secure Coding Standard have been reviewed by the [ISO/IEC JTC1/SC22/WG14](http://www.open-std.org/jtc1/sc22/wg14/) international standardization working group for the C programming language and by other industry groups as appropriate.
## Comments:

|  |
| ----|
| Is there a section that describes the process for updating the Wiki? In particular, what is automated and what needs to be done manually?
For example, when moving or renaming a guideline or changing its Risk Assessment attributes, what pages and/or sections does one need to update by hand and which ones can be left to the NavBot?
                                        Posted by martinsebor at Jan 12, 2010 22:04
                                     |
| Sorry, no, there isn't. (unless our Wiki software, Confluence has such documentation)
Here's my list (from observation) of what gets done automagically for you:
    If you change a wiki page's title, then all references to that page get the title updated.
    We have scripts to change the Prev/Top/Next links at the bottom of each page
    We have scripts to make simple global search/replace edits (eg change "nonvolatile" to "non-volatile")
That's it, AFAIK.
                                        Posted by svoboda at Jan 12, 2010 22:23
                                     |
| Okay, let me try to list some of the things that need to be updated:
Adding a New Guideline
    Add a reference to the guideline to its corresponding section.
    Copy the guideline's Risk Assessment table to the corresponding section's Risk Assessment Summary.
Removing an Existing Guideline
    Remove a reference to the guideline from its corresponding section.
    Remove the guideline's entry from its corresponding section's Risk Assessment Summary.
    Add a reference to the guideline to 6 The Void section.
                                        Posted by martinsebor at Jan 14, 2010 21:03
                                     |
| For some reason, we have a Todo page which has some process hints:
https://www.securecoding.cert.org/confluence/display/seccode/TODO+List 
One of these relates to removing an existing guideline, which is to apply a "deleteme" label when you really want something gone.
Right now, only I have privileges to delete guidelines, so this is one mechanism for getting me to do something.  The other is talking to my wife.  8^)
                                        Posted by rcs at Jan 15, 2010 09:38
                                     |

