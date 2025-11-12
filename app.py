import gradio as gr
from router import ask_model

# models = [
#     "mistral:7b-instruct",
#     "meta-llama/llama-3.1-8b-instruct",
#     "qwen/qwen-2.5-7b-instruct"
# ]
models = [
    "mistralai/mistral-7b-instruct",
    "meta-llama/llama-3.1-8b-instruct",
    "qwen/qwen-2.5-7b-instruct"
]


def chat_fn(model, user_message, history):
    if history is None:
        history = []

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    for h in history:
        messages.append({"role": "user", "content": h[0]})
        messages.append({"role": "assistant", "content": h[1]})

    messages.append({"role": "user", "content": user_message})

    response = ask_model(model, messages)
    print(response)
    print("----------------")
    if "choices" not in response:
        reply = f"[Error] {response.get('error', {}).get('message', 'Unknown error')}"
        history.append((user_message, reply))
        return history, history

    reply = response["choices"][0]["message"]["content"]
    
    history.append((user_message, reply))
   

    return history, history

with gr.Blocks() as demo:
    gr.Markdown("## Mini ChatGPT — OpenRouter + Gradio")
    
    model_dropdown = gr.Dropdown(models, label="Choose Model")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask something...")
    state = gr.State([])

    msg.submit(chat_fn, [model_dropdown, msg, state], [chatbot, state])
    
demo.launch()