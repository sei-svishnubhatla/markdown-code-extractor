> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [DCL37-C. Do not declare or define a reserved identifier](DCL37-C_%20Do%20not%20declare%20or%20define%20a%20reserved%20identifier)
> -   [MSC38-C. Do not treat as an object any predefined identifier that might be implemented as a macro](MSC38-C_%20Do%20not%20treat%20a%20predefined%20identifier%20as%20an%20object%20if%20it%20might%20only%20be%20implemented%20as%20a%20macro)

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=6619179) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=6619150) [](https://www.securecoding.cert.org/confluence/display/seccode/ERR32-C.+Do+not+rely+on+indeterminate+values+of+errno?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I don't think that the errno macro could ever expand to
*errno()

but because that's self-definitional. More likely something like
``` java
#define errno ( *__errno() )  <-- wiki ate the underscores
```
This may well make it "click" for the reader
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 11:05
\| \|
No, `*errno()` is valid.; See C99 section 6.10.3.4 paragraph 2.
> If the name of the macro being replaced is found during this scan of the replacement list (not including the rest of the source file's preprocessing tokens), it is not replaced.  Furthermore, if any nested replacements encounter the name of the macro being replaced, it is not replaced. These nonreplaced macro name preprocessing tokens are no longer available for further replacement even if they are later (re)examined in contexts in which that macro name preprocessing token would otherwise have been replaced.

![](images/icons/contenttypes/comment_16.png) Posted by dmk at Mar 14, 2008 12:58
\| \|
Fair enough, if it's valid it's valid, but I think it's less clear doing it this way; I believe the goal ought to be to convey the message to the reader what's going on - especially one for whom it may never occur that errno is not an int variable - and relying on that bit of knowledge may make it harder to get the point across.
![](images/icons/contenttypes/comment_16.png) Posted by steve at Mar 14, 2008 13:31
\| \|
"Conforming implementations are required to declare errno in \<errno.h\>, although some historic implementations failed to do so." Conform what? C99?
![](images/icons/contenttypes/comment_16.png) Posted by masaki at Feb 04, 2009 21:47
\| \|
Yes. I've adjusted the text to make this clearer.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Feb 05, 2009 09:35
\| \|
Isn't this rule covered by DCL36-C?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Nov 05, 2009 20:20
\| \|
I don't think [DCL36-C. Do not declare an identifier with conflicting linkage classifications](DCL36-C_%20Do%20not%20declare%20an%20identifier%20with%20conflicting%20linkage%20classifications) necessarily covers all possible violations of this rule, but [DCL37-C. Do not use identifiers that are reserved for the implementation](/confluence/pages/createpage.action?spaceKey=c&title=DCL37-C.+Do+not+use+identifiers+that+are+reserved+for+the+implementation) does (as the Deprecation note at the top of this page indicates).
I think this rule can be moved to [99. The Void](/confluence/pages/createpage.action?spaceKey=c&title=99.+The+Void).
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Feb 04, 2011 16:20
\| \|
i moved the errno nce/cs to [DCL37-C. Do not use identifiers that are reserved for the implementation](/confluence/pages/createpage.action?spaceKey=c&title=DCL37-C.+Do+not+use+identifiers+that+are+reserved+for+the+implementation) and also the automated analysis by LDRA.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Feb 06, 2011 11:31
\|
