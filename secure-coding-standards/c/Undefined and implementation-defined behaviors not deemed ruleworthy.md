1.  Do not use identifiers that are already declared
    1.  e.g., don't name a variable `errno`
2.  Do not pass functions invalid values
3.  For floating point exception functions, only pass `0` or bitwise OR of floating point macros
4.  Do not modify the string returned by `setlocale()` or `localeconv()`
5.  Do not call `setjmp()` in stupid places (eg. header files)
6.  Do not call `longjmp()` before calling `setjmp()`
7.  Do not call `va_start()` with a parameter declared with the register storage class, of array type, or a type that isn't compatible with the type after default argument promotions
8.  Do not try to get the address constant of a bit-field
    1.  e.g., do not: `&(t.`*`member-designator`*`)`
9.  When functions fail, data structures often have indeterminate contents
    1.  e.g., `wcsxfrm()`, `wcsftime()`, `mbrtowc()`, `wcrtomb()`, `strxfrm()`, `strftime()`
10. Do not mismatch multibyte conversion states with character sequences in another state
11. Do not change the `LC_CTYPE` in between calls to character conversion functions
12. Only pass functions the type they ask for
    1.  We might already have a rule for this, but I couldn't find it
13. If the result of a function cannot be represented, the behavior is [undefined](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior)
    1.  e.g., `abs()`, `labs()`, `llabs()`, `div()`, `ldiv()`, `lldiv()`.
14. Do not cast a `void` expression to another type.
15. Ensure expressions are compatible with the return types of the functions they call.
16. Source files should always have a trailing newline.
17. Constant expressions must consist entirely of constant components.
18. Do not access anything through an address constant.
19. Do not declare a function with a type qualifier
20. Do not declare an integer constant macro with a non-integer value, or one out of limits
21. Do not use inconsistent comparison functions
22. Do not use `bsearch()` on an array not in the proper order
23. In a header name, do not have the characters ', \\ ", //, or /\* in between the \< and \> or the characters ', \\ //, or /\* in between the quotes.
24. Do not compare pointers that point to different objects.
25. Do not have operations with side effects within an initialization list.
## Comments:

|  |
| ----|
| I would find this list useful if I could rely on it being up to date – is it? (See below). If it is, and/or if we are to commit to keeping it up to date, may I suggest that a brief rationale be provided for each item on the list?
    Item 1 is the subject of DCL37-C. Do not use identifiers that are reserved for the implementation and the example specifically addressed in ERR31-C. Don't redefine errno.
    The last part of Item 7 (Do not call va_start() with a parameter [...whose] type that isn't compatible with the type after default argument promotions) is the subject of DCL10-C. Maintain the contract between the writer and caller of variadic functions and DCL11-C. Understand the type issues associated with variadic functions.
    Items 10, 11, 15, 16, and 25 seem fairly important and failing to observe them may lead to undefined or unspecified behavior. What is the rationale for explicitly excluding them?
    I'm not sure I understand Item 21. What are "inconsistent comparison functions?"
    Item 24 is the subject of ARR36-C. Do not subtract or compare two pointers that do not refer to the same array.
                                        Posted by martinsebor at Jan 17, 2010 13:10
                                     |
| I doubt this link is up to date.  This is a list put together by a couple of my students (now graduated) after I asked them to go through the standard and account for all the undefined behavior.
There may be undefined behaviors listed here that should be addressed, as you suggest.  
As for maintaining this, I don't think that is necessarily a bad idea.  It may make sense to combine this with CC. Undefined Behavior.  This way we can easily account for all 191 explicit undefined behaviors being covered by one or more rules, or a rationale for not including it.  This will also make it easier to maintain, particularly because it becomes part of the document and not just a process step.
Some other suggestions... perhaps we should make close to CC. Undefined Behavior closer to Annex J and included unspecified, undefined, and implementation defined behaviors.  Even cooler still, we should use the new C1X Annex L "Analyzability" that distinguishes between undefined behaviors and critically undefined behaviors for security purposes (the proposal for this Annex was co-authored by Tom Plum and myself).  (I just thought of this for the first time, but we should consider proposing that WG14 reorganize Annex J the same way).
Another small point about CC. Undefined Behavior.  The links right now to the guidelines is only to the identifier.  The problem with this approach is that if the identifier name changes, the links do no ordinarily update.  This is why we usually just put the name of the rule between [] brackets.  Visually I would prefer just referencing the ID's, but the advantage in maintenance is significant.
                                        Posted by rcs at Jan 17, 2010 13:49
                                     |
| My plan for CC. Undefined Behavior has been to: first do a review of all the cases addressed by existing guidelines, then add new guidelines for cases that aren't addressed but should be, and finally mark up all the cases that we feel do not need guidelines to say so. If some of your students would be willing to help with this project for extra credit that'd be fantastic 
Once this is done (assuming someone still has some energy/cycles left in them), I'm hoping for us to do as you suggest and add another similar page and table for Unspecified Behavior, and eventually perhaps also for Implementation-Defined Behavior.
It would be awesome if we could do the same for C++ as well but given the size of it that might be just a pipe dream...
I understand your concern with the links. I considered it but felt that including the full text of each guideline would diminish the readbility of the table by bloating it with excessive text. The text of each guideline does pop up when you hover the mouse over it.
On the subject or links and guideline IDs, what was the rationale for including the full text of title in each instead of just the ID? Using just the ID would obviate all these issues and make it easier for other projects to create more permanent links to the guidelines.
                                        Posted by martinsebor at Jan 18, 2010 18:04
                                     |

