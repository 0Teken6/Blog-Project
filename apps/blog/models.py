from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    

class Post(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return f'Post: {self.title}'
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Category(BaseModel):
    name = models.CharField(max_length=100)
    

class Tag(BaseModel):
    name = models.CharField(max_length=100)
