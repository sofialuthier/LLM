import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def main():
    # Yorumları ve etiketleri içeren veri setini yükleyin
    df = pd.read_csv("combine.csv")  # Bu dosya adını kendi veri setinize göre değiştirin

    # Yorumları ve etiketleri ayırın
    X = df['Body']  # Yorumların bulunduğu sütun adı
    y = df['Comments']  # Etiketlerin bulunduğu sütun adı (örneğin, 'gender', 'age_group')

    # Veriyi eğitim ve test setlerine ayırın
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # TF-IDF vektörleştirici ve Naive Bayes sınıflandırıcıdan oluşan bir pipeline oluşturun
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    # Modeli eğitim verisiyle eğitin
    model.fit(X_train, y_train)

    # Test verisiyle tahminler yapın
    y_pred = model.predict(X_test)

    # Sınıflandırma raporunu yazdırın
    print(classification_report(y_test, y_pred))

    # Yeni yorumları tahmin etmek için modeli kullanın
    new_comments = ["Bu yorum askerlik hakkında", "Bu yorum ev işleri hakkında", "Bu yorum öğrencilik hakkında"]
    predictions = model.predict(new_comments)
    for comment, prediction in zip(new_comments, predictions):
        print(f"Comment: {comment} -> Prediction: {prediction}")

if __name__ == "__main__":
    main()