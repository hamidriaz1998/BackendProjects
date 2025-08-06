from sqlalchemy.orm import joinedload

from app.db import get_db
from app.models import Category, Post, Tag


def insert_sample_data():
    try:
        db = get_db()

        with next(db) as session:
            rows = [
                Post(
                    title="Sample Post",
                    content="This is a sample post.",
                    category=Category(name="Sample Category"),
                    tags=[Tag(name="sample"), Tag(name="post")],
                ),
                Post(
                    title="Another Sample Post",
                    content="This is another sample post.",
                    category=Category(name="Another Sample Category"),
                    tags=[Tag(name="another"), Tag(name="post")],
                ),
                Post(
                    title="Yet Another Sample Post",
                    content="This is yet another sample post.",
                    category=Category(name="Yet Another Sample Category"),
                    tags=[Tag(name="yet")],
                ),
            ]

            session.add_all(rows)
            session.commit()

    except Exception as e:
        print(f"Error inserting sample data: {e}")


def read_post(id):
    try:
        db = get_db()
        with next(db) as session:
            post = (
                session.query(Post)
                .options(joinedload(Post.category), joinedload(Post.tags))
                .filter(Post.id == id)
                .first()
            )
            # if post:
            #     print(post.title)
            #     print(post.content)
            #     print(post.category.name)
            #     for tag in post.tags:
            #         print(tag.name)
            # else:
            #     print("Post not found")
            return post
    except Exception as e:
        print(f"Error reading post: {e}")
        return None


if __name__ == "__main__":
    post = read_post(1)
    if post:
        print(post.title)
        print(post.content)
        print(post.category.name)
        for tag in post.tags:
            print(tag.name)
