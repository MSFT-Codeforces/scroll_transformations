
def build_case(ops):
    return str(len(ops)) + "\n" + "\n".join(ops)

cases = []

# 1) Minimum input (q=1, n=1)
cases.append(build_case([
    "1 1"
]))

# 2) Already sorted increasing (inversion count = 0)
cases.append(build_case([
    "1 1",
    "1 2",
    "1 3",
    "1 4",
    "1 5"
]))

# 3) Strictly decreasing (high inversions for small n)
cases.append(build_case([
    "1 5",
    "1 4",
    "1 3",
    "1 2",
    "1 1"
]))

# 4) Collapse to all equal via transmute (duplicates/ties)
cases.append(build_case([
    "1 1",
    "1 2",
    "1 3",
    "1 4",
    "2 1 9",
    "2 2 9",
    "2 3 9",
    "2 4 9"
]))

# 5) Many duplicates with alternating pattern
cases.append(build_case([
    "1 2",
    "1 1",
    "1 2",
    "1 1",
    "1 2",
    "1 1"
]))

# 6) Mirror-Swap simultaneity (both x and y present)
cases.append(build_case([
    "1 1",
    "1 2",
    "1 1",
    "1 2",
    "3 1 2"
]))

# 7) No-op operations (x == y), including on present and absent values
cases.append(build_case([
    "1 3",
    "1 4",
    "1 3",
    "2 3 3",
    "3 4 4",
    "2 5 5"
]))

# 8) Transform values not present (should be safe no-ops)
cases.append(build_case([
    "1 1",
    "1 2",
    "2 9 1",
    "3 8 7",
    "2 7 6"
]))

# 9) Time-order: append after a transform should not be affected by earlier transforms
cases.append(build_case([
    "1 1",
    "2 1 2",
    "1 1",
    "2 1 3"
]))

# 10) Long remap chain + append in the middle (composition + timing)
cases.append(build_case([
    "1 1",
    "1 2",
    "2 1 2",
    "2 2 3",
    "1 2",
    "2 3 4",
    "2 2 5"
]))

# 11) Mix swap and transmute to test interactions
cases.append(build_case([
    "1 1",
    "1 2",
    "1 3",
    "3 1 3",
    "2 3 2"
]))

# 12) Repeated toggling swaps (parity errors)
cases.append(build_case([
    "1 1",
    "1 2",
    "1 1",
    "1 2",
    "3 1 2",
    "3 1 2",
    "3 1 2"
]))

# 13) Few appends, many transforms (stress transform handling pattern)
cases.append(build_case([
    "1 1",
    "2 1 2",
    "3 2 3",
    "2 3 4",
    "3 4 5",
    "2 5 1",
    "3 1 2",
    "2 2 2",
    "3 2 4",
    "2 4 3"
]))

# 14) Value boundaries (includes 500000)
cases.append(build_case([
    "1 1",
    "1 500000",
    "3 1 500000",
    "2 500000 1",
    "1 500000",
    "3 1 500000"
]))

# 15) Random-like mixed operations (general bug catcher)
cases.append(build_case([
    "1 2",
    "1 3",
    "2 2 1",
    "1 2",
    "3 1 3",
    "1 1",
    "2 3 2",
    "3 2 1",
    "2 1 4",
    "1 3",
    "3 4 2"
]))

print("Test Cases:")
for i, tc in enumerate(cases, 1):
    print(f"Input {i}:")
    print(tc)
    if i != len(cases):
        print()
