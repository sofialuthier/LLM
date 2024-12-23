from transformers import pipeline

# Token'iniz
token = "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"

# BART modelini yükleyin
paraphrase = pipeline(
    "text2text-generation", 
    model="facebook/bart-base", 
    tokenizer="facebook/bart-base"
)

text = "Bu ürün kaliteli ve fiyatı uygun."

# Paraphrasing işlemi
augmented_text = paraphrase(text, max_length=50, num_return_sequences=3)

print("Orijinal:", text)
print("Yeni Metinler:")
for i, result in enumerate(augmented_text):
    print(f"{i + 1}. {result['generated_text']}")


