

## Overview

This project implements a modular framework for **block decomposition of symmetric matrices**, focusing on:

1. Generalizing from **banded SPD matrices** to other matrix types (random SPD, user-defined, graph-based).
2. Presenting **clique-based PSD decomposition** of matrices.
3. Analyzing **positive and negative eigenvalues** (completion number) to quantify how far a matrix is from being PSD.

---

## Project Structure

├── matrices/ # Matrix generation
│ ├── init.py
│ ├── band.py # Generate banded SPD matrices
│ ├── random_spd.py # Generate random SPD matrices
│ └── user_defined.py# Load user-provided matrices
│
├── decomposition/ # Block elimination and PSD decomposition
│ ├── init.py
│ ├── block_elim.py # Block Schur complement elimination
│ ├── cholesky_elim.py # Cholesky-based stable elimination
│ └── psd_factors.py # Clique-based PSD decomposition
│
├── graphs/ # Graph-related utilities
│ ├── init.py
│ ├── adjacency.py # Build adjacency graph from matrix
│ └── cliques.py # Find cliques for PSD decomposition
│
├── experiments/ # Scripts to run research experiments
│ ├── init.py
│ └── run_experiments.py # Main experiment driver
│
├── utils/ # Utility functions
│ ├── init.py
│ ├── eigen_analysis.py # Compute eigenvalues and completion number
│
├── requirements.txt # Python dependencies
└── README.md # Project overview and instructions

## Installation

1. Clone the repository:

```bash
git clone <repo-url>
cd "MA490"

2. Create the Venv

python -m venv venv
# On Windows PowerShell:
./venv/Scripts/activate.ps1
# On Unix/macOS:
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt

## Usage

python -m experiments.run_experiments
