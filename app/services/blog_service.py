from slugify import slugify

from app.dtos.blog import BlogCreate, BlogListResponse
from app.models.post import Post
from app.repositories.blog_repository import BlogRepository
from app.services.category_service import CategoryService
from app.services.tag_service import TagService


class BlogService:
    def __init__(
        self,
        repository: BlogRepository,
        category_service: CategoryService,
        tag_service: TagService,
    ):
        self.repository = repository
        self.category_service = category_service
        self.tag_service = tag_service

    def get_all_posts(self):
        posts = self.repository.get_all()

        return [
            BlogListResponse(
                author=post.author.username,
                category=post.category.name,
                tags=[tag.name for tag in post.tags],
                slug=post.slug,
                title=post.title,
                created_at=post.created_at,
                updated_at=post.updated_at,
            )
            for post in posts
        ]

    def create_post(self, author_id: int, data: BlogCreate):
        category = self.category_service.get_by_name(data.category)
        if category is None:
            category = self.category_service.create(data.category)

        tags = []

        for tag_name in data.tags:
            tag = self.tag_service.get_by_name(tag_name)

            if tag is None:
                tag = self.tag_service.create(tag_name)

            tags.append(tag)

        if data.slug is None:
            data.slug = slugify(data.title)
        else:
            data.slug = slugify(data.slug)

        post = Post(
            author_id=author_id,
            category_id=category.id,
            tags=tags,
            title=data.title,
            content=data.content,
            slug=data.slug,
        )

        self.repository.create(post)

        return BlogListResponse(
            author=post.author.username,
            category=post.category.name,
            tags=[tag.name for tag in post.tags],
            slug=post.slug,
            title=post.title,
            created_at=post.created_at,
            updated_at=post.updated_at,
        )
