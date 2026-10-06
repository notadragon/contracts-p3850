#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
README="$REPO_ROOT/README.md"
BRANCH="contracts-p3850"

GCC_RAW="https://raw.githubusercontent.com/notadragon/gnu_gcc/${BRANCH}"
CLANG_RAW="https://raw.githubusercontent.com/notadragon/llvm-project/${BRANCH}"
EDG_RAW="https://raw.githubusercontent.com/notadragon/edgcpp_compiler/${BRANCH}"

# Counts a markdown table's "| PREFIX-N | ..." rows, excluding rows that
# fall under a "Tasks" heading (open-issues) or a "Fixed upstream by us"
# heading (bug-reports) -- those aren't currently-open items.
count_rows() {
  local raw_base="$1" path="$2" prefix="$3"
  curl -sf "$raw_base/$path" | awk -v prefix="$prefix" '
    /^#/ {
      low = tolower($0)
      exclude = (index(low, "tasks") > 0) || (index(low, "fixed upstream") > 0)
      next
    }
    exclude { next }
    $0 ~ "^\\| *" prefix "-[0-9]+ *\\|" { count++ }
    END { print count + 0 }
  '
}

gcc_open=$(count_rows "$GCC_RAW" open-issues/README.md GCC)
gcc_bugs=$(count_rows "$GCC_RAW" bug-reports/README.md GCC)
clang_open=$(count_rows "$CLANG_RAW" open-issues/README.md CLANG)
clang_bugs=$(count_rows "$CLANG_RAW" bug-reports/README.md CLANG)
edg_open=$(count_rows "$EDG_RAW" open-issues/README.md EDG)
edg_bugs=$(count_rows "$EDG_RAW" bug-reports/README.md EDG)

echo "GCC:   open-issues=$gcc_open  bug-reports=$gcc_bugs"
echo "Clang: open-issues=$clang_open  bug-reports=$clang_bugs"
echo "EDG:   open-issues=$edg_open  bug-reports=$edg_bugs"

sed -i -E \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/gnu_gcc/tree/${BRANCH}/open-issues\))#\1${gcc_open}\2#" \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/gnu_gcc/tree/${BRANCH}/bug-reports\))#\1${gcc_bugs}\2#" \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/llvm-project/tree/${BRANCH}/open-issues\))#\1${clang_open}\2#" \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/llvm-project/tree/${BRANCH}/bug-reports\))#\1${clang_bugs}\2#" \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/edgcpp_compiler/tree/${BRANCH}/open-issues\))#\1${edg_open}\2#" \
  -e "s#(\[)[0-9]+(\]\(https://github.com/notadragon/edgcpp_compiler/tree/${BRANCH}/bug-reports\))#\1${edg_bugs}\2#" \
  "$README"
