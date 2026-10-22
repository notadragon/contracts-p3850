# Preconditions, Postconditions, and Assertions

C++26 contract assertions come in three forms:

- a *precondition*, `pre (predicate)`, checked on entry to a function,
- a *postcondition*, `post (predicate)`, checked when a function returns
  normally, which can name the return value, and
- an *assertion statement*, `contract_assert(predicate);`, checked where it
  appears in a function body.

The following example, from [P2900R14](https://wg21.link/P2900R14),
contains all three:

```cpp
int f(const int x)
  pre (x != 1)                // a precondition assertion
  post(r : r == x && r != 2)  // a postcondition assertion; `r` names the result object of `f`
{
  contract_assert (x != 3);   // an assertion statement
  return x;
}

void g()
{
  f(0);  // no contract violation
  f(1);  // violates precondition assertion of `f`
  f(2);  // violates postcondition assertion of `f`
  f(3);  // violates assertion statement within `f`
  f(4);  // no contract violation
}

int main()
{
  g();
}
```
<!-- celink {"expect": "error"} -->
Try it on Compiler Explorer: [GCC 16.1](https://godbolt.org/z/5WGh8d6bq) | [GCC P3850](https://godbolt.org/z/hEn3cooz6) | [Clang P3850](https://godbolt.org/z/fYYT96c1x) | [EDG P3850](https://godbolt.org/z/bzGMM4WsM)
<!-- /celink -->

Function parameters named in a postcondition must be `const`, so that the
postcondition sees the values the function was called with.

Under the default *enforce* evaluation semantic, the default
contract-violation handler reports the first violation, the precondition of
`f(1)`, and the program terminates, so the later calls are never made.
Remove or reorder the calls in `g` to see the other violations.

EDG on Compiler Explorer uses EDG's C back end, which supports only the
*ignore* and *quick_enforce* evaluation semantics, so there the violation
stops the program immediately, without a report.
