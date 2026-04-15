# Проектна Предлог-Програма / Project Proposal
## Евалуација и собирање на говорни податоци за македонскиот јазик
## Evaluation and Collection of Speech Data for the Macedonian Language

---

### 1. Вовед / Introduction

The Macedonian language remains underrepresented in modern speech technology. While large-scale Text-to-Speech (TTS) and Speech-to-Text (STT) models have achieved impressive results for widely spoken languages, their performance on Macedonian is largely unevaluated and often inadequate. There is also a significant lack of open, validated Macedonian speech datasets that researchers and developers can use to train and improve these models.

This project aims to address both problems simultaneously by building a **web-based platform for evaluating speech models on the Macedonian language** while **crowdsourcing a validated speech dataset** as a byproduct of the evaluation process.

---

### 2. Цели / Objectives

1. **Evaluate existing TTS models** on their ability to correctly synthesize Macedonian speech from text.
2. **Evaluate existing STT models** on their ability to accurately transcribe spoken Macedonian.
3. **Collect a crowdsourced Macedonian speech dataset** consisting of:
   - Model-generated audio with human validation labels
   - Human-recorded corrections where models failed
   - Transcriptions validated or corrected by native speakers
4. **Provide a framework** where new models — including the **Vezilka** models — can be integrated and evaluated alongside existing ones.

---

### 3. Опис на системот / System Description

The system is a locally-hosted web application with three core modules:

#### 3.1 TTS Evaluation Module

The user is presented with predefined Macedonian sentences. They select a TTS model, which generates audio from the text. The user then evaluates whether the model read the text correctly:

- **If correct** — the evaluation is marked as accurate and saved.
- **If incorrect** — the user records themselves reading the same text as a correction.

All data is stored: the original text, the model used, the generated audio, and the user's corrected audio (if applicable).

**Currently available TTS models:**
- **gTTS (Google Text-to-Speech)** — cloud-based, decent Macedonian support
- **espeak** — offline, rule-based synthesis
- **Vezilka TTS models** — can be integrated as additional evaluation targets

#### 3.2 STT Evaluation Module

The user records themselves speaking a Macedonian sentence (optionally guided by a prompt). They select an STT model, which transcribes the audio to text. The user then evaluates the transcription:

- **If correct** — the evaluation is marked as accurate and saved.
- **If incorrect** — the user manually corrects the transcription.

All data is stored: the user's audio, the model used, the generated transcription, and the user's corrected text (if applicable).

**Currently available STT models:**
- **OpenAI Whisper** (tiny, base, small, medium) — multilingual ASR with Macedonian support
- **Vezilka STT models** — can be integrated as additional evaluation targets

#### 3.3 Dataset Collection

Every evaluation — whether marked as correct or corrected by the user — is logged into a structured dataset. Over time, this produces:

- A collection of **validated TTS outputs** with human quality judgments
- A collection of **human-recorded Macedonian speech** with aligned transcriptions
- A collection of **validated STT transcriptions** with correction data
- **Per-model accuracy statistics** enabling direct comparison between models

---

### 4. Интеграција на Vezilka модели / Vezilka Model Integration

The platform is designed to be extensible. The **Vezilka** models for Macedonian TTS and STT can be plugged into the existing model selection dropdowns so they can be tested as well. Users would evaluate Vezilka outputs in exactly the same way as any other model — listening to generated speech, reviewing transcriptions, and providing corrections where needed. This means Vezilka models are tested on the same set of Macedonian sentences, by the same users, under identical conditions as Google TTS, espeak, and Whisper, producing directly comparable results.

---

### 5. Формат на податоци / Data Format

#### TTS Evaluations
| Field | Description |
|-------|-------------|
| `id` | Unique evaluation ID |
| `text` | The Macedonian sentence that was synthesized |
| `model` | The TTS model used |
| `generated_audio` | Path to the model-generated audio file |
| `corrected_audio` | Path to the user's corrected recording (if applicable) |
| `is_correct` | Whether the user marked the output as correct |
| `timestamp` | When the evaluation was performed |

#### STT Evaluations
| Field | Description |
|-------|-------------|
| `id` | Unique evaluation ID |
| `audio` | Path to the user's recorded speech |
| `model` | The STT model used |
| `generated_text` | The model's transcription |
| `corrected_text` | The user's corrected transcription (if applicable) |
| `is_correct` | Whether the user marked the transcription as correct |
| `timestamp` | When the evaluation was performed |

---

### 6. Демо / Demo

A working demo of this system has been implemented and is included alongside this proposal. The demo is a fully functional Gradio web application that runs locally and demonstrates all three modules described above.

**To run the demo:**

```bash
# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ensure ffmpeg is installed
brew install ffmpeg

# Launch the application
python app.py
```

The application opens at `http://localhost:7860` with three tabs:
1. **Евалуација на TTS** — TTS model evaluation
2. **Евалуација на STT** — STT model evaluation
3. **Собрани податоци** — Collected dataset viewer

---

### 7. Технологии / Tech Stack

| Component | Technology |
|-----------|-----------|
| Web UI | Gradio (Python) |
| TTS Engines | gTTS, espeak (pyttsx3), Vezilka (planned) |
| STT Engines | OpenAI Whisper (multiple sizes), Vezilka (planned) |
| Data Storage | CSV files with structured metadata |
| Audio Format | WAV |
| Evaluation Metrics | Word Error Rate (WER) via jiwer |
| Platform | macOS (Apple Silicon compatible, CPU-only) |

---

### 8. Очекувани резултати / Expected Outcomes

1. A **quantitative comparison** of TTS and STT model performance on Macedonian, including Vezilka models.
2. A **crowdsourced Macedonian speech dataset** with human-validated transcriptions and audio corrections.
3. An **open-source evaluation tool** that can be reused by other researchers working on Macedonian speech technology.
4. **Per-model accuracy reports** (WER for STT, human correctness rate for TTS) to identify strengths and weaknesses of each model.

---

### 9. Заклучок / Conclusion

This project bridges the gap between available speech technology and the Macedonian language by providing both an evaluation framework and a data collection pipeline. By enabling native speakers to evaluate and correct model outputs, we simultaneously measure model quality and build the very dataset needed to improve it. The integration of Vezilka models will provide valuable insights into how purpose-built Macedonian models compare against general multilingual systems.

---

*Проект за предметот Говорни технологии / Speech Technologies Course Project*
