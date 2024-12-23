import random
import nltk
from nltk.corpus import wordnet as wn

nltk.download('omw-1.4')
nltk.download('wordnet')

def synonym_replacement(text):
    words = text.split()
    new_words = words.copy()

    for i, word in enumerate(words):
        synonyms = wn.synsets(word, lang='tr')
        if synonyms:
            lemma_names = synonyms[0].lemma_names('tr')
            if lemma_names:
                new_words[i] = random.choice(lemma_names)
    return " ".join(new_words)

text = "Bu ürün kaliteli ve fiyatı uygun."
augmented_text = synonym_replacement(text)

print("Orijinal:", text)
print("Yeni Metin:", augmented_text)
