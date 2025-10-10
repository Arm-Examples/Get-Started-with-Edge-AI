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

def load_prompts(custom_prompt=None):
    """Load prompts from prompts.txt file or use custom prompt"""
    if custom_prompt:
        return custom_prompt
    
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

def validate_model_path(model_name):
    """Validate and convert model name to full path"""
    # Convert simple model name to full path if needed
    if not model_name.endswith('.gguf'):
        model_path = f"models/tinyllama-1.1b-chat-v1.0.{model_name}.gguf"
    else:
        model_path = model_name

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
        raise FileNotFoundError(error_msg)
    
    return model_path

def get_model_info(model_path):
    """Get human-readable model information"""
    if "Q4_K_M" in model_path:
        return "4-bit quantization (balanced)"
    elif "Q8_0" in model_path:
        return "8-bit quantization (best quality, slowest)"
    else:
        return "Custom configuration"

def load_model(model_path, threads, context_size):
    """Load the LLM model and return it along with memory usage"""
    initial_memory = get_memory_usage()
    print("Loading model...")
    
    llm = Llama(model_path=model_path, n_threads=threads, n_ctx=context_size, verbose=False)
    model_loaded_memory = get_memory_usage()
    model_memory = model_loaded_memory - initial_memory
    
    return llm, model_memory, model_loaded_memory

def run_inference(llm, prompt, max_tokens):
    """Run inference on the model and return results with timing"""
    formatted_prompt = f"Question: {prompt}\n\nAnswer:"
    
    start_time = time.time()
    output = llm(formatted_prompt, max_tokens=max_tokens)
    end_time = time.time()
    
    duration = end_time - start_time
    tokens_per_sec = max_tokens / duration
    response_text = output["choices"][0]["text"].strip()
    
    return response_text, duration, tokens_per_sec

def print_header(model_path, model_info, threads, context_size, max_tokens):
    """Print benchmark header information"""
    header = f"""TinyLlama Edge AI Benchmark
Model: {os.path.basename(model_path)}
Type: {model_info}
Threads: {threads}, Context: {context_size}, Tokens: {max_tokens}
{'-' * 50}"""
    print(header)

def print_results(response_text, duration, tokens_per_sec, model_memory, 
                 inference_memory, total_memory, final_memory, threads):
    """Print benchmark results"""
    results = f"""
Model Response:
{'-' * 50}
{response_text}
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

Note: This inference ran locally on your device using {threads} CPU threads."""
    print(results)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Benchmark TinyLlama performance for edge AI applications.")
    parser.add_argument("--model", type=str, default="Q4_K_M", help="Model variant (Q4_K_M, Q8_0)")
    parser.add_argument("--threads", type=int, default=4, help="Number of CPU threads")
    parser.add_argument("--ctx", type=int, default=512, help="Context window size")
    parser.add_argument("--tokens", type=int, default=128, help="Number of tokens to generate")
    parser.add_argument("--prompt", type=str, default=None, help="Custom prompt to use (overrides prompts.txt)")
    return parser.parse_args()

def main():
    """Main function to orchestrate the benchmark"""
    try:
        # Parse command line arguments
        args = parse_arguments()
        
        # Validate model path
        model_path = validate_model_path(args.model)
        model_info = get_model_info(model_path)
        
        # Print benchmark header
        print_header(model_path, model_info, args.threads, args.ctx, args.tokens)
        
        # Load model and measure memory
        llm, model_memory, model_loaded_memory = load_model(model_path, args.threads, args.ctx)
        
        # Load prompt and run inference
        prompt = load_prompts(args.prompt)
        if args.prompt:
            print(f"Using custom prompt: {prompt}")
        else:
            print(f"Selected prompt: {prompt}")
        
        response_text, duration, tokens_per_sec = run_inference(llm, prompt, args.tokens)
        
        # Calculate final memory usage
        final_memory = get_memory_usage()
        inference_memory = final_memory - model_loaded_memory
        total_memory = final_memory - get_memory_usage() + model_memory + inference_memory
        
        # Print results
        print_results(response_text, duration, tokens_per_sec, model_memory, 
                     inference_memory, total_memory, final_memory, args.threads)
        
    except FileNotFoundError as e:
        print(e)
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()