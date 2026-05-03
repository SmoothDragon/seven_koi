"""math/verify.py - Seven Koi computational verification.

Implements the checks scheduled in math/NOTES.md §7.4. Currently:

  * Sanity: Sigma D = 0 (Lemma E ingredient).
  * Sanity: S* = {e_1, ..., e_7, 1} is an 8-card match with no 4-sub-match.
  * Monte Carlo: simulate randomized match-removal until 8 cards remain;
    measure how often the residual contains a 4-card sub-match.

Two Monte Carlo modes:

  Mode A: pick random 4-matches from the entire remaining deck until 8
          cards remain (no game-flow constraints). Tests *abstract*
          reachability of bad 8-card residuals.

  Mode B: maintain an L-card layout (default L = 8), pick random 4-matches
          from the layout only, replenish from the deck after each claim.
          Models real play under the L-card dealing convention. Also reports
          mid-game stalls (when the layout itself becomes a Sidon set).

Cards are encoded as integers in [0, 128) with odd Hamming weight.

Usage:
    python verify.py                      # default: 10k trials, both modes
    python verify.py --trials 100000 --mode a
    python verify.py --mode b --layout-size 9
"""

from __future__ import annotations

import argparse
import itertools
import random
from collections import Counter
from typing import Optional


DECK = tuple(v for v in range(128) if bin(v).count("1") % 2 == 1)
assert len(DECK) == 64

# S* from math/NOTES.md Lemma D: 7 unit vectors plus the all-ones vector.
S_STAR = frozenset([1 << i for i in range(7)] + [127])
assert len(S_STAR) == 8


def fmt(v: int) -> str:
    return f"{v:07b}"


def xor_all(cards) -> int:
    out = 0
    for v in cards:
        out ^= v
    return out


def all_4matches(cards):
    cards = list(cards)
    if len(cards) < 4:
        return []
    return [
        c for c in itertools.combinations(cards, 4)
        if c[0] ^ c[1] ^ c[2] ^ c[3] == 0
    ]


def has_4match(cards) -> bool:
    cards = list(cards)
    if len(cards) < 4:
        return False
    for c in itertools.combinations(cards, 4):
        if c[0] ^ c[1] ^ c[2] ^ c[3] == 0:
            return True
    return False


def random_4match(cards, max_tries: int = 2000) -> Optional[tuple]:
    """Return a uniformly random 4-card subset XOR-ing to 0, or None."""
    cards = list(cards)
    n = len(cards)
    if n < 4:
        return None
    # For small decks, enumerate exhaustively (fast and avoids rejection edge cases).
    if n <= 16:
        ms = all_4matches(cards)
        return random.choice(ms) if ms else None
    # Rejection sampling: each random 4-tuple has ~1/64 chance of being a match.
    for _ in range(max_tries):
        s = random.sample(cards, 4)
        if s[0] ^ s[1] ^ s[2] ^ s[3] == 0:
            return tuple(s)
    # Should be very rare; fall back to exhaustive.
    ms = all_4matches(cards)
    return random.choice(ms) if ms else None


def simulate_mode_a() -> Optional[frozenset]:
    """Pick random 4-matches from the whole remaining deck until 8 cards left."""
    deck = set(DECK)
    while len(deck) > 8:
        m = random_4match(deck)
        if m is None:
            return None
        deck.difference_update(m)
    return frozenset(deck)


def simulate_mode_b(layout_size: int = 8) -> tuple:
    """Maintain a layout of `layout_size` cards; find matches there only.

    Returns (status, layout_at_end, n_matches_claimed).
    status == "residual"  -> deck emptied normally; layout is the 8-card residual.
    status == "stuck"     -> the layout had no 4-card match (mid-game stall).
    """
    bag = list(DECK)
    random.shuffle(bag)
    layout = set(bag[:layout_size])
    deck_remaining = bag[layout_size:]
    n_matches = 0
    while deck_remaining:
        ms = all_4matches(layout)
        if not ms:
            return "stuck", frozenset(layout), n_matches
        m = random.choice(ms)
        layout.difference_update(m)
        n_to_deal = min(layout_size - len(layout), len(deck_remaining))
        for _ in range(n_to_deal):
            layout.add(deck_remaining.pop())
        n_matches += 1
    return "residual", frozenset(layout), n_matches


def sanity_checks():
    print("=== Sanity checks ===")
    assert xor_all(DECK) == 0
    print("  Sigma D = 0  OK  (across all 64 odd-weight cards; basis for Lemma E)")
    assert xor_all(S_STAR) == 0
    assert not has_4match(S_STAR)
    s_star_str = ", ".join(fmt(v) for v in sorted(S_STAR))
    print(f"  S* = {{{s_star_str}}}")
    print("    Sigma S* = 0  OK  (S* is itself an 8-card match)")
    print("    no 4-card sub-match  OK  (S* is unsplittable)")
    print()


def run_mode_a(n_trials: int) -> dict:
    print("=== Mode A: random matches from whole remaining deck ===")
    splittable = unsplittable = stuck = 0
    bad: Counter = Counter()
    for _ in range(n_trials):
        residual = simulate_mode_a()
        if residual is None:
            stuck += 1
            continue
        if has_4match(residual):
            splittable += 1
        else:
            unsplittable += 1
            bad[residual] += 1
    total = splittable + unsplittable
    print(f"  Trials: {n_trials}")
    print(f"  Stuck (no match in remaining deck before residual): {stuck}")
    print(f"  Reached 8-card residual: {total}")
    if total:
        print(f"  Splittable:   {splittable}/{total} = {100*splittable/total:.4f}%")
        print(f"  Unsplittable: {unsplittable}/{total} = {100*unsplittable/total:.4f}%")
    if bad:
        print(f"  Distinct unsplittable residuals: {len(bad)}")
        for res, count in bad.most_common(5):
            tag = "  <- S*" if res == S_STAR else ""
            print(f"    {count:6d} x  {[fmt(v) for v in sorted(res)]}{tag}")
    print()
    return {"splittable": splittable, "unsplittable": unsplittable,
            "stuck": stuck, "bad": bad}


def run_mode_b(n_trials: int, layout_size: int = 8) -> dict:
    print(f"=== Mode B: layout_size = {layout_size}, replenish from deck after each match ===")
    splittable = unsplittable = stuck_mid = 0
    bad: Counter = Counter()
    stuck_layouts: Counter = Counter()
    matches_dist: Counter = Counter()
    for _ in range(n_trials):
        status, layout, n_matches = simulate_mode_b(layout_size)
        matches_dist[n_matches] += 1
        if status == "stuck":
            stuck_mid += 1
            stuck_layouts[layout] += 1
            continue
        if has_4match(layout):
            splittable += 1
        else:
            unsplittable += 1
            bad[layout] += 1
    n_residuals = n_trials - stuck_mid
    print(f"  Trials: {n_trials}")
    print(f"  Mid-game stalls (no 4-match in {layout_size}-card layout): {stuck_mid}")
    print(f"  Reached 8-card residual: {n_residuals}")
    if n_residuals:
        print(f"  Splittable:   {splittable}/{n_residuals} = {100*splittable/n_residuals:.4f}%")
        print(f"  Unsplittable: {unsplittable}/{n_residuals} = {100*unsplittable/n_residuals:.4f}%")
    if bad:
        print(f"  Distinct unsplittable residuals: {len(bad)}")
        for res, count in bad.most_common(5):
            tag = "  <- S*" if res == S_STAR else ""
            print(f"    {count:6d} x  {[fmt(v) for v in sorted(res)]}{tag}")
    if stuck_layouts:
        print(f"  Distinct mid-game stuck layouts: {len(stuck_layouts)}")
        for lay, count in stuck_layouts.most_common(3):
            tag = "  <- S*" if lay == S_STAR else ""
            print(f"    {count:6d} x  {[fmt(v) for v in sorted(lay)]}{tag}")
    print()
    return {"splittable": splittable, "unsplittable": unsplittable,
            "stuck_mid": stuck_mid, "bad": bad, "stuck_layouts": stuck_layouts,
            "matches_dist": matches_dist}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--trials", type=int, default=10000)
    parser.add_argument("--mode", choices=["a", "b", "both"], default="both")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--layout-size", type=int, default=8,
                        help="Mode B layout size (typically 8 or 9)")
    args = parser.parse_args()

    random.seed(args.seed)
    sanity_checks()

    if args.mode in ("a", "both"):
        run_mode_a(args.trials)
    if args.mode in ("b", "both"):
        run_mode_b(args.trials, args.layout_size)


if __name__ == "__main__":
    main()
