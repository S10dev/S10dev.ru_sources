from django.http import HttpResponse
from .models import Post, Group, Comment, Follow
from django.shortcuts import render, get_object_or_404, redirect
import datetime as dt
from django.core.mail import send_mail
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from Users.models import UserProfile
from django.http import Http404
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.core.cache import cache
import requests
# Create your views here.
User = get_user_model()


# @cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )

@login_required()
def new_post(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('/')
    return render(request,"new.html", {'form': form})


def group_posts(request, slug):
    if slug == '404':
        group = None  
    else:
        group = get_object_or_404(Group, slug = slug) 
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html",{"group": group, "page": page, 'paginator':paginator})
    

@login_required()
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    podpisan = Follow.objects.filter(user=author).count()
    podpisok = Follow.objects.filter(author=author).count()
    img = None
    try:
        img = UserProfile.objects.get(user=author).avatar
    except Exception as e:
        print(e)
    following = False
    if Follow.objects.filter(user = request.user, author = author):
        following = True
    return render(request, 'profile.html', {"page":page, "paginator": paginator,
        'author': author, 'following': following, 'img': img, 'podpisok': podpisok,
        'podpisan': podpisan})


def post_view(request, username, post_id):
    for author in User.objects.all():
        if author.username == username:
            post = get_object_or_404(Post, id = post_id)
            items = post.comment.all().order_by('created')
            form = CommentForm(request.POST or None)
            paginator = Paginator(items, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            podpisan = Follow.objects.filter(user=author).count()
            podpisok = Follow.objects.filter(author=author).count()
            return render(request, 'post.html', {'post':post, "paginator": paginator, 'page':page,
                'form':form, 'author':author, 'items':items, 'podpisok': podpisok,
                'podpisan': podpisan})
    raise Http404


@login_required()
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id = post_id, author__username = username)
    if request.user.username != post.author.username:
        return redirect('post', username = username, post_id = post_id)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username = username, post_id = post_id)
    return render(request,"new.html", {'form': form, 'edit': True, 'post':post})


def page_not_found(request, exception):
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required()
def add_comment(request, username, post_id):
    post = Post.objects.get(id = post_id)
    form = CommentForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
        return redirect('post', username=username, post_id=post_id)
    return redirect('post', username=username, post_id=post_id)


@login_required()
def follow_index(request):
    posts = Post.objects.filter(author__following__in=Follow.objects.filter(user=request.user))

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    empty=False
    if len(page.object_list)==0:
        empty=True
    return render(request,'follow.html', {'page': page, 'paginator': paginator, 'followid':True, 'empty':empty})


@login_required()
def profile_follow(request, username):
    if request.user.username == username:
        return redirect('profile', username=username)
    author = User.objects.get(username=username)
    if Follow.objects.filter(user=request.user, author=User.objects.get(username = username)):
        return redirect('profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required()
def profile_unfollow(request, username):
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=username)
    
    
def online(request):
    response = requests.get('https://api.vk.com/method/users.get?user_ids=436744680&access_token=9a3dda559a3dda559a3dda55959a4b105599a3d9a3dda55fa7b6f3497c0cb0b0d50ec72&fields=online&v=5.130')
    return HttpResponse(response.json()['response'][0]['online'])

