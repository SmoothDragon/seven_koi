//! Seven Koi — browser bonus crate (WebAssembly).
//! Game rules and layout size (`L = 10`) live in repo root `CLAUDE.md`.

use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn package_name() -> String {
    "seven_koi_bonus".to_string()
}

/// The 64 odd-weight 7-bit vectors, same convention as `math/verify.py`.
#[wasm_bindgen]
pub fn deck_vector() -> Vec<u32> {
    (0u32..128)
        .filter(|&v| v.count_ones() % 2 == 1)
        .collect()
}

/// True iff the four cards form a legal match (XOR is zero).
#[wasm_bindgen]
pub fn is_four_match(a: u32, b: u32, c: u32, d: u32) -> bool {
    (a ^ b ^ c ^ d) == 0
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn deck_has_64_cards() {
        assert_eq!(deck_vector().len(), 64);
    }

    #[test]
    fn four_basis_vectors_match() {
        assert!(is_four_match(1, 2, 4, 7));
    }
}
