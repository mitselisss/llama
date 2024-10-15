from unsloth import FastLanguageModel, is_bfloat16_supported
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments, TextStreamer

max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

# Load the corresponsing model and tokenizer.
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
    cache_dir="/data/tsolakidis/llama/llama_3.1_model",
    # token = "hf_...", # use one if using gated models like meta-llama/Llama-2-7b-hf
)

# Add LoRA adapters.
model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 32,
    lora_dropout = 0.3, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

# Prepare the dataset.
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

EOS_TOKEN = tokenizer.eos_token # Must add EOS_TOKEN
def formatting_prompts_func(examples):
    instructions = examples["instruction"]
    inputs       = examples["input"]
    outputs      = examples["output"]
    texts = []
    for instruction, input, output in zip(instructions, inputs, outputs):
        # Must add EOS_TOKEN, otherwise your generation will go on forever!
        text = alpaca_prompt.format(instruction, input, output) + EOS_TOKEN
        texts.append(text)
    return { "text" : texts, }
pass

# dataset = load_dataset("yahma/alpaca-cleaned", cache_dir="/home/tsolakidis/Desktop/llama_3.1_fine_tune/alpaca/huggingface", split = "train")
# dataset = dataset.map(formatting_prompts_func, batched = True,)

#url = "generated_jsonls/dataset_created_from_nutrition_imits.jsonl"
url = "generated_jsonls/dataset_created_from_weekly_plans_2.jsonl"
dataset = load_dataset("json", data_files = {"train" : url}, split = "train")
#dataset = dataset.map(formatting_prompts_func, batched = True,)

# Split the dataset into train and eval
train_size = int(0.8 * len(dataset))  # 80% for training
eval_size = len(dataset) - train_size  # Remaining 20% for evaluation
train_dataset = dataset.select(range(train_size))
eval_dataset = dataset.select(range(train_size, len(dataset)))

# Map the formatting function to both datasets
train_dataset = train_dataset.map(formatting_prompts_func, batched=True)
eval_dataset = eval_dataset.map(formatting_prompts_func, batched=True)

# Set the trainer from hugingface library.
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    eval_dataset=eval_dataset,  # Add this line
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    dataset_num_proc = 2,
    packing = False, # Can make training 5x faster for short sequences.
    args = TrainingArguments(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        #num_train_epochs = 1, # Set this for 1 full training run.
        max_steps = 60,
        learning_rate = 5e-4,
        fp16 = not is_bfloat16_supported(),
        bf16 = is_bfloat16_supported(),
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.01,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        save_steps=500,
        save_total_limit=3,
        evaluation_strategy="steps",  # Add this for evaluation during training
        eval_steps=500,  # Specify how often to evaluate
    ),
)

trainer_stats = trainer.train()

# Test the fine-tuned model.
FastLanguageModel.for_inference(model) # Enable native 2x faster inference
inputs = tokenizer(
[
    alpaca_prompt.format(
        # "Which of these two numbers is larger?", # instruction
        # "9.9 or 9.11", # input
        # "", # output - leave this blank for generation!
        "Generate a daily meal plan of breakfast, morning snack, lunch, afternoon snack, dinner, and supper for the following user.", # instruction
        "User profile: 146kg weight, 1.74m height, 1.195 PAL, 48.2230149293169 BMI, 2154.847 BMR, 42 years old, and the user is an adult with obesity.", # input
        "", # output - leave this blank for generation!
    )
], return_tensors = "pt").to("cuda")

text_streamer = TextStreamer(tokenizer)
_ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 1000)

model.save_pretrained("lora_dropout_03_epoch_1_r_16_a_32") # Local saving
tokenizer.save_pretrained("lora_dropout_03_epoch_1_r_16_a_32") # Local saving