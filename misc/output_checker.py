
import os
import re
from typing import Tuple, List


class Fenwick:
    __slots__ = ("n", "bit")

    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, delta: int) -> None:
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += delta
            i += i & -i

    def sum(self, i: int) -> int:
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i &= i - 1
        return s


# Strict: only digits and single spaces between tokens, no leading/trailing spaces
_INT_LINE_RE = re.compile(r"^[0-9]+(?: [0-9]+)*$")
_SINGLE_INT_RE = re.compile(r"^[0-9]+$")


def _normalize_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def _enforce_eof_newline_rule(s: str) -> Tuple[bool, str, str]:
    """
    Allow:
      - no trailing newline, or
      - exactly one trailing newline.
    Disallow multiple trailing newlines (extra blank lines at end).
    """
    if s.endswith("\n"):
        s2 = s[:-1]
        if s2.endswith("\n"):
            return False, "Output has extra blank line(s) at end (more than one trailing newline).", ""
        return True, "OK", s2
    return True, "OK", s


def _parse_n_from_input(input_text: str) -> Tuple[bool, str, int]:
    """
    Parse input (single test case as per statement) and return n,
    the number of type-1 operations (final scroll length).
    """
    inp = _normalize_newlines(input_text)
    toks = inp.split()
    if not toks:
        return False, "Invalid input file: empty.", 0
    try:
        q = int(toks[0])
    except Exception:
        return False, "Invalid input file: first token is not an integer q.", 0
    if q < 1:
        return False, f"Invalid input file: q must be >= 1, got {q}.", 0

    ptr = 1
    n = 0
    for op_idx in range(1, q + 1):
        if ptr >= len(toks):
            return False, f"Invalid input file: incomplete operation at index {op_idx}.", 0
        try:
            t = int(toks[ptr])
        except Exception:
            return False, f"Invalid input file: operation type at index {op_idx} is not an integer.", 0
        ptr += 1

        if t == 1:
            if ptr >= len(toks):
                return False, f"Invalid input file: operation 1 at index {op_idx} missing x.", 0
            ptr += 1
            n += 1
        elif t == 2 or t == 3:
            if ptr + 1 >= len(toks):
                return False, f"Invalid input file: operation {t} at index {op_idx} missing x y.", 0
            ptr += 2
        else:
            return False, f"Invalid input file: unknown operation type {t} at index {op_idx}.", 0

    return True, "OK", n


def check(input_text: str, output_text: str) -> Tuple[bool, str]:
    ok, msg, n = _parse_n_from_input(input_text)
    if not ok:
        return False, msg

    out = _normalize_newlines(output_text)

    # Strict whitespace: reject tabs explicitly (and most other whitespace will fail regex later).
    if "\t" in out:
        return False, "Output contains tab characters; only spaces/newlines are allowed."

    ok, msg, out = _enforce_eof_newline_rule(out)
    if not ok:
        return False, msg

    if out == "":
        return False, "Output is empty; expected 2 lines (final array and inversion count)."

    lines = out.split("\n")
    if len(lines) != 2:
        return False, f"Expected exactly 2 lines, got {len(lines)} line(s)."

    line1, line2 = lines[0], lines[1]

    # Line 1: final array
    if line1 == "":
        return False, "Line 1 is empty; expected the final array."
    if not _INT_LINE_RE.match(line1):
        return False, "Line 1 has invalid formatting; expected integers separated by single spaces, with no leading/trailing spaces."

    # Line 2: inversion count
    if line2 == "":
        return False, "Line 2 is empty; expected the inversion count."
    if not _SINGLE_INT_RE.match(line2):
        return False, "Line 2 has invalid formatting; expected a single nonnegative integer with no surrounding spaces."

    # Parse line 1 array and validate length/range
    a_strs = line1.split(" ")
    if len(a_strs) != n:
        return False, f"Line 1: expected exactly n={n} integers (number of type-1 operations), got {len(a_strs)}."

    MAXV = 500000
    A: List[int] = []
    for i, s in enumerate(a_strs, start=1):
        try:
            v = int(s)
        except Exception:
            return False, f"Line 1: token {i} is not a valid integer."
        if not (1 <= v <= MAXV):
            return False, f"Line 1: value {v} at position {i} is out of range [1..{MAXV}]."
        A.append(v)

    # Parse and validate inversion count
    try:
        reported = int(line2)
    except Exception:
        return False, "Line 2: inversion count is not a valid integer."

    max_inv = n * (n - 1) // 2
    if not (0 <= reported <= max_inv):
        return False, f"Line 2: inversion count {reported} is out of valid range [0..{max_inv}] for n={n}."

    # Self-consistency check: reported inversion count matches inversions of printed array.
    fw = Fenwick(MAXV)
    inv = 0
    seen = 0
    for v in A:
        inv += seen - fw.sum(v)  # previous elements strictly greater than v
        fw.add(v, 1)
        seen += 1

    if inv != reported:
        return False, f"Line 2: reported discord score {reported} does not match inversion count of the printed array ({inv})."

    return True, "OK"


if __name__ == "__main__":
    in_path = os.environ.get("INPUT_PATH", "")
    out_path = os.environ.get("OUTPUT_PATH", "")
    if not in_path or not out_path:
        raise SystemExit(2)
    with open(in_path, "r", encoding="utf-8") as f:
        input_text = f.read()
    with open(out_path, "r", encoding="utf-8") as f:
        output_text = f.read()
    ok, _ = check(input_text, output_text)
    print("True" if ok else "False")
