from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from pymongo import MongoClient
import torch
import pandas as pd
import gc
import tqdm

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

# MongoDB bağlantısı
client = MongoClient('mongodb://localhost:27017/')
db = client['EgitimDatabase']
collection = db['fakerDb']  # Koleksiyon adı

# OPT model and tokenizer setup
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
MODEL_NAME = "distilgpt2"  # Daha küçük model: 'facebook/opt-350m'

# Model ve tokenizer'ı yükle
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto", offload_folder="offload")



# Set padding token
tokenizer.pad_token = tokenizer.eos_token
model.config.pad_token_id = tokenizer.eos_token_id
tokenizer.padding_side = 'left'

BATCH_SIZE = 32
results = []

# Kullanıcıları MongoDB'den çek
users = list(collection.find({}, {"firstName": 1, "age": 1, "gender": 1, "job": 1, 
                                "hobby": 1, "active": 1, "smoking":1, "depression":1, 
                                "anxiety":1, "alcoholic":1, "obesity":1, "married":1,}))

try:
    for i in tqdm.tqdm(range(0, len(users), BATCH_SIZE)):
        user_batch = users[i:i + BATCH_SIZE]
        batch_inputs = []
        
        # Prepare batch inputs
        for u in user_batch:
            try:
                user_input = f"""
                Kullanıcı: {u.get('name', '')}
                Yaş: {u.get('age', '')}
                Cinsiyet: {u.get('gender', '')}
                Meslek: {u.get('job', '')}
                Hobi: {u.get('hobby', '')}
                Aktivite: {u.get('active', '')}
                Sigara: {u.get('smoking', '')}
                Depresyon: {u.get('depression', '')}
                Anksiyete: {u.get('anxiety', '')}
                Alkol: {u.get('alcoholic', '')}
                Obezite: {u.get('obesity', '')}
                Evli: {u.get('married', '')}
                """
                batch_inputs.append(user_input)
            except Exception as e:
                print(f"Error processing user data: {e}")
                continue
        
        if not batch_inputs:
            continue
            
        # Process batch
        try:
            encoded_inputs = tokenizer(batch_inputs, 
                                     return_tensors='pt', 
                                     padding=True, 
                                     truncation=True,
                                     max_length=512)
            encoded_inputs = {k: v.to(device) for k, v in encoded_inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(
                    input_ids=encoded_inputs['input_ids'],
                    attention_mask=encoded_inputs['attention_mask'],
                    max_new_tokens=200, 
                    num_return_sequences=1,
                    pad_token_id=tokenizer.eos_token_id,
                    do_sample=True,
                    temperature=0.7
                )
            
            generated_texts = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            
            # Store results
            for u, text in zip(user_batch, generated_texts):
                results.append({
                    "name": u.get('name', ''),
                    "age": u.get('age', ''),
                    "gender": u.get('gender', ''),
                    "job": u.get('job', ''),
                    "hobby": u.get('hobby', ''),
                    "active": u.get('active', ''),
                    "smoking": u.get('smoking', ''),
                    "depression": u.get('depression', ''),
                    "anxiety": u.get('anxiety', ''),
                    "alcoholic": u.get('alcoholic', ''),
                    "obesity": u.get('obesity', ''),
                    "married": u.get('married', ''),
                    "generated_comment": text
                })
                
        except Exception as e:
            print(f"Error in batch processing: {e}")
            continue
            
        # Memory management
        torch.cuda.empty_cache()
        gc.collect()
        
except Exception as e:
    print(f"Fatal error: {e}")
finally:
    # Save final results
    if results:
        df_comments = pd.DataFrame(results)
        df_comments.to_csv("kullanici_fake.csv", index=False, encoding='utf-8')
    client.close()
