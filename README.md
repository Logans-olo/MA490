

## Overview

This project implements a modular framework for **block decomposition of symmetric matrices**, focusing on:

1. Generalizing from **banded SPD matrices** to other matrix types (random SPD, user-defined, graph-based).
2. Presenting **clique-based PSD decomposition** of matrices.
3. Analyzing **positive and negative eigenvalues** (completion number) to quantify how far a matrix is from being PSD.

---

## Project Structure

README.md # Project overview and instructions

├── requirements.txt # Python dependencies

├── matrices/ # Matrix generation

│ ├── init.py

│ ├── band.py # Generate banded SPD matrices

│ ├── random_spd.py # Generate random SPD matrices

│ └── user_defined.py # Load user-provided matrices

│

├── decomposition/ # Block elimination and PSD decomposition

│ ├── init.py

│ ├── block_elim.py # Block Schur complement elimination

│ ├── cholesky_elim.py # Cholesky-based stable elimination

│ └── psd_factors.py # Clique-based PSD decomposition

│



├── runners/

│ ├── init.py

│ └── run_experiments.py 

│

├── utils/ 

│ ├── init.py

│ ├── eigen_analysis.py # Compute eigenvalues and completion number


---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Logans-olo/MA490.git
cd "MA490"
```
2. Create the Venv
```bash
python -m venv venv
# On Windows PowerShell:
./venv/Scripts/activate.ps1
# On Unix/macOS:
source venv/bin/activate
```

3. Install Dependencies & Use
```bash
pip install -r requirements.txt


python -m experiments.run_experiments
```
