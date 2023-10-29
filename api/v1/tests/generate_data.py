import random
import uuid
import Faker

fake = Faker()

test_data = []

for i in range(10):  # Создаем 10 тестовых записей
    data = {
        "partner_id": random.randint(1, 100),
        "organization_name": fake.company(),
        "organization_website": fake.url(),
        "organization_description": fake.catch_phrase(),
        "organization_email": fake.company_email(),
        "organization_phone": fake.phone_number(),
        "id": str(uuid.uuid4()),
        "inn": "".join([str(random.randint(0, 9)) for _ in range(10)]),
        "ogrn": "".join([str(random.randint(0, 9)) for _ in range(13)]),
        "kpp": "".join([str(random.randint(0, 9)) for _ in range(9)]),
        "hash_password": fake.password(length=12, special_chars=True,
                                       digits=True, upper_case=True,
                                       lower_case=True),
        "region_id": random.randint(1, 20)
    }
    test_data.append(data)

for item in test_data:
    print(item)
