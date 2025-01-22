from transformers import pipeline

generator = pipeline("text-generation", model="gpt-3.5-turbo")
prompt = "Bu bir ekonomi başlığı için yazılmış yorumdur: "
output = generator(prompt, max_length=50, num_return_sequences=5)
print(output)
