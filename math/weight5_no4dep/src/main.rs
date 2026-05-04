//! Largest subset of **all** weight-5 vectors in GF(2)^7 such that no four
//! distinct vectors are linearly dependent (every 4-subset has rank 4).
//!
//! There are C(7,5) = 21 such vectors. Same method as `weight3_no4dep`:
//! forbid-table + greedy lower bound + branch-and-bound.

const N: usize = 21;
const NUM_QUADS: usize = comb_21_4();
const NUM_TRIPLES: usize = comb_21_3();

const fn comb_21_4() -> usize {
    21 * 20 * 19 * 18 / 24
}

const fn comb_21_3() -> usize {
    21 * 20 * 19 / 6
}

fn popcount7(x: u8) -> u32 {
    x.count_ones()
}

fn weight5_masks() -> [u8; N] {
    let mut out = [0u8; N];
    let mut i = 0usize;
    let mut v = 0u8;
    while v < 128 {
        if popcount7(v) == 5 {
            out[i] = v;
            i += 1;
        }
        v += 1;
    }
    assert_eq!(i, N);
    out
}

/// Pascal binomials binom[n][k] for n <= 21, k <= 4
fn binom_tbl() -> [[u32; 5]; 22] {
    let mut b = [[0u32; 5]; 22];
    for n in 0..22 {
        b[n][0] = 1;
        for k in 1..=4.min(n) {
            b[n][k] = b[n - 1][k - 1] + b[n - 1][k];
        }
    }
    b
}

#[cfg_attr(not(test), allow(dead_code))]
fn quad_index_lex(n: usize, i: usize, j: usize, k: usize, l: usize, b: &[[u32; 5]; 22]) -> usize {
    debug_assert!(i < j && j < k && k < l && l < n);
    let mut idx = 0usize;
    for f in 0..i {
        idx += b[n - f - 1][3] as usize;
    }
    for s in (i + 1)..j {
        idx += b[n - s - 1][2] as usize;
    }
    for t in (j + 1)..k {
        idx += b[n - t - 1][1] as usize;
    }
    for u in (k + 1)..l {
        idx += b[n - u - 1][0] as usize;
    }
    idx
}

fn triple_index_lex(n: usize, i: usize, j: usize, k: usize, b: &[[u32; 5]; 22]) -> usize {
    debug_assert!(i < j && j < k && k < n);
    let mut idx = 0usize;
    for f in 0..i {
        idx += b[n - f - 1][2] as usize;
    }
    for s in (i + 1)..j {
        idx += b[n - s - 1][1] as usize;
    }
    for t in (j + 1)..k {
        idx += b[n - t - 1][0] as usize;
    }
    idx
}

fn rank4(mut c: [u32; 4]) -> u32 {
    let mut r = 0usize;
    for pr in 0..7 {
        let mask = 1u32 << pr;
        let mut found = None;
        for j in r..4 {
            if c[j] & mask != 0 {
                found = Some(j);
                break;
            }
        }
        let Some(j) = found else {
            continue;
        };
        c.swap(r, j);
        let p = c[r];
        for j in 0..4 {
            if j != r && (c[j] & mask) != 0 {
                c[j] ^= p;
            }
        }
        r += 1;
        if r == 4 {
            break;
        }
    }
    r as u32
}

fn apply_dependent_quad(
    i: usize,
    j: usize,
    k: usize,
    l: usize,
    deg: &mut [u32; N],
    forbid: &mut [u32; NUM_TRIPLES],
    b: &[[u32; 5]; 22],
) {
    deg[i] += 1;
    deg[j] += 1;
    deg[k] += 1;
    deg[l] += 1;
    let ti = triple_index_lex(N, i, j, k, b);
    let tj = triple_index_lex(N, i, j, l, b);
    let tk = triple_index_lex(N, i, k, l, b);
    let tl = triple_index_lex(N, j, k, l, b);
    forbid[ti] |= 1u32 << l;
    forbid[tj] |= 1u32 << k;
    forbid[tk] |= 1u32 << j;
    forbid[tl] |= 1u32 << i;
}

fn can_add(ch: u32, el: usize, forbid: &[u32; NUM_TRIPLES], b: &[[u32; 5]; 22]) -> bool {
    if ch == 0 {
        return true;
    }
    let mut idxs = [0u8; N];
    let mut nk = 0usize;
    for i in 0..N {
        if (ch >> i) & 1 != 0 {
            idxs[nk] = i as u8;
            nk += 1;
        }
    }
    if nk < 3 {
        return true;
    }
    for ia in 0..nk {
        for ib in (ia + 1)..nk {
            for ic in (ib + 1)..nk {
                let a = idxs[ia] as usize;
                let bb = idxs[ib] as usize;
                let c = idxs[ic] as usize;
                let ti = triple_index_lex(N, a, bb, c, b);
                if (forbid[ti] >> el) & 1 != 0 {
                    return false;
                }
            }
        }
    }
    true
}

fn greedy(order: &[u8; N], forbid: &[u32; NUM_TRIPLES], b: &[[u32; 5]; 22]) -> (u32, u32) {
    let mut m = 0u32;
    let mut c = 0u32;
    for &v in order.iter() {
        let vi = v as usize;
        if can_add(m, vi, forbid, b) {
            m |= 1u32 << vi;
            c += 1;
        }
    }
    (c, m)
}

fn dfs(
    pos: usize,
    order: &[u8; N],
    chosen: u32,
    ones: u32,
    forbid: &[u32; NUM_TRIPLES],
    b: &[[u32; 5]; 22],
    best: &mut u32,
    best_mask: &mut u32,
) {
    let rem = (N - pos) as u32;
    if ones + rem <= *best {
        return;
    }
    if pos == N {
        if ones > *best {
            *best = ones;
            *best_mask = chosen;
        }
        return;
    }
    let v = order[pos] as usize;
    if can_add(chosen, v, forbid, b) {
        dfs(
            pos + 1,
            order,
            chosen | (1u32 << v),
            ones + 1,
            forbid,
            b,
            best,
            best_mask,
        );
    }
    dfs(pos + 1, order, chosen, ones, forbid, b, best, best_mask);
}

fn main() {
    let b = binom_tbl();
    assert_eq!(b[21][4] as usize, NUM_QUADS);
    assert_eq!(b[21][3] as usize, NUM_TRIPLES);

    let masks = weight5_masks();
    let mut deg = [0u32; N];
    let mut forbid = [0u32; NUM_TRIPLES];
    let mut dep = 0usize;
    for i in 0..N {
        for j in (i + 1)..N {
            for k in (j + 1)..N {
                for l in (k + 1)..N {
                    let r = rank4([
                        masks[i] as u32,
                        masks[j] as u32,
                        masks[k] as u32,
                        masks[l] as u32,
                    ]);
                    if r < 4 {
                        dep += 1;
                        apply_dependent_quad(i, j, k, l, &mut deg, &mut forbid, &b);
                    }
                }
            }
        }
    }

    let mut order = [0u8; N];
    for i in 0..N {
        order[i] = i as u8;
    }
    order.sort_unstable_by_key(|&v| std::cmp::Reverse(deg[v as usize]));

    let (mut best, mut best_mask) = greedy(&order, &forbid, &b);
    dfs(
        0,
        &order,
        0,
        0,
        &forbid,
        &b,
        &mut best,
        &mut best_mask,
    );

    println!("GF(2)^7 weight-5 vectors (all C(7,5) = {N}):");
    println!("dependent 4-subsets: {dep} / {NUM_QUADS}");
    println!("maximum |S| with no dependent 4-set: {best}");
    print!("one optimal S (indices 0..{}): ", N - 1);
    for i in 0..N {
        if (best_mask >> i) & 1 != 0 {
            print!("{i} ");
        }
    }
    println!();
    print!("masks (decimal): ");
    for i in 0..N {
        if (best_mask >> i) & 1 != 0 {
            print!("{} ", masks[i]);
        }
    }
    println!();

    assert_eq!(rank4([1, 2, 4, 8]), 4);
    assert_eq!(rank4([1, 2, 4, 7]), 3);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn quad_lex_bijection() {
        let b = binom_tbl();
        let mut r = 0usize;
        for i in 0..N {
            for j in (i + 1)..N {
                for k in (j + 1)..N {
                    for l in (k + 1)..N {
                        assert_eq!(quad_index_lex(N, i, j, k, l, &b), r);
                        r += 1;
                    }
                }
            }
        }
        assert_eq!(r, NUM_QUADS);
    }

    #[test]
    fn triple_lex_bijection() {
        let b = binom_tbl();
        let mut r = 0usize;
        for i in 0..N {
            for j in (i + 1)..N {
                for k in (j + 1)..N {
                    assert_eq!(triple_index_lex(N, i, j, k, &b), r);
                    r += 1;
                }
            }
        }
        assert_eq!(r, NUM_TRIPLES);
    }
}
