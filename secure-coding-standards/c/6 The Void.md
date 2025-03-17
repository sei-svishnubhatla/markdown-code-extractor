This section is basically the trash bin of the CERT C Secure Coding standard. It contains rules and recommendations that have been eliminated from the standard, but not yet erased in case there were bits of information which might still be useful.
> [!info]  
>
> **Information for Editors**  
> To move an existing guideline to [6 The Void](6%20The%20Void) simply label it [void](https://confluence/label/seccode/void).

## Recommendations
-   Page:
    [VOID Always check for errors when using threads](/confluence/display/c/VOID+Always+check+for+errors+when+using+threads)
-   Page:
    [VOID Avoid reopening a file stream](/confluence/display/c/VOID+Avoid+reopening+a+file+stream)
-   Page:
    [VOID Beware of infinite loops](/confluence/display/c/VOID+Beware+of+infinite+loops)
-   Page:
    [VOID Do not create temporary files in shared directories](/confluence/display/c/VOID+Do+not+create+temporary+files+in+shared+directories)
-   Page:
    [VOID Do not make assumptions about the order of global variable initialization across translation units](/confluence/display/c/VOID+Do+not+make+assumptions+about+the+order+of+global+variable+initialization+across+translation+units)
-   Page:
    [VOID Do not use volatile as a synchronization primitive](/confluence/display/c/VOID+Do+not+use+volatile+as+a+synchronization+primitive)
-   Page:
    [VOID EXP01-C. Do not take the size of a pointer to determine the size of the pointed-to type](/confluence/display/c/VOID+EXP01-C.+Do+not+take+the+size+of+a+pointer+to+determine+the+size+of+the+pointed-to+type)
-   Page:
    [void EXP04-C. Do not perform byte-by-byte comparisons involving a structure](/confluence/display/c/void+EXP04-C.+Do+not+perform+byte-by-byte+comparisons+involving+a+structure)
-   Page:
    [VOID EXP21-C. Place constants on the left of equality comparisons](/confluence/display/c/VOID+EXP21-C.+Place+constants+on+the+left+of+equality+comparisons)
-   Page:
    [VOID FIO04-C. Detect and handle input and output errors](/confluence/display/c/VOID+FIO04-C.+Detect+and+handle+input+and+output+errors)
-   Page:
    [void FIO07-C. Prefer fseek() to rewind()](../c/void%20FIO07-C_%20Prefer%20fseek__%20to%20rewind__)
-   Page:
    [void FIO12-C. Prefer setvbuf() to setbuf()](../c/void%20FIO12-C_%20Prefer%20setvbuf__%20to%20setbuf__)
-   Page:
    [void FLP06-C. Understand that floating-point arithmetic in C is inexact](/confluence/display/c/void+FLP06-C.+Understand+that+floating-point+arithmetic+in+C+is+inexact)
-   Page:
    [VOID Initialize local variables immediately after declaration](/confluence/display/c/VOID+Initialize+local+variables+immediately+after+declaration)
-   Page:
    [void MEM08-C. Use realloc() only to resize dynamically allocated arrays](/confluence/display/c/void+MEM08-C.+Use+realloc%28%29+only+to+resize+dynamically+allocated+arrays)
-   Page:
    [void MEM09-C. Do not assume memory allocation functions initialize memory](/confluence/display/c/void+MEM09-C.+Do+not+assume+memory+allocation+functions+initialize+memory)
-   Page:
    [void MSC02-C. Avoid errors of omission](/confluence/display/c/void+MSC02-C.+Avoid+errors+of+omission)
-   Page:
    [void MSC03-C. Avoid errors of addition](/confluence/display/c/void+MSC03-C.+Avoid+errors+of+addition)
-   Page:
    [VOID POS03-C. Do not use volatile as a synchronization primitive with POSIX threads](/confluence/display/c/VOID+POS03-C.+Do+not+use+volatile+as+a+synchronization+primitive+with+POSIX+threads)
-   Page:
    [VOID POS05-C. Avoid race conditions with multiple POSIX threads](/confluence/display/c/VOID+POS05-C.+Avoid+race+conditions+with+multiple+POSIX+threads)
-   Page:
    [VOID POS06-C. Acquire and release POSIX synchronization primitives in the same module, at the same level of abstraction](/confluence/display/c/VOID+POS06-C.+Acquire+and+release+POSIX+synchronization+primitives+in+the+same+module%2C+at+the+same+level+of+abstraction)
-   Page:
    [VOID PRE03-C. Prefer typedefs to defines for encoding non-pointer types](/confluence/display/c/VOID+PRE03-C.+Prefer+typedefs+to+defines+for+encoding+non-pointer+types)
-   Page:
    [VOID PRE13-C. Avoid changing control flow in macro definitions](/confluence/display/c/VOID+PRE13-C.+Avoid+changing+control+flow+in+macro+definitions)
-   Page:
    [VOID Use expression containing sizeof operator to calculate the length of an array](/confluence/display/c/VOID+Use+expression+containing+sizeof+operator+to+calculate+the+length+of+an+array)
-   Page:
    [VOID. INT03-C. Use a secure integer library](/confluence/display/c/VOID.+INT03-C.+Use+a+secure+integer+library)
## Rules
-   Page:
    [VOID ERR31-C. Don't redefine errno](/confluence/display/c/VOID++ERR31-C.+Don%27t+redefine+errno)
-   Page:
    [VOID MSC31-C. Ensure that return values are compared against the proper type](/confluence/display/c/VOID++MSC31-C.+Ensure+that+return+values+are+compared+against+the+proper+type)
-   Page:
    [VOID ARR31-C. Use consistent array notation across all source files](/confluence/display/c/VOID+ARR31-C.+Use+consistent+array+notation+across+all+source+files)
-   Page:
    [void ARR33-C. Guarantee that copies are made into storage of sufficient size](/confluence/display/c/void+ARR33-C.+Guarantee+that+copies+are+made+into+storage+of+sufficient+size)
-   Page:
    [VOID ARR34-C. Ensure that array types in expressions are compatible](/confluence/display/c/VOID+ARR34-C.+Ensure+that+array+types+in+expressions+are+compatible)
-   Page:
    [VOID Do not add or subtract an integer to a pointer if the resulting value does not refer to a valid array element](/confluence/display/c/VOID+Do+not+add+or+subtract+an+integer+to+a+pointer+if+the+resulting+value+does+not+refer+to+a+valid+array+element)
-   Page:
    [VOID Ensure that a mutex is locked successfully before calling pthread_cond_wait()](../c/VOID%20Ensure%20that%20a%20mutex%20is%20locked%20successfully%20before%20calling%20pthread_cond_wait__)
-   Page:
    [void EXP38-C. Do not call offsetof() on bit-field members or invalid types](/confluence/display/c/void+EXP38-C.+Do+not+call+offsetof%28%29+on+bit-field+members+or+invalid+types)
-   Page:
    [void FIO34-C. Use int to capture the return value of character IO functions that might be used to check for end of file](/confluence/display/c/void+FIO34-C.+Use+int+to+capture+the+return+value+of+character+IO+functions+that+might+be+used+to+check+for+end+of+file)
-   Page:
    [void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](../c/void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_)
-   Page:
    [VOID FLP31-C. Do not call functions expecting real values with complex values](/confluence/display/c/VOID+FLP31-C.+Do+not+call+functions+expecting+real+values+with+complex+values)
-   Page:
    [VOID Guarantee that array indices are within the valid range](/confluence/display/c/VOID+Guarantee+that+array+indices+are+within+the+valid+range)
-   Page:
    [void MEM32-C. Detect and handle memory allocation errors](/confluence/display/c/void+MEM32-C.+Detect+and+handle+memory+allocation+errors)
-   Page:
    [VOID POS41-C. When a POSIX thread exit status is not of concern, pthread_detach() or an equivalent function must be used](/confluence/display/c/VOID+POS41-C.+When+a+POSIX+thread+exit+status+is+not+of+concern%2C++pthread_detach%28%29+or+an+equivalent+function+must+be+used)
-   Page:
    [VOID POS54-C. Notify all POSIX threads waiting on a condition variable instead of a single thread](/confluence/display/c/VOID+POS54-C.+Notify+all+POSIX+threads+waiting+on+a+condition+variable+instead+of+a+single+thread)
-   Page:
    [VOID SIG32-C. Do not call longjmp() from inside a signal handler](/confluence/display/c/VOID+SIG32-C.+Do+not+call+longjmp%28%29+from+inside+a+signal+handler)
-   Page:
    [void SIG33-C. Do not recursively invoke the raise() function](/confluence/display/c/void+SIG33-C.+Do+not+recursively+invoke+the+raise%28%29+function)
-   Page:
    [void STR33-C. Size wide character strings correctly](/confluence/display/c/void+STR33-C.+Size+wide+character+strings+correctly)
-   Page:
    [VOID STR35-C. Do not copy data from an unbounded source to a fixed-length array](/confluence/display/c/VOID+STR35-C.+Do+not+copy+data+from+an+unbounded+source+to+a+fixed-length+array)
## Other
-   Page:
    [6 The Void](/confluence/display/c/6+The+Void)
-   Page:
    [Fortify](/confluence/display/c/Fortify)
-   Page:
    [Fortify_V](/confluence/display/c/Fortify_V)
-   Page:
    [Managed String Library](/confluence/display/c/Managed+String+Library)
-   Page:
    [Rec. 15. Concurrency \[POSIX\] (CONP)](../c/Rec_%2015_%20Concurrency%20%5BPOSIX%5D%20_CONP_)
-   Page:
    [Rule 15. Concurrency \[POSIX\] (CONP)](../c/Rule%2015_%20Concurrency%20%5BPOSIX%5D%20_CONP_)
-   Page:
    [VOID 2009 CWE SANS Top 25 Most Dangerous Programming Errors](/confluence/display/c/VOID+2009+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors)
-   Page:
    [VOID 2010 CWE SANS Top 25 Most Dangerous Programming Errors](/confluence/display/c/VOID+2010+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors)
-   Page:
    [VOID 2011 CWE SANS Top 25 Most Dangerous Programming Errors](/confluence/display/c/VOID+2011+CWE+SANS+Top+25+Most+Dangerous+Programming+Errors)
-   Page:
    [VOID All threads must exit before returning or exiting from a main program](/confluence/display/c/VOID+All+threads+must+exit+before+returning+or+exiting+from+a+main+program)
-   Page:
    [VOID Allocate sufficient memory for an object](/confluence/display/c/VOID+Allocate+sufficient+memory+for+an+object)
-   Page:
    [VOID Always provide feedback about the resulting value of a method](/confluence/display/c/VOID+Always+provide+feedback+about+the+resulting+value+of+a+method)
-   Page:
    [VOID API08-C. Avoid parameter names in a function prototype](/confluence/display/c/VOID+API08-C.+Avoid+parameter+names+in+a+function+prototype)
-   Page:
    [VOID Assure Array Offsets Properly Refer to Elements (Wrong section)](../c/VOID%20Assure%20Array%20Offsets%20Properly%20Refer%20to%20Elements%20_Wrong%20section_)
-   Page:
    [VOID Automated Detection Tools](/confluence/display/c/VOID+Automated+Detection+Tools)
-   Page:
    [VOID Be careful using errno with multiple threads](/confluence/display/c/VOID+Be+careful+using+errno+with+multiple+threads)
-   Page:
    [VOID C Rules Implemented in Rose](/confluence/display/c/VOID+C+Rules+Implemented+in+Rose)
-   Page:
    [void CERT C Rules implemented in the LDRA tool suite](/confluence/display/c/void+CERT+C+Rules+implemented+in+the+LDRA+tool+suite)
-   Page:
    [VOID Characters represented as int must be representable as unsigned char or equal EOF](/confluence/display/c/VOID+Characters+represented+as+int+must+be+representable+as+unsigned+char+or+equal+EOF)
-   Page:
    [VOID Check integer values before using C99 functions](/confluence/display/c/VOID+Check+integer+values+before+using+C99+functions)
-   Page:
    [VOID Clean input buffers in loops (DRAFT)](../c/VOID%20Clean%20input%20buffers%20in%20loops%20_DRAFT_)
-   Page:
    [VOID Coverity](/confluence/display/c/VOID+Coverity)
-   Page:
    [VOID Coverity - 1](/confluence/display/c/VOID+Coverity+-+1)
-   Page:
    [VOID Create temporary files securely](/confluence/display/c/VOID+Create+temporary+files+securely)
-   Page:
    [void DCL33-C. Ensure that restrict-qualified source and destination pointers in function arguments do not reference overlapping objects](/confluence/display/c/void+DCL33-C.+Ensure+that+restrict-qualified+source+and+destination+pointers+in+function+arguments+do+not+reference+overlapping+objects)
-   Page:
    [Void DCL35-C. Call functions with the correct number and type of arguments](/confluence/display/c/Void+DCL35-C.+Call+functions+with+the+correct+number+and+type+of+arguments)
-   Page:
    [VOID Define numeric constants in a portable way](/confluence/display/c/VOID+Define+numeric+constants+in+a+portable+way)
-   Page:
    [VOID Disallow particular characters in file names (draft)](../c/VOID%20Disallow%20particular%20characters%20in%20file%20names%20_draft_)
-   Page:
    [VOID Do not allow loops to iterate beyond the end of an array](/confluence/display/c/VOID+Do+not+allow+loops+to+iterate+beyond+the+end+of+an+array)
-   Page:
    [VOID Do not assume the destination array of strncpy() is null-terminated](/confluence/display/c/VOID+Do+not+assume+the+destination+array+of+strncpy%28%29+is+null-terminated)
-   Page:
    [VOID Do not call the longjmp function to terminate a call to a function registered by atexit()](../c/VOID%20Do%20not%20call%20the%20longjmp%20function%20to%20terminate%20a%20call%20to%20a%20function%20registered%20by%20atexit__)
-   Page:
    [VOID Do not make assumptions about the result of malloc(0) or calloc(0)](../c/VOID%20Do%20not%20make%20assumptions%20about%20the%20result%20of%20malloc_0_%20or%20calloc_0_)
-   Page:
    [VOID Do not perform certain operations on questionably signed results](/confluence/display/c/VOID+Do+not+perform+certain+operations+on+questionably+signed+results)
-   Page:
    [VOID Do not return from SIGFPE from inside a signal handler](/confluence/display/c/VOID+Do+not+return+from+SIGFPE+from+inside+a+signal+handler)
-   Page:
    [VOID Do not shift values farther than their type width](/confluence/display/c/VOID+Do+not+shift+values+farther+than+their+type+width)
-   Page:
    [VOID Do not store an address into an object with a longer lifetime](/confluence/display/c/VOID+Do+not+store+an+address+into+an+object+with+a+longer+lifetime)
-   Page:
    [VOID Ensure array offsets properly align in variable-sized arrays of unions and structs](/confluence/display/c/VOID+Ensure+array+offsets+properly+align+in+variable-sized+arrays+of+unions+and+structs)
-   Page:
    [VOID Ensure that source and destination pointers in function arguments do not point to overlapping objects](/confluence/display/c/VOID+Ensure+that+source+and+destination+pointers+in+function+arguments+do+not+point+to+overlapping+objects)
-   Page:
    [VOID EXP31-C. Do not perform side effects in assertions](/confluence/display/c/VOID+EXP31-C.+Do+not+perform+side+effects+in+assertions)
-   Page:
    [VOID fflush() should be called after writing to an output stream if data integrity is important](/confluence/display/c/VOID+fflush%28%29+should+be+called+after+writing+to+an+output+stream+if+data+integrity+is+important)
-   Page:
    [void FIO33-C. Detect and handle input output errors resulting in undefined behavior](/confluence/display/c/void+FIO33-C.+Detect+and+handle+input+output+errors+resulting+in+undefined+behavior)
-   Page:
    [VOID Functions should validate their parameters](/confluence/display/c/VOID+Functions+should+validate+their+parameters)
-   Page:
    [VOID INT20-C. Use the type ptrdiff_t when storing the difference of two pointers](/confluence/display/c/VOID+INT20-C.+Use+the+type+ptrdiff_t+when+storing+the+difference+of+two+pointers)
-   Page:
    [VOID INT36-C. Do not perform bitwise and arithmetic operations on the same variable](/confluence/display/c/VOID+INT36-C.+Do+not+perform+bitwise+and+arithmetic+operations+on+the+same+variable)
-   Page:
    [VOID Integer Arithmetic and Conversion functions](/confluence/display/c/VOID+Integer+Arithmetic+and+Conversion+functions)
-   Page:
    [VOID Klocwork Cross Reference](/confluence/display/c/VOID+Klocwork+Cross+Reference)
-   Page:
    [VOID Klocwork Cross Reference0](/confluence/display/c/VOID+Klocwork+Cross+Reference0)
-   Page:
    [VOID Klocwork Cross Reference1](/confluence/display/c/VOID+Klocwork+Cross+Reference1)
-   Page:
    [VOID Limit depth of nesting](/confluence/display/c/VOID+Limit+depth+of+nesting)
-   Page:
    [VOID Make sure the selected socket port is available.](/confluence/pages/viewpage.action?pageId=87152268)
-   Page:
    [void MSC40-C. Do not use an empty infinite loop](/confluence/display/c/void+MSC40-C.+Do+not+use+an+empty+infinite+loop)
-   Page:
    [VOID No implicit conversion shall change the signed nature of an object or reduce the number of bits in that object](/confluence/display/c/VOID+No+implicit+conversion+shall+change+the+signed+nature+of+an+object+or+reduce+the+number+of+bits+in+that+object)
-   Page:
    [VOID Prefer inline or static functions to function-like macros](/confluence/display/c/VOID+Prefer+inline+or+static+functions+to+function-like+macros)
-   Page:
    [VOID Protect memory when working with sensitive data](/confluence/display/c/VOID+Protect+memory+when+working+with+sensitive+data)
-   Page:
    [VOID ROSE Checkers](/confluence/display/c/VOID+ROSE+Checkers)
-   Page:
    [VOID sciSpider](/confluence/display/c/VOID+sciSpider)
-   Page:
    [VOID Specify a default constructor that initializes each data member to a known safe state.](/confluence/pages/viewpage.action?pageId=87152224)
-   Page:
    [VOID Take granularity into account when comparing floating point values](/confluence/display/c/VOID+Take+granularity+into+account+when+comparing+floating+point+values)
-   Page:
    [VOID Temporary Files (TMP)](../c/VOID%20Temporary%20Files%20_TMP_)
-   Page:
    [VOID Temporary files must be opened with exclusive access](/confluence/display/c/VOID+Temporary+files+must+be+opened+with+exclusive+access)
-   Page:
    [VOID Temporary files must be removed before the program exits](/confluence/display/c/VOID+Temporary+files+must+be+removed+before+the+program+exits)
-   Page:
    [VOID Understand the caveats of floating point exceptions](/confluence/display/c/VOID+Understand+the+caveats+of+floating+point+exceptions)
-   Page:
    [VOID Use variables of type size_t for size parameters to memory allocation routines](/confluence/display/c/VOID+Use+variables+of+type+size_t+for+size+parameters+to+memory+allocation+routines)
-   Page:
    [VOID Use volatile type qualifer for objects of automatic storage duration that are modified between setjmp() and longjmp()](../c/VOID%20Use%20volatile%20type%20qualifer%20for%20objects%20of%20automatic%20storage%20duration%20that%20are%20modified%20between%20setjmp__%20and%20longjmp__)
-   Page:
    [VOID Using ROSE Checkers](/confluence/display/c/VOID+Using+ROSE+Checkers)
[](https://www.securecoding.cert.org/confluence/display/seccode/POS47-C.+Do+not+use+threads+that+can+be+canceled+asynchronously?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1336) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+All+threads+must+exit+before+returning+or+exiting+from+a+main+program?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Please use mostly one-error examples of bad code.
In most examples I've seen that mix several types of errors, I feel the other errors just detract from illustrating the importance of the actual rule/recommendation being broken.
Also it adds redundancy.; And some just go overboard with stupidity, leaving the feeling that the problem is "if you are really stupid your program will be insecure". I mean, free() and a pointless-looking strcpy to a maybe-unallocated pointer in a signal handler?  A signal handler just doing msg = "whatever" would illustrate the problem with the latter just as well - the program might be in the middle of reading the msg pointer when the signal arrived.
A bug in an innocent-looking piece of code looks far more alarming.
(Sorry, I seem to be too tired to figure out how to make a nice list item with a new page.  Just arrived at this site, and the deadline is running out...)
                                        Posted by hbf at Apr 18, 2008 21:05
                                     |
| I've tagged all pages in 2982282 using the void and filtered them out from the {contentbylabel} query used to generate the index for each section. This makes it possible to move any guideline (or any other page) from whatever section it happens to be in to The Void simply by labeling it void. In particular, the title of the guideline can stay unchanged and the section page the guideline is referenced from doesn't need to be updated. Similarly, restoring a guideline from The Void is as simple as deleting the void label.
                                        Posted by martinsebor at Feb 03, 2010 13:45
                                     |

