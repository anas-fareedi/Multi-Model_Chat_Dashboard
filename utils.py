def estimate_cost(model, prompt_tokens, completion_tokens):
    # dummy values — update later
    pricing = {
        "mistral:7b": 0.0005,
        "qwen:2.5b": 0.0002,
        "llama:8b": 0.0004
    }

    if model not in pricing:
        return 0

    total_tokens = prompt_tokens + completion_tokens
    return total_tokens * pricing[model]
