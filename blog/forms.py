from django import forms
from django.contrib.auth.models import User
from .models import Post,Comment,UserProfile

class PostForm(forms.ModelForm):

    class Meta:
        model=Post


        fields=('author','title','text')



        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'postcontent'}),
            #'author': forms.CharField(),
        }


class CommentForm(forms.ModelForm):

    class Meta():
        model=Comment
        fields=('author', 'text')

    widgets={
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'postcontent'}),
    }




class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=('username','first_name','last_name','email','password')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model=UserProfile
        fields=('portfolio_site','profile_pic')

class EditProfileForm(UserForm):
    class Meta():
        model=User
        fields=('first_name','last_name','email','password')
