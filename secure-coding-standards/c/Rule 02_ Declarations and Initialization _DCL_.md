-   Page:
    [DCL30-C. Declare objects with appropriate storage durations](/confluence/display/c/DCL30-C.+Declare+objects+with+appropriate+storage+durations)
-   Page:
    [DCL31-C. Declare identifiers before using them](/confluence/display/c/DCL31-C.+Declare+identifiers+before+using+them)
-   Page:
    [DCL36-C. Do not declare an identifier with conflicting linkage classifications](/confluence/display/c/DCL36-C.+Do+not+declare+an+identifier+with+conflicting+linkage+classifications)
-   Page:
    [DCL37-C. Do not declare or define a reserved identifier](/confluence/display/c/DCL37-C.+Do+not+declare+or+define+a+reserved+identifier)
-   Page:
    [DCL38-C. Use the correct syntax when declaring a flexible array member](/confluence/display/c/DCL38-C.+Use+the+correct+syntax+when+declaring+a+flexible+array+member)
-   Page:
    [DCL39-C. Avoid information leakage when passing a structure across a trust boundary](/confluence/display/c/DCL39-C.+Avoid+information+leakage+when+passing+a+structure+across+a+trust+boundary)
-   Page:
    [DCL40-C. Do not create incompatible declarations of the same function or object](/confluence/display/c/DCL40-C.+Do+not+create+incompatible+declarations+of+the+same+function+or+object)
-   Page:
    [DCL41-C. Do not declare variables inside a switch statement before the first case label](/confluence/display/c/DCL41-C.+Do+not+declare+variables+inside+a+switch+statement+before+the+first+case+label)
> [!info]  
>
> **Information for Editors**  
> In order to have a new guideline automatically listed above be sure to label it [dcl](https://confluence/label/seccode/dcl) and [rule](https://confluence/label/seccode/rule).

## Risk Assessment Summary

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| DCL30-C | High | Probable | High | P6 | L2 |
| DCL31-C | Low | Unlikely | Low |  P3  |  L3  |
| DCL36-C | Medium | Probable | Medium | P8 | L2 |
| DCL37-C | Low | Unlikely | Low | P3 | L3 |
| DCL38-C | Low | Unlikely | Low | P3 | L3 |
| DCL39-C | Low | Unlikely | High | P1 | L3 |
| DCL40-C | Low | Unlikely | Medium | P2 | L3 |
| DCL41-C | Medium | Unlikely | Medium | P4 | L3 |

------------------------------------------------------------------------
[](../c/Rule%2001_%20Preprocessor%20_PRE_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152466)
## Comments:

|  |
| ----|
| I wonder if a rule (or at least recommendation) should be added to forbid (or; at least discourage) the use of extern declarations of global variables and
function prototypes in .c files, as they introduce maintainability dangers. If the definition of a global variable or the signature of a non-static function
is changed in the corresponding .c file, but not in other .c files that have extern declarations to them, the compiler will not be able to detect the
inconsistency between the two translation units. For example if the type of a global variable is change from int64_t to in32_t in the .c file that
defines it, but not in other .c files that contain a corresponding extern declaration, memory corruption will happen. Similarly, if the type of an argument of
a non-static function is changed from int32_t to int64_t in the .c file that defines it, but not in other .c files that contain a corresponding function prototype,
function invocations from these other .c files will pass garbage for the high-order 32 bits of the argument whose type was changed.
To prevent these kinds of defects, I propose the following rule:
Extern declarations of global variables and function prototypes of non-static functions must be placed only in header files. An extern declaration
for a global variable or a non-static function prototype must be declared in exactly one header file. Also, this header file must be included in the
.c file that contains the corresponding definition of the global variable or function, as well as in all other .c files that use the global variable or function.
This enables the compiler to catch inconsistencies between extern declarations or function prototypes and definitions.
                                        Posted by gerivera at Dec 18, 2010 19:50
                                     |
| sounds like DCL15-C. Declare file-scope objects or functions that do not need external linkage as static
and also
DCL19-C. Use as minimal a scope as possible for all variables and functions
                                        Posted by rcs_mgr at Dec 19, 2010 09:23
                                     |
| Maybe my comment was not completely clear, but what I was referring to was to identifiers (functions and global variables specifically)
that need to be visible in more than one translation unit. DCL15-C and DCL19-C refer to the opposite case: identifiers that do not
need to be visible in more than one translation unit.
                                        Posted by gerivera at Dec 20, 2010 10:37
                                     |
| What I think German is referring to is the mitigation we discussed in the context of the reworked Declaring the same function or object in incompatible ways (ARR31). If I recall, it was first suggested by Douglas A. Gwyn in his reply Re: [$wg14-cscg.414] comments on AI involving 7.12:
The best way to address consistency of declarations for external functions is:
Any function with external linkage (i.e. non-static) shall be declared before use by including the header that provides the only interface for it.
There are some details implicit in that wording, such that there is only one such header.
                                        Posted by martinsebor at Dec 21, 2010 19:23
                                     |
| Should not be inserted a recommendation like;VOID DCL19-CPP. Initialize automatic local variables on declaration also for the C language ?The closest recommendation i found about that is expressed in form of EXP33-C. Do not read uninitialized memory but there isn't in the guide an entry that explicitly suggest to initialize on declaration.Is there a reason for the absence of that recommendation there ? 
                                        Posted by rmartelloni at Nov 10, 2014 07:05
                                     |
| The danger of not initializing your variables at declaration is captured in referencing uninitialized memory, which is forbidden by rules EXP30-CPP and EXP33-C, as you note. DCL19-CPP is only a recommendation; you can violate it and still have secure code. Unlike EXP30-CPP and EXP33-C, whose violations result in undefined behavior.I suppose we can make a C analogue of DCL19-CPP, although it doesn't strike me as high priority.
                                        Posted by svoboda at Nov 10, 2014 10:47
                                     |
| Why doesn't it sounds as an high priority recommendation ? In my understanding and as stated there;cwe.mitre.org/data/definitions/457.html, the likelihood of exploitation using an uninitialized variable is high.isn't that a good enough reason to recommend to initialize on declaration and as a consequence prevents the chance of EXP33-C EXP30-CPP ?  
                                        Posted by rmartelloni at Nov 10, 2014 11:31
                                     |
| I think it's a reasonable recommendation (not rule) to have in C (and C++). However, the recommendations for both C and C++ are not under as active of development as the rules are, because recommendations tend to be more stylistic and are not normative.
                                        Posted by aballman at Nov 10, 2014 11:43
                                     |
| A case;against this rule is "last assigned value not used" warning provided e.g. by PC-LINT. It IMHO has more value. Sensible initialization is not always possible at the point of declaration. E.g.
T1 x;
T2 y;
if(my_condition) 
{x=a(); y=b();}
else
{x=c(); y=d();}

 Similar, and more complex, is a switch on my_condition. Static analysis tool should tell if a variable is not initialized (certainly, likely, or conceivably). Since the proposed rule is not enforced by compiler, one would need to have a static analysis tool anyway. In that case, I'd rather go with the "last assigned value not used" warning and warning "used before initialized"
![](images/icons/contenttypes/comment_16.png) Posted by arkhas at Aug 28, 2015 17:16
\|
