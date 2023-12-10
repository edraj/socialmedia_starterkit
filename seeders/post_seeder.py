import io
import json
from factories.post import Post
import requests
from faker import Faker

fake = Faker()


class PostSeeder:
    SPACE_NAME = "core"
    SUBPATH = "posts"
    ATTACHMENTS = [
        ("sample.mp4", "video/mp4"),
        ("sample2.mp4", "video/mp4"),
        ("sample1.jpeg", "image/jpeg"),
        ("sample2.jpeg", "image/jpeg"),
        ("sample3.jpg", "image/jpg"),
    ]

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

    def create_shares(self, original_post: dict):
        # TODO: Create a Share attachment under the original post. Using /public/submit API 
        # TODO: Create a shared post.
        # TODO: Create a Relationship attachment under the shared post that refers to the original post. Using /public/submit API 
        # shared_posts = Post.generate(
        #     count=original_post["num_of_shares"], no_shares=True
        # )
        # for shared_post in shared_posts:
        #     shared_post["is_shared"] = True
        #     shared_req = requests.post(
        #         url=f"{self.url}/managed/request",
        #         json=self.post_request_body(shared_post),
        #         headers={"Authorization": f"Bearer {self.token}"},
        #     )
        #     # Create shared post comments
        #     shared_shortname = shared_req.json()["records"][0]["shortname"]
        #     self.attach_comments(
        #         shared_shortname,
        #         shared_post["num_of_comments"],
        #     )
        #     # Create shared post reactions
        #     self.attach_reactions(
        #         shared_shortname,
        #         shared_post["reacts"],
        #     )
        pass

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
            original_shortname = req.json()["records"][0]["shortname"]

            # Create the posts that shares this post
            self.create_shares(post)
            created_posts_count += post["num_of_shares"]

            # Create original post comments
            self.attach_comments(original_shortname, post["num_of_comments"])

            # Create original post reactions
            self.attach_reactions(
                original_shortname,
                post["reacts"],
            )

            # Randomly attach media
            if fake.random_element(elements=[1, 0, 0]):
                self.attach_media(original_shortname)

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

    def attach_reactions(self, shortname: str, reactions: dict[str, int]):
        for type, count in reactions.items():
            for i in range(count):
                requests.post(
                    url=f"{self.url}/managed/request",
                    json={
                        "space_name": self.SPACE_NAME,
                        "request_type": "create",
                        "records": [
                            {
                                "resource_type": "reaction",
                                "shortname": "auto",
                                "subpath": f"{self.SUBPATH}/{shortname}",
                                "attributes": {
                                    "is_active": True,
                                    "type": type,
                                },
                            }
                        ],
                    },
                    headers={"Authorization": f"Bearer {self.token}"},
                )

    def attach_media(self, shortname: str):
        for _ in range(fake.random_int(min=1, max=5)):
            request_file = io.StringIO(
                json.dumps(
                    {
                        "resource_type": "media",
                        "shortname": "auto",
                        "subpath": f"{self.SUBPATH}/{shortname}",
                        "attributes": {"is_active": True},
                    }
                )
            )
            attachment = fake.random_element(self.ATTACHMENTS)
            media_file = open(f"data/{attachment[0]}", "rb")
            files = {
                "request_record": ("record.json", request_file, "application/json"),
                "payload_file": (
                    media_file.name.split("/")[-1],
                    media_file,
                    attachment[1],
                ),
            }
            requests.post(
                url=f"{self.url}/managed/resource_with_payload",
                headers={"Authorization": f"Bearer {self.token}"},
                data={"space_name": self.SPACE_NAME},
                files=files,
            )
