> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+ROSE+Checkers?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Take+granularity+into+account+when+comparing+floating+point+values?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I will leave the final word to David on this idea's fate, but I think a better idea would be to stress that constructors should be used only for initialization. By itself, the guideline sounds slightly weak to me, as usually people understand the purpose of constructors reasonably well. Perhaps more constructor specific advice will do justice to it. Also try not to step over MET04-J. When defining subclasses, explicitly call the superclass constructor first which someone else is working on currently. Best.
                                        Posted by dmohindr at Mar 24, 2009 20:55
                                     |
| IIRC Java automatically initializes all fields to a default 'null' value. So in the NCCE, day will have the value 0. Which may be an invalid value, depending on your object (it is an invalid day-of-the-month value, after all  But this won't be a legit rule unless you can produce code that depends on an uninitialized value.
Is there any way, in Java, to access an unitialized value? (There is in C/C++, but that is covered by EXP33-C & EXP33-CPP)
                                        Posted by svoboda at Mar 25, 2009 11:13
                                     |
| I'm not sure if there's a way to access an uninitialized value in Java. This recommendation is more intended to avoid problems when developers make use of default constructors without noticing that they are instantly setting the object to an invalid state. 
As Java initializes all integer variables to 0, that variable can be accessed immediately after the constructor method has been called, even if it hasn't been given a valid value with a set method or a constructor with a different signature.
                                        Posted by jsandova at Mar 25, 2009 18:19
                                     |
| Right now, I agree with Dhruv. The rule is fairly weak, mainly because the NCCE is obvious in day being unitialized. Perhaps you can strenghen the rule by adding proper usage of constructors, as Dhruv suggests.  We have included recommendations that prevent users from making common misunderstandings (eg the short-circuit behavior of && and ||) even when the language is well-defined. 
I guess my problem is that this rec is about ensuring that fields have legit values in their ctor. And if 0 is a legit value, it is fine for a ctor to leave it 'unitialized'. It's also legit to initialize the value in its declaration, outside the ctor:
private int day = 1;
Basically this rec has a lot of exceptions to it. To legitimize it, you need to enumerate those recs, and provide code samples.
                                        Posted by svoboda at Mar 26, 2009 11:59
                                     |

