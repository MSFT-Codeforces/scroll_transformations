**Scroll Transformations**

Time Limit: **4 seconds**

Memory Limit: **128 MB**

A rune-smith maintains a scroll that is initially empty. You are given $q$ spells applied in order. Each spell affects the whole scroll (not a single position).

There are three types of spells:

1. **Inscribe**: `1 x`  
   Append the integer $x$ to the end of the scroll.

2. **Transmute**: `2 x y`  
   For every position $i$, if the current value equals $x$, replace it with $y$.

3. **Mirror-Swap**: `3 x y`  
   For every position $i$, replace $x$ with $y$ and replace $y$ with $x$ **simultaneously**.

After all spells are applied, let the final scroll be an array $S$ of length $n$ ($n \ge 1$). You must output:

1. The final array $S$ (space-separated).
2. The **discord score** of $S$, defined as the number of pairs $(i, j)$ such that $1 \le i < j \le n$ and $S[i] > S[j]$ (i.e., the inversion count).

**Input Format:-**

- The first line contains an integer $q$.
- The next $q$ lines describe spells in one of the forms:
  - `1 x`
  - `2 x y`
  - `3 x y`

**Output Format:-**

- Print the final scroll as space-separated integers on the first line.
- Print the discord score (inversion count) on the second line.

**Constraints:-**

- $1 \le q \le 5 \cdot 10^5$
- $1 \le x, y \le 5 \cdot 10^5$
- At least one spell is of type `1`.
**Examples:-**
 - **Input:**
```
6
1 1
1 500000
3 1 500000
2 500000 1
1 500000
3 1 500000
```

 - **Output:**
```
500000 500000 1
2
```

 - **Input:**
```
11
1 2
1 3
2 2 1
1 2
3 1 3
1 1
2 3 2
3 2 1
2 1 4
1 3
3 4 2
```

 - **Output:**
```
2 4 2 4 3
3
```

**Note:-**
In the first example, the scroll evolves as follows:

1. Start with $[]$.
2. Append $1$, append $500000$ \(\rightarrow [1, 500000]\).
3. Mirror-swap \(1\) and \(500000\) (simultaneously) \(\rightarrow [500000, 1]\).
4. Transmute \(500000 \rightarrow 1\) \(\rightarrow [1, 1]\).
5. Append \(500000\) \(\rightarrow [1, 1, 500000]\).
6. Mirror-swap \(1\) and \(500000\) \(\rightarrow [500000, 500000, 1]\).

For \(S = [500000, 500000, 1]\), the inversions are the pairs \((1,3)\) and \((2,3)\), so the discord score is \(2\).

In the first example, the sequence of spells includes both a transmute and multiple mirror-swaps; remember that a mirror-swap exchanges \(x\) and \(y\) at the same time, so all current \(x\) become \(y\) and all current \(y\) become \(x\) in one step.

In the first example, the final output array is therefore exactly the final scroll after applying all \(q\) spells, and the second output line is the number of pairs \((i,j)\) with \(i<j\) and \(S[i]>S[j]\).

In the first example, \(n=3\) so the inversion count can be verified by checking all \(\binom{3}{2}=3\) pairs.

In the first example, the pair \((1,2)\) is not an inversion because \(S[1]=S[2]=500000\) and inversions require a strict inequality.

In the first example, the computed discord score matches the sample output.

In the first example, the operations show that spells affect the entire current scroll, not only newly appended elements.

In the first example, after the transmute \(500000 \rightarrow 1\), both existing elements become equal, which later affects the result of the final mirror-swap.

In the first example, the final mirror-swap turns every \(1\) into \(500000\) and every \(500000\) into \(1\) simultaneously, producing the final arrangement.

In the first example, this final arrangement has two large values before a small value, creating exactly two inversions.

In the first example, this explains why the output is:
- first line: the final array,
- second line: the inversion count.

In the first example, no further transformations occur after the last mirror-swap, so the array printed is the final state.

In the first example, the inversion count is computed on this final state only.

In the first example, the key takeaway is to apply spells in order and count inversions at the end.

In the first example, note that transmute is one-way (\(x \rightarrow y\)), unlike mirror-swap which exchanges both.

In the first example, applying transmute before/after a swap can change the outcome, so operation order matters.

In the first example, the sample demonstrates both order-dependence and simultaneity.

In the second example, apply the spells in order to obtain the final scroll:

- After the first two appends: \([2,3]\).
- Transmute \(2 \rightarrow 1\): \([1,3]\).
- Append \(2\): \([1,3,2]\).
- Mirror-swap \(1\) and \(3\): \([3,1,2]\).
- Append \(1\): \([3,1,2,1]\).
- Transmute \(3 \rightarrow 2\): \([2,1,2,1]\).
- Mirror-swap \(2\) and \(1\): \([1,2,1,2]\).
- Transmute \(1 \rightarrow 4\): \([4,2,4,2]\).
- Append \(3\): \([4,2,4,2,3]\).
- Mirror-swap \(4\) and \(2\): \([2,4,2,4,3]\).

Thus \(S = [2,4,2,4,3]\). To compute the discord score, count pairs \((i,j)\) with \(i<j\) and \(S[i]>S[j]\); the inversions are:
\((2,3)\) since \(4>2\), \((2,5)\) since \(4>3\), and \((4,5)\) since \(4>3\), giving a total of \(3\).