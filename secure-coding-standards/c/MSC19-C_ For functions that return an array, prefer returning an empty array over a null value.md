Many functions have the option of returning a pointer to an object or returning `NULL` if a valid pointer cannot be produced. Some functions return arrays, which appear like a pointer to an object. However, if a function has the option of returning an array or indicating that a valid array is not possible, it should not return `NULL`. Instead, the function should return an empty array. Often, code that calls a function that returns an array intends merely to iterate over the array elements. In this case, the calling code need not change—iterating over the elements works correctly even if the returned array is empty, so the calling code need not check the return value for `NULL`.
This situation is complicated by the fact that C does not keep track of the length of an array. However, two popular methods have emerged to emulate this behavior. The first is to wrap the array in a struct with an integer storing the length. The second is to place a sentinel value at the end of the data in the array. This second approach is most commonly manifested in null-terminated byte strings (NTBSs).
## Noncompliant Code Example (Struct)
In this noncompliant code example, an inventory system keeps track of the total number of different items (denoted `length`). Each item is given an index in the array, and the value for that index is the stock of that item. Adding a new item increases `length` in the struct. Stocking more of an item increases the value for that item's index. For example, if 5 books and 2 erasers are in stock, the inventory would be `stockOfItem[0] = 5` and `stockOfItem[1] = 2`, assuming books are index 0 and erasers are index 1.
The problem arises in this setup when no items are being stocked. `getStock` would recognize that `length = 0` and would return `NULL`. In this noncompliant code example, erroneous behavior results from `getStock` returning `NULL` while `main` neglects to check for such a value. It results in an [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) after returning to the `main` function.
``` c
#include <stdio.h>
enum { INV_SIZE=20 };
typedef struct {
  size_t stockOfItem[INV_SIZE];
  size_t length;
} Inventory;
size_t *getStock(Inventory iv);
int main(void) {
  Inventory iv;
  size_t *item;
  iv.length = 0;
  /*
   * Other code that might modify the inventory but still
   * leave no items in it upon completion.
   */
  item = getStock(iv);
  printf("Stock of first item in inventory: %zd\n", item[0]);
  return 0;
}
size_t *getStock(Inventory iv) {
  if (iv.length == 0) {
    return NULL;
  }
  else {
    return iv.stockOfItem;
  }
}
```
## Compliant Solution
This compliant solution eliminates the `NULL` return and returns the `item` array, even if it is zero-length. The main function can effectively handle this situation without exhibiting erroneous behavior. Since the array lives on the stack, it must prevent returning a value in the stack frame (as mandated by [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations)). So the getStack() function also takes a pointer to `Inventory`, so that it can return a pointer to its contents safely.
``` c
#include <stdio.h>
enum { INV_SIZE=20 };
typedef struct {
  size_t stockOfItem[INV_SIZE];
  size_t length;
} Inventory;
size_t *getStock(Inventory* iv);
int main(void) {
  Inventory iv;
  size_t *item;
  iv.length = 0;
  /*
   * Other code that might modify the inventory but still
   * leave no items in it upon completion.
   */
  item = getStock(&iv);
  if (iv.length != 0) {
    printf("Stock of first item in inventory: %zd\n", item[0]);
  }
  return 0;
}
size_t *getStock(Inventory* iv) {
  return iv->stockOfItem;
}
```
## Noncompliant Code Example (Sentinel Value)
This noncompliant code example implements an inventory system similar to the one described previously. However, instead of storing the length of the array in a struct, a sentinel value of `FINAL_ITEM` is used. The value for the index following the last item is set as `FINAL_ITEM`. It is assumed that out-of-stock items (assigned value 0) are removed from the array, and the contents of later items are shifted to lower indexes.
The following code attempts to return an array of the items in stock, sorted by the amount of each item in stock. The `arraySort` function incorrectly returns `NULL` instead of a pointer to an empty array when no items are in stock. The null return is improperly handled by the `main` function, which is attempting to print out the returned array, and an [abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) results.
``` c
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
enum { FINAL_ITEM=SIZE_MAX, INV_SIZE=20 };
size_t *arraySort(size_t *array);
int main(void) {
  size_t i;
  size_t stockOfItem[INV_SIZE];
  size_t *sortedArray;
  /* Other code that might use stockarray but leaves it empty */
  sortedArray = arraySort(stockOfItem);
  for (i = 0; sortedArray[i] != FINAL_ITEM; i++) {
    printf("Item stock: %zd", sortedArray[i]);
  }
  return 0;
}
/* Create new sorted array */
size_t *arraySort(size_t *array) {
  size_t i;
  size_t *sortedArray;
  for(i = 0; array[i] != FINAL_ITEM; i++);
  if (i == 0) {
    return NULL;
  }
  sortedArray = (size_t*) malloc(sizeof(size_t)*i);
  if (sortedArray == NULL) {
    /* Handle memory error */
  }
  /* Add sorted data to array */
  return sortedArray;
}
```
## Compliant Solution (Sentinel Value)
This compliant solution correctly returns an empty array in the `sortedArray` function. If the size of the array is 0, then `sortedArray` allocates an array of size 1 and fills it with the sentinel value. It can then successfully return that array to the caller function.
``` c
#include <stdio.h>
#include <stdint.h>
#include <malloc.h>
enum { FINAL_ITEM=SIZE_MAX, INV_SIZE=20 };
size_t *arraySort(size_t *array);
int main(void) {
  size_t i;
  size_t stockOfItem[INV_SIZE];
  size_t *sortedArray;
  /* Other code that might use stockarray but leaves it empty */
  sortedArray = arraySort(stockOfItem);
  for (i = 0; sortedArray[i] != FINAL_ITEM; i++) {
    printf("Item stock: %zd", sortedArray[i]);
  }
  return 0;
}
/* Create new sorted array */
size_t *arraySort(size_t *array) {
  size_t i;
  size_t *sortedArray;
  for(i = 0; array[i] != FINAL_ITEM; i++);
  if (i == 0) {
    size_t *emptyArray = (size_t*) malloc(sizeof(size_t));
    if(emptyArray == NULL) {
      /* Handle memory error */
    }
    emptyArray[0] = FINAL_ITEM;
    return emptyArray;
  }
  sortedArray = (size_t*) malloc(sizeof(size_t)*i);
  if (sortedArray == NULL) {
    /* Handle memory error */
  }
  /* Add sorted data to array */
  return sortedArray;
 }
```
## Risk Assessment
Returning `NULL` rather than a zero-length array can lead to [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) when the client code does not handle `NULL` properly. [Abnormal program termination](BB.-Definitions_87152273.html#BB.Definitions-abnormaltermination) can result when the calling function performs operations on `NULL`.

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MSC19-C | Low | Unlikely | High | P1 | L3 |

### Automated Detection

| Tool | Version | Checker | Description |
| ----|----|----|----|
| Parasoft C/C++test | 2024.2 | CERT_C-MSC19-aCERT_C-MSC19-b | Avoid accessing arrays out of boundsAvoid null pointer dereferencing |
| PC-lint Plus | 1.4 | 413, 418, 419, 420, 473,613, 661, 662, 668, 669,
670 | Partially supported |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this guideline on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MSC19-C).
## Bibliography

|  |  |
| ----|----|
| [Bloch 2008] | Item 43, "Return Empty Arrays or Collections, Not Nulls" |

------------------------------------------------------------------------
[](../c/MSC18-C_%20Be%20careful%20while%20handling%20sensitive%20data,%20such%20as%20passwords,%20in%20program%20code) [](../c/Rec_%2048_%20Miscellaneous%20_MSC_) [](https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152333)
## Comments:

|  |
| ----|
| This is a good rule to work on, Glen. I'll comment on the rule after you've 'converted' it from Java to C.
                                        Posted by svoboda at Mar 29, 2009 10:58
                                     |
| Glenn, good rule so far. One style comment:
    Follow my styleguide announcement from last week (add this rule to Misc page)
and one comment wrt content:
    The NCCE and CCE both use magic numbers, vhich violates DCL06-C. Use meaningful symbolic constants to represent literal values...please fix this. (This may have other ramifications since you already have a 'length' item in your struct...maybe just make it static.)
                                        Posted by svoboda at Mar 30, 2009 08:19
                                     |
| Replaced magic number with a macro. Is that okay? I also added it to all the appropriate locations and updated the links of the surrounding guidelines/rules. 
                                        Posted by gstroz at Mar 31, 2009 00:25
                                     |
| You fixed the technical aspects of the code, but overlooked the semantic aspects. If the array length is defined by a macro, what is the length specifier for?
Upon further thought, I realized the rule makes more sense for Java than it does C, becase Java arrays 'know' their own length, C arrays don't. You can still make this a valid rule by having an array that indicates its length somehow. The two most popular ways to do tis is:
    Wrap the array in a struct that provides its length
    Place a sentinal value at the end (eg the C null-terminated byte string)
I suggest you provide examples of both cases. Your curent NCCE/CS pair are close to demonstrating the first case. And your rule needs to point out this only aplies when the function can indicate the array's length somehow.
                                        Posted by svoboda at Mar 31, 2009 14:50
                                     |
| Try using an enumeration constant instead of a define.  See DCL06-C. Use meaningful symbolic constants to represent literal values for an explanation.
                                        Posted by rcs at Mar 31, 2009 17:51
                                     |
| I decided to drop this rule in favor of making MEM13-C. I'll leave this up as progress in case someone else wants to finish it. Labeled it as incomplete.
Edit: Gah, MEM13-C is invalid so back to fixing this 
                                        Posted by gstroz at Apr 01, 2009 22:41
                                     |
| 
    The 1st NCCE has the right idea but the text is garbled, and the code is confusing (shouldn't getStock return a size_t? This bug also occurs in the first CS)
    The 2nd NCCE code is confusing, and needs to contain a comment indicating that the array is terminated by a -1. The intro text should explain this too. And the CS background color is wrong.
    Finally the reference text is good, but the link is invalid.
                                        Posted by svoboda at Apr 04, 2009 08:01
                                     |
| How would fixing these minor errors affect my grade?
                                        Posted by gstroz at Apr 04, 2009 17:16
                                     |
| I can improve your grade by 2 points if you turn this into a complete rule before Monday.
                                        Posted by svoboda at Apr 05, 2009 10:17
                                     |
| I'll give you 1 point for the work you did yesterday. The rule still needs work, but the assignment is over, so this list is for future work:
    The 1st NCCE is still garbled, mainly because NULL is not a proper size_t element.
    Now that I think about it, this rule belongs in the Arrays section.
    The 'sentinel value' should reference C null-terminated byte strings, since that is their approach.
    Also 2nd CS should should use an enum value to store -1, instead of using a 'magic number'.
                                        Posted by svoboda at Apr 06, 2009 11:28
                                     |
| we received a comment to the japanese version that NCCE(sentinel) and CCE(sentinel) can't be compiled.just fixed.one thing to note, I don't understand the intention of "static" declaration, so, replaced with just size_t (without static qualifier).
                                        Posted by yozo at Feb 13, 2013 22:53
                                     |
| The first sentence is difficult for me to understand (and translate to japanese).There are situations in which a function may return an array;on the basis of its length.How can we re-phrase this?"There are situations in which a function may return an array, whose length varies depending on the argument.""There are situations in which a function is expected to return an array of varying length, depending on its argument.""There are situations in which a function should return an array, whose length varies depending on the argument."etc...
                                        Posted by yozo at Feb 13, 2013 23:08
                                     |
| I've rewritten the intro; hopefully it's clearer now.
                                        Posted by svoboda at Feb 18, 2013 11:32
                                     |
| thanks, David!;
                                        Posted by yozo at Feb 18, 2013 22:02
                                     |
| An array without a;FINAL_ITEM value can be catastrophic. It may violate MSC21-C. Use robust loop termination conditions.
                                        Posted by svoboda at Dec 16, 2013 16:42
                                     |
| The first two examples ("Noncompliant Code Example (Struct)" and "Compliant Solution") violate two rules. When compiling using GCC with -Wall, I get the corresponding warnings:printf("Stock of first item in inventory: %d\n", item[0]);

format '%d' expects argument of type 'int', but argument 2 has type 'size_t {aka long long unsigned int}'
See [FIO47-C. Use valid format strings](FIO47-C_%20Use%20valid%20format%20strings)
    size_t *getStock(Inventory iv) {
     return iv.stockOfItem;
    }
function returns address of local variable
See [DCL30-C. Declare objects with appropriate storage durations](DCL30-C_%20Declare%20objects%20with%20appropriate%20storage%20durations)
![](images/icons/contenttypes/comment_16.png) Posted by arnaud.jakob at May 09, 2019 11:29
\| \|
I fixed the first problem by using the format string %zd, which corresponds to size_t.
And I fixed the cond problem by having;`getStock()` take a pointer to `Inventory`, eliminating the DCL30-C violation.
![](images/icons/contenttypes/comment_16.png) Posted by svoboda at May 23, 2019 15:54
\| \|
Thanks for the correction!
![](images/icons/contenttypes/comment_16.png) Posted by arnaud.jakob at May 27, 2019 03:41
\|
