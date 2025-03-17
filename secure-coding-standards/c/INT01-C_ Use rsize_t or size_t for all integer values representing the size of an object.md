The `size_t` type is the unsigned integer type of the result of the `sizeof` operator. Variables of type `size_t` are guaranteed to be of sufficient precision to represent the size of an object. The limit of `size_t` is specified by the `SIZE_MAX` macro.
The type `size_t` generally covers the entire address space. The C Standard, Annex K (normative), "Bounds-checking interfaces," introduces a new type, `rsize_t`, defined to be `size_t` but explicitly used to hold the size of a single object \[[Meyers 2004](AA.-Bibliography_87152170.html#AA.Bibliography-Meyers2004)\]. In code that documents this purpose by using the type `rsize_t`, the size of an object can be checked to verify that it is no larger than `RSIZE_MAX`, the maximum size of a normal single object, which provides additional input validation for library functions. See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation) for additional discussion of C11 Annex K.
Any variable that is used to represent the size of an object, including integer values used as sizes, indices, loop counters, and lengths, should be declared `rsize_t`, if available. Otherwise, it should be declared `size_t`.
## Noncompliant Code Example
In this noncompliant code example, the dynamically allocated buffer referenced by `p` overflows for values of `n > INT_MAX`:
``` c
char *copy(size_t n, const char *c_str) {
  int i;
  char *p;
  if (n == 0) {
    /* Handle unreasonable object size error */
  }
  p = (char *)malloc(n);
  if (p == NULL) {
    return NULL; /* Indicate malloc failure */
  }
  for ( i = 0; i < n; ++i ) {
    p[i] = *c_str++;
  }
  return p;
}
/* ... */
char c_str[] = "hi there";
char *p = copy(sizeof(c_str), c_str);
```
Signed integer overflow causes [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior). The following are two possible conditions under which this code constitutes a serious [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability):
##### `sizeof(size_t) == sizeof(int)`
The unsigned `n` may contain a value greater than `INT_MAX`. Assuming quiet wraparound on signed overflow, the loop executes `n` times because the comparison `i < n` is an unsigned comparison. Once `i` is incremented beyond `INT_MAX`, `i` takes on negative values starting with `(INT_MIN)`. Consequently, the memory locations referenced by `p[i]` precede the memory referenced by `p`, and a write outside array bounds occurs.
##### `sizeof(size_t) > sizeof(int)`
For values of `n` where `0 < n <= INT_MAX`, the loop executes `n` times, as expected.
For values of `n` where `INT_MAX < n <= (size_t)INT_MIN`, the loop executes `INT_MAX` times. Once `i` becomes negative, the loop stops, and `i` remains in the range `0` through `INT_MAX`.
For values of `n` where `(size_t)INT_MIN < n <= SIZE_MAX`, `i` wraps and takes the values `INT_MIN` to `INT_MIN + (n - (size_t)INT_MIN - 1)`. Execution of the loop overwrites memory from `p[INT_MIN]` through `p[INT_MIN + (n - (size_t)INT_MIN - 1)]`.
## Compliant Solution (C11, Annex K)
Declaring `i` to be of type `rsize_t` eliminates the possible integer overflow condition (in this example). Also, the argument `n` is changed to be of type `rsize_t` to document additional [validation](BB.-Definitions_87152273.html#BB.Definitions-validation) in the form of a check against `RSIZE_MAX`:
``` c
char *copy(rsize_t n, const char *c_str) {
  rsize_t i;
  char *p;
  if (n == 0 || n > RSIZE_MAX) {
    /* Handle unreasonable object size error */
  }
  p = (char *)malloc(n);
  if (p == NULL) {
    return NULL;  /* Indicate malloc failure */
  }
  for (i = 0; i < n; ++i) {
    p[i] = *c_str++;
  }
  return p;
}
/* ... */
char c_str[] = "hi there";
char *p = copy(sizeof(c_str), c_str);
```
## Noncompliant Code Example
In this noncompliant code example, the value of `length` is read from a network connection and passed as an argument to a wrapper to `malloc()` to allocate the appropriate data block. Provided that the size of an `unsigned long` is equal to the size of an `unsigned int`, and both sizes are equal to or smaller than the size of `size_t`, this code runs as expected. However, if the size of an `unsigned long` is greater than the size of an `unsigned int`, the value stored in `length` may be truncated when passed as an argument to `alloc()`.  Both read functions return zero on success and nonzero on failure.
``` c
void *alloc(unsigned int blocksize) {
  return malloc(blocksize);
}
int read_counted_string(int fd) {
  unsigned long length;
  unsigned char *data;
  if (read_integer_from_network(fd, &length)) {
    return -1;
  }
  data = (unsigned char*)alloc(length+1);
  if (data == NULL) {
    return -1;  /* Indicate failure */
  }
  if (read_network_data(fd, data, length)) {
    free(data);
    return -1;
  }
  data[length] = '\0';
  /* ... */
  free( data);
  return 0;
}
```
## Compliant Solution (C11, Annex K)
Declaring both `length` and the `blocksize` argument to `alloc()` as `rsize_t` eliminates the possibility of truncation. This compliant solution assumes that `read_integer_from_network()` and `read_network_data()` can also be modified to accept a `length` argument of type pointer to `rsize_t` and `rsize_t`, respectively. If these functions are part of an external library that cannot be updated, care must be taken when casting `length` into an `unsigned long` to ensure that integer truncation does not occur.
``` c
void *alloc(rsize_t blocksize) {
  if (blocksize == 0 || blocksize > RSIZE_MAX) {
    return NULL;  /* Indicate failure */
  }
  return malloc(blocksize);
}
int read_counted_string(int fd) {
  rsize_t length;
  unsigned char *data;
  if (read_integer_from_network(fd, &length)) {
    return -1;
  }
  data = (unsigned char*)alloc(length+1);
  if (data == NULL) {
    return -1; /* Indicate failure */
  }
  if (read_network_data(fd, data, length)) {
    free(data);
    return -1;
  }
  data[length] = '\0';
  /* ... */
  free( data);
  return 0;
}
```
## Risk Assessment
The improper calculation or manipulation of an object's size can result in exploitable [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| INT01-C | Medium | Probable | Medium | P8 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Axivion Bauhaus Suite | 7.2.0 | CertC-INT01 |  |
| CodeSonar | 8.3p0 | LANG.TYPE.BASIC | Basic numerical type used |
| Compass/ROSE |  |  | Can detect violations of this recommendation. In particular, it catches comparisons and operations where one operand is of type size_t or rsize_t and the other is not |
| Splint | 3.1.1 |  |  |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+INT01-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID INT01-CPP. Use rsize_t or size_t for all integer values representing the size of an object |

## Bibliography

|  |  |
| ----|----|
| [Meyers 2004] |  |

------------------------------------------------------------------------
[](../c/INT00-C_%20Understand%20the%20data%20model%20used%20by%20your%20implementation_s_) [](../c/Rec_%2004_%20Integers%20_INT_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152206)
## Comments:

|  |
| ----|
| Does it matter that there is no guarantee from the first sample compliant code that the returned string is null terminated, because there is no guarantee that the input string is the length specified and so on?
Also, doesn't the call: p = copy(20, "hi there"); invoke undefined behaviour?; It is accessing 11 bytes beyond the end of the string.  This is the converse of the 'not null terminated' problem in some ways.
 The second compliant solution again has a null-termination problem.  In the fragment where the result is not used, this is "OK", but the example might be used elsewhere, and then it would matter.
The third example is also vulnerable on an LP32 implementation (as well as LP64).  It also allocates space for a null terminator but does not visibly ensure that it is present. 
                                        Posted by jonathan.leffler@gmail.com at Mar 16, 2008 11:27
                                     |
| >> Once i >> > INT_MAX, i takes on
>> negative values starting with (INT_MIN). Consequently, the memory locations

Not really. Once i overflows, UB happens and there is nothing guaranteed. 
Update: okay, in that same page (INT01-A) I found this code which
claims to be secure & conforming
>> #define BUFF_SIZE 10
>> int main(int argc, char *argv[]){
>>   rsize_t size;
>>   char buf[BUFF_SIZE];
>>   size = atoi(argv[1]); /* vipp: atoi in secure code? */
>>   /* vipp: where are your checks for argc? */
>>   if (size < BUFF_SIZE){
>>    strncpy(buf, argv[2], size); /* vipp: ka-boom */
>>    buf[size] = '\0';
>>  }
>> } 


–
from: <http://groups.google.com/group/comp.lang.c/browse_thread/thread/1ad64a62aa6ec2d7/84c2ed6e56338aad?hl=en#84c2ed6e56338aad>
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 25, 2008 20:42
\| \|
OK, I think I addressed both of these comments.
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 25, 2008 22:25
\| \|
\(1\) rsize_t is like errno_t (see my comments there) in that some work is needed to use the name in portable code.
\(2\) rsize_t is pointless anyway: the purpose of size_t is merely to provide a type that is guaranteed to be big enough to index every byte of an object, and rsize_t says that; that is also its purpose.  The programmer only needs one type for use in declaring indices etc. and size_t is meant for that.  The idea that functions can perform better validation is bogus since if RSIZE_MAX is the largest that an object can be, then that value should be used for SIZE_MAX, and really useful bounds checking must be for the actual object size, not for the largest possible object size.  rsize_t was a mistake and should not be blessed by these guidelines.
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 15, 2008 15:39
\| \|
Well, if you want it to be bashed![](images/icons/emoticons/smile.svg)
Both non-compliant examples are silly because several listed problems are buggy independently of the use of the variables for sizes/indexes, and thus independently of this recommendation:
Example #1: In for(i = 0; i\<n; ++i), 'i' should normally be of the same type as n and must be able to hold the max possible value of n.; Also it looks like a string so you should likely allocate one more byte and append a \0.
Example #2: Passing unsigned long to unsigned int truncates the value, unless you know it's \<= UINT_MAX.  And the integer wraparound test 'length + 1 == 0' is unnecessarily hacky and depends on the type being unsigned, length == ULONG_MAX would be more readable.
If the network functions called in example #2 take unsigned longs, the "compliant solution" is broken when it instead passes rsize_t\*, and when passing rsize_t without first checking that length \<= ULONG_MAX.
Which also illustrates one reason I'd personally sometimes let another guideline trump this one (and some others): Avoid integer type conversions, implicit as well as explicit, by declaring variables what will "meet" each other to have the same type.  Integer conversions often need to be checked for max/min limits to be safe.  So if some size value will have to be passed/declared as int (for printf("%\*..")) or ssize_t (returned from Unix write()), the code may be cleaner if it uses those types for sizes.  There may be no point it having part of it support bigger objects anyway.  Though even then (r)size_t is sometimes just as simple to use since one in any case must ensure that the sizes involved can fit in the smallest integer type they will be stored/passed in.
The text compares sizeof(long) with sizeof(int) when it should compare ULONG_MAX with UINT_MAX.  The results don't have to be the same, though of course they normally are.
And just to bring up a different mess, with the first para (about size_t): It has been argued on comp.std.c that an object can be larger than the max value size_t:  size_t is merely defined as the return type of sizeof, which must return the correct size of an object.  Thus an object may be larger than SIZE_MAX as long as you don't use sizeof on it.  (I think there is/was a defect report on that.)
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Jun 12, 2008 12:41
\| \|
I was mostly concerned with the the order/structure of the wording, not the meaning (which I have not changed)
Ex #1 strings: fixed Ex #2 `length +1`: fixed  
Ex #2 `rsize_t`: not sure what you mean here  
Ex #2 `sizeof` vs `ULONG_MAX`: fixed
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 12, 2008 13:04
\| \|
Err, actually I picked on the "wrong error" with ex#1 length - being a string copy function I expected it to take a length rather than size argument, so the problem was just that the API is surprising.; And length rather than lenght+1 may be OK for unsigned char\* (ex#2).
Ex #2 rsize_t: Point is, the noncompliant code passes (pointer to) unsigned long to the network functions, which is hopefully because these functions take (pointer to) unsigned long.  The compliant solution changes the caller but there is no mention of changing the network functions to match.  If you can change the network functions without too much hassle, certainly do that (and change all callers). But if it's an external API you can't.  In either case, it's the network functions and not the example functions which are the source of the trouble and which originally break this recommendation.{{  
}}
![](images/icons/contenttypes/comment_16.png) Posted by hbf at Jun 12, 2008 14:05
\| \|
Ex #2 `rsize_t`: added a note about needing to update the network functions, thanks ![](images/icons/emoticons/smile.svg)
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 12, 2008 14:51
\| \|
Is this rule supposed to apply to array indices, too?
eg, good or bad:
``` java
int array[ARRAY_MAX];
for (int i = 0; i < ARRAY_MAX; i++) 
  /* ... */
}
```
This code is definitely bad:
``` java
for (size_t i = ARRAY_MAX-1; i >= 0; i--)
```
because i is always nonnegative.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 12, 2009 09:34
\| \|
> ``` java
> size_t n;
> int i;
> [...]
> for ( i = 0; i < n; ++i ) {
>     p[i] = *str++;
> }
> ```
>
> \[...\] sizeof(size_t) \> sizeof(int)
>
> Similar behavior as the case above occurs for values of n \<= UINT_MAX. For values of n \> UINT_MAX, the expression ++i will wrap around to zero before the condition i \< n ever evaluates to false. This causes all memory within \[INT_MIN, INT_MAX\] from the beginning of the output buffer to be overwritten in an infinite loop.

This is wrong. For 0\<n\<=INT_MAX, the loop executes n times, as expected. For n\>INT_MAX, the loop executes INT_MAX+1 times. For each iteration, i is in the range 0 through INT_MAX. Once i becomes negative, the loop will stop, because a negative value for i converts into SIZE_MAX+1+i. Since sizeof(size_t)\>sizeof(int), SIZE_MAX is well above INT_MAX\*2, as well as SIZE_MAX+1+INT_MIN, therefore the size_t values i converts to are always greater than values of n in the range INT_MAX+1 to INT_MAX\*2. I've verified the above on a compiler that has 16-bit int and 32-bit size_t.
![](images/icons/contenttypes/comment_16.png) Posted by sgreen at Aug 25, 2009 00:42
\| \|
Good catch, thanks. I've revised the text to closely match what you have stated above.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 28, 2009 13:51
\| \|
Suppose n == SIZE_MAX + 1 + INT_MIN + 50. Then when i wraps around and takes the values INT_MIN to INT_MIN + 49, the loop will scribble on p\[INT_MIN\] through p\[INT_MIN + 49\]. Then the loop will terminate.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Sep 08, 2009 13:42
\| \|
I've revised this one last time (I hope).
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Sep 16, 2009 08:54
\| \|
signe int compare with unsigned long will promote to unsigned long
![](images/icons/contenttypes/comment_16.png) Posted by 13611593077 at Sep 06, 2019 11:15
\| \|
For the second noncompliant code example, It is stated: "Provided that the size of an;`unsigned long` is equal to the size of an `unsigned int`, and both sizes are equal to or smaller than the size of `size_t`, this code runs as expected. ", however i found few more vulns:
1.  In case `length == 0` , the `\0`  assignment causes an OOB-write. 
2.  \`read_network_data\`  and \`read_integer_from_network\` identifies errors as return values that satisfy: "`< 0"` .   
    This isn't good enough - the correct check should be "\< sizeof(unsigned long)" and "\< length" - As "read\*" methods returns the amount of bytes read as their return value.   
    For example, assuming a platform where \`sizeof(unsigned long) == 8\`, this means a scenario where only 5 out of 8 were read successfully from the network is still treated as a success - and the code continues, eventho it may lead to unexpected behavior. 
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Jan 15, 2023 09:35
\| \|
Itay:
Thanks for the comment.
1\. I realized that the example is itself a bit confused...is it allocating space for a block of chars or a block of null-terminated chars (eg a C string?). So I resolved this by having it allocate length+1 chars. Since the minimum value of length is 0, this always allocates 1 char (if successful), preventing the OOB write.
2\. These two functions are not standard...we invented them just for this example, so we can define them however we want :) ;Basing them off the C fread() or the POSIX read() functions would be troublesome, because both functions return a size_t value, which can never be less than zero. Also, both standard functions can return the number of elements read which may be less than the number requested. IMO it is best to say so explicitly in the examples, since we have other rules about how to use these functions properly.  See CERT rules FIO34-C and FIO37-C for more info about safely reading data from a file.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 17, 2023 08:38
\|
