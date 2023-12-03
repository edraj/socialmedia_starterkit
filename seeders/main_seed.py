from post_seeder import PostSeeder

DMART_URL = "http://0.0.0.0:8282"
TOKEN = ""


if __name__ == "__main__":
    post_seeder = PostSeeder(DMART_URL, TOKEN)
    post_seeder.seed(10)
