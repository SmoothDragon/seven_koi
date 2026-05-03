# Seven Koi — digital bonus (Rust → WebAssembly)

Kickstarter-tier in-browser build. Implements shared deck / match primitives in Rust and compiles them to WASM for use from JavaScript.

## Prerequisites

- [Rust toolchain](https://rustup.rs/) (`rustc`, `cargo`)
- `wasm32-unknown-unknown` target: `rustup target add wasm32-unknown-unknown`
- [wasm-pack](https://rustwasm.github.io/wasm-pack/installer/): `cargo install wasm-pack` (or the installer from that page)

## Build

From this directory (`bonus_web/`):

```bash
wasm-pack build --target web --release
```

This writes JavaScript + WASM bindings into `./pkg/`.

## Run locally

Many teams use `npx serve` or `python3 -m http.server` from `bonus_web/www/` **after** building, so `./pkg/` resolves correctly.

```bash
wasm-pack build --target web --release
cd www
python3 -m http.server 8080
```

Open http://localhost:8080 — the page imports `../pkg/seven_koi_bonus.js`.

## Next steps

- Wire `deck_vector()`, shuffling (`rand` + `getrandom` with `wasm_js` features), layout size `10`, and UI per `CLAUDE.md`.
- Decide on frontend approach: vanilla JS, or a Rust framework that targets WASM (Leptos, Yew, etc.) — keeping this crate small as the “logic core” is usually enough for v1.

## License

Rust crate declares `MIT OR Apache-2.0` in `Cargo.toml`; align crate license with your shipping policy before the campaign.
