# Preconditions, Postconditions, and Assertions

C++26 contract assertions come in three forms:

- a *precondition*, `pre (predicate)`, checked on entry to a function,
- a *postcondition*, `post (predicate)`, checked when a function returns
  normally, which can name the return value, and
- an *assertion statement*, `contract_assert(predicate);`, checked where it
  appears in a function body.

Function parameters named in a postcondition must be `const`, so that the
postcondition sees the values the function was called with.

```cpp
#include <cstdio>

int divide(const int numerator, const int denominator)
  pre (denominator != 0)
  post (r : r * denominator <= numerator)
{
  int result = numerator / denominator;
  contract_assert(result * denominator <= numerator);
  return result;
}

int main()
{
  std::fprintf(stderr, "divide(7, 2) = %d\n", divide(7, 2));
  std::fprintf(stderr, "divide(1, 0) = %d\n", divide(1, 0));  // violation
}
```
<!-- celink {"expect": "error", "stderr": ["divide\\(7, 2\\) = 3"]} -->
Try it on Compiler Explorer: [GCC 16.1](https://godbolt.org/z/aT4b79G48) | [GCC P3850](https://godbolt.org/z/73nPGr7Wq) | [Clang P3850](https://godbolt.org/z/av1xEGda7) | [EDG P3850](https://godbolt.org/z/sd9a96YWz)
<!-- /celink -->

The first call satisfies every contract assertion.  The second violates the
precondition.  Under the default *enforce* evaluation semantic the default
contract-violation handler reports the violation and the program terminates,
so the division by zero is never reached.

EDG on Compiler Explorer uses EDG's C back end, which supports only the
*ignore* and *quick_enforce* evaluation semantics, so there the violation
stops the program immediately, without a report.
