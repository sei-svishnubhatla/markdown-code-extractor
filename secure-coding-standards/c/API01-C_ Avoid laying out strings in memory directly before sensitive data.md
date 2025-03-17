Strings (both character and wide-character) are often subject to buffer overflows, which will overwrite the memory immediately past the string. Many rules warn against buffer overflows, including [STR31-C. Guarantee that storage for strings has sufficient space for character data and the null terminator](STR31-C_%20Guarantee%20that%20storage%20for%20strings%20has%20sufficient%20space%20for%20character%20data%20and%20the%20null%20terminator). Sometimes the danger of buffer overflows can be minimized by ensuring that arranging memory such that data that might be corrupted by a buffer overflow is not sensitive.
## Noncompliant Code Example
This noncompliant code example stores a set of strings using a linked list:
``` c
const size_t String_Size = 20;
struct node_s {
  char name[String_Size];
  struct node_s* next;
}
```
A buffer overflow on `name` would overwrite the `next` pointer, which could then be used to read or write to arbitrary memory.
## Compliant Solution
This compliant solution creates a linked list of strings but stores the `next` pointer before the string:
``` c
const size_t String_Size = 20;
struct node_s {
  struct node_s* next;
  char name[String_Size];
}
```
If buffer overflow occurs on `name`, the `next` pointer remains uncorrupted.
## Compliant Solution
In this compliant solution, the linked list stores pointers to strings that are stored elsewhere. Storing the strings elsewhere protects the `next` pointer from buffer overflows on the strings.
``` c
const size_t String_Size = 20;
struct node_s {
  struct node_s* next;
  char* name;
}
```
## Exceptions
**API01-C-EX1:** Using a string before sensitive data such as pointers is permitted when it is not practical to segregate the strings from the sensitive data.
Each of the following code examples creates a linked list of strings, but each node is actually stored inside an array. This practice ensures that the string is always in front of a `next` pointer regardless of how they are ordered in the struct.
``` c
const size_t String_Size = 20;
struct node_s {
  char name[String_Size];
  struct node_s* next;
}
struct node_s list[10];
```
``` c
const size_t String_Size = 20;
struct node_s {
  struct node_s* next;
  char name[String_Size];
}
struct node_s list[10];
```
## Risk Assessment
Failure to follow this recommendation can result in memory corruption from buffer overflows, which can easily corrupt data or yield remote code execution.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| API01-C | High | Likely | High | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 | array_out_of_boundsfield_overflow_upon_dereference | Supported |
| Parasoft C/C++test | 2024.2 | CERT_C-API01-aCERT_C-API01-b | Avoid overflow when writing to a bufferAvoid using unsafe string functions which may cause buffer overflows |

[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152074) [](../c/Rec_%2013_%20Application%20Programming%20Interfaces%20_API_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152290)
## Comments:

|  |
| ----|
| This recommendation is missing Risk Assessment info. Is that on purpose or it's a gap that should be filled by someone?
                                        Posted by rozenau at Jun 01, 2018 14:59
                                     |
| Risk Assesments are required for our rules only. Our recommendations need not contain Risk Assessment info, although many do. I went ahead and added one for this recommendation, because the values were fairly obvious.
                                        Posted by svoboda at Jun 01, 2018 15:21
                                     |

