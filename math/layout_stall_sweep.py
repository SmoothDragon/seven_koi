#!/usr/bin/env python3
"""
Empirical Mode-B stall sweep: odd-weight XOR deck in GF(2)^n, fixed layout size L.

Mirrors math/verify.py simulate_mode B — shuffle deck, lay out L cards, repeatedly
pick a uniformly random legal 4-card XOR match from the tableau, replenish from the
pile until no cards remain OR the tableau admits no 4-match while the pile is
non-empty (mid-game stall).

Usage:
    python3 math/layout_stall_sweep.py --trials 20000 --seed 1
    python3 math/layout_stall_sweep.py --n-bits 7 --trials 50000 --layout-min 8 --layout-max 12
"""

from __future__ import annotations

import argparse
from collections import defaultdict
import random


def odd_deck(n_bits: int) -> tuple[int, ...]:
    d = tuple(v for v in range(1, 1 << n_bits) if v.bit_count() % 2 == 1)
    assert len(d) == 2 ** (n_bits - 1)
    return d


def all_4matches(cards):
    """All 4-element subsets XORing to zero. O(L^2) via pair sums a^b = c^d."""
    cards = list(cards)
    nlen = len(cards)
    if nlen < 4:
        return []
    pairs_by_xor: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for i in range(nlen):
        for j in range(i + 1, nlen):
            pairs_by_xor[cards[i] ^ cards[j]].append((i, j))
    out: list[tuple[int, int, int, int]] = []
    seen: set[frozenset[int]] = set()
    for same in pairs_by_xor.values():
        mlen = len(same)
        for pi in range(mlen):
            ia, ib = same[pi]
            for pj in range(pi + 1, mlen):
                ic, jd = same[pj]
                if ia in (ic, jd) or ib in (ic, jd):
                    continue
                key = frozenset((cards[ia], cards[ib], cards[ic], cards[jd]))
                if key in seen:
                    continue
                seen.add(key)
                out.append((cards[ia], cards[ib], cards[ic], cards[jd]))
    return out


def simulate_mode_b(
    deck: tuple[int, ...], layout_size: int, rng: random.Random
) -> tuple[str, frozenset, int]:
    if layout_size > len(deck):
        raise ValueError("layout_size cannot exceed deck size")
    bag = list(deck)
    rng.shuffle(bag)
    layout = set(bag[:layout_size])
    deck_remaining = bag[layout_size:]
    n_matches = 0
    while deck_remaining:
        ms = all_4matches(layout)
        if not ms:
            return "stuck", frozenset(layout), n_matches
        m = rng.choice(ms)
        layout.difference_update(m)
        n_to_deal = min(layout_size - len(layout), len(deck_remaining))
        for _ in range(n_to_deal):
            layout.add(deck_remaining.pop())
        n_matches += 1
    return "residual", frozenset(layout), n_matches


def stall_rate(deck: tuple[int, ...], layout_size: int, trials: int, seed: int) -> float:
    stuck = 0
    for t in range(trials):
        rng = random.Random(seed + t)
        status, _lay, _nm = simulate_mode_b(deck, layout_size, rng)
        if status == "stuck":
            stuck += 1
    return stuck / trials


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--trials", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--n-bits", type=int, nargs="+", default=[4, 5, 6, 7])
    ap.add_argument("--layout-min", type=int, default=None, help="Minimum L (default max(4,n))")
    ap.add_argument(
        "--layout-max",
        type=int,
        default=None,
        help="Maximum L (default min(|D|-1, 24); use |D|-1 for full sweep but large L is slow)",
    )
    args = ap.parse_args()

    print(
        "Mode-B mid-game stall rate = fraction of trials where the L-card tableau\n"
        "contains NO 4-card XOR match while the facedown pile is still non-empty.\n"
        f"Deck = all odd-weight nonzero vectors in GF(2)^n, |D|=2^(n-1). Trials={args.trials}, seed base={args.seed}.\n"
    )
    print(f'{"n":>2} {"|D|":>4} {"L":>3} {"stall%":>9}')
    print("-" * 28)

    for n in args.n_bits:
        deck = odd_deck(n)
        dn = len(deck)
        lmin = args.layout_min if args.layout_min is not None else max(4, n)
        layout_cap = 24
        if args.layout_max is not None:
            lmax = args.layout_max
        else:
            lmax = min(dn - 1, layout_cap)
        lmin = max(4, min(lmin, dn - 1))
        lmax = max(lmin, min(lmax, dn - 1))
        for L in range(lmin, lmax + 1):
            block_seed = args.seed + n * 1_000_003 + L * 17_711
            pct = stall_rate(deck, L, args.trials, block_seed)
            print(f"{n:2d} {dn:4d} {L:3d} {100 * pct:9.4f}%")


if __name__ == "__main__":
    main()
