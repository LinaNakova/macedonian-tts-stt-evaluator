"""WER evaluation script for Macedonian ASR.

Usage: python evaluate.py
"""

import os

import pandas as pd
from jiwer import wer

from asr import transcribe

TEST_DIR = os.path.join(os.path.dirname(__file__), "test_set")
GROUND_TRUTH_PATH = os.path.join(TEST_DIR, "ground_truth.csv")
RECORDINGS_DIR = os.path.join(TEST_DIR, "recordings")
RESULTS_PATH = os.path.join(TEST_DIR, "evaluation_results.csv")


def evaluate():
    if not os.path.exists(GROUND_TRUTH_PATH):
        print(f"Ground truth file not found: {GROUND_TRUTH_PATH}")
        print("Create a ground_truth.csv with columns: filename, transcript")
        return

    gt = pd.read_csv(GROUND_TRUTH_PATH)
    if gt.empty:
        print("Ground truth CSV is empty. Add some test recordings first.")
        return

    results = []
    for _, row in gt.iterrows():
        filename = row["filename"]
        reference = row["transcript"]
        audio_path = os.path.join(RECORDINGS_DIR, filename)

        if not os.path.exists(audio_path):
            print(f"WARNING: Audio file not found, skipping: {filename}")
            continue

        hypothesis = transcribe(audio_path)
        file_wer = wer(reference, hypothesis)

        results.append(
            {
                "filename": filename,
                "reference": reference,
                "hypothesis": hypothesis,
                "wer": round(file_wer, 4),
            }
        )
        print(f"  {filename}: WER={file_wer:.4f}")
        print(f"    REF: {reference}")
        print(f"    HYP: {hypothesis}")

    if not results:
        print("No files were evaluated.")
        return

    results_df = pd.DataFrame(results)
    avg_wer = results_df["wer"].mean()

    print("\n" + "=" * 60)
    print(f"Вкупно евалуирани фајлови: {len(results_df)}")
    print(f"Просечен WER: {avg_wer:.4f} ({avg_wer * 100:.2f}%)")
    print("=" * 60)

    results_df.to_csv(RESULTS_PATH, index=False)
    print(f"\nРезултатите се зачувани во: {RESULTS_PATH}")


if __name__ == "__main__":
    evaluate()
