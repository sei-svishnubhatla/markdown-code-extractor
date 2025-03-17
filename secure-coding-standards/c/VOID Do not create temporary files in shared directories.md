> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Standard. This guideline has not been erased yet in case it contains information that might still be useful.

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=2981912) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Do+not+make+assumptions+about+the+order+of+global+variable+initialization+across+translation+units?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| should we move the discussion about tmpfile_s() into a NCCE and perhaps add an "original" NCCE with a mktemp or something? Or is it really not too necessary since we have TONS of examples in FIO43?
                                        Posted by avolkovi at Jun 19, 2008 10:04
                                     |
| Need a non-compliant code example...probably it just calls mkdir() with no frills, + explanation of why this is insecure.
                                        Posted by svoboda at Jun 22, 2008 08:57
                                     |
| Yes, you are right.  I hate to be having all this doubts about this recommendation at this stage of the game, but shouldn't all the examples NCCE/CS show the creation of a temporary file and not just directories?  A good non-compliant code example might be simply calling tmpfile_s() because it cannot be used to specify a secure directory.  Even though this is a TR24731-1, I think this may be OK because this TR is explicitly stated to be in the scope.
I'm also not too sure about any of the compliant solutions showing how to create a secure directory to create temporary files in.  What bothers me the most is that these directories need to be created in an already secure directory, so what is the point?  I think in most cases the secure directory will already exist as part of the installation.  I think all we need to say here is "use a secure directory" and reference FIO17.
The CS should probably show an example of using mkstemp() with perhaps an initial call to make sure the directory is secure.
                                        Posted by rcs_mgr at Jun 22, 2008 09:29
                                     |

