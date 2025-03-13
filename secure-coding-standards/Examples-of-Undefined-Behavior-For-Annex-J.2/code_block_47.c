#define str(s) # s
#define xstr(s) str(s)
#define INCFILE(n) z ## n

#include xstr(INCFILE(3).h)
// #include "z3.h", but fails to compile if s/xstr/str/;