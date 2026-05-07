//! Brute-force the 20-card deck of all weight-3 vectors in GF(2)^6.
//!
//! We consider a "move" to be removing any 4-card subset whose XOR is zero.
//! We explore *all* possible sequences of moves from the full deck down to
//! 8 cards (or earlier terminal states with no legal move), with memoization.
//!
//! For every reachable 8-card residual, we test whether it can be partitioned
//! into two disjoint 4-matches (whose union is the residual).

use std::collections::{BTreeSet, HashMap};

const N: usize = 6;
const W: u32 = 3;
const DECK: usize = 20; // C(6,3)

type State = u32; // 20-bit mask
type MatchMask = u32; // 20-bit mask of 4 cards

fn popcount(x: u32) -> u32 {
    x.count_ones()
}

fn weight_w_masks(n: usize, w: u32) -> Vec<u8> {
    let mut out = Vec::new();
    let lim = 1u32 << n;
    for v in 0..lim {
        if v.count_ones() == w {
            out.push(v as u8);
        }
    }
    out
}

fn all_matches(cards: &[u8]) -> Vec<MatchMask> {
    let mut ms = Vec::new();
    for i in 0..cards.len() {
        for j in (i + 1)..cards.len() {
            for k in (j + 1)..cards.len() {
                for l in (k + 1)..cards.len() {
                    let x = cards[i] ^ cards[j] ^ cards[k] ^ cards[l];
                    if x == 0 {
                        let m = (1u32 << i) | (1u32 << j) | (1u32 << k) | (1u32 << l);
                        ms.push(m);
                    }
                }
            }
        }
    }
    ms
}

fn subset_of(sub: u32, sup: u32) -> bool {
    (sub & sup) == sub
}

fn splits_into_two_matches(state: State, matches: &[MatchMask]) -> bool {
    if popcount(state) != 8 {
        return false;
    }
    for &m1 in matches {
        if !subset_of(m1, state) {
            continue;
        }
        let rest = state ^ m1; // disjoint because m1 subset of state
        // Find a match exactly equal to rest
        for &m2 in matches {
            if m2 == rest {
                return true;
            }
        }
    }
    false
}

#[derive(Default)]
struct ExploreResult {
    reachable_8: BTreeSet<State>,
    terminal_lt8: u32,
    terminal_gt8: u32,
    visited: u32,
}

fn explore_all_to_8(
    state: State,
    matches: &[MatchMask],
    memo_moves: &mut HashMap<State, Vec<State>>,
    res: &mut ExploreResult,
) {
    res.visited += 1;

    let size = popcount(state);
    if size == 8 {
        res.reachable_8.insert(state);
        return;
    }
    if size < 8 {
        res.terminal_lt8 += 1;
        return;
    }

    // memoize successors to avoid re-scanning matches each time
    let succ = if let Some(v) = memo_moves.get(&state) {
        v.clone()
    } else {
        let mut nexts = Vec::new();
        for &m in matches {
            if subset_of(m, state) {
                nexts.push(state ^ m);
            }
        }
        memo_moves.insert(state, nexts.clone());
        nexts
    };

    if succ.is_empty() {
        res.terminal_gt8 += 1;
        return;
    }

    for ns in succ {
        explore_all_to_8(ns, matches, memo_moves, res);
    }
}

fn format_card(v: u8) -> String {
    let mut s = String::new();
    s.push('{');
    let mut first = true;
    for bit in 0..N {
        if (v >> bit) & 1 == 1 {
            if !first {
                s.push(',');
            }
            first = false;
            s.push_str(&format!("{bit}"));
        }
    }
    s.push('}');
    s
}

fn describe_state(state: State, cards: &[u8]) -> String {
    let mut vs = Vec::new();
    for i in 0..cards.len() {
        if (state >> i) & 1 == 1 {
            vs.push(format_card(cards[i]));
        }
    }
    vs.join(" ")
}

fn main() {
    let cards = weight_w_masks(N, W);
    assert_eq!(cards.len(), DECK);

    let matches = all_matches(&cards);
    let full: State = if DECK == 32 { u32::MAX } else { (1u32 << DECK) - 1 };

    println!("GF(2)^{N} weight-{W} deck size: {}", cards.len());
    println!("Total 4-matches (XOR=0) in full deck: {}", matches.len());

    let mut memo_moves: HashMap<State, Vec<State>> = HashMap::new();
    let mut res = ExploreResult::default();
    explore_all_to_8(full, &matches, &mut memo_moves, &mut res);

    println!("Visited nodes (with repetition): {}", res.visited);
    println!("Reachable 8-card residual states: {}", res.reachable_8.len());
    println!("Terminal states with <8 cards: {}", res.terminal_lt8);
    println!("Terminal states with >8 cards but no move: {}", res.terminal_gt8);

    let mut bad = Vec::new();
    for &s in res.reachable_8.iter() {
        if !splits_into_two_matches(s, &matches) {
            bad.push(s);
        }
    }

    if bad.is_empty() {
        println!("RESULT: Every reachable 8-card residual splits into two 4-matches.");
    } else {
        println!(
            "RESULT: Found {} reachable 8-card residual(s) that do NOT split into two 4-matches.",
            bad.len()
        );
        println!("First few counterexamples (as sets of bit positions 0..5):");
        for (idx, s) in bad.iter().take(5).enumerate() {
            println!("  #{idx}: {}", describe_state(*s, &cards));
        }
    }
}

