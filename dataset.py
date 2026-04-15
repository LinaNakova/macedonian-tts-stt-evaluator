import os
import shutil
from datetime import datetime

import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

TTS_AUDIO_DIR = os.path.join(DATASET_DIR, "tts_audio")
TTS_CORRECTIONS_DIR = os.path.join(DATASET_DIR, "tts_corrections")
STT_AUDIO_DIR = os.path.join(DATASET_DIR, "stt_audio")

TTS_CSV = os.path.join(DATASET_DIR, "tts_evaluations.csv")
STT_CSV = os.path.join(DATASET_DIR, "stt_evaluations.csv")

TTS_COLUMNS = [
    "id", "text", "model", "generated_audio", "corrected_audio",
    "is_correct", "timestamp",
]
STT_COLUMNS = [
    "id", "audio", "model", "generated_text", "corrected_text",
    "is_correct", "timestamp",
]


def _ensure_dirs():
    for d in [TTS_AUDIO_DIR, TTS_CORRECTIONS_DIR, STT_AUDIO_DIR]:
        os.makedirs(d, exist_ok=True)
    if not os.path.exists(TTS_CSV):
        pd.DataFrame(columns=TTS_COLUMNS).to_csv(TTS_CSV, index=False)
    if not os.path.exists(STT_CSV):
        pd.DataFrame(columns=STT_COLUMNS).to_csv(STT_CSV, index=False)


def _next_id(csv_path: str) -> int:
    df = pd.read_csv(csv_path)
    if df.empty:
        return 1
    return int(df["id"].max()) + 1


def save_tts_evaluation(
    text: str,
    model: str,
    generated_audio_path: str,
    corrected_audio_path: str | None,
    is_correct: bool,
) -> int:
    """Save a TTS evaluation entry. Returns the assigned ID."""
    _ensure_dirs()
    eval_id = _next_id(TTS_CSV)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Copy generated audio
    gen_filename = f"tts_gen_{eval_id}_{now}.wav"
    shutil.copy2(generated_audio_path, os.path.join(TTS_AUDIO_DIR, gen_filename))

    # Copy corrected audio if provided
    corr_filename = ""
    if corrected_audio_path:
        corr_filename = f"tts_corr_{eval_id}_{now}.wav"
        shutil.copy2(corrected_audio_path, os.path.join(TTS_CORRECTIONS_DIR, corr_filename))

    row = pd.DataFrame([{
        "id": eval_id,
        "text": text,
        "model": model,
        "generated_audio": gen_filename,
        "corrected_audio": corr_filename,
        "is_correct": is_correct,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])
    row.to_csv(TTS_CSV, mode="a", header=False, index=False)
    return eval_id


def save_stt_evaluation(
    audio_path: str,
    model: str,
    generated_text: str,
    corrected_text: str | None,
    is_correct: bool,
) -> int:
    """Save an STT evaluation entry. Returns the assigned ID."""
    _ensure_dirs()
    eval_id = _next_id(STT_CSV)
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Copy user audio
    audio_filename = f"stt_{eval_id}_{now}.wav"
    shutil.copy2(audio_path, os.path.join(STT_AUDIO_DIR, audio_filename))

    row = pd.DataFrame([{
        "id": eval_id,
        "audio": audio_filename,
        "model": model,
        "generated_text": generated_text,
        "corrected_text": corrected_text or "",
        "is_correct": is_correct,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }])
    row.to_csv(STT_CSV, mode="a", header=False, index=False)
    return eval_id


def load_tts_evaluations() -> pd.DataFrame:
    _ensure_dirs()
    return pd.read_csv(TTS_CSV)


def load_stt_evaluations() -> pd.DataFrame:
    _ensure_dirs()
    return pd.read_csv(STT_CSV)
