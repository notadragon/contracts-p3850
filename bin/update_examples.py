#!/usr/bin/env python3
"""Regenerate the Compiler Explorer links in examples/*.md.

Each example code block that should get links is followed by a marker pair:

    ```cpp
    ...
    ```
    <!-- celink {"profile": "default"} -->
    ...generated links, replaced on every run...
    <!-- /celink -->

The JSON in the opening marker accepts:

    profile   name of a compiler set in examples/celink-profiles.json
              (default "default")
    options   extra options appended to every compiler's options
    exclude   list of compiler ids from the profile to give no link
    expect    "success" or "error": the expected exit status when the
              program runs (checked only by --test)
    stdout    list of regexes the program's stdout must match (--test only)
    stderr    list of regexes the program's stderr must match (--test only)

For the Nth marked block of examples/<stem>.md, one .celink per compiler is
written to examples/.celink/<stem>-NN-<compiler-id>.celink.  Stale .celink
files (higher sequence numbers, compilers no longer in the profile, or
examples that no longer exist) are removed.

The .celink tooling lives in the notadragon_wg21 repository, found through
$WG21_REPO (default: ../notadragon_wg21 next to this repository).  Short
URLs are cached next to each .celink in a .celink_cache file, so only
changed examples contact the godbolt shortener.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
CELINK_DIR = EXAMPLES_DIR / ".celink"
PROFILES = EXAMPLES_DIR / "celink-profiles.json"
TARGET = "godbolt"

FENCE_RE = re.compile(r"^```(\w*)\s*$")
OPEN_RE = re.compile(r"^<!--\s*celink\s*(\{.*\})?\s*-->\s*$")
CLOSE_RE = re.compile(r"^<!--\s*/celink\s*-->\s*$")
CELINK_NAME_RE = re.compile(r"^(?P<stem>.+)-(?P<seq>\d{2,})-(?P<id>[^-]+)"
                            r"\.celink(?:_cache)?$")
URL_RE = re.compile(r"\\csname celinkurl@[^@]+@" + TARGET +
                    r"\\endcsname\{([^}]*)\}")


def wg21_tools():
    root = Path(os.environ.get("WG21_REPO",
                               REPO_ROOT.parent / "notadragon_wg21"))
    tools = root / "src/pubs/papers/compilerexplorer/bin"
    if not (tools / "gen_celink.py").exists():
        sys.exit(f"error: celink tools not found under {tools}; "
                 f"set WG21_REPO to the notadragon_wg21 checkout")
    return tools


def parse_blocks(md_path):
    """Return (lines, blocks) where each block is a dict with the code, the
    marker settings, and the line span [start, end) of the marker region."""
    lines = md_path.read_text().splitlines()
    blocks = []
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if not m or not m.group(1):
            i += 1
            continue
        j = i + 1
        while j < len(lines) and lines[j].rstrip() != "```":
            j += 1
        if j == len(lines):
            sys.exit(f"error: {md_path.name}:{i + 1}: unterminated code "
                     f"block")
        code = "\n".join(lines[i + 1:j]) + "\n"
        k = j + 1
        while k < len(lines) and not lines[k].strip():
            k += 1
        om = OPEN_RE.match(lines[k]) if k < len(lines) else None
        if not om:
            i = j + 1
            continue
        try:
            settings = json.loads(om.group(1) or "{}")
        except json.JSONDecodeError as e:
            sys.exit(f"error: {md_path.name}:{k + 1}: bad celink marker "
                     f"JSON: {e}")
        end = k + 1
        while end < len(lines) and not CLOSE_RE.match(lines[end]):
            if FENCE_RE.match(lines[end]) or OPEN_RE.match(lines[end]):
                sys.exit(f"error: {md_path.name}:{k + 1}: celink marker "
                         f"has no closing <!-- /celink -->")
            end += 1
        if end == len(lines):
            sys.exit(f"error: {md_path.name}:{k + 1}: celink marker has no "
                     f"closing <!-- /celink -->")
        blocks.append({"code": code, "settings": settings,
                       "start": k + 1, "end": end})
        i = end + 1
    return lines, blocks


def celink_text(compiler, settings, code):
    options = compiler["options"]
    if settings.get("options"):
        options += " " + settings["options"]
    entry = {"id": compiler["id"], "options": options,
             "source": "example.cpp", "execute": True}
    expect = settings.get("expect")
    if expect == "success":
        entry["expect_runtime_success"] = True
    elif expect == "error":
        entry["expect_runtime_error"] = True
    elif expect is not None:
        sys.exit(f"error: unknown expect value {expect!r}")
    config = {"language": "c++", "view": "single"}
    matchers = []
    for stream in ("stdout", "stderr"):
        names = []
        for n, regex in enumerate(settings.get(stream, [])):
            names.append(f"{stream}{n}")
            matchers.append({"name": names[-1], "regex": regex})
        if names:
            entry["execute_" + stream] = names
    if matchers:
        config["matchers"] = matchers
    config["compilers"] = [entry]
    return ("%%% config\n" + json.dumps(config, indent=2) + "\n"
            "%%% source example.cpp\n" + code)


def write_if_changed(path, text):
    if path.exists() and path.read_text() == text:
        return
    path.write_text(text)


def short_url(tools, celink):
    """Shorten celink (a no-op when its cache is current) and return the
    URL gen_celink.py would use for TARGET."""
    subprocess.run([sys.executable, str(tools / "shorten_celink.py"),
                    "--target", TARGET, str(celink)], check=True)
    with tempfile.TemporaryDirectory() as tmp:
        tex = Path(tmp) / "out.tex"
        subprocess.run([sys.executable, str(tools / "gen_celink.py"),
                        "--fromfile", str(celink), "--tofile", str(tex)],
                       check=True)
        m = URL_RE.search(tex.read_text())
    if not m:
        sys.exit(f"error: no {TARGET} URL generated for {celink.name}")
    url = m.group(1)
    if "/z/" not in url:
        sys.exit(f"error: {celink.name}: {TARGET} URL was not shortened")
    return url


def update_md(md_path, profiles, tools, test, shorten):
    lines, blocks = parse_blocks(md_path)
    stem = md_path.stem
    wanted = set()
    for seq, block in enumerate(blocks, start=1):
        profile_name = block["settings"].get("profile", "default")
        if profile_name not in profiles:
            sys.exit(f"error: {md_path.name}: unknown profile "
                     f"{profile_name!r}")
        exclude = block["settings"].get("exclude", [])
        unknown = set(exclude) - {c["id"] for c in profiles[profile_name]}
        if unknown:
            sys.exit(f"error: {md_path.name}: excluded compilers not in "
                     f"profile {profile_name!r}: {sorted(unknown)}")
        block["celinks"] = []
        for compiler in profiles[profile_name]:
            if compiler["id"] in exclude:
                continue
            name = f"{stem}-{seq:02d}-{compiler['id']}.celink"
            wanted.add(name)
            celink = CELINK_DIR / name
            write_if_changed(celink, celink_text(compiler, block["settings"],
                                                 block["code"]))
            block["celinks"].append((compiler["label"], celink))
    remove_stale(lambda s: s == stem, wanted)
    # Test before shortening so a broken example never gets a public link.
    if test and blocks:
        result = subprocess.run(
            [sys.executable, str(tools / "test_celinks.py")] +
            [str(c) for b in blocks for _, c in b["celinks"]])
        if result.returncode:
            sys.exit(f"error: {md_path.name}: celink tests failed; "
                     f"links not updated")
    if not shorten:
        return
    for block in reversed(blocks):
        links = [f"[{label}]({short_url(tools, celink)})"
                 for label, celink in block["celinks"]]
        lines[block["start"]:block["end"]] = [
            "Try it on Compiler Explorer: " + " | ".join(links)]
    write_if_changed(md_path, "\n".join(lines) + "\n")


def remove_stale(stem_matches, wanted):
    for path in sorted(CELINK_DIR.iterdir()):
        m = CELINK_NAME_RE.match(path.name)
        if not m or not stem_matches(m.group("stem")):
            continue
        if path.name.replace(".celink_cache", ".celink") not in wanted:
            print(f"removing stale {path.relative_to(REPO_ROOT)}")
            path.unlink()


def main():
    parser = argparse.ArgumentParser(
        description="Regenerate Compiler Explorer links in examples/*.md.")
    parser.add_argument("files", nargs="*", type=Path,
                        help="example .md files (default: all of them)")
    parser.add_argument("--test", action="store_true",
                        help="also validate the .celink files against a "
                             "local Compiler Explorer (test_celinks.py)")
    parser.add_argument("--no-shorten", action="store_true",
                        help="write (and with --test, test) the .celink "
                             "files but leave the .md links untouched")
    args = parser.parse_args()

    tools = wg21_tools()
    profiles = json.loads(PROFILES.read_text())
    CELINK_DIR.mkdir(exist_ok=True)
    all_mds = sorted(p for p in EXAMPLES_DIR.glob("*.md")
                     if p.name != "README.md")
    mds = [p.resolve() for p in args.files] if args.files else all_mds
    for md in mds:
        update_md(md, profiles, tools, args.test, not args.no_shorten)
    if not args.files:
        # Examples that were deleted or renamed leave orphaned .celinks.
        stems = {p.stem for p in all_mds}
        remove_stale(lambda s: s not in stems, set())


if __name__ == "__main__":
    main()
