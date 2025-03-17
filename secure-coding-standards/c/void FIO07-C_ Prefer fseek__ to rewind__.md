> [!warning]  
>
> This guideline has been deprecated by:
>
> -   [ERR07-C. Prefer functions that support error checking over equivalent functions that don't](ERR07-C_%20Prefer%20functions%20that%20support%20error%20checking%20over%20equivalent%20functions%20that%20don't)

Section 7.21.9.5 of the C Standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] defines the `rewind()` function as follows:
> The `rewind` function sets the file position indicator for the stream pointed to by `stream` to the beginning of the file. It is equivalent to
>
> ``` java
>  (void)fseek(stream, 0L, SEEK_SET) 
> ```
>
> except that the error indicator for the `stream` is also cleared.

Consequently, `fseek()` should be used instead of `rewind()` to validate that the stream was successfully rewound.
## Noncompliant Code Example
This noncompliant code example sets the file position indicator of an input stream back to the beginning using `rewind()`:
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "r");
if (fp == NULL) {
  /* Handle open error */
}
/* Read data */
rewind(fp);
/* Continue */
```
However, it is impossible to determine if `rewind()` succeeded.
## Compliant Solution
This compliant solution uses `fseek()` instead of `rewind()` and checks to see if the operation succeeded:
``` c
char *file_name;
FILE *fp;
/* Initialize file_name */
fp = fopen(file_name, "r");
if (fp == NULL) {
  /* Handle open error */
}
/* Read data */
if (fseek(fp, 0L, SEEK_SET) != 0) {
  /* Handle repositioning error */
}
/* Continue */
```
## Risk Assessment
Using `rewind()` makes it impossible to determine if the file position indicator was set back to the beginning of the file, potentially resulting in improper control flow.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO07-C | low | unlikely | low | P3 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | ; |
| ECLAIR | 1.2 | CC2.FIO07 | Fully implemented |
| LDRA tool suite | 9.7.1 | 593 S | Fully implemented |
| PRQA QA-C | Unable to render {include} The included page could not be found. | Warncall -wc rewind | Partially implemented |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO07-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO07-CPP. Prefer fseek() to rewind() |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.21.9.5, "The rewind Function" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FIO06-C.+Create+files+with+appropriate+access+permissions?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040) [](https://www.securecoding.cert.org/confluence/display/seccode/FIO08-C.+Take+care+when+calling+remove()+on+an+open+file?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| I think it would be helpful to include a real-world example - even a contrived-but-plausaible one - where this would make a difference. If the FILE pointer is bogus, the followon I/O call (fread or whatever) will fail too. No big deal.
The only example I can think of is trying to do stdio on a character device like a serial port or a socket, and this may well be the example that matters (i.e., somebody opening /dev/fd/0).
But giving a real example would make it *real*.;
                                        Posted by steve at Mar 14, 2008 02:04
                                     |
| There are non-seekable file types - the best known example being a pipe.  That means that the rewind/fseek will fail but subsequent reads or writes will continue to work. I believe that some (but by no means all) character devices are non-seekable - I'm thinking of terminals, /dev/random, etc.  Named FIFOs are not seekable, IIRC.
On the subject of named FIFOs, has any DoS attack been created by creating a FIFO in place of a plain file that a daemon expects to use as a (regular) log file?
                                        Posted by jonathan.leffler@gmail.com at Mar 18, 2008 00:23
                                     |
| This guideline is, IMO adequately, covered in ERR07-C. Prefer functions that support error checking over equivalent functions that don't. I propose to move it to 99. The Void. If no one objects, I'll go ahead and do so.
                                        Posted by martinsebor at Jan 28, 2010 23:39
                                     |
| I would object to removing this rule if it contains any info not covered by ERR07-C. It doesn't; the only problem with rewind() is that it gives no indication of error, which is covered by ERR07-C. So I'm fine with moving this rule to the void.
                                        Posted by svoboda at Jan 29, 2010 16:46
                                     |

