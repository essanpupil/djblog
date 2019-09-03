from django.db import models
from django.utils import timezone
from django.utils.timezone import now


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    publish_date = models.DateTimeField(default=now)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.is_draft:
            self.publish_date = timezone.now()
        
        super(Post, self).save(*args, **kwargs)
