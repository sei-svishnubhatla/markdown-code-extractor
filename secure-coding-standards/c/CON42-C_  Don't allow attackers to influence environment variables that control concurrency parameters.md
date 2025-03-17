> [!info]  
> This rule is under construction. 

The recommended way to use OpenMP is to specify most of the performance parameters in environment variables so that administrators can tweak them for their environment:
For example,
-   Set the default number of threads to use.
–     **OMP_NUM_THREADS *int_literal***
-   OpenMP added an environment variable to control the size of
child threads’ stack
–     **OMP_STACKSIZE**
-   Also added an environment variable to hint to runtime how to
treat idle threads
–     **OMP_WAIT_POLICY**
–     Process binding is enabled if this variable is true … i.e. if true
the runtime will not move threads around between processors.
– **OMP_PROC_BIND true \| false**
The downside of this is that if an attacker can manage to control these variables, they can devastate the performance, for example, they can serialize the program by setting the number of threads to 1.
CAPEC has a generic description of a similar attack pattern:  <https://capec.mitre.org/data/definitions/10.html>
The risk is not limited to OpenMP, and the preferred mitigation is most likely to make sure that environment variables cannot be manipulated.  This would probably make the use of environment variables in OpenMP program ill-advised for set-uid-root programs, for example, where a less privileged user controls the environment.
## Comments:

|  |
| ----|
| OMP_STACKSIZE is especially spooky.; Specify a small stack size and crash the program?
                                        Posted by rcs at Jan 19, 2015 08:10
                                     |
| This all hinges off that being a valid recommended way to use OpenMP;– what source actually recommends that? Perhaps the rule should simply be "don't do that"?Also, I'm not certain how this would be enforceable as a rule – the point to using an environment variable is to allow it to be modifiable external to the program. What range of values is considered "acceptable" for ensuring validity? For instance, setting the number of threads to 1 may destroy performance, but it may also be a totally valid work-around for a yet-to-be-discovered concurrency bug, and so the programmer may wish to allow that value to keep a production server hobbling along in a worst case scenario. There's no way to tell the difference between "I'm the admin of this machine and I need that variable set to this value for my own reasons" vs "I'm the bad guy and I want to mess this up."
                                        Posted by aballman at Jan 19, 2015 11:51
                                     |
| 
Introduction to OpenMP - Tim Mattson (Intel)Video 11 part 4 - Synchronize single masters and stuffI'm not sure this hinges off the recommendation.; If someone could do make an error that compiles (even with warnings) that can result in a security vulnerability it is probably rule worthy.  When people are making recommending that you do something dangerous, the importance of communicating things goes up.  Best example of this was probably the double-free vulnerability in the man page for realloc.I'm not sure how to enforce this as a rule either.  Perhaps it is better as a guideline.  I'm a bit reluctant to say don't do this, because you can see the advantage of administrators being able to manage the performance like this for different platforms.  This might be just a basic awareness thing or perhaps just make another example on one of the "don't trust environment variable" rules.
                                        Posted by rcs at Jan 19, 2015 21:20
                                     |

