# weight3_n6_residual_split

Brute-force check on the **20-card** deck of all **weight-3** vectors in **GF(2)^6** (i.e. all 3-subsets of a 6-element set).

We model play as repeatedly **removing any 4-card XOR-to-zero match** (a 4-set of vectors whose bitwise XOR is `0`). We explore **all possible match-removal sequences** from the full deck down to **8 remaining cards**.

Question tested:

- For every reachable **8-card** residual, does it **split into two disjoint 4-matches**?

## Run

```bash
cargo run --release
```

The program prints the number of reachable 8-card residual states and whether every such state splits (and prints counterexamples if any exist).

