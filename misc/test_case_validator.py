
import sys

MAXQ = 5 * 10**5
MAXV = 5 * 10**5

def is_digits(s: str) -> bool:
    return len(s) > 0 and all('0' <= c <= '9' for c in s)

def bad_spacing_or_chars(line: str) -> bool:
    # Strict: no leading/trailing spaces, no tabs/CR, tokens separated by single spaces only.
    if line == "":
        return True
    if '\t' in line or '\r' in line:
        return True
    if line != line.strip(" "):
        return True
    if "  " in line:  # consecutive spaces not allowed
        return True
    return False

def validate():
    data = sys.stdin.buffer.read().splitlines()
    if not data:
        return False

    i = 0
    nlines = len(data)

    while i < nlines:
        # ---- read q line ----
        try:
            line = data[i].decode('utf-8')
        except Exception:
            return False

        if bad_spacing_or_chars(line):
            return False

        parts = line.split(" ")
        if len(parts) != 1 or not is_digits(parts[0]):
            return False

        try:
            q = int(parts[0])
        except Exception:
            return False

        if not (1 <= q <= MAXQ):
            return False

        i += 1

        # ---- read q operations ----
        seen_type1 = False
        for _ in range(q):
            if i >= nlines:
                return False
            try:
                line = data[i].decode('utf-8')
            except Exception:
                return False

            if bad_spacing_or_chars(line):
                return False

            parts = line.split(" ")
            if len(parts) < 1 or not is_digits(parts[0]):
                return False

            try:
                t = int(parts[0])
            except Exception:
                return False

            if t == 1:
                if len(parts) != 2 or (not is_digits(parts[1])):
                    return False
                x = int(parts[1])
                if not (1 <= x <= MAXV):
                    return False
                seen_type1 = True

            elif t == 2 or t == 3:
                if len(parts) != 3 or (not is_digits(parts[1])) or (not is_digits(parts[2])):
                    return False
                x = int(parts[1])
                y = int(parts[2])
                if not (1 <= x <= MAXV and 1 <= y <= MAXV):
                    return False

            else:
                return False

            i += 1

        # Structural constraint: at least one operation of type 1 per test case
        if not seen_type1:
            return False

    return True


if __name__ == "__main__":
    sys.stdout.write("True" if validate() else "False")
