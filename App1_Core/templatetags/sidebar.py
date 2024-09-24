from django.template import Library
from ..models import Tags,BlogPost,Comment

from django.db.models import Count

register = Library()

@register.inclusion_tag('includes/sidebar.html')
def sidebar_view(tag=None, user=None):
    categories = Tags.objects.all()

    # Getting the posts and comments with high number of likes
    top_post = BlogPost.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
    top_comment = Comment.objects.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')


    context = {
        'categories':categories,
        'tag': tag,
        'top_post': top_post,
        'top_comment': top_comment,
        'user':user
    }
    return context