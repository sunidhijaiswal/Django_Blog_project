from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from .models import Post,Comment, Profile
from .forms import PostForm, UserCreateForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import Permission, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from datetime import datetime
import os

# For change Password
from django.contrib.auth import update_session_auth_hash

# decorators
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        post = Post.objects.order_by('-date')
        return render(request, 'home/home.html', {'post': post})
    else:
        messages.error(request, "You are not Authenticated. Please first Sign Up.....!")
        return redirect('/sign_in')


@login_required(login_url='/sign_in')
def post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # uploaded_file = request.FILES['image']
            # print(uploaded_file.name)
            # print(uploaded_file.size)
            if request.FILES:
                form = PostForm(request.POST,  request.FILES)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, 'You share a Post Successfully....')
                        return redirect('/')
                    except:
                        pass
            else:
                form = PostForm(request.POST)
                if form.is_valid():
                    try:
                        form.save()
                        messages.success(request, 'You share a Post Successfully....')
                        return redirect('/')
                    except:
                        pass
        else:
            form = PostForm()
            return render(request, 'post/post.html', {'form': form})
    else:
        messages.success(request, "You are not authenticated to share post . Please first Sign Up.....!")
        return redirect('/sign_in')


@login_required(login_url='/sign_in')
def view_post(request, id):
    post = Post.objects.get(id=id)
    comment = Comment.objects.filter(post_id=id)
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request, 'post/view_post.html', {'post':post, 'comment':comment, 'profile':profile})


@login_required(login_url='/sign_in')
def edit_post(request, id):
    post = Post.objects.get(id=id)
    post.title = request.POST['title']
    post.content = request.POST['content']
    post.auther = request.POST['auther']
    post.save()
    return redirect('/user/profile/'+'|urlencode')


@login_required(login_url='/sign_in')
def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    messages.success(request, 'Post Deleted Successfully...!!!')
    return redirect('/user/profile/' + '|urlencode')


# ============ User Authentication Related Views =========================
def sign_up(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            u = User.objects.get(id=user.id)
            f = Profile(name='',email=u.email,contact=+91,dob=datetime.now(),gender='',pic='/profile/user.png', user=u)
            f.save()
            messages.success(request, 'You Log In. Successfully...')
            return redirect('/')
    else:
        form = UserCreateForm()
    return render(request, 'auth/sign_up.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You Logged In. Successfully...')
            return redirect('/')

    else:
        form = AuthenticationForm()
    return render(request, 'auth/sign_in.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'You are Log Out...')
    return HttpResponseRedirect('/sign_in')


# ==========  Comments View =========================
@login_required(login_url='/sign_in')
def leave_comment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        c = Comment(name=request.POST['name'], email=request.POST['email'],comment=request.POST['comment'],post=post)
        c.save()
        return redirect('/view_post/'+str(id)+'|urlencode[: safe_chars]')

        
@login_required(login_url='/sign_in')
def delete_comment(request, id):
    c = Comment.objects.get(id=id)
    c.delete()
    return redirect('/')


#=========== User Profile, Setting View =========================
@login_required(login_url='/sign_in') 
def profile(request):
    post = Post.objects.filter(user_id=request.user.id)
    profile = Profile.objects.get(user_id = request.user.id)
    return render(request, 'user/profile.html', {'post': post, 'profile':profile})


@login_required(login_url='/sign_in')
def setting(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'user/setting.html')
    

@login_required(login_url='/sign_in')
def edit_profile(request):
    if request.method == 'POST':
        user = Profile.objects.get(user_id=request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Update Your Profile...')

        else:
            messages.error(request, 'Something is Error...!')
    form = ProfileForm()
    details = Profile.objects.get(user_id=request.user.id)
    return render(request, 'user/profile_setting.html', {'form': form, 'detail':details})


@login_required(login_url='/sign_in')
def update_pic(request):
    if request.method == 'POST':
        u = request.FILES['pic']
        print(u.size)
        if u.size <= 500000:
            profile = Profile.objects.get(user_id=request.user.id)
            profile.pic = request.FILES['pic']
            profile.save()
            messages.success(request, 'Successfully Update Your Picture...')
        else:
            messages.error(request, "Sorry..! Image Size Should must be 500kb or less ....!")

    details = Profile.objects.get(user_id=request.user.id)
    return render(request, 'user/change_pic.html',{'detail':details})


# Change Password
@login_required(login_url='/sign_in')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated...!')
            # return redirect('/user/setting/urlencode')
            print("success")
        else:
            print('error')
            messages.error(request, 'Please correct the error below.')
    form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {'form': form})


# Delete User Account
@login_required(login_url='/sign_in')
def delete_account(request):
    post = Post.objects.filter(user_id=request.user.id)
    for p in post:
        c = Comment.objects.filter(post_id=p.id)
        c.delete()
    post.delete()
    user = User.objects.get(id=request.user.id)
    user.delete()
    messages.success(request, 'Your Account Deleted Successfully...!')
    return redirect('/sign_up')


def search_title(request):
    if request.method == 'POST':
        search_text = request.POST['search-text']
        print(search_text)
    else:
        search_text = ''
    posts = Post.objects.filter(title__contains=search_text)
    print(posts)
    return render_to_response('post/search.html', {'posts': posts})