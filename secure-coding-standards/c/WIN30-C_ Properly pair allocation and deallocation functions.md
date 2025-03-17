Windows provides several APIs for allocating memory.  While some of these functions have converged over time, it is still important to always properly pair allocations and deallocations.  The following table shows the proper pairings.

| Allocator | Deallocator |
| ----|----|
| malloc() | free() |
| realloc() | free() |
| LocalAlloc() | LocalFree() |
| LocalReAlloc(); | LocalFree() |
| GlobalAlloc() | GlobalFree() |
| GlobalReAlloc() | GlobalFree() |
| VirtualAlloc() | VirtualFree() |
| VirtualAllocEx() | VirtualFreeEx() |
| VirtualAllocExNuma() | VirtualFreeEx() |
| AllocateUserPhysicalPages() | FreeUserPhysicalPages() |
| AllocateUserPhysicalPagesNuma() | FreeUserPhysicalPages() |
| HeapAlloc() | HeapFree() |
| HeapReAlloc() | HeapFree() |

## Noncompliant Code Example
In this example, the `FormatMessage()` function allocates a buffer and stores it in the `buf` parameter.  From the documentation of `FORMAT_MESSAGE_ALLOCATE_BUFFER` \[[MSDN](http://msdn.microsoft.com/en-us/library/ms679351(v=vs.85).aspx)\]:
> The function allocates a buffer large enough to hold the formatted message, and places a pointer to the allocated buffer at the address specified by lpBuffer.  The lpBuffer parameter is a pointer to anL PTSTR; you must cast the pointer to an LPTSTR (for example, (LPTSTR)&lpBuffer). The nSize parameter specifies the minimum number of TCHARs to allocate for an output message buffer. The caller should use the LocalFree function to free the buffer when it is no longer needed.

Instead of freeing the memory using `LocalFree()`, this code example uses `GlobalFree()` erroneously.
``` c
LPTSTR buf;
DWORD n = FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER |
                        FORMAT_MESSAGE_FROM_SYSTEM |
                        FORMAT_MESSAGE_IGNORE_INSERTS, 0, GetLastError(),
                        LANG_USER_DEFAULT, (LPTSTR)&buf, 1024, 0);
if (n != 0) {
  /* Format and display the error to the user */
  GlobalFree(buf);
}
```
## Compliant Solution
The compliant solution uses the proper deallocation function as described by the documentation.
``` c
LPTSTR buf;
DWORD n = FormatMessage(FORMAT_MESSAGE_ALLOCATE_BUFFER |
                        FORMAT_MESSAGE_FROM_SYSTEM |
                        FORMAT_MESSAGE_IGNORE_INSERTS, 0, GetLastError(),
                        LANG_USER_DEFAULT, (LPTSTR)&buf, 1024, 0);
if (n != 0) {
  /* Format and display the error to the user */
  LocalFree(buf);
}
```
## Risk Assessment
Mixing allocation and deallocation functions can lead to memory corruption issues, or result in accessing out-of-bounds memory.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN30-C | Low | Probable | Low | P6 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Astrée | 24.04 |  | Supported: Can be checked with appropriate analysis stubs. |
| CodeSonar | 8.3p0 | ALLOC.TM | Type mismatch |
| Coverity | 2017.07 | ALLOC_FREE_MISMATCH (needs improvement) | Partially implemented; needs improvement |
| Klocwork | 2024.4 | FMM.MIGHTFMM.MUST |  |
| Parasoft C/C++test | 2024.2 | CERT_C-WIN30-a | Ensure resources are freed |
| Polyspace Bug Finder | R2024a | CERT C: Rule WIN30-C | Checks for mismatched alloc/dealloc functions on Windows (rule fully covered) |
| PVS-Studio | 7.35 | V701 |  |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerabi) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+FIO03-C).
### Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | MEM51-CPP. Properly deallocate dynamically allocated resources |

------------------------------------------------------------------------
[](../c/Rule%2051_%20Microsoft%20Windows%20_WIN_) [](../c/Rule%2051_%20Microsoft%20Windows%20_WIN_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87151983)
