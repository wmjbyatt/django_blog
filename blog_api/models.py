from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    VISIBILITY_OPTIONS = (
      ('PU', 'Public'),
      ('PR', 'Private'),
      ('DR', 'Draft')
    )

    published_date = models.DateTimeField('date published')
    title = models.TextField()
    user = models.ForeignKey(User, related_name='posts')
    visibility = models.CharField(max_length=2, choices=VISIBILITY_OPTIONS)
    # This should be a TextField. Not sure why it isn't working.
    body = models.CharField(max_length = 100000)
    
    class Meta:
      ordering = ["-published_date"]
    
    def __unicode__(self):
      return self.id
