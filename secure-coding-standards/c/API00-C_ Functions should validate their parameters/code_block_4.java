void f(int *ptr) {
  // Don't need to check that ptr isn't null because callers do that.
  *ptr = 12;
}