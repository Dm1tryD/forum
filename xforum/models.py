from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug+'-'+str(int(time()))

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="author")
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    img = models.ImageField(null=True, upload_to='images',blank=True)
    body = RichTextField(blank=True, db_index=True,null=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    date_pub = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True, null=True)

    def get_absolute_url(self):
        """Returns the generated url link"""
        return reverse('post_detail_url',kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']

class Tag(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="tag_author")
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50,unique=True)

    def get_absolute_url(self):
        """Returns the generated url link"""
        return reverse('tag_detail_url', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug':self.slug})

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, verbose_name="post", related_name="comments_post")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="comment author")
    date_create = models.DateTimeField(auto_now_add=True)
    comment_text = models.TextField()

    class Meta:
        ordering = ['-date_create']