from django.db import models
from config.settings import AUTH_USER_MODEL


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='posts')
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')

    def __str__(self):
        return f'Post: {self.title}'


class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} Category'
    

class Tag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} Tag'