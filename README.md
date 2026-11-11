# C++ Contracts and Extensions

C++26 includes support for contract assertions, adopted with
[P2900R14](https://wg21.link/P2900R14), also known as the Contracts MVP.
[P3850R0](https://wg21.link/P3850R0) lays out a plan for extending that
initial MVP to support a much wider range of use cases in C++29 and beyond.
This project covers the ongoing work to implement those papers and,
eventually, more forward-looking papers that will build even further
on top of what is ready to deliver today.

## Compilers

The various P3850 papers are being implemented in 3 compilers --- GCC,
Clang, and EDG.  Within the branches (all `contracts-p3850`) we are also tracking
open bugs that have not been addressed yet and bug reports that are due against
the upstream compilers.  (Work to upstream those fixes is ongoing).

| Repository | Open Issues | Bug Reports |
|---|---|---|
| [GCC](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850) | [92](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850/open-issues) | [140](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850/bug-reports) |
| [Clang](https://github.com/notadragon/llvm-project/tree/contracts-p3850) | [73](https://github.com/notadragon/llvm-project/tree/contracts-p3850/open-issues) | [33](https://github.com/notadragon/llvm-project/tree/contracts-p3850/bug-reports) |
| [EDG](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850) | [33](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850/open-issues) | [23](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850/bug-reports) |

## Compiler Explorer

All of these compilers have been made available on compiler explorer.

[![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-gcc_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-gcc_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fgcc_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fgcc_notadragon_contracts_p3850)

[![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-clang_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-clang_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fclang_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fclang_notadragon_contracts_p3850)

[![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-edg_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-edg_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fedg_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fedg_notadragon_contracts_p3850)

## Papers

The following papers have been adopted into the C++ draft standard and are
implemented on these forks, along with bug fixes for any known issues related
to these papers that exist in upstream compilers:

- [P2900R14 -- Contracts for C++](https://wg21.link/P2900R14)
- [P3097R3 -- Contracts for C++: Virtual functions](https://wg21.link/P3097R3)

The following papers have been implemented (fully or partially) in these
forks.  Where a newer draft revision exists, it follows the published paper
and is in the [drafts](drafts/) directory:

- [P3098R2 -- Contracts for C++: Postcondition captures](https://wg21.link/P3098R2), [D3098R3](drafts/D3098R3.pdf)
- [P3099R3 -- Contracts for C++: User-defined diagnostic messages](https://wg21.link/P3099R3)
- [P3100R9 -- A framework for systematically addressing undefined behaviour in the C++ Standard](https://wg21.link/P3100R9)
- [P3290R6 -- Integrating Existing Assertions With Contracts](https://wg21.link/P3290R6)
- [P3400R5 -- Controlling Contract-Assertion Properties](https://wg21.link/P3400R5)
- [P3595R0 -- Configuration of Contract Evaluation Semantics](https://wg21.link/P3595R0), [D3595R1](drafts/D3595R1.pdf)
- [P4283R0 -- Requires clauses for Contract Assertions](https://wg21.link/P4283R0), [D4283R1](drafts/D4283R1.pdf)
- [P4298R0 -- Nonthrowing Evaluation Semantics](https://wg21.link/P4298R0), [D4298R1](drafts/D4298R1.pdf)
- [D4299R0 -- C++ Contracts for C](drafts/D4299R0.pdf) (work in progress)
- [D4301R0 -- Context Reports for the Contract-Violation Handler](drafts/D4301R0.pdf) (work in progress)
- [D4405R0 -- Proving Contract Assertions Are Not Violated](drafts/D4405R0.pdf) (work in progress)

## Additional Features

These compilers also provide some features that are not proposed for the
C++ Standard or in any specific paper.  They exist to support
experimentation and are not part of any proposed design.

### `-fcontracts-allow-assume`

[P3100R9](https://wg21.link/P3100R9) introduces the `assume` evaluation
semantic, under which a contract predicate is not evaluated and the
compiler may instead assume that it holds.  A violation of such a contract
assertion is undefined behavior.  P3100 uses this semantic only for
implicit contract assertions; no paper proposes allowing it for contract
assertions written in the source.

All three compilers support `-fcontracts-allow-assume`, which allows the
`assume` semantic to be selected for contract assertions in the source
(through `-fcontract-evaluation-semantic=assume`, a group or configuration
entry, and so on).  Without this flag, an explicit contract assertion
whose semantic resolves to `assume` is treated as `ignore` instead.
Implicit contract assertions do not need the flag.

With this flag, a [P3400R5](https://wg21.link/P3400R5) label can also
produce the `assume` semantic: `assume` may appear in the label's
`allowed_semantics`, and its `compute_semantic` may return it.  Without
the flag, a label whose `compute_semantic` returns `assume` is ill-formed.

When the flag is in effect and contracts are enabled, the macro
`__gcc_contracts_allow_assume` (GCC, and EDG in GCC mode) or
`__clang_contracts_allow_assume` (Clang, and EDG in Clang mode) is defined.

### `-fcontract-violation-information=full|none`

By default (`full`), each contract assertion checked at run time puts its
source location (file, function, line and column), its comment (the text
of the predicate) and any user-supplied message into the object file, for
the violation handler to report.  With
`-fcontract-violation-information=none`, all three compilers leave this
information out: the handler sees an empty file and function name, line
and column 0, an empty comment and no message.  The kind, semantic and
detection mode are still reported, and compile-time diagnostics keep their
locations.

This applies to explicit and implicit contract assertions, in C++ and
(with GCC and Clang, which implement contracts for C) in C.
The `assert` macro of [P3290R6](https://wg21.link/P3290R6) and the
default location of its violation-handling functions follow it too, through
the macro `__gcc_contracts_violation_information_none` (GCC, and EDG in GCC
mode) or `__clang_contracts_violation_information_none` (Clang, and EDG in
Clang mode), defined under `none`.  Sanitizer metadata is not affected;
`-ffile-prefix-map` remaps the paths in it, as it does the file name of a
contract violation under `full`.

## Examples

The [examples](examples/README.md) directory has short examples of using
contracts, each with links to try it in Compiler Explorer.

## Tools

This repository also includes some additional tools for working with and verifying
these implementations.

### Testing

TODO: We will be providing a thorough test suite and cross-compiler integration suite
here soon.
