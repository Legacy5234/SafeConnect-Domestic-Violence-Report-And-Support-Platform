from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.db.models import Count

from . forms import ProfileForm
from App1_Core.forms import ReplyForm

# Create your views here.
#---------------------------------------------------------------------------------------------------------
# USER-PROFILE VIEW
#---------------------------------------------------------------------------------------------------------
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        profile = request.user.profile

    post = profile.user.blogpost.all()

    if request.htmx:
        if 'toppost' in request.GET:
            post = profile.user.blogpost.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            
        elif 'topcomment' in request.GET:
            comments = profile.user.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
            replyform = ReplyForm()

            return render(request, 'partials/loop_profile_comments.html', {'comments':comments, 'replyform':replyform})
        
        elif 'likedpost' in request.GET:
            post = profile.user.likedposts.order_by('-likedpost__created')

        return render(request, 'partials/loop_profile_posts.html', {'post':post})

    context = {
        'profile':profile,
        'post':post,
    }
    return render(request, 'App2_AccountApp/profile.html', context)


#---------------------------------------------------------------------------------------------------------
# USER PROFILE EDIT
#---------------------------------------------------------------------------------------------------------
@login_required
def profile_edit(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('App2_AccountApp:profile')
    context = {
        'form':form,
    }
    return render(request, 'App2_AccountApp/profile_edit.html', context)

#---------------------------------------------------------------------------------------------------------
# DELETE USER ACCOUNT
#---------------------------------------------------------------------------------------------------------
@login_required
def delete_account(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Account Deleted.. Sad to see you go..')
        return redirect('App1_Core:home')
    return render(request, 'App2_AccountApp/delete-user.html')
