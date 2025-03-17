When forking a child process, file descriptors are copied to the child process, which can result in concurrent operations on the file. Concurrent operations on the same file can cause data to be read or written in a nondeterministic order, creating race conditions and unpredictable behavior.
## Noncompliant Code Example
In this example, the programmer wishes to open a file, read a character, fork, and then have both parent and child process read the second character of the file independently. However, because both processes share a file descriptor, one process might get the second character, and one might get the third. Furthermore, there is no guarantee the reads are atomic—the processes might get unpredictable results. Regardless of what the programmer is trying to accomplish with this code, this code is incorrect because it contains a race condition.
``` c
char c;
pid_t pid;
int fd = open(filename, O_RDWR);
if (fd == -1) {
  /* Handle error */
}
read(fd, &c, 1);
printf("root process:%c\n",c);
pid = fork();
if (pid == -1) {
  /* Handle error */
}
if (pid == 0) { /*child*/
  read(fd, &c, 1);
  printf("child:%c\n",c);
}
else { /*parent*/
  read(fd, &c, 1);
  printf("parent:%c\n",c);
}
```
If the file accessed has contents `"abc"`, the output of this program could be either
``` java
root process:a
parent: b
child: c
```
or
``` java
root process: a
child: b
parent: c
```
This code's output cannot reliably be determined and should not be used.
## Compliant Solution
In this compliant solution, the programmer closes the file descriptor in the child after forking and then reopens it, ensuring that the file has not been modified in the meantime. See [POS01-C. Check for the existence of links when dealing with files](POS01-C_%20Check%20for%20the%20existence%20of%20links%20when%20dealing%20with%20files) for details.
``` c
char c;
pid_t pid;
/* Open file and remember file status  */
struct stat orig_st;
if (lstat( filename, &orig_st) != 0) {
  /* handle error */
}
int fd = open(filename, O_RDWR);
if (fd == -1) {
  /* Handle error */
}
struct stat new_st;
if (fstat(fd, &new_st) != 0) {
  /* handle error */
}
if (orig_st.st_dev != new_st.st_dev ||
    orig_st.st_ino != new_st.st_ino) {
  /* file was tampered with while opening */
}
/* file is good, operate on fd */
read(fd,&c,1);
printf("root process:%c\n",c);
pid = fork();
if (pid == -1) {
  /* Handle error */
}
if (pid == 0){ /*child*/
  close(fd);
  /* Reopen file, creating new file descriptor */
  fd = open(filename, O_RDONLY);
  if (fd == -1) {
    /* Handle error */
  }
  if (fstat(fd, &new_st) != 0) {
    /* handle error */
  }
  if (orig_st.st_dev != new_st.st_dev ||
      orig_st.st_ino != new_st.st_ino) {
    /* file was tampered with between opens */
  }
  read(fd, &c, 1);
  read(fd, &c, 1);
  printf("child:%c\n", c);
  close(fd);
}
else { /*parent*/
  read(fd, &c, 1);
  printf("parent:%c\n", c);
  close(fd);
}
```
The output of this code is
``` java
root process:a
child:b
parent:b
```
## Risk Assessment
Because race conditions in code are extremely hard to find, this problem might not appear during standard debugging stages of development. However, depending on what file is being read and how important the order of read operations is, this problem can be particular dangerous.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| POS38-C | medium | unlikely | medium | P4 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| CodeSonar | 8.3p0 | BADFUNC.FORK | Use of fork |
| Helix QAC | 2024.4 | DF4951, DF4952 |  |
| Parasoft C/C++test | 2024.2 | CERT_C-POS38-a | Avoid race conditions when using fork and file descriptors |
| Polyspace Bug Finder | R2024a | CERT C: Rule POS38-C | Checks for file descriptor exposure to child process (rule fully covered) |

## Bibliography
**TODO**
------------------------------------------------------------------------
[](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152195) [](../c/Rule%2050_%20POSIX%20_POS_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152329)
## Comments:

|  |
| ----|
| David, this article is supposed to be more about the non-determinism in the order that parent/child proceses will run in, and that because file access is sequential, the different processes could read different data in different runs of the program. And any program with non-determinism is at risk for a bug.;  I hope I cleared that up with this most recent update, please let me know what you think. 
                                        Posted by hpitelka at Mar 31, 2009 11:34
                                     |
| OK, this is now a valid rule. Comments:
    This rule belongs in POSIX, since fork() is not C99.
    Should reference CON32-C. When data must be accessed by multiple threads, provide a mutex and guarantee no adjacent data is also accessed
    Please abide by the styleguide anouncement I mailed last week.
                                        Posted by svoboda at Mar 31, 2009 14:33
                                     |
| 
    Please abide by the styleguide anouncement I mailed last week. (eg add link to POSIX, add intro to code sections, risk assessment, etc). Study the other rules in the standard if necessary.
                                        Posted by svoboda at Apr 01, 2009 12:55
                                     |
| I'd say this rule is now complete.
                                        Posted by svoboda at Apr 01, 2009 18:30
                                     |
| I rewrote the first paragraph... please double check.
The references are incorrect.
This rule needs a more proscriptive title.
                                        Posted by rcs at Apr 04, 2009 09:40
                                     |
| The requirement not to pass file descriptors through a fork() call is far too restrictive.  Doing so is a very common and useful technique.  For example, to connect two processes with a pipe the pipe is created in the parent and the two file descriptors are passed across fork().
The real problem here is trying to use the same open file description in two processes at the same time.  The pipe example does not have this problem because each process only uses one end of the pipe, and closes the unused end.  The noncompliant code in this rule can be fixed by closing and reopening the file in the child.  There is no need for the parent to close the file descriptor before forking.
                                        Posted by geoffclare at Apr 20, 2009 05:10
                                     |
| I'm not sure whether the title has changed since this comment was made.  The current title "Be careful when using fork and file descriptors" seems fine to me.  It doesn't match the requirements stated within the rule, but that's because those requirements are too restrictive (see my other comment).  The requirements need to change to fit the title, not the other way round.
                                        Posted by geoffclare at Apr 20, 2009 05:17
                                     |
| Reworked the rule to focus on the race condition (of the shared file descriptor).
As it is, the compliant solution sill violates FIO31-C. Do not open a file that is already open but I suspect the problem lies with that rule, not with this one. Adding a comment there.
                                        Posted by svoboda at Apr 20, 2009 11:53
                                     |
| Oops, it does not. FIO31-C is really about not opening a file that is already open. It could use some clarification on that point.
                                        Posted by svoboda at Apr 20, 2009 11:57
                                     |
| Looks good, apart from the last paragraph in the "Compliant Solution" section (beginning "Because file descriptors access files in a sequential manner ...").
I think the paragraph is probably not relevant any more and can be deleted.  (If not deleted, it needs work.  E.g. the beginning clause quoted above is misleading - it is not file descriptors themselves that are sequential, but the read() function.)
There is also a stray piece of text in the "Noncompliant Code Example" section referring to POS01-C.  Perhaps this was meant to be a note that the code also violates POS01-C?
                                        Posted by geoffclare at Apr 20, 2009 12:43
                                     |
| Removed that paragraph. and stray POS01-C reference.
                                        Posted by svoboda at Apr 20, 2009 13:27
                                     |
| I see no real race condition in the non-compliant example. In fact, code that relies on the operating system to synchronize parallel file reads is a common way to divide work among several processes or threads, each performing the same task on sequential chunks of data in the file.
A non-compliant example that in my opinion better illustrates a race condition between a parent and child process involves both a read and a write:
int main() {
  char c;
  pid_t pid;
  int fd, n;
  fd = open("file.txt", O_CREAT | O_RDWR | O_TRUNC, 0600);
  if (-1 == fd) {  return 1; /* Error */ }
  pid = fork();
  if (-1 == pid) { return 2; /* Error */ }
  if (pid) {
    /* Race: assuming parent runs before child */
    n = write(fd, "*", 1);
    printf("write: %d\n", n);
  }
  else {
    /* Race: assuming child runs after parent */
    n = read(fd, &c, 1);
    printf("read: %d: %d\n", n, c);
  }
  return 0;
}

![](images/icons/contenttypes/comment_16.png) Posted by martinsebor at Jan 12, 2010 21:14
\|
