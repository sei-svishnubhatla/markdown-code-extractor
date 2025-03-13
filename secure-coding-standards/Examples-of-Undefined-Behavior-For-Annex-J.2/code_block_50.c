#define my_join(a, b) a ## b
char q[] = my_join(foo, bar);
// Ill-formed, unless 'foobar' is an identifier (or similar preprocessing token)