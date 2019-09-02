from django.db import models
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateTimeField()
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.is_draft:
            self.publish_date = timezone.now()
        
        super(Post, self).save(*args, **kwargs)
