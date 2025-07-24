import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel, PeftConfig
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

# ----------------------------
# Prompts (5 standard + 2 edge-cases)
# ----------------------------
test_prompts = [
    "Create a new Git branch and switch to it.",
    "Compress the folder reports into reports.tar.gz.",
    "List all Python files in the current directory recursively.",
    "Set up a virtual environment and install requests.",
    "Fetch only the first ten lines of a file named output.log.",
    "Find all files modified in the last 24 hours and copy them to backup/.",
    "Show the number of running Docker containers and their names."
]

# ----------------------------
# Evaluation Function
# ----------------------------
def evaluate_model(model, tokenizer, prompts):
    model.eval()
    results = []
    for prompt in prompts:
        formatted_prompt = f"<|system|>\nYou are a helpful assistant that provides accurate command-line instructions.\n<|user|>\n{prompt}\n<|assistant|>\n"
        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(model.device)

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
        response = response.replace(formatted_prompt, "").strip()
        results.append({'prompt': prompt, 'response': response})
    return results

# ----------------------------
# Metrics Computation
# ----------------------------
rouge = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

def compute_metrics(reference, generated):
    bleu = sentence_bleu([reference.split()], generated.split())
    score = rouge.score(reference, generated)
    rouge_l = score['rougeL'].fmeasure
    return round(bleu, 4), round(rouge_l, 4)

# ----------------------------
# Load Base Model
# ----------------------------
print("Loading base model...")
base_model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(base_model_id)
base_model = AutoModelForCausalLM.from_pretrained(base_model_id).to("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Load Fine-Tuned Adapter
# ----------------------------
print("Loading fine-tuned model with adapter...")
adapter_path = "./fine_tuned_model"
config = PeftConfig.from_pretrained(adapter_path)
tuned_model = AutoModelForCausalLM.from_pretrained(base_model_id, torch_dtype=torch.float16)
tuned_model = PeftModel.from_pretrained(tuned_model, adapter_path)
tuned_model = tuned_model.to("cuda" if torch.cuda.is_available() else "cpu")

# ----------------------------
# Evaluate Both Models
# ----------------------------
print("Evaluating base model...")
base_outputs = evaluate_model(base_model, tokenizer, test_prompts)

print("Evaluating fine-tuned model...")
tuned_outputs = evaluate_model(tuned_model, tokenizer, test_prompts)

# ----------------------------
# Compare Outputs + Score
# ----------------------------
print("\n---- Comparison & Scoring ----")
for i, prompt in enumerate(test_prompts):
    base_resp = base_outputs[i]['response']
    tuned_resp = tuned_outputs[i]['response']

    bleu, rouge_l = compute_metrics(base_resp, tuned_resp)
    plan_score = 2 if tuned_resp.strip() == base_resp.strip() else 1  # Adjust as needed

    print(f"\nPrompt: {prompt}")
    print(f"Base: {base_resp}")
    print(f"Fine-tuned: {tuned_resp}")
    print(f"BLEU: {bleu}, ROUGE-L: {rouge_l}, Plan Quality: {plan_score}")
    print("-" * 60)
