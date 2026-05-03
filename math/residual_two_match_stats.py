#!/usr/bin/env python3
"""
Estimate P(residual tableau has exactly 8 cards AND it splits into two 4-XOR matches)
under Mode B (fixed L, random legal 4-match in layout, replenish from pile).

Uses the odd-weight decks: n=6 bits => 32-card beginner analogue, n=7 => 64-card standard.

For an 8-card set R with xor(R)=0 (always true along these removal paths — see Lemma-style
conservation), existence of one 4-card XOR-zero subset implies the complement is also a match.

Usage:
    python3 math/residual_two_match_stats.py --trials 100000 --seed 1
"""

from __future__ import annotations

import argparse
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from layout_stall_sweep import all_4matches, odd_deck, simulate_mode_b  # noqa: E402


def splittable_two_fours(cards: frozenset[int]) -> bool:
    """True iff the 8 cards can partition into two disjoint 4-card XOR-zero subsets."""
    if len(cards) != 8:
        return False
    return bool(all_4matches(list(cards)))


def run_block(
    name: str,
    deck: tuple[int, ...],
    layout_size: int,
    trials: int,
    seed: int,
) -> None:
    rng = random.Random(seed)
    stuck = residuals = eight = splittable = 0
    size_ctr: dict[int, int] = {}

    for t in range(trials):
        sub = random.Random(rng.randint(1, 2**30))
        status, layout, _n = simulate_mode_b(deck, layout_size, sub)
        if status != "residual":
            stuck += 1
            continue
        residuals += 1
        k = len(layout)
        size_ctr[k] = size_ctr.get(k, 0) + 1
        if k == 8:
            eight += 1
            if splittable_two_fours(layout):
                splittable += 1

    print(f"\n=== {name} ===")
    print(f"deck |D| = {len(deck)}, baseline layout L₀ = {layout_size}, trials = {trials}, seed_base = {seed}")
    print(f"mid-game stall: {stuck} ({100 * stuck / trials:.4f}%)")
    print(f"reached clean residual (pile empty): {residuals} ({100 * residuals / trials:.4f}%)")
    if residuals:
        print("residual size histogram (top sizes):")
        for sz, c in sorted(size_ctr.items(), key=lambda x: -x[1])[:8]:
            print(f"  |R|={sz}: {c} ({100 * c / residuals:.2f}% of residuals)")
    if eight:
        print(
            f"P(|R|=8 AND two 4-matches) among all trials: {splittable}/{trials} = {100 * splittable / trials:.4f}%"
        )
        print(
            f"P(two 4-matches | |R|=8): {splittable}/{eight} = {100 * splittable / eight:.4f}%"
        )
    else:
        print("no trials ended with |R| = 8 — cannot estimate conditional split rate")
    print(f"trials with |R| = 8: {eight} ({100 * eight / trials:.4f}% of all trials)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--trials", type=int, default=100_000)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    run_block(
        "Six koi (32-card odd-weight deck, L₀ = 8)",
        odd_deck(6),
        8,
        args.trials,
        args.seed,
    )
    run_block(
        "Seven koi (64-card odd-weight deck, L₀ = 10)",
        odd_deck(7),
        10,
        args.trials,
        args.seed + 1_000_003,
    )


if __name__ == "__main__":
    main()
