import os
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI

prompt_path = os.path.join(os.path.dirname(__file__), "../prompts")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-pro")

MAX_TOKENS = 2000

def parse_model_input(model_string):
    if ":" in model_string:
        provider, model = model_string.split(":", 1)
    elif model_string.startswith("gemini"):
        provider, model = "gemini", model_string
    elif model_string.startswith("anthropic") or model_string.startswith("claude"):
        provider, model = "bedrock", model_string
    else:
        provider, model = "openai", model_string

    return provider, model

def init_chat_model(model_provider, model, max_tokens):
    if model_provider == "openai":
        return ChatOpenAI(
            model=model,
            temperature=0,
            max_tokens=max_tokens
        )

    elif model_provider == "bedrock":
        return ChatBedrock(
            model=model,
            temperature=0,
            max_tokens=max_tokens
        )

    elif model_provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=GEMINI_API_KEY,
            google_api_key=GEMINI_MODEL_NAME,
            temperature=0,
            max_tokens=max_tokens
        )

    else:
        raise ValueError(f"Unsupported model provider: {model_provider}")

def llm_cost(model, metadata):
    # Dummy pricing function — customize as needed
    return round(metadata.get("total_tokens", 0) * 0.00001, 5)