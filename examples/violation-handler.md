# A Custom Contract-Violation Handler

When a contract assertion fails, the implementation calls the
*contract-violation handler*.  A program can replace the default handler by
defining `::handle_contract_violation`, which receives a
`std::contracts::contract_violation` describing the failure.

```cpp
#include <contracts>
#include <cstdio>

void handle_contract_violation(const std::contracts::contract_violation& v)
{
  std::printf("contract violated at %s:%u: %s\n",
              v.location().file_name(), v.location().line(), v.comment());
}

int f(const int x)
  pre (x > 0)
  post (r : r > x)
{
  contract_assert(x < 100);
  return x + 1;
}

int main()
{
  f(0);    // precondition violated
  f(200);  // assertion violated
  std::printf("done\n");
}
```
<!-- celink {"exclude": ["edg_eccp_p3850"], "options": "-fcontract-evaluation-semantic=observe", "expect": "success", "stdout": ["contract violated at .*:11: ", "contract violated at .*:14: ", "done"]} -->
Try it on Compiler Explorer: [GCC 16.1](https://godbolt.org/z/PGhGjfE51) | [GCC P3850](https://godbolt.org/z/f3sTjcMvY) | [Clang P3850](https://godbolt.org/z/f8cozEYzv)
<!-- /celink -->

These links compile with `-fcontract-evaluation-semantic=observe`.  Under
the *observe* semantic, execution continues after the handler returns, so
both violations are reported and the program runs to completion.  Under the
default *enforce* semantic, the program would terminate after the handler
returns from the first violation.

The text of `comment()` is implementation-defined.  GCC and Clang return
the predicate as written; EDG returns its own rendering of it, such as
`(((int)x) > 0)`.

There is no EDG link for this example.  EDG on Compiler Explorer uses EDG's
C back end, which supports only the *ignore* and *quick_enforce* evaluation
semantics, neither of which calls the contract-violation handler.
