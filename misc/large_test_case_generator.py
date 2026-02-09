
import sys
import random

MAXV = 500_000

def emit_header():
    sys.stdout.write("**Test Cases: **\n")

def emit_case_begin(idx, q):
    sys.stdout.write(f"Input {idx}:\n")
    sys.stdout.write(f"{q}\n")

def emit_case_end():
    sys.stdout.write("\n")

def case1_max_descending_appends():
    # q=5e5, all appends, descending -> max inversions
    q = 500_000
    emit_case_begin(1, q)
    w = sys.stdout.write
    for v in range(MAXV, 0, -1):
        w(f"1 {v}\n")
    emit_case_end()

def case2_few_appends_many_transforms_time_order():
    # q=5e5, few appends, many transforms; append in the middle to test non-retroactive transforms
    q = 500_000
    emit_case_begin(2, q)
    w = sys.stdout.write

    init_appends = [1, MAXV, 2, MAXV - 1, MAXV // 2]
    for x in init_appends:
        w(f"1 {x}\n")

    m = 249_995
    for i in range(1, m + 1):
        if i & 1:
            x = (i % MAXV) + 1
            y = MAXV - (i % MAXV)
            w(f"2 {x} {y}\n")
        else:
            x = ((i * 7) % MAXV) + 1
            y = ((i * 13) % MAXV) + 1
            w(f"3 {x} {y}\n")

    mid_appends = [3, 4, 5, 6, 7]
    for x in mid_appends:
        w(f"1 {x}\n")

    for i in range(1, m + 1):
        j = i + 123456  # offset to change values/pattern
        if i & 1:
            x = (j % MAXV) + 1
            y = MAXV - (j % MAXV)
            w(f"2 {x} {y}\n")
        else:
            x = ((j * 7) % MAXV) + 1
            y = ((j * 13) % MAXV) + 1
            w(f"3 {x} {y}\n")

    emit_case_end()

def case3_heavy_mix_swap_transmute():
    # Large n, then many global ops mixing swap and transmute (simultaneity + interaction)
    q = 300_000
    emit_case_begin(3, q)
    w = sys.stdout.write

    n_app = 150_000
    for i in range(n_app):
        w(f"1 {1 if (i % 2 == 0) else MAXV}\n")

    n_ops = q - n_app
    for i in range(1, n_ops + 1):
        r = i % 3
        if r == 1:
            w(f"3 1 {MAXV}\n")
        elif r == 2:
            w("2 1 2\n")
        else:
            w("2 500000 1\n")

    emit_case_end()

def case4_many_duplicates_then_collapse():
    # Many appends from small range -> lots of duplicates; many transmutes collapsing to one value + swaps
    q = 400_000
    emit_case_begin(4, q)
    w = sys.stdout.write

    n_app = 200_000
    # Deterministic pseudo-random small-range values
    seed = 123456789
    x = seed
    for _ in range(n_app):
        x = (1103515245 * x + 12345) & 0x7fffffff
        val = (x % 100) + 1
        w(f"1 {val}\n")

    n_ops = q - n_app
    for i in range(1, n_ops + 1):
        if i <= 100:
            w(f"2 {i} 50\n")
        else:
            if i % 10 == 0:
                w("3 49 50\n")
            else:
                v = (i % 100) + 1
                w(f"2 {v} 50\n")

    emit_case_end()

def case5_noops_absent_values_boundaries():
    # Large n; then many operations that are no-ops (x==y) or target absent values, plus some real swaps
    q = 200_000
    emit_case_begin(5, q)
    w = sys.stdout.write

    n_app = 50_000
    for i in range(n_app):
        w(f"1 {1 if (i % 2 == 0) else MAXV}\n")

    n_ops = q - n_app
    for i in range(1, n_ops + 1):
        r = i % 6
        if r == 0:
            w("2 123456 123456\n")   # no-op, likely absent
        elif r == 1:
            w("3 234567 234567\n")   # no-op swap
        elif r == 2:
            w("2 500000 500000\n")   # no-op on present value
        elif r == 3:
            w("3 1 500000\n")        # real swap
        elif r == 4:
            w("2 400000 1\n")        # likely absent -> no effect
        else:
            w("3 499999 500000\n")   # boundary swap, maybe affects later

    emit_case_end()

def case6_long_transmute_chain_composition():
    # Many identical values then long chain of transmutes: 1->2,2->3,... to test composition handling
    q = 250_000
    emit_case_begin(6, q)
    w = sys.stdout.write

    n_app = 100_000
    for _ in range(n_app):
        w("1 1\n")

    chain_len = 149_999  # values will progress from 1 to 150000
    for t in range(1, chain_len + 1):
        w(f"2 {t} {t+1}\n")

    # one final op to reach q
    w("3 150000 1\n")

    emit_case_end()

def case7_repeated_toggle_swaps_parity():
    # Many appends of two values, then many swaps toggling; parity matters
    q = 300_000
    emit_case_begin(7, q)
    w = sys.stdout.write

    n_app = 150_000
    for i in range(n_app):
        w(f"1 {10 if (i % 2 == 0) else 20}\n")

    n_ops = q - n_app
    for i in range(1, n_ops + 1):
        if i % 2 == 1:
            w("3 10 20\n")
        else:
            w("2 10 10\n")  # no-op to mix

    emit_case_end()

def case8_random_stress_large():
    # Large random mix; includes x==y sometimes; full value range
    q = 500_000
    emit_case_begin(8, q)
    w = sys.stdout.write
    rng = random.Random(12345)

    # Ensure at least one append
    w(f"1 {rng.randint(1, MAXV)}\n")

    for _ in range(q - 1):
        t = rng.random()
        if t < 0.40:
            w(f"1 {rng.randint(1, MAXV)}\n")
        elif t < 0.70:
            x = rng.randint(1, MAXV)
            if rng.random() < 0.05:
                y = x
            else:
                y = rng.randint(1, MAXV)
            w(f"2 {x} {y}\n")
        else:
            x = rng.randint(1, MAXV)
            if rng.random() < 0.05:
                y = x
            else:
                y = rng.randint(1, MAXV)
            w(f"3 {x} {y}\n")

    emit_case_end()

def case9_sorted_then_value_pair_swaps_reverse():
    # Start sorted increasing; then swap value-pairs to effectively reverse; then lots of no-op ops
    q = 350_000
    emit_case_begin(9, q)
    w = sys.stdout.write

    n_app = 175_000
    for v in range(1, n_app + 1):
        w(f"1 {v}\n")

    # Swap pairs (i, n+1-i) for i=1..n/2 => reverses value set
    pair_swaps = n_app // 2  # 87500
    for i in range(1, pair_swaps + 1):
        w(f"3 {i} {n_app + 1 - i}\n")

    remaining = q - n_app - pair_swaps  # 87500
    for i in range(1, remaining + 1):
        if i % 2 == 0:
            w("2 200000 200000\n")  # no-op (absent)
        else:
            w("3 300000 300000\n")  # no-op

    emit_case_end()

def case10_skewed_small_values_heavy_transforms():
    # Many appends among {1,2,3}; many operations among them + boundary 5e5
    q = 450_000
    emit_case_begin(10, q)
    w = sys.stdout.write

    n_app = 200_000
    vals = [1, 2, 3]
    for i in range(n_app):
        w(f"1 {vals[i % 3]}\n")

    n_ops = q - n_app  # 250000
    for i in range(1, n_ops + 1):
        r = i % 6
        if r == 0:
            w("2 1 2\n")
        elif r == 1:
            w("2 2 3\n")
        elif r == 2:
            w("2 3 1\n")
        elif r == 3:
            w("3 1 2\n")
        elif r == 4:
            w("3 2 3\n")
        else:
            w(f"2 1 {MAXV}\n")

    emit_case_end()

def main():
    emit_header()
    case1_max_descending_appends()
    case2_few_appends_many_transforms_time_order()
    case3_heavy_mix_swap_transmute()
    case4_many_duplicates_then_collapse()
    case5_noops_absent_values_boundaries()
    case6_long_transmute_chain_composition()
    case7_repeated_toggle_swaps_parity()
    case8_random_stress_large()
    case9_sorted_then_value_pair_swaps_reverse()
    case10_skewed_small_values_heavy_transforms()

if __name__ == "__main__":
    main()
