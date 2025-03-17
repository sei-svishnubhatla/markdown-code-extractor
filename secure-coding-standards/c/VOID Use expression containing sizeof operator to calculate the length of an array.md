> [!info]  
>
> This guideline has been labeled [void](https://wiki.sei.cmu.edu//confluence/label/seccode/void) and designated for future elimination from the C Secure Coding Practices: See the recommendation [EXP09-C. Use sizeof to determine the size of a type or variable](EXP09-C_%20Use%20sizeof%20to%20determine%20the%20size%20of%20a%20type%20or%20variable) for a related practice. It has not been erased yet in case it contains information that might still be useful.

The length of an array should be calculated from the following expression: `sizeof(array_name)/sizeof(*array_name)`, where array_name is the name of the array. This expression can be used irrespective of the datatype of an array or size of an array.
## Noncompliant Code Example
In this noncompliant code example, the length of the wide character array "array_name" is calculated by sizeof(array_name). The expression sizeof(array_name) will give the size of the entire array, and not the length of the wide character array.
``` java
/* Trying to convert a wide character array into single byte character array */
char *conversion_func(wchar_t *array, rsize_t size) {
      char *char_array;
      char_array = malloc(sizeof(char) * size);
      if (char_array == NULL) {
         /* Handle error */
      }
      /* Copy each character from wide character to single byte character array,
       * considering the size of wide character is more than one byte
       */
      ......
}
int main() {
     wchar_t wchar_array[10];
     char *c;
     /* Initialize the array */
     c = conversion_func(wchar_array, sizeof(wchar_array));
     .....
}
```
For this example, the argument sizeof(wchar_array) will return the number of bytes in wchar_t, which will result in overallocation of buffer for character array in the conversion function.
## Compliant Solution
The expression sizeof(wchar_array)/sizeof(\*wchar_array) will give the correct length of the array.
``` java
/* Trying to convert a wide character array into single byte character array */
char *conversion_func(wchar_t *array, rsize_t size) {
      char *char_array;
      char_array = malloc(sizeof(char) * size);
      if (char_array == NULL) {
         /* Handle error */
      }
      /* Copy each character from wide character to single byte character array,
       * considering the size of wide character is more than one byte
       */
      ......
}
int main() {
     wchar_t wchar_array[10];
     char *c;
     /* Initialize the array */
     c = conversion_func(wchar_array, (sizeof(wchar_array)/sizeof(*wchar_array)));
     .....
}
```
## Exceptions
**STR11-EX1** Only for single-byte character arrays, sizeof(array_name) can result in correct length of single byte character, as size of each element in array is 1.
## Risk Assessment
Improper use of macros may result in undefined behavior.

|  Recommendation  |  Severity  |  Likelihood  |  Remediation Cost  |  Priority  |  Level  |
| ----|----|----|----|----|----|
|  STR11-C  |  medium  |  UNLIKELY  |  medium  |  P4  |  L3  |

## Bibliography
**TODO**
------------------------------------------------------------------------
[](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Understand+the+caveats+of+floating+point+exceptions?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/99.+The+Void?showChildren=false&showComments=false) [](https://www.securecoding.cert.org/confluence/display/seccode/VOID+Use+variables+of+type+size_t+for+size+parameters+to+memory+allocation+routines?showChildren=false&showComments=false)
## Comments:

|  |
| ----|
| Risk Assessment section should be corrected 
                                        Posted by masaki at Nov 12, 2010 05:48
                                     |

