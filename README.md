# Macedonian Speech Model Evaluation & Dataset Collection Tool

A local web application for evaluating Text-to-Speech (TTS) and Speech-to-Text (STT) models on the Macedonian language, while collecting a crowdsourced dataset of corrections.

Built as a student project for a Speech Technologies course.

## Features

- **TTS Evaluation**: Select a TTS model, generate audio from Macedonian text, and mark it as correct or record a correction
- **STT Evaluation**: Record Macedonian speech, transcribe with a Whisper model, and mark the transcription as correct or edit it
- **Dataset Collection**: All evaluations (with corrections) are saved to CSV for research use
- **Multiple Models**: Compare different TTS engines (gTTS, espeak) and Whisper sizes (tiny, base, small, medium)

## Setup

### Prerequisites

- Python 3.9+
- ffmpeg (required by Whisper)
- espeak-ng (optional, for the espeak TTS engine)

```bash
brew install ffmpeg espeak
```

### Install dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Run the app

```bash
source venv/bin/activate
python app.py
```

Opens at `http://localhost:7860` with three tabs:

1. **Евалуација на TTS** — evaluate TTS model output on predefined Macedonian sentences
2. **Евалуација на STT** — evaluate Whisper transcription of your speech
3. **Собрани податоци** — view all collected evaluations

### Run WER evaluation

```bash
python evaluate.py
```

Place test audio in `test_set/recordings/` with ground truth in `test_set/ground_truth.csv`.

## Project Structure

| File | Description |
|------|-------------|
| `app.py` | Main Gradio web application (3 tabs) |
| `asr.py` | Whisper STT with multi-model support and caching |
| `tts.py` | TTS with gTTS (Google) and espeak (pyttsx3) engines |
| `dataset.py` | Saves TTS/STT evaluations to CSV files |
| `sentences.py` | 20 predefined Macedonian sentences for evaluation |
| `evaluate.py` | WER evaluation script using jiwer |

## Dataset Format

### TTS evaluations (`dataset/tts_evaluations.csv`)
```
id, text, model, generated_audio, corrected_audio, is_correct, timestamp
```

### STT evaluations (`dataset/stt_evaluations.csv`)
```
id, audio, model, generated_text, corrected_text, is_correct, timestamp
```

Audio files are stored in `dataset/tts_audio/`, `dataset/tts_corrections/`, and `dataset/stt_audio/`.

## Notes

- gTTS requires an **internet connection**
- espeak works **offline** but may have lower quality for Macedonian
- Whisper models are loaded on first use and cached in memory — first transcription with a new model size will be slower
- `fp16` is disabled (required for Mac CPU/Apple Silicon)
- The app runs on `localhost` only
