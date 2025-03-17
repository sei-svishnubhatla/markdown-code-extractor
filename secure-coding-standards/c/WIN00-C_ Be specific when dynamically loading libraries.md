The `LoadLibrary()` or `LoadLibraryEx()` function calls \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/ms684175(v=vs.85).aspx)\] allow you to dynamically load a library at runtime and use a specific algorithm to locate the library within the file system \[[MSDN](http://msdn.microsoft.com/en-us/library/windows/desktop/ms682586(v=vs.85).aspx)\]. It is possible for an attacker to place a file on the DLL search path such that your application inadvertently loads and executes arbitrary source code.
## Noncompliant Code Example
``` c
#include <Windows.h>
void func(void) {
  HMODULE hMod = LoadLibrary(TEXT("MyLibrary.dll"));
  if (hMod != NULL) {
    typedef void (__cdecl func_type)(void);
    func_type *fn = (func_type *)GetProcAddress(hMod, "MyFunction");
    if (fn != NULL)
      fn();
  }
}
```
If an attacker were to place a malicious DLL named MyLibrary.dll higher on the search path than where the library resides, she could trigger arbitrary code to execute either via the `DllMain()` entrypoint (which is called automatically by the system loader) or by providing an implementation for `MyFunction()`, either of which would run within the security context of your application. If your application runs with elevated privileges (such as a service application), an escalation of privileges could result.
## Compliant Solution
By refusing to load a library unless it is located precisely where expected, you reduce the chance of executing arbitrary code when dynamically loading libraries. This compliant solution uses `LoadLibraryEx()` to ensure that only the application and System32 directories are searched (eliminating other search paths such as the current directory or `PATH` environment variable):
``` c
#include <Windows.h>
void func(void) {
  HMODULE hMod = LoadLibraryEx(TEXT("MyLibrary.dll"), NULL,
                               LOAD_LIBRARY_SEARCH_APPLICATION_DIR |
                               LOAD_LIBRARY_SEARCH_SYSTEM32);
  if (hMod != NULL) {
    typedef void (__cdecl func_type)(void);
    func_type *fn = (func_type *)GetProcAddress(hMod, "MyFunction");
    if (fn != NULL)
      fn();
  }
}
```
## Risk Assessment
Depending on the version of Windows the application is run on, failure to properly specify the library can lead to arbitrary code execution.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| WIN00-C | High | Unlikely | Low | P9 | L2 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.PATH.AFXLOADLIBRARYBADFUNC.PATH.COLOADLIBRARY
BADFUNC.PATH.LOADLIBRARY | Use of AfxLoadLibraryUse of CoLoadLibrary
Use of LoadLibrary |
| Klocwork | 2024.4 | SV.DLLPRELOAD.NONABSOLUTE.DLLSV.DLLPRELOAD.NONABSOLUTE.EXE
SV.DLLPRELOAD.SEARCHPATH |  |
| Parasoft C/C++test | 2024.2 | CERT_C-WIN00-a | Use care to ensure that LoadLibrary() will load the correct library |
| PC-lint Plus | 1.4 | 586 | Fully supported |
| Polyspace Bug Finder | R2024a | CERT C: Rec. WIN00-C | Checks for:Load of library from a relative path can be controlled by external actorLibrary loaded from externally controlled path.Rec. partially covered. |

## Related Guidelines

|  |  |
| ----|----|
|  |  |

## Bibliography

|  |  |
| ----|----|
|  |  |

------------------------------------------------------------------------
[](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_)[](../c/Rec_%2051_%20Microsoft%20Windows%20_WIN_)[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152032)
## Comments:

|  |
| ----|
| Just a semantics comment here. I am not sure if "eliminate" is the best choice of wording for the compliant solution.That phrasing seems to imply that all chances of arbitrary code execution are dealt with by specifying library locations. It seems like more of a partial mitigation to me; considering that the problems mentioned from the non-compliant solution are still present, just in a more limited fashion.
                                        Posted by jloo at Jul 08, 2013 15:17
                                     |
| Yes, perhaps eliminate is too strong of a term here.; This rule really needs a corollary that explains users need to secure their installation directory properly in order to truly eliminate the issue.  But that's extraneous to the contents of the guidelines, so it doesn't really fit anywhere.
                                        Posted by aballman at Jul 08, 2013 20:05
                                     |
| SafeDllSearchMode has defaulted to 1 since XP SP2, and with SafeDllSearchMode being 1, the application directory and system directory are already searched first by default. Is there still a benefit to specifying the load order by hand? If an attacker could force later directories to be tried by deleting the DLL in one of those trusted directories, couldn't they also just replace it with their malicious DLL directly?
                                        Posted by jcsible at Jul 07, 2020 16:47
                                     |
| That will protect your code as long as the library you are searching for lives in the application directory or system directory.If your library lives elsewhere, the compliant solution will fail with a "library not found" error, while the noncompliant code example can still find a malicious library that lives further down the path.Your point might still be worthy of a compliant solution if you are willing to write one.
                                        Posted by svoboda at Aug 14, 2020 15:54
                                     |

