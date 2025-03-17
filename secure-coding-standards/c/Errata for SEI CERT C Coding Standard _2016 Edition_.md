This list of errata lists errors identified since the release of the PDF document entitled [SEI CERT C Coding Standard: Rules for Developing Safe, Reliable, and Secure Systems (2016 Edition)](http://www.cert.org/secure-coding/products-services/secure-coding-download.cfm). These corrections were made to the [SEI CERT C Coding Standard wiki](SEI%20CERT%20C%20Coding%20Standard), which is the most current source for this standards information. The focus of the correction is highlighted in red below in the Before and After columns.  This page does not include additions since this standard was published, if the addition doesn't actually correct a defect that was in the publication.

|  |  |  |  |
| ----|----|----|----|
| Location | Before (with error) | After (with correction) | Rationale |
| p 9, Section 1.6 | Taint and Tainted Sources | Material from this section was contributed to;ISO/IEC TS 17961:2013.Taint and Tainted Sources | Added citation for TS 17961 because it has similar content. |
| p. 21, Section 1.16 | ...Brendan Saulsbury,Robert C. Seacord... | ...Brendan Saulsbury, Roger Scott, Robert C. Seacord... |  |
| p. 30, Section 2.3.1 | ); | } | The last line of the Noncompliant Code Example in section 2.3.1 closes the code block incorrectly with a close-parent-semicolin ");", but should be a closed brace "}". |
| p. 43, Section 3.4.1 | Noncompliant Code Example (Header Guard)A common, but noncompliant, practice is to choose a reserved name for a macro used in a prepro-
cessor conditional guarding against multiple inclusions of a header file. (See also PRE06-C. En-
close header files in an inclusion guard.) | Noncompliant Code Example (Include Guard)A common, but noncompliant, practice is to choose a reserved name for a macro used in a prepro-
cessor conditional guarding against multiple inclusions of a header file. (See also PRE06-C. En-
close header files in an include guard.) | Standardized the term to be "include guard". |
| p 44, Section 3.4.2 | Compliant Solution (Header Guard)This compliant solution avoids using leading underscores in the name of the header guard: | Compliant Solution (Include Guard)This compliant solution avoids using leading underscores in the name of the include guard: | Standardized the term to be "include guard". |
| p 54, Section 3.6.2 | However, compilers are free to implement arg.b = 2 by setting the low byte of a 32-bit registerto 2 , leaving the high bytes unchanged and storing all 32 bits of the register into memory. This
implementation could leak the high-order bytes resident in the register to a user. | However, a conforming compiler is free to implement;arg.b = 2 by setting the low-order bits of a register to 2, leaving the high-order bits unchanged and containing sensitive information. Then the platform copies all register bits into memory, leaving sensitive information in the padding bits. Consequently, this implementation could leak the high-order bits from the register to a user. | A more precise clarification |
| p 55, Section 3.6.3 | memcpy(buf + offset, &arg.c, sizeof(arg.c));offset += sizeof(arg.c); | ; memcpy(buf + offset, &arg.c, sizeof(arg.c));
  offset += sizeof(arg.c);
  /* Set all remaining bytes to zero */
  memset(buf + offset, 0, sizeof(arg) - offset); | Zero out any remaining bytes in array to be copied. Use "buf" not "buff". |
| p 56, Section 3.6.5 | GCC allows specifying declaration attributes using the keyword;__attribute__((__packed__)). When this attribute is present, the compiler will not add padding bytes for memory alignment unless otherwise required by the _Alignas alignment specifier ... | GCC allows specifying declaration attributes using the keyword;__attribute__((__packed__)). When this attribute is present, the compiler will not add padding bytes for memory alignment unless an explicit alignment specifier for a structure member requires the introduction of padding bytes. | Clarification that alignment requirements trump GCC packing attribute. |
| p 57, Section 3.6.7 | However, compilers are free to implement the initialization of arg.a and arg.b by setting thelow byte of a 32-bit register to the value specified, leaving the high bytes unchanged and storing
all 32 bits of the register into memory. This implementation could leak the high-order bytes resi-
dent in the register to a user. |  | Paragraph was spurious and did not apply to code example, so it was removed. |
| p. 72, Section 4.1.8 | MISRA C:2012 Rule 12.1 (advisory) | MISRA C:2012 Rule 13.2 (required) | CERT cross-reference in MISRA C:2012 – Addendum 3 |
| p. 88, Section 4.4.6 | static unsigned int tun_chr_poll(struct file *file, poll_table*wait) {
struct tun_file *tfile = file->private_data;
struct tun_struct *tun = __tun_get(tfile);
struct sock *sk;
unsigned int mask = 0;
if (!tun)
return POLLERR;
sk = tun->sk;
/* T | static;unsigned int tun_chr_poll(struct file *file, poll_table *wait)  {
  assert(file);
  struct tun_file *tfile = file->private_data;
  struct tun_struct *tun = __tun_get(tfile);
  struct sock *sk;
  unsigned int mask = 0;
  if (!tun)
    return POLLERR;
  assert(tun->dev);
  sk = tun->sk;
  assert(sk);
  assert(sk->socket);
  /* The remaining code is omitted because it is unchanged... */
} | Added assert statements to specify pointers that are expected not to be null. |
| p. 95, Section 4.6.7 | On such an architecture, improper pointer alignment is permitted but remains an efficiency problem. | On such an architecture, improper pointer alignment is permitted but remains an efficiency problem.The x86 32- and 64-bit architectures......but they must also ensure that their compiler, along with its optimizer, also respect these guarantees. | Added counterexample and warning to EXP36-C-EX1. (See EXP36-C for full text.) |
| p 105, Section 4.8.5 | ; if (wp->j == 12) {
    /* ... */
  }
} | ; if (wp->j == 12) {
    /* ... */
  }
  /* ... */
  free(wp);
} | Perform proper memory cleanup |
| p 106, Section 4.8.6 | ; if (wp->j == 12) {
    /* ... */
  }
} | ; if (wp->j == 12) {
    /* ... */
  }
  /* ... */
  free(wp);
} | Perform proper memory cleanup |
| p. 111, Section 4.10.1 | if (0 == memcmp(left, right, sizeof(struct s))) { | if ((left && right) &&    (0 == memcmp(left, right, sizeof(struct s)))) { | Added checks to both arguments to avoid possible null dereferences. |
| p. 112, Section 4.10.3 | if (0 == memcmp(left, right, sizeof(struct s))) { | if ((left && right) &&    (0 == memcmp(left, right, sizeof(struct s)))) { | Added checks to both arguments to avoid possible null dereferences. |
| p. 120, Section 4.11.4.2 | float x | float x; | Added semicolon for syntactic correctness. |
| p 125, Section 4.12.8 | printf("%zu, %d\n, align, val); | printf("%zu, %d\n", align, val); | Added quote for syntactic correctness. |
| p. 126, Section 4.13 | 4.13.1Noncompliant Code Example | Performing assignment statements in other contexts do not violate this rule. However, they may violate other rules, such as;EXP30-C. Do not depend on the order of evaluation for side effects.4.13.1
Noncompliant Code Example | Added a reference to related rule EXP30-C to this rule's introduction. |
| p. 128, Section 4.13.9 | while (ch = '\t' && ch == ' ' && ch == '\n') { | while (ch = '\t' || ch == ' ' || ch == '\n') { | Use || to test if a char has one of several values, rather than &&. |
| p. 128, Section 4.13.10 (Noncompliant code) | while ('\t' = ch && ' ' == ch && '\n' == ch) { | while ('\t' = ch || ' ' == ch || '\n' == ch) { | Use || to test if a char has one of several values, rather than &&. |
| p. 128, Section 4.13.10 (Compliant code) | while ('\t' == ch && ' ' == ch && '\n' == ch) { | while ('\t' == ch || ' ' == ch || '\n' == ch) { | Use || to test if a char has one of several values, rather than &&. |
| p.138, Section 4.15 | Previous section is 4.14, rule EXP46-C | New rule EXP47-C. (See wiki for contents) | New rule deemed necessary (vulnerability not covered by pre-existing rule). |
| p. 150, Section 5.3.5.2 | This compliant solution eliminates signed overflow on systems where  long is at least twice the precision of;int: | This compliant solution eliminates signed overflow on systems where 
            long long
           is at least twice the precision of int: | The phrase should be “long long” not “long.” |
| p. 186 Section 6.3.2 | if (PRECISION(INT_MAX) < log2f(fabsf(f_a)) ||(f_a != 0.0F && fabsf(f_a) < FLT_MIN)) {
/* Handle error */ | ; if (isnan(f_a) ||
      PRECISION(INT_MAX) < log2f(fabsf(f_a)) ||
      (f_a != 0.0F && fabsf(f_a) < FLT_MIN)) {
    /* Handle error */ | Code now safely handles NaN. |
| p. 187 Section 6.3.4 | if (isgreater(fabs(d_a), FLT_MAX) ||isless(fabs(d_a), FLT_MIN)) {
/* Handle error */
} else {
f_a = (float)d_a;
}
if (isgreater(fabsl(big_d), FLT_MAX) ||
isless(fabsl(big_d), FLT_MIN)) {
/* Handle error */
} else {
f_b = (float)big_d;
}
if (isgreater(fabsl(big_d), DBL_MAX) ||
isless(fabsl(big_d), DBL_MIN)) {
/* Handle error */ | if;(d_a != 0.0 &&
      (isnan(d_a) ||
       isgreater(fabs(d_a), FLT_MAX) ||
       isless(fabs(d_a), FLT_MIN))) {
    /* Handle error */
  } else {
    f_a = (float)d_a;
  }
  if (big_d != 0.0 &&
      (isnan(big_d) ||
       isgreater(fabs(big_d), FLT_MAX) ||
       isless(fabs(big_d), FLT_MIN))) {
    /* Handle error */
  } else {
    f_b = (float)big_d;
  }
  if (big_d != 0.0 &&
      (isnan(big_d) ||
       isgreater(fabs(big_d), DBL_MAX) ||
       isless(fabs(big_d), DBL_MIN))) {
    /* Handle error */ | Code now safely handles NaN. |
| p. 189, Section 6.4.1 | ; long int big = 1234567890; | ; long int big = 1234567890L; | Addition of type suffix in initialization statement. |
| p. 190, Section 6.4.2 | ; long int big = 1234567890; | ; long int big = 1234567890L; | Addition of type suffix in initialization statement. |
| p. 203, Section 7.2.1 | In this noncompliant code example, a variable length array of size is declared. | In this noncompliant code example, a variable length array of size size is declared. | The second ”size” was missing. |
| p. 226, Section 8.1 | A character string literal is a sequence of zero or more multibyte characters enclosed in double-quotes, as in  "xyz."  | A character string literal is a sequence of zero or more multibyte characters;enclosed in double-quotes, as in  "xyz". | The period should appear outside the quote, not inside the quote because the quote is part of the character string. |
| p. 279 Section 9.5.1 | The code checks for unsigned integer overflow in compliance with;INT32-C. Ensure that operations on signed integers do not result in overflow and also ensures that len is not equal to zero.  | The code attempts to check for unsigned integer overflow in compliance with;INT30-C. Ensure that unsigned integer operations do not wrap and also ensures that len is not equal to zero. | The code uses only unsigned integers. |
| p. 283, Section 10.1.4 | ; if (msg != NULL) {
    /* Handle error */
  } | ; if (msg == NULL) {
    /* Handle error */
  } | An error should be handled only if msg IS null, not IS NOT null. |
| p. 286, Section 10.2.2 | When opening a;FIFO with O_RDONLY or O_WRONLY set:When opening a block special or character special file that supports nonblocking opens:Otherwise, the behavior of O_NONBLOCK is unspecified. | When opening a FIFO with O_RDONLY or O_WRONLY set:If O_NONBLOCK is set, an open() for reading-only returns without delay. An open() for writing-only returns an error if no process currently has the file open for reading.If O_NONBLOCK is clear, an open() for reading-only blocks the calling thread until a thread opens the file for writing. An open() for writing-only blocks the calling thread until a thread opens the file for reading.When opening a block special or character special file that supports nonblocking opens:If O_NONBLOCK is set, the open() function returns without blocking for the device to be ready or available; subsequent behavior is device-specific.If O_NONBLOCK is;clear, the open() function blocks the calling thread until the device is ready or available before returning.Otherwise, the behavior of O_NONBLOCK is unspecified. | Bulleted items were;missing. |
| p. 365, Section 12.2.3 | Signal handlers can refer to objects with static or thread storage a duration that are lock-free atomic objects, as in this compliant solution: | Signal handlers can refer to objects with static or thread storage durations that are lock-free atomic objects, as in this compliant solution: | The phrase should;be “storage durations” not “storage a duration.” |
| p. 374, Section 13.1 | • Those that set errno and return and out-of-band error indicator• Those that set errno and return and in-band error indicator | • Those that set errno and return an out-of-band error indicator• Those that set errno and return an in-band error indicator | Changed 'and' to 'an' to correct both noun phrases |
| p. 375, Section 13.1 | c16rtomb() , cr32rtomb() | c16rtomb() , c32tomb() | The standard library function name was incorrectly spelled. |
| p. 447, Section ; 14.11.1 | This noncompliant code example declares a shared;atomic_boolflag variable and provides a toggle_flag() method that negates the current value of flag: | This noncompliant code example declares a shared atomic_bool flag variable and provides a toggle_flag() method that negates the current value of flag: | The variable should be “atomic_bool flag,” not “atomic_boolflag.” |
| p. 447, Section 14.11.1 | Execution of this code may result in a data race because the value of flag is read, negated, and written back. | Execution of this code may result in unexpected behavior because the value of flag is read, negated, and written back. | Changed "data race" to a more appropriate term. |
| p 456-457, Section 15.1.3 | Replaced Section 15.1.3 (Compliant Solution (Windows) | Replaced Section 15.1.3 (Compliant Solution (Windows) | Old CS was based on CryptGenRandom() which is deprecated. New CS is based on BCryptGenRandom(), which is recommended as replacement. |
| p 458, Section 15.1.6 | “CryptGenRandom Function“ | “BCryptGenRandom Function“ | Updated bib. reference to correspond with new Section 15.1.3 |
| p. 461, Section 15.2.3 | Replaced Section 15.2.3 (Compliant Solution (Windows) | Replaced Section 15.2.3 (Compliant Solution (Windows) | Old CS was based on CryptGenRandom() which is deprecated. New CS is based on BCryptGenRandom(), which is recommended as replacement |
| p 462, Section 15.2.6 | “CryptGenRandom Function“ | “BCryptGenRandom Function“ | Updated bib. reference to correspond with new Section 15.2.3 |
| p. 479, Section A | Previous section is 15.7.8, rule MSC40-C | New rule MSC41-C (See wiki for contents) | New rule deemed necessary (vulnerability not covered by pre-existing rule). |
| p. 501, Section B | "analyzer" definition reference was [ISO/IEC 9899:2011]. | "analyzer" definition reference should be [ISO/IEC TS 17961:2013] | Reference was to the wrong ISO/IEC standard document. |
| p. 519, Section C | 137 The macro va_arg is invoked using the parameter ap that waspassed to a function that invoked the macro va_arg with the same
parameter (7.16). CON37-C | 137 The macro va_arg is invoked using the parameter ap that waspassed to a function that invoked the macro va_arg with the same
parameter (7.16) | Rule CON37-C should be associated with Undefined Behavior 135, not 137. |
| p. 519, Section C | 135 The signal function is used in a multi-threaded program (7.14.1.1). | 135 The signal function is used in a multi-threaded program (7.14.1.1).  CON37-C | Rule CON37-C should be associated with Undefined Behavior 135, not 137. |

