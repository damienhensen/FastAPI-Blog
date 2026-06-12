from app.dtos.blog import BlogListResponse
from app.repositories.blog_repository import BlogRepository


class BlogService:
    def __init__(self, repository: BlogRepository):
        self.repository = repository

    def get_all_posts(self):
        posts = self.repository.get_all()

        return [
            BlogListResponse(
                author=post.author.username,
                category=post.category.name,
                tags=[tag.name for tag in post.tags],
                slug=post.slug,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]
