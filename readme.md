## A seeder script added to create a sample of Posts along with comments and media attachments.

### Folders

#### seeders 
seeder scripts. it's job is to seed a certain number of posts and for each post it does the follows:
- randomly chooses to attach media files or not with 50% chance for each post. Those media files could be images, or videos
- create a random number of shared posts (from 0 to 3)
- create a random number of comments (from 0 to 10)
- create a random number of reactions for each reaction type (from 0 to 15)

#### spaces 
a sample of the data. It includes:
- the `management` space
- the `core` space that has the `posts` folder (already seeded with 30 posts)

### Steps to run the seeders
1. open `/seeder/main_seeder.py` and set `DMART_URL` and `TOKEN` Values. You can also configure the number of the seeded post in line #9
2. run cd `seeders`
3. run `python main_seeder.py`

