import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import argparse
import json
import os
import subprocess
import datetime

# Manually set your base model name
base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"  # <-- CHANGE THIS if you used another model

# Path to your saved LoRA adapter
adapter_path = "./fine_tuned_model"

# Load base model and inject LoRA adapter
base_model = AutoModelForCausalLM.from_pretrained(base_model_name, torch_dtype=torch.float16)
model = PeftModel.from_pretrained(base_model, adapter_path)

# Load tokenizer from base model
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# Move to device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()

# Setup logging
os.makedirs("logs", exist_ok=True)
log_file_path = "logs/trace.jsonl"

def generate_response(instruction):
    prompt = f"<|system|>\nYou are a helpful assistant that provides accurate command-line instructions.\n<|user|>\n{instruction}\n<|assistant|>\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.1,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "<|assistant|>" in response:
        response = response.split("<|assistant|>")[-1].strip()
    return response

def dry_run_if_command(response):
    first_line = response.strip().split('\n')[0]
    if first_line.startswith(("git", "ls", "cd", "mkdir", "rm", "tar", "echo", "python", "./", "curl", "grep", "cat", "find")):
        print("\nDry-run mode:")
        print(f"echo {first_line}")
        subprocess.run(["echo", first_line])
    else:
        print("\nNo shell command detected in the first line.")

def log_trace(instruction, response):
    trace = {
        "timestamp": datetime.datetime.now().isoformat(),
        "instruction": instruction,
        "response": response
    }
    with open(log_file_path, "a") as f:
        f.write(json.dumps(trace) + "\n")

def main():
    parser = argparse.ArgumentParser(description="CLI Agent for Natural Language Instructions")
    parser.add_argument("instruction", type=str, nargs="+", help="Instruction to process")
    args = parser.parse_args()

    instruction = " ".join(args.instruction)
    print(f"\nInstruction: {instruction}")

    response = generate_response(instruction)
    print("\nGenerated Plan:\n" + response)

    dry_run_if_command(response)
    log_trace(instruction, response)

if __name__ == "__main__":
    main()
