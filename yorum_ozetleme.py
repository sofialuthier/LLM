import pandas as pd
from transformers import pipeline
import os

# Hugging Face API anahtarını çevresel değişken olarak ayarlayın
os.environ['HUGGINGFACE_API_KEY'] = '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'

def summarize_comments(comments, model_name="t5-small", batch_size=10):
    summarizer = pipeline("summarization", model=model_name, token=os.getenv('HUGGINGFACE_API_KEY'))
    summaries = []
    for i in range(0, len(comments), batch_size):
        batch = comments[i:i+batch_size]
        # Giriş dizisini 512 token ile sınırlayın
        batch = [comment[:512] for comment in batch]
        batch_summaries = summarizer(batch, max_length=30, min_length=10, do_sample=False)
        summaries.extend([summary['summary_text'] for summary in batch_summaries])
    return summaries

def main():
    # Yorumları ve etiketleri içeren veri setini yükleyin
    df = pd.read_csv("combine.csv")  # Bu dosya adını kendi veri setinize göre değiştirin

    # Yorumları özetleyin
    df['summary'] = summarize_comments(df['Body'].tolist(), batch_size=10)

    # Özetlenmiş yorumları içeren yeni bir CSV dosyası kaydedin
    df[['summary']].to_csv('summarized_comments.csv', index=False)

    print("Özetlenmiş yorumlar 'summarized_comments.csv' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()