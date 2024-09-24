from django.db import models
import uuid
from shortuuid.django_fields import ShortUUIDField

from django.contrib.auth.models import User

# Create your models here.
#---------------------------------------------------------------------------------------------------------
# POST MODEL CLASS
#---------------------------------------------------------------------------------------------------------
class BlogPost(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    post_id = ShortUUIDField(unique=True, length=12, max_length=20, prefix="post", alphabet="abcdefgh1267")
    title = models.CharField(max_length=150)
    cover_image = models.ImageField(upload_to='post_images')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='blogpost')
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    # AUXILLIARY ATTRIBUTES
    tags = models.ManyToManyField('Tags')
    likes = models.ManyToManyField(User, related_name='likedposts', through='LikedPost')

    def __str__(self):
        return str(self.title)
    
    class Meta:
        ordering = ['-created_at']
#---------------------------------------------------------------------------------------------------------
# LIKED-POST MODEL CLASS-THROUGH TABLE
#---------------------------------------------------------------------------------------------------------
class LikedPost(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.post.title}'
    



#---------------------------------------------------------------------------------------------------------
# TAGS/CATEGORY MODEL CLASS
#---------------------------------------------------------------------------------------------------------
class Tags(models.Model):
    name = models.CharField(max_length=50)
    image = models.FileField(upload_to='icons/', null=True, blank=True)
    slug = models.SlugField(max_length=20, unique=True)
    category_ordering = models.IntegerField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Tags'
        ordering = ['category_ordering']


#---------------------------------------------------------------------------------------------------------
# COMMENT MODEL CLASS
#---------------------------------------------------------------------------------------------------------
class Comment(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    comment_id = ShortUUIDField(unique=True, length=15, max_length=22, prefix="comment", alphabet="abcdefgh1267")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comments')
    parent_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)
    
    # AUXILLIARY ATTRIBUTES
    likes = models.ManyToManyField(User, related_name='likedcomments', through='LikedComment')

    def __str__(self):
        try:
            return f'{self.author.username}  : {self.body[:30]}'
        except:
            return f'No Author : {self.body[:30]}'
        
    class Meta:
        ordering = ['-created'] 


#---------------------------------------------------------------------------------------------------------
# LIKED-COMMENT MODEL CLASS-THROUGH TABLE
#---------------------------------------------------------------------------------------------------------
class LikedComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} : {self.comment.body[:30]}'
    
    class Meta:
        ordering = ['-created']



#---------------------------------------------------------------------------------------------------------
# REPLY-COMMENT MODEL CLASS
#---------------------------------------------------------------------------------------------------------
class Reply(models.Model):
    id = models.CharField(max_length=100, default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    reply_id = ShortUUIDField(unique=True, length=15, max_length=20, prefix="reply", alphabet="abcdefgh1267")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='replies', null=True)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, related_name='replies')
    body = models.CharField(max_length=150)
    created = models.DateTimeField(auto_now_add=True)

    # AUXILLIARY ATTRIBUTES
    likes = models.ManyToManyField(User, related_name='likedreplies', through='LikedReply')
    
    def __str__(self):
        try:
            return f'{self.author.username}  : {self.body[:30]}'
        except:
            return f'No Author : {self.body[:30]}'
        
    class Meta:
        verbose_name_plural = 'Replies'
        ordering = ['-created']


#---------------------------------------------------------------------------------------------------------
# REPLY-COMMENT MODEL CLASS-THROUGH TABLE
#---------------------------------------------------------------------------------------------------------
class LikedReply(models.Model):
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.reply.body[:30]}'
    
    class Meta:
        ordering = ['-created']