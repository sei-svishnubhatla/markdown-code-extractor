Copying data to a buffer that is not large enough to hold that data results in a buffer overflow. Buffer overflows occur frequently when manipulating strings \[[Seacord 2013b](AA.-Bibliography_87152170.html#AA.Bibliography-Seacord2013)\]. To prevent such errors, either limit copies through truncation or, preferably, ensure that the destination is of sufficient size to hold the character data to be copied and the null-termination character. (See [STR03-C. Do not inadvertently truncate a string](STR03-C_%20Do%20not%20inadvertently%20truncate%20a%20string).)
When strings live on the heap, this rule is a specific instance of [MEM35-C. Allocate sufficient memory for an object](MEM35-C_%20Allocate%20sufficient%20memory%20for%20an%20object). Because strings are represented as arrays of characters, this rule is related to both [ARR30-C. Do not form or use out-of-bounds pointers or array subscripts](ARR30-C_%20Do%20not%20form%20or%20use%20out-of-bounds%20pointers%20or%20array%20subscripts) and [ARR38-C. Guarantee that library functions do not form invalid pointers](ARR38-C_%20Guarantee%20that%20library%20functions%20do%20not%20form%20invalid%20pointers).
## Noncompliant Code Example (Off-by-One Error)
This noncompliant code example demonstrates an *off-by-one* error \[[Dowd 2006](AA.-Bibliography_87152170.html#AA.Bibliography-Dowd06)\]. The loop copies data from `src` to `dest`. However, because the loop does not account for the null-termination character, it may be incorrectly written 1 byte past the end of `dest`.
``` c
#include <stddef.h>
void copy(size_t n, char src[n], char dest[n]) {
   size_t i;
   for (i = 0; src[i] && (i < n); ++i) {
     dest[i] = src[i];
   }
   dest[i] = '\0';
}
```
## Compliant Solution (Off-by-One Error)
In this compliant solution, the loop termination condition is modified to account for the null-termination character that is appended to `dest`:
``` c
#include <stddef.h>
void copy(size_t n, char src[n], char dest[n]) {
   size_t i;
   for (i = 0; src[i] && (i < n - 1); ++i) {
     dest[i] = src[i];
   }
   dest[i] = '\0';
}
```
## Noncompliant Code Example (`gets()`)
The `gets()` function, which was deprecated in the C99 Technical Corrigendum 3 and removed from C11, is inherently unsafe and should never be used because it provides no way to control how much data is read into a buffer from `stdin`. This noncompliant code example assumes that `gets()` will not read more than `BUFFER_SIZE - 1` characters from `stdin`. This is an invalid assumption, and the resulting operation can result in a buffer overflow.
The `gets()` function reads characters from the `stdin` into a destination array until end-of-file is encountered or a newline character is read. Any newline character is discarded, and a null character is written immediately after the last character read into the array.
``` c
#include <stdio.h>
#define BUFFER_SIZE 1024
void func(void) {
  char buf[BUFFER_SIZE];
  if (gets(buf) == NULL) {
    /* Handle error */
  }
}
```
See also [MSC24-C. Do not use deprecated or obsolescent functions](MSC24-C_%20Do%20not%20use%20deprecated%20or%20obsolescent%20functions).
## Compliant Solution (`fgets()`)
The `fgets()` function reads, at most, one less than the specified number of characters from a stream into an array. This solution is compliant because the number of characters copied from `stdin` to `buf` cannot exceed the allocated memory:
``` c
#include <stdio.h>
#include <string.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  int ch;
  if (fgets(buf, sizeof(buf), stdin)) {
    /* fgets() succeeded; scan for newline character */
    char *p = strchr(buf, '\n');
    if (p) {
      *p = '\0';
    } else {
      /* Newline not found; flush stdin to end of line */
      while ((ch = getchar()) != '\n' && ch != EOF)
        ;
      if (ch == EOF && !feof(stdin) && !ferror(stdin)) {
          /* Character resembles EOF; handle error */ 
      }
    }
  } else {
    /* fgets() failed; handle error */
  }
}
```
The `fgets()` function is not a strict replacement for the `gets()` function because `fgets()` retains the newline character (if read) and may also return a partial line. It is possible to use `fgets()` to safely process input lines too long to store in the destination array, but this is not recommended for performance reasons. Consider using one of the following compliant solutions when replacing `gets()`.
## Compliant Solution (`gets_s()`)
The `gets_s()` function reads, at most, one less than the number of characters specified from the stream pointed to by `stdin` into an array.
The C Standard, Annex K 3.5.4.1 paragraph 4 \[[ISO/IEC 9899:2024](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2024)\], states
> No additional characters are read after a new-line character (which is discarded) or after end-of-file. The discarded new-line character does not count towards number of characters read. A null character is written immediately after the last character read into the array.

If end-of-file is encountered and no characters have been read into the destination array, or if a read error occurs during the operation, then the first character in the destination array is set to the null character and the other elements of the array take unspecified values:
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  if (gets_s(buf, sizeof(buf)) == NULL) {
    /* Handle error */
  }
}
```
## Compliant Solution (`getline()`, POSIX)
The `getline()` function is similar to the `fgets()` function but can dynamically allocate memory for the input buffer. If passed a null pointer, `getline()` dynamically allocates a buffer of sufficient size to hold the input. If passed a pointer to dynamically allocated storage that is too small to hold the contents of the string, the `getline()` function resizes the buffer, using `realloc()`, rather than truncating the input. If successful, the `getline()` function returns the number of characters read, which can be used to determine if the input has any null characters before the newline. The `getline()` function works only with dynamically allocated buffers. Allocated memory must be explicitly deallocated by the caller to avoid memory leaks. (See [MEM31-C. Free dynamically allocated memory when no longer needed](MEM31-C_%20Free%20dynamically%20allocated%20memory%20when%20no%20longer%20needed).)
``` c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void func(void) {
  int ch;
  size_t buffer_size = 32;
  char *buffer = malloc(buffer_size);
  if (!buffer) {
    /* Handle error */
    return;
  }
  if ((ssize_t size = getline(&buffer, &buffer_size, stdin))
        == -1) {
    /* Handle error */
  } else {
    char *p = strchr(buffer, '\n');
    if (p) {
      *p = '\0';
    } else {
      /* Newline not found; flush stdin to end of line */
      while ((ch = getchar()) != '\n' && ch != EOF)
        ;
      if (ch == EOF && !feof(stdin) && !ferror(stdin)) {
         /* Character resembles EOF; handle error */
      }
    }
  }
  free (buffer);
}
```
Note that the `getline()` function uses an [in-band error indicator](BB.-Definitions_87152273.html#BB.Definitions-in-banderrorindicator), in violation of [ERR02-C. Avoid in-band error indicators](ERR02-C_%20Avoid%20in-band%20error%20indicators).
## Noncompliant Code Example (`getchar()`)
Reading one character at a time provides more flexibility in controlling behavior, though with additional performance overhead. This noncompliant code example uses the `getchar()` function to read one character at a time from `stdin` instead of reading the entire line at once. The `stdin` stream is read until end-of-file is encountered or a newline character is read. Any newline character is discarded, and a null character is written immediately after the last character read into the array. Similar to the noncompliant code example that invokes `gets()`, there are no guarantees that this code will not result in a buffer overflow.
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  char *p;
  int ch;
  p = buf;
  while ((ch = getchar()) != '\n' && ch != EOF) {
    *p++ = (char)ch;
  }
  *p++ = 0;
  if (ch == EOF) {
      /* Handle EOF or error */
  }
}
```
After the loop ends, if `ch == EOF`, the loop has read through to the end of the stream without encountering a newline character, or a read error occurred before the loop encountered a newline character. To conform to [FIO34-C. Distinguish between characters read from a file and EOF or WEOF](FIO34-C_%20Distinguish%20between%20characters%20read%20from%20a%20file%20and%20EOF%20or%20WEOF), the error-handling code must verify that an end-of-file or error has occurred by calling `feof()` or `ferror()`.
## Compliant Solution (`getchar()`)
In this compliant solution, characters are no longer copied to `buf` once `index == BUFFERSIZE - 1`, leaving room to null-terminate the string. The loop continues to read characters until the end of the line, the end of the file, or an error is encountered. When `truncated == true`, the input string has been truncated.
``` c
#include <stdio.h>
enum { BUFFERSIZE = 32 };
void func(void) {
  char buf[BUFFERSIZE];
  int ch;
  size_t index = 0;
  bool truncated = false;
  while ((ch = getchar()) != '\n' && ch != EOF) {
    if (index < sizeof(buf) - 1) {
      buf[index++] = (char)ch;
    } else {
      truncated = true;
    }
  }
  buf[index] = '\0';  /* Terminate string */
  if (ch == EOF) {
    /* Handle EOF or error */
  }
  if (truncated) {
    /* Handle truncation */
  }
}
```
## Noncompliant Code Example (`fscanf()`)
In this noncompliant example, the call to `fscanf()` can result in a write outside the character array `buf`:
``` c
#include <stdio.h>
enum { BUF_LENGTH = 1024 };
void get_data(void) {
  char buf[BUF_LENGTH];
  if (1 != fscanf(stdin, "%s", buf)) {
    /* Handle error */
  }
  /* Rest of function */
}
```
## Compliant Solution (`fscanf()`)
In this compliant solution, the call to `fscanf()` is constrained not to overflow `buf`:
``` c
#include <stdio.h>
enum { BUF_LENGTH = 1024 };
void get_data(void) {
  char buf[BUF_LENGTH];
  if (1 != fscanf(stdin, "%1023s", buf)) {
    /* Handle error */
  }
  /* Rest of function */
}
```
## Noncompliant Code Example (`argv`)
In a [hosted environment](BB.-Definitions_87152273.html#BB.Definitions-hostedenvironment), arguments read from the command line are stored in process memory. The function `main()`, called at program startup, is typically declared as follows when the program accepts command-line arguments:
``` c
int main(int argc, char *argv[]) { /* ... */ }
```
Command-line arguments are passed to `main()` as pointers to strings in the array members `argv[0]` through `argv[argc - 1]`. If the value of `argc` is greater than 0, the string pointed to by `argv[0]` is, by convention, the program name. If the value of `argc` is greater than 1, the strings referenced by `argv[1]` through `argv[argc - 1]` are the program arguments.
[Vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) can occur when inadequate space is allocated to copy a command-line argument or other program input. In this noncompliant code example, an attacker can manipulate the contents of `argv[0]` to cause a buffer overflow:
``` c
#include <string.h>
int main(int argc, char *argv[]) {
  /* Ensure argv[0] is not null */
  const char *const name = (argc && argv[0]) ? argv[0] : "";
  char prog_name[128];
  strcpy(prog_name, name);
  return 0;
}
```
## Compliant Solution (`argv`)
The `strlen()` function can be used to determine the length of the strings referenced by `argv[0]` through `argv[argc - 1]` so that adequate memory can be dynamically allocated.
``` c
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]) {
  /* Ensure argv[0] is not null */
  const char *const name = (argc && argv[0]) ? argv[0] : "";
  char *prog_name = (char *)malloc(strlen(name) + 1);
  if (prog_name != NULL) {
    strcpy(prog_name, name);
  } else {
    /* Handle error */
  }
  free(prog_name);
  return 0;
}
```
Remember to add a byte to the destination string size to accommodate the null-termination character.
## Compliant Solution (`argv`)
The `strcpy_s()` function provides additional safeguards, including accepting the size of the destination buffer as an additional argument. (See [STR07-C. Use the bounds-checking interfaces for string manipulation](STR07-C_%20Use%20the%20bounds-checking%20interfaces%20for%20string%20manipulation).)
``` c
#define __STDC_WANT_LIB_EXT1__ 1
#include <stdlib.h>
#include <string.h>
int main(int argc, char *argv[]) {
  /* Ensure argv[0] is not null */
  const char *const name = (argc && argv[0]) ? argv[0] : "";
  char *prog_name;
  size_t prog_size;
  prog_size = strlen(name) + 1;
  prog_name = (char *)malloc(prog_size);
  if (prog_name != NULL) {
    if (strcpy_s(prog_name, prog_size, name)) {
      /* Handle  error */
    }
  } else {
    /* Handle error */
  }
  /* ... */
  free(prog_name);
  return 0;
}
```
The `strcpy_s()` function can be used to copy data to or from dynamically allocated memory or a statically allocated array. If insufficient space is available, `strcpy_s()` returns an error.
## Compliant Solution (`argv`)
If an argument will not be modified or concatenated, there is no reason to make a copy of the string. Not copying a string is the best way to prevent a buffer overflow and is also the most efficient solution. Care must be taken to avoid assuming that `argv[0]` is non-null.
``` c
int main(int argc, char *argv[]) {
  /* Ensure argv[0] is not null */
  const char * const prog_name = (argc && argv[0]) ? argv[0] : "";
  /* ... */
  return 0;
}
```
## Noncompliant Code Example (`getenv()`)
According to the C Standard, 7.22.4.6 \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-2011)\]
> The `getenv` function searches an environment list, provided by the host environment, for a string that matches the string pointed to by `name`. The set of environment names and the method for altering the environment list are implementation defined.

Environment variables can be arbitrarily large, and copying them into fixed-length arrays without first determining the size and allocating adequate storage can result in a buffer overflow.
``` c
#include <stdlib.h>
#include <string.h>
void func(void) {
  char buff[256];
  char *editor = getenv("EDITOR");
  if (editor == NULL) {
    /* EDITOR environment variable not set */
  } else {
    strcpy(buff, editor);
  }
}
```
## Compliant Solution (`getenv()`)
Environmental variables are loaded into process memory when the program is loaded. As a result, the length of these strings can be determined by calling the `strlen()` function, and the resulting length can be used to allocate adequate dynamic memory:
``` c
#include <stdlib.h>
#include <string.h>
void func(void) {
  char *buff;
  char *editor = getenv("EDITOR");
  if (editor == NULL) {
    /* EDITOR environment variable not set */
  } else {
    size_t len = strlen(editor) + 1;
    buff = (char *)malloc(len);
    if (buff == NULL) {
      /* Handle error */
    }  
    memcpy(buff, editor, len);
    free(buff);
  }
}
```
## Noncompliant Code Example (`sprintf()`)
In this noncompliant code example, `name` refers to an external string; it could have originated from user input, the file system, or the network. The program constructs a file name from the string in preparation for opening the file.
``` c
#include <stdio.h>
void func(const char *name) {
  char filename[128];
  sprintf(filename, "%s.txt", name);
}
```
Because the `sprintf()` function makes no guarantees regarding the length of the generated string, a sufficiently long string in `name` could generate a buffer overflow.
## Compliant Solution (`sprintf()`)
The buffer overflow in the preceding noncompliant example can be prevented by adding a precision to the `%s` conversion specification. If the precision is specified, no more than that many bytes are written. The precision `123` in this compliant solution ensures that `filename` can contain the first 123 characters of `name`, the `.txt` extension, and the null terminator.
``` c
#include <stdio.h>
void func(const char *name) {
  char filename[128];
  sprintf(filename, "%.123s.txt", name);
}
```
You can also use `*` to indicate that the precision should be provided as a variadic argument:
``` c
#include <stdio.h>
void func(const char *name) {
  char filename[128];
  sprintf(filename, "%.*s.txt", sizeof(filename) - 5, name);
}
```
## Compliant Solution (`snprintf()`)
A more general solution is to use the `snprintf()` function, which also truncates `name` if it will not fit in the `filename`.
``` c
#include <stdio.h>
void func(const char *name) {
  char filename[128];
  int result = snprintf(filename, sizeof(filename), "%s.txt", name);
  if (result != strlen(filename) {
    /* truncation occurred */
  }
}
```
## Risk Assessment
Copying string data to a buffer that is too small to hold that data results in a buffer overflow. Attackers can exploit this condition to execute arbitrary code with the permissions of the vulnerable process.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR31-C | High | Likely | Medium | P18 | L1 |

### Automated Detection
Array access out of bounds, Buffer overflow from incorrect string format specifier, Destination buffer overflow in string manipulation, Invalid use of standard library string routine, Missing null in string array, Pointer access out of bounds, Tainted NULL or non-null-terminated string, Use of dangerous standard function 

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | SupportedAstrée reports all buffer overflows resulting from copying data to a buffer that is not large enough to hold that data. |
| Axivion Bauhaus Suite | 7.2.0 | CertC-STR31 | Detects calls to unsafe string function that may cause buffer overflowDetects potential buffer overruns, including those caused by unsafe usage of fscanf() |
| CodeSonar | 8.3p0 | LANG.MEM.BOLANG.MEM.TO
MISC.MEM.NTERM
BADFUNC.BO.* | Buffer overrunType overrun
No space for null terminator
A collection of warning classes that report uses of library functions prone to internal buffer overflows |
| Compass/ROSE |  |  | Can detect violations of the rule. However, it is unable to handle cases involving strcpy_s() or manual string copies such as the one in the first example |
| Coverity | 2017.07 | STRING_OVERFLOWBUFFER_SIZEOVERRUNSTRING_SIZE | Fully implemented |
| Fortify SCA | 5.0 |  |  |
| Helix QAC | 2024.4 | C2840, ;C5009, C5038C++0145, C++5009, C++5038DF2840, DF2841, DF2842, DF2843, DF2845, DF2846, DF2847, DF2848, DF2930, DF2931, DF2932, DF2933, DF2935, DF2936, DF2937, DF2938 |  |
| Klocwork | 2024.4 | SV.FMT_STR.BAD_SCAN_FORMATSV.UNBOUND_STRING_INPUT.FUNC |  |
| LDRA tool suite | 9.7.1 | 489 S, 109 D, 66 X, 70 X, 71 X | Partially implemented |
| Parasoft C/C++test | 2024.2 | CERT_C-STR31-aCERT_C-STR31-b
CERT_C-STR31-c
CERT_C-STR31-d
CERT_C-STR31-e | Avoid accessing arrays out of boundsAvoid overflow when writing to a buffer
Prevent buffer overflows from tainted data
Avoid buffer write overflow from tainted data
Avoid using unsafe string functions which may cause buffer overflows |
| PC-lint Plus | 1.4 | 421, 498 | Partially supported |
| Polyspace Bug Finder | R2024a | CERT C: Rule STR31-C | Checks for:Use of dangerous standard functionMissing null in string arrayBuffer overflow from incorrect string format specifierDestination buffer overflow in string manipulationInsufficient destination buffer sizeRule partially covered. |
| PVS-Studio | 7.35 | V518, V645, V727, V755 |  |
| Splint | 3.1.1 |  |  |
| TrustInSoft Analyzer | 1.38 | mem_access | Exhaustively verified (see one compliant and one non-compliant example). |

### Related Vulnerabilities
[CVE-2009-1252](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-1252) results from a violation of this rule. The Network Time Protocol daemon (NTPd), before versions 4.2.4p7 and 4.2.5p74, contained calls to `sprintf` that allow an attacker to execute arbitrary code by overflowing a character array \[[xorl 2009](http://xorl.wordpress.com/2009/06/10/freebsd-sa-0911-ntpd-remote-stack-based-buffer-overflows/)\].
[CVE-2009-0587](http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2009-0587) results from a violation of this rule. Before version 2.24.5, Evolution Data Server performed unchecked arithmetic operations on the length of a user-input string and used the value to allocate space for a new buffer. An attacker could thereby execute arbitrary code by inputting a long string, resulting in incorrect allocation and buffer overflow \[[xorl 2009](http://xorl.wordpress.com/2009/06/10/cve-2009-0587-evolution-data-server-base64-integer-overflows/)\].
[CVE-2021-3156](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-3156) results from a violation of this rule in versions of Sudo before 1.9.5p2. Due to inconsistencies on whether backslashes are escaped, vulnerable versions of Sudo enabled a user to create a heap-based buffer overflow and exploit it to execute arbitrary code. [\[BC\]](https://www.bleepingcomputer.com/news/security/new-linux-sudo-flaw-lets-local-users-gain-root-privileges/).
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ARR32-C).
## Related Guidelines
[Key here](https://wiki.sei.cmu.edu/confluence/display/c/How+this+Coding+Standard+is+Organized#HowthisCodingStandardisOrganized-RelatedGuidelines) (explains table format and definitions)

| Taxonomy | Taxonomy item | Relationship |
| ----|----|----|
| CERT C Secure Coding Standard | STR03-C. Do not inadvertently truncate a string | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CERT C Secure Coding Standard | STR07-C. Use the bounds-checking interfaces for remediation of existing string manipulation codeMSC24-C. Do not use deprecated or obsolescent functionsMEM00-C. Allocate and free memory in the same module, at the same level of abstractionFIO34-C. Distinguish between characters read from a file and EOF or WEOF | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | String Termination [CJM] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Buffer Boundary Violation (Buffer Overflow) [HCB] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TR 24772:2013 | Unchecked Array Copying [XYW] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Using a tainted value to write to an object using a formatted input or output function [taintformatio] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| ISO/IEC TS 17961:2013 | Tainted strings are passed to a string copying function [taintstrcpy] | Prior to 2018-01-12: CERT: Unspecified Relationship |
| CWE 2.11 | CWE-119, Improper Restriction of Operations within the Bounds of a Memory Buffer | 2017-05-18: CERT: Rule subset of CWE |
| CWE 2.11 | CWE-120, Buffer Copy without Checking Size of Input ("Classic Buffer Overflow") | 2017-05-15: CERT: Exact |
| CWE 2.11 | CWE-123, Write-what-where Condition | 2017-06-12: CERT: Partial overlap |
| CWE 2.11 | CWE-125, Out-of-bounds Read | 2017-05-18: CERT: Partial overlap |
| CWE 2.11 | CWE-676, Off-by-one Error | 2017-05-18: CERT: Partial overlap |

## CERT-CWE Mapping Notes
[Key here](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152408#HowthisCodingStandardisOrganized-CERT-CWEMappingNotes) for mapping notes
### CWE-122 and STR31-C
STR31-C = Union( CWE-122, list) where list =
-   Buffer overflows on strings in the stack or data segment
### CWE-125 and STR31-C
Independent( ARR30-C, ARR38-C, EXP39-C, INT30-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
Intersection( STR31-C, CWE-125) =
-   Directly reading beyond the end of a string
STR31-C – CWE-125 =
-   Directly writing beyond the end of a string
CWE-125 – STR31-C =
-   Reading beyond a non-string array
<!-- -->
-   Reading beyond a string using library functions
### CWE-676 and STR31-C
-   Independent( ENV33-C, CON33-C, STR31-C, EXP33-C, MSC30-C, ERR34-C)
<!-- -->
-   STR31-C implies that several C string copy functions, like strcpy() are dangerous.
Intersection( CWE-676, STR31-C) =
-   Buffer Overflow resulting from invocation of the following dangerous functions:
<!-- -->
-   gets(), fscanf(), strcpy(), sprintf()
STR31-C – CWE-676 =
-   Buffer overflow that does not involve the dangerous functions listed above.
CWE-676 - STR31-C =
-   Invocation of other dangerous functions
### CWE-121 and STR31-C
STR31-C = Union( CWE-121, list) where list =
-   Buffer overflows on strings in the heap or data segment
### CWE-123 and STR31-C
Independent(ARR30-C, ARR38-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
Intersection( CWE-123, STR31-C) =
-   Buffer overflow that overwrites a (unrelated) pointer with untrusted data
STR31-C – CWE-123 =
-   Buffer overflow that does not overwrite a (unrelated) pointer
CWE-123 – STR31-C =
-   Arbitrary writes that do not involve buffer overflows
### CWE-119 and STR31-C
Independent( ARR30-C, ARR38-C, ARR32-C, INT30-C, INT31-C, EXP39-C, EXP33-C, FIO37-C)
STR31-C = Subset( Union( ARR30-C, ARR38-C))
STR32-C = Subset( ARR38-C)
CWE-119 = Union( STR31-C, list) where list =
-   Out-of-bounds reads or writes that are not created by string copy operations
### CWE-193 and STR31-C
Intersection( CWE-193, STR31-C) = Ø
CWE-193 involves an integer computation error (typically off-by-one), which is often a precursor to (slight) buffer overflow. However the two errors occur in different operations and are thus unrelated.
## Bibliography

|  |  |
| ----|----|
| [Dowd 2006] | Chapter 7, "Program Building Blocks" ("Loop Constructs," pp. 327–336) |
| [Drepper 2006] | Section 2.1.1, "Respecting Memory Bounds" |
| [ISO/IEC 9899:2024] | K.3.5.4.1, "The gets_s Function" |
| [Lai 2006] |  |
| [NIST 2006] | SAMATE Reference Dataset Test Case ID 000-000-088 |
| [Seacord 2013b] | Chapter 2, "Strings" |
| [xorl 2009] | FreeBSD-SA-09:11: NTPd Remote Stack Based Buffer Overflows |
| [BC] | New Linux SUDO flaw lets local users gain root privileges |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152214) [](../c/Rule%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152047)
## Comments:

|  |
| ----|
| This page made me think of a point that I've dwelled on many times before. Consider the compliant solution you have here:
if (editor) {
  buff = (char *)malloc(strlen(editor)+1);
  strcpy(buff, editor);
}

In the specific scenario listed, it's fine.. but this code construct can lead to vulnerabilities when some bug exists that causes the string you're copying not to be NUL-terminated correctly. For example, imagine a scenario where due to some previous bug, the 'buf' variable isnt correctly NUL-terminated in the following code (or a NUL byte has been skipped and 'buf' now points to memory out of bounds):
``` java
char *ptr;
ptr = (char *)malloc(strlen(buf));
if(ptr == NULL)
&nbsp;&nbsp;&nbsp; return NULL;&nbsp;
strcpy(ptr, buf);&nbsp;
```
The problem here is that strlen(buf) can actually change in between the time the string length is taken and when the strcpy() function is performed. For example, if 'buf' was a pointer to the heap, the malloc() call could rearrange the heap so that strlen(buf) changes, and the subsequent strcpy() results in memory corruption. It seems to me like a more defensive and save construct is like this:
``` java
size_t length;
char *ptr;
length = strlen(buf) + 1;
ptr = (char *)malloc(length);
if(length == NULL)
&nbsp;&nbsp;&nbsp; return NULL;
memcpy(ptr, buf, length);
```
This second solution will not result in an overflow, even if buf somehow points out of bounds. It would be even better if ptr was explicitly NUL-terminated as well probably.;
I know it seems like a small point, but I've run into a couple of vulnerabilities of this nature recently, and the use of a fixed length memcpy() or a fixed-length string copy routine vs strcpy() has meant the difference between just a bug vs an exploitable bug. 
![](images/icons/contenttypes/comment_16.png) Posted by mdowd at Jan 06, 2007 03:31
\| \|
I think this rule as it is should be moved to, or have a complimentary rule in, the array section with non-string related examples. For example, the memcpy() example in this rule doesn't have anything to do with NTBS.
Compared with the other rules in this section, this rule seems have more to do with array mismanagement than the the properties of an NTBS.
![](images/icons/contenttypes/comment_16.png) Posted by jsg at Feb 27, 2007 16:09
\| \|
The memcpy() example is valid, but is there a good reason to use memcpy() rather than strncpy()? AFAICT the only difference is strncpy() zeroes out destination memory after the null terminator.  
(Normmally the null terminator will be the last item in the string, but in a TOCTOU case where  
the src string memory is modified, all bets are off, right?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 28, 2008 09:57
\| \|
A better solution is: const char \*progname=argv\[0\]; // we're not going to modify either one!  
I have a function in my support library that I use to capture a pointer to the "short" program name (after the path prefix, if any); I extended it to also create argv from interactive input when running in a standalone environment.
The TOCTU example is bogus, since for multithreaded programming one must in general ensure that access to shared objects are protected by locking critical regions.  And if the src pointer is out of bounds, it is a huge bug to start with, having nothing to do with the current topic.
The compliant solution for getenv forgot to handle the case where EDITOR is not set.  Proceeding will cause use of an uninitialized "buff".
![](images/icons/contenttypes/comment_16.png) Posted by dagwyn at Apr 16, 2008 21:38
\| \|
Added a check for no EDITOR env var to the getenv() examples.
The TOCTOU example is only partially bogus ![](images/icons/emoticons/smile.svg) You're correct that a vul involving strcpy() in a multithreaded env has bigger problems than strcpy(). The non-compliant example here cause very subtle and difficult bugs in a problematic multi-threaded environment, which are made easier to detect with the compliant solutions.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 05, 2008 10:43
\| \|
The TOCTOU example had been bothering me for a while, and I removed it before I even read your comment. Thanks for the moral support, however.
![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at May 30, 2008 21:11
\| \|
I was going to argue for the memcpy TOCTOU case, but I reread Mark Dowd's comment, which already does an excellent job of arguing the case.
So I'll simply state that his NCCE & CCE should go **somewhere**. Perhaps this rule, perhaps another rule, or a new rule of its own, but it should not be forgotten.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jun 02, 2008 14:52
\| \|
is it ok for the rose implementation of this rule to give false positives?
``` java
char buff[] = "sufficient storage";
strcpy(buff,"abc");
```
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jun 11, 2008 12:56
\| \|
In general, yes, but this false positive is easy to spot, as you are copying from a fixed array to another fixed array...it is easy to compare their indices.
Doesn't that example code also violate STR30-C since the destination array is a string literal?
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jul 08, 2008 17:11
\| \|
no, it is an initialized array on the stack
``` java
char * buff = "sufficient storage";
```
is a string literal in `DATA`
![](images/icons/contenttypes/comment_16.png) Posted by avolkovi at Jul 09, 2008 09:50
\| \|
In paragraph "Noncompliant Code Example (`argv`) (`strcpy()`)" there is this sentence:
If the value of `argc` is greater than zero, the string pointed to by `argv[0]` is, by convention, the program name.
All the compliant examples suggest that there is no dependency between the value of argc and the validity of argv\[0\]. Is this correct, or should error handling occur on argc \<= 0?
![](images/icons/contenttypes/comment_16.png) Posted by erazor_de at Apr 12, 2010 02:51
\| \|
Good point! Programs should not assume that `argc` is positive or that `argv[0]` is non-null. A program with a null name (i.e., an `argc` of zero) can be executed by invoking
``` java
execv("/path/to/program", (char**)0);
```
As a data point, virtually every Linux utility in `/usr/bin` seems to assume that `argv[0]` is non-null and exits with `SIGSEGV` when invoked via the call above.
![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Apr 12, 2010 23:34
\| \|
Removed the following:
> The parameters `argc` and `argv` and the strings pointed to by the `argv` array are not modifiable by the program and retain their last-stored values between program startup and program termination. This requires that a copy of these parameters be made before the strings can be modified.

The standard guarantees the opposite:
> The parameters `argc` and `argv` and the strings pointed to by the `argv` array shall be modifiable by the program, and retain their last-stored values between program  
> startup and program termination.

![](images/icons/contenttypes/comment_16.png) Posted by rcs_mgr at Aug 10, 2011 08:11
\| \|
The "Compliant Solution (snprintf( ))" example seems to directly violate [STR03-C. Do not inadvertently truncate a string](https://www.securecoding.cert.org/confluence/display/seccode/STR03-C.+Do+not+inadvertently+truncate+a+string). If it's considered intentional truncation, a caution might be appropriate.; (Note that the ".txt" can be truncated away.)
![](images/icons/contenttypes/comment_16.png) Posted by jordanbrown at Mar 25, 2014 14:28
\| \|
I can weasel and suggest that when using `snprintf()`, we are truncating the input, but not \*inadvertently\* :) ;Keep in mind that STR03-C is a recommendation, not a rule. It is possible to violate CERT recommendations and still have secure code...that is one of the differences between recommendations and rules.  Truncation is acceptable if it is 'intended' (eg you have consciously decided that truncation is acceptable.)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Mar 27, 2014 12:26
\| \|
The problem with guidelines like [STR03-C. Do not inadvertently truncate a string](https://www.securecoding.cert.org/confluence/display/seccode/STR03-C.+Do+not+inadvertently+truncate+a+string);is that you can't enforce them without knowing the programmer's intent.  This example is too unrealistic to even guess at the intent. In fact, these functions do nothing and would be optimized out into no-ops.
Other examples in this rule also result in truncation:
`  ``char` `buf[BUF_LENGTH];`
`  ``fscanf``(stdin, ``"%1024s"``, buf);`
Some of the compliant solutions use dynamic memory allocation, but I think it is a good idea to show some examples with statically allocated buffers.  In these cases, there is nothing much that can be done except to truncate or return an error.  One of these examples could provide a more obvious case for truncation, perhaps writing out the title of an email message as a preview of the message.  These are normally truncated to fit the space available, with maybe the last few characters being overwritten by "..." to show the title has been truncated.
In other cases like the filename example you might want an error message instead "filename too long".
![](images/icons/contenttypes/comment_16.png) Posted by rcs at Mar 27, 2014 13:52
\| \|
I did say "if".; It's a little hard to come up with vulnerabilities associated with STR03-C (since simply truncating the input is often equivalent to the villain supplying the truncated input in the first place), but having a program-supplied piece of text like the ".txt" get truncated away seems like one of the ways it can happen.
The point is that snprintf isn't a panacea; you also must take STR03-C into account and determine whether its truncation will be acceptable.  A comment to that effect on the example seems appropriate.
![](images/icons/contenttypes/comment_16.png) Posted by jordanbrown at Mar 27, 2014 14:35
\| \|
> When strings live on the heap, this rule is a specific instance of [MEM35-C. Allocate sufficient memory for an object](https://www.securecoding.cert.org/confluence/display/c/MEM35-C.+Allocate+sufficient+memory+for+an+object).

I'm not sure I believe this. All the code examples and intro text deal exclusively with string copy operations, whereas MEM35-C deals with allocation (on the heap). By that argument, this rule and that rule are mutually exclusive.
On the other paw, the title is normative and clearly a subset of MEM35-C (when limited to the heap)
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 16, 2017 11:01
\| \|
IThere is an interesting question here. Consider this code:
1.  char\* dest = malloc(size);
2.  strcpy( dest, src);
If a buffer overflow occurs, is it a violation of STR31-C (buffer overflow on (2)) or MEM35-C (insufficient allocation on (1))?; A static analyzer cannot determine which line was at fault (it could be both).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 16, 2017 11:03
\| \|
It seems to me that the first non-compliant example exhibits a violation of ARR-30C before writing one past the end of the destination buffer:
    for (i = 0; src[i] && (i < n); ++i) {  dest[i] = src[i];
    }
    dest[i] = '\0';
Namely, in the loop condition, the check for \`src\[i\]\` is done before the check on the bound \`i\<n\`. Hence, one might read past the end of \`src\` buffer. The condition should probably be \`i\<n && src\[i\]\`, in which case the issue is indeed on the \`dest\[i\]='\0'\` instruction.
(full disclosure: I didn't found that manually, but in trying to understand why Frama-C was reporting the last instruction as dead code on a test case meant to show the problem).
![](images/icons/contenttypes/comment_16.png) Posted by virgile.prevosto at Dec 13, 2020 13:12
\| \|
True, the code example also violates ARR30-C. You'll find that, as noted by the introduction, this rule overlaps with both ARR30-C and ARR38-C.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Dec 14, 2020 08:37
\| \|
I've just learned, through the code fixes of OpenSSL, how to use optional width and precision values to "%s", [CVE-2021-3712](https://cve.mitre.org/cgi-bin/cvename.cgi?name=%20CVE-2021-3712).
(What I see is [the commits](https://github.com/openbsd/src/commit/3d508f29e57b079dbcf0484f850c5fb0063888ca) in OpenBSD source (mirror) repository...)
How about adding this kind of code as another Compliant Solution(sprintf())?
    the code
    BIO_printf(out, "%*sOrganization: %s\n",
                    indent, "",
                    ref->organization->data);
is fixed as
    BIO_printf(out, "%*sOrganization: %.*s\n",
                    indent, "",
                    ref->organization->length, ref->organization→data);
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Aug 25, 2021 02:02
\| \|
That change is just to handle the case where `ref->organization->data` isn't NUL-terminated. It doesn't help at all if it's so long that `out` overflows, which is what this rule is about.
![](images/icons/contenttypes/comment_16.png) Posted by jcsible at Aug 25, 2021 10:37
\| \|
Hello, Yozo-san. We also already have a compliant solution that uses snprintf. Which is easier in this case than using sprintf("%.\*s).
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Aug 25, 2021 11:34
\| \|
hi, David. I agree to prefer `snprintf` than `sprintf`.
hmm...; my point is to mention (lightly) that precision can be given as an additional argument.
for example, adding the following at the end of Compliant Solution(sprintf());
  You can use the precision "`*`" with an additional argument. e.g.,
`  ``sprintf``(filename, ``"%.*s.txt"``, 123, name);`
  But the better solution is to use `snprintf()``.`
![](images/icons/contenttypes/comment_16.png) Posted by yozo at Sep 06, 2021 16:25
\| \|
I have whipped up a code example that uses %.\* as you suggest.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Sep 07, 2021 09:24
\| \|
Hey, consider adding the following real-world classic example, involving `strncat` :
``` java
char you_cant_overflow_me[] = "CCCCCCC";
char dest[32] = {0}; 
char* src = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"; // longer than 32 bytes
strncpy(dest, "BBBB", sizeof(dest) - 1);  // Initialize the destination buffer to some correctly-terminated string
dest[sizeof(dest) - 1] = '\0';
strncat(dest, src, sizeof(dest) - strlen(dest)); 
printf("%s\n", you_cant_overflow_me);
```
The above code contains an OOB-write of a null byte.;
Both `dest`  and `src`  are initialized correctly as null-terminated strings. Therefore, `sizeof(dest) - strlen(dest) == 32 - 4 == 28. `
Since `strncat`  argument doesn't count the null byte, and always appends it at the end of the destination buffer, 29 bytes would be copied. 
That would lead to an overflow, overwriting the LSB of `you_cant_overflow_me` (note that on different platforms, local variables may be placed at a different order on the stack tho).  This means an empty string would be printed ![](images/icons/emoticons/smile.svg)
Also:
I agree with [Virgile Prevosto](https://wiki.sei.cmu.edu/confluence/display/~virgile.prevosto), there is an OOB-read 1 byte past the buffer
TBH I think this bug is a very good example and we should keep it, just consider stating that this OOB-read also exist 
![](images/icons/contenttypes/comment_16.png) Posted by meowmeow1 at Jan 18, 2023 22:29
\| \|
Interesting code example, it is a 1-byte buffer overflow. ;It is nifty that the overflow overwrites the "you_cant_overflow_me" string, but as this is undefined behavior, you can't rely on this happening, it is platform-specific.
In C23, footnote 375, on s7.26.32.2p2 is specifically to deal with the vulnerability in your sample code:
    Thus, the maximum number of characters that can end up in the array pointed to by s1 is strlen(s1)+n+1.
I don't think this warrants a new example in this rule, however. Since the OOB write occurs inside strncat(), it is more suitable for ARR38-C, but that already has several good example for showing buffer overflows.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at Jan 20, 2023 09:56
\|
