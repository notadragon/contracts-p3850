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
| [GCC](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850) | [4](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850/open-issues) | [35](https://github.com/notadragon/gnu_gcc/tree/contracts-p3850/bug-reports) |
| [Clang](https://github.com/notadragon/llvm-project/tree/contracts-p3850) | [8](https://github.com/notadragon/llvm-project/tree/contracts-p3850/open-issues) | [5](https://github.com/notadragon/llvm-project/tree/contracts-p3850/bug-reports) |
| [EDG](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850) | [20](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850/open-issues) | [18](https://github.com/notadragon/edgcpp_compiler/tree/contracts-p3850/bug-reports) |

## Compiler Explorer

All of these compilers have been made available on compiler explorer.

- GCC: [![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-gcc_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-gcc_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fgcc_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fgcc_notadragon_contracts_p3850)
- Clang: [![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-clang_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-clang_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fclang_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fclang_notadragon_contracts_p3850)
- EDG: [![Status](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-edg_notadragon_contracts_p3850.yml/badge.svg)](https://github.com/compiler-explorer/compiler-workflows/actions/workflows//build-daily-edg_notadragon_contracts_p3850.yml)![Last success](https://img.shields.io/badge/dynamic/json?color=success&label=Last+OK&query=%24.last_success.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fedg_notadragon_contracts_p3850)![Last build](https://img.shields.io/badge/dynamic/json?color=yellow&label=Last+build&query=%24.last_build.timestamp&url=https%3A%2F%2Flambda.compiler-explorer.com%2Fcompiler-build%2Fedg_notadragon_contracts_p3850)

## Papers

The following papers have been implemented (fully or partially) in these forks:

- [P3097R3 -- Contracts for C++: Virtual functions](https://wg21.link/P3097R3)
- [P3098R2 -- Contracts for C++: Postcondition captures](https://wg21.link/P3098R2)
- [P3099R3 -- Contracts for C++: User-defined diagnostic messages](https://wg21.link/P3099R3)
- [P3100R8 -- A framework for systematically addressing undefined behaviour in the C++ Standard](https://wg21.link/P3100R8)
- [P3290R6 -- Integrating Existing Assertions With Contracts](https://wg21.link/P3290R6)
- [P3400R4 -- Controlling Contract-Assertion Properties](https://wg21.link/P3400R4)
- [P3595R0 -- Configuration of Contract Evaluation Semantics](https://wg21.link/P3595R0)
- [P4283R0 -- Requires clauses for Contract Assertions](https://wg21.link/P4283R0)
- [P4298R0 -- Nonthrowing Evaluation Semantics](https://wg21.link/P4298R0)
- D4299 -- C++ Contracts for C (not yet submitted to WG21)
- D4301 -- Context Reports for the Contract-Violation Handler (not yet submitted to WG21)

## Tools

This repository also includes some additional tools for working with and verifying
these implementations.

### Testing

TODO: We will be providing a thorough test suite and cross-compiler integration suite
here soon.
