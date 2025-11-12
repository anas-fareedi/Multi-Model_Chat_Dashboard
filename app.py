import gradio as gr
from router import ask_model

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

def compare_models(user_msg):
    mistral_resp = ask_model("mistralai/mistral-7b-instruct", [{"role": "user", "content": user_msg}])
    llama_resp = ask_model("meta-llama/llama-3.1-8b-instruct", [{"role": "user", "content": user_msg}])
    qwen_resp = ask_model("qwen/qwen-2.5-7b-instruct", [{"role": "user", "content": user_msg}])

    mistral_text = mistral_resp["choices"][0]["message"]["content"]
    llama_text = llama_resp["choices"][0]["message"]["content"]
    qwen_text = qwen_resp["choices"][0]["message"]["content"]

    return mistral_text, llama_text, qwen_text

with gr.Blocks() as demo:
    gr.Markdown("## Mini ChatGPT — OpenRouter + Gradio")
    with gr.Tabs():
        with gr.Tab("Mistral-7B"):
            model_Mistral = "mistralai/mistral-7b-instruct"
            chatbot_mistral = gr.Chatbot()
            msg_mistral = gr.Textbox(label="Ask something...")
            state_mistral = gr.State([])
            msg_mistral.submit(
                lambda user_msg, hist: chat_fn("mistralai/mistral-7b-instruct", user_msg, hist),
                [msg_mistral, state_mistral],
                [chatbot_mistral, state_mistral]
            )

        with gr.Tab("Llama-8B"):
            model_llama = "meta-llama/llama-3.1-8b-instruct"
            chatbot_llama = gr.Chatbot() 
            msg_llama = gr.Textbox(label="Ask something...")
            state_llama = gr.State([])   
            msg_llama.submit(
                lambda user_msg, hist: chat_fn("meta-llama/llama-3.1-8b-instruct", user_msg, hist),
                [msg_llama, state_llama],
                [chatbot_llama, state_llama]
            )
        with gr.Tab("qwen-2.5-7b"):
            model_qwen = "qwen/qwen-2.5-7b-instruct"
            chatbot_qwen = gr.Chatbot()
            msg_qwen = gr.Textbox(label="Ask something...")
            state_qwen = gr.State([])   
            msg_qwen.submit(
                lambda user_msg, hist: chat_fn("qwen/qwen-2.5-7b-instruct", user_msg, hist),
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

demo.launch()