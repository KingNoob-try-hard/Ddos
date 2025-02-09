from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "gpt2-medium"

# Tải mô hình và tokenizer
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Lưu mô hình vào bộ nhớ máy để dùng offline
model.save_pretrained("/sdcard/gpt2-medium")
tokenizer.save_pretrained("/sdcard/gpt2-medium")

print("Tải và lưu GPT-2 Medium thành công!")