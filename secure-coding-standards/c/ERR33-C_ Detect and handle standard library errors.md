The majority of the standard library functions, including I/O functions and memory allocation functions, return either a valid value or a value of the correct return type that indicates an error (for example, −1 or a null pointer). Assuming that all calls to such functions will succeed and failing to check the return value for an indication of an error is a dangerous practice that may lead to [unexpected](BB.-Definitions_87152273.html#BB.Definitions-unexpectedbehavior) or [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) when an error occurs. It is essential that programs detect and appropriately handle all errors in accordance with an error-handling policy.
The successful completion or failure of each of the standard library functions listed in the following table shall be determined either by comparing the function’s return value with the value listed in the column labeled “Error Return” or by calling one of the library functions mentioned in the footnotes.
**Standard Library Functions**

| Function | Successful Return | Error Return |
| ----|----|----|
| aligned_alloc() | Pointer to space | NULL |
| asctime_s() | 0 | Nonzero |
| at_quick_exit() | 0 | Nonzero |
| atexit() | 0 | Nonzero |
| bsearch() | Pointer to matching element | NULL |
| bsearch_s() | Pointer to matching element | NULL |
| btowc() | Converted wide character | WEOF |
| c16rtomb() | Number of bytes | (size_t)(-1) |
| c32rtomb() | Number of bytes | (size_t)(-1) |
| calloc() | Pointer to space | NULL |
| clock() | Processor time | (clock_t)(-1) |
| cnd_broadcast() | thrd_success | thrd_error |
| cnd_init() | thrd_success | thrd_nomem or thrd_error |
| cnd_signal() | thrd_success | thrd_error |
| cnd_timedwait() | thrd_success | thrd_timedout or thrd_error |
| cnd_wait() | thrd_success | thrd_error |
| ctime_s() | 0 | Nonzero |
| fclose() | 0 | EOF (negative) |
| fflush() | 0 | EOF (negative) |
| fgetc() | Character read | EOF1 |
| fgetpos() | 0 | Nonzero, errno > 0 |
| fgets() | Pointer to string | NULL |
| fgetwc() | Wide character read | WEOF1 |
| fopen() | Pointer to stream | NULL |
| fopen_s() | 0 | Nonzero |
| fprintf() | Number of characters (nonnegative) | Negative |
| fprintf_s() | Number of characters (nonnegative) | Negative |
| fputc() | Character written | EOF2 |
| fputs() | Nonnegative | EOF (negative) |
| fputwc() | Wide character written; | WEOF |
| fputws() | Nonnegative | EOF (negative) |
| fread() | Elements read | Elements read |
| freopen() | Pointer to stream | NULL |
| freopen_s() | 0 | Nonzero |
| fscanf() | Number of conversions (nonnegative) | EOF (negative) |
| fscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| fseek() | 0 | Nonzero |
| fsetpos() | 0 | Nonzero, errno > 0 |
| ftell() | File position | −1L, errno > 0 |
| fwprintf() | Number of wide characters (nonnegative) | Negative |
| fwprintf_s() | Number of wide characters (nonnegative) | Negative |
| fwrite() | Elements written | Elements written |
| fwscanf() | Number of conversions (nonnegative) | EOF (negative) |
| fwscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| getc() | Character read | EOF1 |
| getchar() | Character read | EOF1 |
| getenv() | Pointer to string | NULL |
| getenv_s() | Pointer to string | NULL |
| gets_s() | Pointer to string | NULL |
| getwc() | Wide character read | WEOF |
| getwchar() | Wide character read | WEOF |
| gmtime() | Pointer to broken-down time | NULL |
| gmtime_s() | Pointer to broken-down time | NULL |
| localtime() | Pointer to broken-down time | NULL |
| localtime_s() | Pointer to broken-down time | NULL |
| malloc() | Pointer to space | NULL |
| mblen(), s != NULL | Number of bytes | −1 |
| mbrlen(), s != NULL | Number of bytes or status | (size_t)(-1) |
| mbrtoc16() | Number of bytes or status | (size_t)(-1), errno == EILSEQ |
| mbrtoc32() | Number of bytes or status | (size_t)(-1), errno == EILSEQ |
| mbrtowc(), s != NULL | Number of bytes or status | (size_t)(-1), errno == EILSEQ |
| mbsrtowcs() | Number of non-null elements | (size_t)(-1), errno == EILSEQ |
| mbsrtowcs_s() | 0 | Nonzero |
| mbstowcs() | Number of non-null elements | (size_t)(-1) |
| mbstowcs_s() | 0 | Nonzero |
| mbtowc(), s != NULL | Number of bytes | −1 |
| memchr() | Pointer to located character | NULL |
| mktime() | Calendar time | (time_t)(-1) |
| mtx_init() | thrd_success | thrd_error |
| mtx_lock() | thrd_success | thrd_error |
| mtx_timedlock() | thrd_success | thrd_timedout or thrd_error |
| mtx_trylock() | thrd_success | thrd_busy or thrd_error |
| mtx_unlock() | thrd_success | thrd_error |
| printf_s() | Number of characters (nonnegative) | Negative |
| putc() | Character written | EOF2 |
| putwc() | Wide character written | WEOF |
| raise() | 0 | Nonzero |
| realloc() | Pointer to space | NULL |
| remove() | 0 | Nonzero |
| rename() | 0 | Nonzero |
| setlocale() | Pointer to string | NULL |
| setvbuf() | 0 | Nonzero |
| scanf() | Number of conversions (nonnegative) | EOF (negative) |
| scanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| signal() | Pointer to previous function | SIG_ERR, errno > 0 |
| snprintf() | Number of characters that would be written (nonnegative) | Negative |
| snprintf_s() | Number of characters that would be written (nonnegative) | Negative |
| sprintf() | Number of non-null characters written | Negative |
| sprintf_s() | Number of non-null characters written | Negative |
| sscanf() | Number of conversions (nonnegative) | EOF (negative) |
| sscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| strchr() | Pointer to located character | NULL |
| strerror_s() | 0 | Nonzero |
| strftime() | Number of non-null characters | 0 |
| strpbrk() | Pointer to located character | NULL |
| strrchr() | Pointer to located character | NULL |
| strstr() | Pointer to located string | NULL |
| strtod() | Converted value | 0, errno == ERANGE |
| strtof() | Converted value | 0, errno == ERANGE |
| strtoimax() | Converted value | INTMAX_MAX or INTMAX_MIN, errno == ERANGE |
| strtok() | Pointer to first character of a token | NULL |
| strtok_s() | Pointer to first character of a token | NULL |
| strtol() | Converted value | LONG_MAX or LONG_MIN, errno == ERANGE |
| strtold() | Converted value | 0, errno == ERANGE |
| strtoll() | Converted value | LLONG_MAX or LLONG_MIN, errno == ERANGE |
| strtoumax() | Converted value | UINTMAX_MAX, errno == ERANGE |
| strtoul() | Converted value | ULONG_MAX, errno == ERANGE |
| strtoull() | Converted value | ULLONG_MAX, errno == ERANGE |
| strxfrm() | Length of transformed string | >= n |
| swprintf() | Number of non-null wide characters | Negative |
| swprintf_s() | Number of non-null wide characters | Negative |
| swscanf() | Number of conversions (nonnegative) | EOF (negative) |
| swscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| thrd_create() | thrd_success | thrd_nomem or thrd_error |
| thrd_detach() | thrd_success | thrd_error |
| thrd_join() | thrd_success | thrd_error |
| thrd_sleep() | 0 | Negative |
| time() | Calendar time | (time_t)(-1) |
| timespec_get() | Base | 0 |
| tmpfile() | Pointer to stream | NULL |
| tmpfile_s() | 0 | Nonzero |
| tmpnam() | Non-null pointer | NULL |
| tmpnam_s() | 0 | Nonzero |
| tss_create() | thrd_success | thrd_error |
| tss_get() | Value of thread-specific storage | 0 |
| tss_set() | thrd_success | thrd_error |
| ungetc() | Character pushed back | EOF (see below) |
| ungetwc() | Character pushed back | WEOF |
| vfprintf() | Number of characters (nonnegative) | Negative |
| vfprintf_s() | Number of characters (nonnegative) | Negative |
| vfscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vfscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| vfwprintf() | Number of wide characters (nonnegative) | Negative |
| vfwprintf_s() | Number of wide characters (nonnegative) | Negative |
| vfwscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vfwscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| vprintf_s() | Number of characters (nonnegative) | Negative |
| vscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| vsnprintf() | Number of characters that would be written (nonnegative) | Negative |
| vsnprintf_s() | Number of characters that would be written (nonnegative) | Negative |
| vsprintf() | Number of non-null characters (nonnegative) | Negative |
| vsprintf_s() | Number of non-null characters (nonnegative) | Negative |
| vsscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vsscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| vswprintf() | Number of non-null wide characters | Negative |
| vswprintf_s() | Number of non-null wide characters | Negative |
| vswscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vswscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| vwprintf_s() | Number of wide characters (nonnegative) | Negative |
| vwscanf() | Number of conversions (nonnegative) | EOF (negative) |
| vwscanf_s() | Number of conversions (nonnegative) | EOF (negative) |
| wcrtomb() | Number of bytes stored | (size_t)(-1) |
| wcschr() | Pointer to located wide character | NULL |
| wcsftime() | Number of non-null wide characters | 0 |
| wcspbrk() | Pointer to located wide character | NULL |
| wcsrchr() | Pointer to located wide character | NULL |
| wcsrtombs() | Number of non-null bytes | (size_t)(-1), errno == EILSEQ |
| wcsrtombs_s() | 0 | Nonzero |
| wcsstr() | Pointer to located wide string | NULL |
| wcstod() | Converted value | 0, errno == ERANGE |
| wcstof() | Converted value | 0, errno == ERANGE |
| wcstoimax() | Converted value | INTMAX_MAX or INTMAX_MIN, errno == ERANGE |
| wcstok() | Pointer to first wide character of a token | NULL |
| wcstok_s() | Pointer to first wide character of a token | NULL |
| wcstol() | Converted value | LONG_MAX or LONG_MIN, errno == ERANGE |
| wcstold() | Converted value | 0, errno == ERANGE |
| wcstoll() | Converted value | LLONG_MAX or LLONG_MIN, errno == ERANGE |
| wcstombs() | Number of non-null bytes | (size_t)(-1) |
| wcstombs_s() | 0 | Nonzero |
| wcstoumax() | Converted value | UINTMAX_MAX, errno == ERANGE |
| wcstoul() | Converted value | ULONG_MAX, errno == ERANGE |
| wcstoull() | Converted value | ULLONG_MAX, errno == ERANGE |
| wcsxfrm() | Length of transformed wide string | >= n |
| wctob() | Converted character | EOF |
| wctomb(), s != NULL | Number of bytes stored | −1 |
| wctomb_s(), s != NULL | Number of bytes stored | −1 |
| wctrans() | Valid argument to towctrans | 0 |
| wctype() | Valid argument to iswctype | 0 |
| wmemchr() | Pointer to located wide character | NULL |
| wprintf_s() | Number of wide characters (nonnegative) | Negative |
| wscanf() | Number of conversions (nonnegative) | EOF (negative) |
| wscanf_s() | Number of conversions (nonnegative) | EOF (negative) |

Note: According to [FIO35-C](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_)[. Use feof() and ferror() to detect end-of-file and file errors when sizeof(int) == sizeof(char)](void%20FIO35-C_%20Use%20feof__%20and%20ferror__%20to%20detect%20end-of-file%20and%20file%20errors%20when%20sizeof_int_%20==%20sizeof_char_), callers should verify end-of-file and file errors for the functions in this table as follows:
<sup>1</sup> By calling `ferror()` and `feof()`  
<sup>2</sup> By calling `ferror()`
The `ungetc()` function does not set the error indicator even when it fails, so it is not possible to check for errors reliably unless it is known that the argument is not equal to `EOF`.
The C Standard 7.31.3.10 paragraph 3 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2024)\] states that
>  )ne wide character of pushback is guaranteed...

so this should not be an issue if, at most, one character is ever pushed back before reading again. (See [FIO13-C](FIO13-C_%20Never%20push%20back%20anything%20other%20than%20one%20read%20character)[. Never push back anything other than one read character](FIO13-C_%20Never%20push%20back%20anything%20other%20than%20one%20read%20character).)
## Noncompliant Code Example (`setlocale()`)
In this noncompliant code example, the function `utf8_to_wcs()` attempts to convert a sequence of UTF-8 characters to wide characters. It first invokes `setlocale()` to set the global locale to the implementation-defined `en_US.UTF-8` but does not check for failure. The `setlocale()` function will fail by returning a null pointer, for example, when the locale is not installed. The function may fail for other reasons as well, such as the lack of resources.  Depending on the sequence of characters pointed to by `utf8`, the subsequent call to `mbstowcs()` may fail or result in the function storing an unexpected sequence of wide characters in the supplied buffer `wcs`.
``` c
#include <locale.h>
#include <stdlib.h>
int utf8_to_wcs(wchar_t *wcs, size_t n, const char *utf8,
                size_t *size) {
  if (NULL == size) {
    return -1;
  }
  setlocale(LC_CTYPE, "en_US.UTF-8");
  *size = mbstowcs(wcs, utf8, n);
  return 0;
}
```
## Compliant Solution (`setlocale()`)
This compliant solution checks the value returned by `setlocale()` and avoids calling `mbstowcs()` if the function fails. The function also takes care to restore the locale to its initial setting before returning control to the caller.
``` c
#include <locale.h>
#include <stdlib.h>
int utf8_to_wcs(wchar_t *wcs, size_t n, const char *utf8,
                size_t *size) {
  if (NULL == size) {
    return -1;
  }
  const char *save = setlocale(LC_CTYPE, "en_US.UTF-8");
  if (NULL == save) {
    return -1;
  }
  *size = mbstowcs(wcs, utf8, n);
  if (NULL == setlocale(LC_CTYPE, save)) {
    return -1;
  }
  return 0;
}
```
## Noncompliant Code Example (`calloc()`)
In this noncompliant code example, `temp_num`,` tmp2`, and `num_of_records` are derived from a [tainted source](BB.-Definitions_87152273.html#BB.Definitions-taintedsource). Consequently, an attacker can easily cause `calloc()` to fail by providing a large value for `num_of_records`. 
``` c
#include <stdlib.h>
#include <string.h>
enum { SIG_DESC_SIZE = 32 };
typedef struct {
  char sig_desc[SIG_DESC_SIZE];
} signal_info;
void func(size_t num_of_records, size_t temp_num,
          const char *tmp2, size_t tmp2_size_bytes) {
  signal_info *start = (signal_info *)calloc(num_of_records,
                                          sizeof(signal_info));
  if (tmp2 == NULL) {
    /* Handle error */
  } else if (temp_num > num_of_records || temp_num == 0) {
    /* Handle error */
  } else if (tmp2_size_bytes < SIG_DESC_SIZE) {
    /* Handle error */
  }
  signal_info *point = start + temp_num - 1;
  memcpy(point->sig_desc, tmp2, SIG_DESC_SIZE);
  point->sig_desc[SIG_DESC_SIZE - 1] = '\0';
  /* ... */
  free(start);
}
```
When `calloc()` fails, it returns a null pointer that is assigned to `start`. If `start` is null, an attacker can provide a value for `temp_num` that, when scaled by `sizeof(signal_info)`, references a writable address to which control is eventually transferred. The contents of the string referenced by `tmp2` can then be used to overwrite the address, resulting in an arbitrary code execution [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability).
## Compliant Solution (`calloc()`)
To correct this error, ensure the pointer returned by `calloc()` is not null:
``` c
#include <stdlib.h>
#include <string.h>
enum { SIG_DESC_SIZE = 32 };
typedef struct {
  char sig_desc[SIG_DESC_SIZE];
} signal_info;
void func(size_t num_of_records, size_t temp_num,
          const char *tmp2, size_t tmp2_size_bytes) {
  signal_info *start = (signal_info *)calloc(num_of_records,
                                           sizeof(signal_info));
  if (start == NULL) {
    /* Handle allocation error */
  } else if (tmp2 == NULL) {
    /* Handle error */
  } else if (temp_num > num_of_records || temp_num == 0) {
    /* Handle error */
  } else if (tmp2_size_bytes < SIG_DESC_SIZE) {
    /* Handle error */
  }
  signal_info *point = start + temp_num - 1; 
  memcpy(point->sig_desc, tmp2, SIG_DESC_SIZE);
  point->sig_desc[SIG_DESC_SIZE - 1] = '\0';
  /* ... */
  free(start);
}
```
## Noncompliant Code Example (`realloc()`)
This noncompliant code example calls `realloc()` to resize the memory referred to by `p`. However, if `realloc()` fails, it returns a null pointer and the connection between the original block of memory and `p` is lost, resulting in a memory leak.
``` c
#include <stdlib.h>
void *p;
void func(size_t new_size) {
  if (new_size == 0) {
    /* Handle error */
  }
  p = realloc(p, new_size);
  if (p == NULL) {
   /* Handle error */
  }
}
```
This code example complies with [MEM04-C](MEM04-C_%20Beware%20of%20zero-length%20allocations)[. Do not perform zero-length allocations](MEM04-C_%20Beware%20of%20zero-length%20allocations).
## Compliant Solution (`realloc()`)
In this compliant solution, the result of `realloc()` is assigned to the temporary pointer `q` and validated before it is assigned to the original pointer `p`:
``` c
#include <stdlib.h>
void *p;
void func(size_t new_size) {
  void *q;
  if (new_size == 0) {
    /* Handle error */
  }
  q = realloc(p, new_size);
  if (q == NULL) {
   /* Handle error */
  } else {
    p = q;
  }
}
```
## Noncompliant Code Example (`fseek()`)
In this noncompliant code example, the `fseek()` function is used to set the file position to a location `offset` in the file referred to by `file` prior to reading a sequence of bytes from the file. However, if an I/O error occurs during the seek operation, the subsequent read will fill the buffer with the wrong contents.
``` c
#include <stdio.h>
size_t read_at(FILE *file, long offset,
               void *buf, size_t nbytes) {
  fseek(file, offset, SEEK_SET);
  return fread(buf, 1, nbytes, file);
}
```
## Compliant Solution (`fseek()`)
According to the C Standard, the `fseek()` function returns a nonzero value to indicate that an error occurred. This compliant solution tests for this condition before reading from a file to eliminate the chance of operating on the wrong portion of the file if `fseek()` fails:
``` c
#include <stdio.h>
size_t read_at(FILE *file, long offset,
               void *buf, size_t nbytes) {
  if (fseek(file, offset, SEEK_SET) != 0) {
    /* Indicate error to caller */
    return 0;
  }
  return fread(buf, 1, nbytes, file);
}
```
## Noncompliant Code Example (`snprintf()`)
In this noncompliant code example, `snprintf()` is assumed to succeed. However, if the call fails (for example, because of insufficient memory, as described in GNU libc bug [441945](http://bugzilla.redhat.com/show_bug.cgi?id=441945)), the subsequent call to `log_message()` has [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) because the character buffer is uninitialized and need not be null-terminated.
``` c
#include <stdio.h>
extern void log_message(const char *);
void f(int i, int width, int prec) {
  char buf[40];
  snprintf(buf, sizeof(buf), "i = %*.*i", width, prec, i);
  log_message(buf);
  /* ... */
}
```
## Compliant Solution (`snprintf()`)
This compliant solution does not assume that `snprintf()` will succeed regardless of its arguments. It tests the return value of `snprintf()` before subsequently using the formatted buffer. This compliant solution also treats the case where the static buffer is not large enough for `snprintf()` to append the terminating null character as an error.
``` c
#include <stdio.h>
#include <string.h>
extern void log_message(const char *);
void f(int i, int width, int prec) {
  char buf[40];
  int n;
  n = snprintf(buf, sizeof(buf), "i = %*.*i", width, prec, i);
  if (n < 0 || n >= sizeof(buf)) {
    /* Handle snprintf() error */
    strcpy(buf, "unknown error");
  }
  log_message(buf);
}
```
## Compliant Solution (`snprintf(`null`)`)
If unknown, the length of the formatted string can be discovered by invoking `snprintf()` with a null buffer pointer to determine the size required for the output, then dynamically allocating a buffer of sufficient size, and finally calling `snprintf()` again to format the output into the dynamically allocated buffer. Even with this approach, the success of all calls still needs to be tested, and any errors must be appropriately handled. A possible optimization is to first attempt to format the string into a reasonably small buffer allocated on the stack and, only when the buffer turns out to be too small, dynamically allocate one of a sufficient size:
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
extern void log_message(const char *); 
void f(int i, int width, int prec) {
  char buffer[20];
  char *buf = buffer;
  int n  = sizeof(buffer);
  const char fmt[] = "i = %*.*i";
  n = snprintf(buf, n, fmt, width, prec, i);
  if (n < 0) {
    /* Handle snprintf() error */
    strcpy(buffer, "unknown error");
    goto write_log;
  }
  if (n < sizeof(buffer)) {
    goto write_log;
  }
  buf = (char *)malloc(n + 1);
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
  if (buf != buffer) {
    free(buf);
  }
}
```
This solution uses the `goto` statement, as suggested in [MEM12-C](MEM12-C_%20Consider%20using%20a%20goto%20chain%20when%20leaving%20a%20function%20on%20error%20when%20using%20and%20releasing%20resources)[. Consider using a goto chain when leaving a function on error when using and releasing resources](MEM12-C_%20Consider%20using%20a%20goto%20chain%20when%20leaving%20a%20function%20on%20error%20when%20using%20and%20releasing%20resources).
## Exceptions
**ERR33-C-EX1:** It is acceptable to ignore the return value of a function if:
-   that function cannot fail.
-   its return value is inconsequential; that is, it does not indicate an error.
-   it is one of a handful of functions whose return values are not traditionally checked.
These functions are listed in the following table:
**Functions for which Return Values Need Not Be Checked**

| Function | Successful Return | Error Return |
| ----|----|----|
| putchar() | Character written | EOF |
| putwchar() | Wide character written | WEOF |
| puts() | Nonnegative | EOF (negative) |
| putws() | Nonnegative | WEOF |
| printf(), vprintf() | Number of characters (nonnegative) | Negative |
| wprintf(), vwprintf() | Number of wide characters (nonnegative) | Negative |
| kill_dependency() | The input parameter; | NA |
| memcpy(), wmemcpy() | The destination input parameter | NA |
| memmove(), wmemmove() | The destination input parameter; | NA |
| strcpy(), wcscpy() | The destination input parameter; | NA |
| strncpy(), wcsncpy() | The destination input parameter; | NA; |
| strcat(), wcscat() | The destination input parameter; | NA; |
| strncat(), wcsncat() | The destination input parameter; | NA |
| memset(), wmemset() | The destination input parameter | NA; |

The return value of a call to `fprintf()` or one of its variants (`vfprintf()`, `wfprintf()`, `vwfprintf()`) or one of the file output functions `fputc()`, `fputwc()`, `fputs()`, `fputws()` may be ignored if the output is being directed to `stdout` or `stderr` . Otherwise, the return value must be checked.
If a function's return value is to be ignored, it is recommended that the function's return value should be explicitly cast to void to signify the programmer's intent:
``` c
int main() {
  (void) fprintf(stdout, "Hello, world\n"); // fprintf() return value safely ignored
}
```
## Risk Assessment
Failing to detect error conditions can lead to unpredictable results, including [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) and [denial-of-service attacks](BB.-Definitions_87152273.html#BB.Definitions-denial-of-service) or, in some situations, could even allow an attacker to run arbitrary code.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ERR33-C | High | Likely | Medium | P18 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | error-information-unusederror-information-unused-computed | Partially checked |
| Axivion Bauhaus Suite | 7.2.0 | CertC-ERR33 |  |
| CodeSonar | 8.3p0 | LANG.FUNCS.IRVLANG.ERRCODE.NOTEST
LANG.ERRCODE.NZ
 | Ignored return valueMissing Test of Error Code
Non-zero Error Code |
| Compass/ROSE |  |  | Can detect violations of this recommendation when checking for violations of EXP12-C. Do not ignore values returned by functions and EXP34-C. Do not dereference null pointers |
| Coverity | 2017.07 | MISRA C 2012 Rule 22.8MISRA C 2012 Rule 22.9MISRA C 2012 Rule 22.10 | Implemented |
| Cppcheck Premium | 24.11.0 | premium-cert-err33-c |  |
| Helix QAC | 2024.4 | C3200C++3802, C++3803, C++3804DF2820, DF2821, DF2822, DF2823, DF2824, DF2930, DF2931, DF2932, DF2933, DF2934 |  |
| Klocwork | 2024.4 | NPD.CHECK.MUSTNPD.FUNC.MUST
SV.RVT.RETVAL_NOTTESTED |  |
| LDRA tool suite | 9.7.1 | 80 D | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-ERR33-aCERT_C-ERR33-d
CERT_C-ERR33-e
 | The value returned by a standard library function that may return an error should be usedAlways check the returned value of non-void function
Provide error handling for file opening errors right next to the call to fopen |
| Parasoft Insure++ |  |  | Runtime analysis |
| PC-lint Plus | 1.4 | 534 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule ERR33-C | Checks for:Errno not checkedReturn value of a sensitive function not checkedUnprotected dynamic memory allocationRule partially covered. |
| RuleChecker | 24.04 | error-information-unused | Partially checked |
| TrustInSoft Analyzer | 1.38 | pointer arithmetic | Exhaustively verified. |

### Related Vulnerabilities
The [vulnerability](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) in Adobe Flash \[[VU#159523](AA.-Bibliography_87152170.html#AA.Bibliography-VU#159523)\] arises because Flash neglects to check the return value from `calloc()`. Even when `calloc()` returns a null pointer, Flash writes to an offset from the return value. Dereferencing a null pointer usually results in a program crash, but dereferencing an offset from a null pointer allows an [exploit](BB.-Definitions_87152273.html#BB.Definitions-exploit) to succeed without crashing the program.
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ERR33-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | ERR00-C. Adopt and implement a consistent and comprehensive error-handling policy | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | EXP34-C. Do not dereference null pointers | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | FIO13-C. Never push back anything other than one read character | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | MEM04-C. Do not perform zero-length allocations | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | MEM12-C. Consider using a goto chain when leaving a function on error when using and releasing resources | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | ERR10-CPP. Check for error conditions | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C | FIO04-CPP. Detect and handle input and output errors | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Failing to detect and handle standard library errors [liberr] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-252, Unchecked Return Value | 2017-07-06: CERT: Partial overlap |
| CWE 2.11 | CWE-253, Incorrect Check of Function Return Value | 2017-07-06: CERT: Partial overlap |
| CWE 2.11 | CWE-391, Unchecked Error Condition | 2017-07-06: CERT: Rule subset of CWE |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-252/CWE-253/CWE-391 and ERR33-C/POS34-C
Independent( ERR33-C, POS54-C, FLP32-C, ERR34-C) Intersection( CWE-252, CWE-253) = Ø CWE-391 = Union( CWE-252, CWE-253) CWE-391 = Union( ERR33-C, POS34-C, list) where list =
-   Ignoring return values of functions outside the C or POSIX standard libraries
## Bibliography

|  |  |
| ----|----|
| [DHS 2006] | Handle All Errors Safely |
| [Henricson 1997] | Recommendation 12.1, "Check for All Errors Reported from Functions" |
| [ISO/IEC 9899:2024] | Subclause 7.31.3.10, "The ungetc Function" |
| [VU#159523] |  |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152125) [](../c/Rule%2012_%20Error%20Handling%20_ERR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152395)
## Comments:

|  |
| ----|
| The calloc() example has many problems, not only the not handled NULL pointer; from the calloc().if temp_num is bigger than num_of_records, the function tries to write outside the allocated memoryif tmp2 is shorter than SIG_DESC_SIZE, the memcpy copies data beyond the tmp2 stringif tmp2 is longer than SIG_DESC_SIZE, the point->sig_desc will not be null terminated. (This seems to be fixed in the compliant solution)Furthermore, the allocated memory is not freed or pointer to it is not conveyed outside of the function.
                                        Posted by jussi.auvinen at Nov 17, 2015 04:22
                                     |
| Good catches! I've corrected the issues you've pointed out, thanks!
                                        Posted by aballman at Nov 17, 2015 10:09
                                     |
| Will it be helpful to group information from the table “Standard Library Functions” by the item “Successful Return”?(Can grouping of such data be nicer than the supported sorting?)
                                        Posted by markus.elfring at Apr 09, 2023 03:25
                                     |
| All of our tables, including the table in this rule, allow you to sort their elements by whichever column header you click on.
                                        Posted by svoboda at Apr 10, 2023 12:56
                                     |
| Are there any chances that tree (or outline) views will become supported for such widgets?
                                        Posted by markus.elfring at Apr 10, 2023 13:53
                                     |
| I have no idea. We are using Atlassian's Confluence software to run our wiki. You should ask them.
                                        Posted by svoboda at Apr 10, 2023 14:02
                                     |
| Have you got any better contacts to your wiki provider?
                                        Posted by markus.elfring at Apr 10, 2023 14:04
                                     |
| I hope that the section “Exceptions” can be reconsidered and accordingly improved.
                                        Posted by markus.elfring at May 01, 2023 13:02
                                     |
|  How would you call a property (or category) of functions which forward an input parameter as their return value?
                                        Posted by markus.elfring at May 03, 2023 04:51
                                     |
|  Under which circumstances would you care more for data output failures?
                                        Posted by markus.elfring at May 03, 2023 04:56
                                     |
| In OOP, we typically call methods that return their argument chaining methods, because you can chain them together via their return values. ; But I don't know of such functions in the standard C library.
                                        Posted by svoboda at May 04, 2023 08:35
                                     |
| It depends on what you mean by "data output failures", but the general answer is, if they introduce a significant new class of software vulnerabilities.
                                        Posted by svoboda at May 04, 2023 08:35
                                     |
| But I don't know of such functions in the standard C library. How does this feedback fit to documentation for functions like memcpy() and strcat()?
                                        Posted by markus.elfring at May 04, 2023 10:12
                                     |
| It depends on what you mean by "data output failures", … Will the development attention grow for more complete error detection and corresponding exception handling also according to function calls like the following?fputs()printf()putchar()
                                        Posted by markus.elfring at May 04, 2023 10:30
                                     |
| Would you like to help another bit with the avoidance of return value ignorance?How do you think about to move mentioned functions for file adjustments from the table “Functions for which Return Values Need Not Be Checked” into “Standard Library Functions” then?Will further explanations become more helpful instead of using the word “traditionally” for ERR33-C-EX1?
                                        Posted by markus.elfring at May 05, 2023 06:21
                                     |
| It means that memcpy() & similar functions could be used as a chaining function. ;I feel like we are lost in the weeds here.   Do you have a specific suggestion for improving this rule?
                                        Posted by svoboda at May 09, 2023 13:02
                                     |
| I think we've discussed these functions, and we are not going to mention that fputs() & co might return negative values besides EOF.
                                        Posted by svoboda at May 09, 2023 13:20
                                     |
| I would need a very strong argument to merge the table in ERR33-C-EX1 with the table in the introduction. I am currently against merging these tables. Both tables contain data straight from the standard, and which table a function goes into is pretty much our choice, based on the exception text. ;Merging these tables would require us to add an 'is this function in the exception' field, which is more complicated than their current state.
                                        Posted by svoboda at May 09, 2023 13:20
                                     |
| It means that memcpy() & similar functions could be used as a chaining function.It seems that expressed knowledge limitations influence the communication in some ways.Would you find a function property like “pass-through” also appropriate and helpful for further clarifications?Do you have a specific suggestion for improving this rule?Yes, of course.The corresponding change acceptance will take another while.
                                        Posted by markus.elfring at May 10, 2023 02:18
                                     |
| The development attention can eventually be influenced further by available information for the handling of success and error predicates.I see a potential for more collateral evolution here.Remaining return value ignorance can be reduced a bit more, can't it?
                                        Posted by markus.elfring at May 10, 2023 02:26
                                     |
| I am currently against merging these tables.It seems that this feedback indicates another communication difficulty. Which factors do hinder your organisation to integrate further change possibilities so far?…, and which table a function goes into is pretty much our choice, …I am trying to adjust the information presentation in some ways for a while.
Merging these tables would require us to add an 'is this function in the exception' field, which is more complicated than their current state.I proposed to move a few entries. Which function categories will be left over for the description of known exceptions?
                                        Posted by markus.elfring at May 10, 2023 02:51
                                     |
| An fputs() call is used within a source code example for a “compliant solution”. Which special circumstances did influence the situation to keep file output functions in the table “Functions for which Return Values Need Not Be Checked” till May 2023?
                                        Posted by markus.elfring at May 30, 2023 03:15
                                     |
| I believe there is an edge case for the CCE (calloc) which has not been addressed. Since temp_num derives from a "tainted source" (description in the non-compliant portion of the code example), it is possible the value is 0. I believe the result of;
signal_info *point = start + temp_num - 1;

violates [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts) in that case.
![](images/icons/contenttypes/comment_16.png) Posted by 0skellar at Jun 19, 2023 08:37
\| \|
Yow! Good catch...I've fixed both code examples that use temp_num.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 20, 2023 08:53
\| \|
I do also not like the wording which you introduced yesterday.
![](images/icons/emoticons/information.svg) I find the expressed return value ignorance too broad (for file output functions).
![](images/icons/emoticons/help_16.svg) Under which circumstances will you get into the mood to take other possible adjustments into account?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 02:23
\| \|
Markus, can you be more specific about what you think is "too broad" about the update? It is limited to printing stdout and stderr, which are fairly precise constraints. Printing to stdout is effectively the same behavior as printf, which is already in the table of the exception. And printing to stderr is probably done as a way to notify of a prior error. If printing an error to stderr fails, what would be a reliable failback suggestion?
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 08:26
\| \|
I'm sorry, I simply don't understand your question.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 08:29
\| \|
Markus,;
Note that the compliant solution you are referring to is on page [EXP12-C. Do not ignore values returned by functions](EXP12-C_%20Do%20not%20ignore%20values%20returned%20by%20functions), which is a Recommendation, not a Rule. Please see [Rules versus Recommendations](Rules%20versus%20Recommendations) for more information about the difference.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 08:49
\| \|
Markus, do you have precise suggestions? I find these to be ambiguous and open ended and I'm finding it difficult to understand exactly what your suggestions are.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 08:53
\| \|
> It is limited to printing stdout and stderr,

I find such a “restriction” generally questionable for the affected programming interface.
> which are fairly precise constraints.

Please reconsider this view also according to [the functionality “file redirection”](https://en.wikipedia.org/wiki/Redirect_%28computing%29).
> And printing to stderr is probably done as a way to notify of a prior error.

This can usually be often the case.
> If printing an error to stderr fails, what would be a reliable failback suggestion?

Solutions should be known for such a recurring question.
-   [The guidance “Adopt and implement a consistent and comprehensive error-handling policy” is provided](https://wiki.sei.cmu.edu/confluence/display/c/ERR00-C.+Adopt+and+implement+a+consistent+and+comprehensive+error-handling+policy).
-   A bit of information can be transferred by [an ordinary program exit status](https://en.wikipedia.org/wiki/Exit_status).
Further hints and recommendations were published already for more advanced error reporting approaches elsewhere.
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 11:50
\| \|
> …, do you have precise suggestions?

Yes, of course.
It seems to be hard to get the desired acceptance for some of the mentioned change possibilities.
> I find these to be ambiguous and open ended

I hoped that such a clarification approach can eventually trigger more constructive responses.
> and I'm finding it difficult to understand exactly what your suggestions are.

Would you like to take another look at items which we tried to discuss already?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 12:06
\| \|
Reminder: You provided the following feedback on 2019-03-06.
![](images/icons/emoticons/information.svg) “Though EXP12-C is a recommendation, and therefore it gets less priority for updates, we still don't want them to be inconsistent with the rules and exceptions of the rules. ;We're going to change the example so it is consistent.”
![](images/icons/emoticons/help_16.svg)
-   Do we stumble on inconsistencies between known information sources?
-   Is the guidance still improvable accordingly?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 13:01
\| \|
Markus,;
I fail to recognize the inconsistency you are referring to, simply stating that fputs() is used in a Compliant Solution (CS) on that page. Can you precisely define what the inconsistency is in a straightforward "X is not consistent with Y" way for us to consider in a clear and actionable way? 
In particular, if there is a CS that is not consistent with a Rule, we will consider that as a higher priority.  By their nature, recommendations are not always applicable and are likely to have natural conflicts that may result in inconstancies, so we generally deem them as lesser priority, or simply not resolvable.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 13:48
\| \|
> I fail to recognize the inconsistency you are referring to,

I wonder about such a feedback.
> simply stating that fputs() is used in a Compliant Solution (CS) on that page.

![](images/icons/emoticons/information.svg) The information “This compliant solution checks to make sure no output error occurred (see ERR33-C…).” is provided.  
Thus it seems that software developers get encouraged to take special care also for the return value of such a file output function.
![](images/icons/emoticons/help_16.svg) Does the current table “Functions for which Return Values Need Not Be Checked” contain contradictions (in comparison to other programming advices)?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 14:50
\| \|
Markus,
I'm still struggling to understand the precise inconsistency you are referring to, and I don't understand the intent or meaning about what you might be "wonder\[ing\] about such a feedback."
The [EXP12-C](https://wiki.sei.cmu.edu/confluence/display/c/EXP12-C.+Do+not+ignore+values+returned+by+functions) Recommendation does;**recommend** that developers take extra care. It is a Recommendation that is above and beyond the Rule. It is a priority that our CS's do NOT violate Rules. We do not guarantee that our CS's comply with all Recommendations. Because EXP12-C is a Recommendation, some of our CS's may not comply with it, as they may not comply with other Recommendations, depending on the context. Additionally, the Exceptions EXP12-C-EX1 and EXP12-C-EX2 refer to the Exception in this rule ERR33-C-EX1. We interpret those Exceptions to be consistent.
We are not aware of the tables or guidance in *this* Rule contradicting anything else in this or any other Rules. If you find such a contradiction and can provide precise pointers or information that we are able to act on, we will consider it.
That said, we are considering making a change to the examples in EXP12-C, but I don't think it is for the reason you were trying to point out.  EXP12-C says "Unlike this recommendation, \[EXP33-C\] is restricted to functions from the Standard C library." That implies that the significant difference between EXP12-C and EXP33-C is that EXP12-C is about return values for functions that are not from the Standard C library.  However, the only example in EXP12-C uses fputs(), which is part of the Standard C library.  So, the example using a function that is part of the Standard C library is inconsistent with the intent that EXP12-C is about functions not part of the Standard C library.  We are considering changing the example to use a function that is not part of the Standard C library.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 15:42
\| \|
> I find such a “restriction” generally questionable for the affected programming interface.

What is the question? I cannot tell if you think constraining the Exception to stdout and stderr is overly constraining, and the Exception should be broadened? Or if you think the Exception is too broad and overly constraining the Rule.
File redirection happens in the system outside of the program. Its behavior will be specified outside of the program. Often redirection fails will report errors directly to stderr, not as a return value back to the program that invoked stdout or stderr through the shell that redirected the stream to a file.; 
ERR00-C does not address how to report an error when error reporting itself occurs. That becomes a recursive paradox. We don't currently have much in the way of Recommendations regarding reporting program error status or return values on exit. ERR04-C discusses it a little.  So, that could be a possible future improvement we can consider.  But, based on our current understanding of your questions and concern, we would consider it a Recommendation improvement, not a Rule improvement.  Note that ERR00-C and ERR04-C are both Recommendations, not Rules.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 15:53
\| \|
Markus,
> Markus, do you have precise suggestions?

I meant, do you have precise technical suggestions? I do not interpret a "potential for collateral evolution" as a precise technical suggestion. I interpret it as a request for a different approach. Or a philosophical, theoretical, or strategic discussion.; Not a transactional, actionable, precise change request to the Rules.
Examples:
>   Will the development attention grow...
>
> -   I see a potential for more collateral evolution here.
> -   Remaining return value ignorance can be reduced a bit more, can't it?
>
> ...trigger more constructive responses

These all seem like general statements or questions, and not clear, precise, actionable issues to consider.  So, I'm not sure how to act on them or respond.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 21, 2023 16:09
\| \|
> …, and I don't understand the intent or meaning about what you might be "wonder\[ing\] about such a feedback."

![](images/icons/emoticons/information.svg) There are some communication factors involved.
Another example:I pointed the following information out on 2019-02-14.
    2. The function “puts” is still listed in the table “Functions for which
       Return Values Need Not Be Checked” while a “solution” seems to
       represent opposite information.
You gave the following information within a bigger feedback on 2019-03-06.
    You are correct, that's an inconsistency and an error. …
![](images/icons/emoticons/help_16.svg) How interesting is it then that you seem to present other views today?
> We interpret those Exceptions to be consistent.

Our development views are different somehow also for this technical detail.
> We are not aware of the tables or guidance in this Rule contradicting anything else in this or any other Rules.

This view might fit only to your own improvable taxonomy.
> If you find such a contradiction and can provide precise pointers or information that we are able to act on, we will consider it.

How does [information from the advice “CWE-252: Unchecked Return Value”](https://cwe.mitre.org/data/definitions/252.html) fit into the discussed descriptions?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 16:33
\| \|
> File redirection happens in the system outside of the program.

File output can occasionally fail here, can't it?
> Often redirection fails will report errors directly to stderr, not as a return value back to the program that invoked stdout or stderr through the shell that redirected the stream to a file.

![](images/icons/emoticons/help_16.svg) Would you like to reconsider such feedback if you would take test results better into account for [the usage of a file like “/dev/full”](https://en.wikipedia.org/wiki//dev/full)?
> Note that … are both Recommendations, not Rules.

![](images/icons/emoticons/help_16.svg) Can any “Recommendations” eventually become promoted to “Rules” (or related items)?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 21, 2023 17:01
\| \|
I have changed the code examples in EXP12-C to use the asprintf() function. This function is part of the GNU C library, but has never been standardized in either ISO C or POSIX. So those code examples do not violate this rule or [POS54-C. Detect and handle POSIX library errors](POS54-C_%20Detect%20and%20handle%20POSIX%20library%20errors).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 21, 2023 17:02
\| \|
> So, I'm not sure how to act on them or respond.

![](images/icons/emoticons/help_16.svg) How actionable did you;find suggestions like the following?
1.  Move a few entries (according to functions for file adjustments) between mentioned tables
2.  Improve grouping for some data
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 22, 2023 02:08
\| \|
Markus,
> How interesting is it then that you seem to present other views today?

This is an example of how more precision helps.; If you are considering that comment from 2019, you also have to consider the page as it existed at the time of the comment.  At that time, the example in EXP12-C was simply the puts() function. That was changed on 4/2/2019 by David. So, you are applying comments made from a version back then to the version as it is now, and the context has changed.  This information and the previous versions are available in the page history. I interpret and my intent of my messaging now is that was a different precise inconsistency than we are talking about now.  The difference in views is because it is a similar question but on a different piece of code and different context.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 22, 2023 08:58
\| \|
Markus,
> ![](images/icons/emoticons/help_16.svg);How actionable did you find suggestions like the following?

I don't find these particularly actionable. They are open ended, and I don't know what entries or grouping you might be suggesting.  What would help to be more actionable is something like:
1.  Move \[list of specific functions\] from first table to second table and move \[different list of specific functions\] from second table to first table.
2.  Create a new group called X and put \[list of specific functions\] in that group.  Create another new group called Y and put \[another list of specific functions\] in that group.  The purpose for group X is \[explanation\].  The purpose for group Y is \[explanation\].
As things stand right now, we think the lists are accurate and don't need any changes.  We need to understand the very precise changes you think that should be made and very precise improvement value that change will have for us to fully consider your change request.  Otherwise, we will not have enough information to properly consider your change request.
![](images/icons/contenttypes/comment_16.png) Posted by rschiela at Jun 22, 2023 09:05
\| \|
> Move \[list of specific functions\]

![](images/icons/emoticons/help_16.svg)
-   Do you still stumble on understanding difficulties for the wording “functions for file adjustments”?
-   Would you find key words like “file input/output” more appropriate?
> from first table

[Can my change request from 2023-05-05 be understandable](https://wiki.sei.cmu.edu/confluence/display/c/ERR33-C.+Detect+and+handle+standard+library+errors?focusedCommentId=409567270#comment-409567270) (in principle)?
> Create a new group called X …

![](images/icons/emoticons/help_16.svg)
-   [How many groups would you know already if the table “Standard Library Functions” would be sorted by the column “Successful (or Error) Return”?](https://wiki.sei.cmu.edu/confluence/display/c/ERR33-C.+Detect+and+handle+standard+library+errors?focusedCommentId=405504130#comment-405504130)
-   How do you think about possibilities to reduce duplicate data here?
![](images/icons/contenttypes/comment_16.png) Posted by markus.elfring at Jun 22, 2023 11:05
\|
