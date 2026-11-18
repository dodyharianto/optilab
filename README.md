# Project Overview

Optimization project focusing on evaluating several techniques to solve vehicle routing problem: given a depot and some vertices representing customer locations, determine a route that visits all customers once and minimizes the travel distance.

![alt text](image.png)

# Project Structure

```text
optilab/
├── src/
│   └── optilab/                 # Routing algorithms and supporting utilities
│       ├── __init__.py
│       ├── baseline.py          # Nearest-neighbor and 2-opt heuristics
│       ├── data.py              # Reproducible customer-location generation
│       ├── distance.py          # Pairwise distance calculations
│       ├── exact.py             # MILP-based TSP solver
│       └── visualize.py         # Route visualization
├── scripts/
│   ├── benchmark.py             # Compare methods across generated instances
│   ├── run_baseline.py          # Run nearest-neighbor and 2-opt
│   └── run_exact.py             # Run the MILP solver
├── outputs/
│   ├── benchmark_results/
│   │   └── benchmark.csv        # Benchmark distances and runtimes
│   ├── 2-opt.png
│   ├── milp.png
│   └── nearest_neighbor.png
├── pyproject.toml
├── requirements.txt
├── image.png
└── README.md
```
