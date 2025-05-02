from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.user.username)
        return super(Profile, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.user.first_name

    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    view_count = models.IntegerField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    bookmarks =models.ManyToManyField(User, related_name="bookmarks", default=None, blank=True)
    likes = models.ManyToManyField(User, related_name="likes", default=None, blank=True)
    
    def like_count(self):
        return self.likes.count
    
    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField()
    date= models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='replies')



class WebsiteMeta(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    about = models.TextField()