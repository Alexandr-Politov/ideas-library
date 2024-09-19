from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    occupation = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return (f"{self.username}: ({self.first_name} "
                f"{self.last_name} from {self.occupation})")


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Idea(models.Model):
    DIFFICULTY = [("Hard", "Hard"), ("Medium", "Medium"),("Easy", "Easy")]

    name = models.CharField(max_length=255, unique=True)
    diagram = models.ImageField(upload_to="diagrams/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.CharField(max_length=6, choices=DIFFICULTY)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ideas"
    )
    categories = models.ManyToManyField(
        Category,
        related_name="ideas",
        blank=True
    )


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    class Meta:
        ordering = ['-created_at']
