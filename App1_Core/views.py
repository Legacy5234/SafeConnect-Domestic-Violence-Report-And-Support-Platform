from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponse

from . forms import BlogPostForm,EditBlogPostForm,CommentForm,Comment,ReplyForm
from . models import BlogPost,Tags,Reply

# Create your views here.
#---------------------------------------------------------------------------------------------------------
# HOME VIEW
#---------------------------------------------------------------------------------------------------------
def home(request, tag=None):
    if tag:
        post = BlogPost.objects.filter(tags__slug=tag) #Filtering base on the tags 
        tag = get_object_or_404(Tags, slug=tag)
    else:
        post = BlogPost.objects.all()

    paginator = Paginator(post, 2)
    page = int(request.GET.get('page', 1))

    try:
        post = paginator.page(page)
    except:
        return HttpResponse('')

    context = {
        'post': post,
        'tag': tag,

        'page':page
    }

    if request.htmx:
        return render(request, 'partials/loop_home_posts.html', context)
    
    return render(request, 'App1_Core/home.html', context)


#---------------------------------------------------------------------------------------------------------
# POST DETAIL VIEW
#---------------------------------------------------------------------------------------------------------
def post_detail(request, pk):
    post = get_object_or_404(BlogPost, id=pk)

    #Using django_htmx library to get the newest and top comments for the comment tabs
    if request.htmx:
        if 'top' in request.GET:
            #comments = post.comments.filter(likes__isnull=False).distinct()

            # Counting the number of likes a comment has
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        
        return render(request, 'partials/loop_postpage_comments.html', {'comments':comments})

    # Forms
    commentform = CommentForm()
    replyform = ReplyForm()

    context = {
        'post':post,
        'commentform':commentform,
        'replyform':replyform,
    }
    return render(request, 'App1_Core/postdetail.html', context)



#---------------------------------------------------------------------------------------------------------
# CREATE POST VIEW
#---------------------------------------------------------------------------------------------------------
@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            messages.success(request, 'Post Added succesfully..')
            return redirect('App1_Core:home')
    else:
        form = BlogPostForm()
    return render(request, 'App1_Core/createpost.html', {'form': form})

#---------------------------------------------------------------------------------------------------------
# EDIT POST VIEW
#--------------------------------------------------------------------------------------------------------- 
@login_required
def editPost(request, pk):
    post = get_object_or_404(BlogPost, id=pk, author=request.user)

    form = EditBlogPostForm(instance=post)
    if request.method == 'POST':
        form = EditBlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post edited successfully...')
            return redirect('App1_Core:home')
    context = {
        'form':form,
        'post':post
    }
    return render(request, 'App1_Core/editpost.html', context)


#---------------------------------------------------------------------------------------------------------
# DELETE POST VIEW
#--------------------------------------------------------------------------------------------------------- 
@login_required
def delete_post(request, pk):
    post = get_object_or_404(BlogPost, id=pk, author=request.user)

    #Post Delete logic
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully..')
        return redirect('App1_Core:home')

    context = {'post':post}
    return render(request, 'App1_Core/deletepost.html',context)


#---------------------------------------------------------------------------------------------------------
# COMMENT ADD AND DELETE VIEWS
#--------------------------------------------------------------------------------------------------------- 
@login_required
def comment_sent(request, pk):
    post = get_object_or_404(BlogPost, id=pk)

    # Continue display of the form when a reply is made without refreshing the page
    replyform = ReplyForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        'post':post,
        'comments':comment,
        'replyform':replyform,
    }
    return render(request, 'partials/add_comment.html', context)


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'comment deleted successfully..')
        return redirect('App1_Core:post-detail', comment.parent_post.id)
    
    return render(request, 'App1_Core/comment-delete.html', {'comments':comment})


#---------------------------------------------------------------------------------------------------------
# REPLY ADD AND DELETE VIEWS
#---------------------------------------------------------------------------------------------------------
@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    # Continue display of the form when a reply is made without refreshing the page
    replyform = ReplyForm()

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'comments':comment,
        'reply': reply,
        'replyform':replyform,
    }
    return render(request, 'partials/add_reply.html', context)


@login_required
def reply_delete(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted..')
        return redirect('App1_Core:post-detail', reply.parent_comment.parent_post.id)
    
    return render(request, 'App1_Core/reply-delete.html', {'reply':reply})



#---------------------------------------------------------------------------------------------------------
# DRY-DO NOT REPEAT YOURSELF ON LIKE-POST,COMMENT-LIKE AND REPLY-LIKE USING DECORATORS
#---------------------------------------------------------------------------------------------------------
""" This decorator function is made up of three nested function, the outer[args],inner[func] 
    and wrapper[logic],which at the end is injected into the original function.

    OUTER FUNCTION[args] : This is an optional layer,it is only required if additional arguments are needed such as the model
    class in this case

    INNER FUNCTION[func] : This function takes the original function and retrives it's information such as the request object,
    the user id and the post id

    WRAPPER[logic] : The data from the outer and inner function are passed to the wrapper function which also consists of the 
    logic.Once the logic is processed,it returns the result to the original function which then itself returns the final output.
"""

def like_toggle(model): # Outer function Decorator
    def inner_func(func):# Inner function with the original function as it's argument
        def wrapper(request, *args, **kwargs): # Wrapper function with all the data from the outer and inner function

            # The Logic
            post = get_object_or_404(model, id=kwargs.get('pk'))
            #Checking to see if a user already liked a post
            if post.author != request.user: #To ensure no author of a post can like his or her own post
                if request.user in post.likes.all():
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)

            return func(request, post) # Returning back to the wrapper function
        return wrapper # Returning back to the original function
    return inner_func 

# The original function - The Post model
@login_required
@like_toggle(BlogPost)
def like_post(request, post):
    return render(request, 'partials/likes.html', {'post':post})

# The original function - The Comment model
@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'partials/likes_comment.html', {'comments':post})

# The original function - The Reply model
@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'partials/likes_reply.html', {'reply':post})