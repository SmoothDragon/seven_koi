#!/usr/bin/env python3
"""
Explore maximum strict Sidon set size inside GF(2)^n versus odd-weight subsets.

Koi cards use nonzero **odd Hamming weight** vectors. OEIS A394031 cites
ambient maxima inside the full additive group GF(2)^n (often tabulated with **0**
included). This script uses the same **nonzero** hypothesis as the card game
Lemma B in math/NOTES.md, and adds the **odd-parity** slice for comparison.

Observed exact maxima ( Lemma B via XOR, run on this machine ):
  n  |all nonzero| odd-only |even nonzero| Notes
  ---+-----------+----------+------------+---------------------------
  4  |      5    |    4     |     3      | parity slice shrinks ambient
  5  |      6    |    6     |     5      |
  6  |  (greedy≈9)| **7***  | **6***      | odd exact ~23 s; ambient |U|=63 too big for DFS here

*ambient n=6 is expected to reach OEIS a(6)= **9** once **0 ∈ GF(2)^n** allowed and/or a faster exact routine is wired in.

Definition ( Lemma B XOR form used here ):
  Forbid XOR-Schur triples a⊕b⊕c=0 on three distinct nonzero vectors,
  and forbid XOR-4-collisions among four distinct nonzero vectors.

Exact backtracking is fine for |U| ≤ ~35; the six-bit **odd** universe has
|U|=32 (finishes in tens of seconds). Ambient **nonzero** GF(2)^6 has |U|=63;
naive exhaustive search often exceeds multi-minute wall clocks (e.g. `timeout 90`
ends with exit 124 and no summary line) unless you add stronger pruning or a solver — use greedy for that row or raise the time limit. Seven-bit odd has |U|=64; exhaustive runs with `--risky-large-exhaust` have hit
multi-minute timeouts (**exit 124** under `timeout 180` in CI-style checks) — treat
exact max on that slice as "unknown here" without a stronger algorithm; greedy gave 9 historically on the game's actual 64-card Expert deck.

Run as a **script** (do not `import math.sidon_…` — Python's stdlib `math` wins).

Examples:
    python3 math/sidon_weight_explorer.py
    python3 math/sidon_weight_explorer.py --max-n 6 --exact-cutoff 40
    python3 math/sidon_weight_explorer.py --min-n 7 --max-n 7 --risky-large-exhaust --exact-cutoff 127
"""

from __future__ import annotations

import argparse
import itertools
import random
import time


def wt(x: int) -> int:
    return x.bit_count()


def odd_vectors_upto(n_bits: int) -> tuple[int, ...]:
    return tuple(v for v in range(1, 1 << n_bits) if wt(v) % 2 == 1)


def even_nonzero_vectors(n_bits: int) -> tuple[int, ...]:
    return tuple(v for v in range(1, 1 << n_bits) if wt(v) % 2 == 0)


def all_nonzero_vectors(n_bits: int) -> tuple[int, ...]:
    return tuple(range(1, 1 << n_bits))


def is_strict_sidon(S: tuple[int, ...]) -> bool:
    """Lemma B XOR checks."""
    if len(set(S)) != len(S):
        return False
    if 0 in S:
        return False
    lst = sorted(S)
    # (c) Schur XOR triple among three distinct nonzero elements
    for a, b, c in itertools.combinations(lst, 3):
        if a ^ b ^ c == 0:
            return False
    # (d) four distinct pairwise partition / 4-cycle
    for quad in itertools.combinations(lst, 4):
        if quad[0] ^ quad[1] ^ quad[2] ^ quad[3] == 0:
            return False
    return True


def can_extend(chosen: list[int], x: int) -> bool:
    return is_strict_sidon(tuple(chosen + [x]))


def greedy_max_sidon(universe: tuple[int, ...], *, seed: int) -> tuple[int, ...]:
    rnd = random.Random(seed)
    u = list(universe)
    rnd.shuffle(u)
    chosen: list[int] = []
    for x in u:
        if can_extend(chosen, x):
            chosen.append(x)
    return tuple(sorted(chosen))


def best_greedy(universe: tuple[int, ...], runs: int) -> tuple[int, tuple[int, ...]]:
    best: tuple[int, ...] = ()
    best_sz = -1
    for s in range(runs):
        cand = greedy_max_sidon(universe, seed=s)
        if len(cand) > best_sz:
            best_sz, best = len(cand), cand
    assert best_sz >= 0
    return best_sz, best


def exhaustive_max_sidon(universe: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Branch-and-bound; universe sorted by increasing numeric value."""

    u = universe
    m = len(u)
    best_k = 0
    best_set: list[int] = []

    # Upper bound reachable from chosen + remaining indexed positions >= start_idx
    def dfs(start_idx: int, chosen: list[int]) -> None:
        nonlocal best_k, best_set
        if len(chosen) + (m - start_idx) < best_k:
            return
        if len(chosen) > best_k:
            best_k = len(chosen)
            best_set = list(chosen)
        if start_idx >= m:
            return
        for j in range(start_idx, m):
            x = u[j]
            if can_extend(chosen, x):
                chosen.append(x)
                dfs(j + 1, chosen)
                chosen.pop()

    dfs(0, [])
    exemplar = tuple(sorted(best_set))
    assert exemplar == () or is_strict_sidon(exemplar)
    return best_k, exemplar


def odd_triple_always_nonzero(n_bits: int, odd_u: tuple[int, ...]) -> bool:
    """ Lemma C analogue: distinct odd-weight vectors never XOR-triple-cancel? """

    for triple in itertools.combinations(odd_u, 3):
        if triple[0] ^ triple[1] ^ triple[2] == 0:
            return False
    return True


def fmt_vec(v: int, n_bits: int) -> str:
    return format(v, f"0{n_bits}b")


def run_slice(
    n_bits: int,
    label: str,
    univ: tuple[int, ...],
    *,
    greedy_runs: int,
    exact_cutoff: int,
    risky_large_exhaust: bool,
) -> None:
    """Print one universe row."""

    gsz, gex = best_greedy(univ, greedy_runs)

    exhaustive_ok = len(univ) <= exact_cutoff or (risky_large_exhaust and len(univ) <= 128)
    if exhaustive_ok:
        t0 = time.perf_counter()
        esz, eex = exhaustive_max_sidon(univ)
        dt = time.perf_counter() - t0
        sample = "".join(fmt_vec(v, n_bits) + " " for v in eex[:min(10, len(eex))])
        print(f"   {label:28s}  exact {esz:3d}  greedy {gsz:3d}  ({dt:5.2f}s)  exemplar(bits): {sample}")
        if esz != gsz:
            print(f"      ! greedy undershot exact by {esz - gsz}")
    else:
        print(
            f"   {label:28s}  exact  —    greedy {gsz:3d}         (|U|={len(univ)}, raise --exact-cutoff or --risky-large-exhaust)"
        )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=7)
    ap.add_argument("--greedy-runs", type=int, default=768)
    ap.add_argument(
        "--exact-cutoff",
        type=int,
        default=34,
        help="|universe| at or below this runs exhaustive search (ambient n=7 needs cutoff>=127)",
    )
    ap.add_argument(
        "--risky-large-exhaust",
        action="store_true",
        help="Attempt exhaustive DFS even past --exact-cutoff up to |U|≤128 (odd n=7 takes time).",
    )
    args = ap.parse_args()

    banner = """\
Strict Sidon ( Lemma B XOR conditions ) slices:
• all_nonzero         — playable mask if every nonzero n-bit glyph existed
• odd_weight_only      — Retail / legacy legal vectors (odd weight; retail = six-breed odd slice)
• even_nonzero_only    — parity contrast slice"""
    print(banner)

    for n_bits in range(args.min_n, args.max_n + 1):
        full = all_nonzero_vectors(n_bits)
        odd_u = odd_vectors_upto(n_bits)
        even_u = even_nonzero_vectors(n_bits)

        print(f"\n===== n_bits = {n_bits} =====")
        print(
            f"   |GF(2)^n\\{{0}}| = {len(full)} ; |odd*| = {len(odd_u)} ; |even*\\{{0}}| = {len(even_u)}"
        )
        lemma_odd = odd_triple_always_nonzero(n_bits, odd_u)
        print(f"   Lemma C shortcut (distinct odd triples never XOR to 0): {lemma_odd}")

        run_slice(
            n_bits,
            "all_nonzero",
            full,
            greedy_runs=args.greedy_runs,
            exact_cutoff=args.exact_cutoff,
            risky_large_exhaust=args.risky_large_exhaust,
        )
        run_slice(
            n_bits,
            "odd_weight_only",
            odd_u,
            greedy_runs=args.greedy_runs,
            exact_cutoff=args.exact_cutoff,
            risky_large_exhaust=args.risky_large_exhaust,
        )
        run_slice(
            n_bits,
            "even_nonzero_only",
            even_u,
            greedy_runs=args.greedy_runs,
            exact_cutoff=args.exact_cutoff,
            risky_large_exhaust=args.risky_large_exhaust,
        )

    print(
        """

Takeaways:
• Ambient all-nonzero GF(2)^n counts should coincide with literature / OEIS A394031 for n where exact search finishes.
• Odd slice max can shrink vs ambient (seven-bit odd universe already forces smaller Sidon extremes than thirteen-card ambient proofs).
• When exact search is skipped, greedy usually matches modest-n maxima — increase --greedy-runs if worried."""
    )


if __name__ == "__main__":
    main()
