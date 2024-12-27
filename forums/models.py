from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Forum(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(4, "Title must be at least 4 characters.")]
    )
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Comment", related_name="forum_comments")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    text = models.TextField(
        validators=[MinLengthValidator(2, "Comment must be at least two characters.")]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="forum_comments_owner")
    forum = models.ForeignKey("Forum", on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + " ..."
