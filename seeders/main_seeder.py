from post_seeder import PostSeeder

DMART_URL = "http://0.0.0.0:8282"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InVzZXJuYW1lIjoiZG1hcnQifSwiZXhwaXJlcyI6MTcwNDIwMzMzMy45ODIwMDh9.SeDgWXrt2kTEJK6egUBEIVdqy-tG9yVjvDawcqECuEU"


if __name__ == "__main__":
    post_seeder = PostSeeder(DMART_URL, TOKEN)
    post_seeder.seed(1)
