import asyncio
import os
import shutil
import subprocess
import tempfile

import edge_tts
from pydub import AudioSegment

_EDGE_VOICES = {
    "Edge TTS - Marija (женски)": "mk-MK-MarijaNeural",
    "Edge TTS - Aleksandar (машки)": "mk-MK-AleksandarNeural",
}


def _espeak_available() -> bool:
    """Check if espeak-ng is installed."""
    return shutil.which("espeak-ng") is not None


def get_available_models() -> list[str]:
    """Return list of available TTS engine names."""
    models = [
        "Edge TTS - Marija (женски)",
        "Edge TTS - Aleksandar (машки)",
    ]
    if _espeak_available():
        models.append("espeak-ng")
    return models


def speak(text: str, engine: str = "Edge TTS - Marija (женски)") -> str:
    """Convert Macedonian text to speech. Returns path to a .wav file."""
    if engine == "espeak-ng":
        return _speak_espeak(text)
    return _speak_edge(text, engine)


def _speak_edge(text: str, engine: str) -> str:
    """Generate speech using Microsoft Edge TTS (requires internet)."""
    voice = _EDGE_VOICES.get(engine, "mk-MK-MarijaNeural")
    tmp_dir = tempfile.mkdtemp()
    mp3_path = os.path.join(tmp_dir, "response.mp3")
    wav_path = os.path.join(tmp_dir, "response.wav")

    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(mp3_path)

    asyncio.run(_generate())

    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    os.remove(mp3_path)
    return wav_path


def _speak_espeak(text: str) -> str:
    """Generate speech using espeak-ng directly (offline, requires espeak-ng installed)."""
    tmp_dir = tempfile.mkdtemp()
    wav_path = os.path.join(tmp_dir, "response.wav")

    subprocess.run(
        ["espeak-ng", "-v", "mk", "-w", wav_path, text],
        check=True,
        capture_output=True,
    )

    return wav_path
