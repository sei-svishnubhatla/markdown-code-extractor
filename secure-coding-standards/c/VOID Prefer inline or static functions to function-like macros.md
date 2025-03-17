> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+No+implicit+conversion+shall+change+the+signed+nature+of+an+object+or+reduce+the+number+of+bits+in+that+object?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Protect+memory+when+working+with+sensitive+data?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Macros are processed by Preprocessors, whereas inline functions are handled by the Compilers. So the two important benefits of using Compilers (over Preprocessors in this scenario) are
    Ensuring type safety; is simple because compiler does it
    Expressions are evaluated once (this was mentioned earlier) 
                                        Posted by abhi at Feb 15, 2008 14:58
                                     |
| The issue described as the justification for exception PRE00-EX3 does not hold true with any decent compiler. An inline function can most certainly become a compile-time constant through constant folding.
For example, I created the following simple test program based on the add_f function in PRE00-EX3:
[!note]
static inline add_f(int a, int b)
{
    return a + b;
}
int main(int argc, char *argv[])
{
    return add_f(3, 4);
}

I compiled this program with GCC, with optimization turned on. I then disassembled the resulting program. In it, the main function directly moves 7 into eax, the return-value register; main does not call any external function, nor does it perform the addition 3+4 itself.
Does this issue relate to a desire to use the result in a location where C only allows a compile-time constant, such as in the array size in an array declaration?  If so, I agree that the inline function does not currently satisfy that need, but in theory a C compiler could easily support this by checking if it can use a combination of inlining and constant folding to turn the expression into a compile-time constant.
![](images/icons/contenttypes/comment_16.png) Posted by josh@freedesktop.org at Mar 16, 2008 04:51
\| \|
Yes, this relates to the C definition of a constant expression, and is not related to what a quality compiler can do with optimization.
![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 19, 2008 17:31
\| \|
In my opinion that XOR trick used in the swap function should not be used in any example of good coding of any form, and certainly not secure coding. It will misbehave unexpectedly in some situations and is harder to read than the simple use of a temporary variable. For example,
``` java
inline void swap(int *x, int *y) {
  *x ^= *y;
  *y ^= *x;
  *x ^= *y;
}
#define SIZE(a) (sizeof a / sizeof *a)
int main(void) {
  int i;
  int arr[] = {1,2,3,4,5};
  for (i = 0; i <= SIZE(arr) / 2; i++)
    swap(&arr[i],&arr[SIZE(arr)-1-i]);
  for (i = 0; i < SIZE(arr); i++)
    printf("arr[%d] = %d\n",i,arr[i]);
  return 0;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by flashgordon at Mar 20, 2008 16:01
\| \|
I modified PRE00-EX3 slightly to say "Macros can be used to yield a compile-time constant. This is not always possible using inline functions" to leave a little wiggle room for quality compilers.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 22, 2008 17:25
\| \|
Replaced the XOR trick with temporary variable
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 31, 2008 10:58
\| \|
At the start, that should be "Function-like macros".; (There are also macros with invocations that don't resemble function calls.)  Also, static functions would be as good as inline functions in most cases, and are supported in C90 (unlike inline).
Attention should be drawn to the fact that macro parameters are in effect "call by name", as opposed to the "call by value" semantics associated with actual functions.  There are circumstances where call-by-name is essential, and in those cases none of the suggested alternatives can be used.
The SWAP example is bogus, since an experienced coder would have written it as
#define SWAP(a,b) do{tmp=a;a=b;b=tmp;}while(0)  
If C had a "typeof" operator, the tmp variable could even be declared within the block (compound statement) so that the macro would work for a wide variety of types of its arguments.
In many of the examples, the actual problem is using arguments that have side effects, which involves a different rule.  
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 11, 2008 14:01
\| \|
Doug, I believe I've addressed your concerns.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Apr 11, 2008 22:34
\| \|
I think we should bump the severity of this to at least a 2, I feel like arithmetic errors that are unexpected and bypass the compiler are pretty serious and can cause a lot of harm. (mostly in reference to EX4, but also macros in general)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 10:09
\| \|
I added a macro-swap with the XOR trick, but I don't see what the problem is here... the macro allows for the same function to harness the power of an overloaded operator without too many side effects. The XOR is only really a problem if you swap the same variable with itself, which semantically doesn't make too much sense.
The "problem" code above can easily be fixed by replacing the "\<=" in the for loop with a "\<"
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 10:28
\| \|
If swap still bothers you... we could treat swap as a one-of-a-kind trick and change PRE00-EX4 to some other multiline function
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 10:45
\| \|
ok, i feel like i've managed to address all of the concerns with a couple of sidenotes
hopefully, this should make everyone happy
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Apr 17, 2008 11:08
\| \|
Agreed. I raised the priority to P4 (same level)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 01, 2008 12:24
\| \|
Another solution is to write the inline function as such
inline void swap(int \*x, int \*y){
; if (x != y){
        \*x ^=  \*y;
        \*y ^=  \*x;
        \*x ^=  \*y;
  }
}
However, I do agree that using the temp variable is more readable to most programmers.
![](images/icons/contenttypes/comment_16.png) Posted by alaniane at Aug 26, 2009 13:43
\|
