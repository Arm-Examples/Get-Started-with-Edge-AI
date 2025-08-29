from huggingface_hub import hf_hub_download

models = [
    ("Q4_K_M", "smaller, faster"),
    ("Q8_0", "larger, higher quality")
]

repo_id = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"

for variant, description in models:
    filename = f"tinyllama-1.1b-chat-v1.0.{variant}.gguf"
    print(f"Downloading {variant} model ({description})...")
    hf_hub_download(
        repo_id=repo_id,
        filename=filename,
        local_dir="models"
    )