The `getenv()` function searches an environment list for a string that matches a specified name and returns a pointer to a string associated with the matched list member.
Subclause 7.22.4.6 of the C Standard \[[ISO/IEC 9899:2011](https://www.securecoding.cert.org/confluence/display/seccode/AA.+Bibliography#AABibliography-ISOIEC9899-2011)\] states:
> The set of environment names and the method for altering the environment list are [implementation-defined](BB.-Definitions_87152273.html#BB.Definitions-implementationdefinedbehavior).

Depending on the [implementation](BB.-Definitions_87152273.html#BB.Definitions-implementation), multiple environment variables with the same name may be allowed and can cause unexpected results if a program cannot consistently choose the same value. The GNU glibc library addresses this issue in `getenv()` and `setenv()` by always using the first variable it encounters and ignoring the rest. However, it is unwise to rely on this behavior.
One common difference between implementations is whether or not environment variables are case sensitive. Although UNIX-like implementations are generally case sensitive, environment variables are "not case sensitive in Windows 98/Me and Windows NT/2000/XP" \[[MSDN](AA.-Bibliography_87152170.html#AA.Bibliography-MSDN)\].
## Duplicate Environment Variable Detection (POSIX)
The following code defines a function that uses the POSIX `environ` array to manually search for duplicate key entries. Any duplicate environment variables are considered an attack, so the program immediately terminates if a duplicate is detected.
``` c
extern char **environ;
int main(void) {
  if (multiple_vars_with_same_name()) {
    printf("Someone may be tampering.\n");
    return 1;
  }
  /* ... */
  return 0;
}
int multiple_vars_with_same_name(void) {
  size_t i;
  size_t j;
  size_t k;
  size_t l;
  size_t len_i;
  size_t len_j;
  for(size_t i = 0; environ[i] != NULL; i++) {
    for(size_t j = i; environ[j] != NULL; j++) {
      if (i != j) {
        k = 0;
        l = 0;
        len_i = strlen(environ[i]);
        len_j = strlen(environ[j]);
        while (k < len_i && l < len_j) {
          if (environ[i][k] != environ[j][l])
            break;
          if (environ[i][k] == '=')
            return 1;
          k++;
          l++;
        }
      }
    }
  }
  return 0;
}
```
## Noncompliant Code Example
This noncompliant code example behaves differently when compiled and run on Linux and Microsoft Windows platforms:
``` c
if (putenv("TEST_ENV=foo") != 0) {
  /* Handle error */
}
if (putenv("Test_ENV=bar") != 0) {
  /* Handle error */
}
const char *temp = getenv("TEST_ENV");
if (temp == NULL) {
  /* Handle error */
}
printf("%s\n", temp);
```
On an IA-32 Linux machine with GCC 3.4.4, this code prints
``` java
foo
```
whereas, on an IA-32 Windows XP machine with Microsoft Visual C++ 2008 Express, it prints
``` java
bar
```
## Compliant Solution
Portable code should use environment variables that differ by more than capitalization:
``` c
if (putenv("TEST_ENV=foo") != 0) {
  /* Handle error */
}
if (putenv("OTHER_ENV=bar") != 0) {
  /* Handle error */
}
const char *temp = getenv("TEST_ENV");
if (temp == NULL) {
  /* Handle error */
}
printf("%s\n", temp);
```
## Risk Assessment
An attacker can create multiple environment variables with the same name (for example, by using the POSIX `execve()` function). If the program checks one copy but uses another, security checks may be circumvented.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| ENV02-C | Low | Unlikely | Medium | P2 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Compass/ROSE |  |  |  |
| Parasoft C/C++test | 2024.2 | CERT_C-ENV02-a | Usage of system properties (environment variables) should be restricted |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+ENV02-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID ENV00-CPP. Beware of multiple environment variables with the same effective name |
| ISO/IEC TR 24772:2013 | Executing or Loading Untrusted Code [XYS] |
| MITRE CWE | CWE-462, Duplicate key in associative list (Alist)CWE-807, Reliance on untrusted inputs in a security decision |

## Bibliography

|  |  |
| ----|----|
| [ISO/IEC 9899:2011] | Section 7.22.4, "Communication with the Environment" |
| [MSDN] | getenv() |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152092) [](../c/Rec_%2010_%20Environment%20_ENV_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152420)
## Comments:

|  |
| ----|
| The bit about glibc should be replaced by "Most implementations of getenv always return the first matching entry, although it is unwise to rely on this."; There is no need to mention unsetenv, which is not universally available (also it's not generally a good idea for a program to modify the environment strings).
                                        Posted by dagwyn at Apr 17, 2008 20:08
                                     |
| The CCE should accomplish the same task as the the NCCE... as it stands the CCE does not solve the problem within the NCCE, it merely provides a way to discover duplicate entries
                                        Posted by avolkovi at Jun 03, 2008 13:11
                                     |
| Hm, the main thing that bothers me is simply that OS's allow the environment to have multiple values for one var...that strikes me as an OS bug, not an app programmer's bug. It is adequately addressed by the multiple_vars_with_same_name() function, however.
The CCE is IMHO adequate b/c it identifies the problem. I presume there's no legit reason for an env to have duplicate vars.
But the NCCE needs some explanation as to why duplicate env vars are a problem for it. Seems the only problem there is that you don't know what the resulting env data might be.
                                        Posted by svoboda at Jun 04, 2008 15:27
                                     |
| Would it help if we had a putenv() before the first getenv()? Then you wouldn't be sure what value you are reading, if it's the one you put in, or some bogus one.
                                        Posted by avolkovi at Jun 04, 2008 15:45
                                     |
| Yes that would help. Especially if you could demonstrate it reading the wrong value (eg "this works on MSVC)
                                        Posted by svoboda at Jun 04, 2008 16:27
                                     |
| added some code that behaves differently under Linux and Windows
                                        Posted by avolkovi at Jun 05, 2008 11:20
                                     |
| Good NCCE/CCE pair. I'm not going to complain that TEST_ENV/Test_Env are actually not duplicate env vars in Linux  
The 2nd NCCE still needs an explanation as to why dup env vars are harmful to it. (In light of the new  NCCE/CCE pair, do we even need the 2nd NCCE?)
                                        Posted by svoboda at Jun 05, 2008 14:22
                                     |
| The problem is you really can't have dup vars with our setup.... Windows doesn't let you (even if you manually try to add two), and Linux always picks the first one, and removes all... basically I'd need some oddball test machine in order to really have dup vars, so I don't think the second pair is necessary either
                                        Posted by avolkovi at Jun 05, 2008 14:29
                                     |
| If you can't really have dup vars, then this rule is basically useless. At least the 2nd NCCE is. One could rescue this rule by removing the 2nd NCCE/CCE samples, and change the title to reflect the 1st.
                                        Posted by svoboda at Jun 05, 2008 14:39
                                     |
| how about
    removing the second pair
    changing the name to "Beware of multiple environment variables with the same effective name"
    placing the emphasis on how capitalization is not specified (but leave the note about order and multiple vars)
                                        Posted by avolkovi at Jun 05, 2008 14:45
                                     |
| You can have duplicates in Linux if the implementation isn't glibc compliant.
                                        Posted by jpincar at Jun 05, 2008 15:28
                                     |
| Sounds good. I went ahead & made these changes.
                                        Posted by svoboda at Jun 05, 2008 15:30
                                     |
| Regarding the ROSE suggestion, how do we get access to the environment?
                                        Posted by avolkovi at Jul 25, 2008 13:53
                                     |
| answered in the ROSE paragraph.
                                        Posted by svoboda at Jul 25, 2008 15:07
                                     |
| but in most cases the environment will be passed in on startup.... especially in the case where a violation actually matters, that is the one where an attacker controls the environment.
                                        Posted by avolkovi at Jul 25, 2008 15:48
                                     |
| but in all cases, the program will only be interested in a few specific variables and will have to ask for them by name. So scraping the program for env vars like TEST/test will turn up the env vars deemed important to the program.
It's possible we miss a few, such as if the program asks for 'path' but the env only has PATH.  I'm not (yet) concerned about those.
                                        Posted by svoboda at Jul 25, 2008 16:34
                                     |

