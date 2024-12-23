from faker import Faker
import pandas as pd
import random

fake = Faker()
Faker.seed(42)

# 100 bin kullanıcı profili oluşturma
data = []

for _ in range(100000):
    profile = {
        "user_id": fake.unique.random_int(),
        "age": random.randint(18, 80),
        "gender":random.choice([0,1]),
        "marital_status": random.choice(["single", "married", "divorced"]),
        "activity_level": random.uniform(0, 1),  # 0: pasif, 1: çok aktif
        "anxiety_level": random.uniform(0, 1),  # 0: düşük, 1: yüksek
        "economic_interest": random.choice(0, 1),  # Ekonomi ilgisi: 0 (düşük), 1 (yüksek)
    }
    data.append(profile)

# DataFrame'e dönüştür ve kaydet
user_df = pd.DataFrame(data)
user_df.to_csv("user_profiles.csv", index=False)
