import gradio as gr

from asr import transcribe, get_available_models as get_stt_models
from tts import speak, get_available_models as get_tts_models
from dataset import (
    save_tts_evaluation,
    save_stt_evaluation,
    load_tts_evaluations,
    load_stt_evaluations,
)
from sentences import get_sentence, get_total

# ── TTS Evaluation ──────────────────────────────────────────────────────

_tts_index = {"current": 0}
_tts_state = {"generated_audio": None, "text": None, "model": None}


def tts_get_current_sentence():
    return get_sentence(_tts_index["current"]), f"{_tts_index['current'] + 1} / {get_total()}"


def tts_next_sentence():
    _tts_index["current"] = (_tts_index["current"] + 1) % get_total()
    _tts_state["generated_audio"] = None
    text, counter = tts_get_current_sentence()
    return text, counter, None


def tts_prev_sentence():
    _tts_index["current"] = (_tts_index["current"] - 1) % get_total()
    _tts_state["generated_audio"] = None
    text, counter = tts_get_current_sentence()
    return text, counter, None


def tts_generate(text, model):
    if not text:
        return None, "Нема текст."
    try:
        audio_path = speak(text, engine=model)
        _tts_state["generated_audio"] = audio_path
        _tts_state["text"] = text
        _tts_state["model"] = model
        return audio_path, "Аудиото е генерирано."
    except Exception as e:
        return None, f"Грешка: {e}"


def tts_save(is_correct, correction_audio):
    if _tts_state["generated_audio"] is None:
        return "Прво генерирај аудио."

    if not is_correct and correction_audio is None:
        return "Означи како точно или сними ја твојата корекција."

    try:
        eval_id = save_tts_evaluation(
            text=_tts_state["text"],
            model=_tts_state["model"],
            generated_audio_path=_tts_state["generated_audio"],
            corrected_audio_path=correction_audio if not is_correct else None,
            is_correct=is_correct,
        )
        _tts_state["generated_audio"] = None
        return f"Зачувано. (ID: {eval_id})"
    except Exception as e:
        return f"Грешка при зачувување: {e}"


# ── STT Evaluation ──────────────────────────────────────────────────────

_stt_index = {"current": 0}
_stt_state = {"audio_path": None, "generated_text": None, "model": None}


def stt_get_current_prompt():
    return get_sentence(_stt_index["current"]), f"{_stt_index['current'] + 1} / {get_total()}"


def stt_next_prompt():
    _stt_index["current"] = (_stt_index["current"] + 1) % get_total()
    text, counter = stt_get_current_prompt()
    return text, counter


def stt_prev_prompt():
    _stt_index["current"] = (_stt_index["current"] - 1) % get_total()
    text, counter = stt_get_current_prompt()
    return text, counter


def stt_transcribe(audio_path, model):
    if audio_path is None:
        return "", "Нема аудио. Снимете нешто прво."
    try:
        text = transcribe(audio_path, model_name=model)
        _stt_state["audio_path"] = audio_path
        _stt_state["generated_text"] = text
        _stt_state["model"] = model
        if not text:
            return "", "Не беше детектиран говор. Обиди се повторно."
        return text, "Транскрипцијата е готова."
    except Exception as e:
        return "", f"Грешка: {e}"


def stt_save(is_correct, displayed_text):
    if _stt_state["audio_path"] is None:
        return "Прво транскрибирај аудио."

    corrected = None if is_correct else displayed_text

    try:
        eval_id = save_stt_evaluation(
            audio_path=_stt_state["audio_path"],
            model=_stt_state["model"],
            generated_text=_stt_state["generated_text"],
            corrected_text=corrected,
            is_correct=is_correct,
        )
        _stt_state["audio_path"] = None
        _stt_state["generated_text"] = None
        return f"Зачувано. (ID: {eval_id})"
    except Exception as e:
        return f"Грешка при зачувување: {e}"


# ── Dataset Viewer ──────────────────────────────────────────────────────

def refresh_tts_data():
    df = load_tts_evaluations()
    if df.empty:
        return df, "Нема TTS евалуации."
    total = len(df)
    correct = df["is_correct"].sum() if "is_correct" in df.columns else 0
    stats = f"Вкупно: {total} | Точни: {int(correct)} | Коригирани: {total - int(correct)}"
    return df, stats


def refresh_stt_data():
    df = load_stt_evaluations()
    if df.empty:
        return df, "Нема STT евалуации."
    total = len(df)
    correct = df["is_correct"].sum() if "is_correct" in df.columns else 0
    stats = f"Вкупно: {total} | Точни: {int(correct)} | Коригирани: {total - int(correct)}"
    return df, stats


# ── Gradio UI ───────────────────────────────────────────────────────────

initial_tts_text, initial_tts_counter = tts_get_current_sentence()
initial_stt_text, initial_stt_counter = stt_get_current_prompt()

with gr.Blocks(title="Евалуација на говорни модели") as demo:
    gr.Markdown("# Евалуација на говорни модели — Македонски јазик")

    # ── Tab 1: TTS ──
    with gr.Tab("Евалуација на TTS"):
        gr.Markdown("### Текст за читање")
        gr.Markdown("Избери модел, генерирај аудио и оцени дали текстот е прочитан точно.")

        with gr.Row():
            tts_prev_btn = gr.Button("< Претходна", scale=1)
            tts_counter = gr.Textbox(
                value=initial_tts_counter, label="Реченица", interactive=False, scale=1,
            )
            tts_next_btn = gr.Button("Следна >", scale=1)

        tts_text = gr.Textbox(
            value=initial_tts_text, label="Текст", interactive=False, lines=2,
        )
        tts_model = gr.Dropdown(
            choices=get_tts_models(), value=get_tts_models()[0], label="TTS модел",
        )
        tts_gen_btn = gr.Button("Генерирај аудио", variant="primary")

        tts_audio_out = gr.Audio(label="Генерирано аудио", interactive=False)
        tts_status = gr.Textbox(label="Статус", interactive=False)

        tts_correct = gr.Checkbox(label="Аудиото е точно", value=True)
        tts_correction = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Сними ја твојата корекција (ако аудиото не е точно)",
        )
        tts_save_btn = gr.Button("Зачувај евалуација", variant="primary")

        # Events
        tts_next_btn.click(
            fn=tts_next_sentence,
            outputs=[tts_text, tts_counter, tts_audio_out],
        )
        tts_prev_btn.click(
            fn=tts_prev_sentence,
            outputs=[tts_text, tts_counter, tts_audio_out],
        )
        tts_gen_btn.click(
            fn=tts_generate,
            inputs=[tts_text, tts_model],
            outputs=[tts_audio_out, tts_status],
        )
        tts_save_btn.click(
            fn=tts_save,
            inputs=[tts_correct, tts_correction],
            outputs=[tts_status],
        )

    # ── Tab 2: STT ──
    with gr.Tab("Евалуација на STT"):
        gr.Markdown("### Снимај говор")
        gr.Markdown("Прочитај ја реченицата, сними се, избери модел и оцени ја транскрипцијата.")

        with gr.Row():
            stt_prev_btn = gr.Button("< Претходна", scale=1)
            stt_counter = gr.Textbox(
                value=initial_stt_counter, label="Реченица", interactive=False, scale=1,
            )
            stt_next_btn = gr.Button("Следна >", scale=1)

        stt_prompt = gr.Textbox(
            value=initial_stt_text, label="Текст за читање (помош)",
            interactive=False, lines=2,
        )

        stt_audio_in = gr.Audio(
            sources=["microphone", "upload"],
            type="filepath",
            label="Сними го твојот говор",
        )
        stt_model = gr.Dropdown(
            choices=get_stt_models(), value="small", label="STT модел (Whisper)",
        )
        stt_transcribe_btn = gr.Button("Транскрибирај", variant="primary")

        stt_result = gr.Textbox(
            label="Транскрипција (може да ја коригираш)", interactive=True, lines=2,
        )
        stt_status = gr.Textbox(label="Статус", interactive=False)

        stt_correct = gr.Checkbox(label="Транскрипцијата е точна", value=True)
        stt_save_btn = gr.Button("Зачувај евалуација", variant="primary")

        # Events
        stt_next_btn.click(
            fn=stt_next_prompt,
            outputs=[stt_prompt, stt_counter],
        )
        stt_prev_btn.click(
            fn=stt_prev_prompt,
            outputs=[stt_prompt, stt_counter],
        )
        stt_transcribe_btn.click(
            fn=stt_transcribe,
            inputs=[stt_audio_in, stt_model],
            outputs=[stt_result, stt_status],
        )
        stt_save_btn.click(
            fn=stt_save,
            inputs=[stt_correct, stt_result],
            outputs=[stt_status],
        )

    # ── Tab 3: Dataset ──
    with gr.Tab("Собрани податоци"):
        gr.Markdown("### TTS евалуации")
        tts_refresh_btn = gr.Button("Освежи TTS податоци")
        tts_stats = gr.Textbox(label="Статистика", interactive=False)
        tts_table = gr.Dataframe(label="TTS евалуации")

        tts_refresh_btn.click(
            fn=refresh_tts_data,
            outputs=[tts_table, tts_stats],
        )

        gr.Markdown("---")
        gr.Markdown("### STT евалуации")
        stt_refresh_btn = gr.Button("Освежи STT податоци")
        stt_stats = gr.Textbox(label="Статистика", interactive=False)
        stt_table = gr.Dataframe(label="STT евалуации")

        stt_refresh_btn.click(
            fn=refresh_stt_data,
            outputs=[stt_table, stt_stats],
        )

demo.launch(share=True)
