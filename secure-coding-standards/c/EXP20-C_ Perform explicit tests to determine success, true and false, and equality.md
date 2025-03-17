Perform explicit tests to determine success, true/false, and equality to improve the readability and maintainability of code and for compatibility with common conventions.
In particular, do not default the test for nonzero. For instance, suppose a `foo()` function returns 0 to indicate failure or a nonzero value to indicate success. Testing for inequality with 0,
``` c
if (foo() != 0) ...
```
is preferable to
``` c
if (foo()) ...
```
despite the convention that 0 indicates failure. Explicitly testing for inequality with 0 benefits maintainability if `foo()` is later modified to return −1 rather than 0 on failure.
This recommendation is derived from and considers the implications of the following common conventions:
1.  Functions return 0 if false and nonzero if true [\[StackOvflw 2009](AA.-Bibliography_87152170.html#AA.Bibliography-StackOvflw09)\].
2.  Function failures can typically be indicated by −1 or any nonzero number.
3.  Comparison functions (such as the standard library function `strcmp()`, which has a trinary return value) return 0 if the arguments are equal and nonzero otherwise (see [strcmp function](http://elearning.algonquincollege.com/coursemat/pincka/dat2219d.w03/cref/cref11.htm#ref03)).
## Noncompliant Code Example
In this noncompliant code example, `is_banned()` returns 0 if false and nonzero if true:
``` c
LinkedList bannedUsers;
int is_banned(User usr) {
  int x = 0;
  Node cur_node = (bannedUsers->head);
  while (cur_node != NULL) {
    if(!strcmp((char *)cur_node->data, usr->name)) {
      x++;
    }
    cur_node = cur_node->next;
  }
  return x;
}
void processRequest(User usr) {
  if(is_banned(usr) == 1) {
    return;
  }
  serveResults();
}
```
If a banned user is listed twice, the user is granted access. Although `is_banned()` follows the common convention of returning nonzero for true, `processRequest` checks for equality only with 1.
## Compliant Solution
Because most functions guarantee a return value of nonzero only for true, the preceding code is better written by checking for inequality with 0 (false), as follows:
``` c
LinkedList bannedUsers;
int is_banned(User usr) {
  int x = 0;
  Node cur_node = (bannedUsers->head);
  while(cur_node != NULL) {
    if (strcmp((char *)cur_node->data, usr->name)==0) {
      x++;
    }
    cur_node = cur_node->next;
  }
  return x;
}
void processRequest(User usr) {
  if (is_banned(usr) != 0) {
    return;
  }
  serveResults();
}
```
## Noncompliant Code Example
In noncompliant code, function status can typically be indicated by returning −1 on failure or any nonnegative number on success. This is a common convention in the standard C library, but it is discouraged in [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).
Although failures are frequently indicated by a return value of 0, some common conventions may conflict in the future with code in which the test for nonzero is not explicit. In this case, defaulting the test for nonzero welcomes bugs if and when a developer modifies `validateUser()` to return an error code or −1 rather than 0 to indicate a failure (all of which are also common conventions).
``` c
int validateUser(User usr) {
  if(listContains(validUsers, usr)) {
    return 1;
  }
  return 0;
}
void processRequest(User usr, Request request) {
  if(!validateUser(usr)) {
    return "invalid user";
  }
  else {
    serveResults();
  }
}
```
Although the code will work as intended, it is possible that a future modification will result in the following:
``` c
errno_t validateUser(User usr) {
  if(list_contains(allUsers, usr) == 0) {
    return 303; /* User not found error code */
  }
  if(list_contains(validUsers, usr) == 0) {
    return 304; /* Invalid user error code */
  }
  return 0;
}
void processRequest(User usr, Request request) {
  if(!validateUser(usr)) {
    return "invalid user";
  }
  else {
    serveResults();
  }
}
```
In this code, the programmer intended to add error code functionality to indicate the cause of a [validation](BB.-Definitions_87152273.html#BB.Definitions-validation) failure. The new code, however, validates any invalid or nonexisting user. Because there is no explicit test in `processRequest()`, the logical error is not obvious and seems correct by certain conventions.
## Compliant Solution
This compliant code is preferable for improved maintenance. By defining what constitutes a failure and explicitly testing for it, the behavior is clearly implied, and future modifications are more likely to preserve it. If a future modification is made, such as in the previous example, it is immediately obvious that the `if` statement in `processRequest()` does not correctly utilize the specification of `validateUser()`.
``` c
int validateUser(User usr) {
  if(list_contains(validUsers, usr)) {
    return 1;
  }
  return 0;
}
void processRequest(User usr, Request request) {
  if(validateUser(usr) == 0) {
    return "invalid user";
  }
  else {
    serveResults();
  }
}
```
## Noncompliant Code Example
Comparison functions (such as the standard library `strcmp()` function) return 0 if the arguments are equal and nonzero otherwise.
Because many comparison functions return 0 for equality and nonzero for inequality, they can cause confusion when used to test for equality. If someone were to switch the following `strcmp()` call with a function testing for equality, but the programmer did not follow the same convention as `strcmp()`, the programmer might instinctively just replace the function name. Also, when quickly reviewed, the code could easily appear to test for inequality.
``` c
void login(char *usr, char *pw) {
  User user = find_user(usr);
  if (!strcmp((user->password),pw)) {
    grantAccess();
  }
  else {
    denyAccess("Incorrect Password");
  }
}
```
The preceding code works correctly. However, to simplify the login code or to facilitate checking a user's password more than once, a programmer can separate the password-checking code from the login function in the following way:
``` c
int check_password(User *user, char *pw_given) {
  if (!strcmp((user->password),pw_given)) {
    return 1;
  }
  return 0;
}
void login(char *usr, char *pw) {
  User user = find_user(usr);
  if (!check_password(user, pw)) {
    grantAccess();
  }
  else {
    denyAccess("Incorrect Password");
  }
}
```
In an attempt to leave the previous logic intact, the developer just replaces `strcmp()` with a call to the new function. However, doing so produces incorrect behavior. In this case, any user who inputs an incorrect password is granted access. Again, two conventions conflict and produce code that is easily corrupted when modified. To make code maintainable and to avoid these conflicts, such a result should never be defaulted.
## Compliant Solution
This compliant solution, using a comparison function for this purpose, is the preferred approach. By performing an explicit test, any programmer who wishes to modify the equality test can clearly see the implied behavior and convention that is being followed.
``` c
void login(char *usr, char *pw) {
  User user = find_user(usr);
  if (strcmp((user->password),pw) == 0) {
    grantAccess();
  }
  else {
    denyAccess("Incorrect Password");
  }
}
```
## Risk Assessment
Code that does not conform to the common practices presented is difficult to maintain. Bugs can easily arise when modifying helper functions that evaluate true/false or success/failure. Bugs can also easily arise when modifying code that tests for equality using a comparison function that obeys the same conventions as standard library functions such as `strcmp`.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| EXP20-C | Medium | Probable | Low | P12 | L1 |

### Automated Detection

|  |  |  |  |
| ----|----|----|----|
| Tool | Version | Checker | Description |
| Astrée | 24.04 |  | Supported indirectly via MISRA C:2004 Rule 13.2. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-EXP20 | Fully implemented |
| Helix QAC | 2024.4 | C3344,;
C4116 |  |
| LDRA tool suite | 9.7.1 | 114 S | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-EXP20-aCERT_C-EXP20-b
 | Avoid comparing values with the 'TRUE' identifier using equality operators ("==", "!=")Tests of a value against zero should be made explicit, unless the operand is effectively Boolean |
| PC-lint Plus | 1.4 | 697 | Partially supported: reports comparisons of Boolean values to constants other than 0 |

## Bibliography

|  |  |
| ----|----|
| [StackOvflw 2009] | "Should I Return TRUE/FALSE Values from a C Function?" |

------------------------------------------------------------------------
[](../c/EXP19-C_%20Use%20braces%20for%20the%20body%20of%20an%20if,%20for,%20or%20while%20statement) [](../c/Rec_%2003_%20Expressions%20_EXP_) [](../c/Rec_%2009_%20Input%20Output%20_FIO_)
## Comments:

|  |
| ----|
| 
    What exactly is 'defaulting the test for non-zero'? The intro needs to define this phrase, perhaps with a code sample. I presume it means using an expression in an if or while statement that isn't either (1) explicitly boolean, or (2) a comparison or equality operator.
    In general we try to focus on security issues and avoid style issues. I think this rule can have security issues (esp if you can cite code that was exploitable due to violating this rule), but you need to make it clear that this is a security issue, in order to convince those who think this is purely stylistic.
    Speaking of style, although we do not promote a single brace style, we use K&R brace style for our code samples here for consistency...please use it.
    Also text explaining what the code does or why it fails belongs outside the code sample, not as comments within.
    I suspect forcing programmers to #define FAIL as 0 and use FAIL will never fly. Using 0 as a constant for failure is acceptable in the C community for pre-C99. C99 provides boolean types, and you should be promoting them instead.
    Your 3rd CS should abide by PRE00-C. Prefer inline or static functions to function-like macros . Personally I think 'if (strcmp( str1, str2) == 0)...' is sufficient.
    I think you should elaborate on the 2nd NCCE/CS...perhaps with a more concrete example. Also it should come first in the rule, as it is considerably stronger than the others.
                                        Posted by svoboda at Mar 15, 2010 20:48
                                     |
| David has some interesting points.  I started reading this and thought I wouldn't like it, but I actually think you should go ahead and finish developing this guideline.  
I agree with David that this could easily be considered a style guideline.  As such, you should follow David's advice and try to relate this to real world defects/vulnerabilities but also perhaps you can add a "style" label to the guideline so that we could perhaps treat these differently if we ever decide to.  Similarly, another recent guideline on always using open and close braces, even around single statements, could also be viewed as stylistic.  The problem with these guidelines is the number of false positives they will generate if applied to existing code.  For new code, they are probably not bad ideas.
    The guideline starts very poorly.  The rule should be generalized to something like this:
Performing explicit tests to determine success, true/false, and equality makes code both maintainable and compliant with common conventions. In the case that the return value will never change, an explicit test is still preferable to clearly communicate the numeric, rather than boolean, value of the test.
The title has to change as well. Perhaps "Perform explicit tests to determine success, true/false, and equality"
    Instead of this:
(1) Function failures can typically be indicated by one of the following return values: -1, a non-zero number.
I think I would have described the convention as:
(1) Function failures are typically indicated by a negative return value.
do you disagree?
    pointing out that these conventions are controversial is probably not a good idea.  one of our criteria for guidelines is that they be non-controversial. Also, I don't think the idea of explicit tests is necessarily controversial as a good idea, probably only controversial in if it should be enforced as a guideline. I would probably just delete the following:
These conventions are not entirely non-controversial and is a point of contention for many programmers during code reviews. Here is a typical discussion among programmers on the subject of convention (1).
    David is also right in that you should not use a define for 0 but just compare directly.  I think you really have three cases that you clearly need to differentiate.
        Functions that return an error status.  We have a recommendation that applies in this case DCL09-C. Declare functions that return errno with a return type of errno_t.  Your compliant solution should take this recommendation into account (if your NCE returned int and your CS returned errno_t I think that would be OK, or maybe both can retrrn errno_t).
        Functions that return a boolean value.  Follow David's suggestion to use the _Bool type.  According to C99 Section 6.3.1.2 Boolean type
When any scalar value is converted to _Bool, the result is 0 if the value compares equal
to 0; otherwise, the result is 1.58)
This could be a second compliant solution to your second NCE (which David correctly suggests you should lead off with)
        Functions that return a integer value.  I think your comparison function would be a good example of this.  In this case, you are just testing to see if the returned value is 0 (as opposed to 42) because 0 has some particular meaning.
    David is right about if (strcmp( str1, str2) == 0) being sufficient for your third example.  I think I would go further and simply instruct you to make this change.
                                        Posted by rcs at Mar 17, 2010 09:05
                                     |
| The rule is coming along nicely. More comments:
    Needs a 'References' section, which can contain the link to stackoverflow.com. Any other rules have complete reference sections; you can study those for how to cite Stack Overflow.
    The wording for your 3 points in the intro is vague. For (2) your choices are either: -1, or: any non-zero number.  And for (3), it is important to note that for strcmp() return values of +1 or -1 indicate different orderings of the strings. IOW it has a trinary return value.
    Good 1st NCCE. I do wonder if any implementations of the <ctype.h> functions (eg isalpha(), isdigit(), etc) return true values other than 1. (they are allowed to, according to C99). If so, they would also make a good NCCE/CS pair.
    Your 3rd NCCE is correct as written...I presume it is noncompliant due to maintainability issues, just like your 2nd NCCE). Providing a code snippet indicating how it might be easily changed to incorrect code would be useful. You did this already to the 2nd NCCE to good effect.
    I disagree with the remediation cost...these bugs sound like ones that could be fixed automatically.
                                        Posted by svoboda at Mar 18, 2010 09:43
                                     |
| Does the function failure returning non-zero make more sense now? I also added the errno_t stuff.
                                        Posted by ecollazo at Mar 18, 2010 15:55
                                     |
| I made all these changes and added a more comprehensive NCCE for the last strcmp example. I'm looking into the ctype.h functions right now but welcome more recommendations if you have any.
Thanks!
    Enrique
                                        Posted by ecollazo at Mar 18, 2010 15:56
                                     |
| Only one comment: The References section should be the last item in the rule. Also, please use the conventions we use for citing references (which are evident in most of the other rules on this wiki.) For the strcmp() reference, why don't you just cite the definition of strcmp() from the C99 standard?
                                        Posted by svoboda at Mar 18, 2010 16:36
                                     |
| I added missing bang symbol and closing parens in the sample code.The first non-compliant code contains if expression if(!strcmp()){ ...}, and I revised in CS to;if(strcmp()==0){ ... }.this comparison function issue is treated in the third example, and adding some more explanation may be better... 
                                        Posted by yozo at Nov 13, 2013 03:41
                                     |
| Note that non-compliant code example #2 is a bit of a stretch. While it's technically correct, by changing the return value as indicated, the coder is changing the rules of calling validate_user after the fact, and/or the user of the function was not informed properly of the intent of the return values.This recommendation treds dangerously close to supporting the ill-conceived use of;if (some_value == True), which is not the same as if (some_value) (c.f.C FAQ, Booleans, question 9.2).
                                        Posted by ultra.joe.sewell at Jul 15, 2015 15:05
                                     |

