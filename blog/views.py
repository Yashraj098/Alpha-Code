from time import timezone
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Blog
from .forms import BlogForm

def home(request):
    return render(request, 'blog/home.html')

def signupuser(request):
    if request.method=='GET':
        return render(request, 'blog/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(home)
            except IntegrityError:
                return render(request, 'blog/signupuser.html', {'form': UserCreationForm(), 'error':"Username already taken"})

        else:
            return render(request, 'blog/signupuser.html', {'form': UserCreationForm(), 'error':"Passwords didn't match"})


def loginuser(request):
    if request.method=='GET':
        return render(request, 'blog/loginuser.html', {'form': AuthenticationForm()})
    else:
        user=authenticate(request, username=request.POST['username'] ,password=request.POST['password'])
        if user is None:
            return render(request, 'blog/loginuser.html', {'form': AuthenticationForm(),'error':"Passwords didn't match"})
        else:
            login(request, user)
            return redirect(home)

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect(home)
def all_blogs(request):
    blogs= Blog.objects.order_by('-date')
    return render(request, 'blog/all_blogs.html', {'blogs':blogs})

def detail(request, blog_id):
    blog= get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog/detail.html',{'blog':blog})

def createblog(request):
    if request.method=='GET':
        return render(request, 'blog/createblog.html',{'form':BlogForm()})
    else:
        try:
            form=BlogForm(request.POST)
            newblog=form.save(commit=False)
            newblog.user=request.user
            newblog.save()
            return redirect(yourblog)
        except ValueError:
            return render(request,'blog/createblog.html',{'form':BlogForm(),'error':"Bad Data Passed. Try Again"})

@login_required
def viewblog(request, blog_pk):
    blog= get_object_or_404(Blog, pk=blog_pk, user=request.user)
    if request.method=='GET':
        form= BlogForm(instance=blog)
        return render(request, 'blog/viewblog.html', {'blog': blog,'form': form})
    else:
        try:
            form= BlogForm(request.POST, instance=blog)
            form.save()
            return redirect(yourblog)
        except ValueError:
            return render(request, 'todo/viewblog.html', {'blog': blog,'form': form, 'error':"Bad info"})

@login_required
def yourblog(request):
    blogs= Blog.objects.filter(user=request.user)
    return render(request, 'blog/yourblog.html', {'blogs': blogs})

@login_required
def deleteblog(request,blog_pk):
    blog=get_object_or_404(Blog,pk=blog_pk,user=request.user)
    if request.method=='POST':
        blog.delete()
        return redirect(yourblog)
