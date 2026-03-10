import concurrent.futures

import gradio as gr

from router import ask_model, extract_assistant_text, stream_model_text

MODELS = {
    "Mistral-7B": "mistralai/mistral-7b-instruct",
    "Llama-8B": "meta-llama/llama-3.1-8b-instruct",
    "Qwen-2.5-7B": "qwen/qwen-2.5-7b-instruct",
}


def _normalize_chatbot_history(history):
    normalized = []
    for item in history or []:
        if isinstance(item, dict):
            role = item.get("role")
            content = item.get("content")
            if role in {"user", "assistant"}:
                normalized.append({"role": role, "content": "" if content is None else str(content)})
            continue

        if isinstance(item, (list, tuple)) and len(item) == 2:
            user_text = "" if item[0] is None else str(item[0])
            assistant_text = "" if item[1] is None else str(item[1])
            normalized.append({"role": "user", "content": user_text})
            normalized.append({"role": "assistant", "content": assistant_text})
    return normalized


def _build_messages(history, user_message):
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for message in _normalize_chatbot_history(history):
        role = message.get("role")
        content = message.get("content")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content})

    messages.append({"role": "user", "content": user_message})
    return messages


def stream_model(model, user_message, history):
    history = _normalize_chatbot_history(history)
    if not user_message or not user_message.strip():
        yield history, history
        return

    messages = _build_messages(history, user_message)
    updated_history = history + [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ""},
    ]
    yield updated_history, updated_history

    reply = ""
    try:
        for delta in stream_model_text(model, messages):
            reply += delta
            updated_history[-1] = {"role": "assistant", "content": reply}
            yield updated_history, updated_history
    except Exception as exc:
        updated_history[-1] = {"role": "assistant", "content": f"[Stream Error] {exc}"}
        yield updated_history, updated_history


def _single_model_compare(model, user_msg):
    response = ask_model(model, [{"role": "user", "content": user_msg}])
    return extract_assistant_text(response)


def compare_models(user_msg):
    if not user_msg or not user_msg.strip():
        return "Please enter a prompt.", "Please enter a prompt.", "Please enter a prompt."

    model_list = [
        MODELS["Mistral-7B"],
        MODELS["Llama-8B"],
        MODELS["Qwen-2.5-7B"],
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(_single_model_compare, model, user_msg) for model in model_list]
        outputs = [future.result() for future in futures]

    return outputs[0], outputs[1], outputs[2]


def stream_mistral(user_msg, hist):
    yield from stream_model(MODELS["Mistral-7B"], user_msg, hist)


def stream_llama(user_msg, hist):
    yield from stream_model(MODELS["Llama-8B"], user_msg, hist)


def stream_qwen(user_msg, hist):
    yield from stream_model(MODELS["Qwen-2.5-7B"], user_msg, hist)

with gr.Blocks() as demo:
    gr.Markdown("## Mini ChatGPT — OpenRouter + Gradio")
    with gr.Tabs():
        with gr.Tab("Mistral-7B"):
            chatbot_mistral = gr.Chatbot()
            msg_mistral = gr.Textbox(label="Ask something...")
            state_mistral = gr.State([])
            msg_mistral.submit(
                stream_mistral,
                [msg_mistral, state_mistral],
                [chatbot_mistral, state_mistral]
            )

        with gr.Tab("Llama-8B"):
            chatbot_llama = gr.Chatbot()
            msg_llama = gr.Textbox(label="Ask something...")
            state_llama = gr.State([])   
            msg_llama.submit(
                stream_llama,
                [msg_llama, state_llama],
                [chatbot_llama, state_llama]
            )
        with gr.Tab("qwen-2.5-7b"):
            chatbot_qwen = gr.Chatbot()
            msg_qwen = gr.Textbox(label="Ask something...")
            state_qwen = gr.State([])   
            msg_qwen.submit(
                stream_qwen,
                [msg_qwen, state_qwen],
                [chatbot_qwen, state_qwen]
            )
        
        with gr.Tab("Compare Models"):
            gr.Markdown("### Compare all model outputs side by side")

            compare_input = gr.Textbox(
                label="Ask all models at once...",
                placeholder="Type your prompt..."
            )

            with gr.Row():
                mistral_out = gr.Textbox(label="Mistral-7B", lines=8)
                llama_out = gr.Textbox(label="Llama-8B", lines=8)
                qwen_out = gr.Textbox(label="Qwen-2.5-7B", lines=8)

            compare_input.submit(compare_models, compare_input, [mistral_out, llama_out, qwen_out])

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=12)
    demo.launch(share=False)
