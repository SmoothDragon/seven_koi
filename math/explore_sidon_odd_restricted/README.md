# explore_sidon_odd_restricted — Rust

Explores maximum **strict Sidon** set size inside `GF(2)^n` for three universes (**all nonzero**, **odd weight only**, **even nonzero only**).

This replaces the old Python prototype with **Rust** for speed. Improvements:

- **Incremental** Lemma B checks when extending a candidate set (`can_extend`): **O(|S|³)** vs re-validating **O(|S|⁴)** on every DFS step as in naive Python loops.
- DFS uses the same **numeric ascending** universe ordering as the old Python enumerator (combined with incremental `can_extend`).

Exhaustive search is still exponential: **"|U|" in the mid‑60s (seven‑bit odd slice)** can remain **minutes+** despite the optimizations. Prefer the default **`--exact-cutoff 34`** for quick scripting, or **`--risky-large-exhaust`** knowing full ambient **`|U| = 127`** is usually impractical to finish.

## Build / run

```bash
cd math/explore_sidon_odd_restricted
cargo build --release
cargo run --release                      # mirrors old Python CLI defaults (n = 2..7)
cargo run --release -- --help
```

Examples:

```bash
cargo run --release -- --max-n 6 --exact-cutoff 63

# Exact max on legacy seven-species odd universe (|U| = 64); may still take noticeable wall time:
cargo run --release -- --min-n 7 --max-n 7 --exact-cutoff 64
```
