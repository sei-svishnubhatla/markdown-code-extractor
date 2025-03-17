The C99 standard introduced flexible array members into the language. Although flexible array members are a useful addition, they should be properly understood and used with care. In particular, structures with flexible array members should always be accessed with a pointer and not declared directly.
Flexible array members are defined in subclause 6.7.2.1, paragraph 16, of the C99 standard \[[ISO/IEC 9899:1999](AA.-Bibliography_87152170.html#AA.Bibliography-ISO-IEC9899-1999)\] as follows:
> As a special case, the last element of a structure with more than one named member may have an incomplete array type; this is called a flexible array member. In most situations, the flexible array member is ignored. In particular, the size of the structure is as if the flexible array member were omitted except that it may have more trailing padding than the omission would imply. However, when a . (or -\>) operator has a left operand that is (a pointer to) a structure with a flexible array member and the right operand names that member, it behaves as if that member were replaced with the longest array (with the same element type) that would not make the structure larger than the object being accessed; the offset of the array shall remain that of the flexible array member, even if this would differ from that of the replacement array. If this array would have no elements, it behaves as if it had one element but the behavior is undefined if any attempt is made to access that element or to generate a pointer one past it.

The following is an example of a structure that contains a flexible array member:
``` java
struct flexArrayStruct {
  int num;
  int data[];
};
```
This definition means that, when allocating storage space, only the first member, `num`, is considered. Consequently, the result of accessing the member `data` of a variable of type `struct flexArrayStruct` is undefined. To avoid the potential for [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior), structures that contain a flexible array member should always be accessed with a pointer, as shown in the following code example:
``` java
struct flexArrayStruct *structP;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Space is allocated for the struct */
structP = (struct flexArrayStruct *)
   malloc(sizeof(struct flexArrayStruct) + sizeof(int) * array_size);
if (structP == NULL) {
  /* Handle malloc failure */
}
structP->num = 0;
/*
 * Access data[] as if it had been allocated
 * as data[array_size].
 */
for (i = 0; i < array_size; i++) {
  structP->data[i] = 1;
}
```
Before the introduction of flexible array members in the C99 standard, structures with a one-element array as the final member were used to achieve similar functionality. The following code example illustrates how `struct flexArrayStruct` is declared in this case:
``` java
struct flexArrayStruct {
  int num;
  int data[1];
};
```
The approach to acquiring memory in this case is similar to the C99 approach with the exception that 1 is subtracted from `array_size` to account for the element present in the structure definition. The problem with using this approach is that the behavior is undefined when accessing other than the first element of data (see subclause 6.5.6, paragraph 8, of the C99 standard). Consequently, the compiler can generate code that does not return the expected value when accessing the second element of data.  Structures with flexible array members can be used to produce code with defined behavior. However, some restrictions apply:
1.  The incomplete array type *must* be the last element within the structure.
2.  There cannot be an array of structures that contain flexible array members.
3.  A structure that contains a flexible array member cannot be used as a member in the middle of another structure.
## Noncompliant Code Example (Use Flexible Array Members)
When using C99-compliant compilers, the one-element array hack described previously should not be used. In this noncompliant code, just such an array is used where a flexible array member should be used instead:
``` java
struct flexArrayStruct {
  int num;
  int data[1];
};
/* ... */
struct flexArrayStruct *flexStruct;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Dynamically allocate memory for the structure */
flexStruct = (struct flexArrayStruct *)
   malloc(sizeof(struct flexArrayStruct) + sizeof(int) * (array_size - 1));
if (flexStruct == NULL) {
  /* Handle malloc failure */
}
/* Initialize structure */
flexStruct->num = 0;
for (i = 0; i < array_size; i++) {
  flexStruct->data[i] = 0;
}
```
As described, the problem with this code is that, strictly speaking, the only member that is guaranteed to be valid is `flexStruct{{->data[0]}}`. Unfortunately, when using compilers that do not support the C99 standard in full, or at all, this approach may be the only solution. Microsoft Visual Studio 2005, for example, does not implement the C99 syntax.
## Compliant Solution (Use Flexible Array Members)
Fortunately, when working with C99-compliant compilers, the solution is simple: remove the 1 from the array declaration and adjust the size passed to the `malloc()` call accordingly. In other words, use flexible array members:
``` java
struct flexArrayStruct {
  int num;
  int data[];
};
/* ... */
struct flexArrayStruct *flexStruct;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Dynamically allocate memory for the structure */
flexStruct = (struct flexArrayStruct *)
   malloc(sizeof(struct flexArrayStruct) + sizeof(int) * array_size);
if (flexStruct == NULL) {
  /* Handle malloc failure */
}
/* Initialize structure */
flexStruct->num = 0;
for (i = 0; i < array_size; i++) {
  flexStruct->data[i] = 0;
}
```
In this case, the structure will be treated as if the member `data[]` had been declared to be `data[array_size]`.
## Noncompliant Code Example (Declaration)
When using structures with a flexible array member, you should never directly declare an instance of the structure. In this noncompliant code, a variable of type `struct flexArrayStruct` is declared:
``` java
struct flexArrayStruct flexStruct;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Initialize structure */
flexStruct.num = 0;
for (i = 0; i < array_size; i++) {
  flexStruct.data[i] = 0;
}
```
The problem with this code is that the `flexArrayStruct` does not actually reserve space for the integer array data—it can't because the size is not specified. Consequently, while initializing the `num` member to 0 is allowed, attempting to write even one value into data (that is, `data[0]`) will likely overwrite memory not owned by the structure.
## Compliant Solution (Declaration)
The solution is to always declare pointers to structures containing a flexible array member and dynamically allocate memory for them, as the following code snippet illustrates:
``` java
struct flexArrayStruct *flexStruct;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Dynamically allocate memory for the structure */
flexStruct = (struct flexArrayStruct *)
   malloc(sizeof(struct flexArrayStruct) + sizeof(int) * array_size);
if (flexStruct == NULL) {
  /* Handle malloc failure */
}
/* Initialize structure */
flexStruct->num = 0;
for (i = 0; i < array_size; i++) {
  flexStruct->data[i] = 0;
}
```
This code resolves the issue by declaring a pointer to `flexArrayStruct` and then dynamically allocating memory for the pointer to point to. In this case, it is acceptable to access the elements of the `data[]` member. as described in C99, subclause 6.7.2.1, paragraph 16.
## Noncompliant Code Example (Copying)
When using structures with a flexible array member, you should never directly copy an instance of the structure. This noncompliant code attempts to replicate a copy of `struct flexArrayStruct`:
``` java
struct flexArrayStruct *flexStructA;
struct flexArrayStruct *flexStructB;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Allocate memory for flexStructA */
/* Allocate memory for flexStructB */
/* Initialize flexStructA */
/* ... */
*flexStructB = *flexStructA;
```
The problem with this code is that when the structure is copied, the size of the flexible array member is not considered, and only the first member of the structure, `num`, is copied.
## Compliant Solution (Copying)
This compliant solution uses `memcpy()` to properly copy the content of `flexStructA` into `flexStructB`.
``` java
struct flexArrayStruct *flexStructA;
struct flexArrayStruct *flexStructB;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Allocate memory for flexStructA */
/* Allocate memory for flexStructB */
/* Initialize flexStructA */
/* ... */
memcpy(flexStructB, flexStructA, (sizeof(struct flexArrayStruct) + sizeof(int) * array_size));
```
In this case, the copy is explicit, and the flexible array member is accounted for and copied as well.
## Noncompliant Code Example (Reference)
When using structures with a flexible array member, you should never directly pass an instance of the structure in a function call. In this noncompliant code, the flexible array structure is passed directly to a function, which tries to print the array elements:
``` java
void print_array(struct flexArrayStruct structP) {
  size_t i;
  printf("Array is: ");
  for (i = 0; i < structP.num; i++) {
    printf("%d", structP.data[i]);
  }
  printf("\n");
}
struct flexArrayStruct *structP;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Space is allocated for the struct */
structP = (struct flexArrayStruct *)
     malloc(sizeof(struct flexArrayStruct) + sizeof(int) * array_size);
if (structP == NULL) {
  /* Handle malloc failure */
}
structP->num = array_size;
for (i = 0; i < array_size; i++) {
  structP->data[i] = i;
}
print_array(*structP);
```
The problem with this code is that passing the structure directly to the function actually makes a copy of the structure. This copy fails for the same reason that the previous copy example failed.
## Compliant Solution (Reference)
Never allow a structure with a flexible array member to be passed directly in a function call. The noncompliant code can be fixed by changing the function to accept a pointer to the structure:
``` java
void print_array(struct flexArrayStruct *structP) {
  size_t i;
  printf("Array is: ");
  for (i = 0; i < structP->num; i++) {
    printf("%d", structP->data[i]);
  }
  printf("\n");
}
struct flexArrayStruct *structP;
size_t array_size;
size_t i;
/* Initialize array_size */
/* Space is allocated for the struct */
structP = (struct flexArrayStruct *)
     malloc(sizeof(struct flexArrayStruct) + sizeof(int) * array_size);
if (structP == NULL) {
  /* Handle malloc failure */
}
structP->num = array_size;
for (i = 0; i < array_size; i++) {
  structP->data[i] = i;
}
print_array(structP);
```
## Risk Assessment
Failure to use structures with flexible array members correctly can result in [undefined behavior](BB.-Definitions_87152273.html#BB.Definitions-undefinedbehavior).

| Rule | Severity | Likelihood | Remediation Cost | Priority | Level |
| ----|----|----|----|----|----|
| MEMxx-C | Low | Unlikely | Low | P3 | L3 |

### Automated Detection

|  |  |
| ----|----|
| Compass/ROSE | Compass/ROSE can detect some violations of this rule.; In particular, it warns if the last element of a struct is an array with a small index (0 or 1). |

### Related Vulnerabilities
Search for [vulnerabilities](BB.-Definitions_87152273.html#BB.Definitions-vulnerability) resulting from the violation of this rule on the [CERT website](https://www.kb.cert.org/vulnotes/bymetric?searchview&query=FIELD+KEYWORDS+contains+MEMxx-C).
## References

|  |  |
| ----|----|
| [ISO/IEC 9899:1999] | Subclause 6.7.2.1, "Structure and Union Specifiers" |
| [Feather 1997] | ; |

------------------------------------------------------------------------
[](void%20MEM32-C_%20Detect%20and%20handle%20memory%20allocation%20errors)      [](Rule%2008_%20Memory%20Management%20_MEM_)      [](MEM34-C_%20Only%20free%20memory%20allocated%20dynamically)
## Comments:

|  |
| ----|
| This is being developed as a replacement for MEM33-C. Use the correct syntax for flexible array members, right?
If so, we should delete all the text in the old rule and replace with this new text so that we can preserve the history.
                                        Posted by rcs_mgr at Nov 07, 2009 08:10
                                     |
| 
    I would change the title to something like "Understand how flexible array members are to be used".
    The example code (before NCCE/CS pairs) should be blue, since it represents the Right Thing to do.
    Each NCCE/CS code sample doesn't have to re-declare flexArrayStruct, since the definition is the same throughout the rule.
    I would also include the 1st NCCE/CS pair from the original MEM33-C and incorporate it here. Adding an index to the flexible array decl is an easy mistake to make (since it is the Old Way to do things).
Modulo those comments, I think this rule is a better version of MEM33-C and should replace it. The introduction is clearer and the code samples are more illustrative. When you replace MEM33-C, you should just cut'n paste your text over the original text, b/c we should preserve the original comments from MEM33-C.
                                        Posted by svoboda at Nov 07, 2009 13:03
                                     |
| Agreed / understood.; The rationale for starting a seperate page is ensure the new text is of reasonable quality before replacing the old text.  When this is "release ready" I will copy & paste this text over the old as you describe.
                                        Posted by bbabcock at Nov 11, 2009 03:07
                                     |
| What is the status of this rule?; Has this merge happened already or not?
                                        Posted by rcs_mgr at May 24, 2012 10:34
                                     |
| I believe this was "merged" once with MEM33-C circa version 46.; (MEM33-C was updated / replaced with the text of this rule in version 46.)  However, the merge was apparently reverted for reasons unknown to me in version 49...
                                        Posted by bbabcock at May 27, 2012 07:35
                                     |

