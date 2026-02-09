
import sys

def emit_case(idx, q, ops_iter):
    w = sys.stdout.write
    w(f"Input {idx}:\n")
    w(str(q) + "\n")
    for op in ops_iter:
        w(op + "\n")
    w("\n")

def main():
    w = sys.stdout.write
    w("Test Cases: \n")

    idx = 1

    # 1) Minimum input (q=1, n=1)
    emit_case(idx, 1, ["1 1"]); idx += 1

    # 2) Small: basic transmute after appends
    emit_case(idx, 3, [
        "1 1",
        "1 2",
        "2 1 3"
    ]); idx += 1

    # 3) Mirror-swap simultaneity (both x and y present)
    emit_case(idx, 5, [
        "1 1",
        "1 2",
        "1 1",
        "1 2",
        "3 1 2"
    ]); idx += 1

    # 4) Time-order: transmute does not affect later appended elements
    emit_case(idx, 3, [
        "1 5",
        "2 5 3",
        "1 5"
    ]); idx += 1

    # 5) No-ops: x==y in transmute and swap, mixed with real ops
    emit_case(idx, 6, [
        "1 10",
        "2 10 10",
        "3 10 10",
        "1 10",
        "2 10 11",
        "3 11 10"
    ]); idx += 1

    # 6) Transforms on values not present (should be safe), then swap affecting existing
    emit_case(idx, 5, [
        "1 7",
        "2 1 2",
        "3 3 4",
        "2 5 6",
        "3 7 8"
    ]); idx += 1

    # 7) Chain remaps + interleaved append + final swap (composition correctness)
    emit_case(idx, 7, [
        "1 1",
        "1 2",
        "2 1 2",
        "1 1",
        "2 2 3",
        "2 1 2",
        "3 2 3"
    ]); idx += 1

    # 8) Many duplicates + transform creating all-equal + swap after late append
    emit_case(idx, 12, (
        [f"1 {2 if i % 2 == 0 else 1}" for i in range(8)] +
        ["2 2 1",
         "1 2",
         "3 1 2",
         "2 3 4"]
    )); idx += 1

    # 9) Boundary values (1 and 5e5), collapse, append-after, then swap
    MAXV = 500000
    emit_case(idx, 7, [
        "1 1",
        f"1 {MAXV}",
        "1 1",
        f"1 {MAXV}",
        f"2 {MAXV} 1",
        f"1 {MAXV}",
        f"3 1 {MAXV}"
    ]); idx += 1

    # 10) Strictly decreasing small (inversion-heavy, hand-checkable)
    emit_case(idx, 5, [
        "1 5",
        "1 4",
        "1 3",
        "1 2",
        "1 1"
    ]); idx += 1

    # 11) Repeated toggling swaps (parity) + transmute into swapped set
    emit_case(idx, 10, [
        "1 1",
        "1 2",
        "1 1",
        "1 2",
        "1 3",
        "3 1 2",
        "3 1 2",
        "3 1 2",
        "2 3 1",
        "3 1 2"
    ]); idx += 1

    # 12) Stress pattern: many transforms, few appends; with transforms both before and after 2nd append
    q12 = 1000
    ops12 = []
    ops12.append("1 1")
    for t in range(500):
        a = (t % 5) + 1
        b = ((t + 1) % 5) + 1
        if t % 2 == 0:
            ops12.append(f"3 {a} {b}")
        else:
            ops12.append(f"2 {a} {b}")
    ops12.append("1 2")
    for t in range(498):
        a = ((t + 2) % 5) + 1
        b = ((t + 4) % 5) + 1
        if t % 3 == 0:
            ops12.append(f"2 {a} {b}")
        else:
            ops12.append(f"3 {a} {b}")
    assert len(ops12) == q12
    emit_case(idx, q12, ops12); idx += 1

    # 13) Moderate large mixed: 10k appends + 10k transforms (swap/transmute), values in small range
    q13 = 20000
    def ops13_iter():
        for i in range(10000):
            v = (i % 100) + 1
            yield f"1 {v}"
        for k in range(5000):
            x = (k % 100) + 1
            y = ((k + 37) % 100) + 1
            yield f"3 {x} {y}"
            z = ((k + 50) % 100) + 1
            yield f"2 {y} {z}"
    emit_case(idx, q13, ops13_iter()); idx += 1

    # 14) Large n to force 64-bit inversion count if decreasing
    n14 = 100000
    q14 = n14
    def ops14_iter():
        for v in range(n14, 0, -1):
            yield f"1 {v}"
    emit_case(idx, q14, ops14_iter()); idx += 1

    # 15) Max q=500000, n=1: stresses per-operation overhead; many swaps/transmutes
    q15 = 500000
    def ops15_iter():
        yield "1 1"
        for j in range(499999):
            if j % 3 == 0:
                yield "3 1 2"
            elif j % 3 == 1:
                yield "2 1 2"
            else:
                yield "2 2 1"
    emit_case(idx, q15, ops15_iter()); idx += 1

if __name__ == "__main__":
    main()
