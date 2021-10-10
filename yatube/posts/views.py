from django.http.response import Http404
from .models import Post, Group, Follow
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from Users.models import UserProfile
from . import services
User = get_user_model()


# @cache_page(20, key_prefix='index_page')
def index(request):
    """Displaying the index page"""
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'index.html',
        {'page': page, 'paginator': paginator}
    )


@login_required()
def new_post(request):
    """The new post publication"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('/')
    return render(request, 'new.html', {'form': form})


def group_posts(request, slug):
    """Displaying a posts of the certain group"""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        "group.html",
        {
            "group": group,
            "page": page,
            'paginator': paginator
        }
        )


@login_required()
def profile(request, username):
    """Displaying the profile page"""
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
    except Exception:
        pass
    following = services.is_following(request, author)
    return render(
        request,
        'profile.html',
        {
            "page": page,
            "paginator": paginator,
            'author': author,
            'following': following,
            'img': img,
            'podpisok': podpisok,
            'podpisan': podpisan
        }
        )


def post_view(request, username, post_id):
    """Displaying the entire post"""
    for author in User.objects.all():
        if author.username == username:
            post = get_object_or_404(Post, id=post_id)
            items = post.comment.all().order_by('created')
            form = CommentForm(request.POST or None)
            paginator = Paginator(items, 10)
            page_number = request.GET.get('page')
            page = paginator.get_page(page_number)
            return render(
                request,
                'post.html',
                {
                    'post': post,
                    'paginator': paginator,
                    'page': page,
                    'form': form,
                    'author': author,
                    'items': items,
                }
                )
    raise Http404


@login_required()
def post_edit(request, username, post_id):
    """Editing the post"""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if request.user.username != post.author.username:
        return redirect('post', username=username, post_id=post_id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
        )
    if form.is_valid():
        form.save()
        return redirect('post', username=username, post_id=post_id)
    return render(
        request,
        "new.html",
        {
            'form': form,
            'edit': True,
            'post': post
        }
        )


def page_not_found(request, exception):
    """404 error template"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """500 error template"""
    return render(request, "misc/500.html", status=500)


@login_required()
def add_comment(request, username, post_id):
    """Adding comment"""
    post = Post.objects.get(id=post_id)
    form = CommentForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
        return redirect('post', username=username, post_id=post_id)
    return redirect('post', username=username, post_id=post_id)


@login_required()
def follow_feed(request):
    """Displaying the follow feed"""
    posts = Post.objects.filter(
        author__following__in=Follow.objects.filter(user=request.user)
        )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    empty = services.is_empty(page)
    return render(
        request, 'follow.html',
        {
            'page': page,
            'paginator': paginator,
            'empty': empty
        }
        )


@login_required()
def profile_follow(request, username):
    """Following the profile"""
    if request.user.username == username:
        return redirect('profile', username=username)
    author = User.objects.get(username=username)
    if Follow.objects.filter(
            user=request.user,
            author=User.objects.get(username=username)
            ):
        return redirect('profile', username=username)
    Follow.objects.create(user=request.user, author=author)
    return redirect('profile', username=username)


@login_required()
def profile_unfollow(request, username):
    """Unfollowing the profile"""
    if not Follow.objects.filter(
            user=request.user,
            author=User.objects.get(username=username)
            ):
        return redirect('profile', username=username)
    author = User.objects.get(username=username)
    Follow.objects.get(user=request.user, author=author).delete()
    return redirect('profile', username=username)
