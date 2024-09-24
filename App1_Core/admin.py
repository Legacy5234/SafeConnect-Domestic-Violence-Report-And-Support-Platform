from django.contrib import admin
from . models import BlogPost,Tags,Comment,Reply,LikedPost,LikedComment,LikedReply

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Tags, TagAdmin)


admin.site.register(LikedPost)
admin.site.register(LikedComment)
admin.site.register(LikedReply)

