from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from blog.models import Post, Comment, User,UserProfile
from django.utils import timezone
from blog.forms import PostForm, CommentForm, UserForm, UserProfileForm, EditProfileForm, EditProfileFormTwo
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
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

#class CreatePostView(LoginRequiredMixin,CreateView):
    #login_url = '/login/'
    #redirect_field_name = 'blog/post_detail.html'

    #form_class = PostForm
    #tance.author=request.user
    #instance.save()
    #del = Post
@login_required
def CreatePostView(request):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model=Post
    form = PostForm()
    if request.method == "POST":
        form= PostForm(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.author=request.user
            instance.save()
            #return reverse("post_detail",kwargs={'pk':self.pk})
            #return redirect('/post_detail/')

    else:
        form = PostForm()
    return render(request , "blog/post_form.html" , {"form":form})



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
        form_one=EditProfileForm(request.POST,instance=request.user)

        form_two=EditProfileFormTwo(request.POST,instance=request.user.userprofile)
        if form_one.is_valid() and form_two.is_valid():
            user=form_one.save()

            user.save()

            profile=form_two.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()
            #update_session_auth_hash(request,form_pass.user)

            return redirect('/profile_details/')
    else:
        form_one=EditProfileForm(instance=request.user)

        form_two=EditProfileFormTwo(instance=request.user.userprofile)
        args={'form_one':form_one,'form_two':form_two}
        return render(request,'registration/edit_profile.html',args)

def edit_password(request):
    if request.method=="POST":
        form_pass=PasswordChangeForm(data=request.POST,user=request.user)
        if form_pass.is_valid():
            form_pass.save()
            update_session_auth_hash(request,form_pass.user)
            return redirect('/profile_details/')
        else:
            form_pass=PasswordChangeForm(user=request.user)
            args={'form_pass':form_pass}
            return render(request,'registration/edit_password.html',args)

    else:
        form_pass=PasswordChangeForm(user=request.user)
        args={'form_pass':form_pass}
        return render(request,'registration/edit_password.html',args)
