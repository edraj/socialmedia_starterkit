from faker import Faker

fake = Faker()


class Post:
    @staticmethod
    def generate(count: int, no_shares: bool = False) -> list[dict]:
        models: list[dict] = []
        for i in range(count):
            models.append(
                {
                    "content": fake.text(max_nb_chars=500),
                    "reacts": {
                        "like": fake.random_int(min=50, max=99999),
                        "laughing": fake.random_int(min=50, max=99999),
                        "love": fake.random_int(min=50, max=99999),
                        "care": fake.random_int(min=50, max=99999),
                        "sad": fake.random_int(min=50, max=99999),
                    },
                    "num_of_shares": fake.random_int(min=0, max=3)
                    if not no_shares
                    else 0,
                    "num_of_comments": fake.random_int(min=0, max=10),
                }
            )

        return models
