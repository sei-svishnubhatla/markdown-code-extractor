int square(int x) {return x*x;}

enum people {
  Tom=1,
  Dick=2,
  Harry=square(2)
};

struct s {
  int bit:1;
  int two_bits:square(2);
  int all_the_bits;
};