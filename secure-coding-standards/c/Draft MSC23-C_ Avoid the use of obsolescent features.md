The C standard defines certain features of the language to be obsolescent \[[ISO/IEC 9899:2011](AA.-Bibliography_87152170.html#AA.Bibliography-ISO/IEC9899-2011)\]:
> Certain features are obsolescent, which means that they may be considered for withdrawal in future revisions of this International Standard. They are retained because of their widespread use, but their use in new implementations (for implementation features) or new programs (for language \[6.11\] or library features \[7.31\]) is discouraged.

Avoid the use of obsolescent features in your program.
# Linkages of identifiers
Declaring an identifier with internal linkage at file scope without the static storage class specifier is an obsolescent feature \[C11 §6.11.2\]
# External names
Restriction of the significance of an external name to fewer than 255 characters considering each universal character name or extended source character as a single character) is an obsolescent feature that is a concession to existing implementations.  You can ignore this limitation, provided that it is know that your current implementations support longer names \[C11 §6.11.3\].
# Storage-class specifiers
The placement of a storage-class specifier other than at the beginning of the declaration specifiers in a declaration is an obsolescent feature \[C11 §6.11.5\].
# Function declarators
The use of function declarators with empty parentheses (not prototype-format parameter type declarators) is an obsolescent feature \[C11 §6.11.6\].
# Function definitions
The use of function definitions with separate parameter identifier and declaration lists (not prototype-format parameter type and identifier declarators) is an obsolescent feature \[C11 §6.11.7\].
# Boolean type and values `<stdbool.h>`
The ability to undefine and perhaps then redefine the macros `bool`, `true`, and `false` is an obsolescent feature \[C11 §7.31.9 \].
# Input/output `<stdio.h>`
The use of `ungetc()` on a binary stream where the file position indicator is zero prior to the call is an obsolescent feature \[C11 §7.31.11 \].
# General utilities `<stdlib.h>`
Invoking realloc() with a size argument equal to zero is an obsolescent feature \[C11 §7.31.12 \].
