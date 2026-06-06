"""
Train ai-slop-detector ML model and save to QC directory.

Generates synthetic training data, runs the ML pipeline, and
writes models/slop_classifier.pkl to the centrally-owned QC path.
"""
# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "ai-slop-detector>=3.8",
#   "scikit-learn>=1.5",
#   "xgboost==2.0.0",
# ]
# ///

import logging
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

QC_DIR = Path.home() / "gitclones/ai/quality-control"
MODEL_DIR = QC_DIR / "models"


def main():
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    from slop_detector.ml.pipeline import MLPipeline

    pipeline = MLPipeline(output_dir=MODEL_DIR)
    report = pipeline.run(
        n_slop=500,
        n_clean=500,
        model_type="ensemble",
        test_size=0.2,
        save_model=True,
    )
    print(report.summary())

    model_path = MODEL_DIR / "slop_classifier.pkl"
    if not model_path.exists():
        print(f"FATAL: model was not saved to {model_path}", file=sys.stderr)
        sys.exit(1)

    print(f"\nModel saved: {model_path}")
    print(f"Size: {model_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
