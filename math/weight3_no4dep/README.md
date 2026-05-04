# weight3_no4dep

Exact search: largest subset of the **35** weight-3 vectors in **GF(2)^7** such that **no four distinct vectors are linearly dependent** (every 4-subset has full rank 4 over GF(2)).

```bash
cargo run --release
```

Typical output: maximum **|S| = 9** (840 dependent 4-subsets out of 52,325 total). Runtime is dominated by branch-and-bound after a greedy lower bound; a triple-index **forbid mask** makes each `can_add` check cheap.
