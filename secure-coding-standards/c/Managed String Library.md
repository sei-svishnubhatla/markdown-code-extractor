## Managed String Library
The managed string library was developed in response to the need for a string library that can improve the quality and security of newly developed C-language programs while eliminating obstacles to widespread adoption and possible standardization. As the name implies, the managed string library is based on a dynamic approach; memory is allocated and reallocated as required. This approach eliminates the possibility of unbounded copies, null-termination errors, and truncation by ensuring that there is always adequate space available for the resulting string (including the terminating null character). The one exception is if memory is exhausted; that is treated as an error condition. In this way, the managed string library accomplishes the goal of indicating either success or failure. The managed string library also protects against improper data sanitization by (optionally) ensuring that all characters in a string belong to a predefined set of "safe" characters.
### Accessing the library
A beta implementation of the managed string library is available fo [download](attachments/87151999/88025720.zip)
### Additional information
The following documents contain more detailed information about this project:
-   Managed String Course - [Safer Strings in C: Using the Managed String Library](attachments/87151999/88025722.pdf). Software Security Summit, February 7, 2006
-   [Managed String Library for C](http://www.drdobbs.com/184402023). C/C++ Users Journal. Vol. 23, No. 10. Pages 30-34. October 2005
-   [Information Technology - Programming languages, their environments and system software interfaces: Specification for Managed Strings (ISO/IEC JTC1 SC22 WG14 N1175)](http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1175.pdf). Post Berlin mailing, April 4, 2006  
### Revision History
Version 3.7-01-09 includes the following changes:
-   Fixed to run properly on Mac OS X
Version 3.2-17-09 includes the following changes:
-   Fixes proposed by Yannick Moy based on Frama-C and Coverity output
-   Fixes based on ROSE output
-   Fixes based on MSVC 'analyze' command
-   Minimized warnings from gcc
-   Minimized warnings from MSVC
-   Eliminated memory leaks from 'test' program according to valgrind
-   Added 'test.ans' file, contains expected output of test program  
    ------------------------------------------------------------------------
    Last updated October 18, 2010
## Attachments:
![](images/icons/bullet_blue.gif) [string_m_3.7-01-09.zip](attachments/87151999/88025720.zip) (application/zip)  
![](images/icons/bullet_blue.gif) [string_m_3.2-17-09.zip](attachments/87151999/88025721.zip) (application/zip)  
![](images/icons/bullet_blue.gif) [sss-managed-string-coursepdf.pdf](attachments/87151999/88025722.pdf) (application/pdf)  
![](images/icons/bullet_blue.gif) [string_m_3.8-2-07.tar](attachments/87151999/88025723.tar) (application/x-tar)  
![](images/icons/bullet_blue.gif) [string_m_3.9-11-08.tar](attachments/87151999/88025724.tar) (application/x-tar)  
