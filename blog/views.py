from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment, User,UserProfile
from django.utils import timezone
from blog.forms import PostForm, CommentForm, UserForm, UserProfileForm,EditProfileForm

from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django import forms
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class UserPostListView(LoginRequiredMixin,ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).filter(author=self.request.user).order_by('-published_date')

class PostDetailView(DetailView):
        model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    model = Post
    form_class=PostForm
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'





class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

class UserUpdateView(LoginRequiredMixin,UpdateView):


    def get_object(self):
        return self.request.user


class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'

    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).filter(author=self.request.user).order_by('-created_date')


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')



#######################################
## Functions ##
#######################################

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

def searchbar(request):
    if request.method=='GET':
        search=request.GET.get('search')
        post=Post.objects.all().filter(title__icontains=search)
        return render(request,'search.html',{'post':post})

def register(request):
    registered=False

    if request.method=="POST":
        user_form=UserForm(data=request.POST)
        profile_form= UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True

        else:
            print(user_form.errors,profile_form.errors)

    else:
        user_form=UserForm()
        profile_form=UserProfileForm()

    return render(request,'registration/user_registration.html',{'user_form':user_form,'profile_form':profile_form,'registered':registered})


def profile_detail(request):
    user_detail=UserProfile.objects.all()
    my_detail={'user_detail':user_detail}
    return render(request,'registration/profile.html',context=my_detail)

def edit_profile(request):

    if request.method=="POST":
        form=EditProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')

    else:
        form=EditProfileForm(instance=request.user)
        args={'forms':forms}
        return render(request,'registration/edit_profile.html',args)
