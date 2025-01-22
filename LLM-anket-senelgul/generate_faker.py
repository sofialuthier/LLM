import random
from faker import Faker
from pymongo import MongoClient
from datetime import datetime

# Faker instance
fake = Faker()

# MongoDB URI and database/collection name
uri = "mongodb://localhost:27017/"
database_name = "EgitimDatabase"
collection_name = "fakerDB_ikiyuz"

# MongoDB connection
client = MongoClient(uri)

def random_int_from_interval(min, max):
    return random.randint(min, max)

def random_choice(choices):
    return random.choice(choices)

def create_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    user_id = fake.uuid4()

    # User general information
    new_user = {
        "user_id": user_id,
        "age": random_int_from_interval(18, 80),
        "gender": random_choice(['Male', 'Female', 'Non-binary', 'Other']),
        "job": random_choice(['Engineer', 'Doctor', 'Teacher', 'Artist', 'Lawyer', 'Scientist', 'Musician']),
        "email": fake.email(),
        "firstName": first_name,
        "lastName": last_name,
        "smoking": random_choice([True, False]),
        "alcoholic": random_choice([True, False]),
        "depression": random_choice([True, False]),
        "anxiety": random_choice([True, False]),
        "obesity": random_choice([True, False]),
        "active": random_choice([True, False]),
        "hobby": random_choice(['Reading', 'Swimming', 'Gaming', 'Cooking', 'Cycling', 'Hiking']),
        "religion": random_choice(['Christianity', 'Islam', 'Hinduism', 'Buddhism', 'Judaism', 'Atheism', 'Other']),
        "married": random_choice(['Single', 'Married', 'Divorced', 'Widowed']),
        "siblings": random_int_from_interval(0, 5),
        "timestamp_created": datetime.now(),
        "events": []
    }

    # Event data (1-6 events per user)
    for _ in range(random_int_from_interval(1, 6)):
        new_event = {
            "timestamp_event": fake.date_time_this_year(),
            "weight": random_int_from_interval(50, 100),
            "activity": random_choice(['Running', 'Walking', 'Cycling', 'Yoga', 'Gym', 'Swimming']),
            "duration_minutes": random_int_from_interval(10, 120)
        }
        new_user["events"].append(new_event)

    return new_user

def seed_db():
    db = client[database_name]
    collection = db[collection_name]
    
    total_records = 200000
    batch_size = 1000
    total_batches = total_records // batch_size
    
    for batch_num in range(total_batches):
        batch_data = []
        
        # Create batch_size number of users
        for _ in range(batch_size):
            batch_data.append(create_user())
            
        # Insert the batch
        collection.insert_many(batch_data)
        
        # Print progress
        records_inserted = (batch_num + 1) * batch_size
        print(f"Progress: {records_inserted}/{total_records} records inserted ({((records_inserted/total_records)*100):.2f}%)")
    
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_db()
