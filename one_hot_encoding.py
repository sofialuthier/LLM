import pandas as pd

def main():
    # reddit api ile yorumları çekmek için fonksiyon
    df = pd.read_csv("realistic_user_data.csv")  # Bu dosya adını kendi veri setinize göre değiştirin

    # One-hot encoding yapmak istediğiniz sütunları seçin
    columns_to_encode = ['Smoking', 'Alcoholic', 'Depression', 'Anxiety', 'Obesity', 'Active', 'Hobby', 'Married']  # Bu sütun adlarını kendi veri setinize göre değiştirin

    # Seçilen sütunları one-hot encoding ile dönüştürmek
    one_hot_encoded_data = pd.get_dummies(df[columns_to_encode])

    # Orijinal DataFrame'den one-hot encoded sütunları çıkarın
    df = df.drop(columns=columns_to_encode)

    # Orijinal DataFrame'e one-hot encoded verileri eklemek
    df = pd.concat([df, one_hot_encoded_data], axis=1)

    # Sadece one-hot encoded sütunları int'e dönüştürmek
    one_hot_encoded_columns = one_hot_encoded_data.columns
    df[one_hot_encoded_columns] = df[one_hot_encoded_columns].astype(int)

    # Sonucu yeni bir CSV dosyasına kaydetmek
    df.to_csv('combined_one_hot_encoded.csv', index=False)

if __name__ == "__main__":
    main()