import whisper

AVAILABLE_MODELS = ["tiny", "base", "small", "medium"]

_models: dict[str, whisper.Whisper] = {}


def _get_model(model_name: str) -> whisper.Whisper:
    """Load a Whisper model on first use and cache it."""
    if model_name not in _models:
        print(f"Loading Whisper model '{model_name}'...")
        _models[model_name] = whisper.load_model(model_name)
        print(f"Model '{model_name}' loaded.")
    return _models[model_name]


def transcribe(audio_path: str, model_name: str = "small") -> str:
    """Transcribe a Macedonian audio file using the specified Whisper model."""
    model = _get_model(model_name)
    result = model.transcribe(audio_path, language="mk", fp16=False)
    return result["text"].strip()


def get_available_models() -> list[str]:
    """Return list of available Whisper model names."""
    return AVAILABLE_MODELS.copy()
