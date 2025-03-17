Many functions require the allocation of multiple resources. Failing and returning somewhere in the middle of this function without freeing all of the allocated resources could produce a memory leak. It is a common error to forget to free one (or all) of the resources in this manner, so a `goto` chain is the simplest and cleanest way to organize exits while preserving the order of freed resources.
## Noncompliant Code Example (POSIX)
In this noncompliant example, exit code is written for every instance in which the function can terminate prematurely. Notice how failing to close `fin2` produces a resource leak, leaving an open file descriptor.
Please note that these examples assume `errno_t` and `NOERR` to be defined, as recommended in [DCL09-C. Declare functions that return errno with a return type of errno_t](DCL09-C_%20Declare%20functions%20that%20return%20errno%20with%20a%20return%20type%20of%20errno_t). An equivalent compatible example would define `errno_t` as an `int` and `NOERR` as zero.
These examples also assume that `errno` is set if `fopen()` or `malloc()` fail. These are guaranteed by POSIX but not by C11. See [ERR30-C. Take care when reading errno](ERR30-C_%20Take%20care%20when%20reading%20errno) for more details.
``` c
typedef struct object {  /* Generic struct: contents don't matter */
  int propertyA, propertyB, propertyC;
} object_t;
errno_t do_something(void){
  FILE *fin1, *fin2;
  object_t *obj;
  errno_t ret_val;
  fin1 = fopen("some_file", "r");
  if (fin1 == NULL) {
    return errno;
  }
  fin2 = fopen("some_other_file", "r");
  if (fin2 == NULL) {
    fclose(fin1);
    return errno;
  }
  obj = malloc(sizeof(object_t));
  if (obj == NULL) {
    ret_val = errno;
    fclose(fin1);
    return ret_val;  /* Forgot to close fin2!! */
  }
  /* ... More code ... */
  fclose(fin1);
  fclose(fin2);
  free(obj);
  return NOERR;
}
```
This is just a small example; in much larger examples, errors like this are even harder to detect.
## Compliant Solution (POSIX, Nested Ifs)
This compliant solution uses nested if statements to properly close files and free memory in the case that any error occurs. When the number of resources to manage is small (3 in this example), nested if statements will be simpler than a goto chain.
``` c
/* ... Assume the same struct used previously ... */
errno_t do_something(void) {
  FILE *fin1, *fin2;
  object_t *obj;
  errno_t ret_val = NOERR; /* Initially assume a successful return value */
  if ((fin1 = fopen("some_file", "r")) != NULL) {
    if ((fin2 = fopen("some_other_file", "r")) != NULL) {
      if ((obj = malloc(sizeof(object_t))) != NULL) {
        /* ... More code ... */
        /* Clean-up & handle errors */
        free(obj);
      } else {
        ret_val = errno;
      }
      fclose(fin2);
    } else {
      ret_val = errno;
    }
    fclose(fin1);
  } else {
    ret_val = errno;
  }
  return ret_val;
}
```
## Compliant Solution (POSIX, Goto Chain)
Occasionally, the number of resources to manage in one function will be too large to permit using nested ifs to manage them.
In this revised version, a `goto` chain replaces each individual return segment. If no error occurs, control flow falls through to the `SUCCESS` label, releases all of the resources, and returns `NOERR`. If an error occurs, the return value is set to `errno`, control flow jumps to the proper failure label, and the appropriate resources are released before returning.
``` c
/* ... Assume the same struct used previously ... */
errno_t do_something(void) {
  FILE *fin1, *fin2;
  object_t *obj;
  errno_t ret_val = NOERR; /* Initially assume a successful return value */
  fin1 = fopen("some_file", "r");
  if (fin1 == NULL) {
    ret_val = errno;
    goto FAIL_FIN1;
  }
  fin2 = fopen("some_other_file", "r");
  if (fin2 == NULL) {
    ret_val = errno;
    goto FAIL_FIN2;
  }
  obj = malloc(sizeof(object_t));
  if (obj == NULL) {
    ret_val = errno;
    goto FAIL_OBJ;
  }
  /* ... More code ... */
SUCCESS:     /* Clean up everything */
  free(obj);
FAIL_OBJ:   /* Otherwise, close only the resources we opened */
  fclose(fin2);
FAIL_FIN2:
  fclose(fin1);
FAIL_FIN1:
  return ret_val;
}
```
This method is beneficial because the code is cleaner, and the programmer does not need to rewrite similar code upon every function error.
Note that this guideline does not advocate more general uses of goto, which is still [considered harmful](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf). The use of goto in these cases is specifically to transfer control within a single function body.
## Compliant Solution (`copy_process()` from Linux kernel)
Some effective examples of `goto` chains are quite large. This compliant solution is an excerpt from the Linux kernel. This is the `copy_process` function from `kernel/fork.c` from version 2.6.29 of the kernel.
The function uses 17 `goto` labels (not all displayed here) to perform cleanup code should any internal function yield an error code. If no errors occur, the program returns a pointer to the new process `p`. If any error occurs, the program diverts control to a particular `goto` label, which performs cleanup for sections of the function that have currently been successfully executed but not for sections that have not yet been executed. Consequently, only resources that were successfully opened are actually closed.
All comments in this excerpt were added to indicate additional code in the kernel not displayed here.
``` c
static struct task_struct *copy_process(unsigned long clone_flags,
                    unsigned long stack_start,
                    struct pt_regs *regs,
                    unsigned long stack_size,
                    int __user *child_tidptr,
                    struct pid *pid,
                    int trace)
{
  int retval;
  struct task_struct *p;
  int cgroup_callbacks_done = 0;
  if ((clone_flags & (CLONE_NEWNS|CLONE_FS)) == (CLONE_NEWNS|CLONE_FS))
    return ERR_PTR(-EINVAL);
  /* ... */
  retval = security_task_create(clone_flags);
  if (retval)
    goto fork_out;
  retval = -ENOMEM;
  p = dup_task_struct(current);
  if (!p)
    goto fork_out;
  /* ... */
  /* Copy all the process information */
  if ((retval = copy_semundo(clone_flags, p)))
    goto bad_fork_cleanup_audit;
  if ((retval = copy_files(clone_flags, p)))
    goto bad_fork_cleanup_semundo;
  if ((retval = copy_fs(clone_flags, p)))
    goto bad_fork_cleanup_files;
  if ((retval = copy_sighand(clone_flags, p)))
    goto bad_fork_cleanup_fs;
  if ((retval = copy_signal(clone_flags, p)))
    goto bad_fork_cleanup_sighand;
  if ((retval = copy_mm(clone_flags, p)))
    goto bad_fork_cleanup_signal;
  if ((retval = copy_namespaces(clone_flags, p)))
    goto bad_fork_cleanup_mm;
  if ((retval = copy_io(clone_flags, p)))
    goto bad_fork_cleanup_namespaces;
  retval = copy_thread(0, clone_flags, stack_start, stack_size, p, regs);
  if (retval)
    goto bad_fork_cleanup_io;
  /* ... */
  return p;
  /* ... Cleanup code starts here ... */
bad_fork_cleanup_io:
  put_io_context(p->io_context);
bad_fork_cleanup_namespaces:
  exit_task_namespaces(p);
bad_fork_cleanup_mm:
  if (p->mm)
    mmput(p->mm);
bad_fork_cleanup_signal:
  cleanup_signal(p);
bad_fork_cleanup_sighand:
  __cleanup_sighand(p->sighand);
bad_fork_cleanup_fs:
  exit_fs(p); /* Blocking */
bad_fork_cleanup_files:
  exit_files(p); /* Blocking */
bad_fork_cleanup_semundo:
  exit_sem(p);
bad_fork_cleanup_audit:
  audit_free(p);
  /* ... More cleanup code ... */
fork_out:
  return ERR_PTR(retval);
}
```
## Risk Assessment
Failure to free allocated memory or close opened files results in a memory leak and possibly unexpected results.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM12-C | Low | Probable | Medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Klocwork | 2024.4 | MLK.MIGHTMLK.MUST
MLK.RET.MIGHT
MLK.RET.MUST
RH.LEAK
 |  |
| LDRA tool suite | 9.7.1 | 50 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-MEM12-a | Ensure resources are freed |
| PC-lint Plus | 1.4 | 429 | Assistance provided |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM12-C | Checks for memory leak and resource leak (rec. partially covered) |

## Bibliography

|  |  |
| ----|----|
|  | ;Dijkstra, Edgar, "Go To Statement Considered Harmful.", 1968 |
| Linux Kernel Sourcecode (v2.6.xx) | 2.6.29, kernel/fork.c, the copy_process() Function |
| [Seacord 2013] | Chapter 4, "Dynamic Memory Management" |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152220) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_)
## Comments:

|  |
| ----|
| Good idea for a rule, Philip. Comments:
    I notice you created a similar rule in C++. I don't think this is a legit rule for C++ b/c it provides better ways to clean up resources when errors occur.
    Add a link from the 'Memory Management' page and update Risk ASsessment, and add References
    The Compliant solution should probably have a return statement before the 'fail obj' labels to indicate normal termination
                                        Posted by svoboda at Mar 31, 2009 08:18
                                     |
| The (incomplete/blank) rule placed in the C++ section was a mistake.  I was having trouble using the site yesterday and accidentally created it.  I couldn't figure out how to delete that page.
But I have made the following changes:
    I added a link from the Memory Management page and included the Risk Assessment in the table
    I updated the code to include a positive return statement (this is a very good idea, thanks)
    I included a couple references on this page
Is this good, or is there anything else I should do?
                                        Posted by pshirey at Mar 31, 2009 14:59
                                     |
| As written, this is clearly a recommendation and not a guidelines because you are simply recommending an approach to solving the problem "free memory once and only once".
Both the NCE and CS need to compile.
I would prefer to see the test for failure as obj1 == NULL.  This form is easier to read.
Don't start your NCE and CS sections with the example code.  Say something like:
In this noncompliant code example blah blah blah.
and
In this compliant solution, blah blah blah.
"Hence, the goto-chain..."
is a bit too informal style of writing for this.
Point out in the compliant solution that you fall through to the success condition, even though it's kind of obvious.
Why is this just for memory allocation?  What about the allocation/deallocation of other resources, for example, opening and closing files?  
I think you need to generalize this recommendation further.
                                        Posted by rcs at Mar 31, 2009 17:23
                                     |
| I have made the following changes:
    I replaced malloc(...) with allocate_object(); hopefully this should convey the same idea
    I replaced instances of !objx with objx == NULL, as suggested
    I changed the wording around and started the NCE and CS sections with text
    I changed the article to a recommendation and reflected this update on the MEM page
    I noted that this does not only apply to memory allocation
When writing this, opening files and pipes definitely came to mind (since I have used this strategy to maintain them before as well), but I did not include them in the recommendation because:
    From what I have seen from other people's code, this is most commonly an error with memory allocation, specifically
    I felt that a complete generalization was too difficult to capture in one article
After all, this doesn't only apply to things you allocate or open; there could be variables whose contents you need to reset after error too, or even more abstract ideas (such as enabling or disabling interrupts, in the case of kernel code).  I initially tried to include all of this into a single idea, but I felt it was more difficult to understand, so I settled for the more concrete example of memory allocation failures, which I find to be more explanatory.
Is the note at the bottom sufficient?
If not, do you have any recommendations?  Would "Use a Goto-Chain when leaving a function on error after allocating multiple objects or opening multiple files" be okay?
                                        Posted by pshirey at Mar 31, 2009 18:41
                                     |
| 
    Please follow the style conventional to other rules (eg Risk Assessment header)
    Like Rob said, the rule is good, but needs to be generalized further. For instance, you can use a goto chain to close open files properly, and include a open/close file in your code samples. You can use "use & release resources" when speaking about the general problem.
                                        Posted by svoboda at Mar 31, 2009 20:05
                                     |
| I liked the malloc() example better.  I just meant declare a struct of some type, and then allocate sizeof struct.  Mix this in with an fopen() / fclose() and your good to go.
Make sure it compiles. The above code won't compile because allocate_object() is not defined.
See David's comments also.
                                        Posted by rcs at Mar 31, 2009 20:11
                                     |
| (In response to the above two posts)
    I added the Risk Assessment header
    I defined the object struct and represented allocation with something that compiles (malloc(sizeof(object_t)))
    I changed the name of the recommendation to encompass all resources
    I added fopen/fclose to the example
    I edited some of the text to reflect these changes
                                        Posted by pshirey at Mar 31, 2009 22:15
                                     |
| Two remaining nits:
    The CCE doesn't free obj3. (Not sure why you have 3 malloc'd objects...I think 2 is sufficient)
    The C++ comment does not belong in Related Vuls. Besides in C++ one would use destructors (and RAII), not goto, so I don't think the comment belongs in this rule.
                                        Posted by svoboda at Mar 31, 2009 22:27
                                     |
| Whoops, that was an oversight on my part.  The CCE now releases all of the allocated resources as well.  I forgot to explicitly express this since it wasn't necessary in the NCE.
    I explicitly free all resources in SUCCESS
    I removed the Related Vulernabilities section
    I removed the third malloc'd object to make the examples a bit shorter.
                                        Posted by pshirey at Mar 31, 2009 23:19
                                     |
| I still think the CCE needs to be neater. It should proably have an explicit free(obj2) somewhere. I also question the wisdom of releasing resources twice, once for success and once for failure. Wouldn't it be easier to have a return code (perhaps a bool), and have the code fall through the 'failure' modes even if successful?  That would mean the failure labels are really 'release' labels. It also means your 'more code' can't use return to exit, but it can use goto success.  This is a really cool rule...any rule that recommends goto is cool.  But the CCE needs more thought to its design.
                                        Posted by svoboda at Apr 01, 2009 07:42
                                     |
| I agree with David.  The type of the rc should be the same as the return type of the function, which, by the way is wrong (see DCL09-C. Declare functions that return errno with a return type of errno_t).  You'll have to think about what the correct values should be.
                                        Posted by rcs at Apr 01, 2009 08:15
                                     |
| I do not feel comfortable adding errno_t as the return value of the function because I cannot find any instance of this type on my system.  I performed a recursive grep on my system for include files containing "errno_t" and none showed up.  There is also no mention of errno_t in errno.h.  All these results remain consistent with the tests I performed on the Andrew server as well.
Since errno_t doesn't exist on any of the machines that I have access to, wouldn't this create a compatibility issue?  I could define my own errno_t, but that seems contrived and unrelated to the purpose of this example.
The main issue is, I can't get the example to compile that way.  But perhaps I am misunderstanding DCL09-C.
                                        Posted by pshirey at Apr 01, 2009 21:00
                                     |
| Well, it's a give or take; you either have to remember to set the return value every time before you goto, or you have to write the free lines twice at the bottom.  Although the latter option is probably more reasonable, I felt that the former was a bit easier to read and maintain.
I've added a variable for return value though; let me know if you like this version better.
                                        Posted by pshirey at Apr 01, 2009 21:14
                                     |
| Read the threaded discussion at the end of DCL09-C. Declare functions that return errno with a return type of errno_t between Geoff Clare and David Keaton (two heavy weights) regarding this very issue. I can't really add anything to this discussion.
                                        Posted by rcs at Apr 01, 2009 21:18
                                     |
| The CCE is better.
Yes, the approach is give & take. I would probably have initialized retval to error, and change it to success only before the SUCCESS label. But your way is also reasonable, so I'll concede that point.
My only remaining suggestion is to use errno_t as Rob suggests. Go ahead and reference DCL09 if you want to explain why doing it. Define errno_t yourself (as int) if you want it to compile (see the discussion Rob cites for why), but don't define it in the NCCE or CS. That means your return values will be different...NOERR and some standard error value.
                                        Posted by svoboda at Apr 01, 2009 22:38
                                     |
| The examples now contain errno_t.  The return value will now either be NOERR or the errno value returned by the function that failed to gather a resource.
However, NOERR isn't defined in errno.h either, so this is another compatibility issue.  But I assume that this is permissible.
                                        Posted by pshirey at Apr 03, 2009 03:14
                                     |
| Well done. I'd say this rule is now complete.
                                        Posted by svoboda at Apr 03, 2009 10:21
                                     |
| I think the code would be more clear if you simply initialized your resources to NULL, and then used a single goto label like this:
out:
    if (fin) {
        fclose(fin);
    }
    free(obj1);
    free(obj2);
    return ret_val;

![](images/icons/contenttypes/comment_16.png) Posted by dsp@dsp.name at Apr 05, 2009 22:55
\| \|
This is a common simpler approach, and is sometimes useful. The disadvantage of it occurs when you need to prepend every access to your resources with `if (ptr != NULL)`, which bloats the code. And forgetting to check for NULL each time you access a resource is not just a bug but a vulnerability, as dereferencing null pointers usually crashes a program.
This rule's suggested solution prevents memory leaks or null pointer dereferences. So it is safer.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 06, 2009 11:19
\| \|
> The disadvantage of it occurs when you need to prepend every access to your resources with `if (ptr != NULL)`, which bloats the code.

I don't see how prefixing with a test, when necessary (it isn't for free()), bloats the code.; How are you defining bloat?   
> This rule's suggested solution prevents memory leaks or null pointer dereferences. So it is safer.

The solution I presented also prevents memory leaks and null pointer dereferences.  I think it has the added benefit that most programmers will find it easier to read.  The code is easier to maintain and extend by both minimizing (or at least simplifying) the use of goto, and eliminating the need for cleanup to be ordered in a specific way.
![](images/icons/contenttypes/comment_16.png) Posted by dsp@dsp.name at Apr 06, 2009 14:19
\| \|
I see what you're saying, and while that would not be a bad technique for this particular code example, it wouldn't illustrate the concept of a `goto` chain because it would only require one `goto`. So it's more of an issue with the example in general. I would have come up with something more complicated, but I think the fundamental idea is conveyed best with something simple.
However, you can find a much better ("real-life") example in the linux kernel (2.6.xx). Check out the function `copy_process()` in `kernel/fork.c`. (This is where I got the idea, actually) In the most recent version, the chain has 17 `goto` labels – and you certainly wouldn't want to remove them because that would make the code significantly more complicated (and, not to mention, less efficient *and* less "secure").
Come to think of it, do you think I should cite this in the recommendation?
![](images/icons/contenttypes/comment_16.png) Posted by pshirey at Apr 06, 2009 15:18
\| \|
I see. Doug's point is that a goto chain is necessary only when closing resources in a manner that requires that the resource be successfully opened. Since free() takes a null pointer, you can free() a malloc() result regardless of if malloc() returns null. Likewise, by prepending a null check to fclose(), you can close a file regardless of whether it was successfully opened or not. So for opening files and freeing pointers, Doug's 'chainless goto' approach works.
The goto chain is really useful only when your resource-close code behaves depends on the success of your resource-open code. IOW it may crash or behave badly if the resource wasn't opened properly and cannot be 'cleanly closed'.
The upshot is, we need a better NCCE/CS pair that demonstrates a resource-open & resource-close pair where the close code requires that the open code succeeded. Such an example will not be fixable by Doug's suggestion, whereas the current NCCE/CS could.
Philip, you should definitely cite the Linux copy_process() example...you can even quote it in it's own Compliant Solution section.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 07, 2009 09:47
\| \|
What would be the best approach for citing the linux kernel? I added a small bit of text in the compliant solution section, but I'm not sure if this was the right idea or not.
I can come up with a better example later, if you think this is best.
![](images/icons/contenttypes/comment_16.png) Posted by pshirey at Apr 08, 2009 18:30
\| \|
What I had in mind wrt the linux kernel is a separate 'Compliant Solution' which describes the copy_process, and shows the copy_process code (perhaps simplified to illustrate your point). A link to the kernal code is good; the link should be mirrored in the References.
Besides, it might provide a counterexample to Doug Porter's claim (that you can use just one goto label to clean up everything). Your current CCE could be simplified as Doug suggests (though I don't think you should change it).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 09, 2009 10:23
\| \|
> Besides, it might provide a counterexample to Doug Porter's claim (that you can use just one goto label to clean up everything).

You can cleanup everything without ever using goto.; Careful, limited, and consistent use of goto can just ease cleanup in some situations.  I think it is inappropriate to cite the copy_process() function from Linux as an example of using goto to write secure code.  In kernels there are a lot of situations where simplicity and readability suffer for the sake of performance.  If you can easily audit copy_process(), you're much smarter than me.
A core tenet of writing secure code is writing simple code.  Keeping it simple reduces the likelihood of making errors in the first place, and decreases the amount of effort required to later bug fix, extend, or audit the software.  If any use of goto is going to be advocated on this site, it should adhere to this core principle.
![](images/icons/contenttypes/comment_16.png) Posted by dsp@dsp.name at Apr 11, 2009 12:06
\| \|
Pasting the code probably wouldn't be such a good idea; it's over 350 lines just for that one function, and it relies on many more structs and routines (easily amounting to over a thousand lines of code), so I don't think mirroring it would work very well.
I suppose if you really wanted to, you could provide checks for bad/unallocated values in *almost* all kinds of resource-freeing functions (like NULL in `free` and `fclose`), but I think that's more (unnecessary) work than just explicitly stating what your code is doing in the relevant function.
I agree that it is more "secure" for the other functions to check for bad values when possible, but at the same time, I don't see any reason to rely on the behavior of a bunch of other functions when you already know precisely which resources need to be released, or which aspects of the state need to be reverted.
![](images/icons/contenttypes/comment_16.png) Posted by pshirey at Apr 11, 2009 16:48
\| \|
I have made an excerpt of the `copy_process()` function, and added it as a Compliant Solution.
I have also modified the original NCCE/CS pair to open two files and `malloc` one object (rather than open one file and malloc two). IMHO this adequately addresses Doug's issue.
It's true that you can free pointers in any order, and freeing a NULL pointer is guaranteed to do nothing, acording to C99). Consequently, if you malloc two or more pointers, and malloc fails on one, you can pass all your pointers to free w/o needing a goto chain.
However C99 makes no promises wrt passing a NULL pointer to `fclose()`. Therefore for maximum portability you need to pass fclose() only pointers containing the result of a successful call to fopen(). Consequently opening two or more files requires a goto chain to close only those files successfully opened.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 13, 2009 11:32
\| \|
I think this is a bad recommendation.
It is too easy to mess up the label to jump to, especially when modifying the code.; Also, such "goto chains" would not help you, if the logic of this function was not liner:  
``` java
if (foo())
{
    grab resource A
    ...
}
else
{
    grab resource B
    ...
}
```
Instead, in such cases, I prefer initializing all local resource handle variables to some "No Resource" value (NULL for pointers, 0 for file descriptors, etc).  Then use a single "cleanup" label, where each resource handle variable is checked for "do I still have the resource" and the resource is released if it does.  (Note: if the resource is malloced memory, you do not even need to check whether the pointer is NULL -- ANSI C defines "free(NULL)" as a noop).  
So here is you example using my style:
``` java
errno_t do_something(void) {
    FILE *fin1 = NULL, *fin2 = NULL;
    object_t *obj = NULL;
    errno_t ret_val = NOERR; // Initially assume a successful return value
    fin1 = fopen("some_file", "r");
    if (fin == NULL) {
        ret_val = errno;
        goto CLEANUP;
    }
    fin2 = fopen("some_other_file", "r");
    if (fin2 == NULL) {
        ret_val = errno;
        goto CLEANUP;
    }
    obj = malloc(sizeof(object_t));
    if (obj == NULL) {
        ret_val = errno;
        goto CLEANUP;
    }
    // ... more code ...
    CLEANUP:// Clean up everything
    free(obj);
    if (fin2 != NULL)
        fclose(fin2);
    if (fin1 != NULL)
        fclose(fin1);
    return ret_val;
}
```
![](images/icons/contenttypes/comment_16.png) Posted by igorlord@alum.mit.edu at Sep 30, 2010 11:46
\| \|
I would argue that a goto chain works with a nonlinear function if you restrict the goto chain to linear sections:
``` java
if (foo())
{
    grab resource A
    ...
  clean1:
  clean resource A
}
else
{
    grab resource B
    ...
  clean2:
  clean resource B
}
```
I'll agree that your style is less error-prone wrt the goto labels. Two disadvantages:
-   It is slightly slower, due to initializing your pointers to NULL & checking them all later. (Of course, if you were concerned with efficienty your function wouldn't be gib enough to necessitate a goto chain at all.)
<!-- -->
-   It is applicable only when your resource variables can take out-of-bounds values such as NULL. This requires them not to be 'const' for instance.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 30, 2010 17:15
\| \|
There is a wrong parameter name in the first compliant solution:  
`errno_t do_something(``void``) {`
`  ``FILE` `*fin1, *fin2;`
`  ``object_t *obj;`
`  ``errno_t ret_val = NOERR; ``/* Initially assume a successful return value */`
`  ``fin1 = ``fopen``(``"some_file"``, ``"r"``);`
**`  ``if` `(fin == NULL) {`**`  /* should be fin1, not fin */`
`    ``ret_val = ``errno``;`
`    ``goto` `FAIL_FIN1;`
`  ``}`  
`/* ... */ `
![](images/icons/contenttypes/comment_16.png) Posted by sami.merila at Aug 25, 2014 01:37
\| \|
Thank you for pointing that out, I've correct the typo.
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Aug 25, 2014 09:22
\| \|
Considering that this practice is being currently called out as a C++ anti-pattern (e.g. [Modernizing Legacy C++ Code](https://github.com/CppCon/CppCon2014/blob/master/Presentations/Modernizing%20Legacy%20C++%20Code/Modernizing%20Legacy%20C++%20Code%20-%20Gregory%20and%20McNellis%20-%20CppCon%202014.pdf?raw=true), slide 7) in favor of RAII, I would think this recommendation should be labeled "not-for-cpp".
![](images/icons/contenttypes/comment_16.png) Posted by brian.szuter at Oct 31, 2014 08:08
\| \|
Yes, RAII is preferable to goto chains, which is effectively covered by;[VOID MEM13-CPP. Use smart pointers instead of raw pointers for resource management](https://wiki.sei.cmu.edu/confluence/display/cplusplus/VOID+MEM13-CPP.+Use+smart+pointers+instead+of+raw+pointers+for+resource+management). I've added the label, thanks!
![](images/icons/contenttypes/comment_16.png) Posted by aballman at Oct 31, 2014 10:34
\| \|
There was a time when a GOTO chain was considered reasonable behavior for resource (or other) clean-up in the face of a nested error, but this is no longer really the case in several coding shops now-a-days (and in some places for more than 25+ years).; It is now considered an old or antiquated form (almost or pretty much a bad design pattern, or anti-pattern).  Better form now-a-days is nested success (looks like nested "try-catch") as with something like:
    int do_something(void)
    {
        FILE        *afp ;
        int        errval = NOERR ;
        int        tmpval ;
        if ((afp = fopen("fileA","r")) != NULL) { /* try */
            FILE        *bfp ;
            if ((bfp = fopen("fileB","r")) != NULL) { /* try */
                const size_t    objlen = sizeof(object_t) ;
                object_t        *objbuf ;
                if ((objbuf = (object_t *) malloc(objlen)) != NULL) { /* try */
                    size_t    len ;
                    while ((len = fread(objbuf,objlen,1,afp)) > 0) {
                        /* processing */
                    } /* end while */
                    if ((errval == NOERR) && ferror(afp)) errval = Exxx ;
                    free(objbuf) ;
                } else { /* catch */
                    errval = ENOMEM ;    
                    /* possible error report */
                } /* end if (memory-allocation) */
                tmpval = fclose(bfp) ;
                if ((errval == NOERR) && (tmpret == EOF)) errval = errno ;
             } else { /* catch */
                errval = errno ;
                /* possible more reporting */
            } /* end if (file-open B) */
            tmpval = fclose(afp) ;
            if ((errval == NOERR) && (tmpval == EOF)) errval = errno ;
        } else { /* catch */
            errval = errno ;
            /* possible error reporting */
        } /* end if (file-open A) */
        return errval ;
    }
    /* end subroutine (do_something) */
This kind of style sort of follows the nested "try-catch" design pattern from C++ and is now a much more preferred form (cleaner, more readable, better minimally scoped variables, less error prone, et cetera). Actually, it predates "try-catch" but who is counting? The above 'try' and 'catch' comments are not often (or never) actually used though. I included them to made the design pattern more explicit. If the nest is too deep, resort to a subroutine to continue nesting with the outer initialized variables passed down. Too many variables? create a struct and pass that down (as a pointer). Programmers can use their own imaginations to keep things maximally clean and readable (and minimally error prone). About the error return philosophy: rule is to return the first error encountered.
Here (below) is a related companion form for initializing within a subroutine and keeping things open (initialized) and then closing after all processing ends.  This is object oriented (no apologies whatsoever). The principal nested resource allocation-initialization is in the object "start" subroutine (method), along w/ the necessary resource cleanup on allocation-initialization failure.
    struct objproc {
        FILE        *afp ;
        FILE        *bfp ;
        size_t    objlen ;
        object_t    *objbuf ;
    } ;
    int do_something(void)
    {
        struct objproc    procer = { NULL } ;
        int               errval ;
        if ((errval = objproc_start(&procer)) == NOERR) {
            int    tmpret ;
            {
                errval = objproc_process(&procer) ;
            }
            tmpret = objproc_finish(&procer) ;
            if (errval == NOERR) errval = tmpret ;
        } else {
            /* possible error handling */
        } /* end if (processing) */
        return errval ;
    }
    /* end subroutine (do_something) */
    /* our object for processing */
    int objproc_start(struct objproc *procp)
    {
        int        retval = NOERR ;
       if (procp == NULL) return EFAULT ;
       memset(procp,0,sizeof(object_t)) ; /* maximum object hiding */
        if ((procp->afp = fopen("fileA","r")) != NULL) {
            FILE        *bfp ;
            if ((procp->bfp = fopen("fileB","r")) != NULL) {
                object_t    *objp ;
                const size_t    objl = sizeof(object_t) ;
                if ((objp = (object_t *) malloc(objl)) != NULL) {
                    procp->objbuf = objp ;
                    procp->objlen = objl ;
                } else {
                    retval = ENOMEM ;    
                } /* end if (memory-allocation) */
                if (retval != NOERR) {
                    (void) fclose(procp->bfp) ;
                    procp->bfp = NULL ;
                }
             } else {
                retval = errno ;
            } /* end if (file-open B) */
            if (retval != NOERR) {
                (void) fclose(procp->afp) ;
                procp->afp = NULL ;
            }
        } else {
            retval = errno ;
        } /* end if (file-open A) */
        return retval ;
    }
    /* end subroutine (objproc_start) */
    int objproc_finish(struct objproc *procp)
    {
        int        retval = NOERR ;
        int        tmpret ;
       if (procp == NULL) return EFAULT ;
        if (procp->objbuf != NULL) {
            free(procp->objbuf) ;
            procp->objbuf = NULL ;
        }
        if (procp->bfp != NULL) {
            tmpret  = fclose(procp->bfp) ;
            procp->bfp = NULL ;
            if ((retval == NOERR) && (tmpret == EOF)) retval = errno ;
        }
        if (procp->afp != NULL) {
            tmpret  = fclose(procp->afp) ;
            procp->afp = NULL ;
            if ((retval == NOERR) && (tmpret == EOF)) retval = errno ;
        }
        return retval ;
    }
    /* end subroutine (objproc_finish) */
    int objproc_process(struct objproc *procp)
    {
        size_t        len ;
        int            retval = NOERR ;
       if (procp == NULL) return EFAULT ;
        while ((len = fread(procp->objbuf,procp->objlen,1,procp->afp)) > 0) {
            /* processing */
        } /* end while */
        if ((retval == NOERR) && ferror(procp->afp)) {
            retval = Exxx ;
            /* any other error handling */
        }
        return retval ;
    }
    /* end subroutine (objproc_process) */
Yes, no GOTOs at all. Not that I am a (complete) fanatic, but for those interested, here is the defining paper (from 1968!): [Edgar Dijkstra "Go To Statement Considered Harmful.](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf)"  
But like much in coding, many things are a matter of taste. Hopefully everyone agrees on the premise that we want to minimize bugs and increase readability and maintainability.
![](images/icons/contenttypes/comment_16.png) Posted by morano at May 29, 2018 14:23
\| \|
This guideline serves to promote the 'goto' statement for this limited use case. I've added some text to the 'goto chain' compliant solution to explain this.
I've also added a compliant solution that demonstrates the nested-if approach you suggest. It is a good solution, and ideal when the number of resources to manage is small. IMO goto chains are for when there are more than about 3 resources. The example from the Linux kernel manages 17! A nested-if construct would indent such code far too much to the right. Such code is also likely to be tagged as "too complex" by both reviewers and static analysis tools.
Finally, if you can break your resource management among several functions, then you can reduce the number of resources managed by each function to a value small enough to handle with nested ifs. But that introduces other complexities (such as reducing the scope of your local variables...A good idea in general, but not always feasible.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 31, 2018 10:54
\| \|
> The example from the Linux kernel manages 17!

I find that such a number can be reconsidered a bit more.
![](images/icons/emoticons/information.svg) See also a current function implementation: <https://elixir.bootlin.com/linux/v6.3-rc4/source/kernel/fork.c#L2001>
    Markus_Elfring@Sonne:…/Projekte/Linux> spatch …/Projekte/Coccinelle/janitor/show_labels4.cocci fork-excerpt-copy_process.c | rg '^\-[a-z]+' | wc -l
    …
    20
Will you become interested to take another look at any information from sources like the following?
-   Topic “[Source code review around jump label usage (snapshot 2023-03-31)](https://lore.kernel.org/cocci/2f9d7de8-7f99-68cc-f940-a528a1aae70f@web.de/)”
-   Article “[Use of Goto in Systems Code](https://blog.regehr.org/archives/894)” (from 2013-02-04) by John Regehr
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 03, 2023 06:42
\| \|
1.  It is demonstrated that some resources can be properly released by a corresponding selection of jump targets.
2.  Some programmers are sticking to just a single label as an exception handling approach so far.
3.  Under which circumstances would you dare to invest additional development attention for increasing the application of more appropriate labels?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Apr 03, 2023 08:01
\| \|
Markus:Thank for you for your responses.
I suspect that this is a potential area of research. (this == proper resource cleanup in C). In particular, it might be worthwhile to scan code, much like Regehr scanned the Linux kernel, and/or survey developers to see what the current C community actually thinks.  I would be willing to adjust this recommendation based on a paper that did such research and had some definite conclusions to promote...neither link promotes any conclusions.
My current impression, based on both of your links is that there is no consensus in the community on how to best handle resource management in C. (As a contrasting example, the C++ community strongly prefers RAII.)   I personally agree with John Regehr, who said in <https://blog.regehr.org/archives/894#comment-6204>
>   Code should be written in a way that communicates the developer’s intent. Goto is a tool that we sometimes use to accomplish this.

![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Apr 05, 2023 11:23
\|
