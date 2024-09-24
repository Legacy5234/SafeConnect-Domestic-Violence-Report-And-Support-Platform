from django import forms
from .models import BlogPost,Comment,Reply

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'cover_image', 'content', 'is_anonymous','tags']

        labels = {
            'content': 'Post',
            'is_anonymous': 'Make Me Anonymous',
            'cover_image': 'Cover Image',
            'tags': 'Category'
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'input font1 text-4xl'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write Post...', 'class': 'textarea text-light'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'file-input'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'tags': forms.CheckboxSelectMultiple(),
        }



class EditBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'cover_image', 'content', 'is_anonymous', 'tags']
        
        labels = {
            'content': 'Post',
            'is_anonymous': 'Make Me Anonymous',
            'cover_image': 'Cover Image',
            'tags': 'Category'
        }
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'class': 'input font1 text-4xl'}),
            'content': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Write Post...', 'class': 'textarea text-light'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'file-input', 'initial_text': '', 'input_text': 'Change'}),
            'is_anonymous': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'tags': forms.CheckboxSelectMultiple(),
        }



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add comment..'}),
        }
        labels = {
            'body': '',
        }



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['body']
        widgets = {
            'body': forms.TextInput(attrs={'placeholder': 'Add reply..', 'class':"!text-sm"}),
        }
        labels = {
            'body': '',
        }