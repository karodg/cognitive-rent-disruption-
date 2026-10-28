"""Master execution script for Cognitive Rent Disruption replication.

Executes data validation, econometric models, and figure generation.
"""

import sys
import time

from src.data_prep import main as run_data_prep
from src.estimate_models import main as run_models
from src.generate_figures import main as run_figures


def main():
    start_time = time.time()
    print("=" * 76)
    print("REPLICATION PIPELINE: The Cognitive Rent Disruption (Popov, 2026)")
    print("=" * 76)

    print("\n[Step 1/3] Loading and validating panels...")
    run_data_prep()

    print("\n[Step 2/3] Estimating econometric models (Tables 2-5)...")
    run_models()

    print("\n[Step 3/3] Generating publication figures (Figures 1-4)...")
    run_figures()

    elapsed = time.time() - start_time
    print("\n" + "=" * 76)
    print(f"Replication finished successfully in {elapsed:.1f} seconds.")
    print("Output figures: ./figures/")
    print("=" * 76)


if __name__ == "__main__":
    main()
