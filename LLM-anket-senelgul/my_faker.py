import random
from generate_faker import Faker
from pymongo import MongoClient
from datetime import datetime

# Faker instance
fake = Faker()

# MongoDB URI ve veritabanı/collection adı
uri = "mongodb://localhost:27017/"
database_name = "EgitimDatabase"
collection_name = "fakerDB_ikiyuz"

# MongoDB bağlantısı
client = MongoClient(uri)

def random_int_from_interval(min, max):
    """Verilen aralıkta rastgele tam sayı döndürür."""
    return random.randint(min, max)

def random_choice(choices):
    """Liste içinden rastgele seçim yapar."""
    return random.choice(choices)

def seed_db():
    """MongoDB'yi sahte verilerle doldurur."""
    db = client[database_name]
    collection = db[collection_name]

    time_series_data = []

    # Rastgele veriler için kategoriler
    genders = ['Male', 'Female', 'Non-binary', 'Other']
    jobs = ['Engineer', 'Doctor', 'Teacher', 'Artist', 'Lawyer', 'Scientist', 'Musician']
    hobbies = ['Reading', 'Swimming', 'Gaming', 'Cooking', 'Cycling', 'Hiking']
    religions = ['Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism', 'Atheism', 'Other']
    marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
    
    for _ in range(5000):  # 5000 adet veri ekle
        first_name = fake.first_name()
        last_name = fake.last_name()
        user_id = fake.uuid4()

        # Kullanıcıya ait genel bilgiler
        new_user = {
            "user_id": user_id,
            "age": random_int_from_interval(18, 80),
            "gender": random_choice(genders),
            "job": random_choice(jobs),
            "email": fake.email(),
            "firstName": first_name,
            "lastName": last_name,
            "smoking": random_choice([True, False]),
            "alcoholic": random_choice([True, False]),
            "depression": random_choice([True, False]),
            "anxiety": random_choice([True, False]),
            "obesity": random_choice([True, False]),
            "active": random_choice([True, False]),
            "hobby": random_choice(hobbies),
            "religion": random_choice(religions),
            "married": random_choice(marital_statuses),
            "siblings": random_int_from_interval(0, 5),
            "timestamp_created": datetime.now(),
            "events": []
        }

        # Olay verileri (Her kullanıcı için 1 ile 6 arasında olay)
        for _ in range(random_int_from_interval(1, 6)):
            new_event = {
                "timestamp_event": fake.date_time_this_year(),
                "weight": random_int_from_interval(50, 100),  # Ağırlık verisi (örneğin, 50-100 kg arasında)
                "activity": random_choice(['Running', 'Walking', 'Cycling', 'Yoga', 'Gym', 'Swimming']),
                "duration_minutes": random_int_from_interval(10, 120)  # Aktivite süresi (dakika)
            }
            new_user["events"].append(new_event)

        time_series_data.append(new_user)

    # Veritabanına ekleme
    collection.insert_many(time_series_data)
    print("Database seeded with synthetic data! :)")

if __name__ == "__main__":
    seed_db()
