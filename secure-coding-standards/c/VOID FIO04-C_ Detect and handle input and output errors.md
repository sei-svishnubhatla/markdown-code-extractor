> [!warning]  
>
> This guideline has been deprecated by
>
> -   [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors)

Input/output functions described in Section 7.21 of the C Standard provide a clear indication of failure or success. Failure to conditionally branch on detection or absence of an input or output error condition can result in undefined or unexpected behavior. Thus, the results of all input/output functions should be checked, and errors should be handled appropriately.
The following table is derived from a similar table by Richard Kettlewell \[[Kettlewell 2002](AA.-Bibliography_87152170.html#AA.Bibliography-Kettlewell02)\]. The successful completion or failure of each of the standard file I/O functions listed in the table is determined by comparing the function's return value with the value listed in the "Error Return" column or else by calling one of the I/O functions mentioned in the same column.

| Function | Successful Return | Error Return |
| ----|----|----|
| fclose | zero | EOF (negative) |
| fflush | zero | EOF (negative) |
| fgetc | character read | EOF 2 |
| fgetpos | zero | nonzero |
| fgets | pointer to string | NULL |
| fprintf | number of characters (nonnegative) | negative |
| fputc | character written | EOF 1 |
| fputs | nonnegative | EOF (negative) |
| fread | elements read | elements read |
| freopen | pointer to stream | NULL |
| fscanf | number of conversions (non-negative) | EOF (negative) |
| fseek | zero | nonzero |
| fsetpos | zero | nonzero |
| ftell | file position | −1L |
| fwrite | elements written | elements written |
| getc | character read | EOF 2 |
| getchar | character read | EOF 2 |
| printf | number of characters (nonnegative) | negative |
| putc | character written | EOF 1 |
| putchar | character written | EOF 1 |
| puts | nonnegative | EOF (negative) |
| remove | zero | nonzero |
| rename | zero | nonzero |
| setvbuf | zero | nonzero |
| scanf | number of conversions (nonnegative) | EOF (negative) |
| snprintf | number of characters that would be written (nonnegative) | negative |
| sscanf | number of conversions (nonnegative) | EOF (negative) |
| tmpfile | pointer to stream | NULL |
| tmpnam | non-null pointer | NULL |
| ungetc | character pushed back | EOF (negative; see below) |
| vfprintf | number of characters (nonnegative) | negative |
| vfscanf | number of conversions (nonnegative) | EOF (negative) |
| vprintf | number of characters (nonnegative) | negative |
| vscanf | number of conversions (nonnegative) | EOF (negative) |

When [void FIO35-C. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_) applies, callers shall determine the success or failure of the functions above as follows:
1.  By calling `ferror`
2.  By calling `ferror` and `feof`
The `ungetc()` function does not set the error indicator even when it fails, so it is not possible to check for errors reliably unless it is known that the argument is not equal to `EOF`. The C Standard, section 7.21.7.10 \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\], states that "one character of pushback is guaranteed," so this should not be an issue if at most one character is ever pushed back before reading again. (See [FIO13-C. Never push back anything other than one read character](FIO13-C_%20Never%20push%20back%20anything%20other%20than%20one%20read%20character).)
## Noncompliant Code Example (`fseek`)
In this noncompliant code example, the `fseek()` function is used to set the file position to a location `offset` in the file referred to by `file` before reading a sequence of bytes from the file. However, if an I/O error occurs during the seek operation, the subsequent read will fill the buffer with the wrong content.
``` c
size_t read_at(FILE *file, long offset, void *buf, size_t nbytes) {
  fseek(file, offset, SEEK_SET);
  return fread(buf, 1, nbytes, file);
}
```
## Compliant Solution (`fseek`)
According to the C Standard, the `fseek()` function returns a nonzero value to indicate that an error occurred. Testing for this condition before reading from the file eliminates the chance of operating on the wrong portion of the file if `fseek()` failed. Before operating on a file, always test the returned value of `fseek()` to make sure an error did not occur. If an error occurred, handle it appropriately.
``` c
size_t read_at(FILE *file, long offset, void *buf, size_t nbytes) {
  if (fseek(file, offset, SEEK_SET) != 0) {
    /* Indicate error to caller */
    return 0;
  }
  return fread(buf, 1, nbytes, file);
}
```
## Noncompliant Code Example (`snprintf`)
In the following noncompliant code example, `snprinf()` is assumed to succeed. However, if the call fails (for example, because of insufficient memory, as described in GNU libc bug [441945](http://bugzilla.redhat.com/show_bug.cgi?id=441945)), the subsequent call to `log_message()` is likely to result in undefined behavior because the character buffer is not initialized and need not be null-terminated.
``` c
extern void log_message(const char*);
void f(int i, int width, int prec) {
  char buf[40];
  snprintf(buf, sizeof buf, "i = %*.*i", width, prec, i);
  log_message(buf);
  /* ... */
}
```
## Compliant Solution (`snprintf`)
A compliant solution avoids assuming that `snprintf()` succeeds regardless of its arguments and tests the return value of the function before using the buffer the function was passed to format output into. In addition, a compliant solution takes care to null-terminate the formatted string in case the provided buffer wasn't large enough for `snprintf()` to append the terminating `NULL`.
``` c
extern void log_message(const char*);
void f(int i, int width, int prec) {
  char buf[40];
  int n;
  n = snprintf(buf, sizeof buf, "i = %*.*i", width, prec, i);
  if (n < 0) {
    /* Handle snprintf() error */
    strcpy(buf, "unknown error");
  }
  /* Null-terminate buffer in case of overflow */
  buf[sizeof buf - 1] = '\0';    
  log_message(buf);
}
```
When the length of the formatted string is unbounded, it is best to invoke the function twice: first invoke it with a `NULL` buffer to determine the size of output (and dynamically allocate a buffer of sufficient size), and then call `snprintf()` again to format the output into the dynamically allocated buffer. Even with this approach, the success of all calls still needs to be tested, and any errors must be appropriately handled. A possible optimization is to first attempt to format the string into a reasonably small buffer allocated on the stack, and only when the buffer turns out to be too small, dynamically allocate one of a sufficient size. This approach is shown in the following compliant solution:
``` c
void f(int i, int width, int prec) {
  char buffer[20];
  char *buf = buffer;
  int n  = sizeof buffer;
  const char fmt[] = "i = %*.*i";
  n = snprintf(buf, n, fmt, width, prec, i);
  if (n < 0) {
    /* Handle snprintf() error */
    strcpy(buffer, "unknown error");
    goto write_log;
  }
  if (n < sizeof buffer)
    goto write_log;
  buf = (char*)malloc(n + 1);
  if (NULL == buf) {
    /* Handle malloc() error */
    strcpy(buffer, "unknown error");
    goto write_log;
  }
  n = snprintf(buf, n, fmt, width, prec, i);
  if (n < 0) {
    /* Handle snprintf() error */
    strcpy(buffer, "unknown error");
  }
write_log:
  log_message(buf);
  if (buf != buffer)
    free(buf);
}
```
Note that this solution correctly handles memory allocation errors in accordance with [void MEM32-C. Detect and handle memory allocation errors](void%20MEM32-C_%20Detect%20and%20handle%20memory%20allocation%20errors) and uses the `goto` statement as suggested in [MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources](MEM12-C_%20Consider%20using%20a%20goto%20chain%20when%20leaving%20a%20function%20on%20error%20when%20using%20and%20releasing%20resources).
## Exceptions
**EXP12-EX1:** The exception from [EXP12-C. Do not ignore values returned by functions](https://www.securecoding.cert.org/confluence/display/seccode/EXP12-C.+Do+not+ignore+values+returned+by+functions) still applies. If the return value is inconsequential or if any errors can be safely ignored, such as for functions called because of their side effects, the function should be explicitly cast to `void` to signify programmer intent. For an example of this exception, see "Compliant Solution (Remove Existing Destination File)" under "Portable Behavior" in [FIO10-C. Take care when using the rename() function](https://www.securecoding.cert.org/confluence/display/seccode/FIO10-C.+Take+care+when+using+the+rename%28%29+function).
## Risk Assessment
Failure to check file operation errors can result in unexpected behavior.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| FIO04-C | medium | probable | high | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE | ; | ; | Can detect violations of this recommendation when checking for violations of EXP12-C. Do not ignore values returned by functions. |
| Coverity | 2017.07 | CHECKED_RETURN | Finds inconsistencies in how function call return values are handled. Coverity Prevent cannot discover all violations of this recommendation, so further verification is necessary. |
| ECLAIR | 1.2 | CC2.FIO04 | Partially implemented. |
| LDRA tool suite | 9.7.1 | 80 D | Partially implemented. |
| PRQA QA-C | Unable to render {include} The included page could not be found. | 3200 | Partially implemented. |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO04-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID FIO04-CPP. Detect and handle input and output errors |
| ISO/IEC TS 17961 (Draft) | Failing to detect and handle standard library errors [liberr] |
| MITRE CWE | CWE-391, Unchecked error condition |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.21.7.10, "The ungetc Function" |
| [Kettlewell 2002] | Section 6, "I/O Error Checking" |
| [Seacord 2005a] | Chapter 7, "File I/O" |

------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/FIO03-C.+Do+not+make+assumptions+about+fopen()+and+file+creation?showChildren=false&showComments=false)[](https://www.securecoding.cert.org/confluence/pages/viewpage.action?pageId=1040)[](https://www.securecoding.cert.org/confluence/display/seccode/FIO05-C.+Identify+files+using+multiple+file+attributes?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Why is this only a recommendation and not a rule? Seems to me like checking return codes should be something we take for granted
                                        Posted by avolkovi at Mar 06, 2008 09:51
                                     |
| We split this between this recommendation and the following rule:
FIO33-C. Detect and handle input output errors resulting in undefined behavior
The idea was that ignoring the return codes for the functions listed in FIO33-C would lead to undefined behavior, while ignoring the return codes from the functions listed here was just more of a bad idea.
                                        Posted by rcs at Mar 06, 2008 10:09
                                     |
| I think generally a rule "always check error return indications from functions, where available" should be a solid rule of which this is a special case.; The two exceptions for standard I/O functions I know of are ungetc when the pushback has just been getc()ed, and outputs to stderr.  The latter is an exception since if the app is trying to do that and it fails, it presumably cannot print a further message about that to stderr.
                                        Posted by dagwyn at Apr 17, 2008 12:11
                                     |
| I think a note should be added (somewhere) to the effect that even though one might naively thing that fclose cannot fail, for an output stream there is a final buffer flush that might fail.; Further, for fclose() and even for close() on an output stream, a "successful" return does not guarantee that the actual physical I/O operation succeeded, only that the data was transferred to the supporting OS file manager module/buffer.  If the system crashes before the next "sync" (Unix utility), the data may still be lost.
                                        Posted by dagwyn at Apr 17, 2008 12:15
                                     |
| why is fgets not in the table?
                                        Posted by avolkovi at Jul 01, 2008 11:00
                                     |

