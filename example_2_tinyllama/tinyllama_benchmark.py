from llama_cpp import Llama
import time
import argparse
import os
import random
import psutil

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def load_prompts():
    """Load prompts from prompts.txt file, return random prompt"""
    try:
        with open('prompts.txt', 'r') as f:
            content = f.read().strip()
        
        # Split by double newline to separate prompts
        if '\n\n' in content:
            prompts = [p.strip() for p in content.split('\n\n') if p.strip()]
        else:
            prompts = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not prompts:
            return "What is quantization in machine learning?"
        
        # Just return the question directly - no need to add Q: or A:
        return random.choice(prompts)
    except FileNotFoundError:
        print("Warning: prompts.txt not found, using default prompt")
        return "What is quantization in machine learning?"

parser = argparse.ArgumentParser(description="Benchmark TinyLlama performance for edge AI applications.")
parser.add_argument("--model", type=str, default="Q4_K_M", help="Model variant (Q4_K_M, Q8_0)")
parser.add_argument("--threads", type=int, default=4, help="Number of CPU threads")
parser.add_argument("--ctx", type=int, default=512, help="Context window size")
parser.add_argument("--tokens", type=int, default=128, help="Number of tokens to generate")
args = parser.parse_args()

# Convert simple model name to full path if needed
if not args.model.endswith('.gguf'):
    model_path = f"models/tinyllama-1.1b-chat-v1.0.{args.model}.gguf"
else:
    model_path = args.model

# Check if model file exists
if not os.path.exists(model_path):
    available_models = []
    models_dir = "models"
    if os.path.exists(models_dir):
        for file in os.listdir(models_dir):
            if file.endswith('.gguf'):
                variant = file.split('.')[-2] if '.' in file else file
                available_models.append(f"  {variant}")
    
    error_msg = f"""Error: Model file not found: {model_path}

Available models:
{chr(10).join(available_models) if available_models else "  None found"}

Usage: python {os.path.basename(__file__)} --model Q4_K_M"""
    print(error_msg)
    exit(1)

# Get model info
if "Q4_K_M" in model_path:
    model_info = "4-bit quantization (balanced)"
elif "Q8_0" in model_path:
    model_info = "8-bit quantization (best quality, slowest)"
else:
    model_info = "Custom configuration"

header = f"""TinyLlama Edge AI Benchmark
Model: {os.path.basename(model_path)}
Type: {model_info}
Threads: {args.threads}, Context: {args.ctx}, Tokens: {args.tokens}
{'-' * 50}"""
print(header)

# Measure memory before model loading
initial_memory = get_memory_usage()
print("Loading model and running inference...")

llm = Llama(model_path=model_path, n_threads=args.threads, n_ctx=args.ctx, verbose=False)
model_loaded_memory = get_memory_usage()

raw_prompt = load_prompts()
# Format the prompt to encourage a complete answer
prompt = f"Question: {raw_prompt}\n\nAnswer:"

print(f"Selected prompt: {raw_prompt}")
start = time.time()
output = llm(prompt, max_tokens=args.tokens)
end = time.time()
final_memory = get_memory_usage()

duration = end - start
tokens_per_sec = args.tokens / duration

# Calculate memory usage
model_memory = model_loaded_memory - initial_memory
inference_memory = final_memory - model_loaded_memory
total_memory = final_memory - initial_memory

results = f"""
Model Response:
{'-' * 50}
{output["choices"][0]["text"].strip()}
{'-' * 50}

Performance Results:
Inference time: {duration:.2f}s
Speed: {tokens_per_sec:.1f} tokens/sec
Throughput: {60 * tokens_per_sec:.0f} tokens/min

Memory Usage:
Model loading: {model_memory:.1f} MB
Inference overhead: {inference_memory:.1f} MB
Total usage: {total_memory:.1f} MB
Current RAM: {final_memory:.1f} MB

Note: This inference ran locally on your device using {args.threads} CPU threads."""
print(results)