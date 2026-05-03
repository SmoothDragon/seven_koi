/*!
Explore maximum strict Sidon set size inside GF(2)^n versus odd-weight subsets
(Seven Koi card slice). Mirrors the former Python verifier with faster incremental XOR checks.

Definition ( Lemma B XOR conditions in math/NOTES.md ):
• no distinct triple with a xor b xor c == 0
• no distinct quadruple with a xor b xor c xor d == 0
*/

use clap::Parser;
use rand::seq::SliceRandom;
use rand::rngs::StdRng;
use rand::SeedableRng;
use std::time::Instant;

#[derive(Parser)]
#[command(verbatim_doc_comment)]
struct Args {
    #[arg(long, default_value_t = 2)]
    min_n: u32,

    #[arg(long, default_value_t = 7)]
    max_n: u32,

    #[arg(long, default_value_t = 768)]
    greedy_runs: u32,

    /// |universe| at or below this runs exhaustive search (ambient n = 7 typically needs cutoff >= 127).
    #[arg(long, default_value_t = 34)]
    exact_cutoff: usize,

    /// Exhaustive DFS beyond --exact-cutoff up to |U|<=128 may still take substantial wall time (ambient |U|=127 is often impractical brute-force).
    #[arg(long)]
    risky_large_exhaust: bool,
}

#[inline]
fn odd_vectors_upto(n_bits: u32) -> Vec<u32> {
    let limit = 1u32 << n_bits;
    (1..limit)
        .filter(|&v| v.count_ones() % 2 == 1)
        .collect()
}

#[inline]
fn even_nonzero_vectors(n_bits: u32) -> Vec<u32> {
    let limit = 1u32 << n_bits;
    (1..limit)
        .filter(|&v| v.count_ones() % 2 == 0)
        .collect()
}

#[inline]
fn all_nonzero_vectors(n_bits: u32) -> Vec<u32> {
    let limit = 1u32 << n_bits;
    (1..limit).collect()
}

/// Incremental Lemma B check: `chosen` is already strict Sidon, test adding `x` (must not appear in chosen).
#[inline]
fn can_extend(chosen: &[u32], x: u32) -> bool {
    debug_assert!(
        chosen.iter().all(|&c| c != x),
        "universe construction should omit duplicates before extend"
    );
    if x == 0 {
        return false;
    }

    let n = chosen.len();

    // New triples: x with two distinct elements from chosen  => x xor a xor b != 0
    for i in 0..n {
        for j in i + 1..n {
            if chosen[i] ^ chosen[j] ^ x == 0 {
                return false;
            }
        }
    }

    // New quadruples involving x exactly once: x xor a xor b xor c != 0 for distinct a,b,c in chosen
    for i in 0..n {
        for j in i + 1..n {
            for k in j + 1..n {
                if chosen[i] ^ chosen[j] ^ chosen[k] ^ x == 0 {
                    return false;
                }
            }
        }
    }

    true
}

#[cfg(debug_assertions)]
fn verify_strict_sidon(vals: &[u32]) -> bool {
    let n = vals.len();
    for i in 0..n {
        for j in i + 1..n {
            for k in j + 1..n {
                if vals[i] ^ vals[j] ^ vals[k] == 0 {
                    return false;
                }
            }
        }
    }
    if n >= 4 {
        for i in 0..n {
            for j in i + 1..n {
                for k in j + 1..n {
                    for l in k + 1..n {
                        if vals[i] ^ vals[j] ^ vals[k] ^ vals[l] == 0 {
                            return false;
                        }
                    }
                }
            }
        }
    }
    true
}

fn greedy_max_sidon(universe: &[u32], seed: u64) -> Vec<u32> {
    let mut rnd = StdRng::seed_from_u64(seed);
    let mut u = universe.to_vec();
    u.shuffle(&mut rnd);
    let mut chosen: Vec<u32> = Vec::new();
    for &x in &u {
        if can_extend(&chosen, x) {
            chosen.push(x);
        }
    }
    chosen.sort_unstable();
    chosen
}

fn best_greedy(universe: &[u32], runs: u32) -> (usize, Vec<u32>) {
    let mut best: Vec<u32> = Vec::new();
    for s in 0..runs {
        let cand = greedy_max_sidon(universe, s as u64);
        if cand.len() > best.len() {
            best = cand;
        }
    }
    (best.len(), best)
}

fn exhaustive_max_sidon(universe: &[u32]) -> (usize, Vec<u32>) {
    let mut u = universe.to_vec();
    u.sort_unstable();
    let m = u.len();
    let mut best_k = 0usize;
    let mut best_set = Vec::<u32>::new();

    fn dfs(
        u: &[u32],
        m: usize,
        start_idx: usize,
        chosen: &mut Vec<u32>,
        best_k: &mut usize,
        best_set: &mut Vec<u32>,
    ) {
        if chosen.len() + (m - start_idx) < *best_k {
            return;
        }
        if chosen.len() > *best_k {
            *best_k = chosen.len();
            *best_set = chosen.clone();
        }
        if start_idx >= m {
            return;
        }
        for j in start_idx..m {
            let x = u[j];
            if can_extend(chosen, x) {
                chosen.push(x);
                dfs(u, m, j + 1, chosen, best_k, best_set);
                chosen.pop();
            }
        }
    }

    let mut chosen = Vec::new();
    dfs(&u, m, 0, &mut chosen, &mut best_k, &mut best_set);

    best_set.sort_unstable();
    #[cfg(debug_assertions)]
    {
        assert!(best_set.is_empty() || verify_strict_sidon(&best_set));
    }
    (best_k, best_set)
}

fn odd_triple_always_nonzero(odd_u: &[u32]) -> bool {
    let n = odd_u.len();
    for i in 0..n {
        for j in i + 1..n {
            for k in j + 1..n {
                if odd_u[i] ^ odd_u[j] ^ odd_u[k] == 0 {
                    return false;
                }
            }
        }
    }
    true
}

fn fmt_vec(v: u32, n_bits: u32) -> String {
    format!("{:0width$b}", v, width = n_bits as usize)
}

fn run_slice(
    n_bits: u32,
    label: &str,
    univ: &[u32],
    greedy_runs: u32,
    exact_cutoff: usize,
    risky_large_exhaust: bool,
) {
    let (gsz, _gex) = best_greedy(univ, greedy_runs);

    let exhaustive_ok = univ.len() <= exact_cutoff || (risky_large_exhaust && univ.len() <= 128);

    if exhaustive_ok {
        let t0 = Instant::now();
        let (esz, eex) = exhaustive_max_sidon(univ);
        let dt = t0.elapsed().as_secs_f64();

        let take = eex.len().min(10);
        let sample: String = eex[..take]
            .iter()
            .map(|v| fmt_vec(*v, n_bits) + " ")
            .collect();

        println!(
            "   {:28}  exact {:3}  greedy {:3}  ({:5.2}s)  exemplar(bits): {}",
            label, esz, gsz, dt, sample
        );
        if esz != gsz {
            println!("      ! greedy undershot exact by {}", esz - gsz);
        }
    } else {
        println!(
            "   {:28}  exact  —    greedy {:3}         (|U|={}, raise --exact-cutoff or --risky-large-exhaust)",
            label,
            gsz,
            univ.len()
        );
    }
}

fn main() {
    let args = Args::parse();

    println!(
        "Strict Sidon ( Lemma B XOR conditions ) slices:\n\
         • all_nonzero         — playable mask if every nonzero n-bit glyph existed\n\
         • odd_weight_only      — Seven Koi legal vectors (excluding omitted-koi analogue)\n\
         • even_nonzero_only    — parity contrast slice"
    );

    for n_bits in args.min_n..=args.max_n {
        let full = all_nonzero_vectors(n_bits);
        let odd_u = odd_vectors_upto(n_bits);
        let even_u = even_nonzero_vectors(n_bits);

        println!("\n===== n_bits = {} =====", n_bits);
        println!(
            "   |GF(2)^n\\{{0}}| = {} ; |odd*| = {} ; |even*\\{{0}}| = {}",
            full.len(),
            odd_u.len(),
            even_u.len()
        );
        let lemma_odd = odd_triple_always_nonzero(&odd_u);
        println!(
            "   Lemma C shortcut (distinct odd triples never XOR to 0): {}",
            lemma_odd
        );

        run_slice(
            n_bits,
            "all_nonzero",
            &full,
            args.greedy_runs,
            args.exact_cutoff,
            args.risky_large_exhaust,
        );
        run_slice(
            n_bits,
            "odd_weight_only",
            &odd_u,
            args.greedy_runs,
            args.exact_cutoff,
            args.risky_large_exhaust,
        );
        run_slice(
            n_bits,
            "even_nonzero_only",
            &even_u,
            args.greedy_runs,
            args.exact_cutoff,
            args.risky_large_exhaust,
        );
    }

    println!(
        "\n\nTakeaways:\n\
         • Ambient all-nonzero GF(2)^n counts should coincide with literature / OEIS A394031 for n where exact search finishes.\n\
         • Odd slice max can shrink vs ambient (seven-bit odd universe already forces smaller Sidon extremes than thirteen-card ambient proofs).\n\
         • When exact search is skipped, greedy usually matches modest-n maxima — increase --greedy-runs if worried."
    );
}
