The C function `strtok()` is a string tokenization function that takes two arguments: an initial string to be parsed and a `const`-qualified character delimiter. It returns a pointer to the first character of a token or to a null pointer if there is no token.
The first time `strtok()` is called, the string is parsed into tokens and a character delimiter. The `strtok()` function parses the string up to the first instance of the delimiter character, replaces the character in place with a null byte (`'\0'`), and returns the address of the first character in the token. Subsequent calls to `strtok()` begin parsing immediately after the most recently placed null character.
Because `strtok()` modifies the initial string to be parsed, the string is subsequently unsafe and cannot be used in its original form. If you need to preserve the original string, copy it into a buffer and pass the address of the buffer to `strtok()` instead of the original string.
## Noncompliant Code Example
In this example, the `strtok()` function is used to parse the first argument into colon-delimited tokens; it outputs each word from the string on a new line. Assume that `PATH` is `"/usr/bin:/usr/sbin:/sbin"`.
``` c
char *token;
char *path = getenv("PATH");
token = strtok(path, ":");
puts(token);
while (token = strtok(0, ":")) {
  puts(token);
}
printf("PATH: %s\n", path);
/* PATH is now just "/usr/bin" */
```
After the loop ends, `path` is modified as follows: `"/usr/bin\0/bin\0/usr/sbin\0/sbin\0"`. This is an issue because the local `path` variable becomes `/usr/bin` and because the environment variable `PATH` has been unintentionally changed, which can have unintended consequences. (See [ENV30-C. Do not modify the object referenced by the return value of certain functions](ENV30-C_%20Do%20not%20modify%20the%20object%20referenced%20by%20the%20return%20value%20of%20certain%20functions).)
## Compliant Solution
In this compliant solution, the string being tokenized is copied into a temporary buffer that is not referenced after the call to `strtok()`:
``` c
char *token;
const char *path = getenv("PATH");
/* PATH is something like "/usr/bin:/bin:/usr/sbin:/sbin" */
char *copy = (char *)malloc(strlen(path) + 1);
if (copy == NULL) {
  /* Handle error */
}
strcpy(copy, path);
token = strtok(copy, ":");
puts(token);
while (token = strtok(0, ":")) {
  puts(token);
}
free(copy);
copy = NULL;
printf("PATH: %s\n", path);
/* PATH is still "/usr/bin:/bin:/usr/sbin:/sbin" */
```
Another possibility is to provide your own implementation of `strtok()` that does not modify the initial arguments.
## Risk Assessment
The *Linux Programmer's Manual* (man) page on `strtok(3)` \[[Linux 2008](AA.-Bibliography_87152170.html#AA.Bibliography-Linux08)\] states:
> Never use this function. This function modifies its first argument. The identity of the delimiting character is lost. This function cannot be used on constant strings.

The improper use of `strtok()` is likely to result in truncated data, producing unexpected results later in program execution.

| Recommendation | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| STR06-C | Medium | Likely | Medium | P12 | L1 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | (customization) | Users who wish to avoid using strtok() entirely can add a custom check for all uses of strtok(). |
| Compass/ROSE |  |  |  |
| Helix QAC | 2024.4 | C5007 |  |
| LDRA tool suite | 9.7.1 | 602 S | Enhanced Enforcement |

### Related Vulnerabilities
Search for vulnerabilities resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+STR06-C).
## Related Guidelines

|  |  |
| ----|----|
| SEI CERT C++ Coding Standard | VOID STR06-CPP. Do not assume that strtok() leaves the parse string unchanged |
| MITRE CWE | CWE-464, Addition of data structure sentinel |

## Bibliography

|  |  |
| ----|----|
| [Linux 2008] | strtok(3) |

------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152066) [](../c/Rec_%2007_%20Characters%20and%20Strings%20_STR_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152413)
## Comments:

|  |
| ----|
| I have two question regarding detecting this using ROSE...
    how do we know once it's safe to use the string again? certain function calls may leave it unchanged (puts), while others may make it "safe" again (memcpy)
    what if it is the programmer's intent to use the string, knowing full well that it has been modified?
                                        Posted by avolkovi at Jul 10, 2008 10:51
                                     |
| Answer#1: A string passed to strtok() is no longer safe, as strtok() modifies it. Theoretically you should never refer to a string after passing it to strtok(). The CCE accomplishes this by giving strtok() a copy of the string and then freeing the copy.
Whoops, the CS isn't actually freeing the copy...must fix that 
A fully rigorous solution would do sophisticated data flow analysis on the pointed-to strings...for now we can just pretend each char* points to a separate string.
Answer#2: For the purpose of this rule, using the string after knowing it has been modified falls into that purgatory of technically-correct-but-bad-style code, also inhabited by constructs such as "if (a = b) ...". Even if the code does the right thing, it may still be considered a mistake and 'fixed' by a future maintainer, which can lead to vuls later on...the Debian SSL vul being a prime example.
                                        Posted by svoboda at Jul 11, 2008 11:24
                                     |
| Ok, so it's not too strict too say that the only valid use for a string after getting passed to strtok is as an argument to strcpy, memcpy, free, or as the lhs to an assignment? and that after one of those calls the string becomes valid again.
                                        Posted by avolkovi at Jul 11, 2008 12:35
                                     |
| Is there a reason not to use strncpy in the solution?;
                                        Posted by asolano at Apr 04, 2013 13:44
                                     |
| Because strcpy() is safe in this instance, as the destination string 's memory is allocated to be large enough to hold it.
                                        Posted by svoboda at Apr 05, 2013 12:17
                                     |
| Indeed. Thanks for the clarification.;
                                        Posted by asolano at Apr 05, 2013 13:43
                                     |

