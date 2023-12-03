from factories.post import Post
import requests
from faker import Faker

fake = Faker()


class PostSeeder:
    SPACE_NAME = "core"
    SUBPATH = "posts"

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token

    def post_request_body(self, post_body: dict) -> dict:
        return {
            "space_name": self.SPACE_NAME,
            "request_type": "create",
            "records": [
                {
                    "resource_type": "content",
                    "shortname": "auto",
                    "subpath": self.SUBPATH,
                    "attributes": {
                        "is_active": True,
                        "payload": {
                            "content_type": "json",
                            "schema_shortname": "post",
                            "body": post_body,
                        },
                    },
                }
            ],
        }

    def seed(self, count: int = 10) -> int:
        posts: list = Post.generate(count)
        created_posts_count = 0
        for post in posts:
            req = requests.post(
                url=f"{self.url}/managed/request",
                json=self.post_request_body(post),
                headers={"Authorization": f"Bearer {self.token}"},
            )

            if req.status_code != 200:
                continue

            created_posts_count += 1
            response = req.json()
            original_shortname = response["records"][0]["shortname"]

            # Create the posts which shared this post
            shared_posts = Post.generate(count=post["num_of_shares"], no_shares=True)
            for shared_post in shared_posts:
                created_posts_count += 1
                shared_post["shared_from"] = original_shortname
                shared_req = requests.post(
                    url=f"{self.url}/managed/request",
                    json=self.post_request_body(shared_post),
                    headers={"Authorization": f"Bearer {self.token}"},
                )
                resshared_ponse = shared_req.json()
                shared_shortname = resshared_ponse["records"][0]["shortname"]
                # Create shared post comments
                self.attach_comments(shared_shortname, shared_post["num_of_comments"])

            # Create original post comments
            self.attach_comments(original_shortname, post["num_of_comments"])

        print(f"Created {created_posts_count} post")

    def attach_comments(self, shortname: str, num_of_comments: int):
        for i in range(num_of_comments):
            requests.post(
                url=f"{self.url}/managed/request",
                json={
                    "space_name": self.SPACE_NAME,
                    "request_type": "create",
                    "records": [
                        {
                            "resource_type": "comment",
                            "shortname": "auto",
                            "subpath": f"{self.SUBPATH}/{shortname}",
                            "attributes": {
                                "is_active": True,
                                "body": fake.text(max_nb_chars=100),
                            },
                        }
                    ],
                },
                headers={"Authorization": f"Bearer {self.token}"},
            )
