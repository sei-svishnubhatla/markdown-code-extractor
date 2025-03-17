Memory is a limited resource and can be exhausted. Available memory is typically bounded by the sum of the amount of physical memory and the swap space allocated to the operating system by the administrator. For example, a system with 1GB of physical memory configured with 2GB of swap space may be able to allocate, at most, 3GB of heap space total to all running processes (minus the size of the operating system itself and the text and data segments of all running processes). Once all virtual memory has been allocated, requests for more memory will fail. As discussed in [ERR33-C. Detect and handle standard library errors](ERR33-C_%20Detect%20and%20handle%20standard%20library%20errors), programs that fail to check for and properly handle memory allocation failures will have [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior) and are likely to crash when heap space is exhausted. Heap exhaustion can result from
-   A memory leak
-   An infinite loop
-   The program requiring more memory than is present by default in the heap
-   Incorrect implementation of common data structures (for example, hash tables or vectors)
-   Overall system memory being exhausted, possibly because of other processes
-   The maximum size of a process's data segment being exceeded
If `malloc()` is unable to return the requested memory, it returns `NULL` instead.
However, simply checking for and handling memory allocation failures may not be sufficient. Programs such as long-servers that manipulate large data sets need to be designed in a way that permits them to deliver their services when system resources, including the heap, are in short supply. Making use of additional storage devices, such as disk space or databases, is essential in such systems.
## Noncompliant Code Example
This example places no upper bound on the memory space required. As a result, the program can easily exhaust the heap. A heap error will be generated if the heap continues to be populated, even if there is no space available.
``` c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
enum {MAX_LENGTH=100};
typedef struct namelist_s {
  char name[MAX_LENGTH];
  struct namelist_s* next;
} *namelist_t;
int main() {
  namelist_t names = NULL;
  char new_name[MAX_LENGTH];
  do {
    /* 
     * Adding unknown number of records to a list;
     * the user can enter as much data as he wants
     * and exhaust the heap.
     */
    puts("To quit, enter \"quit\"");
    puts("Enter record:");
    fgets(new_name, MAX_LENGTH, stdin);
    if (strcmp(new_name, "quit") != 0) {
      /* 
       * Names continue to be added without bothering 
       * about the size on the heap.
       */
      unsigned int i = strlen(new_name) - 1;
      if (new_name[i] == '\n') new_name[i] = '\0';
      namelist_t new_entry = (namelist_t) malloc(sizeof( struct namelist_s));
      if (new_entry == NULL) {
        /* Handle error */
      }
      strcpy( new_entry->name, new_name);
      new_entry->next = names;
      names = new_entry;
    }
    puts(new_name);
  } while (strcmp( new_name, "quit") != 0);
  return 0;
}
```
## Compliant Solution
If the objects or data structures are large enough to potentially cause heap exhaustion, the programmer should consider using databases instead to ensure that records are written to the disk and that the data structure does not outgrow the heap.
In the previous noncompliant code example, the user can reuse a single `long` variable to store the input and write that value into a simple database containing a table `User` with a field `userID` along with any other required fields. This prevents the heap from being exhausted.
## Risk Assessment
It is difficult to pinpoint violations of this recommendation because [static analysis](BB.-Definitions_87152273.html#BB.Definitions-staticanalysis) tools are currently unable to identify code that can lead to heap exhaustion. The heap size also varies for different runtime environments.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEM11-C | Low | Probable | High | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | ALLOC.LEAKIO.TAINT.SIZE
MISC.MEM.SIZE.BAD
(general) | LeakTainted allocation size
Unreasonable size argument
Library models account for allocator failure cases |
| LDRA tool suite | 9.7.1 | 26 S, 140 S, 6 D, 28 D, 5 C, 1 U | Partially implemented |
| PC-lint Plus | 1.4 | 413, 613 | Assistance provided: reports use of null pointers including those which could be returned when a call to an allocation function fails |
| Polyspace Bug Finder | R2024a | CERT C: Rec. MEM11-C | Checks for unprotected dynamic memory allocation (rule partially covered) |

## Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEM11-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID MEM12-CPP. Do not assume infinite heap space |
| CERT Oracle Secure Coding Standard for Java | MSC05-J. Do not exhaust heap space |
| MITRE CWE | CWE-770, Allocation of resources without limits or throttling |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152072) [](../c/Rec_%2008_%20Memory%20Management%20_MEM_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152289)
## Comments:

|  |
| ----|
| The opening sentence in this rule:
A program will crash if memory is requested while the heap is exhausted.
may be close to true on systems with memory overcommitting behavior (AIX and Linux) where malloc() may return a non-NULL pointer that may cause the SIGSEGV signal to be sent to the process when dereferenced. Such behavior is widely considered in violation of the C and POSIX standards and should be disabled by the system administrator for security.
A conforming implementation of malloc() either returns a pointer to a region of memory of the requested size of NULL on failure.
A better wording would be:
Programs that fail to check for and properly handle memory allocation failures will have undefined behavior and likely crash when heap space is exhausted.
                                        Posted by martinsebor at Jan 10, 2010 21:59
                                     |
| We made the wording change.
The overcommitting problem is significant; although it tends to only happen in programs that would exhaust a normal heap anyway. Since the problem and solutions are platform-dependent, we haven't included it in the rule...not sure if itw worth including.
                                        Posted by svoboda at Jan 11, 2010 11:29
                                     |
| There's little a program can do to prevent or handle the overcommitting behavior if the sysadmin doesn't disable it. Maybe it would be worth making it a recommendation for programs to terminate at startup when overcommitting behavior is detected (similarly to the guidance given ENV02-C. Beware of multiple environment variables with the same effective name). Unfortunately, the detection would have to rely on implementation-specific means since memory overcomitting isn't addressed or even mentioned in any standard.
                                        Posted by martinsebor at Jan 11, 2010 15:30
                                     |
| removed reference to setrlimit() in intro paragraph since this is a POSIX specific function.
                                        Posted by rcs_mgr at Feb 06, 2012 09:36
                                     |
| How is this substantively different from MEM32-C. Detect and handle memory allocation errors or its replacement ERR33-C. Detect and handle standard library errors?I think this should basically be rolled into ERR33-C and deprecated.; Objections?
                                        Posted by aballman at Sep 10, 2013 13:23
                                     |

