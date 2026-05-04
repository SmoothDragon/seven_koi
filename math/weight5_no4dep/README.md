# weight5_no4dep

Largest subset of the **21** weight-5 vectors in **GF(2)^7** (i.e. all of \( \binom{7}{5} \) patterns) such that **no four distinct vectors are linearly dependent** over GF(2).

```bash
cargo run --release
```

Current output: **|S| = 9** (105 dependent 4-subsets out of 5,985). Same algorithm as `../weight3_no4dep/`.
